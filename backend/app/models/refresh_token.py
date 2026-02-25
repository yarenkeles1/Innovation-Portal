"""
RefreshToken model for managing refresh token state.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func

from app.db import Base


class RefreshToken(Base):
    """RefreshToken model for storing and tracking refresh tokens."""

    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True)
    jti = Column(String(36), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    revoked = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)

    def __repr__(self) -> str:
        """String representation of RefreshToken."""
        return f"<RefreshToken(id={self.id}, user_id={self.user_id}, revoked={self.revoked})>"
