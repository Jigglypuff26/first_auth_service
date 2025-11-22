from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
import secrets
from app.models.token import PasswordResetToken

def create_reset_token(db: Session, user_id: str, expires_hours: int = 1) -> PasswordResetToken:
    # Delete any existing tokens for this user
    db.query(PasswordResetToken).filter(PasswordResetToken.user_id == user_id).delete()
    
    token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(hours=expires_hours)
    
    reset_token = PasswordResetToken(
        user_id=user_id,
        token=token,
        expires_at=expires_at
    )
    
    db.add(reset_token)
    db.commit()
    db.refresh(reset_token)
    return reset_token

def get_valid_reset_token(db: Session, token: str) -> Optional[PasswordResetToken]:
    return db.query(PasswordResetToken).filter(
        PasswordResetToken.token == token,
        PasswordResetToken.expires_at > datetime.utcnow(),
        PasswordResetToken.is_used == False
    ).first()

def mark_token_as_used(db: Session, token_id: str) -> None:
    token = db.query(PasswordResetToken).filter(PasswordResetToken.id == token_id).first()
    if token:
        token.is_used = True
        db.commit()