from .settings_base import *

DEBUG = True

ALLOWED_HOSTS = [
    'localhost'
]

DATABASES = SQLITE

SENDFILE_BACKEND = 'sendfile.backends.development'
