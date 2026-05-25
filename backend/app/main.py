from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
import logging
from datetime import datetime, timedelta, timezone

from app.core.config import get_settings
from app.core.limiter import limiter
from app.db.database import (
    engine,
    Base,
    SessionLocal,
    test_connection_async,
    test_connection,
)
from app.models.models import (
    User,
    EnvironmentalData,
)
from app.api.endpoints import auth, data, cities, websocket, alerts, ml
from app.schemas.schemas import HealthResponse

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

settings = get_settings()

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # --- Startup ---
    logger.info(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} starting up...")
    db_url = settings.DATABASE_URL
    logger.info(
        f"📊 Database: {db_url.split('@')[1] if '@' in db_url else 'local'}"
    )
    logger.info("🔐 Authentication enabled: JWT")
    logger.info("📡 API URL: /api")
    logger.info("📚 Swagger Docs: /api/docs")
    from app.services.scheduler import start_scheduler
    start_scheduler()
    
    # Create tables and seed data
    create_tables()
    seed_local_data()
    
    yield
    
    # --- Shutdown ---
    from app.services.scheduler import stop_scheduler
    stop_scheduler()
    logger.info(f"{settings.APP_NAME} shutting down...")

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="TerraPulse AI - Environmental Monitoring Backend API",
    version=settings.APP_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

# Add rate limiter to app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Cache control middleware for public endpoints
class CacheControlMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        path = request.url.path

        # Cache city data for 5 minutes
        if path.startswith("/api/cities"):
            response.headers["Cache-Control"] = (
                "public, max-age=300, stale-while-revalidate=60"
            )
        # Cache ML forecasts for 30 minutes
        elif path.startswith("/api/ml/forecast"):
            response.headers["Cache-Control"] = "public, max-age=1800"
        # No caching for auth endpoints
        elif path.startswith("/api/auth"):
            response.headers["Cache-Control"] = "no-store"
        # No caching for health checks
        elif path.startswith("/api/health"):
            response.headers["Cache-Control"] = "no-store"

        return response


app.add_middleware(CacheControlMiddleware)


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
    """Seed a demo user and sample environmental readings for local development.

    Each EnvironmentalData record receives a fresh timestamp so the dashboard
    never shows stale data.  If the newest existing record is older than
    12 hours the old seed data is deleted and re-inserted with current times.
    """
    db = SessionLocal()
    try:
        from app.api.endpoints.cities import CITY_COORDINATES
        from app.core.security import AuthService

        # --- Demo user ---
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

        # --- Environmental seed data ---
        needs_seed = False
        existing_count = db.query(EnvironmentalData).count()

        if existing_count == 0:
            needs_seed = True
        else:
            # Check staleness: if the newest record is older than 12 hours, re-seed
            from sqlalchemy import func

            newest_ts = db.query(func.max(EnvironmentalData.timestamp)).scalar()
            if newest_ts is not None and newest_ts < datetime.now(timezone.utc) - timedelta(
                hours=12
            ):
                logger.info("Seed data is stale (>12 h old) — deleting and re-seeding")
                db.query(EnvironmentalData).delete()
                needs_seed = True

        if needs_seed:
            now = datetime.now(timezone.utc)
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
                        timestamp=now - timedelta(minutes=index),
                    )
                )

        db.commit()
        logger.info("Local demo data is ready")
    except Exception as e:
        db.rollback()
        logger.warning(f"Could not seed local demo data: {e}")
    finally:
        db.close()


# Create tables on startup (Moved to lifespan)
# create_tables()
# seed_local_data()

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
        "docs": "/api/docs",
    }


@app.get("/api/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint with component status"""
    db_status = await test_connection_async()

    # Check WAQI API availability (lightweight check)
    waqi_status = "disabled"
    if settings.WAQI_API_TOKEN and settings.WAQI_API_TOKEN != "demo":
        try:
            import httpx

            async with httpx.AsyncClient(timeout=5) as client:
                r = await client.get(
                    f"https://api.waqi.info/feed/delhi/?token={settings.WAQI_API_TOKEN}",
                    follow_redirects=True,
                )
            waqi_status = "ok" if r.status_code == 200 else "degraded"
        except Exception as e:
            logger.warning(f"WAQI health check failed: {e}")
            waqi_status = "unreachable"

    # Overall status
    overall_status = "healthy"
    if db_status.get("status") != "connected":
        overall_status = "degraded"
    if waqi_status == "unreachable":
        overall_status = "degraded"

    return HealthResponse(
        status=overall_status,
        version=settings.APP_VERSION,
        database=db_status,
        timestamp=datetime.now(timezone.utc),
        components={"database": db_status.get("status"), "waqi_api": waqi_status},
    )


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check_alias():
    """Root health check alias for uptime probes and cold-start pings."""
    return await health_check()


@app.get("/api/status", tags=["Health"])
async def status():
    """Detailed status endpoint"""
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "debug": settings.DEBUG,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "features": {
            "authentication": True,
            "database": True,
            "caching": settings.REDIS_ENABLED,
            "api_logging": True,
        },
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
        },
    )


# ============ Startup/Shutdown Events ============
# Moved to lifespan context manager


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
