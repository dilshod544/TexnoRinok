from .base import *
from decouple import config, Csv

DEBUG = True

# Override logging for detailed output
LOGGING['root']['level'] = 'DEBUG'

import os

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*', cast=Csv())
if '.vercel.app' not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append('.vercel.app')

# Render dynamic hostname support
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

import dj_database_url

# HTTPS & Security
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = False  # Vercel handles SSL termination
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# Database configuration using single DATABASE_URL env var
DATABASES = {
    'default': dj_database_url.config(
        default=config('POSTGRES_URL', default=config('DATABASE_URL', default='')),
        conn_max_age=600,
        ssl_require=True,
    )
}
