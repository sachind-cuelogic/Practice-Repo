"""
Django settings for prepairit project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import django.conf.global_settings as DEFAULT_SETTINGS

import os
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5v38lo%)(zwm7^3b5%hds!mn#a*jm=h!r&*_%5*q0qj&uhxawd'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tinymce',

    'core',
    'ppiauth',
    'account',
    'knowledgebase',
    'assessment',
    'captcha',
    'taggit',
)

AUTH_USER_MODEL = 'ppiauth.PPIUser'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'ppiauth.middleware.PPIAuthLoginMiddleware'
)

ROOT_URLCONF = 'prepairit.urls'

WSGI_APPLICATION = 'prepairit.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'prepairit',
        'USER': 'prepairit',
        'PASSWORD': '0EC3448B9DD7812FABB4329000A12F300A0E30BFB34C637B654AE519672D2BB0',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Calcutta'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Templates
TEMPLATE_DIRS = [
    os.path.join(BASE_DIR, 'templates')
]

TEMPLATE_CONTEXT_PROCESSORS = (
    'ppiauth.context_processors.login_form',
    'django.core.context_processors.request',
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Media (upload) files
MEDIA_ROOT = '/var/tmp/media/'
MEDIA_URL = '/media/'

# Email
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'shruti.hiremath@cuelogic.co.in'
EMAIL_HOST_PASSWORD = 'shruti0409'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'shruti.hiremath@cuelogic.co.in'

RECAPTCHA_PUBLIC_KEY = '6LcrYgATAAAAAGHyVeRJbnP-XIgTzUytlzcNYQ7f'
# Private key for Recaptcha
RECAPTCHA_PRIVATE_KEY = '6LcrYgATAAAAAMAjtRvOG0tlowVVBnHSHZKRj9wt'

# settings mandatory for django-resized 0.3.5
DJANGORESIZED_DEFAULT_SIZE = [1920, 1080]
DJANGORESIZED_DEFAULT_QUALITY = 75
DJANGORESIZED_DEFAULT_KEEP_META = True

TAGGIT_CASE_INSENSITIVE = True
