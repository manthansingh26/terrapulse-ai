import os
import logging
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database connection string
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# Debug: Print connection info (SAFE - password not shown)
logger.info(f"Connecting to: postgresql://{os.getenv('DB_USER')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")

try:
    # Create engine
    engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info("✅ Database engine created successfully")
except Exception as e:
    logger.error(f"❌ Failed to create database engine: {e}")
    raise

# Base class
Base = declarative_base()

class EnvironmentalData(Base):
    """Store real-time environmental data"""
    __tablename__ = "environmental_data"
    
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String(100), index=True)
    aqi = Column(Float)
    co2 = Column(Float)
    temperature = Column(Float)
    humidity = Column(Float)
    wind_speed = Column(Float)
    rainfall = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    class Config:
        from_attributes = True

class AirQualityHistory(Base):
    """Store historical air quality data"""
    __tablename__ = "air_quality_history"
    
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String(100), index=True)
    aqi = Column(Float)
    co2 = Column(Float)
    pm25 = Column(Float, nullable=True)
    pm10 = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

# Create tables if they don't exist
try:
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Database tables verified/created successfully")
except Exception as e:
    logger.error(f"❌ Failed to create tables: {e}")

def get_db():
    """Dependency for database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_connection():
    """Test database connection"""
    try:
        from sqlalchemy import text
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        logger.info("✅ Database connection test PASSED")
        return True
    except Exception as e:
        logger.error(f"❌ Database connection test FAILED: {e}")
        return False

# Test connection on import
if __name__ == "__main__":
    test_connection()
