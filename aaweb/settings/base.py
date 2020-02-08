# mz changes: search for: #mz, see also production.py

"""
Django settings for aaweb project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from configparser import RawConfigParser   #mz ++

#mz ++
config = RawConfigParser()
config['DEFAULT'] = {'SQLITE': ''}   # '' (~False) --or-- True
config.read('/etc/django/aaweb/env.ini')

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # probably same with/without abspath
BASE_DIR = os.path.dirname(PROJECT_DIR)

#mz ++
# PROJECT_ROOT = PROJECT_DIR   # (this is shopon project style)
DEV_TMP_DIR = os.path.join(BASE_DIR, '.devtmp')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    'home',
    'search',

    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',

    'modelcluster',
    'taggit',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_extensions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',   #mz ++ moved from bellow
    'whitenoise.middleware.WhiteNoiseMiddleware',      #mz ++
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #mz -- 'django.middleware.security.SecurityMiddleware',

    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

ROOT_URLCONF = 'aaweb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'aaweb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

#mz ++
dbname = __package__.rsplit('.')[-2]
# postgres: missing or SQLITE=   ; sqlite: SQLITE=True, Yes, atp.
if os.environ.get('MZ_SQLITE') or bool(config.get('main', 'SQLITE')):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, '%s.sqlite3' % dbname),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'ATOMIC_REQUESTS': True,
            'CONN_MAX_AGE': 1800,
            'HOST': 'localhost',  # ne '', kvůli např. reset_db
            'PORT': 5432,
            'NAME': dbname,
            'USER': dbname,
            'PASSWORD': os.environ.get('MZ_DB_PASSWORD') or config.get('main', 'DB_PASSWORD'),
        }
    }

#mz --
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
'''

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

#mz changed
TIME_ZONE = 'Europe/Prague'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]


#mz -- replaced bellow
# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# Javascript / CSS assets being served from cache (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/3.0/ref/contrib/staticfiles/#manifeststaticfilesstorage
#STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
#STATIC_URL = '/static/'
#MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
#MEDIA_URL = '/media/'

#mz ++
# Media and static settings, development
# https://docs.djangoproject.com/en/3.0/howto/static-files/ (+ shopon project ideas)
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_ROOT = os.path.join(DEV_TMP_DIR, 'static')
STATIC_URL = '/static/'
# (shopon style, project level static/)
#STATICFILES_DIRS = [
#    os.path.join(PROJECT_DIR, 'static'),
#]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_ROOT = os.path.join(DEV_TMP_DIR, 'static', 'root')
MEDIA_URL = '/media/'
#MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_ROOT = os.path.join(DEV_TMP_DIR, 'media')
DEFAULT_FILE_STORAGE = 'django_b2.storage.B2Storage'    # github.com/pyutil/django-b2 (using b2sdk, by zvolsky)
B2_APP_KEY_ID = os.environ.get('B2_APP_KEY_ID') or config.get('b2', 'B2_APP_KEY_ID')
B2_APP_KEY = os.environ.get('B2_APP_KEY') or config.get('b2', 'B2_APP_KEY')
B2_BUCKET_NAME = os.environ.get('B2_BUCKET_NAME') or config.get('b2', 'B2_BUCKET_NAME')
B2_LOCAL_CACHE = 'FM'   # requires MEDIA_ROOT

#mz ++
# colorlog + https://gist.github.com/raphaelyancey/bf8b53a2dbf675f9c99cf39f9e52c224
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
    },
    'formatters': {
        'colored': {
            '()': 'colorlog.ColoredFormatter',  # colored output

            # --> %(log_color)s is very important, that's what colors the line
            'format': '%(log_color)s[%(levelname)s] %(asctime)s :: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'colorlog.StreamHandler',
            'formatter': 'colored',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/opentrafficweb/django.log',   # changed !!!!!!!!
            'formatter': 'colored',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

# Wagtail settings

WAGTAIL_SITE_NAME = "aaweb"

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'http://example.com'
