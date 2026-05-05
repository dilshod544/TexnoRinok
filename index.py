import os
import sys

# Add current directory to path
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "techshop.settings.production")

try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    app = application
except Exception as e:
    # Log the error to stderr so it shows up in Vercel logs
    print(f"CRITICAL: Failed to load Django application: {e}", file=sys.stderr)
    raise e
