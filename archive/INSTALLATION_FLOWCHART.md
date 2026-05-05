# TerraPulse-AI Installation Flow Diagram

## 📊 Installation Process Overview

```
┌─────────────────────────────────────────────────────────────────┐
│           PHASE 0: PRE-INSTALLATION PREPARATION                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Save project folder to cloud/external drive               │
│  2. Print QUICK_REFERENCE.md for reference                    │
│  3. Perform PC reset                                           │
│  4. Extract/restore project folder after reset                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ⬇️
┌─────────────────────────────────────────────────────────────────┐
│              PHASE 1: INSTALL REQUIRED SOFTWARE                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │ Tier 1: ESSENTIAL (Must Install)                      │   │
│  ├────────────────────────────────────────────────────────┤   │
│  │ 1️⃣  Python 3.11+                                       │   │
│  │    ✅ https://www.python.org/downloads/                │   │
│  │    ⚠️  Check "Add Python to PATH"                      │   │
│  │                                                        │   │
│  │ 2️⃣  Node.js LTS (v20+)                                 │   │
│  │    ✅ https://nodejs.org/                              │   │
│  │    ℹ️  npm included automatically                       │   │
│  │                                                        │   │
│  │ 3️⃣  PostgreSQL 15                                      │   │
│  │    ✅ https://www.postgresql.org/download/             │   │
│  │    🔑 Password: 2601 (WRITE THIS DOWN!)                │   │
│  │    🔑 Port: 5432 (default)                             │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │ Tier 2: RECOMMENDED                                   │   │
│  ├────────────────────────────────────────────────────────┤   │
│  │ 4️⃣  Git                                                │   │
│  │    ✅ https://git-scm.com/download/win                 │   │
│  │                                                        │   │
│  │ 5️⃣  VS Code                                            │   │
│  │    ✅ https://code.visualstudio.com/                   │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │ Tier 3: OPTIONAL                                      │   │
│  ├────────────────────────────────────────────────────────┤   │
│  │ 6️⃣  Docker Desktop                                     │   │
│  │    ✅ https://www.docker.com/products/docker-desktop   │   │
│  │    💡 Makes deployment easy                            │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ⬇️
                         [Restart PC]
                              ⬇️
┌─────────────────────────────────────────────────────────────────┐
│           PHASE 2: VERIFY INSTALLATIONS (Optional)             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Open Command Prompt and run:                                 │
│                                                                 │
│  python --version          ✅ Should show 3.11+               │
│  node --version            ✅ Should show v20+                │
│  npm --version             ✅ Should show version             │
│  psql --version            ✅ Should show v15                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ⬇️
┌─────────────────────────────────────────────────────────────────┐
│         PHASE 3: AUTOMATED PROJECT SETUP (Recommended)        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Open Command Prompt                                       │
│  2. Navigate to project folder: cd terrapulse-ai              │
│  3. Run automation script:                                    │
│                                                                 │
│     ╔══════════════════════════════════════════════════╗     │
│     ║  SETUP_AFTER_INSTALL.bat                         ║     │
│     ╚══════════════════════════════════════════════════╝     │
│                                                                 │
│  This script will:                                            │
│  ✅ Check all installations                                   │
│  ✅ Create Python virtual environment                         │
│  ✅ Install all Python packages (backend)                     │
│  ✅ Install all npm packages (frontend)                       │
│  ✅ Create .env configuration file                            │
│  ✅ Display next steps                                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ⬇️
┌─────────────────────────────────────────────────────────────────┐
│           PHASE 4: DATABASE SETUP (Manual - 2 minutes)        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Open Command Prompt                                       │
│  2. Run: psql -U postgres -h localhost                        │
│  3. Enter password: 2601                                      │
│  4. Copy-paste this command:                                  │
│                                                                 │
│     CREATE DATABASE terrapulse_db;                            │
│                                                                 │
│  5. Exit with: \q                                             │
│                                                                 │
│  ✅ Database created!                                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ⬇️
┌─────────────────────────────────────────────────────────────────┐
│           PHASE 5: FINAL VERIFICATION (Optional)              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Run health check:                                            │
│                                                                 │
│  ╔══════════════════════════════════════════════════╗        │
│  ║  VERIFY_INSTALLATION.bat                         ║        │
│  ╚══════════════════════════════════════════════════╝        │
│                                                                 │
│  This checks:                                                 │
│  ✅ Python installation                                       │
│  ✅ Node.js installation                                      │
│  ✅ npm packages                                              │
│  ✅ PostgreSQL installation                                   │
│  ✅ Project folders exist                                     │
│  ✅ Virtual environment created                               │
│  ✅ Backend packages installed                                │
│  ✅ Frontend packages installed                               │
│  ✅ .env file created                                         │
│  ✅ Docker (if installed)                                     │
│  ✅ Git (if installed)                                        │
│                                                                 │
│  Result: Shows passes and failures                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ⬇️
┌─────────────────────────────────────────────────────────────────┐
│        PHASE 6: RUN THE APPLICATION (3 Terminals)             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Terminal 1: BACKEND                                          │
│  ───────────────────────────────────────────────────────────  │
│  cd backend                                                   │
│  venv\Scripts\activate                                        │
│  python -m uvicorn app.main:app --reload                      │
│                                                                 │
│  🎯 Backend runs at: http://localhost:8000                    │
│  📚 Swagger Docs: http://localhost:8000/api/docs              │
│                                                                 │
│  Terminal 2: FRONTEND                                         │
│  ───────────────────────────────────────────────────────────  │
│  cd frontend                                                  │
│  npm run dev                                                  │
│                                                                 │
│  🎯 Frontend runs at: http://localhost:3000                   │
│                                                                 │
│  Terminal 3 (Optional): DATABASE                              │
│  ───────────────────────────────────────────────────────────  │
│  cd backend                                                   │
│  python reset_db.py                                           │
│                                                                 │
│  💾 Initializes database with sample data                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              ⬇️
┌─────────────────────────────────────────────────────────────────┐
│        PHASE 7: ACCESS THE APPLICATION                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🌐 Open Browser:                                              │
│                                                                 │
│  Frontend Dashboard:                                          │
│  📍 http://localhost:3000                                     │
│                                                                 │
│  API Documentation:                                           │
│  📍 http://localhost:8000/api/docs                            │
│                                                                 │
│  Health Check:                                                │
│  📍 http://localhost:8000/api/health                          │
│                                                                 │
│  Test Credentials:                                            │
│  👤 Username: admin or user@example.com                       │
│  🔐 Password: Check backend README for test users             │
│                                                                 │
│  ✅ Application is LIVE! 🎉                                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Alternative: Docker Automatic Setup (Single Command)

```
If you installed Docker:

┌──────────────────────────────────────┐
│ cd terrapulse-ai                     │
│ docker-compose up -d                 │
└──────────────────────────────────────┘
         ⬇️
┌──────────────────────────────────────────────────────────┐
│  Services automatically start:                          │
│                                                         │
│  🌐 Frontend:    http://localhost:3000                 │
│  ⚙️  Backend:     http://localhost:8000                │
│  💾 Database:    localhost:5432                        │
│  🔧 PgAdmin:     http://localhost:5050                 │
│  📦 Redis:       localhost:6379                        │
│                                                         │
└──────────────────────────────────────────────────────────┘
```

---

## 📊 Time Breakdown

```
┌─────────────────────────────────────────────────────┐
│ Installation Time Estimate                         │
├─────────────────────────────────────────────────────┤
│                                                    │
│ Download All Software:        30 minutes          │
│ Install Python:                10 minutes          │
│ Install Node.js:               10 minutes          │
│ Install PostgreSQL:            15 minutes          │
│ Install Git (optional):        5 minutes           │
│ Install VS Code (optional):    10 minutes          │
│ Restart PC:                    5 minutes           │
│ Run SETUP_AFTER_INSTALL.bat:   10 minutes          │
│ Create Database:               5 minutes           │
│ Verify Installation:           5 minutes           │
│ Start Backend & Frontend:      5 minutes           │
│                                                    │
│ ────────────────────────────────────────────────── │
│ TOTAL TIME:                    ~1 hour 50 minutes  │
│                                                    │
└─────────────────────────────────────────────────────┘
```

---

## 📋 Decision Points

```
Do you want to use Docker?
    │
    ├─ YES → Skip step 1-3, install Docker, use docker-compose up
    │
    └─ NO → Follow Phases 1-7 above


Do you want to use VS Code?
    │
    ├─ YES → Install and add Python/TypeScript extensions
    │
    └─ NO → Any text editor works (Notepad++, Sublime, etc.)


Do you want to use Git?
    │
    ├─ YES → Install Git for version control
    │
    └─ NO → Can still use the application
```

---

## 🎯 Key Checkpoints

After each phase, verify:

| Phase | Check | Command |
|-------|-------|---------|
| 1 | Python installed | `python --version` |
| 1 | Node.js installed | `node --version` |
| 1 | PostgreSQL ready | `psql --version` |
| 3 | Setup completed | Check for `/backend/venv` |
| 3 | Dependencies | Check `frontend/node_modules` |
| 4 | Database | `psql -U postgres` then `\l` |
| 6 | Backend running | Open http://localhost:8000 |
| 6 | Frontend running | Open http://localhost:3000 |
| 7 | Full app | Login and navigate pages |

---

## 🚨 Common Issues & Quick Fixes

```
❌ Python not found
   → Add Python to PATH and restart Command Prompt
   → Or reinstall Python with PATH option checked

❌ npm packages fail to install
   → npm cache clean --force
   → Delete node_modules folder
   → npm install again

❌ PostgreSQL connection error
   → Check password is exactly: 2601
   → Ensure PostgreSQL service is running
   → Verify port 5432 is available

❌ Port already in use
   → Kill the process or change the port
   → See COMPLETE_INSTALLER_GUIDE.md for details

❌ Virtual environment not working
   → Delete backend/venv folder
   → Run: python -m venv venv again
   → Reactivate: venv\Scripts\activate
```

---

## 📞 Help Resources

```
📖 Documentation Files (in order):
   1. QUICK_REFERENCE.md              ← Start here!
   2. COMPLETE_INSTALLER_GUIDE.md     ← Detailed help
   3. CLAUDE.md                       ← Project info
   4. INSTALLER_PACKAGE_SUMMARY.md    ← Overview

🤖 Automation Scripts:
   1. SETUP_AFTER_INSTALL.bat         ← Setup automation
   2. VERIFY_INSTALLATION.bat         ← Health check
   3. setup_after_install.sh          ← Linux/Mac version

🌐 Online Resources:
   → Python: https://docs.python.org/3.11/
   → Node.js: https://nodejs.org/en/docs/
   → PostgreSQL: https://www.postgresql.org/docs/
   → FastAPI: https://fastapi.tiangolo.com/
   → React: https://react.dev/
```

---

**Created:** April 23, 2026  
**Status:** ✅ COMPLETE  
**Follow this diagram for guaranteed success!** ✨
