"""
Django settings for mobile_notifications project.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e+j^+aem273h=i-l4k(+r-+cw3)c!!3pv$nsz%p7@ifclv)!56'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mobile_notifications_app',
    'push_notifications',
    'rest_framework_swagger',
    'djcelery',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'mobile_notifications.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mobile_notifications.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mobile_notifications_dev',
        'USER': 'audetemidevuser',
        'PASSWORD': 'dbpassaudetemi',
        'HOST': 'audetemidev.cse7c3solg0d.us-west-2.rds.amazonaws.com',
        'PORT': '3306',
    }
}

PUSH_NOTIFICATIONS_SETTINGS = {
    "GCM_API_KEY": "AIzaSyAij2ryWnS9kwVAbn76nDMyJWyB3CZy4Ko",
    #"GCM_API_KEY": "AIzaSyBasJXS_YeSZhSFhiprScRvjNsWXxYq920",
    "APNS_CERTIFICATE": BASE_DIR + "/mobile_notifications_app/SnapHelpFinalPwd.pem",
    "APNS_CA_CERTIFICATES": BASE_DIR + "/mobile_notifications_app/aps_development.cer",
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static/'),
    )
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = '/static'


# CELERY_BROKER_URL = 'amqp://guest:guest@localhost//'

# #: Only add pickle to this list if your broker is secured
# #: from unwanted access (see userguide/security.html)

BROKER_URL = 'amqp://'

CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


#########################################################################################
## System Cron Jobs
#########################################################################################

from celery.schedules import crontab

# The default Django db scheduler
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"

CELERY_TIMEZONE = 'UTC'

CELERYBEAT_SCHEDULE = {
    
    "remove_system_generated_notifications": {
        "task": "mobile_notifications_app.tasks.remove_system_generated_notifications",
        "schedule": crontab(minute=30, hour=1),
        "args": (),
    },

    "remove_user_generated_notifications": {
        "task": "mobile_notifications_app.tasks.remove_user_generated_notifications",
        "schedule": crontab(minute=45, hour=1),
        "args": (),
    }
}

#########################################################################################
## System Cron Jobs Ends
#########################################################################################
