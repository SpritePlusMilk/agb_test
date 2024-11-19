from os import getenv

from project.settings.general import BASE_DIR

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
