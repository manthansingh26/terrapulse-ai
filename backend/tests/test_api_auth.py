"""Tests for authentication endpoints."""


def _register_user(client, username="testuser", email="test@example.com", password="securepass123"):
    """Helper to register a user."""
    return client.post(
        "/api/auth/register",
        json={
            "username": username,
            "email": email,
            "full_name": "Test User",
            "password": password,
        },
    )


def test_register_new_user(client):
    """POST /api/auth/register should create a new user."""
    response = _register_user(client)
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["user"]["username"] == "testuser"


def test_register_duplicate_username(client):
    """POST /api/auth/register with duplicate username should fail."""
    _register_user(client, username="dupuser", email="dup1@example.com")
    response = _register_user(client, username="dupuser", email="dup2@example.com")
    assert response.status_code == 400


def test_login_valid_credentials(client):
    """POST /api/auth/login with correct credentials should return a token."""
    _register_user(client, username="loginuser", email="login@example.com", password="mypassword123")
    response = client.post(
        "/api/auth/login",
        json={"username": "loginuser", "password": "mypassword123"},
    )
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


def test_login_wrong_password(client):
    """POST /api/auth/login with wrong password should return 401."""
    _register_user(client, username="wrongpw", email="wrongpw@example.com", password="realpassword1")
    response = client.post(
        "/api/auth/login",
        json={"username": "wrongpw", "password": "wrongpassword"},
    )
    assert response.status_code == 401
