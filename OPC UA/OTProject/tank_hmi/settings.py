from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent


# Security
SECRET_KEY = "django-insecure-change-this-key"

DEBUG = True

ALLOWED_HOSTS = []


# Applications
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "process",
]


# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]


# URL configuration
ROOT_URLCONF = "tank_hmi.urls"


# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates"
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# WSGI / ASGI
WSGI_APPLICATION = "tank_hmi.wsgi.application"
ASGI_APPLICATION = "tank_hmi.asgi.application"


# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = []


# Internationalization
LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Brussels"

USE_I18N = True

USE_TZ = True


# Static files
STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]


# Default primary key
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ALLOWED_HOSTS = [
    "192.168.1.50",
    "localhost",
    "127.0.0.1",
]