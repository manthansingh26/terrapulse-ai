from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.ml.aqi_model import (
    explain_record,
    load_evaluation_samples,
    load_feature_importance,
    load_metrics,
    load_run_history,
    load_run_metrics,
    predict_record,
    train_model,
)
from app.models.models import EnvironmentalData
from app.schemas.schemas import (
    AQIForecastResponse,
    AQIPredictionExplanationResponse,
    EvaluationSampleItem,
    FeatureImportanceItem,
    MLDataQualityResponse,
    MLRunSummary,
    MLTrainingResponse,
)

router = APIRouter(prefix="/ml", tags=["Machine Learning"])


def latest_city_record(db: Session, city: str) -> EnvironmentalData | None:
    return (
        db.query(EnvironmentalData)
        .filter(EnvironmentalData.city == city)
        .order_by(EnvironmentalData.timestamp.desc())
        .first()
    )


@router.post("/train", response_model=MLTrainingResponse)
async def train_aqi_model(db: Session = Depends(get_db)):
    """Train the AQI forecasting model and save model artifacts."""
    metrics = train_model(db)
    return metrics


@router.get("/metrics", response_model=MLTrainingResponse)
async def get_model_metrics():
    """Return latest trained model metrics."""
    try:
        return load_metrics()
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get("/runs", response_model=list[MLRunSummary])
async def get_model_runs():
    """Return recent versioned model training runs."""
    return load_run_history()


@router.get("/runs/{run_id}", response_model=MLTrainingResponse)
async def get_model_run(run_id: str):
    """Return metrics for a specific model training run."""
    try:
        return load_run_metrics(run_id)
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get("/data-quality", response_model=MLDataQualityResponse)
async def get_ml_data_quality(db: Session = Depends(get_db)):
    """Return training dataset freshness and completeness signals."""
    total_records = db.query(func.count(EnvironmentalData.id)).scalar() or 0
    monitored_cities = db.query(func.count(func.distinct(EnvironmentalData.city))).scalar() or 0
    latest_timestamp = db.query(func.max(EnvironmentalData.timestamp)).scalar()
    missing_aqi = (
        db.query(func.count(EnvironmentalData.id))
        .filter(EnvironmentalData.aqi.is_(None))
        .scalar()
        or 0
    )
    missing_weather = (
        db.query(func.count(EnvironmentalData.id))
        .filter(
            or_(
                EnvironmentalData.temperature.is_(None),
                EnvironmentalData.humidity.is_(None),
                EnvironmentalData.wind_speed.is_(None),
                EnvironmentalData.rainfall.is_(None),
                EnvironmentalData.co2.is_(None),
            )
        )
        .scalar()
        or 0
    )

    freshness_status = "no_data"
    if latest_timestamp:
        now = datetime.now(latest_timestamp.tzinfo or timezone.utc)
        latest = latest_timestamp if latest_timestamp.tzinfo else latest_timestamp.replace(tzinfo=timezone.utc)
        age_hours = (now - latest).total_seconds() / 3600
        if age_hours <= 6:
            freshness_status = "fresh"
        elif age_hours <= 24:
            freshness_status = "aging"
        else:
            freshness_status = "stale"

    try:
        latest_metrics = load_metrics()
        synthetic_rows = int(latest_metrics.get("synthetic_rows_inserted", 0))
    except FileNotFoundError:
        synthetic_rows = 0

    total_cells = total_records * 6
    missing_ratio = round((missing_aqi + missing_weather) / total_cells, 4) if total_cells else 0.0

    return MLDataQualityResponse(
        total_records=total_records,
        monitored_cities=monitored_cities,
        latest_timestamp=latest_timestamp,
        missing_aqi=missing_aqi,
        missing_weather=missing_weather,
        missing_ratio=missing_ratio,
        freshness_status=freshness_status,
        source_tracking_enabled=False,
        synthetic_rows_last_run=synthetic_rows,
    )


@router.get("/feature-importance", response_model=list[FeatureImportanceItem])
async def get_feature_importance():
    """Return feature importance for the trained AQI model."""
    try:
        return load_feature_importance()
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get("/evaluation-samples", response_model=list[EvaluationSampleItem])
async def get_evaluation_samples():
    """Return predicted-vs-actual AQI samples from the test split."""
    try:
        return load_evaluation_samples()
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get("/forecast/all", response_model=list[AQIForecastResponse])
async def forecast_all_cities(db: Session = Depends(get_db)):
    """Predict AQI 24 hours ahead for every monitored city."""
    subquery = (
        db.query(
            EnvironmentalData.city,
            func.max(EnvironmentalData.timestamp).label("max_timestamp"),
        )
        .group_by(EnvironmentalData.city)
        .subquery()
    )

    records = (
        db.query(EnvironmentalData)
        .filter(
            and_(
                EnvironmentalData.city == subquery.c.city,
                EnvironmentalData.timestamp == subquery.c.max_timestamp,
            )
        )
        .all()
    )

    try:
        predictions = [predict_record(record) for record in records]
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{exc}. Run POST /api/ml/train first.",
        ) from exc

    for prediction in predictions:
        prediction["generated_at"] = datetime.fromisoformat(prediction["generated_at"])

    return sorted(predictions, key=lambda item: item["predicted_aqi_24h"], reverse=True)


@router.get("/explain/top", response_model=list[AQIPredictionExplanationResponse])
async def explain_top_city_forecasts(
    limit: int = 5,
    db: Session = Depends(get_db),
):
    """Explain the highest-risk latest city forecasts."""
    subquery = (
        db.query(
            EnvironmentalData.city,
            func.max(EnvironmentalData.timestamp).label("max_timestamp"),
        )
        .group_by(EnvironmentalData.city)
        .subquery()
    )

    records = (
        db.query(EnvironmentalData)
        .filter(
            and_(
                EnvironmentalData.city == subquery.c.city,
                EnvironmentalData.timestamp == subquery.c.max_timestamp,
            )
        )
        .all()
    )

    try:
        explanations = [explain_record(record) for record in records]
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{exc}. Run POST /api/ml/train first.",
        ) from exc

    for explanation in explanations:
        explanation["generated_at"] = datetime.fromisoformat(explanation["generated_at"])

    return sorted(explanations, key=lambda item: item["predicted_aqi_24h"], reverse=True)[:limit]


@router.get("/forecast/{city}", response_model=AQIForecastResponse)
async def forecast_city(city: str, db: Session = Depends(get_db)):
    """Predict AQI 24 hours ahead for one city."""
    record = latest_city_record(db, city)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No latest AQI data found for city: {city}",
        )

    try:
        prediction = predict_record(record)
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{exc}. Run POST /api/ml/train first.",
        ) from exc

    prediction["generated_at"] = datetime.fromisoformat(prediction["generated_at"])
    return prediction


@router.get("/explain/{city}", response_model=AQIPredictionExplanationResponse)
async def explain_city_forecast(city: str, db: Session = Depends(get_db)):
    """Explain a 24-hour AQI forecast for one city."""
    record = latest_city_record(db, city)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No latest AQI data found for city: {city}",
        )

    try:
        explanation = explain_record(record)
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{exc}. Run POST /api/ml/train first.",
        ) from exc

    explanation["generated_at"] = datetime.fromisoformat(explanation["generated_at"])
    return explanation
