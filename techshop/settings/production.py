from .base import *

DEBUG = False
ALLOWED_HOSTS = ['*']

# Ensure you set the ALLOWED_HOSTS properly in the .env file in production
# Example: ALLOWED_HOSTS=example.com,www.example.com

# Security headers for production
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True

# If using HTTPS:
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_HSTS_SECONDS = 31536000
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
