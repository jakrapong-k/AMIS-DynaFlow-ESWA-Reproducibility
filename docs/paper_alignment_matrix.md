# Paper-to-repository alignment matrix

| Manuscript component | Public repository artifact |
|---|---|
| QI-MOGA offline Pareto baseline generation | `src/amis_dynaflow/qi_moga/`, `scripts/run_qi_moga.py`, `configs/qi_moga.yaml` |
| GAT-MAPPO real-time adaptation | `src/amis_dynaflow/gat_mappo/`, `scripts/train_gat_mappo.py`, `configs/gat_mappo.yaml` |
| TFT probabilistic service-time forecasting | `src/amis_dynaflow/tft/`, `scripts/train_tft.py`, `configs/tft.yaml` |
| Two-phase closed-loop workflow | `scripts/reproduce_main_results.py` |
| Fixed random seeds | `configs/seeds.yaml` |
| Training/evaluation scripts | `scripts/` |
| Model configuration files | `configs/` |
| Synthetic data generation | `scripts/generate_synthetic_data.py` |
| Anonymized data structures | `data/schema/` |
| Clinical data privacy restriction | `docs/privacy_statement.md` |
| Proof risk mitigation for QI terminology | `docs/proof_checklist.md` |
