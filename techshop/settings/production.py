from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    'fossil-five.vercel.app',
    '.vercel.app',
    'localhost',
    '127.0.0.1',
]

SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_MANIFEST_STRICT = False
