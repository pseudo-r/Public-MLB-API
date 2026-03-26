"""apps.mlb app configuration."""
from django.apps import AppConfig


class MLBConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.mlb"
    label = "mlb"
    verbose_name = "MLB"
