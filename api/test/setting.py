import os

from django.contrib.admin import AdminSite

from app_common.utilities.file_prepare import check_create_dir
from app_common.config import DjangoConfigAgent

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PROJECT_NAME = "sensor_tracker"

LOCAL_APPS = [
    'general',
    'platforms',
    'instruments',
    'api',
]

DJANGO_APPS = [
    'django.contrib.admin',
    'django_filters',
    'rest_framework',
    'rest_framework.authtoken',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_admin_listfilter_dropdown',
    'log',
    'drf_yasg',
]

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sensor_tracker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'api/html/'),
            os.path.join(BASE_DIR, 'sensor_tracker/templates/'),
            os.path.join(BASE_DIR, 'api/templates/'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    }
]

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/sensor_tracker/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static/"),
]
SUIT_CONFIG = {
    'ADMIN_NAME': 'Sensor Tracker',
    'SEARCH_URL': ''
}

RESOURCE_DIR = check_create_dir(os.path.join(os.path.expanduser("~"), "resource"))
PROJECT_RESOURCE_DIR = check_create_dir(os.path.join(RESOURCE_DIR, PROJECT_NAME))
user_yml_setting = os.path.join(*[PROJECT_RESOURCE_DIR, "passwd", "pw_info.yml"])
config_agent = DjangoConfigAgent()
config_agent.load(setting_path=user_yml_setting,
                  setting_template=os.path.join(os.path.dirname(__file__), 'config.yml.stock'))

MEDIA_ROOT = PROJECT_RESOURCE_DIR
MEDIA_URL = '/media/'

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
}

AdminSite.site_header = 'Sensor Tracker'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config_agent.django_settings['SECRET_KEY']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config_agent.database['NAME'],
        'USER': config_agent.database['USER'],
        'PASSWORD': config_agent.database['PASSWORD'],
        'HOST': 'localhost',
        'PORT': '5432'
    }
}

ALLOWED_HOSTS = config_agent.general_info['ALLOWED_HOSTS']

DEBUG = config_agent.DEBUG

STATIC_ROOT = '/etc/nginx/html/sensor_tracker/'
FILE_UPLOAD_MAX_MEMORY_SIZE = 20000
if config_agent.general_info['STATIC_ROOT']:
    STATIC_ROOT = config_agent.general_info['STATIC_ROOT']

if DEBUG:
    DEVELOPMENT_APPS = [
        'debug_toolbar',
    ]

    INSTALLED_APPS = INSTALLED_APPS + DEVELOPMENT_APPS

    DEVELOPMENT_MIDDLEWAARE = [
        'debug_toolbar.middleware.DebugToolbarMiddleware'
    ]
    MIDDLEWARE = MIDDLEWARE + DEVELOPMENT_MIDDLEWAARE

    INTERNAL_IPS = ['127.0.0.1']
