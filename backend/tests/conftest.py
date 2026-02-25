"""
Pytest configuration and fixtures for testing.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient

from app.db import Base, get_db
from app.main import app
from app.models import User


# Create test database
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Create a fresh test database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db: Session):
    """Create a test client with a test database."""
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db: Session) -> User:
    """Create a test user."""
    user = User(
        email="test@example.com",
        hashed_password="$2b$12$fakehash",  # Fake bcrypt hash
        role="user",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_admin_user(db: Session) -> User:
    """Create a test admin user."""
    admin = User(
        email="admin@example.com",
        hashed_password="$2b$12$fakehash",  # Fake bcrypt hash
        role="admin",
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin
