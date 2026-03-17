# EPIC — Module Coûts

**Application OOTI** — Gestion de projets pour cabinets d'architecture
**Version 1.0** — Février 2026

---

## 1. Identification

| Champ | Valeur |
|---|---|
| **Nom** | Coûts |
| **Référence** | EPIC-007 |
| **Module parent** | Gestion |
| **Priorité** | Haute |
| **Auteur** | Architecte Logiciel Senior |
| **Date de création** | 26 février 2026 |
| **Statut** | Draft |
| **EPICs liés** | EPIC-002 Projets, EPIC-004 Facturation, EPIC-005 Temps, EPIC-008 Finances, EPIC-013 Notes de frais |

---

## 2. Contexte & Problématique

### 2.1 Contexte métier

Les cabinets d'architecture opèrent dans un environnement économique où la maîtrise des coûts est un facteur déterminant de rentabilité. Chaque projet mobilise une combinaison de ressources internes (salaires, temps passé), de ressources externes (sous-traitants, co-traitants, BET spécialisés) et de frais divers (déplacements, impressions, fournitures). La structure de coûts d'une agence d'architecture est par nature complexe et multi-dimensionnelle :

- **Coûts directs projet** : heures de travail des collaborateurs, sous-traitance technique (structure, fluides, acoustique, VRD...), co-traitance, impressions et maquettes, déplacements chantier.
- **Coûts indirects** : masse salariale globale, loyer et charges locatives, assurances professionnelles (RC décennale, RC professionnelle), abonnements logiciels (AutoCAD, Revit, SketchUp...), fournitures de bureau, formation continue.
- **Coûts de sous-traitance** : les cabinets travaillent systématiquement avec des bureaux d'études techniques (BET), des économistes de la construction, des paysagistes, des géomètres, qui génèrent des factures à suivre et à imputer aux projets.

### 2.2 Problématique

Sans outil centralisé de suivi des coûts, les cabinets d'architecture font face aux difficultés suivantes :

1. **Absence de vision consolidée** : les coûts sont dispersés entre tableurs, factures papier, relevés bancaires et logiciels comptables. Il est impossible d'obtenir rapidement une vision globale des dépenses de l'agence.
2. **Impossibilité de mesurer la rentabilité projet** : sans imputation précise des coûts directs et indirects à chaque projet, le cabinet ne peut pas déterminer quels projets sont rentables et lesquels génèrent des pertes.
3. **Dépassements budgétaires non détectés** : l'absence de comparaison budget prévisionnel / coûts réels en temps réel conduit à des dépassements découverts trop tard, parfois après la fin du projet.
4. **Suivi des sous-traitants défaillant** : les contrats de sous-traitance, les acomptes versés, les factures reçues et les situations de paiement sont suivis de manière artisanale, générant des retards de paiement et des litiges.
5. **Taux horaires imprécis** : le calcul du coût réel d'un collaborateur (salaire brut + charges patronales + frais de structure) est rarement actualisé, faussant les devis et la rentabilité calculée.
6. **Exports comptables manuels** : la transmission des données de coûts au cabinet comptable repose sur des exports manuels fastidieux et sources d'erreurs.

### 2.3 Impact

L'absence de maîtrise des coûts se traduit directement par :
- Une marge nette moyenne de 3 à 8 % pour les cabinets d'architecture, alors qu'une bonne gestion permettrait d'atteindre 12 à 18 %.
- Des décisions de pricing (honoraires) basées sur l'intuition plutôt que sur des données réelles de coûts.
- Une incapacité à négocier efficacement avec les sous-traitants faute de données historiques comparatives.
- Un risque financier accru sur les projets à forfait.

---

## 3. Objectif

### 3.1 Objectif principal

Fournir aux cabinets d'architecture un module centralisé et exhaustif de suivi des coûts, permettant une vision en temps réel des dépenses à l'échelle de l'agence et de chaque projet, la comparaison systématique budget prévisionnel vs coûts réels, et l'optimisation de la rentabilité globale.

### 3.2 Objectifs spécifiques

| # | Objectif | Indicateur de succès |
|---|---|---|
| O1 | Centraliser l'ensemble des coûts de l'agence dans une interface unique | 100 % des catégories de coûts couvertes (salaires, sous-traitance, frais généraux, notes de frais) |
| O2 | Permettre l'imputation précise des coûts à chaque projet et phase | Chaque coût est rattaché à un projet et optionnellement à une phase |
| O3 | Offrir une comparaison budget prévisionnel vs réel en temps réel | Tableau de bord avec indicateurs d'écart accessibles en moins de 2 clics |
| O4 | Gérer le cycle de vie complet des entreprises externes | CRUD complet, contrats, factures reçues, situations de paiement |
| O5 | Calculer automatiquement les taux horaires réels des collaborateurs | Taux horaire calculé à partir du salaire brut, charges et temps de travail effectif |
| O6 | Automatiser les exports comptables | Export au format requis par les logiciels comptables courants (FEC, CSV, DATEV) |
| O7 | Détecter les dépassements budgétaires en amont | Alertes automatiques à 80 %, 90 % et 100 % du budget consommé |

---

## 4. Périmètre Fonctionnel

### 4.1 Navigation et structure

Le module Coûts est accessible depuis deux points d'entrée dans l'application :

#### 4.1.1 Entrée Agence (Sidebar GESTION > Coûts)

Six sous-menus composent la vue agence :

| Sous-menu | Description | Accès |
|---|---|---|
| **Résumé** | Tableau de bord synthétique des coûts agence avec KPIs, graphiques et tendances | Admin, Direction |
| **Entreprises Externes** | Gestion des sous-traitants, co-traitants, fournisseurs : annuaire, contrats, factures | Admin, Chef de projet |
| **Notes de frais** | Vue consolidée de toutes les notes de frais de l'agence (lien EPIC-013) | Admin, Direction |
| **Salaires** | Masse salariale, coûts par collaborateur, taux horaires, charges sociales | Admin, Direction (données sensibles) |
| **Frais généraux** | Loyer, assurances, abonnements logiciels, fournitures, maintenance, etc. | Admin, Direction |
| **Exports** | Génération d'exports comptables multi-formats avec filtres et périodes | Admin, Comptable |

#### 4.1.2 Entrée Projet (Onglet COÛTS dans la fiche projet)

Quatre sous-sections composent la vue projet :

| Sous-section | Description |
|---|---|
| **Planning** | Planning prévisionnel de facturation des sous-traitants et des dépenses projet |
| **Factures** | Factures fournisseurs reçues et imputées au projet |
| **Devis** | Devis fournisseurs reçus, comparés et validés |
| **Éléments de dépense** | Détail granulaire de chaque ligne de dépense du projet |

### 4.2 Fonctionnalités détaillées

#### 4.2.1 Vue Résumé des coûts agence

- **KPIs principaux** : coûts totaux période, coûts par catégorie (salaires, sous-traitance, frais généraux, notes de frais), ratio coûts/chiffre d'affaires, évolution mensuelle.
- **Graphiques** : répartition des coûts par catégorie (camembert), évolution mensuelle (courbe), top 10 projets les plus coûteux (barres), comparaison budget vs réel par projet (barres groupées).
- **Filtres** : période (mois, trimestre, année, personnalisé), projet, catégorie de coût, entreprise externe.
- **Alertes** : projets en dépassement budgétaire, factures fournisseurs en attente de paiement, échéances contractuelles sous-traitants.

#### 4.2.2 Gestion des Entreprises Externes

- **Annuaire** : création, modification, archivage des entreprises (sous-traitants BET, co-traitants, fournisseurs récurrents).
- **Fiche entreprise** : raison sociale, SIRET/SIREN, adresse, contacts, RIB, type (sous-traitant, co-traitant, fournisseur), spécialité (structure, fluides, acoustique, VRD, paysage...), conditions de paiement par défaut, documents (Kbis, assurances, attestations).
- **Contrats** : rattachement de contrats de sous-traitance par projet, montant, échéancier de paiement, conditions de révision, pénalités.
- **Historique** : historique complet des projets réalisés avec chaque entreprise, montants facturés, évaluation qualité.

#### 4.2.3 Factures fournisseurs

- **Création** : saisie manuelle ou import (scan OCR en phase ultérieure).
- **Champs** : numéro de facture, date, date d'échéance, entreprise émettrice, projet(s) imputé(s), phase(s), montant HT, TVA, montant TTC, devise, statut (reçue, validée, en paiement, payée, litige).
- **Workflow de validation** : soumission > validation chef de projet > validation direction > paiement.
- **Rapprochement** : lien avec le contrat de sous-traitance, vérification du montant restant contractuel.
- **Pièces jointes** : stockage du PDF de la facture originale.

#### 4.2.4 Notes de frais consolidées

- **Agrégation** : vue consolidée de toutes les notes de frais saisies individuellement par les collaborateurs (données provenant du module EPIC-013 Notes de frais).
- **Filtres** : par collaborateur, par projet, par catégorie (transport, restauration, hébergement, fournitures), par statut (soumise, validée, remboursée), par période.
- **Totaux** : montant total par période, moyenne par collaborateur, répartition par catégorie.
- **Imputation** : vérification que chaque note de frais est bien imputée à un projet.

#### 4.2.5 Salaires et taux horaires

- **Masse salariale** : vue globale de la masse salariale mensuelle et annuelle de l'agence.
- **Coût par collaborateur** : salaire brut mensuel, taux de charges patronales, coût total employeur, nombre d'heures travaillées (lien EPIC-005 Temps), taux horaire réel calculé.
- **Taux horaire moyen** : calcul automatique du taux horaire moyen de l'agence, par grade/niveau, par département.
- **Formule de calcul** : `Taux horaire = (Salaire brut annuel × (1 + taux charges)) / Nombre d'heures productives annuelles`.
- **Simulation** : outil de simulation pour ajuster les taux horaires en fonction de scénarios (augmentation salariale, embauche, variation du taux de charges).
- **Confidentialité** : accès strictement limité aux rôles Admin et Direction. Les données individuelles ne sont jamais visibles par les collaborateurs standards.

#### 4.2.6 Frais généraux

- **Catégories** : loyer et charges locatives, assurances (RC décennale, RC professionnelle, multirisque), abonnements logiciels (licences), téléphonie et internet, fournitures de bureau, entretien et maintenance, formation professionnelle, honoraires comptables et juridiques, divers.
- **Saisie** : montant, date, catégorie, description, récurrence (ponctuel, mensuel, trimestriel, annuel), fournisseur, pièce justificative.
- **Récurrence** : gestion automatique des charges récurrentes avec génération automatique des écritures.
- **Répartition** : possibilité de ventiler les frais généraux sur les projets au prorata (heures, surface, CA...).

#### 4.2.7 Exports comptables

- **Formats** : CSV, Excel (XLSX), FEC (Fichier des Écritures Comptables, norme française), PDF récapitulatif.
- **Filtres** : période, catégorie de coût, projet, entreprise externe, statut de paiement.
- **Contenu** : journal des achats, balance fournisseurs, grand livre auxiliaire fournisseurs, état récapitulatif TVA déductible.
- **Planification** : possibilité de programmer des exports automatiques périodiques (mensuel, trimestriel).
- **Historique** : conservation de l'historique des exports générés avec date, périmètre et utilisateur.

#### 4.2.8 Coûts par projet

- **Synthèse** : coût total du projet, décomposé par catégorie (main d'oeuvre interne, sous-traitance, frais directs, quote-part frais généraux).
- **Budget vs réel** : comparaison du budget prévisionnel initial avec les coûts réels engagés, calcul de l'écart en montant et en pourcentage.
- **Par phase** : ventilation des coûts par phase de projet (esquisse, APS, APD, PRO, DCE, DET, AOR...).
- **Rentabilité** : calcul de la marge projet = honoraires facturés - coûts totaux.
- **Indicateurs visuels** : code couleur vert/orange/rouge selon le niveau de consommation budgétaire.

#### 4.2.9 Planning de facturation sous-traitants

- **Échéancier** : calendrier prévisionnel des factures attendues de chaque sous-traitant par projet.
- **Suivi** : comparaison entre le planning prévisionnel et les factures effectivement reçues.
- **Alertes** : notification des factures attendues non reçues, des écarts de montant entre prévisionnel et réel.

#### 4.2.10 Devis fournisseurs

- **Réception** : enregistrement des devis reçus des fournisseurs et sous-traitants.
- **Comparaison** : mise en parallèle de plusieurs devis pour un même besoin (tableau comparatif).
- **Validation** : workflow de validation du devis retenu (soumission > validation chef de projet > validation direction).
- **Transformation** : conversion d'un devis validé en commande/contrat puis suivi des factures associées.
- **Archivage** : conservation de tous les devis (retenus et non retenus) pour historique et benchmark.

---

## 5. User Stories

### US-C01 — Vue résumé des coûts agence

**En tant que** dirigeant de cabinet d'architecture,
**Je veux** accéder à un tableau de bord synthétique présentant l'ensemble des coûts de l'agence avec des KPIs, graphiques et alertes,
**Afin de** piloter la rentabilité globale de l'agence et prendre des décisions éclairées sur la stratégie financière.

**Critères d'acceptance :**

1. Le tableau de bord affiche les KPIs suivants : coûts totaux de la période sélectionnée, répartition par catégorie (salaires, sous-traitance, frais généraux, notes de frais), ratio coûts/chiffre d'affaires, variation par rapport à la période précédente (N-1).
2. Un graphique en camembert présente la répartition des coûts par catégorie avec les pourcentages et montants associés.
3. Un graphique en courbe affiche l'évolution mensuelle des coûts sur les 12 derniers mois avec possibilité de superposer les données de l'année précédente.
4. Un classement des 10 projets les plus coûteux est affiché sous forme de barres horizontales, avec accès direct à la fiche coûts du projet au clic.
5. Les filtres suivants sont disponibles et combinables : période (mois, trimestre, année, dates personnalisées), projet(s), catégorie(s) de coût, entreprise(s) externe(s), collaborateur(s).
6. Une zone d'alertes affiche les projets en dépassement budgétaire (>90 % du budget consommé), les factures fournisseurs en attente de validation depuis plus de 7 jours, et les échéances contractuelles sous-traitants à venir dans les 30 jours.
7. Les données sont actualisées en temps réel (ou au maximum avec un délai de 5 minutes) sans rechargement manuel de la page.
8. Le tableau de bord est accessible uniquement aux utilisateurs ayant le rôle Admin ou Direction.

---

### US-C02 — Gestion des entreprises externes (sous-traitants)

**En tant que** chef de projet,
**Je veux** gérer un annuaire complet des entreprises externes (sous-traitants, co-traitants, fournisseurs) avec leurs informations, contrats et historique,
**Afin de** centraliser les informations de mes partenaires, faciliter la collaboration et garder une trace de toutes les relations contractuelles.

**Critères d'acceptance :**

1. Je peux créer une nouvelle entreprise externe en renseignant : raison sociale (obligatoire), type (sous-traitant / co-traitant / fournisseur, obligatoire), SIRET/SIREN, adresse complète, contacts (nom, email, téléphone), RIB/IBAN, spécialité(s) (structure, fluides, acoustique, VRD, paysage, économie de la construction...), conditions de paiement par défaut (délai en jours, mode de paiement).
2. Je peux modifier les informations d'une entreprise existante, et l'historique des modifications est conservé (date, utilisateur, champs modifiés).
3. Je peux archiver une entreprise (soft delete) sans perdre l'historique des projets et factures associés. L'entreprise archivée n'apparaît plus dans les listes de sélection mais reste accessible via un filtre "Archivés".
4. La liste des entreprises externes est affichée sous forme de tableau avec tri et filtres : par type, par spécialité, par statut (actif/archivé), recherche textuelle sur le nom.
5. La fiche d'une entreprise affiche un onglet "Projets" listant tous les projets sur lesquels elle est intervenue, avec le montant total facturé par projet.
6. La fiche d'une entreprise affiche un onglet "Documents" permettant d'uploader et consulter les documents administratifs (Kbis, attestation d'assurance, attestation URSSAF, contrats-cadres).
7. Je peux rattacher un contrat de sous-traitance à un projet avec les informations suivantes : objet du contrat, montant forfaitaire ou taux, échéancier de paiement prévisionnel, date de début et fin, conditions de révision.
8. La fiche affiche un résumé financier : montant total contractualisé, montant total facturé, montant total payé, solde restant dû.

---

### US-C03 — Création et édition de facture fournisseur

**En tant que** chef de projet ou administrateur,
**Je veux** créer, modifier et suivre les factures reçues des fournisseurs et sous-traitants,
**Afin de** assurer un suivi rigoureux des engagements financiers et des paiements à réaliser.

**Critères d'acceptance :**

1. Je peux créer une facture fournisseur en renseignant : numéro de facture (obligatoire, unique par entreprise), date de facture (obligatoire), date d'échéance (calculée automatiquement selon les conditions de paiement de l'entreprise, modifiable), entreprise émettrice (sélection depuis l'annuaire, obligatoire), projet(s) imputé(s) (obligatoire, multi-sélection possible), phase(s) du projet, montant HT, taux de TVA, montant TTC (calcul automatique), devise.
2. Je peux rattacher un fichier PDF de la facture originale (upload de document, formats acceptés : PDF, JPG, PNG, taille max 10 Mo).
3. La facture suit un workflow de validation configurable : Reçue > En validation > Validée > En paiement > Payée, avec possibilité de statut "Litige". Chaque changement de statut est horodaté avec l'utilisateur.
4. Le chef de projet peut valider une facture si son montant est inférieur ou égal au montant restant sur le contrat de sous-traitance. Si dépassement, une alerte est affichée et la validation nécessite l'approbation de la direction.
5. Je peux ventiler le montant d'une facture sur plusieurs projets et/ou plusieurs phases avec des pourcentages ou montants, la somme devant correspondre au montant total de la facture.
6. La liste des factures est affichable et filtrable par : statut, entreprise, projet, période, montant, date d'échéance (échues, à échoir dans 7/15/30 jours).
7. Le système envoie une notification automatique lorsqu'une facture arrive à échéance dans les 7 jours et n'est pas encore en statut "En paiement" ou "Payée".
8. La modification d'une facture déjà validée nécessite une demande de dé-validation par la direction, avec traçabilité de la raison.

---

### US-C04 — Notes de frais consolidées

**En tant que** directeur d'agence,
**Je veux** visualiser une vue consolidée de toutes les notes de frais de l'agence avec des filtres et totaux,
**Afin de** contrôler les dépenses de frais professionnels, vérifier leur bonne imputation aux projets et identifier d'éventuels abus.

**Critères d'acceptance :**

1. La vue consolidée affiche l'ensemble des notes de frais saisies par les collaborateurs (données provenant du module EPIC-013 Notes de frais) sous forme de tableau paginé avec : date, collaborateur, catégorie (transport, restauration, hébergement, fournitures, divers), description, montant, projet imputé, statut (soumise, validée, remboursée, rejetée).
2. Les filtres suivants sont disponibles et combinables : période (dates de/à), collaborateur(s), projet(s), catégorie(s), statut(s), montant minimum/maximum.
3. Des totaux sont affichés en pied de tableau et en en-tête : montant total pour la sélection courante, nombre de notes de frais, montant moyen par note.
4. Un graphique de répartition par catégorie est affiché, ainsi qu'un graphique d'évolution mensuelle.
5. Un KPI "Montant moyen par collaborateur" est calculé et affiché, avec possibilité de comparer les collaborateurs entre eux.
6. Je peux identifier rapidement les notes de frais non imputées à un projet (filtre "Sans projet") pour demander aux collaborateurs de compléter l'imputation.
7. L'export de la vue consolidée est possible au format CSV et Excel avec les filtres appliqués.
8. L'accès à cette vue est restreint aux rôles Admin et Direction ; un chef de projet ne voit que les notes de frais de son équipe projet.

---

### US-C05 — Gestion des salaires et taux horaires

**En tant que** directeur d'agence,
**Je veux** gérer la masse salariale de l'agence, définir les coûts par collaborateur et calculer automatiquement les taux horaires réels,
**Afin de** connaître le coût réel de chaque collaborateur, calculer précisément la rentabilité des projets et établir des devis cohérents.

**Critères d'acceptance :**

1. Je peux saisir pour chaque collaborateur : salaire brut mensuel, taux de charges patronales (pourcentage ou montant), nombre d'heures contractuelles annuelles, date d'effet (pour historiser les changements de salaire).
2. Le système calcule automatiquement le taux horaire réel selon la formule : `Taux horaire = (Salaire brut annuel × (1 + taux de charges patronales)) / Nombre d'heures productives annuelles`, où le nombre d'heures productives = heures contractuelles - congés - jours fériés - absences.
3. Un tableau affiche la masse salariale mensuelle et annuelle de l'agence avec : nombre de collaborateurs, coût total employeur, salaire brut moyen, taux horaire moyen, répartition par grade/niveau (stagiaire, junior, confirmé, senior, associé).
4. Le taux horaire moyen de l'agence est calculé et disponible comme paramètre pour les modules Projets (EPIC-002) et Honoraires.
5. Un outil de simulation permet de modéliser l'impact d'une augmentation salariale, d'une embauche ou d'un changement de taux de charges sur le coût horaire moyen et la masse salariale annuelle.
6. L'historique des salaires de chaque collaborateur est conservé avec les dates d'effet, permettant de reconstituer le coût à n'importe quelle période.
7. Les données salariales individuelles sont strictement confidentielles : accès limité aux rôles Admin et Direction. Les chefs de projet accèdent uniquement au taux horaire moyen par grade (sans détail individuel).
8. Un export anonymisé de la masse salariale est disponible pour le cabinet comptable, regroupant les données par catégorie sans détail nominatif.

---

### US-C06 — Gestion des frais généraux

**En tant que** administrateur de l'agence,
**Je veux** saisir, catégoriser et suivre l'ensemble des frais généraux de l'agence (loyer, assurances, abonnements, fournitures...),
**Afin de** avoir une vision complète des charges fixes et variables de l'agence et pouvoir les intégrer dans le calcul du coût de revient.

**Critères d'acceptance :**

1. Je peux créer un frais général en renseignant : catégorie (sélection depuis une liste paramétrable : loyer, charges locatives, assurance RC décennale, assurance RC professionnelle, assurance multirisque, abonnements logiciels, téléphonie/internet, fournitures de bureau, entretien/maintenance, formation, honoraires comptables, honoraires juridiques, divers), montant HT, taux de TVA, montant TTC, date, description, fournisseur (optionnel, lien vers annuaire), pièce justificative (upload PDF).
2. Je peux définir un frais comme récurrent avec une périodicité (mensuel, trimestriel, semestriel, annuel) et une date de fin optionnelle. Le système génère automatiquement les écritures aux dates prévues.
3. La liste des frais généraux est affichée avec filtres par : catégorie, période, récurrence (ponctuel/récurrent), fournisseur. Les totaux par catégorie et le total général sont affichés.
4. Un graphique de répartition par catégorie est disponible, ainsi qu'une évolution mensuelle.
5. Je peux définir une clé de répartition pour ventiler les frais généraux sur les projets : au prorata des heures passées, au prorata du chiffre d'affaires, à parts égales, ou selon une répartition manuelle.
6. Le système calcule le coût de structure mensuel par collaborateur = total frais généraux mensuels / nombre de collaborateurs, et l'intègre optionnellement dans le calcul du taux horaire complet.
7. Les frais récurrents affichent une alerte lorsqu'un renouvellement approche (30 jours avant l'échéance de contrat), permettant d'anticiper les renégociations.
8. La modification ou suppression d'un frais général récurrent propose le choix : modifier/supprimer uniquement cette occurrence, toutes les occurrences futures, ou toutes les occurrences.

---

### US-C07 — Exports comptables des coûts

**En tant que** administrateur ou comptable,
**Je veux** générer des exports structurés des données de coûts dans différents formats compatibles avec les logiciels comptables,
**Afin de** transmettre les données au cabinet comptable de manière fiable, rapide et sans ressaisie manuelle.

**Critères d'acceptance :**

1. Je peux générer un export au format FEC (Fichier des Écritures Comptables) conforme à la norme française (article A.47 A-1 du Livre des Procédures Fiscales), contenant les champs obligatoires : JournalCode, JournalLib, EcritureNum, EcritureDate, CompteNum, CompteLib, CompAuxNum, CompAuxLib, PieceRef, PieceDate, EcritureLib, Debit, Credit, EcrtureLet, DateLet, ValidDate, Montantdevise, Idevise.
2. Je peux générer un export au format CSV et Excel (XLSX) avec un mapping de colonnes configurable (correspondance entre les champs OOTI et les champs attendus par le logiciel comptable du client).
3. Je peux générer un export PDF récapitulatif présentant un état synthétique des coûts par catégorie et par projet pour la période sélectionnée.
4. Les filtres suivants sont disponibles pour délimiter le périmètre de l'export : période (date début, date fin, obligatoire), catégorie(s) de coût, projet(s), entreprise(s) externe(s), statut des factures (toutes, validées uniquement, payées uniquement).
5. Avant la génération, un écran de prévisualisation affiche le nombre de lignes, le total des montants et un aperçu des 20 premières lignes, permettant de vérifier la cohérence avant export.
6. L'historique des exports générés est conservé avec : date de génération, utilisateur, format, périmètre (filtres appliqués), nombre de lignes, lien de téléchargement (conservation 90 jours).
7. Je peux programmer un export automatique récurrent (mensuel ou trimestriel) avec envoi par email à une adresse configurable.
8. Le système détecte et signale les anomalies avant export : factures sans numéro, écritures sans compte comptable, incohérences de TVA.

---

### US-C08 — Coûts par projet (vue projet)

**En tant que** chef de projet,
**Je veux** visualiser l'ensemble des coûts de mon projet ventilés par catégorie et par phase, avec une comparaison budget vs réel,
**Afin de** piloter la rentabilité de mon projet en temps réel et anticiper les dépassements budgétaires.

**Critères d'acceptance :**

1. L'onglet COÛTS de la fiche projet affiche un récapitulatif : coût total du projet, décomposé en coûts de main d'oeuvre interne (heures × taux horaire, données EPIC-005), coûts de sous-traitance (factures des entreprises externes), frais directs (notes de frais imputées au projet), quote-part de frais généraux (si la clé de répartition est activée).
2. Un tableau comparatif Budget vs Réel affiche pour chaque catégorie de coût et chaque phase : le montant budgété, le montant réel engagé, l'écart en montant et en pourcentage, avec un code couleur (vert < 80 %, orange 80-100 %, rouge > 100 %).
3. Un graphique en barres groupées permet de visualiser la comparaison budget vs réel par phase du projet (esquisse, APS, APD, PRO, DCE, DET, AOR).
4. Le coût de main d'oeuvre interne est calculé automatiquement en multipliant les heures saisies dans le module Temps (EPIC-005) par le taux horaire du collaborateur concerné (données EPIC-007 Salaires).
5. La marge du projet est calculée et affichée : Marge = Honoraires facturés (EPIC-004) - Coûts totaux. Le taux de marge est également affiché.
6. Je peux accéder au détail de chaque catégorie de coût en cliquant dessus : liste des factures sous-traitants, liste des notes de frais, détail des heures par collaborateur.
7. Des alertes sont affichées lorsque le budget est consommé à plus de 80 % (orange), 90 % (alerte) et 100 % (rouge/blocage optionnel), configurables par le chef de projet.
8. Un bouton "Exporter le détail des coûts" permet de générer un PDF ou Excel récapitulatif des coûts du projet pour communication au maître d'ouvrage ou usage interne.

---

### US-C09 — Planning de facturation sous-traitants

**En tant que** chef de projet,
**Je veux** établir et suivre un planning prévisionnel de facturation pour chaque sous-traitant intervenant sur mon projet,
**Afin de** anticiper les flux de trésorerie, vérifier la cohérence des factures reçues et détecter les retards ou écarts.

**Critères d'acceptance :**

1. Je peux créer un planning de facturation pour chaque sous-traitant du projet en définissant : les échéances prévues (dates), le montant prévu pour chaque échéance, la phase du projet concernée, la description/objet de l'échéance (ex : "Acompte 30 % études structure", "Solde études fluides").
2. Le planning est affiché sous forme de tableau chronologique avec les colonnes : date prévue, objet, montant prévu, montant facturé (réel), écart, statut (à venir, facture reçue, validée, payée, en retard).
3. Une vue timeline/Gantt simplifié permet de visualiser le planning de facturation de tous les sous-traitants du projet sur un même axe temporel.
4. Lorsqu'une facture fournisseur est saisie et rattachée au projet, le système propose automatiquement de la rapprocher d'une échéance du planning, et met à jour le statut et le montant réel.
5. Le système génère une alerte automatique lorsqu'une échéance prévue est dépassée de plus de 7 jours sans facture reçue correspondante.
6. Le total du planning doit correspondre au montant du contrat de sous-traitance. Un avertissement est affiché en cas d'écart entre le total des échéances et le montant contractuel.
7. Le planning est modifiable : ajout, suppression, modification d'échéances, avec historique des modifications.
8. Un récapitulatif global affiche : montant total contractuel, montant total facturé à date, montant restant à facturer, pourcentage d'avancement financier.

---

### US-C10 — Devis fournisseurs

**En tant que** chef de projet,
**Je veux** enregistrer, comparer et valider les devis reçus des fournisseurs et sous-traitants pour mon projet,
**Afin de** sélectionner la meilleure offre de manière traçable et objectivable, et transformer le devis retenu en engagement contractuel.

**Critères d'acceptance :**

1. Je peux enregistrer un devis fournisseur avec les informations suivantes : entreprise émettrice (sélection depuis l'annuaire), date de réception, date de validité, objet/description, montant HT, taux de TVA, montant TTC, devise, projet imputé, phase du projet, fichier joint (PDF du devis).
2. Je peux saisir le détail des lignes du devis : désignation, quantité, prix unitaire, montant, ce qui permet une comparaison fine entre devis concurrents.
3. Un tableau comparatif permet de mettre en parallèle jusqu'à 5 devis reçus pour un même besoin, avec mise en évidence des écarts de prix ligne par ligne et sur le total.
4. Le devis suit un workflow de validation : Reçu > Présélectionné > Validé (retenu) > Refusé. Seul un devis peut être en statut "Validé" pour un même besoin. La validation d'un devis passe automatiquement les autres en statut "Refusé".
5. La validation d'un devis par la direction génère optionnellement la création automatique d'un contrat de sous-traitance et d'un planning de facturation associé.
6. Le montant du devis validé est automatiquement intégré dans le budget prévisionnel du projet (catégorie sous-traitance).
7. L'historique complet des devis (retenus et non retenus) est conservé pour benchmark et négociation future avec les fournisseurs.
8. Je peux filtrer les devis par : statut, projet, entreprise, période de réception, montant.

---

### US-C11 — Budget prévisionnel vs coûts réels

**En tant que** directeur d'agence ou chef de projet,
**Je veux** définir un budget prévisionnel détaillé pour chaque projet et le comparer en temps réel aux coûts réels engagés,
**Afin de** détecter les dépassements budgétaires au plus tôt, prendre des mesures correctives et améliorer la précision des estimations futures.

**Critères d'acceptance :**

1. Je peux définir un budget prévisionnel pour chaque projet, ventilé par catégorie de coût : main d'oeuvre interne (en heures et en montant), sous-traitance (par lot technique : structure, fluides, VRD...), frais directs (déplacements, impressions, maquettes...), frais généraux (quote-part).
2. Le budget peut être détaillé par phase de projet (esquisse, APS, APD, PRO, DCE, DET, AOR) pour chaque catégorie de coût, formant une matrice Catégorie × Phase.
3. Le système calcule automatiquement les coûts réels engagés pour chaque cellule de la matrice en agrégeant : les heures saisies × taux horaire (EPIC-005), les factures fournisseurs validées, les notes de frais imputées, la quote-part de frais généraux.
4. Un tableau de bord Budget vs Réel affiche pour chaque ligne : budget prévu, coût réel, écart (montant et %), reste à engager estimé, projection à fin de projet (coût final estimé basé sur le rythme de consommation actuel).
5. Des alertes configurables sont déclenchées aux seuils suivants (par défaut) : 80 % du budget consommé (notification informative), 90 % (alerte à valider), 100 % (alerte bloquante optionnelle nécessitant une validation direction pour continuer à imputer des coûts).
6. Un graphique en courbe affiche l'évolution dans le temps des coûts réels cumulés vs le budget prévisionnel (courbe en S), permettant de visualiser les tendances et projections.
7. Le budget prévisionnel peut être révisé (création d'une nouvelle version) avec conservation de l'historique des versions précédentes et de la justification de la révision.
8. Un rapport de synthèse "Budget vs Réel" est exportable en PDF et Excel pour présentation en comité de direction ou au maître d'ouvrage.

---

## 6. Hors Périmètre

Les éléments suivants sont explicitement exclus du périmètre de cet EPIC et pourront faire l'objet d'évolutions futures :

| # | Élément exclu | Justification |
|---|---|---|
| HP-01 | OCR et reconnaissance automatique des factures fournisseurs | Complexité technique élevée, prévue en V2. La saisie manuelle est suffisante pour la V1. |
| HP-02 | Intégration directe avec les logiciels comptables (Sage, Cegid, QuickBooks) | Nécessite des connecteurs API spécifiques à chaque éditeur. Les exports FEC/CSV couvrent le besoin en V1. |
| HP-03 | Gestion de la paie (calcul des bulletins de salaire, DSN) | Hors périmètre métier de OOTI. Les données salariales sont saisies manuellement ou importées. |
| HP-04 | Gestion de la trésorerie et des flux bancaires | Relève du module Finances (EPIC-008). Seuls les coûts engagés sont gérés ici. |
| HP-05 | Rapprochement bancaire automatique | Relève du module Finances (EPIC-008). |
| HP-06 | Gestion des devises multiples avec conversion automatique | En V1, une seule devise par organisation (EUR par défaut). La multi-devise sera traitée en V2. |
| HP-07 | Prévisions et intelligence artificielle (prédiction des coûts) | Nécessite un historique de données suffisant. Prévue en V3. |
| HP-08 | Application mobile pour la saisie des frais | La saisie mobile est couverte par le module Notes de frais (EPIC-013). |
| HP-09 | Gestion des appels d'offres sous-traitants | Processus complet d'appel d'offres (envoi, réception, analyse) non couvert. Seul l'enregistrement des devis reçus est inclus. |
| HP-10 | Calcul automatique de la TVA intracommunautaire | Complexité fiscale reportée en V2. |

---

## 7. Règles Métier

### 7.1 Règles de calcul

| # | Règle | Formule / Description |
|---|---|---|
| RM-01 | Calcul du taux horaire réel | `Taux horaire = (Salaire brut annuel × (1 + taux charges patronales)) / Heures productives annuelles` |
| RM-02 | Heures productives annuelles | `Heures productives = Heures contractuelles - (Congés payés × 7h) - (Jours fériés × 7h) - (Absences × 7h) - (Formation × 7h)` |
| RM-03 | Taux horaire complet (avec frais de structure) | `Taux horaire complet = Taux horaire réel + (Frais généraux mensuels / Nombre collaborateurs / Heures productives mensuelles)` |
| RM-04 | Coût de main d'oeuvre projet | `Coût MO = Σ (Heures saisies par collaborateur × Taux horaire du collaborateur)` |
| RM-05 | Marge projet | `Marge = Honoraires facturés - Coûts totaux (MO + Sous-traitance + Frais directs + Quote-part frais généraux)` |
| RM-06 | Taux de marge projet | `Taux de marge = (Marge / Honoraires facturés) × 100` |
| RM-07 | Projection coût final | `Coût final estimé = Coûts réels + (Budget restant × Coefficient de dérive)`, où `Coefficient de dérive = Coûts réels / Budget consommé théorique à date` |
| RM-08 | TVA facture fournisseur | `Montant TTC = Montant HT × (1 + Taux TVA)`. Taux par défaut : 20 %. Taux réduits acceptés : 10 %, 5.5 %, 2.1 %. |

### 7.2 Règles de gestion

| # | Règle | Description |
|---|---|---|
| RG-01 | Unicité facture fournisseur | Le couple (entreprise externe, numéro de facture) doit être unique. Le système refuse la création d'un doublon. |
| RG-02 | Cohérence contrat / factures | Le total des factures validées pour un contrat de sous-traitance ne peut pas dépasser le montant contractuel sans validation explicite de la direction (dépassement avec justification obligatoire). |
| RG-03 | Imputation obligatoire | Toute facture fournisseur doit être imputée à au moins un projet. Les factures sans imputation sont signalées dans le tableau de bord. |
| RG-04 | Date d'échéance automatique | À la création d'une facture, la date d'échéance est calculée automatiquement à partir de la date de facture + délai de paiement de l'entreprise. Modifiable manuellement. |
| RG-05 | Validation hiérarchique | La validation d'une facture fournisseur suit la hiérarchie : montant < 5 000 EUR : chef de projet. Montant >= 5 000 EUR et < 20 000 EUR : chef de projet + direction. Montant >= 20 000 EUR : direction uniquement. Seuils configurables par organisation. |
| RG-06 | Archivage vs suppression | Aucune donnée financière ne peut être supprimée (conformité comptable). Seul l'archivage (soft delete) est autorisé. |
| RG-07 | Confidentialité salariale | Les données salariales individuelles sont accessibles uniquement aux rôles Admin et Direction. Le taux horaire moyen par grade est accessible aux chefs de projet. |
| RG-08 | Récurrence frais généraux | Les frais généraux récurrents génèrent automatiquement une écriture à chaque échéance. L'utilisateur est notifié 7 jours avant la génération pour modification ou annulation. |
| RG-09 | Versionnement du budget | Toute modification du budget prévisionnel d'un projet crée une nouvelle version. L'historique des versions est conservé avec la date, l'utilisateur et le motif de la révision. |
| RG-10 | Clôture mensuelle | Une fois la période comptable clôturée (action manuelle admin), les écritures de la période ne peuvent plus être modifiées. Seules des écritures de régularisation sont possibles sur la période suivante. |
| RG-11 | Taux de change | En V1, une seule devise par organisation. Si une facture est reçue dans une autre devise, la conversion est faite manuellement au taux du jour par l'utilisateur. |
| RG-12 | Durée de conservation | Les données de coûts sont conservées pendant 10 ans minimum conformément aux obligations légales françaises (article L123-22 du Code de commerce). |

---

## 8. Critères d'Acceptance Globaux

### 8.1 Fonctionnels

| # | Critère | Description |
|---|---|---|
| CAG-01 | Complétude des catégories | Le module couvre les 4 catégories de coûts : salaires, sous-traitance, frais généraux, notes de frais. Aucune catégorie de dépense courante d'un cabinet d'architecture n'est laissée de côté. |
| CAG-02 | Cohérence des calculs | Les totaux par catégorie + les totaux par projet convergent vers le même total général. Aucun écart d'arrondi supérieur à 0,01 EUR. |
| CAG-03 | Traçabilité | Chaque action (création, modification, validation, suppression logique) est historisée avec l'horodatage, l'utilisateur et les valeurs avant/après. |
| CAG-04 | Intégrité référentielle | La suppression d'un projet n'est pas possible s'il a des coûts associés. L'archivage d'une entreprise externe ne supprime pas les factures et contrats existants. |
| CAG-05 | Temps de réponse | Le tableau de bord Résumé se charge en moins de 3 secondes. Les listes paginées (factures, frais) se chargent en moins de 2 secondes. Les exports se génèrent en moins de 30 secondes pour 10 000 lignes. |
| CAG-06 | Conformité comptable | Les exports FEC respectent l'intégralité de la norme (article A.47 A-1 du LPF). Les données sont conformes au PCG (Plan Comptable Général). |
| CAG-07 | Confidentialité | Les données salariales ne sont jamais exposées aux utilisateurs non autorisés, y compris via les API, les exports et les logs. |

### 8.2 Non-fonctionnels

| # | Critère | Description |
|---|---|---|
| CANF-01 | Responsive | L'interface est utilisable sur tablette (1024px minimum). Les tableaux complexes proposent un scroll horizontal. |
| CANF-02 | Accessibilité | Conformité RGAA niveau AA. Les tableaux financiers sont navigables au clavier. Les contrastes de couleur respectent les ratios WCAG 2.1. |
| CANF-03 | Internationalisation | Les montants sont formatés selon la locale de l'utilisateur (séparateur décimal, symbole monétaire). Les dates respectent le format local. |
| CANF-04 | Sécurité | Chiffrement des données salariales au repos (AES-256). Audit trail non modifiable. Tokens d'accès aux exports avec expiration. |
| CANF-05 | Volumétrie | Le module supporte jusqu'à 50 000 factures fournisseurs, 1 000 entreprises externes et 500 collaborateurs sans dégradation de performance. |

---

## 9. Definition of Done (DoD)

Chaque User Story est considérée comme terminée ("Done") lorsque l'ensemble des critères suivants sont satisfaits :

### 9.1 Développement

- [ ] Le code est écrit conformément aux conventions de codage du projet (linting, formatting).
- [ ] Le code est versionné dans la branche feature dédiée et a fait l'objet d'une Pull Request.
- [ ] La revue de code a été réalisée par au moins un pair et tous les commentaires ont été adressés.
- [ ] Les tests unitaires couvrent au minimum 80 % des lignes de code métier (calculs, règles de gestion).
- [ ] Les tests d'intégration couvrent les interactions avec les modules liés (EPIC-002 Projets, EPIC-004 Facturation, EPIC-005 Temps, EPIC-013 Notes de frais).
- [ ] Les migrations de base de données sont réversibles (up/down) et testées.

### 9.2 Qualité

- [ ] Les critères d'acceptance de la User Story sont tous vérifiés et documentés (captures d'écran ou lien vers les tests).
- [ ] Les tests end-to-end (E2E) couvrent les parcours critiques : création de facture, validation, export comptable, budget vs réel.
- [ ] Aucun bug bloquant ou majeur n'est ouvert sur la User Story.
- [ ] Les performances sont validées : temps de chargement conformes aux critères CAG-05.
- [ ] La gestion des erreurs est implémentée : messages d'erreur explicites en français, aucune stacktrace exposée à l'utilisateur.

### 9.3 Documentation

- [ ] La documentation API (Swagger/OpenAPI) est à jour pour chaque endpoint créé ou modifié.
- [ ] Le guide utilisateur est mis à jour avec les captures d'écran des nouvelles fonctionnalités.
- [ ] Les règles métier implémentées sont documentées dans le code (commentaires) et dans la documentation technique.

### 9.4 Déploiement

- [ ] La fonctionnalité est déployée sur l'environnement de staging et validée par le Product Owner.
- [ ] Les scripts de migration de données sont préparés et testés (si migration de données existantes).
- [ ] Le feature flag est configuré (si déploiement progressif).
- [ ] Les métriques de monitoring sont en place (temps de réponse, taux d'erreur, usage).

---

## 10. Dépendances

### 10.1 Dépendances entrantes (ce module dépend de)

| Module source | Nature de la dépendance | Impact | Criticité |
|---|---|---|---|
| **EPIC-002 Projets** | Liste des projets, phases, statuts. Le module Coûts impute chaque coût à un projet et optionnellement à une phase. | Bloquant : impossible de créer des factures ou budgets sans projets existants. | **Critique** |
| **EPIC-005 Temps** | Heures saisies par collaborateur et par projet. Le module Coûts utilise ces données pour calculer le coût de main d'oeuvre interne. | Bloquant pour le calcul du coût MO. Peut fonctionner en mode dégradé (sans coût MO) si le module Temps n'est pas encore livré. | **Haute** |
| **EPIC-013 Notes de frais** | Notes de frais individuelles des collaborateurs. Le module Coûts agrège ces données dans la vue consolidée. | Non bloquant : la vue Notes de frais consolidées sera vide tant que le module Notes de frais n'est pas opérationnel. | **Moyenne** |
| **Module Utilisateurs/RH** | Liste des collaborateurs, rôles, grades/niveaux. Nécessaire pour la gestion des salaires et les contrôles d'accès. | Bloquant pour la gestion des salaires. | **Haute** |

### 10.2 Dépendances sortantes (d'autres modules dépendent de ce module)

| Module cible | Nature de la dépendance | Impact |
|---|---|---|
| **EPIC-004 Facturation** | Le module Facturation utilise les données de coûts pour calculer la marge sur les factures émises et la rentabilité client. | Les calculs de marge seront incomplets sans les données de coûts. |
| **EPIC-008 Finances** | Le module Finances agrège les données de coûts dans les états financiers globaux (compte de résultat, bilan prévisionnel). | Les états financiers ne refléteront pas les charges sans le module Coûts. |
| **EPIC-002 Projets** | L'onglet Coûts de la fiche projet (vue synthétique) dépend des données calculées par ce module. | L'onglet Coûts sera vide ou incomplet sans ce module. |

### 10.3 Dépendances techniques

| Composant | Description | Statut |
|---|---|---|
| Service de stockage de fichiers | Pour l'upload des factures PDF, devis et pièces justificatives. S3 ou équivalent. | À confirmer |
| Service de notification | Pour les alertes (dépassement budget, échéances, factures en attente). Email et in-app. | Existant |
| Service d'export | Génération de fichiers CSV, XLSX, PDF. Bibliothèques : openpyxl (Excel), reportlab (PDF). | À développer |
| Service de permissions | Gestion fine des droits d'accès par rôle (confidentialité salariale). | Existant, à enrichir |

---

## 11. Modèle de Données

### 11.1 Entités principales

#### ExternalCompany (Entreprise Externe)

```
ExternalCompany {
    id                  : UUID, PK
    name                : VARCHAR(255), NOT NULL          -- Raison sociale
    type                : ENUM('subcontractor', 'co_contractor', 'supplier'), NOT NULL  -- Type
    siret               : VARCHAR(14), UNIQUE, NULLABLE   -- Numéro SIRET
    siren               : VARCHAR(9), NULLABLE            -- Numéro SIREN
    address_street      : VARCHAR(255)                    -- Adresse - Rue
    address_city        : VARCHAR(100)                    -- Adresse - Ville
    address_postal_code : VARCHAR(10)                     -- Adresse - Code postal
    address_country     : VARCHAR(100), DEFAULT 'France'  -- Adresse - Pays
    contact_name        : VARCHAR(255)                    -- Nom du contact principal
    contact_email       : VARCHAR(255)                    -- Email du contact
    contact_phone       : VARCHAR(20)                     -- Téléphone du contact
    iban                : VARCHAR(34), NULLABLE           -- IBAN
    bic                 : VARCHAR(11), NULLABLE           -- BIC/SWIFT
    specialty           : VARCHAR(255)[]                  -- Spécialités (structure, fluides, etc.)
    payment_delay_days  : INTEGER, DEFAULT 30             -- Délai de paiement par défaut (jours)
    payment_method      : ENUM('transfer', 'check', 'card'), DEFAULT 'transfer'
    notes               : TEXT                            -- Notes libres
    is_archived         : BOOLEAN, DEFAULT FALSE          -- Archivé (soft delete)
    organization_id     : UUID, FK -> Organization        -- Organisation propriétaire
    created_at          : TIMESTAMP, NOT NULL
    updated_at          : TIMESTAMP, NOT NULL
    created_by          : UUID, FK -> User
    updated_by          : UUID, FK -> User
}
```

#### SubcontractorContract (Contrat de sous-traitance)

```
SubcontractorContract {
    id                  : UUID, PK
    external_company_id : UUID, FK -> ExternalCompany, NOT NULL
    project_id          : UUID, FK -> Project, NOT NULL
    reference           : VARCHAR(100)                    -- Référence du contrat
    subject             : VARCHAR(500), NOT NULL          -- Objet du contrat
    contract_type       : ENUM('fixed_price', 'time_material', 'mixed'), NOT NULL
    amount              : DECIMAL(12,2), NOT NULL         -- Montant contractuel
    currency            : VARCHAR(3), DEFAULT 'EUR'
    start_date          : DATE, NOT NULL
    end_date            : DATE
    revision_conditions : TEXT                            -- Conditions de révision
    penalty_conditions  : TEXT                            -- Conditions de pénalités
    status              : ENUM('draft', 'active', 'completed', 'terminated', 'suspended'), DEFAULT 'draft'
    signed_document_url : VARCHAR(500)                    -- URL du contrat signé
    organization_id     : UUID, FK -> Organization
    created_at          : TIMESTAMP, NOT NULL
    updated_at          : TIMESTAMP, NOT NULL
    created_by          : UUID, FK -> User
    updated_by          : UUID, FK -> User
}
```

#### SupplierInvoice (Facture fournisseur)

```
SupplierInvoice {
    id                  : UUID, PK
    invoice_number      : VARCHAR(100), NOT NULL          -- Numéro de facture
    external_company_id : UUID, FK -> ExternalCompany, NOT NULL
    contract_id         : UUID, FK -> SubcontractorContract, NULLABLE
    invoice_date        : DATE, NOT NULL                  -- Date de la facture
    due_date            : DATE, NOT NULL                  -- Date d'échéance
    amount_ht           : DECIMAL(12,2), NOT NULL         -- Montant HT
    vat_rate            : DECIMAL(5,2), DEFAULT 20.00     -- Taux de TVA
    vat_amount          : DECIMAL(12,2), NOT NULL         -- Montant TVA
    amount_ttc          : DECIMAL(12,2), NOT NULL         -- Montant TTC
    currency            : VARCHAR(3), DEFAULT 'EUR'
    status              : ENUM('received', 'pending_validation', 'validated', 'pending_payment', 'paid', 'disputed'), DEFAULT 'received'
    payment_date        : DATE, NULLABLE                  -- Date de paiement effectif
    payment_reference   : VARCHAR(255), NULLABLE          -- Référence du paiement
    description         : TEXT                            -- Description / Objet
    document_url        : VARCHAR(500)                    -- URL du PDF de la facture
    organization_id     : UUID, FK -> Organization
    created_at          : TIMESTAMP, NOT NULL
    updated_at          : TIMESTAMP, NOT NULL
    created_by          : UUID, FK -> User
    updated_by          : UUID, FK -> User
    validated_by        : UUID, FK -> User, NULLABLE
    validated_at        : TIMESTAMP, NULLABLE

    UNIQUE(external_company_id, invoice_number)           -- Unicité par entreprise
}
```

#### InvoiceProjectAllocation (Imputation facture-projet)

```
InvoiceProjectAllocation {
    id                  : UUID, PK
    supplier_invoice_id : UUID, FK -> SupplierInvoice, NOT NULL
    project_id          : UUID, FK -> Project, NOT NULL
    phase_id            : UUID, FK -> ProjectPhase, NULLABLE
    amount              : DECIMAL(12,2), NOT NULL         -- Montant imputé
    percentage          : DECIMAL(5,2)                    -- Pourcentage de la facture
    created_at          : TIMESTAMP, NOT NULL
    updated_at          : TIMESTAMP, NOT NULL
}
```

#### Salary (Données salariales)

```
Salary {
    id                  : UUID, PK
    employee_id         : UUID, FK -> User, NOT NULL
    monthly_gross       : DECIMAL(10,2), NOT NULL         -- Salaire brut mensuel
    annual_gross        : DECIMAL(12,2), NOT NULL         -- Salaire brut annuel (calculé)
    charges_rate        : DECIMAL(5,2), NOT NULL          -- Taux de charges patronales (%)
    charges_amount      : DECIMAL(10,2), NOT NULL         -- Montant charges patronales mensuelles (calculé)
    total_employer_cost : DECIMAL(10,2), NOT NULL         -- Coût total employeur mensuel (calculé)
    contractual_hours   : INTEGER, DEFAULT 1820           -- Heures contractuelles annuelles
    productive_hours    : INTEGER                         -- Heures productives annuelles (calculé)
    hourly_rate         : DECIMAL(8,2), NOT NULL          -- Taux horaire réel (calculé)
    hourly_rate_full    : DECIMAL(8,2), NULLABLE          -- Taux horaire complet (avec frais de structure)
    grade               : ENUM('intern', 'junior', 'mid', 'senior', 'associate', 'partner')
    effective_date      : DATE, NOT NULL                  -- Date d'effet
    end_date            : DATE, NULLABLE                  -- Date de fin (si changement)
    is_current          : BOOLEAN, DEFAULT TRUE           -- Enregistrement courant
    organization_id     : UUID, FK -> Organization
    created_at          : TIMESTAMP, NOT NULL
    updated_at          : TIMESTAMP, NOT NULL
    created_by          : UUID, FK -> User
}
```

#### GeneralExpense (Frais généraux)

```
GeneralExpense {
    id                  : UUID, PK
    category            : ENUM('rent', 'charges', 'insurance_decennial', 'insurance_professional',
                               'insurance_multi', 'software_licenses', 'telecom', 'office_supplies',
                               'maintenance', 'training', 'accounting_fees', 'legal_fees', 'other'), NOT NULL
    description         : VARCHAR(500), NOT NULL
    amount_ht           : DECIMAL(10,2), NOT NULL
    vat_rate            : DECIMAL(5,2), DEFAULT 20.00
    vat_amount          : DECIMAL(10,2)
    amount_ttc          : DECIMAL(10,2), NOT NULL
    expense_date        : DATE, NOT NULL
    supplier_name       : VARCHAR(255), NULLABLE          -- Fournisseur (texte libre ou lien)
    external_company_id : UUID, FK -> ExternalCompany, NULLABLE
    is_recurring        : BOOLEAN, DEFAULT FALSE
    recurrence_type     : ENUM('monthly', 'quarterly', 'semi_annual', 'annual'), NULLABLE
    recurrence_end_date : DATE, NULLABLE
    recurrence_parent_id: UUID, FK -> GeneralExpense, NULLABLE  -- Lien vers l'écriture mère
    document_url        : VARCHAR(500)                    -- Pièce justificative
    accounting_code     : VARCHAR(20), NULLABLE           -- Code comptable (PCG)
    organization_id     : UUID, FK -> Organization
    created_at          : TIMESTAMP, NOT NULL
    updated_at          : TIMESTAMP, NOT NULL
    created_by          : UUID, FK -> User
}
```

#### CostBudget (Budget prévisionnel)

```
CostBudget {
    id                  : UUID, PK
    project_id          : UUID, FK -> Project, NOT NULL
    version             : INTEGER, DEFAULT 1              -- Version du budget
    is_current          : BOOLEAN, DEFAULT TRUE           -- Version courante
    revision_reason     : TEXT, NULLABLE                  -- Motif de la révision
    total_planned       : DECIMAL(12,2), NOT NULL         -- Total budget prévu
    total_actual        : DECIMAL(12,2), DEFAULT 0        -- Total coûts réels (calculé)
    status              : ENUM('draft', 'approved', 'revised', 'closed'), DEFAULT 'draft'
    approved_by         : UUID, FK -> User, NULLABLE
    approved_at         : TIMESTAMP, NULLABLE
    organization_id     : UUID, FK -> Organization
    created_at          : TIMESTAMP, NOT NULL
    updated_at          : TIMESTAMP, NOT NULL
    created_by          : UUID, FK -> User
}
```

#### CostBudgetLine (Ligne de budget)

```
CostBudgetLine {
    id                  : UUID, PK
    cost_budget_id      : UUID, FK -> CostBudget, NOT NULL
    category            : ENUM('labor', 'subcontracting', 'direct_expenses', 'general_expenses'), NOT NULL
    sub_category        : VARCHAR(100), NULLABLE          -- Sous-catégorie (ex: structure, fluides...)
    phase_id            : UUID, FK -> ProjectPhase, NULLABLE
    planned_amount      : DECIMAL(12,2), NOT NULL         -- Montant prévu
    actual_amount       : DECIMAL(12,2), DEFAULT 0        -- Montant réel (calculé)
    planned_hours       : DECIMAL(8,2), NULLABLE          -- Heures prévues (catégorie labor)
    actual_hours        : DECIMAL(8,2), NULLABLE          -- Heures réelles (calculé, catégorie labor)
    notes               : TEXT
    created_at          : TIMESTAMP, NOT NULL
    updated_at          : TIMESTAMP, NOT NULL
}
```

#### SupplierQuote (Devis fournisseur)

```
SupplierQuote {
    id                  : UUID, PK
    external_company_id : UUID, FK -> ExternalCompany, NOT NULL
    project_id          : UUID, FK -> Project, NOT NULL
    phase_id            : UUID, FK -> ProjectPhase, NULLABLE
    reference           : VARCHAR(100)                    -- Référence du devis
    quote_date          : DATE, NOT NULL                  -- Date du devis
    validity_date       : DATE                            -- Date de validité
    subject             : VARCHAR(500), NOT NULL          -- Objet
    amount_ht           : DECIMAL(12,2), NOT NULL
    vat_rate            : DECIMAL(5,2), DEFAULT 20.00
    amount_ttc          : DECIMAL(12,2), NOT NULL
    currency            : VARCHAR(3), DEFAULT 'EUR'
    status              : ENUM('received', 'shortlisted', 'accepted', 'rejected'), DEFAULT 'received'
    comparison_group_id : UUID, NULLABLE                  -- Groupe de comparaison (même besoin)
    document_url        : VARCHAR(500)                    -- PDF du devis
    contract_id         : UUID, FK -> SubcontractorContract, NULLABLE  -- Contrat généré
    notes               : TEXT
    organization_id     : UUID, FK -> Organization
    created_at          : TIMESTAMP, NOT NULL
    updated_at          : TIMESTAMP, NOT NULL
    created_by          : UUID, FK -> User
    validated_by        : UUID, FK -> User, NULLABLE
    validated_at        : TIMESTAMP, NULLABLE
}
```

#### SupplierQuoteLine (Ligne de devis fournisseur)

```
SupplierQuoteLine {
    id                  : UUID, PK
    supplier_quote_id   : UUID, FK -> SupplierQuote, NOT NULL
    designation         : VARCHAR(500), NOT NULL          -- Désignation
    quantity            : DECIMAL(10,2), DEFAULT 1
    unit                : VARCHAR(50), NULLABLE           -- Unité (forfait, jour, heure, m², etc.)
    unit_price          : DECIMAL(10,2), NOT NULL         -- Prix unitaire HT
    amount              : DECIMAL(12,2), NOT NULL         -- Montant ligne HT
    sort_order          : INTEGER, DEFAULT 0
    created_at          : TIMESTAMP, NOT NULL
    updated_at          : TIMESTAMP, NOT NULL
}
```

#### BillingSchedule (Planning de facturation sous-traitant)

```
BillingSchedule {
    id                  : UUID, PK
    contract_id         : UUID, FK -> SubcontractorContract, NOT NULL
    project_id          : UUID, FK -> Project, NOT NULL
    phase_id            : UUID, FK -> ProjectPhase, NULLABLE
    scheduled_date      : DATE, NOT NULL                  -- Date prévue
    description         : VARCHAR(500), NOT NULL          -- Objet (ex: "Acompte 30%")
    planned_amount      : DECIMAL(12,2), NOT NULL         -- Montant prévu
    supplier_invoice_id : UUID, FK -> SupplierInvoice, NULLABLE  -- Facture rapprochée
    actual_amount       : DECIMAL(12,2), NULLABLE         -- Montant réel (facture)
    status              : ENUM('upcoming', 'due', 'invoice_received', 'validated', 'paid', 'overdue'), DEFAULT 'upcoming'
    organization_id     : UUID, FK -> Organization
    created_at          : TIMESTAMP, NOT NULL
    updated_at          : TIMESTAMP, NOT NULL
    created_by          : UUID, FK -> User
}
```

#### CostExportHistory (Historique des exports)

```
CostExportHistory {
    id                  : UUID, PK
    export_format       : ENUM('fec', 'csv', 'xlsx', 'pdf'), NOT NULL
    date_from           : DATE, NOT NULL                  -- Période début
    date_to             : DATE, NOT NULL                  -- Période fin
    filters_applied     : JSONB                           -- Filtres appliqués (sérialisés)
    line_count          : INTEGER, NOT NULL                -- Nombre de lignes
    total_amount        : DECIMAL(14,2)                   -- Montant total
    file_url            : VARCHAR(500)                    -- Lien de téléchargement
    file_expiry_date    : DATE                            -- Date d'expiration du fichier
    organization_id     : UUID, FK -> Organization
    created_at          : TIMESTAMP, NOT NULL
    created_by          : UUID, FK -> User
}
```

### 11.2 Diagramme relationnel simplifié

```
┌──────────────────┐       ┌─────────────────────────┐
│ ExternalCompany  │──1:N──│ SubcontractorContract    │
│                  │       │                          │──1:N──┐
│                  │──1:N──│                          │       │
└──────────────────┘       └─────────────────────────┘       │
        │                           │                         │
        │ 1:N                       │ 0:1                     │
        ▼                           ▼                         ▼
┌──────────────────┐       ┌─────────────────┐    ┌──────────────────────┐
│ SupplierInvoice  │       │ SupplierQuote   │    │ BillingSchedule      │
│                  │       │                 │    │                      │
│                  │──1:N──┤                 │    │                      │
└──────────────────┘       └─────────────────┘    └──────────────────────┘
        │                           │
        │ 1:N                       │ 1:N
        ▼                           ▼
┌───────────────────────┐  ┌─────────────────────┐
│InvoiceProjectAllocation│  │ SupplierQuoteLine   │
│                       │  │                     │
└───────────────────────┘  └─────────────────────┘
        │
        │ N:1
        ▼
┌──────────────────┐       ┌─────────────────┐
│ Project          │──1:N──│ CostBudget      │──1:N──┐
│ (EPIC-002)       │       │                 │       │
└──────────────────┘       └─────────────────┘       │
                                                      ▼
                                              ┌─────────────────┐
                                              │ CostBudgetLine  │
                                              │                 │
                                              └─────────────────┘

┌──────────────────┐       ┌─────────────────────┐
│ User / Employee  │──1:N──│ Salary              │
│ (Module RH)      │       │                     │
└──────────────────┘       └─────────────────────┘

┌──────────────────────┐   ┌─────────────────────┐
│ GeneralExpense       │   │ CostExportHistory   │
│                      │   │                     │
└──────────────────────┘   └─────────────────────┘
```

---

## 12. Estimation & Découpage

### 12.1 Estimation globale

| Métrique | Valeur |
|---|---|
| **Durée estimée** | 7 à 9 semaines |
| **Nombre de sprints** | 4 à 5 sprints (sprints de 2 semaines) |
| **Effort estimé** | 280 à 360 points d'effort (story points) |
| **Équipe recommandée** | 2 développeurs backend, 1 développeur frontend, 1 QA, 1 Product Owner (temps partiel) |

### 12.2 Découpage en sprints

#### Sprint 1 — Fondations et Entreprises Externes (Semaines 1-2)

| User Story | Effort (SP) | Priorité | Détail |
|---|---|---|---|
| **US-C02** — Gestion des entreprises externes | 21 | Haute | CRUD complet, annuaire, fiche entreprise, documents, spécialités |
| Infrastructure technique | 13 | Haute | Mise en place des modèles de données (ExternalCompany, SubcontractorContract), API REST, permissions par rôle |
| Contrats de sous-traitance | 8 | Haute | Création/édition de contrats, rattachement projet, échéancier |
| **Total Sprint 1** | **42** | | |

**Objectif du sprint** : L'annuaire des entreprises externes est opérationnel. Les contrats de sous-traitance peuvent être créés et rattachés aux projets.

**Livrables** :
- API CRUD ExternalCompany avec filtres et pagination
- API CRUD SubcontractorContract
- Interface utilisateur : liste des entreprises, fiche détaillée avec onglets, formulaire de création/édition
- Upload de documents administratifs (Kbis, assurances)
- Tests unitaires et d'intégration

---

#### Sprint 2 — Factures Fournisseurs et Devis (Semaines 3-4)

| User Story | Effort (SP) | Priorité | Détail |
|---|---|---|---|
| **US-C03** — Création/édition facture fournisseur | 21 | Haute | CRUD factures, workflow de validation, imputation multi-projet, pièces jointes |
| **US-C10** — Devis fournisseurs | 13 | Moyenne | Enregistrement, comparaison, validation, transformation en contrat |
| **US-C09** — Planning de facturation sous-traitants | 13 | Moyenne | Échéancier, rapprochement avec factures, alertes |
| **Total Sprint 2** | **47** | | |

**Objectif du sprint** : Le cycle de vie complet d'une facture fournisseur est fonctionnel (réception, validation, paiement). Les devis peuvent être comparés et validés. Le planning de facturation sous-traitants est opérationnel.

**Livrables** :
- API CRUD SupplierInvoice avec workflow de statuts
- API InvoiceProjectAllocation (ventilation multi-projet)
- API CRUD SupplierQuote et SupplierQuoteLine
- API CRUD BillingSchedule
- Interface utilisateur : liste des factures avec filtres, formulaire de saisie, workflow de validation, tableau comparatif des devis, timeline de facturation
- Notifications automatiques (échéances, validations)
- Tests unitaires, d'intégration et E2E

---

#### Sprint 3 — Salaires, Frais Généraux et Coûts Projet (Semaines 5-6)

| User Story | Effort (SP) | Priorité | Détail |
|---|---|---|---|
| **US-C05** — Gestion des salaires et taux horaires | 21 | Haute | Saisie salaires, calcul taux horaire, masse salariale, simulation, confidentialité |
| **US-C06** — Gestion des frais généraux | 13 | Haute | CRUD frais généraux, récurrence, catégories, répartition |
| **US-C08** — Coûts par projet (vue projet) | 13 | Haute | Synthèse coûts projet, ventilation par catégorie/phase, intégration EPIC-005 |
| **Total Sprint 3** | **47** | | |

**Objectif du sprint** : La masse salariale est gérée avec calcul automatique des taux horaires. Les frais généraux sont saisis et catégorisés. L'onglet Coûts de la fiche projet affiche les données consolidées.

**Livrables** :
- API CRUD Salary avec historisation et calcul automatique du taux horaire
- API CRUD GeneralExpense avec gestion de la récurrence
- API de calcul des coûts projet (agrégation MO + sous-traitance + frais directs + frais généraux)
- Interface utilisateur : gestion des salaires (accès restreint), gestion des frais généraux, onglet Coûts dans la fiche projet
- Intégration avec EPIC-005 (récupération des heures saisies)
- Tests unitaires, d'intégration et E2E

---

#### Sprint 4 — Budget vs Réel, Notes de Frais, Tableau de Bord (Semaines 7-8)

| User Story | Effort (SP) | Priorité | Détail |
|---|---|---|---|
| **US-C11** — Budget prévisionnel vs réel | 21 | Haute | Matrice budget, calcul écarts, alertes seuils, versionnement, projections |
| **US-C04** — Notes de frais consolidées | 8 | Moyenne | Vue agrégée, filtres, totaux, intégration EPIC-013 |
| **US-C01** — Vue résumé des coûts agence | 21 | Haute | Tableau de bord KPIs, graphiques, alertes, filtres |
| **Total Sprint 4** | **50** | | |

**Objectif du sprint** : Le budget prévisionnel est géré avec comparaison temps réel. La vue consolidée des notes de frais est fonctionnelle. Le tableau de bord agence offre une vision synthétique de tous les coûts.

**Livrables** :
- API CRUD CostBudget et CostBudgetLine avec versionnement
- API de calcul budget vs réel avec alertes configurables
- API d'agrégation des notes de frais (intégration EPIC-013)
- API du tableau de bord (KPIs, graphiques)
- Interface utilisateur : gestion du budget avec matrice catégorie × phase, graphique courbe en S, vue consolidée des notes de frais, tableau de bord agence avec graphiques interactifs
- Tests unitaires, d'intégration et E2E

---

#### Sprint 5 — Exports, Polissage et Stabilisation (Semaines 8-9)

| User Story | Effort (SP) | Priorité | Détail |
|---|---|---|---|
| **US-C07** — Exports comptables des coûts | 21 | Haute | Export FEC, CSV, XLSX, PDF, programmation, historique |
| Polissage UX et corrections | 8 | Moyenne | Retours QA et PO, ajustements d'interface, messages d'erreur |
| Tests de performance et sécurité | 8 | Haute | Volumétrie, temps de réponse, audit confidentialité salariale |
| Documentation | 5 | Moyenne | Documentation API, guide utilisateur, documentation technique |
| **Total Sprint 5** | **42** | | |

**Objectif du sprint** : Les exports comptables sont fonctionnels et conformes. Le module est stabilisé, performant et documenté. Le passage en production est validé.

**Livrables** :
- Service d'export multi-format (FEC, CSV, XLSX, PDF)
- API CostExportHistory avec programmation récurrente
- Prévisualisation des exports
- Détection d'anomalies pré-export
- Corrections de bugs et améliorations UX issues des retours QA/PO
- Rapport de tests de performance (conformité CAG-05)
- Audit de sécurité (confidentialité des données salariales)
- Documentation API (Swagger), guide utilisateur, documentation technique

---

### 12.3 Récapitulatif des efforts

| Sprint | Semaines | Story Points | User Stories couvertes |
|---|---|---|---|
| Sprint 1 | S1-S2 | 42 | US-C02 (entreprises externes) |
| Sprint 2 | S3-S4 | 47 | US-C03 (factures), US-C10 (devis), US-C09 (planning) |
| Sprint 3 | S5-S6 | 47 | US-C05 (salaires), US-C06 (frais généraux), US-C08 (coûts projet) |
| Sprint 4 | S7-S8 | 50 | US-C11 (budget vs réel), US-C04 (notes de frais), US-C01 (résumé) |
| Sprint 5 | S8-S9 | 42 | US-C07 (exports), stabilisation, documentation |
| **Total** | **9 semaines** | **228 SP** | **11 User Stories** |

### 12.4 Risques et mitigations

| # | Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|---|
| R1 | Retard EPIC-002 Projets (dépendance bloquante) | Moyenne | Élevé | Prévoir des données de test mockées. Développer les API indépendamment et intégrer dès que EPIC-002 est disponible. |
| R2 | Complexité du format FEC | Moyenne | Moyen | Prévoir une analyse technique approfondie en début de Sprint 5. Solliciter l'expertise d'un comptable pour valider la conformité. |
| R3 | Confidentialité des données salariales | Faible | Élevé | Implémenter le contrôle d'accès dès le Sprint 3 (pas en post-livraison). Tests de pénétration dédiés. |
| R4 | Performance du tableau de bord (agrégation de données volumineuses) | Moyenne | Moyen | Mettre en place des vues matérialisées ou un cache pour les KPIs. Requêtes optimisées avec index appropriés. |
| R5 | Intégration avec EPIC-005 Temps (calcul coût MO) | Faible | Moyen | Prévoir un mode dégradé sans les heures, avec possibilité de saisie manuelle du coût MO en attendant l'intégration. |
| R6 | Scope creep sur les règles métier comptables | Haute | Moyen | Cadrer strictement le périmètre V1 (pas de multi-devise, pas d'OCR, pas d'intégration comptable directe). |

### 12.5 Critères de lancement en production

- [ ] 100 % des critères d'acceptance des 11 User Stories sont validés.
- [ ] 0 bug bloquant, 0 bug majeur ouvert.
- [ ] Couverture de tests > 80 % sur le code métier.
- [ ] Tests de performance validés (CAG-05).
- [ ] Audit de sécurité validé (confidentialité salariale, permissions).
- [ ] Export FEC validé par un expert-comptable.
- [ ] Documentation utilisateur et API complète.
- [ ] Formation des utilisateurs pilotes réalisée.
- [ ] Données de migration préparées et testées (si migration depuis un système existant).

---

*Document rédigé le 26 février 2026 — Version 1.0*
*EPIC-007 Module Coûts — Application OOTI*
