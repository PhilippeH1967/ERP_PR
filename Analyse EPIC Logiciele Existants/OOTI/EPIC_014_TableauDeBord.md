# EPIC -- Module Tableau de bord

**Application OOTI -- Gestion de projets pour cabinets d'architecture**
**Version 1.0 -- Fevrier 2026**

---

## Table des matieres

1. [Identification](#1-identification)
2. [Contexte et Problematique](#2-contexte-et-problematique)
3. [Objectif](#3-objectif)
4. [Perimetre Fonctionnel](#4-perimetre-fonctionnel)
5. [User Stories](#5-user-stories)
6. [Hors Perimetre](#6-hors-perimetre)
7. [Regles Metier](#7-regles-metier)
8. [Criteres Globaux](#8-criteres-globaux)
9. [Definition of Done (DoD)](#9-definition-of-done-dod)
10. [Dependances](#10-dependances)
11. [Modele de Donnees](#11-modele-de-donnees)
12. [Estimation](#12-estimation)

---

## 1. Identification

| Champ | Valeur |
|---|---|
| **Nom** | Tableau de bord |
| **Reference** | EPIC-014 |
| **Module parent** | General |
| **Priorite** | Moyenne |
| **Auteur** | Equipe Produit OOTI |
| **Date de creation** | 26 fevrier 2026 |
| **Version du document** | 1.0 |
| **Statut** | Redaction |

### EPICs lies

| Reference | Nom | Nature de la dependance |
|---|---|---|
| EPIC-002 | Projets | Fournit les donnees de projets actifs, avancement, planning Gantt |
| EPIC-003 | Honoraires | Fournit les montants facturables et le chiffre d'affaires planifie |
| EPIC-004 | Facturation | Fournit le solde des factures impayees et le CA realise |
| EPIC-005 | Temps | Fournit le pourcentage de temps saisi par les collaborateurs |
| EPIC-008 | Finances | Fournit les donnees de couts, marges et synthese financiere |

---

## 2. Contexte et Problematique

### Contexte

Dans un cabinet d'architecture, la direction et les chefs de projet doivent piloter simultanement de nombreux indicateurs : rentabilite des projets, suivi des facturations, temps passes, echeances a venir. Ces informations sont dispersees entre plusieurs modules de l'application (Projets, Honoraires, Facturation, Temps, Finances) et necessitent de naviguer entre de multiples ecrans pour obtenir une vision globale de l'activite de l'agence.

Les cabinets d'architecture operent dans un environnement ou la marge financiere est souvent reduite. Une visibilite insuffisante sur les indicateurs cles (honoraires facturables, factures impayees, taux de saisie des temps) peut entrainer des retards de facturation, une degradation de la tresorerie et une perte de controle sur la rentabilite des projets.

### Problematique

**L'absence d'une vue synthetique centralisee** engendre plusieurs difficultes operationnelles :

- **Perte de temps** : les dirigeants et chefs de projet doivent consulter 4 a 5 modules differents pour reconstituer manuellement un tableau de bord de pilotage, ce qui represente en moyenne 30 a 45 minutes par jour.
- **Decisions tardives** : sans vision consolidee en temps reel, les anomalies (factures impayees en hausse, temps non saisis, depassement de budget) sont detectees trop tard pour etre corrigees efficacement.
- **Manque de visibilite sur les echeances** : les jalons de projet, taches a venir, conges et evenements ne sont pas agriges dans une vue unique, ce qui augmente le risque d'oubli et de desorganisation.
- **Absence de personnalisation** : chaque role (dirigeant, chef de projet, collaborateur) a des besoins de pilotage differents, mais tous voient les memes ecrans sans possibilite d'adaptation.
- **Deconnexion entre le planifie et le realise** : la comparaison entre le chiffre d'affaires projete et le chiffre d'affaires realise n'est pas immediatement accessible, ce qui limite le pilotage financier strategique.

---

## 3. Objectif

### Objectif principal

Concevoir et implementer un **tableau de bord centralisee** constituant la page d'accueil de l'application OOTI (accessible via **GENERAL > Tableau de bord**), offrant une vue synthetique, personnalisable et actualisee en temps reel de l'ensemble de l'activite de l'agence.

### Objectifs specifiques

| # | Objectif | Indicateur de succes |
|---|---|---|
| O1 | Centraliser les KPIs cles (facturable, impaye, temps saisi) en une seule vue | 100 % des KPIs identifies sont affiches sur le tableau de bord |
| O2 | Fournir une synthese financiere visuelle (CA projete vs realise) | Le graphique affiche les courbes comparatives sur 12 mois glissants |
| O3 | Afficher un planning projet resume sous forme de Gantt | Les projets actifs sont visibles avec leur avancement en pourcentage |
| O4 | Agreger les echeances a venir (jalons, taches, conges, evenements) | Les elements des 2 prochaines semaines sont affiches dans la sidebar |
| O5 | Permettre la personnalisation des widgets affiches | L'utilisateur peut masquer/afficher chaque widget individuellement |
| O6 | Adapter l'affichage selon le role utilisateur | Un admin voit les donnees de toute l'agence, un collaborateur voit ses projets |
| O7 | Reduire le temps de consultation quotidien des indicateurs | Objectif : passer de 30-45 min a moins de 5 min pour obtenir une vue globale |
| O8 | Offrir un bloc-notes personnel directement sur le dashboard | Chaque utilisateur dispose d'un espace de notes persistant |

---

## 4. Perimetre Fonctionnel

### 4.1 Vue d'ensemble du tableau de bord

Le tableau de bord se decompose en plusieurs zones fonctionnelles :

```
+------------------------------------------------------------------+
|  [Logo Agence]           TABLEAU DE BORD              [oeil icon] |
+------------------------------------------------------------------+
|  +-------------+ +-------------+ +-------------+ +-------------+ |
|  | FACTURABLE  | | NON PAYE    | | TEMPS       | | NOTE        | |
|  | Montant HT  | | Solde TTC   | | ENREGISTRE  | | Bloc-notes  | |
|  |             | | [=========] | | XX %        | | libre       | |
|  +-------------+ +-------------+ +-------------+ +-------------+ |
+------------------------------------------------------------------+
|                                        |                          |
|  SYNTHESE FINANCIERE                   |  A VENIR                 |
|  +-------------------------------+     |  +--------------------+  |
|  | CA Projete vs CA Realise      |     |  | Jalons cles        |  |
|  | [Graphique courbes mensuel]   |     |  | - Jalon 1 (J+3)    |  |
|  |                               |     |  | - Jalon 2 (J+7)    |  |
|  | Filtre: [Annee] [Periode]     |     |  +--------------------+  |
|  +-------------------------------+     |  | Taches             |  |
|                                        |  | - Tache 1 (J+1)    |  |
|  PLANNING PROJET                       |  | - Tache 2 (J+5)    |  |
|  +-------------------------------+     |  +--------------------+  |
|  | [Vue Gantt resumee]           |     |  | Conges              |  |
|  | Projet A  [===========    ]   |     |  | - P. Dupont (3-5/3) |  |
|  | Projet B  [=======        ]   |     |  +--------------------+  |
|  | Projet C  [=============== ]  |     |  | Evenements          |  |
|  +-------------------------------+     |  | - Reunion (28/2)    |  |
|                                        |  +--------------------+  |
+------------------------------------------------------------------+
```

### 4.2 Detail des zones fonctionnelles

#### 4.2.1 Bandeau superieur

- Affichage du **logo de l'agence** en haut a gauche (configurable dans les parametres generaux).
- Titre de la page : "Tableau de bord".
- **Bouton "oeil"** en haut a droite permettant d'ouvrir le panneau de personnalisation des widgets.

#### 4.2.2 KPI Cards (4 cartes en ligne)

| KPI | Source de donnees | Contenu affiche | Comportement |
|---|---|---|---|
| **Facturable** | EPIC-003 Honoraires | Montant total HT des honoraires facturables non encore factures | Rafraichissement temps reel, clic pour naviguer vers le module Honoraires |
| **Non paye** | EPIC-004 Facturation | Solde TTC total des factures emises mais non reglees, avec barre de progression (payee vs non payee) | Barre de progression visuelle, clic pour naviguer vers le module Facturation |
| **Temps enregistre** | EPIC-005 Temps | Pourcentage de temps saisi par rapport au temps de travail theorique (periode en cours : semaine ou mois) | Affichage en pourcentage avec indicateur couleur (vert >= 80 %, orange 50-79 %, rouge < 50 %) |
| **Note** | Stockage local (DashboardConfig) | Bloc-notes libre en texte riche, contenu personnel a l'utilisateur | Edition directe sur le dashboard, sauvegarde automatique |

#### 4.2.3 Synthese financiere

- **Type de graphique** : courbes (line chart) superposees sur un axe temporel mensuel.
- **Donnees affichees** :
  - Chiffre d'affaires HT realise vs planifie (2 courbes).
  - Couts HT realises vs planifies (2 courbes, affichage optionnel via legende cliquable).
  - Marge HT realisee vs planifiee (2 courbes, affichage optionnel via legende cliquable).
- **Axe X** : mois de l'annee (janvier a decembre).
- **Axe Y** : montant en euros (echelle dynamique).
- **Filtres** : selecteur d'annee (annee en cours par defaut), selecteur de periode (trimestre, semestre, annee complete).
- **Interactivite** : survol (tooltip avec valeurs exactes), clic sur un point pour naviguer vers le detail financier du mois concerne.

#### 4.2.4 Planning projet resume

- **Type de vue** : diagramme de Gantt simplifie.
- **Donnees affichees** : projets actifs de l'utilisateur (ou de l'agence pour un admin) avec :
  - Nom du projet.
  - Barre de progression coloree (vert = dans les temps, orange = retard modere, rouge = retard critique).
  - Dates de debut et fin previsionnelles.
  - Pourcentage d'avancement.
- **Tri** : par date de fin la plus proche par defaut.
- **Limite** : affichage des 10 premiers projets avec possibilite de "voir plus" pour naviguer vers le module Projets.

#### 4.2.5 Section "A venir" (sidebar droite)

La sidebar affiche les elements a venir dans les **2 prochaines semaines**, organises en 4 sous-sections :

| Sous-section | Contenu | Source |
|---|---|---|
| **Jalons cles** | Jalons de projet dont la date d'echeance est dans les 14 prochains jours | EPIC-002 Projets |
| **Taches** | Taches assignees a l'utilisateur dont la date d'echeance est dans les 14 prochains jours | EPIC-002 Projets |
| **Conges** | Conges approuves des membres de l'equipe dans les 14 prochains jours | Module RH / Conges |
| **Evenements** | Evenements d'agence (reunions, revues, presentations) dans les 14 prochains jours | Module Calendrier |

Chaque element affiche : intitule, date (et heure si applicable), personne concernee (pour les conges), projet associe (pour les jalons et taches).

#### 4.2.6 Personnalisation des widgets

- Accessible via le **bouton "oeil"** dans le bandeau superieur.
- Panneau lateral (ou modal) affichant la liste de tous les widgets avec un interrupteur (toggle) pour chaque :
  - KPI Facturable
  - KPI Non paye
  - KPI Temps enregistre
  - KPI Note
  - Synthese financiere
  - Planning projet
  - Jalons cles
  - Taches
  - Conges
  - Evenements
- La configuration est **sauvegardee par utilisateur** et persistee entre les sessions.
- Un bouton "Reinitialiser par defaut" permet de restaurer la configuration initiale (tous les widgets visibles).

---

## 5. User Stories

### US-TB01 -- Affichage des KPIs cles (Facturable, Non paye, Temps enregistre)

**En tant que** dirigeant ou chef de projet,
**Je veux** voir sur la page d'accueil trois indicateurs cles (montant facturable HT, solde impaye TTC, pourcentage de temps enregistre) presentes sous forme de cartes synthetiques,
**Afin de** disposer en un coup d'oeil d'une vision instantanee de la sante financiere et operationnelle de l'agence sans avoir a naviguer dans plusieurs modules.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---|---|
| CA-01 | La carte "Facturable" affiche le montant total HT des honoraires facturables non factures, calcule a partir des donnees du module Honoraires (EPIC-003) | Verifier que le montant correspond a la somme des lignes d'honoraires facturables dont le statut est "Non facture" |
| CA-02 | La carte "Non paye" affiche le solde TTC total des factures emises non reglees, issu du module Facturation (EPIC-004) | Verifier que le montant correspond a la somme des factures ayant le statut "Emise" ou "En retard" |
| CA-03 | La carte "Non paye" comporte une barre de progression horizontale representant le ratio montant paye / montant total facture | Verifier que la barre de progression affiche le bon ratio (ex : 60 % paye = barre remplie a 60 %) |
| CA-04 | La carte "Temps enregistre" affiche le pourcentage de temps saisi par rapport au temps de travail theorique de la periode en cours (semaine courante par defaut) | Verifier que le pourcentage est coherent avec les donnees du module Temps (EPIC-005) : (temps saisi / temps theorique) x 100 |
| CA-05 | Le pourcentage de temps enregistre est accompagne d'un indicateur de couleur : vert si >= 80 %, orange si entre 50 % et 79 %, rouge si < 50 % | Tester les trois seuils avec des jeux de donnees differents |
| CA-06 | Les donnees des trois KPIs sont actualisees automatiquement a chaque chargement de la page et toutes les 5 minutes sans rechargement complet (polling ou WebSocket) | Modifier une donnee source (ex : enregistrer une facture) et verifier que le KPI se met a jour dans un delai de 5 minutes maximum |
| CA-07 | Un clic sur chaque carte KPI redirige l'utilisateur vers le module source correspondant (Honoraires, Facturation, Temps) | Verifier la navigation vers le bon module pour chaque carte |
| CA-08 | Les montants sont formates selon la locale de l'utilisateur (separateur de milliers, symbole monetaire, nombre de decimales) | Tester avec les locales fr-FR (1 234,56 EUR) et en-US ($1,234.56) |

---

### US-TB02 -- Bloc-notes personnel

**En tant que** utilisateur de l'application (quel que soit mon role),
**Je veux** disposer d'un bloc-notes libre integre directement sur le tableau de bord, dont le contenu est personnel et persistant,
**Afin de** pouvoir noter rapidement des rappels, idees ou informations importantes sans quitter la page d'accueil.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---|---|
| CA-01 | Le bloc-notes est affiche dans la quatrieme carte KPI en haut du tableau de bord, intitulee "Note" | Verifier la presence et la position du widget Note |
| CA-02 | Le contenu du bloc-notes est editable directement dans la carte via un champ de texte riche (gras, italique, listes a puces, liens) | Tester la saisie et le formatage de texte dans le bloc-notes |
| CA-03 | Le contenu est sauvegarde automatiquement apres 2 secondes d'inactivite de saisie (debounce), sans action manuelle de l'utilisateur | Saisir du texte, attendre 2 secondes, recharger la page et verifier la persistance |
| CA-04 | Le contenu du bloc-notes est strictement personnel : chaque utilisateur a son propre contenu, invisible pour les autres utilisateurs | Se connecter avec deux comptes differents et verifier que les contenus sont independants |
| CA-05 | Le bloc-notes accepte un contenu d'une longueur maximale de 5 000 caracteres. Au-dela, un message d'information est affiche et la saisie est bloquee | Saisir un texte depassant 5 000 caracteres et verifier le comportement |
| CA-06 | Un indicateur visuel confirme la sauvegarde reussie (ex : icone de validation ephemere ou texte "Sauvegarde" affiche brievement) | Verifier l'apparition de l'indicateur apres chaque sauvegarde automatique |
| CA-07 | Le bloc-notes affiche un placeholder incitatif lorsqu'il est vide (ex : "Ajoutez vos notes ici...") | Verifier la presence du placeholder sur un compte dont le bloc-notes est vide |

---

### US-TB03 -- Synthese financiere (graphique annuel)

**En tant que** dirigeant ou responsable financier de l'agence,
**Je veux** visualiser sur le tableau de bord un graphique de synthese financiere presentant les courbes du chiffre d'affaires, des couts et de la marge (realises vs planifies) mois par mois sur une annee,
**Afin de** suivre la performance financiere de l'agence, identifier les ecarts entre le previsionnel et le reel, et anticiper les ajustements necessaires.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---|---|
| CA-01 | Le graphique affiche par defaut les courbes du CA HT realise et du CA HT planifie sur les 12 mois de l'annee en cours | Verifier la presence des deux courbes de CA sur l'annee en cours |
| CA-02 | Les courbes de Couts HT (realises vs planifies) et de Marge HT (realisee vs planifiee) sont disponibles et activables/desactivables via la legende cliquable du graphique | Cliquer sur les elements de la legende et verifier l'apparition/disparition des courbes correspondantes |
| CA-03 | Le survol (hover) d'un point de donnee affiche un tooltip contenant les valeurs exactes de tous les indicateurs actifs pour le mois concerne (CA, Couts, Marge, en realise et planifie) | Survoler differents points et verifier l'exactitude des valeurs affichees dans le tooltip |
| CA-04 | Les donnees du graphique proviennent du croisement entre le module Finances (EPIC-008) pour les donnees realisees et le module Honoraires (EPIC-003) pour les donnees planifiees | Verifier la coherence des montants affiches avec les modules sources |
| CA-05 | L'axe Y s'adapte dynamiquement a la plage de valeurs affichees (echelle automatique) pour garantir une lisibilite optimale | Tester avec des jeux de donnees de magnitudes differentes (ex : agence a 50 000 EUR/mois vs 500 000 EUR/mois) |
| CA-06 | Un selecteur d'annee permet de visualiser les donnees d'annees precedentes (historique disponible sur les 3 dernieres annees minimum) | Changer l'annee selectionnee et verifier le rechargement correct des courbes |
| CA-07 | Un selecteur de periode permet de filtrer l'affichage par trimestre (T1, T2, T3, T4), semestre (S1, S2) ou annee complete | Tester chaque option de filtre et verifier que seuls les mois concernes sont affiches |
| CA-08 | Le graphique est responsive et s'adapte a la largeur du conteneur sans perte de lisibilite (labels, legende, tooltip) | Redimensionner la fenetre du navigateur et verifier le comportement adaptatif du graphique |

---

### US-TB04 -- Planning projet resume

**En tant que** chef de projet ou dirigeant,
**Je veux** voir sur le tableau de bord un planning Gantt simplifie montrant l'avancement des projets actifs,
**Afin de** suivre en un coup d'oeil l'etat d'avancement de chaque projet et identifier rapidement ceux qui prennent du retard.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---|---|
| CA-01 | Le planning affiche sous forme de diagramme de Gantt simplifie les projets ayant le statut "Actif" dans le module Projets (EPIC-002) | Verifier que seuls les projets actifs sont affiches et que les projets termines ou en pause sont exclus |
| CA-02 | Chaque projet est represente par une barre horizontale indiquant la periode (date de debut a date de fin previsionnelle) et le pourcentage d'avancement | Verifier la correspondance entre les dates et la longueur de la barre, et l'exactitude du pourcentage affiche |
| CA-03 | La couleur de la barre de progression est codee selon l'etat du projet : vert = dans les temps (avancement >= avancement theorique), orange = retard modere (ecart < 15 %), rouge = retard critique (ecart >= 15 %) | Creer des projets avec differents niveaux de retard et verifier le code couleur |
| CA-04 | Les projets sont tries par date de fin la plus proche par defaut | Verifier l'ordre d'affichage des projets dans le Gantt |
| CA-05 | Le nombre de projets affiches est limite a 10. Un lien "Voir tous les projets" permet de naviguer vers la vue complete du module Projets (EPIC-002) | Creer plus de 10 projets actifs et verifier la troncature et la presence du lien |
| CA-06 | Le survol d'une barre de projet affiche un tooltip avec : nom du projet, chef de projet, date de debut, date de fin, avancement en pourcentage, budget consomme en pourcentage | Survoler differentes barres et verifier les informations du tooltip |
| CA-07 | Un clic sur un projet dans le Gantt redirige vers la fiche detaillee du projet dans le module Projets | Verifier la navigation pour 3 projets differents |
| CA-08 | Le planning affiche une ligne verticale representant la date du jour (marqueur "aujourd'hui") pour contextualiser visuellement les echeances | Verifier la presence et la position correcte du marqueur |

---

### US-TB05 -- Widget "A venir" (Jalons, Taches, Conges, Evenements)

**En tant que** collaborateur, chef de projet ou dirigeant,
**Je veux** voir dans une sidebar du tableau de bord les evenements a venir dans les deux prochaines semaines, organises par categories (jalons, taches, conges, evenements),
**Afin de** anticiper les echeances proches, organiser ma charge de travail et etre informe des absences de mes collegues.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---|---|
| CA-01 | La sidebar "A venir" est positionnee sur le cote droit du tableau de bord et contient 4 sous-sections clairement identifiees : Jalons cles, Taches, Conges, Evenements | Verifier la presence et le positionnement de la sidebar et de ses 4 sous-sections |
| CA-02 | La sous-section "Jalons cles" affiche les jalons de projet dont la date d'echeance se situe dans les 14 prochains jours calendaires, avec le nom du jalon, le nom du projet associe et la date d'echeance | Creer des jalons avec des dates dans et hors de la fenetre de 14 jours et verifier le filtrage |
| CA-03 | La sous-section "Taches" affiche les taches assignees a l'utilisateur connecte dont la date d'echeance se situe dans les 14 prochains jours, avec le nom de la tache, le projet associe et la date limite | Verifier que seules les taches de l'utilisateur connecte sont affichees (pas celles des autres) |
| CA-04 | La sous-section "Conges" affiche les conges approuves de tous les membres de l'equipe de l'utilisateur dans les 14 prochains jours, avec le nom du collaborateur, les dates de debut et fin du conge | Verifier la presence des conges approuves et l'absence des conges en attente ou refuses |
| CA-05 | La sous-section "Evenements" affiche les evenements d'agence (reunions, revues de projet, presentations) planifies dans les 14 prochains jours, avec l'intitule, la date, l'heure et le lieu le cas echeant | Creer des evenements dans et hors de la fenetre et verifier |
| CA-06 | Les elements de chaque sous-section sont tries par date chronologique croissante (le plus proche en premier) | Verifier l'ordre d'affichage dans chaque sous-section |
| CA-07 | Un clic sur un element de la sidebar (jalon, tache, evenement) redirige vers la vue detaillee de cet element dans le module correspondant | Verifier la navigation pour au moins un element de chaque sous-section |
| CA-08 | Lorsqu'une sous-section ne contient aucun element a venir, un message "Aucun element a venir" est affiche pour eviter un espace vide | Vider une sous-section et verifier l'affichage du message |

---

### US-TB06 -- Personnalisation des widgets affiches

**En tant que** utilisateur de l'application,
**Je veux** pouvoir choisir quels widgets du tableau de bord sont affiches ou masques, via un panneau de personnalisation accessible par le bouton "oeil",
**Afin de** adapter le tableau de bord a mes besoins specifiques et n'afficher que les informations pertinentes pour mon activite quotidienne.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---|---|
| CA-01 | Un bouton representant une icone "oeil" est visible en haut a droite du tableau de bord | Verifier la presence et la position du bouton |
| CA-02 | Un clic sur le bouton "oeil" ouvre un panneau lateral (drawer) ou une modale listant tous les widgets disponibles avec un interrupteur (toggle) on/off pour chacun : Facturable, Non paye, Temps enregistre, Note, Synthese financiere, Planning projet, Jalons cles, Taches, Conges, Evenements | Verifier que les 10 widgets sont listes avec un toggle fonctionnel |
| CA-03 | La desactivation d'un toggle masque immediatement le widget correspondant sur le tableau de bord, sans necessiter de rechargement de la page | Desactiver un widget et verifier sa disparition instantanee |
| CA-04 | La reactivation d'un toggle reaffiche immediatement le widget a sa position originale dans la mise en page | Reactiver un widget masque et verifier son reaffichage a la bonne position |
| CA-05 | La configuration des widgets visibles est sauvegardee automatiquement et persiste entre les sessions (stockage cote serveur associe au profil utilisateur) | Modifier la configuration, se deconnecter, se reconnecter et verifier la persistance |
| CA-06 | Un bouton "Reinitialiser par defaut" dans le panneau de personnalisation restaure la configuration initiale (tous les widgets visibles) | Masquer plusieurs widgets, cliquer sur le bouton de reinitialisation et verifier que tous les widgets sont de nouveau affiches |
| CA-07 | La personnalisation est propre a chaque utilisateur : la configuration de l'utilisateur A n'affecte pas celle de l'utilisateur B | Configurer deux comptes differemment et verifier l'independance |

---

### US-TB07 -- Adaptation du tableau de bord selon le role utilisateur

**En tant que** administrateur systeme ou dirigeant de l'agence,
**Je veux** que le tableau de bord affiche des donnees adaptees au role de l'utilisateur connecte (vue globale agence pour les admins, vue restreinte aux projets personnels pour les collaborateurs),
**Afin de** garantir que chaque utilisateur accede aux informations pertinentes pour son niveau de responsabilite, tout en respectant les principes de confidentialite et de segmentation des donnees.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---|---|
| CA-01 | Un utilisateur ayant le role "Administrateur" ou "Dirigeant" voit les KPIs agreges de l'ensemble de l'agence (total facturable, total impaye, taux de temps enregistre global) | Se connecter en tant qu'admin et verifier que les KPIs couvrent tous les projets et tous les collaborateurs |
| CA-02 | Un utilisateur ayant le role "Chef de projet" voit les KPIs agreges de ses projets uniquement (facturable de ses projets, impaye de ses projets, temps enregistre de ses equipes) | Se connecter en tant que chef de projet et verifier la restriction aux projets dont il est responsable |
| CA-03 | Un utilisateur ayant le role "Collaborateur" voit les KPIs relatifs a ses propres donnees (honoraires facturables de ses projets, factures de ses projets, son propre taux de temps enregistre) | Se connecter en tant que collaborateur et verifier la restriction a ses donnees personnelles |
| CA-04 | La synthese financiere affiche les donnees de l'agence entiere pour un admin, et les donnees des projets de l'utilisateur pour un chef de projet ou collaborateur | Comparer les graphiques entre un compte admin et un compte collaborateur |
| CA-05 | Le planning projet resume affiche tous les projets actifs de l'agence pour un admin, et uniquement les projets assignes pour les autres roles | Verifier la liste des projets affiches selon le role |
| CA-06 | La sous-section "Conges" dans la sidebar "A venir" affiche les conges de toute l'agence pour un admin, et ceux de l'equipe du collaborateur pour les autres roles | Verifier le perimetre des conges affiches selon le role |
| CA-07 | Les regles de filtrage par role sont appliquees cote serveur (API) et non uniquement cote client, afin de garantir la securite des donnees | Inspecter les appels API avec des tokens de differents roles et verifier que les reponses sont correctement filtrees |
| CA-08 | En cas de changement de role d'un utilisateur, le tableau de bord reflete immediatement le nouveau perimetre de donnees lors de la prochaine connexion | Modifier le role d'un utilisateur, se reconnecter et verifier la mise a jour du perimetre |

---

### US-TB08 -- Filtrage de la synthese financiere par periode

**En tant que** dirigeant ou responsable financier,
**Je veux** pouvoir filtrer le graphique de synthese financiere par annee et par periode (trimestre, semestre, annee complete),
**Afin de** analyser les tendances financieres sur differentes granularites temporelles et comparer les performances d'une periode a l'autre.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---|---|
| CA-01 | Un selecteur d'annee est affiche au-dessus ou a cote du graphique de synthese financiere, avec l'annee en cours selectionnee par defaut | Verifier la presence du selecteur et la valeur par defaut |
| CA-02 | Le selecteur d'annee propose les 3 dernieres annees plus l'annee en cours (ex : 2023, 2024, 2025, 2026) | Verifier les options disponibles dans le selecteur |
| CA-03 | Un selecteur de periode permet de choisir entre : Annee complete (par defaut), Semestre 1 (janvier-juin), Semestre 2 (juillet-decembre), Trimestre 1 (janvier-mars), Trimestre 2 (avril-juin), Trimestre 3 (juillet-septembre), Trimestre 4 (octobre-decembre) | Verifier que toutes les options de periode sont disponibles |
| CA-04 | Le changement d'annee ou de periode declenche un rechargement du graphique avec les donnees correspondantes, avec un indicateur de chargement visible pendant le temps de traitement | Changer l'annee et la periode et verifier le rechargement avec spinner |
| CA-05 | Les filtres d'annee et de periode sont combinables : il est possible de selectionner le T2 de 2025 par exemple | Selectionner une combinaison annee + periode et verifier l'affichage |
| CA-06 | La selection des filtres est conservee pendant la session de navigation mais revient aux valeurs par defaut (annee en cours, annee complete) a la prochaine connexion | Verifier la persistance pendant la session et la reinitialisation apres deconnexion/reconnexion |
| CA-07 | Si aucune donnee n'est disponible pour la periode selectionnee, le graphique affiche un message "Aucune donnee disponible pour cette periode" au lieu d'un graphique vide | Selectionner une periode sans donnees et verifier l'affichage du message |

---

## 6. Hors Perimetre

Les elements suivants sont explicitement **exclus** du perimetre de cet EPIC et pourront faire l'objet d'evolutions ulterieures :

| # | Element exclu | Justification |
|---|---|---|
| HP-01 | Tableau de bord multi-agences (vue consolidee de plusieurs entites juridiques) | Necessite une architecture multi-tenant non prevue dans la version 1.0 |
| HP-02 | Export du tableau de bord en PDF ou image | Fonctionnalite secondaire, envisageable en version 1.1 |
| HP-03 | Widgets personnalisables par drag-and-drop (reorganisation libre de la mise en page) | Complexite technique significative, la version 1.0 se limite au masquage/affichage |
| HP-04 | Alertes et notifications push depuis le tableau de bord (ex : notification quand un seuil KPI est depasse) | Sera traite dans un EPIC dedie aux Notifications |
| HP-05 | Dashboards multiples par utilisateur (ex : "Mon dashboard", "Dashboard equipe", "Dashboard financier") | La version 1.0 offre un seul tableau de bord avec personnalisation des widgets |
| HP-06 | Integration de KPIs provenant de systemes externes (ERP, CRM, outils BIM) | Sera traite dans un EPIC dedie aux Integrations |
| HP-07 | Historique et versioning des notes du bloc-notes | La version 1.0 offre un contenu unique sans historique de modifications |
| HP-08 | Comparaison de periodes en superposition sur le graphique financier (ex : 2025 vs 2024 sur le meme graphique) | Fonctionnalite avancee envisageable en version 1.1 |
| HP-09 | Widgets de type "objectifs et OKR" ou "satisfaction client" | En dehors du perimetre fonctionnel initial de OOTI |
| HP-10 | Mode "plein ecran" pour les widgets individuels | Fonctionnalite secondaire, envisageable en version ulterieure |

---

## 7. Regles Metier

### RM-01 : Calcul du KPI "Facturable"

- Le montant facturable HT est calcule comme la somme des montants d'honoraires ayant le statut "Facturable" et n'ayant pas encore fait l'objet d'une facture.
- Formule : `SUM(honoraire.montant_ht) WHERE honoraire.statut = 'Facturable' AND honoraire.facture_id IS NULL`
- Le montant est exprime dans la devise principale de l'agence.
- En cas de projets multi-devises, la conversion est effectuee au taux de change du jour.

### RM-02 : Calcul du KPI "Non paye"

- Le solde impaye TTC est calcule comme la somme des montants TTC des factures ayant le statut "Emise", "Envoyee" ou "En retard", diminuee des paiements partiels deja enregistres.
- Formule : `SUM(facture.montant_ttc - facture.montant_paye) WHERE facture.statut IN ('Emise', 'Envoyee', 'En retard')`
- La barre de progression represente le ratio : `montant_total_paye / montant_total_facture * 100`

### RM-03 : Calcul du KPI "Temps enregistre"

- Le pourcentage est calcule sur la base de la semaine en cours (du lundi au dimanche).
- Temps theorique = nombre de jours ouvrables de la semaine x duree journaliere theorique du collaborateur (definie dans son profil, par defaut 8h).
- Formule : `(temps_total_saisi / temps_theorique_semaine) * 100`
- Pour un admin, le pourcentage est la moyenne des pourcentages individuels de tous les collaborateurs actifs.
- Seuils de couleur : vert >= 80 %, orange >= 50 % et < 80 %, rouge < 50 %.

### RM-04 : Donnees de la synthese financiere

- Le CA HT realise correspond a la somme des factures dont la date de facturation tombe dans le mois concerne et dont le statut est different de "Brouillon" et "Annulee".
- Le CA HT planifie correspond a la somme des revenus previsionnels definis dans le budget des projets (EPIC-003 Honoraires), ventiles par mois.
- Les Couts HT realises correspondent a la somme des depenses comptabilisees dans le module Finances (EPIC-008) pour le mois concerne.
- Les Couts HT planifies correspondent a la somme des budgets de depenses previsionnels des projets.
- La Marge HT = CA HT - Couts HT (calculee pour le realise et le planifie separement).

### RM-05 : Determination de l'etat d'avancement du projet (code couleur Gantt)

- L'avancement theorique est calcule au prorata temporel : `(date_du_jour - date_debut) / (date_fin - date_debut) * 100`
- Ecart = avancement_reel - avancement_theorique
- Vert : ecart >= 0 % (dans les temps ou en avance)
- Orange : ecart entre -1 % et -14 % (retard modere)
- Rouge : ecart <= -15 % (retard critique)
- Si la date de fin previsionnelle est depassee et le projet n'est pas termine, l'etat est automatiquement rouge.

### RM-06 : Fenetre temporelle "A venir"

- La fenetre de 14 jours calendaires est calculee a partir de la date du jour (J) a minuit : du jour J inclus au jour J+13 inclus.
- Les elements dont la date d'echeance tombe exactement sur J sont inclus dans la section "A venir".
- Les elements passes (date < J) ne sont jamais affiches dans la section "A venir".

### RM-07 : Filtrage par role utilisateur

- Le filtrage est applique **cote serveur** (au niveau de l'API) pour garantir la securite des donnees.
- Les roles reconnus sont : `Administrateur`, `Dirigeant`, `Chef de projet`, `Collaborateur`.
- `Administrateur` et `Dirigeant` : acces a toutes les donnees de l'agence.
- `Chef de projet` : acces aux donnees des projets dont il est le responsable designe.
- `Collaborateur` : acces a ses propres donnees (temps saisi, taches assignees) et aux donnees des projets auxquels il est affecte.

### RM-08 : Sauvegarde du bloc-notes

- Le contenu du bloc-notes est sauvegarde automatiquement 2 secondes apres la derniere frappe clavier (mecanisme de debounce).
- La sauvegarde est effectuee via un appel API PATCH sur l'endpoint de la configuration du dashboard.
- En cas d'echec de sauvegarde (erreur reseau), l'utilisateur est informe par une notification d'erreur non bloquante et le contenu est conserve localement (localStorage) jusqu'a la prochaine sauvegarde reussie.
- Le contenu est limite a 5 000 caracteres. Au-dela, la saisie est bloquee et un compteur de caracteres est affiche.

### RM-09 : Rafraichissement des donnees

- Les KPIs sont rafraichis automatiquement toutes les 5 minutes via un mecanisme de polling ou de WebSocket.
- La synthese financiere est rechargee uniquement lors du changement de filtre ou du chargement initial de la page.
- Le planning projet et la section "A venir" sont rechargees au chargement de la page et toutes les 15 minutes.
- Un rafraichissement manuel est possible via un bouton "Actualiser" (icone de rechargement) visible dans le bandeau superieur.

### RM-10 : Performance de chargement

- Le temps de chargement initial du tableau de bord (avec tous les widgets actifs) ne doit pas depasser **3 secondes** sur une connexion standard (10 Mbps).
- Les appels API pour les KPIs doivent repondre en moins de **500 ms**.
- Le graphique de synthese financiere doit se rendre en moins de **1 seconde** apres reception des donnees.

---

## 8. Criteres Globaux

### 8.1 Performance

| Critere | Seuil |
|---|---|
| Temps de chargement initial de la page (tous widgets actifs) | <= 3 secondes |
| Temps de reponse des API KPIs | <= 500 ms |
| Temps de rendu du graphique financier | <= 1 seconde |
| Frequence de rafraichissement automatique des KPIs | Toutes les 5 minutes |
| Frequence de rafraichissement du planning et de la sidebar | Toutes les 15 minutes |

### 8.2 Accessibilite

| Critere | Exigence |
|---|---|
| Conformite WCAG | Niveau AA minimum |
| Navigation clavier | Tous les elements interactifs (cartes KPI, graphique, toggles, liens) sont accessibles au clavier |
| Lecteur d'ecran | Les KPIs et les elements de la sidebar sont decrits par des labels ARIA semantiques |
| Contraste des couleurs | Ratio de contraste minimum de 4.5:1 pour le texte, 3:1 pour les elements graphiques |
| Textes alternatifs | Le graphique de synthese financiere propose une alternative textuelle (tableau de donnees accessible) |

### 8.3 Responsive Design

| Critere | Exigence |
|---|---|
| Desktop (>= 1280px) | Mise en page complete : 4 KPI cards en ligne, synthese financiere + planning a gauche, sidebar a droite |
| Tablette (768px - 1279px) | KPI cards sur 2 lignes de 2, sidebar sous le contenu principal |
| Mobile (< 768px) | KPI cards empilees verticalement, widgets empiles, sidebar sous le contenu principal |
| Graphique | Le graphique de synthese financiere s'adapte a la largeur du conteneur, les labels sont tronques si necessaire |

### 8.4 Securite

| Critere | Exigence |
|---|---|
| Authentification | Le tableau de bord n'est accessible qu'aux utilisateurs authentifies |
| Autorisation | Le filtrage par role est applique cote serveur (API) |
| Protection des donnees | Les notes personnelles sont chiffrees au repos (encryption at rest) |
| Injection | Les champs de saisie (bloc-notes) sont proteges contre les injections XSS |
| Audit | Les acces au tableau de bord sont traces dans les logs d'audit |

### 8.5 Compatibilite navigateurs

| Navigateur | Version minimale |
|---|---|
| Google Chrome | Version 100+ |
| Mozilla Firefox | Version 100+ |
| Microsoft Edge | Version 100+ |
| Safari | Version 15+ |

---

## 9. Definition of Done (DoD)

Un element (User Story, fonctionnalite) est considere comme **"Done"** lorsque l'ensemble des criteres suivants sont satisfaits :

### 9.1 Developpement

- [ ] Le code source est ecrit, revise (code review par au moins 1 pair) et merge dans la branche de developpement.
- [ ] Le code respecte les conventions de codage du projet (linting, formatage, nommage).
- [ ] Les composants front-end sont developpes en suivant le design system de l'application.
- [ ] Les appels API sont documentes (endpoints, parametres, reponses) dans la documentation OpenAPI/Swagger.
- [ ] Les cas d'erreur sont geres de maniere explicite (messages d'erreur utilisateur, logging cote serveur).

### 9.2 Tests

- [ ] Les tests unitaires sont ecrits et passent avec une couverture minimale de 80 % sur les fonctions metier (calcul des KPIs, filtrage par role, regles de fenetre temporelle).
- [ ] Les tests d'integration verifient les interactions entre le tableau de bord et les modules sources (Honoraires, Facturation, Temps, Finances, Projets).
- [ ] Les tests end-to-end (E2E) couvrent les parcours critiques : chargement du dashboard, interaction avec les KPIs, filtrage du graphique, personnalisation des widgets.
- [ ] Les tests de performance valident les seuils definis (chargement < 3s, API < 500ms).
- [ ] Les tests d'accessibilite (audit Lighthouse ou equivalent) atteignent un score minimum de 90/100.
- [ ] Les tests de compatibilite navigateurs sont effectues sur les 4 navigateurs cibles.

### 9.3 Documentation

- [ ] La documentation technique (architecture des composants, flux de donnees) est a jour.
- [ ] La documentation utilisateur (guide d'utilisation du tableau de bord) est redigee.
- [ ] Les release notes sont preparees pour la fonctionnalite.

### 9.4 Validation

- [ ] La fonctionnalite est validee par le Product Owner en environnement de recette.
- [ ] Les criteres d'acceptation de chaque User Story sont verifies et valides.
- [ ] La fonctionnalite est deployee en environnement de pre-production et testee.
- [ ] Aucun bug bloquant ou majeur n'est ouvert sur la fonctionnalite.

---

## 10. Dependances

### 10.1 Dependances fonctionnelles (modules OOTI)

| Dependance | Module source | Nature | Impact |
|---|---|---|---|
| DEP-01 | EPIC-002 Projets | Donnees projets actifs, avancement, jalons, taches | Bloquant pour US-TB04 (Planning projet) et US-TB05 (A venir : Jalons, Taches) |
| DEP-02 | EPIC-003 Honoraires | Montants facturables, budget previsionnel, CA planifie | Bloquant pour US-TB01 (KPI Facturable) et US-TB03 (Synthese financiere : CA planifie) |
| DEP-03 | EPIC-004 Facturation | Factures emises, soldes impayes, paiements | Bloquant pour US-TB01 (KPI Non paye) et US-TB03 (Synthese financiere : CA realise) |
| DEP-04 | EPIC-005 Temps | Temps saisis, temps theoriques | Bloquant pour US-TB01 (KPI Temps enregistre) |
| DEP-05 | EPIC-008 Finances | Couts realises, marges | Bloquant pour US-TB03 (Synthese financiere : Couts et Marge) |
| DEP-06 | Module RH / Conges | Conges approuves des collaborateurs | Bloquant pour US-TB05 (A venir : Conges) |
| DEP-07 | Module Calendrier | Evenements d'agence | Bloquant pour US-TB05 (A venir : Evenements) |
| DEP-08 | Module Utilisateurs / Roles | Roles et permissions des utilisateurs | Bloquant pour US-TB07 (Adaptation selon le role) |
| DEP-09 | Module Parametres | Logo de l'agence, devise principale, locale | Non bloquant (valeurs par defaut utilisees en l'absence) |

### 10.2 Dependances techniques

| Dependance | Nature | Impact |
|---|---|---|
| DEP-T01 | Bibliotheque de graphiques (ex : Chart.js, Recharts, D3.js) | Necessaire pour US-TB03 (graphique de synthese financiere) |
| DEP-T02 | Bibliotheque de diagramme de Gantt (ex : dhtmlxGantt, Frappe Gantt) | Necessaire pour US-TB04 (planning projet resume) |
| DEP-T03 | Editeur de texte riche leger (ex : Tiptap, Quill, Slate) | Necessaire pour US-TB02 (bloc-notes personnel) |
| DEP-T04 | Mecanisme de rafraichissement temps reel (WebSocket ou polling HTTP) | Necessaire pour US-TB01 (actualisation des KPIs) |
| DEP-T05 | API REST backend avec endpoints agreges pour le dashboard | Necessaire pour l'ensemble des US (performance des appels) |

### 10.3 Matrice de dependance entre User Stories

```
US-TB01 (KPIs)          --> DEP-02, DEP-03, DEP-04
US-TB02 (Bloc-notes)    --> Aucune dependance externe (stockage autonome)
US-TB03 (Synthese fin.) --> DEP-02, DEP-03, DEP-05
US-TB04 (Planning)      --> DEP-01
US-TB05 (A venir)       --> DEP-01, DEP-06, DEP-07
US-TB06 (Personnalis.)  --> Aucune dependance externe (stockage autonome)
US-TB07 (Roles)         --> DEP-08 + toutes les US precedentes
US-TB08 (Filtrage)      --> US-TB03 (prerequis)
```

---

## 11. Modele de Donnees

### 11.1 Entite : DashboardConfig

Configuration du tableau de bord propre a chaque utilisateur.

```
DashboardConfig
+-------------------+------------------+-------------------------------------------+
| Champ             | Type             | Description                               |
+-------------------+------------------+-------------------------------------------+
| id                | UUID (PK)        | Identifiant unique de la configuration    |
| user_id           | UUID (FK -> User)| Reference vers l'utilisateur proprietaire  |
| visible_widgets   | JSON (array)     | Liste des widgets actives (ex :            |
|                   |                  | ["facturable", "non_paye",                |
|                   |                  |  "temps_enregistre", "note",              |
|                   |                  |  "synthese_financiere",                   |
|                   |                  |  "planning_projet", "jalons",             |
|                   |                  |  "taches", "conges", "evenements"])        |
| note_content      | TEXT             | Contenu du bloc-notes personnel            |
|                   |                  | (max 5 000 caracteres, format HTML)        |
| note_updated_at   | TIMESTAMP        | Date de derniere modification de la note  |
| created_at        | TIMESTAMP        | Date de creation de la configuration      |
| updated_at        | TIMESTAMP        | Date de derniere modification             |
+-------------------+------------------+-------------------------------------------+
```

**Contraintes :**
- `user_id` est unique (un seul enregistrement DashboardConfig par utilisateur).
- `visible_widgets` contient par defaut les 10 widgets (configuration initiale).
- `note_content` est limite a 5 000 caracteres cote serveur (validation).

### 11.2 Entite : Widget (reference, non persistee en base)

Definition de la structure d'un widget cote application (objet de configuration).

```
Widget
+-------------------+------------------+-------------------------------------------+
| Champ             | Type             | Description                               |
+-------------------+------------------+-------------------------------------------+
| type              | ENUM             | Type du widget. Valeurs possibles :       |
|                   |                  | 'facturable', 'non_paye',                |
|                   |                  | 'temps_enregistre', 'note',              |
|                   |                  | 'synthese_financiere',                   |
|                   |                  | 'planning_projet', 'jalons',             |
|                   |                  | 'taches', 'conges', 'evenements'         |
| label             | STRING           | Libelle affiche a l'utilisateur           |
| data_source       | STRING           | Endpoint API fournissant les donnees     |
|                   |                  | (ex : /api/v1/dashboard/kpi/facturable)  |
| refresh_interval  | INTEGER          | Intervalle de rafraichissement en         |
|                   |                  | secondes (ex : 300 = 5 min)              |
| category          | ENUM             | Categorie du widget :                     |
|                   |                  | 'kpi', 'chart', 'planning', 'sidebar'   |
| default_visible   | BOOLEAN          | Visible par defaut (true/false)           |
| min_role          | ENUM             | Role minimum requis pour voir ce widget  |
|                   |                  | (null = tous les roles)                  |
+-------------------+------------------+-------------------------------------------+
```

### 11.3 Configuration des widgets (reference applicative)

| type | label | data_source | refresh_interval | category | default_visible |
|---|---|---|---|---|---|
| facturable | Facturable | /api/v1/dashboard/kpi/facturable | 300 | kpi | true |
| non_paye | Non paye | /api/v1/dashboard/kpi/non-paye | 300 | kpi | true |
| temps_enregistre | Temps enregistre | /api/v1/dashboard/kpi/temps | 300 | kpi | true |
| note | Note | /api/v1/dashboard/note | N/A | kpi | true |
| synthese_financiere | Synthese financiere | /api/v1/dashboard/finance/synthese | N/A | chart | true |
| planning_projet | Planning projet | /api/v1/dashboard/projets/planning | 900 | planning | true |
| jalons | Jalons cles | /api/v1/dashboard/a-venir/jalons | 900 | sidebar | true |
| taches | Taches | /api/v1/dashboard/a-venir/taches | 900 | sidebar | true |
| conges | Conges | /api/v1/dashboard/a-venir/conges | 900 | sidebar | true |
| evenements | Evenements | /api/v1/dashboard/a-venir/evenements | 900 | sidebar | true |

### 11.4 Endpoints API du tableau de bord

| Methode | Endpoint | Description | Parametres |
|---|---|---|---|
| GET | /api/v1/dashboard/config | Recuperer la configuration du dashboard de l'utilisateur | - |
| PATCH | /api/v1/dashboard/config | Mettre a jour la configuration (widgets visibles) | `{ visible_widgets: string[] }` |
| GET | /api/v1/dashboard/kpi/facturable | Recuperer le KPI facturable | - |
| GET | /api/v1/dashboard/kpi/non-paye | Recuperer le KPI impayes | - |
| GET | /api/v1/dashboard/kpi/temps | Recuperer le KPI temps enregistre | `?periode=semaine\|mois` |
| GET | /api/v1/dashboard/note | Recuperer le contenu du bloc-notes | - |
| PATCH | /api/v1/dashboard/note | Mettre a jour le contenu du bloc-notes | `{ content: string }` |
| GET | /api/v1/dashboard/finance/synthese | Recuperer les donnees de synthese financiere | `?annee=2026&periode=T1\|T2\|T3\|T4\|S1\|S2\|annee` |
| GET | /api/v1/dashboard/projets/planning | Recuperer le planning Gantt resume | `?limit=10` |
| GET | /api/v1/dashboard/a-venir/jalons | Recuperer les jalons a venir (14 jours) | - |
| GET | /api/v1/dashboard/a-venir/taches | Recuperer les taches a venir (14 jours) | - |
| GET | /api/v1/dashboard/a-venir/conges | Recuperer les conges a venir (14 jours) | - |
| GET | /api/v1/dashboard/a-venir/evenements | Recuperer les evenements a venir (14 jours) | - |

### 11.5 Diagramme de relations

```
+-----------+         +-------------------+
|   User    |1------1 | DashboardConfig   |
+-----------+         +-------------------+
| id (PK)   |         | id (PK)           |
| role      |         | user_id (FK)      |
| ...       |         | visible_widgets   |
+-----------+         | note_content      |
      |               | note_updated_at   |
      |               +-------------------+
      |
      |  (via API, filtrage par role)
      |
      +-------> EPIC-002 Projets (projets, jalons, taches)
      +-------> EPIC-003 Honoraires (montants facturables, CA planifie)
      +-------> EPIC-004 Facturation (factures, impayes, CA realise)
      +-------> EPIC-005 Temps (temps saisis, temps theoriques)
      +-------> EPIC-008 Finances (couts, marges)
```

---

## 12. Estimation

### 12.1 Estimation globale

| Parametre | Valeur |
|---|---|
| **Duree totale estimee** | 3 a 4 semaines |
| **Nombre de sprints** | 2 sprints (de 2 semaines chacun) |
| **Effort total estime** | 120 a 160 points d'effort (story points) |
| **Equipe recommandee** | 2 developpeurs front-end, 1 developpeur back-end, 1 designer UI/UX, 1 QA |

### 12.2 Estimation par User Story

| User Story | Complexite | Story Points | Sprint | Justification |
|---|---|---|---|---|
| US-TB01 : KPIs cles | Moyenne | 13 | Sprint 1 | 3 KPIs a developper, chacun avec un appel API dedie, formatage, indicateurs de couleur, navigation. Integration avec 3 modules sources differents. |
| US-TB02 : Bloc-notes | Faible | 8 | Sprint 1 | Integration d'un editeur de texte riche leger, sauvegarde automatique avec debounce, gestion du localStorage en fallback. Composant relativement autonome. |
| US-TB03 : Synthese financiere | Elevee | 21 | Sprint 1 | Integration d'une bibliotheque de graphiques, 6 series de donnees (3 indicateurs x planifie/realise), legende interactive, tooltips, responsivite. Agregation de donnees complexe cote API. |
| US-TB04 : Planning projet | Elevee | 21 | Sprint 1 | Integration d'une bibliotheque Gantt, calcul de l'avancement theorique vs reel, code couleur dynamique, tooltips riches, marqueur "aujourd'hui". Necessite un endpoint API agrege performant. |
| US-TB05 : Widgets "A venir" | Moyenne | 13 | Sprint 2 | 4 sous-sections a developper avec des sources de donnees differentes, filtrage temporel (14 jours), tri chronologique, liens de navigation. |
| US-TB06 : Personnalisation | Moyenne | 13 | Sprint 2 | Panneau de personnalisation (drawer/modal), 10 toggles, sauvegarde de la configuration, reactivite instantanee de l'interface, bouton de reinitialisation. |
| US-TB07 : Adaptation par role | Elevee | 21 | Sprint 2 | Filtrage cote serveur sur tous les endpoints API du dashboard (12 endpoints), tests de securite, verification de la non-fuite de donnees entre roles. Impact transversal sur toutes les US precedentes. |
| US-TB08 : Filtrage par periode | Faible | 8 | Sprint 2 | Selecteurs d'annee et de periode, rechargement du graphique avec indicateur de chargement. S'appuie sur l'infrastructure deja construite pour US-TB03. |

### 12.3 Repartition par sprint

#### Sprint 1 (Semaines 1-2) -- Fondations et composants principaux

| Tache | Effort | Responsable |
|---|---|---|
| Mise en place de la structure de page du tableau de bord (layout, grille, bandeau superieur, logo) | 5 pts | Front-end |
| Developpement des endpoints API pour les KPIs (facturable, non paye, temps) | 8 pts | Back-end |
| Developpement des 3 cartes KPI (front-end) | 8 pts | Front-end |
| Integration de l'editeur de texte riche et developpement du bloc-notes (US-TB02) | 8 pts | Front-end |
| Endpoint API pour le bloc-notes (GET/PATCH) | 3 pts | Back-end |
| Integration de la bibliotheque de graphiques et developpement de la synthese financiere (US-TB03) | 13 pts | Front-end |
| Endpoint API agrege pour la synthese financiere | 8 pts | Back-end |
| Integration de la bibliotheque Gantt et developpement du planning projet (US-TB04) | 13 pts | Front-end |
| Endpoint API agrege pour le planning projet | 8 pts | Back-end |
| Tests unitaires et d'integration Sprint 1 | 5 pts | QA + Dev |
| **Total Sprint 1** | **79 pts** | |

#### Sprint 2 (Semaines 3-4) -- Widgets complementaires, personnalisation et transversal

| Tache | Effort | Responsable |
|---|---|---|
| Developpement de la sidebar "A venir" avec les 4 sous-sections (US-TB05) | 8 pts | Front-end |
| Endpoints API pour les 4 sections "A venir" (jalons, taches, conges, evenements) | 5 pts | Back-end |
| Developpement du panneau de personnalisation des widgets (US-TB06) | 8 pts | Front-end |
| Endpoint API pour la configuration du dashboard (GET/PATCH) | 3 pts | Back-end |
| Implementation du filtrage par role sur tous les endpoints API (US-TB07) | 13 pts | Back-end |
| Adaptation front-end pour le filtrage par role | 5 pts | Front-end |
| Developpement des filtres de periode pour la synthese financiere (US-TB08) | 5 pts | Front-end |
| Mise en place du mecanisme de rafraichissement automatique (polling/WebSocket) | 5 pts | Full-stack |
| Tests unitaires, d'integration et E2E Sprint 2 | 8 pts | QA + Dev |
| Tests de performance et d'accessibilite | 5 pts | QA |
| Tests de compatibilite navigateurs | 3 pts | QA |
| Corrections de bugs et ajustements finaux | 5 pts | Dev |
| **Total Sprint 2** | **73 pts** | |

### 12.4 Risques identifies et impacts sur l'estimation

| Risque | Probabilite | Impact | Mitigation | Impact sur delai |
|---|---|---|---|---|
| Indisponibilite des API sources (Honoraires, Facturation, Temps, Finances) | Moyenne | Eleve | Developper avec des donnees mockees, prevoir des stubs API. Definir un contrat d'interface en amont avec les equipes des modules sources. | +3 a 5 jours |
| Complexite d'integration de la bibliotheque Gantt | Moyenne | Moyen | Realiser un POC en Sprint 0 pour valider le choix de la bibliotheque. Prevoir une solution de repli (barres de progression simples en CSS). | +2 a 3 jours |
| Performance insuffisante des endpoints agreges (temps de reponse > 500ms) | Faible | Eleve | Prevoir des mecanismes de cache cote serveur (Redis), pagination, et optimisation des requetes SQL. | +2 jours |
| Complexite du filtrage par role cote serveur | Moyenne | Moyen | Commencer par le developpement du filtrage des Sprint 1 pour anticiper les difficultes. | +2 a 3 jours |

### 12.5 Synthese des livrables par sprint

| Sprint | Livrables | Critere de validation |
|---|---|---|
| Sprint 1 | Page du tableau de bord avec KPIs, bloc-notes, synthese financiere et planning projet | Les 4 premieres US (TB01 a TB04) sont fonctionnelles et testees en environnement de developpement |
| Sprint 2 | Sidebar "A venir", personnalisation des widgets, filtrage par role, filtrage par periode, rafraichissement automatique | Les 4 US restantes (TB05 a TB08) sont fonctionnelles, le dashboard complet est teste en recette |

---

*Document redige par l'equipe Produit OOTI -- Version 1.0 -- Fevrier 2026*
*Revisions a planifier apres validation par le Product Owner et les parties prenantes techniques.*
