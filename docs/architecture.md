# Architecture

## Stack technique

| Composant | Technologie |
|-----------|------------|
| Backend | Django 6.0 + Django REST Framework |
| Frontend | Vue 3 + TypeScript + Pinia + TailwindCSS |
| Base de données | PostgreSQL 16 |
| Cache / Queue | Redis 7 |
| Tâches async | Celery + Celery Beat |
| Conteneurs | Docker + Docker Compose |
| API docs | drf-spectacular (OpenAPI 3) |
| PDF | Reportlab + Matplotlib |
| Excel | openpyxl |

## Structure du projet

```
ERP/
├── backend/
│   ├── apps/
│   │   ├── core/           # Tenant, RLS, roles, auth, taxes, labor rules
│   │   ├── projects/       # Projets, phases, tâches, WBS, templates
│   │   ├── clients/        # Clients, contacts, adresses
│   │   ├── time_entries/   # Feuilles de temps, approbations, verrouillage
│   │   ├── billing/        # Facturation, paiements, retenues, taxes
│   │   ├── expenses/       # Dépenses, catégories, workflow
│   │   ├── suppliers/      # Fournisseurs, factures ST, retenues
│   │   ├── consortiums/    # Consortiums, membres, vue duale
│   │   ├── leaves/         # Congés, banque, types
│   │   ├── planning/       # Allocations, jalons, disponibilité, Gantt
│   │   ├── dashboards/     # KPIs, rapports, system health
│   │   ├── data_ops/       # Import/export, Intacct CSV
│   │   └── notifications/  # Notifications in-app
│   ├── config/             # Settings, URLs, Celery
│   └── manage.py
├── frontend/
│   ├── src/
│   │   ├── features/       # Modules par domaine (projects, billing, etc.)
│   │   ├── shared/         # Layouts, composables, plugins
│   │   ├── router/         # Routes + guards RBAC
│   │   ├── locales/        # i18n FR/EN
│   │   └── plugins/        # Axios, i18n
│   └── package.json
├── docs/                   # Documentation
├── docker-compose.yml
└── _bmad-output/           # Planning artifacts (PRD, epics, mockups)
```

## Multi-tenancy

- Modèle `TenantScopedModel` — tous les modèles métier héritent de ce mixin
- Header `X-Tenant-Id` pour le scoping API
- `UserTenantAssociation` lie un user Django à un tenant
- Row-Level Security implicite via les querysets filtrés

## Rôles RBAC (8 rôles)

| Rôle | Description |
|------|------------|
| ADMIN | Accès total, configuration |
| FINANCE | Facturation, paiements, dépenses, exports |
| PM | Chef de projet — projets, approbations, planification |
| PROJECT_DIRECTOR | Directeur de projet — vision globale |
| BU_DIRECTOR | Directeur d'unité — KPIs BU |
| DEPT_ASSISTANT | Assistante — saisie projets, délégation |
| PAIE | Paie — validation, contrôles, verrouillage |
| EMPLOYEE | Employé — saisie temps, congés, dépenses |

## Schéma de données simplifié

```
Tenant ─── Project ─── Phase ─── Task
              │           │         │
              │           │     TimeEntry
              │           │
              ├── Invoice ─── InvoiceLine
              │
              ├── EmployeeAssignment
              │
              ├── Amendment
              │
              └── Consortium ─── ConsortiumMember
```
