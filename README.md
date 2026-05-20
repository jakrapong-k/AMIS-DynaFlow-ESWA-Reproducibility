# AMIS-DynaFlow

**AMIS-DynaFlow** is a paper-aligned reference implementation package for:

> *AMIS-DynaFlow: A Multi-Agent Deep Reinforcement Learning Framework with Quantum-Inspired Operators for Real-Time Patient Flow Optimization in Oncology Centers*  
> Accepted in *Expert Systems with Applications*.

This repository is designed to support reproducibility, auditability, and safe public sharing after article acceptance. It mirrors the three-component architecture described in the manuscript:

1. **QI-MOGA**: probabilistic amplitude-based multi-objective genetic algorithm for offline Pareto baseline generation.
2. **GAT-MAPPO**: graph-attention-based multi-agent proximal policy optimization for decentralized real-time adaptation.
3. **TFT**: Temporal Fusion Transformer-style probabilistic service-time forecasting with quantile outputs.

> **Important scope note**: this repository is a reproducibility/scaffold package, not a production-ready clinical application. It does not provide a deployed API service, authentication layer, or operational MLOps stack.

> **Important privacy note**: the real clinical dataset used in the study is not included. This repository provides sample data, data schemas, preprocessing logic, configuration files, and executable workflow scripts for methodological replication. Sample-data workflow results are intended to validate the computational workflow, not to exactly reproduce the clinical performance values reported in the paper.

## Repository structure

```text
AMIS-DynaFlow-ESWA-Reproducibility/
├── configs/                 # Model and experiment configuration files
├── data/
│   ├── schema/              # Public data schemas
│   └── sample/              # Sample demonstration data
├── docs/                    # Reproducibility and developer documentation
├── results/                 # Sample outputs from the sample-data workflow
├── scripts/                 # CLI scripts for data, training, optimization, and evaluation
├── src/amis_dynaflow/       # Python package
└── tests/                   # Lightweight validation tests
```

For a deeper breakdown, see `docs/project_structure.md`.

## Quickstart

```bash
git clone https://github.com/jakrapong-k/AMIS-DynaFlow-ESWA-Reproducibility.git
cd AMIS-DynaFlow-ESWA-Reproducibility
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Then run the sample reproducibility workflow:

```bash
python scripts/generate_sample_data.py --config configs/experiment_main.yaml
python scripts/preprocess_data.py --config configs/experiment_main.yaml
python scripts/train_tft.py --config configs/tft.yaml
python scripts/run_qi_moga.py --config configs/qi_moga.yaml
python scripts/train_gat_mappo.py --config configs/gat_mappo.yaml
python scripts/evaluate_baselines.py --config configs/experiment_main.yaml
python scripts/reproduce_main_results.py --config configs/experiment_main.yaml
```

Expected final summary output:

```text
results/sample_outputs/reproduction_summary.csv
```


## Local MVP run (safe development)

For running the merged backend/frontend MVP locally (mock-only, no real hospital integrations), use:

- `docs/local_mvp_runbook.md`
- Helper scripts:
  - `bash scripts/run_backend_mvp.sh`
  - `bash scripts/run_frontend_mvp.sh`

## Development setup

- Environment setup and troubleshooting: `docs/development_setup.md`
- Project directory and module map: `docs/project_structure.md`

## Reproducibility configuration

The sample-data workflow uses fixed random seeds:

```text
42, 123, 456, 789, 2024
```

These seeds are defined in `configs/seeds.yaml` and are used across data generation, forecasting, optimization, and evaluation steps.

## Scope of this public package

Included:

- executable sample data generation;
- public data schemas and data dictionary;
- preprocessing pipeline;
- paper-aligned QI-MOGA reference implementation;
- quantile forecasting module that mimics the public workflow of the TFT component;
- lightweight graph-attention/MAPPO-style adaptive policy scaffold;
- evaluation scripts and reproducibility guide;
- privacy and proof-checking documentation.

Not included:

- real patient-level clinical records;
- protected hospital identifiers;
- production EHR/HIS credentials;
- any personally identifiable information.

## Citation

After the ESWA article DOI is available, update `CITATION.cff` with the final DOI.

## License

This package is released under the MIT License. See `LICENSE`.


## Frontend MVP (Phase 4)
- React skeleton and run guide: `docs/frontend_mvp_run_instructions.md`
- Source location: `frontend/`
