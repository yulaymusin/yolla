import os
from pathlib import Path
from yolla.settings_production import SECRET_KEY, DATABASES, SERVER_EMAIL, DEFAULT_FROM_EMAIL, ADMINS, MANAGERS, \
    EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_USE_TLS, EMAIL_PORT, PROTOCOL, DOMAIN, SITE_NAME

BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = False
ALLOWED_HOSTS = ['*']
if DEBUG is False:
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
else:
    SECRET_KEY = 'django-insecure-6+vppi!!wdwrqsu&hmr9^9#l2tdz=ss0ikvp16y7x*y%xsd!-o'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'yolla.participant',
    'yolla.common',
    'yolla.category',
    'yolla.topic',
    'yolla.opinion',
    'yolla.article',
    'yolla.jumbotron',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django.middleware.locale.LocaleMiddleware',
    'yolla.common.middlewares.TimezoneMiddleware',
    'yolla.common.middlewares.LanguageMiddleware',
]
ROOT_URLCONF = 'yolla.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
            ],
        },
    },
]
WSGI_APPLICATION = 'yolla.wsgi.application'

# Database
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'yolla',
            'USER': 'postgres',
            'PASSWORD': '123',
            'HOST': 'localhost',
            'PORT': '54321',
            'TEST': {
                'NAME': 'testyolla',
            },
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# Internationalization
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]
LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', 'English'),  # English
)
RTL_LANGUAGES_CODES = ('ar',)
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# More settings & Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
FILE_UPLOAD_PERMISSIONS = 0o644
FILE_UPLOAD_HANDLERS = ['django.core.files.uploadhandler.TemporaryFileUploadHandler', ]

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/participants/login'

if DEBUG is False:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'errors_file': {
                'level': 'ERROR',
                'class': 'logging.FileHandler',
                'filename': 'logs/debug.log',
            },
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler'
            },
        },
        'loggers': {
            'django': {
                'handlers': ['errors_file'],
                'level': 'ERROR',
                'propagate': True,
            },
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True,
            },
        },
    }
else:
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = 'email-debug'

    # SQL query logging
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
            }
        },
        'loggers': {
            'django.db.backends': {
                'handlers': ['console'],
                'level': 'DEBUG',
            },
        }
    }

AUTH_USER_MODEL = 'participant.Participant'
