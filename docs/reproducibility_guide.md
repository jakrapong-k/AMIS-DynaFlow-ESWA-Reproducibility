# Reproducibility guide

This guide reproduces the public synthetic workflow of AMIS-DynaFlow.

## 1. Install

```bash
pip install -r requirements.txt
```

## 2. Generate synthetic data

```bash
python scripts/generate_synthetic_data.py --config configs/experiment_main.yaml
```

## 3. Preprocess

```bash
python scripts/preprocess_data.py --config configs/experiment_main.yaml
```

## 4. Generate quantile service-time forecasts

```bash
python scripts/train_tft.py --config configs/tft.yaml
```

## 5. Generate Pareto baseline schedules

```bash
python scripts/run_qi_moga.py --config configs/qi_moga.yaml
```

## 6. Run graph-attention adaptation scaffold

```bash
python scripts/train_gat_mappo.py --config configs/gat_mappo.yaml
```

## 7. Evaluate

```bash
python scripts/evaluate_baselines.py --config configs/experiment_main.yaml
```

## 8. One-command synthetic reproduction

```bash
python scripts/reproduce_main_results.py --config configs/experiment_main.yaml
```

The synthetic workflow validates the computational structure. It is not intended to exactly reproduce clinical outcomes reported in the article because the real clinical data cannot be shared publicly.
