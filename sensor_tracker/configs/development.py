from sensor_tracker.configs.base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '12345'

DEBUG = True

ALLOWED_HOSTS = ['*']

STATIC_ROOT = '/usr/local/etc/nginx/html/sensor_tracker/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sensor_tracker',
        'USER': 'sensor_tracker',
        'PASSWORD': '12345',
        'HOST': 'localhost',
        'PORT': '',
    }
}

DEVELOPMENT_APPS = [
    'debug_toolbar',
]

INSTALLED_APPS = INSTALLED_APPS + DEVELOPMENT_APPS

DEVELOPMENT_MIDDLEWAARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]
MIDDLEWARE = MIDDLEWARE + DEVELOPMENT_MIDDLEWAARE

INTERNAL_IPS = ['127.0.0.1']

