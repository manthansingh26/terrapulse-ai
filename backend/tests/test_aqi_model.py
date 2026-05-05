from datetime import datetime, timedelta

import numpy as np
import pytest

from app.ml.aqi_model import (
    FEATURE_NAMES,
    aqi_risk_level,
    build_run_metadata,
    build_supervised_dataset,
    build_supervised_examples,
    factor_direction,
    make_run_id,
    make_feature_vector,
    temporal_train_test_split,
)
from app.models.models import EnvironmentalData


def make_record(city: str, timestamp: datetime, aqi: int | None = 80) -> EnvironmentalData:
    return EnvironmentalData(
        city=city,
        aqi=aqi,
        co2=420.0,
        temperature=30.0,
        humidity=55.0,
        wind_speed=4.0,
        rainfall=0.2,
        timestamp=timestamp,
    )


def test_make_feature_vector_matches_contract():
    timestamp = datetime(2026, 5, 3, 14, 0)
    record = make_record("Ahmedabad", timestamp, aqi=120)
    vector = make_feature_vector(record, {"Ahmedabad": 7})

    assert len(vector) == len(FEATURE_NAMES)
    assert vector == [
        120.0,
        420.0,
        30.0,
        55.0,
        4.0,
        0.2,
        14.0,
        float(timestamp.weekday()),
        5.0,
        7.0,
    ]


def test_build_supervised_dataset_uses_24_hour_target_per_city():
    start = datetime(2026, 5, 1, 0, 0)
    records = [
        make_record("Ahmedabad", start + timedelta(hours=hour), aqi=hour)
        for hour in range(30)
    ]

    features, targets = build_supervised_dataset(records)

    assert features.shape == (6, len(FEATURE_NAMES))
    assert np.array_equal(targets, np.array([24, 25, 26, 27, 28, 29], dtype=float))


def test_temporal_train_test_split_keeps_latest_targets_for_test():
    start = datetime(2026, 5, 1, 0, 0)
    records = [
        make_record("Ahmedabad", start + timedelta(hours=hour), aqi=hour)
        for hour in range(40)
    ]
    dataset = build_supervised_examples(records)

    _, _, y_train, y_test, train_timestamps, test_timestamps = temporal_train_test_split(
        dataset,
        test_size=0.25,
    )

    assert len(y_train) == 12
    assert len(y_test) == 4
    assert max(train_timestamps) < min(test_timestamps)
    assert np.array_equal(y_test, np.array([36, 37, 38, 39], dtype=float))


def test_temporal_train_test_split_rejects_invalid_test_size():
    start = datetime(2026, 5, 1, 0, 0)
    records = [
        make_record("Ahmedabad", start + timedelta(hours=hour), aqi=hour)
        for hour in range(30)
    ]
    dataset = build_supervised_examples(records)

    with pytest.raises(ValueError, match="test_size"):
        temporal_train_test_split(dataset, test_size=1.0)


def test_build_run_metadata_creates_registry_payload():
    metrics = {
        "model_name": "RandomForestRegressor",
        "model_version": "v1.0-rf",
        "trained_at": "2026-05-03T06:07:41.700720",
        "training_rows": 100,
        "test_rows": 25,
        "synthetic_rows_inserted": 0,
        "validation_strategy": "time_based_holdout",
        "train_window_start": "2026-05-01T00:00:00",
        "train_window_end": "2026-05-02T00:00:00",
        "test_window_start": "2026-05-02T01:00:00",
        "test_window_end": "2026-05-03T00:00:00",
        "mae": 5.1,
        "rmse": 7.2,
        "r2": 0.91,
        "features": FEATURE_NAMES,
    }

    run_metrics, run_summary = build_run_metadata(metrics)
    run_id = make_run_id(metrics["trained_at"])

    assert run_metrics["run_id"] == run_id
    assert run_metrics["artifact_uri"] == f"runs/{run_id}"
    assert run_metrics["model_artifact"] == "aqi_forecaster.joblib"
    assert run_summary == {
        "run_id": run_id,
        "model_name": "RandomForestRegressor",
        "model_version": "v1.0-rf",
        "trained_at": "2026-05-03T06:07:41.700720",
        "validation_strategy": "time_based_holdout",
        "training_rows": 100,
        "test_rows": 25,
        "mae": 5.1,
        "rmse": 7.2,
        "r2": 0.91,
        "artifact_uri": f"runs/{run_id}",
    }


@pytest.mark.parametrize(
    ("feature", "value", "expected_direction"),
    [
        ("current_aqi", 160, "increases_risk"),
        ("current_aqi", 40, "reduces_risk"),
        ("wind_speed", 2, "increases_risk"),
        ("wind_speed", 8, "reduces_risk"),
        ("rainfall", 1.2, "reduces_risk"),
        ("hour", 18, "increases_risk"),
    ],
)
def test_factor_direction(feature: str, value: float, expected_direction: str):
    direction, reason = factor_direction(feature, value)

    assert direction == expected_direction
    assert reason


@pytest.mark.parametrize(
    ("aqi", "expected"),
    [
        (25, "Good"),
        (75, "Fair"),
        (150, "Poor"),
        (250, "Unhealthy"),
        (350, "Severe"),
    ],
)
def test_aqi_risk_level(aqi: int, expected: str):
    assert aqi_risk_level(aqi) == expected
