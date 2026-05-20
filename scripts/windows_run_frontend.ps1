param(
    [string]$ApiBaseUrl = "http://127.0.0.1:8000/api/v1"
)

$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$frontendDir = Join-Path $repoRoot "frontend"

if (-not (Test-Path $frontendDir)) {
    throw "[frontend] frontend directory not found: $frontendDir"
}

Set-Location $frontendDir

Write-Host "[frontend] Installing dependencies..."
npm install

$env:VITE_API_BASE_URL = $ApiBaseUrl
Write-Host "[frontend] VITE_API_BASE_URL=$env:VITE_API_BASE_URL"
Write-Host "[frontend] Starting Vite dev server..."
npm run dev -- --host 127.0.0.1
