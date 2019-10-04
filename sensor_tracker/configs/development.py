from sensor_tracker.configs.base import *

DEBUG = True

STATIC_ROOT = '/usr/local/etc/nginx/html/sensor_tracker/'

DEVELOPMENT_APPS = [
    'debug_toolbar',
]

INSTALLED_APPS = INSTALLED_APPS + DEVELOPMENT_APPS

DEVELOPMENT_MIDDLEWAARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]
MIDDLEWARE = MIDDLEWARE + DEVELOPMENT_MIDDLEWAARE

INTERNAL_IPS = ['127.0.0.1']
