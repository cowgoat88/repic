"""
Django settings for repicsite project.

Generated by 'django-admin startproject' using Django 2.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import platform


if platform.platform().startswith('Linux'):
    ENVIRONMENT = 'prod'
else:
    ENVIRONMENT = 'dev'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = ['192.168.1.118', '192.168.1.110', '192.168.1.108']



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'storages',
    'repicimages',
    'zappa_django_utils',
    'scrap',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'repicsite.urls'

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

WSGI_APPLICATION = 'repicsite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

if ENVIRONMENT == 'prod':
    DATABASES = {
        'default': {
            'ENGINE': 'zappa_django_utils.db.backends.s3sqlite',
            'NAME': 'sqlite.db',
            'BUCKET': 'repic-db'    
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'zappa_django_utils.db.backends.s3sqlite',
            'NAME': 'sqlite.db',
            'BUCKET': 'repic-db'
        }
    }

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/


ROOT_PATH = os.path.dirname(__file__)
STATIC_ROOT = os.path.join(ROOT_PATH, 'static')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'repicimages/static/css'),
)
# Local Static

STATIC_URL = '/static/'



'''
# AWS STATIC STORAGE!
AWS_S3_HOST = 's3-us-west-1.amazonaws.com'
AWS_STORAGE_BUCKET_NAME = 'repicbot'

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME


STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN

STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
'''
