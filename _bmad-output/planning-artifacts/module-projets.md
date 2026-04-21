# Module Projets — Spécification complète

**Version:** 1.2.000
**Date:** 2026-04-21
**Statut:** Bloc 1 complet (~95%) — finalisation en cours, audit d'alignement code/doc le 2026-04-21

---

## 1. Vue d'ensemble

Le module Projets est le **cœur de l'ERP**. Tous les autres modules (feuilles de temps, facturation, dépenses, ST, planification) sont liés aux projets. Il permet de créer, configurer, **planifier** et piloter l'ensemble des projets du cabinet d'architecture depuis une interface centralisée.

### 1.1 Objectifs

- Créer des projets depuis des **templates pré-configurés** (phases + tâches déployées automatiquement)
- Gérer la **structure WBS** sur 3 niveaux (Phase → Tâche → Sous-tâche) avec codes WBS (3.1, 3.2, 3.2.1)
- **Planifier les projets** : dates par phase/tâche, Gantt interactif, dépendances FS/SS, affectation des ressources et charge équipe
- Suivre le **budget par tâche** et les honoraires
- Suivre l'**avancement** (% par tâche, planifié vs réel)
- **Facturer par tâche** (pas par phase)
- Saisir les **feuilles de temps par tâche**
- Piloter la **marge** et la **rentabilité** (CA - Coûts)

### 1.2 Acteurs et rôles

| Rôle | Actions |
|------|---------|
| **Assistante (DEPT_ASSISTANT)** | Crée et saisit les projets, assigne PM/personnel, planifie les heures, **contrôle les feuilles de temps**, **crée des factures** |
| **Chef de projet (PM)** | Crée et saisit les projets, consulte, saisit l'avancement, planifie les heures, valide les feuilles de temps (1er niveau), **valide les factures (1er niveau)** |
| **Finance (FINANCE)** | Crée et saisit les projets, modifie les budgets, **crée des factures**, **valide les factures (2e niveau)**, suit les honoraires, assure la **rentabilité des projets** |
| **Associé en charge (PROJECT_DIRECTOR)** | Supervise les projets sous sa responsabilité, **approuve les avenants** |
| **Employé (EMPLOYEE)** | Consulte les projets assignés, saisit les feuilles de temps |
| **Admin (ADMIN)** | Accès complet |

**Notes importantes** :
- La **saisie initiale d'un projet** peut être faite par : Assistante, Chef de projet, ou Finance
- La **création d'une facture** peut être faite par : Assistante ou Finance
- La **validation des factures** est à deux niveaux : PM (1er) puis Finance (2e)
- La **validation des avenants** est du ressort de l'**Associé en charge**

---

## 2. Architecture des données

### 2.1 Modèle hiérarchique (WBS Option B — 3 niveaux)

```
Projet (PR-2026-001)
├── Phase 1: Concept (conteneur)
│   ├── Tâche 1.1: Analyse conditions existantes (opérationnel)
│   ├── Tâche 1.2: Esquisse et options
│   │   ├── Sous-tâche 1.2.1: Options préliminaires
│   │   └── Sous-tâche 1.2.2: Option retenue
│   └── Tâche 1.3: Estimation classe D
├── Phase 2: Préliminaire
│   ├── Tâche 2.1: Plans préliminaires
│   └── Tâche 2.2: Devis préliminaires
├── Phase 3: Définitif
│   ├── Tâche 3.1: Plans architecturaux détaillés
│   ├── Tâche 3.2: Plans structure et fondations
│   └── Tâche 3.3: Plans et devis MEP
├── Phase 4: Appel d'offres
├── Phase 5: Surveillance (HORAIRE)
├── Phase QA: Qualité (SUPPORT)
└── Phase GP: Gestion de projet (SUPPORT)
```

**Principes clés :**
- La **Phase** est un conteneur de regroupement (type REALIZATION ou SUPPORT)
- La **Tâche** est l'unité opérationnelle (facturation, feuilles de temps, budget)
- La **Sous-tâche** est une subdivision optionnelle d'une tâche (via `parent` FK self-ref sur Task)
- Le **code WBS** (1.2, 1.2.1) identifie chaque élément de manière unique dans le projet
- Les feuilles de temps sont saisies **par tâche ou sous-tâche**
- La facturation se fait **par tâche**

### 2.2 Modèle Project

| Champ | Type | Description |
|-------|------|-------------|
| `code` | CharField (db_indexed) | Code projet unique (PR-2026-001) — unique par tenant |
| `name` | CharField | Nom du projet |
| `client` | FK Client | Client (nullable pour projets internes) |
| `template` | FK ProjectTemplate | Template utilisé à la création |
| `contract_type` | CharField | FORFAITAIRE / CONSORTIUM / CO_DEV / CONCEPTION_CONSTRUCTION |
| `status` | CharField | ACTIVE / ON_HOLD / COMPLETED / CANCELLED |
| `is_internal` | Boolean | Projet interne (sans client) |
| `is_public` | Boolean | Projet public (vs privé) |
| `is_consortium` | Boolean | Projet en consortium (module consortium reporté) |
| `consortium` | FK Consortium (nullable) | Lien vers l'entité consortium si applicable |
| `services_transversaux` | JSONField | Liste des services transversaux (BIM, PAYSAGE, DD, CIVIL, PATRIMOINE, DESIGN_INT, ECLAIRAGE) |
| `business_unit` | CharField | Unité d'affaires |
| `legal_entity` | CharField | Entité juridique |
| `start_date` / `end_date` | DateField | Dates du projet |
| `construction_cost` | DecimalField | Coût de construction estimé |
| `address`, `city`, `postal_code`, `country` | CharField | Localisation du projet |
| `surface` | DecimalField | Superficie |
| `surface_unit` | CharField | m² ou pi² |
| `currency` | CharField | Devise (défaut: CAD) |
| `tags` | JSONField | Étiquettes |
| `title_on_invoice` | CharField | Titre affiché sur les factures |
| `total_fees` | DecimalField | Honoraires totaux HT |
| `fee_calculation_method` | CharField | FORFAIT / COUT_TRAVAUX / HORAIRE |
| `fee_rate_pct` | DecimalField | % du coût de construction |
| `pm` | FK User | Chef de projet |
| `associate_in_charge` | FK User | Associé en charge |
| `invoice_approver` | FK User | Approbateur final factures (Finance, 2e niveau) |
| `bu_director` | FK User | Directeur d'unité |

**Mixins** : TenantScopedModel (isolation), VersionedModel (optimistic locking via header `If-Match`), HistoricalRecords (django-simple-history).

### 2.3 Modèle Phase

| Champ | Type | Description |
|-------|------|-------------|
| `code` | CharField | Code phase (1, 2, 3, QA, GP) |
| `name` | CharField | Nom (Concept, Préliminaire, Définitif, Qualité…) |
| `client_facing_label` | CharField | Libellé client |
| `phase_type` | CharField | REALIZATION / SUPPORT |
| `billing_mode` | CharField | FORFAIT / HORAIRE |
| `order` | Integer | Ordre d'affichage |
| `start_date` / `end_date` | DateField | Dates de la phase |
| `is_mandatory` | Boolean | Phase obligatoire (non supprimable) |
| `is_locked` | Boolean | Phase verrouillée |
| `budgeted_hours` | DecimalField | Heures budgétées |
| `budgeted_cost` | DecimalField | Budget |

### 2.4 Modèle Task

Remplace `WBSElement` (deprecated — retrait planifié, voir §10).

| Champ | Type | Description |
|-------|------|-------------|
| `wbs_code` | CharField | Code WBS unique dans le projet (3.1, 3.2.1) |
| `name` | CharField | Nom de la tâche |
| `client_facing_label` | CharField | Libellé client |
| `phase` | FK Phase | Phase parente |
| `parent` | FK Task (self) | Tâche parente (pour sous-tâches) |
| `task_type` | CharField | TASK / SUBTASK |
| `billing_mode` | CharField | FORFAIT / HORAIRE |
| `order` | Integer | Ordre |
| `start_date` / `end_date` | DateField | Dates de la tâche (ajouté migration 0007) |
| `budgeted_hours` | DecimalField | Heures budgétées |
| `budgeted_cost` | DecimalField | Budget |
| `hourly_rate` | DecimalField | Taux horaire (pour HORAIRE) |
| `is_billable` | Boolean | Facturable |
| `is_active` | Boolean | Active |
| `progress_pct` | DecimalField | % avancement (0-100) |

**Contrainte unique :** `(project, wbs_code)` — un code WBS ne peut apparaître qu'une fois par projet.

### 2.5 Modèle FinancialPhase

Couche financière groupant des phases de réalisation pour le pilotage budgétaire et la facturation agrégée.

| Champ | Type | Description |
|-------|------|-------------|
| `name` | CharField | Nom de la phase financière |
| `code` | CharField | Code |
| `billing_mode` | CharField | FORFAIT / HORAIRE |
| `fixed_amount` | DecimalField | Montant fixe (pour FORFAIT) |
| `hourly_budget_max` | DecimalField | Budget horaire max |
| `project` | FK Project | Projet rattaché |

### 2.6 Modèle Amendment (Avenants)

Implémenté techniquement — **UX complète et validation fonctionnelle à finaliser** (voir §9). **Approbation par l'Associé en charge.**

| Champ | Type | Description |
|-------|------|-------------|
| `amendment_number` | CharField | Numéro séquentiel (auto-incrémenté par projet) |
| `description` | TextField | Description de l'avenant |
| `status` | CharField | DRAFT / SUBMITTED / APPROVED / REJECTED |
| `budget_impact` | DecimalField | Impact budgétaire (positif ou négatif) |
| `approval_date` | DateField | Date d'approbation |
| `project` | FK Project | Projet principal |
| `requested_by` | FK User | Demandeur (Assistante, PM ou Finance) |
| `approved_by` | FK User | Approbateur (**Associé en charge**) |

**Mixins** : VersionedModel, HistoricalRecords. **Contrainte unique** : `(project, amendment_number)`.

### 2.7 Modèle SupportService

Services transversaux du cabinet (BIM, Paysage, Design intérieur, etc.) budgétables et facturables.

| Champ | Type |
|-------|------|
| `code`, `name`, `client_facing_label` | CharField |
| `budgeted_hours`, `budgeted_cost` | DecimalField |
| `billing_mode`, `is_billable` | CharField / Boolean |
| `project` | FK Project |

---

## 3. Templates de projet

### 3.1 Template "Architecture standard" (ARCH-STD)

**Total : 7 phases, 23 tâches**

```
Phase 1: Concept (obligatoire, FORFAIT)
├── 1.1 Analyse conditions existantes
├── 1.2 Esquisse et options conceptuelles
└── 1.3 Estimation classe D

Phase 2: Préliminaire (obligatoire, FORFAIT)
├── 2.1 Plans préliminaires
├── 2.2 Devis préliminaires
└── 2.3 Estimation classe C

Phase 3: Définitif (obligatoire, FORFAIT)
├── 3.1 Plans architecturaux détaillés
├── 3.2 Plans structure et fondations
├── 3.3 Plans et devis MEP
├── 3.4 Devis quantitatif
└── 3.5 Estimation classe B

Phase 4: Appel d'offres (optionnel, FORFAIT)
├── 4.1 Préparation documents d'appel d'offres
├── 4.2 Analyse des soumissions
└── 4.3 Recommandation d'attribution

Phase 5: Surveillance (optionnel, HORAIRE @ 125$/h)
├── 5.1 Surveillance de chantier
├── 5.2 Réunions de chantier
└── 5.3 Inspection et réception

Phase QA: Qualité (SUPPORT, FORFAIT)
├── QA.1 Contrôle qualité plans (non facturable)
├── QA.2 Revue de conformité (non facturable)
└── QA.3 Vérification normes (non facturable)

Phase GP: Gestion de projet (obligatoire, SUPPORT, FORFAIT)
├── GP.1 Coordination équipe (non facturable)
├── GP.2 Réunions client (facturable)
└── GP.3 Administration projet (non facturable)
```

### 3.2 Déploiement du template

Quand l'acteur (Assistante, PM ou Finance) crée un projet et choisit un template :
1. Les phases se créent automatiquement
2. Les tâches se créent sous chaque phase avec leur code WBS
3. L'acteur peut ajouter/supprimer des phases et tâches
4. Les phases obligatoires (Concept, Préliminaire, Définitif, Gestion de projet) ne peuvent pas être supprimées

Source : [seed_templates.py](../../backend/apps/projects/management/commands/seed_templates.py).

---

## 4. Onglets du projet (12 onglets)

### 4.1 Vue d'ensemble
- Informations projet (code, nom, client, dates, statut)
- KPIs : utilisation %, heures consommées, heures budgétées
- Mode lecture / édition

### 4.2 Phases
- CRUD phases avec édition inline
- Assignation d'employés par phase (bouton "Affecter")
- Badge obligatoire / optionnel
- Dates début/fin

### 4.3 Tâches (WBS)
- Tâches **groupées par phase** avec en-têtes dépliables
- Colonnes : WBS Code | Nom | Mode | Budget ($) | Heures | Facturable | Actions
- Budget et heures éditables inline (ADMIN/FINANCE uniquement)
- Ajout/suppression de tâches par phase
- Badge TASK / SUBTASK
- Support sous-tâches via FK `parent`

### 4.4 Équipe
- Assignation d'employés aux phases/tâches (via ResourceAllocation du module planning)
- Nom, phase, %, période
- Max 100% par phase, anti-doublon personne/phase

### 4.5 Budget
- **Section Honoraires** : montant total HT, méthode de calcul, taux
- **KPI cards** : Budget total, Facturé, % consommé, Solde
- **Table budget par tâche** groupée par phase
- Budget éditable inline (ADMIN/FINANCE)
- Bouton "Créer une facture" (accessible à Assistante ou Finance)

### 4.6 Avancement
- Tâches groupées par phase
- **% avancement saisissable** par tâche (0-100, sauvegarde au blur)
- Colonnes : WBS, Tâche, Budget, Heures planifiées, Heures réelles, % Avancement, Écart
- Code couleur écart : vert (<10%), ambre (10-25%), rouge (>25%)
- Totaux par phase

### 4.7 Avenants ⚠️ *UX à finaliser (voir §9)*
- CRUD avenants avec workflow (Brouillon → Soumis → Approuvé/Rejeté)
- Saisie par Assistante, PM ou Finance
- **Approbation par l'Associé en charge**
- Impact budget ±
- Numéro auto-incrémenté
- Historique des modifications

### 4.8 Sous-traitants
- Liste des factures ST liées au projet
- Colonnes : Fournisseur, No facture, Date, Montant, Refacturable, Statut
- Totaux

### 4.9 Finance
- **5 KPI cards** : CA facturé, Coûts salaires, Coûts ST, Marge, Marge %
- Pilotage de la rentabilité projet (rôle Finance)
- Table résumé par année (*placeholder — lien avec données réelles à faire*)

### 4.10 Facturation
- Liste des factures du projet
- Colonnes : No facture, Statut, Montant, Dates
- Bouton "Créer une facture" (accessible à **Assistante ou Finance**)
- **Workflow de validation** :
  1. Création : **Assistante** ou **Finance**
  2. Validation 1er niveau : **Chef de projet (PM)**
  3. Validation 2e niveau : **Finance** → envoi au client → numéro définitif FAC-YYYY-XXXXX
- Lien vers la fiche facture

### 4.11 Gantt
- Gantt interactif dédié : phases + tâches
- Zoom, milestones, dépendances FS/SS (modèle + API)
- Édition dates par drag

### 4.12 Documents / Métadonnées
- Documents attachés au projet
- Historique des changements (django-simple-history)

---

## 5. Workflows

### 5.1 Création de projet (Wizard 5 étapes)

La saisie initiale peut être effectuée par **Assistante, Chef de projet, ou Finance**.

```
1. Étape 1 — Identification
   Code, nom, client, BU, entité juridique, dates, adresse,
   surface, services transversaux, PM, Associé en charge,
   approbateur facture (Finance), is_public, consortium (optionnel)
2. Étape 2 — Budget & Phases
   Heures et coûts budgétés par phase/tâche
3. Étape 3 — Ressources
   Affectation de profils (virtuels puis réels)
4. Étape 4 — Sous-traitants
   Budget ST, refacturable/absorbé (optionnel)
5. Étape 5 — Confirmation
   Récapitulatif + création (statut = ACTIVE)
```

### 5.2 Vie du projet
```
6. Assistante/PM assigne le personnel (à la demande du PM)
7. Assistante/PM planifie les heures par tâche
8. PM consulte budget, heures, avancement
9. PM saisit % avancement par tâche
10. Avenants : création (Assistante/PM/Finance) → approbation Associé en charge → impact budget
11. ST : mandats liés aux tâches
12. Contrôle des feuilles de temps : Assistante contrôle, PM valide (1er niveau)
```

### 5.3 Facturation depuis le projet
```
13. Assistante ou Finance → onglet Facturation → "Créer facture"
14. Lignes pré-remplies par TÂCHE (budget, facturé à ce jour)
15. Assistante/Finance saisit "à facturer ce mois"
16. Chef de projet (PM) valide (1er niveau)
17. Finance valide (2e niveau) et envoie → numéro définitif FAC-YYYY-XXXXX
```

### 5.4 Clôture
```
18. PM → statut COMPLETED
19. Vérifications : tout facturé ? heures verrouillées ? ST payés ?
```

---

## 6. API Endpoints

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET/POST | `/api/v1/projects/` | Liste / Créer projet |
| GET/PATCH/DELETE | `/api/v1/projects/{id}/` | Détail / Modifier / Supprimer |
| POST | `/api/v1/projects/{id}/create_from_template/` | Créer depuis template |
| GET | `/api/v1/projects/{id}/dashboard/` | KPIs projet (health, heures, budget) |
| GET | `/api/v1/projects/{id}/team_stats/` | Statistiques équipe |
| GET/POST | `/api/v1/projects/{id}/phases/` | CRUD phases |
| GET/POST/PATCH/DELETE | `/api/v1/projects/{id}/tasks/` | CRUD tâches |
| GET/POST | `/api/v1/projects/{id}/amendments/` | CRUD avenants |
| GET/POST | `/api/v1/project_templates/` | CRUD templates |
| ~~GET/POST~~ | ~~`/api/v1/projects/{id}/wbs/`~~ | **DEPRECATED** — utiliser `/tasks/` (retrait planifié §10) |

**Permissions** :
- Toutes les vues : `IsAuthenticated`
- EMPLOYEE : voit uniquement les projets assignés via ResourceAllocation
- Transitions de statut validées (dict `VALID_TRANSITIONS`) : COMPLETED/CANCELLED sont terminaux
- Suppression phase refusée si `is_mandatory=True`
- Suppression template refusée si utilisé par un projet (409 TEMPLATE_IN_USE)

---

## 7. Lien avec les autres modules

| Module | Lien avec Projet |
|--------|-----------------|
| **Feuilles de temps** | Saisie par tâche (FK `task` sur TimeEntry), contrôle Assistante, validation PM |
| **Facturation** | Lignes par tâche (FK `task` sur InvoiceLine), création Assistante/Finance, validation PM (1er) puis Finance (2e) |
| **Sous-traitants** | Factures ST liées au projet (FK `project` sur STInvoice) |
| **Dépenses** | Rapport de dépenses lié au projet |
| **Congés** | Pas de lien direct (lié à l'employé) |
| **Planification** | `ResourceAllocation` — heures planifiées par tâche, charge équipe, Gantt |
| **Consortium** | FK `consortium` + `is_consortium` (module consortium **reporté**) |
| **Intacct** | Export CSV des données financières projet |

---

## 8. État d'implémentation

### Backend ✅
- Modèle Project complet (localisation, surface, devise, tags, honoraires, public/privé, consortium, services transversaux)
- Modèle Task (WBS Option B) avec contrainte unique `(project, wbs_code)` et support 3 niveaux via `parent` FK
- Dates start/end sur Task (migration 0007)
- FK `task` sur TimeEntry et InvoiceLine
- Template "Architecture standard" (7 phases, 23 tâches incluant Qualité)
- Service `create_project_from_template` avec déploiement phases + tâches
- Transfer PM / Associé en charge (`ProjectTransfer` view)
- Endpoints dashboard + team_stats
- ~240 tests backend (**couverture ~50% — objectif 85%, voir §9**)

### Frontend ✅
- Wizard 5 étapes avec preview template (phases + tâches)
- 12 onglets dans la fiche projet
- Onglet Tâches avec CRUD inline groupé par phase
- Onglet Budget basé sur tâches + section Honoraires
- Onglet Avancement avec % saisissable + code couleur
- Onglet Finance avec KPIs (placeholder pour données réelles)
- Onglets Avenants, ST, Facturation fonctionnels
- Gantt interactif dédié (onglet 4.11)
- Vue simplifiée employé (EmployeeProjectView)

### Implémenté mais non validé / à finaliser (voir §9)
- **Avenants** : workflow et endpoints implémentés, UX complète à valider par Philippe
- **Dashboard temps réel WebSocket** : non implémenté (NFR32)

### Hors scope actuel (reporté)
- **Consortium** : modèle et 6 onglets frontend présents mais **module complet reporté** — ne pas finaliser maintenant
- **Personnel lending + CA repatriation** (Story 3.9) : non implémenté
- **3-level budget view & rebaseline** (Story 12.2) : non implémenté
- **Project reopening + archival** (Story 12.3) : non implémenté
- **Ressources virtuelles (profils)** : partiellement couvert via `ResourceAllocation`, nomenclature "virtuelle" à clarifier

---

## 9. Chantiers à finaliser (module projets)

Philippe souhaite **finaliser le module projets** avant de passer à la suite. Chantiers identifiés par l'audit 2026-04-21, promus **Epic 12 MVP-1** (décision 2026-04-21). Sprint plan : [sprint-module-projets-finalization.md](../implementation-artifacts/sprint-module-projets-finalization.md).

### 9.1 Avenants — validation fonctionnelle → Story 12.1
- Valider le parcours UX complet (création par Assistante/PM/Finance → approbation Associé en charge → impact budget)
- **Avenants visibles dans la planification et le Gantt** avec leurs propres phases/tâches (swimlane dédié)
- **Facturation flexible** : choix entre facture mergée avec le projet principal OU facture dédiée avenant
- Story détaillée : [12-1-amendment-ux-functional-validation.md](../implementation-artifacts/12-1-amendment-ux-functional-validation.md)

### 9.2 Couverture de tests → Story 12.2 ✅ (livrée 2026-04-21)
- Tests backend : ~50% → **95.31%** sur `apps/projects/` (138 tests)
- Matrice permissions (401/403/200/404 cross-tenant) + optimistic lock + audit trail couverts
- **Bugs de dette technique détectés** (hors scope 12.2, à traiter séparément) :
  - N+1 dans `ProjectListSerializer` (get_active_phase / get_budget_hours / get_total_invoiced)
  - `TaskSerializer.validate()` type-coerce manquant pour `start_date` string sur `partial=True`
- Story détaillée : [12-2-projects-app-test-coverage.md](../implementation-artifacts/12-2-projects-app-test-coverage.md)

### 9.3 Finance — brancher les données réelles → Story 12.3
- Remplacer les placeholders par les vrais chiffres (CA facturé, coûts salaires, coûts ST, marge)
- Liens `InvoiceLine → Task` et `TimeEntry → Task` à consommer
- **Cashflow** : factures payées/impayées, aging >60j, cash net
- **Décisions paiement sous-traitants** (Finance uniquement, audit trail)
- **MVP-2** : lien API logiciel de comptabilité (Acomba / QuickBooks / Sage)
- Story détaillée : [12-3-finance-tab-real-data.md](../implementation-artifacts/12-3-finance-tab-real-data.md)

### 9.4 Nettoyage dette WBSElement → Story 12.4
- Retirer le modèle `WBSElement` deprecated
- Retirer l'endpoint `/wbs/` legacy
- Migration de retrait propre (backfill avec reverse symétrique puis `DeleteModel`)
- Vérifier aucune référence côté frontend
- Story détaillée : [12-4-wbselement-deprecation-cleanup.md](../implementation-artifacts/12-4-wbselement-deprecation-cleanup.md)

### 9.5 Dashboard temps réel (NFR32) — **MVP-1 confirmé (2026-04-21)** → Story 12.5
- WebSocket (Django Channels + channels-redis) pour :
  - **Dashboard temps réel** : KPIs, alertes, pipelines poussés sur mutations (facture, time entry, dépense, ST)
  - **Presence indicator** : badge "En cours d'édition par [utilisateur]" sur **Préparation facture** + **Budget projet**
- Heartbeat 30s, timeout 60s (archi actée architecture.md §Real-Time Presence)
- Passage Django WSGI → **ASGI (Uvicorn)** en prod Hostinger, nginx `/ws/` upgrade
- Story détaillée : [12-5-realtime-dashboard-presence-nfr32.md](../implementation-artifacts/12-5-realtime-dashboard-presence-nfr32.md)

---

## 10. Dette technique

### 10.1 WBSElement deprecated
Le modèle `WBSElement` coexiste avec `Task` (qui le remplace). Il doit être retiré :
- **Backend** : supprimer modèle + ViewSet + serializer + migrations (migration de suppression)
- **Frontend** : retirer toute référence à `/wbs/`
- **Tests** : retirer les tests legacy `WBSElement`

**Décision B2 actée** (2026-04-21) → Story [12-4-wbselement-deprecation-cleanup.md](../implementation-artifacts/12-4-wbselement-deprecation-cleanup.md) (ready-for-dev).

### 10.2 Alignement nomenclature
- "Directeur de projet" → **"Associé en charge"** (vérifier qu'il ne reste pas de références dans le code ou l'UI)

---

## 11. Tests

Fichier Excel de tests : `tests_module_projet.xlsx` (45 tests, 12 sections).

**Profils testés :** Assistante, PM, Finance, Employé, Admin, Associé en charge.

**Gap actuel** : couverture backend ~50%, objectif ≥85% (voir §9.2).
