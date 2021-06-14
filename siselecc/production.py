from .settings import *
import os

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'siselecc',
        'USER':  env.str('USER'),
        'PASSWORD': env.str('PASSWORD'),
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Configure your Q cluster
# More details https://django-q.readthedocs.io/en/latest/configure.html
Q_CLUSTER = {
    "name": "conf",
    # Use Django's ORM + database for broker
    "orm": "default",
}

# STATIC_ROOT only required for deployment.
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
