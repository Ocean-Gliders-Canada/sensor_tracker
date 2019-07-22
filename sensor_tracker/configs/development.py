from sensor_tracker.configs.base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '12345'

DEBUG = True

ALLOWED_HOSTS = ['*']

STATIC_ROOT = '/usr/local/etc/nginx/html/sensor_tracker/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sensor_tracker3',
        'USER': 'xiang',
        'PASSWORD': '12345',
        'HOST': 'localhost',
        'PORT': '',
    }
}

DEVELOPMENT_APPS = [
    'debug_toolbar',
    'django_filters'
]

INSTALLED_APPS = INSTALLED_APPS + DEVELOPMENT_APPS

DEVELOPMENT_MIDDLEWAARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]
MIDDLEWARE = MIDDLEWARE + DEVELOPMENT_MIDDLEWAARE

INTERNAL_IPS = ['127.0.0.1']


REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
}

