from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import QueuePool
import logging

from app.core.config import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()

database_url = settings.DATABASE_URL
engine_kwargs = {
    "pool_pre_ping": True,
    "echo": settings.DEBUG,
}

if database_url.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}
else:
    if database_url.startswith("postgresql://"):
        database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)
    engine_kwargs.update(
        {
            "poolclass": QueuePool,
            "pool_size": 10,
            "max_overflow": 20,
            "connect_args": {
                "connect_timeout": 10,
                "options": "-c timezone=utc",
            },
        }
    )

# Create database engine with connection pooling where the driver supports it.
engine = create_engine(database_url, **engine_kwargs)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

# Declarative base for models
Base = declarative_base()


def get_db() -> Session:
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_connection() -> bool:
    """Test database connection"""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            logger.info("✅ Database connection successful")
            return True
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        return False


async def test_connection_async() -> dict:
    """Test database connection (async)"""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            return {
                "status": "connected",
                "database": settings.DATABASE_URL.split("@")[1] if "@" in settings.DATABASE_URL else "unknown"
            }
    except Exception as e:
        return {
            "status": "disconnected",
            "error": str(e)
        }
