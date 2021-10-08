"""
Django settings for siselecc project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
# _________________________________________________
prototipo_e-vote
BASE_DIR
SECRET_KEY
DEBUG
ALLOWED_HOSTS
INSTALLED_APPS
MIDDLEWARE
Q_CLUSTER
ROOT_URLCONF
TEMPLATES
WSGI_APPLICATION
AUTH_PASSWORD_VALIDATORS
LANGUAGE_CODE
TIME_ZONE
USE_I18N
USE_L10N
USE_TZ
STATIC_URL
STATICFILES_DIRS
"""

from pathlib import Path
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/


# _____________________________________________________________________
# environ init
env = environ.Env()
environ.Env.read_env()
# ____________________

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = tuple(env.list('ALLOWED_HOSTS', default=[]))


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #
    'apps.gest_usuario',
    'apps.gest_elector',
    'apps.gest_cargo',
    'apps.gest_preparacion',
    'apps.gest_programacion',
    'apps.gest_cifrado',
    'apps.gest_votacion',
    'apps.bienvenida',
    # LIBRARIES
    # # for import/export data with included Django admin.
    'import_export',
    # A multiprocessing task queue for Django
    'django_q',
    # https://django-debug-toolbar.readthedocs.io/en/latest/installation.html
    'debug_toolbar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# Configure your Q cluster
# More details https://django-q.readthedocs.io/en/latest/configure.html


ROOT_URLCONF = 'siselecc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {'extras': 'siselecc.templatetags.extras', }
        },
    },
]

WSGI_APPLICATION = 'siselecc.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'es-ar'

TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

# Email
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD')

# Para django toolbar
INTERNAL_IPS = tuple(env.list('ALLOWED_HOSTS', default=[]))
