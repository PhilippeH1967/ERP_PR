# Story 1.2: Core Models, Multi-Tenancy & Audit Trail

Status: done

## Story

As a **developer**,
I want the core infrastructure models (Tenant, TenantScopedModel, VersionedModel, AuditMixin) and PostgreSQL RLS middleware,
So that all future models inherit multi-tenancy isolation, optimistic locking, and audit capabilities.

## Acceptance Criteria

1. **Given** the Django project from Story 1.1 **When** I create a model inheriting from TenantScopedModel **Then** the model automatically includes `tenant_id` FK and is filtered by RLS policies
2. **And** the TenantMiddleware reads `tenant_id` from JWT claims and sets the PostgreSQL session variable
3. **And** VersionedModel provides a `version` integer field with auto-increment on save
4. **And** AuditMixin integrates django-simple-history with `history_user`, `history_date`, `history_change_reason`
5. **And** OptimisticLockMixin returns 409 Conflict when version mismatch on update
6. **And** RLS policies are created via `python manage.py setup_rls`
7. **And** Unit tests verify tenant isolation (user A cannot see user B's data)

## Tasks / Subtasks

- [x] Task 1: Install and configure django-simple-history (AC: #4)
  - [x] 1.1 Added `django-simple-history>=3.7,<4.0` to `requirements/base.txt`
  - [x] 1.2 Added `simple_history` to `INSTALLED_APPS` in `config/settings/base.py`
  - [x] 1.3 Added `simple_history.middleware.HistoryRequestMiddleware` to `MIDDLEWARE`
  - [x] 1.4 Docker image rebuilt successfully

- [x] Task 2: Create core base models in `apps/core/models.py` (AC: #1, #3, #4)
  - [x] 2.1 `Tenant` model: id, name, slug (unique), is_active, created_at
  - [x] 2.2 `TenantScopedModel` abstract: tenant FK (CASCADE, db_index=True), inherits TimestampedModel
  - [x] 2.3 `TimestampedModel` abstract: created_at (auto_now_add), updated_at (auto_now)
  - [x] 2.4 `VersionedModel` abstract: version (PositiveIntegerField, default=1), auto-increment via F() on save
  - [x] 2.5 AuditMixin pattern documented: models add `history = HistoricalRecords()`
  - [x] 2.6 Migration 0001_initial created and applied (Tenant + SampleTenantModel)

- [x] Task 3: Create TenantMiddleware in `apps/core/middleware.py` (AC: #2)
  - [x] 3.1 TenantMiddleware extracts `X-Tenant-Id` header (JWT in Story 1.3)
  - [x] 3.2 Executes `SET app.current_tenant = {tenant_id}` via cursor
  - [x] 3.3 Stores `request.tenant_id` for view access
  - [x] 3.4 Returns 400 for invalid tenant_id, skips exempt paths (health, schema, admin)
  - [x] 3.5 Added to MIDDLEWARE after CorsMiddleware, before SessionMiddleware

- [x] Task 4: Create OptimisticLockMixin in `apps/core/mixins.py` (AC: #5)
  - [x] 4.1 `OptimisticLockMixin` for DRF serializers: checks If-Match header or version in payload
  - [x] 4.2 Raises `VersionConflictError` (409) with `{"error": {"code": "VERSION_CONFLICT", ...}}`
  - [x] 4.3 On match: proceeds with save, version auto-incremented by VersionedModel
  - [x] 4.4 `VersionConflictError` handled by custom exception handler (dict details support added)

- [x] Task 5: Create `setup_rls` management command (AC: #6)
  - [x] 5.1 Created `apps/core/management/commands/setup_rls.py`
  - [x] 5.2 Auto-discovers all non-abstract TenantScopedModel subclasses
  - [x] 5.3 `ALTER TABLE {table} ENABLE ROW LEVEL SECURITY`
  - [x] 5.4 Creates tenant_isolation policy with USING + WITH CHECK
  - [x] 5.5 Idempotent: `DROP POLICY IF EXISTS` before CREATE
  - [x] 5.6 Error handling per table with summary
  - [x] 5.7 structlog logging + stdout summary

- [x] Task 6: Create a sample TenantScopedModel for testing (AC: #1, #7)
  - [x] 6.1 `SampleTenantModel(TenantScopedModel, VersionedModel)` with name field, db_table=core_sample
  - [x] 6.2 Migration created and applied
  - [x] 6.3 `setup_rls` ran: core_sample RLS policy created

- [x] Task 7: Write comprehensive tests (AC: #1-#7)
  - [x] 7.1 test_models.py: Tenant CRUD (3 tests), TenantScopedModel FK + cascade (2 tests), VersionedModel auto-increment (4 tests)
  - [x] 7.2 AuditMixin pattern documented (HistoricalRecords testing deferred to models that use it)
  - [x] 7.3 test_middleware.py: valid tenant, missing tenant, invalid tenant 400, health exempt, schema exempt, session variable (6 tests)
  - [x] 7.4 test_mixins.py: version match succeeds, mismatch 409, no version proceeds, error attributes (4 tests)
  - [x] 7.5 test_rls.py: all data visible, app-level filtering, cross-tenant isolation, session variable (4 tests)
  - [x] 7.6 test_management.py: runs successfully, finds models, idempotent (3 tests)
  - [x] 7.7 All 32 tests pass (0 regressions, 26 new + 6 existing)
  - [x] 7.8 ruff: 0 errors

## Dev Notes

### Story 1.1 Learnings (APPLY THESE)

- **pytest config key**: Use `pythonpath` not `python_paths` in pyproject.toml
- **DRF exception routing**: Only endpoints routed through DRF trigger custom exception handler. Django's default 404 returns HTML.
- **ruff strictness**: All imports must be explicit. Unused imports = error. Use `# noqa` sparingly.
- **Docker ports**: Local ports 5434 (postgres) and 5174 (vue) due to conflicts. Internal Docker ports unchanged.
- **API response format**: Already implemented in `apps/core/renderers.py` and `apps/core/exceptions.py`. All new endpoints must use it.

### Critical Architecture Requirements

**Tenant Model:**
```python
class Tenant(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "core_tenant"
```

**TenantScopedModel (abstract):**
```python
class TenantScopedModel(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, db_index=True)

    class Meta:
        abstract = True
```

**VersionedModel (abstract):**
```python
class VersionedModel(models.Model):
    version = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        if self.pk:  # Only increment on update, not create
            self.version += 1
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
```

**AuditMixin pattern — models add:**
```python
from simple_history.models import HistoricalRecords

class Invoice(TenantScopedModel, VersionedModel):
    # ... fields ...
    history = HistoricalRecords()
```

### TenantMiddleware Implementation Pattern

```python
class TenantMiddleware:
    EXEMPT_PATHS = ["/api/v1/health/", "/admin/", "/api/schema/"]

    def __call__(self, request):
        if any(request.path.startswith(p) for p in self.EXEMPT_PATHS):
            return self.get_response(request)

        tenant_id = request.headers.get("X-Tenant-Id")
        # Story 1.3 will switch to JWT extraction:
        # tenant_id = request.auth.get("tenant_id") if hasattr(request, "auth") else None

        if not tenant_id:
            # Return 400 for API, pass through for non-API
            ...

        with connection.cursor() as cursor:
            cursor.execute("SET app.current_tenant = %s", [tenant_id])

        request.tenant_id = int(tenant_id)
        request.tenant = Tenant.objects.get(pk=tenant_id)
        return self.get_response(request)
```

### PostgreSQL RLS — Exact SQL

```sql
-- Enable RLS on table
ALTER TABLE {table} ENABLE ROW LEVEL SECURITY;

-- Drop existing policy (idempotent)
DROP POLICY IF EXISTS tenant_isolation ON {table};

-- Create isolation policy
CREATE POLICY tenant_isolation ON {table}
  USING (tenant_id = current_setting('app.current_tenant')::int)
  WITH CHECK (tenant_id = current_setting('app.current_tenant')::int);
```

### OptimisticLockMixin — 409 Response Format

```json
{
  "error": {
    "code": "VERSION_CONFLICT",
    "message": "Record modified by another user",
    "details": {
      "current_version": 4,
      "your_version": 3
    }
  }
}
```

Implement via custom DRF exception in `apps/core/exceptions.py`:
```python
class VersionConflictError(APIException):
    status_code = 409
    default_detail = "Record modified by another user"
    default_code = "VERSION_CONFLICT"
```

### Files to MODIFY (from Story 1.1)

| File | Action |
|------|--------|
| `apps/core/models.py` | Replace stub with Tenant, TenantScopedModel, TimestampedModel, VersionedModel |
| `apps/core/middleware.py` | Replace stub with TenantMiddleware |
| `apps/core/mixins.py` | Replace stub with OptimisticLockMixin |
| `apps/core/exceptions.py` | Add VersionConflictError class |
| `config/settings/base.py` | Add `simple_history` to INSTALLED_APPS, add middleware |
| `requirements/base.txt` | Uncomment django-simple-history, add version pin |

### Files to CREATE

| File | Purpose |
|------|---------|
| `apps/core/management/commands/setup_rls.py` | RLS policy management command |
| `apps/core/tests/test_middleware.py` | TenantMiddleware tests |
| `apps/core/tests/test_mixins.py` | OptimisticLockMixin tests |
| `apps/core/tests/test_rls.py` | Tenant isolation tests |
| `apps/core/tests/test_management.py` | setup_rls command tests |

### Naming Conventions (Enforce)

| Context | Convention | Example |
|---------|-----------|---------|
| Django models | PascalCase singular | `Tenant`, `TenantScopedModel` |
| DB tables | snake_case (Django auto: `{app}_{model}`) | `core_tenant` |
| DB columns | snake_case | `tenant_id`, `created_at`, `is_active` |
| FK fields | `{model}_id` (Django auto) | `tenant_id` |
| Indexes | `idx_{table}_{columns}` | `idx_core_tenant_slug` |
| Constraints | `uq_{table}_{columns}` | `uq_core_tenant_slug` |

### What This Story Does NOT Include

- **Story 1.3**: JWT token generation/validation, SSO. TenantMiddleware uses `X-Tenant-Id` header for now.
- **Story 1.4**: RBAC, django-rules predicates, ProjectRole model
- Real application models (Project, Invoice, etc.) — those come in Epics 2-5

### PgBouncer Compatibility Note

PgBouncer in transaction pooling mode resets session variables between transactions. TenantMiddleware MUST set `app.current_tenant` at the START of every request, not once per connection. This is already handled by the middleware pattern above.

### References

- [Source: _bmad-output/planning-artifacts/architecture.md — Multi-tenancy, RLS, Base Models, Middleware]
- [Source: _bmad-output/planning-artifacts/epics.md — Epic 1 Story 1.2 AC and requirements]
- [Source: _bmad-output/planning-artifacts/prd.md — NFR9 (salary RLS), NFR10 (audit), NFR28 (80% coverage), NFR31 (optimistic locking)]
- [Source: _bmad-output/implementation-artifacts/1-1-project-scaffolding-docker-infrastructure.md — Previous story learnings]

## Dev Agent Record

### Agent Model Used

Claude Opus 4.6 (1M context)

### Debug Log References

- Ruff DJ012: Meta class must come before save() method in VersionedModel — reordered
- Ruff F401: Unused imports (rest_framework.status, Response, APIRequestFactory, django.conf.settings) — removed
- Ruff I001: Unsorted imports in test_management.py — reordered
- Ruff E501: Migration auto-generated lines >100 chars — added per-file-ignore in pyproject.toml
- Exception handler updated to support dict-type details from VersionConflictError
- VersionedModel uses F("version") + 1 with refresh_from_db() to avoid race conditions

### Completion Notes List

- Ultimate context engine analysis completed — comprehensive developer guide created
- All 7 tasks (30 subtasks) completed and verified
- Models: Tenant, TimestampedModel, TenantScopedModel, VersionedModel, SampleTenantModel
- Middleware: TenantMiddleware with X-Tenant-Id header extraction, exempt paths, session variable SET
- Mixins: OptimisticLockMixin with VersionConflictError (409)
- Management: setup_rls command — auto-discovers models, creates RLS policies, idempotent
- Tests: 32 total (26 new + 6 existing), all passing
- Ruff: 0 errors

### Change Log

- 2026-03-17: Story 1.2 implemented — core models, multi-tenancy middleware, optimistic locking, RLS setup

### File List

**Modified:**
- backend/requirements/base.txt — added django-simple-history
- backend/config/settings/base.py — added simple_history to INSTALLED_APPS, TenantMiddleware + HistoryRequestMiddleware to MIDDLEWARE
- backend/apps/core/models.py — replaced stub with Tenant, TimestampedModel, TenantScopedModel, VersionedModel, SampleTenantModel
- backend/apps/core/middleware.py — replaced stub with TenantMiddleware
- backend/apps/core/mixins.py — replaced stub with OptimisticLockMixin + VersionConflictError
- backend/apps/core/exceptions.py — added dict details support for VersionConflictError
- backend/apps/core/tests/test_models.py — replaced stub with 9 tests (Tenant, TenantScopedModel, VersionedModel)
- backend/pyproject.toml — added migrations E501 per-file-ignore

**Created:**
- backend/apps/core/migrations/0001_initial.py — Tenant + SampleTenantModel migration
- backend/apps/core/management/commands/setup_rls.py — RLS policy management command
- backend/apps/core/tests/test_middleware.py — 6 TenantMiddleware tests
- backend/apps/core/tests/test_mixins.py — 4 OptimisticLockMixin tests
- backend/apps/core/tests/test_rls.py — 4 tenant isolation tests
- backend/apps/core/tests/test_management.py — 3 setup_rls command tests
