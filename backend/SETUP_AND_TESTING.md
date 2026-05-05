# FastAPI Backend - Setup & Testing Guide

## ✅ What We Built

### Backend Project Structure
```
backend/
├── app/
│   ├── main.py                 # FastAPI application (400+ lines)
│   ├── api/endpoints/
│   │   ├── auth.py             # Authentication (register, login, refresh)
│   │   ├── data.py             # Environmental data (CRUD, history, stats)
│   │   └── cities.py           # Cities data (20 cities, coordinates)
│   ├── core/
│   │   ├── config.py           # Configuration management
│   │   └── security.py         # JWT authentication
│   ├── db/
│   │   └── database.py         # SQLAlchemy setup, connection pooling
│   ├── models/
│   │   └── models.py           # User, EnvironmentalData, AirQualityHistory, APILog
│   └── schemas/
│       └── schemas.py          # Pydantic validation schemas (50+ schemas)
├── requirements.txt             # All dependencies (18 packages)
├── .env                         # Configuration
└── README.md                    # Full documentation
```

### Key Components Created

1. **FastAPI Application** (main.py)
   - CORS middleware configured
   - Exception handlers
   - Health check endpoints
   - Startup/shutdown events
   - Automatic Swagger documentation

2. **Authentication** (core/security.py + api/endpoints/auth.py)
   - JWT token generation
   - Password hashing (bcrypt)
   - Token refresh mechanism
   - User registration and login
   - Current user dependency injection

3. **Database** (db/database.py + models/models.py)
   - Connection pooling (10 connections, 20 overflow)
   - SQLAlchemy ORM setup
   - 4 database models: User, EnvironmentalData, AirQualityHistory, APILog
   - Automatic table creation on startup

4. **API Endpoints** (api/endpoints/)
   - **Auth** (5 endpoints): register, login, refresh, get_me
   - **Data** (8 endpoints): save, latest, history, statistics, air_quality, all_latest, clear_old_data
   - **Cities** (3 endpoints): all, individual city, coordinates

5. **Validation Schemas** (schemas/schemas.py)
   - User schemas (Register, Login, Response)
   - Environmental data schemas
   - Air quality schemas
   - City data schemas
   - Statistics schemas

## 🚀 Setup Instructions

### Step 1: Navigate to Backend Directory
```bash
cd backend
```

### Step 2: Create Virtual Environment (Optional but Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

Expected output:
```
Successfully installed fastapi-0.104.1
Successfully installed uvicorn[standard]-0.24.0
Successfully installed sqlalchemy-2.0.23
... (16 more packages)
```

### Step 4: Configure Environment
The `.env` file is already configured with:
- Database: `postgresql://postgres:2601@localhost:5432/terrapulse_db`
- Secret Key: Set to development value (change in production!)
- API Keys: WAQI and OpenWeatherMap ready

### Step 5: Start the Backend Server
```bash
# With auto-reload (development)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using Python module
python -m uvicorn app.main:app --reload
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
✅ Database tables created successfully
✅ Database connection successful
✅ FastAPI Backend initialized successfully
```

## 📊 Testing the Backend

### 1. Test Health Check (No Auth Required)
```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "2.0.0",
  "database": {
    "status": "connected",
    "database": "terrapulse_db"
  },
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

### 2. Register a New User
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "demo@example.com",
    "username": "demouser",
    "full_name": "Demo User",
    "password": "DemoPassword123"
  }'
```

Expected response:
```json
{
  "id": 1,
  "email": "demo@example.com",
  "username": "demouser",
  "full_name": "Demo User",
  "is_active": true,
  "is_admin": false,
  "created_at": "2024-01-15T10:30:45.123456"
}
```

### 3. Login (Get JWT Token)
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "demouser",
    "password": "DemoPassword123"
  }'
```

Expected response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

**Save the `access_token` value - you'll need it for authenticated requests!**

### 4. Get Current User Info
```bash
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Replace `YOUR_ACCESS_TOKEN` with the token from step 3.

### 5. Get All Cities Data
```bash
curl -X GET "http://localhost:8000/api/cities/all"
```

Expected response (array of 20 cities):
```json
[
  {
    "city": "Ahmedabad",
    "latitude": 23.0225,
    "longitude": 72.5714,
    "current_aqi": null,
    "current_temperature": null,
    "current_humidity": null,
    "aqi_status": "No Data",
    "aqi_color": "#808080",
    "last_updated": null
  },
  ...
]
```

### 6. Get Specific City Data
```bash
curl -X GET "http://localhost:8000/api/cities/Mumbai"
```

### 7. Save Environmental Data (Requires Auth)
```bash
curl -X POST "http://localhost:8000/api/data/save" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "city": "Ahmedabad",
    "aqi": 150,
    "co2": 450.5,
    "temperature": 28.5,
    "humidity": 65,
    "wind_speed": 12.3,
    "rainfall": 0
  }'
```

### 8. View API Documentation
Open browser: **http://localhost:8000/api/docs**

This opens the interactive Swagger UI where you can:
- See all endpoints
- Test endpoints directly
- See request/response schemas
- Test authentication flow

## 🔍 Swagger UI Testing (GUI)

1. Go to http://localhost:8000/api/docs
2. Click on any endpoint (e.g., "POST /api/auth/register")
3. Click "Try it out"
4. Fill in the required fields
5. Click "Execute"
6. See the response immediately

### Example Swagger Flow:
1. **POST /api/auth/register** → Create account
2. **POST /api/auth/login** → Get token
3. **Copy `access_token`**
4. Click "Authorize" button (top right)
5. Paste: `Bearer YOUR_TOKEN`
6. Now test authenticated endpoints!

## 📝 Key Endpoints Summary

| Endpoint | Method | Auth | Purpose |
|----------|--------|------|---------|
| `/api/health` | GET | ❌ | Health check |
| `/api/auth/register` | POST | ❌ | Create account |
| `/api/auth/login` | POST | ❌ | Login, get token |
| `/api/auth/me` | GET | ✅ | Get user info |
| `/api/cities/all` | GET | ❌ | All 20 cities |
| `/api/cities/{city}` | GET | ❌ | Single city |
| `/api/data/save` | POST | ✅ | Save data |
| `/api/data/latest/{city}` | GET | ❌ | Latest data |
| `/api/data/history/{city}` | GET | ❌ | Historical data |
| `/api/data/statistics/{city}` | GET | ❌ | City stats |

## ✨ Features Implemented

✅ **JWT Authentication**
- User registration with email validation
- Secure password hashing (bcrypt)
- JWT token generation and validation
- Token refresh mechanism
- Role-based access (admin only endpoints)

✅ **API Endpoints**
- 18 total endpoints across 3 routers
- Proper HTTP status codes
- Input validation with Pydantic
- Comprehensive error handling

✅ **Database**
- PostgreSQL connection pooling
- 4 SQLAlchemy models
- Automatic table creation
- Data persistence

✅ **Documentation**
- Auto-generated Swagger UI
- ReDoc documentation
- Comprehensive docstrings
- Example schemas

✅ **Production Ready**
- CORS middleware
- Logging throughout
- Environment configuration
- Exception handling
- Startup/shutdown events

## 🎯 Next Phase

Now that the backend is complete, we can:

1. **Test Backend Integration** with existing database
2. **Create React Frontend** to consume these APIs
3. **Setup Docker** for containerization
4. **Deploy to Cloud** (AWS/Azure)

## 🐛 Troubleshooting

### "Connection refused" error?
- Check PostgreSQL is running: `psql -U postgres -d terrapulse_db`
- Verify DATABASE_URL in .env file
- Check port 5432 is available

### "Module not found" error?
- Activate virtual environment first
- Run: `pip install -r requirements.txt`

### "Port 8000 already in use"?
- Use different port: `uvicorn app.main:app --port 8001`
- Or kill process: `lsof -i :8000` then `kill -9 <PID>`

### JWT Token not working?
- Make sure token is from /api/auth/login
- Include "Bearer" prefix: `Authorization: Bearer TOKEN`
- Check token hasn't expired (30 minutes default)

## 📚 Documentation

- Full API docs at: http://localhost:8000/api/docs
- Backend README: [README.md](README.md)
- Main app: [app/main.py](app/main.py)
- Models: [app/models/models.py](app/models/models.py)
- Schemas: [app/schemas/schemas.py](app/schemas/schemas.py)

---

**FastAPI Backend Setup Complete! ✅**

Ready to move to React Frontend? Let's go! 🚀
