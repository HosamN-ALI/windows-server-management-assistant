#Requires -RunAsAdministrator

$ErrorActionPreference = "Stop"

function Write-Header {
    param($Message)
    Write-Host "`n=============================================" -ForegroundColor Cyan
    Write-Host $Message -ForegroundColor Cyan
    Write-Host "=============================================`n" -ForegroundColor Cyan
}

function Write-Step {
    param($Message)
    Write-Host "-> $Message" -ForegroundColor Yellow
}

function Write-Success {
    param($Message)
    Write-Host "✓ $Message" -ForegroundColor Green
}

function Write-Error {
    param($Message)
    Write-Host "✗ Error: $Message" -ForegroundColor Red
}

function Test-WindowsServer2019 {
    $version = [System.Environment]::OSVersion.Version
    return ($version.Major -eq 10 -and $version.Build -eq 17763)
}

try {
    Write-Header "Windows Server 2019 Assistant - Setup Script"

    # Check Windows Server 2019
    Write-Step "Checking Windows Server 2019..."
    if (!(Test-WindowsServer2019)) {
        Write-Error "This script requires Windows Server 2019 (Build 17763)"
        exit 1
    }
    Write-Success "Windows Server 2019 detected"

    # Enable TLS 1.2
    Write-Step "Enabling TLS 1.2..."
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    Write-Success "TLS 1.2 enabled"

    # Install Server Prerequisites
    Write-Step "Installing Server Prerequisites..."
    Install-WindowsFeature -Name Web-Server -IncludeManagementTools
    Install-WindowsFeature -Name NET-Framework-45-Features
    Write-Success "Server prerequisites installed"

    # Install Chocolatey if not installed
    Write-Step "Checking for Chocolatey installation..."
    if (!(Get-Command choco -ErrorAction SilentlyContinue)) {
        Write-Step "Installing Chocolatey..."
        Set-ExecutionPolicy Bypass -Scope Process -Force
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
        Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
        Write-Success "Chocolatey installed successfully"
    } else {
        Write-Success "Chocolatey is already installed"
    }

    # Install Python 3.8 (Server 2019 Compatible)
    Write-Step "Installing Python 3.8 (Server 2019 Compatible)..."
    choco install python --version=3.8.10 -y
    refreshenv
    Write-Success "Python 3.8 installed successfully"

    # Install Node.js LTS
    Write-Step "Installing Node.js LTS..."
    choco install nodejs-lts --version=14.21.3 -y
    refreshenv
    Write-Success "Node.js LTS installed successfully"

    # Install Git
    Write-Step "Installing Git..."
    choco install git --version=2.35.1 -y
    refreshenv
    Write-Success "Git installed successfully"

    # Install Security Tools
    Write-Header "Installing Security Tools"

    Write-Step "Installing OWASP ZAP..."
    choco install zap --version=2.11.1 -y
    Write-Success "OWASP ZAP installed successfully"

    Write-Step "Installing Python Security Tools..."
    python -m pip install --upgrade pip
    python -m pip install sqlmap==1.5.12
    Write-Success "Python security tools installed successfully"

    # Install Python Dependencies
    Write-Step "Installing Python project dependencies..."
    python -m pip install -r requirements.txt
    Write-Success "Python dependencies installed successfully"

    # Install Frontend Dependencies
    Write-Step "Installing Frontend dependencies..."
    Push-Location frontend
    npm install --legacy-peer-deps
    Pop-Location
    Write-Success "Frontend dependencies installed successfully"

    # Configure Windows Features
    Write-Step "Configuring Windows Features..."
    Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
    Set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem' -Name 'LongPathsEnabled' -Value 1
    Write-Success "Windows features configured"

    # Configure Firewall
    Write-Step "Configuring Windows Firewall..."
    New-NetFirewallRule -DisplayName "FastAPI Backend" -Direction Inbound -Protocol TCP -LocalPort 8000 -Action Allow
    New-NetFirewallRule -DisplayName "React Frontend" -Direction Inbound -Protocol TCP -LocalPort 3000 -Action Allow
    Write-Success "Firewall rules configured"

    # Create .env file if it doesn't exist
    Write-Step "Creating .env file..."
    if (!(Test-Path .env)) {
        $envContent = @"
# Server Configuration
SECRET_KEY=development-secret-key-change-in-production
OPENAI_API_KEY=your-openai-key-here
AZURE_SPEECH_KEY=your-azure-speech-key-here
AZURE_SPEECH_REGION=your-region-here

# Database Configuration
DATABASE_URL=sqlite:///./app.db

# CORS Settings
CORS_ORIGINS=http://localhost:3000

# Windows Server Settings
SERVER_NAME=WIN-SERVER-2019
SERVER_ENVIRONMENT=development
"@
        $envContent | Out-File -FilePath .env -Encoding UTF8
        Write-Success ".env file created successfully"
    } else {
        Write-Host "Warning: .env file already exists, skipping creation" -ForegroundColor Yellow
    }

    Write-Header "Installation Complete!"
    $completionMessage = @"
Next steps:
1. Update .env with your API keys
2. Start backend: cd backend; python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
3. Start frontend: cd frontend; npm start

Documentation:
- API Docs: http://localhost:8000/docs
- Project Profile: See PROJECT_PROFILE.md

Note: For production use, configure HTTPS and update security settings
"@
    Write-Host $completionMessage -ForegroundColor Green

} catch {
    Write-Error $_.Exception.Message
    Write-Host "`nInstallation failed. Please check the error message above." -ForegroundColor Red
    exit 1
}

Write-Host "`nPress any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
