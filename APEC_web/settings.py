"""
Django settings for example project.

Generated by 'django-admin startproject' using Django 1.10.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
root = environ.Path(__file__) - 2
env = environ.Env()
environ.Env.read_env(root('.env'))
BASE_DIR = root()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#9-u7b%vyd_50j!bl)ii=6thk^&pkf1a!nf70uh&bnclbvbgv-'

# SECURITY WARNING: don't run with debug turned on in production!

###############################
# For deploiment:

#./manage collectstatic
#DEBUG = False
#ALLOWED_HOSTS = ['ec2-18-221-153-167.us-east-2.compute.amazonaws.com', '18.221.153.167', 'www.4qmmm.com', '4qmmm.com']

DEBUG = True
ALLOWED_HOSTS = []
###############################

# Application definition

INSTALLED_APPS = [

    #
    'channels',
    'django_remote_submission',
    'django_celery_results',
    'rest_framework',
    'django_filters',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ESTM.apps.EstmConfig',
    'archive_ESTM.apps.ArchiveEstmConfig',

    #login
    'django.contrib.sites',
    'users.apps.UsersConfig',
    'allauth', # new
    'allauth.account', # new
    'allauth.socialaccount', # new

    'crispy_forms',

]

CRISPY_TEMPLATE_PACK = 'bootstrap3'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'APEC_web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'APEC_web.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': 'db.sqlite3',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'apec_web',
        'USER': 'yoelvis',
        'PASSWORD': 'Camaron8!',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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

SITE_ID = 1

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_UNIQUE_EMAIL = True

LOGIN_REDIRECT_URL = 'home'
ACCOUNT_LOGOUT_REDIRECT_URL = 'home'

AUTH_USER_MODEL = 'users.CustomUser'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",

    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

# Folder where uploaded files go
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# When DEBUG = True and you have included django.core.staticfiles in your INSTALLED_APPS, 
# Django will serve the files located in the STATICFILES_DIRS tuple using the STATIC_URL 
# path as the starting point.
# In production this responsibility should be given to Nginx, Apache, CloudFront, etc. 
# When DEBUG = False, Django will not automatically serve any static files. 
# When you run:
# python manage.py collectstatic

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'staticfiles')] # if your static files folder is named "staticfiles"

# Celery configuration

CELERY_RESULT_BACKEND = 'django-db'
CELERY_BROKER_URL = 'redis://127.0.0.1:6379'

# Channels
ASGI_APPLICATION = "APEC_web.routing.application"

CHANNEL_LAYERS = {
    'default': {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
    },
}

# django_remote_submission parameters
PYTHON_PATH = env('PYTHON_PATH')
PYTHON_ARGUMENTS = env.list('PYTHON_ARGUMENTS')
SERVER_HOSTNAME = env('SERVER_HOSTNAME')
SERVER_PORT = env.int('SERVER_PORT')
REMOTE_DIRECTORY = env('REMOTE_DIRECTORY')
REMOTE_FILENAME = env('REMOTE_FILENAME')
REMOTE_USER = env('REMOTE_USER')
REMOTE_PASSWORD = env('REMOTE_PASSWORD')

#email for grant request
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '465'
EMAIL_HOST_USER = 'ESTMaccess@gmail.com'
EMAIL_HOST_PASSWORD = 'Habana2000!'
EMAIL_USE_TLS = False  # port 587
EMAIL_USE_SSL = True  # port 465

#ACCOUNT_EMAIL_VERIFICATION = "mandatory"
#ACCOUNT_EMAIL_REQUIRED = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.security.DisallowedHost': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': True,
        },
        # Mine:
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django_remote_submission': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'celery': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'server': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}
