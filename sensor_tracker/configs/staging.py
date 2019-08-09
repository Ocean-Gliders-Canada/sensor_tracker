from sensor_tracker.configs.base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''  # refer to ceotr-admin

DEBUG = True

ALLOWED_HOSTS = ['bugs.ocean.dal.ca', 'glidertest.ocean.dal.ca:8001']

STATIC_ROOT = '/etc/nginx/html/sensor_tracker_stg/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sensor_tracker_stg',
        'USER': 'sensor_tracker',
        'PASSWORD': '',  # refer to ceotr-admin
        'HOST': 'localhost',
        'PORT': '5432',
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

FORCE_SCRIPT_NAME = '/sensor_tracker_stg'

INTERNAL_IPS = ['*']
