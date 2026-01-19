from .base import *
from decouple import config
from pathlib import Path

# Ensure BASE_DIR is available (should be imported from base.py)
try:
    _ = BASE_DIR
except NameError:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Database configuration - Set DATABASES unconditionally
# Default to SQLite for development
DATABASE_ENGINE = config('DATABASE_ENGINE', default='sqlite3')

# Always set DATABASES - no conditionals that might fail
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR / 'db.sqlite3'),
    }
}

# Override with PostgreSQL if specified
if DATABASE_ENGINE == 'postgresql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME', default='lms_db'),
            'USER': config('DB_USER', default='postgres'),
            'PASSWORD': config('DB_PASSWORD', default=''),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432'),
        }
    }

# Ensure DEBUG is True for development
DEBUG = config('DEBUG', default=True, cast=bool)

# Ensure ALLOWED_HOSTS is set
ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='localhost,127.0.0.1',
    cast=lambda v: [s.strip() for s in v.split(',') if s.strip()]
)

# CORS settings for development
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:3000,http://127.0.0.1:3000',
    cast=lambda v: [s.strip() for s in v.split(',') if s.strip()]
)

CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=False, cast=bool)
