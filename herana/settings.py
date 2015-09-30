"""
Django settings for the herana project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'true') == 'true'

# SECURITY WARNING: keep the secret key used in production secret!
if DEBUG:
    SECRET_KEY = '-r&cjf5&l80y&(q_fiidd$-u7&o$=gv)s84=2^a2$o^&9aco0o'
else:
    SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# XXX set me
# GOOGLE_ANALYTICS_ID = set this to something

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'grappelli.dashboard',
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pipeline',
    'django_extensions',

    'herana',
    'registration',
    'debug'
)

if DEBUG:
    INSTALLED_APPS += ('debug_toolbar',)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

ANONYMOUS_USER_ID = -1

ROOT_URLCONF = 'herana.urls'

WSGI_APPLICATION = 'herana.wsgi.application'

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(default='postgres://herana:herana@localhost:5432/herana')
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'herana', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                "django.contrib.auth.context_processors.auth",
                "django.core.context_processors.debug",
                "django.core.context_processors.i18n",
                "django.core.context_processors.media",
                "django.core.context_processors.request",
                "django.core.context_processors.static",
                "django.core.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "herana.context_processors.google_analytics",
            ],
        },
    },
]

TEMPLATE_DEBUG = DEBUG

# file uploads
if not DEBUG:
    DEFAULT_FILE_STORAGE = 'herana.botopatch.S3Storage'
    AWS_S3_FILE_OVERWRITE = False
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = "herana-media"
    AWS_S3_HOST = "s3-eu-west-1.amazonaws.com"
    AWS_HEADERS = {
        'Cache-Control': 'max-age=86400',
    }

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

ASSETS_DEBUG = DEBUG
ASSETS_URL_EXPIRE = False

# assets must be placed in the 'static' dir of your Django app

# where the compiled assets go
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# the URL for assets
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "pipeline.finders.PipelineFinder",
)

PYSCSS_LOAD_PATHS = [
    os.path.join(BASE_DIR, 'herana', 'static'),
    os.path.join(BASE_DIR, 'herana', 'static', 'bower_components'),
]

PIPELINE_CSS = {
    'css': {
        'source_filenames': (
            'bower_components/fontawesome/css/font-awesome.css',
            'stylesheets/app.scss',
        ),
        'output_filename': 'app.css',
    },
}
PIPELINE_JS = {
    'js': {
        'source_filenames': (
            'bower_components/jquery/dist/jquery.min.js',
            'javascript/app.js',
        ),
        'output_filename': 'app.js',
    },
}
PIPELINE_CSS_COMPRESSOR = None
PIPELINE_JS_COMPRESSOR = None

PIPELINE_COMPILERS = (
    'herana.pipeline.PyScssCompiler',
)

STATICFILES_STORAGE = 'herana.pipeline.GzipManifestPipelineStorage'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(levelname)s %(module)s %(process)d %(thread)d %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'ERROR'
    },
    'loggers': {
        # put any custom loggers here
        # 'your_package_name': {
        #    'level': 'DEBUG' if DEBUG else 'INFO',
        # },
        'django': {
            'level': 'INFO',
        }
    }
}

# Registration
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_AUTO_LOGIN = True

# Grappelli
GRAPPELLI_INDEX_DASHBOARD = 'herana.dashboard.CustomIndexDashboard'
GRAPPELLI_ADMIN_TITLE = 'Herana University-Community Engagement Assessment Instrument'

# Custom User Model
AUTH_USER_MODEL = 'herana.CustomUser'

SUPPORT_EMAIL = 'francois@compressdsl.com'
DEFAULT_FROM_EMAIL = os.environ.get('DJANGO_DEFAULT_FROM_EMAIL', SUPPORT_EMAIL)
EMAIL_HOST = 'smtp.mandrillapp.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'webapps@code4sa.org'
EMAIL_HOST_PASSWORD = os.environ.get('DJANGO_EMAIL_HOST_PASSWORD')
EMAIL_SUBJECT_PREFIX = '[Herana] '

DOMAIN = "herana.code4sa.org"
