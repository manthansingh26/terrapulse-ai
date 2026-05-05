# Docker Setup Guide

Setup TerraPulse AI using Docker and Docker Compose.

## Why Docker?

✅ **No dependency issues** - Everything bundled  
✅ **One command startup** - `docker-compose up`  
✅ **Same on all machines** - Windows, Mac, Linux  
✅ **Easy database** - PostgreSQL included  
✅ **Production-ready** - Same setup for dev and prod  

---

## Prerequisites

### Install Docker

**Windows/Mac:**
- Download [Docker Desktop](https://www.docker.com/products/docker-desktop)
- Install and run

**Linux:**
```bash
sudo apt-get install docker.io docker-compose
sudo usermod -aG docker $USER
```

**Verify installation:**
```bash
docker --version
docker-compose --version
```

---

## Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/terrapulse-ai.git
cd terrapulse-ai
```

---

## Step 2: Configure Environment

```bash
# Copy configuration
cp .env.example .env

# Edit .env (optional - defaults work for local dev)
nano .env
```

---

## Step 3: Start Services

```bash
# Start all services in background
docker-compose up -d

# Or see logs in terminal (Ctrl+C to stop)
docker-compose up
```

**What starts:**
- ✅ **PostgreSQL** (Port 5432) - Database
- ✅ **Redis** (Port 6379) - Cache
- ✅ **FastAPI Backend** (Port 8000) - API Server
- ✅ **React Frontend** (Port 3000) - Web App
- ✅ **PgAdmin** (Port 5050) - Database UI

---

## Step 4: Access Application

Open in your browser:

| Service | URL | Credentials |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | demo / demo123 |
| **API Docs** | http://localhost:8000/api/docs | (public) |
| **ReDoc** | http://localhost:8000/api/redoc | (public) |
| **PgAdmin** | http://localhost:5050 | admin / admin |
| **Backend API** | http://localhost:8000 | (JSON API) |

---

## Useful Docker Commands

### View Status
```bash
# See running containers
docker-compose ps

# Show service details
docker-compose ps -a
```

### View Logs
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs backend
docker-compose logs frontend

# Follow logs (live)
docker-compose logs -f backend
```

### Stop Services
```bash
# Stop all
docker-compose down

# Stop specific service
docker-compose stop backend

# Stop and remove volumes (WARNING: deletes data!)
docker-compose down -v
```

### Restart Services
```bash
# Restart all
docker-compose restart

# Restart specific
docker-compose restart backend
```

### Execute Commands
```bash
# Run command in container
docker-compose exec backend python -m pytest

# Get shell in container
docker-compose exec backend /bin/bash
docker-compose exec frontend /bin/sh

# PostgreSQL shell
docker-compose exec postgres psql -U postgres -d terrapulse_db
```

---

## Development Workflow

### 1. Make Code Changes

**Backend:**
```bash
# Edit backend/app/main.py or other files
# Changes auto-reload due to volume mount
```

**Frontend:**
```bash
# Edit frontend/src/pages/Dashboard.tsx or other files
# Hot reload happens automatically via Vite
```

### 2. View Changes

**Backend Changes:**
```
http://localhost:8000/api/docs  # API docs refresh
```

**Frontend Changes:**
```
http://localhost:3000  # Automatically reloads
```

### 3. Check Logs

```bash
# See what's happening
docker-compose logs -f

# Or specific service
docker-compose logs -f backend
```

---

## Common Tasks

### Reset Database

```bash
# Stop services and remove database
docker-compose down -v

# Start fresh
docker-compose up -d

# Database will be recreated automatically
```

### Rebuild Images

```bash
# Rebuild all images
docker-compose build

# Rebuild specific service
docker-compose build backend

# Rebuild and restart
docker-compose up -d --build
```

### View Database

```bash
# Using PgAdmin: http://localhost:5050
# Or command line:
docker-compose exec postgres psql -U postgres -d terrapulse_db

# Example queries:
SELECT * FROM public.user;
SELECT COUNT(*) FROM public.environmental_data;
```

### Run Backend Tests

```bash
docker-compose exec backend python -m pytest tests/
```

### Run Frontend Tests

```bash
docker-compose exec frontend npm test
```

---

## Environment Variables

Key variables in `.env`:

```bash
# Database
DB_HOST=postgres  # Not localhost when using Docker!
DB_PASSWORD=postgres
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/terrapulse_db

# APIs
WAQI_API_KEY=demo
OPENWEATHER_API_KEY=your_key

# JWT
JWT_SECRET_KEY=your-secret-key

# Email (optional)
SMTP_EMAIL=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

---

## Production Mode

```bash
# Use production compose file
docker-compose -f docker-compose.prod.yml up -d

# Or with environment
docker-compose -f docker-compose.prod.yml up -d -e DEBUG=False
```

---

## Troubleshooting

### Port Already in Use

```bash
# On Windows
netstat -ano | findstr :8000

# On macOS/Linux
lsof -i :8000

# Kill process or change port in docker-compose.yml
```

### Container Won't Start

```bash
# Check logs
docker-compose logs backend

# Rebuild
docker-compose build --no-cache backend

# Restart
docker-compose restart backend
```

### Database Connection Failed

```bash
# Check PostgreSQL is healthy
docker-compose ps postgres

# Check logs
docker-compose logs postgres

# Verify connection string in .env
DATABASE_URL=postgresql://postgres:PASSWORD@postgres:5432/terrapulse_db
```

### Permission Denied (Linux)

```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Logout and login or:
newgrp docker
```

---

## Clean Up

```bash
# Stop and remove containers
docker-compose down

# Remove images
docker image rm terrapulse-backend terrapulse-frontend postgres:15-alpine

# Remove volumes (WARNING: deletes data!)
docker-compose down -v

# Clean everything
docker-compose down -v --remove-orphans
```

---

## Next Steps

- **Edit Code**: Make changes in `backend/app/` or `frontend/src/`
- **Run Tests**: See test commands above
- **View Logs**: `docker-compose logs -f`
- **Deploy**: See `DEPLOYMENT.md` for cloud deployment

---

**Happy Coding! 🐳**
