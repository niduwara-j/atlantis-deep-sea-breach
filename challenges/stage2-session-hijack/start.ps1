$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
& "$PSScriptRoot\setup.ps1"
docker compose config --quiet
if ($LASTEXITCODE -ne 0) { throw 'Compose configuration check failed.' }
docker compose up -d --build
if ($LASTEXITCODE -ne 0) { throw 'Docker startup failed. Check that Docker Desktop is running.' }
docker compose ps
$challengeReady = $false
for ($attempt = 0; $attempt -lt 15; $attempt++) {
    try {
        $health = Invoke-WebRequest -UseBasicParsing -Uri 'http://127.0.0.1:8092/healthz' -TimeoutSec 3
        if ($health.StatusCode -eq 200) { $challengeReady = $true; break }
    } catch { }
    Start-Sleep -Seconds 2
}
if (-not $challengeReady) { throw 'The browser endpoint is not ready. Run docker compose logs --tail 60 web gateway.' }
Write-Host 'Browser endpoint verified. Open http://127.0.0.1:8092/session-hijack/'
