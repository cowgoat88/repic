from .base import *

DATABASES = {
      'default': {
          'ENGINE': 'zappa_django_utils.db.backends.s3sqlite',
          'NAME': 'sqlite.db',
          'BUCKET': 'repic-db'    
      }
}

# AWS STATIC STORAGE!
AWS_S3_HOST = 's3-us-west-1.amazonaws.com'
AWS_STORAGE_BUCKET_NAME = 'repicbot'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN

STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'