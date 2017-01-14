"""
Django settings for repo_classifier project.

Generated by 'django-admin startproject' using Django 1.10.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5v6@0v4zs7fz*a3*k@-ke$rv0plv9l4qsicib$cl&n!5+4bu40'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'classification.apps.ClassificationConfig',
    'data_collection.apps.DataCollectionConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'import_export',
    'pipeline',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'repo_classifier.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'repo_classifier.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


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


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'staticfiles')
STATICFILES_STORAGE = 'pipeline.storage.NonPackagingPipelineCachedStorage'

STATICFILES_DIRS = (
    ('d3', os.path.join(BASE_DIR, 'node_modules', 'd3')),
    ('d3-tip', os.path.join(BASE_DIR, 'node_modules', 'd3-tip')),
    ('jquery', os.path.join(BASE_DIR, 'node_modules', 'jquery', 'dist')),
    ('bootstrap', os.path.join(BASE_DIR, 'node_modules', 'bootstrap', 'dist')),
    ('bootstrap-fileinput', os.path.join(BASE_DIR, 'node_modules', 'bootstrap-fileinput')),
    ('data', os.path.join(BASE_DIR, 'data')),
    ('static', os.path.join(BASE_DIR, 'classification', 'static')),
)

PIPELINE = {
    'CSS_COMPRESSOR': None,
    'JS_COMPRESSOR': None,
    'DISABLE_WRAPPER': True,

    'STYLESHEETS': {
        'static': {
            'source_filenames': (
                os.path.join('static', 'style.css'),
            ),
            'output_filename': os.path.join('css', 'style.css'),
        },
        'bootstrap': {
            'source_filenames': (
                os.path.join('bootstrap', 'css', 'bootstrap.css'),
                os.path.join('bootstrap-fileinput', 'css', 'fileinput.css'),
            ),
            'output_filename': os.path.join('css', 'bootstrap.css'),
        },
    },
    'JAVASCRIPT': {
        'static': {
            'source_filenames': (
                os.path.join('static', 'app.js'),
                os.path.join('static', 'vis.js'),
            ),
            'output_filename': os.path.join('js', 'app.js'),
        },
        'd3': {
            'source_filenames': (
                os.path.join('d3', 'd3.js'),
            ),
            'output_filename': os.path.join('js', 'd3.js'),
        },
        'd3-tip': {
            'source_filenames': (
                os.path.join('d3-tip', 'index.js'),
            ),
            'output_filename': os.path.join('js', 'd3-tip.js'),
        },
        'bootstrap': {
            'source_filenames': (
                os.path.join('jquery', 'jquery.js'),
                os.path.join('bootstrap', 'js', 'bootstrap.js'),
                os.path.join('bootstrap-fileinput', 'js', 'fileinput.js'),
            ),
            'output_filename': os.path.join('js', 'bootstrap.js'),
        },
    },
}

STATICFILES_FINDERS = (
    'pipeline.finders.AppDirectoriesFinder',
    'pipeline.finders.FileSystemFinder',
    'pipeline.finders.CachedFileFinder',
    'pipeline.finders.PipelineFinder',
)


# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s  %(levelname)s - %(module)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}
