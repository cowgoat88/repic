from .base import *

DATABASES = {
      'default': {
          'ENGINE': 'zappa_django_utils.db.backends.s3sqlite',
          'NAME': 'sqlite.db',
          'BUCKET': 'repic-db'    
      }
}

# Local Static
STATIC_URL = '/static/'