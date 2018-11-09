# Python imports
from os.path import join
from decouple import config
# project imports
from .common import *

# uncomment the following line to include i18n
# from .i18n import *


# ##### DEBUG CONFIGURATION ###############################
DEBUG = True

# allow all hosts during development
ALLOWED_HOSTS = ['*']

# ##### AFTER_LOGIN/LOGOUT CONFIGURATION #########################
LOGIN_URL = config('LOGIN_URL')
LOGIN_REDIRECT_URL = config('LOGIN_REDIRECT_URL')
LOGOUT_REDIRECT_URL = config('LOGOUT_REDIRECT_URL')


# ##### DATABASE CONFIGURATION ############################
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DEV_DB'),
        'USER': config('DEV_USER'),
        'HOST': config("DEV_HOST"),
        'PASSWORD': config("DEV_USER_PASSWORD"),
        'PORT': config("DEV_PORT"),

    },
    'slave1': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DEV_DB'),
        'USER': config('DEV_USER'),
        'HOST': config("DEV_HOST"),
        'PASSWORD': config("DEV_USER_PASSWORD"),
        'PORT': config("DEV_PORT"),
    }
}
# DATABASE_ROUTERS = ['rpcserver.routers.ReplRouter',state_routers.MasterSlaveReplica,transaction_routers.logrouter]
REPLICATED_DATABASE_DOWNTIME = 20

# ##### APPLICATION CONFIGURATION #########################

INSTALLED_APPS = DEFAULT_APPS + CUSTOM_APPS + THIRD_PARTY_APPS
TAGGIT_CASE_INSENSITIVE = False
CORS_ORIGIN_ALLOW_ALL = True
