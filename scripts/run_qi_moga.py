#!/usr/bin/env python
from pathlib import Path
import argparse, sys
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from amis_dynaflow.utils.io import load_yaml, ensure_dir
from amis_dynaflow.qi_moga.optimizer import QIMOGAOptimizer

parser = argparse.ArgumentParser()
parser.add_argument('--config', default='configs/qi_moga.yaml')
args = parser.parse_args()
cfg = load_yaml(args.config)['qi_moga']
services = pd.read_csv(cfg['input']['processed_services'])
opt = QIMOGAOptimizer(population_size=cfg['population_size'], generations=cfg['generations'], candidate_states=cfg['candidate_states'], chromosome_length=cfg['chromosome_length'], mutation_rate=cfg['mutation_rate'], seed=cfg['seed'])
archive, metrics = opt.run(services)
ensure_dir(Path(cfg['output']['pareto_archive']).parent)
archive.to_csv(cfg['output']['pareto_archive'], index=False)
metrics.to_csv(cfg['output']['metrics'], index=False)
print('QI-MOGA Pareto archive written.')
