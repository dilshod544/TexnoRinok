import os
import sys
import django
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

# Ensure project root is in sys.path
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.insert(0, path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "techshop.settings.production")

# IMPORTANT: Initialize Django first
django.setup()

# Run migrations once on startup
try:
    print("Executing database migrations...")
    call_command('migrate', interactive=False)
    print("Migrations successful.")
except Exception:
    import traceback
    print("AUTO-MIGRATION FAILED:")
    traceback.print_exc()

# Vercel MUST see these at the top-level
app = get_wsgi_application()
application = app
