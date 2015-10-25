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
    'storages',
    'mptt',
    'easy_thumbnails',
    's3direct',
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
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
STATIC_URL = '/static/'

# Parse database configuration from $DATABASE_URL
# import dj_database_url
# DATABASES = {}
# DATABASES['default'] =  dj_database_url.config()

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'upline',
#         'USER': 'root',
#         'PASSWORD': 'LCLvyk45429',
#         'HOST': 'mysql65762-upline.jelasticlw.com.br',
#         'PORT': '3306',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'upline',
#         'USER': 'root',
#         'PASSWORD': '',
#         'HOST': '127.0.0.1',
#         'PORT': '3306',
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'upline',
        'USER': 'upline',
        'PASSWORD': 'batatinhafrita123',
        'HOST': 'upline.c5rmgxifqspm.us-east-1.rds.amazonaws.com',
        'PORT': '5432',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'pt-br'

from django.conf.locale.en import formats as en_formats
from django.conf.locale.pt_BR import formats as pt_formats

en_formats.DATETIME_FORMAT = "d/m/Y H:i:s"
en_formats.DATE_FORMAT = "d/m/Y"
en_formats.DATETIME_INPUT_FORMATS = "d/m/Y H:i:s"
en_formats.SHORT_DATETIME_FORMAT = "d/m/Y H:i:s"
en_formats.DATE_FORMAT = "d/m/Y"            
en_formats.SHORT_DATE_FORMAT = "d/m/Y"
en_formats.DATE_INPUT_FORMATS = "d/m/Y"   

pt_formats.DATETIME_FORMAT = "d/m/Y H:i:s"
pt_formats.DATE_FORMAT = "d/m/Y"
pt_formats.DATETIME_INPUT_FORMATS = "d/m/Y H:i:s"
pt_formats.SHORT_DATETIME_FORMAT = "d/m/Y H:i:s"
pt_formats.DATE_FORMAT = "d/m/Y"            
pt_formats.SHORT_DATE_FORMAT = "d/m/Y"
pt_formats.DATE_INPUT_FORMATS = "d/m/Y"   

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

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

AWS_ACCESS_KEY_ID = 'AKIAJML75IMVN3ZTEVTQ'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'upline-virtual'
AWS_QUERYSTRING_AUTH = False
S3DIRECT_REGION = 'us-east-1'


OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Access to your groups'}
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

# STATIC_URL = '/static/'

PUSH_NOTIFICATIONS_SETTINGS = {
        "GCM_API_KEY": "AIzaSyA3DfmoFEOFhNz1cbtpa3V1Fv9TVy0PQos",
        # "APNS_CERTIFICATE": "/path/to/your/certificate.pem",
}

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

SUIT_CONFIG = {
    'ADMIN_NAME': '<img src="/static/admin/images/logo.png" />',
    'HEADER_DATE_FORMAT': 'd/m/Y',
    'HEADER_TIME_FORMAT': 'H:i',
    'SHOW_REQUIRED_ASTERISK': True,
    'CONFIRM_UNSAVED_CHANGES': True,
    'MENU': (

        {'label': u'Notificações', 'icon':'icon-lock', 'models': (
            {'label': 'Notificações', 'model':'upline.notification', 'icon':None},
            {'label': 'Mensagens de Notificação', 'model':'upline.siteconfiguration', 'icon':None},)},
         {'label': 'Convites', 'icon':'icon-user', 'models': (
            {'label': 'Convites', 'model':'upline.invite', 'icon':None},
            {'label': 'Convidados', 'model':'upline.invited', 'icon':None},)},
        {'label': 'Pessoas', 'icon':'icon-user', 'models': (
            {'label': 'Usuários', 'model':'auth.user', 'icon':None},
            {'label': 'Grupos', 'model':'auth.group', 'icon':None},
            {'label': 'Membros', 'model':'upline.member', 'icon':None},
            {'label': 'Contatos', 'model':'upline.contact', 'icon':None},
            {'label': 'Clientes', 'model':'upline.client', 'icon':None},
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
            {'label': 'Graduações', 'model':'upline.level', 'icon':None},
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

EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'no-reply@uplinevirtual.com'
EMAIL_HOST_PASSWORD = '0f734e622675a9b3112854a520a91015'
EMAIL_USE_TLS = True

APPLICATION_NAME = "Upline Virtual"
APPLICATION_URL = "http://www.google.com.br"


# S3DIRECT CONFIGURATIONS
def create_media_filename(filename):
    import uuid
    ext = filename.split('.')[-1]
    filename = '%s.%s' % (uuid.uuid4().hex, ext)
    return os.path.join('media', filename)

def create_posts_filename(filename):
    import uuid
    ext = filename.split('.')[-1]
    filename = '%s.%s' % (uuid.uuid4().hex, ext)
    return os.path.join('posts', filename)

def create_training_filename(filename):
    import uuid
    ext = filename.split('.')[-1]
    filename = '%s.%s' % (uuid.uuid4().hex, ext)
    return os.path.join('training_steps', filename)


S3DIRECT_DESTINATIONS = {
    'training_steps': (create_training_filename, lambda u: u.is_staff,),
    'posts': (create_posts_filename, lambda u: u.is_staff,),
    'media': (create_media_filename,lambda u: u.is_staff,),

}

