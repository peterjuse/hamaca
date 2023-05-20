"""
Archivo de configuracion de la aplicacion web en el entorno de desarrollo
"""

from .base import *

# Este entorno utiliza el DEBUG
DEBUG = True

# Lista de aplicaciones extra para poder realizar un optimo debug
INSTALLED_APPS += [
    'django.contrib.admin',  
    # 'debug_toolbar',
]

# Agregando middleware para debug
MIDDLEWARE += [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# Cache para Django
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'default-locmemcache',
        'TIMEOUT': 5,
    }
}

# Base de datos
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hamaca',
        'USER': 'gateway',
        'PASSWORD': 'iotgateway',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}