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

- **Projet** → **Phase** → **Tâche** (WBS Option B, validée)
- Pas de sous-tâches dans la structure actuelle (à ré-évaluer si besoin client)
- Numérotation : `{code_projet}-{séquence_phase}-{séquence_tâche}`

## Avenants

- Chaque avenant est un **mini-contrat** rattaché au projet principal
- Numéro auto : `{code_projet}-AV-{séquentiel}` + numéro externe libre
- Peut avoir ses propres phases, ressources, mode de facturation (cible MVP-1.5)

## Facturation

### Modes disponibles
- **Forfait** : montant fixe
- **Temps & matériel (T&M)** : taux horaires × heures
- **Cost-plus** : coûts réels + marge

Chaque phase d'un avenant peut utiliser un mode différent (MVP-1.5).

### Règles
- Numéro de facture auto-incrémenté, unique, non modifiable après émission
- Une facture émise ne peut plus être modifiée — créer un avoir ou une facture rectificative
- Les libellés de lignes de facture reprennent le **WBS client**
- Taxes : architecture fiscale complète prévue MVP-2 (entités juridiques, TPS/TVQ, CTI/RTI)

## Fournisseurs et sous-traitants

- Un **fournisseur** peut être lié à une ou plusieurs **dépenses** projet
- Un **sous-traitant** est un fournisseur avec un contrat de prestation (souvent lié à une phase)
- Les factures fournisseur transitent par le workflow d'approbation (PM → finance → paiement)

## Consortiums

- Un consortium regroupe le cabinet + partenaires externes sur un projet commun
- Répartition des revenus et coûts selon la quote-part définie au contrat de consortium
- Les heures et dépenses sont attribuables au cabinet ou aux partenaires selon la règle du consortium

## Contraintes métier clés

### Allocation ressources
- **% affectation** : max 100% par phase, empêcher doublon personne/phase
- Auto-calcul du % restant lors de l'affectation

### Dates
- `date_fin >= date_debut` à la création **ET** modification (projet, phase, tâche, avenant, congé)
- Validation côté backend (serializer) **ET** frontend (form)

### Feuilles de temps
- Heures **validées** ne peuvent plus être modifiées par l'employé
- Un employé ne peut saisir des heures projet sur une journée validée en congé
- Les heures doivent être rattachées à une tâche existante du projet (pas de saisie libre)

### Congés
- Chevauchement interdit entre deux demandes de congés du même employé
- Validation par le responsable RH avant impact sur la planification

## Cas à remonter immédiatement à l'utilisateur

- Libellé "Directeur de projet" trouvé dans le code ou l'UI
- Rapport ou facture client affichant les libellés standards au lieu des libellés client
- % affectation permettant > 100% par phase sans garde-fou
- Facture émise modifiable après émission
- Saisie de temps possible sur une journée validée en congé
