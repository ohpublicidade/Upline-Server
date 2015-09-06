 # -*- coding: utf-8 -*-
"""
Django settings for upline_server project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'm*^q4c8y9ir@82vr!d#k)b7fkl3@^b_&h&*f@failins&d4bb4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'upline',
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "push_notifications",
    'oauth2_provider',
    'corsheaders',
    'rest_framework',
    # 'storages',
    'mptt',
    'django_mptt_admin',
    'django_extensions',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware'
)

ROOT_URLCONF = 'upline_server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'../upline/tempaltes/')],
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

WSGI_APPLICATION = 'upline_server.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Static asset configuration
# STATIC_ROOT = 'staticfiles'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

# Parse database configuration from $DATABASE_URL
# import dj_database_url
# DATABASES = {}
# DATABASES['default'] =  dj_database_url.config()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'upline',
        'USER': 'root',
        'PASSWORD': '5aLnE7sYgE',
        'HOST': 'mysql65741-upline.jelasticlw.com.br',
        'PORT': '3306',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'upline',
#         'USER': 'upline',
#         'PASSWORD': 'batatinhafrita123',
#         'HOST': 'upline.c5rmgxifqspm.us-east-1.rds.amazonaws.com',
#         'PORT': '5432',
#     }
# }

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

# DEFAULT_FILE_STORAGE = 'libs.storages.S3Storage.S3Storage'

OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Access to your groups'}
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

# STATIC_URL = '/static/'

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

SUIT_CONFIG = {
    'ADMIN_NAME': '<img src="/static/admin/images/logo.png" />',
    'HEADER_DATE_FORMAT': 'd/m/Y', # Saturday, 16th March 2013
    'HEADER_TIME_FORMAT': 'H:i',
    'SHOW_REQUIRED_ASTERISK': True,
    'CONFIRM_UNSAVED_CHANGES': True,
    'MENU': (
        {'label': 'Pessoas', 'icon':'icon-user', 'models': (
            {'label': 'Usuários', 'model':'auth.user', 'icon':None},
            {'label': 'Grupos', 'model':'auth.group', 'icon':None},
            {'label': 'Membros', 'model':'upline.member', 'icon':None},
            {'label': 'Contatos', 'model':'upline.contact', 'icon':None},
            {'label': 'Aparelhos iOS', 'model':'push_notifications.apnsdevice', 'icon':None},
            {'label': 'Aparelhos Android', 'model':'push_notifications.gcmdevice', 'icon':None},
        )},
        {'label': 'Vendas', 'icon':'icon-shopping-cart', 'models': (
            {'label': 'Produtos', 'model':'upline.product', 'icon':None},
            {'label': 'Vendas', 'model':'upline.sale', 'icon':None},
        )},
        {'label': u'Calendários', 'icon':'icon-calendar', 'models': (
            {'label': 'Calendarios', 'model':'upline.calendar', 'icon':None},
            {'label': 'Eventos', 'model':'upline.event', 'icon':None},
        )},
        {'label': 'Noticias', 'url':'upline.post', 'icon':'icon-pencil'},
        {'label': 'Midias', 'icon':'icon-file', 'models': (
            {'label': 'Tipos de Midia', 'model':'upline.mediatype', 'icon':None},
            {'label': 'Categorias de Midia', 'model':'upline.mediacategory', 'icon':None},
            {'label': 'Midias', 'model':'upline.media', 'icon':None},
        )},
        {'label': 'Treinamentos', 'icon':'icon-tasks', 'models': (
            {'label': 'Niveis', 'model':'upline.level', 'icon':None},
            {'label': 'Treinamentos', 'model':'upline.training', 'icon':None},
            {'label': 'Etapas de Treinamento', 'model':'upline.trainingstep', 'icon':None},
            # {'label': 'Metas', 'model':'upline.media', 'icon':None},
        )},
        {'label': 'Locais', 'icon':'icon-map-marker', 'models': (
            {'label': 'Estados', 'model':'upline.state', 'icon':None},
            {'label': 'Cidades', 'model':'upline.city', 'icon':None},
            {'label': 'CEPs', 'model':'upline.postalcode', 'icon':None},
        )},
        
    )
}

