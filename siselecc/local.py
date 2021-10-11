
from .settings import *


# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html
# 'debug_toolbar',
INSTALLED_APPS.append('debug_toolbar')


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# STATICFILES_DIRS only required for development.
STATICFILES_DIRS = [("static")]


# Para django toolbar
INTERNAL_IPS = ['127.0.0.1', ]
