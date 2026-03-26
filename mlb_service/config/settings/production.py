"""Production settings."""

from .base import *  # noqa: F401, F403

DEBUG = False

# Security
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Use Redis cache in production
import environ  # noqa: E402

env = environ.Env()

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL", default="redis://localhost:6379/2"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# Production logging — JSON format
LOGGING["root"]["handlers"] = ["json"]  # type: ignore[name-defined] # noqa: F405
LOGGING["loggers"]["django"]["handlers"] = ["json"]  # type: ignore[name-defined] # noqa: F405
LOGGING["loggers"]["apps"]["handlers"] = ["json"]  # type: ignore[name-defined] # noqa: F405
LOGGING["loggers"]["clients"]["handlers"] = ["json"]  # type: ignore[name-defined] # noqa: F405
