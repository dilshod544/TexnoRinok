import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'techshop.settings.production')
from techshop.wsgi import application
app = application
