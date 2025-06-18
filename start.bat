@echo off
echo Windows Server Management and Penetration Testing Assistant
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js 16+ from https://nodejs.org
    pause
    exit /b 1
)

echo Setting up backend...
cd backend

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r ..\requirements.txt

REM Check if .env file exists
if not exist ".env" (
    echo Creating default .env file...
    echo # Application Settings > .env
    echo DEBUG=true >> .env
    echo HOST=0.0.0.0 >> .env
    echo PORT=8000 >> .env
    echo SECRET_KEY=your-secret-key-change-in-production >> .env
    echo. >> .env
    echo # Authentication >> .env
    echo ACCESS_TOKEN_EXPIRE_MINUTES=30 >> .env
    echo ALGORITHM=HS256 >> .env
    echo. >> .env
    echo # Security Settings >> .env
    echo REQUIRE_CONFIRMATION_FOR_PRIVILEGED=true >> .env
    echo POWERSHELL_EXECUTION_POLICY=RemoteSigned >> .env
    echo MAX_COMMAND_TIMEOUT=300 >> .env
    echo. >> .env
    echo # Tool Configurations >> .env
    echo CHOCOLATEY_PATH=choco >> .env
    echo WINGET_PATH=winget >> .env
    echo.
    echo Default .env file created. Please review and update as needed.
)

echo.
echo Starting FastAPI backend server...
echo Backend will be available at: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo Default login credentials:
echo Username: admin
echo Password: admin123
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the FastAPI server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
