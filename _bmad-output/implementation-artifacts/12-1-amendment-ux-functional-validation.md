# Story 12.1: Amendment (Avenant) UX Functional Validation

Status: draft

## Story
As a **PM or Assistante de département**, I want a complete end-to-end UX workflow to create, validate and consume amendments (avenants) — including dedicated phases/tasks visible in the planning & Gantt chart and flexible invoicing — So that contractual changes are formally tracked, visibly planned, and billable either combined or separately.

## Context
- Epic 12 (Project Lifecycle Extended) is **implemented technically but not functionally validated** (decision 2026-04-21).
- Models, migrations and API endpoints for `Amendment` exist, including HistoricalRecords audit trail (story 3.10) and VersionedModel optimistic locking.
- Approval authority is the **Associé en charge** (not PM, not BU Director).
- Initial capture may be done by **Assistante de département, PM or Finance**.
- An amendment is a **mini-contract attached to the main project**, with its **own phases/tasks** (décision métier Philippe 2026-04-21).
- Avenant phases/tasks must appear in the **planning and Gantt chart** alongside (but distinguishable from) the original project phases/tasks.
- Avenant hours/expenses must be billable either **merged into the main invoice** OR on a **dedicated invoice** (choice at invoice creation).
- Reference: `_bmad-output/planning-artifacts/module-projets.md` §9.1, §2.6, §4.7.

## Acceptance Criteria

### AC1 — Creation form (all 3 roles)
- **Given** a user with role `DEPT_ASSISTANT`, `PM` or `FINANCE` on an active project
- **When** they open the Avenants tab and click "Nouvel avenant"
- **Then** a SlideOver opens with: external number (free text), internal number auto-generated `{project_code}-AV-{seq}`, description, amount delta, effective date, attached document upload
- **And** the form lets the user add **phases and tasks dedicated to the avenant** (same structure as main project phases/tasks, with their own start/end dates)
- **And** fields follow existing charte graphique (read/edit mode pattern, auto-save where applicable)

### AC2 — Approval workflow (Associé en charge only)
- **Given** a draft amendment
- **When** the Associé en charge opens it
- **Then** they see "Valider" / "Rejeter" actions
- **And** no other role (PM, Finance, Assistante, BU Director) can validate
- **And** the amendment state machine: `DRAFT → PENDING_APPROVAL → APPROVED` (or `REJECTED`)
- **And** each transition is captured in `HistoricalRecords` with actor + timestamp

### AC3 — Budget impact
- **Given** an amendment in state `APPROVED`
- **When** any user opens the project Budget tab
- **Then** current contract value = original contract + Σ(approved amendment deltas)
- **And** the Budget tab header shows both "Contrat original" and "Contrat courant"
- **And** a breakdown line per amendment is visible (number, date, delta, actor)

### AC4 — Planning & Gantt visibility
- **Given** an approved amendment with its own phases/tasks
- **When** a user opens the Planning tab or the Gantt chart of the project
- **Then** avenant phases/tasks appear in a **dedicated visual group** (e.g. swimlane or color-coded band) labelled with the avenant number
- **And** the avenant phases/tasks are distinguishable from main project phases (color, icon, or legend)
- **And** resource allocation (`ResourceAllocation`) can be assigned to avenant tasks the same way as main tasks
- **And** time entries (`time_entries`) can be saved against avenant tasks (using WBS client labels — domain.md rule)

### AC5 — Invoicing flexibility (merged OR dedicated)
- **Given** approved amendments with billable hours/expenses
- **When** Assistante or Finance creates an invoice
- **Then** the invoice creation screen offers a choice: **"Inclure dans la facture projet"** OR **"Facture dédiée avenant"**
- **And** if "dédiée" is chosen, only the avenant lines are included, and the invoice header references the avenant number
- **And** if "merged", the invoice clearly separates main project lines and avenant lines (grouped section per avenant)
- **And** invoice PDF uses **WBS client labels** for all lines (domain.md rule)
- **And** validation workflow unchanged: created by Assistante/Finance → PM validates (1st) → Finance validates (2nd)

### AC6 — Permissions & isolation
- **Given** a user without role on the tenant
- **When** they hit `GET/POST/PATCH /api/amendments/`
- **Then** 401 (unauthenticated) or 403 (wrong tenant / wrong role)
- **And** a user from tenant A cannot see amendments from tenant B (TenantScopedModel)

## Tasks / Subtasks

### Backend
- [ ] **TDD first** — write failing tests (see Tests section) before any code change
- [ ] Verify `Amendment` model has `status` field with `AmendmentStatus` TextChoices (`DRAFT`, `PENDING_APPROVAL`, `APPROVED`, `REJECTED`)
- [ ] Add state transition service `apps/projects/services/amendment_workflow.py` (submit, approve, reject) with `@transaction.atomic`
- [ ] Restrict `approve/reject` actions to user with role `PROJECT_DIRECTOR` (Associé en charge) — permission class
- [ ] Compute `current_contract_value` on `Project` via annotated queryset (no N+1)
- [ ] Expose `/api/projects/{id}/budget-summary/` endpoint returning original + current + amendments breakdown
- [ ] Ensure `Phase` / `Task` models support `amendment` FK (nullable) so phases/tasks can belong to an avenant
- [ ] Planning + Gantt data endpoints return avenant-grouping metadata (avenant number, color key)
- [ ] `billing` module: support invoice creation mode `MERGED` vs `AMENDMENT_DEDICATED` with validation
- [ ] Invoice serializer: if `AMENDMENT_DEDICATED`, require `amendment_id` and exclude main project lines
- [ ] Permissions test matrix: 401 unauth, 403 wrong role, 200 correct role, 403 cross-tenant

### Frontend
- [ ] Avenants tab (`frontend/src/modules/projects/tabs/AvenantsTab.vue`) : liste + SlideOver nouvel avenant
- [ ] SlideOver creation form with read/edit pattern from `shared/components/`
- [ ] Phases/tasks sub-editor inside avenant SlideOver (reuse Phase/Task edit UI components)
- [ ] Display state chip with French labels (Brouillon / En attente / Validé / Refusé)
- [ ] "Valider" / "Rejeter" CTA visible only for Associé en charge
- [ ] Budget tab: show "Contrat courant" section with breakdown
- [ ] Planning tab: render avenant phases/tasks in dedicated swimlane/color group
- [ ] Gantt chart: avenant bars distinct from main project bars (color + legend)
- [ ] Billing screen: "Inclure dans facture projet" vs "Facture dédiée avenant" choice UI
- [ ] Unit tests (Vitest) for store mutations and component render
- [ ] E2E test (Playwright) for the full flow: Assistante creates → Associé validates → Budget updates → Gantt shows → Invoice dedicated/merged

### Documentation
- [ ] Update `module-projets.md` §4.7 with screenshot of final UX (once validated)
- [ ] Flip Epic 12 status annotation from "⚠️ implémenté techniquement" to "✅ validé fonctionnellement" in `epics.md`

## Tests

### Backend (pytest + factory_boy)
- [ ] `test_amendment_creation_by_assistant_pm_finance` — all three roles can create
- [ ] `test_amendment_approval_only_by_project_director` — 403 for PM, Finance, Assistant
- [ ] `test_amendment_state_machine_transitions` — valid and invalid transitions
- [ ] `test_amendment_history_tracked` — `amendment.history.count()` grows on each change
- [ ] `test_current_contract_value_computation` — original + sum(approved deltas)
- [ ] `test_amendment_tenant_isolation` — cross-tenant returns empty
- [ ] `test_amendment_phases_tasks_isolated_in_gantt_payload` — avenant metadata present
- [ ] `test_time_entry_on_amendment_task_uses_wbs_client_label`
- [ ] `test_invoice_dedicated_amendment_excludes_main_lines`
- [ ] `test_invoice_merged_groups_amendment_lines_separately`
- [ ] `test_budget_summary_endpoint_no_n_plus_1` — `assertNumQueries`

### Frontend (Vitest + Playwright)
- [ ] Vitest: amendment store create/approve actions, state chip rendering, invoice mode selector
- [ ] Playwright E2E: full happy path (create → approve → plan → Gantt → dedicated invoice → merged invoice) with test accounts

## Risks & Open Questions
- **Risk** : existing Amendment rows created during technical implementation may have inconsistent state — check if a data migration is needed to reset to `DRAFT`.
- **Risk** : adding `amendment` FK on `Phase`/`Task` requires a migration; verify no regressions on existing planning queries.
- **Open** : does approval require a secondary document upload (signed PDF) ? → clarify with Philippe.
- **Open** : should rejected amendments be deletable or kept for audit ? → default: kept, soft-delete disabled.
- **Open** : visual treatment for avenant bars in Gantt — color rule to confirm with charte graphique.

## Dev Agent Record
### Agent Model Used
_To be filled by dev agent_
### Completion Notes List
_To be filled during implementation_
### Change Log
- 2026-04-21: Story drafted from module-projets.md §9.1 finalization chantier
- 2026-04-21: Added AC4 (planning/Gantt visibility) and AC5 (invoicing flexibility merged vs dedicated) per Philippe
### File List
_To be filled during implementation_

## References
- [_bmad-output/planning-artifacts/module-projets.md](../planning-artifacts/module-projets.md) §2.6, §4.7, §9.1
- [_bmad-output/planning-artifacts/epics.md](../planning-artifacts/epics.md) Epic 12
- [.claude/rules/domain.md](../../.claude/rules/domain.md) — Avenants, Associé en charge, WBS client
- [.claude/rules/security.md](../../.claude/rules/security.md) — permissions DRF
- Story 3.10 (Project Lifecycle & Leadership Management) — audit trail foundations
