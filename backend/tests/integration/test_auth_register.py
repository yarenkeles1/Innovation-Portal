"""
Integration tests for user registration endpoint.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import User


def test_register_success(client: TestClient, db: Session) -> None:
    """Test successful user registration.
    
    Given: Valid email and password
    When: POST /api/auth/register is called
    Then: User is created in database and HTTP 201 is returned
    """
    response = client.post(
        "/api/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "securepassword123",
        },
    )
    
    assert response.status_code == 201
    assert response.json() == {"message": "user created"}
    
    # Verify user was created in database
    user = db.query(User).filter(User.email == "newuser@example.com").first()
    assert user is not None
    assert user.email == "newuser@example.com"
    assert user.role == "user"


def test_register_duplicate_email(client: TestClient, db: Session) -> None:
    """Test registration with duplicate email.
    
    Given: An already registered email
    When: POST /api/auth/register is called with the same email
    Then: HTTP 400 is returned with error message
    """
    # Create initial user
    client.post(
        "/api/auth/register",
        json={
            "email": "existing@example.com",
            "password": "securepassword123",
        },
    )
    
    # Try to register with same email
    response = client.post(
        "/api/auth/register",
        json={
            "email": "existing@example.com",
            "password": "differentpassword123",
        },
    )
    
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


def test_register_short_password(client: TestClient) -> None:
    """Test registration with password too short.
    
    Given: Password shorter than 8 characters
    When: POST /api/auth/register is called
    Then: HTTP 422 is returned (validation error)
    """
    response = client.post(
        "/api/auth/register",
        json={
            "email": "user@example.com",
            "password": "short",
        },
    )
    
    assert response.status_code == 422
    assert "password" in response.json()["detail"][0]["loc"]
