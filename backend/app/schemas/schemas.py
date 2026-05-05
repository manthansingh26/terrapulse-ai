from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


# ==================== Auth Schemas ====================

class UserRegister(BaseModel):
    """User registration schema"""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = None
    password: str = Field(..., min_length=8, max_length=100)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "full_name": "John Doe",
                "password": "securepassword123"
            }
        }


class UserLogin(BaseModel):
    """User login schema - accepts email or username"""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123"
            }
        }


class Token(BaseModel):
    """Token response schema"""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    """Token data schema"""
    username: Optional[str] = None
    user_id: Optional[int] = None


class UserResponse(BaseModel):
    """User response schema"""
    id: int
    email: str
    username: str
    full_name: Optional[str] = None
    is_active: bool
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== Environmental Data Schemas ====================

class EnvironmentalDataBase(BaseModel):
    """Base environmental data schema"""
    city: str
    aqi: Optional[int] = None
    co2: Optional[float] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    wind_speed: Optional[float] = None
    rainfall: Optional[float] = None


class EnvironmentalDataCreate(EnvironmentalDataBase):
    """Create environmental data schema"""
    pass


class EnvironmentalDataResponse(EnvironmentalDataBase):
    """Environmental data response schema"""
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True


# ==================== Air Quality Schemas ====================

class AirQualityHistoryBase(BaseModel):
    """Base air quality history schema"""
    city: str
    aqi: Optional[int] = None
    co2: Optional[float] = None
    pm25: Optional[float] = None
    pm10: Optional[float] = None


class AirQualityHistoryCreate(AirQualityHistoryBase):
    """Create air quality history schema"""
    pass


class AirQualityHistoryResponse(AirQualityHistoryBase):
    """Air quality history response schema"""
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True


# ==================== City Data Schemas ====================

class CityDataResponse(BaseModel):
    """City data response schema"""
    city: str
    latitude: float
    longitude: float
    current_aqi: Optional[int] = None
    current_temperature: Optional[float] = None
    current_humidity: Optional[float] = None
    aqi_status: str
    aqi_color: str
    last_updated: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "city": "Ahmedabad",
                "latitude": 23.0225,
                "longitude": 72.5714,
                "current_aqi": 150,
                "current_temperature": 28.5,
                "current_humidity": 65,
                "aqi_status": "Unhealthy for Sensitive Groups",
                "aqi_color": "#FF7F50",
                "last_updated": "2024-01-01T12:00:00"
            }
        }


# ==================== Statistics Schemas ====================

class CityStatistics(BaseModel):
    """City statistics schema"""
    city: str
    avg_aqi: float
    max_aqi: int
    min_aqi: int
    avg_temperature: float
    avg_humidity: float
    data_points: int
    period_days: int

    class Config:
        from_attributes = True


class CityRiskInsight(BaseModel):
    """ML-style risk insight for a city."""
    city: str
    current_aqi: int
    predicted_aqi_24h: int
    risk_score: int
    risk_level: str
    confidence: float
    recommendation: str


class MLInsightsResponse(BaseModel):
    """Portfolio-ready ML insights response for the dashboard."""
    model_name: str
    model_version: str
    generated_at: datetime
    monitored_cities: int
    avg_current_aqi: float
    avg_predicted_aqi_24h: float
    high_risk_cities: int
    confidence: float
    trend: str
    insights: list[CityRiskInsight]


class AQIForecastResponse(BaseModel):
    """Prediction response from the trained AQI model."""
    city: str
    current_aqi: int
    predicted_aqi_24h: int
    change: int
    risk_level: str
    confidence: float
    generated_at: datetime


class PredictionExplanationFactor(BaseModel):
    """Single factor contributing to a prediction explanation."""
    feature: str
    label: str
    value: float
    importance: float
    direction: str
    reason: str


class AQIPredictionExplanationResponse(AQIForecastResponse):
    """Forecast response with model explanation factors."""
    explanation_summary: str
    factors: list[PredictionExplanationFactor]


class MLTrainingResponse(BaseModel):
    """Model training result."""
    run_id: Optional[str] = None
    model_name: str
    model_version: str
    trained_at: datetime
    training_rows: int
    test_rows: int
    synthetic_rows_inserted: int
    validation_strategy: Optional[str] = None
    train_window_start: Optional[datetime] = None
    train_window_end: Optional[datetime] = None
    test_window_start: Optional[datetime] = None
    test_window_end: Optional[datetime] = None
    mae: float
    rmse: float
    r2: float
    features: list[str]
    artifact_uri: Optional[str] = None
    model_artifact: Optional[str] = None


class MLRunSummary(BaseModel):
    """Summary of a versioned ML training run."""
    run_id: str
    model_name: str
    model_version: str
    trained_at: datetime
    validation_strategy: str
    training_rows: int
    test_rows: int
    mae: float
    rmse: float
    r2: float
    artifact_uri: str


class MLDataQualityResponse(BaseModel):
    """Training dataset quality summary for ML operations."""
    total_records: int
    monitored_cities: int
    latest_timestamp: Optional[datetime] = None
    missing_aqi: int
    missing_weather: int
    missing_ratio: float
    freshness_status: str
    source_tracking_enabled: bool
    synthetic_rows_last_run: int


class FeatureImportanceItem(BaseModel):
    """Feature importance row."""
    feature: str
    importance: float


class EvaluationSampleItem(BaseModel):
    """Predicted-vs-actual evaluation row from the model test split."""
    sample: int
    actual_aqi: int
    predicted_aqi: int
    error: int


# ==================== Health & Status Schemas ====================

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    database: dict
    timestamp: datetime


class ErrorResponse(BaseModel):
    """Error response schema"""
    error: str
    detail: Optional[str] = None
    status_code: int

    class Config:
        json_schema_extra = {
            "example": {
                "error": "Not Found",
                "detail": "Resource not found",
                "status_code": 404
            }
        }


# ==================== Alert Schemas ====================

class AlertCheckRequest(BaseModel):
    """Request to check and send alerts"""
    city: str
    aqi_value: int

    class Config:
        json_schema_extra = {
            "example": {
                "city": "Ahmedabad",
                "aqi_value": 250
            }
        }


class AlertHistoryResponse(BaseModel):
    """Alert history response schema"""
    id: int
    city: str
    aqi_value: int
    alert_type: str
    email_sent: bool
    email_recipient: Optional[str] = None
    last_alert_time: datetime

    class Config:
        from_attributes = True


class AlertResponse(BaseModel):
    """Alert check response schema"""
    alert_triggered: bool
    email_sent: bool
    city: str
    aqi_value: int
    threshold: int
    message: str


class MLForecastAlertResponse(BaseModel):
    """ML-based early warning alert response."""
    alert_triggered: bool
    email_sent: bool
    city: str
    current_aqi: int
    predicted_aqi_24h: int
    threshold: int
    confidence: float
    message: str


class MultipleAlertsRequest(BaseModel):
    """Request to check multiple cities"""
    cities_data: list[dict]

    class Config:
        json_schema_extra = {
            "example": {
                "cities_data": [
                    {"city": "Ahmedabad", "aqi_value": 250},
                    {"city": "Mumbai", "aqi_value": 180}
                ]
            }
        }
