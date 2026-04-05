"""
Base settings for ERP project.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/topics/settings/
"""

import os
from datetime import timedelta

from celery.schedules import crontab
from pathlib import Path

import structlog

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ── Jazzmin Admin Theme ──
JAZZMIN_SETTINGS = {
    "site_title": "PR | ERP Admin",
    "site_header": "PR | ERP",
    "site_brand": "Provencher Roy",
    "welcome_sign": "Administration ERP — Provencher Roy",
    "copyright": "",
    "search_model": ["auth.User", "core.Tenant"],
    "topmenu_links": [
        {"name": "ERP App", "url": "/", "new_window": True},
        {"name": "API Swagger", "url": "/api/schema/swagger-ui/", "new_window": True},
    ],
    "show_sidebar": True,
    "navigation_expanded": False,
    "order_with_respect_to": [
        "core",
        "auth",
        "clients",
        "projects",
        "time_entries",
        "billing",
        "expenses",
        "suppliers",
        "notifications",
        "data_ops",
    ],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.User": "fas fa-user",
        "auth.Group": "fas fa-users",
        "core.Tenant": "fas fa-building",
        "core.ProjectRole": "fas fa-user-shield",
        "core.Delegation": "fas fa-exchange-alt",
        "core.UserTenantAssociation": "fas fa-link",
        "clients.Client": "fas fa-handshake",
        "clients.Contact": "fas fa-address-book",
        "clients.ClientAddress": "fas fa-map-marker-alt",
        "projects.Project": "fas fa-project-diagram",
        "projects.Phase": "fas fa-tasks",
        "projects.ProjectTemplate": "fas fa-clipboard-list",
        "projects.Amendment": "fas fa-file-contract",
        "time_entries.TimeEntry": "fas fa-clock",
        "time_entries.WeeklyApproval": "fas fa-check-double",
        "billing.Invoice": "fas fa-file-invoice-dollar",
        "billing.Payment": "fas fa-money-check-alt",
        "billing.CreditNote": "fas fa-receipt",
        "billing.DunningLevel": "fas fa-envelope-open-text",
        "expenses.ExpenseReport": "fas fa-receipt",
        "expenses.ExpenseCategory": "fas fa-tags",
        "suppliers.ExternalOrganization": "fas fa-truck",
        "suppliers.STInvoice": "fas fa-file-alt",
        "notifications.Notification": "fas fa-bell",
    },
    "default_icon_parents": "fas fa-folder",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": True,
    "use_google_fonts_cdn": True,
    "changeform_format": "horizontal_tabs",
}
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": True,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-primary",
    "accent": "accent-primary",
    "navbar": "navbar-dark navbar-primary",
    "no_navbar_border": True,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": True,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-change-me-in-production",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DJANGO_DEBUG", "False").lower() in ("true", "1", "yes")

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# Application definition
DJANGO_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "corsheaders",
    "rest_framework",
    "drf_spectacular",
    "django_filters",
    "simple_history",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.openid_connect",
    "rest_framework_simplejwt",
    "rules",
]

LOCAL_APPS = [
    "apps.core",
    "apps.clients",
    "apps.suppliers",
    "apps.projects",
    "apps.time_entries",
    "apps.billing",
    "apps.expenses",
    "apps.dashboards",
    "apps.notifications",
    "apps.consortiums",
    "apps.leaves",
    "apps.planning",
    "apps.data_ops",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "apps.core.middleware.TenantMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "erp_dev"),
        "USER": os.environ.get("POSTGRES_USER", "erp_user"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "change-me"),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        "ATOMIC_REQUESTS": True,
        "CONN_MAX_AGE": 600,
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "fr"
TIME_ZONE = "America/Toronto"
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ("fr", "Fran\u00e7ais"),
    ("en", "English"),
]

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django REST Framework
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "apps.core.renderers.WrappedJSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "apps.core.pagination.StandardPagination",
    "PAGE_SIZE": 25,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
    "DEFAULT_VERSION": "v1",
    "ALLOWED_VERSIONS": ["v1"],
    "EXCEPTION_HANDLER": "apps.core.exceptions.custom_exception_handler",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# drf-spectacular settings
SPECTACULAR_SETTINGS = {
    "TITLE": "ERP API",
    "DESCRIPTION": "Professional Services ERP - API Documentation",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SCHEMA_PATH_PREFIX": r"/api/v[0-9]+",
    "COMPONENT_SPLIT_REQUEST": True,
}

# Celery Configuration
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/1")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/2")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 300  # 5 minutes
CELERY_BEAT_SCHEDULE = {
    "send-timesheet-reminders-wed": {
        "task": "apps.time_entries.tasks.send_timesheet_reminders",
        "schedule": crontab(hour=17, minute=0, day_of_week="wed"),
    },
    "send-timesheet-reminders-fri": {
        "task": "apps.time_entries.tasks.send_timesheet_reminders",
        "schedule": crontab(hour=12, minute=0, day_of_week="fri"),
    },
    "escalate-missing-timesheets": {
        "task": "apps.time_entries.tasks.escalate_missing_timesheets",
        "schedule": crontab(hour=17, minute=0, day_of_week="fri"),
    },
    "expire-delegations": {
        "task": "apps.core.tasks.expire_delegations",
        "schedule": crontab(hour=1, minute=0),
    },
}

# Redis Cache
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": os.environ.get("REDIS_URL", "redis://localhost:6379/0"),
    }
}

# Structlog Configuration
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(0),
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=True,
)

# Sentry Configuration
SENTRY_DSN = os.environ.get("SENTRY_DSN", "")
SENTRY_ENVIRONMENT = os.environ.get("SENTRY_ENVIRONMENT", "development")
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.celery import CeleryIntegration
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        environment=SENTRY_ENVIRONMENT,
        integrations=[DjangoIntegration(), CeleryIntegration()],
        traces_sample_rate=0.1,
        send_default_pii=False,
    )

# CORS — defaults closed; opened per-environment in local.py
CORS_ALLOWED_ORIGINS = []
CORS_ALLOW_CREDENTIALS = True

# django-allauth configuration
AUTHENTICATION_BACKENDS = [
    "rules.permissions.ObjectPermissionBackend",
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION = "none"  # SSO handles verification
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
LOGIN_REDIRECT_URL = "/"
ACCOUNT_LOGOUT_REDIRECT_URL = "/"

# Microsoft Entra ID OIDC provider
_entra_client_id = os.environ.get("ENTRA_CLIENT_ID", "")
_entra_tenant_id = os.environ.get("ENTRA_TENANT_ID", "")
_entra_client_secret = os.environ.get("ENTRA_CLIENT_SECRET", "")
SOCIALACCOUNT_PROVIDERS = {}
if _entra_client_id and _entra_tenant_id:
    SOCIALACCOUNT_PROVIDERS = {
        "openid_connect": {
            "APPS": [
                {
                    "provider_id": "entra",
                    "name": "Microsoft Entra ID",
                    "client_id": _entra_client_id,
                    "secret": _entra_client_secret,
                    "settings": {
                        "server_url": (
                            f"https://login.microsoftonline.com/{_entra_tenant_id}/v2.0"
                        ),
                    },
                }
            ]
        }
    }

# djangorestframework-simplejwt configuration
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": False,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "TOKEN_OBTAIN_SERIALIZER": "apps.core.auth.CustomTokenObtainPairSerializer",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}
