import os
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    """Application configuration"""
    
    # App
    APP_NAME: str = "TerraPulse AI - Backend"
    APP_VERSION: str = "2.0.0"
    API_PREFIX: str = "/api"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:2601@localhost:5432/terrapulse_db"
    )
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production-12345")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS - configurable based on environment
    ALLOWED_ORIGINS: list[str] = []
    
    # APIs
    WAQI_API_TOKEN: str = os.getenv("WAQI_API_TOKEN", "demo")
    OPENWEATHERMAP_API_KEY: str = os.getenv("OPENWEATHERMAP_API_KEY", "")
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    REDIS_ENABLED: bool = os.getenv("REDIS_ENABLED", "False").lower() == "true"

    # Email Alerts
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    ALERT_EMAIL: str = os.getenv("ALERT_EMAIL", "admin@terrapulse.com")
    AQI_ALERT_THRESHOLD: int = int(os.getenv("AQI_ALERT_THRESHOLD", "200"))
    
    @field_validator("SECRET_KEY")
    @classmethod
    def secret_key_must_be_strong(cls, v: str) -> str:
        """Validate SECRET_KEY is strong and not a default value"""
        weak_defaults = {
            "changeme",
            "secret",
            "your-secret-key",
            "your-secret-key-change-in-production-12345",
            "supersecret",
            "password",
            "123456",
            "demo"
        }
        
        if v.lower() in weak_defaults or len(v) < 32:
            raise ValueError(
                "SECRET_KEY is too weak or is a default value. "
                "Generate one with: python -c \"import secrets; print(secrets.token_hex(32))\""
            )
        return v
    
    def __init__(self, **data):
        super().__init__(**data)
        # Set CORS origins based on environment
        if self.ENVIRONMENT == "production":
            self.ALLOWED_ORIGINS = [
                "https://terrapulse-ai.vercel.app",
                os.getenv("ALLOWED_ORIGINS", "https://terrapulse-ai.vercel.app").split(","),
            ]
            # Flatten if it's a list
            if isinstance(self.ALLOWED_ORIGINS[-1], list):
                self.ALLOWED_ORIGINS = self.ALLOWED_ORIGINS[:-1] + self.ALLOWED_ORIGINS[-1]
        else:
            # Development: allow localhost
            allowed = os.getenv(
                "ALLOWED_ORIGINS",
                "http://localhost:5173,http://localhost:3000,http://localhost:8501,http://127.0.0.1:5173,http://127.0.0.1:3000"
            )
            self.ALLOWED_ORIGINS = [origin.strip() for origin in allowed.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings"""
    return Settings()
