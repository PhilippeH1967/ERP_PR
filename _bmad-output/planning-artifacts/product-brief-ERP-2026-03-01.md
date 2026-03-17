---
stepsCompleted: [1, 2, 3, 4, 5, 6]
status: complete
inputDocuments:
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
  - "Analyse EPIC Logiciele Existants/ChangePoint/CHANGEPOINT_EPIC_Projets.md"
  - "Analyse EPIC Logiciele Existants/ChangePoint/CHANGEPOINT_EPIC_FeuillesDeTemps.md"
  - "Analyse EPIC Logiciele Existants/ChangePoint/CHANGEPOINT_EPIC_Facturation.md"
  - "Analyse EPIC Logiciele Existants/ChangePoint/CHANGEPOINT_Analyse_Projets_WBS_Facturation.md"
  - "Analyse EPIC Logiciele Existants/ChangePoint/CHANGEPOINT_UX_Recommandations.md"
  - "ConfigTechSouhaitée"
date: 2026-03-01
author: Philippe
---

# Product Brief: ERP

<!-- Content will be appended sequentially through collaborative workflow steps -->

## Executive Summary

ERP is a custom-built project management and business operations platform designed specifically for a 400-person architecture firm currently constrained by an aging, unintuitive PSA tool (Planview ChangePoint) supplemented by scattered Excel spreadsheets. The platform consolidates project management, time tracking, invoicing, financial oversight, resource planning, expense management, and business development into a single, modern, AI-assisted application — purpose-built for the workflows, contract types, and organizational structure of a multi-entity architecture practice.

The solution draws functional inspiration from two reference applications — ChangePoint (for its depth in project structure, WBS hierarchy, multi-entity billing, and contract management) and OOTI (for its modern UX, opportunity pipeline, and architecture-specific design) — while surpassing both through superior usability, integrated AI assistance, native accounting integration (Intact/Sage), mobile field capabilities, OCR expense processing, and a tailored fit to the firm's specific operational needs. The platform is designed with future SaaS commercialization in mind (Phase 1: internal use, Phase 2: multi-tenant product for architecture firms).

---

## Core Vision

### Problem Statement

A 400-person architecture firm managing hundreds of concurrent projects across multiple legal entities (Provencher_Roy Prod, PRAA) is severely hampered by its current tooling. The primary system — Planview ChangePoint — suffers from a rigid, unintuitive interface that creates daily friction: timesheets are hard to read and slow to complete, project forecasting tools are difficult to use, the invoicing workflow is overly complex, expense reporting is problematic, and basic corrections (such as changing a client on a project) are impossible once set. As a result, project managers and employees spend excessive time fighting the tool instead of managing projects, and critical processes — financial tracking, team planning, invoice creation — have migrated to disconnected Excel spreadsheets.

### Problem Impact

- **For 400 employees**: Time entry is tedious and slow, leading to incomplete or delayed timesheets that directly impact billing accuracy and project profitability tracking. Field architects on construction sites have no mobile access for time or expense entry.
- **For project managers**: Lack of clear forecasting and planning tools forces reliance on Excel, creating information silos, version control issues, and an inability to manage projects effectively within a single system. No AI-assisted detection of scope creep or budget overruns.
- **For associates and directors**: No consolidated real-time view of project financial health, margins, CA/salary ratios, and resource utilization — strategic decisions are made on stale or incomplete data across disconnected spreadsheets.
- **For administration and finance**: Invoice creation is unnecessarily complex with 10+ distinct billing formats, subcontractor tracking is fragmented with no Purchase Order management, financial reporting requires manual consolidation from multiple sources, and data must be manually re-entered into the Intact (Sage) accounting system. CPI indexation on multi-year contracts is handled manually.
- **For the firm overall**: The gap between what the tools provide and what the firm needs results in disorganized workflows, lost productivity across all levels, and an inability to scale operations efficiently or commercialize operational expertise.

### Why Existing Solutions Fall Short

**ChangePoint** provides deep project structure capabilities (WBS hierarchy, multi-entity billing, contract management) but fails on usability. Its interface is rooted in legacy PSA design — dense, rigid, and unforgiving of errors. It was not conceived for architecture-specific project management and lacks modern UX patterns that employees expect in 2026. It has no mobile capabilities, no AI assistance, no OCR processing, limited integration with external accounting systems, and no support for architecture-specific contract types (forfaitaire, consortium, co-développement, conception-construction).

**OOTI** offers a more modern, visually appealing interface with architecture-specific modules (opportunities, proposals, architecture project phases) but has not been adopted. While more complete in some areas (opportunity pipeline, cleaner design), it remains a commercial off-the-shelf product that cannot be tailored to the firm's specific multi-entity structure, dual salary costing model, 10+ invoice formats, CPI indexation requirements, or internal processes.

**Excel** fills the gaps left by both — financial tracking, team planning, invoice preparation, resource allocation — but introduces fragmentation, manual errors, lack of real-time visibility, and zero collaboration capability.

No single existing solution combines the depth of ChangePoint, the modern UX of OOTI, native integration with Intact (Sage) accounting, AI-powered project intelligence, mobile field capabilities, and the operational specificity the firm requires.

### Proposed Solution

A custom-built ERP platform using a modern technology stack (Django 5.0 + Vue 3 + TypeScript + PostgreSQL 16) that:

1. **Replaces ChangePoint** as the central project management, time tracking, and invoicing system — with full functional parity on critical workflows (WBS hierarchy, multi-entity billing, contract management) and vastly superior usability.
2. **Eliminates Excel dependency** by providing native financial tracking, team planning, resource allocation, and invoice creation directly within the platform.
3. **Adopts the best of OOTI's design** — modern UX patterns, architecture-specific modules (opportunities, proposals, project phases), clean visual design — while tailoring every workflow to the firm's actual processes.
4. **Integrates AI assistance** across the platform: auto-filling timesheets from calendar/project patterns, predictive RAF (remaining work) in hours, out-of-scope detection for amendment proposals, resource planning suggestions based on historical WBS similarity, proactive alerts on budget and schedule risks, and project health scoring.
5. **Supports architecture-specific contract types** natively — forfaitaire, consortium, co-développement, conception-construction — each with distinct billing, financial tracking, and reporting rules.
6. **Manages complex billing** with 10+ configurable invoice formats per client, complete billing dossiers (invoice + timesheets in client-specific format + subcontractor invoices), and Purchase Order management.
7. **Provides dual salary costing** — standard cost per profile (visible to PMs/direction) and real cost per person (direction/finance only) — with granular role-based permissions and CA/salary ratio as a key KPI.
8. **Supports subcontractor management** with dedicated budgets, Purchase Orders, invoice tracking, and integration into project financials.
9. **Enables mobile field operations** — time entry and expense reporting on construction sites with OCR-powered receipt scanning for automatic expense pre-filling.
10. **Implements 2-level timesheet approval workflow** (project manager → direction/finance) designed for speed and minimal friction across 400 users.
11. **Implements virtual resource profiles** — generic resource archetypes (Chargé de projet, Architecte senior, Technologue junior, etc.) positioned on tasks before assigning real employees, enabling budget estimation, capacity planning, and progressive team assignment with multi-employee allocation and percentage-based hour distribution.
12. **Structures projects on two axes** — sequential realization phases (Étude préparatoire → Concept → Préliminaire → Définitif → Appel d'offres → Surveillance) and transversal support services (Gestion de projet, BIM, 3D, Paysage, Design) as global project-level tasks.
13. **Separates realization and financial layers** — financial phases (defined by Accounting) can group multiple realization phases, with distinct billing modes (fixed-price and hourly) within the same project, dual hourly rates (internal cost vs contractual), and a dedicated invoice preparation screen with CA/Salary ratio tracking.
14. **Tracks supplier payments independently** — 3-state invoice lifecycle (Received → Authorized → Paid) with PM authorization workflow and Accounting payment tracking, fully independent from client billing.
15. **Manages service proposals (offres de services)** — lightweight proto-projects with time tracking and authorization controls, converting to full projects when won with potential client change tracking.
16. **Manages consortium projects** — dedicated consortium entity linking multiple independent projects, with dual financial views (consortium-level vs Provencher-level), member coefficient tracking, profit-sharing calculation per project, and BU Director dashboard with cross-consortium visibility. Consortium revenue is excluded from Provencher CA — only invoices issued to consortium + profit share count.
17. **Manages internal projects** with a lighter task/subtask structure distinct from client projects.
18. **Interfaces with Intact (Sage) accounting software** bidirectionally — invoices, payments, expense reports, and financial data flow seamlessly, eliminating manual double-entry.
19. **Supports multi-currency operations** and semi-automatic CPI indexation for multi-year contracts.
20. **Provides executive dashboards** with real-time KPIs, drill-down capability, and configurable widgets for associates and directors.
21. **Maintains a complete audit trail** on all modifications for compliance and traceability.
22. **Integrates SSO** via Microsoft Entra ID (Microsoft 365) for seamless authentication across the firm.
23. **Includes data migration** from ChangePoint (10+ years of time, project, and billing data).
24. **Is designed for future SaaS commercialization** with multi-tenant architecture (PostgreSQL Row-Level Security) from day one — Phase 1 internal use, Phase 2 product for other architecture firms.

### Key Differentiators

| Differentiator | Description |
|---|---|
| **Purpose-built for architecture firms** | Designed from the ground up for architecture-specific contract types (forfaitaire, consortium, co-dev, conception-construction), project phases, WBS structures, and multi-entity operations |
| **UX-first design** | Modern, intuitive interface inspired by best-in-class SaaS that employees actually want to use — reducing the "fighting the tool" problem, with mobile-optimized field experience |
| **AI-integrated operations** | Intelligent assistance woven into daily workflows: auto-fill timesheets, predictive RAF, out-of-scope detection, proactive budget/schedule alerts, resource planning from historical data |
| **Complex billing engine** | 10+ configurable invoice formats, complete billing dossiers, client-specific timesheet formatting, subcontractor invoice aggregation, Purchase Order management |
| **Dual financial intelligence** | Standard and real salary costing with granular permissions, CA/salary ratio tracking, semi-automatic CPI indexation, executive dashboards with real-time KPIs |
| **Zero Excel dependency** | Every process currently managed in spreadsheets is natively supported with real-time collaboration and AI-assisted analysis |
| **Accounting integration (Intact/Sage)** | Bidirectional synchronization of invoices, payments, expenses, and financial data — eliminating reconciliation overhead |
| **Mobile + OCR** | Field-ready time and expense entry with OCR receipt scanning — no architecture firm ERP offers this combination |
| **Commercialization-ready** | Multi-tenant architecture from day one enables Phase 2 SaaS offering to other architecture firms, with data migration tooling as a competitive advantage |
| **Virtual resource profiles** | Generic resource archetypes enable budget estimation and capacity planning before real staff assignment — with multi-employee allocation and percentage-based hour distribution |
| **Two-axis project structure** | Sequential realization phases + transversal support services (BIM, 3D, etc.) as global project tasks — matching how architecture firms actually organize work |
| **Dual financial layer** | Separate realization (PM) and financial (Accounting) layers with mixed billing modes, dual hourly rates, and 7-column invoice preparation screen with CA/Salary ratio |
| **Supplier payment independence** | 3-state invoice lifecycle with PM authorization, fully independent from client billing — cross-project payment consolidation by supplier |
| **Service proposal pipeline** | Lightweight proto-projects with time tracking, seamless conversion to projects with client change tracking and commercial ROI reporting |
| **Consortium management** | Dedicated consortium entity with multi-project support, dual financial views (consortium vs firm), member coefficient tracking, and profit-sharing calculation — a rare capability in architecture ERPs |
| **Full ownership and control** | Custom-built solution with no vendor lock-in — evolves with the firm's needs and becomes a marketable product |

---

## Target Users

### Organizational Structure

The firm operates with a **matrix organization**: 6 Business Units (organized by geography or specialty) crossed with shared support services (3D, BIM, Sustainable Development, Landscape — with more possible in the future). Two legal entities (Provencher_Roy Prod, PRAA) overlay this structure. Personnel lending between BUs is common, with revenue (CA) from lent staff repatriated to the person's home BU. Support services receive allocated budgets per project but the project manager retains full responsibility for the entire project.

### Primary Users

#### 1. Marc — Chef de projet / Architecte (~50-60 people)

**Profile:** Architect with 8+ years of experience who manages 2-4 projects simultaneously while continuing to practice architecture (design, drawings, site visits). This dual role — practitioner AND manager — is the norm, not the exception.

**Context:** Marc splits his day between design work and project management. He needs to track budgets, plan team resources, monitor RAF, approve timesheets, request support services (3D, BIM), and prepare billing dossiers — all while actively contributing to architectural deliverables. His time for administrative tasks is extremely limited.

**Current Pain:**
- Loses 30-45 minutes daily fighting ChangePoint for time entry, project tracking, and forecasting
- Maintains parallel Excel spreadsheets for financial tracking and team planning because ChangePoint's tools are unusable
- Cannot detect scope creep until it's too late — no proactive alerts or out-of-scope analysis
- Invoice preparation is a multi-hour ordeal assembling billing dossiers manually
- Requesting support resources (3D, BIM) is informal with no visibility on availability

**Success Vision:**
- AI auto-fills his timesheet in under 2 minutes each day
- A single dashboard shows all his projects' health: budget consumed, RAF, CA/salary ratio, upcoming milestones
- Proactive alerts warn him when a project approaches 80% budget on a phase or detects out-of-scope work
- Invoice preparation takes 15 minutes instead of 2 hours — templates auto-populate with the right format per client
- Can request and see availability of support service resources directly in the planning module

#### 2. Sophie — Employé / Architecte (~300 people)

**Profile:** Architect or technician working on 1-3 projects simultaneously. Represents the majority of the 400 employees. Some work primarily in the office, others split time between office and construction sites.

**Context:** Sophie's primary interaction with the ERP is daily time entry and occasional expense reporting. She needs the system to stay out of her way — fast, intuitive, minimal clicks.

**Current Pain:**
- Time entry in ChangePoint is tedious: hard-to-read interface, slow navigation, unclear project/phase assignments
- On construction sites, she has no mobile access — notes time on paper and enters it days later, leading to inaccuracies
- Expense reports require manual data entry with no receipt scanning

**Success Vision:**
- Opens the app, sees her timesheet pre-filled by AI based on her project assignments and calendar — confirms with one click
- On site, snaps a photo of a receipt and the OCR pre-fills the expense report
- Mobile app for time entry works offline and syncs when connected
- Total daily interaction: under 2 minutes

#### 3. Nathalie — Administration / Finance (~5-8 people)

**Profile:** Member of the finance/administration team responsible for invoicing, subcontractor management, PO tracking, payment follow-up, and Intact (Sage) synchronization.

**Context:** Nathalie manages the entire billing cycle — from invoice preparation to client delivery to payment tracking. She handles complex billing dossiers with 10+ formats, manages subcontractor POs and budgets, processes CPI indexation on multi-year contracts, and ensures financial data flows correctly to Intact.

**Current Pain:**
- Assembling billing dossiers is manual: invoice + timesheets in client-specific format + subcontractor invoices
- 10+ invoice formats to manage with no template system
- Subcontractor tracking (budgets, POs, invoices) is scattered across Excel files
- Financial data must be manually re-entered into Intact (Sage) — double entry, risk of errors
- CPI indexation on multi-year contracts calculated manually

**Success Vision:**
- Selects a project, chooses the client's billing template, and the system auto-generates the complete dossier
- Subcontractor budgets and POs are tracked within the project, with alerts on budget consumption
- Invoices sync bidirectionally with Intact — no manual re-entry
- CPI indexation is proposed semi-automatically with one-click application via amendment

#### 4. Isabelle — Assistante de BU (6 people — one per BU)

**Profile:** Business Unit assistant acting as the operational backbone of her BU. Supports associates, directors, and project managers with data entry, report preparation, project creation, and day-to-day administrative follow-up. The most intensive "power user" of the ERP.

**Context:** Isabelle is the go-to person in her BU for anything operational. She creates projects, enters contract data, prepares financial reports, helps PMs who struggle with the tool, tracks missing timesheets and pending approvals, and ensures BU-level processes run smoothly.

**Current Pain:**
- Spends significant time doing data entry that PMs should do but find too difficult in ChangePoint
- Acts as a human bridge between what the tool requires and what the PMs actually do
- Prepares Excel reports that should be available natively in the system
- No standardized process — each BU works differently

**Success Vision:**
- The ERP is intuitive enough that PMs handle most tasks themselves — freeing Isabelle for higher-value work
- Project creation and data entry are streamlined with templates and smart defaults
- BU-level dashboards and reports are available with one click — no manual Excel assembly
- Evolves into a "key user" who configures workflows and templates, with advanced features like custom reports and the ability to assist PMs remotely

#### 5. Éric — Spécialiste service support (~20-30 people across 3D, BIM, Sustainable Development, Landscape)

**Profile:** Specialist working across multiple projects from multiple BUs simultaneously. May work on 5-10 projects at any given time — significantly more than a typical architect.

**Context:** Éric's time is a shared resource allocated across BUs. He receives work requests from project managers, delivers specialized outputs (3D renderings, BIM models, sustainability analyses, landscape designs), and tracks his time against allocated budgets per project.

**Current Pain:**
- Multi-project time entry is tedious when working on 5-10 projects daily
- No visibility on his own workload forecast or upcoming commitments
- Budget consumption for his services is tracked in Excel by his manager

**Success Vision:**
- Time entry interface optimized for high multi-project volume — favorites, quick-switch, AI suggestions
- Can see his own assignment schedule and upcoming project commitments
- Understands how much budget remains for his services on each project

### Secondary Users

#### 6. Pierre — Associé / Directeur (~6-10 people)

**Profile:** Partner/director overseeing a portfolio of 10-20+ projects across one or more BUs. Makes strategic decisions, drives business development, participates in opportunity qualification and go/no-go decisions, and defines WBS structures on projects he leads.

**Current Pain:**
- No consolidated view of project portfolio health — must ask PMs or review Excel files
- Business development tracked informally — no pipeline visibility
- CA/salary ratios and utilization metrics calculated manually, often outdated

**Success Vision:**
- Executive dashboard shows portfolio health at a glance: projects in green/yellow/red, overall margins, utilization rates
- Opportunity pipeline with stages, win probability, and projected revenue
- Drill-down from portfolio to project to phase with progressive detail
- AI-powered alerts flag projects requiring attention before they become critical

#### 7. François — Développement des affaires (~2-4 people + associates)

**Profile:** Dedicated business development professional working alongside associates to identify, pursue, and convert opportunities into projects. Manages the pipeline from lead detection through proposal to contract signature.

**Current Pain:**
- No centralized opportunity tracking — uses email, Excel, and personal notes
- No visibility into pipeline health, conversion rates, or projected revenue
- Disconnect between opportunity won and project creation — manual handoff

**Success Vision:**
- Full opportunity pipeline with customizable stages, probability scoring, and revenue projections
- Seamless transition from opportunity to project creation upon contract signature — WBS defined by the associate/PM who led the proposal
- Historical proposal database for reference and reuse

#### 8. Luc — Contrôleur de gestion (~2-3 people)

**Profile:** Financial controller with a configurable scope of visibility — may oversee specific associates, specific BUs, or the entire firm. Primary consumer of financial analytics and reporting.

**Context:** Luc doesn't create much data but analyzes it intensively. His interface is oriented around reports, dynamic filters, cross-tabulations, and exports. He navigates by dimension of analysis (BU, period, contract type, associate) rather than by individual project.

**Current Pain:**
- Financial analysis requires manual consolidation from ChangePoint, Excel, and Intact
- No real-time visibility on firm-wide or BU-level financial health
- Report generation is manual and time-consuming
- Cannot easily compare profitability across BUs, contract types, or time periods

**Success Vision:**
- Integrated BI-lite reporting module with combinable filters (BU + period + contract type + associate)
- Real-time KPIs: profitability by project/phase/BU/entity, CA/salary ratios, utilization rates, RAF consolidations
- Interactive charts with drill-down, exportable to Excel
- Saveable and shareable report configurations
- Configurable visibility scope matching his oversight perimeter

#### 9. Catherine — Responsable service support (~4 people — one per service)

**Profile:** Manager of a shared support service (3D, BIM, Sustainable Development, or Landscape). Manages team allocation across projects from all BUs, monitors budget consumption, and arbitrates competing resource requests.

**Current Pain:**
- Team workload tracked in Excel with no real-time visibility
- Resource requests arrive informally (email, chat, hallway conversations)
- No way to see the full picture of team capacity vs. demand across all BUs
- Budget tracking per project is manual

**Success Vision:**
- Capacity planning dashboard showing team workload, availability, and upcoming commitments
- Formal resource request workflow from PMs with visibility on availability
- Budget consumption alerts per project — proactive notification when a project approaches its allocated support budget
- View of lent/borrowed personnel and impact on team capacity

#### 10. Daniel — Administrateur système (1-2 people)

**Profile:** IT administrator responsible for SSO configuration (Azure AD), user management, role-based permissions, audit trail oversight, system monitoring, and data migration from ChangePoint.

**Success Vision:**
- SSO via Azure AD with automatic user provisioning
- Granular role-based permissions configurable through an admin interface — including sensitive data access controls (real salary costs)
- Audit trail accessible for compliance reviews
- Monitoring dashboard for system health

### Interaction Levels

The 10 personas map to 3 distinct UX interaction levels that should guide interface design:

| Level | Personas | Population | Daily Time in ERP | Design Priority |
|---|---|---|---|---|
| **1 — Minimal** | Sophie, Éric | ~330 | 2-5 min | Speed, simplicity, mobile, AI auto-fill |
| **2 — Operational** | Marc, Isabelle, Nathalie, Catherine | ~70 | 15 min - full day | Efficiency, contextual dashboards, workflows |
| **3 — Strategic** | Pierre, François, Luc | ~15 | 10-30 min | Visibility, analytics, drill-down, pipeline |

*Daniel (System Admin) operates at a separate maintenance/configuration level with infrequent but deep interactions.*

### User Journey

#### Discovery & Onboarding (Internal Deployment)

| Phase | Experience |
|---|---|
| **Announcement** | Firm-wide communication that the new ERP replaces ChangePoint — emphasis on ease of use and AI assistance |
| **Training** | Role-based: 10 min for employees (time/expenses), 30 min for support specialists (multi-project), 2 hours for PMs (full project management), 1 hour for finance (billing + Intact), half-day for BU assistants (power user) |
| **First Week** | AI learns from ChangePoint historical data to pre-fill timesheets. Employees experience the "magic moment" when their timesheet appears pre-filled correctly |
| **First Month** | PMs discover they can manage projects without Excel. Finance completes first invoice cycle end-to-end with Intact sync. BU assistants configure their first report templates |
| **Ongoing** | AI improves predictions over time. System becomes indispensable as historical data builds. Progressive feature discovery through contextual onboarding |

#### Key "Aha!" Moments by Persona

| Persona | "Aha!" Moment |
|---|---|
| **Marc (PM)** | First proactive alert: "Phase Esquisse on Project X is at 82% budget with 40% work remaining" — catches what would have been missed |
| **Sophie (Employee)** | Opens app Monday morning, timesheet for last week pre-filled correctly — confirms in 3 clicks |
| **Nathalie (Finance)** | Generates a complete billing dossier in 10 minutes instead of 2 hours — with client-specific format auto-applied |
| **Isabelle (Assistante BU)** | Realizes PMs are entering their own data because the tool is easy — she can focus on analysis and reporting |
| **Éric (Support)** | Switches between 7 projects in his timesheet effortlessly — AI knows his pattern and pre-fills accurately |
| **Pierre (Associé)** | Opens executive dashboard, sees all 15 projects at a glance with one in red — drills down and takes action in 5 minutes |
| **François (BD)** | Opportunity won → project created automatically with WBS template — zero manual handoff |
| **Luc (Contrôleur)** | Runs a cross-BU profitability report in 30 seconds that used to take a full day of Excel consolidation |
| **Catherine (Resp. support)** | Sees her team's workload for the next 3 months across all BUs — arbitrates a resource conflict before it becomes a problem |
| **Daniel (Admin)** | New employee appears automatically via Azure AD sync, assigned the right role and permissions — zero manual setup |

---

## Success Metrics

### Platform KPIs (Operational Metrics Visible in the ERP)

Business metrics that the ERP must track and display to users — combining OOTI-inspired dashboard patterns with the firm's specific needs.

#### Financial Health KPIs

| KPI | Description | Visibility |
|---|---|---|
| **Carnet de commandes (Backlog)** | Total value of signed contracts minus invoiced amounts — the firm's future revenue pipeline. Current coverage: ~12 months. Alert threshold: <9 months | Associates, Controllers, Finance |
| **Ratio CA/Salaire — Standard** | Revenue generated divided by standard salary cost (by profile) — the primary profitability indicator for project management, calculated per project, phase, person, BU, and firm-wide | PMs, Associates, Finance, Controllers |
| **Ratio CA/Salaire — Réel** | Revenue generated divided by real salary cost (by person) — the true profitability measure, restricted access | Associates, Finance, Controllers only |
| **Taux de facturation (Billing rate)** | Billed hours / total available hours (including vacations and absences) — measures how much of total payroll converts to billable revenue | BU Directors, Associates, Finance, Controllers |
| **Montant facturable (Billable amount)** | Total fees earned but not yet invoiced — identifies invoicing backlog | Finance, PMs, Associates |
| **Factures impayées (Outstanding invoices)** | Total invoiced but unpaid — tracks cash collection health with aging breakdown | Finance, Associates |
| **Marge par projet (Project margin)** | Revenue minus costs per project with color coding: green (>20%), orange (0-20%), red (<0%) — in both Realized and Projected modes | PMs, Associates, Controllers |
| **CA réalisé vs projeté (Actual vs projected revenue)** | Monthly comparison of invoiced revenue vs planned revenue — detects billing delays and forecast accuracy | Associates, Controllers |
| **RAF (Remaining work)** | AI-predicted remaining hours per project/phase — based on historical patterns and current consumption rate | PMs, Associates |
| **Budget sous-traitants** | Budget allocated vs consumed per subcontractor/PO per project | PMs, Finance |

#### Hours Analysis KPIs

| KPI | Description | Visibility |
|---|---|---|
| **Heures facturées** | Total billable hours per person, BU, project, and firm | PMs, BU Directors, Finance, Controllers |
| **Heures non facturées — Admin/Internes** | Time on internal projects, meetings, training | BU Directors, Finance, Associates |
| **Heures non facturées — Non affectées** | Bench time, between projects | BU Directors, Finance, Associates |
| **Heures non facturées — Hors périmètre** | Work beyond contract scope — feeds out-of-scope detection for amendments | PMs, BU Directors, Associates |
| **Congés / Absences planifiées** | Vacations, holidays — impacts capacity planning | PMs, Catherine, BU Directors |
| **Absentéisme** | Unplanned absences (sick leave, etc.) — tracked by BU and period for HR trend detection and capacity adjustment | BU Directors, HR, Associates |
| **Écart prévision / réel** | Planned hours vs actual hours per WBS — measures estimation quality | PMs, Controllers |

#### Operational KPIs

| KPI | Description | Visibility |
|---|---|---|
| **Taux de saisie des temps (Timesheet completion rate)** | % of employees who submitted timesheets on time | PMs (their team), BU assistants, Finance |
| **Taux d'utilisation (Utilization rate)** | Billable hours / available hours (excluding vacations) per person, team, BU, firm | PMs, Associates, Controllers |
| **Charge des services support** | Capacity vs demand for 3D, BIM, DD, Landscape services | Catherine (service managers), Direction |
| **Pipeline d'opportunités** | Number and value of opportunities by stage, with conversion rates and projected revenue | François, Associates |
| **Projets en alerte** | Count of projects with AI-detected risks (budget overrun, scope creep, RAF anomaly) | PMs, Associates |
| **Approbations en attente** | Pending timesheet approvals, pending POs, pending invoices — aging and count | PMs, Finance, BU assistants |

### Business Objectives

#### Phase 1 — Internal Deployment (Months 1-6)

| Objective | Target | Measurement |
|---|---|---|
| **Full ChangePoint replacement** | 100% of active projects migrated, ChangePoint decommissioned | Migration completion report |
| **Timesheet completion quality** | 100% of employees submitting complete timesheets weekly (mandatory usage) — quality and punctuality measured, not adoption | Platform analytics — % on-time, % complete |
| **Excel elimination** | 80% reduction of operational Excel files within 6 months, 100% at 12 months | User survey + process audit |
| **Invoice cycle time reduction** | Average invoice preparation time reduced by 60% (from ~2h to <45 min per billing dossier) | Time tracking on billing tasks |
| **Financial data consistency** | 100% of invoices synchronized with Intact (Sage) without manual re-entry | Sync error logs |
| **User satisfaction** | Net Promoter Score > 40 (vs current ChangePoint baseline — expected negative) | Quarterly user survey |

#### Phase 2 — Commercialization (Starting Month 6)

| Objective | Target | Measurement |
|---|---|---|
| **Product market readiness** | Multi-tenant architecture validated, first external demo delivered | Product milestone |
| **First external clients** | 2-3 pilot architecture firms onboarded within 12 months of Phase 2 start | Client contracts |
| **SaaS revenue** | First recurring revenue from external clients | Financial records |
| **Data migration tooling** | ChangePoint migration toolkit reusable for external clients | Successful external migration |
| **Time-to-value for external client** | From contract signature to first productive month — baseline to be established | Client onboarding tracking |

### Key Performance Indicators

#### User Engagement KPIs (Platform Health)

| KPI | Target | Frequency |
|---|---|---|
| **Daily Active Users (DAU)** | 400/400 on workdays (mandatory system) | Daily |
| **Average time entry duration** | <2 min per day for employees, <5 min for support specialists | Weekly |
| **AI auto-fill acceptance rate** | Month 1-3: >40%, Month 3-6: >55%, Month 6+: >70% | Monthly |
| **Mobile usage rate** | >30% of field staff using mobile for time/expenses within 3 months | Monthly |
| **OCR success rate** | >85% of scanned receipts correctly parsed on first attempt | Monthly |
| **Time-to-autonomy** | New user fully autonomous within 1 day (employees), 1 week (PMs) | Per onboarding |

#### Financial Impact KPIs

| KPI | Target | Frequency |
|---|---|---|
| **Billing cycle time** | Invoice prepared within 5 business days of period close (vs current 15+ days) | Monthly |
| **Revenue leakage reduction** | <2% of billable hours not invoiced (vs current estimated 5-8%) | Quarterly |
| **Intact sync accuracy** | 99.9% of transactions synced without manual correction | Monthly |
| **Forecast accuracy (RAF)** | AI-predicted RAF within 15% of actual remaining hours at project completion | Per project |
| **Out-of-scope detection** | >80% of scope deviations flagged by AI before exceeding 10% budget impact | Per project |

#### Strategic KPIs

| KPI | Target | Frequency |
|---|---|---|
| **Ratio CA/Salaire firm-wide** | Maintain or improve current firm average (baseline to be established) | Monthly |
| **Carnet de commandes** | Maintain 9+ months of revenue coverage (alert below 9 months) | Monthly |
| **Taux de facturation firm-wide** | Target to be baselined from current ChangePoint data | Monthly |
| **Project health score** | <10% of active projects in "red" status | Monthly |
| **Resource utilization** | 75-85% billable utilization across the firm | Monthly |
| **Support service bottleneck** | 0 projects delayed >1 week due to support resource unavailability | Monthly |
| **Absenteeism rate** | Track and trend by BU — alert on anomalies vs firm average | Monthly |

#### Technical KPIs

| KPI | Target | Frequency |
|---|---|---|
| **Page load time** | <2 seconds for standard pages, <3 seconds for dashboards | Continuous |
| **Concurrent user capacity** | 400 users without performance degradation | Load testing |
| **System uptime** | 99.5%+ availability during business hours | Monthly |

---

## MVP Scope

### Core Features (MVP — Phase 1)

The MVP must enable the firm to fully decommission ChangePoint by delivering the 4 essential modules that support daily operations for 400 employees. Development is AI-assisted (Claude), meaning a lean, iterative approach with disciplined scope control.

#### Module 1: Project Management

| Feature | Description |
|---|---|
| **Project creation & configuration** | Create projects with metadata: client, contract type (forfaitaire, consortium, co-dev, conception-construction), legal entity, BU, construction cost (informational KPI), dates, status. 2-screen wizard: screen 1 = basic info, screen 2 = structure selection |
| **Two-axis project structure** | Sequential realization phases (Étude préparatoire, Concept, Préliminaire, Définitif, Appel d'offres, Surveillance) + transversal support services (Gestion de projet, BIM, 3D, Paysage, Design — extensible). Support services are global project-level tasks, not broken down by phase |
| **Project templates** | Pre-configured templates by contract type with phases (checked by default) and support services (optional). Template is a starting point, not a constraint — PM adjusts freely after creation. Hybrid approach: a few standard templates as accelerators |
| **Virtual resource profiles** | Generic resource archetypes positioned on tasks BEFORE assigning real employees. Used for budgeting (average hourly rate per profile), timeline planning, and capacity reservation. Positioned on main tasks (phases + support services); subtasks inherit from parent by default. Complete position reference list from the firm (see Appendix A) |
| **Multi-employee assignment** | A virtual profile can be replaced by one or multiple employees with percentage-based hour distribution (e.g., Sophie 60% = 90h, Jean 40% = 60h on 150h total). PM can assign partially and complete later. Employee selection modal presents candidates in 3 priority tiers: (1) matching profile with availability, (2) similar profiles, (3) all other employees |
| **WBS hierarchy** | Multi-level Work Breakdown Structure with phases, tasks, subtasks — configurable per project type |
| **Contract management** | Contract value, amendments, budget tracking per WBS element |
| **Multi-entity support** | Projects assigned to Provencher_Roy Prod or PRAA with entity-specific settings |
| **Internal projects** | Lighter task/subtask structure for non-billable internal work |
| **Project dashboard** | Per-project view: budget consumed, hours consumed vs planned, team, virtual vs assigned status, phase completion indicators (green/yellow/red) |
| **Subcontractor management** | Three budget layers: internal fees, refacturable subcontractors (billed to client with markup %), absorbed subcontractors (firm cost). Per subcontractor: supplier name, budget, refacturable flag, markup %, calculated client amount. Configurable subcontractor types (structural engineer, mechanical, electrical, civil, acoustic, LEED, etc.) |
| **Personnel lending tracking** | Track inter-BU staff loans with CA repatriation to home BU |
| **Support service budget allocation** | Allocate budgets for 3D, BIM, DD, Landscape services per project — tracked as global project tasks |

#### Module 2: Time Tracking

| Feature | Description |
|---|---|
| **Authorization-based visibility** | Employees only see projects and tasks where they are assigned — no scrolling through 200 projects. Assignment automatically creates time entry permissions. No assignment = not visible in timesheet |
| **Weekly timesheet entry** | Desktop interface for entering hours per project/phase/task per day. Grouped by Project > Phases | Support. Daily total indicator when different from norm (7.5h or 8h). Draft save + weekly submit |
| **Phase and person blocking** | Two levels: (1) Phase locked — no one can enter time (e.g., completed phase, shown greyed with padlock icon); (2) Person blocked on a phase — specific individual blocked but others can still enter. 1-click blocking by PM from access management screen. Unblocking possible |
| **Multi-project support** | Optimized for users working on 5-10 projects (support specialists) — favorites, quick-switch |
| **2-level approval workflow** | PM approves → Finance/Direction approves, with status tracking and notifications |
| **Timesheet reminders** | Automated reminders for incomplete/late timesheets |
| **Hours categorization** | Billable, non-billable (admin, internal), absence types (vacation, sick, holiday) |
| **Correction workflow** | Allow timesheet corrections after approval with audit trail |
| **Hours reports** | Hours by project, by person, by BU, by period — with facturable/non-facturable breakdown |

#### Module 3: Invoicing & Financial Layer

| Feature | Description |
|---|---|
| **Dual project layers** | Realization layer (PM): work phases, profiles, hours, team. Financial layer (Accounting): billing phases, contractual rates, payment schedule. Financial phases can group multiple realization phases (e.g., "Études" covers Étude préparatoire + Concept) |
| **Mixed billing modes** | Same project can have fixed-price phases (billed by % advancement with milestones) and hourly phases (billed monthly). Per financial phase: mode (fixed/hourly), amount or max budget, payment schedule |
| **Dual hourly rates** | Internal rate (firm cost, e.g., 165$/h) vs contractual rate (billed to client, e.g., 185$/h). Margin = difference. Contractual rates defined by Accounting per project, may vary per profile and contract |
| **Invoice preparation screen** | Key screen for Accounting with 7 columns per deliverable: (1) Deliverable name, (2) Total contract amount, (3) Invoiced to date, (4) % billing advancement, (5) % hours advancement (fixed-price) or supplier invoice amounts (subcontractors), (6) Amount to bill this month (editable — the Accounting decision), (7) % advancement after billing (real-time recalculation). Visual alerts: red when hours > billing +10pts, green when billing ahead, yellow badge at >90% |
| **CA/Salary ratio banner** | Global project indicator displayed above invoice preparation: ratio before billing (invoiced to date / salaries to date) and ratio after billing (with current month). Compared to firm target (configurable). Real-time recalculation as Accounting adjusts amounts |
| **Non-billable tasks** | Tasks that consume hours but generate no revenue — no linked financial phase. Tracked normally for cost visibility. Examples: architecture competitions, internal rework, project-specific training |
| **Invoice creation** | Create invoices linked to projects with line items, taxes, amounts |
| **10+ configurable billing templates** | Client-specific invoice formats selectable per project |
| **Billing dossier assembly** | Generate complete billing package: invoice + timesheets in client format + subcontractor invoices |
| **Invoice status workflow** | Draft → Submitted → Approved → Sent → Paid — with status tracking |
| **Payment tracking** | Record payments received, track outstanding amounts, aging analysis |
| **Manual export for Intact** | Export invoice data in a structured format (CSV/Excel) for manual import into Intact (Sage) |
| **Multi-currency** | Invoice in multiple currencies with exchange rate management |

#### Module 4: Expense Reports

| Feature | Description |
|---|---|
| **Expense entry** | Create expense reports with date, amount, category, project, description |
| **Receipt attachment** | Upload receipt photos/PDFs attached to expense lines |
| **Approval workflow** | Submit → PM approval → Finance approval |
| **Expense categories** | Configurable categories (travel, meals, supplies, etc.) |
| **Multi-currency expenses** | Enter expenses in foreign currencies with conversion |
| **Expense reports** | By person, by project, by BU, by period |

#### Module 5: Supplier Payment Tracking

| Feature | Description |
|---|---|
| **Supplier invoice lifecycle** | 3-state workflow: Received (entered by PM or Accounting) → Authorized (PM verifies and approves "bon à payer") → Paid (Accounting executes payment). Each invoice is in exactly one state at any time |
| **Separation of responsibilities** | PM: receives/enters invoices, verifies conformity, authorizes payment. Accounting: executes payments, maintains registry |
| **Per-subcontractor project view (PM)** | List of invoices per supplier on a project, cumulative vs planned budget, indicators: total received / total authorized / total paid / remaining budget / authorized but unpaid |
| **Pending authorizations view (Accounting)** | Cross-project view of all authorized-but-unpaid invoices, with action to mark as paid |
| **Payment report (Accounting)** | Cross-project payment report grouped by supplier — a single supplier may have invoices from multiple projects consolidated into one payment. With amounts, authorization dates, exportable |
| **Independence from client billing** | Supplier payment flow is completely independent from client invoicing. A supplier can be paid before or after being re-billed to the client. The two flows only merge in profitability reporting |

#### Module 6: Service Proposals (Offres de services)

| Feature | Description |
|---|---|
| **Proposal creation** | Lightweight single-screen creation: code (OFF-YYYY-NNN), title, client, submission deadline, internal effort budget (hours), standard task checklist (analysis, design, writing, submission assembly, presentation/jury — extensible) |
| **Proposal lifecycle** | Statuses: En cours → Soumise → Gagnée / Perdue / Abandonnée → Convertie (if won). Contextual status change buttons |
| **Time tracking on proposals** | Same authorization mechanism as projects: employees only see proposals they're assigned to. Time is always non-billable. PM controls who can enter time |
| **No subcontractors or financial layer** | Proposals are internal effort only — no subcontractor management, no financial phases, no billing |
| **Conversion to project** | When won: new project code generated (PRJ-YYYY-NNN), client can change (alert if different from proposal client), PM selects template and contract mode. Project starts clean — no team or operational data transfer. Proposal closed with "converted" status and link to project. Proposal time history preserved as reference |
| **Client tracking** | Both proposal client (donneur d'ouvrage) and project client preserved. Useful for reporting: who we respond to vs who we work for |
| **Commercial reporting** | Conversion rate, average cost per proposal (hours and $), project acquisition cost (e.g., 1 in 4 won × 200h avg = 800h acquisition cost), lost proposal costs visible |
| **PM dashboard integration** | "My active proposals" section with status and submission deadline countdown |

#### Module 7: Consortium Management

| Feature | Description |
|---|---|
| **Consortium entity** | Distinct entity: name, member list with individual coefficients (salary × coefficient), profit-sharing rule (fixed per agreement OR proportional to effort), effort basis if proportional (hours or $ invoiced), Provencher role (mandataire/leader or partner) |
| **Multi-project support** | One consortium can have N projects. Each project is independent for profit-sharing calculations. Consortium links to its projects |
| **Project creation flag** | PM checks "Consortium project" checkbox at project creation → selects existing consortium or creates new one. Rest of creation flow identical to standard projects |
| **Standard operations** | Time entry, invoicing, billing cycle — all identical to standard projects. No special interface for daily operations |
| **Dual financial view** | Consortium view: client revenue, member costs (received invoices), margin, profit sharing. Provencher view: invoices issued to consortium + profit share = Provencher CA. Critical rule: consortium client revenue is NOT in Provencher's chiffre d'affaires |
| **Partner data ingestion** | Other members' costs/hours enter via received invoices only (manual entry or accounting API). No direct time entry from external partners |
| **Full visibility** | PMs, Finance, and BU Directors see costs/hours for both Provencher AND other consortium members |
| **BU Director dashboard** | Dedicated recap table: all active consortiums with their projects, ratios, progress, outstanding client invoices. Data fed by manual entry or accounting API. Separated from standard project views |
| **Profit sharing calculation** | Per-project calculation: consortium revenue − member invoices = margin → distributed per agreement rules. Provencher's share tracked as CA |

#### Cross-Cutting MVP Features

| Feature | Description |
|---|---|
| **SSO Microsoft Entra ID** | Single sign-on integration with automatic user provisioning |
| **Role-based permissions** | 5+ permission levels with granular access control (especially for salary cost data) |
| **Audit trail** | Complete modification history on all critical entities |
| **Role-based dashboards** | Personalized home dashboard per role: PM, Employee, Finance, BU Assistant, Associate, Controller |
| **Basic reporting** | Financial KPIs: carnet de commandes, ratio CA/salaire (standard), taux de facturation, marge par projet |
| **Data migration** | Import ChangePoint data: projects, WBS, time entries, billing history (10+ years) |
| **Dual salary costing** | Standard cost per profile + real cost per person with permission-controlled visibility |

### Out of Scope for MVP

| Feature | Rationale | Target Phase |
|---|---|---|
| **Opportunity pipeline** | Not essential for daily operations — firm can continue current BD process | Phase 2 |
| **Mobile app** | Desktop-first launch — field staff can use desktop temporarily | Phase 1.5 |
| **OCR receipt scanning** | Nice-to-have — manual receipt upload sufficient for MVP | Phase 1.5 |
| **AI auto-fill timesheets** | Requires 3+ months of historical usage data to train effectively | Phase 1.5 |
| **AI predictive RAF** | Needs historical data + validated baseline from manual RAF tracking | Phase 2 |
| **AI out-of-scope detection** | Advanced feature requiring mature project data | Phase 2 |
| **AI proactive alerts** | Dependent on AI models being trained on firm data | Phase 2 |
| **AI resource planning** | Complex feature requiring historical WBS patterns | Phase 2 |
| **Intact/Sage bidirectional sync** | Manual export sufficient initially — integration in Phase 1.5 | Phase 1.5 |
| **CPI indexation** | Manual calculation acceptable for now — low volume of multi-year contracts | Phase 2 |
| **Cmd+K universal search** | Power-user feature — standard navigation sufficient for MVP | Phase 2 |
| **Advanced executive dashboards** | Basic KPI dashboards in MVP — advanced drill-down and BI-lite in Phase 2 | Phase 2 |
| **Advanced resource planning** | Basic team assignment in MVP — capacity planning with AI in Phase 2 | Phase 2 |
| **Multi-tenant SaaS** | Internal deployment first — SaaS preparation deferred to commercialization phase | Phase 2 |

### MVP Success Criteria

| Criteria | Gate | Measurement |
|---|---|---|
| **ChangePoint decommissioned** | All active projects migrated, all 400 users on the new platform | Migration report |
| **100% timesheet submission** | Every employee submitting complete weekly timesheets via the ERP | Platform analytics |
| **Invoice cycle operational** | Finance team producing invoices end-to-end in the ERP with successful Intact export | Process validation |
| **Expense reports functional** | Employees submitting expense reports through the ERP instead of legacy process | Usage metrics |
| **No critical blocking bugs** | Zero P0/P1 bugs preventing daily operations for >4 hours | Bug tracking |
| **User satisfaction baseline** | NPS survey conducted to establish baseline for future improvement | Survey results |

### Future Vision

#### Phase 1.5 — Enhancement (3-6 months post-MVP)

| Feature | Value |
|---|---|
| **Mobile app (time + expenses)** | Field architects enter time and expenses on construction sites — eliminates paper-based workarounds |
| **OCR receipt scanning** | Photo → auto-parsed expense line — reduces expense entry time by 80% |
| **AI auto-fill timesheets** | AI learns from 3+ months of patterns and pre-fills timesheets — target 70% acceptance rate |
| **Intact/Sage bidirectional sync** | Automated invoice/payment synchronization — eliminates manual export/import |
| **Enhanced reporting** | Advanced cross-BU reports, hours analysis (non-billable breakdown, absenteeism), export improvements |

#### Phase 2 — Intelligence & Commercialization (6-18 months post-MVP)

| Feature | Value |
|---|---|
| **Opportunity pipeline** | Full BD cycle: lead → opportunity → proposal → contract → project creation |
| **AI predictive RAF** | AI predicts remaining hours with confidence intervals based on historical project patterns |
| **AI out-of-scope detection** | Automatic detection of work exceeding contract scope — proposes amendments |
| **AI proactive alerts** | Budget warnings, schedule risks, utilization anomalies — pushed to relevant users |
| **AI resource planning** | Suggests optimal team composition based on similar historical projects |
| **Advanced executive dashboards** | BI-lite module with drill-down, combinable filters, saveable reports |
| **CPI indexation** | Semi-automatic CPI calculation for multi-year contracts |
| **Multi-tenant SaaS** | PostgreSQL Row-Level Security, tenant configuration, white-labeling |
| **ChangePoint migration toolkit** | Reusable migration tooling for external architecture firms leaving ChangePoint |
| **Cmd+K universal search** | Power-user search across all entities |

---

## Appendix A: Position Reference List (Virtual Profiles)

The following 31 positions constitute the firm's complete position reference, used as virtual resource profiles for project planning and budget estimation. This list is configurable and extensible.

| # | Position (French) | Position (English) |
|---|---|---|
| 1 | Architecte | Architect |
| 2 | Architecte associé(e) | Associate Architect |
| 3 | Architecte patron | Principal Architect |
| 4 | Architecte paysagiste | Landscape Architect |
| 5 | Chargé(e) de conception | Design Lead |
| 6 | Chargé(e) de conception adjoint(e) | Assistant Design Lead |
| 7 | Chargé(e) de coordination | Project Coordinator |
| 8 | Chargé(e) de projet | Project Manager |
| 9 | Chargé(e) de projet adjoint(e) | Assistant Project Manager |
| 10 | Chargé(e) de projet design | Design Project Manager |
| 11 | Chargé(e) d'estimation | Cost Estimator |
| 12 | Chargé(e) d'exécution | Construction Lead |
| 13 | Chargé(e) de programmation | Architectural Programmer |
| 14 | Consultant en bâtiment | Building Consultant |
| 15 | Contrôle qualité | Quality Control |
| 16 | Designer associé(e) | Associate Designer |
| 17 | Designer d'intérieur | Interior Designer |
| 18 | Designer urbain | Urban Designer |
| 19 | Étude de codes | Code Compliance Specialist |
| 20 | Maquette | Physical Model Specialist |
| 21 | Membre de l'équipe de conception | Design Team Member |
| 22 | Membre de l'équipe d'exécution | Construction Team Member |
| 23 | Rédaction de devis | Specifications Writer |
| 24 | Spécialiste 3D | 3D Visualization Specialist |
| 25 | Spécialiste BIM | BIM Specialist |
| 26 | Spécialiste de mobilier | Furniture Specialist |
| 27 | Spécialiste en durabilité | Sustainability Specialist |
| 28 | Support à la rédaction | Specifications Support |
| 29 | Support technique | Technical Support Specialist |
| 30 | Surveillant(e) de chantier | Site Supervisor |
| 31 | Urbaniste | Urban Planner |

*Source: listePoste.xlsx — firm's official position reference*
