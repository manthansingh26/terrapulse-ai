"""Tests for health and status endpoints."""


def test_root_returns_welcome(client):
    """GET / should return a welcome message."""
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert "message" in body
    assert "TerraPulse" in body["message"]


def test_health_check(client):
    """GET /api/health should return healthy status."""
    response = client.get("/api/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "healthy"
    assert "version" in body
    assert "database" in body


def test_status_endpoint(client):
    """GET /api/status should return app metadata."""
    response = client.get("/api/status")
    assert response.status_code == 200
    body = response.json()
    assert "app_name" in body
    assert "version" in body
    assert "features" in body
    assert body["features"]["authentication"] is True
