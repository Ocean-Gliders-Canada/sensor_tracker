from sensor_tracker.configs.base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '12345'

DEBUG = True

ALLOWED_HOSTS = ['*']

STATIC_ROOT = '/usr/local/etc/nginx/html/sensor_tracker/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sensor_tracker_2019_04_12',
        'USER': 'sensor_tracker',
        'PASSWORD': '12345',
        'HOST': 'localhost',
        'PORT': '',
    }
}
