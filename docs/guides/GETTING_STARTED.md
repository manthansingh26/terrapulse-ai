# Quick Start Guide - 5 Minutes

Get TerraPulse AI up and running in 5 minutes!

## ⚡ The Fastest Way

### Prerequisites
- Docker & Docker Compose (or Node.js 18+ & Python 3.11+)

### Setup (< 2 minutes)

```bash
# 1. Clone & Enter directory
cd terrapulse-ai

# 2. Copy configuration
cp .env.example .env

# 3. Start everything
docker-compose up -d
```

### Access (< 1 minute)

Open in your browser:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/docs
- **Database**: http://localhost:5050 (pgadmin/admin)

### Login (< 2 minutes)

Use demo credentials:
- **Username**: `demo`
- **Password**: `demo123`

---

## ✅ Done!

You now have:
- ✅ React frontend running
- ✅ FastAPI backend running
- ✅ PostgreSQL database running
- ✅ Redis cache running
- ✅ All services healthy

---

## 🚀 What's Next?

### Explore the App
- Dashboard: See real-time environmental data
- Map: View cities on interactive map
- Analytics: Check historical trends
- Profile: View user information

### Make Your First API Call
```bash
curl http://localhost:8000/api/cities/all
```

### Start Development
```bash
# Stop containers
docker-compose down

# Start backend locally
cd backend && python -m uvicorn app.main:app --reload

# Start frontend locally (in another terminal)
cd frontend && npm run dev
```

---

## 📖 Learn More

- **Full Setup**: See [SETUP_LOCAL.md](./SETUP_LOCAL.md) or [SETUP_DOCKER.md](./SETUP_DOCKER.md)
- **API Docs**: Check [../api/REST_ENDPOINTS.md](../api/REST_ENDPOINTS.md)
- **Issues?**: See [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)

---

**That's it! You're ready to go. 🎉**
