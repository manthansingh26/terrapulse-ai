from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.sql import func
from datetime import datetime

from app.db.database import Base


class User(Base):
    """User model for authentication"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, username={self.username})>"


class EnvironmentalData(Base):
    """Environmental data model"""
    __tablename__ = "environmental_data"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String(100), index=True, nullable=False)
    aqi = Column(Integer, nullable=True)
    co2 = Column(Float, nullable=True)
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    wind_speed = Column(Float, nullable=True)
    rainfall = Column(Float, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    def __repr__(self):
        return f"<EnvironmentalData(city={self.city}, aqi={self.aqi}, temp={self.temperature})>"


class AirQualityHistory(Base):
    """Air quality history model"""
    __tablename__ = "air_quality_history"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String(100), index=True, nullable=False)
    aqi = Column(Integer, nullable=True)
    co2 = Column(Float, nullable=True)
    pm25 = Column(Float, nullable=True)
    pm10 = Column(Float, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    def __repr__(self):
        return f"<AirQualityHistory(city={self.city}, aqi={self.aqi}, pm25={self.pm25})>"


class APILog(Base):
    """API usage logging"""
    __tablename__ = "api_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    endpoint = Column(String(255), nullable=False)
    method = Column(String(10), nullable=False)
    status_code = Column(Integer, nullable=False)
    response_time_ms = Column(Integer, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    def __repr__(self):
        return f"<APILog(endpoint={self.endpoint}, status={self.status_code})>"


class AlertHistory(Base):
    """Alert history for AQI notifications"""
    __tablename__ = "alert_history"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String(100), index=True, nullable=False)
    aqi_value = Column(Integer, nullable=False)
    alert_type = Column(String(50), nullable=False, default="high_aqi")
    email_sent = Column(Boolean, default=True)
    email_recipient = Column(String(255), nullable=True)
    last_alert_time = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    def __repr__(self):
        return f"<AlertHistory(city={self.city}, aqi={self.aqi_value}, type={self.alert_type})>"
