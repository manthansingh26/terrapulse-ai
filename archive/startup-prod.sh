#!/bin/bash
# startup-prod.sh - Production environment startup script

set -e

echo "🚀 Starting TerraPulse AI - Production Environment"
echo "=================================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if .env exists with production values
if [ ! -f .env ]; then
    echo "❌ .env file not found. Create it with production values first."
    exit 1
fi

# Build images
echo "🔨 Building Docker images..."
docker-compose -f docker-compose.prod.yml build

# Start services
echo "🟢 Starting production services..."
docker-compose -f docker-compose.prod.yml up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 15

# Check health
echo "🏥 Checking service health..."
docker-compose -f docker-compose.prod.yml ps

# Display service URLs
echo ""
echo "✅ Production services are running!"
echo "=================================================="
echo "📱 Frontend:    http://localhost:3000"
echo "⚙️  Backend API: http://localhost:8000"
echo "📚 API Docs:    http://localhost:8000/api/docs"
echo "=================================================="
echo ""
echo "View logs:"
echo "  docker-compose -f docker-compose.prod.yml logs -f"
echo ""
echo "Stop services: docker-compose -f docker-compose.prod.yml down"
