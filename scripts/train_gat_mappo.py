#!/usr/bin/env python
from pathlib import Path
import argparse, sys
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from amis_dynaflow.utils.io import load_yaml, ensure_dir
from amis_dynaflow.gat_mappo.policy import GraphAttentionPolicyScaffold

parser = argparse.ArgumentParser()
parser.add_argument('--config', default='configs/gat_mappo.yaml')
args = parser.parse_args()
cfg = load_yaml(args.config)['gat_mappo']
services = pd.read_csv('results/sample_outputs/processed/services_processed.csv')
pred = pd.read_csv(cfg['input']['tft_predictions'])
policy = GraphAttentionPolicyScaffold(num_heads=cfg['graph_attention']['num_heads'], temperature=cfg['graph_attention']['attention_temperature'], seed=cfg['seed'])
adapted, metrics = policy.adapt_schedule(services, pred)
ensure_dir(Path(cfg['output']['adapted_schedule']).parent)
adapted.to_csv(cfg['output']['adapted_schedule'], index=False)
metrics.to_csv(cfg['output']['metrics'], index=False)
print('GAT-MAPPO adaptation scaffold output written.')
