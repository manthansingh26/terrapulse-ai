# 🚀 LAPTOP RESET - Complete Setup Guide

## 📌 Before You Reset

**SAVE THESE FILES** to an external drive or cloud storage:

```
📁 terrapulse-ai/
├── 📄 app_streamlit.py              ← Main frontend (YOUR DESIGN!)
├── 📄 requirements_streamlit.txt    ← Python dependencies
├── 📄 run_streamlit.bat             ← Windows launcher
├── 📄 run_streamlit.sh              ← Linux/Mac launcher
├── 📁 backend/                      ← All backend code
├── 📁 frontend/                     ← React code (optional)
├── 📄 .env.example                  ← Config template
└── 📄 README.md                     ← Documentation
```

**ZIP it all:**
```bash
# Windows
tar -czf terrapulse-ai-backup.tar.gz terrapulse-ai/

# Or just copy the folder to USB/Cloud
```

---

## 💾 Restore After Reset

### Step 1: Unzip Your Files
```bash
# Extract backup
tar -xzf terrapulse-ai-backup.tar.gz
cd terrapulse-ai
```

### Step 2: Install Python
- Windows: Download from python.org
- macOS: `brew install python3`
- Linux: `sudo apt install python3 python3-pip`

### Step 3: Install Dependencies
```bash
# Install all requirements
pip install -r requirements_streamlit.txt

# Verify
pip list | grep streamlit
```

### Step 4: Start Backend
**Terminal 1:**
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
# Runs on http://localhost:8000
```

### Step 5: Start Frontend
**Terminal 2:**
```bash
# From project root
python -m streamlit run app_streamlit.py

# Or use launcher script
# Windows: run_streamlit.bat
# Mac/Linux: ./run_streamlit.sh
```

### Step 6: Login & Use
```
Open: http://localhost:8501
Username: demo
Password: demo123
```

---

## ✅ Verification Checklist

After reset, verify everything works:

- [ ] Python 3.8+ installed: `python --version`
- [ ] Pip updated: `pip --version`
- [ ] Backend dependencies: `cd backend && pip install -r requirements.txt`
- [ ] Frontend dependencies: `pip install -r requirements_streamlit.txt`
- [ ] Backend runs: `python -m uvicorn app.main:app --reload`
- [ ] Frontend runs: `python -m streamlit run app_streamlit.py`
- [ ] Can login: demo/demo123
- [ ] Dashboard shows data: ✅
- [ ] City Details work: ✅
- [ ] Profile displays: ✅

---

## 🔧 Quick Reference

### URLs
```
Frontend (Streamlit):  http://localhost:8501
Backend API:           http://localhost:8000
API Swagger Docs:      http://localhost:8000/api/docs
API ReDoc:             http://localhost:8000/api/redoc
```

### Commands (Copy & Paste)

**Start Backend:**
```bash
cd backend && python -m uvicorn app.main:app --reload
```

**Start Frontend:**
```bash
python -m streamlit run app_streamlit.py
```

**Install Dependencies:**
```bash
pip install -r requirements_streamlit.txt
pip install -r backend/requirements.txt
```

**Test Backend:**
```bash
curl http://localhost:8000/api/health
```

**Change Streamlit Port:**
```bash
streamlit run app_streamlit.py --server.port 8502
```

---

## 📋 What You're Getting

### Frontend (Streamlit - YOUR DESIGN)
- **File:** `app_streamlit.py`
- **Lines:** 600+
- **Features:**
  - Authentication (Login/Register)
  - Dashboard with statistics
  - City details & analytics
  - User profile
  - Real-time charts
  - Interactive data tables

### Backend (FastAPI - UNCHANGED)
- **Location:** `backend/`
- **Features:**
  - 18+ REST endpoints
  - JWT authentication
  - Database integration
  - Data validation
  - Error handling

### Configuration
- **File:** `.env.example`
- **Copy to:** `.env`
- **Contains:** API keys, database settings, JWT secrets

---

## 🎯 File Checklist

### Must Have (Core Files)
```
✅ app_streamlit.py              - Streamlit frontend (ESSENTIAL!)
✅ requirements_streamlit.txt    - Frontend dependencies
✅ backend/app/main.py           - FastAPI entry point
✅ backend/requirements.txt      - Backend dependencies
✅ .env.example                  - Configuration template
```

### Nice to Have (Documentation)
```
✅ STREAMLIT_SETUP.md            - Detailed setup
✅ STREAMLIT_FRONTEND_RESTORED.md - What you got
✅ README.md                     - Project overview
✅ run_streamlit.bat/sh          - Quick launchers
```

### Optional (React Frontend)
```
📁 frontend/                     - React app (keep as backup)
```

---

## 🐛 If Something Goes Wrong

### Backend won't start
```bash
# Check if port is in use
netstat -ano | findstr :8000

# Kill process
taskkill /PID <PID> /F

# Try different port
python -m uvicorn app.main:app --reload --port 8001
```

### Streamlit won't start
```bash
# Reinstall
pip uninstall streamlit -y
pip install streamlit

# Clear cache
streamlit cache clear

# Try different port
streamlit run app_streamlit.py --server.port 8502
```

### Can't login
```bash
# Check backend is running on :8000
# Check API docs work: http://localhost:8000/api/docs
# Try demo/demo123
```

### Dependencies failed
```bash
# Clear pip cache
pip cache purge

# Reinstall everything
pip install --upgrade pip
pip install -r requirements_streamlit.txt --force-reinstall
```

---

## 🔄 Database (Optional)

The app **works WITHOUT database**, using mock data.

To use real database (PostgreSQL):

1. **Install PostgreSQL**
   ```bash
   # Windows: Download from postgresql.org
   # Mac: brew install postgresql
   # Linux: sudo apt install postgresql
   ```

2. **Configure Connection**
   ```bash
   # Edit .env
   DATABASE_URL=postgresql://user:password@localhost:5432/terrapulse_db
   ```

3. **Run Backend**
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload
   # It will create tables automatically
   ```

---

## 📊 Architecture After Reset

```
Your Laptop (After Reset)
│
├─── Frontend (Port 8501)
│    ├── Streamlit App
│    ├── Plotly Charts
│    ├── Data Tables
│    └── User Interface
│
├─── Backend (Port 8000)
│    ├── FastAPI Server
│    ├── REST Endpoints
│    ├── JWT Auth
│    └── Database Queries
│
└─── Database (Optional)
     └── PostgreSQL
         └── Environmental Data
```

---

## ✨ Environment Setup (Copy These Commands)

### Windows PowerShell
```powershell
# Install Python 3.11+
python --version

# Clone/Copy project
cd Documents
# Paste your backed-up terrapulse-ai folder here

# Setup
cd terrapulse-ai
pip install -r requirements_streamlit.txt
pip install -r backend/requirements.txt

# Terminal 1: Start backend
cd backend
python -m uvicorn app.main:app --reload

# Terminal 2: Start frontend
python -m streamlit run app_streamlit.py
```

### macOS/Linux Bash
```bash
# Install Python
python3 --version

# Setup
cd ~/projects  # or wherever
cd terrapulse-ai

pip3 install -r requirements_streamlit.txt
pip3 install -r backend/requirements.txt

# Terminal 1: Backend
cd backend
python3 -m uvicorn app.main:app --reload

# Terminal 2: Frontend
python3 -m streamlit run app_streamlit.py
```

---

## 🎓 Learning Resources

After setup works, explore:

1. **Frontend Code:** `app_streamlit.py`
   - Learn Streamlit architecture
   - Understand API calls
   - Modify dashboard

2. **Backend Code:** `backend/app/main.py`
   - Learn FastAPI
   - Understand endpoints
   - Database queries

3. **API Documentation:** http://localhost:8000/api/docs
   - Test endpoints
   - See request/response formats
   - Try authentication

---

## 🎊 Success Indicators

After following these steps, you should see:

✅ **Backend Output:**
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

✅ **Streamlit Output:**
```
You can now view your Streamlit app in your browser.
  
  Local URL: http://localhost:8501
```

✅ **App Working:**
- Login page loads
- Demo/demo123 works
- Dashboard shows data
- City details load
- Profile displays

---

## 📞 Support Files Included

When you restore, you'll also get:

```
📄 STREAMLIT_SETUP.md              - Detailed tech guide
📄 STREAMLIT_FRONTEND_RESTORED.md  - What's included
📄 README.md                       - Project overview
📄 CONTRIBUTING.md                 - Development guide
📄 CHANGELOG.md                    - Version history
```

Use these as reference during development!

---

## 🎯 Quick Start Template

**Copy this entire section after reset:**

```bash
# 1. Go to project
cd terrapulse-ai

# 2. Install dependencies
pip install -r requirements_streamlit.txt
pip install -r backend/requirements.txt

# 3. Open two terminals

# Terminal 1: Backend
cd backend
python -m uvicorn app.main:app --reload

# Terminal 2: Frontend
python -m streamlit run app_streamlit.py

# 4. Open browser
# Frontend: http://localhost:8501
# API Docs: http://localhost:8000/api/docs

# 5. Login
# demo / demo123

# Done! ✅
```

---

## 🛡️ Backup Strategy

**Before Reset:**
```bash
# Create backup locations
mkdir ~/backups
cp -r terrapulse-ai ~/backups/

# Or cloud storage (Google Drive, Dropbox, OneDrive)
# Sync entire terrapulse-ai folder
```

**After Reset:**
```bash
# Restore from backup
cp -r ~/backups/terrapulse-ai ~/projects/

# Verify all files present
ls -la ~/projects/terrapulse-ai/
```

---

## 📈 Next Steps

**Immediate (After Reset):**
1. ✅ Restore files
2. ✅ Install dependencies
3. ✅ Start backend
4. ✅ Start frontend
5. ✅ Login and verify

**Short Term:**
- Explore the dashboard
- Try different cities
- Check historical data
- Review profile

**Long Term:**
- Customize the design
- Add new features
- Connect real database
- Deploy to server

---

## 🎉 You're All Set!

Everything you need is documented here. After your laptop reset:

1. **Restore files from backup** ← Most important!
2. **Follow setup steps** ← Copy/paste commands
3. **Verify everything works** ← Check URLs
4. **Start developing** ← Modify as needed

**No data loss. No starting over. Just restore and run!** ✅

---

**Happy coding after your laptop reset! 🚀**

Created: April 26, 2026  
Designed for: TerraPulse AI Project  
Safety Level: Production-Ready ✅
