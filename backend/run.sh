#!/bin/bash
# TerraPulse AI - FastAPI Backend Startup Script (macOS/Linux)

echo ""
echo "========================================="
echo "   TerraPulse AI - FastAPI Backend"
echo "========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed"
    echo "Please install Python 3.11+ from https://www.python.org"
    exit 1
fi

echo "[1/3] Checking Python version..."
python3 --version

# Check if venv exists
if [ ! -d "venv" ]; then
    echo ""
    echo "[2/3] Creating virtual environment..."
    python3 -m venv venv
else
    echo ""
    echo "[2/3] Virtual environment already exists"
fi

# Activate venv
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi

# Install requirements
echo ""
echo "[3/3] Installing dependencies..."
pip install -q -r requirements.txt

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

# Run the server
echo ""
echo "========================================="
echo "   API Server Starting..."
echo "========================================="
echo ""
echo "URL: http://localhost:8000"
echo "API Docs: http://localhost:8000/api/docs"
echo "ReDoc: http://localhost:8000/api/redoc"
echo ""
echo "Press CTRL+C to stop the server"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
