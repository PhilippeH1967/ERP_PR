"""Core app URL configuration."""

from django.db import connection
from django.urls import path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


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

    # Database check
    try:
        connection.ensure_connection()
        checks["database"] = "ok"
    except Exception:
        checks["database"] = "error"
        healthy = False

    # Redis/cache check
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
]
