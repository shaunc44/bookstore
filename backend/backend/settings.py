"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 1.11.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from . settings_secret import Secret as sec
from os.path import abspath, basename, dirname, join, normpath


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DJANGO_ROOT = dirname(dirname(abspath(__file__)))
SITE_ROOT = dirname(DJANGO_ROOT)
SITE_NAME = basename(DJANGO_ROOT)


# MEDIA_ROOT = os.path.join(CURRENT_PATH, 'media').replace('\\','/')
MEDIA_ROOT = os.path.join(DJANGO_ROOT, 'media/')
MEDIA_URL = '/media/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = sec.secret_key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True # Turn to false when site goes live, or users will see error reports

ALLOWED_HOSTS = [] # when live set to domain name


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pipeline', # used for react
    'rest_framework',
    'api',
    'cart',
    'orders',
]

# THIRD_PARTY_APPS = [
#     'rest_framework',
# ]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [join(SITE_ROOT, 'frontend/templates')], # should this be frontend/templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DJANGO_ROOT, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = normpath(join(SITE_ROOT, 'static'))

STATICFILES_DIRS = [
    normpath(join(DJANGO_ROOT, "frontend/static"))
]

CART_SESSION_ID = 'cart'


# Django Pipeline (and browserify)
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)

# browserify-specific
PIPELINE_COMPILERS = (
    'pipeline.compilers.es6.ES6Compiler',
    'pipeline_browserify.compiler.BrowserifyCompiler',
)

PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.NoopCompressor'
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.uglifyjs.UglifyJSCompressor'


if DEBUG:
    PIPELINE_BROWSERIFY_ARGUMENTS = '-t babelify'

PIPELINE = {
    'PIPELINE_ENABLED': True,
    # 'CSS_COMPRESSOR': 'pipeline.compressors.cssmin.CSSMinCompressor',
    # 'CSS_COMPRESSOR': 'pipeline.compressors.NoopCompressor',
    # # 'JS_COMPRESSOR': 'pipeline.compressors.slimit.SlimItCompressor',
    # 'JS_COMPRESSOR': 'pipeline.compressors.uglifyjs.UglifyJSCompressor',
    # 'CSSMIN': 'cssmin',
    'STYLESHEETS': {
        'colors': {
            'source_filenames': (
                # 'css/style.css',
                'css/base.css',
                '*.css'
                # 'bookstore/static/admin/css/*.css',
                # 'bookstore/static/css/base.css',
                # 'bookstore/static/rest_framework/css/*.css',
            ),
            'output_filename': 'css/colors.css'
        }
    },
    'JAVASCRIPT': {
        'stats': {
            'source_filenames': (
                'js/bower_components/jquery/dist/jquery.min.js',
                'js/bower_components/react/JSXTransformer.js',
                'js/bower_components/react/react-with-addons.js',
                'js/app.browserify.js',
                'js/**/*.js'
            ),
            'output_filename': 'js/stats.js'
        }
    }
}


# Redirect to home URL after login (Default redirects to /accounts/profile/)
LOGIN_REDIRECT_URL = '/'

# PIPELINE['CSS_COMPRESSOR'] = 'pipeline.compressors.yuglify.YuglifyCompressor'
# PIPELINE['CSS_COMPRESSOR'] = 'pipeline.compressors.cssmin.CSSMinCompressor'
# PIPELINE['JS_COMPRESSOR'] = 'pipeline.compressors.yuglify.YuglifyCompressor'
# PIPELINE['JS_COMPRESSOR'] = 'pipeline.compressors.slimit.SlimItCompressor'




