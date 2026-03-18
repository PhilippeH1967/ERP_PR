"""
Core middleware for multi-tenancy and request tracking.

TenantMiddleware sets the PostgreSQL session variable `app.current_tenant`
for RLS policy enforcement on every request.
"""

import structlog
from django.db import connection
from django.http import JsonResponse

logger = structlog.get_logger()

# Paths exempt from tenant context requirement
TENANT_EXEMPT_PATHS = (
    "/api/v1/health/",
    "/api/v1/auth/",
    "/api/schema/",
    "/admin/",
    "/accounts/",
)


class TenantMiddleware:
    """
    Extract tenant_id from JWT claims or X-Tenant-Id header.

    Priority:
    1. JWT token payload (via simplejwt — decoded by DRF before views)
    2. X-Tenant-Id header (development/testing fallback)
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip tenant context for exempt paths
        if any(request.path.startswith(p) for p in TENANT_EXEMPT_PATHS):
            request.tenant_id = None
            request.tenant = None
            return self.get_response(request)

        # Try to extract tenant_id from JWT token
        tenant_id = self._extract_tenant_from_jwt(request)

        # Fallback to X-Tenant-Id header (development/testing)
        if tenant_id is None:
            tenant_id = request.headers.get("X-Tenant-Id")

        if not tenant_id:
            request.tenant_id = None
            request.tenant = None
            return self.get_response(request)

        try:
            tenant_id = int(tenant_id)
        except (ValueError, TypeError):
            return JsonResponse(
                {
                    "error": {
                        "code": "INVALID_TENANT",
                        "message": "Tenant ID must be a valid integer",
                        "details": [],
                    }
                },
                status=400,
            )

        # Validate tenant exists
        from apps.core.models import Tenant

        try:
            tenant = Tenant.objects.get(pk=tenant_id, is_active=True)
        except Tenant.DoesNotExist:
            return JsonResponse(
                {
                    "error": {
                        "code": "TENANT_NOT_FOUND",
                        "message": "Tenant not found or inactive",
                        "details": [],
                    }
                },
                status=404,
            )

        # Set PostgreSQL session variable for RLS
        with connection.cursor() as cursor:
            cursor.execute("SET app.current_tenant = %s", [str(tenant_id)])

        request.tenant_id = tenant_id
        request.tenant = tenant

        logger.bind(tenant_id=tenant_id)

        return self.get_response(request)

    def _extract_tenant_from_jwt(self, request):
        """Decode JWT from Authorization header to extract tenant_id claim."""
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return None

        token_str = auth_header[7:]  # Strip "Bearer "
        try:
            from rest_framework_simplejwt.tokens import AccessToken

            token = AccessToken(token_str, verify=False)  # Verify happens in DRF
            return token.get("tenant_id")
        except Exception:
            return None
