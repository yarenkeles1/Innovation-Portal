"""
Authentication API routes.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.auth import UserRegisterRequest, UserLoginRequest, TokenResponse, UserResponse
from app.auth.service import AuthService

router = APIRouter()

# Bcrypt maximum password length
MAX_PASSWORD_LENGTH = 72


@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
def register(
    request: UserRegisterRequest,
    db: Session = Depends(get_db),
) -> dict:
    """Register a new user.
    
    Args:
        request: Registration request with email and password
        db: Database session
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If email is already registered or validation fails
    """
    try:
        # Validate email format (basic check)
        if len(request.email) > 320:
            raise ValueError("Email is too long")
        
        # Validate password strength and length (bcrypt limit is 72 bytes)
        if len(request.password) < 8:
            raise ValueError("Password must be at least 8 characters")
        
        if len(request.password) > MAX_PASSWORD_LENGTH:
            raise ValueError(f"Password must be at most {MAX_PASSWORD_LENGTH} characters")
        
        # Register user
        user = AuthService.register_user(request.email, request.password, db)
        
        return {"message": "user created"}
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration failed",
        )


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login(
    request: UserLoginRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """Authenticate user and return tokens.
    
    Args:
        request: Login request with email and password
        db: Database session
        
    Returns:
        TokenResponse with access_token, refresh_token, and expires_in
        
    Raises:
        HTTPException: If credentials are invalid
    """
    try:
        # Authenticate user
        user = AuthService.authenticate_user(request.email, request.password, db)
        
        # Create tokens
        tokens = AuthService.create_tokens(user, db)
        
        return TokenResponse(**tokens)
    
    except ValueError:
        # Use generic error message to prevent user enumeration
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
