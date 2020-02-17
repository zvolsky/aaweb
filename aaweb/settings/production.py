#mz --
'''
from .base import *
DEBUG = False
try:
    from .local import *
except ImportError:
    pass
'''

#mz ++ everything to the end

from .base import *

# TODO: fix ALLOWED_HOSTS
# jakým mechanismem běží mojeknihovna.eu - není v sites-enabled

config = RawConfigParser()
config['DEFAULT'] = {'ALLOWED_HOSTS': '*'}   # toto asi nechodí
config.read('/etc/django/aaweb/env.ini')


DEBUG = False
SECRET_KEY = os.environ.get('MZ_SECRET_KEY') or config.get('main', 'SECRET_KEY')
# v ALLOWED_HOSTS musí být i www.<domena>, tj. např. <domena>,www.<domena>,*.<domena>
#ALLOWED_HOSTS = (os.environ.get('MZ_ALLOWED_HOSTS') or config.get('main', 'ALLOWED_HOSTS')
#                 ).replace(',', ' ').replace(';', ' ').split()

ALLOWED_HOSTS = ['*']  # works together with SuspiciousTenantMiddleware

# sendgrid: https://simpleisbetterthancomplex.com/tutorial/2016/06/13/how-to-send-email.html
# sendinblue
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-relay.sendinblue.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'zvolsky@seznam.cz'
EMAIL_HOST_PASSWORD = config.get('sendinblue', 'SMTP-PWD')
EMAIL_USE_TLS = True

X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 300
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_REFERRER_POLICY = 'same-origin'

try:
    from .local import *
except ImportError:
    pass
