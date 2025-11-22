from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.core.database import get_db
from app.core.config import settings
from app.core.security import create_access_token
from app.core.exceptions import InvalidCredentialsException, InactiveUserException, InvalidResetTokenException
from app.schemas import user as user_schemas
from app.schemas import token as token_schemas
from app.crud import user as user_crud
from app.crud import token as token_crud
from app.services.auth_service import AuthService

router = APIRouter()

@router.post("/register", response_model=user_schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_create: user_schemas.UserCreate,
    db: Session = Depends(get_db)
):
    """Register a new user"""
    return user_crud.create_user(db=db, user_create=user_create)

@router.post("/login", response_model=token_schemas.Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login user and return access token"""
    user = user_crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise InvalidCredentialsException()
    
    if not user.is_active:
        raise InactiveUserException()
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, 
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@router.post("/password-reset-request")
async def password_reset_request(
    request: token_schemas.PasswordResetRequest,
    db: Session = Depends(get_db),
    auth_service: AuthService = Depends()
):
    """Request password reset"""
    return await auth_service.request_password_reset(request.email, db)

@router.post("/password-reset-confirm")
async def password_reset_confirm(
    confirm: token_schemas.PasswordResetConfirm,
    db: Session = Depends(get_db),
    auth_service: AuthService = Depends()
):
    """Confirm password reset with token"""
    return await auth_service.confirm_password_reset(confirm.token, confirm.new_password, db)

@router.get("/verify-token")
async def verify_token(
    current_user = Depends(get_current_active_user)
):
    """Verify if token is valid"""
    return {"valid": True, "user": {"email": current_user.email, "id": str(current_user.id)}}