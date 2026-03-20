"""
WSGI config for hindex project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application


environment = os.getenv('TIER', "local").title()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'hindex.config.{environment.lower()}')
os.environ.setdefault("DJANGO_CONFIGURATION", environment)

application = get_wsgi_application()
