# Phase 2.3 Quick Reference - Docker & CI/CD Deployment

## 🚀 Getting Started - 30 Second Setup

### Windows
```bash
.\startup-dev.bat
```

### Linux/Mac
```bash
chmod +x startup-dev.sh
./startup-dev.sh
```

That's it! Everything starts automatically.

---

## 📍 Service URLs

| Service | URL | Credentials |
|---------|-----|-------------|
| Frontend | http://localhost:3000 | N/A |
| Backend API | http://localhost:8000 | N/A |
| API Swagger | http://localhost:8000/api/docs | N/A |
| API ReDoc | http://localhost:8000/api/redoc | N/A |
| PgAdmin | http://localhost:5050 | admin@example.com / admin |
| Redis | localhost:6379 | N/A |

---

## 🧪 Testing the Setup

### 1. Check Backend Health
```bash
curl http://localhost:8000/api/health
```
Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2026-04-18T10:30:00Z"
}
```

### 2. Check Frontend
Open browser: http://localhost:3000
- Should see login page
- Try demo credentials (if available)

### 3. Test Database Connection
```bash
# Access PostgreSQL
docker-compose exec postgres psql -U postgres -d terrapulse_db

# Check tables
\dt

# Exit
\q
```

### 4. View All Service Logs
```bash
# See everything happening
docker-compose logs -f

# Or specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

---

## 📦 Docker Commands Reference

### Check Running Services
```bash
docker-compose ps
```

### View Service Status
```bash
docker-compose ps --services
```

### Check Resource Usage
```bash
docker stats
```

### Restart a Service
```bash
docker-compose restart backend
docker-compose restart frontend
docker-compose restart postgres
```

### Stop All Services (Keep Data)
```bash
docker-compose down
```

### Stop All Services (Delete Data)
```bash
docker-compose down -v
```

### Rebuild Images
```bash
docker-compose build --no-cache
```

### Run a Command in Container
```bash
# Python shell in backend
docker-compose exec backend python

# NPM command in frontend
docker-compose exec frontend npm list

# PostgreSQL shell
docker-compose exec postgres psql -U postgres -d terrapulse_db
```

---

## 🔧 Common Tasks

### View Backend Logs
```bash
docker-compose logs -f backend --tail=100
```

### Access Backend Container
```bash
docker-compose exec backend bash
```

### Database Backup
```bash
docker-compose exec postgres pg_dump -U postgres terrapulse_db > backup.sql
```

### Database Restore
```bash
cat backup.sql | docker-compose exec -T postgres psql -U postgres terrapulse_db
```

### Clear Old Data
```bash
docker-compose exec backend python -c "
from app.db.database import Base, engine
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
print('Database reset!')
"
```

### Add Sample Data
```bash
docker-compose exec backend python -c "
from app.db.database import SessionLocal
from app.models.models import EnvironmentalData
from datetime import datetime

db = SessionLocal()
# Add sample data here
db.commit()
db.close()
"
```

---

## 🌐 Container Network

### Check Network
```bash
docker network ls
docker network inspect terrapulse_terrapulse-network
```

### Container DNS Names (Internal)
- Backend: http://backend:8000
- Frontend: http://frontend:3000
- Database: postgres:5432
- Redis: redis:6379

---

## 📊 Monitoring

### Real-Time Stats
```bash
docker stats --no-stream
```

### Memory Usage
```bash
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```

### Check Service Health
```bash
docker-compose exec backend curl http://localhost:8000/api/health
```

---

## 🔐 Security

### Change Database Password
Edit `.env`:
```
DB_PASSWORD=your-new-secure-password
```

Then restart:
```bash
docker-compose down -v
docker-compose up -d
```

### Change JWT Secret
Edit `.env`:
```
JWT_SECRET_KEY=your-new-secret-key
```

Restart backend:
```bash
docker-compose restart backend
```

### Change PgAdmin Credentials
Edit `docker-compose.yml`:
```yaml
pgadmin:
  environment:
    PGADMIN_DEFAULT_EMAIL: newemail@example.com
    PGADMIN_DEFAULT_PASSWORD: newpassword
```

---

## 📈 Scaling

### Run Multiple Frontend Instances
```bash
docker-compose up -d --scale frontend=3
```

### Monitor Multiple Instances
```bash
docker ps
docker stats
```

---

## 🚨 Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000  # Mac/Linux
netstat -ano | findstr :8000  # Windows

# Kill process or use different port
docker-compose -f docker-compose.yml -p myapp up -d
```

### Container Won't Start
```bash
# Check logs
docker-compose logs backend

# Try rebuild
docker-compose build --no-cache backend

# Full reset
docker-compose down -v
docker-compose up -d
```

### Database Connection Failed
```bash
# Check database logs
docker-compose logs postgres

# Verify database is running
docker-compose exec postgres pg_isready -U postgres

# Restart database
docker-compose restart postgres
```

### Out of Memory
```bash
# Check memory usage
docker stats

# Remove unused images/containers
docker image prune
docker container prune
docker volume prune
```

### Slow Performance
```bash
# Check CPU/Memory
docker stats

# Check logs for errors
docker-compose logs

# Increase Docker resources (Settings > Resources)
```

---

## 📋 CI/CD GitHub Actions

### Workflow Triggers
- ✅ Push to `main` or `develop`
- ✅ Pull requests to `main` or `develop`
- ✅ Manual trigger via GitHub UI

### What Gets Tested
1. Backend (Python)
   - Linting (flake8)
   - Formatting (black)
   - Tests (pytest)
   - Coverage report

2. Frontend (TypeScript)
   - Lint checks
   - Type checking
   - Build verification

3. Docker
   - Build backend image
   - Build frontend image
   - Push to Docker Hub (on main/develop)

4. Security
   - Trivy vulnerability scan
   - SARIF report

### View CI/CD Status
- GitHub: Actions tab → Workflows
- Check specific commit: green ✅ or red ❌

### View Test Failures
1. Click on failed workflow
2. See detailed logs
3. Fix code locally
4. Push again

---

## 🎯 Production Deployment

### Using production-compose
```bash
# Setup .env with production values
docker-compose -f docker-compose.prod.yml up -d
```

### Using startup script
```bash
./startup-prod.sh
```

### Check Production Status
```bash
docker-compose -f docker-compose.prod.yml ps
docker-compose -f docker-compose.prod.yml logs
```

---

## 🆘 Quick Help

### All Services Down?
```bash
docker-compose restart
```

### Need Fresh Start?
```bash
docker-compose down -v  # Delete everything
docker-compose up -d    # Start fresh
```

### Need Specific Service Logs?
```bash
docker-compose logs SERVICE_NAME -f --tail=50
```

### Port Issues?
```bash
# List all port mappings
docker-compose ps

# Use different ports
docker-compose -f docker-compose.yml -p custom_name up -d
```

---

## 📞 Environment Variables

In `.env` file:

```bash
# Database
DB_PASSWORD=2601
DATABASE_URL=postgresql://postgres:2601@postgres:5432/terrapulse_db

# Authentication
JWT_SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# APIs
WAQI_API_KEY=demo
OPENWEATHER_API_KEY=your-key

# Cache
REDIS_URL=redis://redis:6379/0

# Debug
DEBUG=False

# Frontend
VITE_API_URL=http://localhost:8000/api
```

---

## ✅ Checklist Before Production

- [ ] Docker images built successfully
- [ ] All services healthy (docker-compose ps)
- [ ] Database connected
- [ ] Backend health check passing
- [ ] Frontend loads
- [ ] API documentation accessible
- [ ] CI/CD pipeline passing
- [ ] Environment variables configured
- [ ] Passwords changed from defaults
- [ ] Secrets not in version control
- [ ] Backups configured
- [ ] Monitoring setup
- [ ] Logs accessible

---

**Get Help:**
- Docs: DOCKER_DEPLOYMENT_GUIDE.md
- Logs: `docker-compose logs -f`
- Status: `docker-compose ps`

**Ready to deploy!** 🚀
