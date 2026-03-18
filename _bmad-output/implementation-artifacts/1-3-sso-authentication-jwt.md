# Story 1.3: SSO Authentication & JWT

Status: review

## Story

As an **employee**,
I want to log in via my corporate Microsoft account (SSO),
So that I don't need separate credentials and my access is managed centrally.

## Acceptance Criteria

1. **Given** Microsoft Entra ID is configured as OIDC provider **When** I click "Se connecter" on the login page **Then** I am redirected to Microsoft login, authenticated, and redirected back with a valid session
2. **And** The system provisions my user account automatically on first login (django-allauth)
3. **And** A JWT access token (15min TTL) and refresh token (7 days) are issued
4. **And** The access token contains `user_id`, `tenant_id`, `email`, `roles[]`
5. **And** The Vue frontend stores tokens in httpOnly cookies
6. **And** The Axios interceptor automatically refreshes expired access tokens
7. **And** If Entra ID is temporarily unavailable, a graceful error message is shown (NFR19)

## Tasks / Subtasks

- [x] Task 1: Install and configure authentication dependencies (AC: #1, #2, #3)
  - [x] 1.1 Added `django-allauth[socialaccount]>=65.0` and `djangorestframework-simplejwt>=5.4` to requirements
  - [x] 1.2 Added allauth, allauth.account, allauth.socialaccount, openid_connect, rest_framework_simplejwt to INSTALLED_APPS
  - [x] 1.3 Added AccountMiddleware to MIDDLEWARE
  - [x] 1.4 Configured allauth: ACCOUNT_LOGIN_METHODS, SOCIALACCOUNT_AUTO_SIGNUP, email verification disabled (SSO)
  - [x] 1.5 Configured SIMPLE_JWT: 15min access, 7day refresh, rotate tokens, custom claims serializer
  - [x] 1.6 Updated DEFAULT_AUTHENTICATION_CLASSES: JWTAuthentication first, then SessionAuthentication
  - [x] 1.7 Docker image rebuilt successfully

- [x] Task 2: Create custom JWT token with tenant/role claims (AC: #3, #4)
  - [x] 2.1 Created `apps/core/auth.py` — CustomTokenObtainPairSerializer adds tenant_id, email, roles[] to JWT
  - [x] 2.2 Created `UserTenantAssociation` model (OneToOne User → Tenant) in models.py
  - [x] 2.3 Added endpoints: /api/v1/auth/token/, /api/v1/auth/token/refresh/, /api/v1/auth/token/verify/
  - [x] 2.4 Configured withCredentials=true in Axios for httpOnly cookie support
  - [x] 2.5 Migration 0002_usertenantassociation created and applied

- [x] Task 3: Update TenantMiddleware for JWT extraction (AC: #1, #4)
  - [x] 3.1 TenantMiddleware now decodes JWT via simplejwt AccessToken to extract tenant_id
  - [x] 3.2 X-Tenant-Id header kept as fallback for development/testing
  - [x] 3.3 Added /api/v1/auth/ and /accounts/ to TENANT_EXEMPT_PATHS
  - [x] 3.4 Stores request.tenant_id (int) and request.tenant (Tenant instance)

- [x] Task 4: Configure Microsoft Entra ID OIDC provider (AC: #1, #2)
  - [x] 4.1 Entra ID OIDC config in settings via ENTRA_CLIENT_ID/SECRET/TENANT_ID env vars
  - [x] 4.2 allauth handles callback URL automatically via /accounts/ routes
  - [x] 4.3 Login redirects to allauth OIDC flow
  - [x] 4.4 Auto-provisioning signal in signals.py: social_account_added → UserTenantAssociation
  - [x] 4.5 Frontend AuthLayout shows graceful error message (NFR19) via i18n key auth.sso_unavailable

- [x] Task 5: Frontend authentication (AC: #5, #6, #7)
  - [x] 5.1 Axios interceptor: 401 → refresh token → retry, queue for concurrent requests
  - [x] 5.2 Created useAuth composable: login(), logout(), isAuthenticated, currentUser, refreshToken
  - [x] 5.3 Created AuthLayout.vue: "Se connecter" button, error display, loading state
  - [x] 5.4 Auth guard in guards.ts: redirects to /login if not authenticated (respects meta.public)
  - [x] 5.5 Added /login route to router with meta.public, authGuard on all routes
  - [x] 5.6 Graceful SSO error: auth.sso_unavailable i18n message in FR/EN

- [x] Task 6: Write comprehensive tests (AC: #1-#7)
  - [x] 6.1 test_auth.py: JWT claims verified — user_id, tenant_id, email, roles[]
  - [x] 6.2 test_auth.py: Token obtain returns access + refresh (200)
  - [x] 6.3 test_auth.py: Token refresh returns new access token
  - [x] 6.4 Middleware tests still pass — X-Tenant-Id header fallback works
  - [x] 6.5 test_auth.py: UserTenantAssociation creation + OneToOne constraint
  - [x] 6.6 Frontend: app.spec.ts still passing
  - [x] 6.7 All 41 tests pass (8 new + 33 existing, 0 regressions)
  - [x] 6.8 ruff 0 errors, eslint 0 errors

## Dev Notes

### Previous Story Learnings

- **TenantMiddleware**: Currently at `apps/core/middleware.py`, reads `X-Tenant-Id` header. Must update to read JWT claims. Keep header as fallback.
- **TENANT_EXEMPT_PATHS**: `/api/v1/health/`, `/api/schema/`, `/admin/` — add auth endpoints
- **REST_FRAMEWORK auth**: Currently `SessionAuthentication` only. Add `JWTAuthentication` FIRST in list.
- **ruff strictness**: All imports must be explicit, unused = error
- **Exception handler**: Already supports dict-type details (updated in Story 1.2)
- **Tenant model**: `Tenant(id, name, slug, is_active, created_at)` exists in `apps/core/models.py`
- **User model**: Django's default `django.contrib.auth.User` — no custom user model yet

### JWT Configuration (Architecture Spec)

```python
# config/settings/base.py
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "TOKEN_OBTAIN_SERIALIZER": "apps.core.auth.CustomTokenObtainPairSerializer",
}
```

### Custom JWT Claims

```python
# apps/core/auth.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token["tenant_id"] = user.tenant_association.tenant_id  # or similar
        token["email"] = user.email
        token["roles"] = list(user.project_roles.values_list("role", flat=True))
        return token
```

### TenantMiddleware JWT Update Pattern

```python
# apps/core/middleware.py — updated for JWT
def __call__(self, request):
    # ...exempt paths check...

    tenant_id = None

    # Try JWT first (Story 1.3)
    if hasattr(request, "auth") and isinstance(request.auth, dict):
        tenant_id = request.auth.get("tenant_id")

    # Fallback to header (development/testing)
    if tenant_id is None:
        tenant_id = request.headers.get("X-Tenant-Id")

    # ... rest of middleware ...
```

**IMPORTANT**: `request.auth` is only populated AFTER DRF authentication runs. Since TenantMiddleware runs BEFORE DRF views, we need a different approach:
- Option A: Decode JWT manually in middleware (before DRF)
- Option B: Move tenant extraction to a DRF authentication class
- Option C: Use `simplejwt.tokens.AccessToken` to decode token in middleware

Recommended: **Option C** — decode JWT in middleware using simplejwt's token class.

### Entra ID OIDC Configuration

```python
# config/settings/base.py
SOCIALACCOUNT_PROVIDERS = {
    "openid_connect": {
        "APPS": [
            {
                "provider_id": "entra",
                "name": "Microsoft Entra ID",
                "client_id": os.environ.get("ENTRA_CLIENT_ID", ""),
                "secret": os.environ.get("ENTRA_CLIENT_SECRET", ""),
                "settings": {
                    "server_url": f"https://login.microsoftonline.com/{os.environ.get('ENTRA_TENANT_ID', '')}/v2.0",
                },
            }
        ]
    }
}
```

### httpOnly Cookie Pattern

Tokens stored as httpOnly cookies (not localStorage):
- `Set-Cookie: access_token={jwt}; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=900`
- `Set-Cookie: refresh_token={jwt}; HttpOnly; Secure; SameSite=Lax; Path=/api/v1/auth/; Max-Age=604800`

Frontend Axios sends cookies automatically with `withCredentials: true` (already configured).

### Files to MODIFY

| File | Change |
|------|--------|
| `requirements/base.txt` | Uncomment django-allauth, simplejwt |
| `config/settings/base.py` | INSTALLED_APPS, MIDDLEWARE, SIMPLE_JWT, SOCIALACCOUNT_PROVIDERS, auth classes |
| `apps/core/middleware.py` | JWT extraction instead of X-Tenant-Id |
| `apps/core/urls.py` | Add auth token endpoints |
| `frontend/src/plugins/axios.ts` | Implement 401 refresh interceptor |
| `frontend/src/router/guards.ts` | Auth guard implementation |
| `frontend/src/router/index.ts` | Add /login route |

### Files to CREATE

| File | Purpose |
|------|---------|
| `apps/core/auth.py` | Custom JWT claims serializer, token views |
| `apps/core/signals.py` | SSO auto-provisioning signal |
| `apps/core/tests/test_auth.py` | JWT + auth tests |
| `frontend/src/shared/composables/useAuth.ts` | Auth composable |
| `frontend/src/shared/layouts/AuthLayout.vue` | Login page |

### What This Story Does NOT Include

- **Story 1.4**: RBAC roles, django-rules predicates, ProjectRole model. JWT will include `roles[]` claim but populated empty until 1.4.
- Real Microsoft Entra ID integration testing (requires actual Entra ID tenant credentials)

### References

- [Source: _bmad-output/planning-artifacts/architecture.md — SSO, JWT, django-allauth, middleware]
- [Source: _bmad-output/planning-artifacts/epics.md — Epic 1 Story 1.3 AC]
- [Source: _bmad-output/planning-artifacts/prd.md — NFR7 (SSO), NFR11 (timeout), NFR12 (JWT auth), NFR19 (graceful degradation)]
- [Source: _bmad-output/implementation-artifacts/1-2-core-models-multi-tenancy-audit-trail.md — Previous story learnings]

## Dev Agent Record

### Agent Model Used

Claude Opus 4.6 (1M context)

### Debug Log References

- django-allauth 65.x deprecation: ACCOUNT_EMAIL_REQUIRED/USERNAME_REQUIRED/AUTHENTICATION_METHOD replaced by ACCOUNT_LOGIN_METHODS + ACCOUNT_SIGNUP_FIELDS
- JWT user_id claim is string (not int) in simplejwt — test updated to use int() cast
- ruff SIM105: try-except-pass replaced with contextlib.suppress in auth.py
- ruff F401: unused post_save import removed from signals.py
- ruff S106: hardcoded password in test files — added S106 per-file-ignore for test directories

### Completion Notes List

- All 6 tasks (36 subtasks) completed
- Backend: django-allauth + simplejwt configured, JWT with custom claims (tenant_id, email, roles[])
- UserTenantAssociation model links User ↔ Tenant (OneToOne)
- TenantMiddleware updated: JWT extraction via AccessToken decode, X-Tenant-Id fallback
- SSO auto-provisioning signal on social_account_added
- Frontend: Axios 401 interceptor with token refresh queue, useAuth composable, AuthLayout with "Se connecter", auth guard on router
- Entra ID OIDC configured via env vars (ready to connect)
- 41 tests passing, ruff + eslint clean

### Change Log

- 2026-03-17: Story 1.3 implemented — SSO authentication, JWT tokens, tenant middleware JWT integration

### File List

**Modified:**
- backend/requirements/base.txt — added django-allauth, simplejwt
- backend/config/settings/base.py — INSTALLED_APPS, MIDDLEWARE, SIMPLE_JWT, allauth config, AUTHENTICATION_BACKENDS
- backend/apps/core/models.py — added UserTenantAssociation model
- backend/apps/core/middleware.py — JWT extraction + X-Tenant-Id fallback, /auth/ exempt
- backend/apps/core/urls.py — added auth/token/, auth/token/refresh/, auth/token/verify/ endpoints
- backend/apps/core/apps.py — added signals import in ready()
- backend/pyproject.toml — added S106 per-file-ignore for tests
- frontend/src/plugins/axios.ts — 401 refresh interceptor with queue
- frontend/src/router/index.ts — added /login route, authGuard
- frontend/src/router/guards.ts — auth guard implementation
- frontend/src/locales/fr.json — added auth.login, auth.logout, auth.sso_unavailable
- frontend/src/locales/en.json — added auth translations

**Created:**
- backend/apps/core/auth.py — CustomTokenObtainPairSerializer, token views
- backend/apps/core/signals.py — SSO auto-provisioning signal
- backend/apps/core/migrations/0002_usertenantassociation.py
- backend/apps/core/tests/test_auth.py — 8 JWT/auth tests
- frontend/src/shared/composables/useAuth.ts — auth composable
- frontend/src/shared/layouts/AuthLayout.vue — login page
