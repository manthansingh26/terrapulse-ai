"""Unit tests for the ML model utilities (no database required)."""

from app.ml.aqi_model import aqi_risk_level, city_code_map, FEATURE_NAMES


def test_aqi_risk_level_good():
    assert aqi_risk_level(30) == "Good"


def test_aqi_risk_level_fair():
    assert aqi_risk_level(75) == "Fair"


def test_aqi_risk_level_poor():
    assert aqi_risk_level(150) == "Poor"


def test_aqi_risk_level_unhealthy():
    assert aqi_risk_level(250) == "Unhealthy"


def test_aqi_risk_level_severe():
    assert aqi_risk_level(350) == "Severe"


def test_city_code_map_contains_expected_cities():
    codes = city_code_map()
    assert isinstance(codes, dict)
    assert "Delhi" in codes
    assert "Mumbai" in codes
    assert "Bangalore" in codes
    # Codes should be unique integers
    assert len(set(codes.values())) == len(codes)


def test_feature_names_length():
    assert len(FEATURE_NAMES) == 10
    assert "current_aqi" in FEATURE_NAMES
    assert "temperature" in FEATURE_NAMES
