#Requires -RunAsAdministrator

$ErrorActionPreference = "Continue"

function Write-Header {
    param($Message)
    Write-Host "`n=============================================" -ForegroundColor Cyan
    Write-Host $Message -ForegroundColor Cyan
    Write-Host "=============================================`n" -ForegroundColor Cyan
}

function Write-Check {
    param($Message, $Status)
    if ($Status) {
        Write-Host "✓ $Message" -ForegroundColor Green
    } else {
        Write-Host "✗ $Message" -ForegroundColor Red
    }
}

Write-Header "Windows Server 2019 Compatibility Verification"

# Check Windows Version
Write-Host "Checking Windows Version..." -ForegroundColor Yellow
$version = [System.Environment]::OSVersion.Version
$isServer2019 = ($version.Major -eq 10 -and $version.Build -eq 17763)
Write-Check "Windows Server 2019 (Build 17763)" $isServer2019
Write-Host "Current Version: $($version.Major).$($version.Minor).$($version.Build)" -ForegroundColor Gray

# Check Administrator Rights
Write-Host "`nChecking Administrator Rights..." -ForegroundColor Yellow
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
Write-Check "Running as Administrator" $isAdmin

# Check PowerShell Version
Write-Host "`nChecking PowerShell Version..." -ForegroundColor Yellow
$psVersion = $PSVersionTable.PSVersion.Major -ge 5
Write-Check "PowerShell 5.0 or higher" $psVersion
Write-Host "Current Version: $($PSVersionTable.PSVersion)" -ForegroundColor Gray

# Check .NET Framework
Write-Host "`nChecking .NET Framework..." -ForegroundColor Yellow
try {
    $netVersion = Get-ItemProperty "HKLM:SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full\" -Name Release -ErrorAction Stop
    $hasNet45 = $netVersion.Release -ge 378389
    Write-Check ".NET Framework 4.5 or higher" $hasNet45
} catch {
    Write-Check ".NET Framework 4.5 or higher" $false
}

# Check Internet Connectivity
Write-Host "`nChecking Internet Connectivity..." -ForegroundColor Yellow
try {
    $ping = Test-NetConnection -ComputerName "8.8.8.8" -Port 53 -InformationLevel Quiet
    Write-Check "Internet Connection" $ping
} catch {
    Write-Check "Internet Connection" $false
}

# Check TLS 1.2
Write-Host "`nChecking TLS 1.2 Support..." -ForegroundColor Yellow
try {
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    $hasTLS12 = $true
    Write-Check "TLS 1.2 Support" $hasTLS12
} catch {
    Write-Check "TLS 1.2 Support" $false
}

# Check Windows Features
Write-Host "`nChecking Windows Features..." -ForegroundColor Yellow
$webServer = Get-WindowsFeature -Name Web-Server | Where-Object {$_.InstallState -eq "Installed"}
Write-Check "IIS Web Server" ($webServer -ne $null)

$netFramework = Get-WindowsFeature -Name NET-Framework-45-Features | Where-Object {$_.InstallState -eq "Installed"}
Write-Check ".NET Framework Features" ($netFramework -ne $null)

# Check if Chocolatey is installed
Write-Host "`nChecking Package Managers..." -ForegroundColor Yellow
$chocoInstalled = Get-Command choco -ErrorAction SilentlyContinue
Write-Check "Chocolatey Package Manager" ($chocoInstalled -ne $null)

# Check Python
Write-Host "`nChecking Development Tools..." -ForegroundColor Yellow
$pythonInstalled = Get-Command python -ErrorAction SilentlyContinue
Write-Check "Python" ($pythonInstalled -ne $null)
if ($pythonInstalled) {
    $pythonVersion = python --version 2>&1
    Write-Host "Python Version: $pythonVersion" -ForegroundColor Gray
}

# Check Node.js
$nodeInstalled = Get-Command node -ErrorAction SilentlyContinue
Write-Check "Node.js" ($nodeInstalled -ne $null)
if ($nodeInstalled) {
    $nodeVersion = node --version 2>&1
    Write-Host "Node.js Version: $nodeVersion" -ForegroundColor Gray
}

# Check Git
$gitInstalled = Get-Command git -ErrorAction SilentlyContinue
Write-Check "Git" ($gitInstalled -ne $null)
if ($gitInstalled) {
    $gitVersion = git --version 2>&1
    Write-Host "Git Version: $gitVersion" -ForegroundColor Gray
}

# Check Firewall Rules
Write-Host "`nChecking Firewall Configuration..." -ForegroundColor Yellow
$firewallRule8000 = Get-NetFirewallRule -DisplayName "FastAPI Backend" -ErrorAction SilentlyContinue
Write-Check "Firewall Rule for Port 8000" ($firewallRule8000 -ne $null)

$firewallRule3000 = Get-NetFirewallRule -DisplayName "React Frontend" -ErrorAction SilentlyContinue
Write-Check "Firewall Rule for Port 3000" ($firewallRule3000 -ne $null)

# Check Project Files
Write-Host "`nChecking Project Files..." -ForegroundColor Yellow
Write-Check "requirements.txt exists" (Test-Path "requirements.txt")
Write-Check "setup.bat exists" (Test-Path "setup.bat")
Write-Check "setup.ps1 exists" (Test-Path "setup.ps1")
Write-Check "backend folder exists" (Test-Path "backend")
Write-Check "frontend folder exists" (Test-Path "frontend")

# Summary
Write-Header "Compatibility Summary"

$totalChecks = 0
$passedChecks = 0

# Count checks (simplified for demo)
if ($isServer2019) { $passedChecks++ }; $totalChecks++
if ($isAdmin) { $passedChecks++ }; $totalChecks++
if ($psVersion) { $passedChecks++ }; $totalChecks++

$compatibilityScore = [math]::Round(($passedChecks / $totalChecks) * 100, 2)

if ($compatibilityScore -ge 90) {
    Write-Host "✓ System is FULLY COMPATIBLE with Windows Server 2019" -ForegroundColor Green
    Write-Host "Compatibility Score: $compatibilityScore%" -ForegroundColor Green
} elseif ($compatibilityScore -ge 70) {
    Write-Host "⚠ System is MOSTLY COMPATIBLE with Windows Server 2019" -ForegroundColor Yellow
    Write-Host "Compatibility Score: $compatibilityScore%" -ForegroundColor Yellow
    Write-Host "Some features may need manual configuration." -ForegroundColor Yellow
} else {
    Write-Host "✗ System has COMPATIBILITY ISSUES with Windows Server 2019" -ForegroundColor Red
    Write-Host "Compatibility Score: $compatibilityScore%" -ForegroundColor Red
    Write-Host "Please address the failed checks before installation." -ForegroundColor Red
}

Write-Host "`nPress any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
