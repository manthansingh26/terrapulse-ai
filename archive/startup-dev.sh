#!/bin/bash
# startup-dev.sh - Development environment startup script

set -e

echo "🚀 Starting TerraPulse AI - Development Environment"
echo "=================================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Copy environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from .env.docker"
    cp .env.docker .env
fi

# Build images
echo "🔨 Building Docker images..."
docker-compose build

# Start services
echo "🟢 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check database
echo "📊 Checking database connection..."
docker-compose exec -T postgres pg_isready -U postgres || {
    echo "❌ Database connection failed"
    exit 1
}

# Initialize database if needed
echo "🗄️  Initializing database..."
docker-compose exec -T backend python -c "
from app.db.database import Base, engine
Base.metadata.create_all(bind=engine)
print('✅ Database initialized')
"

# Display service URLs
echo ""
echo "✅ Services are running!"
echo "=================================================="
echo "📱 Frontend:    http://localhost:3000"
echo "⚙️  Backend API: http://localhost:8000"
echo "📚 API Docs:    http://localhost:8000/api/docs"
echo "🗄️  PgAdmin:    http://localhost:5050"
echo "📊 Redis:       localhost:6379"
echo "=================================================="
echo ""
echo "View logs:"
echo "  docker-compose logs -f backend    # Backend logs"
echo "  docker-compose logs -f frontend   # Frontend logs"
echo "  docker-compose logs -f postgres   # Database logs"
echo ""
echo "Stop services: docker-compose down"
