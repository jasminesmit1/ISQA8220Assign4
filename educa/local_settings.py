import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DEBUG = True

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'jrsmith072@gmail.com'
EMAIL_HOST_PASSWORD = 'Mookie09'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
