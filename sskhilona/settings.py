"""
Django settings for sskhilona project.
"""

from pathlib import Path
import os
import dj_database_url
import cloudinary

BASE_DIR = Path(**file**).resolve().parent.parent

# ---------------- SECURITY ----------------

SECRET_KEY = os.environ.get(
"DJANGO_SECRET_KEY",
"django-insecure-#lw4%&t4n=^4ln%gbs_@!jof3!mv#)yv3_0sq2e9!8%d=*$izw"
)

DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "*").split(",")

# ---------------- INSTALLED APPS ----------------

INSTALLED_APPS = [
"django.contrib.admin",
"django.contrib.auth",
"django.contrib.contenttypes",
"django.contrib.sessions",
"django.contrib.messages",
"django.contrib.staticfiles",

```
# Third-party
"rest_framework",
"rest_framework.authtoken",
"corsheaders",

# Cloudinary
"cloudinary",
"cloudinary_storage",

# Local apps
"shop",
```

]

# ---------------- MIDDLEWARE ----------------

MIDDLEWARE = [
"corsheaders.middleware.CorsMiddleware",
"django.middleware.security.SecurityMiddleware",
"whitenoise.middleware.WhiteNoiseMiddleware",

```
"django.contrib.sessions.middleware.SessionMiddleware",
"django.middleware.common.CommonMiddleware",
"django.middleware.csrf.CsrfViewMiddleware",
"django.contrib.auth.middleware.AuthenticationMiddleware",
"django.contrib.messages.middleware.MessageMiddleware",
"django.middleware.clickjacking.XFrameOptionsMiddleware",
```

]

ROOT_URLCONF = "sskhilona.urls"

# ---------------- TEMPLATES ----------------

TEMPLATES = [
{
"BACKEND": "django.template.backends.django.DjangoTemplates",
"DIRS": [],
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

WSGI_APPLICATION = "sskhilona.wsgi.application"

# ---------------- DATABASE ----------------

DATABASES = {
"default": dj_database_url.parse(
os.environ.get("DATABASE_URL"),
conn_max_age=600,
ssl_require=False
)
}

# ---------------- PASSWORD VALIDATION ----------------

AUTH_PASSWORD_VALIDATORS = [
{"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
{"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
{"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
{"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------------- INTERNATIONALIZATION ----------------

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"

USE_I18N = True
USE_TZ = True

# ---------------- STATIC FILES ----------------

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_DIRS = [
os.path.join(BASE_DIR, "static"),
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ---------------- CLOUDINARY STORAGE ----------------

# Force Django to use Cloudinary for all uploaded files

DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.environ.get("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": os.environ.get("CLOUDINARY_API_KEY"),
    "API_SECRET": os.environ.get("CLOUDINARY_API_SECRET"),
}
# Cloudinary configuration

cloudinary.config(
cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
api_key=os.environ.get("CLOUDINARY_API_KEY"),
api_secret=os.environ.get("CLOUDINARY_API_SECRET")
)

# ---------------- DEFAULT PRIMARY KEY ----------------

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------- CORS ----------------

CORS_ALLOW_ALL_ORIGINS = True

# ---------------- DJANGO REST FRAMEWORK ----------------

REST_FRAMEWORK = {
"DEFAULT_AUTHENTICATION_CLASSES": [
"rest_framework.authentication.TokenAuthentication",
],
}
