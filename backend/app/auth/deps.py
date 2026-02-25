"""
Dependency injection functions for authentication and authorization.
"""
from typing import Optional
from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import User
from app.auth.tokens import decode_token, validate_token_expiry


def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
) -> User:
    """Get current authenticated user from JWT token.
    
    Args:
        authorization: Authorization header from request
        db: Database session
        
    Returns:
        User object
        
    Raises:
        HTTPException: If token is invalid, expired, or user not found
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = parts[1]
    
    payload = decode_token(token)
    if not payload or not validate_token_expiry(payload):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token claims",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


def require_role(*allowed_roles: str):
    """Dependency that requires user to have one of the specified roles.
    
    Args:
        allowed_roles: Tuple of allowed role strings
        
    Returns:
        Dependency function that validates user role
    """
    def check_role(current_user: User = Depends(get_current_user)) -> User:
        """Check if user has required role.
        
        Args:
            current_user: Current authenticated user
            
        Returns:
            User object if authorized
            
        Raises:
            HTTPException: If user role is not allowed
        """
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return current_user
    
    return check_role
