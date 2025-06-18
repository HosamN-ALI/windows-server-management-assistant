@echo off
echo ========================================
echo Windows Server 2019 Assistant - Setup Script
echo ========================================
echo.

:: Check for admin privileges and Windows Server 2019
ver | find "Version 10.0.17763" >nul
if %errorLevel% neq 0 (
    echo Error: This script requires Windows Server 2019
    pause
    exit /b 1
)

net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Error: Please run this script as Administrator
    pause
    exit /b 1
)

:: Enable TLS 1.2 for downloads
powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12"

:: Install Server Prerequisites
echo Installing Server Prerequisites...
powershell -Command "Install-WindowsFeature Web-Server"
powershell -Command "Install-WindowsFeature NET-Framework-45-Features"

:: Install Chocolatey
echo Installing Chocolatey Package Manager...
@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
call refreshenv

echo.
echo Installing Python 3.8 (Server 2019 Compatible)...
choco install python --version=3.8.10 -y
call refreshenv

echo.
echo Installing Node.js LTS...
choco install nodejs-lts --version=14.21.3 -y
call refreshenv

echo.
echo Installing Git...
choco install git --version=2.35.1 -y
call refreshenv

echo.
echo Installing Security Tools...

echo Installing OWASP ZAP...
choco install zap --version=2.11.1 -y

echo Installing Python Security Tools...
python -m pip install --upgrade pip
pip install sqlmap==1.5.12

echo.
echo Installing Python Dependencies...
pip install -r requirements.txt

echo.
echo Installing Frontend Dependencies...
cd frontend
call npm install --legacy-peer-deps
cd ..

echo.
echo Setting up Windows Features...
powershell -Command "Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force"
powershell -Command "Set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem' -Name 'LongPathsEnabled' -Value 1"

echo.
echo Creating .env file...
(
echo # Server Configuration
echo SECRET_KEY=development-secret-key-change-in-production
echo OPENAI_API_KEY=your-openai-key-here
echo AZURE_SPEECH_KEY=your-azure-speech-key-here
echo AZURE_SPEECH_REGION=your-region-here
echo.
echo # Database Configuration
echo DATABASE_URL=sqlite:///./app.db
echo.
echo # CORS Settings
echo CORS_ORIGINS=http://localhost:3000
echo.
echo # Windows Server Settings
echo SERVER_NAME=WIN-SERVER-2019
echo SERVER_ENVIRONMENT=development
) > .env

echo.
echo Configuring Windows Firewall...
netsh advfirewall firewall add rule name="FastAPI Backend" dir=in action=allow protocol=TCP localport=8000
netsh advfirewall firewall add rule name="React Frontend" dir=in action=allow protocol=TCP localport=3000

echo.
echo ========================================
echo Installation Complete!
echo.
echo Next steps:
echo 1. Update .env with your API keys
echo 2. Start backend: cd backend ^& python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
echo 3. Start frontend: cd frontend ^& npm start
echo.
echo Note: For production use, configure HTTPS and update security settings
echo ========================================

pause
