# Story 12.3: Finance Tab — Connect Real Data (Remove Placeholders)

Status: draft

## Story
As a **PM, Associé en charge, Finance user or BU Director**, I want the project Finance tab to display real CA billed, salary costs, subcontractor costs, expenses, margin, margin % **and project cash flow** (paid/unpaid invoices + supplier payments decisions), So that I can monitor project profitability and liquidity without relying on placeholder zeros.

## Context
- The project Finance tab currently shows **hardcoded zeros** everywhere:
  - [ProjectDetail.vue:527-530](../../frontend/src/features/projects/views/ProjectDetail.vue#L527-L530) — `financeData` placeholder array
  - [ProjectDetail.vue:1715-1747](../../frontend/src/features/projects/views/ProjectDetail.vue#L1715-L1747) — KPI cards and annual table with `0,00 $`
- Footer message : *"Les données financières seront calculées automatiquement à partir des factures et des feuilles de temps."* — the promise must now be fulfilled.
- **Finance role scope** (domain.md §Acteurs + Philippe 2026-04-21) :
  1. Assure la **rentabilité** des projets (CA, coûts, marge)
  2. Gère le **cash flow** des projets (factures payées / impayées, aging)
  3. **Décide des paiements fournisseurs** (validation + exécution)
  4. Valide la 2ᵉ étape des factures client
- Data sources already exist in the backend:
  - `Invoice` / `InvoiceLine` → CA facturé + statut `PAID` / `APPROVED` pour cash flow ([backend/apps/billing/models.py](../../backend/apps/billing/models.py))
  - `TimeEntry` → heures validées × taux horaire → coûts salaires ([backend/apps/time_entries/models.py](../../backend/apps/time_entries/models.py))
  - `STInvoice` → coûts sous-traitants + décision paiement ([backend/apps/suppliers/models.py](../../backend/apps/suppliers/models.py))
  - `ExpenseLine` → dépenses projet ([backend/apps/expenses/models.py](../../backend/apps/expenses/models.py))
  - `Amendment` → impact sur le contrat courant (story 12.1)
- **Intégration comptabilité = MVP-2** : le lien API avec le logiciel de comptabilité (ex : Acomba, QuickBooks, Sage) est **hors périmètre de cette story**. Cette story prépare les données en interne ; la synchronisation bancaire et l'export comptable seront traités en MVP-2.
- Reference : `_bmad-output/planning-artifacts/module-projets.md` §9.3, §4.10.

## Acceptance Criteria

### AC1 — KPI cards rentabilité (rangée 1)
- **Given** a project with invoices, time entries, ST invoices and expenses
- **When** a user opens the Finance tab
- **Then** the 5 KPI cards de la ligne **Rentabilité** affichent :
  - **CA facturé** : Σ invoice lines of status `APPROVED` + `PAID` (excl. tax)
  - **Coûts salaires** : Σ (validated time entries × cost rate at entry date)
  - **Coûts ST** : Σ ST invoices (paid + approved)
  - **Marge** = CA facturé − (coûts salaires + coûts ST + dépenses non refacturables)
  - **Marge %** = Marge / CA facturé (display `—` if CA = 0)
- **And** values formatées en `fr-CA` locale avec 2 décimales

### AC2 — KPI cards cash flow (rangée 2, nouveau)
- **Given** the same project
- **When** user views Finance tab
- **Then** une seconde rangée de KPI **Cash flow** apparaît :
  - **Facturé payé** : Σ invoices `PAID`
  - **Facturé impayé** : Σ invoices `APPROVED` not `PAID` (total dû par le client)
  - **Aging > 60j** : Σ invoices `APPROVED` avec due_date > 60 jours (alerte rouge)
  - **ST à payer** : Σ `STInvoice` status `APPROVED` non encore payée (dette fournisseur)
  - **Cash net projet** = Facturé payé − ST déjà payées − dépenses remboursées
- **And** chaque carte cliquable → ouvre un panneau listant les factures correspondantes

### AC3 — Tableau paiements fournisseurs (décision Finance)
- **Given** Finance user on Finance tab
- **When** ils consultent la section "Paiements fournisseurs à décider"
- **Then** tableau listant les `STInvoice` en statut `APPROVED` et non payées :
  - Colonnes : Fournisseur, Nᵒ facture, Date réception, Montant, Échéance, État (À payer / Suspendu / Payée), CTA "Décider"
- **And** Finance peut marquer `SCHEDULED` (planifier paiement) ou `ON_HOLD` (suspendre) avec motif
- **And** chaque décision est captée dans `HistoricalRecords` (actor + timestamp + motif)
- **And** non-Finance roles voient le tableau en **lecture seule** (pas de CTA)

### AC4 — Annual breakdown table
- **Given** the same project
- **When** the Finance tab loads
- **Then** annual table shows one row per fiscal year (CA, Coûts, Marge $, Marge %)
- **And** rows ordered descending (current year first) + row "Total"

### AC5 — Backend endpoint contract
- **Given** authenticated user with project access
- **When** they call `GET /api/projects/{id}/finance-summary/`
- **Then** response shape :
  ```json
  {
    "profitability": {
      "ca_facture": "125000.00",
      "couts_salaires": "68000.00",
      "couts_st": "12000.00",
      "couts_depenses_non_refacturables": "2500.00",
      "marge": "42500.00",
      "marge_pct": 34.0
    },
    "cashflow": {
      "facture_paye": "80000.00",
      "facture_impaye": "45000.00",
      "aging_gt_60j": "15000.00",
      "st_a_payer": "7000.00",
      "cash_net": "68000.00"
    },
    "contract": {
      "original": "120000.00",
      "courant": "135000.00",
      "reste_a_facturer": "10000.00"
    },
    "annual": [
      {"year": 2026, "ca": "80000.00", "couts": "45000.00", "marge": "35000.00", "marge_pct": 43.75}
    ],
    "st_payments_pending": [
      {"id": 42, "supplier": "ACME Engineering", "invoice_no": "F-2026-0012", "amount": "3500.00", "due_date": "2026-05-15", "status": "APPROVED"}
    ]
  }
  ```
- **And** all amounts are `Decimal` strings (2 decimals), never floats
- **And** endpoint is **tenant-scoped** (TenantScopedModel queryset)

### AC6 — Permissions
- **Given** any of : PM, Associé en charge (PROJECT_DIRECTOR), Finance, BU Director, Admin
- **When** they access the endpoint
- **Then** 200 with the payload
- **And** unauthenticated → 401
- **And** Employee without access → 403
- **And** cross-tenant → 404
- **And** Finance-only actions on `STInvoice` decision (AC3) → 403 for non-Finance

### AC7 — Performance
- **Given** the endpoint is called
- **When** the project has 10k+ time entries and 500+ invoice lines
- **Then** response time ≤ 500ms (measured locally)
- **And** Redis cache TTL 60s keyed by `tenant_id:project_id`, invalidated on invoice/time-entry/ST-invoice save
- **And** `assertNumQueries` ≤ 8 (no N+1)

### AC8 — Amendments & contract courant (from story 12.1)
- **Given** a project with approved amendments
- **When** user views Finance tab
- **Then** "Contrat original" / "Contrat courant" / "Reste à facturer" visibles en entête
- **And** le lien entre CA facturé et contrat courant est explicite

## Tasks / Subtasks

### Backend
- [ ] **TDD first** — write failing tests (see Tests section) before any code change
- [ ] Create service `apps/projects/services/finance_summary.py` with pure functions :
  - `compute_profitability(project)` → ca, couts_salaires, couts_st, depenses, marge
  - `compute_cashflow(project)` → paye, impaye, aging, st_a_payer, cash_net
  - `compute_contract(project)` → original, courant, reste_a_facturer (depends on story 12.1)
  - `compute_annual(project)` → list[{year, ca, couts, marge}]
  - `list_pending_st_payments(project)` → queryset of STInvoice
- [ ] Wire service to `GET /api/projects/{id}/finance-summary/` in `apps/projects/views.py`
- [ ] Add `POST /api/st-invoices/{id}/schedule-payment/` and `/hold-payment/` actions (Finance-only)
- [ ] Permission classes : project access check + `IsFinance` for ST payment decisions
- [ ] Redis cache with Django signals on save invalidating tenant+project key
- [ ] Serializer returns `Decimal` strings, not floats
- [ ] `select_related` / `prefetch_related` — verify `assertNumQueries` ≤ 8

### Frontend
- [ ] Replace placeholder `financeData` in [ProjectDetail.vue:527-530](../../frontend/src/features/projects/views/ProjectDetail.vue#L527-L530) with reactive state from API
- [ ] `projectApi.financeSummary(projectId)` in `features/projects/api.ts`
- [ ] Deux rangées de KPI : **Rentabilité** (5 cartes) + **Cash flow** (5 cartes)
- [ ] Section "Contrat" : original / courant / reste à facturer (bandeau)
- [ ] Section "Paiements ST à décider" : tableau + CTA Finance-only
- [ ] Annual table avec ligne "Total"
- [ ] Loading skeleton pendant fetch, empty state si aucune activité
- [ ] Error state : afficher message backend (UX rule #5)
- [ ] Remove footer placeholder message ([ProjectDetail.vue:1747](../../frontend/src/features/projects/views/ProjectDetail.vue#L1747))

### Documentation
- [ ] Update `module-projets.md` §4.10 Finance marqué ✅ connecté
- [ ] Documenter le périmètre MVP-2 : API compta externe (non dans cette story)

## Tests

### Backend (pytest + factory_boy)
- [ ] `test_finance_profitability_happy_path` — KPI rentabilité corrects
- [ ] `test_finance_cashflow_aging_gt_60j` — factures > 60 jours comptées
- [ ] `test_finance_cashflow_cash_net_computation`
- [ ] `test_finance_only_validated_time_entries`
- [ ] `test_finance_only_approved_or_paid_invoices`
- [ ] `test_finance_amendment_contract_current` — original + Σ amendments
- [ ] `test_finance_annual_breakdown` — multi-year
- [ ] `test_finance_empty_project` — zéros sans crash, empty state
- [ ] `test_finance_marge_pct_division_by_zero` — CA=0 → null, pas crash
- [ ] `test_st_payment_decision_finance_only` — 403 pour PM, 200 pour Finance
- [ ] `test_st_payment_decision_audit_trail` — HistoricalRecords capturée
- [ ] `test_finance_summary_no_n_plus_1` — `assertNumQueries` ≤ 8
- [ ] `test_finance_summary_cache_invalidated_on_save`
- [ ] `test_finance_summary_permissions` — 401/403/404 matrix
- [ ] `test_finance_summary_tenant_isolation`

### Frontend (Vitest + Playwright)
- [ ] Vitest : `financeSummary` API call, reactive binding, loading/empty/error
- [ ] Vitest : KPI formatting fr-CA, aging badge rouge > 60j
- [ ] Vitest : ST payments decision CTA visible Finance only
- [ ] Playwright E2E : ouvre onglet Finance sur projet seed → KPI réels, décision paiement ST

## Risks & Open Questions
- **Risk** : `TimeEntry` doit stocker `cost_rate_snapshot` au moment de la saisie. Si seulement `Employee.current_rate` existe, audit + migration snapshot requise.
- **Risk** : statut `STInvoice` — vérifier que le workflow existant supporte `APPROVED` / `SCHEDULED` / `PAID` / `ON_HOLD`.
- **Risk** : cache invalidation incomplète si signal manquant sur un modèle → tests de cohérence obligatoires.
- **Open** : aging seuil 60j ou 30/60/90j tri-bucket ? → MVP-1 : un seul bucket `>60j`, enrichir plus tard.
- **Open** : fiscal year — calendrier ou avril-mars ? → défaut : année calendaire.
- **Open** : "non refacturable" flag sur `ExpenseLine` — confirmer existence, sinon dériver depuis catégorie.
- **Out of scope (MVP-2)** : synchronisation bancaire, export comptable automatique, API vers logiciel de compta (Acomba/QB/Sage). Prévoir des hooks/serializers extensibles pour faciliter l'ajout MVP-2.

## Dev Agent Record
### Agent Model Used
_To be filled by dev agent_
### Completion Notes List
_To be filled during implementation_
### Change Log
- 2026-04-21: Story drafted from module-projets.md §9.3 finalization chantier
- 2026-04-21: Added AC2 (cash flow), AC3 (ST payment decisions), MVP-2 note on accounting API per Philippe
### File List
_To be filled during implementation_

## References
- [_bmad-output/planning-artifacts/module-projets.md](../planning-artifacts/module-projets.md) §4.10, §9.3
- [.claude/rules/domain.md](../../.claude/rules/domain.md) — Finance rentabilité + cash flow
- [.claude/rules/security.md](../../.claude/rules/security.md) — permissions + isolement tenant
- [.claude/rules/database.md](../../.claude/rules/database.md) — N+1, aggrégations
- Story 12.1 — Amendments (contrat courant)
- [frontend/src/features/projects/views/ProjectDetail.vue](../../frontend/src/features/projects/views/ProjectDetail.vue) — placeholders à remplacer
- **MVP-2** : API comptabilité externe (hors scope, à concevoir séparément)
