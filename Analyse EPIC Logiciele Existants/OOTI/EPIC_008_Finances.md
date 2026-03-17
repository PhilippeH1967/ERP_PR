# EPIC — Module Finances

**Application OOTI — Gestion de projets pour cabinets d'architecture**
**Version 1.0 — Fevrier 2026**

---

## 1. Identification de l'EPIC

| Champ | Valeur |
|---|---|
| **Nom de l'EPIC** | Finances |
| **Reference** | EPIC-008 |
| **Module parent** | Gestion |
| **Priorite** | Moyenne |
| **Statut** | A planifier |
| **Date de creation** | Fevrier 2026 |
| **Auteur** | -- |
| **EPICs lies** | EPIC-002 (Projets), EPIC-003 (Honoraires), EPIC-004 (Facturation), EPIC-007 (Couts), EPIC-011 (Rapports) |

---

## 2. Contexte & Problematique

Dans un cabinet d'architecture, le pilotage financier est un enjeu strategique majeur. Les dirigeants et chefs de projet doivent pouvoir suivre en temps reel la sante financiere de l'agence et de chaque projet individuellement : chiffre d'affaires realise et projete, couts cumules (salaires, sous-traitants, frais generaux), et marge nette. Cette visibilite est indispensable pour prendre des decisions eclairees sur l'allocation des ressources, la negociation des honoraires futurs et l'identification des projets non rentables.

Sans outil centralise, les cabinets recourent a des tableaux Excel disparates, consolides manuellement en fin de mois ou de trimestre. Ce processus est chronophage, source d'erreurs, et ne permet pas une vision en temps reel. Les donnees financieres sont eclatees entre la comptabilite, les feuilles de temps, les factures et les contrats de sous-traitance, rendant extremement difficile le calcul precis de la marge par projet. Les directeurs d'agence ne disposent pas d'une vue synthetique leur permettant de comparer la performance financiere entre projets, entre annees ou entre entites.

Le module Finances de OOTI vise a resoudre ces problematiques en consolidant automatiquement les donnees issues des modules Honoraires, Facturation, Temps et Couts pour produire des tableaux de bord financiers dynamiques, des graphiques de suivi et des indicateurs de rentabilite actionables.

---

## 3. Objectif de l'EPIC

Permettre aux utilisateurs de OOTI de consulter et analyser la performance financiere globale de l'agence et de chaque projet via un module dedie (GESTION > Finances), offrant quatre vues complementaires (Resume, Chiffre d'affaires, Couts, Marge) ainsi qu'une vue Finance au niveau de chaque projet (onglet FINANCE). Le module doit permettre de basculer entre les modes Realise et Projete, d'inclure ou exclure les couts fixes, de filtrer par annee, projet et entite, et d'exporter les donnees financieres pour une exploitation externe.

---

## 4. Perimetre Fonctionnel

### 4.1 Vues globales Agence (GESTION > Finances)

- **Resume financier** : tableau de bord synthetique avec KPIs financiers cles (CA annuel, couts totaux, marge globale, nombre de projets rentables/deficitaires)
- **Chiffre d'affaires** : vue detaillee du CA par projet, par mois, par annee, avec distinction facturable vs facture vs paye
- **Couts** : vue consolidee de tous les couts (salaires, sous-traitants, frais generaux) ventiles par projet
- **Marge** : vue de la marge (CA - Couts) par projet, par annee, en mode realise et projete

### 4.2 Vue Finance d'un projet (onglet FINANCE)

- Graphique a barres Chiffre d'affaires / Couts par annee
- Courbe Marge planifiee cumulee superposee au graphique
- Tableau Marge par annee : CA, Salaires, Couts, Marge
- Toggle Realise / Projete
- Toggle Afficher couts fixes
- Filtre par annee

### 4.3 Fonctionnalites transversales

- Filtrage multi-criteres (annee, projet, entite)
- Export des donnees financieres (CSV, Excel)
- Indicateurs de rentabilite par projet (marge en %, seuils d'alerte)
- Graphiques interactifs (barres, courbes, camemberts)

---

## 5. User Stories

### US-FI01 — Synthese financiere globale de l'agence

**En tant que** Directeur d'agence / Responsable financier
**Je veux** acceder a un tableau de bord synthetique de la performance financiere globale de mon agence
**Afin de** visualiser en un coup d'oeil les indicateurs cles (CA, couts, marge) et detecter rapidement les tendances positives ou negatives

**Criteres d'acceptance :**

1. Le tableau de bord est accessible via le menu lateral GESTION > Finances > Resume
2. Les KPIs suivants sont affiches en haut de page sous forme de cartes : Chiffre d'affaires annuel (realise et projete), Couts totaux annuels, Marge globale (montant et pourcentage), Nombre de projets rentables vs deficitaires
3. Un graphique a barres affiche la comparaison CA vs Couts par mois pour l'annee en cours
4. Une courbe de marge cumulee est superposee au graphique a barres
5. Un tableau recapitulatif liste les projets avec leur CA, leurs couts et leur marge, tries par marge decroissante
6. Un filtre par annee permet de basculer entre les exercices fiscaux
7. Un filtre par entite permet de restreindre la vue a une agence/entite specifique
8. Les donnees sont rafraichies automatiquement a chaque acces a la page (donnees en temps reel)

---

### US-FI02 — Vue Chiffre d'affaires

**En tant que** Directeur d'agence / Chef de projet
**Je veux** consulter une vue detaillee du chiffre d'affaires de l'agence
**Afin de** analyser les revenus par projet, par mois et par annee, et comprendre l'ecart entre le CA facturable, facture et paye

**Criteres d'acceptance :**

1. La vue est accessible via le menu GESTION > Finances > Chiffre d'affaires
2. Un tableau affiche par projet : le nom du projet, le CA total planifie (honoraires signes), le CA facturable (avancement x honoraires), le CA facture (factures emises HT), le CA paye (paiements recus HT)
3. Une ligne de total en pied de tableau somme toutes les colonnes
4. Un graphique a barres groupees permet de visualiser par mois les trois montants (facturable, facture, paye)
5. Un filtre par annee permet de selectionner l'exercice fiscal
6. Un filtre par projet permet de cibler un ou plusieurs projets specifiques
7. Un indicateur d'ecart (%) entre CA facturable et CA facture est affiche par projet pour identifier les retards de facturation
8. Le bouton ACTIONS permet l'export des donnees en CSV et Excel

---

### US-FI03 — Vue Couts consolides

**En tant que** Directeur d'agence / Responsable financier
**Je veux** consulter une vue consolidee de tous les couts de l'agence, ventiles par categorie et par projet
**Afin de** comprendre la structure de couts, identifier les postes les plus importants et controler les depenses

**Criteres d'acceptance :**

1. La vue est accessible via le menu GESTION > Finances > Couts
2. Le tableau affiche par projet : le nom du projet, les couts salariaux (temps x taux horaire), les couts de sous-traitance (factures sous-traitants), les frais generaux imputes, le total des couts
3. Trois cartes KPI en haut de page affichent : Total salaires, Total sous-traitants, Total frais generaux
4. Un graphique a barres empilees visualise la repartition des couts par categorie pour chaque projet
5. Un toggle "Afficher couts fixes" permet d'inclure ou d'exclure les frais generaux (loyer, assurances, charges fixes) du calcul
6. Un filtre par annee permet de selectionner la periode
7. Un filtre par entite permet de restreindre la vue a une agence specifique
8. Le bouton ACTIONS permet l'export des donnees en CSV et Excel

---

### US-FI04 — Vue Marge globale

**En tant que** Directeur d'agence / Responsable financier
**Je veux** consulter la marge de chaque projet et de l'agence dans son ensemble
**Afin de** identifier les projets rentables, les projets deficitaires et piloter la performance economique globale

**Criteres d'acceptance :**

1. La vue est accessible via le menu GESTION > Finances > Marge
2. Le tableau affiche par projet : le nom du projet, le chiffre d'affaires, les couts totaux, la marge en valeur absolue (EUR), la marge en pourcentage (%)
3. Un code couleur indique le niveau de marge : vert (marge > 20%), orange (marge entre 0% et 20%), rouge (marge negative)
4. Un graphique a barres horizontales compare la marge de chaque projet, trie par marge decroissante
5. Deux modes d'affichage sont disponibles : REALISE (calcule sur les donnees reelles : CA facture, couts constates) et PROJETE (calcule sur les previsions : CA planifie, couts estimes)
6. Une ligne de total affiche la marge globale de l'agence
7. Un filtre par annee et par entite est disponible
8. Le bouton ACTIONS permet l'export des donnees en CSV et Excel

---

### US-FI05 — Finance d'un projet (vue projet)

**En tant que** Chef de projet / Directeur d'agence
**Je veux** visualiser la performance financiere detaillee d'un projet specifique depuis l'onglet FINANCE du projet
**Afin de** analyser la marge realisee et projetee, le chiffre d'affaires et les couts de ce projet annee par annee

**Criteres d'acceptance :**

1. L'onglet FINANCE est accessible depuis la vue detaillee d'un projet (barre d'onglets du projet)
2. Un graphique a barres affiche le Chiffre d'affaires (barre bleue) et les Couts (barre rouge) par annee sur toute la duree du projet
3. Une courbe Marge planifiee cumulee (ligne continue) est superposee au graphique a barres
4. Sous le graphique, un tableau "Marge (EUR)" liste par annee les colonnes : Annee, Chiffre d'affaires, Salaires, Couts (sous-traitants + frais generaux), Marge (CA - Salaires - Couts)
5. Une ligne de total en pied de tableau affiche les sommes de chaque colonne
6. Le graphique et le tableau se mettent a jour dynamiquement lors du changement de mode ou de filtre
7. La devise affichee est celle du projet (heritee de la configuration du projet)
8. Le bouton ACTIONS permet d'exporter les donnees du graphique et du tableau

---

### US-FI06 — Mode Realise vs Projete

**En tant que** Chef de projet / Directeur d'agence
**Je veux** basculer entre le mode Realise et le mode Projete sur toutes les vues financieres
**Afin de** comparer la performance financiere reelle avec les previsions et detecter les ecarts

**Criteres d'acceptance :**

1. Deux boutons (toggle ou onglets) "REALISE" et "PROJETE" sont affiches en haut de chaque vue financiere (Resume, CA, Couts, Marge, Finance projet)
2. En mode REALISE, les donnees affichees sont : CA = montant des factures emises (HT), Couts = salaires constates (temps x taux) + factures sous-traitants payees + frais generaux imputes
3. En mode PROJETE, les donnees affichees sont : CA = honoraires planifies x avancement prevu, Couts = budget previsionnel salaires + budget previsionnel sous-traitants + estimation frais generaux
4. Le basculement entre les deux modes est instantane (< 1 seconde) sans rechargement de page
5. Le mode selectionne est conserve lors de la navigation entre les sous-menus (Resume, CA, Couts, Marge)
6. Un indicateur visuel clair (couleur, icone ou badge) indique le mode actif en permanence

---

### US-FI07 — Filtrage et selection de periode

**En tant que** Chef de projet / Directeur d'agence
**Je veux** filtrer les donnees financieres par annee, par projet et par entite
**Afin de** cibler mon analyse sur une periode, un perimetre ou un projet specifique

**Criteres d'acceptance :**

1. Un selecteur d'annee est present sur toutes les vues financieres avec les options : "Toutes les annees" et chaque annee fiscale disponible (ex : 2024, 2025, 2026)
2. Un selecteur de projet est present sur les vues globales (Resume, CA, Couts, Marge) permettant de filtrer sur un ou plusieurs projets
3. Un selecteur d'entite est present pour les agences multi-entites, permettant de restreindre la vue a une entite specifique
4. Les filtres sont cumulables : il est possible de filtrer par annee ET par entite simultanement
5. La modification d'un filtre met a jour instantanement les donnees, graphiques et tableaux affiches
6. Les filtres selectionnes sont affiches de maniere visible (badges ou chips) et peuvent etre supprimes individuellement
7. Un bouton "Reinitialiser les filtres" remet tous les filtres a leur valeur par defaut
8. Sur la vue Finance d'un projet (onglet FINANCE), seul le filtre par annee est disponible (le projet est deja selectionne)

---

### US-FI08 — Export des donnees financieres

**En tant que** Directeur d'agence / Responsable financier / Comptable
**Je veux** exporter les donnees financieres affichees dans un fichier exploitable
**Afin de** les integrer dans mes outils de comptabilite, les partager avec mon expert-comptable ou les archiver

**Criteres d'acceptance :**

1. Un bouton ACTIONS > Exporter est present sur chaque vue financiere (Resume, CA, Couts, Marge, Finance projet)
2. Les formats d'export disponibles sont : CSV (separateur point-virgule) et Excel (.xlsx)
3. L'export respecte les filtres actifs : seules les donnees filtrees sont exportees
4. L'export inclut les colonnes visibles du tableau avec les en-tetes en francais
5. Le fichier exporte contient une ligne d'en-tete avec les noms des colonnes et une ligne de total en pied
6. Le nom du fichier genere inclut le type de vue, la periode et la date d'export (ex : "Marge_2025_export_2026-02-26.xlsx")
7. L'export se declenche en moins de 5 secondes pour un volume de 100 projets
8. Un message de confirmation indique que l'export a ete telecharge avec succes

---

### US-FI09 — Indicateurs de rentabilite par projet

**En tant que** Directeur d'agence / Chef de projet
**Je veux** visualiser des indicateurs de rentabilite synthetiques pour chaque projet
**Afin de** identifier immediatement les projets qui necessitent une attention particuliere (marge faible ou negative)

**Criteres d'acceptance :**

1. Chaque projet affiche un indicateur de marge en pourcentage (%) dans les tableaux financiers
2. Un code couleur est applique automatiquement : vert si marge >= 20%, orange si marge entre 0% et 20%, rouge si marge < 0%
3. Une icone d'alerte (triangle) est affichee a cote des projets dont la marge realisee est inferieure de plus de 10 points a la marge projetee
4. Le tableau de bord Resume affiche le nombre total de projets rentables (marge > 0%) et deficitaires (marge <= 0%)
5. Un tri par marge (croissante ou decroissante) est disponible dans tous les tableaux financiers
6. Les seuils de rentabilite (20% et 0%) sont configurables dans les parametres financiers de l'entite
7. Un tooltip au survol de l'indicateur affiche le detail : CA, Couts, Marge en valeur et en pourcentage

---

### US-FI10 — Graphiques et visualisations financieres

**En tant que** Directeur d'agence / Chef de projet
**Je veux** disposer de graphiques interactifs pour visualiser les donnees financieres
**Afin de** comprendre rapidement les tendances, les repartitions et les evolutions financieres sans lire des tableaux de chiffres

**Criteres d'acceptance :**

1. Le graphique a barres groupees (CA vs Couts) est affiche sur la vue Resume et sur l'onglet Finance projet, avec une barre par annee (ou par mois selon la granularite selectionnee)
2. La courbe de marge cumulee est superposee au graphique a barres avec un axe Y secondaire
3. Un graphique a barres empilees est disponible sur la vue Couts pour visualiser la repartition des couts par categorie (salaires, sous-traitants, frais generaux)
4. Un graphique a barres horizontales est disponible sur la vue Marge pour comparer les marges entre projets
5. Les graphiques sont interactifs : le survol d'un element affiche un tooltip avec les valeurs detaillees
6. Les graphiques sont redimensionnables et s'adaptent a la taille de l'ecran (responsive)
7. Une legende cliquable permet d'afficher/masquer les series de donnees individuellement
8. Les graphiques utilisent les couleurs standards de l'application : bleu pour le CA, rouge/orange pour les couts, vert pour la marge positive, rouge pour la marge negative

---

## 6. Hors Perimetre (Out of Scope)

- Saisie et modification des honoraires d'un projet (couvert par EPIC-003 -- Honoraires)
- Emission, modification et envoi des factures (couvert par EPIC-004 -- Facturation)
- Saisie des temps par les collaborateurs (couvert par EPIC-005 -- Temps)
- Gestion du planning et de l'avancement des phases (couvert par EPIC-006 -- Planning)
- Saisie et configuration des couts (salaires, sous-traitants, frais generaux) (couvert par EPIC-007 -- Couts)
- Rapports cross-entites et rapports avances (couvert par EPIC-011 -- Rapports)
- Comptabilite generale (grand livre, bilan, compte de resultat) -- hors perimetre applicatif
- Gestion de la tresorerie et previsions de cash-flow -- hors perimetre applicatif
- Connexion avec un logiciel de comptabilite externe (Sage, QuickBooks, etc.) -- hors perimetre V1

---

## 7. Regles Metier

1. **Marge = Chiffre d'affaires - Couts totaux**, ou Couts totaux = Salaires + Sous-traitants + Frais generaux (si couts fixes actives)
2. **Le chiffre d'affaires realise** correspond au montant total HT des factures emises sur la periode, tel que calcule par le module Facturation (EPIC-004)
3. **Le chiffre d'affaires projete** correspond aux honoraires signes (EPIC-003) ponderes par l'avancement previsionnel des phases
4. **Les couts salariaux** sont calcules a partir des temps saisis (EPIC-005) multiplies par le taux horaire de chaque collaborateur (configure dans EPIC-007)
5. **Les couts de sous-traitance** correspondent aux factures sous-traitants enregistrees dans le module Couts (EPIC-007)
6. **Les frais generaux** sont repartis au prorata du temps passe sur chaque projet par rapport au temps total de l'agence, sauf configuration specifique
7. **Les couts fixes** (loyer, assurances, charges) sont optionnels et actives/desactives via le toggle "Afficher couts fixes"
8. **La devise** de chaque projet est heritee de la configuration du projet et ne peut pas etre modifiee dans le module Finances
9. **L'annee fiscale** est configurable par entite (par defaut : janvier a decembre) via les parametres financiers
10. **Les donnees financieres sont en lecture seule** dans le module Finances : aucune saisie directe n'est possible, toutes les donnees proviennent des modules sources (Honoraires, Facturation, Temps, Couts)
11. **Un projet sans honoraires definis** affiche un CA planifie de 0 et une marge basee uniquement sur les couts
12. **Les pourcentages de marge** sont arrondis a 2 decimales pour l'affichage

---

## 8. Criteres d'Acceptance Globaux de l'EPIC

- Toutes les User Stories US-FI01 a US-FI10 sont developpees et validees
- Les donnees financieres affichees sont coherentes avec les modules sources : les montants de CA correspondent aux factures emises (EPIC-004), les couts correspondent aux donnees du module Couts (EPIC-007), les honoraires correspondent au module Honoraires (EPIC-003)
- Le basculement Realise / Projete fonctionne correctement sur toutes les vues et produit des resultats coherents
- Le toggle Couts fixes inclut/exclut correctement les frais generaux dans tous les calculs de marge
- Les filtres (annee, projet, entite) fonctionnent de maniere cumulative et mettent a jour instantanement les vues
- Les graphiques sont lisibles, interactifs et s'affichent correctement sur desktop et tablette
- Les exports CSV et Excel contiennent des donnees correctes et formatees
- Les droits d'acces sont respectes : un chef de projet ne voit que les finances de ses projets, un directeur voit l'ensemble
- Les performances sont acceptables : chargement < 3 secondes pour une vue consolidee de 50 projets, basculement de mode < 1 seconde
- Tous les montants sont affiches avec la devise appropriee et un formatage coherent (separateurs de milliers, 2 decimales)

---

## 9. Definition of Done (DoD)

- Le code est developpe, revu par un pair et merge sur la branche principale
- Les tests unitaires couvrent les fonctions critiques : calcul de marge, consolidation des couts, aggregation du CA, application des filtres
- Les tests d'integration valident les flux complets : donnees Honoraires + Facturation + Temps + Couts -> vues Finances coherentes
- Les tests de non-regression verifient que les modifications n'impactent pas les modules sources
- La documentation technique est mise a jour (API endpoints, modeles de donnees, regles de calcul)
- Les graphiques sont testes sur les navigateurs cibles (Chrome, Firefox, Safari) en resolution desktop et tablette
- La fonctionnalite a ete testee et validee par le Product Owner
- Aucun bug bloquant ou critique n'est ouvert
- Les donnees de demo sont coherentes et representatives (projets avec CA, couts et marges variees)
- Les exports ont ete verifies : contenu correct, formatage lisible, encodage UTF-8

---

## 10. Dependances

### Depend de :

| EPIC | Raison |
|---|---|
| EPIC-002 (Projets) | Les donnees financieres sont rattachees a des projets existants |
| EPIC-003 (Honoraires) | Le CA planifie est calcule a partir des honoraires signes |
| EPIC-004 (Facturation) | Le CA realise est calcule a partir des factures emises et des paiements recus |
| EPIC-005 (Temps) | Les couts salariaux sont calcules a partir des temps saisis par les collaborateurs |
| EPIC-007 (Couts) | Les couts de sous-traitance et frais generaux proviennent du module Couts |

### Requis par :

| EPIC | Raison |
|---|---|
| EPIC-011 (Rapports) | Les rapports financiers exploitent les donnees consolidees du module Finances |

### APIs requises :

- API Finances (lecture consolidee) : endpoints de lecture des donnees financieres agreges
- API Projets (EPIC-002) : liste des projets, details projet
- API Honoraires (EPIC-003) : honoraires planifies par projet et par phase
- API Facturation (EPIC-004) : factures emises, paiements recus, montants HT
- API Temps (EPIC-005) : heures saisies par collaborateur, par projet, par phase
- API Couts (EPIC-007) : taux horaires, factures sous-traitants, frais generaux
- API Entites : liste des entites, parametres fiscaux

---

## 11. Modele de Donnees Principal

### Objet : FinancialSummary (Synthese financiere par projet et par annee)

| Champ | Type | Description |
|---|---|---|
| id | UUID | Identifiant unique de l'enregistrement |
| project_id | UUID (FK) | Reference du projet (EPIC-002) |
| year | Integer | Annee fiscale (ex : 2025) |
| month | Integer (nullable) | Mois (1-12), null pour les agregats annuels |
| revenue_planned | Decimal(12,2) | CA planifie (honoraires x avancement prevu) |
| revenue_invoiced | Decimal(12,2) | CA facture (total factures emises HT) |
| revenue_paid | Decimal(12,2) | CA encaisse (total paiements recus HT) |
| revenue_actual | Decimal(12,2) | CA retenu pour le mode Realise (= revenue_invoiced) |
| costs_salaries | Decimal(12,2) | Couts salariaux (temps x taux horaire) |
| costs_subcontractors | Decimal(12,2) | Couts sous-traitants (factures sous-traitants) |
| costs_general | Decimal(12,2) | Frais generaux imputes au projet |
| costs_fixed | Decimal(12,2) | Couts fixes alloues au projet (loyer, assurances) |
| costs_total | Decimal(12,2) | Total couts (salaires + sous-traitants + generaux + fixes) |
| margin_planned | Decimal(12,2) | Marge projetee (revenue_planned - costs estimes) |
| margin_actual | Decimal(12,2) | Marge realisee (revenue_actual - costs constates) |
| margin_percent | Decimal(5,2) | Marge en pourcentage (margin_actual / revenue_actual x 100) |
| currency | String(3) | Devise (EUR, CAD, USD...) heritee du projet |
| entity_id | UUID (FK) | Reference de l'entite/agence |
| computed_at | Timestamp | Date et heure du dernier calcul |
| created_at | Timestamp | Date de creation |
| updated_at | Timestamp | Date de derniere modification |

### Objet : FinancialSettings (Parametres financiers par entite)

| Champ | Type | Description |
|---|---|---|
| id | UUID | Identifiant unique |
| entity_id | UUID (FK) | Reference de l'entite/agence |
| fiscal_year_start | Integer | Mois de debut de l'annee fiscale (1 = janvier, 4 = avril, etc.) |
| include_fixed_costs | Boolean | Inclure les couts fixes par defaut dans les calculs de marge |
| default_currency | String(3) | Devise par defaut de l'entite (EUR, CAD, USD...) |
| margin_threshold_green | Decimal(5,2) | Seuil de marge haute en % (par defaut : 20.00) |
| margin_threshold_orange | Decimal(5,2) | Seuil de marge basse en % (par defaut : 0.00) |
| general_costs_allocation_method | String | Methode de repartition des frais generaux (prorata_time, prorata_revenue, fixed_amount) |
| created_at | Timestamp | Date de creation |
| updated_at | Timestamp | Date de derniere modification |

### Objet : FinancialSnapshot (Historique des calculs financiers)

| Champ | Type | Description |
|---|---|---|
| id | UUID | Identifiant unique |
| financial_summary_id | UUID (FK) | Reference du FinancialSummary |
| snapshot_date | Date | Date du snapshot |
| snapshot_type | String | Type (monthly_close, quarterly_close, manual) |
| data | JSON | Copie integrale des donnees financieres a la date du snapshot |
| created_by | UUID (FK) | Utilisateur ayant declenche le snapshot |
| created_at | Timestamp | Date de creation |

---

## 12. Estimation & Decoupage

### Effort global estime : 4 a 6 semaines de developpement (selon taille de l'equipe)

### Sprint 1 — Fondations et Vue Resume (2 semaines)

| User Story | Contenu | Points |
|---|---|---|
| US-FI01 | Tableau de bord Resume financier (KPIs, graphique barres CA/Couts, courbe marge) | 13 |
| US-FI06 | Toggle Realise / Projete (mecanique de basculement sur toutes les vues) | 8 |
| US-FI07 | Filtrage par annee, projet, entite (composants de filtrage reutilisables) | 8 |
| -- | **Modele de donnees** : creation des tables FinancialSummary, FinancialSettings | 5 |
| -- | **API consolidation** : endpoints de lecture agregee depuis Honoraires, Facturation, Temps, Couts | 8 |
| | **Total Sprint 1** | **42** |

### Sprint 2 — Vues detaillees CA, Couts, Marge (2 semaines)

| User Story | Contenu | Points |
|---|---|---|
| US-FI02 | Vue Chiffre d'affaires (tableau par projet, graphique barres groupees facturable/facture/paye) | 8 |
| US-FI03 | Vue Couts consolides (tableau ventile, graphique barres empilees, toggle couts fixes) | 8 |
| US-FI04 | Vue Marge globale (tableau avec code couleur, graphique barres horizontales, modes Realise/Projete) | 8 |
| US-FI10 | Graphiques et visualisations (composants graphiques interactifs, tooltips, legendes) | 8 |
| | **Total Sprint 2** | **32** |

### Sprint 3 — Finance projet, Rentabilite et Export (1 a 2 semaines)

| User Story | Contenu | Points |
|---|---|---|
| US-FI05 | Onglet FINANCE dans la vue projet (graphique barres + courbe marge cumulee + tableau marge par annee) | 8 |
| US-FI09 | Indicateurs de rentabilite (codes couleur, icones alerte, seuils configurables, tooltips) | 5 |
| US-FI08 | Export des donnees financieres (CSV, Excel, respect des filtres, formatage) | 5 |
| -- | **Tests d'integration** : validation coherence donnees entre modules sources et vues Finances | 5 |
| -- | **Tests de performance** : validation des temps de chargement et de basculement | 3 |
| | **Total Sprint 3** | **26** |

### Recapitulatif

| Sprint | Duree | Points | Objectif principal |
|---|---|---|---|
| Sprint 1 | 2 semaines | 42 | Fondations, API, Resume, Filtres, Toggle Realise/Projete |
| Sprint 2 | 2 semaines | 32 | Vues CA, Couts, Marge, Graphiques |
| Sprint 3 | 1-2 semaines | 26 | Finance projet, Rentabilite, Export, Tests |
| **Total** | **5-6 semaines** | **100** | |

### Equipe suggeree :

- 1 developpeur back-end (API consolidation, modele de donnees, calculs)
- 1 developpeur front-end (composants UI, graphiques, tableaux, filtres)
- 1 designer UI/UX (maquettes des graphiques et tableaux de bord)
- 1 QA (tests fonctionnels, validation des calculs, coherence inter-modules)

### Risques identifies :

- **Coherence des donnees** : la consolidation de donnees provenant de 4 modules differents (Honoraires, Facturation, Temps, Couts) necessite des tests rigoureux pour garantir l'exactitude des calculs
- **Performance** : l'aggregation de grandes quantites de donnees financieres (projets multiples x annees multiples) peut impacter les temps de reponse -- prevoir du caching ou du pre-calcul
- **Dependances fortes** : le module Finances ne peut fonctionner que si les modules EPIC-003, EPIC-004, EPIC-005 et EPIC-007 sont operationnels et exposent leurs APIs
