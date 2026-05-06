from .base import *
from decouple import config, Csv

DEBUG = config('DEBUG', default=False, cast=bool)

# Override logging for detailed output
LOGGING['root']['level'] = 'DEBUG'

import os

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*', cast=Csv())
if '*' not in ALLOWED_HOSTS:
    if '.vercel.app' not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append('.vercel.app')
    
    # Render dynamic hostname support
    RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
    if RENDER_EXTERNAL_HOSTNAME and RENDER_EXTERNAL_HOSTNAME not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

import dj_database_url

# HTTPS & Security
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = False  # Vercel/Render handle SSL termination
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# Use POSTGRES_URL or DATABASE_URL if available, otherwise fallback to base settings (SQLite)
db_url = config('POSTGRES_URL', default=config('DATABASE_URL', default=None))

if db_url:
    DATABASES = {
        'default': dj_database_url.config(
            default=db_url,
            conn_max_age=600,
            ssl_require=True,
        )
    }
else:
    # Keep the default from base.py (likely SQLite)
    pass


# Force Supabase Storage for Production
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME', default='media')
AWS_S3_ENDPOINT_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.ckzmzsgkuqyuauhwbzdr.supabase.co'
AWS_S3_REGION_NAME = 'eu-central-1'
AWS_S3_CUSTOM_DOMAIN = f'ckzmzsgkuqyuauhwbzdr.supabase.co/storage/v1/object/public/{AWS_STORAGE_BUCKET_NAME}'
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False

DEFAULT_FILE_STORAGE = 'techshop.storage_backends.SupabaseMediaStorage'
if 'storages' not in INSTALLED_APPS:
    INSTALLED_APPS.append('storages')
