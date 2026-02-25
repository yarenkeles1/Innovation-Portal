"""
JWT token creation and validation utilities.
"""
from datetime import datetime, timedelta
from typing import Optional
import uuid

from jose import JWTError, jwt

from app.core.settings import settings


def create_access_token(user_id: int, role: str) -> str:
    """Create a JWT access token.
    
    Args:
        user_id: ID of the user
        role: Role of the user (e.g., 'user' or 'admin')
        
    Returns:
        JWT access token string
    """
    exp = datetime.utcnow() + timedelta(minutes=settings.access_token_expires_min)
    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": exp,
        "iat": datetime.utcnow(),
    }
    token = jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm="HS256",
    )
    return token


def create_refresh_token() -> tuple[str, str]:
    """Create a JWT refresh token with a unique JTI.
    
    Returns:
        Tuple of (jti, token) where jti is the unique identifier and token is the JWT
    """
    jti = str(uuid.uuid4())
    exp = datetime.utcnow() + timedelta(days=settings.refresh_token_expires_days)
    payload = {
        "jti": jti,
        "exp": exp,
        "iat": datetime.utcnow(),
    }
    token = jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm="HS256",
    )
    return jti, token


def decode_token(token: str) -> Optional[dict]:
    """Decode and validate a JWT token.
    
    Args:
        token: JWT token string
        
    Returns:
        Dictionary of claims if valid, None if invalid or expired
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=["HS256"],
        )
        return payload
    except JWTError:
        return None


def validate_token_expiry(payload: dict) -> bool:
    """Validate that a token has not expired.
    
    Args:
        payload: Decoded token payload
        
    Returns:
        True if token is not expired, False otherwise
    """
    if "exp" not in payload:
        return False
    
    exp_timestamp = payload["exp"]
    return datetime.utcfromtimestamp(exp_timestamp) > datetime.utcnow()
