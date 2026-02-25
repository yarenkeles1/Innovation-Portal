"""
Admin API routes with role-based access control.
"""
from fastapi import APIRouter, Depends

from app.models import User
from app.auth.deps import require_role

router = APIRouter()


@router.get("/status", response_model=dict)
def get_admin_status(
    current_user: User = Depends(require_role("admin")),
) -> dict:
    """Get admin status endpoint (admin only).
    
    Args:
        current_user: Current authenticated user (must have admin role)
        
    Returns:
        Status dictionary
    """
    return {"status": "ok"}
