import os

from config.settings.base import *  # NOQA

SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS += ["localhost"]  # NOQA

INSTALLED_APPS += []  # NOQA

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # NOQA
    }
}

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"] # NOQA
STATIC_ROOT = BASE_DIR / "staticfiles" # NOQA

MEDIA_ROOT = BASE_DIR / "media/" # NOQA
MEDIA_URL = "media/"
