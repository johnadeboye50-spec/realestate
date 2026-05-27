import os

SECRET_KEY = 'a811ac582082ebdf2b72a05c9479d963eb552a05b473d8512661d72908f951e9'

# ===== DATABASE CONFIGURATION =====
# Use MySQL for development if you want to view the schema in MySQL Workbench.
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Johnperry144@localhost:3307/realestate_db'

# Suppress warning about tracking modifications (saves memory)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# ===== FILE UPLOAD SETTINGS =====
# Maximum file size for uploads (16MB = 16 * 1024 * 1024 bytes)
# Prevents users from uploading huge files that could crash your server
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

# Where to save uploaded property images
UPLOAD_FOLDER = os.path.join('app', 'static', 'uploads')

# Allowed file extensions for property images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# ===== PAGINATION =====
# Number of properties to show per page
PROPERTIES_PER_PAGE = 12

# ===== EMAIL CONFIGURATION (Optional - for contact forms) =====
# Use Gmail or other SMTP service to send emails
# Uncomment and fill when you need email functionality
# MAIL_SERVER = 'smtp.gmail.com'
# MAIL_PORT = 587
# MAIL_USE_TLS = True
# MAIL_USERNAME = 'your-email@gmail.com'
# MAIL_PASSWORD = 'your-app-password'  # Use App Password, not regular password
# MAIL_DEFAULT_SENDER = 'your-email@gmail.com'

# ===== SESSION CONFIGURATION =====
# How long user sessions last before requiring re-login
# 31 days = 31 * 24 * 60 * 60 seconds
PERMANENT_SESSION_LIFETIME = 2678400  # 31 days

# ===== DEVELOPMENT/DEBUG SETTINGS =====
# Set to False in production!
DEBUG = True

# Show detailed error pages (turn off in production)
TESTING = False

# ===== SECURITY HEADERS (Production) =====
# Uncomment these for production hosting
# SESSION_COOKIE_SECURE = True  # Only send cookies over HTTPS
# SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access to session cookie
# SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection

# ===== RECAPTCHA (Optional - prevent spam) =====
# Get keys from: https://www.google.com/recaptcha
# RECAPTCHA_PUBLIC_KEY = 'your-site-key'
# RECAPTCHA_PRIVATE_KEY = 'your-secret-key'
