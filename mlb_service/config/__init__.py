"""config package — imports the Celery application."""
from .celery import app as celery_app

__all__ = ["celery_app"]
