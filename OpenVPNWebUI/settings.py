"""
Django settings for OpenVPNWebUI project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
import platform
from django.contrib.messages import constants as messages
# read user setting from config.yml
from .conf import ConfigManager

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG = ConfigManager.load_user_config()
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY') or 'django-insecure-803cf=uonr+vx87tjd5)xd8qxn0mfnh5h=9cwvqk!4=-+u+@a7'

# SECURITY WARNING: don't run with debug turned on in production!
if platform.system().startswith("Windows"):
    DEBUG = False
else:
    DEBUG = CONFIG.DEBUG or False

ALLOWED_HOSTS = ['*', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ovpn.apps.OvpnConfig',
    'users.apps.UsersConfig',
    'authentication.apps.AuthenticationConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'authentication.middleware.auth.AuthMiddleware',
]

ROOT_URLCONF = 'OpenVPNWebUI.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'utils.context_processors.get_version_number',
                'utils.context_processors.get_openvpn_servers',
            ],
        },
    },
]

WSGI_APPLICATION = 'OpenVPNWebUI.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.{}'.format(CONFIG.DB_ENGINE.lower()),
        'NAME': CONFIG.DB_NAME,
        'USER': CONFIG.DB_USER,
        'PASSWORD': CONFIG.DB_PASSWORD,
        'HOST': CONFIG.DB_HOST,
        'PORT': int(CONFIG.DB_PORT),
        'OPTIONS': {
            'charset': 'utf8mb4'},
    }}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

version_file_path = Path(BASE_DIR, "version.txt")
if version_file_path.is_file():
    with open(version_file_path) as v_file:
        APP_VERSION_NUMBER = v_file.read().strip()

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
# 4h
SESSION_COOKIE_AGE = 60 * 60 * 4 

# logs
if DEBUG:
    main_log_file = "logs/OpenVPNWEBUI.log"
    req_log_file = "logs/django_request.log"
else:
    main_log_file = CONFIG.LOG_FILES
    req_log_file = CONFIG.REQ_LOG_FILES
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        "verbose": {
            "format":  "{asctime} {process:d} {threadName} {thread:d} {filename} {lineno} {levelname}: {message}",
            # {filename} - views.py
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    'filters': {
        # 'special': {
        #     '()': 'project.logging.SpecialFilter',
        #     'foo': 'bar',
        # },
        # catch log only if debug is True
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'default': {
            'level':CONFIG.LOG_LEVEL or "INFO",
            'class':'logging.handlers.RotatingFileHandler',
            # 'class':'logging.handlers.TimedRotatingFileHandler',
            'filename': main_log_file,
            'maxBytes': 1024*1024*5, # 5 MB
            # 'when': 'midnight',
            'backupCount': 10,
            'formatter':'verbose',
        },  
        'request_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': req_log_file,
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 10,
            'formatter':'standard',
        },
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',  
            'formatter': 'standard'
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        },
        # catch request status 200
        'django.server': {
            'handlers': ['request_handler', "console"],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}

# import mimetypes
# mimetypes.add_type("text/css", ".css", True)
# mimetypes.add_type("text/javascript", ".js", True)