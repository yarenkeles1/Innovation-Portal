"""
Database configuration and session management.
"""
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from typing import Generator

from app.core.settings import settings


# Create database engine
engine: Engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
    echo=False,
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Create declarative base for models
Base = declarative_base()


def init_db() -> None:
    """Initialize the database by creating all tables.
    
    This function creates all tables defined in the SQLAlchemy models.
    In a production environment, use Alembic migrations instead.
    """
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Database session dependency for FastAPI.
    
    Yields a database session and ensures it's properly closed after use.
    This is used as a dependency in FastAPI routes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
