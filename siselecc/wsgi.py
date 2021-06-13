"""
WSGI config for siselecc project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
import environ

from django.core.wsgi import get_wsgi_application

# _____________________________________________________________________
# environ init
env = environ.Env()
environ.Env.read_env()
# ____________________
os.environ["DJANGO_SETTINGS_MODULE"] = env.str('DJANGO_SETTINGS_MODULE')

application = get_wsgi_application()
