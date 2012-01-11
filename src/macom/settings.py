# -*- coding: utf-8 -*-

from os.path import dirname, abspath, isdir, split, join, isfile

DEBUG = True

TEMPLATE_DEBUG = True

def find_db(path, name):
    db = join(path, name)
    if isfile(db):
        return db
    else:
        parent, _ = split(path)
        if parent == '/':
            raise Exception('Database %s not found' % name)
        else:
            return find_db(parent, name)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': find_db(abspath(dirname(__file__)), 'sqlite.db'),
        'USER': '', # Not used with sqlite3.
        'PASSWORD': '', # Not used with sqlite3.
        'HOST': '', # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '', # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Argentina/Buenos_Aires'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es-AR'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'x@gqjtfz*e0rn17x#3%aw)@6=q-c4$37r7x#jmx1&+ld1#clp0'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
)

TEMPLATE_DIRS = (
    'templates',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'macom.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.markup',
    'macom.diagrama',
    'macom.web',
    'macom.api',
    'macom.app',
    'south',
    'taggit',
)

DIAGRAM_SERVICE_URL = 'http://10.20.109.140:8080/plantuml/proxy'

def find_media(path):
    media = join(path, 'media')
    if isdir(media):
        return media
    else:
        parent, _ = split(path)
        if parent == '/':
            raise 'Media not found'
        else:
            return find_media(parent)

MEDIA_ROOT = find_media(abspath(dirname(__file__)))
