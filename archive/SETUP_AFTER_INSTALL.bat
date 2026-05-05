@echo off
REM ===================================================
REM TerraPulse-AI Complete Setup Script
REM Run this AFTER installing Python, Node.js, and PostgreSQL
REM ===================================================

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║     TerraPulse-AI - Complete Setup Automation         ║
echo ║          For use after PC reset                       ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Check if required software is installed
echo [STEP 1] Checking for required software...
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python first.
    pause
    exit /b 1
) else (
    echo ✅ Python found
    python --version
)

node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js not found! Please install Node.js first.
    pause
    exit /b 1
) else (
    echo ✅ Node.js found
    node --version
)

psql --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  PostgreSQL not found in PATH (may still work)
) else (
    echo ✅ PostgreSQL found
    psql --version
)

echo.
echo [STEP 2] Creating Python virtual environment for backend...
cd backend
python -m venv venv
echo ✅ Virtual environment created

echo.
echo [STEP 3] Activating virtual environment and installing Python packages...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
echo ✅ Backend packages installed

echo.
echo [STEP 4] Installing frontend packages...
cd ..\frontend
npm install
echo ✅ Frontend packages installed

echo.
echo [STEP 5] Creating .env file from template...
cd ..
if not exist .env (
    echo Creating .env file...
    (
        echo # Database Configuration
        echo DATABASE_URL=postgresql://postgres:2601@localhost:5432/terrapulse_db
        echo.
        echo # JWT Configuration
        echo JWT_SECRET_KEY=your-secret-key-change-this-in-production
        echo JWT_ALGORITHM=HS256
        echo ACCESS_TOKEN_EXPIRE_MINUTES=30
        echo.
        echo # API Keys
        echo WAQI_API_KEY=demo
        echo OPENWEATHER_API_KEY=your-key-here
        echo.
        echo # Frontend Configuration
        echo VITE_API_URL=http://localhost:8000/api
        echo.
        echo # Debug Mode
        echo DEBUG=True
    ) > .env
    echo ✅ .env file created
) else (
    echo ✅ .env file already exists
)

echo.
echo [STEP 6] Initialization complete!
echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║           🎉 Setup Complete! 🎉                      ║
echo ╚════════════════════════════════════════════════════════╝
echo.
echo Next steps:
echo.
echo 1. CREATE DATABASE in PostgreSQL:
echo    - Open Command Prompt as Administrator
echo    - Run: psql -U postgres -h localhost
echo    - Enter password: 2601
echo    - Run: CREATE DATABASE terrapulse_db;
echo    - Run: \q to exit
echo.
echo 2. INITIALIZE DATABASE:
echo    - Run: cd backend
echo    - Run: venv\Scripts\activate
echo    - Run: python reset_db.py
echo.
echo 3. START BACKEND (in Terminal 1):
echo    - Run: cd backend
echo    - Run: venv\Scripts\activate
echo    - Run: python -m uvicorn app.main:app --reload
echo.
echo 4. START FRONTEND (in Terminal 2):
echo    - Run: cd frontend
echo    - Run: npm run dev
echo.
echo 5. OPEN BROWSER:
echo    - Frontend: http://localhost:3000
echo    - Backend API: http://localhost:8000
echo    - Swagger Docs: http://localhost:8000/api/docs
echo.
echo ═════════════════════════════════════════════════════════
echo For detailed instructions, see: COMPLETE_INSTALLER_GUIDE.md
echo ═════════════════════════════════════════════════════════
echo.

pause
