from dotenv import load_dotenv

from config.settings.base import *  # NOQA

SECRET_KEY = getenv("SECRET_KEY")
load_dotenv()
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS += [  # NOQA
    "localhost",
    "127.0.0.1",
]

INTERNAL_IPS = [  # NOQA
    "127.0.0.1",
    "localhost",  # NOQA
]

INSTALLED_APPS += [  # NOQA
    "django_extensions",
    "debug_toolbar",
]

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # NOQA

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # NOQA
    }
}
