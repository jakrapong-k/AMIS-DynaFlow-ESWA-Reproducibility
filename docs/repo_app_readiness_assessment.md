# Repository Assessment for App Readiness

## 1) Current repository structure and roles

### Root-level files
- `README.md`: project overview, scope, sample workflow, and limitations around real clinical data.
- `requirements.txt` / `environment.yml`: dependency definitions for pip/conda.
- `CITATION.cff`, `LICENSE`: citation metadata and MIT license.

### `configs/`
- Centralized runtime settings for each module and workflow (`experiment_main.yaml`, `tft.yaml`, `qi_moga.yaml`, `gat_mappo.yaml`, `seeds.yaml`).
- Good separation of concerns, but no schema validation for config keys.

### `data/`
- `sample/`: synthetic/sample datasets for reproducibility demonstrations.
- `schema/`: JSON schemas for patient/service/resource/pathway entities.
- Useful for safe sharing, but there is no data versioning strategy (e.g., DVC/LakeFS) and no explicit validation gate in CI.

### `src/amis_dynaflow/`
- Core package with modular components:
  - `tft/quantile_forecaster.py`: a lightweight surrogate for TFT (currently gradient boosting quantile regressors).
  - `qi_moga/optimizer.py`: probabilistic amplitude-inspired multi-objective optimizer.
  - `gat_mappo/policy.py`: schedule adaptation scaffold with attention-like transition weighting.
  - `simulation/`: sample data generation and metrics helpers.
  - `utils/`: seed + I/O helpers.
- Strength: clear modular decomposition.
- Limitation: production-grade RL/training infra is intentionally scaffold-level.

### `scripts/`
- End-to-end executable pipeline steps from sample data generation to evaluation and summary.
- `reproduce_main_results.py` orchestrates all stages sequentially.
- Limitation: script orchestration is shell-subprocess based, lacks robust experiment tracking/logging/retry logic.

### `results/sample_outputs/`
- Snapshot artifacts from sample-data workflow.
- Good for reproducibility demos, but no artifact lineage metadata.

### `tests/`
- Minimal smoke test that runs the full sample workflow and checks summary output exists.
- Limitation: no unit tests for core algorithmic behaviors, edge cases, or data contracts.

### `docs/`
- Reproducibility and privacy documents are present, aligned with publication transparency.

## 2) What is currently missing

1. **Application layer**
   - No API service (REST/gRPC) for inference/optimization.
   - No web UI for operations teams.
   - No authentication/authorization boundaries.

2. **Operational reliability**
   - No structured logging, tracing, or monitoring hooks.
   - No model registry, versioned artifacts, or staged deployment flow.
   - No background job scheduler / queue for long-running optimization.

3. **Data/ML governance**
   - No CI checks for schema validation and drift alerts.
   - No explicit feature-store or training-serving parity mechanism.
   - No offline/online evaluation dashboards.

4. **Engineering quality depth**
   - Test coverage is very thin.
   - No static analysis/type check pipeline configuration in repo.
   - No containerization/deployment manifests (`Dockerfile`, Helm, compose).

## 3) Observed technical risks/issues

1. **Reproducibility test is broad but shallow**
   - One smoke test verifies output existence, but may miss silent quality regressions.

2. **Scaffold-vs-production expectation gap**
   - README states paper-aligned reference and safety/public constraints, but teams might over-assume production readiness without guardrails.

3. **Tight coupling to file-based local workflow**
   - Multiple scripts read/write fixed local paths; harder to run as cloud-native services.

4. **No explicit input contract enforcement during runtime**
   - Schemas exist, but pipeline scripts do not enforce strict validation at each stage.

## 4) Recommended roadmap to become a real trial app

## Phase 1 (2-4 weeks): harden reproducibility package
- Add contract tests per module (`tft`, `qi_moga`, `gat_mappo`) with deterministic fixtures.
- Add schema validation step in preprocess/train scripts.
- Add structured logging + run metadata (run_id, seed, config hash).
- Add `Dockerfile` and `docker-compose` for one-command execution.

## Phase 2 (3-6 weeks): create MVP application surfaces
- Build API backend (FastAPI recommended):
  - `POST /forecast`
  - `POST /optimize`
  - `POST /adapt-schedule`
  - `GET /runs/{id}`
- Introduce async job queue (Celery/RQ) for optimization tasks.
- Add lightweight web dashboard for uploading datasets, triggering runs, and comparing metrics.

## Phase 3 (4-8 weeks): MLOps + security readiness
- Add model/artifact registry (MLflow or equivalent).
- Add CI/CD with linting, typing, tests, security scans.
- Add RBAC/auth (OIDC), audit trail, and PHI-safe logging policy.
- Add monitoring stack: data drift, performance drift, SLO alerts.

## Phase 4 (ongoing): clinical trial/pilot readiness
- Integrate hospital data adapters (HL7/FHIR mapping layer).
- Add human-in-the-loop override UX and explainability views.
- Define governance SOPs: model approval, rollback, incident response.

## 5) Suggested target architecture

- **Frontend**: React/Next.js operations dashboard.
- **Backend**: FastAPI orchestration + domain services.
- **Compute workers**: separate workers for TFT forecast, QI-MOGA optimization, and GAT-MAPPO adaptation.
- **Storage**: Postgres (metadata), object storage (artifacts), Redis (queue/cache).
- **MLOps**: MLflow + Great Expectations + Evidently.
- **Deployment**: Docker/Kubernetes with staged environments (dev/stage/prod).

## 6) Definition of Done for "App ทดลองใช้งานจริง"

A release candidate should meet all:
1. User can upload new data, run full pipeline, and view/export KPIs via UI.
2. Every run is traceable (`code version + config + data hash + seed + artifact lineage`).
3. Validation and failure reasons are visible and recoverable.
4. Security controls (auth, audit logs, secret handling) are in place.
5. Minimum reliability target (e.g., 99% successful pipeline completion on sample workload).

