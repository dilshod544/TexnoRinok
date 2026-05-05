import os
import sys
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

# Ensure project root is in sys.path
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.insert(0, path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "techshop.settings.production")

# Run migrations automatically on Vercel
try:
    call_command('migrate', interactive=False)
except Exception as e:
    print(f"Migration error: {e}")

# MUST be at the absolute top-level for Vercel's build-time static analysis
app = get_wsgi_application()
application = app
