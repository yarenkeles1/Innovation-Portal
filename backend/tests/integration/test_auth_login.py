"""
Integration tests for user login endpoint.
"""
import pytest
from fastapi.testclient import TestClient
from jose import jwt

from app.core.settings import settings
from app.auth.security import hash_password
from app.models import User
from sqlalchemy.orm import Session


def test_login_success(client: TestClient, db: Session) -> None:
    """Test successful login with valid credentials.
    
    Given: A registered user with valid credentials
    When: POST /api/auth/login is called
    Then: HTTP 200 is returned with access_token, refresh_token, and token_type
    """
    # Register user first
    email = "logintest@example.com"
    password = "securepassword123"
    
    client.post(
        "/api/auth/register",
        json={"email": email, "password": password},
    )
    
    # Login
    response = client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert data["expires_in"] == 15 * 60  # 15 minutes in seconds
    
    # Verify access token is valid JWT
    decoded = jwt.decode(
        data["access_token"],
        settings.jwt_secret,
        algorithms=["HS256"],
    )
    assert decoded["sub"] == "1"  # First user ID is 1


def test_login_invalid_password(client: TestClient, db: Session) -> None:
    """Test login with invalid password.
    
    Given: A registered user with incorrect password
    When: POST /api/auth/login is called
    Then: HTTP 401 is returned with generic error message
    """
    # Register user
    email = "user@example.com"
    client.post(
        "/api/auth/register",
        json={"email": email, "password": "correctpassword123"},
    )
    
    # Try login with wrong password
    response = client.post(
        "/api/auth/login",
        json={"email": email, "password": "wrongpassword123"},
    )
    
    assert response.status_code == 401
    assert "invalid credentials" in response.json()["detail"].lower()


def test_login_nonexistent_user(client: TestClient) -> None:
    """Test login with nonexistent email.
    
    Given: An email that is not registered
    When: POST /api/auth/login is called
    Then: HTTP 401 is returned with generic error message (no user enumeration)
    """
    response = client.post(
        "/api/auth/login",
        json={"email": "nonexistent@example.com", "password": "somepassword123"},
    )
    
    assert response.status_code == 401
    assert "invalid credentials" in response.json()["detail"].lower()


def test_login_token_contains_user_claims(client: TestClient, db: Session) -> None:
    """Test that access token contains correct user claims.
    
    Given: A registered user
    When: POST /api/auth/login is called
    Then: The returned access_token contains user id and role in claims
    """
    # Register user
    email = "claimtest@example.com"
    password = "securepassword123"
    
    client.post(
        "/api/auth/register",
        json={"email": email, "password": password},
    )
    
    # Login
    response = client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )
    
    data = response.json()
    
    # Decode token without verification
    decoded = jwt.decode(
        data["access_token"],
        settings.jwt_secret,
        algorithms=["HS256"],
    )
    
    assert "sub" in decoded  # user id
    assert "role" in decoded  # user role
    assert decoded["role"] == "user"
    assert "exp" in decoded  # expiration
    assert "iat" in decoded  # issued at
