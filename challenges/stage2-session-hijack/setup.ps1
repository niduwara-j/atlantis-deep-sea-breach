$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
if (-not (Test-Path -LiteralPath '.env')) {
    $randomBytes = New-Object byte[] 16
    $generator = [System.Security.Cryptography.RandomNumberGenerator]::Create()
    try { $generator.GetBytes($randomBytes) } finally { $generator.Dispose() }
    $suffix = -join ($randomBytes | ForEach-Object { $_.ToString('x2') })
    $flag = 'Atlantis{session_hijack_' + $suffix + '}'
    [System.IO.File]::WriteAllText((Join-Path $PSScriptRoot '.env'), "CHALLENGE_FLAG=$flag`n", (New-Object System.Text.UTF8Encoding($false)))
} else {
    $line = Get-Content -LiteralPath '.env' | Where-Object { $_ -match '^CHALLENGE_FLAG=' } | Select-Object -First 1
    if (-not $line) { throw 'Existing .env has no CHALLENGE_FLAG. Fix it before continuing.' }
    $flag = $line.Substring('CHALLENGE_FLAG='.Length)
}
New-Item -ItemType Directory -Path 'private' -Force | Out-Null
[System.IO.File]::WriteAllText((Join-Path $PSScriptRoot 'private\ctfd-flag.txt'), $flag, (New-Object System.Text.UTF8Encoding($false)))
Write-Host 'Ready. The private CTFd flag is in private\ctfd-flag.txt. Existing flags are preserved.'
