from os import getenv
from pathlib import Path

# Основные настройки Django
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-@622-2)6#x-)w#qp@5458=!e50hx4(+1y*xxgfp8)b4q%hl434'

DEBUG = bool(getenv('DEBUG', 1))

ALLOWED_HOSTS = ALLOWED_HOSTS.split(' ') if (ALLOWED_HOSTS := getenv('ALLOWED_HOSTS')) else []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_spectacular',
    'drf_spectacular_sidecar',
    'parser.apps.ParserConfig',
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

ROOT_URLCONF = 'project.urls'

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

WSGI_APPLICATION = 'project.wsgi.application'


# Database

if getenv('DB_ENGINE'):
    DATABASES = {
        'default': {
            'ENGINE': getenv('DB_ENGINE', 'django.db.backends.sqlite3'),
            'NAME': getenv('POSTGRES_DB', BASE_DIR / 'db.sqlite3'),
            'USER': getenv('POSTGRES_USER', 'testuser'),
            'PASSWORD': getenv('POSTGRES_PASSWORD', 'password'),
            'HOST': getenv('POSTGRES_HOST', 'localhost'),
            'PORT': int(getenv('POSTGRES_PORT', '5432')),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        },
    }

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

STATIC_ROOT = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Настройки DRF
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
}

# Настройки drf-spectacular
SPECTACULAR_SETTINGS = {
    'SWAGGER_UI_DIST': 'SIDECAR',
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
    'TITLE': 'Тестовое задание',
    'DESCRIPTION': 'Swagger',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# Настройка брокера для Celery
CELERY_BROKER_URL = 'redis://redis:6379/1'
CELERY_TIMEZONE = TIME_ZONE
