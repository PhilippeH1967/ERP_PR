---
stepsCompleted: [1, 2, 3, 4]
status: 'complete'
completedAt: '2026-03-17'
inputDocuments:
  - "_bmad-output/planning-artifacts/prd.md"
  - "_bmad-output/planning-artifacts/architecture.md"
  - "_bmad-output/planning-artifacts/ux-design-specification.md"
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
---

# ERP - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for ERP, decomposing the requirements from the PRD, UX Design, Architecture, and validated mockups into implementable stories.

### Definition of Done (All Stories)

Every story is considered "done" only when ALL of the following are met:

1. **Backend unit tests (pytest):** All acceptance criteria are covered by unit tests in the Django app's `tests/` folder. Minimum 80% coverage on business logic (NFR28). Tests follow co-located pattern: `test_models.py`, `test_views.py`, `test_serializers.py`, `test_services.py`.
2. **Frontend unit tests (Vitest):** All Vue components and Pinia stores created or modified have unit tests in the feature's test files. Composables and utility functions are tested.
3. **API contract tests:** DRF endpoints return standardized response format (`{"data": ...}` / `{"error": {...}}`). Response schemas match drf-spectacular OpenAPI spec.
4. **Optimistic locking verified:** Any story touching financial entities includes tests for version conflict (409) scenarios.
5. **RLS tenant isolation verified:** Any story creating new tenant-scoped models includes a test proving cross-tenant data is invisible.
6. **Audit trail verified:** Any story modifying financial entities includes a test proving django-simple-history records changes with user, date, and reason.
7. **Linting passes:** `ruff` (Python) and `eslint` (TypeScript) report zero errors.
8. **Code review:** Story passes adversarial code review (`/bmad-bmm-code-review`) before marking as done.

## Requirements Inventory

### Functional Requirements

- FR1: [MVP-1] PM can create a new project via a 4-step wizard: Step 1 — Metadata, Step 2 — Budget, Step 3 — Resources & Planning, Step 4 — Subcontractors
- FR1b: [MVP-1] Step 1 includes project start date and end date (previsional)
- FR1c: [MVP-1] Step 1 includes designation of the three project leadership roles: PM, Associé en charge, Invoice Approver
- FR1d: [MVP-1] Step 3 allows PM to assign virtual resource profiles at the phase level (not task level)
- FR1e: [MVP-1] Step 3 includes a simplified Gantt view showing all phases on a quarterly timeline with editable start/end dates per phase
- FR1f: [MVP-1] Step 4 (Subcontractors) is explicitly optional with warning if no ST budget allocated
- FR1g: [MVP-1] After project creation, confirmation screen with invitation to Associé en charge for review
- FR2: [MVP-1] PM can select a project template by contract type that pre-configures phases and support services
- FR3: [MVP-1] PM can define a two-axis project structure with sequential realization phases and transversal support services
- FR4: [MVP-1] PM can position virtual resource profiles on project phases for budget estimation before assigning real employees
- FR5: [MVP-1] PM can replace a virtual profile with one or multiple employees using percentage-based hour distribution
- FR6: [MVP-1] PM can select employees via a 3-tier priority modal: matching profile with availability, similar profiles, all other employees
- FR7: [MVP-1] PM can manage a multi-level WBS hierarchy (phases, tasks, subtasks) with standard internal and client-facing labels
- FR7b: [MVP-1] PM can add, remove, or reorder phases during project creation
- FR8: [MVP-1] PM can track contract value, amendments, and budget consumption per WBS element
- FR9: [MVP-1] PM can manage subcontractors with three budget layers: internal fees, refacturable, and absorbed
- FR10: [MVP-1.5] PM can flag a project as "consortium" and associate it with a consortium entity
- FR11: [MVP-1] Admin or Finance can create and manage internal projects with a lighter task/subtask structure
- FR12: [MVP-1] PM can view a project dashboard showing budget consumed, hours consumed vs planned, team status, and phase completion indicators
- FR13: [MVP-1] BU Director and Finance can track personnel lending between BUs with CA repatriation to home BU
- FR14: [MVP-1] PM can allocate budgets for support services (3D, BIM, DD, Landscape) on projects they manage
- FR15: [MVP-1] Each project has a designated PM and Associé en charge with oversight of financial performance
- FR15b: [MVP-1] At project creation, PM must designate an Invoice Approver (Chargé de contrat) who may differ from the PM
- FR15c: [MVP-1] Each project has a lifecycle status: Active, Completed, On Hold, Cancelled
- FR15d: [MVP-1] PM transfer capability — PM role can be reassigned to another employee mid-project
- FR15e: [MVP-1] Associé en charge change — can be reassigned with proper authorization
- FR15f: [MVP-1] BU Director change — can be reassigned at the BU level
- FR15g: [MVP-1] Complete immutable change history for all leadership role changes with timestamp, old value, new value, and change initiator
- FR15h: [MVP-1] PM or Finance can formally close a project through a checklist-based workflow with final margin calculation
- FR15i: [MVP-1.5] Direction or Finance can reopen a closed project with justification and audit entry
- FR15j: [MVP-1.5] Closed projects are logically archived after a configurable period with restore capability
- FR15k: [MVP-1.5] PM can create and manage contract amendments (avenants) with sequential numbering, approval status, and phase/task impact tracking
- FR15l: [MVP-1.5] Project budget view distinguishes original contract value, cumulative amendments, consumed to date, and remaining
- FR15m: [MVP-2] PM can transfer a project between legal entities or Finance can merge/split projects with full reconciliation
- FR15n: [MVP-1.5] PM can rebaseline a project budget without modifying contractual value for variance reporting
- FR16: [MVP-1] Employee can view and enter time only on projects and tasks where they are assigned
- FR17: [MVP-1] Employee can enter hours per project/phase/task per day in a weekly timesheet view with client-facing labels
- FR18: [MVP-1] Employee can see daily total indicators when different from the norm (7.5h or 8h)
- FR19: [MVP-1] Employee can save timesheet as draft and submit weekly for approval
- FR20: [MVP-1] PM, Finance, or Admin can block a phase or block a specific person on a phase from time entry
- FR21: [MVP-1] PM can approve submitted timesheets as first-level approver
- FR22: [MVP-1] Finance/Direction can approve timesheets as second-level approver
- FR22b: [MVP-1] System enforces anti-self-approval: secondary timesheet approver assigned per project
- FR23: [MVP-1] PM or Finance defines billing mode per task (fixed-price or hourly)
- FR23b: [MVP-1] Mandatory phases "Gestion de projet" and "Qualité" are included in every project template by default
- FR24: [MVP-1] PM can request timesheet modifications on entries not yet fully validated
- FR25: [MVP-1] Finance can modify timesheets that have been fully validated with complete audit trail
- FR26: [MVP-1] System sends automated reminders for incomplete or late timesheets
- FR27: [MVP-1] Employee can manage favorites and quick-switch between multiple projects
- FR27b: [MVP-1.5] System can import employee absences from HRIS via scheduled sync or manual file upload
- FR27c: [MVP-1.5] Finance or Admin can unlock a closed time period for a specific employee with justification and auto re-lock
- FR27d: [MVP-1.5] Finance can perform bulk time corrections with before/after audit trail
- FR27e: [MVP-1] If employee assignment changes after timesheet submission, system flags affected entries for PM review
- FR28: [MVP-1] Finance can define financial phases that group multiple realization phases with distinct billing modes
- FR29: [MVP-1] Finance can set dual hourly rates per project: internal cost rate and contractual client rate
- FR30: [MVP-1] Finance can prepare invoices via a 7-column screen with phase/task hierarchy and billing sections
- FR30b: [MVP-1] Dashboard "Heures sans facturation prévue ce mois" with slide-over project detail
- FR30c: [MVP-1] Provisional invoice numbers (PROV-xxxx) assigned at creation, definitive number assigned at send time
- FR30d: [MVP-1] Project-linked invoices — "Créer facture" from project Budget tab auto-populates all billable phases as invoice lines (Added v1.1.012)
- FR30e: [MVP-1] Free invoices — Simple invoices without project link, manual lines with libre labels (Added v1.1.012)
- FR30f: [MVP-1] Sub-contractor lines — ST invoices (refacturable) automatically included in project invoices with line_type=ST (Added v1.1.012)
- FR30g: [MVP-1] Free lines — Manual lines (Dépense, Autre) can be added at bottom of any invoice (Added v1.1.012)
- FR30h: [MVP-1] Invoiced hours tracking — TimeEntry.is_invoiced marks hours included in a sent invoice, "$" badge on timesheet cells (Added v1.1.012)
- FR30i: [MVP-1] Mark hours invoiced — Action on SENT/PAID invoices marks matching time entries as invoiced (Added v1.1.012)
- FR30j: [MVP-1] Project Budget tab — Phase-level budget editing by ADMIN/FINANCE, KPI cards (Added v1.1.012)
- FR31: [MVP-1] Finance can view visual alerts when hours advancement diverges from billing advancement by more than 10 points
- FR32: [MVP-1] Finance can view a real-time CA/Salary ratio banner comparing to firm target (configurable)
- FR33: [MVP-1] Finance can create invoices using 10+ configurable billing templates per client
- FR33b: [MVP-1] Finance or PM can define per-client custom invoice line labels with WBS element mapping
- FR34: [MVP-1] Finance can assemble billing dossiers with configurable annexes
- FR34b: [MVP-1] Print-ready invoice brouillon with 5 columns, banking references, and complete formatting
- FR35: [MVP-1] PM approves invoices via an accordion-based list with slide-over brouillon preview
- FR36: [MVP-1] Finance can track invoice status through workflow: Draft → Submitted → Approved → Sent → Paid
- FR37: [MVP-1] Finance can record payments received and track outstanding amounts with aging analysis
- FR37b: [MVP-1.5] Finance can manage automated dunning process with configurable escalation levels and templates
- FR38: [MVP-1] Finance can export invoice data to Intact (Sage) in structured format (CSV/Excel)
- FR39: [MVP-1] PM can track non-billable tasks that consume hours but generate no revenue
- FR39b: [MVP-1.5] Finance can issue a credit note (avoir) against a previously sent invoice with sequential numbering
- FR39c: [MVP-1.5] Finance can cancel a sent invoice and reissue a corrected version with full audit trail
- FR39d: [MVP-1] Finance can record partial payments on an invoice with outstanding balance tracking
- FR39e: [MVP-1.5] Finance can write off small outstanding balances below a configurable threshold with justification
- FR39f: [MVP-1] Finance can allocate a single client payment across multiple invoices
- FR39g: [MVP-1] System tracks contractual holdback (retenue) per project as a running balance with release capability
- FR39h: [MVP-1] Each invoice and credit note maintains a complete adjustment history
- FR39i: [MVP-1.5] When client holdback is released, system alerts Finance that corresponding ST holdbacks may be eligible for release
- FR40: [MVP-1] Employee can create expense reports with date, amount, category, project, description, refacturable flag, and tax type
- FR40b: [MVP-1] Mandatory receipt attachment (photo/PDF) for each expense line
- FR40c: [MVP-1] Expense templates/models for recurring expenses
- FR41: [MVP-1] Employee can upload receipt photos/PDFs attached to expense lines
- FR41b: [MVP-1] Slide-over receipt preview via eye icon on each expense line
- FR42: [MVP-1] 4-role expense approval workflow: Employee submits → Designated approver → Finance Analyst → Finance processes payment
- FR42b: [MVP-1] PM must designate expense approvers per project at project creation
- FR42c: [MVP-1] PM can modify the refacturable flag on expense lines during approval
- FR42d: [MVP-1] Finance validates GL accounts, tax breakdown (HT, TPS, TVQ), and can adjust reimbursable amount
- FR42e: [MVP-1] Payment processing and export are separate steps from validation
- FR42f: [MVP-1] Expense reports grouped by Employee → Project → Category in the Finance view
- FR43: [MVP-1] PM or Finance can define per project whether expenses are refundable to client and budget
- FR43b: [MVP-1] Refacturable expenses are included in client invoices as a separate section
- FR44: [MVP-1] Admin can configure expense categories (travel, meals, supplies, etc.)
- FR45: [MVP-1] Finance can generate expense reports by person, project, BU, and period
- FR46: [MVP-1] Finance can export expense reports in Intact API import format
- FR46b: [MVP-1.5] Finance can reverse a previously validated/paid expense with justification
- FR46c: [MVP-1.5] PM or Finance can reject an expense with structured reason and employee notification
- FR47: [MVP-1] 3-role supplier payment workflow: Analyst enters invoice → PM authorizes payment → Analyst validates execution
- FR47b: [MVP-1] PM views supplier invoices grouped by Project → Subcontractor with slide-over detail
- FR47c: [MVP-1] Batch operations for authorizing multiple supplier invoices
- FR48: [MVP-1] After PM authorization, Analyst validates that payment has been executed
- FR49: [MVP-1] Finance can view all authorized-but-unpaid invoices across projects and mark them as paid
- FR50: [MVP-1] Finance can generate cross-project payment reports grouped by supplier
- FR51: [MVP-1] PM can view per-subcontractor cumulative invoices vs planned budget per project
- FR52: [MVP-1.5] Finance can import subcontractor invoices via Intact API
- FR52b: [MVP-1.5] Analyst can register a supplier credit note against a previously recorded invoice
- FR52c: [MVP-1.5] PM or Analyst can flag a ST invoice as contested/in dispute with reason and supporting documents
- FR52d: [MVP-1.5] Analyst can record a partial payment on a ST invoice with remaining balance tracked
- FR52e: [MVP-1.5] PM can manage contractual holdback on ST invoices with release tracking
- FR52f: [MVP-1.5] Each ST invoice supports multiple document attachments and version history
- FR53: [MVP-1.5] Director, Proposal Manager, or Finance can create a service proposal with code, title, client, deadline, budget, task checklist
- FR53b: [MVP-1.5] PM or Director can track competitive positioning on proposals
- FR53c: [MVP-1.5] Team assignment on proposals with estimated hours and visibility-based access
- FR54: [MVP-1.5] Lifecycle management: En cours → Soumise → Gagnée / Perdue / Abandonnée → Convertie
- FR55: [MVP-1.5] Employee can track time on assigned proposals (always non-billable)
- FR56: [MVP-1.5] Convert won proposal to full project with template selection
- FR57: [MVP-1.5] Commercial reporting: conversion rate, average cost per proposal, project acquisition cost
- FR58: [MVP-1.5] Active proposals displayed on PM/Director dashboard with status and deadline countdown
- FR59: [MVP-1.5] Finance can create a consortium entity with name, client, PR role, contract reference, and member coefficients
- FR59b: [MVP-2] Profit-sharing rules: type of clause, measurement modes, trigger threshold, evaluation frequency
- FR59c: [MVP-2] Profit-sharing rules can be defined at consortium level or per project
- FR60: [MVP-1.5] Finance can associate multiple projects to a consortium
- FR61: [MVP-1.5] Dual financial perspective: consortium view and Provencher view
- FR62: [MVP-1.5] System excludes consortium client revenue from Provencher's CA
- FR62b: [MVP-1.5] Subcontractors can invoice consortium directly or via PR
- FR63: [MVP-1.5] BU Director consortium recap dashboard
- FR64: [MVP-1.5] Finance enters partner invoices grouped by Project → Partner
- FR64a: [MVP-1.5] Finance can record basic profit distributions per consortium project
- FR64b: [MVP-2] Import existing consortium data via Excel template with validation
- FR64c: [MVP-2] Profit distribution guided workflow with 5 steps
- FR64c2: [MVP-2] Distribution 2-level approval
- FR64d: [MVP-2] Effort-vs-coefficient alerts with evolution and exportable reports
- FR64e: [MVP-2] Treasury/Cash tab with bank balance, working capital, cash flow, payment capacity
- FR64f: [MVP-1.5] Consortium-to-client invoices following 7-column structure
- FR64g: [MVP-2] Manual treasury adjustments with audit trail
- FR64h: [MVP-1.5] ST consortium tab: register, track, authorize ST invoices to consortium
- FR64i: [MVP-1.5] Per-project financial synthesis with dual KPIs
- FR64j: [MVP-1.5] Budget tab: global budget by phase/task with columns per partner
- FR64k: [MVP-2] Tax declarations at consortium level
- FR64l: [MVP-2] Tax declaration history
- FR64m: [MVP-2] Automated fiscal compliance analysis
- FR65: [MVP-1] User can authenticate via SSO Microsoft Entra ID with automatic user provisioning
- FR66: [MVP-1] Admin can assign roles with granular permissions: 8 distinct roles
- FR67: [MVP-1] System enforces role-based visibility on salary cost data via PostgreSQL RLS
- FR68: [MVP-1] System maintains a complete audit trail on all modifications to critical entities
- FR69: [MVP-1] Any role holder can delegate their tasks and permissions for a defined scope and period
- FR70: [MVP-1] System grants the delegate the delegator's permissions for the delegated scope only
- FR71: [MVP-1] Dept. Assistant can perform clerical project tasks for PMs and invoicing tasks by delegation
- FR72: [MVP-1] Employee can view a personalized home dashboard based on their role
- FR73: [MVP-1] PM can view financial KPIs: carnet de commandes, CA/salary ratio, billing rate, margin
- FR74: [MVP-1] Finance can generate hours reports by project, person, BU, and period
- FR75: [MVP-1] Admin can view system health metrics
- FR76: [MVP-1] Application is fully bilingual French/English with user-selectable language preference
- FR76b: [MVP-1] All user-facing strings are externalized in translation files (Vue I18n)
- FR77: [MVP-1] System renders all dates, numbers, and currency amounts through locale-aware formatters
- FR78: [MVP-1] Admin can configure HR labor rules per jurisdiction
- FR79: [MVP-1] System automatically flags overtime and highlights non-working days in timesheet grid
- FR80: [MVP-1] Admin can configure expense policies per jurisdiction
- FR81: [MVP-1.5] Finance can set invoice currency per client or project with exchange rate management
- FR82: [MVP-1.5] System displays dual currency amounts on financial screens
- FR83: [MVP-1] Admin can configure BUs, position reference list, project templates, invoice formats, and tax settings
- FR84: [MVP-1] Admin can import ChangePoint data: projects, WBS, time entries, and billing history
- FR85: [MVP-1] System validates data migration integrity and generates automated reconciliation reports
- FR85b: [MVP-1] System supports a parallel run period with reconciliation and rollback plan
- FR86: [MVP-1] Admin or Finance can manage clients via a 5-tab interface
- FR86b: [MVP-1] Automatic duplicate detection on client creation
- FR86c: [MVP-1] Each client has a unique alias/acronym, searchable across the application
- FR86d: [MVP-1.5] Client group membership
- FR86e: [MVP-1] Client contacts are selectable when creating projects
- FR87: [MVP-1] System maintains per-client financial history
- FR88: [MVP-1] Client records are linked to projects and invoices
- FR88b: [MVP-1] External Organizations registry shared between ST management, consortium members, and proposal competitors
- FR89: [MVP-1] Centralized notification center with badge count
- FR90: [MVP-1] Dashboard "Actions requises" section with pending items grouped by urgency
- FR91: [MVP-1] Users can configure notification preferences per event type and channel
- FR92: [MVP-1] Admin can broadcast system-wide announcements
- FR93: [MVP-1.5] Bulk imports via standardized templates with validation and dry-run preview
- FR94: [MVP-1.5] Bulk exports with current filters applied
- FR95: [MVP-2] Data retention and archival policies
- FR96: [MVP-2] Data purge with legal retention requirements
- FR97: [MVP-2] All bulk operations logged in dedicated operations journal
- FR98: [MVP-2] Year-end adjustment entries at project or consortium level
- FR99: [MVP-2] Bank reconciliation at consortium level

### NonFunctional Requirements

- NFR1: [MVP-1] All primary screens load in < 2 seconds
- NFR2: [MVP-1] Draft save completes in < 500ms with visual confirmation
- NFR3: [MVP-1] CA/Salary ratio and % advancement recalculate in < 1 second
- NFR4: [MVP-1] Standard reports generate in < 5 seconds
- NFR5: [MVP-1] Project and employee search results appear in < 500ms
- NFR6: [MVP-1] Complete billing dossier generates in < 30 seconds
- NFR7: [MVP-1] SSO via Microsoft Entra ID (OIDC/SAML 2.0) — no local passwords
- NFR8: [MVP-1] All data encrypted in transit (TLS 1.3) and at rest (AES-256)
- NFR9: [MVP-1] Real salary costs accessible only to Finance/Direction via PostgreSQL RLS
- NFR10: [MVP-1] All CUD operations on financial entities logged with user, timestamp, old/new values
- NFR11: [MVP-1] Automatic timeout after 30 min inactivity with concurrent session limit
- NFR12: [MVP-1] All endpoints authenticated via JWT with role-based authorization
- NFR13: [MVP-1] 400+ simultaneous users with < 10% degradation during peak
- NFR14: [MVP-1] 10+ years historical data with no degradation on current-period queries
- NFR15: [MVP-1] Architecture supports 2x user growth (800 users) without redesign
- NFR16: [MVP-1] Time entry tables partitioned by period for query performance at scale
- NFR17: [MVP-1] 99.5% availability during business hours (Mon-Fri 7:00-19:00 ET)
- NFR18: [MVP-1] Automated daily backups with point-in-time recovery (RPO < 1h, RTO < 4h)
- NFR19: [MVP-1] Core operations continue if Intact API or Entra ID temporarily unavailable
- NFR20: [MVP-1] 100% data integrity validation on ChangePoint migration
- NFR21: [MVP-1.5] WCAG 2.1 Level AA compliance
- NFR22: [MVP-1] Full functionality on desktop 1280px+, read-only on tablet 1024px+
- NFR23: [MVP-1] CSV/Excel export generates valid, importable files with zero formatting errors
- NFR24: [MVP-1.5] Bidirectional Intact API sync handles versioning and error recovery
- NFR25: [MVP-1] Entra ID supports auto-provisioning/deprovisioning with group-based role mapping
- NFR26: [MVP-1] Excel imports validate format and content with clear error messages before processing
- NFR27: [MVP-1] Auto-generated OpenAPI 3.0 specification via drf-spectacular
- NFR28: [MVP-1] Minimum 80% test coverage on backend business logic
- NFR29: [MVP-1] Zero-downtime deployment via Docker with rolling updates
- NFR30: [MVP-1] Templates, formats, categories configurable without code changes
- NFR31: [MVP-1] Optimistic locking on all financial entities with conflict warning and options
- NFR32: [MVP-1] Real-time presence indicator on invoice preparation and project budget screens

### Additional Requirements

**From Architecture:**
- Starter template: cookiecutter-django (backend) + npm create vue@latest (frontend) — impacts Epic 1 Story 1
- Django 6.0 with built-in Background Tasks Framework for lightweight async
- Celery retained for heavy tasks (billing dossier, migration, bulk imports)
- PostgreSQL RLS middleware for multi-tenancy (TenantScopedModel base class)
- VersionedModel + OptimisticLockMixin for NFR31 concurrency control
- WebSocket presence tracking via Django Channels for NFR32
- django-simple-history on all financial models for audit trail
- django-rules + custom ProjectRole model for RBAC with 8 roles
- django-allauth with OIDC for Microsoft Entra ID SSO
- JWT (simplejwt) with 15min access + 7-day refresh tokens
- Redis 7 serving 4 roles: app cache, config cache, session store, Celery broker
- OpenAPI codegen for TypeScript API client from drf-spectacular
- Uvicorn as ASGI server (Django Channels support)
- GitHub Actions CI/CD pipeline
- Sentry + structlog for monitoring and logging
- On-premise Docker deployment with Nginx reverse proxy

**From UX Design:**
- Role-adaptive landing pages (Employee → timesheet, PM → dashboard, Finance → billing)
- Design system: TailwindCSS 4 + Headless UI + TanStack Table + Chart.js
- Dark mode support from Day 1
- System font stack (no custom web fonts), monospace for financial amounts
- Two-Minute Rule: any routine task completes in under 2 minutes
- Slide-over panels for project detail (not full-page navigation)
- Command palette (Cmd+K) for power users
- Role-based color coding: Employee (blue), PM (amber), Finance (green), Director (purple), Admin (gray)
- VeeValidate + Zod for form validation
- Keyboard-first interaction patterns (Tab navigation in timesheet grid)

**From Validated Mockups:**
- 10 validated HTML mockups define screen-level UX for all major modules
- Flow bar with role badges and step progression across all workflow screens
- KPI dashboard pattern: 3-5 column grid with numeric value + label + trend
- 7-column invoice editor with editable cells (yellow background #FFFBEB)
- Expense 4-role workflow with status progression bar
- Consortium dual-view with effort reconciliation tables
- Client 5-tab interface with financial summary and aging analysis
- Proposal pipeline with checklist progress indicators
- Delegation card layout with active/inactive states
- Admin role matrix with visibility rules

### FR Coverage Map

- FR1, FR1b, FR1c, FR1d, FR1e, FR1f, FR1g: Epic 3 — Project Creation Wizard
- FR2: Epic 3 — Project Templates
- FR3: Epic 3 — Two-Axis Project Structure
- FR4: Epic 3 — Virtual Resource Profiles
- FR5: Epic 3 — Virtual-to-Real Assignment
- FR6: Epic 3 — 3-Tier Employee Selection
- FR7, FR7b: Epic 3 — WBS Hierarchy & Dual Labels
- FR8: Epic 3 — Contract & Budget Tracking
- FR9: Epic 3 — Subcontractor Budget Layers
- FR10: Epic 12 — Consortium Project Flag
- FR11: Epic 3 — Internal Projects
- FR12: Epic 3 — Project Dashboard
- FR13: Epic 3 — Personnel Lending
- FR14: Epic 3 — Support Service Budgets
- FR15, FR15b: Epic 3 — Project Leadership Roles
- FR15c: Epic 3 — Project Lifecycle Status
- FR15d, FR15e, FR15f: Epic 3 — Leadership Role Transfer
- FR15g: Epic 3 — Immutable Change History
- FR15h: Epic 3 — Project Closing Checklist
- FR15i: Epic 12 — Project Reopening
- FR15j: Epic 12 — Project Archival
- FR15k, FR15l: Epic 12 — Contract Amendments
- FR15m: Epic 18 — Project Transfer Between Entities
- FR15n: Epic 12 — Budget Rebaseline
- FR16: Epic 4 — Authorization-Based Visibility
- FR17: Epic 4 — Weekly Time Entry with Client Labels
- FR18: Epic 4 — Daily Total Indicators
- FR19: Epic 4 — Draft & Submit
- FR20: Epic 4 — Phase/Person Blocking
- FR21: Epic 4 — PM First-Level Approval
- FR22: Epic 4 — Finance Second-Level Approval
- FR22b: Epic 4 — Anti-Self-Approval
- FR23, FR23b: Epic 3 — Billing Mode & Mandatory Phases
- FR24: Epic 4 — Timesheet Modification Request
- FR25: Epic 4 — Finance Validated Timesheet Correction
- FR26: Epic 4 — Automated Reminders
- FR27: Epic 4 — Favorites & Quick-Switch
- FR27b: Epic 17 — HRIS Absence Import
- FR27c: Epic 17 — Period Unlock
- FR27d: Epic 17 — Bulk Time Corrections
- FR27e: Epic 4 — Assignment Change Flagging
- FR28: Epic 5 — Financial Phases
- FR29: Epic 5 — Dual Hourly Rates
- FR30, FR30b, FR30c: Epic 5 — 7-Column Invoice Preparation
- FR31: Epic 5 — Hours vs Billing Alerts
- FR32: Epic 5 — CA/Salary Ratio Banner
- FR33, FR33b: Epic 5 — Invoice Templates & Client Labels
- FR34, FR34b: Epic 5 — Billing Dossiers
- FR35: Epic 5 — Invoice Approval Workflow
- FR36: Epic 5 — Invoice Status Tracking
- FR37: Epic 5 — Payment Recording & Aging
- FR37b: Epic 14 — Automated Dunning
- FR38: Epic 5 — Intact Export
- FR39: Epic 5 — Non-Billable Task Tracking
- FR39b: Epic 14 — Credit Notes
- FR39c: Epic 14 — Invoice Cancellation/Reissue
- FR39d: Epic 5 — Partial Payments
- FR39e: Epic 14 — Write-Offs
- FR39f: Epic 5 — Multi-Invoice Payment Allocation
- FR39g: Epic 5 — Holdback Tracking
- FR39h: Epic 5 — Adjustment History
- FR39i: Epic 14 — Cross-Linked Holdback Alerts
- FR40, FR40b, FR40c: Epic 6 — Expense Entry
- FR41, FR41b: Epic 6 — Receipt Management
- FR42, FR42b, FR42c, FR42d, FR42e, FR42f: Epic 6 — 4-Role Approval Workflow
- FR43, FR43b: Epic 6 — Refacturable Expense Config
- FR44: Epic 6 — Expense Categories
- FR45: Epic 6 — Expense Reporting
- FR46: Epic 6 — Intact Export
- FR46b: Epic 17 — Expense Reversal
- FR46c: Epic 17 — Expense Rejection Workflow
- FR47, FR47b, FR47c: Epic 7 — ST Invoice Entry & Authorization
- FR48: Epic 7 — Payment Execution Validation
- FR49: Epic 7 — Cross-Project Payment View
- FR50: Epic 7 — Cross-Project Payment Reports
- FR51: Epic 7 — ST Budget vs Actual
- FR52: Epic 15 — ST Intact Import
- FR52b: Epic 15 — ST Credit Notes
- FR52c: Epic 15 — ST Disputes
- FR52d: Epic 15 — ST Partial Payments
- FR52e: Epic 15 — ST Holdbacks
- FR52f: Epic 15 — ST Document Attachments
- FR53, FR53b, FR53c: Epic 13 — Proposal Creation & Team
- FR54: Epic 13 — Proposal Lifecycle
- FR55: Epic 13 — Proposal Time Tracking
- FR56: Epic 13 — Proposal-to-Project Conversion
- FR57: Epic 13 — Commercial Reporting
- FR58: Epic 13 — Dashboard Integration
- FR59: Epic 16 — Consortium Entity Creation
- FR59b, FR59c: Epic 18 — Advanced Profit-Sharing Rules
- FR60: Epic 16 — Multi-Project Association
- FR61: Epic 16 — Dual Financial Perspective
- FR62, FR62b: Epic 16 — CA Exclusion Rule & ST Distinction
- FR63: Epic 16 — BU Director Dashboard
- FR64: Epic 16 — Partner Invoices
- FR64a: Epic 16 — Basic Profit Distributions
- FR64b: Epic 18 — Consortium Excel Import
- FR64c, FR64c2: Epic 18 — Guided Profit Distribution
- FR64d: Epic 18 — Effort-vs-Coefficient Alerts
- FR64e: Epic 18 — Treasury/Cash Management
- FR64f: Epic 16 — Consortium Client Invoicing
- FR64g: Epic 18 — Treasury Adjustments
- FR64h: Epic 16 — ST Consortium Tab
- FR64i: Epic 16 — Per-Project Financial Synthesis
- FR64j: Epic 16 — Budget Tab by Partner
- FR64k, FR64l: Epic 18 — Tax Declarations
- FR64m: Epic 18 — Fiscal Compliance Analysis
- FR65: Epic 1 — SSO Authentication
- FR66: Epic 1 — Role Assignment (8 Roles)
- FR67: Epic 1 — RLS Salary Visibility
- FR68: Epic 1 — Audit Trail
- FR69: Epic 9 — Delegation Creation
- FR70: Epic 9 — Delegated Permissions
- FR71: Epic 9 — Dept. Assistant Delegation
- FR72: Epic 8 — Role-Based Dashboard
- FR73: Epic 8 — PM Financial KPIs
- FR74: Epic 8 — Hours Reports
- FR75: Epic 8 — System Health Metrics
- FR76, FR76b: Epic 1 — Bilingual FR/EN
- FR77: Epic 1 — Locale-Aware Formatters
- FR78: Epic 10 — HR Labor Rules
- FR79: Epic 10 — Overtime Flagging
- FR80: Epic 10 — Expense Policies per Jurisdiction
- FR81: Epic 17 — Invoice Currency per Client
- FR82: Epic 17 — Dual Currency Display
- FR83: Epic 10 — Admin Configuration (BUs, Positions, Templates, Formats, Tax)
- FR84: Epic 11 — ChangePoint Import
- FR85, FR85b: Epic 11 — Migration Validation & Parallel Run
- FR86, FR86b, FR86c, FR86e: Epic 2 — Client Management
- FR86d: Epic 17 — Client Groups
- FR87: Epic 2 — Client Financial History
- FR88: Epic 2 — Client-Project Linking
- FR88b: Epic 2 — External Organizations Registry
- FR89: Epic 8 — Notification Center
- FR90: Epic 8 — Actions Requises
- FR91: Epic 8 — Notification Preferences
- FR92: Epic 8 — System Announcements
- FR93: Epic 17 — Bulk Imports
- FR94: Epic 17 — Bulk Exports
- FR95: Epic 18 — Data Retention & Archival
- FR96: Epic 18 — Data Purge
- FR97: Epic 18 — Operations Journal
- FR98: Epic 18 — Year-End Adjustments
- FR99: Epic 18 — Bank Reconciliation

## Epic List

### Epic 1: Foundation & Platform Setup — DONE (Updated v1.1.012)
Developers and admins can start: project scaffolding, SSO authentication, RBAC with 8 roles, multi-tenancy RLS, audit trail, bilingual support, Docker infrastructure, optimistic locking framework, real-time presence framework.
**FRs covered:** FR65, FR66, FR67, FR68, FR76, FR76b, FR77

### Epic 2: Client & Organization Management — DONE (Updated v1.1.012)
Finance and Admin can manage the client database via a 5-tab interface with duplicate detection, contacts, financial history, and the shared External Organizations registry used across modules.
**FRs covered:** FR86, FR86b, FR86c, FR86e, FR87, FR88, FR88b

### Epic 3: Project Creation & Management — DONE (Updated v1.1.012)
PMs can create projects via the 4-step wizard, manage WBS with dual labels, position virtual resource profiles, assign real employees, manage subcontractor budgets, track project health on dashboard, and close projects.
**FRs covered:** FR1-FR1g, FR2, FR3, FR4, FR5, FR6, FR7, FR7b, FR8, FR9, FR11, FR12, FR13, FR14, FR15, FR15b, FR15c, FR15d, FR15e, FR15f, FR15g, FR15h, FR23, FR23b

### Epic 4: Time Tracking & Approval — DONE (Updated v1.1.012)
Employees enter time on assigned projects in a weekly grid, PMs approve as first level, Finance as second level. Phase/person blocking, anti-self-approval, automated reminders, favorites. Extended with PAIE role, 11 payroll controls, period freeze/unlock, and phase-level locking.
**FRs covered:** FR16, FR17, FR18, FR19, FR20, FR21, FR22, FR22b, FR24, FR25, FR26, FR27, FR27e

### Epic 5: Invoicing & Financial Layer — DONE (Updated v1.1.012)
Finance defines financial phases, sets dual rates, prepares invoices via the 7-column screen with CA/Salary ratio, manages payments (partial + multi-allocation), tracks holdbacks, assembles billing dossiers, and exports to Intact. Extended with RBAC billing permissions, print preview, project-linked invoices, free invoices, ST refacturable lines, invoiced hours tracking, and project Budget tab.
**FRs covered:** FR28, FR29, FR30, FR30b, FR30c, FR30d, FR30e, FR30f, FR30g, FR30h, FR30i, FR30j, FR31, FR32, FR33, FR33b, FR34, FR34b, FR35, FR36, FR37, FR38, FR39, FR39d, FR39f, FR39g, FR39h

### Epic 6: Expense Management
Employees create expense reports with receipts, 4-role approval workflow (Employee → Approver → Finance Analyst → Finance Payment), refacturable tracking, categories configuration, reporting, and Intact export.
**FRs covered:** FR40, FR40b, FR40c, FR41, FR41b, FR42, FR42b, FR42c, FR42d, FR42e, FR42f, FR43, FR43b, FR44, FR45, FR46

### Epic 7: Supplier Payment Tracking
Finance manages the 3-state ST invoice lifecycle (Received → Authorized → Paid), PM authorization workflow, batch operations, cross-project payment reporting, budget vs actual tracking per subcontractor.
**FRs covered:** FR47, FR47b, FR47c, FR48, FR49, FR50, FR51

### Epic 8: Dashboards, Notifications & Actions
Each role sees a personalized dashboard with relevant KPIs, centralized notification center with badge count, "Actions requises" section, configurable notification preferences, and system announcements.
**FRs covered:** FR72, FR73, FR74, FR75, FR89, FR90, FR91, FR92

### Epic 9: Delegation & Access
Users can delegate responsibilities with defined scope and period, delegate sees banner and acts within permissions, all actions logged with delegation context, Dept. Assistant delegation for PMs and Finance.
**FRs covered:** FR69, FR70, FR71

### Epic 10: Configuration & Regional Settings — DONE (Updated v1.1.012)
Admin configures HR labor rules per jurisdiction, overtime thresholds, expense policies, BUs, position profiles, project templates, invoice formats, tax settings, and user management — all without code changes.
**FRs covered:** FR78, FR79, FR80, FR83

### Epic 11: ChangePoint Data Migration
Admin imports 10+ years of historical data from ChangePoint (projects, WBS, time entries, billing history), validates integrity with automated reconciliation, executes parallel run period with rollback plan.
**FRs covered:** FR84, FR85, FR85b

### Epic 12: Project Lifecycle Extended (MVP-1.5)
PMs manage full project lifecycle: contract amendments with 3-level budget tracking, budget rebaseline for variance reporting, project reopening with justification, archival with restore, consortium project flagging.
**FRs covered:** FR10, FR15i, FR15j, FR15k, FR15l, FR15n

### Epic 13: Service Proposals (MVP-1.5)
Directors manage the BD pipeline: create proposals with checklist, assign teams, track competitive positioning, manage lifecycle (En cours → Soumise → Gagnée/Perdue), track non-billable time, convert to project, commercial KPIs.
**FRs covered:** FR53, FR53b, FR53c, FR54, FR55, FR56, FR57, FR58

### Epic 14: Billing Extended (MVP-1.5)
Finance handles complex billing scenarios: credit notes, invoice cancellation/reissue, automated dunning with escalation, write-offs for small balances, cross-linked holdback alerts (client → ST).
**FRs covered:** FR37b, FR39b, FR39c, FR39e, FR39i

### Epic 15: Supplier Extended (MVP-1.5)
Finance handles advanced ST scenarios: credit notes, dispute management with history, partial payments, contractual holdbacks with release, Intact API import, multi-document attachments.
**FRs covered:** FR52, FR52b, FR52c, FR52d, FR52e, FR52f

### Epic 16: Consortium Management (MVP-1.5)
Finance creates and manages consortiums: entity with member coefficients, dual financial view (consortium vs Provencher), partner invoicing, basic profit distributions, consortium client invoicing, ST consortium tab, per-project synthesis, budget by partner.
**FRs covered:** FR59, FR60, FR61, FR62, FR62b, FR63, FR64, FR64a, FR64f, FR64h, FR64i, FR64j

### Epic 17: Multi-Currency, Data Operations & Extended Features (MVP-1.5)
Finance works with multi-currency invoicing, Admin performs bulk imports/exports, Finance manages time corrections (period unlock, bulk corrections, HRIS import), expense reversal/rejection, client groups.
**FRs covered:** FR27b, FR27c, FR27d, FR46b, FR46c, FR81, FR82, FR86d, FR93, FR94

### Epic 18: Strategic Intelligence & Advanced Features (MVP-2)
Advanced consortium features (guided profit distribution, treasury, tax declarations, fiscal compliance), data retention/archival/purge, year-end adjustments, bank reconciliation, project entity transfers.
**FRs covered:** FR15m, FR59b, FR59c, FR64b, FR64c, FR64c2, FR64d, FR64e, FR64g, FR64k, FR64l, FR64m, FR95, FR96, FR97, FR98, FR99

---

## Epic 1: Foundation & Platform Setup — DONE (Updated v1.1.012)

Developers and admins can start: project scaffolding, SSO authentication, RBAC with 8 roles, multi-tenancy RLS, audit trail, bilingual support, Docker infrastructure.

### Story 1.1: Project Scaffolding & Docker Infrastructure — DONE

As a **developer**,
I want a fully scaffolded Django 6 + Vue 3 project with Docker Compose running all services,
So that I can start building features on a production-ready foundation.

**Acceptance Criteria:**

**Given** a fresh development environment
**When** I run `docker-compose up`
**Then** Django (Uvicorn), Vue dev server (Vite), PostgreSQL 16, Redis 7, Celery worker, and Celery Beat all start successfully
**And** Django serves the API at `localhost:8000/api/v1/`
**And** Vue dev server serves at `localhost:5173` with HMR
**And** The project follows the architecture directory structure exactly (backend/apps/, frontend/src/features/)
**And** ruff (Python) and eslint (TypeScript) are configured and passing
**And** pytest and vitest run with 0 tests passing (empty test suites)

### Story 1.2: Core Models, Multi-Tenancy & Audit Trail — DONE

As a **developer**,
I want the core infrastructure models (Tenant, TenantScopedModel, VersionedModel, AuditMixin) and PostgreSQL RLS middleware,
So that all future models inherit multi-tenancy isolation, optimistic locking, and audit capabilities.

**Acceptance Criteria:**

**Given** the Django project from Story 1.1
**When** I create a model inheriting from TenantScopedModel
**Then** the model automatically includes `tenant_id` FK and is filtered by RLS policies
**And** the TenantMiddleware reads `tenant_id` from JWT claims and sets the PostgreSQL session variable
**And** VersionedModel provides a `version` integer field with auto-increment on save
**And** AuditMixin integrates django-simple-history with `history_user`, `history_date`, `history_change_reason`
**And** OptimisticLockMixin returns 409 Conflict when version mismatch on update
**And** RLS policies are created via `python manage.py setup_rls`
**And** Unit tests verify tenant isolation (user A cannot see user B's data)

### Story 1.3: SSO Authentication & JWT — DONE

As an **employee**,
I want to log in via my corporate Microsoft account (SSO),
So that I don't need separate credentials and my access is managed centrally.

**Acceptance Criteria:**

**Given** Microsoft Entra ID is configured as OIDC provider
**When** I click "Se connecter" on the login page
**Then** I am redirected to Microsoft login, authenticated, and redirected back with a valid session
**And** The system provisions my user account automatically on first login (django-allauth)
**And** A JWT access token (15min TTL) and refresh token (7 days) are issued
**And** The access token contains `user_id`, `tenant_id`, `email`, `roles[]`
**And** The Vue frontend stores tokens in httpOnly cookies
**And** The Axios interceptor automatically refreshes expired access tokens
**And** If Entra ID is temporarily unavailable, a graceful error message is shown (NFR19)

### Story 1.4: RBAC Framework & Role Assignment — DONE

As an **admin**,
I want to assign one of 8 roles to users with per-project granularity,
So that each user sees only what their role permits.

**Acceptance Criteria:**

**Given** an authenticated admin user
**When** I assign role "PM" to user "Jean-François" on project "Complexe Desjardins"
**Then** the ProjectRole record `(user=JF, project=CD, role=PM)` is created
**And** django-rules predicates (`is_project_pm`, `is_finance`, `can_approve_invoice`) resolve correctly
**And** DRF permission classes deny access when role is insufficient (403 Forbidden)
**And** The 8 roles are available: EMPLOYEE, PM, PROJECT_DIRECTOR, BU_DIRECTOR, FINANCE, DEPT_ASSISTANT, PROPOSAL_MANAGER, ADMIN
**And** Real salary cost fields are hidden via RLS for users without Finance/Direction/Project Director role (FR67)
**And** The `usePermissions` Vue composable exposes role checks to frontend components
**And** Anti-self-approval predicate is available for future use (FR22b)

### Story 1.5: Bilingual Support & Locale-Aware Formatting — DONE

As an **employee**,
I want to use the application in French or English with properly formatted dates and numbers,
So that I can work in my preferred language.

**Acceptance Criteria:**

**Given** an authenticated user with language preference "fr"
**When** I navigate any screen
**Then** all UI labels, buttons, and messages display in French
**And** I can switch language via user preferences and the change takes effect immediately
**And** All dates render as YYYY-MM-DD (Quebec standard) with locale-aware formatters
**And** All currency amounts render with proper separators ($10,200.50 for EN, 10 200,50 $ for FR)
**And** All monetary amounts in API responses are `string` type (not float)
**And** Vue I18n is configured with externalized translation files (no hardcoded text — FR76b)
**And** The frontend uses system font stack with monospace for financial amounts

### Story 1.6: Frontend Shell & Design System Foundation — DONE

As a **user**,
I want a consistent application shell with sidebar navigation, top bar, and role-based landing page,
So that I can navigate the application efficiently.

**Acceptance Criteria:**

**Given** an authenticated user
**When** I log in
**Then** I see MainLayout with collapsible sidebar, top bar (search, notifications bell, user menu)
**And** The sidebar shows navigation items filtered by my role permissions
**And** I land on my role-adaptive default page (Employee → /timesheets, PM → /dashboard, Finance → /billing)
**And** TailwindCSS 4 design tokens are configured (colors, typography, spacing per UX spec)
**And** Headless UI components (Modal, SlideOver, Tabs, Combobox) are available in shared/components/
**And** Dark mode toggle works via Tailwind `dark:` prefix
**And** The DRF API returns standardized responses: `{"data": ...}` for success, `{"error": {...}}` for errors
**And** Axios interceptor handles 401 (refresh), 403 (redirect), 409 (conflict dialog), 500 (Sentry + toast)

## Epic 2: Client & Organization Management — DONE (Updated v1.1.012)

Finance and Admin can manage the client database via a 5-tab interface with duplicate detection, contacts, financial history, and the shared External Organizations registry.

### Story 2.1: Client CRUD & 5-Tab Interface — DONE

As a **Finance user**,
I want to create and manage clients via a 5-tab interface,
So that all client information is centralized and structured.

**Acceptance Criteria:**

**Given** an authenticated Finance or Admin user
**When** I create a new client
**Then** I can fill the Identification tab: name, legal entity, alias/acronym, sector
**And** the Contacts tab allows adding multiple contacts with name, role, email, phone, language preference
**And** the Addresses tab supports multiple addresses including billing addresses
**And** the Billing Parameters tab captures payment terms, tax settings, default invoice template
**And** the CRM tab stores Associé en charge, notes, relationship history
**And** the client is persisted with `tenant_id` and full audit trail
**And** the client list view shows all clients with search, filter by sector/entity, and pagination

### Story 2.2: Client Duplicate Detection & Alias Search — DONE

As a **Finance user**,
I want the system to detect potential duplicate clients on creation and search clients by alias,
So that the client registry stays clean and findable.

**Acceptance Criteria:**

**Given** I am creating a new client with name "Ville de Montréal"
**When** a client "Ville de Montreal" (without accent) already exists
**Then** the system shows a warning: "Possible duplicate found: Ville de Montreal"
**And** I can choose to merge, view existing, or proceed with creation
**And** duplicate detection uses name similarity and alias matching (FR86b)
**And** each client has a unique alias/acronym searchable across the application (FR86c)
**And** the global search includes client aliases in results

### Story 2.3: Client Financial History & Project Linking — DONE

As a **Finance user**,
I want to see per-client financial history and linked projects,
So that I can assess client health and relationship value.

**Acceptance Criteria:**

**Given** a client with active and past projects
**When** I view the client detail page
**Then** I see total CA generated, invoices outstanding, payment history, and linked projects (FR87)
**And** the projects list shows project code, name, PM, status with links to project detail
**And** creating a project auto-links the selected client (FR88)
**And** client contacts are selectable when creating projects (FR86e)
**And** aging analysis shows outstanding invoices grouped by 0-30j, 31-60j, 61-90j, 90+j

### Story 2.4: External Organizations Registry

As a **Finance user**,
I want a shared registry of external organizations,
So that the same firm doesn't get entered multiple times across modules.

**Acceptance Criteria:**

**Given** I need to add a subcontractor to a project
**When** I search the External Organizations registry
**Then** I find the existing entry or create a new one
**And** each organization has: name, NEQ, address, contacts, banking info, and type tags
**And** the same organization can be tagged as ST on one project and Partner on another (FR88b)
**And** deduplication check runs on creation (name + NEQ matching)
**And** the registry is used by: ST management, consortium member selection, and proposal competitor tracking

## Epic 3: Project Creation & Management — DONE (Updated v1.1.012)

PMs can create projects via the 4-step wizard, manage WBS with dual labels, position virtual resource profiles, assign real employees, manage subcontractor budgets, track project health, and close projects.

### Story 3.1: Project Model & Template System — DONE

As a **PM**,
I want to select a project template by contract type,
So that I don't start from a blank page every time.

**Acceptance Criteria:**

**Given** an authenticated PM
**When** I start creating a new project
**Then** I can select from templates organized by contract type (forfaitaire, consortium, co-développement, conception-construction)
**And** the template pre-configures sequential realization phases and transversal support services (FR2, FR3)
**And** mandatory phases "Gestion de projet" and "Qualité" are included by default (FR23b)
**And** the Project model includes: code, name, client FK, BU, entity, contract type, start/end dates, lifecycle status (FR15c)
**And** templates are configurable by Admin without code changes

### Story 3.2: Project Wizard Step 1 — Metadata — DONE

As a **PM**,
I want to enter project identification, dates, and leadership roles in Step 1,
So that the project is properly identified and assigned.

**Acceptance Criteria:**

**Given** I have selected a template
**When** I fill Step 1
**Then** I can enter: project code, name, client, BU, legal entity, contract type (FR1)
**And** I set project start date and end date (FR1b)
**And** I designate PM, Associé en charge, and Invoice Approver (FR1c, FR15, FR15b)
**And** I can define phases with standard and client-facing labels (FR7)
**And** I can add, remove, or reorder phases (FR7b)
**And** I can set billing mode per phase: fixed-price or hourly (FR23)

### Story 3.3: Project Wizard Step 2 — Budget — DONE

As a **PM**,
I want to configure hours and costs per phase/task in Step 2,
So that the project has a clear budget baseline.

**Acceptance Criteria:**

**Given** I have completed Step 1
**When** I fill Step 2
**Then** I can set budgeted hours and cost budgets per phase and task
**And** the system calculates total budget from hours × rate grid
**And** I can track contract value per WBS element (FR8)
**And** the budget summary shows: total honoraires, total ST, total project cost

### Story 3.4: Project Wizard Step 3 — Resources & Planning — DONE

As a **PM**,
I want to position virtual resource profiles on phases and see a Gantt timeline,
So that I can plan capacity before assigning real people.

**Acceptance Criteria:**

**Given** I have completed Step 2
**When** I fill Step 3
**Then** I can assign virtual resource profiles at the phase level (FR1d, FR4)
**And** I see a simplified Gantt view on a quarterly timeline (FR1e)
**And** I can edit start/end dates per phase on the Gantt
**And** I can allocate budgets for support services (FR14)

### Story 3.5: Project Wizard Step 4 — Subcontractors & Confirmation — DONE

As a **PM**,
I want to optionally configure subcontractor budgets and finalize creation,
So that the project is complete with all budget layers.

**Acceptance Criteria:**

**Given** I have completed Step 3
**When** I reach Step 4
**Then** I can configure subcontractors with three budget layers: internal fees, refacturable with markup %, absorbed (FR9)
**And** Step 4 is optional with warning if no ST budget (FR1f)
**And** subcontractors are selected from External Organizations registry
**And** on confirmation, project is created with status "Active"
**And** confirmation screen shows summary with invitation to Associé en charge (FR1g)

### Story 3.6: Virtual-to-Real Resource Assignment — DONE

As a **PM**,
I want to replace virtual profiles with real employees,
So that my team is assigned and can start entering time.

**Acceptance Criteria:**

**Given** a project with virtual profiles
**When** I assign a real employee
**Then** I see a 3-tier priority modal (FR6)
**And** I can assign multiple employees with percentage-based distribution (FR5)
**And** assignment automatically creates timesheet permissions
**And** partial assignment is allowed

### Story 3.7: WBS Management & Dual Labels — DONE

As a **PM**,
I want to manage a multi-level WBS with standard and client-facing labels,
So that internal tracking and client documents use appropriate nomenclature.

**Acceptance Criteria:**

**Given** a created project
**When** I manage the WBS
**Then** I can create phases, tasks, subtasks in hierarchy (FR7)
**And** each element has standard and client-facing labels
**And** client labels display on timesheets, reports, and invoices
**And** I can edit WBS post-creation
**And** budget consumption is trackable per WBS element (FR8)

### Story 3.8: Project Dashboard & Health Indicators

As a **PM**,
I want to see project health indicators for all my projects,
So that I can quickly identify projects needing attention.

**Acceptance Criteria:**

**Given** an authenticated PM with active projects
**When** I view my dashboard
**Then** I see health indicators: green/yellow/red (FR12)
**And** each card shows: budget %, hours vs planned, team status, phase completion
**And** I can click to see detail in a slide-over
**And** dashboard updates in real-time via WebSocket

### Story 3.9: Internal Projects & Personnel Lending

As an **Admin or Finance user**,
I want to create internal projects and track personnel lending,
So that non-client work and inter-BU costs are tracked.

**Acceptance Criteria:**

**Given** an authenticated Admin or Finance user
**When** I create an internal project
**Then** lighter structure, no financial layer (FR11)
**And** personnel lending tracked with CA repatriation to home BU (FR13)
**And** internal projects distinguishable in all lists

### Story 3.10: Project Lifecycle & Leadership Management — DONE

As a **PM or Finance user**,
I want to manage lifecycle status and leadership changes with full history,
So that project governance is maintained.

**Acceptance Criteria:**

**Given** an active project
**When** I change status or leadership
**Then** On Hold blocks time entry and billing (FR15c)
**And** PM, Associé en charge, BU Director can be transferred (FR15d-f)
**And** all changes immutably recorded (FR15g)
**And** project closing via checklist workflow with final margin (FR15h)

## Epic 4: Time Tracking & Approval — DONE (Updated v1.1.012)

Employees enter time on assigned projects, PMs approve first level, Finance second. Blocking, reminders, favorites. Extended with PAIE role, payroll controls, period freeze/unlock, and phase-level locking.

### Story 4.1: Weekly Timesheet Entry Grid — DONE

As an **employee**,
I want to enter hours in a weekly grid showing only my assigned projects,
So that I can complete my timesheet quickly and accurately.

**Acceptance Criteria:**

**Given** an authenticated employee assigned to projects
**When** I open the timesheet
**Then** I see only assigned projects/phases/tasks (FR16)
**And** weekly grid with days as columns, project/phase rows (FR17)
**And** client-facing labels displayed
**And** Tab navigation between cells, auto-save <500ms (NFR2)
**And** daily totals with norm indicators (FR18)

### Story 4.2: Timesheet Draft, Submit & Favorites — DONE

As an **employee**,
I want to save drafts, submit weekly, and use favorites,
So that I can work incrementally.

**Acceptance Criteria:**

**Given** a partially filled timesheet
**When** I submit
**Then** confirmation with under/over warning (FR19)
**And** can recall before PM approval
**And** favorites and quick-switch available (FR27)
**And** assignment change after submission flags entries for PM review (FR27e)

### Story 4.3: Phase & Person Blocking — DONE

As a **PM**,
I want to block phases or specific persons from time entry,
So that I control who enters time where.

**Acceptance Criteria:**

**Given** an active project
**When** I block a phase or person
**Then** blocked items appear grayed with lock icon (FR20)
**And** phase block = no one; person block = only that individual
**And** single-click blocking, immediate WebSocket update

### Story 4.4: Two-Level Timesheet Approval — DONE

As a **PM**,
I want to approve submitted timesheets as first-level approver,
So that project hours are validated.

**Acceptance Criteria:**

**Given** submitted timesheets
**When** I approve
**Then** pending queue grouped by employee (FR21)
**And** approve or request modifications (FR24)
**And** bulk approval available
**And** anti-self-approval enforced (FR22b)

### Story 4.5: Finance Second-Level Approval & Corrections — DONE

As a **Finance user**,
I want second-level approval and correction capabilities,
So that time data is accurate for billing.

**Acceptance Criteria:**

**Given** PM-approved timesheets
**When** I review
**Then** second-level approval (FR22)
**And** can modify validated timesheets with audit trail (FR25)

### Story 4.6: Automated Timesheet Reminders

As a **system**,
I want to send reminders for incomplete timesheets,
So that submission rates stay at 100%.

**Acceptance Criteria:**

**Given** configured reminder schedule
**When** deadline approaches
**Then** in-app and email reminders sent (FR26)
**And** configurable frequency
**And** PM dashboard shows missing count

### Story 4.7: Per-Entry PM Approval with Multi-PM Support — DONE (Added v1.1.012)

As a **PM**,
I want to approve individual timesheet entries rather than entire sheets, with multi-PM color coding,
So that each PM approves only their own project entries independently.

**Acceptance Criteria:**

**Given** submitted timesheet entries spanning multiple projects
**When** a PM opens the approval queue
**Then** entries are approvable individually per project/phase (not per sheet)
**And** color coding distinguishes: blue = my projects, green = already approved, gray = other PM's projects
**And** multiple PMs can approve entries on the same employee's timesheet independently
**And** rejection includes comments visible to the employee (banner + project/phase detail)

### Story 4.8: PAIE Role with Payroll Controls Dashboard — DONE (Added v1.1.012)

As a **PAIE user**,
I want a dedicated payroll validation dashboard with automated controls,
So that payroll anomalies are detected before processing.

**Acceptance Criteria:**

**Given** an authenticated PAIE user
**When** I open the PAIE tab in approvals
**Then** I see 11 payroll controls: overtime + sick leave, >10h/day, weekend work, LNT 50h weekly cap, statutory holidays, consecutive days, missing submissions, negative hours, future entries, cross-project daily limit, part-time overflow
**And** I can validate or reject entries with bulk operations
**And** completeness checks flag employees with missing timesheets
**And** PAIE role has dedicated permissions (ADMIN/FINANCE/PAIE) on lock/unlock/freeze operations

### Story 4.9: Period Freeze with Unlock Exceptions — DONE (Added v1.1.012)

As a **Finance or Admin user**,
I want to freeze all time entry before a given date with per-employee unlock exceptions,
So that payroll periods are locked while allowing corrections when needed.

**Acceptance Criteria:**

**Given** a configured period freeze date
**When** PeriodFreeze is activated
**Then** no employee can create or modify time entries before the freeze date
**And** PeriodUnlock exceptions can be granted per employee with justification
**And** only ADMIN, FINANCE, or PAIE roles can freeze/unfreeze periods
**And** all freeze/unlock operations use transaction.atomic for data integrity

### Story 4.10: Phase-Level Locking (TimesheetLock) — DONE (Added v1.1.012)

As a **PM or Finance user**,
I want to lock time entry at the phase/task level,
So that completed phases cannot receive new time entries.

**Acceptance Criteria:**

**Given** a project with completed phases
**When** I lock a phase via TimesheetLock
**Then** no employee can enter time on that phase
**And** lock applies at the task level within the phase
**And** locked phases show visual lock indicator in the timesheet grid
**And** only PM, Finance, or Admin can lock/unlock phases

### Story 4.11 (Deferred MVP-1.5): Daily Validation Max 15h — (Updated v1.1.012)

> Note: Daily validation logic (max 15h per day) is implemented as part of the 11 payroll controls in Story 4.8.

## Epic 5: Invoicing & Financial Layer — DONE (Updated v1.1.012)

Finance defines financial phases, sets dual rates, prepares invoices via 7-column screen, manages payments, holdbacks, and exports to Intact. Extended with RBAC billing permissions, print preview, project-linked invoices, free invoices, ST refacturable lines, invoiced hours tracking, and project Budget tab.

### Story 5.1: Financial Phases & Dual Rate Configuration — DONE

As a **Finance user**,
I want to define financial phases and configure dual rates,
So that billing reflects contractual terms.

**Acceptance Criteria:**

**Given** a project with realization phases
**When** I configure financials
**Then** financial phases group realization phases with billing modes (FR28)
**And** mixed modes per project supported
**And** dual hourly rates: internal cost + contractual client, via manual or Excel import (FR29)

### Story 5.2: 7-Column Invoice Preparation Screen — DONE

As a **Finance user**,
I want to prepare invoices via the 7-column screen,
So that I can make informed billing decisions.

**Acceptance Criteria:**

**Given** a project with financial phases and approved timesheets
**When** I open invoice preparation
**Then** 7 columns: deliverable, contract amount, invoiced to date, % billing, % hours/ST, amount this month (editable), % after billing (FR30)
**And** sections: forfait, horaire, ST, dépenses, retenue, taxes
**And** real-time recalculation <1s (NFR3)
**And** provisional numbers PROV-xxxx, definitive at send (FR30c)
**And** presence indicator (NFR32)

### Story 5.3: CA/Salary Ratio Banner & Visual Alerts

As a **Finance user**,
I want CA/Salary ratio and visual alerts,
So that I spot profitability issues.

**Acceptance Criteria:**

**Given** invoice preparation open
**When** I edit amounts
**Then** double ratio banner: before and after billing vs firm target (FR32)
**And** alerts when hours diverge from billing >10 points (FR31)
**And** yellow badge at >90% advancement
**And** "Heures sans facturation" dashboard with slide-over (FR30b)

### Story 5.4: Invoice Templates & Client Labels

As a **Finance user**,
I want configurable billing templates with client-specific labels,
So that each client receives their preferred format.

**Acceptance Criteria:**

**Given** a project with client
**When** I prepare invoice
**Then** 10+ templates per client (FR33)
**And** WBS maps to client-specific labels (FR33b)
**And** print-ready brouillon with banking references (FR34b)

### Story 5.5: Billing Dossier Assembly

As a **Finance user**,
I want to assemble billing dossiers with annexes,
So that clients receive complete documentation.

**Acceptance Criteria:**

**Given** a prepared invoice
**When** I assemble dossier
**Then** configurable annexes (FR34)
**And** generates in <30s as Celery task (NFR6)
**And** downloadable PDF

### Story 5.6: Invoice Approval Workflow & Status Tracking — DONE

As a **PM**,
I want to approve invoices via accordion list with preview,
So that billing is validated before sending.

**Acceptance Criteria:**

**Given** prepared invoice
**When** submitted for approval
**Then** accordion list with slide-over brouillon (FR35)
**And** workflow: Draft → Submitted → Approved → Sent → Paid (FR36)
**And** optimistic locking prevents concurrent edits

### Story 5.7: Payment Recording, Aging & Holdback Tracking — DONE

As a **Finance user**,
I want to record payments, track aging, and manage holdbacks,
So that receivables are accurately monitored.

**Acceptance Criteria:**

**Given** sent invoices
**When** I record payments
**Then** partial payments with balance tracking (FR39d)
**And** multi-invoice allocation (FR39f)
**And** aging by 0-30/31-60/61-90/90+ (FR37)
**And** holdback running balance with release capability (FR39g)
**And** complete adjustment history (FR39h)

### Story 5.8: Non-Billable Tracking & Intact Export

As a **PM**,
I want non-billable task tracking and Intact export,
So that all costs are visible and accounting syncs.

**Acceptance Criteria:**

**Given** project with billable and non-billable tasks
**When** I view financials
**Then** non-billable tracked for cost visibility (FR39)
**And** Intact export in CSV/Excel (FR38)
**And** valid importable files (NFR23)

### Story 5.9: Billing RBAC Permissions — DONE (Added v1.1.012)

As a **Finance user**,
I want role-based access control on all billing operations,
So that only authorized users can create, approve, send, and record payments on invoices.

**Acceptance Criteria:**

**Given** the invoice workflow (Draft -> Submitted -> Approved -> Sent -> Paid)
**When** a user attempts a billing action
**Then** permissions are enforced per role: Finance can create/edit, PM can approve, Finance can send/record payment
**And** print preview is available to authorized users at the appropriate workflow stages
**And** unauthorized actions return 403 Forbidden

### Story 5.10: Invoice Print Preview — DONE (Added v1.1.012)

As a **Finance or PM user**,
I want a print-ready invoice preview (brouillon),
So that I can review the invoice before sending.

**Acceptance Criteria:**

**Given** an invoice in Submitted or Approved status
**When** I open print preview
**Then** I see a formatted brouillon with 5 columns, banking references, and complete formatting (FR34b)
**And** the preview is accessible via slide-over from the approval accordion list

### Story 5.11: Project-Linked Invoice Creation — DONE (Added v1.1.012)

As a **Finance user**,
I want to create an invoice directly from a project's Budget tab with auto-populated lines,
So that all billable phases are pre-filled as invoice lines with correct amounts from the project budget.

**Acceptance Criteria:**

**Given** a project with defined phases and budgets
**When** I click "Créer facture" from the project Budget tab
**Then** the system creates a new invoice linked to the project
**And** all billable phases are auto-populated as invoice lines with budget amounts from project phases (FR30d)
**And** for HORAIRE phases, only uninvoiced PM_APPROVED hours are included
**And** for FORFAITAIRE phases, the full phase budget is used as the line amount

### Story 5.12: Free Invoices Without Project Reference — DONE (Added v1.1.012)

As a **Finance user**,
I want to create simple invoices without linking to a project,
So that I can bill for miscellaneous services not tied to a specific project.

**Acceptance Criteria:**

**Given** the invoice creation screen
**When** I create a free invoice without selecting a project
**Then** the system allows manual line entry with libre labels (FR30e)
**And** the invoice follows the same workflow (Draft → Submitted → Approved → Sent → Paid)
**And** free lines (Dépense, Autre) can be added at the bottom of any invoice for ad-hoc charges (FR30g)

### Story 5.13: Sub-Contractor Refacturable Lines in Invoices — DONE (Added v1.1.012)

As a **Finance user**,
I want ST invoices marked as refacturable to be automatically included in project invoices,
So that sub-contractor costs are correctly passed through to the client.

**Acceptance Criteria:**

**Given** a project with refacturable ST invoices
**When** I create or view a project-linked invoice
**Then** refacturable ST invoices are automatically included as invoice lines with line_type=ST (FR30f)
**And** ST lines appear in the ST section of the invoice alongside internal fee lines

### Story 5.14: Invoiced Hours Tracking on TimeEntry — DONE (Added v1.1.012)

As a **Finance user**,
I want time entries included in sent invoices to be marked as invoiced,
So that the same hours are never double-billed on subsequent invoices.

**Acceptance Criteria:**

**Given** an invoice in SENT or PAID status
**When** the mark-hours-invoiced action is triggered
**Then** all matching time entries are marked with is_invoiced=True (FR30i)
**And** a "$" badge is displayed on timesheet cells for invoiced entries (FR30h)
**And** for HORAIRE phases, only uninvoiced PM_APPROVED hours are included when creating new invoices
**And** the is_invoiced flag prevents double-billing of the same hours

### Story 5.15: Project Budget Tab with Phase-Level Editing — DONE (Added v1.1.012)

As an **ADMIN or Finance user**,
I want a Budget tab on the project detail page with phase-level budget editing and KPI cards,
So that I can manage project budgets and track invoicing progress at the phase level.

**Acceptance Criteria:**

**Given** a project detail page
**When** I navigate to the Budget tab
**Then** I see KPI cards: total budget, total invoiced, % consumed, remaining budget (FR30j)
**And** each phase row shows budgeted amount, invoiced amount, and remaining
**And** ADMIN and FINANCE roles can edit phase-level budgets
**And** budget changes are tracked in the audit trail
**And** a "Créer facture" button is available to generate project-linked invoices (FR30d)

## Epic 6: Expense Management

Employees submit expense reports with receipts, 4-role approval workflow, export Intact.

### Story 6.1: Expense Report Creation & Receipt Upload

As an **employee**,
I want to create expense reports with receipts,
So that I can submit project expenses for reimbursement.

**Acceptance Criteria:**

**Given** an authenticated employee
**When** I create an expense report
**Then** lines with: date, amount, category, project, description, refacturable flag, tax type (FR40)
**And** mandatory receipt per line (FR40b)
**And** slide-over preview via eye icon (FR41b)
**And** expense templates for recurring types (FR40c)

### Story 6.2: Expense Categories & Project Configuration

As an **Admin**,
I want to configure expense categories and refundability rules,
So that policies are enforced consistently.

**Acceptance Criteria:**

**Given** Admin access
**When** I configure expenses
**Then** categories configurable (FR44)
**And** per-project refundability and budget (FR43)
**And** refacturable expenses flagged for client invoices (FR43b)
**And** PM designates expense approvers per project (FR42b)

### Story 6.3: 4-Role Expense Approval Workflow

As a **designated approver**,
I want to review and approve expenses,
So that project expenses are validated.

**Acceptance Criteria:**

**Given** submitted expense report
**When** workflow begins
**Then** 4 roles: Employee → Approver → Finance Analyst → Finance Payment (FR42)
**And** approver can modify refacturable flag (FR42c)
**And** Finance validates GL/taxes (FR42d)
**And** payment separate from validation (FR42e)

### Story 6.4: Expense Reporting & Intact Export

As a **Finance user**,
I want expense reports and Intact export,
So that I can process efficiently.

**Acceptance Criteria:**

**Given** approved expenses
**When** I view Finance dashboard
**Then** grouped by Employee → Project → Category (FR42f)
**And** reports by person, project, BU, period (FR45)
**And** Intact export (FR46)

## Epic 7: Supplier Payment Tracking

Finance manages ST invoice lifecycle: Received → Authorized → Paid, with cross-project reporting.

### Story 7.1: ST Invoice Entry & PM Authorization

As a **Finance Analyst**,
I want to enter ST invoices and route to PMs,
So that supplier payments follow proper approval.

**Acceptance Criteria:**

**Given** project with subcontractors
**When** I enter ST invoice
**Then** 3-role workflow: Analyst → PM → Analyst (FR47)
**And** PM views grouped by Project → ST with slide-over (FR47b)
**And** batch authorization (FR47c)
**And** cumulative vs budget tracking (FR51)

### Story 7.2: Payment Execution & Validation

As a **Finance Analyst**,
I want to validate payment execution,
So that ST payment status is accurate.

**Acceptance Criteria:**

**Given** PM-authorized invoices
**When** I process payments
**Then** validate execution (FR48)
**And** view all authorized-unpaid across projects (FR49)
**And** 3-state lifecycle enforced

### Story 7.3: Cross-Project Payment Reports

As a **Finance user**,
I want payment reports grouped by supplier,
So that I can optimize payment runs.

**Acceptance Criteria:**

**Given** ST invoices across projects
**When** I generate reports
**Then** cross-project grouped by supplier (FR50)
**And** exportable to Excel/CSV

## Epic 8: Dashboards, Notifications & Actions

Role-based dashboards with KPIs, notification center, "Actions requises".

### Story 8.1: Role-Based Dashboards

As a **user**,
I want a personalized dashboard based on my role,
So that I see what matters most.

**Acceptance Criteria:**

**Given** authenticated user
**When** I land on dashboard
**Then** role-adaptive content (FR72)
**And** KPI cards with trend arrows, real-time via WebSocket
**And** <2s load (NFR1)

### Story 8.2: PM Financial KPIs & Hours Reports

As a **PM**,
I want financial KPIs and hours reports,
So that I monitor profitability.

**Acceptance Criteria:**

**Given** PM with projects
**When** I view KPIs
**Then** carnet de commandes, CA/salary ratio, billing rate, margin (FR73)
**And** hours reports by project/person/BU/period (FR74)
**And** <5s generation (NFR4)

### Story 8.3: System Health & Admin Metrics

As an **Admin**,
I want system health metrics,
So that I monitor performance.

**Acceptance Criteria:**

**Given** Admin access
**When** I view admin dashboard
**Then** response times, error rates, adoption by BU (FR75)

### Story 8.4: Notification Center & Actions Requises

As a **user**,
I want centralized notifications and action items,
So that I never miss pending actions.

**Acceptance Criteria:**

**Given** pending actions
**When** I view dashboard or bell icon
**Then** badge count, aggregated items from all modules (FR89)
**And** "Actions requises" grouped by urgency (FR90)
**And** configurable preferences per event/channel (FR91)
**And** admin announcements (FR92)
**And** real-time via WebSocket

## Epic 9: Delegation & Access

Users delegate responsibilities with defined scope, visual banner, audit trail.

### Story 9.1: Delegation Creation & Scope Management

As a **role holder**,
I want to delegate to a colleague for a defined period,
So that work continues during absence.

**Acceptance Criteria:**

**Given** user with delegatable permissions
**When** I create delegation
**Then** select delegate, define scope (projects/modules), set period (FR69)
**And** delegate notified, delegation audited
**And** multiple simultaneous delegations supported

### Story 9.2: Delegated Actions & Audit Trail

As a **delegate**,
I want to act on behalf of the delegator with clear indicators,
So that I fulfill responsibilities without confusion.

**Acceptance Criteria:**

**Given** active delegation
**When** I log in
**Then** yellow banner with scope and "Exit delegation" button (FR70)
**And** all actions logged "Par délégation de..."
**And** cannot act outside scope

### Story 9.3: Department Assistant Delegation

As a **Dept. Assistant**,
I want to perform clerical and invoicing tasks by delegation,
So that I support my BU efficiently.

**Acceptance Criteria:**

**Given** delegations from PM and Finance
**When** I access the system
**Then** clerical tasks for PMs, invoicing tasks from Finance (FR71)
**And** each delegation has distinct scope
**And** delegation auto-expires, history preserved

## Epic 10: Configuration & Regional Settings — DONE (Updated v1.1.012)

Admin configures regional parameters, categories, templates, formats, tax — all without code. Extended with user management.

### Story 10.1: HR Labor Rules & Overtime Configuration — DONE

As an **Admin**,
I want to configure HR rules per jurisdiction,
So that work rules are enforced regionally.

**Acceptance Criteria:**

**Given** Admin access
**When** I configure HR rules
**Then** per jurisdiction: work week, overtime, holidays, vacation, pay period (FR78)
**And** overtime flagged automatically, holidays highlighted in timesheet (FR79)

### Story 10.2: Expense Policies & Business Configuration — DONE

As an **Admin**,
I want to configure expense policies and business parameters,
So that operational rules are consistent.

**Acceptance Criteria:**

**Given** Admin access
**When** I configure
**Then** expense policies per jurisdiction (FR80)
**And** BUs, positions (31 profiles), templates, invoice formats, tax settings (FR83)
**And** no code changes required (NFR30)

### Story 10.3: User Management — DONE (Added v1.1.012)

As an **Admin**,
I want to manage users, assign roles, and configure BU membership,
So that organizational structure is maintained in the system.

**Acceptance Criteria:**

**Given** Admin access
**When** I manage users
**Then** I can create, edit, deactivate users
**And** assign roles (8 roles) and BU membership
**And** configure position profiles from the 31-profile reference list
**And** user changes are audited

## Epic 11: ChangePoint Data Migration

Import 10+ years historical data, validate integrity, parallel run.

### Story 11.1: ChangePoint Data Import

As an **Admin**,
I want to import ChangePoint data,
So that historical context is available.

**Acceptance Criteria:**

**Given** ChangePoint export files
**When** I run migration
**Then** imports projects, WBS, time entries, billing history (FR84)
**And** async Celery task with progress
**And** idempotent, error logging per record

### Story 11.2: Migration Validation & Reconciliation

As an **Admin**,
I want to validate migration integrity,
So that I certify accuracy before go-live.

**Acceptance Criteria:**

**Given** completed import
**When** I validate
**Then** automated reconciliation reports CP vs ERP per project (FR85)
**And** 100% integrity (NFR20)
**And** exportable report

### Story 11.3: Parallel Run Period

As a **Finance user**,
I want parallel operation during transition,
So that billing accuracy is verified.

**Acceptance Criteria:**

**Given** validated migration
**When** parallel run begins
**Then** timesheets in ERP only, invoices in both (FR85b)
**And** daily reconciliation, Finance sign-off gate
**And** 48h rollback plan

## Epic 12: Project Lifecycle Extended (MVP-1.5)

Amendments, rebaseline, reopening, archival, consortium flag.

### Story 12.1: Contract Amendments (Avenants)

As a **PM**,
I want to create contract amendments,
So that contractual changes are formally tracked.

**Acceptance Criteria:**

**Given** active project
**When** I create amendment
**Then** sequential number, impact on value and phases (FR15k)
**And** approval workflow: Draft → PM → Associate → Active
**And** dashboard shows current value = original + amendments

### Story 12.2: Three-Level Budget View & Rebaseline

As a **PM**,
I want three budget levels and rebaseline capability,
So that I track progress against contractual and operational budgets.

**Acceptance Criteria:**

**Given** project with amendments
**When** I view budget
**Then** original, current contract, consumed, remaining (FR15l)
**And** rebaseline without changing contract (FR15n)
**And** variance reports against any of three levels

### Story 12.3: Project Reopening & Archival

As a **Finance user**,
I want to reopen closed projects and manage archival,
So that exceptions are possible while keeping system clean.

**Acceptance Criteria:**

**Given** closed project
**When** reopened
**Then** justification required, audit entry, notifications (FR15i)
**And** archival after configurable period (FR15j)
**And** archived excluded from active but accessible via filter

### Story 12.4: Consortium Project Flag

As a **PM**,
I want to flag a project as consortium,
So that it links to consortium financial tracking.

**Acceptance Criteria:**

**Given** project
**When** I flag as consortium
**Then** associate with consortium entity (FR10)
**And** visible in consortium module

## Epic 13: Service Proposals (MVP-1.5)

BD pipeline: proposals, time tracking, competitive positioning, conversion to project.

### Story 13.1: Proposal Creation & Team Assignment

As a **Director**,
I want to create proposals with team and checklist,
So that I track BD efforts.

**Acceptance Criteria:**

**Given** authenticated Director/Proposal Manager
**When** I create proposal
**Then** code OFF-YYYY-NNN, client, deadline, budget, checklist, team with hours (FR53, FR53c)

### Story 13.2: Proposal Lifecycle & Pipeline Dashboard

As a **Director**,
I want lifecycle management and pipeline view,
So that I track BD performance.

**Acceptance Criteria:**

**Given** active proposals
**When** I view pipeline
**Then** Kanban + list with KPIs (FR54)
**And** competitive positioning tracking (FR53b)
**And** dashboard with countdown (FR58)

### Story 13.3: Proposal Time Tracking

As an **employee**,
I want to track time on proposals,
So that BD effort is measured.

**Acceptance Criteria:**

**Given** assigned to proposal
**When** I enter time
**Then** appears in timesheet, always non-billable (FR55)

### Story 13.4: Proposal-to-Project Conversion & Reporting

As a **Director**,
I want to convert proposals and view commercial KPIs,
So that BD feeds into execution.

**Acceptance Criteria:**

**Given** won proposal
**When** I convert
**Then** new project code, template selection, client confirmation (FR56)
**And** commercial reporting: conversion rate, cost per proposal (FR57)

## Epic 14: Billing Extended (MVP-1.5)

Credit notes, cancellation, dunning, write-offs, holdback cross-linking.

### Story 14.1: Credit Notes (Avoirs)

As a **Finance user**,
I want to issue credit notes,
So that billing corrections are formal and auditable.

**Acceptance Criteria:**

**Given** sent invoice
**When** I issue credit note
**Then** references original, NC-xxxx numbering, approval workflow (FR39b)
**And** net balance tracked per invoice

### Story 14.2: Invoice Cancellation & Reissue

As a **Finance user**,
I want to cancel and reissue invoices,
So that errors are corrected with traceability.

**Acceptance Criteria:**

**Given** invoice with error
**When** I cancel
**Then** marked "Annulée" with link to replacement (FR39c)
**And** full audit trail

### Story 14.3: Automated Dunning Process

As a **Finance user**,
I want automated dunning for unpaid invoices,
So that collection is systematic.

**Acceptance Criteria:**

**Given** overdue invoices
**When** dunning triggers
**Then** configurable escalation levels and templates (FR37b)
**And** dashboard, batch reminders, suspension capability

### Story 14.4: Write-Offs & Cross-Linked Holdback Alerts

As a **Finance user**,
I want write-offs and holdback release alerts,
So that minor amounts don't clutter and holdbacks are coordinated.

**Acceptance Criteria:**

**Given** small balances or holdback releases
**When** conditions met
**Then** write-off with justification (FR39e)
**And** client holdback release alerts for corresponding ST holdbacks (FR39i)

## Epic 15: Supplier Extended (MVP-1.5)

ST credit notes, disputes, partial payments, holdbacks, Intact import, attachments.

### Story 15.1: ST Credit Notes & Partial Payments

As a **Finance Analyst**,
I want ST credit notes and partial payments,
So that ST tracking reflects complexity.

**Acceptance Criteria:**

**Given** recorded ST invoice
**When** I register credit note or partial payment
**Then** cumulative recalculated (FR52b), balance tracked (FR52d)

### Story 15.2: ST Dispute Management

As a **PM**,
I want to flag ST invoices as disputed,
So that contested amounts are handled properly.

**Acceptance Criteria:**

**Given** incorrect ST invoice
**When** I flag as disputed
**Then** reason, resolution date, documents (FR52c)
**And** suspended from payment, visible in tracking

### Story 15.3: ST Contractual Holdbacks

As a **PM**,
I want ST holdback management,
So that retenues are tracked per subcontractor.

**Acceptance Criteria:**

**Given** ST with holdback clause
**When** configured
**Then** accumulated, released, remaining tracked (FR52e)
**And** cross-linked with client holdback alerts (FR39i)

### Story 15.4: ST Intact Import & Document Attachments

As a **Finance user**,
I want ST import from Intact and document attachments,
So that entry is minimized and docs centralized.

**Acceptance Criteria:**

**Given** Intact ST data
**When** I import
**Then** API import with validation (FR52)
**And** multiple attachments and version history per invoice (FR52f)

## Epic 16: Consortium Management (MVP-1.5)

Consortium entity, dual financial view, partner invoicing, profit distributions, budget by partner.

### Story 16.1: Consortium Entity & Member Configuration

As a **Finance user**,
I want to create consortium entities with members,
So that partnerships are structured.

**Acceptance Criteria:**

**Given** Finance user
**When** I create consortium
**Then** name, client, PR role, members with coefficients totaling 100% (FR59)
**And** multiple projects associable (FR60)

### Story 16.2: Dual Financial Perspective

As a **Finance user**,
I want to toggle consortium vs Provencher view,
So that I see both perspectives.

**Acceptance Criteria:**

**Given** consortium project
**When** I toggle view
**Then** consortium view: client revenue, costs, margin; Provencher view: invoices + profit share (FR61)
**And** consortium CA excluded from Provencher CA (FR62)

### Story 16.3: Partner Invoicing & ST Consortium

As a **Finance user**,
I want to enter partner invoices and manage consortium STs,
So that member costs are tracked.

**Acceptance Criteria:**

**Given** consortium with projects
**When** I manage invoices
**Then** partner invoices by Project → Partner (FR64)
**And** ST consortium vs ST via PR distinction (FR62b, FR64h)

### Story 16.4: Basic Profit Distribution

As a **Finance user**,
I want to record profit distributions manually,
So that member payments are tracked.

**Acceptance Criteria:**

**Given** consortium project
**When** I record distribution
**Then** date, amount per member, justification (FR64a)
**And** simple manual entry, audited

### Story 16.5: Consortium Invoicing & Financial Synthesis

As a **Finance user**,
I want consortium client invoicing and per-project synthesis,
So that billing and monitoring are integrated.

**Acceptance Criteria:**

**Given** billable consortium work
**When** I prepare invoice
**Then** 7-column structure with consortium annexes (FR64f)
**And** dual KPIs, member breakdown, ST bars (FR64i)
**And** budget by phase with partner columns (FR64j)

### Story 16.6: BU Director Consortium Dashboard

As a **BU Director**,
I want consortium recap dashboard,
So that I monitor all consortium projects.

**Acceptance Criteria:**

**Given** BU Director with consortiums
**When** I view dashboard
**Then** all consortiums with projects, ratios, progress, outstanding (FR63)

## Epic 17: Multi-Currency, Data Operations & Extended Features (MVP-1.5)

Multi-currency, bulk ops, time extended, expense extended, client groups.

### Story 17.1: Multi-Currency Invoicing

As a **Finance user**,
I want multi-currency invoicing with dual display,
So that international clients are served.

**Acceptance Criteria:**

**Given** non-base currency client
**When** I configure currency
**Then** per client/project with exchange rates (FR81)
**And** dual display on financial screens (FR82)

### Story 17.2: Bulk Import & Export

As an **Admin**,
I want bulk data operations,
So that large ops don't require manual entry.

**Acceptance Criteria:**

**Given** Admin access
**When** I import/export
**Then** standardized templates with validation and dry-run (FR93)
**And** export any list with filters (FR94)
**And** async tasks with progress

### Story 17.3: Time Tracking Extended Features

As a **Finance user**,
I want HRIS import, period unlock, and bulk corrections,
So that time data stays accurate.

**Acceptance Criteria:**

**Given** advanced time needs
**When** I use extended features
**Then** HRIS absence import (FR27b)
**And** period unlock with auto re-lock (FR27c)
**And** bulk corrections with audit trail (FR27d)

### Story 17.4: Expense Extended & Client Groups

As a **Finance user**,
I want expense reversal, rejection workflows, and client groups,
So that edge cases are handled.

**Acceptance Criteria:**

**Given** validated expenses or related clients
**When** I manage
**Then** reversal with justification (FR46b)
**And** structured rejection with resubmit (FR46c)
**And** client group membership (FR86d)

## Epic 18: Strategic Intelligence & Advanced Features (MVP-2)

Advanced consortium, data retention, financial operations.

### Story 18.1: Advanced Profit-Sharing Rules

As a **Finance user**,
I want complex profit-sharing rules,
So that partnership agreements are modeled accurately.

**Acceptance Criteria:**

**Given** consortium
**When** I configure rules
**Then** clause type, measurement modes, thresholds (FR59b)
**And** consortium or per-project level (FR59c)

### Story 18.2: Guided Profit Distribution Workflow

As a **Finance user**,
I want a 5-step guided distribution workflow,
So that distributions are transparent and approved.

**Acceptance Criteria:**

**Given** consortium with rules
**When** I initiate distribution
**Then** 5 steps: statement, cash flow, margin, parameters, allocation (FR64c)
**And** 2-level approval (FR64c2)
**And** effort-vs-coefficient alerts (FR64d)

### Story 18.3: Treasury & Cash Management

As a **Finance user**,
I want consortium treasury tracking,
So that financial health is visible.

**Acceptance Criteria:**

**Given** consortium
**When** I view treasury
**Then** bank balance, working capital, cash flow, payment capacity (FR64e)
**And** manual adjustments with audit (FR64g)

### Story 18.4: Tax Declarations & Fiscal Compliance

As a **Finance user**,
I want tax declarations and compliance analysis,
So that obligations are tracked.

**Acceptance Criteria:**

**Given** consortium with tax obligations
**When** I manage declarations
**Then** consolidated per period, workflow tracking (FR64k, FR64l)
**And** automated compliance analysis exportable PDF (FR64m)

### Story 18.5: Consortium Excel Import

As a **Finance user**,
I want to import historical consortium data,
So that migration doesn't require manual entry.

**Acceptance Criteria:**

**Given** historical data
**When** I import
**Then** validated Excel template, preview before commit (FR64b)

### Story 18.6: Data Retention, Archival & Purge

As an **Admin**,
I want retention policies and purge capabilities,
So that the system stays performant.

**Acceptance Criteria:**

**Given** Admin access
**When** I configure retention
**Then** archival rules per entity type (FR95)
**And** purge with double confirmation (FR96)
**And** operations journal (FR97)

### Story 18.7: Year-End Adjustments, Bank Reconciliation & Entity Transfers

As a **Finance user**,
I want year-end adjustments, bank reconciliation, and entity transfers,
So that financial closing is managed.

**Acceptance Criteria:**

**Given** financial closing scenarios
**When** I perform operations
**Then** adjustment entries at project/consortium level (FR98)
**And** bank reconciliation with transaction matching (FR99)
**And** project transfer between entities (FR15m)

---

## MVP-1.5 Deferred Stories (Added v1.1.012)

The following stories were identified during MVP-1 sprints V1-V5 and BMAD audits as important but non-blocking. They are prioritized for MVP-1.5 implementation.

### Deferred 1: Vue comptabilite conforme au mockup

As a **Finance or PAIE user**,
I want the accounting view to match the validated mockup (timesheet-mockups.html section "Comptabilite"),
So that monthly reporting is complete and usable.

**Scope:** Monthly view per project with hours by week, billing status, "Generer rapport" button, and list of unsubmitted timesheets.

### Deferred 2: Relance des retardataires

As a **PAIE user**,
I want a "Relancer" button per employee and automated email reminders,
So that late timesheet submissions are systematically followed up.

**Scope:** Manual "Relancer" button in PAIE view, automated email reminders Wednesday and Friday, escalation to manager if not submitted after deadline.

### Deferred 3: PeriodLock dedicated model (replace status-based locking)

As a **developer**,
I want a dedicated PeriodLock model instead of using LOCKED status on TimeEntry,
So that the workflow status field is preserved for its intended purpose (DRAFT/SUBMITTED/APPROVED/VALIDATED).

**Scope:** New PeriodLock model, migration from status-based locking, audit trail for lock/unlock operations, automatic re-lock after PeriodUnlock expiration.

### Deferred 4: Heures contrat par employe (replace hardcoded 40h)

As a **Finance or HR user**,
I want per-employee contractual hours instead of the hardcoded 40h default,
So that part-time employees and special contracts are handled correctly in payroll controls.

**Scope:** Add contractual_hours field to employee profile, use in all payroll controls and norm calculations, support part-time and forfaitaire contracts.

### Deferred 5: Onglet Budget projet avec montants par phase (Added v1.1.012)

As a **Chef de projet or Finance user**,
I want a Budget tab in the project detail view with budgeted amounts per phase,
So that invoice lines can be pre-filled automatically from the approved budget.

**Scope:** Budget tab in project detail, amount entry per phase, link between budget lines and invoice line pre-fill, validation that invoiced amounts do not exceed budget.

### Deferred 6: Calcul automatique TPS/TVQ sur lignes de facture (Added v1.1.012)

As a **Finance user**,
I want TPS and TVQ taxes to be calculated automatically on invoice lines,
So that tax amounts are always correct and I do not have to compute them manually.

**Scope:** Automatic TPS (5%) and TVQ (9.975%) calculation on each invoice line, tax summary on invoice, support for tax-exempt lines, recalculation on line edit.

### Deferred 7: Allocation de paiements multi-factures (Added v1.1.012)

As a **Finance user**,
I want to allocate a single payment across multiple invoices via the PaymentAllocation model,
So that partial payments and batch payments are tracked accurately.

**Scope:** UI for PaymentAllocation creation, split a payment across selected invoices, automatic update of invoice paid/remaining amounts, validation that total allocations equal payment amount.
