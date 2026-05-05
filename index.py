import os
import sys
import traceback

# 1. Ensure project root is in sys.path FIRST
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.insert(0, path)

# 2. Set settings module BEFORE importing Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "techshop.settings.production")

# 3. Use pg8000 as psycopg2 replacement (pure Python, works on Vercel)
try:
    import psycopg2
except ImportError:
    try:
        from pg8000 import dbapi
        sys.modules["psycopg2"] = dbapi
        sys.modules["psycopg2.extensions"] = dbapi
        sys.modules["psycopg2.extras"] = dbapi
    except ImportError:
        pass

# 4. Initialize Django
try:
    from django.core.wsgi import get_wsgi_application
    app = get_wsgi_application()
except Exception as e:
    error_msg = traceback.format_exc()
    print(f"Django startup error:\n{error_msg}", file=sys.stderr)

    def app(environ, start_response):
        status = '500 Internal Server Error'
        output = f"Django failed to start:\n\n{error_msg}".encode('utf-8')
        response_headers = [
            ('Content-type', 'text/plain'),
            ('Content-Length', str(len(output)))
        ]
        start_response(status, response_headers)
        return [output]

# Top-level export for Vercel
application = app
