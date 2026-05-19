from __future__ import annotations
import numpy as np
import pandas as pd


class GraphAttentionPolicyScaffold:
    """Lightweight graph-attention adaptation scaffold for the public sample-data workflow."""

    def __init__(self, num_heads=4, temperature=1.0, seed=42):
        self.num_heads = num_heads
        self.temperature = temperature
        self.rng = np.random.default_rng(seed)

    def build_attention(self, services: pd.DataFrame) -> pd.DataFrame:
        transitions = services.sort_values(['patient_id', 'sequence_order'])
        edges = []
        for _, group in transitions.groupby('patient_id'):
            stations = group['station_id'].tolist()
            for a, b in zip(stations[:-1], stations[1:]):
                edges.append((a, b))
        if not edges:
            return pd.DataFrame(columns=['source_station', 'target_station', 'attention_weight'])
        edge_df = pd.DataFrame(edges, columns=['source_station', 'target_station']).value_counts().reset_index(name='count')
        edge_df['attention_weight'] = edge_df['count'] / edge_df.groupby('source_station')['count'].transform('sum')
        return edge_df

    def adapt_schedule(self, services: pd.DataFrame, predictions: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
        df = services.merge(predictions, on=['patient_id', 'station_id', 'sequence_order', 'planned_start_min'], how='left')
        if 'q90' not in df:
            df['q90'] = df['service_duration_min']
        if 'q50' not in df:
            df['q50'] = df['service_duration_min']
        station_pressure = df.groupby('station_id')['q90'].transform('mean')
        pressure_norm = station_pressure / (station_pressure.mean() + 1e-9)
        df['adapted_start_min'] = np.maximum(0, df['planned_start_min'] + np.round((pressure_norm - 1.0) * 5).astype(int))
        attention = self.build_attention(df)
        metrics = pd.DataFrame([{
            'num_edges': int(len(attention)),
            'mean_attention_weight': float(attention['attention_weight'].mean()) if len(attention) else 0.0,
            'adapted_services': int(len(df))
        }])
        return df, metrics
