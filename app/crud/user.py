from sqlalchemy.orm import Session
from typing import Optional
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password
from app.core.exceptions import UserNotFoundException, UserAlreadyExistsException

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def get_user(db: Session, user_id: str) -> User:
    user = get_user_by_id(db, user_id)
    if not user:
        raise UserNotFoundException()
    return user

def create_user(db: Session, user_create: UserCreate) -> User:
    # Check if user already exists
    db_user = get_user_by_email(db, user_create.email)
    if db_user:
        raise UserAlreadyExistsException()
    
    hashed_password = get_password_hash(user_create.password)
    db_user = User(
        email=user_create.email,
        hashed_password=hashed_password,
        full_name=user_create.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def update_user_password(db: Session, user_id: str, new_hashed_password: str) -> User:
    user = get_user(db, user_id)
    user.hashed_password = new_hashed_password
    db.commit()
    db.refresh(user)
    return user