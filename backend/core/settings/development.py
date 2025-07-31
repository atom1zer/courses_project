from .base import *

DEBUG = True

CSRF_TRUSTED_ORIGINS = [
    "http://*",
    "https://*",
]

CORS_ALLOW_ALL_ORIGINS = True

INSTALLED_APPS.append("silk")

MIDDLEWARE.append("silk.middleware.SilkyMiddleware")
