import os

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
    "localhost",
]

INSTALLED_APPS += [  # NOQA
    "django_extensions",
    "debug_toolbar",
]  # NOQA

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # NOQA

GRAPH_MODELS = {
    "all_applications": True,
    "group_models": True,
}

if os.environ.get("GITHUB_WORKFLOW"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "postgres",
            "USER": "postgres",
            "PASSWORD": "postgres",
            "HOST": "0.0.0.0",
            "PORT": "5432",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRES_DB"),
            "USER": os.environ.get("POSTGRES_USER"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
            "HOST": os.environ.get("POSTGRES_HOST"),
            "PORT": os.environ.get("POSTGRES_PORT"),
        },
        # "default": {
        #     "ENGINE": "django.db.backends.sqlite3",
        #     "NAME": BASE_DIR / "db.sqlite3",
        # }
    }
