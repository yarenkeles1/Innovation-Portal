"""
Settings and configuration loader for the application.
Uses Pydantic Settings to load configuration from environment variables.
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # JWT Configuration
    jwt_secret: str = "your-secret-key-change-in-production"
    access_token_expires_min: int = 15
    refresh_token_expires_days: int = 7

    # Database Configuration
    database_url: str = "sqlite:///./app.db"

    # Application
    environment: str = "development"

    class Config:
        """Pydantic config."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
