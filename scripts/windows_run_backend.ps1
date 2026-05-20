param(
    [string]$Host = "127.0.0.1",
    [int]$Port = 8000
)

$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repoRoot

if (-not (Test-Path ".venv")) {
    Write-Host "[backend] Creating virtual environment (.venv)..."
    python -m venv .venv
}

$pythonExe = Join-Path $repoRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $pythonExe)) {
    throw "[backend] Missing $pythonExe. Ensure Python is installed correctly."
}

Write-Host "[backend] Installing/updating dependencies from requirements.txt..."
& $pythonExe -m pip install --upgrade pip
& $pythonExe -m pip install -r requirements.txt

if (-not (Test-Path ".env") -and (Test-Path ".env.example")) {
    Write-Host "[backend] Creating .env from .env.example (placeholder values)..."
    Copy-Item .env.example .env -Force
}
if (-not (Test-Path "backend/.env") -and (Test-Path "backend/.env.example")) {
    Write-Host "[backend] Creating backend/.env from backend/.env.example (placeholder values)..."
    Copy-Item backend/.env.example backend/.env -Force
}

Write-Host "[backend] Starting FastAPI on http://$Host`:$Port ..."
& $pythonExe -m uvicorn backend.app.main:app --reload --host $Host --port $Port
