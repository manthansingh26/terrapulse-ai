@echo off
REM TerraPulse AI - FastAPI Backend Startup Script (Windows)

echo.
echo =========================================
echo   TerraPulse AI - FastAPI Backend
echo =========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://www.python.org
    pause
    exit /b 1
)

echo [1/3] Checking Python version...
python --version

REM Check if venv exists
if not exist "venv" (
    echo.
    echo [2/3] Creating virtual environment...
    python -m venv venv
) else (
    echo.
    echo [2/3] Virtual environment already exists
)

REM Activate venv
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install requirements
echo.
echo [3/3] Installing dependencies...
pip install -q -r requirements.txt

if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

REM Run the server
echo.
echo =========================================
echo   API Server Starting...
echo =========================================
echo.
echo URL: http://localhost:8000
echo API Docs: http://localhost:8000/api/docs
echo ReDoc: http://localhost:8000/api/redoc
echo.
echo Press CTRL+C to stop the server
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
