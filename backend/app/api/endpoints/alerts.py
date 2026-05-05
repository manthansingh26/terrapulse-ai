from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import logging

from app.db.database import get_db
from app.models.models import AlertHistory, EnvironmentalData, User
from app.schemas.schemas import (
    AlertCheckRequest,
    AlertResponse,
    AlertHistoryResponse,
    MLForecastAlertResponse,
    MultipleAlertsRequest
)
from app.core.config import get_settings
from app.core.email import send_alert_email, send_forecast_alert_email
from app.core.security import get_current_user
from app.ml.aqi_model import predict_record

router = APIRouter(prefix="/alerts", tags=["Alerts"])
logger = logging.getLogger(__name__)
settings = get_settings()


def recent_alert_exists(db: Session, city: str, alert_type: str) -> AlertHistory | None:
    one_hour_ago = datetime.utcnow() - timedelta(hours=1)
    return db.query(AlertHistory).filter(
        AlertHistory.city == city,
        AlertHistory.alert_type == alert_type,
        AlertHistory.last_alert_time >= one_hour_ago
    ).first()


@router.post(
    "/test",
    response_model=AlertResponse,
    status_code=status.HTTP_200_OK,
    tags=["Alerts"]
)
async def test_alert_endpoint(
    request: AlertCheckRequest,
    db: Session = Depends(get_db)
):
    """
    Test endpoint - Send alert email WITHOUT authentication.
    Use this to verify email configuration works.

    Body: {"city": "Ahmedabad", "aqi_value": 250}
    """
    city = request.city
    aqi_value = request.aqi_value

    logger.info(f"🧪 TEST ALERT: City={city}, AQI={aqi_value}")

    # Send email
    email_sent = send_alert_email(
        city=city,
        aqi_value=aqi_value,
        recipient=settings.ALERT_EMAIL
    )

    # Log to database
    alert = AlertHistory(
        city=city,
        aqi_value=aqi_value,
        alert_type="test_alert",
        email_sent=email_sent,
        email_recipient=settings.ALERT_EMAIL,
        last_alert_time=datetime.utcnow()
    )
    db.add(alert)
    db.commit()

    return AlertResponse(
        alert_triggered=True,
        email_sent=email_sent,
        city=city,
        aqi_value=aqi_value,
        threshold=settings.AQI_ALERT_THRESHOLD,
        message=f"Test alert processed. Email {'SENT' if email_sent else 'FAILED'} to {settings.ALERT_EMAIL}"
    )


@router.post(
    "/check",
    response_model=AlertResponse,
    status_code=status.HTTP_200_OK
)
async def check_and_send_alert(
    request: AlertCheckRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Check if AQI exceeds threshold and send email alert.
    Won't send duplicate alerts within 1 hour for the same city.
    """
    city = request.city
    aqi_value = request.aqi_value
    threshold = settings.AQI_ALERT_THRESHOLD

    # Check if AQI exceeds threshold
    if aqi_value <= threshold:
        return AlertResponse(
            alert_triggered=False,
            email_sent=False,
            city=city,
            aqi_value=aqi_value,
            threshold=threshold,
            message=f"AQI {aqi_value} is below threshold {threshold}"
        )

    # Check if alert was sent recently (within 1 hour)
    recent_alert = recent_alert_exists(db, city, "high_aqi")

    if recent_alert:
        time_since = datetime.utcnow() - recent_alert.last_alert_time
        minutes_left = 60 - int(time_since.total_seconds() / 60)
        return AlertResponse(
            alert_triggered=False,
            email_sent=False,
            city=city,
            aqi_value=aqi_value,
            threshold=threshold,
            message=f"Alert already sent {int(time_since.total_seconds() / 60)} minutes ago. Retry in {minutes_left} minutes"
        )

    # Send email alert
    email_sent = send_alert_email(
        city=city,
        aqi_value=aqi_value,
        recipient=settings.ALERT_EMAIL
    )

    # Log alert to database
    alert = AlertHistory(
        city=city,
        aqi_value=aqi_value,
        alert_type="high_aqi",
        email_sent=email_sent,
        email_recipient=settings.ALERT_EMAIL,
        last_alert_time=datetime.utcnow()
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)

    logger.info(f"Alert processed for {city}: AQI={aqi_value}, email_sent={email_sent}")

    return AlertResponse(
        alert_triggered=True,
        email_sent=email_sent,
        city=city,
        aqi_value=aqi_value,
        threshold=threshold,
        message=f"Alert triggered! Email {'sent' if email_sent else 'failed to send'} to {settings.ALERT_EMAIL}"
    )


@router.post(
    "/ml/check/{city}",
    response_model=MLForecastAlertResponse,
    status_code=status.HTTP_200_OK
)
async def check_ml_forecast_alert(
    city: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Send an early warning when the trained model predicts AQI will cross threshold."""
    record = db.query(EnvironmentalData).filter(
        EnvironmentalData.city == city
    ).order_by(EnvironmentalData.timestamp.desc()).first()

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No environmental data found for city: {city}"
        )

    try:
        prediction = predict_record(record)
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{exc}. Run POST /api/ml/train first."
        ) from exc

    current_aqi = prediction["current_aqi"]
    predicted_aqi = prediction["predicted_aqi_24h"]
    confidence = prediction["confidence"]
    threshold = settings.AQI_ALERT_THRESHOLD

    if predicted_aqi <= threshold:
        return MLForecastAlertResponse(
            alert_triggered=False,
            email_sent=False,
            city=city,
            current_aqi=current_aqi,
            predicted_aqi_24h=predicted_aqi,
            threshold=threshold,
            confidence=confidence,
            message=f"Predicted AQI {predicted_aqi} is below threshold {threshold}"
        )

    recent_alert = recent_alert_exists(db, city, "ml_forecast_aqi")
    if recent_alert:
        time_since = datetime.utcnow() - recent_alert.last_alert_time
        minutes_left = max(0, 60 - int(time_since.total_seconds() / 60))
        return MLForecastAlertResponse(
            alert_triggered=False,
            email_sent=False,
            city=city,
            current_aqi=current_aqi,
            predicted_aqi_24h=predicted_aqi,
            threshold=threshold,
            confidence=confidence,
            message=f"ML forecast alert already sent {int(time_since.total_seconds() / 60)} minutes ago. Retry in {minutes_left} minutes"
        )

    email_sent = send_forecast_alert_email(
        city=city,
        current_aqi=current_aqi,
        predicted_aqi=predicted_aqi,
        confidence=confidence,
        recipient=settings.ALERT_EMAIL
    )

    alert = AlertHistory(
        city=city,
        aqi_value=predicted_aqi,
        alert_type="ml_forecast_aqi",
        email_sent=email_sent,
        email_recipient=settings.ALERT_EMAIL,
        last_alert_time=datetime.utcnow()
    )
    db.add(alert)
    db.commit()

    return MLForecastAlertResponse(
        alert_triggered=True,
        email_sent=email_sent,
        city=city,
        current_aqi=current_aqi,
        predicted_aqi_24h=predicted_aqi,
        threshold=threshold,
        confidence=confidence,
        message=f"ML early warning triggered. Email {'sent' if email_sent else 'failed'} to {settings.ALERT_EMAIL}"
    )


@router.post(
    "/ml/check-all",
    response_model=list[MLForecastAlertResponse],
    status_code=status.HTTP_200_OK
)
async def check_all_ml_forecast_alerts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Check every latest city forecast and send early warning alerts where needed."""
    latest_by_city = {}
    records = db.query(EnvironmentalData).order_by(
        EnvironmentalData.city,
        EnvironmentalData.timestamp.desc()
    ).all()

    for record in records:
        latest_by_city.setdefault(record.city, record)

    results = []
    for city in latest_by_city:
        result = await check_ml_forecast_alert(
            city=city,
            db=db,
            current_user=current_user
        )
        results.append(result)

    return results


@router.post(
    "/check-all",
    response_model=list[AlertResponse],
    status_code=status.HTTP_200_OK
)
async def check_all_cities_alerts(
    request: MultipleAlertsRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Check multiple cities and send alerts for those exceeding threshold"""
    results = []

    for city_data in request.cities_data:
        city = city_data.get("city")
        aqi_value = city_data.get("aqi_value")

        if city and aqi_value:
            alert_request = AlertCheckRequest(city=city, aqi_value=aqi_value)
            result = await check_and_send_alert(
                request=alert_request,
                db=db,
                current_user=current_user
            )
            results.append(result)

    return results


@router.get(
    "/history",
    response_model=list[AlertHistoryResponse],
    status_code=status.HTTP_200_OK
)
async def get_alert_history(
    days: int = 7,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get alert history for the specified number of days"""
    cutoff_date = datetime.utcnow() - timedelta(days=days)

    alerts = db.query(AlertHistory).filter(
        AlertHistory.last_alert_time >= cutoff_date
    ).order_by(AlertHistory.last_alert_time.desc()).all()

    return alerts


@router.get(
    "/history/{city}",
    response_model=list[AlertHistoryResponse],
    status_code=status.HTTP_200_OK
)
async def get_city_alert_history(
    city: str,
    days: int = 7,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get alert history for a specific city"""
    cutoff_date = datetime.utcnow() - timedelta(days=days)

    alerts = db.query(AlertHistory).filter(
        AlertHistory.city == city,
        AlertHistory.last_alert_time >= cutoff_date
    ).order_by(AlertHistory.last_alert_time.desc()).all()

    if not alerts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No alert history found for city: {city}"
        )

    return alerts
