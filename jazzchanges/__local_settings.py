# Local settings for jazzchanges project.
LOCAL_SETTINGS = True
from settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

INTERNAL_IPS = ('127.0.0.1',)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_DIR, 'changes.sqlite'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': ''
    }
}


# Make this unique, and don't share it with anybody.
SECRET_KEY = 'nds_$1_(f1=zw-56pl7z-91&amp;=%^frf)#5l_1gb(bcog_))0@hh'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

if DEBUG:
    # Show emails in the console during developement.
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    INSTALLED_APPS += ('devserver', 'debug_toolbar', 'django_coverage')

    COVERAGE_REPORT_HTML_OUTPUT_DIR = os.path.join(PROJECT_DIR, 'test-reports')