import os
import sys
from django.core.wsgi import get_wsgi_application

# Ensure project root is in sys.path
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.insert(0, path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "techshop.settings.production")

# MUST be at the absolute top-level for Vercel's build-time static analysis
app = get_wsgi_application()
application = app
