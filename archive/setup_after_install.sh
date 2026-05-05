#!/bin/bash

# ===================================================
# TerraPulse-AI Complete Setup Script (macOS/Linux)
# Run this AFTER installing Python, Node.js, and PostgreSQL
# ===================================================

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║   TerraPulse-AI - Complete Setup Automation           ║"
echo "║        For macOS/Linux after PC reset                 ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Check if required software is installed
echo "[STEP 1] Checking for required software..."
echo ""

if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found! Please install Python first."
    exit 1
fi
echo "✅ Python found"
python3 --version

if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found! Please install Node.js first."
    exit 1
fi
echo "✅ Node.js found"
node --version

if ! command -v psql &> /dev/null; then
    echo "⚠️  PostgreSQL not found in PATH (may still work)"
else
    echo "✅ PostgreSQL found"
    psql --version
fi

echo ""
echo "[STEP 2] Creating Python virtual environment for backend..."
cd backend
python3 -m venv venv
echo "✅ Virtual environment created"

echo ""
echo "[STEP 3] Activating virtual environment and installing Python packages..."
source venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Backend packages installed"

echo ""
echo "[STEP 4] Installing frontend packages..."
cd ../frontend
npm install
echo "✅ Frontend packages installed"

echo ""
echo "[STEP 5] Creating .env file from template..."
cd ..
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cat > .env << 'EOF'
# Database Configuration
DATABASE_URL=postgresql://postgres:2601@localhost:5432/terrapulse_db

# JWT Configuration
JWT_SECRET_KEY=your-secret-key-change-this-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Keys
WAQI_API_KEY=demo
OPENWEATHER_API_KEY=your-key-here

# Frontend Configuration
VITE_API_URL=http://localhost:8000/api

# Debug Mode
DEBUG=True
EOF
    echo "✅ .env file created"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "[STEP 6] Initialization complete!"
echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║           🎉 Setup Complete! 🎉                      ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo ""
echo "1. CREATE DATABASE in PostgreSQL:"
echo "   - Open Terminal"
echo "   - Run: psql -U postgres -h localhost"
echo "   - Enter password: 2601"
echo "   - Run: CREATE DATABASE terrapulse_db;"
echo "   - Run: \q to exit"
echo ""
echo "2. INITIALIZE DATABASE:"
echo "   - Run: cd backend"
echo "   - Run: source venv/bin/activate"
echo "   - Run: python reset_db.py"
echo ""
echo "3. START BACKEND (in Terminal 1):"
echo "   - Run: cd backend"
echo "   - Run: source venv/bin/activate"
echo "   - Run: python -m uvicorn app.main:app --reload"
echo ""
echo "4. START FRONTEND (in Terminal 2):"
echo "   - Run: cd frontend"
echo "   - Run: npm run dev"
echo ""
echo "5. OPEN BROWSER:"
echo "   - Frontend: http://localhost:3000"
echo "   - Backend API: http://localhost:8000"
echo "   - Swagger Docs: http://localhost:8000/api/docs"
echo ""
echo "═════════════════════════════════════════════════════════"
echo "For detailed instructions, see: COMPLETE_INSTALLER_GUIDE.md"
echo "═════════════════════════════════════════════════════════"
echo ""
