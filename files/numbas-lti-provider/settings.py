import os
import environ

env = environ.Env(
    DEBUG=(bool, False),
    LOGLEVEL=(str,'WARNING'),
    LANGUAGE_CODE=(str,'en'),
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

SESSION_COOKIE_NAME = 'numbas_lti_provider'

ALLOWED_HOSTS = [env('SERVERNAME'), '127.0.0.1', 'localhost']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'statici18n',
    'huey.contrib.djhuey',
    'numbas_lti',
    'bootstrapform',
    'bootstrap_datepicker_plus',
]

MIDDLEWARE = [
    'django_cookies_samesite.middleware.CookiesSameSite',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django_auth_lti.middleware_patched.MultiLTILaunchAuthMiddleware',
    'numbas_lti.middleware.NumbasLTIResourceMiddleware',
]

AUTHENTICATION_BACKENDS = ['numbas_lti.backends.LTIAuthBackend','django.contrib.auth.backends.ModelBackend']

LTI_INSTRUCTOR_ROLES = ['Instructor','Administrator','ContentDeveloper','Manager','TeachingAssistant']

ROOT_URLCONF = 'numbasltiprovider.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': env('LOGLEVEL').upper(),
    },
}

if DEBUG:
    # make all loggers use the console.
    for logger in LOGGING['loggers']:
        LOGGING['loggers'][logger]['handlers'] = ['console']

WSGI_APPLICATION = 'numbasltiprovider.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'numbas_lti',
        'USER': 'numbas_lti',
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': 'postgres',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = env('LANGUAGE_CODE')
LOCALE_PATHS = (os.path.join(BASE_DIR,'locale'),)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

MEDIA_ROOT = '/srv/numbas-lti-media/'
MEDIA_URL = '/media/'

STATIC_URL = '/static/'
STATIC_ROOT = '/srv/numbas-lti-static/'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Channels

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.environ.get('REDIS_URL','redis://redis:6379')],
        },
        "ROUTING": "numbasltiprovider.routing.channel_routing",
    },
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SUPPORT_NAME = 'the Numbas team' # the name of your support contact
SUPPORT_URL = None  # set to "mailto:your_email_address", or the URL of a page containing contact info

SESSION_COOKIE_SAMESITE = None  # Allow cookies to be set through cross-origin POST requests, such as when a resource is embedded in an iframe
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = None  
CSRF_COOKIE_SECURE = True
DCS_SESSION_COOKIE_SAMESITE = 'None'  # Allow cookies to be set through cross-origin POST requests, such as when a resource is embedded in an iframe
DCS_CSRF_COOKIE_SAMESITE = 'None'

EMAIL_COMPLETION_RECEIPTS = True
DEFAULT_FROM_EMAIL = 'numbas@{}'.format(env('SERVERNAME'))

REQUEST_TIMEOUT = 60    # Number of seconds to wait for requests to timeout, such as outcome reports or fetching SCORM packages

HUEY = {
    'connection': {
        'host': 'redis',
        'port': 6379,
    },
}

