"""Core app URL configuration."""

from django.db import connection
from django.urls import path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenVerifyView

from apps.core.auth import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    auth_config,
    auth_me,
    delegation_delete,
    delegation_list_create,
    user_create,
    user_list,
    user_update,
)


@api_view(["GET"])
@permission_classes([AllowAny])
def api_root(request):
    """API root endpoint — version info."""
    return Response(
        {
            "name": "ERP API",
            "version": "1.0.0",
            "status": "ok",
        }
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    """Health check endpoint — verifies database and cache connectivity."""
    checks = {}
    healthy = True

    try:
        connection.ensure_connection()
        checks["database"] = "ok"
    except Exception:
        checks["database"] = "error"
        healthy = False

    try:
        from django.core.cache import cache

        cache.set("_health_check", "1", timeout=5)
        if cache.get("_health_check") == "1":
            checks["cache"] = "ok"
        else:
            checks["cache"] = "error"
            healthy = False
    except Exception:
        checks["cache"] = "error"
        healthy = False

    status_code = 200 if healthy else 503
    return Response(
        {"status": "healthy" if healthy else "unhealthy", "checks": checks},
        status=status_code,
    )


urlpatterns = [
    path("", api_root, name="api-root"),
    path("health/", health_check, name="health-check"),
    # JWT Authentication endpoints
    path("auth/token/", CustomTokenObtainPairView.as_view(), name="token-obtain"),
    path("auth/token/refresh/", CustomTokenRefreshView.as_view(), name="token-refresh"),
    path("auth/token/verify/", TokenVerifyView.as_view(), name="token-verify"),
    path("auth/me/", auth_me, name="auth-me"),
    path("auth/config/", auth_config, name="auth-config"),
    path("users/", user_list, name="user-list"),
    path("users/create/", user_create, name="user-create"),
    path("users/<int:pk>/", user_update, name="user-update"),
    path("delegations/", delegation_list_create, name="delegation-list"),
    path("delegations/<int:pk>/", delegation_delete, name="delegation-delete"),
]
