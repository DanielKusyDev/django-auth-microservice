# Change all credentials!

DEBUG = True
SECRET_KEY = 'secret'
ALLOWED_HOSTS = ['*']

# Databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'root',
        'PASSWORD': 'pass',
        'HOST': 'postgres',
        'PORT': '5432',
    }
}

# Celery
CELERY_BROKER_URL = 'amqp://guest:guest@rabbit:5672/'

BASE_URL = "http://127.0.0.1:8000"
INTERNAL_IPS = [
    '127.0.0.1',
]
