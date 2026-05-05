# Docker Deployment Guide

## Quick Start - Development

### Prerequisites
- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Docker Compose 2.0+
- 4GB RAM minimum (8GB recommended)

### Starting Development Environment

**Windows:**
```bash
.\startup-dev.bat
```

**Linux/Mac:**
```bash
chmod +x startup-dev.sh
./startup-dev.sh
```

### Services Available
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/docs
- **PgAdmin**: http://localhost:5050 (admin@example.com / admin)
- **Redis**: localhost:6379

### Common Commands

```bash
# View all services
docker-compose ps

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres

# Access backend shell
docker-compose exec backend bash

# Access database shell
docker-compose exec postgres psql -U postgres -d terrapulse_db

# Stop all services
docker-compose down

# Remove all data (fresh start)
docker-compose down -v
```

---

## Production Deployment

### Prerequisites
- Docker Engine 20.10+
- Docker Compose 2.0+
- 16GB RAM minimum
- SSL/TLS certificate (for HTTPS)
- Domain name

### Environment Setup

Create `.env` file with production values:

```bash
# Database
DB_PASSWORD=your-strong-password-here
DATABASE_URL=postgresql://postgres:your-strong-password-here@postgres:5432/terrapulse_db

# JWT Configuration
JWT_SECRET_KEY=your-super-secret-key-change-in-production-12345
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Keys
WAQI_API_KEY=your-waqi-api-key
OPENWEATHER_API_KEY=your-openweather-api-key

# Redis
REDIS_URL=redis://redis:6379/0

# Frontend
VITE_API_URL=https://yourdomain.com/api

# Debug Mode (set to False in production)
DEBUG=False
```

### Starting Production Environment

**Windows:**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

**Linux/Mac:**
```bash
chmod +x startup-prod.sh
./startup-prod.sh
```

### Health Checks

```bash
# Check all services
docker-compose -f docker-compose.prod.yml ps

# Check service health
docker-compose -f docker-compose.prod.yml exec backend curl http://localhost:8000/api/health

# View production logs
docker-compose -f docker-compose.prod.yml logs -f
```

---

## CI/CD with GitHub Actions

### Setup

1. Push to GitHub
2. Add Docker Hub credentials:
   - `DOCKER_USERNAME`
   - `DOCKER_PASSWORD`

### Workflow Triggers

Automatic on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop`

### Pipeline Steps

1. **Backend Tests**
   - Lint (flake8)
   - Format check (black)
   - Unit tests (pytest)
   - Coverage reporting

2. **Frontend Tests**
   - Lint
   - Type checking (TypeScript)
   - Build

3. **Docker Build** (main/develop only)
   - Build backend image
   - Build frontend image
   - Push to Docker Hub

4. **Security Scanning**
   - Trivy vulnerability scan
   - SARIF report to GitHub

---

## Azure Deployment (Optional)

### Using Azure Container Instances

```bash
# Create resource group
az group create --name terrapulse-rg --location eastus

# Create container registry
az acr create --resource-group terrapulse-rg \
  --name terrapulseregistry --sku Basic

# Build and push to Azure
az acr build --registry terrapulseregistry \
  --image terrapulse-backend:latest ./backend

az acr build --registry terrapulseregistry \
  --image terrapulse-frontend:latest ./frontend

# Deploy using Container Instances
az container create \
  --resource-group terrapulse-rg \
  --name terrapulse-app \
  --image terrapulseregistry.azurecr.io/terrapulse-backend:latest \
  --cpu 2 --memory 3.5 \
  --registry-login-server terrapulseregistry.azurecr.io \
  --registry-username <username> \
  --registry-password <password> \
  --ports 8000 \
  --environment-variables DATABASE_URL=... JWT_SECRET_KEY=...
```

### Using Azure App Service

1. Push images to Azure Container Registry
2. Create App Service Plan
3. Create Web App
4. Configure deployment settings
5. Enable continuous integration

---

## AWS Deployment (Optional)

### Using ECS + ECR

```bash
# Create ECR repositories
aws ecr create-repository --repository-name terrapulse-backend
aws ecr create-repository --repository-name terrapulse-frontend

# Tag and push images
aws ecr get-login-password --region us-east-1 | docker login \
  --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

docker tag terrapulse-backend:latest \
  <account-id>.dkr.ecr.us-east-1.amazonaws.com/terrapulse-backend:latest

docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/terrapulse-backend:latest

# Create ECS cluster
aws ecs create-cluster --cluster-name terrapulse-cluster

# Register task definitions and services
# (See AWS ECS documentation for detailed steps)
```

---

## Monitoring & Logging

### View Logs

```bash
# All services
docker-compose logs

# Specific service
docker-compose logs backend
docker-compose logs frontend
docker-compose logs postgres

# Follow logs in real-time
docker-compose logs -f backend

# Last 100 lines
docker-compose logs --tail=100
```

### Performance Monitoring

```bash
# CPU and memory usage
docker stats

# Detailed statistics
docker stats --no-stream
```

### Database Backups

```bash
# Backup database
docker-compose exec postgres pg_dump \
  -U postgres terrapulse_db > backup.sql

# Restore database
cat backup.sql | docker-compose exec -T postgres \
  psql -U postgres terrapulse_db
```

---

## Troubleshooting

### Port Already in Use

```bash
# Find which process is using port 8000
lsof -i :8000  # Linux/Mac
netstat -ano | findstr :8000  # Windows

# Kill the process or use different port
docker-compose -f docker-compose.yml -p myproject up -d
```

### Database Connection Failed

```bash
# Check PostgreSQL logs
docker-compose logs postgres

# Verify database is running
docker-compose exec postgres psql -U postgres -c "SELECT 1"

# Reset database
docker-compose down -v
docker-compose up -d postgres
```

### Container Won't Start

```bash
# Check container logs
docker logs <container-id>

# Inspect container
docker inspect <container-id>

# Rebuild image
docker-compose build --no-cache <service>
```

### Out of Memory

```bash
# Check Docker resource limits
docker stats

# Increase Docker memory (in Docker Desktop Settings)
# Linux: increase swap or available memory
```

---

## Security Considerations

### Best Practices

1. **Change Default Passwords**
   - Update DB_PASSWORD
   - Update JWT_SECRET_KEY
   - Update PgAdmin credentials

2. **Use HTTPS**
   - Get SSL certificate (Let's Encrypt)
   - Configure reverse proxy (Nginx)

3. **Environment Variables**
   - Never commit .env files
   - Use Docker secrets in production
   - Rotate API keys regularly

4. **Network Security**
   - Use private networks
   - Restrict port access
   - Enable firewall rules

5. **Keep Images Updated**
   - Pull latest base images regularly
   - Update dependencies
   - Use image scanning (Trivy)

---

## Scaling

### Horizontal Scaling

```yaml
# Scale frontend to 3 instances
docker-compose up -d --scale frontend=3

# Add load balancer (Nginx)
# Configure in docker-compose.yml
```

### Vertical Scaling

Increase resources in host machine:
```bash
# Linux: increase available memory/CPU
# Docker Desktop: settings > resources
```

---

## Contact & Support

For issues or questions:
- 🐛 GitHub Issues: https://github.com/yourusername/terrapulse-ai/issues
- 📧 Email: support@example.com
- 💬 Discord: [Your Discord Server]
