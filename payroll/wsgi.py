"""
WSGI config for payroll project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Use Heroku settings by default, fallback to production
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'payroll.settings.heroku')

application = get_wsgi_application()
