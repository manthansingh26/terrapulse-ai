from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from datetime import datetime

from app.core.config import get_settings
from app.db.database import engine, Base, SessionLocal, test_connection_async, test_connection
from app.models.models import User, EnvironmentalData, AirQualityHistory, APILog, AlertHistory
from app.api.endpoints import auth, data, cities, websocket, alerts, ml
from app.schemas.schemas import HealthResponse

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="TerraPulse AI - Environmental Monitoring Backend API",
    version=settings.APP_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create database tables
def create_tables():
    """Create all database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created successfully")
    except Exception as e:
        logger.error(f"❌ Error creating tables: {e}")


# Seed local demo data
def seed_local_data():
    """Seed a demo user and sample environmental readings for local development."""
    db = SessionLocal()
    try:
        from app.api.endpoints.cities import CITY_COORDINATES
        from app.core.security import AuthService

        if not db.query(User).filter(User.username == "demo").first():
            db.add(
                User(
                    email="demo@example.com",
                    username="demo",
                    full_name="Demo User",
                    hashed_password=AuthService.hash_password("demo123"),
                    is_active=True,
                    is_admin=False,
                )
            )

        if db.query(EnvironmentalData).count() == 0:
            for index, city in enumerate(CITY_COORDINATES):
                db.add(
                    EnvironmentalData(
                        city=city,
                        aqi=55 + ((index * 23) % 220),
                        co2=410 + (index * 3),
                        temperature=24 + ((index * 1.7) % 12),
                        humidity=42 + ((index * 5) % 45),
                        wind_speed=4 + ((index * 0.8) % 7),
                        rainfall=0,
                    )
                )

        db.commit()
        logger.info("Local demo data is ready")
    except Exception as e:
        db.rollback()
        logger.warning(f"Could not seed local demo data: {e}")
    finally:
        db.close()


# Create tables on startup
create_tables()
seed_local_data()

# Test connection
if test_connection():
    logger.info("✅ FastAPI Backend initialized successfully")
else:
    logger.warning("⚠️ Database connection failed - some features may not work")


# ============ Health Routes ============

@app.get("/", tags=["Health"])
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to TerraPulse AI Backend",
        "version": settings.APP_VERSION,
        "docs": "/api/docs"
    }


@app.get("/api/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    db_status = await test_connection_async()

    return HealthResponse(
        status="healthy",
        version=settings.APP_VERSION,
        database=db_status,
        timestamp=datetime.utcnow()
    )


@app.get("/api/status", tags=["Health"])
async def status():
    """Detailed status endpoint"""
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "debug": settings.DEBUG,
        "timestamp": datetime.utcnow().isoformat(),
        "features": {
            "authentication": True,
            "database": True,
            "caching": settings.REDIS_ENABLED,
            "api_logging": True
        }
    }


# ============ API Routes ============

# Include routers
app.include_router(auth.router, prefix=settings.API_PREFIX)
app.include_router(data.router, prefix=settings.API_PREFIX)
app.include_router(cities.router, prefix=settings.API_PREFIX)
app.include_router(websocket.router, prefix=settings.API_PREFIX)
app.include_router(alerts.router, prefix=settings.API_PREFIX)
app.include_router(ml.router, prefix=settings.API_PREFIX)


# ============ Error Handlers ============

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": str(exc) if settings.DEBUG else "An error occurred",
        }
    )


# ============ Startup/Shutdown Events ============

@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} starting up...")
    logger.info(f"📊 Database: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'unknown'}")
    logger.info(f"🔐 Authentication enabled: JWT")
    logger.info(f"📡 API URL: /api")
    logger.info(f"📚 Swagger Docs: /api/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info(f"🛑 {settings.APP_NAME} shutting down...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
