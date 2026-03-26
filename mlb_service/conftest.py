"""Root conftest — sets Django settings for all tests."""
import django
from django.conf import settings


def pytest_configure():
    pass  # Settings loaded via DJANGO_SETTINGS_MODULE in pyproject.toml
