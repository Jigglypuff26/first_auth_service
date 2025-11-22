from sqlalchemy.orm import Session
from app.core.security import get_password_hash
from app.core.exceptions import InvalidResetTokenException
from app.crud import user as user_crud
from app.crud import token as token_crud
from app.services.email_service import EmailService

class AuthService:
    def __init__(self):
        self.email_service = EmailService()
    
    async def request_password_reset(self, email: str, db: Session):
        user = user_crud.get_user_by_email(db, email)
        
        # For security reasons, don't reveal if email exists
        if not user or not user.is_active:
            return {
                "message": "If the email exists in our system, you will receive password reset instructions"
            }
        
        # Create reset token
        reset_token = token_crud.create_reset_token(db, str(user.id))
        
        # Send email (in production)
        if self.email_service.is_configured():
            await self.email_service.send_password_reset_email(
                email=user.email,
                token=reset_token.token,
                user_name=user.full_name or user.email
            )
        
        return {
            "message": "If the email exists in our system, you will receive password reset instructions"
        }
    
    async def confirm_password_reset(self, token: str, new_password: str, db: Session):
        reset_token = token_crud.get_valid_reset_token(db, token)
        if not reset_token:
            raise InvalidResetTokenException()
        
        # Update password
        hashed_password = get_password_hash(new_password)
        user_crud.update_user_password(db, str(reset_token.user_id), hashed_password)
        
        # Mark token as used
        token_crud.mark_token_as_used(db, str(reset_token.id))
        
        return {"message": "Password has been reset successfully"}