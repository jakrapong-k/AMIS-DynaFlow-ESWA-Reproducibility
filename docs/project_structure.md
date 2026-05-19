# Project Structure

This document explains the role of each top-level directory in the repository.

## Top-level map

```text
.
├── configs/
├── data/
├── docs/
├── results/
├── scripts/
├── src/
├── tests/
├── README.md
├── requirements.txt
└── environment.yml
```

## Directory responsibilities

### `src/amis_dynaflow/`
Core Python package for the reproducibility workflow:
- `tft/`: quantile forecasting scaffold (TFT-style workflow approximation)
- `qi_moga/`: quantum-inspired multi-objective optimization
- `gat_mappo/`: adaptive scheduling policy scaffold
- `simulation/`: sample data generation and metrics helpers
- `utils/`: shared utility functions

### `scripts/`
CLI entry points for end-to-end execution:
- sample data generation
- preprocessing
- forecasting training/inference flow
- QI-MOGA optimization
- GAT-MAPPO adaptation
- baseline evaluation
- one-command reproduction orchestration

### `configs/`
YAML configuration files for experiments and module behavior.

### `data/`
- `sample/`: synthetic/sample data for safe public reproduction
- `schema/`: JSON schema definitions for input contracts

### `results/sample_outputs/`
Reference outputs from sample workflow runs.

### `tests/`
Lightweight workflow smoke tests.

### `docs/`
Supporting documentation (reproducibility, privacy, setup, and assessment notes).

## Notes for app-readiness planning

This repository is currently optimized for reproducibility workflows. API, auth, job queue, and deployment assets are planned future additions and are not part of the current core package.
