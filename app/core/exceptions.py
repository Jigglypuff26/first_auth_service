from fastapi import HTTPException, status

class AuthException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class UserNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

class UserAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

class InvalidCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

class InactiveUserException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")

class InvalidResetTokenException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired reset token")