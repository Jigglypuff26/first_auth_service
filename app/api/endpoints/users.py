from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.dependencies import get_current_active_user
from app.schemas.user import UserResponse

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user=Depends(get_current_active_user)):
    """Get current user information"""
    return current_user

@router.get("/{user_id}", response_model=UserResponse)
async def read_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user)
):
    """Get user by ID (for testing purposes)"""
    from app.crud.user import get_user
    return get_user(db, user_id)