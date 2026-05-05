import os
import sys

# Pure Python PostgreSQL driver for Vercel compatibility
try:
    import pg8000.native
    # Monkeypatch psycopg2 to use pg8000
    # This allows Django's standard postgres backend to work without psycopg2 binary
    from pg8000 import psycopg2
    sys.modules["psycopg2"] = psycopg2
except ImportError:
    pass

from django.core.wsgi import get_wsgi_application

# Ensure project root is in sys.path
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.insert(0, path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "techshop.settings.production")

# WSGI application entry point
app = get_wsgi_application()
application = app
