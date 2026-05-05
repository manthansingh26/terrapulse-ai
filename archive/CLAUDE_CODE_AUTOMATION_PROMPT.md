# 🤖 Claude Code Automation Prompt
## Complete TerraPulse-AI Setup - Full Transcript

**Copy everything below and paste into Claude Code to automate setup after PC reset**

---

## 📋 FULL CLAUDE CODE PROMPT (Copy & Paste Below This Line)

```
You are an automated setup assistant for the TerraPulse-AI project. Your task is to help the user complete the full installation and setup process after a PC reset. Follow these steps exactly in order.

IMPORTANT: These steps assume the user has already installed:
- Python 3.11+ (with PATH configured)
- Node.js LTS (v20+)
- PostgreSQL 15 (with password: 2601)

STEP 1: VERIFY INSTALLATIONS
=================================
First, verify that all required software is installed. Run these commands:

1. Check Python:
   Command: python --version
   Expected: Python 3.11 or higher
   If fails: User must reinstall Python and add to PATH

2. Check Node.js:
   Command: node --version
   Expected: v20.x or higher
   If fails: User must reinstall Node.js

3. Check npm:
   Command: npm --version
   Expected: Should show a version number
   If fails: npm comes with Node.js, check Node.js installation

4. Check PostgreSQL:
   Command: psql --version
   Expected: PostgreSQL 15.x
   If fails: User must reinstall PostgreSQL

If all verification commands pass, proceed to STEP 2.


STEP 2: NAVIGATE TO PROJECT
=================================
Guide the user to navigate to their project directory:

Command: cd d:\Projects\terrapulse-ai
Then verify with: dir

Expected output: Should show backend/, frontend/, .env, SETUP_AFTER_INSTALL.bat, etc.
If not found: Ask user to restore the project folder from backup


STEP 3: CREATE PYTHON VIRTUAL ENVIRONMENT
=================================
Create the virtual environment for backend:

Commands in sequence:
1. cd backend
2. python -m venv venv
3. venv\Scripts\activate

Expected: Command prompt should show (venv) prefix
If fails: Delete backend/venv folder and retry


STEP 4: UPGRADE PIP AND INSTALL BACKEND PACKAGES
=================================
Install all Python dependencies:

Commands in sequence:
1. python -m pip install --upgrade pip
2. pip install -r requirements.txt

Wait for completion (should take 2-3 minutes)
Expected: Shows "Successfully installed" for all packages
If fails: Run "pip list" and check if key packages like fastapi, sqlalchemy exist


STEP 5: VERIFY BACKEND PACKAGES
=================================
Verify critical backend packages are installed:

Commands:
1. pip list | findstr fastapi
2. pip list | findstr sqlalchemy
3. pip list | findstr psycopg2
4. pip list | findstr pydantic

Expected: All should return package versions
If any fails: Run "pip install -r requirements.txt" again


STEP 6: NAVIGATE TO FRONTEND AND INSTALL NPM PACKAGES
=================================
Install frontend dependencies:

Commands in sequence:
1. cd ..\frontend
2. npm install

Wait for completion (should take 3-5 minutes)
Expected: Shows "added X packages" and "Y vulnerabilities"
Note: Vulnerabilities are usually minor and safe
If fails: Run "npm cache clean --force" then "npm install" again


STEP 7: VERIFY FRONTEND PACKAGES
=================================
Verify critical frontend packages are installed:

Commands:
1. npm list react
2. npm list react-router-dom
3. npm list axios

Expected: All should show version numbers
If any fails: Run "npm install" again


STEP 8: CREATE DATABASE IN POSTGRESQL
=================================
Create the main database. This requires PostgreSQL to be running.

Commands:
1. psql -U postgres -h localhost
   (When prompted, enter password: 2601)

2. Once connected (you'll see "postgres=# " prompt), run:
   CREATE DATABASE terrapulse_db;

3. Verify with:
   \l

4. Exit:
   \q

Expected: Should show "CREATE DATABASE" message and terrapulse_db in the list
If connection fails: 
  - Check PostgreSQL is running (Windows Services)
  - Verify password is exactly "2601"
  - Check port 5432 is available


STEP 9: VERIFY DATABASE CONNECTION
=================================
Test that backend can connect to database:

Commands from backend folder:
1. cd ..\backend
2. venv\Scripts\activate
3. python -c "from app.db.database import engine; engine.dispose(); print('✅ Database connection successful!')"

Expected: Shows "✅ Database connection successful!"
If fails: Check .env file has correct DATABASE_URL


STEP 10: CREATE ENV FILE (IF NOT EXISTS)
=================================
Check if .env file exists in root directory:

Commands:
1. cd ..\..
   (Go back to project root)

2. Check file:
   type .env

If .env already exists with DATABASE_URL, skip this step.

If .env doesn't exist or is empty, create it with these contents:

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


STEP 11: VERIFY .ENV FILE
=================================
Verify the .env file has correct database URL:

Commands:
1. type .env | findstr DATABASE_URL

Expected: Shows "DATABASE_URL=postgresql://postgres:2601@localhost:5432/terrapulse_db"
If missing or wrong: Edit .env and correct the DATABASE_URL


STEP 12: INITIALIZE DATABASE WITH SAMPLE DATA (OPTIONAL)
=================================
Optional: Load sample data into the database:

Commands:
1. cd backend
2. venv\Scripts\activate
3. python reset_db.py

Wait for completion
Expected: Shows "Database initialized" or similar message
If fails: Database still works, sample data just won't be loaded


STEP 13: READY FOR PRODUCTION - FINAL CHECKLIST
=================================
Verify everything is ready:

Checklist:
✅ Python virtual environment created (backend/venv exists)
✅ All Python packages installed (pip list shows all packages)
✅ All npm packages installed (frontend/node_modules exists)
✅ PostgreSQL database created (terrapulse_db exists)
✅ .env file configured (has DATABASE_URL)
✅ Database connection works (test command succeeded)
✅ Project structure intact (backend/ and frontend/ folders exist)

If all checked, ready to run the application!


STEP 14: START BACKEND SERVER
=================================
Open a NEW terminal/command prompt and run:

Commands:
1. cd d:\Projects\terrapulse-ai\backend
2. venv\Scripts\activate
3. python -m uvicorn app.main:app --reload

Expected: Shows "Uvicorn running on http://127.0.0.1:8000"
Once running, keep this terminal open

You can access:
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/api/docs
- Health Check: http://localhost:8000/api/health


STEP 15: START FRONTEND SERVER
=================================
Open ANOTHER NEW terminal/command prompt and run:

Commands:
1. cd d:\Projects\terrapulse-ai\frontend
2. npm run dev

Expected: Shows "VITE v5.x.x  ready in XXX ms" and local address like "http://localhost:5173" or "http://localhost:3000"
Once running, keep this terminal open


STEP 16: OPEN IN BROWSER
=================================
Open your web browser and navigate to:

Primary URL:
http://localhost:3000

This is your TerraPulse-AI frontend dashboard.

Available URLs:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Swagger Docs: http://localhost:8000/api/docs
- Health Check: http://localhost:8000/api/health


STEP 17: TEST LOGIN
=================================
Test the application with demo credentials:

If prompted to login:
Username: admin
Password: admin

Or try:
Email: user@example.com
Password: password

If login works: ✅ Full setup successful!
If login fails: Check backend terminal for error messages


STEP 18: VERIFY ALL ENDPOINTS
=================================
Test critical API endpoints:

Using browser or curl:

1. Health Check:
   curl http://localhost:8000/api/health

2. Get All Cities:
   curl http://localhost:8000/api/cities/all

3. Get Latest Data:
   curl http://localhost:8000/api/data/latest/Ahmedabad

4. Get All Latest:
   curl http://localhost:8000/api/data/all/latest

All should return JSON data with 200 status.


TROUBLESHOOTING GUIDE
=================================

If Python package installation fails:
- Run: pip install --upgrade pip
- Delete backend/venv folder
- Recreate: python -m venv venv
- Rerun: pip install -r requirements.txt

If npm installation fails:
- Run: npm cache clean --force
- Delete frontend/node_modules folder
- Rerun: npm install

If database connection fails:
- Check PostgreSQL service is running
- Verify password is exactly: 2601
- Check port 5432 availability
- Try: psql -U postgres -h localhost (test connection)

If port already in use:
- Backend port 8000: 
  - netstat -ano | findstr :8000
  - taskkill /PID [PID] /F
- Frontend port 3000:
  - netstat -ano | findstr :3000
  - taskkill /PID [PID] /F

If virtual environment won't activate:
- Delete backend/venv folder
- Recreate: python -m venv venv
- Try activate again: venv\Scripts\activate


SUMMARY OF COMPLETED SETUP
=================================

You have successfully:
✅ Verified all software installations
✅ Created Python virtual environment
✅ Installed all backend dependencies (18 packages)
✅ Installed all frontend dependencies
✅ Created PostgreSQL database
✅ Configured environment variables
✅ Started backend server on port 8000
✅ Started frontend server on port 3000
✅ Tested application login
✅ Verified API endpoints

Application is now LIVE and READY!

Access at: http://localhost:3000


NEXT STEPS
=================================

1. Keep both terminals running (backend and frontend)
2. You can now:
   - Create new users
   - View environmental data
   - Check air quality metrics
   - View analytics and maps
   - Access API documentation

3. To stop:
   - Press Ctrl+C in both terminals

4. To restart:
   - Rerun the commands from STEP 14 and 15


PRODUCTION DEPLOYMENT (OPTIONAL)
=================================

For deployment, you can use Docker:

If Docker installed:
1. cd d:\Projects\terrapulse-ai
2. docker-compose up -d

This will start all services automatically.

For more information, see:
- DOCKER_DEPLOYMENT_GUIDE.md
- README.md in backend/ folder
- README.md in frontend/ folder


END OF SETUP INSTRUCTIONS
=================================

Questions? Refer to:
- QUICK_REFERENCE.md (quick lookup)
- COMPLETE_INSTALLER_GUIDE.md (detailed help)
- INSTALLATION_FLOWCHART.md (visual diagram)

Setup completed successfully! 🎉
```

---

## 🎯 HOW TO USE THIS

1. **Copy everything between the triple backticks** (the prompt above)
2. **Open Claude Code** in VS Code
3. **Paste the entire prompt**
4. **Let Claude execute all steps automatically**

Claude will:
- ✅ Verify all installations
- ✅ Create virtual environment
- ✅ Install all packages
- ✅ Create database
- ✅ Configure environment
- ✅ Start both servers
- ✅ Test the application
- ✅ Provide troubleshooting

---

## ⚠️ IMPORTANT NOTES

1. **Before running this prompt:**
   - Must have Python 3.11+ installed
   - Must have Node.js installed
   - Must have PostgreSQL installed (password: 2601)
   - Project folder must be at: `d:\Projects\terrapulse-ai`

2. **Claude Code will ask for confirmation** before running dangerous commands

3. **Keep both servers running** after setup completes

4. **If anything fails**, Claude will suggest fixes

---

## 📝 ALTERNATIVE: Step-by-Step Manual

If you prefer NOT to use Claude Code automation, just run each section manually in order. The transcript is detailed enough to follow manually too.

---

**Status: Ready for Claude Code automation! 🚀**
