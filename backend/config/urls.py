"""URL configuration for ERP project."""

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # API v1
    path("api/v1/", include("apps.core.urls")),
    path("api/v1/", include("apps.clients.urls")),
    path("api/v1/", include("apps.suppliers.urls")),
    path("api/v1/", include("apps.projects.urls")),
    path("api/v1/", include("apps.time_entries.urls")),
    path("api/v1/", include("apps.billing.urls")),
    path("api/v1/", include("apps.expenses.urls")),
    path("api/v1/", include("apps.dashboards.urls")),
    path("api/v1/", include("apps.data_ops.urls")),
    # SSO (django-allauth)
    path("accounts/", include("allauth.urls")),
    # OpenAPI schema
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
