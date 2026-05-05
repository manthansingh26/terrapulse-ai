@echo off
REM ===================================================
REM TerraPulse-AI Verification & Health Check Script
REM Run this after starting the application
REM ===================================================

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║   TerraPulse-AI Verification & Health Check           ║
echo ╚════════════════════════════════════════════════════════╝
echo.

setlocal enabledelayedexpansion
set passed=0
set failed=0

echo [CHECK 1] Python Installation
echo ────────────────────────────────
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ FAILED: Python not found
    set /a failed+=1
) else (
    echo ✅ PASSED: Python installed
    python --version
    set /a passed+=1
)
echo.

echo [CHECK 2] Node.js Installation
echo ────────────────────────────────
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ FAILED: Node.js not found
    set /a failed+=1
) else (
    echo ✅ PASSED: Node.js installed
    node --version
    set /a passed+=1
)
echo.

echo [CHECK 3] npm Package Manager
echo ────────────────────────────────
npm --version >nul 2>&1
if errorlevel 1 (
    echo ❌ FAILED: npm not found
    set /a failed+=1
) else (
    echo ✅ PASSED: npm installed
    npm --version
    set /a passed+=1
)
echo.

echo [CHECK 4] PostgreSQL Installation
echo ────────────────────────────────
psql --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  WARNING: psql not in PATH (may still be installed)
) else (
    echo ✅ PASSED: PostgreSQL installed
    psql --version
    set /a passed+=1
)
echo.

echo [CHECK 5] Python Backend Folder
echo ────────────────────────────────
if exist backend\requirements.txt (
    echo ✅ PASSED: backend folder found
    set /a passed+=1
) else (
    echo ❌ FAILED: backend folder or requirements.txt missing
    set /a failed+=1
)
echo.

echo [CHECK 6] Frontend Folder
echo ────────────────────────────────
if exist frontend\package.json (
    echo ✅ PASSED: frontend folder found
    set /a passed+=1
) else (
    echo ❌ FAILED: frontend folder or package.json missing
    set /a failed+=1
)
echo.

echo [CHECK 7] Python Virtual Environment
echo ────────────────────────────────
if exist backend\venv\Scripts\activate.bat (
    echo ✅ PASSED: Virtual environment created
    set /a passed+=1
) else (
    echo ⚠️  WARNING: Virtual environment not found (run SETUP_AFTER_INSTALL.bat)
)
echo.

echo [CHECK 8] Backend Dependencies
echo ────────────────────────────────
if exist backend\venv\Lib\site-packages\fastapi (
    echo ✅ PASSED: FastAPI installed
    set /a passed+=1
) else (
    echo ⚠️  WARNING: FastAPI not found in venv (run SETUP_AFTER_INSTALL.bat)
)
echo.

echo [CHECK 9] Frontend Dependencies
echo ────────────────────────────────
if exist frontend\node_modules\react (
    echo ✅ PASSED: npm dependencies installed
    set /a passed+=1
) else (
    echo ⚠️  WARNING: node_modules not found (run: cd frontend ^&^& npm install)
)
echo.

echo [CHECK 10] Environment Configuration
echo ────────────────────────────────
if exist .env (
    echo ✅ PASSED: .env file found
    set /a passed+=1
) else (
    echo ⚠️  WARNING: .env file not found (will be created by SETUP_AFTER_INSTALL.bat)
)
echo.

echo [CHECK 11] Docker Installation (Optional)
echo ────────────────────────────────
docker --version >nul 2>&1
if errorlevel 1 (
    echo ℹ️  INFO: Docker not installed (optional)
) else (
    echo ✅ PASSED: Docker installed
    docker --version
    set /a passed+=1
)
echo.

echo [CHECK 12] Git Installation (Optional)
echo ────────────────────────────────
git --version >nul 2>&1
if errorlevel 1 (
    echo ℹ️  INFO: Git not installed (optional)
) else (
    echo ✅ PASSED: Git installed
    git --version
    set /a passed+=1
)
echo.

echo ╔════════════════════════════════════════════════════════╗
echo ║              Summary of Checks                        ║
echo ╚════════════════════════════════════════════════════════╝
echo Passed: !passed!
echo Failed: !failed!
echo.

if !failed! equ 0 (
    echo ✅ ALL CRITICAL CHECKS PASSED!
    echo.
    echo You are ready to run the application:
    echo.
    echo Terminal 1 (Backend^):
    echo   cd backend
    echo   venv\Scripts\activate
    echo   python -m uvicorn app.main:app --reload
    echo.
    echo Terminal 2 (Frontend^):
    echo   cd frontend
    echo   npm run dev
    echo.
    echo Then open: http://localhost:3000
    echo.
) else (
    echo ❌ SOME CHECKS FAILED
    echo Please run COMPLETE_INSTALLER_GUIDE.md to fix issues
    echo.
)

pause
