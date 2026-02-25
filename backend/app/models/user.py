"""
User model for database persistence.
"""
from sqlalchemy import Column, Integer, String, DateTime, func

from app.db import Base


class User(Base):
    """User model for storing user account information."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(320), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String(32), nullable=False, default="user")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self) -> str:
        """String representation of User."""
        return f"<User(id={self.id}, email={self.email}, role={self.role})>"
