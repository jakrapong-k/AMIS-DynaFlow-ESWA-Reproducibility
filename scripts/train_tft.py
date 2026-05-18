#!/usr/bin/env python
from pathlib import Path
import argparse, sys
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from amis_dynaflow.utils.io import load_yaml, ensure_dir
from amis_dynaflow.tft.quantile_forecaster import QuantileServiceTimeForecaster

parser = argparse.ArgumentParser()
parser.add_argument('--config', default='configs/tft.yaml')
args = parser.parse_args()
cfg = load_yaml(args.config)['tft']
df = pd.read_csv(cfg['input']['processed_services'])
model = QuantileServiceTimeForecaster(cfg['quantiles'], cfg['seed']).fit(df)
pred = model.predict(df)
metrics = pd.DataFrame([model.evaluate(df)])
ensure_dir(Path(cfg['output']['predictions']).parent)
pred.to_csv(cfg['output']['predictions'], index=False)
metrics.to_csv(cfg['output']['metrics'], index=False)
print('TFT-style quantile predictions written.')
