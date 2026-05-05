# 🚀 TerraPulse-AI Complete Installer Guide

**For use after PC reset. This guide includes all required software and step-by-step installation instructions.**

---

## 📋 System Requirements

- **OS:** Windows 10 or Windows 11
- **RAM:** 8 GB minimum (16 GB recommended)
- **Storage:** 10 GB free space
- **Internet:** Required for downloading and installing

---

## ✅ Complete List of Required Software

### **1. Python 3.11+ (REQUIRED)**
- **Download:** https://www.python.org/downloads/
- **Version:** Python 3.11 or 3.12
- **File:** python-3.11.8-amd64.exe (or latest)

### **2. Node.js & npm (REQUIRED for Frontend)**
- **Download:** https://nodejs.org/
- **Version:** LTS (Long Term Support)
- **File:** node-v20.x-x64.msi (or latest LTS)
- **Includes:** npm automatically

### **3. PostgreSQL 15 (REQUIRED for Database)**
- **Download:** https://www.postgresql.org/download/
- **Version:** PostgreSQL 15
- **File:** postgresql-15.5-1-windows-x64.exe (or latest)
- **Username:** postgres
- **Password:** 2601 (use this for the project)

### **4. Git (RECOMMENDED)**
- **Download:** https://git-scm.com/download/win
- **File:** Git-2.43.0-64-bit.exe (or latest)

### **5. Docker Desktop (OPTIONAL but Recommended)**
- **Download:** https://www.docker.com/products/docker-desktop
- **File:** Docker Desktop Installer.exe
- **Benefits:** Easy deployment and containerization

### **6. VS Code (OPTIONAL but Recommended)**
- **Download:** https://code.visualstudio.com/
- **File:** VSCodeUserSetup-x64.exe (or latest)

### **7. Redis (OPTIONAL for Caching)**
- **Download (Windows):** https://github.com/microsoftarchive/redis/releases
- **Alternative:** https://redis.io/docs/getting-started/installation/install-redis-on-windows/
- **File:** Redis-x64-3.2.100-msi.exe

---

## 🔧 Step-by-Step Installation Instructions

### **STEP 1: Install Python 3.11**

1. Download from https://www.python.org/downloads/
2. Run the installer
3. **IMPORTANT:** Check ✅ "Add Python 3.11 to PATH"
4. Choose "Install Now" or customize installation
5. Wait for completion
6. **Verify:** Open Command Prompt and run:
   ```bash
   python --version
   pip --version
   ```

---

### **STEP 2: Install Node.js & npm**

1. Download from https://nodejs.org/ (LTS version)
2. Run the installer (.msi file)
3. Follow the installation wizard
4. Accept default settings
5. Check "npm package manager" is selected
6. Complete the installation
7. **Verify:** Open Command Prompt and run:
   ```bash
   node --version
   npm --version
   ```

---

### **STEP 3: Install PostgreSQL 15**

1. Download from https://www.postgresql.org/download/
2. Run the installer
3. Follow the setup wizard:
   - **Installation Directory:** C:\Program Files\PostgreSQL\15
   - **Port:** 5432 (default)
   - **Superuser Password:** `2601` (important!)
   - **Locale:** Default
4. Complete the installation
5. **Stack Builder** may ask to install additional tools (skip for now)
6. **Verify:** Open Command Prompt and run:
   ```bash
   psql --version
   ```
7. Test connection:
   ```bash
   psql -U postgres -h localhost
   ```
   Enter password: `2601`
   Type `\q` to quit

---

### **STEP 4: Install Git (Recommended)**

1. Download from https://git-scm.com/download/win
2. Run the installer
3. Accept default settings
4. Click through the wizard
5. Complete the installation
6. **Verify:** Open Command Prompt and run:
   ```bash
   git --version
   ```

---

### **STEP 5: Install VS Code (Optional but Recommended)**

1. Download from https://code.visualstudio.com/
2. Run the installer
3. Accept license and install location
4. Complete installation
5. **Recommended Extensions:**
   - Python (Microsoft)
   - Pylance (Microsoft)
   - ES7+ React/Redux/React-Native snippets
   - Tailwind CSS IntelliSense
   - TypeScript Vue Plugin
   - GitHub Copilot (optional)

---

### **STEP 6: Install Docker Desktop (Optional but Recommended)**

1. Download from https://www.docker.com/products/docker-desktop
2. Run the installer
3. Follow the setup wizard
4. Enable "Use WSL 2 based engine" (recommended)
5. Complete the installation
6. Restart your computer
7. **Verify:** Open Command Prompt and run:
   ```bash
   docker --version
   docker run hello-world
   ```

---

### **STEP 7: Install Redis (Optional for Caching)**

**Option A: Via Chocolatey (Recommended):**
```bash
choco install redis-64
```

**Option B: Manual Download:**
1. Download from https://github.com/microsoftarchive/redis/releases
2. Run the installer
3. Accept default settings
4. Complete installation
5. **Verify:**
   ```bash
   redis-cli --version
   ```

---

## 📁 Project Setup After Installation

### **STEP 1: Clone or Copy Project**

```bash
# Option 1: If using Git
git clone <your-repo-url>
cd terrapulse-ai

# Option 2: Copy your saved project folder
```

---

### **STEP 2: Setup Backend**

```bash
# Navigate to backend folder
cd backend

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip

# Install all Python dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

---

### **STEP 3: Setup Frontend**

```bash
# Navigate to frontend folder
cd frontend

# Install all npm dependencies
npm install

# Verify installation
npm list

# (Optional) Check TypeScript compilation
npm run type-check
```

---

### **STEP 4: Setup Database**

```bash
# Connect to PostgreSQL
psql -U postgres -h localhost

# Create database (in psql terminal)
CREATE DATABASE terrapulse_db;

# Exit psql
\q

# Run database initialization (from backend folder)
cd backend
python reset_db.py
```

---

### **STEP 5: Configure Environment Variables**

Create `.env` file in root directory:

```env
# Database Configuration
DATABASE_URL=postgresql://postgres:2601@localhost:5432/terrapulse_db

# JWT Configuration
JWT_SECRET_KEY=your-secret-key-change-this-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Keys
WAQI_API_KEY=demo
OPENWEATHER_API_KEY=your-key-here

# Email Configuration (Optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password

# Redis Configuration (Optional)
REDIS_URL=redis://localhost:6379/0

# Frontend Configuration
VITE_API_URL=http://localhost:8000/api

# Debug Mode
DEBUG=True
```

---

## 🚀 Running the Application

### **Terminal 1: Start Backend**

```bash
cd backend
venv\Scripts\activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Backend will run at:** http://localhost:8000
**API Docs at:** http://localhost:8000/api/docs

---

### **Terminal 2: Start Frontend**

```bash
cd frontend
npm run dev
```

**Frontend will run at:** http://localhost:3000

---

## ✅ Verification Checklist

After installation, verify everything works:

```bash
# Python
python --version          # Should show 3.11+
pip list                  # Should show all packages

# Node.js
node --version           # Should show v20.x+
npm --version            # Should show 9.x+

# PostgreSQL
psql --version           # Should show version 15
# Connect: psql -U postgres -h localhost (password: 2601)

# Git (if installed)
git --version            # Should show 2.43+

# Backend API
curl http://localhost:8000/api/health    # Should return healthy status

# Frontend
curl http://localhost:3000               # Should return HTML
```

---

## 🔗 Important Project Files

After setup, key files to remember:

```
terrapulse-ai/
├── backend/
│   ├── requirements.txt          # Python dependencies
│   ├── app/main.py               # FastAPI entry point
│   ├── app/db/database.py         # Database connection
│   ├── run.bat                    # Run backend easily
│   └── .env                       # Backend configuration
│
├── frontend/
│   ├── package.json              # npm dependencies
│   ├── vite.config.ts            # Vite configuration
│   ├── src/App.tsx               # React entry point
│   └── src/services/api.ts       # API client
│
├── docker-compose.yml            # Docker configuration
├── .env                          # Project configuration
└── README.md                      # Project documentation
```

---

## 🐳 Docker Quick Start (Alternative to Manual Installation)

If you have Docker Desktop installed:

```bash
# In project root directory
docker-compose up -d

# This starts:
# - PostgreSQL      at localhost:5432
# - FastAPI Backend at localhost:8000
# - React Frontend  at localhost:3000
# - Redis           at localhost:6379
```

To stop:
```bash
docker-compose down
```

---

## 🆘 Troubleshooting

### **Python not found**
- Ensure "Add Python to PATH" was checked during installation
- Restart Command Prompt after installation
- Reinstall Python if needed

### **npm ERR! 404**
- Run `npm cache clean --force`
- Delete `node_modules` folder
- Run `npm install` again

### **PostgreSQL Connection Error**
- Check PostgreSQL is running: `services.msc`
- Verify password is `2601`
- Ensure port 5432 is not in use

### **Port Already in Use**
- Backend (8000): `netstat -ano | findstr :8000`
- Frontend (3000): `netstat -ano | findstr :3000`
- Kill process: `taskkill /PID <PID> /F`

### **Virtual Environment Issues**
- Delete `backend/venv` folder
- Recreate: `python -m venv venv`
- Reactivate: `venv\Scripts\activate`

---

## 📦 Summary of What Gets Installed

| Software | Purpose | Size |
|----------|---------|------|
| Python 3.11 | Backend runtime | ~100 MB |
| Node.js | Frontend runtime | ~200 MB |
| PostgreSQL 15 | Database | ~300 MB |
| Git | Version control | ~50 MB |
| VS Code | Code editor | ~200 MB |
| Docker Desktop | Containerization | ~1 GB |
| Python packages | Dependencies | ~500 MB |
| Node packages | Dependencies | ~800 MB |
| **TOTAL** | | **~3.5 GB** |

---

## 📝 Quick Reference Commands

```bash
# Python Backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload

# Node Frontend
npm install
npm run dev
npm run build

# PostgreSQL
psql -U postgres -h localhost
CREATE DATABASE terrapulse_db;

# Docker
docker-compose up -d
docker-compose down
docker ps

# Git
git clone <url>
git status
git add .
git commit -m "message"
git push
```

---

## 🎯 Next Steps After Installation

1. ✅ Install all required software (this guide)
2. ✅ Setup project files
3. ✅ Create `.env` configuration file
4. ✅ Initialize database
5. ✅ Start backend and frontend
6. ✅ Test all endpoints
7. ✅ Deploy to production (Docker)

---

## 📞 Support Resources

- **Python:** https://docs.python.org/3.11/
- **Node.js:** https://nodejs.org/en/docs/
- **PostgreSQL:** https://www.postgresql.org/docs/15/
- **FastAPI:** https://fastapi.tiangolo.com/
- **React:** https://react.dev/
- **Docker:** https://docs.docker.com/

---

**Last Updated:** April 23, 2026  
**Status:** Complete & Ready for PC Reset ✅
