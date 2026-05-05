.PHONY: help install dev build prod test lint format clean docker-up docker-down docker-logs

# ============================================================================
# TerraPulse AI - Development & Production Tasks
# ============================================================================

help:
	@echo "TerraPulse AI - Makefile Commands"
	@echo "=================================="
	@echo ""
	@echo "Development:"
	@echo "  make dev              Start development environment (Docker)"
	@echo "  make dev-local        Start development locally (no Docker)"
	@echo "  make install          Install all dependencies"
	@echo ""
	@echo "Testing & Quality:"
	@echo "  make test             Run all tests"
	@echo "  make test-backend     Run backend tests"
	@echo "  make test-frontend    Run frontend tests"
	@echo "  make lint             Run linters (backend & frontend)"
	@echo "  make type-check       Run type checks (TypeScript & Python)"
	@echo "  make format           Format code (backend & frontend)"
	@echo ""
	@echo "Building:"
	@echo "  make build            Build for production"
	@echo "  make build-backend    Build backend Docker image"
	@echo "  make build-frontend   Build frontend Docker image"
	@echo ""
	@echo "Production:"
	@echo "  make prod             Start production environment"
	@echo "  make prod-logs        View production logs"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-up        Start Docker services"
	@echo "  make docker-down      Stop Docker services"
	@echo "  make docker-logs      View Docker logs"
	@echo "  make docker-clean     Remove Docker images & volumes"
	@echo ""
	@echo "Utilities:"
	@echo "  make setup            Initial setup (copy .env.example to .env)"
	@echo "  make clean            Clean all build artifacts"
	@echo "  make reset-db         Reset database (delete data)"
	@echo ""

# ============================================================================
# Setup & Installation
# ============================================================================

setup:
	@echo "Setting up TerraPulse AI..."
	@if [ ! -f .env ]; then cp .env.example .env; echo "Created .env file"; fi
	@echo "Setup complete! Edit .env with your configuration"

install:
	@echo "Installing dependencies..."
	cd frontend && npm install
	cd ../backend && pip install -r requirements.txt
	@echo "Installation complete!"

# ============================================================================
# Development
# ============================================================================

dev:
	@echo "Starting development environment with Docker..."
	docker-compose up -d
	@echo ""
	@echo "Services running:"
	@echo "  Frontend:    http://localhost:3000"
	@echo "  Backend:     http://localhost:8000"
	@echo "  API Docs:    http://localhost:8000/api/docs"
	@echo "  PgAdmin:     http://localhost:5050"
	@echo ""

dev-local:
	@echo "Starting development environment locally..."
	@echo "Starting backend..."
	cd backend && python -m uvicorn app.main:app --reload &
	@echo "Starting frontend..."
	cd frontend && npm run dev &
	@echo ""
	@echo "Services running:"
	@echo "  Frontend:    http://localhost:3000 (will open automatically)"
	@echo "  Backend:     http://localhost:8000"
	@echo ""

# ============================================================================
# Testing
# ============================================================================

test: test-backend test-frontend
	@echo "All tests completed!"

test-backend:
	@echo "Running backend tests..."
	cd backend && python -m pytest tests/ -v

test-frontend:
	@echo "Running frontend tests..."
	cd frontend && npm test -- --watch=false

# ============================================================================
# Code Quality
# ============================================================================

lint:
	@echo "Running linters..."
	@echo "Backend linting..."
	cd backend && flake8 app/
	@echo "Frontend linting..."
	cd frontend && npm run lint
	@echo "Linting complete!"

type-check:
	@echo "Running type checks..."
	@echo "Backend type checking..."
	cd backend && mypy app/
	@echo "Frontend type checking..."
	cd frontend && npm run type-check
	@echo "Type checking complete!"

format:
	@echo "Formatting code..."
	@echo "Backend formatting..."
	cd backend && black app/
	@echo "Frontend formatting..."
	cd frontend && npm run format
	@echo "Formatting complete!"

# ============================================================================
# Building
# ============================================================================

build: build-backend build-frontend
	@echo "Build complete!"

build-backend:
	@echo "Building backend Docker image..."
	docker build -t terrapulse-backend:latest ./backend

build-frontend:
	@echo "Building frontend Docker image..."
	docker build -t terrapulse-frontend:latest ./frontend

# ============================================================================
# Production
# ============================================================================

prod:
	@echo "Starting production environment..."
	docker-compose -f docker-compose.prod.yml up -d
	@echo ""
	@echo "Production services running on:"
	@echo "  Frontend:  http://localhost:3000"
	@echo "  Backend:   http://localhost:8000"
	@echo ""

prod-logs:
	docker-compose -f docker-compose.prod.yml logs -f

prod-down:
	@echo "Stopping production environment..."
	docker-compose -f docker-compose.prod.yml down

# ============================================================================
# Docker
# ============================================================================

docker-up:
	@echo "Starting Docker services..."
	docker-compose up -d
	@sleep 5
	@echo "Services are ready!"

docker-down:
	@echo "Stopping Docker services..."
	docker-compose down

docker-logs:
	docker-compose logs -f

docker-clean:
	@echo "Cleaning Docker images and volumes..."
	docker-compose down -v
	docker image prune -f

# ============================================================================
# Database
# ============================================================================

reset-db:
	@echo "WARNING: This will delete all database data!"
	@read -p "Are you sure? (y/N) " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker-compose down -v; \
		echo "Database reset complete. Run 'make dev' to start fresh."; \
	fi

db-backup:
	@echo "Backing up database..."
	docker-compose exec postgres pg_dump -U postgres terrapulse_db > backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "Backup complete!"

# ============================================================================
# Utilities
# ============================================================================

clean:
	@echo "Cleaning build artifacts..."
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf build/ dist/ .egg-info/
	cd frontend && rm -rf node_modules dist .vite
	@echo "Cleanup complete!"

logs:
	docker-compose logs -f

shell-backend:
	docker-compose exec backend /bin/bash

shell-frontend:
	docker-compose exec frontend /bin/sh

shell-db:
	docker-compose exec postgres psql -U postgres -d terrapulse_db

status:
	@echo "Service Status:"
	@docker-compose ps

# ============================================================================
# Deployment Helpers
# ============================================================================

push-images:
	@echo "Pushing Docker images to registry..."
	docker tag terrapulse-backend:latest your-registry/terrapulse-backend:latest
	docker tag terrapulse-frontend:latest your-registry/terrapulse-frontend:latest
	docker push your-registry/terrapulse-backend:latest
	docker push your-registry/terrapulse-frontend:latest

# ============================================================================
# Default Target
# ============================================================================

.DEFAULT_GOAL := help
