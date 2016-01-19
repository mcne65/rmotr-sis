import os
from os.path import dirname

PROJECT_ROOT = dirname(dirname(dirname(dirname(os.path.realpath(__file__)))))
BASE_DIR = os.path.join(PROJECT_ROOT, 'rmotr_sis')

ADMINS = (
    ('Martin Zugnoni', 'martin@rmotr.com'),
    ('Santiago Basulto', 'santiago@rmotr.com'),
)

SECRET_KEY = '^gtiou3uf0!)(zu6e-96ydcvzzws)eilo832qoam(snd%9ak_)'

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Thirt part apps
    'taggit',
    'dbbackup',
    'crispy_forms',

    # Own apps
    'rmotr_sis',
    'accounts',
    'students',
    'courses',
    'assignments',
    'applications',
    'tracks'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Own middlewares
    'accounts.middlewares.LastActivityMiddleware',
)

ROOT_URLCONF = 'rmotr_sis.urls'

WSGI_APPLICATION = 'rmotr_sis.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'rmotr_sis',
        'USER': 'rmotr',
        'PASSWORD': 'rmotr',
        'HOST': 'localhost'
    }
}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, "static"),
)

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'APP_DIRS': True,
    'DIRS': [
        os.path.join(BASE_DIR, 'templates')
    ],
    'OPTIONS': {
        'context_processors': [
            'django.contrib.auth.context_processors.auth',
            'django.template.context_processors.debug',
            'django.template.context_processors.i18n',
            'django.template.context_processors.media',
            'django.template.context_processors.static',
            'django.template.context_processors.tz',
            'django.contrib.messages.context_processors.messages',
            'django.contrib.messages.context_processors.messages',
            'rmotr_sis.context_processors.mixpanel_settings',
            'rmotr_sis.context_processors.site_context_processor'
        ]
    }
}]

# Auth
LOGIN_REDIRECT_URL = '/'
AUTH_USER_MODEL = 'accounts.User'

CRISPY_TEMPLATE_PACK = 'bootstrap3'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_TEMPLATE_LOCATION = os.path.join(TEMPLATES[0]['DIRS'][0], 'emails')

SCHOLARSHIP_ASSIGNMENTS = {
    'assignment_1': 'https://gist.github.com/martinzugnoni/9d7d68ea37c165278493',  # find-next-prime
    'assignment_2': 'https://gist.github.com/martinzugnoni/2b60deae6fa639543c50',  # max-adjacent-product
    'assignment_3': 'https://gist.github.com/martinzugnoni/dc6952632af3ce5a2ef1',  # find-anagrams
}

COURSE_PRICE = 30000  # 300.00 USD

MIXPANEL_TRACKING_ENABLED = True
