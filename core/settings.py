import datetime
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ENVIRONMENT VARIABLES
DEBUG = os.getenv("DEBUG", False) == "true"
SECRET_KEY = os.getenv("SECRET_KEY")
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
MAILING_URL = os.getenv('MAILING_URL')
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS")

if ALLOWED_HOSTS:
    ALLOWED_HOSTS = ALLOWED_HOSTS.split(",")
if CORS_ALLOWED_ORIGINS:
    CORS_ALLOWED_ORIGINS = CORS_ALLOWED_ORIGINS.split(",")

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
# Databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}
INSTALLED_APPS = [
    # Django stuff
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party packages
    'rest_framework',
    'rules.apps.AutodiscoverRulesConfig',
    'drf_yasg',
    'django_rest_passwordreset',
    'corsheaders',
    'django_filters',

    'apps.users',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
    }
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

WSGI_APPLICATION = 'core.wsgi.application'

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

# Lang & Time zone
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Statics
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')


# DRF
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 50,
    'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'EXCEPTION_HANDLER': 'core.errors.drf_exception_handler'
}

# django-rules
AUTHENTICATION_BACKENDS = (
    'rules.permissions.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# drf-yasg
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'USE_SESSION_AUTH': False
}

# RESET_PASSWORD
DJANGO_REST_PASSWORDRESET_TOKEN_CONFIG = {
    "CLASS": "django_rest_passwordreset.tokens.RandomStringTokenGenerator",
    "OPTIONS": {
        "min_length": 20,
        "max_length": 30
    }
}

# auth
AUTH_USER_MODEL = 'users.User'
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(hours=3),
}

# Micro-services
MAILING_BASE_PATH = '/api/v1'

try:
    from .local_settings import *
except ImportError:
    pass
