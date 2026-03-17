---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8]
lastStep: 8
status: 'complete'
completedAt: '2026-03-17'
inputDocuments:
  - "_bmad-output/planning-artifacts/prd.md"
  - "_bmad-output/planning-artifacts/product-brief-ERP-2026-03-01.md"
  - "_bmad-output/planning-artifacts/ux-design-specification.md"
  - "_bmad-output/planning-artifacts/party-mode-reflexion-saisie-projet.md"
  - "_bmad-output/mockups/flux/valide/flux-01-depenses.html"
  - "_bmad-output/mockups/flux/valide/flux-02-projet.html"
  - "_bmad-output/mockups/flux/valide/flux-03-facturation.html"
  - "_bmad-output/mockups/flux/valide/flux-04-soustraitants.html"
  - "_bmad-output/mockups/flux/valide/flux-06-clients.html"
  - "_bmad-output/mockups/flux/valide/flux-07-propositions.html"
  - "_bmad-output/mockups/flux/valide/flux-09-consortium.html"
  - "_bmad-output/mockups/flux/valide/flux-10-delegation.html"
  - "_bmad-output/mockups/flux/valide/flux-11-admin.html"
  - "_bmad-output/mockups/flux/valide/timesheet-mockups.html"
workflowType: 'architecture'
project_name: 'ERP'
user_name: 'Philippe'
date: '2026-03-17'
---

# Architecture Decision Document

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._

## Project Context Analysis

### Requirements Overview

**Functional Requirements:**

99+ functional requirements organized across 14 domains. The architectural complexity concentrates in five areas:

1. **Dual Financial Layer (FR28-FR39i):** The separation between realization tracking (PM perspective: phases, hours, virtual profiles) and billing (Finance perspective: financial phases, contractual rates, invoice preparation). Financial phases group multiple realization phases with distinct billing modes (fixed-price or hourly). The 7-column invoice preparation screen requires real-time recalculation of CA/Salary ratios and advancement percentages. Includes: credit notes (FR39b), invoice cancellation/reissue (FR39c), partial payments (FR39d), write-offs (FR39e), multi-invoice payment allocation (FR39f), contractual holdback tracking (FR39g), complete adjustment history (FR39h), and cross-linked client↔ST holdback alerts (FR39i). Provisional invoice numbers (PROV-xxxx) assigned at creation, definitive at send time (FR30c).

2. **Consortium Management (FR59-FR64m):** Beyond dual financial perspective (consortium view vs Provencher view) and profit-sharing, includes: profit-sharing rules with multiple measurement modes (FR59b-c), basic manual profit distributions for MVP-1.5 (FR64a), guided profit distribution workflow for MVP-2 (FR64c-c2) with 2-level approval, consortium-to-client invoicing (FR64f), dedicated ST consortium tab (FR64h), per-project financial synthesis with dual KPIs (FR64i), budget tab with partner columns (FR64j), tax declarations at consortium level (FR64k-l), automated fiscal compliance analysis (FR64m), treasury/cash management (FR64e, FR64g). Mockups confirm: effort reconciliation (coefficient vs actual hours vs actual revenue), payment capacity assessment, and TPS/TVQ compliance tracking.

3. **Project Lifecycle & Amendments (FR1-FR15n):** Two-axis project structure (sequential phases + transversal support services) with 4-step creation wizard. Lifecycle management: project status (Active/Completed/On Hold/Cancelled) with FR15c, checklist-based project closing (FR15h), reopening (FR15i), archival (FR15j). Contract amendments (FR15k-l) introduce a 3-level budget tracking system: original contract, current contract (after amendments), and rebaselined plan (FR15n). Leadership role changes are immutably tracked (FR15g). Mockups confirm: WBS hierarchy with client-facing label distinction, budget tracking across hours/$/ ratios, and phase-level Gantt timeline.

4. **Expense Reports (FR40-FR46c):** 4-role approval workflow: Employee submits → Designated expense approver validates → Finance Analyst validates GL/taxes → Finance processes payment/export. Includes receipt management (FR40b, FR41b), expense templates (FR40c), expense reversal (FR46b), structured rejection with resubmission (FR46c). Mockups confirm: flow bar with role badges, KPI cards, bulk actions, refacturable flag tracking.

5. **Supplier Payment Tracking (FR47-FR52f):** Extended beyond 3-state lifecycle to include: ST credit notes (FR52b), dispute management with history (FR52c), partial payments with balance tracking (FR52d), contractual holdback per ST (FR52e), multi-document attachments and version history (FR52f). Mockups confirm: dual invoice tables (at-authorization vs authorized-waiting-payment), budget tracking by subcontractor and phase, Intact import integration.

**Additional Domains:**

6. **Service Proposals (FR53-FR58):** Lifecycle management (En cours → Soumise → Gagnée/Perdue/Abandonnée → Convertie) with Kanban + list views, competitive positioning tracking (FR53b), team assignment with visibility control (FR53c), conversion to project (FR56), commercial reporting KPIs (FR57). Mockups confirm: 6-item checklist tracking, pipeline dashboard, hours tracking per proposal, sales analytics (conversion rate, cost per proposal, win/loss analysis).

7. **Client Management (FR86-FR88b):** 5-tab client interface (Identification, Contacts, Addresses, Billing Parameters, CRM), duplicate detection (FR86b), alias/acronym search (FR86c), client groups (FR86d). External Organizations registry (FR88b) is a shared table used by ST management, consortium member selection, and proposal competitor tracking — deduplication across modules. Mockups confirm: financial summary with CA/unpaid/payment delay, associated projects list, aging analysis with follow-up tracking.

8. **Notification Center (FR89-FR92):** Centralized bell icon with badge, "Actions requises" dashboard section, per-event notification preferences, system-wide announcements.

9. **Data Operations (FR93-FR97):** Bulk imports via standardized templates with validation and dry-run (FR93), bulk exports with current filters (FR94), data retention/archival policies (FR95), data purge with legal retention (FR96), operations journal (FR97).

10. **Financial Operations (FR98-FR99):** Year-end adjustment entries (FR98), bank reconciliation at consortium level (FR99).

**Non-Functional Requirements:**

32 NFRs drive architectural decisions in 8 categories:

| Category | Key NFRs | Architectural Impact |
|----------|----------|---------------------|
| Performance | NFR1-6: <2s page load, <500ms draft save, <1s invoice recalc, <5s reports, <500ms search, <30s billing dossier | Caching strategy, query optimization, async processing |
| Security | NFR7-12: SSO Entra ID, TLS 1.3, AES-256, audit trail, 30min timeout, JWT auth | Authentication middleware, encryption, event sourcing |
| Scalability | NFR13-16: 400+ concurrent, 10+ years data, 2x growth support, time entry partitioning | Connection pooling, pagination, partitioning |
| Reliability | NFR17-19: 99.5% uptime, <1h RPO / <4h RTO, graceful degradation | Infrastructure redundancy, backup automation |
| Data Integrity | NFR20: 100% migration validation | Reconciliation tooling |
| Accessibility & UI | NFR21-22: WCAG 2.1 AA, desktop 1280px+ / tablet 1024px+ | Responsive design, a11y compliance |
| Integration | NFR23-26: Valid exports, bidirectional Intact sync, Entra auto-provision, Excel validation | API contracts, error handling |
| Concurrency | NFR31-32: Optimistic locking on all financial entities, real-time presence indicators | Versioning strategy, WebSocket architecture |
| Other | NFR27-30: OpenAPI spec, 80% test coverage, zero-downtime deploy, no-code config | CI/CD, documentation, admin interface |

**Scale & Complexity:**

- Primary domain: Full-stack web application (Django 5 + DRF backend, Vue 3 + Pinia frontend)
- Complexity level: Enterprise
- Estimated architectural components: 14+ Django apps, 12+ Vue feature modules
- User roles: 8 distinct roles with granular RBAC and delegation
- Concurrent users: 400+ (peak during Monday morning and monthly billing cycle)
- Historical data: 10+ years with partitioning requirement
- Phasing: MVP-1 (operational foundation), MVP-1.5 (productivity), MVP-2 (strategic intelligence + SaaS)

### Technical Constraints & Dependencies

**Imposed Technology Stack (from PRD):**
- Backend: Django 5.0 + Django REST Framework
- Frontend: Vue 3 + TypeScript + Pinia + TailwindCSS
- Database: PostgreSQL 16 (with Row-Level Security for multi-tenancy)
- Cache/Queue: Redis 7
- Async Tasks: Celery + Celery Beat
- Containerization: Docker + Docker Compose
- Web Server: Nginx (reverse proxy)
- API Docs: drf-spectacular (OpenAPI 3)

**UX Design System (from UX Spec + Mockups):**
- TailwindCSS + Headless UI (Vue) + TanStack Table + Chart.js + vue-chartjs
- VeeValidate + Zod for form validation
- Role-based color coding: Employee (blue #DBEAFE), PM (amber #FEF3C7), Finance (green #DCFCE7), Director (purple #EDE9FE), Admin (gray #F3F4F6)
- System font stack (no custom web fonts)
- Dark mode from Day 1 via Tailwind `dark:` prefix
- Monospace for financial amounts (column alignment)

**External Integrations:**
- Microsoft Entra ID (SSO via OIDC/SAML 2.0)
- Intact/Sage (invoice export CSV/Excel initially, bidirectional sync Phase 1.5)
- ChangePoint (one-time data migration: projects, WBS, time entries, billing history — 10+ years)
- HRIS (absence import via scheduled sync or manual file upload — Phase 1.5)
- Microsoft 365 (production email via Graph API)

**Organizational Constraints:**
- Dual legal entities: Provencher_Roy Prod and PRAA — impacts billing, tax (TPS/TVQ), and financial reporting
- 6 Business Units with independent reporting
- 31 position profiles (virtual profile reference list)
- 10+ invoice template formats per client
- Bilingual FR/EN application (Vue I18n)

### Cross-Cutting Concerns Identified

1. **RBAC & Permissions** — 8 roles with per-project, per-BU, and delegation-based access. Anti-self-approval enforcement (FR22b). Affects every API endpoint and UI component. Must support "acting as delegate" context switching with audit trail. Mockups confirm: role matrix with visibility rules (salary cost, billing, admin), delegation banner, and role-scoped views per module.

2. **Audit Trail** — Complete modification history on all financial entities (invoices, credit notes, payments, time corrections, budget changes, holdbacks, amendments, leadership role changes, expense reversals, ST disputes). Required for annual audit. Spans all modules. Mockups confirm: audit log table with delegation context tracking.

3. **Multi-Tenancy** — PostgreSQL RLS for data isolation. Per-tenant configuration (entities, BUs, positions, templates, invoice formats, tax settings). Must be transparent to application code. tenant_id in JWT claims.

4. **Real-Time Updates** — Django Channels (WebSocket) for: live dashboard updates, invoice preparation recalculations, notification delivery, and real-time presence indicators (NFR32: "Currently being edited by [user]"). Mockups confirm: KPI cards with trend indicators update in real-time.

5. **Dual Financial Layer** — The realization/billing separation permeates project management, time tracking, invoicing, and reporting. Every financial calculation must understand which layer it operates in. Three budget levels compound this: original, contractual (after amendments), rebaselined. Mockups confirm: 7-column invoice editor with editable cells, ratio banner with good/warning/danger states.

6. **Background Processing** — Celery for: report generation, billing dossier assembly, data migration jobs, scheduled reminders (timesheet, dunning), notification dispatch, bulk imports/exports, Excel validation. Requires robust task monitoring and error handling.

7. **Client-Specific Customization** — Invoice labels (FR33b), invoice templates (FR33), dunning schedules (FR37b), billing parameters, and tax settings vary per client/project. Configuration model must be flexible without becoming unmanageable.

8. **Optimistic Locking & Concurrency** — NFR31 requires versioned concurrency control on all financial entities. NFR32 requires WebSocket-based presence indicators on invoice preparation and project budget screens. Conflict resolution UX: show other user's changes with reload/force-save options.

9. **Shared Entity Registry** — External Organizations (FR88b) is referenced by ST management, consortium membership, and proposal competitors. Deduplication and type-tagging (same firm can be ST on one project, partner on another). This cross-module dependency requires careful data model design.

10. **Holdback Cross-Linking** — Client holdbacks (FR39g) and ST holdbacks (FR52e) are linked via FR39i: releasing client holdback triggers alerts for corresponding ST holdback releases. This creates a cross-module financial dependency between billing and suppliers.

## Starter Template Evaluation

### Primary Technology Domain

Full-stack web application with separated backend (Django 6 + DRF) and frontend (Vue 3 + TypeScript). The tech stack is imposed by project configuration. The evaluation focuses on scaffolding tools.

**Version Update (March 2026):** The PRD specifies Django 5.0, but Django 6.0.3 is now the latest stable release (December 2025). Django 6.0 introduces a built-in Background Tasks Framework (unified API for background work, compatible with Celery as worker), native Content Security Policy support, and template partials. Django 5.2 is the current LTS. TailwindCSS has moved to v4.2.1 (5x faster builds). Vue 3.5.30 is the latest stable.

### Approach: Two Separate Starters (Backend + Frontend)

Given the enterprise complexity (14+ Django apps, WebSocket via Django Channels, Celery async processing, multi-tenant RLS), a monorepo Django+Vue starter would be too limiting. The architecture uses **two distinct projects** communicating via REST API + WebSocket.

### Starter Options Considered

| Option | Type | Verdict | Rationale |
|--------|------|---------|-----------|
| **cookiecutter-django** (2026.02.20) | Backend | ✅ Selected | Industry standard, production-ready, active maintenance, Docker + Celery + PostgreSQL preconfigured |
| **npm create vue@latest** | Frontend | ✅ Selected | Official Vue.js scaffolder, all required options (TS, Pinia, Router, Vitest, Playwright) |
| Monorepo Django+Vue (gtalarico, dja-vue) | Full-stack | ❌ Rejected | Too simplistic, no Celery/Channels support, unmaintained |
| vue3-enterprise-boilerplate (idimetrix) | Frontend | ❌ Rejected | Opinionated with unwanted libraries |
| Custom from scratch | Both | ❌ Rejected | No reason to reinvent what cookiecutter-django provides |

### Selected Backend Starter: cookiecutter-django (2026.02.20)

**Initialization Command:**

```bash
cookiecutter gh:cookiecutter/cookiecutter-django
```

**Key options:** PostgreSQL 16, Docker, Celery, DRF, Whitenoise

**Architectural Decisions Provided by Starter:**
- **Database:** PostgreSQL configured (versions 14-18)
- **Containerization:** Docker + Docker Compose for dev & production (Traefik + LetsEncrypt)
- **Async Tasks:** Celery + Flower preconfigured
- **Configuration:** Environment variables via django-environ
- **Static Files:** Whitenoise
- **Email:** Anymail (dev/test); production via Microsoft 365 Graph API
- **Security:** SSL by default, secure settings
- **Testing:** pytest preconfigured

**Post-Scaffolding Additions Required:**
- Upgrade to Django 6.0 (if cookiecutter scaffolds 5.2 LTS)
- Django REST Framework + drf-spectacular (OpenAPI 3)
- Django Channels (WebSocket for real-time updates)
- django-filter, django-cors-headers
- PostgreSQL Row-Level Security (custom middleware for multi-tenancy)
- SSO Microsoft Entra ID (django-allauth with OIDC)
- Redis 7 configuration for cache + Channels layer
- django-simple-history (audit trail)
- django-rules (predicate-based permissions)

### Selected Frontend Starter: npm create vue@latest

**Initialization Command:**

```bash
npm create vue@latest erp-frontend
# Interactive options selected:
# ✓ TypeScript
# ✓ Vue Router
# ✓ Pinia
# ✓ Vitest (unit testing)
# ✓ Playwright (E2E testing)
# ✓ ESLint + Prettier
```

**Architectural Decisions Provided by Starter:**
- **Language:** TypeScript with strict mode
- **State Management:** Pinia (official Vue 3 store)
- **Routing:** Vue Router 4
- **Build Tooling:** Vite (fast HMR, optimized builds)
- **Testing:** Vitest (unit) + Playwright (E2E)
- **Code Quality:** ESLint + Prettier

**Post-Scaffolding Additions Required:**
- TailwindCSS 4.x
- Headless UI (Vue) — accessible unstyled components
- TanStack Table (Vue) — high-performance data tables
- Chart.js + vue-chartjs — dashboard visualizations
- VeeValidate + Zod — form validation
- Axios (API client with JWT interceptor)
- VueUse (utility composables)
- Vue I18n (bilingual FR/EN)

**Note:** Project initialization using these commands should be the first implementation story.

## Core Architectural Decisions

### Decision Priority Analysis

**Critical Decisions (Block Implementation):**
- Multi-tenancy strategy (shared schema + RLS)
- Authentication method (SSO Microsoft Entra ID via django-allauth)
- API authentication (JWT)
- RBAC model (django-rules + custom ProjectRole, 8 roles)
- Hosting (on-premise Docker)
- Django version (6.0)
- Optimistic locking strategy (NFR31)

**Important Decisions (Shape Architecture):**
- Audit trail implementation (django-simple-history)
- API versioning (URL-based)
- Frontend component organization (feature-based)
- API client generation (OpenAPI codegen)
- CI/CD (GitHub Actions)
- Monitoring (Sentry + structlog)
- Real-time presence (NFR32)
- ASGI server (Uvicorn)

**Deferred Decisions (Post-MVP):**
- Multi-currency exchange rate provider
- Intact/Sage bidirectional sync protocol
- Mobile app technology
- AI/ML model selection (Phase 1.5+)

### Data Architecture

**Django Version: 6.0 (current: 6.0.3)**
- Decision: Use Django 6.0 instead of PRD-specified 5.0
- Built-in Background Tasks Framework for lightweight async (emails, notifications)
- Celery retained for heavy tasks (billing dossier generation, data migration, scheduled jobs, bulk imports)
- Native CSP support eliminates need for django-csp
- Rationale: Latest stable, active security support, background tasks reduce Celery dependency for simple cases
- Affects: All backend code, deployment configuration

**Multi-Tenancy: Shared Schema + Row-Level Security**
- Decision: Single PostgreSQL schema with RLS policies on all tenant-scoped tables
- Every tenant-scoped model includes a `tenant_id` FK
- Django middleware resolves tenant from JWT claims and sets `app.current_tenant` session variable
- RLS policies filter all queries transparently: `CREATE POLICY tenant_isolation ON {table} USING (tenant_id = current_setting('app.current_tenant')::int)`
- Rationale: Simpler migrations than schema-per-tenant, mature PostgreSQL feature, sufficient isolation for SaaS Phase 2
- Affects: Every Django model, all migrations, middleware layer

**Audit Trail: django-simple-history**
- Decision: Use django-simple-history on all financial models (Invoice, CreditNote, Payment, Holdback, TimeEntry corrections, Budget changes, Amendments, ExpenseReport, STInvoice, STDispute, ProfitDistribution, TaxDeclaration)
- Stores complete model snapshots on every change
- Includes `history_user` (who), `history_date` (when), `history_change_reason` (why)
- Delegation context tracked: `history_delegation_id` when action performed by delegate
- Rationale: Required for annual audit compliance, simple to implement, proven at scale
- Affects: All financial models, admin interface, reporting

**Optimistic Locking (NEW — NFR31)**
- Decision: `version` integer field on all financial entities (Invoice, CreditNote, Budget, TimeEntry, STInvoice, ExpenseReport, Holdback, Amendment)
- DRF serializer validates version on update; returns 409 Conflict with current state if mismatch
- Frontend displays conflict dialog: shows other user's changes, offers reload or force-save
- Rationale: NFR31 mandates no silent overwrites on financial data
- Affects: All financial model serializers, frontend error handling

**Caching Strategy: Redis 7**
- Decision: Redis serves four roles:
  1. **Application cache**: Dashboard KPIs, project summaries (invalidated on write)
  2. **Configuration cache**: Tenant settings, templates, rate tables (TTL-based, 15min)
  3. **Session store**: Django session backend
  4. **Celery broker + result backend**: Task queue
- Rationale: Single Redis instance covers all use cases, reduces infrastructure complexity
- Affects: Django cache framework config, Celery config, session config

**Consortium Data Model:**
- Decision: Based on real consortium tracking data and expanded PRD (FR59-FR64m):
  - **Two rate types per member**: Associate rate (fixed hourly) and Employee rate (gross salary × multiplier)
  - **Multiplier varies**: configurable per consortium AND per project
  - **Consortium is the invoicing entity** — invoices client directly
  - **Profit sharing**: MVP-1.5 manual entry (FR64a), MVP-2 guided workflow (FR64c)
  - **Treasury**: MVP-2 cash flow tracking (FR64e, FR64g)
  - **Tax declarations**: MVP-2 at consortium level (FR64k-l)
  - **Fiscal compliance**: MVP-2 automated analysis (FR64m)
- Rationale: Phased approach — manual entry first, automation later
- Affects: Consortium models, billing module, reporting dashboards

### Authentication & Security

**SSO: django-allauth with OIDC (Microsoft Entra ID)**
- Decision: Use django-allauth with its OpenID Connect provider for Microsoft Entra ID
- No local passwords — all authentication via corporate SSO
- Fallback: service account with API key for system integrations (Celery tasks, API-to-API)
- Rationale: django-allauth is well-maintained, supports OIDC natively, large community
- Affects: Authentication middleware, user model, login flow

**RBAC: django-rules + Custom ProjectRole Model**
- Decision: Hybrid approach:
  - `django-rules` for predicate-based permission checks (e.g., `is_project_pm`, `can_approve_invoice`)
  - Custom `ProjectRole` model: `(user_id, project_id, role)` where role is one of: EMPLOYEE, PM, PROJECT_DIRECTOR, BU_DIRECTOR, FINANCE, DEPT_ASSISTANT, PROPOSAL_MANAGER, ADMIN
  - Anti-self-approval enforced via predicate (FR22b): `cannot_approve_own_timesheet`
  - Delegation modeled as `Delegation(delegator, delegate, project, permissions[], start_date, end_date)`
  - DRF permissions classes compose django-rules predicates
- Rationale: Predicates are lightweight, role-per-project is explicit, delegation is first-class
- Affects: Every API endpoint, every Vue component (role-based visibility), middleware

**API Authentication: JWT (djangorestframework-simplejwt)**
- Decision: JWT with short-lived access tokens (15min) + refresh tokens (7 days)
- Access token contains: `user_id`, `tenant_id`, `email`, `roles[]`
- Refresh handled transparently by Axios interceptor on frontend
- Rationale: Stateless, standard for SPA, works well with SSO
- Affects: DRF authentication classes, Axios interceptor, token storage (httpOnly cookie preferred)

**Real-Time Presence (NEW — NFR32)**
- Decision: WebSocket channel per financial screen (invoice preparation, project budget)
- Heartbeat every 30s; presence cleared after 60s timeout
- Message format: `{"type": "presence.update", "payload": {"user": "Nathalie", "screen": "invoice_prep", "project_id": 42}}`
- Rationale: NFR32 mandates immediate feedback when two users edit the same financial record
- Affects: Django Channels consumers, frontend WebSocket composable, invoice/budget screens

### API & Communication Patterns

**API Versioning: URL-Based**
- Decision: `/api/v1/` prefix for all endpoints
- Rationale: Explicit, simple, easy to maintain; appropriate for internal-first application becoming SaaS
- Affects: URL configuration, DRF router setup

**Real-Time: Django Channels + Redis Channel Layer**
- Decision: WebSocket via Django Channels for:
  - Invoice preparation: real-time CA/Salary ratio recalculation
  - Dashboard: live KPI updates
  - Notifications: push delivery
  - Presence: NFR32 editing indicators
- Redis as channel layer backend (reuses existing Redis instance)
- Rationale: Native Django solution, no additional infrastructure
- Affects: ASGI configuration, frontend WebSocket client, Pinia store subscriptions

**Pagination: Mixed Strategy**
- Decision:
  - **Offset/Limit** (default): Project lists, invoice lists, supplier lists — typically <1000 items
  - **Cursor-based**: Time entries history (10+ years of data), audit logs — potentially millions of rows
- DRF pagination classes configured per ViewSet
- Rationale: Simple pagination for normal use cases, cursor for large datasets
- Affects: DRF pagination configuration, frontend list components

**Error Handling: Structured Error Responses**
- Decision: Standardized JSON error format across all endpoints:
  ```json
  {"error": {"code": "VALIDATION_ERROR", "message": "...", "details": [{"field": "...", "message": "..."}]}}
  ```
- DRF exception handler customized to produce consistent format
- Business errors: specific codes → `BUDGET_EXCEEDED`, `PHASE_LOCKED`, `INVOICE_ALREADY_SENT`, `VERSION_CONFLICT`, `HOLDBACK_PENDING`
- Frontend Axios interceptor maps errors to user-friendly messages
- Affects: DRF exception handler, frontend error handling

### Frontend Architecture

**Component Organization: Feature-Based**
- Decision: `/src/features/{module}/` structure:
  ```
  src/features/
    projects/     → views, components, stores, api, types
    timesheet/    → views, components, stores, api, types
    billing/      → views, components, stores, api, types
    suppliers/    → views, components, stores, api, types
    consortiums/  → views, components, stores, api, types
    dashboard/    → views, components, stores, api, types
    expenses/     → views, components, stores, api, types
    proposals/    → views, components, stores, api, types
    clients/      → views, components, stores, api, types
    admin/        → views, components, stores, api, types
    delegation/   → views, components, stores, api, types
    data-ops/     → views, components, stores, api, types
  src/shared/     → design system, layouts, utilities
  ```
- Each feature is self-contained with its own Pinia store, API service, types, and components
- Rationale: Maps directly to ERP modules, clear ownership, easy to navigate
- Affects: Project structure, import conventions, code splitting

**API Client: OpenAPI Codegen**
- Decision: Generate TypeScript API client from drf-spectacular OpenAPI spec
- Axios instance with JWT interceptor used as HTTP transport
- Rationale: Eliminates frontend-backend type drift, reduces manual API client code
- Affects: Build pipeline (codegen step), frontend API layer, CI/CD

**Email: Microsoft 365 (Production) / Anymail (Dev/Test)**
- Decision: Production emails via Microsoft Graph API (M365 environment), Anymail with console backend for development and testing
- Rationale: Organization already on M365, consistent with SSO strategy
- Affects: Django email backend configuration, environment-specific settings

### Infrastructure & Deployment

**Hosting: On-Premise Docker**
- Decision: Self-hosted on company servers using Docker Compose
- Services: Django (ASGI via Uvicorn), Vue 3 (Nginx static), PostgreSQL 16, PgBouncer, Redis 7, Celery workers, Celery Beat
- PgBouncer in transaction pooling mode between Django and PostgreSQL — manages connection pool for 400+ concurrent users without exhausting PostgreSQL connections (max_db_connections: 100, default_pool_size: 25)
- Nginx as reverse proxy with TLS termination
- Recommended server sizing: 16 cores, 32-64 GB RAM, SSD NVMe
- Uvicorn: 4-8 workers for HTTP/WebSocket handling
- Celery: 4-8 workers for async tasks
- Rationale: Company preference for data sovereignty, existing server infrastructure. Single-node Docker Compose sufficient for 400 business users (peak ~300 req/min). Scale to Docker Swarm/Kubernetes only at Phase 2 SaaS (2000+ users)
- Affects: Docker Compose configuration, deployment scripts, backup strategy, Django DATABASE settings (point to PgBouncer, not PostgreSQL directly)

**ASGI Server: Uvicorn**
- Decision: Uvicorn as ASGI server for Django
- Rationale: Higher performance than Daphne, actively maintained, excellent Django Channels integration
- Affects: Docker configuration, ASGI entry point, production settings

**CI/CD: GitHub Actions**
- Decision: GitHub-hosted repository with GitHub Actions pipelines:
  - PR checks: lint (ruff + eslint), type check, unit tests, security scan
  - Main branch: build Docker images, run integration tests
  - Deploy: SSH to server, pull images, docker compose up
- Rationale: Code on GitHub, native integration, generous free tier
- Affects: `.github/workflows/` configuration, Docker image registry (GHCR)

**Monitoring: Sentry + structlog**
- Decision:
  - **Sentry**: Error tracking, performance monitoring (both Django and Vue 3 SDKs)
  - **structlog**: Structured JSON logging for Django (queryable, parseable)
  - Logs shipped to file or syslog (no external log service initially)
- Rationale: Sentry is industry standard for error tracking, structlog produces machine-readable logs
- Affects: Django logging config, Vue 3 error boundary, Sentry DSN configuration

### Decision Impact Analysis

**Implementation Sequence:**
1. Project scaffolding (cookiecutter-django + create vue)
2. Docker Compose environment setup
3. PostgreSQL 16 + Redis 7 configuration
4. Django 6.0 upgrade + background tasks setup
5. Authentication (django-allauth + Entra ID + JWT)
6. RBAC framework (django-rules + ProjectRole model)
7. RLS multi-tenancy middleware
8. Optimistic locking base (version field + DRF mixin)
9. Core Django apps (projects, employees, clients, time entries)
10. DRF API + drf-spectacular
11. Frontend scaffold + TailwindCSS 4 + OpenAPI codegen
12. Django Channels (WebSocket + presence)
13. Celery + Django background tasks
14. Feature modules (billing, suppliers, expenses, proposals, consortiums, etc.)

**Cross-Component Dependencies:**
- JWT ← depends on → SSO (Entra ID issues tokens)
- RLS ← depends on → JWT (tenant_id extracted from token)
- WebSocket ← depends on → JWT (authentication) + Redis (channel layer)
- Presence ← depends on → WebSocket + optimistic locking
- OpenAPI codegen ← depends on → DRF endpoints (spec must exist first)
- Audit trail ← depends on → Core models (must be added to financial models)
- Holdback cross-linking ← depends on → Billing + Suppliers apps both operational
- External Organizations ← depends on → Core app (shared by suppliers, consortiums, proposals)
- Django background tasks ← depends on → Django 6.0 (built-in framework)
- Consortium import ← depends on → Consortium data model + standardized Excel template

## Implementation Patterns & Consistency Rules

### Potential Conflict Points Identified

**30+ potential conflict points** across 5 categories where AI agents could make incompatible decisions if not standardized.

### Naming Patterns

**Database Naming Conventions:**
- Tables: `snake_case`, plural → `projects`, `time_entries`, `invoice_lines`, `credit_notes`, `external_organizations`
- Columns: `snake_case` → `created_at`, `tenant_id`, `unit_price`, `holdback_balance`
- Foreign keys: `{related_model}_id` → `project_id`, `employee_id`, `amendment_id`
- Indexes: `idx_{table}_{column(s)}` → `idx_time_entries_project_id`
- Constraints: `uq_{table}_{column(s)}` / `ck_{table}_{rule}` → `uq_employees_email`
- Version field: `version` (integer, for optimistic locking — NFR31)

**API Naming Conventions:**
- REST endpoints: plural, snake_case → `/api/v1/time_entries/`, `/api/v1/credit_notes/`, `/api/v1/external_organizations/`
- Route parameters: `{id}` (DRF default) → `/api/v1/projects/{id}/phases/`
- Query parameters: `snake_case` → `?business_unit_id=3&fiscal_year=2026`
- Custom headers: `X-Tenant-Id`, `X-Request-Id`, `If-Match` (optimistic locking version)
- Nested resources max 2 levels: `/projects/{id}/phases/` yes — use filters beyond that
- Action endpoints: `/api/v1/invoices/{id}/approve/`, `/api/v1/invoices/{id}/cancel/`

**Code Naming Conventions:**

| Context | Convention | Example |
|---------|-----------|---------|
| Django models | PascalCase, singular | `TimeEntry`, `InvoiceLine`, `CreditNote`, `ExternalOrganization` |
| Django apps | snake_case, plural | `time_entries`, `credit_notes`, `external_organizations` |
| Python functions/variables | snake_case | `get_billing_summary()`, `holdback_balance` |
| Vue components | PascalCase | `ProjectCard.vue`, `HoldbackTracker.vue` |
| Vue composables | camelCase, prefix `use` | `useProjectStore`, `usePresence` |
| Pinia stores | camelCase, prefix `use`, suffix `Store` | `useProjectStore`, `useClientStore` |
| TypeScript interfaces | PascalCase, no I prefix | `Project`, `CreditNote`, `Amendment` |
| TypeScript enums | PascalCase | `ProjectStatus.Active`, `BillingMode.FixedPrice` |
| CSS classes | kebab-case (Tailwind utilities) | custom classes: `invoice-header` |
| Vue files | PascalCase | `ProjectCard.vue`, `AmendmentHistory.vue` |
| TS files (non-component) | camelCase | `apiClient.ts`, `dateUtils.ts` |

### Structure Patterns

**Backend (Django):**
```
backend/
  config/              → settings, urls, asgi, wsgi, celery_app
  apps/
    core/              → Tenant, AuditMixin, TenantScopedModel, VersionedModel, middleware, utils
    employees/         → Employee, ProjectRole, Delegation, PositionProfile
    projects/          → Project, Phase, SupportService, Template, VirtualProfile, Amendment
    time_entries/      → TimeEntry, TimesheetLock, WeeklyApproval
    billing/           → FinancialPhase, Invoice, InvoiceLine, CreditNote, Payment,
                         PaymentAllocation, Holdback, WriteOff, BillingDossier, DunningLevel
    expenses/          → ExpenseReport, ExpenseLine, ExpenseCategory
    suppliers/         → ExternalOrganization, STInvoice, STPayment, STCreditNote,
                         STDispute, STHoldback
    proposals/         → Proposal, ProposalTeam, ProposalChecklist
    consortiums/       → Consortium, ConsortiumMember, ConsortiumProject,
                         MemberRate, ProfitDistribution, TaxDeclaration
    clients/           → Client, Contact, ClientAddress, ClientGroup
    dashboards/        → KPI aggregation endpoints
    notifications/     → Notification, NotificationPreference, WebSocket consumers
  templates/           → email templates, PDF templates
  static/
```
- Tests co-located: `apps/projects/tests/test_models.py`, `test_views.py`, `test_serializers.py`
- Each app contains: `models.py`, `serializers.py`, `views.py`, `urls.py`, `permissions.py`, `filters.py`, `services.py` (if needed), `tests/`

**Frontend (Vue 3):**
```
frontend/src/
  features/
    projects/
      views/           → ProjectList.vue, ProjectDetail.vue, ProjectCreate.vue
      components/      → ProjectCard.vue, PhaseTable.vue, AmendmentHistory.vue
      stores/          → useProjectStore.ts
      api/             → projectApi.ts
      types/           → project.types.ts
      composables/     → useProjectFilters.ts
    billing/           → InvoicePreparation, CreditNoteForm, HoldbackTracker, DunningDashboard
    timesheet/
    expenses/
    suppliers/
    proposals/
    consortiums/
    clients/
    dashboard/
    admin/
    delegation/
    data-ops/
  shared/
    components/        → BaseButton, DataTable, Modal, SlideOver, ConfirmDialog, FileUpload
    composables/       → useAuth, usePermissions, useNotification, useWebSocket, usePresence, useLocale
    layouts/           → MainLayout, AuthLayout
    utils/             → dateUtils, formatters, validators
    types/             → common.types.ts, api.types.ts
  router/              → index.ts, guards.ts
  plugins/             → axios.ts, i18n.ts, sentry.ts, websocket.ts
```

### Format Patterns

**API Response Formats:**

Success (single resource):
```json
{"data": {"id": 1, "name": "Project Alpha", "status": "active", "version": 3}}
```

Success (paginated list):
```json
{"data": [...], "meta": {"count": 42, "next": "...", "previous": "..."}}
```

Error:
```json
{"error": {"code": "VALIDATION_ERROR", "message": "...", "details": [{"field": "amount", "message": "Must be positive"}]}}
```

Version conflict (409):
```json
{"error": {"code": "VERSION_CONFLICT", "message": "Record modified by another user", "details": {"current_version": 4, "your_version": 3, "modified_by": "Nathalie", "modified_at": "2026-03-17T14:30:00Z"}}}
```

**Data Exchange Formats:**
- JSON fields: `snake_case` (consistent Python → JS, DRF serialization handles natively)
- Dates: ISO 8601 strings → `"2026-03-17T14:30:00Z"`
- Monetary amounts: `Decimal` in backend, `string` in JSON to avoid float rounding → `"15234.50"`
- Booleans: native JSON `true/false`
- Null: allowed only for optional fields, never as default value
- IDs: integers (PostgreSQL `BIGINT` auto-increment)
- Percentages: stored as `Decimal(5,2)` → `"65.50"` (not 0.655)

### Communication Patterns

**Event System (Django Signals + Channels):**
- Django signals: `{model}_{action}` → `invoice_created`, `timeentry_approved`, `holdback_released`, `amendment_approved`
- WebSocket groups: `{entity}_{id}` → `project_42`, `dashboard_bu_3`
- Presence groups: `presence_{screen}_{entity_id}` → `presence_invoice_prep_42`
- WebSocket message format:
```json
{"type": "invoice.updated", "payload": {"id": 12, "status": "approved", "version": 4}, "timestamp": "2026-03-17T14:30:00Z"}
```
- Presence message format:
```json
{"type": "presence.update", "payload": {"users": [{"id": 5, "name": "Nathalie", "since": "2026-03-17T14:28:00Z"}]}}
```
- Celery task naming: `{app}.tasks.{action}` → `billing.tasks.generate_dossier`, `notifications.tasks.send_dunning_email`
- Django background task naming: `{app}.tasks.{action}` → same convention as Celery

**State Management (Pinia):**
- One store per feature: `useProjectStore`, `useBillingStore`, `useClientStore`
- State: raw data only
- Getters: computed/filtered data
- Actions: API calls + mutations
- No shared global state between features — use events (mitt) or shared composables
- Loading states in each store: `{ loading: boolean, error: string | null }`
- Version tracking in store for optimistic locking: `{ data: T, version: number }`

### Process Patterns

**Error Handling:**
- Backend: custom DRF exception handler → standardized format (see above)
- Frontend: global Axios interceptor for 401 (refresh token), 403 (redirect), 409 (conflict dialog), 500 (Sentry + toast)
- Business errors: specific codes → `BUDGET_EXCEEDED`, `PHASE_LOCKED`, `INVOICE_ALREADY_SENT`, `VERSION_CONFLICT`, `HOLDBACK_PENDING`, `AMENDMENT_REQUIRES_APPROVAL`
- Logging: `structlog` with context bindings → `log.info("invoice.created", invoice_id=42, project_id=7, version=1)`

**Loading States:**
- Naming: `isLoading`, `isSubmitting`, `isFetching` in stores
- Skeleton loaders for initial page load
- Inline spinner for user actions (buttons)
- No global loading states — each feature manages its own

**Validation:**
- Backend: DRF serializer as source of truth (complete validation)
- Frontend: lightweight client-side validation (required fields, formats) via VeeValidate + Zod
- Never trust frontend — all business rules validated server-side
- Optimistic locking: version check is server-side only

**Optimistic Locking Flow:**
1. Frontend fetches entity → stores `version` from response
2. User edits → frontend sends PUT/PATCH with `If-Match: {version}` header
3. Backend checks version match → 200 OK with new version, or 409 Conflict
4. On 409: frontend shows conflict dialog with other user's changes
5. User chooses: reload (fetch latest) or force-save (re-submit with current version)

### Enforcement Guidelines

**All AI Agents MUST:**
1. Follow naming conventions exactly as described above
2. Place files in the defined folder structure — no ad-hoc directories
3. Use the standardized API response format (`data`/`error` wrapper)
4. Write tests in the `tests/` folder of each Django app, co-located
5. Use `snake_case` for all JSON exchanged between backend and frontend
6. Represent monetary amounts as `Decimal` (backend) / `string` (JSON)
7. Log with `structlog` in structured JSON, never `print()`
8. Name Celery/background tasks with full path `{app}.tasks.{action}`
9. Include `version` field on all financial entity serializers
10. Track delegation context in audit trail when applicable

**Pattern Enforcement:**
- Linting: `ruff` (Python) + `eslint` (TypeScript) with naming rules
- CI: automated API response format verification via integration tests
- Code review: pattern checklist validated before merge

**Good Examples:**
```python
# Backend: correct model with versioning + audit
class Invoice(TenantScopedModel, VersionedModel):
    project = models.ForeignKey("projects.Project", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=InvoiceStatus.choices)
    history = HistoricalRecords()
```
```typescript
// Frontend: correct store pattern with version tracking
export const useBillingStore = defineStore('billing', () => {
  const invoice = ref<Invoice | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  async function updateInvoice(id: number, data: Partial<Invoice>) {
    isLoading.value = true
    error.value = null
    try {
      const response = await billingApi.update(id, data, {
        headers: { 'If-Match': invoice.value?.version }
      })
      invoice.value = response.data
    } catch (e) {
      if (e.response?.status === 409) { /* show conflict dialog */ }
      else { error.value = e.message }
    } finally { isLoading.value = false }
  }

  return { invoice, isLoading, error, updateInvoice }
})
```

**Anti-Patterns:**
- ❌ `userId` in JSON (use `user_id`)
- ❌ `IProject` interface prefix (use `Project`)
- ❌ `print("debug")` in Python (use `structlog`)
- ❌ `GET /api/v1/project/` singular endpoint (use `/api/v1/projects/` plural)
- ❌ `amount: 15234.5` as float in JSON (use `"15234.50"` as string)
- ❌ Deeply nested routes `/projects/{id}/phases/{pid}/entries/{eid}` (use flat + filters)
- ❌ Global Pinia store shared across features (use per-feature stores)
- ❌ Silent PUT without `If-Match` on financial entities (use optimistic locking)
- ❌ Missing `version` field in financial entity responses

## Project Structure & Boundaries

### Requirements to Architecture Mapping

| FR Domain | Django App (backend) | Vue Feature (frontend) |
|-----------|---------------------|----------------------|
| FR1-FR15n (Projects) | `apps/projects/` | `features/projects/` |
| FR16-FR27e (Time Tracking) | `apps/time_entries/` | `features/timesheet/` |
| FR28-FR39i (Billing) | `apps/billing/` | `features/billing/` |
| FR40-FR46c (Expenses) | `apps/expenses/` | `features/expenses/` |
| FR47-FR52f (Suppliers) | `apps/suppliers/` | `features/suppliers/` |
| FR53-FR58 (Proposals) | `apps/proposals/` | `features/proposals/` |
| FR59-FR64m (Consortiums) | `apps/consortiums/` | `features/consortiums/` |
| FR65-FR71 (Users/RBAC) | `apps/employees/` | `features/admin/` |
| FR72-FR75 (Dashboards) | `apps/dashboards/` | `features/dashboard/` |
| FR76-FR85b (Localization/Config) | `apps/core/` | `shared/plugins/i18n` |
| FR86-FR88b (Clients) | `apps/clients/` | `features/clients/` |
| FR89-FR92 (Notifications) | `apps/notifications/` | `shared/composables/` |
| FR93-FR97 (Data Operations) | `apps/data_ops/` | `features/data-ops/` |
| FR98-FR99 (Financial Ops) | `apps/consortiums/` | `features/consortiums/` |

### Complete Project Directory Structure

```
erp-provencher/
├── README.md
├── docker-compose.yml
├── docker-compose.prod.yml
├── .env.example
├── .gitignore
├── .github/
│   └── workflows/
│       ├── ci-backend.yml
│       ├── ci-frontend.yml
│       └── deploy.yml
│
├── backend/
│   ├── Dockerfile
│   ├── Dockerfile.prod
│   ├── requirements/
│   │   ├── base.txt
│   │   ├── local.txt
│   │   └── production.txt
│   ├── manage.py
│   ├── pyproject.toml                → ruff, pytest config
│   ├── conftest.py                   → shared fixtures
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings/
│   │   │   ├── base.py
│   │   │   ├── local.py
│   │   │   ├── production.py
│   │   │   └── test.py
│   │   ├── urls.py
│   │   ├── asgi.py                   → ASGI + Channels routing
│   │   ├── wsgi.py
│   │   └── celery_app.py
│   ├── apps/
│   │   ├── core/
│   │   │   ├── models.py             → Tenant, AuditMixin, TenantScopedModel, VersionedModel
│   │   │   ├── middleware.py          → TenantMiddleware (RLS), RequestIDMiddleware
│   │   │   ├── permissions.py         → base predicates (is_admin, is_finance, etc.)
│   │   │   ├── exceptions.py          → custom DRF exception handler
│   │   │   ├── pagination.py          → StandardPagination, CursorPagination
│   │   │   ├── renderers.py           → wrapped response renderer (data/error)
│   │   │   ├── mixins.py              → OptimisticLockMixin (version check)
│   │   │   ├── utils.py
│   │   │   ├── management/
│   │   │   │   └── commands/
│   │   │   │       ├── setup_rls.py
│   │   │   │       └── seed_data.py
│   │   │   └── tests/
│   │   │       ├── test_middleware.py
│   │   │       ├── test_permissions.py
│   │   │       └── test_mixins.py
│   │   ├── employees/
│   │   │   ├── models.py             → Employee, ProjectRole, Delegation, PositionProfile
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   ├── permissions.py
│   │   │   ├── filters.py
│   │   │   ├── signals.py            → SSO user provisioning
│   │   │   └── tests/
│   │   ├── projects/
│   │   │   ├── models.py             → Project, Phase, SupportService, ProjectTemplate,
│   │   │   │                            VirtualProfile, PhaseAssignment, WBSElement, Amendment
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   ├── permissions.py         → is_project_pm, is_project_director predicates
│   │   │   ├── filters.py
│   │   │   ├── services.py            → project closing checklist, amendment workflow
│   │   │   ├── signals.py
│   │   │   └── tests/
│   │   ├── time_entries/
│   │   │   ├── models.py             → TimeEntry, TimesheetLock, WeeklyApproval, PeriodUnlock
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   ├── permissions.py         → anti-self-approval predicate (FR22b)
│   │   │   ├── filters.py
│   │   │   ├── services.py            → bulk time corrections (FR27d)
│   │   │   └── tests/
│   │   ├── billing/
│   │   │   ├── models.py             → FinancialPhase, Invoice, InvoiceLine, CreditNote,
│   │   │   │                            Payment, PaymentAllocation, Holdback, WriteOff,
│   │   │   │                            BillingDossier, InvoiceTemplate, ClientLabel,
│   │   │   │                            DunningLevel, DunningAction
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   ├── permissions.py         → can_approve_invoice, can_send_dunning
│   │   │   ├── filters.py
│   │   │   ├── services.py            → invoice calculation, CA/salary ratio, dunning logic,
│   │   │   │                            holdback tracking, payment allocation
│   │   │   ├── exports.py             → CSV/Excel export for Intact/Sage
│   │   │   └── tests/
│   │   ├── expenses/
│   │   │   ├── models.py             → ExpenseReport, ExpenseLine, ExpenseCategory, ExpenseApproval
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   ├── permissions.py         → 4-role approval chain
│   │   │   ├── filters.py
│   │   │   ├── exports.py             → Intact export
│   │   │   └── tests/
│   │   ├── suppliers/
│   │   │   ├── models.py             → ExternalOrganization, STInvoice, STPayment,
│   │   │   │                            STCreditNote, STDispute, STHoldback
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   ├── permissions.py
│   │   │   ├── filters.py
│   │   │   ├── services.py            → holdback cross-linking alerts (FR39i)
│   │   │   └── tests/
│   │   ├── proposals/
│   │   │   ├── models.py             → Proposal, ProposalTeam, ProposalChecklist, CompetitorTracking
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   ├── permissions.py
│   │   │   ├── services.py            → proposal-to-project conversion (FR56)
│   │   │   └── tests/
│   │   ├── consortiums/
│   │   │   ├── models.py             → Consortium, ConsortiumMember, ConsortiumProject,
│   │   │   │                            MemberRate, ProfitDistribution, TaxDeclaration, TreasuryEntry
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   ├── permissions.py
│   │   │   ├── filters.py
│   │   │   ├── services.py            → ratio calculations, billing alerts, fiscal compliance
│   │   │   ├── importers.py           → Excel import (FR64b)
│   │   │   └── tests/
│   │   ├── clients/
│   │   │   ├── models.py             → Client, Contact, ClientAddress, ClientGroup
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   ├── permissions.py
│   │   │   ├── filters.py
│   │   │   ├── services.py            → duplicate detection (FR86b)
│   │   │   └── tests/
│   │   ├── dashboards/
│   │   │   ├── views.py              → KPI aggregation endpoints
│   │   │   ├── serializers.py
│   │   │   ├── urls.py
│   │   │   ├── services.py            → dashboard data computation
│   │   │   └── tests/
│   │   ├── notifications/
│   │   │   ├── models.py             → Notification, NotificationPreference
│   │   │   ├── consumers.py           → WebSocket consumers (Channels)
│   │   │   ├── presence.py            → Presence tracking consumer (NFR32)
│   │   │   ├── routing.py             → WebSocket URL routing
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── urls.py
│   │   │   ├── tasks.py               → Celery tasks (send_email, send_dunning, reminders)
│   │   │   └── tests/
│   │   └── data_ops/
│   │       ├── models.py             → ImportJob, ExportJob, OperationsLog
│   │       ├── serializers.py
│   │       ├── views.py
│   │       ├── urls.py
│   │       ├── permissions.py
│   │       ├── importers.py           → bulk import engine (FR93)
│   │       ├── exporters.py           → bulk export engine (FR94)
│   │       ├── tasks.py               → async import/export tasks
│   │       └── tests/
│   ├── templates/
│   │   ├── emails/
│   │   │   ├── timesheet_reminder.html
│   │   │   ├── dunning_level1.html
│   │   │   ├── dunning_level2.html
│   │   │   └── dunning_level3.html
│   │   └── pdf/
│   │       └── invoice_base.html
│   └── static/
│       └── img/
│           └── logo.png
│
├── frontend/
│   ├── Dockerfile
│   ├── Dockerfile.prod
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── tailwind.config.ts
│   ├── eslint.config.js
│   ├── .prettierrc
│   ├── env.d.ts
│   ├── index.html
│   ├── public/
│   │   └── favicon.ico
│   ├── src/
│   │   ├── main.ts
│   │   ├── App.vue
│   │   ├── router/
│   │   │   ├── index.ts
│   │   │   └── guards.ts              → auth guard, role guard
│   │   ├── plugins/
│   │   │   ├── axios.ts               → interceptors (JWT refresh, 409 conflict)
│   │   │   ├── i18n.ts
│   │   │   ├── sentry.ts
│   │   │   └── websocket.ts           → WebSocket connection manager
│   │   ├── features/
│   │   │   ├── projects/
│   │   │   │   ├── views/
│   │   │   │   │   ├── ProjectList.vue
│   │   │   │   │   ├── ProjectCreate.vue        → 4-step wizard
│   │   │   │   │   └── ProjectDetail.vue
│   │   │   │   ├── components/
│   │   │   │   │   ├── ProjectCard.vue
│   │   │   │   │   ├── PhaseTable.vue
│   │   │   │   │   ├── SupportServiceList.vue
│   │   │   │   │   ├── VirtualProfileAssignment.vue
│   │   │   │   │   ├── AmendmentHistory.vue
│   │   │   │   │   ├── ProjectClosingChecklist.vue
│   │   │   │   │   ├── BudgetThreeLevelView.vue
│   │   │   │   │   └── ProjectRecapBanner.vue
│   │   │   │   ├── stores/ → useProjectStore.ts
│   │   │   │   ├── api/ → projectApi.ts
│   │   │   │   ├── types/ → project.types.ts
│   │   │   │   └── composables/ → useProjectFilters.ts
│   │   │   ├── timesheet/
│   │   │   │   ├── views/ → TimesheetWeek.vue
│   │   │   │   ├── components/ → TimesheetGrid, TimesheetRow, WeekNavigation, LockedPhaseIndicator
│   │   │   │   ├── stores/ → useTimesheetStore.ts
│   │   │   │   ├── api/ → timesheetApi.ts
│   │   │   │   └── types/ → timesheet.types.ts
│   │   │   ├── billing/
│   │   │   │   ├── views/ → InvoicePreparation (7-col), InvoiceList, BillingDossier,
│   │   │   │   │            CreditNoteForm, PaymentTracking, DunningDashboard
│   │   │   │   ├── components/ → InvoiceLineEditor, CaSalaryRatioBar, HoldbackTracker,
│   │   │   │   │                 PaymentAllocationForm, PresenceIndicator, ConflictDialog
│   │   │   │   ├── stores/ → useBillingStore.ts
│   │   │   │   ├── api/ → billingApi.ts
│   │   │   │   └── types/ → billing.types.ts
│   │   │   ├── expenses/
│   │   │   │   ├── views/ → ExpenseList, ExpenseCreate, ExpenseApproval
│   │   │   │   ├── components/ → ExpenseLineForm, ReceiptPreview, ApprovalChain
│   │   │   │   ├── stores/ → useExpenseStore.ts
│   │   │   │   ├── api/ → expenseApi.ts
│   │   │   │   └── types/ → expense.types.ts
│   │   │   ├── suppliers/
│   │   │   │   ├── views/ → SupplierList, STInvoiceEntry, PaymentAuth
│   │   │   │   ├── components/ → STBudgetTracker, DisputePanel, HoldbackST
│   │   │   │   ├── stores/ → useSupplierStore.ts
│   │   │   │   ├── api/ → supplierApi.ts
│   │   │   │   └── types/ → supplier.types.ts
│   │   │   ├── proposals/
│   │   │   │   ├── views/ → ProposalList, ProposalCreate, ProposalConvert
│   │   │   │   ├── components/ → ProposalChecklist, PipelineKanban, CompetitorTracker
│   │   │   │   ├── stores/ → useProposalStore.ts
│   │   │   │   ├── api/ → proposalApi.ts
│   │   │   │   └── types/ → proposal.types.ts
│   │   │   ├── consortiums/
│   │   │   │   ├── views/ → ConsortiumDashboard, ConsortiumDetail, ConsortiumImport, TaxDeclaration
│   │   │   │   ├── components/ → DualFinancialView, MemberRateTable, ProfitDistributionLog,
│   │   │   │   │                 EffortReconciliation, TreasuryPanel, BillingAlertPanel
│   │   │   │   ├── stores/ → useConsortiumStore.ts
│   │   │   │   ├── api/ → consortiumApi.ts
│   │   │   │   └── types/ → consortium.types.ts
│   │   │   ├── clients/
│   │   │   │   ├── views/ → ClientList, ClientDetail (5-tab)
│   │   │   │   ├── components/ → ClientForm, ContactList, AgingAnalysis, FinancialHistory
│   │   │   │   ├── stores/ → useClientStore.ts
│   │   │   │   ├── api/ → clientApi.ts
│   │   │   │   └── types/ → client.types.ts
│   │   │   ├── dashboard/
│   │   │   │   ├── views/ → HomeDashboard.vue
│   │   │   │   ├── components/ → KpiCard, ProjectStatusWidget, AlertsWidget, ActionsRequises
│   │   │   │   ├── stores/ → useDashboardStore.ts
│   │   │   │   └── api/ → dashboardApi.ts
│   │   │   ├── admin/
│   │   │   │   ├── views/ → UserManagement, RoleManagement, TenantSettings, DunningConfig
│   │   │   │   ├── components/ → RoleMatrix, MigrationStatus, AuditLogViewer
│   │   │   │   ├── stores/ → useAdminStore.ts
│   │   │   │   └── api/ → adminApi.ts
│   │   │   ├── delegation/
│   │   │   │   ├── views/ → DelegationManage.vue
│   │   │   │   ├── components/ → DelegationCard, DelegationBanner, DelegationHistory
│   │   │   │   ├── stores/ → useDelegationStore.ts
│   │   │   │   └── api/ → delegationApi.ts
│   │   │   └── data-ops/
│   │   │       ├── views/ → ImportWizard, ExportCenter, OperationsJournal
│   │   │       ├── components/ → ImportPreview, ValidationReport
│   │   │       ├── stores/ → useDataOpsStore.ts
│   │   │       └── api/ → dataOpsApi.ts
│   │   ├── shared/
│   │   │   ├── components/
│   │   │   │   ├── BaseButton.vue
│   │   │   │   ├── BaseInput.vue
│   │   │   │   ├── BaseSelect.vue
│   │   │   │   ├── BaseModal.vue
│   │   │   │   ├── SlideOver.vue
│   │   │   │   ├── DataTable.vue
│   │   │   │   ├── ConfirmDialog.vue
│   │   │   │   ├── ConflictDialog.vue       → reusable 409 handler
│   │   │   │   ├── FileUpload.vue
│   │   │   │   ├── ToastNotification.vue
│   │   │   │   └── SkeletonLoader.vue
│   │   │   ├── composables/
│   │   │   │   ├── useAuth.ts
│   │   │   │   ├── usePermissions.ts
│   │   │   │   ├── useNotification.ts
│   │   │   │   ├── useWebSocket.ts
│   │   │   │   ├── usePresence.ts           → NFR32
│   │   │   │   ├── useOptimisticLock.ts     → NFR31
│   │   │   │   └── useLocale.ts
│   │   │   ├── layouts/
│   │   │   │   ├── MainLayout.vue           → sidebar + topbar + delegation banner
│   │   │   │   └── AuthLayout.vue           → login/SSO redirect
│   │   │   ├── utils/
│   │   │   │   ├── dateUtils.ts
│   │   │   │   ├── formatters.ts            → currency, numbers, dates
│   │   │   │   └── validators.ts
│   │   │   └── types/
│   │   │       ├── common.types.ts          → ApiResponse<T>, PaginatedResponse<T>
│   │   │       └── auth.types.ts
│   │   └── assets/
│   │       ├── styles/
│   │       │   └── main.css                 → Tailwind imports + custom
│   │       └── images/
│   ├── e2e/
│   │   ├── playwright.config.ts
│   │   └── specs/
│   └── vitest.config.ts
│
├── pgbouncer/
│   └── pgbouncer.ini              → pool_mode=transaction, max_db_connections=100
│
├── nginx/
│   ├── nginx.conf
│   └── conf.d/
│       └── default.conf
│
└── docs/
    ├── api/                          → generated OpenAPI docs
    └── consortium-import-template.xlsx
```

### Architectural Boundaries

**API Boundaries:**
- All frontend → backend traffic goes through `/api/v1/` (REST) or `ws://` (WebSocket)
- No direct DB access from frontend
- Each Django app exposes its own `urls.py` mounted in `config/urls.py`
- Auth boundary: JWT verified by DRF before any access, RLS applied after
- Optimistic lock boundary: `If-Match` header verified by `OptimisticLockMixin`

**Component Boundaries (Frontend):**
- Features never import from each other directly
- Inter-feature communication via: router (navigation), mitt events (notifications), or shared composables
- `shared/` is the only authorized cross-cutting dependency

**Data Boundaries:**
- Each Django app owns its models — no cross-app FKs except to `core`, `employees`, and `clients`
- Authorized exceptions: `Project` (referenced by `time_entries`, `billing`, `consortiums`, `proposals`, `expenses`), `Client` (referenced by `projects`, `billing`, `proposals`), `ExternalOrganization` in `suppliers` (referenced by `consortiums`, `proposals`)
- All cross-app queries go through serializers, never direct model access from another app

**Service Boundaries:**
- Business logic in `services.py` (billing calculations, consortium ratios, holdback tracking, duplicate detection)
- Serializers handle validation and data transformation only
- Views handle HTTP concerns only (request/response, permissions, pagination)
- Celery/background tasks for anything > 500ms (PDF generation, email, billing dossier assembly, import processing)

### Detailed Requirements to Structure Mapping

| FR | Backend Location | Frontend Location | Notes |
|----|-----------------|-------------------|-------|
| FR1-FR4 (Project creation) | `apps/projects/views.py` | `features/projects/views/ProjectCreate.vue` | 4-step wizard |
| FR5-FR6 (Virtual profiles) | `apps/projects/models.py` | `features/projects/components/VirtualProfileAssignment.vue` | 3-tier priority modal |
| FR7 (WBS + dual labels) | `apps/projects/models.py:WBSElement` | `features/projects/components/PhaseTable.vue` | Client-facing labels |
| FR15h (Project closing) | `apps/projects/services.py` | `features/projects/components/ProjectClosingChecklist.vue` | Checklist workflow |
| FR15k-l (Amendments) | `apps/projects/models.py:Amendment` | `features/projects/components/AmendmentHistory.vue` | 3-level budget |
| FR15n (Rebaseline) | `apps/projects/models.py` | `features/projects/components/BudgetThreeLevelView.vue` | Original/contract/plan |
| FR16-FR27 (Time tracking) | `apps/time_entries/` | `features/timesheet/` | Weekly grid |
| FR22b (Anti-self-approval) | `apps/time_entries/permissions.py` | N/A (server-side only) | Predicate check |
| FR28-FR30 (Invoice prep) | `apps/billing/services.py` | `features/billing/views/InvoicePreparation.vue` | 7-col, WebSocket |
| FR33b (Client labels) | `apps/billing/models.py:ClientLabel` | `features/billing/components/` | Per-project config |
| FR37b (Dunning) | `apps/billing/models.py:DunningLevel` | `features/billing/views/DunningDashboard.vue` | Configurable levels |
| FR39b (Credit notes) | `apps/billing/models.py:CreditNote` | `features/billing/views/CreditNoteForm.vue` | Approval workflow |
| FR39d-f (Payments) | `apps/billing/models.py:Payment,PaymentAllocation` | `features/billing/views/PaymentTracking.vue` | Partial + allocation |
| FR39g (Holdbacks) | `apps/billing/models.py:Holdback` | `features/billing/components/HoldbackTracker.vue` | Running balance |
| FR40-FR46 (Expenses) | `apps/expenses/` | `features/expenses/` | 4-role approval |
| FR47-FR52 (Suppliers) | `apps/suppliers/` | `features/suppliers/` | ST lifecycle |
| FR52b-e (ST extended) | `apps/suppliers/models.py` | `features/suppliers/components/` | Credit notes, disputes, holdbacks |
| FR53-FR58 (Proposals) | `apps/proposals/` | `features/proposals/` | Kanban + conversion |
| FR59-FR64 (Consortiums) | `apps/consortiums/` | `features/consortiums/` | Dual financial view |
| FR64e,g (Treasury) | `apps/consortiums/models.py:TreasuryEntry` | `features/consortiums/components/TreasuryPanel.vue` | Cash flow (MVP-2) |
| FR64k-m (Tax/Fiscal) | `apps/consortiums/models.py:TaxDeclaration` | `features/consortiums/views/TaxDeclaration.vue` | Compliance (MVP-2) |
| FR65-FR71 (RBAC) | `apps/employees/`, `apps/core/permissions.py` | `features/admin/`, `shared/composables/usePermissions.ts` | Cross-cutting |
| FR72-FR75 (Dashboards) | `apps/dashboards/` | `features/dashboard/` | Real-time KPIs |
| FR86-FR88b (Clients) | `apps/clients/` | `features/clients/` | 5-tab interface |
| FR88b (Ext. Organizations) | `apps/suppliers/models.py:ExternalOrganization` | Shared across features | Deduplication |
| FR89-FR92 (Notifications) | `apps/notifications/` | `shared/composables/useNotification.ts` | Bell + actions |
| FR93-FR97 (Data Ops) | `apps/data_ops/` | `features/data-ops/` | Bulk import/export |

### Cross-Cutting Concerns Mapping

| Concern | Backend Files | Frontend Files |
|---------|--------------|----------------|
| Authentication (SSO) | `config/settings/base.py`, `apps/employees/signals.py` | `shared/composables/useAuth.ts`, `plugins/axios.ts`, `router/guards.ts` |
| RBAC | `apps/core/permissions.py`, `apps/employees/models.py:ProjectRole` | `shared/composables/usePermissions.ts` |
| Multi-tenancy (RLS) | `apps/core/middleware.py`, `apps/core/models.py:TenantScopedModel` | Transparent (JWT contains tenant_id) |
| Audit trail | `apps/core/models.py:AuditMixin` + django-simple-history | N/A (backend only) |
| Optimistic locking | `apps/core/mixins.py:OptimisticLockMixin`, `apps/core/models.py:VersionedModel` | `shared/composables/useOptimisticLock.ts`, `shared/components/ConflictDialog.vue` |
| Presence | `apps/notifications/presence.py` | `shared/composables/usePresence.ts` |
| Notifications | `apps/notifications/` | `shared/composables/useNotification.ts`, `plugins/websocket.ts` |
| Error handling | `apps/core/exceptions.py` | `plugins/axios.ts`, `plugins/sentry.ts` |
| Delegation | `apps/employees/models.py:Delegation` | `features/delegation/`, `shared/layouts/MainLayout.vue` (banner) |

### Integration Points

**External Integrations:**
- Microsoft Entra ID → `apps/employees/signals.py` (SSO user provisioning)
- Intact/Sage → `apps/billing/exports.py`, `apps/expenses/exports.py` (CSV/Excel export)
- ChangePoint → `apps/core/management/commands/` (one-time data migration)
- Sentry → `config/settings/production.py` + `frontend/src/plugins/sentry.ts`
- Microsoft 365 → `apps/notifications/tasks.py` (production email via Graph API)
- HRIS → `apps/time_entries/` (absence import — Phase 1.5)

**Data Flow:**
```
[Vue 3 SPA] ←→ [Nginx] ←→ [Django ASGI (Uvicorn, 4-8 workers)]
                                 ├── REST API (DRF)
                                 ├── WebSocket (Channels + Presence)
                                 ├── [PgBouncer] ←→ [PostgreSQL 16 + RLS]
                                 ├── [Redis 7] (cache + broker + channels)
                                 ├── [Celery Workers (4-8)] → heavy async tasks
                                 └── [Django Background Tasks] → lightweight async
```

### Development Workflow

**Local Development:**
- `docker-compose up` starts all services (Django, Vue dev server, PostgreSQL, Redis, Celery)
- Django runs on port 8000 (Uvicorn ASGI for WebSocket support)
- Vue dev server on port 5173 (Vite HMR)
- Nginx proxies both in production; in dev, direct access

**Build & Deploy:**
- CI builds Docker images tagged with commit SHA
- Deploy: SSH to server → pull images → `docker compose -f docker-compose.prod.yml up -d`
- Frontend built as static assets, served by Nginx
- Database migrations run as part of deploy script

## Architecture Validation Results

### Coherence Validation ✅

**Decision Compatibility:**
All technology choices are compatible and form a proven enterprise stack. Django 6.0 + DRF + Channels + Celery work together natively. The Django 6.0 Background Tasks Framework complements Celery without conflict. PostgreSQL 16 supports RLS for multi-tenancy. Redis 7 serves as Celery broker, Channels layer, and Django cache without conflicts. django-allauth OIDC feeds JWT tokens to simplejwt seamlessly. django-rules complements custom ProjectRole without overlapping DRF permissions. TailwindCSS 4 is compatible with Headless UI and TanStack Table.

**Pattern Consistency:**
snake_case flows consistently from database columns through API endpoints to JSON fields — no conversion layer needed. PascalCase is consistent across Vue components, TypeScript interfaces, and Django models. Feature-based organization mirrors between backend (Django apps) and frontend (Vue features) with 1:1 mapping.

**Structure Alignment:**
The 14 Django apps map directly to the 14 FR domains. Component boundaries are respected: no cross-app FK except to core/employees/clients/projects (shared reference data). Services layer isolates business logic from HTTP concerns. Tests are co-located within each app.

### Requirements Coverage Validation ✅

**Functional Requirements Coverage (99+ FRs — 100%):**

| Domain | FRs | Architecture Support |
|--------|-----|---------------------|
| Projects (FR1-FR15n) | 20+ | `apps/projects/` — models, phases, templates, WBS, virtual profiles, amendments, lifecycle, rebaseline |
| Time Tracking (FR16-FR27e) | 12+ | `apps/time_entries/` — weekly grid, locks, approvals, anti-self-approval, bulk corrections, period unlock |
| Billing (FR28-FR39i) | 18+ | `apps/billing/` — invoices, credit notes, holdbacks, payment allocation, write-offs, dossiers, dunning, exports |
| Expenses (FR40-FR46c) | 10+ | `apps/expenses/` — reports, 4-role approval, receipts, categories, reversal, rejection, exports |
| Suppliers (FR47-FR52f) | 10+ | `apps/suppliers/` — ST invoices, credit notes, disputes, partial payments, holdbacks, attachments |
| Proposals (FR53-FR58) | 8 | `apps/proposals/` — lifecycle, checklist, team, competitors, conversion, KPIs |
| Consortiums (FR59-FR64m) | 18+ | `apps/consortiums/` — members, rates, profit distribution, treasury, tax, fiscal compliance, import |
| Users/RBAC (FR65-FR71) | 7 | `apps/employees/` + `apps/core/` — 8 roles, delegation, audit |
| Dashboards (FR72-FR75) | 4 | `apps/dashboards/` — KPI aggregation, real-time widgets |
| Localization (FR76-FR85b) | 12+ | `apps/core/` + `shared/plugins/i18n` — locale-aware, migration, parallel run |
| Clients (FR86-FR88b) | 6 | `apps/clients/` — 5-tab interface, contacts, duplicate detection, groups |
| Notifications (FR89-FR92) | 4 | `apps/notifications/` — WebSocket, email, preferences, announcements |
| Data Operations (FR93-FR97) | 5 | `apps/data_ops/` — bulk import/export, archival, purge, journal |
| Financial Ops (FR98-FR99) | 2 | `apps/consortiums/` — year-end adjustments, bank reconciliation |

**Non-Functional Requirements Coverage (32/32 — 100%):**

| NFR Category | Architectural Support |
|-------------|----------------------|
| Performance (NFR1-6) | Redis cache, WebSocket for real-time recalc, cursor pagination, Celery async |
| Security (NFR7-12) | Entra ID OIDC, JWT, RLS, django-simple-history, structlog, CSP (Django 6 native) |
| Scalability (NFR13-16) | Cursor pagination, Celery + Django background tasks, Redis cache, partitioning |
| Reliability (NFR17-19) | Docker containers, automated backups, Sentry monitoring, graceful degradation |
| Data Integrity (NFR20) | Migration commands + reconciliation scripts |
| Accessibility (NFR21-22) | Headless UI (ARIA), responsive design, TailwindCSS breakpoints |
| Integration (NFR23-26) | openpyxl exports, Intact API, Entra auto-provision, Excel validation |
| Concurrency (NFR31-32) | VersionedModel + OptimisticLockMixin + usePresence composable |
| Other (NFR27-30) | drf-spectacular, pytest 80%+, Docker rolling updates, admin no-code config |

### Implementation Readiness Validation ✅

**Decision Completeness:**
- All libraries specified with versions verified (March 2026)
- Naming patterns documented with concrete examples for every context
- Anti-patterns identified to prevent common mistakes
- API response format standardized with JSON examples
- Enforcement guidelines with linting and CI checks
- Optimistic locking flow documented step by step

**Structure Completeness:**
- Complete directory tree with ~150+ explicitly named files
- Each Django app has mandatory files listed (models, serializers, views, urls, permissions, tests)
- Each Vue feature has standard structure (views, components, stores, api, types)
- Docker, CI/CD, and infrastructure files all specified

**Pattern Completeness:**
- 30+ potential conflict points identified and resolved
- Naming conventions for every context (DB, API, Python, Vue, TS, CSS)
- Communication patterns (Django signals, WebSocket messages, Celery tasks, Pinia stores, presence)
- Process patterns (error handling, loading states, validation strategy, optimistic locking)

### Gap Analysis Results

**Critical Gaps: NONE**

**Important Gaps (non-blocking, to be addressed in implementation stories):**

1. **ChangePoint Data Migration** — Migration commands placeholder defined in `apps/core/management/commands/`. Detailed field mapping will be specified in the dedicated migration epic/story.

2. **Consortium Excel Import Template** — Standardized format (FR64b) to be designed. Location defined at `docs/consortium-import-template.xlsx`. Will be specified in the consortium implementation story.

3. **Invoice PDF Templates** — ReportLab in stack, `templates/pdf/` structure defined. The 10+ client-specific formats will be implemented iteratively as part of the billing epic.

4. **UX Spec TailwindCSS Version** — UX spec references TailwindCSS 3.x. Architecture uses 4.x — UX concepts remain valid, only CSS configuration syntax changes (v4 uses `@theme` instead of `tailwind.config.js`).

**Nice-to-Have Gaps (post-MVP):**
- Feature flags for progressive rollout
- Business metrics monitoring (Grafana dashboards beyond Sentry)
- Interactive API documentation (Swagger UI via drf-spectacular — already in stack)
- Storybook for design system documentation

### Architecture Completeness Checklist

**✅ Requirements Analysis**
- [x] Project context thoroughly analyzed (99+ FRs, 32 NFRs, 10 cross-cutting concerns)
- [x] Scale and complexity assessed (enterprise, 400+ users, 14 Django apps, 12 Vue features)
- [x] Technical constraints identified (imposed stack, SSO Entra ID, dual legal entities)
- [x] Cross-cutting concerns mapped (RBAC, audit, multi-tenancy, real-time, financial layer, notifications, locking, presence)

**✅ Architectural Decisions**
- [x] Critical decisions documented with versions (Django 6.0.3, PostgreSQL 16, Redis 7, Vue 3.5.30, TailwindCSS 4.2.1)
- [x] Technology stack fully specified (all libraries named with rationale)
- [x] Integration patterns defined (SSO, Intact export, ChangePoint migration, M365 email, HRIS)
- [x] Performance considerations addressed (caching, pagination, async, WebSocket)
- [x] Optimistic locking and presence documented (NFR31-32)

**✅ Implementation Patterns**
- [x] Naming conventions established (DB, API, Python, Vue, TS, CSS — with examples)
- [x] Structure patterns defined (backend apps, frontend features, shared components)
- [x] Communication patterns specified (signals, WebSocket, Celery, Pinia, mitt events, presence)
- [x] Process patterns documented (error handling, loading states, validation, optimistic locking)
- [x] Enforcement guidelines with linting and CI checks

**✅ Project Structure**
- [x] Complete directory structure defined (~150+ files across backend, frontend, infra)
- [x] Component boundaries established (API, frontend, data, service)
- [x] Integration points mapped (6 external, internal data flow diagram)
- [x] Requirements to structure mapping complete (99+ FRs → specific files/directories)

### Architecture Readiness Assessment

**Overall Status:** READY FOR IMPLEMENTATION

**Confidence Level:** HIGH

**Key Strengths:**
- Proven, cohesive technology stack (Django 6 + Vue 3 mature ecosystem)
- Django 6.0 Background Tasks reduces Celery dependency for simple cases
- Detailed consistency patterns that prevent AI agent conflicts
- Explicit FR → file mapping — every requirement has a clear "home"
- RLS multi-tenancy architecture enables future SaaS without refactoring
- Clear separation of concerns (views → serializers → services → models)
- Optimistic locking and presence integrated from design phase (NFR31-32)
- 14 functional domains fully covered (vs 11 in previous architecture)
- Consortium model validated against real operational data

**Areas for Future Enhancement (Post-MVP):**
- Feature flags for progressive deployment
- Business metrics monitoring (Grafana)
- Multi-currency with dynamic exchange rates
- Bidirectional Intact/Sage sync (Phase 1.5)
- Mobile app evaluation
- Storybook for design system documentation

### Implementation Handoff

**AI Agent Guidelines:**
- Follow all architectural decisions exactly as documented
- Use implementation patterns consistently across all components
- Respect project structure and boundaries — no ad-hoc directories
- Refer to this document for all architectural questions
- When in doubt, follow the anti-patterns list to avoid common mistakes

**First Implementation Priority:**
1. `cookiecutter gh:cookiecutter/cookiecutter-django` → scaffold backend
2. `npm create vue@latest erp-frontend` → scaffold frontend
3. `docker-compose.yml` → wire all services together
4. Core app (Tenant model, RLS middleware, VersionedModel, OptimisticLockMixin, base permissions)
5. Authentication (django-allauth + Entra ID + JWT)
