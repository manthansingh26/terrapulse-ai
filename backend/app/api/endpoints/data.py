from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from datetime import datetime, timedelta
import logging

from app.db.database import get_db
from app.models.models import EnvironmentalData, AirQualityHistory, User, AlertHistory
from app.schemas.schemas import (
    EnvironmentalDataResponse, EnvironmentalDataCreate,
    AirQualityHistoryResponse, CityDataResponse, CityStatistics,
    CityRiskInsight, MLInsightsResponse
)
from app.core.security import get_current_user
from app.core.config import get_settings
from app.core.email import send_alert_email
from app.ml.aqi_model import load_metrics, predict_record

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter(prefix="/data", tags=["Environmental Data"])


def classify_risk(score: int) -> str:
    """Classify AQI risk score for dashboard storytelling."""
    if score >= 80:
        return "Critical"
    if score >= 60:
        return "High"
    if score >= 35:
        return "Moderate"
    return "Low"


def build_recommendation(risk_level: str, city: str) -> str:
    """Generate a concise operational recommendation."""
    if risk_level == "Critical":
        return f"Trigger public health alert for {city} and prioritize traffic and industrial emission controls."
    if risk_level == "High":
        return f"Increase monitoring frequency in {city} and notify sensitive groups."
    if risk_level == "Moderate":
        return f"Keep {city} under observation and compare readings with weather changes."
    return f"Maintain baseline monitoring for {city}."


@router.post(
    "/save",
    response_model=EnvironmentalDataResponse,
    status_code=status.HTTP_201_CREATED
)
async def save_environmental_data(
    data: EnvironmentalDataCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Save environmental data and trigger alert if AQI > 200"""

    env_data = EnvironmentalData(
        city=data.city,
        aqi=data.aqi,
        co2=data.co2,
        temperature=data.temperature,
        humidity=data.humidity,
        wind_speed=data.wind_speed,
        rainfall=data.rainfall
    )

    db.add(env_data)
    db.commit()
    db.refresh(env_data)

    # Check if AQI alert should be triggered
    if data.aqi and data.aqi > settings.AQI_ALERT_THRESHOLD:
        one_hour_ago = datetime.utcnow() - timedelta(hours=1)
        recent_alert = db.query(AlertHistory).filter(
            AlertHistory.city == data.city,
            AlertHistory.last_alert_time >= one_hour_ago
        ).first()

        if not recent_alert:
            email_sent = send_alert_email(
                city=data.city,
                aqi_value=data.aqi,
                recipient=settings.ALERT_EMAIL
            )

            alert = AlertHistory(
                city=data.city,
                aqi_value=data.aqi,
                alert_type="high_aqi",
                email_sent=email_sent,
                email_recipient=settings.ALERT_EMAIL,
                last_alert_time=datetime.utcnow()
            )
            db.add(alert)
            db.commit()

            logger.info(f"🚨 AQI Alert: {data.city} AQI={data.aqi}, email_sent={email_sent}")

    return env_data


@router.get("/latest/{city}", response_model=EnvironmentalDataResponse)
async def get_latest_data(
    city: str,
    db: Session = Depends(get_db)
):
    """Get latest environmental data for a city"""

    data = db.query(EnvironmentalData).filter(
        EnvironmentalData.city == city
    ).order_by(EnvironmentalData.timestamp.desc()).first()

    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No data found for city: {city}"
        )

    return data


@router.get("/history/{city}", response_model=list[EnvironmentalDataResponse])
async def get_historical_data(
    city: str,
    days: int = Query(7, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Get historical environmental data for a city"""

    start_date = datetime.utcnow() - timedelta(days=days)

    data = db.query(EnvironmentalData).filter(
        EnvironmentalData.city == city,
        EnvironmentalData.timestamp >= start_date
    ).order_by(EnvironmentalData.timestamp.desc()).all()

    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No historical data found for city: {city}"
        )

    return data


@router.get("/statistics/{city}", response_model=CityStatistics)
async def get_city_statistics(
    city: str,
    days: int = Query(7, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Get city statistics"""

    start_date = datetime.utcnow() - timedelta(days=days)

    records = db.query(EnvironmentalData).filter(
        EnvironmentalData.city == city,
        EnvironmentalData.timestamp >= start_date
    ).all()

    if not records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No data found for city: {city}"
        )

    # Calculate statistics
    aqi_values = [r.aqi for r in records if r.aqi is not None]
    temp_values = [r.temperature for r in records if r.temperature is not None]
    humidity_values = [r.humidity for r in records if r.humidity is not None]

    stats = CityStatistics(
        city=city,
        avg_aqi=sum(aqi_values) / len(aqi_values) if aqi_values else 0,
        max_aqi=max(aqi_values) if aqi_values else 0,
        min_aqi=min(aqi_values) if aqi_values else 0,
        avg_temperature=sum(temp_values) / len(temp_values) if temp_values else 0,
        avg_humidity=sum(humidity_values) / len(humidity_values) if humidity_values else 0,
        data_points=len(records),
        period_days=days
    )

    return stats


@router.get("/air-quality/{city}", response_model=list[AirQualityHistoryResponse])
async def get_air_quality_history(
    city: str,
    days: int = Query(7, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Get air quality history for a city"""

    start_date = datetime.utcnow() - timedelta(days=days)

    data = db.query(AirQualityHistory).filter(
        AirQualityHistory.city == city,
        AirQualityHistory.timestamp >= start_date
    ).order_by(AirQualityHistory.timestamp.desc()).all()

    return data


@router.get("/all/latest", response_model=list[EnvironmentalDataResponse])
async def get_all_latest(
    db: Session = Depends(get_db)
):
    """Get latest data for all cities"""

    # Subquery to get latest timestamp per city
    subquery = db.query(
        EnvironmentalData.city,
        func.max(EnvironmentalData.timestamp).label("max_timestamp")
    ).group_by(EnvironmentalData.city).subquery()

    # Join to get the actual records
    data = db.query(EnvironmentalData).filter(
        and_(
            EnvironmentalData.city == subquery.c.city,
            EnvironmentalData.timestamp == subquery.c.max_timestamp
        )
    ).all()

    return data


@router.get("/ml/insights", response_model=MLInsightsResponse)
async def get_ml_insights(
    db: Session = Depends(get_db)
):
    """Generate trained-model AQI forecasts and risk scores from latest city readings."""

    subquery = db.query(
        EnvironmentalData.city,
        func.max(EnvironmentalData.timestamp).label("max_timestamp")
    ).group_by(EnvironmentalData.city).subquery()

    latest_records = db.query(EnvironmentalData).filter(
        and_(
            EnvironmentalData.city == subquery.c.city,
            EnvironmentalData.timestamp == subquery.c.max_timestamp
        )
    ).all()

    if not latest_records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No environmental data available for ML insights"
        )

    insights: list[CityRiskInsight] = []
    for record in latest_records:
        try:
            prediction = predict_record(record)
        except FileNotFoundError as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{exc}. Run POST /api/ml/train first."
            ) from exc

        current_aqi = prediction["current_aqi"]
        predicted_aqi = prediction["predicted_aqi_24h"]
        risk_score = max(0, min(100, round((predicted_aqi / 300) * 100)))
        confidence = prediction["confidence"]
        risk_level = classify_risk(risk_score)

        insights.append(
            CityRiskInsight(
                city=record.city,
                current_aqi=current_aqi,
                predicted_aqi_24h=predicted_aqi,
                risk_score=risk_score,
                risk_level=risk_level,
                confidence=round(confidence, 2),
                recommendation=build_recommendation(risk_level, record.city)
            )
        )

    insights.sort(key=lambda item: item.risk_score, reverse=True)
    avg_current = sum(item.current_aqi for item in insights) / len(insights)
    avg_predicted = sum(item.predicted_aqi_24h for item in insights) / len(insights)
    avg_confidence = sum(item.confidence for item in insights) / len(insights)
    high_risk_count = len([item for item in insights if item.risk_level in {"High", "Critical"}])
    trend = "rising" if avg_predicted > avg_current + 5 else "improving" if avg_predicted < avg_current - 5 else "stable"
    metrics = load_metrics()

    return MLInsightsResponse(
        model_name=metrics["model_name"],
        model_version=metrics["model_version"],
        generated_at=datetime.utcnow(),
        monitored_cities=len(insights),
        avg_current_aqi=round(avg_current, 1),
        avg_predicted_aqi_24h=round(avg_predicted, 1),
        high_risk_cities=high_risk_count,
        confidence=round(avg_confidence, 2),
        trend=trend,
        insights=insights
    )


@router.delete("/clear-old-data")
async def clear_old_data(
    days: int = Query(30, ge=1),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Clear data older than specified days (admin only)"""

    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    cutoff_date = datetime.utcnow() - timedelta(days=days)

    deleted_env = db.query(EnvironmentalData).filter(
        EnvironmentalData.timestamp < cutoff_date
    ).delete()

    deleted_air = db.query(AirQualityHistory).filter(
        AirQualityHistory.timestamp < cutoff_date
    ).delete()

    db.commit()

    return {
        "deleted_environmental_records": deleted_env,
        "deleted_air_quality_records": deleted_air
    }
