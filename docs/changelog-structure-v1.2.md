# Refonte structure WBS — v1.2 (2026-06-06)

Refonte du modèle de structure projet : **« la phase est un regroupement standard, la tâche (et la sous-tâche) est l'unité opérationnelle »**.

## Principe

| Niveau | Rôle | Porte les données ? |
|---|---|---|
| **Phase** | Regroupement **standard** du cabinet (paramétrage) | ❌ agrégat lecture seule |
| **Tâche** sans sous-tâche (feuille) | Unité de saisie | ✅ budget, dates, planif, facturation, temps |
| **Tâche-mère** (avec sous-tâches) | Regroupement | ❌ agrégat lecture seule |
| **Sous-tâche** | Unité de saisie (feuille) | ✅ idem feuille |

Règle unique : **budget / heures / dates / planification / facturation / saisie de temps vivent sur les feuilles** (nœuds sans enfant). Phase et tâche-mère **agrègent** (Σ / min-max), sans double-comptage.

## Modèle de données

- **Nouveau `StandardPhase`** (`projects`, tenant-scoped, unique `(tenant, code)`, `is_mandatory`, `is_active`) — jeu global de phases standard, paramétrage **admin uniquement**. Seed : `python manage.py seed_standard_phases` (idempotent). Jeu canonique : Étude préparatoire, Concept, Préliminaire, Définitif, Appel d'offres, Surveillance, Gestion de projet (oblig.), Qualité.
- **`WBSElement` supprimé** (déprécié, remplacé par `Task`) — migration `0012_delete_wbselement`.
- Migration de cadrage `time_entries 0007` (options de champs, non destructif).

## API

- `PhaseViewSet` (projet) : lecture pour tout authentifié, **écriture réservée ADMIN** (les PM ne définissent pas les phases).
- `StandardPhaseViewSet` `/api/v1/standard_phases/` : lecture authentifiée, écriture ADMIN.
- `PhaseSerializer` : agrégats `tasks_budgeted_hours/cost`, `planned_hours`, `actual_hours`, `tasks_start_date/end_date`, `has_tasks`, `task_count` (Σ des tâches saisissables ; planif/réel via `task__phase`).
- `TaskSerializer` : `is_chargeable` (feuille), `effective_budgeted_hours/cost`, planif/réel en rollup pour les mères.
- Création projet (`create_project_from_template`) : instancie les phases depuis `StandardPhase` (fallback template si non paramétré).

## Frontend

- **Structure › Phases** : budget/heures en lecture seule (Σ tâches), formulaire allégé (nom/libellé/type/ordre), phases vides marquées « Sans tâche », édition réservée admin.
- **Structure › Tâches** : la feuille porte le budget (éditable) ; tâche-mère en lecture seule (rollup) ; actions « Déplacer » (ré-imputation) et « + Tâche » avec sélecteur de phase ; phases vides masquées.
- **Avenant** : ajoute/modifie des **tâches** sur les phases standard (badge `AV-n`) ; **plus d'allocation/planification** dans le slide-over.
- **Gantt** (planification) : tâches/sous-tâches affichées par défaut et cliquables ; **tâche-mère non cliquable** (agrégat) ; **phases sans tâche masquées** ; barre seulement si la tâche a ses propres dates ; **contrôle budget non bloquant** (rouge si planifié > budget). `PhaseSlideOver` en lecture seule.
- **Vue d'ensemble** : table phases sur les agrégats ; KPI « Heures planifiées ».
- **Paramétrage** : écran *Administration › Phases standard* (CRUD admin).

## Cohérence (règles métier)

Voir [.claude/rules/domain.md](../.claude/rules/domain.md) — section « Hiérarchie projet ». Garde-fous à remonter : budget/planif au niveau phase, phase modifiée par non-admin, double-comptage d'agrégat, réapparition de `WBSElement`.

## Reste à faire (chantier B — non livré)

- **Saisie de temps « par tâche »** : la feuille de temps enregistre encore les heures au niveau **phase**. Migration du module timesheet (grille hebdo, contrainte d'unicité, verrous, approbations) à cadrer (maquette d'abord).
