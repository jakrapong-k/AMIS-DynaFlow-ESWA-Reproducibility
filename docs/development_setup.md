# Development Setup

This guide helps set up a local development environment for the AMIS-DynaFlow reproducibility package.

## 1) Prerequisites

- Python 3.10+
- `pip` (or conda, optional)
- Git

## 2) Create and activate virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

## 3) Install dependencies

### Option A: pip

```bash
pip install -r requirements.txt
```

### Option B: conda

```bash
conda env create -f environment.yml
conda activate amis-dynaflow
```

## 4) Configure local environment variables

```bash
cp .env.example .env
```

Edit `.env` values if you need custom local paths.

## 5) Run sample reproducibility workflow

```bash
python scripts/generate_sample_data.py --config configs/experiment_main.yaml
python scripts/preprocess_data.py --config configs/experiment_main.yaml
python scripts/train_tft.py --config configs/tft.yaml
python scripts/run_qi_moga.py --config configs/qi_moga.yaml
python scripts/train_gat_mappo.py --config configs/gat_mappo.yaml
python scripts/evaluate_baselines.py --config configs/experiment_main.yaml
python scripts/reproduce_main_results.py --config configs/experiment_main.yaml
```

Expected output summary:

- `results/sample_outputs/reproduction_summary.csv`

## 6) Run tests

```bash
pytest -q
```

## 7) Common troubleshooting

- If Python cannot import `amis_dynaflow`, make sure you run commands from repository root.
- If dependencies conflict, recreate `.venv` and reinstall from `requirements.txt`.
- If output files are missing, re-run the workflow in the exact order shown above.
