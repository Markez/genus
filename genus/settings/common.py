# Python imports
from os.path import abspath, basename, dirname, join, normpath
import sys
from decouple import config

# ##### PATH CONFIGURATION ################################

# fetch Django's project directory
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# fetch the project_root
PROJECT_ROOT = dirname(DJANGO_ROOT)

# the name of the whole site
SITE_NAME = basename(DJANGO_ROOT)

# collect static files here
STATIC_ROOT = join(PROJECT_ROOT, 'run', 'static')

# collect media files here
MEDIA_ROOT = join(PROJECT_ROOT, 'run', 'media')

# look for static assets here
STATICFILES_DIRS = [
    join(PROJECT_ROOT, 'static'),
]

# look for templates here
# This is an internal setting, used in the TEMPLATES directive
PROJECT_TEMPLATES = [
    join(PROJECT_ROOT, 'templates'),
]

# add apps/ to the Python path
sys.path.append(normpath(join(PROJECT_ROOT, 'apps')))

# ##### APPLICATION CONFIGURATION #########################
# these are the apps
DEFAULT_APPS = [
    'jet.dashboard',
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

CUSTOM_APPS = [
    'apps.alpha',
    'apps.common',
    'apps.accounts',
    'apps.api',
]

THIRD_PARTY_APPS = [
    'django_otp',
    'django_otp.plugins.otp_totp',
    'sslserver',
    'django_secrets',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',
    'rangefilter',
    'silk',

]

# Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'silk.middleware.SilkyMiddleware',
]

# template stuff
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': PROJECT_TEMPLATES,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages'
            ],
        },
    },
]

#swagger settings
SWAGGER_SETTINGS = {
   'api_path': '/',
   'is_authenticated': True,
   'is_superuser': True,
   'permission_denied_handler': 'django.contrib.auth.views.login',
   'exclude_namespaces': ["internal_apis"],
   'base_path': '/docs',
}

# Internationalization
USE_I18N = False


# ##### SECURITY CONFIGURATION ############################

# We store the secret key here
# The required SECRET_KEY is fetched at the end of this file
SECRET_FILE = normpath(join(PROJECT_ROOT, 'run', 'SECRET.key'))

# these persons receive error notification
ADMINS = (
    (config('ADMIN_NAME'), config('ADMIN_EMAIL_ADDRESS')),
)
MANAGERS = ADMINS

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

# ##### DJANGO RUNNING CONFIGURATION ######################

# the default WSGI application
WSGI_APPLICATION = '%s.wsgi.application' % SITE_NAME

# the root URL configuration
ROOT_URLCONF = '%s.urls' % SITE_NAME

# the URL for static files
STATIC_URL = '/static/'

# the URL for media files
MEDIA_URL = '/media/'

# ##### DEBUG CONFIGURATION ###############################
DEBUG = False

# ##### EMAIL CONFIGURATION #########################
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_PORT = 587
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True

# ##### ENVIRONMENT CONFIGURATION #########################
ENVIRONMENT_NAME = config('ENVIRONMENT_NAME')
ENVIRONMENT_COLOR = config('ENVIRONMENT_COLOR')

# ##### MESSAGING CONFIGURATION #########################
from django.contrib.messages import constants as message_constants

MESSAGE_LEVEL = message_constants.DEBUG
MESSAGE_LEVEL = 10  # DEBUG

# ##### COOKIE CONFIGURATION #########################
SESSION_COOKIE_AGE = 60 * 60 * 24 * 30

# ##### AFTER_LOGIN/LOGOUT CONFIGURATION #########################
#rest-swagger login details
LOGIN_URL = 'rest_framework:login'
LOGOUT_URL = 'rest_framework:logout'
# LOGIN_REDIRECT_URL = config('LOGIN_REDIRECT_URL')

# ##### COOQUEING_AUTOMATION_DETAILS_WITH_CELERY CONFIGURATION #########################
BROKER_URL = config('BROKER_URL')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND')
CELERY_ACCEPT_CONTENT = [config('CELERY_ACCEPT_CONTENT')]
CELERY_TASK_SERIALIZER = config('CELERY_SERIALIZER')
CELERY_RESULT_SERIALIZER = config('CELERY_SERIALIZER')
CELERY_TIMEZONE = config('CELERY_TIMEZONE')

# ##### PROFILER CONFIGURATION #########################
SILKY_PYTHON_PROFILER = True
SITE_ID = 1

# ##### LOGGING CONFIGURATION #########################
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },

        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': PROJECT_ROOT + "/logs.log",
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'alpha': {
            'handlers': ['console', 'logfile'],
            'level': 'INFO',
            'propagate': True,
        },
        'common': {
            'handlers': ['console', 'logfile'],
            'level': 'INFO',
            'propagate': True,
        },
        'accounts': {
            'handlers': ['console', 'logfile'],
            'level': 'INFO',
            'propagate': True,
        },
        'common_backend': {
            'handlers': ['console', 'logfile'],
            'level': 'INFO',
            'propagate': True,
        },
        'accounts_backend': {
            'handlers': ['console', 'logfile'],
            'level': 'INFO',
            'propagate': True,
        },
        'sms_sender': {
            'handlers': ['console', 'logfile'],
            'level': 'INFO',
            'propagate': True,
        },
        'apis_view': {
              'handlers': ['console', 'logfile'],
              'level': 'INFO',
              'propagate': True,
          },
    }
}

# finally grab the SECRET KEY
try:
    SECRET_KEY = open(SECRET_FILE).read().strip()
except IOError:
    try:
        from django.utils.crypto import get_random_string
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!$%&()=+-_'
        SECRET_KEY = get_random_string(50, chars)
        with open(SECRET_FILE, 'w') as f:
            f.write(SECRET_KEY)
    except IOError:
        raise Exception('Could not open %s for writing!' % SECRET_FILE)
