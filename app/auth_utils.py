import os 
import secrets
import smtplib
from email.message import EmailMessage
from app import app


def generate_verification_code(length=6):
    """Generate a random verification code ."""
    return ''.join(secrets.choice('0123456789') for _ in range(length))

def send_email(to_email, subject, body):
    """Send a plain text email via SMTP."""
    host = os.getenv('SMTP_HOST')
    port = int(os.getenv('SMTP_PORT', '587'))
    user = os.getenv('SMTP_USER')
    password = os.getenv('SMTP_PASSWORD')
    sender = os.getenv('SMTP_FROM') or user
    use_tls = os.getenv('SMTP_USE_TLS', 'true').lower() == 'true'

    if not host or not user or not password:
        app.logger.error("SMTP not configured. Email not sent.")
        return False

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to_email
    msg.set_content(body)

    try:
        with smtplib.SMTP(host, port) as server:
            if use_tls:
                server.starttls()
            server.login(user, password)
            server.send_message(msg)
        return True
    except Exception as e:
        app.logger.error(f"Failed to send email: {e}")
        return False
    
def send_verification_code_message(to_email, code, expiry_minutes=30):
    body = (
        "Welcome to The Property \n\n"
        f"Your email verification code is: {code}\n\n"
        f"This code will expire in {expiry_minutes} minutes.\n\n"
    )
    return send_email(to_email, "Email Verification Code", body)
