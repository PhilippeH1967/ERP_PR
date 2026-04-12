---
stepsCompleted: ['step-01-init', 'step-02-discovery', 'step-02b-vision', 'step-02c-executive-summary', 'step-03-success', 'step-04-journeys', 'step-05-domain', 'step-06-innovation', 'step-07-project-type', 'step-08-scoping', 'step-09-functional', 'step-10-nonfunctional', 'step-11-polish', 'step-12-complete']
status: complete
classification:
  projectType: SaaS B2B
  domain: Professional Services / Architecture ERP
  complexity: high
  projectContext: greenfield
inputDocuments:
  - "_bmad-output/planning-artifacts/product-brief-ERP-2026-03-01.md"
  - "_bmad-output/planning-artifacts/party-mode-reflexion-saisie-projet.md"
  - "_bmad-output/mockups/erp-mockups.html"
  - "listePoste.xlsx"
  - "Analyse EPIC Logiciele Existants/OOTI/EPIC_001_Opportunites.md"
  - "Analyse EPIC Logiciele Existants/OOTI/EPIC_004_Facturation.md"
  - "Analyse EPIC Logiciele Existants/OOTI/EPIC_005_Temps.md"
  - "Analyse EPIC Logiciele Existants/OOTI/EPIC_006_Planning.md"
  - "Analyse EPIC Logiciele Existants/OOTI/EPIC_007_Couts.md"
  - "Analyse EPIC Logiciele Existants/OOTI/EPIC_008_Finances.md"
  - "Analyse EPIC Logiciele Existants/OOTI/EPIC_009_Collaborateurs.md"
  - "Analyse EPIC Logiciele Existants/OOTI/EPIC_010_Clients.md"
  - "Analyse EPIC Logiciele Existants/OOTI/EPIC_011_Rapports.md"
  - "Analyse EPIC Logiciele Existants/OOTI/EPIC_012_Validation.md"
  - "Analyse EPIC Logiciele Existants/OOTI/EPIC_013_NotesDeFrais.md"
  - "Analyse EPIC Logiciele Existants/OOTI/EPIC_014_TableauDeBord.md"
  - "Analyse EPIC Logiciele Existants/OOTI/EPIC_015_Collaboration.md"
  - "Analyse EPIC Logiciele Existants/OOTI/EPIC_016_Configuration.md"
  - "Analyse EPIC Logiciele Existants/OOTI/EPIC_017_Notifications.md"
  - "Analyse EPIC Logiciele Existants/OOTI/UX_Recommandations.md"
documentCounts:
  briefs: 1
  research: 0
  reflections: 1
  mockups: 1
  referenceData: 1
  ootiAnalysis: 16
date: 2026-03-03
lastUpdated: 2026-04-01
author: Philippe
---

# Product Requirements Document - ERP

> **Version History:** v1.1.012 (2026-04-01) — Added PAIE role (9th role), time entry status flow (DRAFT→SUBMITTED→PM_APPROVED→FINANCE_APPROVED→PAIE_VALIDATED→LOCKED), period locking (PeriodFreeze/PeriodUnlock/TimesheetLock), 11 payroll controls, billing permissions matrix, per-entry PM approval with multi-PM color coding, MVP-1.5 deferred backlog from Sprint V5 and BMAD audits. Added project-linked invoices, free invoices, ST refacturable lines, invoiced hours tracking, mark-hours-invoiced action, project Budget tab with phase-level editing (Added v1.1.012). All additions marked "(Added v1.1.012)" or "(Updated v1.1.012)".

## Executive Summary

ERP is a custom-built project management and business operations platform designed specifically for a 400-person architecture firm (Provencher_Roy) operating across two legal entities (Provencher_Roy Prod, PRAA) and 6 Business Units. The firm is currently constrained by an aging, unintuitive PSA tool (Planview ChangePoint) supplemented by scattered Excel spreadsheets. The platform consolidates project management, time tracking, invoicing, financial oversight, resource planning, expense management, and business development into a single, modern application — purpose-built for the workflows, contract types, and organizational structure of a multi-entity architecture practice.

The solution draws functional inspiration from two reference applications — ChangePoint (for its depth in project structure, WBS hierarchy, multi-entity billing, and contract management) and OOTI (for its modern UX, opportunity pipeline, and architecture-specific design) — while surpassing both through superior usability, integrated AI assistance, native accounting integration (Intact/Sage), mobile field capabilities, OCR expense processing, and a tailored fit to the firm's specific operational needs. The platform is designed with future SaaS commercialization in mind (Phase 1: internal use, Phase 2: multi-tenant product for architecture firms).

### What Makes This Special

1. **Built by architects, for architects** — The platform supports architecture-specific workflows including sequential realization phases, transversal support services, virtual resource profiles, consortium management, and contract types (forfaitaire, consortium, co-développement, conception-construction) that no generic ERP can provide.

2. **Radical simplicity over feature bloat** — Project creation via a 4-step wizard (Metadata → Budget → Resources & Planning → Subcontractors), timesheet entry under 5 minutes/week, invoice preparation pre-populated from approved hours. Every interaction is designed around the Two-Minute Rule.

3. **Right time, right tools** — Django 5, Vue 3, TypeScript, PostgreSQL 16 with Row-Level Security, Redis 7, Celery for async processing. AI capabilities planned for Phase 1.5+ (auto-fill timesheets, predictive RAF, out-of-scope detection).

4. **Commercialization-ready from day one** — Multi-tenant PostgreSQL RLS architecture enables Phase 2 SaaS offering to other architecture firms, with data migration tooling from ChangePoint as a competitive advantage.

---

## Project Classification

| Attribute | Value |
|---|---|
| **Project Type** | SaaS B2B |
| **Domain** | Professional Services / Architecture ERP |
| **Complexity** | High |
| **Project Context** | Greenfield |
| **Tech Stack** | Django 5.0 + Vue 3 + TypeScript + Pinia + TailwindCSS + PostgreSQL 16 + Redis 7 + Celery |

---

## Success Criteria

### User Success

| Metric | Target | Measurement | Timeline |
|---|---|---|---|
| **Timesheet entry time** | < 5 min/week (baseline ChangePoint: ~15-20 min) | Time-on-task analytics on sample of 50 users | Month 1 post go-live |
| **Project creation time** | < 10 min via 4-step wizard | Time-to-completion tracking | Month 1 |
| **Zero Excel fallback** | No core process requires Excel (audit of active spreadsheets) | BU-by-BU audit of operational Excel files still in use | Month 3 |
| **Self-service rate** | 90% of daily tasks without help desk | Help desk ticket volume vs active user count | Month 3 |
| **Net Promoter Score** | ≥ 40 | Quarterly NPS survey (baseline at go-live, target at month 6) | Month 6 |

### Business Success

| Metric | Target | Measurement | Timeline |
|---|---|---|---|
| **ChangePoint decommissioned** | 100% of active projects migrated | Automated reconciliation: CP totals = ERP totals per project | Go-live |
| **Timesheet submission** | 100% weekly submission rate | System report: submitted / expected per week | Month 1 |
| **Invoice cycle** | 10 invoices in parallel match ChangePoint to the dollar | Side-by-side comparison signed off by Finance | Go-live gate |
| **Billing accuracy** | Reduce billing leakage by 15% vs 2025 baseline ($X) | Compare CA/Salary ratio and uncollected hours YoY | Month 6 |
| **Expense reports** | 100% of expense submissions through ERP | Zero paper/email expense reports | Month 2 |
| **Time to invoice** | -30% reduction vs ChangePoint avg (baseline: X days) | Average days from period close to invoice sent | Month 6 |

### Technical Success

| Metric | Target | Measurement |
|---|---|---|
| **System uptime** | 99.5% during business hours (Mon-Fri 7:00-19:00 ET) | Monitoring (UptimeRobot or equivalent) |
| **Page load time** | < 2 seconds for all primary screens | Lighthouse/synthetic monitoring |
| **Concurrent users** | 400+ with < 10% degradation at peak (Monday 8-10 AM) | Load test before go-live |
| **Data migration integrity** | 100% validated — zero financial data loss | Automated reconciliation script per project |

---

## Product Scope

### In Scope

- **Project Management** — 4-step creation wizard, two-axis structure (sequential phases + transversal support services), virtual resource profiles, multi-employee assignment, WBS hierarchy, contract management, subcontractor management, internal projects, project dashboard
- **Time Tracking** — Authorization-based visibility, weekly entry, 3-level approval (PM → Finance → PAIE), per-entry PM approval, multi-PM color coding, period locking (freeze/unlock), phase/person blocking, payroll controls, correction workflows, favorites and quick-switch
- **Invoicing & Financial Layer** — Dual project layers (realization + financial), mixed billing modes, dual hourly rates, 7-column invoice preparation, CA/Salary ratio tracking, 10+ billing templates, billing dossiers, invoice workflow, payment tracking, Intact export
- **Expense Reports** — Expense entry with receipt upload, 3-level approval, per-project refundability, configurable categories, reporting, Intact export
- **Supplier Payment Tracking** — 3-state lifecycle, PM authorization + Finance payment, cross-project reporting
- **Service Proposals** — Proposal creation and lifecycle, time tracking, conversion to project, commercial reporting
- **Consortium Management** — Consortium entity, multi-project support, dual financial views, profit-sharing calculation
- **User & Access Management** — SSO Microsoft Entra ID, 9 roles with RBAC (including PAIE), salary data visibility enforcement, audit trail, delegation
- **Client Management** — 5-tab client interface, duplicate detection, financial history
- **Dashboards & Reporting** — Role-based dashboards, financial KPIs, hours reports, system health
- **Localization** — Bilingual French/English, locale-aware formatting, jurisdiction-specific labor and expense rules
- **Notification Center** — Centralized notifications, actions requises dashboard section
- **Data Migration** — ChangePoint import (projects, WBS, time entries, billing history)

### Out of Scope

| Feature | Rationale | Target Phase |
|---|---|---|
| **Opportunity pipeline** | Not essential for daily operations | Phase 2 |
| **Mobile native app** | Desktop-first; responsive web sufficient for MVP | Phase 1.5 |
| **OCR receipt scanning** | Manual upload sufficient initially | Phase 1.5 |
| **AI auto-fill timesheets** | Requires 3+ months historical data | Phase 1.5 |
| **AI predictive RAF** | Needs mature project data | Phase 2 |
| **AI out-of-scope detection** | Advanced feature requiring training data | Phase 2 |
| **AI proactive alerts** | Dependent on AI models | Phase 2 |
| **AI resource planning** | Requires historical WBS patterns | Phase 2 |
| **Intact bidirectional sync** | Manual export sufficient initially | Phase 1.5 |
| **CPI indexation** | Low volume of multi-year contracts | Phase 2 |
| **Cmd+K universal search** | Standard navigation sufficient | Phase 2 |
| **Advanced executive dashboards** | Basic KPIs in MVP, BI-lite later | Phase 2 |
| **Multi-tenant SaaS** | Internal deployment first | Phase 2 |

---

## User Journeys

### Journey 1: Marie — Employee (Architect/Engineer)

**Profile:** Architect or technician, 25-45 years old, working on 1-3 projects simultaneously. Represents ~300 of the 400 employees. Primary interaction: daily time entry and occasional expense reports.

**Weekly Timesheet Entry:**
1. Marie opens the ERP on Monday morning. Her weekly timesheet view displays only projects/phases where she is assigned.
2. She enters hours per project/phase/task per day. Client-facing labels (libellés client) are displayed for each phase and task.
3. Daily total indicators highlight when her hours differ from the norm (7.5h or 8h).
4. She saves as draft throughout the week, then submits weekly for approval.
5. Total weekly interaction: under 5 minutes.

**Expense Report:**
1. Marie incurs a project-related expense on a construction site.
2. She creates an expense report, uploads a receipt (photo/PDF), selects the project, category, and flags as refacturable if applicable.
3. The report goes through 3-level approval: PM validates project relevance → Finance validates GL accounts and tax breakdown → Finance processes payment/export.

### Journey 2: Jean-François — Project Manager (Senior Architect)

**Profile:** Architect with 8+ years experience, manages 2-4 projects simultaneously while practicing architecture. Dual practitioner/manager role is the norm.

**Project Creation:**
1. Jean-François launches the 4-step project creation wizard.
2. **Step 1 — Metadata:** Selects contract type (triggering template), enters project identification, sets start/end dates, designates PM, Associé en charge, and Invoice Approver. Defines phases/WBS with standard and client-facing labels.
3. **Step 2 — Budget:** Configures hours and costs per phase/task, sets billing mode (fixed-price or hourly), assigns rate grid.
4. **Step 3 — Resources & Planning:** Positions virtual resource profiles at the phase level. Views a simplified Gantt showing all phases on a quarterly timeline with editable start/end dates per phase.
5. **Step 4 — Subcontractors:** Optionally configures subcontractor budgets. System warns if no ST budget allocated. Can skip this step.
6. On confirmation, the Associé en charge is invited to review.

**Daily Dashboard:**
1. Jean-François opens his personalized dashboard showing all projects with health indicators (green/yellow/red).
2. He sees budget consumed, hours consumed vs planned, team status, and phase completion per project.
3. He approves pending time entries individually (per-entry, not per-sheet) for his projects. Color coding distinguishes his projects (blue), already-approved entries (green), and other PMs' projects (grey). *(Updated v1.1.012)*

### Journey 3: Nathalie — Finance/Controller

**Profile:** Member of the finance/administration team (5-8 people). Manages the entire billing cycle, subcontractor tracking, and Intact synchronization.

**Invoice Preparation:**
1. Nathalie opens the invoice preparation screen for a project. The 7-column layout shows: deliverable name, total contract amount, invoiced to date, % billing advancement, % hours advancement, amount to bill this month (editable), % advancement after billing.
2. The CA/Salary ratio banner displays real-time calculations as she adjusts amounts.
3. Visual alerts highlight phases where hours diverge from billing by more than 10 points.
4. She selects the client's billing template (from 10+ configurable formats), assembles the billing dossier (invoice + client-formatted timesheets + subcontractor invoices), and routes for PM approval.
5. After approval, she exports to Intact in structured format.

**Expense Validation:**
1. Nathalie receives approved expense reports from PMs.
2. She validates GL accounts, verifies tax breakdown (HT, TPS, TVQ), adjusts reimbursable amounts if needed.
3. She processes payment and export separately from validation.

### Journey 4: Sophie — Department Assistant (BU Assistant)

**Profile:** Business Unit assistant (6 people, one per BU). Operational backbone of her BU — supports associates, directors, and PMs with data entry, report preparation, and administrative follow-up.

**Daily Operations:**
1. Sophie tracks missing timesheets and pending approvals for her BU using the dashboard.
2. She assists PMs with project creation when needed, leveraging templates and smart defaults.
3. She generates BU-level reports with one click — no manual Excel assembly.
4. She acts as delegate for PMs during absences, with clear delegation scope and audit trail.

### Journey 5: Pierre — Associate/BU Director

**Profile:** Partner/director overseeing 10-20+ projects across one or more BUs. Makes strategic decisions, drives business development, and defines WBS structures.

**Executive Dashboard:**
1. Pierre opens his executive dashboard showing portfolio health at a glance: projects in green/yellow/red, overall margins, utilization rates.
2. He drills down from portfolio to project to phase with progressive detail.
3. For consortium projects, he toggles between Provencher view and consortium view to see dual financial perspectives.
4. He reviews and approves invoices via an accordion-based list with slide-over brouillon preview.

### Journey 6: Admin — System Administrator

**Profile:** IT administrator (1-2 people). Responsible for SSO, user management, permissions, audit trail, and system health.

**System Management:**
1. Admin configures SSO via Microsoft Entra ID with auto-provisioning.
2. Assigns roles (9 distinct roles, including PAIE) with granular permissions through the admin interface. *(Updated v1.1.012)*
3. Monitors system health: response times, error rates, adoption by BU.
4. Manages data migration from ChangePoint (10+ years of data).
5. Configures templates, formats, categories, positions, and tax settings without code changes.

---

## Domain-Specific Requirements

### Architecture Firm Domain

The ERP operates in the professional services domain, specifically for architecture firms. Key domain characteristics that drive requirements:

1. **Two-Axis Project Structure** — Architecture projects are organized along two axes: sequential realization phases (Étude préparatoire → Concept → Préliminaire → Définitif → Appel d'offres → Surveillance) and transversal support services (Gestion de projet, BIM, 3D, Paysage, Design). Support services are global project-level tasks, not broken down by phase.

2. **Architecture-Specific Contract Types** — Four contract types with distinct billing, tracking, and reporting rules: forfaitaire (fixed-fee), consortium (multi-firm partnership), co-développement, and conception-construction.

3. **Virtual Resource Profiles** — 31 position archetypes (from Architecte to Urbaniste) used for budget estimation and capacity planning before assigning real employees. Complete reference list from listePoste.xlsx.

4. **Dual Salary Costing** — Standard cost per profile (visible to PMs/direction) and real cost per person (restricted to Finance/Direction). CA/Salary ratio is the primary profitability KPI.

5. **Multi-Entity Operations** — Two legal entities (Provencher_Roy Prod, PRAA) with entity-specific tax settings (TPS/TVQ), billing rules, and financial reporting.

6. **Personnel Lending** — Inter-BU staff loans are common. Revenue (CA) from lent staff is repatriated to the person's home BU.

7. **Complex Billing** — 10+ configurable invoice formats per client. Billing dossiers include invoice + timesheets in client-specific format + subcontractor invoices. Client-facing labels (libellés client) on phases and tasks differ from internal standard labels.

8. **Consortium Management** — Dedicated consortium entity linking multiple independent projects. Dual financial views (consortium-level vs Provencher-level). Critical accounting rule: consortium client revenue is excluded from Provencher's CA.

9. **Support Service Allocation** — Shared support services (3D, BIM, Sustainable Development, Landscape) receive allocated budgets per project. Support specialists may work on 5-10 projects simultaneously.

10. **Subcontractor Management** — Three budget layers: internal fees, refacturable subcontractors (billed to client with markup %), and absorbed subcontractors (firm cost). 3-state invoice lifecycle (Received → Authorized → Paid) independent from client billing.

---

## Innovation & Novel Patterns

### Novel Architectural Patterns

1. **Dual Financial Layer** — Separation between realization tracking (PM perspective: phases, hours, virtual profiles) and billing (Finance perspective: financial phases, contractual rates, invoice preparation). Financial phases can group multiple realization phases with mixed billing modes within the same project. This pattern is rare in architecture ERPs and enables the firm's complex billing requirements.

2. **Virtual-to-Real Resource Transition** — Virtual resource profiles are positioned on project phases for budget estimation. PMs progressively replace virtual profiles with real employees using a 3-tier priority modal (matching profile + available, similar profiles, all employees) with percentage-based hour distribution. This pattern enables budget planning before team formation.

3. **WBS Dual Labeling** — Each WBS element maintains both a standard internal label and a client-facing label. All timesheet entries, reports, and invoices shown to clients use the client-facing labels, while internal dashboards can display both. This solves the persistent problem of client-specific nomenclature in architecture projects.

4. **Consortium Dual View** — A toggle between "Provencher view" (invoices issued to consortium + profit share = firm's CA) and "Consortium view" (client revenue, member costs, margin, profit sharing). The critical accounting rule — consortium client revenue excluded from Provencher's CA — is enforced at the data model level.

5. **Phase/Person Blocking & Period Locking** — Multi-level blocking mechanism: phase-level blocking (no one can enter time on a completed phase), person-level blocking (specific individual blocked but others can still enter), and global period freeze (no entries before a cutoff date, with targeted unlock exceptions). This granular control prevents unauthorized time entry while maintaining flexibility. *(Updated v1.1.012)*

6. **4-Step Project Creation Wizard** — Structured creation flow (Metadata → Budget → Resources & Planning → Subcontractors) with optional Step 4 and post-creation completion capabilities. Balances thoroughness with speed — projects can be created quickly and refined over time.

### Innovation Opportunities (Future Phases)

- **AI Auto-Fill Timesheets** (Phase 1.5) — Learning from 3+ months of patterns to pre-fill weekly timesheets
- **AI Predictive RAF** (Phase 2) — Predicting remaining hours based on historical project patterns
- **AI Out-of-Scope Detection** (Phase 2) — Automatic detection of work exceeding contract scope
- **AI Proactive Alerts** (Phase 2) — Budget warnings, schedule risks, utilization anomalies
- **OCR Receipt Scanning** (Phase 1.5) — Photo → auto-parsed expense line

---

## SaaS B2B Specific Requirements

### Multi-Tenancy Architecture

- **PostgreSQL Row-Level Security (RLS)** on all tenant-scoped tables from day one
- Every tenant-scoped model includes a `tenant_id` FK
- Django middleware resolves tenant from JWT claims and sets PostgreSQL session variable
- RLS policies filter all queries transparently
- Per-tenant configuration: entities, BUs, positions, templates, invoice formats, tax settings

### SaaS Readiness (Phase 2)

- Multi-tenant architecture validated for external clients
- White-labeling capability
- Self-service onboarding for new tenants
- ChangePoint migration toolkit reusable for external architecture firms
- Per-tenant billing and subscription management

### Security & Compliance

- SSO via Microsoft Entra ID (OIDC/SAML 2.0) — no local passwords
- JWT authentication with short-lived access tokens (15min) + refresh tokens (7 days)
- All data encrypted in transit (TLS 1.3) and at rest (AES-256)
- Role-based access control with 9 distinct roles (including PAIE) and delegation *(Updated v1.1.012)*
- Real salary costs restricted via PostgreSQL RLS
- Complete audit trail on all financial entity modifications
- OWASP Top 10 compliance

### Data Architecture

- PostgreSQL 16 as primary datastore
- Redis 7 for caching, session store, Celery broker, and WebSocket channel layer
- Time entry tables partitioned by period for query performance at scale
- 10+ years historical data support with no degradation on current-period queries
- Automated daily backups with point-in-time recovery (RPO <1 hour, RTO <4 hours)

---

## Project Scoping & Phased Development

### MVP Strategy & Philosophy

The MVP must enable the firm to **fully decommission ChangePoint** by delivering the essential modules that support daily operations for 400 employees. Development is AI-assisted (Claude Code), meaning a lean team can deliver enterprise-grade functionality through disciplined scope control and iterative development.

The phasing strategy prioritizes **operational necessity** over feature richness: if 400 employees cannot do their daily work without a feature, it is MVP-1. If it enhances productivity but has a manual workaround, it is MVP-1.5. If it provides strategic value but is not operationally blocking, it is MVP-2.

### Product Arbitration Rules

When scope decisions arise during development, apply these rules in order:

1. **80/20 Rule** — Build the 20% of features that cover 80% of use cases. Edge cases are handled manually until data proves they need automation.
2. **Standardize First** — Resist per-BU or per-PM customization requests. Offer configuration within defined boundaries, not unlimited flexibility.
3. **Manual Fallback Acceptable** — If a feature is complex and low-frequency (e.g., CPI indexation, consortium profit distribution), a manual process with good UX is acceptable for MVP.
4. **Financial Accuracy is Non-Negotiable** — Any feature touching invoicing, billing, or financial reporting must be correct to the cent. No approximations, no rounding shortcuts.
5. **Voluntary Technical Debt** — Accept UI polish debt (e.g., basic table instead of advanced grid) but never accept data model debt. The schema must be right from day one.
6. **Simple First, Smart Later** — Phase 1 uses rules-based logic. AI/ML features (auto-fill, predictive RAF, anomaly detection) are explicitly Phase 1.5 or Phase 2.

### Phasing Strategy

#### MVP-1: Operational Foundation (Months 1-6)
Replace ChangePoint. Every employee can enter time, every PM can manage projects, every Finance user can produce invoices. No Excel required for core operations.

#### MVP-1.5: Productivity Enhancement (Months 7-9)
Add features that significantly improve daily productivity but have manual workarounds in MVP-1. Service proposals, consortium management, AI-assisted timesheets, mobile access.

#### MVP-2: Strategic Intelligence (Months 10-15)
AI-powered features, advanced analytics, opportunity pipeline, multi-tenant SaaS commercialization.

### MVP-1 Feature Set

| Module | Key Capabilities |
|---|---|
| **Project Management** | 4-step wizard, templates, WBS hierarchy, virtual profiles, subcontractors, project dashboard, internal projects |
| **Time Tracking** | Weekly entry, 3-level approval (PM per-entry → Finance → PAIE), multi-PM color coding, phase/person blocking, period freeze/unlock, 11 payroll controls, favorites, reminders, correction workflows |
| **Invoicing & Financial Layer** | Dual layers, mixed billing, dual rates, 7-column prep screen, CA/Salary ratio, templates, dossiers, Intact export |
| **Expense Reports** | Entry with receipts, 3-level approval, refacturable tracking, categories, Intact export |
| **Supplier Payment Tracking** | 3-state lifecycle, PM authorization, Finance payment, cross-project reporting |
| **Cross-Cutting** | SSO, RBAC (9 roles including PAIE), audit trail, dashboards, bilingual, client management, notifications |

### MVP-1.5 Features

| Feature | Value |
|---|---|
| **Service Proposals** | Proposal lifecycle, time tracking, conversion to project, commercial reporting |
| **Consortium Management (core)** | Consortium entity, dual financial views, profit-sharing calculation |
| **Import absences from HRIS** | Scheduled sync or manual file upload |
| **Automated dunning** | Configurable escalation levels for unpaid invoices |
| **Import ST invoices via Intact API** | Subcontractor invoice import |
| **Consortium flag on projects** | Flag project as consortium, associate with consortium entity |
| **Invoice currency per client** | Exchange rate management |
| **Dual currency display** | Financial screens show both currencies |
| **Client group membership** | Client grouping capability |

### MVP-1.5 Deferred Items — Identified During MVP-1 Development (Added v1.1.012)

The following items were identified during Sprint V1-V5 development and BMAD audits as important improvements with manual workarounds in MVP-1:

| Area | Item | Origin |
|---|---|---|
| **Timesheets** | Accounting view (monthly by project, hours by week, billing status, "Generate report" button) | Mockup audit |
| **Timesheets** | Late submission reminders (auto-email Wed/Fri, escalate to manager) | Sprint V5 |
| **Timesheets** | Per-employee contract hours (replace hardcoded 40h with actual part-time/forfaitaire) | Sprint V5 |
| **Timesheets** | Separate PeriodLock model (decouple from TimeEntry status to preserve workflow) | BMAD audit |
| **Timesheets** | Audit trail for lock/unlock operations (dedicated model) | BMAD audit |
| **Timesheets** | Auto-expiry of PeriodUnlock after N days | BMAD audit |
| **Timesheets** | WebSocket/polling for real-time lock status refresh | BMAD audit |
| **Projects** | Amendments as mini-contracts (own phases, resources, billing) | Sprint V4 |
| **Projects** | Auto-numbered amendments ({code}-AV-{seq}) | Sprint V4 |
| **Projects** | Team tab with "+ Assign member" button, employee names instead of IDs | Mockup audit |
| **Projects** | Assignment % control (max 100% per phase, auto-calculate remaining) | Sprint V4 |
| **UX** | i18n on all business pages | Sprint V3 |
| **UX** | Searchable dropdowns everywhere (unified pattern) | Mockup audit |
| **Security** | Tenant filtering on approve/reject entry endpoints | BMAD audit |
| **Security** | N+1 query optimization on PM dashboard | BMAD audit |
| **Security** | Week boundary consistency (Mon-Sun vs Sun-Sat) | BMAD audit |
| **Billing** | Calcul automatique TPS/TVQ — taxes calculées automatiquement sur les lignes de facture | Sprint V5 (Added v1.1.012) |
| **Billing** | Allocation de paiements multi-factures — répartir un paiement sur plusieurs factures (PaymentAllocation) | Sprint V5 (Added v1.1.012) |

### MVP-2 Features

| Feature | Value |
|---|---|
| **Opportunity pipeline** | Full BD cycle: lead → opportunity → proposal → contract |
| **AI auto-fill timesheets** | Pre-fill from patterns after 3+ months of data |
| **AI predictive RAF** | Confidence-interval predictions based on historical data |
| **AI out-of-scope detection** | Automatic scope deviation flagging |
| **AI proactive alerts** | Budget/schedule/utilization anomaly detection |
| **Advanced executive dashboards** | BI-lite with drill-down, combinable filters, saveable reports |
| **CPI indexation** | Semi-automatic calculation for multi-year contracts |
| **Multi-tenant SaaS** | External client onboarding, white-labeling |
| **ChangePoint migration toolkit** | Reusable for external firms |
| **Advanced consortium features** | Excel import, profit distribution tracking, billing-vs-cost alerts |

### Go-Live Criteria

| Criteria | Gate |
|---|---|
| **ChangePoint decommissioned** | All active projects migrated, all 400 users on new platform |
| **100% timesheet submission** | Every employee submitting complete weekly timesheets |
| **Invoice cycle operational** | Finance producing invoices end-to-end with Intact export |
| **Expense reports functional** | Employees submitting through the ERP |
| **No critical blocking bugs** | Zero P0/P1 bugs preventing daily operations for >4 hours |
| **User satisfaction baseline** | NPS survey conducted |
| **Data migration validated** | 100% integrity verification on migrated data |
| **Performance validated** | 400 concurrent users with <2s page loads |
| **Security validated** | SSO functional, RBAC enforced, audit trail operational |

### Exception Cases

| Exception | Handling |
|---|---|
| **PM creates project without subcontractors** | Step 4 is optional; system warns but allows skip |
| **Employee assigned to 10+ projects** | Favorites and quick-switch optimize multi-project entry |
| **Consortium with 4+ members** | Scalable data model, no artificial member limit |
| **Invoice in foreign currency** | MVP-1.5 feature; MVP-1 uses base currency only |
| **Retroactive timesheet correction** | Finance can modify validated timesheets with full audit trail |
| **PM transfer mid-project** | Leadership role change with immutable history |
| **Phase completed but corrections needed** | Finance override with audit trail |
| **Client changes billing format** | Template selection is per-invoice, not locked |
| **Cross-BU personnel lending** | Tracked with CA repatriation to home BU |
| **Delegate exceeds scope** | System enforces delegation boundaries; audit trail logs all actions |
| **Subcontractor budget overrun** | Visual alerts; PM can request amendment |
| **Data migration discrepancy** | Automated reconciliation reports; manual correction workflow |

### Multi-Entity Strategy

The two legal entities (Provencher_Roy Prod, PRAA) are handled as follows:
- Each project is assigned to exactly one legal entity
- Entity-specific tax settings (TPS/TVQ rates)
- Entity-specific invoice numbering sequences
- Consolidated and per-entity financial reporting
- Entity field is set at project creation and cannot be changed

### Risk Mitigation Strategy

| Risk Category | Risk | Mitigation |
|---|---|---|
| **Technical** | PostgreSQL RLS performance at scale | Load testing early; partition time entry tables; optimize critical queries |
| **Technical** | ChangePoint data migration complexity | Dedicated migration sprint; automated validation; parallel run period |
| **Technical** | Real-time recalculation performance | WebSocket + server-side caching; denormalized KPI tables |
| **Operational** | User resistance to new tool | Role-based training; intuitive UX; progressive rollout by BU |
| **Operational** | Incomplete timesheet adoption | Automated reminders; manager accountability; blocking mechanisms |
| **Operational** | Finance workflow disruption | Parallel billing cycle (old + new) for first month |
| **Resource** | AI-assisted development bottleneck | Modular architecture enables parallel development; clear API contracts |
| **Resource** | Domain expertise gaps | Regular PM/Finance user testing; iterative feedback loops |

---

## Functional Requirements

> **Numbering convention:** FRs use a module-sequential scheme (FR1-FR15 = Project, FR16-FR27 = Time, etc.) with lettered sub-FRs (FR15k, FR39b) for additions. Gaps exist due to iterative development. Backlog items should reference FR codes, not sequence numbers. A full renumbering with module prefixes (PM-001, TT-001, INV-001) is planned for the architecture phase.

> **Data model reference:** The entity relationships underlying these FRs (Project, Phase, Task, Invoice, CreditNote, Payment, Holdback, Amendment, Expense, STInvoice, Consortium, Distribution, Client, Contact, Organization, etc.) are specified in the architecture document (`_bmad-output/planning-artifacts/architecture.md`). The PRD defines *what*, the architecture defines *how*.

> **Multi-entity in MVP-1:** All MVP-1 screens operate under a single legal entity (Provencher_Roy Prod). No entity selection field is visible in the UI. The data model includes `entity_id` from day one (for MVP-1.5 readiness) but the field is auto-populated and hidden. Entity-specific tax settings and invoice numbering are configured but for one entity only.

### Project Management

- **FR1:** [MVP-1] PM can create a new project via a 4-step wizard: Step 1 — Metadata (identification, project start/end dates, responsible roles, contract type, phases/WBS), Step 2 — Budget (hours and costs per phase/task, billing mode, rate grid), Step 3 — Resources & Planning (virtual profiles by phase + phase-level Gantt timeline), Step 4 — Subcontractors (optional, can be completed after project creation)
- **FR1b:** [MVP-1] Step 1 includes project start date and end date (previsional)
- **FR1c:** [MVP-1] Step 1 includes designation of the three project leadership roles: PM, Associé en charge, Invoice Approver
- **FR1d:** [MVP-1] Step 3 allows PM to assign virtual resource profiles at the phase level (not task level)
- **FR1e:** [MVP-1] Step 3 includes a simplified Gantt view showing all phases on a quarterly timeline with editable start/end dates per phase
- **FR1f:** [MVP-1] Step 4 (Subcontractors) is explicitly optional. Warning if no ST budget is allocated. PM can skip Step 4
- **FR1g:** [MVP-1] After project creation, confirmation screen with invitation to Associé en charge for review
- **FR2:** [MVP-1] PM can select a project template by contract type that pre-configures phases and support services
- **FR3:** [MVP-1] PM can define a two-axis project structure with sequential realization phases (Étude préparatoire, Concept, Préliminaire, Définitif, Appel d'offres, Surveillance) and transversal support services (Gestion de projet, BIM, 3D, Paysage, Design — extensible)
- **FR4:** [MVP-1] PM can position virtual resource profiles on project phases for budget estimation before assigning real employees
- **FR5:** [MVP-1] PM can replace a virtual profile with one or multiple employees using percentage-based hour distribution (from project dashboard, post-creation)
- **FR6:** [MVP-1] PM can select employees via a 3-tier priority modal: (1) matching profile with availability, (2) similar profiles, (3) all other employees
- **FR7:** [MVP-1] PM can manage a multi-level WBS hierarchy (phases, tasks, subtasks). Each phase has a standard internal label and a client-facing label
- **FR7b:** [MVP-1] PM can add, remove, or reorder phases during project creation
- **FR8:** [MVP-1] PM can track contract value, amendments, and budget consumption per WBS element
- **FR9:** [MVP-1] PM can manage subcontractors with three budget layers: internal fees, refacturable (billed to client with markup %), and absorbed (firm cost)
- **FR10:** [MVP-1.5] PM can flag a project as "consortium" and associate it with a consortium entity
- **FR11:** [MVP-1] Admin or Finance can create and manage internal projects with a lighter task/subtask structure
- **FR12:** [MVP-1] PM can view a project dashboard showing budget consumed, hours consumed vs planned, team status, virtual vs assigned status, and phase completion indicators (green/yellow/red)
- **FR13:** [MVP-1] BU Director and Finance can track personnel lending between BUs with CA repatriation to home BU
- **FR14:** [MVP-1] PM can allocate budgets for support services (3D, BIM, DD, Landscape) on projects they manage
- **FR15:** [MVP-1] Each project has a designated PM and Associé en charge. The Associé en charge oversees financial performance, approves invoices, and ensures BU alignment
- **FR15b:** [MVP-1] At project creation, PM must designate an Invoice Approver (Chargé de contrat) who may differ from the PM
- **FR15c:** [MVP-1] Each project has a lifecycle status: Active, Completed, On Hold, Cancelled. On Hold blocks time entry and billing. Completed/Cancelled archives the project
- **FR15d:** [MVP-1] PM transfer capability — PM role can be reassigned to another employee mid-project
- **FR15e:** [MVP-1] Associé en charge change — can be reassigned with proper authorization
- **FR15f:** [MVP-1] BU Director change — can be reassigned at the BU level
- **FR15g:** [MVP-1] Complete immutable change history for all leadership role changes (PM, Associé en charge, Invoice Approver, BU Director) with timestamp, old value, new value, and change initiator
- **FR15h:** [MVP-1] PM or Finance can formally close a project through a checklist-based workflow: all timesheets completed and approved, all expenses processed, all ST invoices settled or written off, final client invoice issued, holdback status recorded (released or pending), final margin calculated and frozen. Closing changes status to "Completed" and blocks further time/expense entry
- **FR15i:** [MVP-1.5] Direction or Finance can reopen a closed project with justification. Reopening restores Active status, creates an audit entry, and optionally notifies the PM and Associate in Charge. Reopened projects are flagged visually in all lists
- **FR15j:** [MVP-1.5] Closed projects are logically archived after a configurable period (default 12 months). Archived projects are excluded from active searches and dashboards but remain accessible via an "Include archived" filter. Full data is preserved. Finance or Admin can restore an archived project
- **FR15k:** [MVP-1.5] PM can create and manage contract amendments (avenants) on a project. Each amendment has: number (sequential), date, description, impact on contract value (+/-), impact on phases/tasks (new phases, modified budgets, extended timeline), approval status (Draft → PM approved → Associate approved → Active). The system maintains a version history of the contractual budget: original contract, amendment 1, amendment 2, etc. The project dashboard shows current contractual value = original + sum of amendments. Each amendment is linked to the phases/tasks it modifies
- **FR15l:** [MVP-1.5] The project budget view distinguishes: original contract value, cumulative amendments, current contract value (original + amendments), consumed to date, and remaining. Amendment impact is traceable per phase/task (which amendment created or modified each budget line)
- **FR15m:** [MVP-2] PM can transfer a project between legal entities. Direction can merge or split projects with full financial reconciliation
- **FR15n:** [MVP-1.5] PM can rebaseline a project budget without modifying the contractual value. The rebaselined budget represents the PM's realistic plan and is used for variance reporting (plan vs actual). The system maintains three budget levels: original contract, current contract (after amendments), and rebaselined plan. Variance reports can compare actuals against any of the three levels

### Time Tracking

- **FR16:** [MVP-1] Employee can view and enter time only on projects and tasks where they are assigned. No assignment = not visible in timesheet
- **FR17:** [MVP-1] Employee can enter hours per project/phase/task per day in a weekly timesheet view. Client-facing labels (libellés client) are displayed for each phase and task
- **FR18:** [MVP-1] Employee can see daily total indicators when different from the norm (7.5h or 8h)
- **FR19:** [MVP-1] Employee can save timesheet as draft and submit weekly for approval
- **FR20:** [MVP-1] PM, Finance, or Admin can block a phase (no one can enter time) or block a specific person on a phase
- **FR21:** [MVP-1] PM can approve submitted time entries individually (per-entry, not per-sheet) as first-level approver. Multi-PM support with color coding: blue = my projects, green = already approved, grey = other PM's projects *(Updated v1.1.012)*
- **FR22:** [MVP-1] Finance/Direction can approve timesheets as second-level approver
- **FR22c:** [MVP-1] PAIE can validate timesheets as third-level approver after Finance approval, with 11 automated payroll controls run before validation *(Added v1.1.012)*
- **FR22b:** [MVP-1] System enforces anti-self-approval: a secondary timesheet approver is assigned per project. No employee can approve their own time entries
- **FR23:** [MVP-1] PM or Finance defines billing mode per task (fixed-price or hourly). Employees do not choose billing categorization
- **FR23b:** [MVP-1] Mandatory phases "Gestion de projet" and "Qualité" are included in every project template by default
- **FR24:** [MVP-1] PM can request timesheet modifications on entries not yet fully validated
- **FR25:** [MVP-1] Finance can modify timesheets that have been fully validated, with complete audit trail
- **FR26:** [MVP-1] System sends automated reminders for incomplete or late timesheets
- **FR27:** [MVP-1] Employee can manage favorites and quick-switch between multiple projects
- **FR27b:** [MVP-1.5] System can import employee absences from HRIS via scheduled sync or manual file upload. Absence validation remains in HRIS — ERP only consumes approved absences
- **FR27c:** [MVP-1.5] Finance or Admin can unlock a closed time period for a specific employee with justification (e.g., late correction). Unlocking creates an audit entry and re-locks automatically after a configurable delay (default 48h)
- **FR27d:** [MVP-1.5] Finance can perform bulk time corrections: transfer hours from one project/phase/task to another for a specific employee and period, with before/after audit trail
- **FR27e:** [MVP-1] If an employee's project assignment changes after they have submitted (but not yet approved) a timesheet, the system flags the affected entries for PM review rather than silently invalidating them

### Time Entry Status Flow (Added v1.1.012)

The time entry lifecycle follows a 6-state workflow reflecting the 3-level approval chain:

```
DRAFT → SUBMITTED → PM_APPROVED → FINANCE_APPROVED → PAIE_VALIDATED → LOCKED
```

| Status | Description | Who transitions |
|---|---|---|
| **DRAFT** | Employee is editing, not yet submitted | Employee (auto on create) |
| **SUBMITTED** | Employee submitted for review | Employee |
| **PM_APPROVED** | Project Manager approved the individual entry | PM (per-entry) |
| **FINANCE_APPROVED** | Finance validated the week | Finance |
| **PAIE_VALIDATED** | Payroll controls passed and PAIE validated | PAIE role |
| **LOCKED** | Period frozen — no further modifications | System (on period freeze) |

Rejection at any level returns the entry to DRAFT with a rejection reason visible to the employee. Anti-self-approval is enforced at all levels.

### Period Locking (Added v1.1.012)

Three complementary locking mechanisms protect time entry integrity:

- **FR27f:** [MVP-1] **PeriodFreeze** — Finance, Admin, or PAIE can set a global freeze date. No time entries can be created or modified before this date across the entire tenant. Only one active freeze date exists at a time (latest wins). Used to close payroll periods permanently.
- **FR27g:** [MVP-1] **PeriodUnlock** — Finance or Admin can grant temporary exceptions to a frozen period for a specific date range. Each unlock requires a reason (Correction, Amendment, or Audit) and a justification note. Enables late corrections without unfreezing the entire period. *(MVP-1.5: auto-expiry after configurable delay, audit trail model)*
- **FR27h:** [MVP-1] **TimesheetLock** — PM, Finance, or Admin can lock a specific phase (all employees blocked) or a specific person on a phase. Granular blocking independent of period freeze. Used for completed phases or personnel changes.
- **FR27i:** [MVP-1] Lock/unlock/freeze operations are restricted to ADMIN, FINANCE, and PAIE roles. All operations are recorded with user and timestamp.

### Payroll Controls (Added v1.1.012)

- **FR27j:** [MVP-1] The PAIE role has access to 11 automated payroll validation controls that run on each employee's weekly timesheet before validation. Controls produce alerts at three severity levels (error, warning, info):

| # | Code | Severity | Rule |
|---|---|---|---|
| 1 | INCOMPLETE_HOURS | warning | Total hours < contract hours with no declared absence |
| 2 | OVERTIME_WITH_SICK | error | Overtime declared in the same week as sick leave — forbidden |
| 3 | OVERTIME_WITH_LEAVE | warning | Overtime declared in the same week as other leave — adjusted threshold |
| 4 | OVERTIME | warning/error | Hours exceed contract threshold (error if >10h overtime) |
| 5 | DAY_OVER_10H | warning | Single day exceeds 10 hours |
| 6 | WEEKEND_WORK | warning | Hours entered on Saturday or Sunday |
| 7 | SICK_AND_WORK_SAME_DAY | error | Sick leave and work hours on the same day — forbidden |
| 8 | UNUSUAL_TREND | info | Weekly hours deviate >20% from 4-week rolling average |
| 9 | CONSECUTIVE_OVERTIME | error | 3+ consecutive weeks of overtime — burn-out risk |
| 10 | PM_NOT_APPROVED | error | Entries still in SUBMITTED status (PM has not approved) |
| 11 | LEGAL_MAX_50H | error | Total hours exceed 50h/week (LNT Québec legal maximum) |

- **FR27k:** [MVP-1] PAIE can validate individual employees or perform bulk validation. Validation with outstanding error-level alerts requires explicit override.
- **FR27l:** [MVP-1] PAIE can reject entries back to DRAFT with a rejection reason visible to the employee.

### Billing Permissions (Added v1.1.012)

- **FR27m:** [MVP-1] Billing module access is governed by a role-based permission matrix:

| Operation | ADMIN | FINANCE | PM | PROJECT_DIRECTOR |
|---|---|---|---|---|
| **View** invoices, templates, payments | Yes | Yes | Yes (own projects) | Yes (own projects) |
| **Create/Edit** invoices, credit notes, payments | Yes | Yes | No | No |
| **Submit** invoices for approval | Yes | Yes | Yes | No |
| **Approve** invoices | Yes | Yes | No | Yes |

- **FR27n:** [MVP-1] EMPLOYEE, DEPT_ASSISTANT, PAIE, BU_DIRECTOR, and PROPOSAL_MANAGER roles have no direct billing access unless granted via delegation.

### Invoicing & Financial Layer

- **FR28:** [MVP-1] Finance can define financial phases that group multiple realization phases with distinct billing modes (fixed-price or hourly)
- **FR29:** [MVP-1] Finance can set dual hourly rates per project: internal cost rate and contractual client rate, via manual entry or Excel file import
- **FR30:** [MVP-1] Finance can prepare invoices via a 7-column screen with phase/task hierarchy: (1) deliverable name, (2) total contract amount, (3) invoiced to date, (4) % billing advancement, (5) % hours advancement (fixed-price) or supplier invoice amounts (subcontractors), (6) amount to bill this month (editable), (7) % advancement after billing. Sections: forfait, horaire, ST, dépenses, retenue, taxes. Double CA/Salary ratio banner
- **FR30b:** [MVP-1] Dashboard "Heures sans facturation prévue ce mois" with slide-over project detail for hours without planned billing
- **FR30c:** [MVP-1] Provisional invoice numbers (PROV-xxxx) assigned at creation, definitive number assigned at send time
- **FR30d:** [MVP-1] Project-linked invoices — "Créer facture" from project Budget tab auto-populates all billable phases as invoice lines with budget amounts from project phases. For HORAIRE phases, only uninvoiced PM_APPROVED hours are included. For FORFAITAIRE phases, the full phase budget is used as the line amount *(Added v1.1.012)*
- **FR30e:** [MVP-1] Free invoices — Simple invoices without project link, with manual lines using libre labels. Used for miscellaneous billing not tied to a specific project *(Added v1.1.012)*
- **FR30f:** [MVP-1] Sub-contractor lines — ST invoices marked as refacturable are automatically included in project invoices with line_type=ST. These lines appear in the ST section of the invoice alongside internal fee lines *(Added v1.1.012)*
- **FR30g:** [MVP-1] Free lines — Manual lines (Dépense, Autre) can be added at the bottom of any invoice for ad-hoc charges not covered by project phases or ST invoices *(Added v1.1.012)*
- **FR30h:** [MVP-1] Invoiced hours tracking — TimeEntry.is_invoiced field marks hours that have been included in a sent invoice. For HORAIRE phases, only uninvoiced PM_APPROVED hours are included when creating new invoices. A "$" badge is displayed on timesheet cells for invoiced entries *(Added v1.1.012)*
- **FR30i:** [MVP-1] Mark hours invoiced — Action on SENT or PAID invoices marks all matching time entries as invoiced (is_invoiced=True). This prevents double-billing of the same hours on subsequent invoices *(Added v1.1.012)*
- **FR30j:** [MVP-1] Project Budget tab — Phase-level budget editing accessible to ADMIN and FINANCE roles. Displays KPI cards: total budget, total invoiced, % consumed, remaining budget. Each phase row shows budgeted amount, invoiced amount, and remaining. Budget changes are tracked in audit trail *(Added v1.1.012)*
- **FR31:** [MVP-1] Finance can view visual alerts when hours advancement diverges from billing advancement by more than 10 points (red when hours > billing, green when billing ahead, yellow badge at >90%)
- **FR32:** [MVP-1] Finance can view a real-time CA/Salary ratio banner above the invoice preparation screen: ratio before billing (invoiced to date / salaries to date) and ratio after billing (with current month), compared to firm target (configurable)
- **FR33:** [MVP-1] Finance can create invoices using 10+ configurable billing templates per client
- **FR33b:** [MVP-1] Finance or PM can define per-client custom invoice line labels. WBS elements map to client-specific labels on the invoice
- **FR34:** [MVP-1] Finance can assemble billing dossiers with configurable annexes: summary hours, detail by phase/task, detail by phase/task/person, ST invoices, expense receipts, partner invoices
- **FR34b:** [MVP-1] Print-ready invoice brouillon with 5 columns, banking references, and complete formatting for client delivery
- **FR35:** [MVP-1] PM approves invoices via an accordion-based list with slide-over brouillon preview
- **FR36:** [MVP-1] Finance can track invoice status through workflow: Draft → Submitted → Approved → Sent → Paid
- **FR37:** [MVP-1] Finance can record payments received and track outstanding amounts with aging analysis
- **FR37b:** [MVP-1.5] Finance can manage automated dunning process with configurable escalation levels, adjustable delays, customizable templates, dunning dashboard, batch reminders, and suspension capability
- **FR38:** [MVP-1] Finance can export invoice data to Intact (Sage) in structured format (CSV/Excel)
- **FR39:** [MVP-1] PM can track non-billable tasks that consume hours but generate no revenue — no linked financial phase, tracked for cost visibility
- **FR39b:** [MVP-1.5] Finance can issue a credit note (avoir) against a previously sent invoice. The credit note references the original invoice number, specifies the amount credited (partial or full), the reason, and the affected line items. Credit notes receive a sequential number (NC-xxxx) and follow the same approval workflow as invoices (Finance prepares → PM approves → sent to client). The system tracks the net balance per invoice (original amount - credit notes)
- **FR39c:** [MVP-1.5] Finance can cancel (annuler) a sent invoice and reissue a corrected version. The cancelled invoice retains its number but is marked "Annulée" with link to the replacement. The replacement receives a new sequential number. Both appear in the invoice history with full audit trail
- **FR39d:** [MVP-1] Finance can record partial payments on an invoice. The system tracks: original amount, payments received (with dates and references), outstanding balance. The aging analysis (FR37) uses the outstanding balance, not the original amount
- **FR39e:** [MVP-1.5] Finance can write off (radier) small outstanding balances below a configurable threshold (e.g., <$50) with justification. Write-offs are tracked separately and reportable
- **FR39f:** [MVP-1] Finance can allocate a single client payment across multiple invoices. The system records the payment amount, allocation per invoice, and remaining unallocated balance
- **FR39g:** [MVP-1] The system tracks contractual holdback (retenue) per project as a running balance: holdback accumulated on each invoice, holdback released (partial or full), holdback remaining. Finance can issue a specific holdback release invoice at project completion or at contractual milestones. The holdback balance is visible on the project dashboard and in the client financial history
- **FR39h:** [MVP-1] Each invoice and credit note maintains a complete adjustment history
- **FR39i:** [MVP-1.5] When client holdback is released on a project (FR39g), the system alerts Finance that corresponding ST holdbacks (FR52e) may be eligible for release. The alert lists affected STs with their holdback balances. Finance can then process ST holdback releases individually: original issuance, corrections, cancellations, credit notes, payments, write-offs — all with dates, amounts, users, and justifications

### Expense Reports

- **FR40:** [MVP-1] Employee can create expense reports with date, amount, category, project, description, refacturable flag, and tax type
- **FR40b:** [MVP-1] Mandatory receipt attachment (photo/PDF) for each expense line
- **FR40c:** [MVP-1] Expense templates/models for recurring expenses (e.g., standard travel, standard meal)
- **FR41:** [MVP-1] Employee can upload receipt photos/PDFs attached to expense lines
- **FR41b:** [MVP-1] Slide-over receipt preview via eye icon on each expense line
- **FR42:** [MVP-1] 4-role expense approval workflow: Employee submits → Designated expense approver (often PM) validates project relevance and refacturable flag → Finance Analyst validates GL accounts and tax breakdown → Finance processes payment and export. Each role has distinct actions and screens
- **FR42b:** [MVP-1] PM must designate expense approvers per project at project creation
- **FR42c:** [MVP-1] PM can modify the refacturable flag on expense lines during approval
- **FR42d:** [MVP-1] Finance validates GL accounts, tax breakdown (HT, TPS, TVQ), and can adjust reimbursable amount
- **FR42e:** [MVP-1] Payment processing and export are separate steps from validation
- **FR42f:** [MVP-1] Expense reports grouped by Employee → Project → Category in the Finance view
- **FR43:** [MVP-1] PM or Finance can define per project: whether expenses are refundable to client, which types are refundable, and budget
- **FR43b:** [MVP-1] Refacturable expenses are included in client invoices as a separate section
- **FR44:** [MVP-1] Admin can configure expense categories (travel, meals, supplies, etc.)
- **FR45:** [MVP-1] Finance can generate expense reports by person, project, BU, and period
- **FR46:** [MVP-1] Finance can export expense reports in Intact API import format
- **FR46b:** [MVP-1.5] Finance can reverse (annuler) a previously validated/paid expense with justification. Reversed expenses are marked visually and excluded from future exports. If the expense was refactured to a client, a corresponding credit note line is flagged
- **FR46c:** [MVP-1.5] PM or Finance can reject an expense with a structured reason (non-compliant, missing receipt, wrong project, duplicate, over policy limit). The employee is notified and can correct and resubmit or contest the rejection with a note

### Supplier Payment Tracking

- **FR47:** [MVP-1] 3-role supplier payment workflow: Analyst enters invoice → PM authorizes payment → Analyst validates payment execution
- **FR47b:** [MVP-1] PM views supplier invoices grouped by Project → Subcontractor with slide-over detail
- **FR47c:** [MVP-1] Batch operations for authorizing multiple supplier invoices
- **FR48:** [MVP-1] After PM authorization, Analyst validates that payment has been executed
- **FR49:** [MVP-1] Finance can view all authorized-but-unpaid invoices across projects and mark them as paid
- **FR50:** [MVP-1] Finance can generate cross-project payment reports grouped by supplier
- **FR51:** [MVP-1] PM can view per-subcontractor cumulative invoices vs planned budget per project
- **FR52:** [MVP-1.5] Finance can import subcontractor invoices via Intact API
- **FR52b:** [MVP-1.5] Analyst can register a supplier credit note against a previously recorded invoice. The credit note reduces the cumulative amount for that ST on the project. Budget consumption is recalculated accordingly
- **FR52c:** [MVP-1.5] PM or Analyst can flag a ST invoice as "contested/in dispute" with reason, expected resolution date, and supporting documents. Contested invoices are suspended from payment but remain visible in budget tracking. The system tracks dispute history and resolution
- **FR52d:** [MVP-1.5] Analyst can record a partial payment on a ST invoice with remaining balance tracked. The ST cumulative view shows paid vs authorized vs outstanding
- **FR52e:** [MVP-1.5] PM can manage contractual holdback on ST invoices (percentage-based, similar to client holdback). The system tracks: holdback accumulated, holdback released, holdback remaining per ST per project. Release requires PM authorization
- **FR52f:** [MVP-1.5] Each ST invoice supports multiple document attachments and version history (for amendments to the same invoice reference)

### Service Proposals

- **FR53:** [MVP-1.5] Director, Proposal Manager, or Finance can create a service proposal with code (OFF-YYYY-NNN), title, client, deadline, budget, task checklist, sales rep, public/private classification, and "Create timesheet task" option
- **FR53b:** [MVP-1.5] PM or Director can track competitive positioning on proposals: competitors, win/loss reasons, public vs private classification
- **FR53c:** [MVP-1.5] Team assignment on proposals with estimated hours, visibility-based (only assigned employees see the proposal)
- **FR54:** [MVP-1.5] Lifecycle management: En cours → Soumise → Gagnée / Perdue / Abandonnée → Convertie. Kanban + paginated list view with KPIs (conversion rate, average cost)
- **FR55:** [MVP-1.5] Employee can track time on assigned proposals (always non-billable). Same authorization mechanism as projects
- **FR56:** [MVP-1.5] Convert won proposal to full project: new code (PRJ-YYYY-NNN), template selection, potential client change (alert if different). Coherent with 4-step wizard and consortium flow. Proposal closed with "converted" status and link to project
- **FR57:** [MVP-1.5] Commercial reporting: conversion rate, average cost per proposal (hours and $), project acquisition cost, lost proposal costs
- **FR58:** [MVP-1.5] Active proposals displayed on PM/Director dashboard with status and submission deadline countdown

### Consortium Management

- **FR59:** [MVP-1.5] Finance can create a consortium entity with: name, client (donneur d'ouvrage — must exist in client registry), PR role (mandataire/partner), contract reference. Members are selected from a shared "External Organizations" registry (same table as subcontractors). Each member has a single coefficient (%) totaling 100%
- **FR59b:** [MVP-2] Profit-sharing rules: type of clause (fixed or variable), measurement modes (effort in hours, effort in $ facturation, contractual coefficient — all three can be active simultaneously), trigger threshold, evaluation frequency
- **FR59c:** [MVP-2] Profit-sharing rules can be defined at consortium level or per project (override coefficients, clause type, threshold, modes)
- **FR60:** [MVP-1.5] Finance can associate multiple projects to a consortium. Projects linked from project creation wizard (step 1, consortium flag) with option to inherit or override rules
- **FR61:** [MVP-1.5] Dual financial perspective: consortium view (client revenue, member costs, margin) and Provencher view (invoices issued + profit share = CA). Comparative table shows all 3 measurement modes per partner
- **FR62:** [MVP-1.5] System excludes consortium client revenue from Provencher's CA — only invoices issued to consortium + profit share count. Consortium invoices client; PR invoices consortium
- **FR62b:** [MVP-1.5] Subcontractors can invoice consortium directly or via PR. System distinguishes "ST consortium" from "ST via PR" in all views
- **FR63:** [MVP-1.5] BU Director consortium recap dashboard with projects, ratios, progress, outstanding client invoices
- **FR64:** [MVP-1.5] Finance enters partner invoices grouped by Project → Partner. Each shows phase, amount, source (manual/API), status
- **FR64a:** [MVP-1.5] Finance can record basic profit distributions per consortium project: date, amount per member, justification note. No guided workflow or automated calculation (MVP-2) — simple manual entry to avoid Excel tracking during MVP-1.5
- **FR64b:** [MVP-2] Import existing consortium data via Excel template with validation
- **FR64c:** [MVP-2] Profit distribution guided workflow: Step 1 — Financial statement at date, Step 2 — Cash flow (bank, receivables, payables, tax provision, working capital reserve), Step 3 — Distributable margin, Step 4 — Parameters (mode, amount, period), Step 5 — Calculated allocation with editable adjusted amounts. Justification note required
- **FR64c2:** [MVP-2] Distribution 2-level approval: Associate in Charge via app + each partner confirmed by Analyst (notification button, confirmation outside app). Workflow: Draft → Associate approves → Partners confirm → Payments
- **FR64d:** [MVP-2] Effort-vs-coefficient alerts with monthly/quarterly/annual/since-start evolution. Reports exportable PDF/Excel on custom periods
- **FR64e:** [MVP-2] Treasury/Cash tab: bank balance (receipts - disbursements - adjustments), working capital, monthly cash flow, payment capacity prioritizing: 1) ST, 2) Partners, 3) Tax provision, 4) Working capital reserve, 5) Distributions
- **FR64f:** [MVP-1.5] Consortium-to-client invoices following 7-column structure (FR30) with global budget, consortium-specific annexes
- **FR64g:** [MVP-2] Manual treasury adjustments (bank fees, interest, corrections) with audit trail. Categories configurable
- **FR64h:** [MVP-1.5] "ST consortium" tab: register, track, authorize ST invoices to consortium. Distinguishes "ST consortium" vs "ST via PR" (read-only)
- **FR64i:** [MVP-1.5] Per-project financial synthesis: dual KPIs (consortium global vs PR share), member breakdown, ST consumption bars. Partner costs "n/d"
- **FR64j:** [MVP-1.5] Budget tab: global budget by phase/task with columns per partner (coefficient-based) + ST consortium. PR highlighted, partners grey
- **FR64k:** [MVP-2] Tax declarations at consortium level (consolidating all projects). Frequency config (monthly/quarterly/annual), tax numbers. Editable adjustment column. Workflow: To prepare → Confirmed → Remitted
- **FR64l:** [MVP-2] Tax declaration history with period, projects, adjustments, total remitted, status
- **FR64m:** [MVP-2] Automated fiscal compliance analysis: concordance sales/TPS/TVQ, CTI/RTI vs invoices, unclaimed credits detection, timeliness, cumulative variance, provision vs actual, adjustment coherence. Exportable PDF

### User & Access Management

- **FR65:** [MVP-1] User can authenticate via SSO Microsoft Entra ID (OIDC/SAML 2.0) with automatic user provisioning. No local passwords
- **FR66:** [MVP-1] Admin can assign roles with granular permissions: Employee, PM, Associé en charge (Project Director), Dept. Assistant, Finance/Controller, Paie, Associate/BU Director, Proposal Manager, Admin *(Updated v1.1.012 — added PAIE role)*
- **FR66b:** [MVP-1] The PAIE (Payroll) role is the 9th RBAC role, responsible for: (1) third-level timesheet validation after Finance approval, (2) running and reviewing 11 automated payroll controls per employee per week, (3) bulk or individual validation/rejection of timesheets, (4) period freeze management (setting global freeze dates), (5) period unlock for late corrections. The PAIE role has no access to billing, project creation, or expense approval. *(Added v1.1.012)*

- **FR66c:** [MVP-1] Complete role list with primary responsibilities *(Added v1.1.012)*:

| Role | Key Responsibilities |
|---|---|
| EMPLOYEE | Time entry, expense submission, view own data |
| PM | Project management, first-level time approval (per-entry), expense approval, budget tracking |
| PROJECT_DIRECTOR | Invoice approval, project oversight, financial performance |
| BU_DIRECTOR | BU-level reporting, personnel lending, executive dashboards |
| FINANCE | Billing, second-level time approval, expense validation, period management, Intact export |
| PAIE | Third-level time validation, payroll controls, period freeze/unlock |
| DEPT_ASSISTANT | Clerical support for PMs, delegation-based access |
| PROPOSAL_MANAGER | Service proposal lifecycle |
| ADMIN | System configuration, user management, data migration, full access |

- **FR67:** [MVP-1] System enforces role-based visibility on salary cost data: real salary costs restricted to Finance/Direction/Project Director via PostgreSQL RLS
- **FR68:** [MVP-1] System maintains a complete audit trail on all modifications to critical entities (financial transactions, time corrections, budget changes, leadership role changes)
- **FR69:** [MVP-1] Any role holder can delegate their tasks and permissions to another person for a defined scope and period
- **FR70:** [MVP-1] System grants the delegate the delegator's permissions for the delegated scope only, with full audit trail of actions taken as delegate
- **FR71:** [MVP-1] Dept. Assistant can perform clerical project tasks for PMs and handle invoicing tasks by delegation from Finance

### Dashboards & Reporting

- **FR72:** [MVP-1] Employee can view a personalized home dashboard based on their role (Employee → timesheets, PM → project health, Finance → billing, Director → executive KPIs, Admin → system health)
- **FR73:** [MVP-1] PM can view financial KPIs: carnet de commandes, CA/salary ratio (standard and real where authorized), billing rate, margin per project
- **FR74:** [MVP-1] Finance can generate hours reports by project, person, BU, and period with billable/non-billable breakdown
- **FR75:** [MVP-1] Admin can view system health metrics: response times, error rates, adoption by BU

### Localization & Regional Configuration

- **FR76:** [MVP-1] Application is fully bilingual French/English with user-selectable language preference
- **FR76b:** [MVP-1] All user-facing strings are externalized in translation files (Vue I18n) — no hardcoded text
- **FR77:** [MVP-1] System renders all dates, numbers, and currency amounts through locale-aware formatters
- **FR78:** [MVP-1] Admin can configure HR labor rules per jurisdiction: standard work week, overtime thresholds, holiday calendar, vacation accrual, pay period
- **FR79:** [MVP-1] System automatically flags overtime based on jurisdiction rules and highlights non-working days in the timesheet grid
- **FR80:** [MVP-1] Admin can configure expense policies per jurisdiction: per diem rates, mileage rates, refundable categories, tax rules
- **FR81:** [MVP-1.5] Finance can set invoice currency per client or project with exchange rate management
- **FR82:** [MVP-1.5] System displays dual currency amounts on financial screens when invoice currency differs from base currency
- **FR83:** [MVP-1] Admin can configure BUs, position reference list (31 profiles), project templates, invoice formats, and tax settings through the admin interface
- **FR84:** [MVP-1] Admin can import ChangePoint data: projects, WBS, time entries, and billing history (10+ years)
- **FR85:** [MVP-1] System validates data migration integrity and generates automated reconciliation reports for manual correction of inconsistencies
- **FR85b:** [MVP-1] System supports a parallel run period (minimum 1 full billing cycle) where both ChangePoint and ERP operate simultaneously. During parallel run: timesheets are entered in ERP only (ChangePoint read-only), invoices are produced in both systems for comparison, a daily reconciliation report highlights discrepancies between the two systems. Finance sign-off on reconciliation is a go-live gate. A documented rollback plan allows reversion to ChangePoint within 48h if critical issues are discovered

### Client Management

- **FR86:** [MVP-1] Admin or Finance can manage clients via a 5-tab interface: Identification (name, legal entity, alias/acronym with duplicate detection), Contacts (with roles and language preference), Addresses (including multiple billing addresses), Billing Parameters (templates, payment terms, tax settings), CRM (Associé en charge, notes, relationship history)
- **FR86b:** [MVP-1] Automatic duplicate detection on client creation based on name similarity and alias
- **FR86c:** [MVP-1] Each client has a unique alias/acronym, searchable across the application
- **FR86d:** [MVP-1.5] Client group membership — ability to link related clients (e.g., subsidiaries, divisions)
- **FR86e:** [MVP-1] Client contacts are selectable when creating projects (for correspondence, invoice delivery)
- **FR87:** [MVP-1] System maintains per-client financial history: total CA generated, invoices outstanding, payment history, and linked projects
- **FR88:** [MVP-1] Client records are linked to projects and invoices; creating a project auto-links the selected client
- **FR88b:** [MVP-1] Admin or Finance can manage an "External Organizations" registry (organizations externes) used for both subcontractors and consortium partners. Each organization has: name, NEQ, address, contacts, banking info, and type tags (can be ST on one project and Partner on another). Deduplication check on creation. The same registry is used by: ST management (FR9, FR47), consortium member selection (FR59), and proposal competitor tracking (FR53b). This avoids duplicate entries when the same firm plays different roles across projects

### Notification Center

- **FR89:** [MVP-1] System provides a centralized notification center (bell icon with badge count) aggregating actionable items from all modules: pending approvals, overdue timesheets, invoice milestones, budget alerts, delegation requests
- **FR90:** [MVP-1] Each user's dashboard displays an "Actions requises" section showing pending items requiring their attention, grouped by urgency and module
- **FR91:** [MVP-1] Users can configure notification preferences per event type and per channel (in-app, email, or both)
- **FR92:** [MVP-1] Admin can broadcast system-wide announcements visible to all users or filtered by role/BU

### Data Operations & Administration

- **FR93:** [MVP-1.5] Admin can perform bulk imports of master data (clients, contacts, organizations, WBS templates, rate grids) via standardized Excel/CSV templates with validation, error reporting per row, and dry-run preview before commit
- **FR94:** [MVP-1.5] Admin can export any list or report view to Excel/CSV with current filters applied. All major tables (projects, clients, invoices, timesheets, expenses, ST invoices) support bulk export
- **FR95:** [MVP-2] Admin can configure data retention and archival policies: projects archived after X months of "Completed" status, timesheets older than Y years moved to cold storage, configurable per entity type. Archived data is excluded from active queries but accessible via dedicated archive search
- **FR96:** [MVP-2] Admin can purge archived data according to legal retention requirements (configurable minimum retention period per data type). Purge operations require double confirmation and create an irreversible audit log entry
- **FR97:** [MVP-2] All bulk operations (import, export, archive, purge) are logged in a dedicated operations journal with: operation type, user, timestamp, record count, status (success/partial/failed), and downloadable error report

### Financial Operations

- **FR98:** [MVP-2] Finance can record year-end adjustment entries (ecritures de regularisation) at project or consortium level with: date, description, debit/credit accounts, amount, justification. These entries are flagged as "adjustment" and excluded from operational reporting but included in financial statements
- **FR99:** [MVP-2] Finance can perform bank reconciliation at consortium level: import bank statement (CSV/OFX), match transactions to recorded payments/receipts, flag unmatched items for investigation. Reconciliation status per period (matched, partial, pending)

---

## Non-Functional Requirements

### Performance

- **NFR1:** [MVP-1] All primary screens load in < 2 seconds
- **NFR2:** [MVP-1] Draft save completes in < 500ms with visual confirmation
- **NFR3:** [MVP-1] CA/Salary ratio and % advancement recalculate in < 1 second
- **NFR4:** [MVP-1] Standard reports generate in < 5 seconds
- **NFR5:** [MVP-1] Project and employee search results appear in < 500ms
- **NFR6:** [MVP-1] Complete billing dossier generates in < 30 seconds

### Security

- **NFR7:** [MVP-1] SSO via Microsoft Entra ID (OIDC/SAML 2.0) — no local passwords
- **NFR8:** [MVP-1] All data encrypted in transit (TLS 1.3) and at rest (AES-256)
- **NFR9:** [MVP-1] Real salary costs accessible only to Finance/Direction via PostgreSQL RLS
- **NFR10:** [MVP-1] All CUD operations on financial entities logged with user, timestamp, old/new values
- **NFR11:** [MVP-1] Automatic timeout after 30 min inactivity. Concurrent session limit per user
- **NFR12:** [MVP-1] All endpoints authenticated via JWT with role-based authorization

### Scalability

- **NFR13:** [MVP-1] 400+ simultaneous users with < 10% degradation during peak (Monday 8-10 AM)
- **NFR14:** [MVP-1] 10+ years historical data with no degradation on current-period queries
- **NFR15:** [MVP-1] Architecture supports 2x user growth (800 users) without redesign
- **NFR16:** [MVP-1] Time entry tables partitioned by period for query performance at scale

### Reliability

- **NFR17:** [MVP-1] 99.5% availability during business hours (Mon-Fri 7:00-19:00 ET)
- **NFR18:** [MVP-1] Automated daily backups with point-in-time recovery. RPO < 1 hour, RTO < 4 hours
- **NFR19:** [MVP-1] Core operations continue if Intact API or Entra ID temporarily unavailable (graceful degradation)

### Data Integrity

- **NFR20:** [MVP-1] 100% data integrity validation on ChangePoint migration with automated reconciliation reports

### Accessibility & UI

- **NFR21:** [MVP-1.5] WCAG 2.1 Level AA compliance (keyboard navigation, screen reader support, color contrast)
- **NFR22:** [MVP-1] Full functionality on desktop 1280px+. Read-only capability on tablet 1024px+

### Integration

- **NFR23:** [MVP-1] CSV/Excel export generates valid, importable files with zero formatting errors
- **NFR24:** [MVP-1.5] Bidirectional Intact API sync handles versioning and error recovery
- **NFR25:** [MVP-1] Entra ID supports auto-provisioning/deprovisioning with group-based role mapping
- **NFR26:** [MVP-1] Excel imports validate format and content with clear error messages before processing

### Documentation

- **NFR27:** [MVP-1] Auto-generated OpenAPI 3.0 specification via drf-spectacular, always synchronized with code

### Testing

- **NFR28:** [MVP-1] Minimum 80% test coverage on backend business logic (billing, permissions, workflows)

### Deployment

- **NFR29:** [MVP-1] Zero-downtime deployment via Docker with rolling updates

### Configuration

- **NFR30:** [MVP-1] Templates, formats, categories, positions, tax settings, and other operational parameters are configurable without code changes

### Concurrency

- **NFR31:** [MVP-1] Optimistic locking on all financial entities (invoices, budgets, timesheets, ST invoices, expenses). If two users edit the same record simultaneously, the second save displays a conflict warning showing the other user's changes, with options to reload or force-save. No silent overwrites
- **NFR32:** [MVP-1] Real-time presence indicator on invoice preparation and project budget screens: "Currently being edited by [user]" with timestamp. WebSocket-based for immediate feedback

---

## Implementation Status (Updated 2026-04-07)

### Version: v1.2.000 — Commit efd3c5e

### Bloc 1 — Projets (~95% complete)

| Feature | FR | Status |
|---------|-----|--------|
| Project CRUD + WBS Option B (Phase→Task) | FR1-FR10 | ✅ Implemented |
| Templates (7 phases, 23 tasks) | FR1e | ✅ Implemented |
| Project wizard 5 steps (ST, consortium) | FR1-FR10 | ✅ Implemented |
| Client management (5-tab) | FR1 | ✅ Implemented |
| Consortium entity + members + vue duale | FR59-FR62 | ✅ Implemented |
| Consortium 6 onglets (overview, dual, projets, factures, distributions, taxes) | FR59-FR64 | ✅ UI complete (data placeholders for financial tabs) |
| Sub-tasks (3 levels WBS) | FR1e | ✅ Implemented |
| Transfer responsable (PM/Associate) | FR15d | ✅ Implemented |
| Gantt interactif (phases, zoom, milestones) | FR1e/US-PL06 | ✅ Implemented |
| Phase dependencies (FS/SS) | US-PL06 | ✅ Model + API |
| Public/Privé, Services transversaux | FR10 | ✅ Implemented |

### Bloc 2 — Cycle de Production (~90% complete)

| Feature | FR | Status |
|---------|-----|--------|
| Timesheet grid by task (WBS) | FR16-FR19 | ✅ Implemented |
| 3-level approval (PM/Finance/Paie) | FR21-FR22c | ✅ Implemented |
| 11 payroll controls | FR27j-FR27l | ✅ Implemented |
| Period locking (freeze + unlock) | FR27f-FR27i | ✅ Implemented |
| Dynamic contract hours (labor_rule) | FR78 | ✅ Implemented |
| Reminders Wed/Fri + PM escalation | FR26 | ✅ Celery tasks |
| Retrospective corrections (Finance) | FR25 | ✅ bulk_correct API |
| Hours transfer between projects | FR27d | ✅ transfer_hours API |
| Leave types (7 Québec standard) | Module J | ✅ Implemented |
| Leave request workflow + bank | Module J | ✅ Implemented |
| Auto-create TimeEntry on leave approval | Module J | ✅ Implemented |
| Suppliers/ST 6 entities fully exposed | FR47-FR52 | ✅ Implemented |
| Batch authorize + disputes + holdbacks | FR47c | ✅ Implemented |
| Resource allocation + load alerts | US-PL01/PL11 | ✅ Implemented |
| Milestones + auto-overdue detection | US-PL07 | ✅ Implemented |
| Availability generation (contract - leaves) | US-PL03 | ✅ Implemented |

### Bloc 3 — Cycle Financier (~85% complete)

| Feature | FR | Status |
|---------|-----|--------|
| Configurable tax schemes (6 standard) | FR83 | ✅ Implemented |
| Dynamic tax calculation (TPS, TVQ, TVH, TVA, PST, Exonéré) | FR83 | ✅ Implemented |
| Invoice 7-column structure | FR30 | ✅ Implemented |
| Invoice workflow (Draft→Submit→Approve→Send→Paid) | FR30-FR35 | ✅ Implemented |
| Credit notes, payments, holdbacks, write-offs | FR36-FR39 | ✅ Implemented |
| Expense workflow (6 steps) + receipt upload | FR40-FR46 | ✅ Implemented |
| 15 expense categories seeded | FR40 | ✅ Implemented |
| Intacct Phase 1 CSV exports (4 types) | FR84 | ✅ Implemented |

### Bloc 4 — Pilotage (~80% complete)

| Feature | FR | Status |
|---------|-----|--------|
| Role-based dashboards (5 roles) | FR72 | ✅ Implemented |
| PM KPIs (CA/salary ratio, billing rate, carnet) | FR73 | ✅ Implemented |
| Hours reports (by project/employee/BU) | FR74 | ✅ Implemented |
| System health metrics | FR75 | ✅ Implemented |
| Import 13 types (6 ref + 7 transactional) | FR84/FR93 | ✅ Implemented |
| Route guards (RBAC on frontend routes) | FR72 | ✅ Implemented |

### Sprint 3-4 — Planned: Full ABAC (Attribute-Based Access Control)

**Status:** Planned (not started) — Estimated 15-20 days (2 sprints)
**Source:** Brainstorming session 2026-04-11, Proposition C
**Tech Spec:** `_bmad-output/tech-specs/tech-spec-sidebar-quick-win-2026-04-11.md` (section Sprint 3-4)
**Brainstorming:** `_bmad-output/brainstorming/brainstorming-session-2026-04-11-200000.md` (ideas #19-#24, #36)

| ID | Feature | Brainstorming Idea | Description | Effort |
|----|---------|-------------------|-------------|--------|
| C1 | PermissionMatrix model | #20 | CRUD matrix per module × action (CRUD + Approve + Export) × scope (global/BU/project). Replaces fixed ProjectRole progressively | 5 days |
| C2 | Reusable permission profiles | #21 | Templates: "Assistante BU type 1", "PM + delegation factures". Admin assigns profile + individual overrides | 2 days |
| C3 | Temporary permissions with auto-expiry | #22 | Expiry date on permissions. Celery daily task deactivates expired permissions | 1 day |
| C4 | Admin "Permissions" page | #23 | Visual matrix 16 modules × 6 actions × 3 scopes. Profile drag-drop, filter by user/module | 3 days |
| C5 | "Effective permissions" audit view | #23 | Tab on user profile: preview effective menu ("View as"). Icons per action | 2 days |
| C6 | App Selector mode (multi-hat) | #36 | Dropdown top of sidebar: "Mode PM" / "Mode Architecte". Switches entire menu | 2 days |
| C7 | DEPT_ASSISTANT full mirror mode | #19 | Sophie sees the menu of PM(s)/Director(s) she assists. Toggle to switch "mirror" | 3 days |
| C8 | Per-project permission override | #24 | Marie = EMPLOYEE globally but "Sub-PM" on a specific project. Override at project level | 2 days |

**Dependencies:**
- Sprint 1 (role-adaptive sidebar) ✅ Completed
- Sprint 2 (smart adaptive UX) ✅ Completed
- Migration strategy: existing ProjectRole must be translated to PermissionMatrix without breaking access

**What it unlocks:**
- Sophie (DEPT_ASSISTANT): full mirror mode instead of current hybrid menu
- Total flexibility: admin configures any permission combo without code changes
- Multi-hat: Jean-François can switch between "PM mode" and "Architect mode"
- Audit: visualize exactly what each user sees (support simplification)
- SaaS readiness: ABAC model is the foundation for Phase 2 multi-tenant

### Deferred to MVP-2

| Feature | FR | Notes |
|---------|-----|-------|
| Intacct Phase 2-3 (bidirectional API) | FR84 | API sync not started |
| ChangePoint full migration (10+ years) | FR84-FR85 | Command exists, reconciliation needed |
| Service proposals lifecycle | FR53 | Not started |
| Consortium variable profit-sharing rules | FR59b-FR59c | Model needed (3 modes, threshold, frequency) |
| Advanced Gantt (drag-drop, critical path) | US-PL06 | Current: form-based date editing |
| WebSocket real-time lock refresh | NFR32 | Polling only |
| Parallel run reconciliation (ChangePoint vs ERP) | FR85b | Not started |
| Import absences from HRIS | FR27b | Leave model ready, import handler needed |
| Auto-expiry PeriodUnlock | FR27c | Model ready, Celery task needed |

### UX Improvement History (2026-04-11)

**Brainstorming session:** 43 ideas generated across 5 themes (Personnalisation, Action-driven, ABAC, Architecture sidebar, Vocabulaire)
**Mockup:** `_bmad-output/mockups/flux/sidebar-quick-win-personas.html` — 9 personas with full dashboards

| Sprint | Proposition | Status | Commit | Key deliverables |
|--------|-------------|--------|--------|------------------|
| Sprint 1 | A — Quick Win Sidebar | ✅ Completed | 2ac52d2 | useSidebarMenu composable, 9 role menus, contextual logo PR\|Production/Direction/Finance/Paie/Admin, 70+ i18n keys, Mon/Ma/Mes prefixes |
| Sprint 1+ | Dashboard + Pages Employee | ✅ Completed | f75338c | STApprovalQueue (PM), EmployeeProjectView, dashboard previsionnel semaine, conges KPI |
| Sprint 2 | B — Smart Adaptive UX | ✅ Completed | 570893f | Cmd+K search, Action Center "A faire", collapsible sections, badges/health/freshness, favorites API |
| Sprint 3-4 | C — Full ABAC | Planned | — | PermissionMatrix, profiles, auto-expiry, admin page, mirror mode, app selector |

### Test Coverage

- **361 backend tests** (pytest) — all passing
- **357+ visual tests** documented in `tests_visuels/plan_tests_complet_v3.xlsx` (13 tabs) + `plan_tests_master_v2.xlsx` (17 tabs)
- **58 UX tests** added for Sprint 1+2 in `plan_tests_master_v2.xlsx` (SB-001→SB-014, CK-001→CK-006, AC-001→AC-006, SC-001→SC-003, BG-001→BG-003, HI-001→HI-002, FV-001→FV-002)
- Last full QA report: 361 PASS (backend), 4 bugs fixed (BUG-001→004), 3 PARTIAL resolved
