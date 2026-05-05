import os
import sys
import traceback

# 1. Ensure project root is in sys.path FIRST
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.insert(0, path)

# 2. Set settings module BEFORE importing Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "techshop.settings.production")

# 4. Initialize Django
try:
    from django.core.wsgi import get_wsgi_application
    _app = get_wsgi_application()
except Exception as e:
    error_msg = traceback.format_exc()
    print(f"Django startup error:\n{error_msg}", file=sys.stderr)

    def _app(environ, start_response):
        status = '500 Internal Server Error'
        output = f"Django failed to start:\n\n{error_msg}".encode('utf-8')
        response_headers = [
            ('Content-type', 'text/plain'),
            ('Content-Length', str(len(output)))
        ]
        start_response(status, response_headers)
        return [output]

# Wrap the WSGI app to catch runtime errors as well
def application(environ, start_response):
    try:
        return _app(environ, start_response)
    except Exception as e:
        error_msg = traceback.format_exc()
        print(f"WSGI Runtime error:\n{error_msg}", file=sys.stderr)
        status = '500 Internal Server Error'
        output = f"Django WSGI runtime error:\n\n{error_msg}".encode('utf-8')
        response_headers = [
            ('Content-type', 'text/plain'),
            ('Content-Length', str(len(output)))
        ]
        start_response(status, response_headers)
        return [output]
