from __future__ import annotations
import numpy as np
import pandas as pd


def evaluate_schedule(services: pd.DataFrame) -> dict:
    df = services.copy()
    if 'adapted_start_min' in df.columns:
        start_col = 'adapted_start_min'
    else:
        start_col = 'planned_start_min'
    df['completion_min'] = df[start_col] + df['service_duration_min']
    patient_group = df.groupby('patient_id')
    arrival = patient_group[start_col].min()
    completion = patient_group['completion_min'].max()
    total_time = (completion - arrival).mean()
    waiting = np.maximum(0, df[start_col] - df.groupby('patient_id')[start_col].transform('min')).mean()
    station_load = df.groupby('station_id')['service_duration_min'].sum()
    resource_load = df.groupby('resource_id')['service_duration_min'].sum()
    return {
        'patient_waiting_time': float(waiting),
        'total_time_in_system': float(total_time),
        'resource_utilization_balance': float(station_load.var() / (station_load.mean() + 1e-9)),
        'staff_workload_equity': float(resource_load.var() / (resource_load.mean() + 1e-9)),
        'num_services': int(len(df))
    }
