# 📌 TerraPulse-AI Quick Reference Card

## 🔗 Download Links (Save These!)

| Software | Download Link | Version |
|----------|---------------|---------|
| Python | https://www.python.org/downloads/ | 3.11+ |
| Node.js | https://nodejs.org/ | LTS (v20+) |
| PostgreSQL | https://www.postgresql.org/download/ | 15 |
| Git | https://git-scm.com/download/win | Latest |
| VS Code | https://code.visualstudio.com/ | Latest |
| Docker Desktop | https://www.docker.com/products/docker-desktop | Latest |

---

## ⚙️ Installation Order (IMPORTANT)

1. **Python 3.11+** ← Start here
2. **Node.js (with npm)** ← Second
3. **PostgreSQL 15** ← Third (password: **2601**)
4. **Git** (optional) ← Fourth
5. **VS Code** (optional) ← Fifth
6. **Docker Desktop** (optional) ← Last

---

## 🚀 After Installation Setup (Windows)

### Option 1: Automatic Setup (Recommended)
```bash
SETUP_AFTER_INSTALL.bat
```
Then run database creation steps manually.

### Option 2: Manual Setup
```bash
# Backend Setup
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Frontend Setup
cd frontend
npm install

# Create .env file
# (Use the template in COMPLETE_INSTALLER_GUIDE.md)
```

### Create Database
```bash
psql -U postgres -h localhost
CREATE DATABASE terrapulse_db;
\q
```

---

## 🖥️ Running the Application

### Terminal 1: Backend
```bash
cd backend
venv\Scripts\activate
python -m uvicorn app.main:app --reload
```
✅ Runs at: **http://localhost:8000**
📚 Docs at: **http://localhost:8000/api/docs**

### Terminal 2: Frontend
```bash
cd frontend
npm run dev
```
✅ Runs at: **http://localhost:3000**

### Terminal 3 (Optional): Database Admin
```bash
cd backend
python reset_db.py  # Or use PgAdmin
```

---

## 🔑 Important Credentials

| Item | Value |
|------|-------|
| PostgreSQL User | postgres |
| PostgreSQL Password | **2601** |
| Database Name | terrapulse_db |
| Backend Port | 8000 |
| Frontend Port | 3000 |
| Redis Port | 6379 |
| PgAdmin Port | 5050 |

---

## ✅ Verification Commands

```bash
# Python
python --version
pip list

# Node.js
node --version
npm --version

# PostgreSQL
psql --version
psql -U postgres -h localhost  # password: 2601

# Backend Status
curl http://localhost:8000/api/health

# Frontend
curl http://localhost:3000
```

---

## 📁 Project Structure After Setup

```
terrapulse-ai/
├── backend/
│   ├── venv/                    # Virtual environment
│   ├── requirements.txt
│   ├── run.bat
│   └── app/
│
├── frontend/
│   ├── node_modules/            # npm packages
│   ├── package.json
│   ├── src/
│   └── public/
│
├── .env                         # Configuration file
├── docker-compose.yml
└── COMPLETE_INSTALLER_GUIDE.md
```

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| `python: command not found` | Add Python to PATH and restart Command Prompt |
| `npm ERR! 404` | `npm cache clean --force` then `npm install` |
| `PostgreSQL error` | Check password is `2601`, port is 5432 |
| `Port already in use` | Kill process or change port |
| `Module not found` | Ensure virtual environment is activated |

---

## 🐳 Docker Alternative (One Command Setup)

```bash
# If Docker installed
docker-compose up -d

# Services:
# - Frontend:  http://localhost:3000
# - Backend:   http://localhost:8000
# - Database:  localhost:5432
# - PgAdmin:   http://localhost:5050
# - Redis:     localhost:6379

# Stop
docker-compose down
```

---

## 📋 Setup Checklist

- [ ] Downloaded all installers
- [ ] Installed Python (added to PATH)
- [ ] Installed Node.js
- [ ] Installed PostgreSQL (password: 2601)
- [ ] Installed Git (optional)
- [ ] Installed VS Code (optional)
- [ ] Copied project to new location
- [ ] Ran SETUP_AFTER_INSTALL.bat
- [ ] Created terrapulse_db database
- [ ] Created .env file
- [ ] Started backend server
- [ ] Started frontend server
- [ ] Opened http://localhost:3000 ✅

---

## 🔗 Test URLs After Starting

```
Frontend:          http://localhost:3000
Backend API:       http://localhost:8000
Swagger Docs:      http://localhost:8000/api/docs
API Health:        http://localhost:8000/api/health
PgAdmin (Docker):  http://localhost:5050
```

---

## 💾 Important Files to Save

Before PC reset, save:
- ✅ Project folder (all code)
- ✅ This quick reference
- ✅ COMPLETE_INSTALLER_GUIDE.md
- ✅ Database backup (optional)
- ✅ .env file configuration

---

## 🎓 Learning Resources

- **Python/FastAPI:** https://fastapi.tiangolo.com/
- **React/Frontend:** https://react.dev/
- **PostgreSQL:** https://www.postgresql.org/docs/
- **Docker:** https://docs.docker.com/
- **Node.js/npm:** https://docs.npmjs.com/

---

## 📞 Common Commands

```bash
# Activate virtual environment
venv\Scripts\activate              # Windows
source venv/bin/activate           # macOS/Linux

# Install packages
pip install -r requirements.txt
npm install

# Update packages
pip install --upgrade pip
npm update

# Run tests
pytest
npm run type-check

# Build for production
npm run build

# Git operations
git clone <url>
git status
git add .
git commit -m "message"
git push
```

---

## 🎯 What Gets Installed

- **Python 3.11+** - Backend runtime
- **Node.js 20+** - Frontend runtime + npm
- **PostgreSQL 15** - Database
- **18 Python packages** - Backend dependencies
- **15+ npm packages** - Frontend dependencies
- **Git** - Version control
- **Docker** - Containerization

**Total Size:** ~3-4 GB

---

## 🚨 Critical Passwords & Keys

Keep these secure! Save somewhere safe:

```
PostgreSQL Password: 2601
JWT Secret: (will be in .env)
API Keys: (will be in .env)
```

⚠️ Change `JWT_SECRET_KEY` before production!

---

**Last Updated:** April 23, 2026  
**Status:** Ready for PC Reset ✅

Print this page and keep it handy during setup!
