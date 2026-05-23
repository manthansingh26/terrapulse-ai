"""Tests for city data endpoints."""

from app.models.models import EnvironmentalData
from datetime import datetime


def _seed_city(db_session, city="Delhi", aqi=150):
    """Insert a single city record for testing."""
    record = EnvironmentalData(
        city=city,
        aqi=aqi,
        co2=420.0,
        temperature=32.0,
        humidity=55.0,
        wind_speed=5.0,
        rainfall=0.0,
        timestamp=datetime.utcnow(),
    )
    db_session.add(record)
    db_session.commit()
    return record


def test_get_all_cities_empty(client):
    """GET /api/cities/all with no data returns an empty list."""
    response = client.get("/api/cities/all")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_all_cities_with_data(client, db_session):
    """GET /api/cities/all should return seeded city data."""
    _seed_city(db_session, "Mumbai", 120)
    response = client.get("/api/cities/all")
    assert response.status_code == 200
    cities = response.json()
    assert len(cities) >= 1
    city_names = [c["city"] for c in cities]
    assert "Mumbai" in city_names


def test_get_single_city(client, db_session):
    """GET /api/cities/{city} should return data for a known city."""
    _seed_city(db_session, "Delhi", 200)
    response = client.get("/api/cities/Delhi")
    assert response.status_code == 200
    body = response.json()
    assert body["city"] == "Delhi"
    assert body["current_aqi"] == 200


def test_get_unknown_city_returns_404(client):
    """GET /api/cities/{city} with a fake city should return 404."""
    response = client.get("/api/cities/FakeCity123")
    assert response.status_code == 404
