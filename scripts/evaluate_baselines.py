#!/usr/bin/env python
from pathlib import Path
import argparse, sys
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from amis_dynaflow.utils.io import load_yaml, ensure_dir
from amis_dynaflow.simulation.metrics import evaluate_schedule

parser = argparse.ArgumentParser()
parser.add_argument('--config', default='configs/experiment_main.yaml')
args = parser.parse_args()
cfg = load_yaml(args.config)
out = ensure_dir(cfg['experiment']['output_dir'])
base = pd.read_csv(Path(cfg['paths']['processed_dir']) / 'services_processed.csv')
adapted_path = Path(out) / 'gat_mappo_adapted_schedule.csv'
adapted = pd.read_csv(adapted_path) if adapted_path.exists() else base.copy()
rows = []
for name, df in [('synthetic_current_practice', base), ('amis_dynaflow_public_workflow', adapted)]:
    metrics = evaluate_schedule(df)
    metrics['configuration'] = name
    rows.append(metrics)
pd.DataFrame(rows).to_csv(Path(out) / 'evaluation_summary.csv', index=False)
print('Evaluation summary written.')
