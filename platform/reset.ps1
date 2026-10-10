# Reset and clean the CTFd platform to initial state
Write-Host "[*] Tearing down CTFd containers and clearing database volumes..." -ForegroundColor Yellow
docker compose -f .\platform\docker-compose.yml down -v

Write-Host "[*] Rebuilding and launching clean CTFd instance..." -ForegroundColor Cyan
docker compose -f .\platform\docker-compose.yml up -d

Write-Host "[+] Atlantis CTF Platform has been successfully reset! Running at http://localhost:8000" -ForegroundColor Green
