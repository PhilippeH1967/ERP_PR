"""
Test settings for ERP project.
"""

import os

from .base import *  # noqa: F401, F403

# Speed up tests
DEBUG = False
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# Use in-memory SQLite for faster tests (switch to PostgreSQL for RLS tests later)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "erp_test",
        "USER": os.environ.get("POSTGRES_USER", "erp_user"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "change-me"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        "ATOMIC_REQUESTS": True,
    }
}

# Disable Celery in tests
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# Disable Sentry in tests
SENTRY_DSN = ""

# Use console email backend
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
