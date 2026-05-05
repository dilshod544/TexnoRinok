import os
import sys
import traceback

# 1. Ensure project root is in sys.path FIRST
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.insert(0, path)

# 2. Set settings module BEFORE importing Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "techshop.settings.production")

# 3. Try to initialize Django, catch and display any errors
try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    app = application
except Exception as e:
    # If Django fails to start, return the error as plain text
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

    application = app
