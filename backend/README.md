# TerraPulse AI - FastAPI Backend

Production-grade REST API backend for TerraPulse AI environmental monitoring system.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Edit `.env` file with your settings:
- Database credentials (already configured for localhost)
- Secret key for JWT (change in production!)
- API keys (WAQI, OpenWeatherMap)

### 3. Run the Backend

```bash
# Development (with auto-reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or use Python directly
python -m uvicorn app.main:app --reload
```

Backend will be available at: **http://localhost:8000**

### 4. Access API Documentation

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## 📋 API Endpoints

### Authentication (`/api/auth`)
- `POST /register` - Register new user
- `POST /login` - Login user (get JWT token)
- `POST /refresh` - Refresh access token
- `GET /me` - Get current user info

### Environmental Data (`/api/data`)
- `POST /save` - Save environmental data (requires auth)
- `GET /latest/{city}` - Get latest data for city
- `GET /history/{city}` - Get historical data (default: 7 days)
- `GET /statistics/{city}` - Get statistics for city
- `GET /air-quality/{city}` - Get air quality history
- `GET /all/latest` - Get latest data for all cities
- `DELETE /clear-old-data` - Clear old data (admin only)

### Cities (`/api/cities`)
- `GET /all` - Get data for all 20 cities
- `GET /{city}` - Get data for specific city
- `GET /coordinates/all` - Get coordinates for all cities

### Health (`/`)
- `GET /` - Root endpoint
- `GET /api/health` - Health check with database status
- `GET /api/status` - Detailed status

## 🔐 Authentication

### How to Get JWT Token

1. **Register a new user**:
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "password": "securepassword123"
  }'
```

2. **Login to get token**:
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "securepassword123"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

3. **Use token in requests**:
```bash
curl -X GET "http://localhost:8000/api/data/latest/Ahmedabad" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 📊 Database Schema

### Users Table
- `id` (Integer, Primary Key)
- `email` (String, Unique)
- `username` (String, Unique)
- `full_name` (String, Optional)
- `hashed_password` (String)
- `is_active` (Boolean)
- `is_admin` (Boolean)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### Environmental Data Table
- `id` (Integer, Primary Key)
- `city` (String, Indexed)
- `aqi` (Integer)
- `co2` (Float)
- `temperature` (Float)
- `humidity` (Float)
- `wind_speed` (Float)
- `rainfall` (Float)
- `timestamp` (DateTime, Indexed)

### Air Quality History Table
- `id` (Integer, Primary Key)
- `city` (String, Indexed)
- `aqi` (Integer)
- `co2` (Float)
- `pm25` (Float)
- `pm10` (Float)
- `timestamp` (DateTime, Indexed)

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints/
│   │       ├── __init__.py
│   │       ├── auth.py         # Authentication endpoints
│   │       ├── data.py         # Data endpoints
│   │       └── cities.py       # Cities endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Configuration management
│   │   └── security.py         # JWT & authentication
│   ├── db/
│   │   ├── __init__.py
│   │   └── database.py         # Database connection & session
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py           # SQLAlchemy models
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── schemas.py          # Pydantic schemas
│   └── utils/
│       └── __init__.py
├── requirements.txt             # Python dependencies
├── .env                         # Configuration file
└── README.md                    # This file
```

## 🧪 Testing

Run tests with pytest:

```bash
pytest
```

## 🔧 Configuration

All settings are in `.env` file:

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | postgres://... | PostgreSQL connection string |
| `SECRET_KEY` | your-secret-key | JWT secret (change in production!) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | 30 | JWT expiration time |
| `WAQI_API_TOKEN` | demo | Air Quality API token |
| `OPENWEATHERMAP_API_KEY` | - | Weather API key |
| `REDIS_ENABLED` | False | Enable Redis caching |
| `DEBUG` | False | Debug mode |

## 🐳 Docker

Build and run with Docker:

```bash
# Build image
docker build -t terrapulse-backend .

# Run container
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@db:5432/db \
  terrapulse-backend
```

## 📝 Features

✅ **JWT Authentication** - Secure token-based auth
✅ **PostgreSQL** - Robust relational database
✅ **Connection Pooling** - Efficient database connections
✅ **Comprehensive Logging** - Track all operations
✅ **Error Handling** - Graceful error responses
✅ **API Documentation** - Auto-generated Swagger docs
✅ **CORS Support** - Frontend integration ready
✅ **Admin Panel** - Admin-only operations
✅ **City Data** - 20 Indian cities tracked

## 🚧 Next Steps

- [ ] Add email verification
- [ ] Implement password reset
- [ ] Add two-factor authentication
- [ ] Create admin dashboard
- [ ] Add role-based access control (RBAC)
- [ ] Implement API rate limiting
- [ ] Add request/response caching
- [ ] Setup comprehensive logging/monitoring

## 📞 Support

For issues or questions, please create an issue on GitHub.

---

**Built with ❤️ using FastAPI**
