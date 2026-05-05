from __future__ import annotations

import json
import math
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from random import Random
from typing import Iterable

import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from app.api.endpoints.cities import CITY_COORDINATES
from app.models.models import EnvironmentalData


FEATURE_NAMES = [
    "current_aqi",
    "co2",
    "temperature",
    "humidity",
    "wind_speed",
    "rainfall",
    "hour",
    "day_of_week",
    "month",
    "city_code",
]

FEATURE_LABELS = {
    "current_aqi": "Current AQI",
    "co2": "CO2",
    "temperature": "Temperature",
    "humidity": "Humidity",
    "wind_speed": "Wind speed",
    "rainfall": "Rainfall",
    "hour": "Hour of day",
    "day_of_week": "Day of week",
    "month": "Month",
    "city_code": "City pattern",
}

FEATURE_BASELINES = {
    "current_aqi": 100,
    "co2": 430,
    "temperature": 30,
    "humidity": 55,
    "wind_speed": 4,
    "rainfall": 0.5,
    "hour": 12,
    "day_of_week": 3,
    "month": 6,
    "city_code": 0,
}

ARTIFACT_DIR = Path(__file__).resolve().parent / "artifacts"
MODEL_PATH = ARTIFACT_DIR / "aqi_forecaster.joblib"
METRICS_PATH = ARTIFACT_DIR / "metrics.json"
FEATURE_IMPORTANCE_PATH = ARTIFACT_DIR / "feature_importance.json"
EVALUATION_SAMPLES_PATH = ARTIFACT_DIR / "evaluation_samples.json"
RUNS_DIR = ARTIFACT_DIR / "runs"
RUN_HISTORY_PATH = ARTIFACT_DIR / "run_history.json"
LATEST_RUN_PATH = ARTIFACT_DIR / "latest_run.json"
MAX_RUN_HISTORY = 25


@dataclass
class ModelBundle:
    model: RandomForestRegressor
    city_codes: dict[str, int]
    trained_at: str


@dataclass
class SupervisedDataset:
    features: np.ndarray
    targets: np.ndarray
    target_timestamps: list[datetime]


def city_code_map() -> dict[str, int]:
    return {city: index for index, city in enumerate(sorted(CITY_COORDINATES))}


def aqi_risk_level(aqi: int) -> str:
    if aqi > 300:
        return "Severe"
    if aqi > 200:
        return "Unhealthy"
    if aqi > 100:
        return "Poor"
    if aqi > 50:
        return "Fair"
    return "Good"


def make_feature_vector(record: EnvironmentalData, codes: dict[str, int]) -> list[float]:
    timestamp = record.timestamp or datetime.utcnow()
    return [
        float(record.aqi or 0),
        float(record.co2 or 420),
        float(record.temperature or 28),
        float(record.humidity or 55),
        float(record.wind_speed or 4),
        float(record.rainfall or 0),
        float(timestamp.hour),
        float(timestamp.weekday()),
        float(timestamp.month),
        float(codes.get(record.city, -1)),
    ]


def ensure_synthetic_history(db, days: int = 45) -> int:
    """Create deterministic hourly history if the database has too little data.

    Real projects should replace this with live ingestion. For portfolio development,
    this gives the model enough structured data to train and demonstrate the pipeline.
    """
    existing = db.query(EnvironmentalData).count()
    required = len(CITY_COORDINATES) * 24 * 7
    if existing >= required:
        return 0

    rng = Random(2601)
    now = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    inserted = 0

    for city_index, city in enumerate(CITY_COORDINATES):
        city_bias = 35 + ((city_index * 17) % 95)
        for hour_offset in range(days * 24, 0, -1):
            ts = now - timedelta(hours=hour_offset)
            daily_cycle = math.sin((ts.hour / 24) * 2 * math.pi)
            weekly_cycle = math.cos((ts.weekday() / 7) * 2 * math.pi)
            seasonal_pressure = math.sin((ts.timetuple().tm_yday / 365) * 2 * math.pi)
            traffic_peak = 28 if ts.hour in {8, 9, 18, 19, 20} else 0
            weekend_relief = -12 if ts.weekday() >= 5 else 0
            weather_noise = rng.uniform(-10, 10)

            temperature = 24 + city_index % 9 + max(0, daily_cycle) * 7 + rng.uniform(-1.8, 1.8)
            humidity = 62 - daily_cycle * 12 + rng.uniform(-6, 6)
            wind_speed = max(1.0, 4.8 + weekly_cycle * 1.5 + rng.uniform(-1.2, 1.2))
            rainfall = max(0, rng.gauss(0.4, 1.0)) if humidity > 70 else 0
            co2 = 410 + city_bias * 0.7 + traffic_peak * 1.1 + rng.uniform(-8, 8)
            aqi = (
                city_bias
                + traffic_peak
                + weekend_relief
                + max(0, temperature - 30) * 2.4
                + max(0, 65 - humidity) * 0.45
                - wind_speed * 2.8
                - rainfall * 3
                + seasonal_pressure * 14
                + weather_noise
            )
            aqi = int(max(25, min(360, round(aqi))))

            db.add(
                EnvironmentalData(
                    city=city,
                    aqi=aqi,
                    co2=round(co2, 2),
                    temperature=round(temperature, 2),
                    humidity=round(humidity, 2),
                    wind_speed=round(wind_speed, 2),
                    rainfall=round(rainfall, 2),
                    timestamp=ts,
                )
            )
            inserted += 1

    db.commit()
    return inserted


def build_supervised_examples(records: Iterable[EnvironmentalData]) -> SupervisedDataset:
    codes = city_code_map()
    by_city: dict[str, list[EnvironmentalData]] = {}
    for record in records:
        if record.aqi is None:
            continue
        by_city.setdefault(record.city, []).append(record)

    features: list[list[float]] = []
    targets: list[float] = []
    target_timestamps: list[datetime] = []
    for city_records in by_city.values():
        city_records.sort(key=lambda item: item.timestamp or datetime.min)
        for index, record in enumerate(city_records[:-24]):
            future = city_records[index + 24]
            if future.aqi is None:
                continue
            features.append(make_feature_vector(record, codes))
            targets.append(float(future.aqi))
            target_timestamps.append(future.timestamp or datetime.min)

    if not features:
        raise ValueError("Not enough historical records to train AQI forecaster")

    return SupervisedDataset(
        features=np.array(features, dtype=float),
        targets=np.array(targets, dtype=float),
        target_timestamps=target_timestamps,
    )


def build_supervised_dataset(records: Iterable[EnvironmentalData]) -> tuple[np.ndarray, np.ndarray]:
    dataset = build_supervised_examples(records)
    return dataset.features, dataset.targets


def temporal_train_test_split(
    dataset: SupervisedDataset,
    test_size: float = 0.2,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, list[datetime], list[datetime]]:
    if not 0 < test_size < 1:
        raise ValueError("test_size must be between 0 and 1")

    sample_count = len(dataset.targets)
    if sample_count < 2:
        raise ValueError("At least two supervised examples are required")

    ordered_indexes = sorted(
        range(sample_count),
        key=lambda index: dataset.target_timestamps[index],
    )
    split_index = max(1, min(sample_count - 1, int(sample_count * (1 - test_size))))
    train_indexes = ordered_indexes[:split_index]
    test_indexes = ordered_indexes[split_index:]

    return (
        dataset.features[train_indexes],
        dataset.features[test_indexes],
        dataset.targets[train_indexes],
        dataset.targets[test_indexes],
        [dataset.target_timestamps[index] for index in train_indexes],
        [dataset.target_timestamps[index] for index in test_indexes],
    )


def make_run_id(trained_at: str) -> str:
    parsed = datetime.fromisoformat(trained_at.replace("Z", "+00:00"))
    return parsed.strftime("%Y%m%dT%H%M%S%fZ")


def load_run_history() -> list[dict]:
    if not RUN_HISTORY_PATH.exists():
        return []
    return json.loads(RUN_HISTORY_PATH.read_text(encoding="utf-8"))


def load_run_metrics(run_id: str) -> dict:
    run_metrics_path = RUNS_DIR / run_id / "metrics.json"
    if not run_metrics_path.exists():
        raise FileNotFoundError(f"Model run not found: {run_id}")
    return json.loads(run_metrics_path.read_text(encoding="utf-8"))


def build_run_metadata(metrics: dict) -> tuple[dict, dict]:
    run_id = metrics.get("run_id") or make_run_id(metrics["trained_at"])
    run_metrics = {
        **metrics,
        "run_id": run_id,
        "artifact_uri": f"runs/{run_id}",
        "model_artifact": MODEL_PATH.name,
    }
    run_summary = {
        "run_id": run_id,
        "model_name": run_metrics["model_name"],
        "model_version": run_metrics["model_version"],
        "trained_at": run_metrics["trained_at"],
        "validation_strategy": run_metrics["validation_strategy"],
        "training_rows": run_metrics["training_rows"],
        "test_rows": run_metrics["test_rows"],
        "mae": run_metrics["mae"],
        "rmse": run_metrics["rmse"],
        "r2": run_metrics["r2"],
        "artifact_uri": run_metrics["artifact_uri"],
    }
    return run_metrics, run_summary


def save_model_run(
    metrics: dict,
    feature_importance: list[dict],
    evaluation_samples: list[dict],
) -> dict:
    run_metrics, run_summary = build_run_metadata(metrics)
    run_id = run_metrics["run_id"]
    run_dir = RUNS_DIR / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    (run_dir / "metrics.json").write_text(json.dumps(run_metrics, indent=2), encoding="utf-8")
    (run_dir / "feature_importance.json").write_text(
        json.dumps(feature_importance, indent=2),
        encoding="utf-8",
    )
    (run_dir / "evaluation_samples.json").write_text(
        json.dumps(evaluation_samples, indent=2),
        encoding="utf-8",
    )

    history = [entry for entry in load_run_history() if entry.get("run_id") != run_id]
    history.insert(0, run_summary)
    RUN_HISTORY_PATH.write_text(json.dumps(history[:MAX_RUN_HISTORY], indent=2), encoding="utf-8")
    LATEST_RUN_PATH.write_text(json.dumps(run_summary, indent=2), encoding="utf-8")
    return run_metrics


def train_model(db) -> dict:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    inserted = ensure_synthetic_history(db)
    records = db.query(EnvironmentalData).order_by(EnvironmentalData.city, EnvironmentalData.timestamp).all()
    dataset = build_supervised_examples(records)
    x_train, x_test, y_train, y_test, train_timestamps, test_timestamps = temporal_train_test_split(dataset)

    model = RandomForestRegressor(
        n_estimators=180,
        max_depth=14,
        min_samples_leaf=3,
        random_state=2601,
        n_jobs=1,
    )
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)

    rmse = math.sqrt(mean_squared_error(y_test, predictions))
    metrics = {
        "model_name": "RandomForestRegressor",
        "model_version": "v1.0-rf",
        "trained_at": datetime.utcnow().isoformat(),
        "training_rows": int(len(x_train)),
        "test_rows": int(len(x_test)),
        "synthetic_rows_inserted": inserted,
        "validation_strategy": "time_based_holdout",
        "train_window_start": min(train_timestamps).isoformat(),
        "train_window_end": max(train_timestamps).isoformat(),
        "test_window_start": min(test_timestamps).isoformat(),
        "test_window_end": max(test_timestamps).isoformat(),
        "mae": round(float(mean_absolute_error(y_test, predictions)), 3),
        "rmse": round(float(rmse), 3),
        "r2": round(float(r2_score(y_test, predictions)), 3),
        "features": FEATURE_NAMES,
    }

    bundle = {
        "model": model,
        "city_codes": city_code_map(),
        "trained_at": metrics["trained_at"],
        "feature_names": FEATURE_NAMES,
    }
    joblib.dump(bundle, MODEL_PATH)

    importance = permutation_importance(
        model,
        x_test,
        y_test,
        n_repeats=5,
        random_state=2601,
        n_jobs=1,
    )
    feature_importance = sorted(
        [
            {"feature": name, "importance": round(float(score), 5)}
            for name, score in zip(FEATURE_NAMES, importance.importances_mean)
        ],
        key=lambda item: item["importance"],
        reverse=True,
    )

    sample_count = min(80, len(y_test))
    sample_indexes = np.linspace(0, len(y_test) - 1, sample_count, dtype=int) if sample_count else []
    evaluation_samples = [
        {
            "sample": index + 1,
            "actual_aqi": int(round(float(y_test[row_index]))),
            "predicted_aqi": int(round(float(predictions[row_index]))),
            "error": int(round(float(predictions[row_index] - y_test[row_index]))),
        }
        for index, row_index in enumerate(sample_indexes)
    ]

    metrics = save_model_run(metrics, feature_importance, evaluation_samples)
    METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    FEATURE_IMPORTANCE_PATH.write_text(json.dumps(feature_importance, indent=2), encoding="utf-8")
    EVALUATION_SAMPLES_PATH.write_text(json.dumps(evaluation_samples, indent=2), encoding="utf-8")
    return metrics


def load_model() -> dict:
    if not MODEL_PATH.exists():
        raise FileNotFoundError("AQI model is not trained yet")
    return joblib.load(MODEL_PATH)


def load_metrics() -> dict:
    if not METRICS_PATH.exists():
        raise FileNotFoundError("AQI model metrics are not available")
    return json.loads(METRICS_PATH.read_text(encoding="utf-8"))


def load_feature_importance() -> list[dict]:
    if not FEATURE_IMPORTANCE_PATH.exists():
        raise FileNotFoundError("AQI feature importance is not available")
    return json.loads(FEATURE_IMPORTANCE_PATH.read_text(encoding="utf-8"))


def load_evaluation_samples() -> list[dict]:
    if not EVALUATION_SAMPLES_PATH.exists():
        raise FileNotFoundError("AQI evaluation samples are not available")
    return json.loads(EVALUATION_SAMPLES_PATH.read_text(encoding="utf-8"))


def factor_direction(feature: str, value: float) -> tuple[str, str]:
    baseline = FEATURE_BASELINES.get(feature, 0)
    if feature in {"current_aqi", "co2", "temperature"}:
        if value > baseline:
            return "increases_risk", f"{FEATURE_LABELS[feature]} is above the training baseline"
        return "reduces_risk", f"{FEATURE_LABELS[feature]} is below the training baseline"

    if feature == "humidity":
        if value < 45:
            return "increases_risk", "Low humidity can worsen particulate concentration"
        if value > 70:
            return "reduces_risk", "Higher humidity can suppress airborne particulates"
        return "neutral", "Humidity is near the normal operating range"

    if feature == "wind_speed":
        if value < baseline:
            return "increases_risk", "Low wind speed can reduce pollutant dispersion"
        return "reduces_risk", "Higher wind speed can improve pollutant dispersion"

    if feature == "rainfall":
        if value > baseline:
            return "reduces_risk", "Rainfall can wash out airborne particulates"
        return "neutral", "Rainfall is too low to materially reduce AQI risk"

    if feature == "hour":
        if int(value) in {8, 9, 18, 19, 20}:
            return "increases_risk", "The timestamp falls in a typical traffic peak window"
        return "neutral", "The timestamp is outside the strongest traffic peak windows"

    if feature == "day_of_week":
        if int(value) < 5:
            return "increases_risk", "Weekday activity can raise traffic and industrial exposure"
        return "reduces_risk", "Weekend timing can lower traffic-related exposure"

    if feature == "month":
        return "seasonal", "The model uses month to capture seasonal AQI patterns"

    return "location_pattern", "The model learned a city-specific historical pattern"


def explain_record(record: EnvironmentalData, top_n: int = 4) -> dict:
    prediction = predict_record(record)
    importance = {item["feature"]: max(float(item["importance"]), 0) for item in load_feature_importance()}
    values = dict(zip(FEATURE_NAMES, make_feature_vector(record, city_code_map())))
    ranked_features = sorted(
        FEATURE_NAMES,
        key=lambda feature: importance.get(feature, 0),
        reverse=True,
    )

    factors = []
    for feature in ranked_features[:top_n]:
        value = round(float(values[feature]), 3)
        direction, reason = factor_direction(feature, value)
        factors.append(
            {
                "feature": feature,
                "label": FEATURE_LABELS[feature],
                "value": value,
                "importance": round(importance.get(feature, 0), 5),
                "direction": direction,
                "reason": reason,
            }
        )

    primary = factors[0]["label"] if factors else "model inputs"
    summary = (
        f"{record.city} is forecast at AQI {prediction['predicted_aqi_24h']} "
        f"mainly due to {primary.lower()} and recent environmental context."
    )

    return {
        **prediction,
        "explanation_summary": summary,
        "factors": factors,
    }


def predict_record(record: EnvironmentalData) -> dict:
    bundle = load_model()
    model = bundle["model"]
    city_codes = bundle["city_codes"]
    features = np.array([make_feature_vector(record, city_codes)], dtype=float)
    predicted = int(max(0, round(float(model.predict(features)[0]))))
    current = int(record.aqi or 0)
    delta = predicted - current
    confidence = max(0.68, min(0.96, 0.93 - abs(delta) / 420))
    return {
        "city": record.city,
        "current_aqi": current,
        "predicted_aqi_24h": predicted,
        "change": delta,
        "risk_level": aqi_risk_level(predicted),
        "confidence": round(confidence, 2),
        "generated_at": datetime.utcnow().isoformat(),
    }
