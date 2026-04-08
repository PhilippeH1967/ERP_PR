"""
Production settings for ERP project.
"""

import os

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F401, F403

DEBUG = False

# Validate required environment variables
_hosts = os.environ.get("DJANGO_ALLOWED_HOSTS", "")
if not _hosts:
    raise ImproperlyConfigured("DJANGO_ALLOWED_HOSTS must be set in production")
ALLOWED_HOSTS = [h.strip() for h in _hosts.split(",") if h.strip()]

_secret = os.environ.get("DJANGO_SECRET_KEY", "")
if not _secret or "insecure" in _secret:
    raise ImproperlyConfigured("DJANGO_SECRET_KEY must be set to a secure value in production")

# Security settings — SSL is optional (set DJANGO_SECURE_SSL=true to enable)
_use_ssl = os.environ.get("DJANGO_SECURE_SSL", "false").lower() == "true"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https") if _use_ssl else None
# SSL redirect handled by Nginx, not Django (avoids healthcheck issues)
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = _use_ssl
CSRF_COOKIE_SECURE = _use_ssl
SECURE_HSTS_SECONDS = 31536000 if _use_ssl else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = _use_ssl
SECURE_HSTS_PRELOAD = _use_ssl
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

# CSRF trusted origins
_csrf_origins = os.environ.get("CSRF_TRUSTED_ORIGINS", "")
if _csrf_origins:
    CSRF_TRUSTED_ORIGINS = [o.strip() for o in _csrf_origins.split(",") if o.strip()]

# CORS
_cors_origins = os.environ.get("CORS_ALLOWED_ORIGINS", "")
if _cors_origins:
    CORS_ALLOWED_ORIGINS = [o.strip() for o in _cors_origins.split(",") if o.strip()]

# Sentry
SENTRY_ENVIRONMENT = "production"

# Static files served by Nginx
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
