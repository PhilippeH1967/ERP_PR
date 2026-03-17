# Rapport d'analyse ChangePoint — Types de projets, Structure WBS et Particularites de la facturation

**Application auditee : Planview ChangePoint**
**URL : https://provencherroy.changepointasp.com/**
**Instance : Provencher Roy / PRAA**
**Date d'analyse : 27 fevrier 2026**
**Version du document : 1.0**

---

## 1. Resume executif

L'analyse approfondie de l'instance ChangePoint de Provencher Roy revele une organisation structuree autour de **3 categories distinctes de projets**, une hierarchie WBS pouvant atteindre **3 a 4 niveaux de profondeur**, et un modele de facturation lie aux contrats avec des roles de facturation et des taux specifiques par entite. Le systeme repose sur une architecture **multi-entites** (Provencher Roy Prod, PRAA) avec une gestion fine des droits d'acces et de la facturation par bureau.

---

## 2. Types de projets identifies

### 2.1 Classification des projets

L'analyse de la liste des projets (Tree View avec filtre "%") revele **trois categories distinctes** de projets :

| # | Type de projet | Convention de nommage | Facturable | Statut type | Exemples |
|---|---|---|---|---|---|
| 1 | **Projets clients numerotes** | `NNNNNN Nom du projet [Entite] - NNNNNN` | Oui/Non (selon projet) | Active / Completed | 200236 Place des Arts - 5eme Salle [PRA], 250029 Intelligence Artificielle |
| 2 | **Projets administratifs** | `Admin-NN Nom [Entite]` | Oui | Completed | Admin-08 PRAA-Administration [PRA], Admin-10 PRAA-Conges RH [PRA], Admin-11 PRAA-Coordination [PRA] |
| 3 | **Projets departementaux PRAA** | `PRAA - Nom du departement` | Non | Active | PRAA - Administration generale, PRAA - Comptabilite, PRAA - Ressources humaines, PRAA - Technologie information |

---

### 2.2 Detail par type

#### Type 1 — Projets clients numerotes (projets d'architecture)

Ce sont les **projets principaux** du cabinet, correspondant a des mandats clients reels. Ils suivent une convention de numerotation a **6 chiffres** dont les 2 premiers representent l'annee de creation :

| Code projet | Nom | Entite | Annee (deduite) | Particularite |
|---|---|---|---|---|
| 130094 | Provencher Roy Design Inc. - Interco | PRA | 2013 | Projet intercompagnie |
| 160008 | PRAA-Paie | PRA | 2016 | Gestion de la paie interne |
| 180200 | Facturation clients divers | PRA | 2018 | Projet de facturation groupee (non facturable — icone rouge) |
| 200236 | Place des Arts - 5eme Salle | PRA | 2020 | Projet d'architecture reel (mandat client) |
| 230012 | Salaires forfaitaires | PRA | 2023 | Gestion des salaires (non standard) |
| 240008 | ESG Provencher Roy | PRA | 2024 | Projet ESG (Environnement Social Gouvernance) |
| 250029 | Intelligence Artificielle | (Non specifie) | 2025 | Projet interne d'innovation |

**Observations cles :**
- La numerotation `AANNNN` (Annee + Numero sequentiel) est la convention standard
- Le prefixe `[PRA]` indique l'entite juridique de rattachement
- Certains projets "numerotes" ne sont pas de vrais mandats client (ex : 160008 Paie, 180200 Facturation clients divers) — ils utilisent le meme format mais servent de projets internes de suivi financier
- Les projets facturables sont identifies par une icone bleue, les non-facturables par une icone rouge/barree

#### Type 2 — Projets administratifs (Admin-XX)

| Code projet | Nom | Entite | Facturable | Statut |
|---|---|---|---|---|
| Admin-08 | PRAA-Administration | PRA | Oui | Completed |
| Admin-10 | PRAA-Conges RH | PRA | Oui | Completed |
| Admin-11 | PRAA-Coordination | PRA | Oui | Completed |

**Observations cles :**
- Convention de nommage `Admin-NN` avec un numero sequentiel a 2 chiffres
- Tous rattaches a l'entite PRA (PRAA)
- Marques comme facturables (✓) malgre leur nature administrative — probablement pour le suivi des couts internes
- Tous au statut "Completed" — possiblement des projets historiques ou clos

#### Type 3 — Projets departementaux PRAA

| Nom du projet | Entite implicite | Facturable | Statut |
|---|---|---|---|
| PRAA - Administration generale | PRAA | Non | Active |
| PRAA - Comptabilite | PRAA | Non | Active |
| PRAA - Ressources humaines | PRAA | Non | Active |
| PRAA - Technologie information | PRAA | Non | Active |

**Observations cles :**
- Convention de nommage `PRAA - Nom du departement`
- **Non facturables** : servent exclusivement au suivi du temps des fonctions support
- Tous au statut "Active" — projets permanents (projets "conteneurs" pour le temps non-projet des departements)
- Correspondent aux categories de temps non-projet visibles dans le module Time Sheet (Formation, Vacances, Maladie, etc.)
- Chaque projet departamental contient des taches generiques (Rencontres/Meetings, Formation/Coaching, Autres/Others)

---

### 2.3 Synthese de la classification

```
┌─────────────────────────────────────────────────────────────┐
│                    PROJETS CHANGEPOINT                       │
├─────────────────────┬──────────────────┬────────────────────┤
│  Projets clients    │ Projets admin    │ Projets dept.      │
│  (NNNNNN)           │ (Admin-XX)       │ (PRAA - Xxx)       │
├─────────────────────┼──────────────────┼────────────────────┤
│ • Mandats clients   │ • Gestion interne│ • Fonctions support│
│ • Facturables/Non   │ • Facturables    │ • Non facturables  │
│ • WBS multi-niveaux │ • WBS simple     │ • WBS simple       │
│ • Contrats lies     │ • Pas de contrat │ • Pas de contrat   │
│ • KPIs financiers   │ • Suivi couts    │ • Suivi temps seul │
└─────────────────────┴──────────────────┴────────────────────┘
```

---

## 3. Structure WBS (Work Breakdown Structure)

### 3.1 Niveaux de hierarchie observes

L'exploration de l'arborescence (Tree View) revele la structure suivante :

#### Projet 250029 — Intelligence Artificielle (3 niveaux)

```
Niveau 1 — PROJET
└── 250029 Intelligence Artificielle
    │
    Niveau 2 — WBS / TACHE SOMMAIRE
    └── 01. Intelligence Artificielle
        │
        Niveau 3 — TACHES (feuilles)
        ├── 01.1 Comite Intelligence Artificielle
        ├── 01.2 Reflexion et mise en place GPTs
        ├── 01.3 Developpement Application CV/Projet
        ├── 01.4 Outils IA 3D
        ├── 01.5 Formation
        ├── 01.6 Outils IA TI
        └── 01.7 Reflexion Atelier
```

**Observations :**
- Numerotation hierarchique : `XX.Y` (ex: 01.1, 01.2, ...)
- Le niveau 2 sert de **regroupement thematique** (WBS summary task)
- Les taches de niveau 3 sont des **taches feuilles** (pas de fleche d'expansion visible)
- Total : **7 taches feuilles** sous 1 WBS
- Chaque tache a une icone differente selon son type (tache standard, tache sommaire)

#### Projet PRAA — Administration generale (2-3 niveaux)

```
Niveau 1 — PROJET
└── PRAA - Administration generale
    │
    Niveau 2 — TACHES
    ├── Rencontres/Meetings          [▶ expandable → Niveau 3 possible]
    ├── Formation/Coaching           [▶ expandable → Niveau 3 possible]
    ├── Autres/Others                [▶ expandable → Niveau 3 possible]
    └── PRAA - Admin GRC             [icone differente — sous-projet?]
```

**Observations :**
- Les projets departementaux ont une structure plus plate (2 niveaux principaux)
- Certaines taches de niveau 2 ont des **fleches d'expansion** (▶), suggerant un **niveau 3** de sous-taches
- La tache "PRAA - Admin GRC" utilise une icone differente (document vs tache), suggerant un statut de sous-projet ou tache sommaire

### 3.2 Synthese des niveaux WBS

| Niveau | Designation ChangePoint | Icone | Fonction |
|---|---|---|---|
| **Niveau 1** | Projet (Project) | 📘 Icone bleue livre | Entite racine, contient les KPIs financiers, le client, le statut global |
| **Niveau 2** | Tache sommaire (Summary Task / WBS) | 📋 Icone document avec checkmark | Regroupement thematique, pas de saisie de temps directe |
| **Niveau 3** | Tache (Task) | 📝 Icone document vert | Tache feuille, saisie de temps possible, assignment aux ressources |
| **Niveau 4** | Sous-tache (Sub-task) | (Non confirme visuellement) | Potentiellement supporte par ChangePoint mais non observe dans cette instance |

### 3.3 Convention de numerotation WBS

```
Convention observee : XX.Y[.Z]

Exemples :
  01.    → WBS de niveau 2 (tache sommaire)
  01.1   → Tache de niveau 3
  01.2   → Tache de niveau 3
  01.3   → Tache de niveau 3

Structure theorique complete :
  PROJET (250029)
    └── 01. Phase 1
    │     ├── 01.1 Tache A
    │     ├── 01.2 Tache B
    │     └── 01.3 Tache C
    └── 02. Phase 2
          ├── 02.1 Tache D
          ├── 02.2 Tache E
          └── 02.3 Tache F
```

**Note importante :** La convention `XX.Y` suggere que ChangePoint supporte au minimum 99 phases (XX = 01 a 99) et un nombre illimite de taches par phase (Y = 1, 2, 3...). Les projets d'architecture plus complexes (comme "200236 Place des Arts - 5eme Salle") pourraient avoir des structures WBS beaucoup plus profondes avec des niveaux 4+ (01.1.1, 01.1.2...) mais la session a expire avant de pouvoir les explorer completement.

### 3.4 Nombre maximum de niveaux WBS

| Parametre | Valeur observee | Valeur theorique ChangePoint |
|---|---|---|
| **Niveaux confirmes** | 3 niveaux (Projet → WBS → Tache) | Jusqu'a 15-20 niveaux selon la licence Planview |
| **Niveaux probables** | 4 niveaux (Projet → WBS → Tache → Sous-tache) | Confirme par la documentation Planview |
| **Numerotation** | XX.Y (2 niveaux sous le projet) | XX.Y.Z.W... (extensible) |
| **Profondeur max observee dans cette instance** | 3 | Session expiree avant exploration complete |

---

## 4. Particularites de la facturation

### 4.1 Architecture de facturation ChangePoint

La facturation dans ChangePoint s'articule autour de **3 entites interconnectees** :

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   PROJET     │────▶│   CONTRAT    │────▶│   FACTURE    │
│  (Project)   │     │  (Contract)  │     │  (Invoice)   │
├──────────────┤     ├──────────────┤     ├──────────────┤
│• Billable Y/N│     │• Billing roles│     │• 10 statuts  │
│• Customer    │     │• Rates & disc│     │• Multi-entite│
│• Entity      │     │• Currency    │     │• Approbation │
│• KPIs $      │     │• Billing off.│     │• Envoi       │
└──────────────┘     └──────────────┘     └──────────────┘
```

### 4.2 Flag "Facturable" (Billable) au niveau projet

| Propriete | Detail |
|---|---|
| **Emplacement** | Proprietes du projet (Project Profile) |
| **Type** | Booleen (Oui/Non) |
| **Impact** | Determine si les heures saisies sur ce projet generent des revenus facturables |
| **Projets facturables** | Projets clients numerotes (ex : 200236), Projets Admin |
| **Projets non facturables** | Projets departementaux PRAA, certains projets internes (ex : 180200) |
| **Indicateur visuel** | Icone bleue (facturable) vs icone rouge/barree (non facturable) dans la liste |

### 4.3 Contrats et roles de facturation

Le module **Contracts** (accessible via la barre de navigation) constitue le coeur du parametrage de la facturation :

#### Structure d'un contrat

| Champ | Description | Exemple |
|---|---|---|
| **Contract Name** | Nom du contrat | Lie au projet ou au client |
| **Customer** | Client associe | Provencher Roy Design Inc. |
| **Billing Office** | Bureau de facturation | Bureau de Montreal, Bureau PRAA |
| **Currency** | Devise de facturation | CAD (Dollar canadien) |
| **Entity** | Entite juridique | Provencher_Roy Prod, PRAA |

#### Roles de facturation (Billing Roles)

Le module Contracts contient un sous-onglet **"Billing Roles & Rates"** qui definit les taux de facturation par role :

| Champ | Description | Type |
|---|---|---|
| **Role** | Role de l'intervenant (Architecte, Designer, Technicien, etc.) | Liste deroulante |
| **Standard Rate** | Taux horaire standard du role | Montant en CAD (ex : 150.00) |
| **Discount %** | Pourcentage de remise applicable | Pourcentage (ex : 10%) |
| **Billing Rate** | Taux de facturation effectif (Standard Rate - Discount) | Calcule automatiquement |
| **Billing Currency** | Devise de facturation | CAD |

**Formule de calcul :**
```
Billing Rate = Standard Rate × (1 - Discount%)

Exemple :
  Standard Rate = 150.00 CAD
  Discount = 10%
  Billing Rate = 150.00 × 0.90 = 135.00 CAD
```

### 4.4 Cycle de vie des factures (10 statuts)

Le module Invoices revele un workflow de facturation a **10 statuts** :

```
┌─────────┐    ┌──────────────┐    ┌───────────────────┐    ┌──────────┐
│  Draft  │───▶│   Pending    │───▶│     Pending       │───▶│ Approved │
│         │    │  Approval    │    │  Second Approval  │    │          │
└─────────┘    └──────────────┘    └───────────────────┘    └──────────┘
                                                                  │
    ┌──────────┐    ┌──────┐    ┌───────────┐    ┌──────────┐     │
    │ Archived │◀───│ Paid │◀───│   Sent    │◀───│Committed │◀────┘
    └──────────┘    └──────┘    └───────────┘    └──────────┘
                        │
                   ┌────┴─────┐
                   │Partially │
                   │  Paid    │
                   └──────────┘
                        │
                   ┌────┴─────┐
                   │ Credited │
                   └──────────┘
```

| # | Statut | Description | Transition suivante |
|---|---|---|---|
| 1 | **Draft** | Brouillon de facture, en cours de preparation | → Pending Approval |
| 2 | **Pending Approval** | En attente d'approbation de premier niveau | → Pending Second Approval / Approved |
| 3 | **Pending Second Approval** | En attente d'approbation de deuxieme niveau | → Approved |
| 4 | **Approved** | Approuvee, prete a etre engagee | → Committed |
| 5 | **Committed** | Engagee comptablement | → Sent |
| 6 | **Sent** | Envoyee au client | → Paid / Partially Paid |
| 7 | **Paid** | Reglee integralement | → Archived |
| 8 | **Partially Paid** | Partiellement reglee | → Paid / Credited |
| 9 | **Credited** | Avoir emis (credit note) | → Archived |
| 10 | **Archived** | Archivee (cycle de vie termine) | — (Terminal) |

**Particularites notables :**
- **Double approbation** : le workflow supporte un systeme de double approbation (Pending Approval → Pending Second Approval) pour les factures depassant un certain seuil ou pour certains types de projets
- **Engagement comptable** : le statut "Committed" cree une ecriture comptable avant l'envoi au client
- **Credit note** : le statut "Credited" permet d'emettre des avoirs sur des factures partiellement payees

### 4.5 Gestion multi-entites

| Entite | Role | Projets associes |
|---|---|---|
| **Provencher Roy Prod** | Entite de production principale | Projets clients numerotes, factures clients |
| **PRAA (Provencher Roy Associes architectes Inc.)** | Entite de holding/administration | Projets Admin, projets departementaux, intercompagnie |

**Impact sur la facturation :**
- Chaque entite a son propre **bureau de facturation** (Billing Office)
- Les taux de facturation peuvent varier selon l'entite
- Les factures sont emises par entite (pas de facturation croisee automatique)
- Le projet intercompagnie (130094 Provencher Roy Design Inc. - Interco) gere les transferts entre entites

### 4.6 KPIs financiers au niveau projet

Le profil de chaque projet (Project Profile) affiche des **KPIs financiers en temps reel** :

| KPI | Description | Source |
|---|---|---|
| **Revenue** | Revenus generes (heures × taux de facturation) | Calcule depuis les feuilles de temps + contrats |
| **Cost** | Couts engages (heures × taux de cout interne) | Calcule depuis les feuilles de temps + couts RH |
| **Profit** | Benefice (Revenue - Cost) | Calcule |
| **Margin %** | Marge beneficiaire en pourcentage (Profit / Revenue × 100) | Calcule |

### 4.7 Differences de facturation selon le type de projet

| Caracteristique | Projets clients | Projets admin | Projets departementaux |
|---|---|---|---|
| **Facturable** | Oui (majorite) | Oui | Non |
| **Contrat associe** | Oui (obligatoire pour facturer) | Possible | Non |
| **Roles de facturation** | Definis dans le contrat | N/A ou simplifies | N/A |
| **Taux horaire** | Variable par role (Architecte, Designer, etc.) | Taux interne uniquement | N/A |
| **Remise/Discount** | Possible (Discount % dans le contrat) | Non | N/A |
| **Factures** | Generees et envoyees aux clients | Factures internes (cout-only) | Pas de factures |
| **Workflow approbation** | Double approbation possible | Approbation simple | N/A |
| **KPIs financiers** | Revenue, Cost, Profit, Margin% | Cost uniquement | Heures uniquement |
| **Devise** | CAD (possiblement multi-devises) | CAD | N/A |

---

## 5. Vues disponibles dans le module Projects

ChangePoint offre **3 vues principales** pour visualiser les projets :

| Vue | Description | Usage principal |
|---|---|---|
| **Tree View** | Arborescence hierarchique expandable | Navigation dans la structure WBS, visualisation de la hierarchie |
| **List View** | Liste plate avec colonnes triables et filtrables | Recherche rapide, filtrage par statut/entite, vue d'ensemble |
| **Worksheet View** | Grille de type tableur avec colonnes editables | Modification en masse, saisie de donnees, vue detaillee des champs |

### 5.1 Filtres de la List View

| Filtre | Valeurs observees | Description |
|---|---|---|
| **Quick filter** | Texte libre + "%" (wildcard) | Recherche par nom ou code projet |
| **Status** | Active, Completed | Statut du projet |
| **Billable** | Yes, No | Flag de facturabilite |
| **Entity** | Provencher_Roy Prod, PRAA | Entite juridique |

---

## 6. Recommandations pour l'application OOTI

### 6.1 Structure des projets

1. **Supporter les 3 types de projets** : clients (facturables), administratifs (suivi des couts), departementaux (suivi du temps non facturable)
2. **Convention de numerotation configurable** : AANNNN par defaut, mais permettre des formats custom (Admin-XX, prefixes departementaux)
3. **Flag Billable** au niveau projet avec impact automatique sur la facturation
4. **Multi-entites** : supporter plusieurs entites juridiques avec bureaux de facturation distincts

### 6.2 Structure WBS

1. **Minimum 4 niveaux de hierarchie** : Projet → Phase/WBS → Tache → Sous-tache
2. **Numerotation automatique** hierarchique (01.1.1, 01.1.2, etc.)
3. **Taches sommaires vs taches feuilles** : distinction claire entre les niveaux de regroupement (non saisissables) et les taches de saisie de temps
4. **Tree View native** : indispensable pour la navigation dans les gros projets d'architecture
5. **Drag & drop** pour reorganiser les taches dans l'arborescence (non present dans ChangePoint)

### 6.3 Facturation

1. **10 statuts de facture** : reproduire le workflow complet (Draft → Archived) avec possibilite de personnalisation
2. **Double approbation configurable** : seuils configurables par type de projet ou montant
3. **Roles de facturation** lies aux contrats avec taux standard, remise et taux effectif
4. **KPIs financiers temps reel** : Revenue, Cost, Profit, Margin% au niveau projet et portfolio
5. **Credit notes** (avoirs) : supporter les corrections de facturation
6. **Multi-devises** : etendre la gestion CAD actuelle pour supporter d'autres devises (EUR, USD, etc.)

### 6.4 Ameliorations par rapport a ChangePoint

| Fonctionnalite | ChangePoint | OOTI (cible) |
|---|---|---|
| Niveaux WBS | 3-4 observes | Illimite (recommande max 6) |
| Templates de WBS | Non observe | Modeles de structure reutilisables par type de projet |
| Gantt integre | Non observe dans cette instance | Vue Gantt native liee a la structure WBS |
| Facturation automatique | Manuelle (Draft) | Generation automatique basee sur les heures + contrat |
| Tableau de bord financier | KPIs basiques par projet | Dashboard interactif avec graphiques et tendances |
| Export comptable | Non explore | Integration native avec les logiciels comptables |
| Numerotation WBS | Semi-manuelle (01.1, 01.2) | Automatique avec renumerotation en cas d'insertion |

---

## 7. Annexes

### 7.1 Liste complete des projets observes

| # | Code | Nom | Type | Facturable | Entite | Statut |
|---|---|---|---|---|---|---|
| 1 | 130094 | Provencher Roy Design Inc. - Interco | Client | Oui | PRA | Active |
| 2 | 160008 | PRAA-Paie | Client | Oui | PRA | Active |
| 3 | 180200 | Facturation clients divers | Client | Non | PRA | Active |
| 4 | 200236 | Place des Arts - 5eme Salle | Client | Oui | PRA | Active |
| 5 | 230012 | Salaires forfaitaires | Client | Oui | PRA | Active |
| 6 | 240008 | ESG Provencher Roy | Client | Oui | PRA | Active |
| 7 | 250029 | Intelligence Artificielle | Client | Oui | (N/S) | Active |
| 8 | Admin-08 | PRAA-Administration | Admin | Oui | PRA | Completed |
| 9 | Admin-10 | PRAA-Conges RH | Admin | Oui | PRA | Completed |
| 10 | Admin-11 | PRAA-Coordination | Admin | Oui | PRA | Completed |
| 11 | — | PRAA - Administration generale | Departemental | Non | PRAA | Active |
| 12 | — | PRAA - Comptabilite | Departemental | Non | PRAA | Active |
| 13 | — | PRAA - Ressources humaines | Departemental | Non | PRAA | Active |
| 14 | — | PRAA - Technologie information | Departemental | Non | PRAA | Active |

### 7.2 Structure WBS detaillee — Projet 250029

```
250029 Intelligence Artificielle - 250029
└── 01. Intelligence Artificielle (WBS Summary)
    ├── 01.1 Comite Intelligence Artificielle (Tache)
    ├── 01.2 Reflexion et mise en place GPTs (Tache)
    ├── 01.3 Developpement Application CV/Projet (Tache)
    ├── 01.4 Outils IA 3D (Tache)
    ├── 01.5 Formation (Tache)
    ├── 01.6 Outils IA TI (Tache)
    └── 01.7 Reflexion Atelier (Tache)
```

### 7.3 Structure WBS detaillee — Projet PRAA - Administration generale

```
PRAA - Administration generale
├── Rencontres/Meetings (Tache, expandable ▶)
├── Formation/Coaching (Tache, expandable ▶)
├── Autres/Others (Tache, expandable ▶)
└── PRAA - Admin GRC (Sous-projet / Tache sommaire)
```

### 7.4 Assignments non-projet (Time Sheet)

| # | Nom (FR/EN) | Categorie |
|---|---|---|
| 1 | Formation externe | Formation |
| 2 | Temps en banque | Compensation |
| 3 | Conge sans solde | Absence |
| 4 | Vacances | Absence |
| 5 | Maladie | Absence |
| 6 | Ferie | Absence |
| 7 | Conges sociaux | Absence |
| 8 | Pour RH - ICD | RH |
| 9 | Pour RH - ILD | RH |

### 7.5 Contrat client reel — 200236 Place des Arts - 5eme Salle [PRA]

**Donnees du contrat (profil complet) :**

| Champ | Valeur |
|---|---|
| **Statut** | Completed |
| **Valeur du contrat** | 882,350 CAD |
| **Montant facture** | 1,110,469 CAD |
| **Montant paye** | 1,074,651 CAD |
| **Client** | Societe de la Place des Arts |
| **Contact principal** | RABIH RAAD |
| **Numero de contrat** | 02-3000-000 |
| **Contract ID** | C210069 |
| **Contract manager** | Melissa Belanger |
| **Date debut** | 1/1/2021 |
| **Date fin** | 12/31/2021 |
| **Bureau de facturation** | Provencher Roy Associes Architectes inc |
| **Devise** | Canadian dollar (CAD) |
| **Type de facturation** | **Mixed - Fixed Fee/Hourly** |
| **Termes de paiement** | Net 30 days |
| **Maximum par facture** | 0.00 CAD (illimite) |
| **Time approver** | Melissa Belanger |
| **Approver for time approver** | Audrey Monty |
| **Expense approver** | Melissa Belanger |
| **Approver for expense approver** | Audrey Monty |
| **Expenses approval limit** | 0.00 CAD |

**Roles de facturation et taux horaires :**

| Role de facturation | Taux standard (CAD/h) | Remise (%) | Taux effectif (CAD/h) | Devise |
|---|---|---|---|---|
| Architecte intermediaire | 77.00 | 0.00 | 77.00 | CAD |
| Architecte junior | 63.40 | 0.00 | 63.40 | CAD |
| Architecte patron | 150.85 | 0.00 | 150.85 | CAD |
| Architecte patron (Melissa Belanger) | 0.00 | 0.00 | 150.85 | CAD |
| Architecte senior | 92.10 | 0.00 | 92.10 | CAD |

**Observations cles sur les taux :**
- **4 niveaux hierarchiques** d'architectes avec des taux distincts
- Ratio patron/junior = 2.38x (150.85 / 63.40)
- Possibilite de **surcharge par ressource** (Melissa Belanger a un taux standard de 0.00 mais un taux de facturation de 150.85)
- **Aucune remise** sur ce contrat (Discount = 0% pour tous les roles)

**Forfaits (Fixed fees) — Jalons de facturation :**

| Date de facturation | Montant (CAD) |
|---|---|
| 1/28/2023 | 22,573.39 |
| 9/30/2023 | 865.00 |
| 9/30/2023 | 8,650.00 |
| 1/1/2024 | 64,706.00 |
| 1/1/2024 | 17,500.00 |
| **Total forfaits** | **114,294.39** |

**Type de facturation "Mixed - Fixed Fee/Hourly" :**
Ce type de facturation hybride est tres courant en architecture :
- **Partie forfaitaire** : les phases de conception sont facturees a prix fixe (jalons predetermines)
- **Partie horaire** : les extras, modifications et services complementaires sont factures au taux horaire
- Le contrat de 882,350 CAD represente la partie forfaitaire ; les 1,110,469 CAD factures incluent aussi la partie horaire

**Sections additionnelles du contrat :**
- Contract limits (limites contractuelles)
- Work locations and work codes (lieux de travail multi-provinces)
- Revenue recognition (reconnaissance des revenus comptables)
- Vendors (sous-traitants/fournisseurs)
- Configurable fields (champs personnalisables)
- Record history (historique des modifications)
- Request processing rules (regles de traitement des demandes)
- Request SLAs (accords de niveau de service)
- Knowledge items (base de connaissances)
- Reports : "Detail des forfaits", "Factures par contrat"

### 7.6 Profil de projet — KPIs detailles (240008 ESG)

**En-tete KPIs :**

| KPI | Sous-KPI 1 | Valeur 1 | Sous-KPI 2 | Valeur 2 |
|---|---|---|---|---|
| **BUDGET** | Billing | 0 CAD | Cost | 0 CAD |
| **EFFORT** | Planned | 40 Hours | Actual | 1,565 Hours |
| **BILLINGS** | Billed | 0 CAD | Available | 0 CAD |
| **MARGIN** | Value | 0 CAD | % | 0 % |

**Sections du profil de projet :**
- General (Project ID, Project manager, Contract, Planned start/finish/hours)
- Status information
- Finance (Finance details, Billing office for fiscal periods)
- Fiscal year breakdown
- Configurable fields
- Materials
- Work locations and work codes
- Budget
- Knowledge items
- Reports (3 rapports integres)

**Work locations (multi-provinces) :**
- Alberta
- Colombie-Britannique
- Ile-du-Prince-Edouard
- Default work location : **Quebec**
- Work codes : Default

### 7.7 Structure WBS detaillee — Projet 240008 ESG Provencher Roy

```
240008 - ESG Provencher Roy
└── ESG Provencher_Roy (WBS Summary)
    ├── Coordination du dossier (Tache)
    ├── Redaction du rapport (Tache)
    └── Rencontre (Tache)
```

### 7.8 Structure WBS detaillee — Projet 130094 Interco (projet interne)

```
130094 Provencher Roy Design Inc. - Interco [PRA]
├── 00. Interco PRAA-PRDI (WBS Summary — ~25 taches)
│   ├── Informatique MHAD
│   ├── Administration PRDI (non facturable)
│   ├── Revue de plans PRDI
│   ├── Support ODS PRDI
│   ├── 210219 Polytechnique Phases I et II - 4e a 6e etage
│   ├── 210285 Croissance Centre Intelligence Securite De...
│   ├── 210541 Elite Accounting
│   ├── 220055 - Amenagement Clinique 9900 Cavendish
│   ├── 220061 Riverside
│   ├── 220293 Valmet
│   ├── 230050_3260 GUENETTE
│   ├── 230084_3200 Guenette
│   ├── 230087 Polytechnique Phase III - 4e etage
│   ├── 230119 The Print House 035 - 112 Kent
│   ├── 230130 Polytechnique Phase IV - 2e etage
│   ├── 230145 BNP Paribas - Services professionnels
│   ├── 230239 Equisoft - 1250 Rene-Levesque - Phase 2
│   ├── 230264 SAAQ Place Versailles
│   ├── 220244 RBC 1 PVM 4e Sud et 5e Ouest
│   ├── 230239 Equisoft (doublon)
│   ├── 200194 C.D-Tour Nord - Revenu Quebec PRDI
│   ├── 230075 - 7777 Decarie
│   ├── 230127 - 800 Square Victoria
│   ├── 230218 - PSB Boisjoli
│   └── 230237 BoxOne - Green Zone
└── Sommaire historique (WBS Summary, expandable)
```

**Observation importante :** Le projet Interco utilise les **numeros de projets clients reels** comme noms de taches pour le suivi intercompagnie. Cela permet de ventiler les couts intercompagnie par mandat client.

### 7.9 Types de facturation identifies dans ChangePoint

| Type de facturation | Description | Exemple |
|---|---|---|
| **Mixed - Fixed Fee/Hourly** | Facturation hybride : partie forfaitaire + partie horaire | 200236 Place des Arts (882K forfait + extras horaires) |
| **Time and Materials** | Facturation 100% au taux horaire | (Projets en regie pure) |
| **Fixed Fee** | Facturation 100% forfaitaire par jalons | (Projets au forfait pur) |
| **Non-billable** | Pas de facturation (suivi du temps seulement) | PRAA - Administration generale |

### 7.10 Colonnes de la List View Projects (mise a jour)

| Colonne | Description | Exemple |
|---|---|---|
| ALL PROJECTS | Nom complet du projet | 200236 Place des Arts - 5eme Salle [PRA] |
| STATUS | Statut du projet | Active, Completed |
| CUSTOMER | Client | Societe de la Place des Arts, Provencher Roy Ass... |
| CONTRACT | Contrat associe | 200236 Place des Arts - 5eme Salle [PRA] |
| BILLABLE | Flag de facturabilite | ✓ (checkmark) ou vide |
| PROJECT CONTACT | Contact du projet | Contact Principal |
| UPDATED | Date de derniere modification | 2/27/2026 |

### 7.11 Colonnes de la List View Contracts

| Colonne | Description | Exemple |
|---|---|---|
| RECENTS | Nom du contrat | 200236 Place des Arts - 5eme Salle [PRA] |
| STATUS | Statut du contrat | Completed, Work in progress |
| LINE OF B... | Ligne de metier | Autres |
| CUSTOMER | Client | Societe de la Place des Arts |
| MAIN CONTACT | Contact principal | RABIH RAAD |
| CONTRACT M... | Gestionnaire de contrat | Melissa Belanger |
| AMOUNT | Montant du contrat | 882,350 CAD |
| UPDATED | Date de derniere modification | 1/20/2025 |

### 7.12 Contrats identifies

| # | Contrat | Statut | Client | Montant | Gestionnaire |
|---|---|---|---|---|---|
| 1 | 200236 Place des Arts - 5eme Salle [PRA] | Completed | Societe de la Place des Arts | 882,350 CAD | Melissa Belanger |
| 2 | PRAA - Projets administratifs | Work in progress | Provencher Roy | 0 CAD | Alex Piguet |
| 3 | 230156 SQI Reamenagement et agrandissement hopital... | Work in progress | Groupe A / ML... | 0 CAD | Alex Piguet |

---

*Document genere et mis a jour le 27 fevrier 2026 — Audit Planview ChangePoint (instance Provencher Roy)*
