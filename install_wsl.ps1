Write-Host "=== HealthAI Build Setup ===" -ForegroundColor Cyan
Write-Host "Enabling WSL features..." -ForegroundColor Yellow

# Enable WSL
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

Write-Host ""
Write-Host "WSL features enabled!" -ForegroundColor Green
Write-Host ""
Write-Host "Now installing Ubuntu 22.04..." -ForegroundColor Yellow

# Install Ubuntu 22.04 (best for Buildozer)
wsl --install -d Ubuntu-22.04 --no-launch

Write-Host ""
Write-Host "=== Done! ===" -ForegroundColor Green
Write-Host "Ubuntu is installed. A restart may be required." -ForegroundColor Cyan
Write-Host "After restart, run the HealthAI build script." -ForegroundColor Cyan
Write-Host ""
Read-Host "Press Enter to close"
