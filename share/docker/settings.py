# Django settings for regularcom project.

# import djcelery
# djcelery.setup_loader()

# BROKER_URL = 'amqp://guest:guest@localhost:5672/'
# CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
# CELERY_RESULT_BACKEND = 'database'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

from django.core.exceptions import ImproperlyConfigured

def get_env_variable(var_name, default_value=None):
    return os.environ.get(var_name, default_value)
    # try:
    #     return os.environ[var_name]
    # except KeyError:
    #     if default_value:
    #         return default_value
    #     raise ImproperlyConfigured("Environment variable %s not set" % var_name)

APP_PATH = get_env_variable('APP_PATH', '/app')

# Make this unique, and don't share it with anybody.
SECRET_KEY = get_env_variable('SECRET_KEY', 'secret_key')

#DEBUG = False
DEBUG = get_env_variable('DEBUG', True)
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        # 'NAME': './database.db',                      # Or path to database file if using sqlite3.

        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': get_env_variable('DB_NAME', 'vegeclic'), # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': get_env_variable('DB_USER', 'postgres'),
        'PASSWORD': get_env_variable('DB_PASSWORD', ''),
        'HOST': get_env_variable('DB_HOST', 'postgres'), # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': get_env_variable('DB_PORT', ''), # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['www.vegeclic.fr',]

INTERNAL_IPS = ('127.0.0.1',)

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
#TIME_ZONE = 'America/Chicago'
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'fr'
MODELTRANSLATION_DEFAULT_LANGUAGE = 'fr'

gettext = lambda s: s

LANGUAGES = (
    ('de', gettext('German')),
    ('fr', gettext('French')),
)

MODELTRANSLATION_FALLBACK_LANGUAGES = {
    'default': ('fr', 'de',),
}

LOCALE_PATHS = (
    '%s/conf/locale' % APP_PATH,
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = get_env_variable('MEDIA_ROOT', '%s/static/media' % APP_PATH)

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = get_env_variable('MEDIA_URL', '/static/media/')

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = get_env_variable('STATIC_ROOT', '%s/static_files/' % APP_PATH)

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = get_env_variable('STATIC_URL', '/static/')

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    get_env_variable('STATICFILES_DIR', '%s/static' % APP_PATH),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
    # 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'fandjango.middleware.FacebookMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'mailbox.middleware.MailboxMiddleware',
    'wallets.middleware.WalletMiddleware',
    'carts.middleware.CartMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
)

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#         'LOCATION': 'unique-snowflake'
#     }
# }

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': get_env_variable('CACHE_LOCATION', 'memcached:11211'),
        'TIMEOUT': 3600,
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
        }
    }
}

CACHE_MIDDLEWARE_SECONDS = 3600

ROOT_URLCONF = 'regularcom.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'regularcom.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    get_env_variable('TEMPLATE_DIR', '%s/templates' % APP_PATH),
)

INSTALLED_APPS = (
    # 'djcelery',
    'modeltranslation',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'products',
    'suppliers',
    'common',
    'accounts',
    'blog',
    'customers',
    'carts',
    'mailbox',
    'pro',
    'wallets',
    # 'celerytest',
    'south',
    # 'debug_toolbar',
    #'fandjango',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

AUTH_USER_MODEL = 'accounts.Account'
# LOGIN_REDIRECT_URL = '/customers/'
LOGIN_REDIRECT_URL = '/'

START_YEAR = 2013

AVE_LOGIN = get_env_variable('AVE_LOGIN')
AVE_PASSWD = get_env_variable('AVE_PASSWD')
AVE_SUPPLIER_NAME = 'AVE'
AVE_CHUNK = 300
# AVE_LIMIT_SIZE = AVE_CHUNK*47
AVE_LIMIT_SIZE = None
AVE_LOCAL_RETRIEVE = False

# TEMPLATE_STRING_IF_INVALID = 'INVALID_TEMPLATE_STRING'

EMAIL_HOST = get_env_variable('EMAIL_HOST')
EMAIL_PORT = get_env_variable('EMAIL_PORT')
EMAIL_USE_TLS = True
EMAIL_HOST_USER = get_env_variable('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_env_variable('EMAIL_HOST_PASSWORD')
EMAIL_SUBJECT_PREFIX = '[Végéclic] '

PRICE_MARGIN_RATE = 50
PRICE_PRO_MARGIN_RATE = 33
DEGRESSIVE_PRICE_RATE = 1.5
DELIVERY_DAY_OF_WEEK = 1
VALIDATING_DAY_OF_WEEK = 6
DELAY_BETWEEN_DEFINITON_N_DELIVERY = 9
PACKAGING_WEIGHT_RATE = 10

EMAIL_ADMIN = get_env_variable('EMAIL_ADMIN')
BALANCE_INIT = 0

DEFAULT_CURRENCY = 'Euro'
DEFAULT_WEIGHT = 150

FACEBOOK_APPLICATION_ID = get_env_variable('FACEBOOK_APPLICATION_ID')
FACEBOOK_APPLICATION_SECRET_KEY = get_env_variable('FACEBOOK_APPLICATION_SECRET_KEY')
FACEBOOK_APPLICATION_NAMESPACE = get_env_variable('FACEBOOK_APPLICATION_NAMESPACE')
# FACEBOOK_APPLICATION_CANVAS_URL = 'https://apps.facebook.com/vegeclic'
FACEBOOK_APPLICATION_CANVAS_URL = get_env_variable('FACEBOOK_APPLICATION_CANVAS_URL')
FANDJANGO_SITE_URL = FACEBOOK_APPLICATION_CANVAS_URL
FACEBOOK_ADMIN_ID = get_env_variable('FACEBOOK_ADMIN_ID')
FACEBOOK_PAGE_ID = get_env_variable('FACEBOOK_PAGE_ID')

TWITTER_ACCOUNTS = [
    {'oauth_token': get_env_variable('OAUTH_TOKEN_1'),
     'oauth_secret': get_env_variable('OAUTH_SECRET_1'),
     'consumer_key': get_env_variable('CONSUMER_KEY_1'),
     'consumer_secret': get_env_variable('CONSUMER_SECRET_1')},

    {'oauth_token': get_env_variable('OAUTH_TOKEN_2'),
     'oauth_secret': get_env_variable('OAUTH_SECRET_2'),
     'consumer_key': get_env_variable('CONSUMER_KEY_2'),
     'consumer_secret': get_env_variable('CONSUMER_SECRET_2')},
]
