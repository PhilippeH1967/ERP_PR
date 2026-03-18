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
    "/api/schema/",
    "/admin/",
)


class TenantMiddleware:
    """
    Extract tenant_id from request and set PostgreSQL session variable.

    Current: reads X-Tenant-Id header (development/testing).
    Story 1.3 will switch to JWT claim extraction.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip tenant context for exempt paths
        if any(request.path.startswith(p) for p in TENANT_EXEMPT_PATHS):
            request.tenant_id = None
            request.tenant = None
            return self.get_response(request)

        # Extract tenant_id from header (Story 1.3 will use JWT)
        tenant_id = request.headers.get("X-Tenant-Id")

        if not tenant_id:
            # Allow unauthenticated requests to pass through
            # (DRF permission classes will handle auth enforcement)
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
                        "message": "X-Tenant-Id must be a valid integer",
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
