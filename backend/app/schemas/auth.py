"""
Pydantic schemas for user-related requests and responses.
"""
from pydantic import BaseModel, Field
from datetime import datetime


class UserRegisterRequest(BaseModel):
    """Request schema for user registration."""

    email: str = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="User password (minimum 8 characters)")


class UserResponse(BaseModel):
    """Response schema for user data without password."""

    id: int = Field(..., description="User ID")
    email: str = Field(..., description="User email")
    role: str = Field(..., description="User role (user or admin)")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        """Pydantic config."""
        from_attributes = True


class UserLoginRequest(BaseModel):
    """Request schema for user login."""

    email: str = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class TokenResponse(BaseModel):
    """Response schema for authentication token."""

    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Access token expiry in seconds")
