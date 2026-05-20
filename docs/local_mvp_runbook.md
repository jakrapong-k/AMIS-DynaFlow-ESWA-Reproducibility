# Local MVP Runbook (Phase 5)

This runbook explains how to run the AMIS-DynaFlow MVP locally in **safe development mode**.

> Safety scope: local-only mock/stub MVP. No real hospital systems, no real clinical databases, and no real patient data are required.

## 1) Prerequisites

- Python 3.10+
- Node.js 18+
- npm 9+
- Git

## 2) Prepare environment variables (placeholders only)

From repository root:

```bash
cp .env.example .env
cp backend/.env.example backend/.env
```

Notes:
- Use only placeholder/local values in `.env` and `backend/.env`.
- Do **not** add real credentials or production endpoints.
- `DATABASE_URL` and `REDIS_URL` are placeholders for future integration and are not required for current mock MVP routes.

## 3) Install dependencies

### Backend

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
cd ..
```

## 4) Run backend (FastAPI + uvicorn)

Option A (direct):

```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

Option B (helper script):

```bash
bash scripts/run_backend_mvp.sh
```

Backend docs:
- Swagger UI: <http://localhost:8000/docs>
- OpenAPI JSON: <http://localhost:8000/openapi.json>

## 5) Backend health checks

In a new terminal:

```bash
curl -sS http://localhost:8000/api/v1/health
curl -sS http://localhost:8000/api/v1/health/ready
curl -sS http://localhost:8000/api/v1/health/live
```

Expected behavior: each endpoint returns a JSON response with healthy status fields.

## 6) Run frontend (React + Vite)

Option A (direct):

```bash
cd frontend
npm run dev
```

Option B (helper script):

```bash
bash scripts/run_frontend_mvp.sh
```

The app is typically available at <http://localhost:5173>.

## 7) Frontend → mock backend API integration

Default API base URL is `http://localhost:8000/api/v1`.

Optional override:

```bash
export VITE_API_BASE_URL="http://localhost:8000/api/v1"
```

Quick API smoke check:

```bash
curl -sS http://localhost:8000/api/v1/dashboard/summary
```

Then open frontend dashboard and verify data is rendered from mock API responses.

## 8) Local verification checklist

- [ ] Backend starts successfully on port 8000.
- [ ] Frontend starts successfully on port 5173 (or Vite-assigned port).
- [ ] Frontend can call mock backend API (`/api/v1/*`).
- [ ] No real patient data is required.
- [ ] No hospital system connection is used.

## 9) Lightweight readiness tests

From repository root:

```bash
# Backend tests
PYTHONPATH=backend pytest backend/tests -q

# Existing repository workflow tests
pytest tests -q

# Frontend tests
cd frontend && npm test
```

If package installation is restricted in your environment, run these commands on a normal local developer machine and keep this runbook as the source of truth.

## 10) Explicit non-goals for this local MVP

- No production deployment.
- No real EHR/HIS integration.
- No real credentials/secrets in repository files.
- No ingestion of real patient-identifiable data.
