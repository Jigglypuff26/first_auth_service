import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

class EmailService:
    def __init__(self):
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.smtp_username = settings.SMTP_USERNAME
        self.smtp_password = settings.SMTP_PASSWORD
        self.from_email = settings.FROM_EMAIL
    
    def is_configured(self) -> bool:
        return all([
            self.smtp_server,
            self.smtp_username,
            self.smtp_password,
            self.from_email
        ])
    
    async def send_password_reset_email(self, email: str, token: str, user_name: str = None):
        if not self.is_configured():
            print(f"Password reset token for {email}: {token}")
            return
        
        subject = "Password Reset Request"
        
        # In production, you would use your actual frontend URL
        reset_url = f"https://yourapp.com/reset-password?token={token}"
        
        body = f"""
        Hello {user_name or 'User'},
        
        You have requested to reset your password. Please click the link below to reset your password:
        
        {reset_url}
        
        This link will expire in 1 hour.
        
        If you did not request this reset, please ignore this email.
        
        Best regards,
        The Auth Service Team
        """
        
        html_body = f"""
        <html>
            <body>
                <h2>Password Reset Request</h2>
                <p>Hello {user_name or 'User'},</p>
                <p>You have requested to reset your password. Please click the link below to reset your password:</p>
                <p><a href="{reset_url}">Reset Password</a></p>
                <p>This link will expire in 1 hour.</p>
                <p>If you did not request this reset, please ignore this email.</p>
                <br>
                <p>Best regards,<br>The Auth Service Team</p>
            </body>
        </html>
        """
        
        await self._send_email(email, subject, body, html_body)
    
    async def _send_email(self, to_email: str, subject: str, body: str, html_body: str = None):
        message = MIMEMultipart("alternative")
        message["From"] = self.from_email
        message["To"] = to_email
        message["Subject"] = subject
        
        message.attach(MIMEText(body, "plain"))
        if html_body:
            message.attach(MIMEText(html_body, "html"))
        
        try:
            await aiosmtplib.send(
                message,
                hostname=self.smtp_server,
                port=self.smtp_port,
                username=self.smtp_username,
                password=self.smtp_password,
                use_tls=True
            )
        except Exception as e:
            print(f"Failed to send email: {e}")
            # In production, you might want to log this properly