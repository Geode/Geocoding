
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
#BASE_DIR = os.path.dirname(os.path.dirname(__file__))
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'si5%-mzd5t_v-&d2&j*e&$^n!(txw5-^lh83nbsi4bm&0vua3!'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

BOWER_INSTALLED_APPS = (
    'jquery',
    'bootstrap',
    'modernizr',
    'underscore',
    'nvd3',
    'twitter-bootstrap-wizard#1.3.2',
    'typeahead.js',
    'bloodhound',
)

BING_API_KEY = ''
GOOGLE_API_KEY = ''
GOOGLE_CLIENT = ''
GOOGLE_CLIENT_SECRET = ''
