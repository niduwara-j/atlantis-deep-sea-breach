$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
docker compose restart web
if ($LASTEXITCODE -ne 0) { throw 'Challenge reset failed.' }
Write-Host 'Sessions have been reset. All players must log in again and obtain the new trace.'
Write-Host 'The CTFd flag and competition scores are unchanged. Check docker compose ps for health.'
