#!/usr/bin/env python
from pathlib import Path
import argparse, sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from amis_dynaflow.utils.io import load_yaml
from amis_dynaflow.simulation.sample_data import generate_sample_data

parser = argparse.ArgumentParser()
parser.add_argument('--config', default='configs/experiment_main.yaml')
args = parser.parse_args()
cfg = load_yaml(args.config)
exp = cfg['experiment']
out = cfg['paths']['sample_dir']
generate_sample_data(exp['num_patients'], exp['num_stations'], exp['seeds'][0], out)
print(f'Sample data written to {out}')
