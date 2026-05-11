from .base import *
from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)

# Override logging for detailed output
LOGGING['root']['level'] = 'DEBUG'

import os

# Render dynamic hostname support
render_hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if render_hostname and render_hostname not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(render_hostname)
    https_origin = f'https://{render_hostname}'
    if https_origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(https_origin)

import dj_database_url

# HTTPS & Security
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = False  # Vercel/Render handle SSL termination
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

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


# Supabase Storage (optional, if credentials are present)
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', default='')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', default='')
if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME', default='media')
    AWS_S3_ENDPOINT_URL = config('AWS_S3_ENDPOINT_URL', default='https://ckzmzsgkuqyuauhwbzdr.supabase.co/storage/v1/s3')
    AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='eu-central-1')
    AWS_S3_CUSTOM_DOMAIN = config('AWS_S3_CUSTOM_DOMAIN', default=f'ckzmzsgkuqyuauhwbzdr.supabase.co/storage/v1/object/public/{AWS_STORAGE_BUCKET_NAME}')
    AWS_DEFAULT_ACL = None
    AWS_S3_ADDRESSING_STYLE = 'path'
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_FILE_OVERWRITE = False

    DEFAULT_FILE_STORAGE = 'techshop.storage_backends.SupabaseMediaStorage'
    if 'storages' not in INSTALLED_APPS:
        INSTALLED_APPS.append('storages')
