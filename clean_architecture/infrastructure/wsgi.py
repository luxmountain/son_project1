"""
WSGI config for Clean Architecture
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'infrastructure.settings')
application = get_wsgi_application()
