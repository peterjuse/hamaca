"""
Archivo de configuracion de la aplicacion web bajo el entorno de produccion
"""
import os

from .base import *
from socket import gethostname, gethostbyname 

# Aesegurando que el entorno de desarrollo no puede usar el DEBUG
DEBUG = False

# Obtencion de la clave secreta de operaciones en el dispositivo
assert os.getenv('DJANGO_SECRET_KEY') is not None, (
    'Por favor provea la variable de entorno '
    'DJANGO_SECRET_KEY con su valor ')

# MIDDLEWARE += [
     # 'allow_cidr.middleware.AllowCIDRMiddleware',
#     'django.contrib.admin',  
# ]

# ALLOWED_HOSTS += [
#     gethostname(),
#     gethostbyname(gethostname()),
#     'localhost',
# ]

# Hosts que son permitidos por el ambiente de produccion
ALLOWED_HOSTS_CIDR_NETS = [
    '192.168.1.0/24',
    '192.168.0.0/24',
]

# Configuracion de la base de datos
DATABASES['default'].update({
    'NAME': os.getenv('DJANGO_DB_NAME'),
    'USER': os.getenv('DJANGO_DB_USER'),
    'PASSWORD': os.getenv('DJANGO_DB_PASSWORD'),
    'HOST': os.getenv('DJANGO_DB_HOST'),
    'PORT': os.getenv('DJANGO_DB_PORT'),
})

# Cache utilizadas en produccion
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#         'LOCATION': 'default-locmemcache',
#         'TIMEOUT': int(os.getenv('DJANGO_CACHE_TIMEOUT'), ),
#     }
# }

# Para poder utilizar AWS  
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY_ID')
# AWS_STORAGE_BUCKET_NAME = os.getenv('DJANGO_UPLOAD_S3_BUCKET')