import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent.parent


# SECRET_KEY = os.getenv("SECRET_KEY")
SECRET_KEY = os.environ.get(
    "SECRET_KEY", "django-insecure-6hdy-)5o6k6it_6x%s#u0#guc3(au!=v%%qb674(upu6rrht7b"
)

DEBUG = os.environ.get("DEBUG", True)

# ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(",")
ALLOWED_HOSTS = ["127.0.0.1", "0.0.0.0"]

if os.environ.get("ALLOWED_HOSTS") is not None:
    try:
        ALLOWED_HOSTS += os.environ.get("ALLOWED_HOSTS").split(",")
    except Exception as e:
        print("Cant set ALLOWED_HOSTS, using default instead")

AUTH_USER_MODEL = "users.User"


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # local
    "apps.users",
    "apps.courses",
    # 3rd party
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "drf_standardized_response",
    "drf_standardized_errors",
    'drf_spectacular',
    'storages',
]


MIDDLEWARE = [
    # cors
    "corsheaders.middleware.CorsMiddleware",
    # local
    # "apps.api_keys.middleware.APIKeyMiddleware",
    # "apps.users.middleware.ClientDataMiddleware",
    # django
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "core.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database

# DATABASES = {
#     "default": {
#         #"ENGINE": "django.db.backends.sqlite3",
# 	#"NAME": BASE_DIR / "db.sqlite3",
#         "ENGINE": f"django.db.backends.{os.getenv('SQL_ENGINE', 'sqlite3')}",
#         "NAME": os.getenv("SQL_DATABASE", BASE_DIR / "db.sqlite3"),
#         "USER": os.getenv("SQL_USER"),
#         "PASSWORD": os.getenv("SQL_PASSWORD"),
#         "HOST": os.getenv("SQL_HOST"),
#         "PORT": os.getenv("SQL_PORT"),
#     }
# }

DATABASES = {
    "default": {
        #"ENGINE": "django.db.backends.sqlite3",
	#"NAME": BASE_DIR / "db.sqlite3",
        "ENGINE": f"django.db.backends.{os.environ.get('SQL_ENGINE', 'sqlite3')}",
        "NAME": os.environ.get("SQL_DATABASE", BASE_DIR / "db.sqlite3"),
        "USER": os.environ.get("SQL_USER"),
        "PASSWORD": os.environ.get("SQL_PASSWORD"),
        "HOST": os.environ.get("SQL_HOST"),
        "PORT": os.environ.get("SQL_PORT"),
    }
}


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Locale

LANGUAGES = [
    ("en", "English"),
    ("ru", "Russian"),
]

LOCALE_PATHS = [
    BASE_DIR / "locale",
]

LANGUAGE_CODE = "en"


# Internationalization

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = "static/"

STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "media/"

MEDIA_ROOT = BASE_DIR / "media"


# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Geo

GEOIP_PATH = "static"


# Email

# EMAIL_BACKEND = os.getenv(
#     "EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
# )
EMAIL_BACKEND = (
    f"django.core.mail.backends.{os.environ.get('EMAIL_BACKEND', 'smtp')}.EmailBackend"
)

EMAIL_HOST = os.environ.get("EMAIL_HOST","smtp.yandex.ru")

EMAIL_PORT = os.environ.get("EMAIL_PORT",587)

EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER","yahweh@yhwh-design.ru")

EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

EMAIL_SERVER = EMAIL_HOST_USER

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

EMAIL_ADMIN = EMAIL_HOST_USER


# Celery

CELERY_BROKER_URL = os.environ.get("BROKER_URL", "redis://redis:6379/0")

CELERY_RESULT_BACKEND = os.environ.get("RESULT_BACKEND", "redis://redis:6379/0")

CELERY_ACCEPT_CONTENT = ["json"]

CELERY_TASK_SERIALIZER = "json"

CELERY_RESULT_SERIALIZER = "json"

CELERY_TIMEZONE = "UTC"

REDIS_HOST = os.environ.get('REDIS_HOST', '127.0.0.1')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')


# Django Rest Framework

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        # "rest_framework.renderers.JSONRenderer",
        "drf_standardized_response.renderers.StandardizedJSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "EXCEPTION_HANDLER": "drf_standardized_errors.handler.exception_handler",
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    # "DEFAULT_AUTHENTICATION_CLASSES": [
    #     "rest_framework.authentication.TokenAuthentication",
    #     # "apps.auth_tokens.auth.TokenAuthentication",
    # ],
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Antanaitis courses", # название проекта
    "VERSION": "0.0.1", # версия проекта
    "SERVE_INCLUDE_SCHEMA": False, # исключить эндпоинт /schema
    "SWAGGER_UI_SETTINGS": {
        "filter": True, # включить поиск по тегам
    },
    "COMPONENT_SPLIT_REQUEST": True
}


DRF_STANDARDIZED_RESPONSE = {
    "WRAP_PAGINATED_RESPONSE": True,
}


DRF_STANDARDIZED_ERRORS = {
    "ENABLE_IN_DEBUG_FOR_UNHANDLED_EXCEPTIONS": True,
}

#Yandex S3

AWS_S3_ACCESS_KEY_ID = os.getenv('AWS_S3_ACCESS_KEY_ID')
AWS_S3_SECRET_ACCESS_KEY = os.getenv('AWS_S3_SECRET_ACCESS_KEY')
AWS_S3_ENDPOINT_URL = 'https://storage.yandexcloud.net'
# AWS_STORAGE_BUCKET_NAME = 'coursestest'
AWS_STORAGE_BUCKET_NAME = 'atom1zer-backet'
# AWS_S3_REGION_NAME = 'your_bucket_region' 
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_FILE_OVERWRITE = False
# AWS_QUERYSTRING_AUTH = False

STORAGES = {

    # Media file (image) management  
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
    },
   
    # CSS and JS file management
    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
    },
}

#Yandex S3
