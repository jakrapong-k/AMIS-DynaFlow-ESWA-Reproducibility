#!/usr/bin/env python
from pathlib import Path
import argparse, sys
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from amis_dynaflow.utils.io import load_yaml, ensure_dir

parser = argparse.ArgumentParser()
parser.add_argument('--config', default='configs/experiment_main.yaml')
args = parser.parse_args()
cfg = load_yaml(args.config)
syn = Path(cfg['paths']['synthetic_dir'])
out = ensure_dir(cfg['paths']['processed_dir'])
patients = pd.read_csv(syn / 'synthetic_patients.csv')
services = pd.read_csv(syn / 'synthetic_services.csv')
services = services.merge(patients[['patient_id','arrival_time_min','acuity_level','no_show_probability','emergency_flag']], on='patient_id', how='left')
services['hour_of_day'] = services['planned_start_min'] // 60
services.to_csv(out / 'services_processed.csv', index=False)
patients.to_csv(out / 'patients_processed.csv', index=False)
print(f'Processed data written to {out}')
