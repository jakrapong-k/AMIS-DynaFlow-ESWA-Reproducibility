#!/usr/bin/env python
from pathlib import Path
import argparse, subprocess, sys
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('--config', default='configs/experiment_main.yaml')
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
steps = [
    ['python', 'scripts/generate_synthetic_data.py', '--config', args.config],
    ['python', 'scripts/preprocess_data.py', '--config', args.config],
    ['python', 'scripts/train_tft.py', '--config', 'configs/tft.yaml'],
    ['python', 'scripts/run_qi_moga.py', '--config', 'configs/qi_moga.yaml'],
    ['python', 'scripts/train_gat_mappo.py', '--config', 'configs/gat_mappo.yaml'],
    ['python', 'scripts/evaluate_baselines.py', '--config', args.config],
]
for step in steps:
    subprocess.run(step, cwd=root, check=True)
summary = pd.read_csv(root / 'results/sample_outputs/evaluation_summary.csv')
summary.to_csv(root / 'results/sample_outputs/reproduction_summary.csv', index=False)
print(summary)
