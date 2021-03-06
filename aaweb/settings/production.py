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
DEBUG_TOOLBAR = False

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
ADMINS = (('Mirek', 'zvolsky@seznam.cz'), ('admin', 'aaweb.eu@gmail.com'))

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

# https://stackoverflow.com/questions/21943962/how-to-see-details-of-django-errors-with-gunicorn
LOGGING = {
'version': 1,
'disable_existing_loggers': False,
'filters': {
    'require_debug_false': {
        '()': 'django.utils.log.RequireDebugFalse',
    },
    'require_debug_true': {
        '()': 'django.utils.log.RequireDebugTrue',
    },
},
'formatters': {
    'django.server': {
        '()': 'django.utils.log.ServerFormatter',
        'format': '[%(server_time)s] %(message)s',
    }
},
'handlers': {
    'console': {
        'level': 'INFO',
        'filters': ['require_debug_true'],
        'class': 'logging.StreamHandler',
    },
    # Custom handler which we will use with logger 'django'.
    # We want errors/warnings to be logged when DEBUG=False
    'console_on_not_debug': {
        'level': 'WARNING',
        'filters': ['require_debug_false'],
        'class': 'logging.StreamHandler',
    },
    'django.server': {
        'level': 'INFO',
        'class': 'logging.StreamHandler',
        'formatter': 'django.server',
    },
    'mail_admins': {
        'level': 'ERROR',
        'filters': ['require_debug_false'],
        'class': 'django.utils.log.AdminEmailHandler'
    },
    'gunicorn': {
        'level': 'DEBUG',
        'class': 'logging.handlers.RotatingFileHandler',
        'formatter': 'django.server',
        'filename': '/home/www-data/dj/aaweb/aaweb/log/gunicorn/error.log',
        'maxBytes': 1024 * 1024 * 32,  # 32 mb
    }
},
'loggers': {
    'django': {
        'handlers': ['console', 'mail_admins', 'console_on_not_debug', 'gunicorn'],  # , 'gunicorn' (fails)
        'level': 'INFO',
    },
    'django.server': {
        'handlers': ['django.server'],
        'level': 'INFO',
        'propagate': False,
    },
}
}

'''
# https://stackoverflow.com/questions/21943962/how-to-see-details-of-django-errors-with-gunicorn - jinak?
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(module)s %(process)d %(thread)d %(message)s'
        }
    },
    'handlers': {
        'gunicorn': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': '/home/www-data/dj/aaweb/aaweb/log/gunicorn/error.log',
            'maxBytes': 1024 * 1024 * 32,  # 32 mb
        }
    },
    'loggers': {
        'gunicorn.errors': {
            'level': 'DEBUG',
            'handlers': ['gunicorn'],
            'propagate': True,
        },
    }
}
'''
