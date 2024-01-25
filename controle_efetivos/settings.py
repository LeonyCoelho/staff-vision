import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_3n5%s4u$6%xu+%y$usko%g4&01sbmvn%)jf-_pg-7p4hw+$v8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['10.42.68.2', '10.42.68.2:88']

CSRF_TRUSTED_ORIGINS = ['http://10.42.68.2:88']

# ALLOWED_HOSTS = []

SESSION_COOKIE_NAME = 'session_controle_efetivos'



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app_efetivos',
    'django_crontab',
    'channels'
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

ROOT_URLCONF = 'controle_efetivos.urls'

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

WSGI_APPLICATION = 'controle_efetivos.wsgi.application'



# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
     'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':'controle_efetivosdb',
        'USER': 'adm',
        'PASSWORD':'abc@123',
     }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

# Tamanho máximo de upload de arquivos (em bytes)
DATA_UPLOAD_MAX_MEMORY_SIZE = 2621440  # Defina o tamanho desejado

# Tamanho máximo de um arquivo de upload (em bytes)
FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440  # Defina o tamanho desejado

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True

CRONJOBS = [
<<<<<<< HEAD
    ('55 06 * * *', 'app_efetivos.cron.reset', '>> /home/deploy/controle-de-efetivo/logs/reset.log'),
    ('55 18 * * *', 'app_efetivos.cron.reset', '>> /home/deploy/controle-de-efetivo/logs/reset.log')
=======
    ('55 06 * * *', 'app_efetivo.cron.reset'),
    ('55 18 * * *', 'app_efetivo.cron.reset')
>>>>>>> 30f4f925aadc4739c0673881ded798bd92a28b74
]


MEDIA_URL = 'media/'
MEDIAFILES_DIRS = [
    os.path.join(BASE_DIR, 'app_efetivos/media'),
]
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'app_efetivos/static'),
]
STATICFILES = [
    # outros arquivos estáticos
    'bootstrap.min.css',
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
