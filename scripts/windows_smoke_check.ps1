param(
    [string]$BaseUrl = "http://127.0.0.1:8000/api/v1"
)

$ErrorActionPreference = "Stop"

function Invoke-JsonGet {
    param([string]$Url)
    $response = Invoke-RestMethod -Method Get -Uri $Url -TimeoutSec 10
    Write-Host "[OK] GET $Url"
    $response | ConvertTo-Json -Depth 8
}

Write-Host "[smoke] Using API base URL: $BaseUrl"

Invoke-JsonGet "$BaseUrl/health" | Out-Null
Invoke-JsonGet "$BaseUrl/health/ready" | Out-Null
Invoke-JsonGet "$BaseUrl/health/live" | Out-Null
Invoke-JsonGet "$BaseUrl/dashboard/summary" | Out-Null
Invoke-JsonGet "$BaseUrl/runs" | Out-Null
Invoke-JsonGet "$BaseUrl/runs/run_mock_001/metrics" | Out-Null
Invoke-JsonGet "$BaseUrl/runs/run_mock_001/artifacts" | Out-Null

Write-Host "[smoke] All mock API smoke checks passed."
