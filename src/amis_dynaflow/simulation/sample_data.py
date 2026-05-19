from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd


def generate_sample_data(num_patients: int, num_stations: int, seed: int, output_dir: str | Path) -> None:
    rng = np.random.default_rng(seed)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    pathway_templates = []
    for pid in range(1, 9):
        length = int(rng.integers(3, 7))
        seq = rng.choice(np.arange(1, num_stations + 1), size=length, replace=False).tolist()
        pathway_templates.append({
            'pathway_id': f'P{pid:02d}',
            'station_sequence': '>'.join(map(str, seq)),
            'clinical_group': rng.choice(['consultation', 'chemotherapy', 'radiology', 'follow_up'])
        })
    pathways = pd.DataFrame(pathway_templates)

    patients = pd.DataFrame({
        'patient_id': [f'P{i:06d}' for i in range(1, num_patients + 1)],
        'arrival_time_min': np.clip(rng.normal(180, 90, num_patients).astype(int), 0, 479),
        'pathway_id': rng.choice(pathways['pathway_id'], size=num_patients),
        'acuity_level': rng.integers(1, 6, num_patients),
        'no_show_probability': rng.uniform(0.10, 0.15, num_patients).round(4),
        'emergency_flag': rng.binomial(1, 0.035, num_patients)
    })

    resources = []
    resource_types = ['staff', 'equipment', 'room']
    for station_id in range(1, num_stations + 1):
        for k in range(int(rng.integers(1, 4))):
            resources.append({
                'resource_id': f'R{station_id:02d}_{k+1}',
                'station_id': station_id,
                'capacity': int(rng.integers(1, 4)),
                'resource_type': resource_types[k % len(resource_types)]
            })
    resources = pd.DataFrame(resources)

    service_rows = []
    pathway_lookup = dict(zip(pathways['pathway_id'], pathways['station_sequence']))
    for _, p in patients.iterrows():
        stations = [int(s) for s in pathway_lookup[p['pathway_id']].split('>')]
        current = int(p['arrival_time_min'])
        for order, station_id in enumerate(stations, start=1):
            duration = int(max(5, rng.gamma(shape=2.2 + 0.25 * p['acuity_level'], scale=9.0)))
            resource_pool = resources[resources['station_id'] == station_id]['resource_id'].tolist()
            resource_id = rng.choice(resource_pool) if resource_pool else f'R{station_id:02d}_1'
            service_rows.append({
                'patient_id': p['patient_id'],
                'station_id': station_id,
                'sequence_order': order,
                'planned_start_min': current,
                'service_duration_min': duration,
                'resource_id': resource_id
            })
            current += duration + int(rng.integers(5, 25))
    services = pd.DataFrame(service_rows)

    patients.to_csv(output_dir / 'sample_patients.csv', index=False)
    pathways.to_csv(output_dir / 'sample_pathways.csv', index=False)
    resources.to_csv(output_dir / 'sample_resources.csv', index=False)
    services.to_csv(output_dir / 'sample_services.csv', index=False)
