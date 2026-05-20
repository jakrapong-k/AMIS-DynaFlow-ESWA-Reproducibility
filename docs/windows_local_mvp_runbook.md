# Windows-first Local MVP Runbook (Copy/Paste)

This runbook is designed for **real Windows user machines** (Windows 10/11) and uses only **mock/local data**.

> Safety scope: local-only MVP with mock API data. No real hospital systems, no real EHR integration, and no real patient data.

## 1) Prerequisites

Install these first:

- **Git for Windows**
- **Python 3.10+** (enable "Add python.exe to PATH")
- **Node.js 18+ LTS** (npm bundled)
- **PowerShell 5.1+** (built-in) or PowerShell 7+

Optional but useful:
- VS Code

## 2) Open PowerShell in repository root

```powershell
cd C:\path\to\AMIS-DynaFlow-ESWA-Reproducibility
```

## 3) Create local env files (placeholders only)

```powershell
Copy-Item .env.example .env -Force
Copy-Item backend/.env.example backend/.env -Force
```

Rules:
- Keep only placeholder/local values.
- Do not add production credentials.
- `DATABASE_URL` and `REDIS_URL` are placeholders and not required for current mock routes.

## 4) Backend setup + run

### Option A: one command via helper script (recommended)

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\windows_run_backend.ps1
```

What it does:
- Creates `.venv` if missing
- Installs Python dependencies from `requirements.txt`
- Starts FastAPI/Uvicorn on `http://127.0.0.1:8000`

### Option B: manual commands

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

## 5) Frontend setup + run

Open a **new PowerShell window** at repo root:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\windows_run_frontend.ps1
```

What it does:
- Installs frontend dependencies (`npm install`)
- Sets `VITE_API_BASE_URL` to `http://127.0.0.1:8000/api/v1` for the process
- Runs Vite dev server (usually `http://127.0.0.1:5173`)

## 6) API smoke test (mock/local only)

With backend running, execute:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\windows_smoke_check.ps1
```

Expected:
- Health endpoints return `ok`/healthy payloads
- Mock endpoints (`/dashboard/summary`, `/runs`, `/runs/{id}/metrics`) return JSON

## 7) Quick manual checks

- Open backend docs: <http://127.0.0.1:8000/docs>
- Open frontend app: <http://127.0.0.1:5173>
- Confirm dashboard/runs pages show mock responses

## 8) Non-goals / explicit constraints

- No production deployment
- No connection to real hospital systems
- No real patient-identifiable data
- No real secret management in local MVP

## 9) Troubleshooting

- **`python` not found**: reinstall Python and check PATH option.
- **Execution policy blocks scripts**: run with `-ExecutionPolicy Bypass` exactly as shown.
- **Port 8000 already used**: stop old process or change `-Port` in backend script.
- **Port 5173 already used**: Vite may choose another port; see terminal output.
- **Corporate proxy / npm errors**: configure npm proxy or use trusted network.
