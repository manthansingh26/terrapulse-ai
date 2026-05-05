@echo off
REM TerraPulse AI - Streamlit Frontend Launcher
REM This script starts the Streamlit app

echo.
echo ====================================
echo  TerraPulse AI - Streamlit Frontend
echo ====================================
echo.

REM Check if streamlit is installed
python -m pip show streamlit >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Streamlit and dependencies...
    python -m pip install -r requirements_streamlit.txt
    if %errorlevel% neq 0 (
        echo Error: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo.
echo ✓ Starting Streamlit app on http://localhost:8501
echo.
echo Make sure the backend is running on http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo.

REM Run streamlit
python -m streamlit run app_streamlit.py

pause
