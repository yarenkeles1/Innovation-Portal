"""
Authentication service functions for business logic.
"""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models import User, RefreshToken
from app.auth.security import hash_password, verify_password
from app.auth.tokens import create_access_token, create_refresh_token
from app.core.settings import settings


class AuthService:
    """Service class for authentication operations."""

    @staticmethod
    def register_user(email: str, password: str, db: Session) -> User:
        """Register a new user.
        
        Args:
            email: User email address
            password: Plain text password
            db: Database session
            
        Returns:
            Created User object
            
        Raises:
            ValueError: If email already exists
        """
        hashed_pwd = hash_password(password)
        user = User(email=email.lower(), hashed_password=hashed_pwd)
        
        try:
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        except IntegrityError:
            db.rollback()
            raise ValueError(f"Email {email} is already registered")

    @staticmethod
    def authenticate_user(email: str, password: str, db: Session) -> User:
        """Authenticate a user with email and password.
        
        Args:
            email: User email address
            password: Plain text password
            db: Database session
            
        Returns:
            User object if authentication successful
            
        Raises:
            ValueError: If credentials are invalid
        """
        user = db.query(User).filter(User.email == email.lower()).first()
        
        if not user or not verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")
        
        return user

    @staticmethod
    def create_tokens(user: User, db: Session) -> dict:
        """Create access and refresh tokens for a user.
        
        Args:
            user: User object
            db: Database session
            
        Returns:
            Dictionary with access_token, refresh_token, and expires_in
        """
        # Create access token
        access_token = create_access_token(user.id, user.role)
        
        # Create refresh token
        jti, refresh_token = create_refresh_token()
        
        # Store refresh token in database
        expires_at = datetime.utcnow() + timedelta(
            days=settings.refresh_token_expires_days
        )
        token_record = RefreshToken(
            jti=jti,
            user_id=user.id,
            expires_at=expires_at,
        )
        db.add(token_record)
        db.commit()
        
        # Return token information
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": settings.access_token_expires_min * 60,  # Convert to seconds
        }
