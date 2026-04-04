# Module Projets — Spécification complète

**Version:** 1.1.012
**Date:** 2026-04-04
**Statut:** Bloc 1 développé — en validation

---

## 1. Vue d'ensemble

Le module Projets est le **cœur de l'ERP**. Tous les autres modules (feuilles de temps, facturation, dépenses, ST, planification) sont liés aux projets. Il permet de créer, configurer et piloter l'ensemble des projets d'architecture depuis une interface centralisée.

### 1.1 Objectifs

- Créer des projets depuis des **templates pré-configurés** (phases + tâches déployées automatiquement)
- Gérer la **structure WBS** (Phase → Tâche → Sous-tâche) avec codes WBS (3.1, 3.2)
- Suivre le **budget par tâche** et les honoraires
- Suivre l'**avancement** (% par tâche, planifié vs réel)
- **Facturer par tâche** (pas par phase)
- Saisir les **feuilles de temps par tâche**
- Piloter la **marge** (CA - Coûts)

### 1.2 Acteurs et rôles

| Rôle | Actions |
|------|---------|
| **Assistante (DEPT_ASSISTANT)** | Crée les projets, assigne PM/personnel, planifie les heures |
| **Chef de projet (PM)** | Consulte, valide les factures, saisit l'avancement, planifie les heures |
| **Finance (FINANCE)** | Modifie les budgets, prépare les factures, suit les honoraires |
| **Directeur (PROJECT_DIRECTOR)** | Valide les factures (2e niveau), approuve les avenants |
| **Employé (EMPLOYEE)** | Consulte les projets assignés, saisit les feuilles de temps |
| **Admin (ADMIN)** | Accès complet |

---

## 2. Architecture des données

### 2.1 Modèle hiérarchique (WBS Option B)

```
Projet (PR-2026-001)
├── Phase 1: Concept (conteneur)
│   ├── Tâche 1.1: Analyse conditions existantes (opérationnel)
│   ├── Tâche 1.2: Esquisse et options
│   └── Tâche 1.3: Estimation classe D
├── Phase 2: Préliminaire
│   ├── Tâche 2.1: Plans préliminaires
│   └── Tâche 2.2: Devis préliminaires
├── Phase 3: Définitif
│   ├── Tâche 3.1: Plans architecturaux détaillés
│   ├── Tâche 3.2: Plans structure et fondations
│   └── Tâche 3.3: Plans et devis MEP
├── Phase 4: Appel d'offres
└── Phase 5: Surveillance (HORAIRE)
```

**Principes clés :**
- La **Phase** est un conteneur de regroupement
- La **Tâche** est l'unité opérationnelle (facturation, feuilles de temps, budget)
- Le **code WBS** (3.1, 3.2) identifie chaque tâche de manière unique dans le projet
- Les feuilles de temps sont saisies **par tâche**
- La facturation se fait **par tâche**

### 2.2 Modèle Project

| Champ | Type | Description |
|-------|------|-------------|
| `code` | CharField | Code projet unique (PR-2026-001) |
| `name` | CharField | Nom du projet |
| `client` | FK Client | Client (nullable pour projets internes) |
| `template` | FK ProjectTemplate | Template utilisé à la création |
| `contract_type` | CharField | FORFAITAIRE / HORAIRE |
| `status` | CharField | ACTIVE / ON_HOLD / COMPLETED / CANCELLED |
| `is_internal` | Boolean | Projet interne (sans client) |
| `business_unit` | CharField | Unité d'affaires |
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
| `invoice_approver` | FK User | Approbateur factures |
| `bu_director` | FK User | Directeur d'unité |

### 2.3 Modèle Phase

| Champ | Type | Description |
|-------|------|-------------|
| `code` | CharField | Code phase (1, 2, 3, GP) |
| `name` | CharField | Nom (Concept, Préliminaire, Définitif...) |
| `client_facing_label` | CharField | Libellé client |
| `phase_type` | CharField | REALIZATION / SUPPORT |
| `billing_mode` | CharField | FORFAIT / HORAIRE / POURCENTAGE |
| `order` | Integer | Ordre d'affichage |
| `is_mandatory` | Boolean | Phase obligatoire (non supprimable) |
| `is_locked` | Boolean | Phase verrouillée |
| `budgeted_hours` | DecimalField | Heures budgétées |
| `budgeted_cost` | DecimalField | Budget |

### 2.4 Modèle Task (nouveau — remplace WBSElement)

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
| `budgeted_hours` | DecimalField | Heures budgétées |
| `budgeted_cost` | DecimalField | Budget |
| `hourly_rate` | DecimalField | Taux horaire (pour HORAIRE) |
| `is_billable` | Boolean | Facturable |
| `is_active` | Boolean | Active |
| `progress_pct` | DecimalField | % avancement (0-100) |

**Contrainte unique :** `(project, wbs_code)` — un code WBS ne peut apparaître qu'une fois par projet.

---

## 3. Templates de projet

### 3.1 Template "Architecture standard" (ARCH-STD)

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

GP: Gestion de projet (obligatoire, FORFAIT)
├── GP.1 Coordination équipe (non facturable)
├── GP.2 Réunions client (facturable)
└── GP.3 Administration projet (non facturable)
```

**Total : 6 phases, 20 tâches**

### 3.2 Déploiement du template

Quand l'assistante crée un projet et choisit un template :
1. Les phases se créent automatiquement
2. Les tâches se créent sous chaque phase avec leur code WBS
3. L'assistante peut ajouter/supprimer des phases et tâches
4. Les phases obligatoires ne peuvent pas être supprimées

---

## 4. Onglets du projet (10 onglets)

### 4.1 Vue d'ensemble
- Informations projet (code, nom, client, dates, statut)
- KPIs : utilisation %, heures consommées, heures budgétées
- Mode lecture / édition

### 4.2 Phases
- CRUD phases avec édition inline
- Assignation d'employés par phase (bouton "Affecter")
- Badge obligatoire / optionnel

### 4.3 Tâches (nouveau — remplace WBS)
- Tâches **groupées par phase** avec en-têtes dépliables
- Colonnes : WBS Code | Nom | Mode | Budget ($) | Heures | Facturable | Actions
- Budget et heures éditables inline (ADMIN/FINANCE uniquement)
- Ajout/suppression de tâches par phase
- Badge TASK / SUBTASK

### 4.4 Équipe
- Assignation d'employés aux phases/tâches
- Nom, phase, %, période

### 4.5 Avenants
- CRUD avenants avec workflow (Brouillon → Soumis → Approuvé)
- Impact budget

### 4.6 Budget
- **Section Honoraires** : montant total HT, méthode de calcul, taux
- **KPI cards** : Budget total, Facturé, % consommé, Solde
- **Table budget par tâche** groupée par phase : WBS, Tâche, Mode, Budget, Heures, Facturé, Solde
- Budget éditable inline (ADMIN/FINANCE)
- Bouton "Créer une facture" (Finance)

### 4.7 Avancement (nouveau)
- Tâches groupées par phase
- **% avancement saisissable** par tâche (0-100, sauvegarde au blur)
- Colonnes : WBS, Tâche, Budget, Heures planifiées, Heures réelles, % Avancement, Écart
- Code couleur écart : vert (<10%), ambre (10-25%), rouge (>25%)
- Totaux par phase

### 4.8 Finance (nouveau)
- **5 KPI cards** : CA facturé, Coûts salaires, Coûts ST, Marge, Marge %
- Table résumé par année (placeholder — sera alimenté par les données réelles)

### 4.9 Sous-traitants
- Liste des factures ST liées au projet
- Colonnes : Fournisseur, No facture, Date, Montant, Refacturable, Statut
- Totaux

### 4.10 Facturation
- Liste des factures du projet
- Colonnes : No facture, Statut, Montant, Dates
- Bouton "Créer une facture"
- Lien vers la fiche facture

---

## 5. Workflows

### 5.1 Création de projet
```
1. Assistante → Nouveau projet
2. Choisit template → Preview phases + tâches
3. Remplit : code, nom, client, adresse, surface
4. Phases + tâches se déploient automatiquement
5. Assigne PM + Associé en charge
6. Projet statut = ACTIF
```

### 5.2 Vie du projet
```
7. Assistante assigne le personnel (à la demande du PM)
8. Assistante/PM planifie les heures par tâche
9. PM consulte budget, heures, avancement
10. PM saisit % avancement par tâche
11. Avenants : création → approbation Directeur → impact budget
12. ST : mandats liés aux tâches
```

### 5.3 Facturation depuis le projet
```
13. Finance → onglet Facturation → "Créer facture"
14. Lignes pré-remplies par TÂCHE (budget, facturé à ce jour)
15. Finance saisit "à facturer ce mois"
16. PM valide la facture
17. Finance envoie → numéro définitif FAC-YYYY-XXXXX
```

### 5.4 Clôture
```
18. PM → statut TERMINÉ
19. Vérifications : tout facturé ? heures verrouillées ? ST payés ?
```

---

## 6. API Endpoints

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET/POST | `/projects/` | Liste / Créer projet |
| GET/PATCH/DELETE | `/projects/{id}/` | Détail / Modifier / Supprimer |
| POST | `/projects/{id}/create_from_template/` | Créer depuis template |
| GET | `/projects/{id}/dashboard/` | KPIs projet |
| GET/POST | `/projects/{id}/phases/` | CRUD phases |
| GET/POST | `/projects/{id}/tasks/` | CRUD tâches |
| PATCH/DELETE | `/projects/{id}/tasks/{task_id}/` | Modifier / Supprimer tâche |
| GET/POST | `/projects/{id}/wbs/` | CRUD WBS (legacy) |
| GET/POST | `/projects/{id}/assignments/` | CRUD affectations |
| GET/POST | `/projects/{id}/amendments/` | CRUD avenants |
| GET/POST | `/project_templates/` | CRUD templates |
| POST | `/invoices/create_from_project/` | Créer facture depuis projet |

---

## 7. Lien avec les autres modules

| Module | Lien avec Projet |
|--------|-----------------|
| **Feuilles de temps** | Saisie par tâche (FK task sur TimeEntry) |
| **Facturation** | Lignes par tâche (FK task sur InvoiceLine) |
| **Sous-traitants** | Factures ST liées au projet (FK project sur STInvoice) |
| **Dépenses** | Rapport de dépenses lié au projet |
| **Congés** | Pas de lien direct (lié à l'employé) |
| **Planification** | Heures planifiées par tâche (Bloc 2) |
| **Intacct** | Export CSV des données financières projet |

---

## 8. État d'implémentation

### Backend ✅
- Modèle Project avec tous les champs (localisation, surface, devise, tags, honoraires)
- Modèle Task (WBS Option B) avec contrainte unique (project, wbs_code)
- FK Task sur TimeEntry et InvoiceLine
- Template "Architecture standard" (6 phases, 20 tâches)
- Service create_from_template avec déploiement phases + tâches
- 240 tests backend passent

### Frontend ✅
- 10 onglets dans la fiche projet
- Wizard avec preview template (phases + tâches)
- Onglet Tâches avec CRUD inline groupé par phase
- Onglet Budget basé sur tâches + section Honoraires
- Onglet Avancement avec % saisissable + code couleur
- Onglet Finance avec KPIs placeholder
- Onglets ST et Facturation fonctionnels

### À compléter (Bloc 2+)
- Ressources virtuelles (profils) → Module Planification
- Heures réelles dans Avancement (lien TimeEntry → Task)
- Montant facturé réel dans Budget (lien InvoiceLine → Task)
- Finance : CA, Coûts, Marge calculés depuis les données réelles
- Gantt simplifié (MVP-2)

---

## 9. Tests

Fichier Excel de tests : `tests_module_projet.xlsx` (45 tests, 12 sections)

**Profils testés :** Assistante, PM, Finance, Employé, Admin, Directeur
