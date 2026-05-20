# Frontend MVP Run Instructions (Phase 4)

This document explains how to run the Frontend MVP skeleton for AMIS-DynaFlow.

## Scope
- Frontend is a **React + Vite** skeleton in `frontend/`.
- It consumes existing backend mock/stub APIs from FastAPI (`/api/v1`).
- Pages included:
  - Dashboard (`/`)
  - Login mock (`/login`)
  - Queue/Status (`/queue`)
  - Metrics (`/metrics`)
  - Artifacts (`/artifacts`)

## 1) Start backend mock API
From repository root:

```bash
uvicorn backend.app.main:app --reload --port 8000
```

Health check:

```bash
curl http://localhost:8000/api/v1/health
```

## 2) Install frontend dependencies
Open another terminal, from repository root:

```bash
cd frontend
npm install
```

## 3) Configure API base URL (optional)
By default frontend uses:

- `http://localhost:8000/api/v1`

To override:

```bash
export VITE_API_BASE_URL="http://localhost:8000/api/v1"
```

## 4) Run frontend

```bash
npm run dev
```

Open local URL shown by Vite (typically `http://localhost:5173`).

## 5) Run basic tests

```bash
npm test
```

## Notes
- This MVP is intentionally mock-only and does **not** connect to real hospital data.
- Authentication is mock flow based on backend stub `/auth/login`.
