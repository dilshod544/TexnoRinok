import os
import sys
from django.core.wsgi import get_wsgi_application

# Add current directory to path to ensure techshop package is findable
sys.path.append(os.path.join(os.path.dirname(__file__)))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "techshop.settings.production")

application = get_wsgi_application()
app = application
