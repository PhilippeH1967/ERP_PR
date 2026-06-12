# domain.md

Terminologie et règles métier ERP. À lire **dès qu'on modifie** :
- Modèles, serializers, vues des apps métier (projects, clients, suppliers, consortiums, billing, expenses, time_entries, leaves, planning)
- Interfaces utilisateur touchant la nomenclature
- Rapports ou documents envoyés à un acteur externe (client, fournisseur, consortium)

## Acteurs du système

| Acteur | App Django | Description |
|---|---|---|
| **Client** | `clients` | Donneur d'ordre, destinataire des livrables et factures |
| **Projet** | `projects` | Mandat réalisé pour un client (avec phases, tâches, équipe) |
| **Employé** | `core` (User) | Utilisateur du cabinet — associé, PM, technicien, paie, finance |
| **Fournisseur** | `suppliers` | Sous-traitant ou prestataire externe |
| **Consortium** | `consortiums` | Groupement temporaire cabinet + partenaires pour un projet commun |
| **Facture** | `billing` | Document de facturation émis au client |
| **Dépense** | `expenses` | Frais projet (déplacement, matériel, sous-traitance) |
| **Feuille de temps** | `time_entries` | Heures saisies par employé sur une tâche |
| **Congé** | `leaves` | Absence planifiée d'un employé |
| **Planification** | `planning` | Allocation temporelle des ressources sur les projets |

## Terminologie

### "Associé en charge"
**Jamais** utiliser "Directeur de projet" dans l'application. Le terme canonique est **"Associé en charge"**.

- Rôle : associé du cabinet responsable de la supervision d'un projet
- UI, emails, rapports, libellés de champs, factures : toujours "Associé en charge"

### PM vs Associé en charge
- **PM (Project Manager)** : gère le projet au quotidien (planning, équipe, livrables). Rôle `PM` ou `PROJECT_DIRECTOR`.
- **Associé en charge** : supervise plusieurs projets. Rôle `PROJECT_DIRECTOR` (associé).

Dans les filtres de dropdowns :
- Sélection d'un PM : rôles `PM` + `PROJECT_DIRECTOR`
- Sélection d'un Associé en charge : rôle `PROJECT_DIRECTOR` uniquement

### "Occupation des ressources"
Le terme canonique côté UI (page `/planning` + menu) est **"Occupation"** (jamais
"Planification" dans les libellés vus par l'utilisateur). Le concept technique
interne — allocation des ressources, `ResourceAllocation`, Gantt — garde son nom ;
c'est uniquement le **libellé d'interface** qui dit "Occupation".

## WBS — Structure projet

Deux niveaux de nomenclature coexistent :

### WBS client (mode par défaut)
Le client fournit **ses propres libellés** de phases et tâches (ex : *"Phase 1 — Étude de faisabilité"*). Choisi à l'étape 1 du wizard de création de projet.

### WBS standard interne
Phases/tâches standards du cabinet, utilisées si le client n'a pas de nomenclature propre.

### Règle d'affichage — les libellés client priment
Dans tous les documents et interfaces **vus par ou destinés au client** :

- **Feuilles de temps** (saisie employés sur un projet client)
- **Factures** émises au client
- **Rapports** de temps envoyés au client (par la compta)
- **Validation** des heures par le PM
- **Vues projet** côté client / portail
- **Bons de commande**, **livrables**, **documents contractuels**

Les libellés standards restent visibles **en interne** pour le suivi et les métriques agrégées (dashboards, reporting cabinet).

**Pourquoi** : les clients sont très exigeants sur le suivi heures/tâches/sous-tâches. Les documents doivent refléter leur nomenclature, pas la nôtre.

## Hiérarchie projet

- **Projet** → **Phase** → **Tâche** → **Sous-tâche**
- Numérotation WBS de la tâche : `{code_phase}.{séquence}` (ex. `1.1`), sous-tâche : `{wbs_parent}.{séquence}` (ex. `1.1.1`)

### Phases = regroupements standard (paramétrage)
- Les phases sont un **jeu standard du cabinet**, défini dans le **paramétrage** (`StandardPhase`, écran *Administration › Phases standard*, **admin uniquement**).
- À la création d'un projet, **toutes les phases standard** sont instanciées (vides). Les **PM ne créent/modifient/suppriment pas** de phase sur un projet (réservé ADMIN — `PhaseViewSet` en écriture admin-only ; fallback template si aucun jeu standard paramétré).
- Une phase est un **pur regroupement** : elle **ne porte ni budget, ni dates, ni mode de facturation**. Elle **agrège** ses tâches.

### Tâches / sous-tâches = unité opérationnelle
- La **tâche** (ou sous-tâche) porte : **budget** (heures et $), **dates**, **planification** (allocations), **mode de facturation**, **saisie de temps**.
- Notion de **« saisissable » / feuille** : un nœud **sans enfant**. Une tâche **avec** sous-tâches devient un **agrégat en lecture seule** (comme la phase) ; seules ses sous-tâches sont saisissables. Le budget/heures/planif **vivent uniquement sur les feuilles** (pas de double-comptage).
- Une tâche peut être **déplacée** vers une autre phase (ré-imputation) — recalcul automatique des agrégats.

### Catalogue de tâches/sous-tâches standard (paramétrage)
- Un **catalogue** de tâches et sous-tâches standard par phase est défini dans le **paramétrage** (`StandardTask`, écran *Administration › Tâches standard*, **admin uniquement** ; `parent` self-FK pour les sous-tâches).
- Au démarrage d'un projet, sur une **phase sans tâche** (ou pour compléter une phase existante), l'utilisateur **ajoute** des tâches/sous-tâches depuis ce catalogue (endpoint `task_suggestions`). Les tâches **déjà présentes sont exclues** (déduplication par nom) — le picker ne s'applique donc pas en doublon.
- Le catalogue **propose** ; les tâches instanciées restent éditables/supprimables sur le projet (budget, dates… vivent sur la tâche, pas sur le standard).

### Services transversaux = phases SUPPORT imputables
- Les **services transversaux** (BIM, Développement durable, Paysage, Génie civil, Patrimoine, Design intérieur, Éclairage…) sélectionnés au wizard deviennent chacun une **phase de type SUPPORT** (`Phase.PhaseType.SUPPORT`), nommée d'après le service, contenant **une tâche feuille imputable** du même nom.
- Conséquence : on **impute du temps** sur un service transversal (via sa tâche feuille), au même titre qu'une tâche de réalisation. Comme pour toute phase, **budget / facturation / saisie vivent sur la tâche**, jamais sur la phase support elle-même.
- Le modèle `SupportService` (ancienne structure **parallèle non imputable**) est **déprécié** : les données existantes ont été converties en phases SUPPORT + tâches (migration `projects 0016`). Ne plus créer de `SupportService`.

### Agrégation (lecture seule, calculée)
- **Phase** : `tasks_budgeted_hours/cost`, `planned_hours`, `actual_hours`, `tasks_start_date/end_date` = Σ / min-max des **tâches saisissables** de la phase.
- **Tâche-mère** : `effective_budgeted_*`, `planned_hours`, `actual_hours` = Σ de ses **sous-tâches**.
- Les **phases sans tâche** sont **masquées** dans les écrans opérationnels (Tâches, Gantt, Budget) ; visibles en structure, marquées « Sans tâche ».

> Le modèle déprécié `WBSElement` a été **supprimé** (remplacé par `Task`).

## Avenants

- Chaque avenant est un **mini-contrat** rattaché au projet principal
- Numéro auto : `{code_projet}-AV-{séquentiel}` + numéro externe libre
- Un avenant **ajoute/modifie des tâches** sur les **phases standard existantes** (il ne crée pas de phase). Les tâches d'avenant portent un `amendment` et un badge `AV-n`.
- **Pas d'affectation de ressources ni de planification** dans le slide-over d'avenant — ça se fait dans le **Gantt**, au niveau des tâches.

## Facturation

### Modes disponibles
- **Forfait** : montant fixe
- **Temps & matériel (T&M)** : taux horaires × heures
- **Cost-plus** : coûts réels + marge

Le **mode de facturation se définit au niveau de la tâche** (feuille), pas de la phase.

### Règles
- Numéro de facture auto-incrémenté, unique, non modifiable après émission
- Une facture émise ne peut plus être modifiée — créer un avoir ou une facture rectificative
- Les libellés de lignes de facture reprennent le **WBS client**
- Taxes : architecture fiscale complète prévue MVP-2 (entités juridiques, TPS/TVQ, CTI/RTI)

### Adresse de facturation par projet
- Chaque projet peut désigner **son** adresse de facturation parmi les **adresses de son client** (`Project.billing_address`) — deux projets d'un même client peuvent facturer à deux adresses. **Sans désignation**, l'adresse de facturation par défaut du client s'applique.
- Une adresse d'un **autre client** est refusée ; **changer le client** d'un projet purge la désignation devenue invalide.
- Les adresses s'**ajoutent/éditent** depuis le projet (elles vivent dans la fiche client, partagées) mais la **suppression** se fait uniquement dans la fiche client. **Anti-doublon** : même ligne 1 + ville + code postal (insensible casse/espaces) refusée pour un même client.

### Coût de construction (projets externes)
- Champ **`construction_cost`** : montant **informatif** du coût de construction, saisi sur la **Vue d'ensemble** d'un projet. Sert au calcul/contexte des honoraires.
- **Projets externes uniquement** : masqué pour les projets internes (`is_internal`).

## Équipes (paramétrage)

- Une **équipe** (`Team`) est un **groupe d'employés réutilisable** défini en paramétrage (*Administration › Équipes*).
- **Création / modification** réservées à **Finance, Paie et Admin** (`IsFinancePaieOrAdmin`). Lecture ouverte aux authentifiés.
- On peut **affecter une équipe en entier** sur un projet (action `assign_team` → ajoute tous ses membres aux `team_members` du projet). L'affectation se fait **au niveau projet** (pas tâche).
- Les **profils virtuels** (ressources non nominatives) s'ajoutent à l'équipe d'un projet **sans passer par un avenant**. Le dropdown de membres est **recherchable par nom**.

## Projet interne

- Un projet **interne** (`is_internal`) — congés, formation, administration cabinet — est **masqué pour tous sauf ADMIN** (queryset `ProjectViewSet` filtré).
- Il porte les **tâches obligatoires** de saisie (Congés, Formation, Maladie) affichées d'office dans les feuilles de temps. Recréables via la commande de seed dédiée (`seed_internal_mandatory_tasks`).

## Fournisseurs et sous-traitants

- Un **fournisseur** peut être lié à une ou plusieurs **dépenses** projet
- Un **sous-traitant** est un fournisseur avec un contrat de prestation (souvent lié à une phase)
- Les factures fournisseur transitent par le workflow d'approbation (PM → finance → paiement)

## Consortiums

- Un consortium regroupe le cabinet + partenaires externes sur un projet commun
- Répartition des revenus et coûts selon la quote-part définie au contrat de consortium
- Les heures et dépenses sont attribuables au cabinet ou aux partenaires selon la règle du consortium

## Contraintes métier clés

### Allocation ressources / planification
- La planification se fait dans l'onglet **Gantt**, au niveau **tâche / sous-tâche** (jamais la phase ni une tâche-mère, qui sont des agrégats non cliquables).
- Contrôle **non bloquant** : si les heures planifiées dépassent le budget de la tâche → signalé en **rouge** (on ne bloque pas).
- Une barre Gantt ne s'affiche que si la tâche a **ses propres dates** (pas de fallback sur la phase).

### Dates
- `date_fin >= date_debut` à la création **ET** modification (projet, tâche, sous-tâche, avenant, congé)
- Les **dates de phase sont dérivées** (min/max des tâches), en lecture seule — on ne les saisit pas.
- Validation côté backend (serializer) **ET** frontend (form)

### Feuilles de temps
- **Blocages de saisie** : une tâche **fermée** (`Task.is_active=False`) refuse la saisie de **tout le monde** ; un blocage ciblé (`TimeEntryBlock`) la refuse pour **une personne** sur une tâche, une phase ou **tout le projet**. Les deux sont réversibles et contrôlés à l'API (pas seulement masqués).
- Heures **validées** ne peuvent plus être modifiées par l'employé
- Un employé ne peut saisir des heures projet sur une journée validée en congé
- Les heures doivent être rattachées à une tâche existante du projet (pas de saisie libre)

### Congés
- Chevauchement interdit entre deux demandes de congés du même employé
- Validation par le responsable RH avant impact sur la planification

## Cas à remonter immédiatement à l'utilisateur

- Libellé "Directeur de projet" trouvé dans le code ou l'UI
- Rapport ou facture client affichant les libellés standards au lieu des libellés client
- Facture émise modifiable après émission
- Saisie de temps possible sur une journée validée en congé
- **Budget, dates, mode de facturation ou planification saisis au niveau d'une phase** (doivent vivre sur la tâche/sous-tâche)
- **Phase créée/modifiée/supprimée par un non-admin** sur un projet (réservé ADMIN — paramétrage)
- **Tâche standard créée/modifiée par un non-admin** (catalogue `StandardTask` réservé ADMIN)
- **Équipe créée/modifiée par un rôle hors Finance/Paie/Admin**
- **Projet interne visible par un non-admin** (doit être masqué)
- **Coût de construction affiché/saisi sur un projet interne** (réservé aux projets externes)
- Libellé "Planification" dans l'UI là où "Occupation" est attendu
- **Budget de tâche éditable ailleurs** que sur la tâche (Échéancier / fiche tâche) — Finances › Budget doit rester une synthèse en lecture seule
- **Projet référençant l'adresse d'un autre client** (`billing_address`) ou **suppression d'adresse possible depuis un projet**
- **Service transversal non imputable** (stocké en `SupportService` au lieu d'une phase SUPPORT + tâche feuille)
- **Double-comptage** d'agrégat (tâche-mère + sous-tâches comptées ensemble)
- Réapparition du modèle `WBSElement` (supprimé)
