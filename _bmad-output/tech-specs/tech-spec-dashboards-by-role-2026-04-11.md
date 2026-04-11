---
title: Tech Spec — Dashboards adaptatifs par rôle (Sprint 1bis)
project: PR|ERP
sprint: 1bis
proposition: A (complement)
date: 2026-04-11
author: Philippe Haumesser
status: draft
level: 1
duration: 2-3 days
related_brainstorming: _bmad-output/brainstorming/brainstorming-session-2026-04-11-200000.md
related_mockup: _bmad-output/mockups/flux/flux-08-dashboards.html
related_spec: _bmad-output/tech-specs/tech-spec-sidebar-quick-win-2026-04-11.md
---

# Tech Spec — Dashboards adaptatifs par rôle

## 1. Problem & Solution

### Problem
Le composant `DashboardView.vue` est actuellement **monolithique** : un seul écran qui affiche les mêmes blocs (avec des conditions `v-if` sur les rôles) pour tous les utilisateurs. Cela entraîne :
- Bruit visuel pour Marie (employée) qui voit des KPIs financiers grisés ou tronqués
- Cognition lourde pour Pierre (BU Director) qui doit scroller pour trouver ses 3 KPIs stratégiques
- Aucun alignement avec le mockup `flux-08-dashboards.html` qui propose une **vision distincte par persona**
- Pas d'agrégation backend dédiée par rôle (les KPIs PM et BU sont dans deux endpoints séparés mais l'employé n'a rien de spécifique)

Le brainstorming a identifié 9 idées qui s'appliquent directement aux dashboards :
- **#12** Vue "Cockpit Direction" (3 cartes pour Pierre)
- **#13** Sidebar Pierre quasi vide (déjà couvert par le Sprint 1 sidebar)
- **#33** Vue "Mon agenda" sidebar (à intégrer au dashboard EMPLOYEE)
- **#37** Dashboards multiples épinglés (Sprint 2)
- **#41** Quest log gamifié (Sprint 2)

### Solution
Refactor du `DashboardView.vue` en **composant orchestrateur** qui charge dynamiquement un sous-composant **par rôle dominant**. Chaque sous-composant :
- A son propre layout, KPIs et data sources
- Aligné strictement sur le mockup `flux-08-dashboards.html`
- Récupère ses données via un endpoint backend dédié `/api/v1/dashboard/role/{role}/`
- Réutilise les services backend existants (`get_role_dashboard_kpis`, `get_pm_financial_kpis`, etc.) en les enrichissant

**Stratégie :** Backend (enrichir les services + ajouter 4 nouveaux endpoints) + Frontend (5 composants persona). Pas de breaking change sur l'existant.

---

## 2. Requirements

### Fonctionnelles

| ID | Requirement | Critère d'acceptation |
|---|---|---|
| **D1** | Le `DashboardView.vue` doit charger dynamiquement un sous-composant selon le rôle dominant | Marie voit `<EmployeeDashboard>`, Pierre voit `<DirectorDashboard>`, etc. |
| **D2** | **Dashboard EMPLOYEE** (Marie) — 4 KPIs + heures budgetées vs réelles + projets | KPIs : Heures semaine (réel/budget), Heures mois (réel/budget), Taux facturable, Actions requises. Plus : **tableau "Heures budgetées vs réelles" par projet (mois)** avec écart et avancement, graphique journalier Lun-Ven, panel actions |
| **D3** | **Dashboard PM** (Jean-François) — 5 KPIs + planification 2 mois + factures + ST | KPIs : Carnet commandes, Ratio CA/S, Taux facturation, Marge moyenne, Actions requises. **Widget "Planification 2 mois à venir"** (planifié vs réel avril, planifié mai, statut planif), tableau santé projets, **table approbations enrichie avec colonnes "Heures planifiées" + "Total semaine" + alerte burnout**, **section "Factures clients à valider"**, **section "Factures sous-traitants à contrôler"** avec ratio vs budget |
| **D4** | **Dashboard PROJECT_DIRECTOR** (Robert) — 4 KPIs + Mon travail + Consortiums séparés | KPIs portfolio : Projets supervisés, CA YTD, Marge moyenne, Approbations en attente. **Section "Mon travail personnel"** en haut (4 KPIs persos : heures sem./mois, notes de frais, congés). Liste factures à approuver. **Section "Mes consortiums" séparée et complète** : tableau consortiums + sous-tables Factures consortium + ST consortium |
| **D5** | **Dashboard BU_DIRECTOR** (Pierre) — 5 KPIs BU + Mon travail + Consortiums séparés | **Section "Mon travail personnel"** (4 KPIs persos). KPIs BU : Carnet BU, CA YTD, Taux utilisation, Consortiums actifs, Projets à risque. Tableau projets en alerte. **Section "Consortiums BU" séparée** : tableau des 3 consortiums + sous-tables Factures + Distributions à calculer |
| **D6** | **Dashboard FINANCE** (Nathalie) — Centre d'action + Notes de frais double validation + Aging en surveillance + Consortiums séparés | **Section "À traiter aujourd'hui" en premier** (5 KPIs prioritaires : timesheets, factures à soumettre, ST à payer, notes de frais, export Intacct du jour). **Section Notes de frais avec workflow PM → Directeur → Finance** (colonnes séparées). Aging factures **déplacé en bas** comme "vue de surveillance". Action panel **"Imports / Exports Intacct"** avec 4 actions (export factures, export NF, import paiements, import factures ST). **Section Consortiums séparée** en bas avec 4 KPIs spécifiques (factures consortium, ST consortium, distributions, quote-part PR YTD) |
| **D7** | **Dashboard PAIE** (Sylvie) — 4 KPIs paie + alertes contrôles | KPIs : Feuilles à valider, Alertes critiques, Périodes verrouillées, Total heures cette semaine. Tableau des 11 contrôles avec compteurs |
| **D8** | **Dashboard ADMIN** — 5 KPIs système | KPIs : Statut système, Temps de réponse moyen, Erreurs 24h, Utilisateurs actifs, Stockage. Graphique d'utilisation + journal des erreurs récentes |
| **D9** | Tous les dashboards affichent le **prénom + rôle + BU** dans le header | "Bonjour Marie 👋 — Architecte senior · BU Bâtiment · Semaine 10 (10-14 mars 2026)" |
| **D10** | Tous les dashboards exposent un endpoint backend dédié sous `/api/v1/dashboard/role/{role}/` | Réponse JSON structurée avec `kpis`, `widgets`, `actions` |
| **D11** | Aucun appel API redondant — les KPIs sont agrégés en **une seule requête** par dashboard | Chaque dashboard fait 1 requête principale au load (+ requêtes lazy pour widgets non critiques) |
| **D12** | Le DEPT_ASSISTANT et le PROPOSAL_MANAGER utilisent un dashboard "minimal" générique en Sprint 1bis | Sprint 3 (ABAC) : DEPT_ASSISTANT verra un dashboard miroir; Sprint 1.5 (module Proposals) : PROPOSAL_MANAGER aura son dashboard commercial |

### Hors scope

- ❌ Dashboards multiples épinglés par utilisateur (Sprint 2)
- ❌ Quest log gamifié (Sprint 2)
- ❌ Drill-down depuis les KPIs vers des écrans détaillés (existant à conserver, pas de nouvelle navigation)
- ❌ Customisation des KPIs par utilisateur (Sprint 3)
- ❌ Widgets drag-drop / redimensionnables (out of scope MVP)
- ❌ Mise en cache côté frontend (les KPIs sont rechargés à chaque navigation)
- ❌ Intégration WebSocket pour temps réel (Sprint 2 si demandé)
- ❌ Dashboard PROPOSAL_MANAGER complet (attend module Proposals MVP-1.5)
- ❌ Dashboard DEPT_ASSISTANT en mode miroir complet (attend ABAC Sprint 3)

---

## 3. Technical Approach

### Stack
- **Backend :** Django 6 + DRF (ajouts dans `apps/dashboards/`)
- **Frontend :** Vue 3 + TypeScript + Pinia
- **Charts :** Chart.js (déjà installé via vue-chartjs)

### Architecture Overview

```
DashboardView.vue (orchestrateur)
       │
       │  computed: roleComponent (basé sur dominantRole de useSidebarMenu)
       │
       ├─→ EmployeeDashboard.vue       (1 endpoint: /api/v1/dashboard/role/employee/)
       ├─→ PMDashboard.vue             (1 endpoint: /api/v1/dashboard/role/pm/)
       ├─→ ProjectDirectorDashboard.vue (1 endpoint: /api/v1/dashboard/role/project_director/)
       ├─→ BUDirectorDashboard.vue     (1 endpoint: /api/v1/dashboard/role/bu_director/)
       ├─→ FinanceDashboard.vue        (1 endpoint: /api/v1/dashboard/role/finance/)
       ├─→ PaieDashboard.vue           (1 endpoint: /api/v1/dashboard/role/paie/)
       ├─→ AdminDashboard.vue          (1 endpoint: /api/v1/dashboard/role/admin/)
       └─→ MinimalDashboard.vue        (fallback pour DEPT_ASSISTANT et PROPOSAL_MANAGER)
```

Chaque sous-composant :
- Importe `useDashboardStore` (Pinia)
- Au mount, appelle `store.fetchRoleDashboard(role)`
- Affiche les KPIs depuis `store.dashboards[role]`

### Backend — Nouveaux endpoints

```python
# backend/apps/dashboards/urls.py
urlpatterns = [
    # Existant (à conserver pour rétrocompatibilité)
    path("dashboard/", role_dashboard),
    path("dashboard/pm-kpis/", pm_financial_kpis),
    path("dashboard/bu-director/", bu_director_kpis),
    path("dashboard/system-health/", system_health),
    path("dashboard/hours-report/", hours_report),

    # Nouveaux — un par rôle
    path("dashboard/role/employee/", employee_dashboard),
    path("dashboard/role/pm/", pm_dashboard),
    path("dashboard/role/project_director/", project_director_dashboard),
    path("dashboard/role/bu_director/", bu_director_dashboard),
    path("dashboard/role/finance/", finance_dashboard),
    path("dashboard/role/paie/", paie_dashboard),
    path("dashboard/role/admin/", admin_dashboard),
]
```

### Backend — Format de réponse standardisé

Chaque endpoint renvoie :

```json
{
  "data": {
    "user": {
      "first_name": "Marie",
      "last_name": "Lavoie",
      "role_label": "Architecte senior",
      "business_unit": "BU Bâtiment",
      "current_week_label": "Semaine 10 (10-14 mars 2026)"
    },
    "kpis": [
      {
        "key": "hours_week",
        "label": "Heures cette semaine",
        "value": "28.5",
        "unit": "h",
        "detail": "Norme: 37.5h · Reste 9h",
        "color": "primary",
        "trend": null
      },
      ...
    ],
    "widgets": {
      "weekly_chart": {
        "days": [
          {"label": "Lun", "hours": 7.5, "color": "success"},
          {"label": "Mar", "hours": 7.5, "color": "success"},
          {"label": "Mer", "hours": 6.0, "color": "warning"},
          {"label": "Jeu", "hours": 7.5, "color": "success"},
          {"label": "Ven", "hours": 0.0, "color": "danger"}
        ]
      },
      "assigned_projects": [
        {"code": "P-2024-042", "name": "Complexe Desjardins Ph.2", "role": "Architecture", "hours_week": 15.0, "allocation_pct": 60, "pm_name": "J-F Tremblay"},
        ...
      ]
    },
    "actions": [
      {"icon": "📅", "color": "danger", "title": "Compléter feuille de temps", "detail": "Vendredi 14 mars — 0h saisies", "cta": "Saisir →", "link": "/timesheets"},
      {"icon": "🧾", "color": "warning", "title": "2 dépenses à soumettre", "detail": "Transport + repas — 87.50 $", "cta": "Soumettre →", "link": "/expenses"}
    ]
  }
}
```

### Backend — KPIs détaillés par rôle

#### EMPLOYEE (Marie)
| KPI | Source | Calcul |
|---|---|---|
| Heures cette semaine | `TimeEntry` | `SUM(hours)` where `employee=user, week=current` |
| Taux facturable | `TimeEntry` + `Phase.is_billable` | `billable_hours / total_hours × 100` |
| Projets actifs | `EmployeeAssignment` | `COUNT DISTINCT project` where `is_active=True` |
| Actions requises | Composite | `COUNT` (timesheet incomplete + expenses pending + leaves pending) |

**Widgets :**
- `weekly_chart` : tableau Lun-Ven avec `{label, hours, color}` (color basé sur ratio à norme journalière)
- `assigned_projects` : liste projets avec `code, name, role, hours_week, allocation_pct, pm_name`

#### PM (Jean-François) — Réutilise `get_pm_financial_kpis` + enrichissement
| KPI | Source |
|---|---|
| Carnet commandes | `SUM(budget_total) - SUM(invoiced)` sur projets gérés |
| Ratio CA/Salaires | `total_invoiced / (total_hours × avg_hourly_cost)` |
| Taux facturation | `billable_hours / total_hours × 100` |
| Marge moyenne | `(total_invoiced - total_costs) / total_invoiced × 100` |
| Actions requises | `WeeklyApproval` PENDING + `ExpenseReport` à valider sur projets gérés |

**Widgets :**
- `project_health` : tableau `{code, name, status_color, budget_consumed_pct, hours_pct, ca_salary, alerts}`
- `pending_approvals` : top 10 entrées à approuver

#### PROJECT_DIRECTOR (Robert) — Nouveau service
| KPI | Source |
|---|---|
| Projets supervisés | `Project.objects.filter(associate_in_charge=user)` |
| CA YTD | `Invoice.SUM(total)` sur projets supervisés, `date.year=current` |
| Marge moyenne | Idem PM mais sur projets supervisés |
| Approbations en attente | `Invoice.status='SUBMITTED'` sur projets supervisés (anti-self) |

**Widgets :**
- `pending_invoices` : factures à approuver avec préview slideover

#### BU_DIRECTOR (Pierre) — Réutilise `get_bu_director_kpis` + enrichissement
| KPI | Source |
|---|---|
| Carnet commandes BU | Somme budgets restants sur projets de la BU |
| CA facturé YTD | `Invoice.SUM(total)` BU + année courante |
| Taux utilisation | `billable_hours / total_hours` au niveau BU |
| Consortiums actifs | `Consortium.objects.filter(status='ACTIVE')` (pas filtré par BU) |
| Projets à risque | `Project` avec `health_status IN ('yellow', 'red')` |

**Widgets :**
- `at_risk_projects` : tableau projets en alerte
- `consortium_recap` : récap consortiums (FR63)

#### FINANCE (Nathalie) — Nouveau service composite
| KPI | Source |
|---|---|
| CA facturé (mois) | `Invoice.SUM(total)` mois courant |
| Comptes recevables | `Invoice.SUM(total)` `status='SENT'` |
| Heures totales (sem.) | `TimeEntry.SUM(hours)` semaine courante |
| Fournisseurs à payer | `STInvoice.SUM(amount)` `status='authorized'` |
| Timesheets à valider | `WeeklyApproval` `finance_status='PENDING'` |

**Widgets :**
- `aging_invoices` : aging 30/60/90j
- `expense_queue` : notes de frais à valider

#### PAIE (Sylvie) — Nouveau service
| KPI | Source |
|---|---|
| Feuilles à valider | `WeeklyApproval` `paie_status='PENDING'` |
| Alertes critiques | Compte des alertes `severity='error'` des 11 contrôles paie |
| Périodes verrouillées | `PeriodFreeze.objects.filter(is_active=True).count()` |
| Total heures (sem.) | `TimeEntry.SUM(hours)` semaine courante |

**Widgets :**
- `payroll_controls` : tableau des 11 contrôles avec compteurs (errors, warnings, info)
- `unlock_requests` : demandes de déverrouillage en attente

#### ADMIN — Réutilise `get_system_health` + enrichissement
| KPI | Source |
|---|---|
| Statut système | OK / DEGRADED / DOWN (basé sur Sentry events) |
| Temps réponse moyen | Moyenne `request_duration` 1h |
| Erreurs (24h) | `Sentry.events.count()` 24h |
| Utilisateurs actifs | `User.objects.filter(last_login__gte=now-1h).count()` |
| Stockage | `disk_usage_pct` |

**Widgets :**
- `recent_errors` : 5 dernières erreurs Sentry
- `usage_chart` : utilisateurs actifs/heure sur 24h

### Frontend — Composants à créer

```
frontend/src/features/dashboard/
├── views/
│   └── DashboardView.vue                 (refactor: orchestrateur)
├── components/
│   ├── KpiCard.vue                       (composant réutilisable, 1 KPI)
│   ├── WeeklyHoursChart.vue              (graphique barres Lun-Ven)
│   ├── ActionsRequiredPanel.vue          (panneau actions à droite)
│   ├── ProjectHealthTable.vue            (tableau santé projets)
│   ├── AgingInvoicesWidget.vue           (aging 30/60/90)
│   ├── PayrollControlsWidget.vue         (11 contrôles paie)
│   └── personas/
│       ├── EmployeeDashboard.vue
│       ├── PMDashboard.vue
│       ├── ProjectDirectorDashboard.vue
│       ├── BUDirectorDashboard.vue
│       ├── FinanceDashboard.vue
│       ├── PaieDashboard.vue
│       ├── AdminDashboard.vue
│       └── MinimalDashboard.vue
└── stores/
    └── useDashboardStore.ts              (nouveau)
```

### Frontend — Store Pinia

```typescript
// frontend/src/features/dashboard/stores/useDashboardStore.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import apiClient from '@/plugins/axios'

interface RoleDashboardData {
  user: { first_name: string; last_name: string; role_label: string; business_unit: string; current_week_label: string }
  kpis: Array<{ key: string; label: string; value: string; unit?: string; detail?: string; color?: string; trend?: number }>
  widgets: Record<string, unknown>
  actions: Array<{ icon: string; color: string; title: string; detail: string; cta: string; link: string }>
}

export const useDashboardStore = defineStore('dashboard', () => {
  const dashboards = ref<Record<string, RoleDashboardData>>({})
  const loading = ref<Record<string, boolean>>({})
  const errors = ref<Record<string, string | null>>({})

  async function fetchRoleDashboard(role: string) {
    loading.value[role] = true
    errors.value[role] = null
    try {
      const response = await apiClient.get(`dashboard/role/${role}/`)
      dashboards.value[role] = response.data?.data || response.data
    } catch (e) {
      errors.value[role] = 'Erreur de chargement du tableau de bord'
    } finally {
      loading.value[role] = false
    }
  }

  return { dashboards, loading, errors, fetchRoleDashboard }
})
```

### Frontend — Orchestrateur

```vue
<!-- frontend/src/features/dashboard/views/DashboardView.vue -->
<script setup lang="ts">
import { computed, defineAsyncComponent } from 'vue'
import { useSidebarMenu } from '@/shared/composables/useSidebarMenu'

const { dominantRole } = useSidebarMenu()

const DASHBOARD_COMPONENTS: Record<string, ReturnType<typeof defineAsyncComponent>> = {
  EMPLOYEE: defineAsyncComponent(() => import('../components/personas/EmployeeDashboard.vue')),
  PM: defineAsyncComponent(() => import('../components/personas/PMDashboard.vue')),
  PROJECT_DIRECTOR: defineAsyncComponent(() => import('../components/personas/ProjectDirectorDashboard.vue')),
  BU_DIRECTOR: defineAsyncComponent(() => import('../components/personas/BUDirectorDashboard.vue')),
  FINANCE: defineAsyncComponent(() => import('../components/personas/FinanceDashboard.vue')),
  PAIE: defineAsyncComponent(() => import('../components/personas/PaieDashboard.vue')),
  ADMIN: defineAsyncComponent(() => import('../components/personas/AdminDashboard.vue')),
  DEPT_ASSISTANT: defineAsyncComponent(() => import('../components/personas/MinimalDashboard.vue')),
  PROPOSAL_MANAGER: defineAsyncComponent(() => import('../components/personas/MinimalDashboard.vue')),
}

const DashboardComponent = computed(() =>
  DASHBOARD_COMPONENTS[dominantRole.value] || DASHBOARD_COMPONENTS.EMPLOYEE
)
</script>

<template>
  <component :is="DashboardComponent" />
</template>
```

### Tests

**Backend (pytest) :**
- Test 1 endpoint par rôle = 7 nouveaux tests qui vérifient :
  - Code 200 avec utilisateur du bon rôle
  - Structure JSON conforme (`data.user`, `data.kpis`, `data.widgets`, `data.actions`)
  - KPIs présents avec les bonnes clés
  - Code 403 si l'utilisateur n'a pas le rôle requis (sauf admin qui peut accéder à tous)

**Frontend (Vitest) :**
- Test du store : `fetchRoleDashboard` met bien à jour `dashboards[role]`
- Test de l'orchestrateur : sélectionne le bon composant selon `dominantRole`
- Smoke test de chaque composant persona : se monte sans erreur avec données mockées

---

## 4. Implementation Plan

### Stories (8 stories pour 2-3 jours)

#### Story 1 : Backend — services + endpoints (4 nouveaux rôles)
**Durée :** 5h
**Livrable :**
- `apps/dashboards/services.py` enrichi avec :
  - `get_employee_dashboard(user, tenant_id)`
  - `get_finance_dashboard(user, tenant_id)`
  - `get_paie_dashboard(user, tenant_id)`
  - `get_project_director_dashboard(user, tenant_id)`
- `apps/dashboards/views.py` : 7 nouveaux endpoints
- `apps/dashboards/urls.py` : routage `/api/v1/dashboard/role/{role}/`
- Format JSON standardisé `{user, kpis, widgets, actions}` pour tous

#### Story 2 : Backend — tests pytest
**Durée :** 3h
**Livrable :**
- `apps/dashboards/tests/test_views.py` enrichi avec 7 nouveaux tests
- Coverage : 1 test happy path + 1 test forbidden par endpoint

#### Story 3 : Frontend — store + composants partagés
**Durée :** 2h
**Livrable :**
- `useDashboardStore.ts` (Pinia)
- `KpiCard.vue` (composant réutilisable accentué par couleur)
- `WeeklyHoursChart.vue` (Chart.js bar chart)
- `ActionsRequiredPanel.vue` (slideover-friendly)

#### Story 4 : Frontend — DashboardView orchestrateur + EmployeeDashboard
**Durée :** 3h
**Livrable :**
- Refactor `DashboardView.vue` en orchestrateur
- Création `EmployeeDashboard.vue` strictement aligné sur le mockup `dash-emp` du flux-08
- Test visuel avec `employe@test.com`

#### Story 5 : Frontend — PMDashboard + ProjectDirectorDashboard + BUDirectorDashboard
**Durée :** 4h
**Livrable :**
- Les 3 composants Direction
- Réutilisation du `ProjectHealthTable.vue`
- Tests visuels avec `pm@test.com`, `director@test.com`, et créer un PROJECT_DIRECTOR si besoin

#### Story 6 : Frontend — FinanceDashboard + PaieDashboard
**Durée :** 4h
**Livrable :**
- `FinanceDashboard.vue` avec `AgingInvoicesWidget`
- `PaieDashboard.vue` avec `PayrollControlsWidget`
- Tests visuels avec `finance@test.com` et `paie@test.com`

#### Story 7 : Frontend — AdminDashboard + MinimalDashboard
**Durée :** 2h
**Livrable :**
- `AdminDashboard.vue` (réutilise les KPIs `get_system_health`)
- `MinimalDashboard.vue` (fallback générique pour DEPT_ASSISTANT et PROPOSAL_MANAGER)
- Test visuel avec `admin@provencher-roy.com`

#### Story 8 : Tests Vitest + déploiement
**Durée :** 3h
**Livrable :**
- Tests Vitest store + orchestrateur
- Build production OK
- Commit + push GitHub
- Déploiement Hostinger
- Validation post-déploiement avec 5 personas

### Order d'implémentation
1 → 2 (backend complet, peut être déployé indépendamment)
3 → 4 → 5 → 6 → 7 (frontend incrémental)
8 (validation finale)

---

## 5. Acceptance Criteria

- [ ] 7 nouveaux endpoints backend `/api/v1/dashboard/role/{role}/` répondent avec le format JSON standardisé
- [ ] Marie (`employe@test.com`) voit le dashboard EMPLOYEE avec ses 4 KPIs + graphique semaine + projets assignés + actions requises
- [ ] Jean-François (`pm@test.com`) voit le dashboard PM avec ses 5 KPIs financiers + santé projets
- [ ] Nathalie (`finance@test.com`) voit le dashboard FINANCE avec ses 5 KPIs + aging factures
- [ ] Sylvie (`paie@test.com`) voit le dashboard PAIE avec ses 4 KPIs + tableau des 11 contrôles
- [ ] Pierre (à créer ou tester via admin avec role BU_DIRECTOR) voit le dashboard BU_DIRECTOR
- [ ] Robert (à créer ou tester avec role PROJECT_DIRECTOR) voit le dashboard PROJECT_DIRECTOR
- [ ] L'admin voit le dashboard ADMIN avec les KPIs système
- [ ] DEPT_ASSISTANT et PROPOSAL_MANAGER voient le `MinimalDashboard` de fallback
- [ ] Le `DashboardView.vue` charge dynamiquement le bon composant selon `dominantRole`
- [ ] Aucun appel API n'est fait pour les KPIs d'un rôle que l'utilisateur ne consulte pas
- [ ] Tous les tests backend passent (`docker compose exec django pytest apps/dashboards/`)
- [ ] Le build Vite passe sans erreur
- [ ] L'application est déployée sur Hostinger
- [ ] L'utilisateur peut switcher entre les comptes seed et observer un dashboard différent à chaque fois

---

## 6. Non-Functional Requirements

### Performance
- **NFR-D1 :** Le chargement initial d'un dashboard doit être < 1.5s sur connexion 4G
- **NFR-D2 :** Une seule requête HTTP au load (les widgets sont inclus dans la réponse principale)
- **NFR-D3 :** Les agrégations SQL doivent utiliser des `aggregate()` Django et non des boucles Python
- **NFR-D4 :** Les requêtes complexes (santé projets) doivent être indexées correctement

### Security
- **NFR-D5 :** Chaque endpoint vérifie que l'utilisateur a le rôle correspondant (pas d'EMPLOYEE qui appelle `/dashboard/role/admin/`)
- **NFR-D6 :** Les KPIs financiers sont filtrés par `tenant_id` strictement
- **NFR-D7 :** Les `salary_cost` et `cost_data` ne sont retournés que pour les rôles autorisés (`CostFieldFilterMixin`)

### Accessibility
- **NFR-D8 :** Tous les KPIs ont un `aria-label` descriptif
- **NFR-D9 :** Les couleurs vert/jaune/rouge sont accompagnées d'icônes ou de texte (daltonisme)
- **NFR-D10 :** Les graphiques Chart.js incluent un fallback texte

### UX
- **NFR-D11 :** Les dashboards sont mobile-friendly (>= 768px)
- **NFR-D12 :** Les KPIs ont un ordre cohérent : le plus important en premier (à gauche)
- **NFR-D13 :** Les valeurs monétaires sont formatées en français (`28 500 $` et non `$28,500`)

---

## 7. Dependencies, Risks, Timeline

### Dependencies
- ✅ Sprint 1 sidebar (le composable `useSidebarMenu` doit exister pour fournir `dominantRole`)
- ✅ Services backend `get_role_dashboard_kpis`, `get_pm_financial_kpis`, `get_bu_director_kpis`, `get_system_health` existent déjà (à enrichir)
- ✅ Chart.js + vue-chartjs déjà dans les dépendances frontend
- ✅ Comptes de test seed couvrant les rôles principaux
- ⚠️ Pas de compte PROJECT_DIRECTOR seed — à ajouter dans `seed_test_users.py` (1 ligne)

### Risks

| Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|
| **Performance des agrégations sur grosses BU** | Moyenne | Moyen | Profiling Django Debug Toolbar + `select_related`/`prefetch_related` ; cache Redis si besoin (Sprint 2) |
| **Données absentes pour un rôle (ex: pas de projet)** | Forte | Faible | Empty states gérés explicitement dans chaque composant persona |
| **Discordance entre KPI affiché et la donnée réelle** | Moyenne | Élevé | Tests pytest qui vérifient les calculs sur des fixtures |
| **Composants persona divergent du mockup** | Moyenne | Faible | Validation visuelle manuelle obligatoire avant push |
| **Surcharge cognitive si trop d'infos par dashboard** | Faible | Moyen | Respect strict du mockup (max 5 KPIs + 2 widgets + 1 panel actions) |

### Timeline
- **Démarrage :** Après livraison du Sprint 1 sidebar (dépendance dure sur `useSidebarMenu`)
- **Story 1 (services backend) :** Jour 1 matin (5h)
- **Story 2 (tests backend) :** Jour 1 après-midi (3h)
- **Story 3 (composants partagés) :** Jour 2 matin (2h)
- **Story 4 (orchestrateur + Employee) :** Jour 2 matin/après-midi (3h)
- **Story 5 (PM + PD + BU) :** Jour 2 après-midi / Jour 3 matin (4h)
- **Story 6 (Finance + Paie) :** Jour 3 (4h)
- **Story 7 (Admin + Minimal) :** Jour 3 (2h)
- **Story 8 (tests + déploiement) :** Jour 3 (3h)
- **Total :** ~26h de dev = **2.5-3 jours ouvrés**
- **Cible de livraison :** **2026-04-16** (en supposant Sprint 1 sidebar livré le 2026-04-13)

### Milestones
- **M1 (J1, fin) :** Backend complet avec 7 endpoints + tests verts
- **M2 (J2, fin) :** EmployeeDashboard + PMDashboard livrés et testés
- **M3 (J3, fin) :** Tous les dashboards livrés, déployés et validés sur Hostinger

---

## 8. Success Metrics (post-deployment)

À mesurer après 1 semaine :

1. **Temps de chargement moyen** : < 1.5s par dashboard (mesurer via Lighthouse / Sentry)
2. **Taux d'engagement** : % d'utilisateurs qui restent > 30s sur leur dashboard (vs. simplement passer à un autre écran)
3. **Réduction des questions support** : "Comment je trouve X ?" → -50% (les actions requises pointent directement vers les écrans)
4. **NPS sur le dashboard** : Mini-sondage 1 question après 1 semaine d'usage

---

## 9. Next Steps After This Sprint

Une fois Sprint 1bis livré :
- **Sprint 2 (Proposition B)** : Ajouter section "Aujourd'hui" en tête du sidebar (intégrera une partie des actions du dashboard)
- **Sprint 2 (Proposition B)** : Dashboards multiples épinglés par utilisateur
- **Sprint 3 (Proposition C)** : Dashboards customisables via la matrice ABAC

---

## 10. Sign-off

| Rôle | Nom | Date | Statut |
|---|---|---|---|
| Product Owner | Philippe Haumesser | 2026-04-11 | À valider |
| Tech Lead | Philippe Haumesser | 2026-04-11 | À valider |

**Prochaine étape :** Validation par Philippe → bascule vers l'implémentation après Sprint 1 sidebar (Story 1 = backend services).
