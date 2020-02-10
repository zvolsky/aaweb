from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd-a4a@=rr7p)^0vb8hq&6wp1+!a6gddcx$b48owolzfgu#1pd&'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# MailHog - remove BASE_URL from settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost' #'0.0.0.0'
EMAIL_PORT = 1025
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False

try:
    from .local import *
except ImportError:
    pass
