import os
import sys

# Ensure project root is in sys.path
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.insert(0, path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "techshop.settings.production")

try:
    from django.core.wsgi import get_wsgi_application
    app = get_wsgi_application()
except Exception as e:
    import traceback
    print("CRITICAL ERROR DURING INITIALIZATION:", file=sys.stderr)
    print(traceback.format_exc(), file=sys.stderr)
    # Return a simple response if possible, but Vercel handles stderr well
    raise e
