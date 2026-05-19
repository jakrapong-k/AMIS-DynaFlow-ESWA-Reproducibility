from __future__ import annotations
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error


class QuantileServiceTimeForecaster:
    """Public lightweight quantile forecaster for sample-data reproducibility.

    This mirrors the public workflow expected from the TFT component: multi-quantile
    service-time predictions. Production TFT implementations can replace this class
    while preserving the input/output contract.
    """

    def __init__(self, quantiles=(0.1, 0.5, 0.9), seed: int = 42):
        self.quantiles = list(quantiles)
        self.seed = seed
        self.models = {}
        self.feature_cols = ['station_id', 'sequence_order', 'planned_start_min']

    def fit(self, df: pd.DataFrame) -> 'QuantileServiceTimeForecaster':
        x = df[self.feature_cols]
        y = df['service_duration_min']
        for q in self.quantiles:
            loss = 'squared_error' if abs(q - 0.5) < 1e-9 else 'quantile'
            kwargs = {'random_state': self.seed, 'n_estimators': 20, 'max_depth': 3}
            if loss == 'quantile':
                kwargs.update({'loss': 'quantile', 'alpha': q})
            else:
                kwargs.update({'loss': 'squared_error'})
            model = GradientBoostingRegressor(**kwargs)
            model.fit(x, y)
            self.models[q] = model
        return self

    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        out = df[['patient_id', 'station_id', 'sequence_order', 'planned_start_min']].copy()
        x = df[self.feature_cols]
        for q, model in self.models.items():
            out[f'q{int(q*100):02d}'] = np.maximum(1.0, model.predict(x))
        if {'q10', 'q50', 'q90'} <= set(out.columns):
            out['interval_width'] = out['q90'] - out['q10']
        return out

    def evaluate(self, df: pd.DataFrame) -> dict:
        pred = self.predict(df)
        median_col = f'q{int(0.5*100):02d}' if 'q50' in pred else list(pred.filter(regex='^q').columns)[0]
        y_true = df['service_duration_min'].to_numpy()
        y_pred = pred[median_col].to_numpy()
        return {
            'MAE': float(mean_absolute_error(y_true, y_pred)),
            'RMSE': float(mean_squared_error(y_true, y_pred) ** 0.5),
            'num_records': int(len(df))
        }
