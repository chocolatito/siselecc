from .settings import *
<<<<<<< HEAD

=======
import os
>>>>>>> b2470755c0381c26487255a6a234eafb66578674
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

# STATIC_ROOT only required for deployment.
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
