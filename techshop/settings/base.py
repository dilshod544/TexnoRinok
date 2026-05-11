from pathlib import Path
import os
from decouple import config

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Security
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production-use-env-variable')
DEBUG = config('DEBUG', default=True, cast=bool)


def _split_csv(value):
    return [item.strip() for item in (value or '').split(',') if item.strip()]


def _unique(values):
    seen = set()
    result = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result


DEFAULT_ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.vercel.app',
    '.onrender.com',
    'texnorinokmalika.uz',
    'www.texnorinokmalika.uz',
]
ALLOWED_HOSTS = _unique(
    _split_csv(config('ALLOWED_HOSTS', default='')) or DEFAULT_ALLOWED_HOSTS
)

DEFAULT_CSRF_TRUSTED_ORIGINS = [
    'https://texnorinokmalika.uz',
    'https://www.texnorinokmalika.uz',
]
CSRF_TRUSTED_ORIGINS = _unique(
    _split_csv(config('CSRF_TRUSTED_ORIGINS', default='')) or DEFAULT_CSRF_TRUSTED_ORIGINS
)

# Application definition
INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    # Local apps
    'apps.products',
    'apps.cart',
    'apps.orders',
    'apps.accounts',
    'apps.store_admin',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'techshop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'apps.cart.context_processors.cart_count',
                'apps.products.context_processors.categories',
            ],
        },
    },
]

WSGI_APPLICATION = 'techshop.wsgi.application'

import dj_database_url

# Database — Switch between Vercel/Neon Postgres and local SQLite
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
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'uz'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ('uz', "O'zbekcha"),
    ('ru', 'Русский'),
]

MODELTRANSLATION_DEFAULT_LANGUAGE = 'uz'
MODELTRANSLATION_LANGUAGES = ('uz', 'ru')
MODELTRANSLATION_FALLBACK_LANGUAGES = ('uz',)

LOCALE_PATHS = [BASE_DIR / 'locale']

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
# Static files (always use WhiteNoise for now)
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.StaticFilesStorage'

USE_S3 = config('USE_S3', default=False, cast=bool)

if USE_S3:
    INSTALLED_APPS.append('storages')
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_ENDPOINT_URL = config('AWS_S3_ENDPOINT_URL', default=f'https://ckzmzsgkuqyuauhwbzdr.supabase.co/storage/v1/s3')
    AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='eu-central-1')
    AWS_S3_ADDRESSING_STYLE = 'path'
    
    # SUPABASE PUBLIC URL FORMAT
    AWS_S3_CUSTOM_DOMAIN = f'ckzmzsgkuqyuauhwbzdr.supabase.co/storage/v1/object/public/{AWS_STORAGE_BUCKET_NAME}'
    
    AWS_DEFAULT_ACL = None
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_FILE_OVERWRITE = False
    
    DEFAULT_FILE_STORAGE = 'techshop.storage_backends.SupabaseMediaStorage'
else:
    MEDIA_ROOT = BASE_DIR / 'media'

MEDIA_URL = '/media/'
WHITENOISE_MANIFEST_STRICT = False

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Auth
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Domain / SEO
SITE_DOMAIN = config('SITE_DOMAIN', default='texnorinokmalika.uz')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
