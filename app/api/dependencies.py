from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_token
from app.crud.user import get_user_by_id
from app.core.exceptions import AuthException

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    payload = verify_token(token)
    if payload is None:
        raise AuthException("Invalid authentication credentials")
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise AuthException("Invalid token")
    
    user = get_user_by_id(db, user_id)
    if user is None:
        raise AuthException("User not found")
    
    return user

def get_current_active_user(current_user=Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user