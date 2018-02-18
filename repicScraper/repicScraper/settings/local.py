from .base import *

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'repic',
        'USER': 'root',
        'PASSWORD': 'grooving',
        'HOST': 'localhost',
        'PORT': '3306'
    }
}