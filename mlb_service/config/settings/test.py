"""Test settings — uses SQLite in-memory for speed."""

import os as _os

import environ as _environ

from .base import *  # noqa: E402, F401, F403

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Disable cache in tests
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

LOGGING_LEVEL = "WARNING"

# Opt into a separate test database explicitly; never use production DATABASE_URL.


if _os.environ.get("TEST_DATABASE_URL"):
    DATABASES = {"default": _environ.Env.db_url_config(_os.environ["TEST_DATABASE_URL"])}
MIDDLEWARE = [m for m in MIDDLEWARE if m != "whitenoise.middleware.WhiteNoiseMiddleware"]  # noqa: F405
INGEST_REQUIRE_STAFF = False
