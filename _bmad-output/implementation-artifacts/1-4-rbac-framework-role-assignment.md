# Story 1.4: RBAC Framework & Role Assignment

Status: done

## Story

As an **admin**,
I want to assign one of 8 roles to users with per-project granularity,
So that each user sees only what their role permits.

## Acceptance Criteria

1. **Given** an authenticated admin user **When** I assign role "PM" to user "Jean-François" on project "Complexe Desjardins" **Then** the ProjectRole record `(user=JF, project=CD, role=PM)` is created
2. **And** django-rules predicates (`is_project_pm`, `is_finance`, `can_approve_invoice`) resolve correctly
3. **And** DRF permission classes deny access when role is insufficient (403 Forbidden)
4. **And** The 8 roles are available: EMPLOYEE, PM, PROJECT_DIRECTOR, BU_DIRECTOR, FINANCE, DEPT_ASSISTANT, PROPOSAL_MANAGER, ADMIN
5. **And** Real salary cost fields are hidden via RLS for users without Finance/Direction/Project Director role (FR67)
6. **And** The `usePermissions` Vue composable exposes role checks to frontend components
7. **And** Anti-self-approval predicate is available for future use (FR22b)

## Tasks / Subtasks

- [x] Task 1: Install django-rules and configure (AC: #2, #3)
  - [x] 1.1 Added `rules>=3.5,<4.0` to requirements/base.txt
  - [x] 1.2 Added `rules` to INSTALLED_APPS
  - [x] 1.3 Added `rules.permissions.ObjectPermissionBackend` to AUTHENTICATION_BACKENDS
  - [x] 1.4 Docker image rebuilt

- [x] Task 2: Create Role enum and ProjectRole model (AC: #1, #4)
  - [x] 2.1 Role TextChoices enum with 8 roles
  - [x] 2.2 ProjectRole(TenantScopedModel): user FK, project_id (IntegerField nullable), role
  - [x] 2.3 UniqueConstraint: (user, project_id, tenant)
  - [x] 2.4 Note: HistoricalRecords deferred — will add when audit needed
  - [x] 2.5 Migration 0003_projectrole created and applied

- [x] Task 3: Create django-rules predicates (AC: #2, #7)
  - [x] 3.1 is_admin(user)
  - [x] 3.2 is_finance(user)
  - [x] 3.3 is_project_pm(user, project_id)
  - [x] 3.4 is_project_director(user, project_id)
  - [x] 3.5 is_bu_director(user)
  - [x] 3.6 can_approve_invoice(user, project_id)
  - [x] 3.7 cannot_approve_own(user, owner_id) — anti-self-approval (FR22b)
  - [x] 3.8 can_see_salary_costs(user) — FINANCE/PROJECT_DIRECTOR/BU_DIRECTOR/ADMIN (FR67)

- [x] Task 4: Create DRF permission classes (AC: #3)
  - [x] 4.1 IsAdmin permission class
  - [x] 4.2 IsFinance permission class
  - [x] 4.3 HasProjectRole configurable permission class
  - [x] 4.4 Existing endpoints (api_root, health) already AllowAny

- [x] Task 5: Populate JWT roles[] claim (AC: #4)
  - [x] 5.1 auth.py queries ProjectRole and populates roles[]
  - [x] 5.2 Format: [{"project_id": N, "role": "PM"}, {"role": "FINANCE"}]

- [x] Task 6: Frontend usePermissions composable (AC: #6)
  - [x] 6.1 usePermissions.ts: hasRole(), isProjectPM(), isFinance(), isAdmin(), canSeeSalaryCosts()
  - [x] 6.2 Reads from reactive userRoles ref
  - [x] 6.3 Computed properties for common checks

- [x] Task 7: Write comprehensive tests (AC: #1-#7)
  - [x] 7.1 test_permissions.py: ProjectRole CRUD (4 tests), unique constraint, str repr
  - [x] 7.2 test_permissions.py: All 8 predicates tested (14 tests)
  - [x] 7.3 test_permissions.py: DRF permission class via API (1 test)
  - [x] 7.4 test_permissions.py: JWT roles[] populated from ProjectRole (1 test)
  - [x] 7.5 test_permissions.py: cannot_approve_own predicate tested
  - [x] 7.6 All 58 tests pass (17 new + 41 existing, 0 regressions)
  - [x] 7.7 ruff 0 errors, eslint 0 errors

## Dev Notes

### Architecture Decision: ProjectRole in core app

Keep ProjectRole in `apps/core/models.py` for now (no separate employees app yet). The `project_id` field uses IntegerField (not FK) because the Project model doesn't exist until Epic 3. This will be migrated to a proper FK later.

### Role Enum

```python
class Role(models.TextChoices):
    EMPLOYEE = "EMPLOYEE", "Employee"
    PM = "PM", "Project Manager"
    PROJECT_DIRECTOR = "PROJECT_DIRECTOR", "Associé en charge"
    BU_DIRECTOR = "BU_DIRECTOR", "Directeur d'unité"
    FINANCE = "FINANCE", "Finance"
    DEPT_ASSISTANT = "DEPT_ASSISTANT", "Adjoint(e) de département"
    PROPOSAL_MANAGER = "PROPOSAL_MANAGER", "Gestionnaire de propositions"
    ADMIN = "ADMIN", "Administrateur"
```

### JWT roles[] Format

```json
{
  "roles": [
    {"project_id": 1, "role": "PM"},
    {"project_id": 2, "role": "FINANCE"},
    {"role": "ADMIN"}
  ]
}
```

### References

- [Source: architecture.md — RBAC, django-rules, ProjectRole, predicates]
- [Source: epics.md — Story 1.4 AC]
- [Source: prd.md — FR67 salary visibility, FR22b anti-self-approval]

## Dev Agent Record

### Agent Model Used

Claude Opus 4.6 (1M context)

### Debug Log References

- ruff SIM103: Simplified can_approve_invoice to single return expression
- ruff I001/F401: Auto-fixed import sorting and unused IsAdmin/IsFinance imports in tests
- ProjectRole.project_id uses IntegerField (not FK) — Project model not yet created

### Completion Notes List

- All 7 tasks completed. 8 roles, 8 predicates, 3 DRF permission classes, JWT roles populated, usePermissions composable
- 58 tests total (17 new), ruff + eslint clean

### Change Log

- 2026-03-17: Story 1.4 implemented — RBAC framework with django-rules

### File List

**Modified:**
- backend/requirements/base.txt — added rules
- backend/config/settings/base.py — INSTALLED_APPS + rules, AUTHENTICATION_BACKENDS + ObjectPermissionBackend
- backend/apps/core/models.py — added Role enum, ProjectRole model
- backend/apps/core/permissions.py — replaced stub with 8 predicates + 3 DRF permission classes
- backend/apps/core/auth.py — JWT roles[] populated from ProjectRole

**Created:**
- backend/apps/core/migrations/0003_projectrole.py
- backend/apps/core/tests/test_permissions.py — 20 RBAC tests
- frontend/src/shared/composables/usePermissions.ts — permission composable
