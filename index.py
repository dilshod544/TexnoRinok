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

# Setup Django properly before running commands
django.setup()

# Run migrations automatically on Vercel (Disabled temporarily for debugging)
# try:
#     print("Starting migrations...")
#     call_command('migrate', interactive=False)
#     print("Migrations completed successfully.")
# except Exception as e:
#     import traceback
#     print("Migration error occurred:")
#     traceback.print_exc()

# Get WSGI application
app = get_wsgi_application()
application = app
