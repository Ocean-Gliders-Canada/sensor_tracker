from sensor_tracker.configs.base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''  # refer to ceotr-admin

DEBUG = False

ALLOWED_HOSTS = ['bugs.ocean.dal.ca']

STATIC_ROOT = '/etc/nginx/html/sensor_tracker/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sensor_tracker',
        'USER': 'sensor_tracker',
        'PASSWORD': '',  # refer to ceotr-admin
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

FORCE_SCRIPT_NAME = '/sensor_tracker'
