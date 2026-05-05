@echo off
REM startup-dev.bat - Development environment startup script for Windows

echo 🚀 Starting TerraPulse AI - Development Environment
echo ==================================================

REM Check if Docker is running
docker info > nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not running. Please start Docker first.
    exit /b 1
)

REM Copy environment file if it doesn't exist
if not exist .env (
    echo 📝 Creating .env file from .env.docker
    copy .env.docker .env
)

REM Build images
echo 🔨 Building Docker images...
docker-compose build

REM Start services
echo 🟢 Starting services...
docker-compose up -d

REM Wait for services to be ready
echo ⏳ Waiting for services to be ready...
timeout /t 10 /nobreak

REM Check database
echo 📊 Checking database connection...
docker-compose exec -T postgres pg_isready -U postgres
if errorlevel 1 (
    echo ❌ Database connection failed
    exit /b 1
)

REM Display service URLs
echo.
echo ✅ Services are running!
echo ==================================================
echo 📱 Frontend:    http://localhost:3000
echo ⚙️  Backend API: http://localhost:8000
echo 📚 API Docs:    http://localhost:8000/api/docs
echo 🗄️  PgAdmin:    http://localhost:5050
echo 📊 Redis:       localhost:6379
echo ==================================================
echo.
echo View logs:
echo   docker-compose logs -f backend    # Backend logs
echo   docker-compose logs -f frontend   # Frontend logs
echo   docker-compose logs -f postgres   # Database logs
echo.
echo Stop services: docker-compose down
echo.
