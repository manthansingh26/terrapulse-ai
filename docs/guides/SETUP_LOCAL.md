# Local Development Setup

Setup TerraPulse AI on your local machine without Docker.

## Prerequisites

### System Requirements
- **OS**: Windows, macOS, or Linux
- **RAM**: 4GB minimum (8GB recommended)
- **Disk**: 2GB available space

### Required Software

**Backend Requirements:**
```bash
# Python 3.11 or higher
python --version

# PostgreSQL 15 (or Docker PostgreSQL)
# OR: Use managed database (Cloud SQL, RDS, etc.)

# Node.js 18+ (for frontend)
node --version
npm --version
```

**Frontend Requirements:**
```bash
# Node.js 18+
node --version
npm --version
```

---

## Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/terrapulse-ai.git
cd terrapulse-ai
```

---

## Step 2: Setup Database

### Option A: Docker Database (Recommended)

```bash
# Start only PostgreSQL container
docker run --name terrapulse-db \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=terrapulse_db \
  -p 5432:5432 \
  -d postgres:15-alpine
```

### Option B: Local PostgreSQL

```bash
# Install PostgreSQL 15
# https://www.postgresql.org/download/

# Create database
createdb terrapulse_db

# Verify connection
psql -d terrapulse_db -c "SELECT 1"
```

### Option C: Managed Database

- AWS RDS
- Google Cloud SQL
- Azure Database for PostgreSQL
- DigitalOcean Managed Databases

Update `DATABASE_URL` in `.env` with your connection string.

---

## Step 3: Configure Environment

```bash
# Copy example config
cp .env.example .env

# Edit with your values (important!)
nano .env  # or use your editor
```

**Key variables to set:**
```
DB_HOST=localhost
DB_PORT=5432
DB_PASSWORD=postgres
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/terrapulse_db
JWT_SECRET_KEY=your-secret-key-here
```

---

## Step 4: Setup Backend

```bash
cd backend

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database (first time)
# This creates tables and initial data
python -c "from app.db.database import Base, engine; Base.metadata.create_all(bind=engine)"

# Start backend server
python -m uvicorn app.main:app --reload
```

**Backend should now be running on:** http://localhost:8000

Test it:
```bash
curl http://localhost:8000/api/health
# Should return: {"status":"ok",...}
```

---

## Step 5: Setup Frontend

```bash
cd frontend  # From another terminal!

# Install dependencies
npm install

# Start development server
npm run dev
```

**Frontend should now be running on:** http://localhost:3000

---

## Step 6: Access Application

Open your browser:

| Service | URL | Login |
|---------|-----|-------|
| **Frontend** | http://localhost:3000 | demo / demo123 |
| **API Docs** | http://localhost:8000/api/docs | (no login) |
| **Backend** | http://localhost:8000 | (JSON API) |

---

## ✅ Verification

### Check Backend
```bash
# In backend terminal, should see logs:
INFO:     Application startup complete
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Check Frontend
```bash
# In frontend terminal, should see:
  ➜  Local:   http://localhost:3000/
```

### Test API
```bash
curl -X GET http://localhost:8000/api/cities/all
# Should return JSON array of cities
```

### Test Database
```bash
psql -d terrapulse_db -c "SELECT COUNT(*) FROM public.user;"
```

---

## 🧪 Run Tests

### Backend Tests
```bash
cd backend
python -m pytest tests/
# or with coverage:
pytest tests/ --cov=app
```

### Frontend Tests
```bash
cd frontend
npm test
# or watch mode:
npm run test:watch
```

---

## 🐛 Common Issues & Solutions

### "Port 8000 already in use"
```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows

# Or change port in backend:
python -m uvicorn app.main:app --reload --port 8001
```

### "Database connection failed"
```bash
# Check PostgreSQL is running
psql --version

# Verify database exists
psql -l | grep terrapulse_db

# Check connection string in .env
# Test connection:
psql -U postgres -h localhost -d terrapulse_db
```

### "Module not found"
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### "Port 3000 already in use"
```bash
cd frontend
npm run dev -- --port 3001  # Use different port
```

---

## 📦 Development Dependencies

### Backend
- FastAPI 0.104.1
- SQLAlchemy 2.0
- PostgreSQL driver (psycopg2)
- Python 3.11+

### Frontend
- React 18.2
- TypeScript 5.3
- Vite 5.0
- Node.js 18+

---

## 🚀 Next Steps

### Start Development
```bash
# Backend in Terminal 1
cd backend && source venv/bin/activate && python -m uvicorn app.main:app --reload

# Frontend in Terminal 2
cd frontend && npm run dev
```

### Make Code Changes
- **Backend**: Edit `backend/app/` and changes reload automatically
- **Frontend**: Edit `frontend/src/` and changes reload automatically

### Check Code Quality
```bash
# Backend
cd backend && flake8 app/ && black app/

# Frontend
cd frontend && npm run lint && npm run format
```

---

## 📖 More Information

- **Backend Setup**: See `backend/SETUP_AND_TESTING.md`
- **Frontend Setup**: See `frontend/README.md`
- **API Documentation**: See `../api/REST_ENDPOINTS.md`
- **Troubleshooting**: See `TROUBLESHOOTING.md`

---

**Happy Developing! 🚀**
