"""
Integration tests for role-based authorization.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.auth.tokens import create_access_token
from app.auth.security import hash_password
from app.models import User


def test_admin_access_with_admin_role(client: TestClient, db: Session) -> None:
    """Test admin endpoint access with admin role.
    
    Given: A user with admin role and valid access token
    When: GET /api/admin/status is called with admin token
    Then: HTTP 200 is returned with status ok
    """
    # Create an admin user in the database
    admin_user = User(
        email="admin@example.com",
        hashed_password=hash_password("adminpassword123"),
        role="admin",
    )
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    
    # Create admin token for this user
    admin_token = create_access_token(user_id=admin_user.id, role="admin")
    
    response = client.get(
        "/api/admin/status",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_admin_access_with_user_role(client: TestClient, db: Session) -> None:
    """Test admin endpoint access with regular user role.
    
    Given: A user with user role and valid access token
    When: GET /api/admin/status is called with user token
    Then: HTTP 403 is returned (insufficient permissions)
    """
    # Create a regular user in the database
    regular_user = User(
        email="user@example.com",
        hashed_password=hash_password("userpassword123"),
        role="user",
    )
    db.add(regular_user)
    db.commit()
    db.refresh(regular_user)
    
    # Create user token for this user
    user_token = create_access_token(user_id=regular_user.id, role="user")
    
    response = client.get(
        "/api/admin/status",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    
    assert response.status_code == 403
    assert "insufficient permissions" in response.json()["detail"].lower()


def test_admin_access_without_token(client: TestClient) -> None:
    """Test admin endpoint access without authentication token.
    
    Given: No authorization header
    When: GET /api/admin/status is called
    Then: HTTP 401 is returned (unauthorized)
    """
    response = client.get("/api/admin/status")
    
    assert response.status_code == 401


def test_admin_access_with_invalid_token(client: TestClient) -> None:
    """Test admin endpoint access with malformed JWT.
    
    Given: An invalid JWT token
    When: GET /api/admin/status is called
    Then: HTTP 401 is returned (invalid token)
    """
    response = client.get(
        "/api/admin/status",
        headers={"Authorization": "Bearer invalid.token.here"},
    )
    
    assert response.status_code == 401
    assert "invalid" in response.json()["detail"].lower()


def test_admin_access_with_missing_bearer_prefix(client: TestClient, db: Session) -> None:
    """Test admin endpoint with token missing Bearer prefix.
    
    Given: Authorization header without Bearer prefix
    When: GET /api/admin/status is called
    Then: HTTP 401 is returned
    """
    # Create an admin user
    admin_user = User(
        email="admin2@example.com",
        hashed_password=hash_password("adminpassword123"),
        role="admin",
    )
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    
    admin_token = create_access_token(user_id=admin_user.id, role="admin")
    
    response = client.get(
        "/api/admin/status",
        headers={"Authorization": admin_token},  # Missing "Bearer "
    )
    
    assert response.status_code == 401
