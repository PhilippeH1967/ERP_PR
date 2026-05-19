"""Tenant context for code that runs outside the HTTP request cycle.

`TenantMiddleware` sets ``app.current_tenant`` for web/API requests so
PostgreSQL RLS can scope queries. Celery tasks, management commands and
any other non-request code path have no middleware, so they must set the
tenant explicitly before touching tenant-scoped tables — otherwise, once
the app connects with a non-superuser/non-owner role (audit F1), RLS
fails closed and those queries error.

Usage::

    for tenant in Tenant.objects.filter(is_active=True):
        with tenant_context(tenant.id):
            ...  # queries here are scoped to `tenant`
"""

import contextlib

from django.db import connection


@contextlib.contextmanager
def tenant_context(tenant_id):
    """Bind ``app.current_tenant`` to ``tenant_id`` for the block.

    Resets the GUC on exit so a pooled/persistent Celery connection never
    leaks a tenant context into the next iteration or task.
    """
    if tenant_id is None:
        raise ValueError("tenant_context requires a tenant_id")

    with connection.cursor() as cursor:
        cursor.execute("SET app.current_tenant = %s", [str(tenant_id)])
        try:
            yield
        finally:
            # RESET → empty string → `current_setting(...)::int` fails
            # closed for any subsequent unscoped query (safe default).
            cursor.execute("RESET app.current_tenant")
