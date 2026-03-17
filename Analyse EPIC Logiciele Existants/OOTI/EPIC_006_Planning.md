# EPIC -- Module Planning & Disponibilite

**Application OOTI -- Gestion de projets pour cabinets d'architecture**
**Version 1.0 -- Fevrier 2026**

---

## 1. Identification de l'EPIC

| Champ | Valeur |
|---|---|
| **Nom** | Planning & Disponibilite |
| **Reference** | EPIC-006 |
| **Module parent** | Equipe |
| **Priorite** | Haute |
| **Statut** | A faire |
| **Responsable** | Chef de produit / Architecte logiciel |
| **EPICs lies** | EPIC-002 Projets, EPIC-005 Temps, EPIC-009 Collaborateurs |
| **Date de creation** | 26/02/2026 |
| **Derniere mise a jour** | 26/02/2026 |
| **Estimation globale** | 6 a 9 semaines (4-5 sprints) |

---

## 2. Contexte & Problematique

### 2.1 Contexte general

Dans un cabinet d'architecture, la gestion du planning et de la disponibilite des collaborateurs constitue un enjeu strategique majeur. Les equipes travaillent simultanement sur plusieurs projets aux temporalites differentes (concours, esquisse, APS, APD, PRO, DCE, chantier), et chaque collaborateur peut etre affecte a plusieurs missions en parallele. La capacite a planifier efficacement les ressources humaines conditionne directement la rentabilite de l'agence et la qualite des livrables.

### 2.2 Problematique

Les cabinets d'architecture font face a plusieurs difficultes recurrentes :

- **Manque de visibilite globale** : les dirigeants n'ont pas de vue consolidee de la charge de travail de l'ensemble des collaborateurs sur l'ensemble des projets. Les arbitrages d'affectation se font souvent de maniere informelle, sans donnees fiables.
- **Sur-charge et sous-charge non detectees** : certains collaborateurs se retrouvent en surcharge de travail (depassement de leur capacite hebdomadaire) tandis que d'autres sont sous-utilises, sans que la direction en soit informee en temps reel.
- **Absence de lien entre planning et budget** : le suivi de la consommation budgetaire par phase de projet n'est pas relie au planning previsionnel, ce qui empeche d'anticiper les depassements de budget.
- **Gestion manuelle des disponibilites** : les conges, jours feries, temps partiels et autres absences ne sont pas integres automatiquement dans le calcul de la capacite disponible, ce qui fausse les previsions de charge.
- **Pas de planning projet structure** : les phases de projet ne sont pas visualisees sur une timeline (Gantt), rendant difficile le suivi des delais et la coordination entre les differentes phases.
- **Difficulte d'anticipation** : sans outil de statistiques et de prevision, les agences ne peuvent pas anticiper les periodes de creux ou de pic d'activite pour ajuster leur strategie commerciale (reponse a de nouveaux concours, recrutement temporaire, etc.).

### 2.3 Contexte applicatif

Le module Planning & Disponibilite s'inscrit dans l'ecosysteme OOTI au sein de la section **EQUIPE** de la barre laterale. Il se compose de trois sous-menus : **Planning**, **Disponibilite** et **Statistiques**. Par ailleurs, au niveau de chaque projet (section **PROJETS**), un onglet **PLANNING** offre une vue Gantt specifique au projet avec des sous-onglets dedies : Planning (Gantt), Budget (consommation) et Ressources (collaborateurs affectes).

Ce module est etroitement lie a :
- **EPIC-002 Projets** : pour les phases, les dates et la structure des projets.
- **EPIC-005 Temps** : pour les heures realisees (saisie des temps) et la comparaison avec les heures planifiees.
- **EPIC-009 Collaborateurs** : pour les informations sur les employes, leurs contrats (temps plein/partiel), leurs competences et leurs conges.

---

## 3. Objectif de l'EPIC

### 3.1 Objectif principal

Fournir aux dirigeants, chefs de projet et collaborateurs d'un cabinet d'architecture un ensemble d'outils de planification, de gestion de la disponibilite et de suivi statistique permettant d'optimiser l'affectation des ressources humaines sur les projets, de visualiser la charge de travail en temps reel et d'anticiper les besoins futurs.

### 3.2 Objectifs specifiques

1. **Planification globale** : offrir une vue consolidee du planning de charge de tous les collaborateurs sur tous les projets, avec des capacites de filtrage, de tri et d'affectation par glisser-deposer.
2. **Gestion de la disponibilite** : calculer automatiquement la capacite disponible de chaque collaborateur en tenant compte de son contrat (temps plein, temps partiel), de ses conges et des jours feries.
3. **Suivi statistique** : fournir des indicateurs de performance (taux d'occupation, heures planifiees vs realisees, previsions de charge) pour eclairer les decisions strategiques.
4. **Planning projet (Gantt)** : permettre la visualisation et la gestion des phases de projet sur un diagramme de Gantt interactif, avec suivi budgetaire et suivi des ressources integres.
5. **Detection des anomalies** : alerter automatiquement en cas de sur-charge ou de sous-charge d'un collaborateur, ou en cas de depassement previsionnel du budget d'une phase.

### 3.3 Indicateurs de succes

| Indicateur | Cible |
|---|---|
| Taux d'adoption du planning par les chefs de projet | > 80% apres 3 mois |
| Reduction du temps de planification hebdomadaire | -50% par rapport au processus manuel |
| Precision des previsions de charge (planifie vs realise) | Ecart < 15% |
| Taux de detection anticipee des sur-charges | > 90% |
| Satisfaction utilisateur (module Planning) | > 4/5 |

---

## 4. Perimetre Fonctionnel

### 4.1 Planning Agence (niveau global)

#### 4.1.1 Vue Planning global

- Affichage d'un planning de charge consolide montrant tous les collaborateurs et tous les projets de l'agence.
- Axe vertical : liste des collaborateurs (groupables par equipe, service ou competence).
- Axe horizontal : echelle temporelle configurable (semaine, mois, trimestre).
- Chaque cellule indique le nombre d'heures planifiees pour un collaborateur donne sur une periode donnee, reparties par projet (code couleur).
- Barre de capacite visuelle : barre de progression montrant le ratio heures planifiees / capacite disponible pour chaque collaborateur et chaque periode.
- Code couleur pour les niveaux de charge : vert (< 80%), orange (80-100%), rouge (> 100%).

#### 4.1.2 Modes de vue

- **Vue par collaborateur** : le collaborateur est l'axe principal, les projets sont affiches en sous-lignes.
- **Vue par projet** : le projet est l'axe principal, les collaborateurs affectes sont affiches en sous-lignes.
- Basculement entre les deux vues via un selecteur.

#### 4.1.3 Affectation de ressources

- Affectation d'un collaborateur a un projet/phase par glisser-deposer (drag & drop) depuis un panneau lateral listant les collaborateurs disponibles.
- Formulaire d'affectation : selection du collaborateur, du projet, de la phase, de la periode (date de debut / date de fin), du nombre d'heures par semaine.
- Modification d'une affectation existante par redimensionnement (duree) ou deplacement (dates) directement sur le planning.
- Suppression d'une affectation avec confirmation.

#### 4.1.4 Filtres et recherche

- Filtre par collaborateur (multi-selection).
- Filtre par projet (multi-selection).
- Filtre par equipe ou service.
- Filtre par periode (date de debut / date de fin).
- Filtre par niveau de charge (sous-charge, charge normale, sur-charge).
- Recherche textuelle sur le nom du collaborateur ou du projet.

### 4.2 Disponibilite

#### 4.2.1 Vue des disponibilites

- Tableau affichant pour chaque collaborateur et chaque periode : la capacite totale (heures contractuelles), les heures d'absence (conges, jours feries, maladie), la capacite disponible nette, les heures deja planifiees, le solde disponible.
- Vue configurable par periode : semaine, mois, trimestre.
- Code couleur sur le solde disponible : vert (disponible), orange (presque plein), rouge (surcharge), gris (absent).

#### 4.2.2 Prise en compte des conges et absences

- Integration automatique des conges valides (provenant du module Collaborateurs / EPIC-009).
- Integration des jours feries selon le calendrier applicable (configurable par pays/region).
- Prise en compte du type de contrat : temps plein (base horaire standard configurable, ex. 35h, 39h, 40h), temps partiel (pourcentage ou nombre d'heures specifie).
- Types d'absence pris en compte : conges payes, RTT, conge maladie, conge maternite/paternite, conge sans solde, formation, autre absence.

#### 4.2.3 Calcul automatique de la capacite

- Formule : **Capacite disponible = Heures contractuelles - Heures d'absence (conges + jours feries)**
- Le calcul est effectue automatiquement pour chaque collaborateur et chaque periode.
- Mise a jour en temps reel lorsqu'un conge est ajoute, modifie ou supprime.

### 4.3 Statistiques Planning

#### 4.3.1 Taux d'occupation par collaborateur

- Calcul : **Taux d'occupation = Heures planifiees / Capacite disponible x 100**
- Affichage sous forme de tableau et de graphique (barres ou jauge).
- Filtrage par periode, par equipe, par projet.
- Classement des collaborateurs par taux d'occupation (croissant/decroissant).

#### 4.3.2 Taux d'occupation par projet

- Calcul : **Taux d'occupation projet = Heures planifiees sur le projet / Budget heures total du projet x 100**
- Vue de l'avancement de la consommation des heures par projet.
- Comparaison entre projets.

#### 4.3.3 Heures planifiees vs heures realisees

- Comparaison entre les heures planifiees (issues de ce module) et les heures reellement saisies (issues du module Temps / EPIC-005).
- Affichage sous forme de graphique (barres groupees : planifie vs realise).
- Calcul de l'ecart en heures et en pourcentage.
- Ventilation par collaborateur, par projet, par phase.

#### 4.3.4 Previsions de charge

- Projection de la charge future basee sur les affectations planifiees.
- Visualisation sur une timeline (prochaines semaines / prochains mois).
- Identification des periodes de pic et de creux.
- Aide a la decision pour le staffing et la reponse a de nouveaux projets.

### 4.4 Planning Projet (Gantt)

#### 4.4.1 Diagramme de Gantt interactif

- Affichage des phases du projet sous forme de barres horizontales sur une timeline.
- Axe vertical : liste des phases du projet (ordonnees selon la structure du projet).
- Axe horizontal : echelle temporelle (jours, semaines, mois) avec zoom.
- Barres redimensionnables et deplacables par glisser-deposer pour modifier les dates de debut/fin.
- Couleur des barres configurable par type de phase (esquisse, APS, APD, PRO, DCE, chantier, etc.).
- Affichage du pourcentage d'avancement sur chaque barre.

#### 4.4.2 Gestion des phases

- Creation, modification et suppression de phases directement depuis le Gantt.
- Champs : nom de la phase, date de debut, date de fin, duree (calculee automatiquement), budget heures, responsable.
- Liaisons entre phases (fin-debut, debut-debut) avec visualisation des dependances par des fleches.
- Decalage automatique des phases dependantes en cas de modification d'une phase amont (optionnel, activable).

#### 4.4.3 Jalons (Milestones)

- Ajout de jalons sur la timeline (losanges ou marqueurs visuels).
- Champs : titre du jalon, date, description, statut (a venir, en cours, atteint, en retard).
- Les jalons sont affiches sur le Gantt avec une icone distinctive.
- Alerte visuelle lorsqu'un jalon est en retard (date depassee et statut non "atteint").

#### 4.4.4 Vue Budget (sous-onglet)

- Affichage de la consommation budgetaire par phase dans le temps.
- Graphique empile montrant pour chaque phase : budget initial, heures consommees, heures restantes.
- Indicateur de depassement budgetaire par phase (code couleur).
- Courbe d'avancement (S-curve) : comparaison entre la consommation prevue et la consommation reelle.

#### 4.4.5 Vue Ressources (sous-onglet)

- Affichage des collaborateurs affectes a chaque phase du projet.
- Pour chaque affectation : nom du collaborateur, role, heures planifiees par semaine, periode.
- Possibilite d'ajouter ou retirer un collaborateur d'une phase.
- Visualisation de la charge par collaborateur sur le projet (barre de charge).

#### 4.4.6 Modes d'affichage

- **Vue Planning** : le diagramme de Gantt interactif (vue par defaut).
- **Vue Tableau** : liste tabulaire des phases avec colonnes triables (nom, dates, duree, budget, avancement, responsable).
- Basculement entre les deux vues via un toggle.

#### 4.4.7 Outils du Gantt

- **Zoom** : zoom avant/arriere sur l'echelle temporelle (jour, semaine, mois, trimestre, annee).
- **Plein ecran** : mode plein ecran pour une meilleure visualisation.
- **Aujourd'hui** : bouton pour recentrer la vue sur la date du jour.
- **Export** : export du Gantt en PDF, PNG ou CSV.
- **Filtres** : filtre par phase, par statut de phase, par responsable.
- **Impression** : mise en page optimisee pour l'impression.

---

## 5. User Stories

### US-PL01 -- Planning global de l'agence

**En tant que** dirigeant ou chef de projet,
**je veux** visualiser le planning de charge de tous les collaborateurs de l'agence sur tous les projets,
**afin de** disposer d'une vue d'ensemble me permettant de prendre des decisions eclairees sur l'affectation des ressources et d'identifier rapidement les desequilibres de charge.

#### Criteres d'acceptance

1. **CA-01** : Le planning global affiche sur l'axe vertical la liste de tous les collaborateurs actifs de l'agence, et sur l'axe horizontal une echelle temporelle. Chaque cellule indique le nombre total d'heures planifiees pour le collaborateur sur la periode donnee.
2. **CA-02** : L'utilisateur peut choisir la granularite temporelle parmi : semaine, mois, trimestre. Le changement de granularite met a jour l'affichage en moins de 2 secondes.
3. **CA-03** : Pour chaque collaborateur et chaque periode, une barre de progression visuelle indique le ratio heures planifiees / capacite disponible. Le code couleur est applique : vert (< 80% de la capacite), orange (80-100%), rouge (> 100%).
4. **CA-04** : Les heures planifiees sont ventilees par projet avec un code couleur distinct par projet. Au survol d'une cellule, un tooltip affiche le detail : nom du projet, phase, heures planifiees.
5. **CA-05** : L'utilisateur peut basculer entre la vue "par collaborateur" (collaborateurs en lignes, projets en sous-lignes) et la vue "par projet" (projets en lignes, collaborateurs en sous-lignes) via un selecteur.
6. **CA-06** : Des filtres sont disponibles : par collaborateur (multi-selection), par projet (multi-selection), par equipe/service, par periode (date debut/fin), par niveau de charge. Les filtres sont combinables et s'appliquent instantanement.
7. **CA-07** : Une barre de recherche permet de rechercher un collaborateur ou un projet par son nom. Les resultats filtrent le planning en temps reel a mesure de la saisie.
8. **CA-08** : Le planning se charge en moins de 3 secondes pour une agence de 50 collaborateurs et 100 projets actifs.

---

### US-PL02 -- Affectation de ressources sur les projets

**En tant que** chef de projet ou dirigeant,
**je veux** affecter des collaborateurs a des projets et des phases via le planning global,
**afin de** planifier la charge de travail de maniere visuelle et intuitive, et m'assurer que chaque projet dispose des ressources necessaires.

#### Criteres d'acceptance

1. **CA-01** : Un panneau lateral affiche la liste des collaborateurs disponibles, avec pour chacun son nom, son poste, sa photo et son taux de charge actuel sur la periode visible.
2. **CA-02** : L'utilisateur peut creer une affectation par glisser-deposer (drag & drop) d'un collaborateur depuis le panneau lateral vers une cellule du planning (intersection collaborateur/periode/projet).
3. **CA-03** : A la suite du glisser-deposer, un formulaire d'affectation s'ouvre avec les champs pre-remplis : collaborateur, projet (a selectionner si non pre-determine), phase (liste deroulante des phases du projet), date de debut, date de fin, heures par semaine. L'utilisateur confirme ou ajuste les valeurs.
4. **CA-04** : Une affectation existante peut etre modifiee directement sur le planning : redimensionnement horizontal pour changer la duree, deplacement pour changer les dates, double-clic pour ouvrir le formulaire d'edition.
5. **CA-05** : La suppression d'une affectation necessite une confirmation ("Etes-vous sur de vouloir supprimer cette affectation ?"). La suppression est immediate apres confirmation.
6. **CA-06** : Lors de la creation ou modification d'une affectation, le systeme verifie en temps reel si le collaborateur depasse sa capacite disponible sur la periode concernee. Si c'est le cas, un avertissement visuel est affiche (icone + message) mais l'affectation reste possible (avertissement, pas blocage).
7. **CA-07** : Les modifications d'affectation sont sauvegardees automatiquement (auto-save) et le planning se met a jour immediatement pour tous les utilisateurs connectes (mise a jour en temps reel ou au rechargement).
8. **CA-08** : L'historique des modifications d'affectation est conserve : date de modification, utilisateur ayant effectue la modification, valeurs avant/apres.

---

### US-PL03 -- Vue Disponibilite des collaborateurs

**En tant que** dirigeant ou responsable des ressources humaines,
**je veux** visualiser la disponibilite de chaque collaborateur en tenant compte de sa capacite contractuelle, de ses conges et des jours feries,
**afin de** connaitre precisement le temps disponible de chacun avant de proceder a des affectations.

#### Criteres d'acceptance

1. **CA-01** : La vue Disponibilite affiche un tableau avec en lignes les collaborateurs et en colonnes les periodes (semaines, mois ou trimestres selon le choix de l'utilisateur).
2. **CA-02** : Pour chaque cellule (collaborateur x periode), les informations suivantes sont affichees : capacite totale (heures contractuelles), heures d'absence (conges + jours feries), capacite disponible nette, heures deja planifiees, solde disponible (capacite nette - heures planifiees).
3. **CA-03** : Le solde disponible est mis en evidence par un code couleur : vert (solde > 20% de la capacite), orange (solde entre 0% et 20%), rouge (solde negatif = surcharge), gris (collaborateur totalement absent sur la periode).
4. **CA-04** : Les conges valides issus du module Collaborateurs (EPIC-009) sont automatiquement integres dans le calcul. Toute modification de conge se repercute immediatement sur la vue Disponibilite.
5. **CA-05** : Les jours feries sont pris en compte selon le calendrier configure pour l'agence (pays/region). Les jours feries reduisent proportionnellement la capacite de la periode.
6. **CA-06** : Le type de contrat du collaborateur est pris en compte : un collaborateur a temps partiel (ex. 80%) voit sa capacite calculee au prorata (ex. 28h/semaine pour une base 35h).
7. **CA-07** : L'utilisateur peut filtrer par equipe, par type de contrat (temps plein / temps partiel), par disponibilite (uniquement les collaborateurs ayant du solde disponible).
8. **CA-08** : Un clic sur une cellule ouvre le detail de la disponibilite du collaborateur sur la periode : liste des jours, heures contractuelles par jour, absences par jour (avec type d'absence), heures planifiees par jour (avec detail des projets).

---

### US-PL04 -- Gestion des conges et absences dans le planning

**En tant que** chef de projet,
**je veux** que les conges et absences des collaborateurs soient automatiquement refletes dans le planning de charge,
**afin de** ne pas affecter un collaborateur sur une periode ou il est absent et d'avoir des previsions de charge fiables.

#### Criteres d'acceptance

1. **CA-01** : Lorsqu'un conge est valide dans le module Collaborateurs (EPIC-009), il apparait automatiquement dans le planning global sous forme d'une barre distincte (hachures ou couleur specifique, ex. gris clair) sur la ligne du collaborateur concerne, pour la periode du conge.
2. **CA-02** : Les types d'absence sont differencies visuellement : conges payes (bleu clair), RTT (violet), maladie (rouge clair), formation (jaune), autre (gris). La legende est accessible en permanence.
3. **CA-03** : Si un collaborateur a une affectation existante sur une periode ou un conge est ensuite valide, le systeme genere une alerte visuelle sur l'affectation concernee indiquant un conflit.
4. **CA-04** : Le detail du conflit est accessible : "Le collaborateur [Nom] est en conge du [date] au [date] mais est affecte au projet [Nom] pour [X] heures/semaine sur cette periode."
5. **CA-05** : Les jours feries sont affiches sur l'axe temporel du planning (colonnes grisees ou marqueurs verticaux) pour tous les collaborateurs.
6. **CA-06** : La capacite disponible du collaborateur est recalculee automatiquement a chaque ajout, modification ou suppression de conge, et le planning se met a jour en consequence.
7. **CA-07** : L'utilisateur peut visualiser depuis le planning le calendrier d'absences d'un collaborateur en cliquant sur son nom (panneau lateral ou popup).
8. **CA-08** : Un recapitulatif des conflits actifs (affectations sur periodes de conge) est accessible depuis un bouton/icone dedie dans la barre d'outils du planning.

---

### US-PL05 -- Statistiques de planning (taux d'occupation)

**En tant que** dirigeant d'agence,
**je veux** consulter des statistiques sur le taux d'occupation des collaborateurs et des projets,
**afin d'** evaluer l'efficacite de l'utilisation des ressources, identifier les desequilibres et prendre des decisions strategiques (recrutement, reponse a de nouveaux concours, etc.).

#### Criteres d'acceptance

1. **CA-01** : Un tableau de bord "Statistiques Planning" affiche les indicateurs principaux : taux d'occupation moyen de l'agence, nombre de collaborateurs en surcharge (> 100%), nombre de collaborateurs en sous-charge (< 50%), nombre de projets en depassement budgetaire previsionnel.
2. **CA-02** : Le taux d'occupation par collaborateur est affiche sous forme de tableau triable et de graphique a barres horizontales. La formule est : Heures planifiees / Capacite disponible x 100. Le code couleur s'applique (vert/orange/rouge).
3. **CA-03** : Le taux d'occupation par projet est affiche sous forme de tableau et de graphique : Heures planifiees totales sur le projet / Budget heures total x 100. Un indicateur montre si le projet risque de depasser son budget.
4. **CA-04** : Un graphique "Planifie vs Realise" affiche pour une periode donnee (semaine, mois, trimestre) les heures planifiees et les heures reellement saisies (provenant du module Temps / EPIC-005), sous forme de barres groupees. L'ecart est calcule en heures et en pourcentage.
5. **CA-05** : La ventilation "Planifie vs Realise" est disponible par collaborateur, par projet et par phase. L'utilisateur peut naviguer entre ces niveaux de detail.
6. **CA-06** : Un graphique de prevision de charge affiche la charge planifiee sur les prochaines semaines/mois, permettant d'identifier les periodes de pic et de creux. La capacite totale de l'agence est representee par une ligne horizontale de reference.
7. **CA-07** : Tous les graphiques et tableaux sont filtrables par periode (date debut/fin), par equipe, par projet. Les filtres sont combinables.
8. **CA-08** : Les donnees statistiques sont exportables en CSV et PDF. L'export PDF inclut les graphiques.

---

### US-PL06 -- Planning Gantt d'un projet

**En tant que** chef de projet,
**je veux** visualiser et gerer les phases de mon projet sur un diagramme de Gantt interactif,
**afin de** planifier les differentes etapes du projet, suivre leur avancement et communiquer le planning aux parties prenantes.

#### Criteres d'acceptance

1. **CA-01** : Le diagramme de Gantt affiche sur l'axe vertical la liste des phases du projet (dans l'ordre defini par la structure du projet) et sur l'axe horizontal une echelle temporelle. Chaque phase est representee par une barre horizontale allant de sa date de debut a sa date de fin.
2. **CA-02** : L'utilisateur peut modifier les dates d'une phase directement sur le Gantt : deplacement de la barre (change les dates de debut et fin), redimensionnement a gauche (change la date de debut), redimensionnement a droite (change la date de fin). La duree est recalculee automatiquement.
3. **CA-03** : L'utilisateur peut creer une nouvelle phase directement depuis le Gantt via un bouton "+ Ajouter une phase" ou par double-clic sur une zone vide. Le formulaire de creation comporte : nom, date de debut, date de fin, budget heures, responsable, couleur.
4. **CA-04** : Chaque barre de phase affiche son nom et son pourcentage d'avancement. Le pourcentage est calcule automatiquement a partir des heures realisees / heures budgetees (donnees du module Temps).
5. **CA-05** : Les barres de phases sont colorees selon le type de phase (configurable) : esquisse, APS, APD, PRO, DCE, chantier, etc. La legende des couleurs est affichee.
6. **CA-06** : Les dependances entre phases (liens fin-debut) sont representees par des fleches entre les barres. L'utilisateur peut creer un lien en cliquant sur le bord droit d'une phase et en tirant vers le bord gauche d'une autre phase.
7. **CA-07** : L'utilisateur peut basculer entre la "Vue Planning" (Gantt) et la "Vue Tableau" (liste tabulaire des phases avec colonnes : nom, date debut, date fin, duree, budget, avancement, responsable, statut). Les deux vues sont synchronisees.
8. **CA-08** : Des outils de zoom sont disponibles : zoom avant/arriere (boutons + molette), presets de zoom (jour, semaine, mois, trimestre, annee), bouton "Aujourd'hui" pour recentrer la vue sur la date du jour. Un mode plein ecran est disponible.

---

### US-PL07 -- Gestion des jalons

**En tant que** chef de projet,
**je veux** definir et suivre des jalons (milestones) sur le planning de mon projet,
**afin de** marquer les dates cles du projet (reunions client, depots de permis, jurys de concours, livraisons) et suivre leur respect.

#### Criteres d'acceptance

1. **CA-01** : L'utilisateur peut ajouter un jalon sur le Gantt en cliquant sur un bouton dedie ou en effectuant un clic droit sur la timeline. Le formulaire de creation comporte : titre (obligatoire), date (obligatoire), description (optionnelle), couleur ou icone (optionnel).
2. **CA-02** : Les jalons sont affiches sur le Gantt sous forme de losanges (ou marqueurs en forme de diamant) positionnes a la date du jalon, distincts visuellement des barres de phase.
3. **CA-03** : Chaque jalon possede un statut : "A venir" (date future), "Atteint" (marque manuellement comme atteint), "En retard" (date depassee et statut non "Atteint"). Le statut "En retard" est determine automatiquement par le systeme.
4. **CA-04** : Les jalons en retard sont mis en evidence visuellement : couleur rouge, icone d'avertissement. Un compteur de jalons en retard est affiche dans la barre d'outils du Gantt.
5. **CA-05** : L'utilisateur peut modifier un jalon (titre, date, description, statut) par double-clic sur le losange ou via un menu contextuel.
6. **CA-06** : L'utilisateur peut supprimer un jalon avec une confirmation prealable.
7. **CA-07** : Les jalons sont visibles dans la vue Tableau sous forme de lignes distinctes (icone de jalon dans la colonne type).
8. **CA-08** : Les jalons sont inclus dans l'export PDF/PNG du Gantt avec leur titre et leur date.

---

### US-PL08 -- Vue Budget du planning projet

**En tant que** chef de projet ou directeur financier,
**je veux** visualiser la consommation budgetaire de chaque phase du projet dans le temps, directement depuis le planning,
**afin de** suivre l'avancement financier du projet, detecter les depassements et prendre des mesures correctives.

#### Criteres d'acceptance

1. **CA-01** : Le sous-onglet "Budget" du planning projet affiche un graphique empile (stacked bar chart) montrant pour chaque phase du projet : le budget initial (en heures), les heures consommees a date, les heures restantes estimees.
2. **CA-02** : Un code couleur indique l'etat budgetaire de chaque phase : vert (consommation < 80% du budget), orange (80-100%), rouge (> 100% = depassement).
3. **CA-03** : Une courbe d'avancement (S-curve) est affichee, comparant la courbe de consommation prevue (lineaire ou pondree) et la courbe de consommation reelle. L'ecart entre les deux courbes est visible.
4. **CA-04** : Les heures consommees proviennent du module Temps (EPIC-005) et sont mises a jour automatiquement. La derniere date de mise a jour est affichee.
5. **CA-05** : Un tableau recapitulatif accompagne le graphique : phase, budget heures, heures consommees, heures restantes, pourcentage consomme, ecart (heures), ecart (%).
6. **CA-06** : L'utilisateur peut cliquer sur une phase pour voir le detail de la consommation : ventilation par collaborateur, par semaine/mois.
7. **CA-07** : Un indicateur de projection est affiche : "Au rythme actuel, le budget de la phase [X] sera epuise le [date]", calcule a partir de la vitesse de consommation moyenne.
8. **CA-08** : Les donnees budgetaires sont exportables en CSV et PDF.

---

### US-PL09 -- Vue Ressources du planning projet

**En tant que** chef de projet,
**je veux** visualiser et gerer les collaborateurs affectes a chaque phase de mon projet,
**afin de** m'assurer que chaque phase dispose des competences necessaires et que la charge est bien repartie.

#### Criteres d'acceptance

1. **CA-01** : Le sous-onglet "Ressources" du planning projet affiche la liste des collaborateurs affectes au projet, groupes par phase.
2. **CA-02** : Pour chaque affectation, les informations suivantes sont visibles : nom du collaborateur, role/poste, phase, date de debut et de fin de l'affectation, heures planifiees par semaine, total heures planifiees sur la periode.
3. **CA-03** : L'utilisateur peut ajouter un collaborateur a une phase via un bouton "+ Ajouter une ressource" qui ouvre un formulaire : selection du collaborateur (liste deroulante avec recherche), phase, dates, heures par semaine.
4. **CA-04** : L'utilisateur peut modifier une affectation existante (dates, heures par semaine) ou la supprimer (avec confirmation).
5. **CA-05** : Une barre de charge par collaborateur est affichee, montrant pour chaque collaborateur du projet la repartition de sa charge entre les differentes phases (barre empilee).
6. **CA-06** : Si un collaborateur affecte au projet est en surcharge (toutes affectations confondues, tous projets), un indicateur d'avertissement est affiche a cote de son nom.
7. **CA-07** : Le total des heures planifiees par phase est compare au budget de la phase. Un indicateur visuel montre si les ressources planifiees depassent le budget (rouge) ou sont en-dessous (vert).
8. **CA-08** : L'utilisateur peut voir la disponibilite d'un collaborateur en cliquant sur son nom (ouverture d'un panneau montrant sa charge sur tous les projets pour la periode).

---

### US-PL10 -- Export et partage du planning

**En tant que** chef de projet,
**je veux** exporter et partager le planning de mon projet,
**afin de** communiquer le planning aux clients, aux partenaires (BET, economistes) et aux equipes internes qui n'ont pas acces a l'outil.

#### Criteres d'acceptance

1. **CA-01** : L'utilisateur peut exporter le diagramme de Gantt au format PDF. Le PDF est genere en mode paysage, avec une mise en page optimisee incluant le titre du projet, la date d'export, la legende des couleurs et les jalons.
2. **CA-02** : L'utilisateur peut exporter le diagramme de Gantt au format PNG (image haute resolution, minimum 150 DPI).
3. **CA-03** : L'utilisateur peut exporter les donnees du planning au format CSV : une ligne par phase avec les colonnes nom, date debut, date fin, duree, budget heures, heures realisees, avancement, responsable.
4. **CA-04** : L'export PDF et PNG respecte les filtres appliques : si l'utilisateur a filtre certaines phases, seules les phases filtrees sont exportees.
5. **CA-05** : Un mode impression est disponible, ouvrant un apercu avant impression avec des options de mise en page (orientation, echelle, inclusion/exclusion des jalons, inclusion/exclusion de la legende).
6. **CA-06** : L'utilisateur peut generer un lien de partage en lecture seule du planning (URL unique securisee) valide pour une duree configurable (24h, 7 jours, 30 jours, permanent). Ce lien est accessible sans connexion a l'application.
7. **CA-07** : L'export inclut optionnellement la vue Budget et/ou la vue Ressources en pages supplementaires du PDF.
8. **CA-08** : L'historique des exports est conserve : date, format, utilisateur ayant exporte.

---

### US-PL11 -- Detection de sur-charge / sous-charge

**En tant que** dirigeant ou responsable des ressources,
**je veux** etre alerte automatiquement lorsqu'un collaborateur est en situation de sur-charge ou de sous-charge,
**afin de** reagir rapidement pour reequilibrer la charge de travail et preserver la sante des equipes tout en optimisant l'utilisation des ressources.

#### Criteres d'acceptance

1. **CA-01** : Le systeme detecte automatiquement les situations de sur-charge : un collaborateur est considere en sur-charge lorsque ses heures planifiees depassent sa capacite disponible (> 100%) sur une periode donnee (semaine ou mois).
2. **CA-02** : Le systeme detecte automatiquement les situations de sous-charge : un collaborateur est considere en sous-charge lorsque ses heures planifiees representent moins de 50% de sa capacite disponible sur une periode donnee.
3. **CA-03** : Les seuils de sur-charge (defaut : 100%) et de sous-charge (defaut : 50%) sont configurables par l'administrateur dans les parametres du module.
4. **CA-04** : Sur le planning global, les collaborateurs en sur-charge sont mis en evidence : barre rouge, icone d'avertissement, mise en surbrillance de la ligne.
5. **CA-05** : Sur le planning global, les collaborateurs en sous-charge sont mis en evidence : barre verte pale, icone informative, mise en surbrillance de la ligne.
6. **CA-06** : Un panneau "Alertes de charge" est accessible depuis la barre d'outils du planning. Il liste toutes les situations de sur-charge et de sous-charge actives et futures (sur les 4 prochaines semaines), avec pour chacune : nom du collaborateur, periode concernee, taux de charge, detail des affectations.
7. **CA-07** : Des notifications (in-app et optionnellement par email) sont envoyees aux dirigeants et chefs de projet concernes lorsqu'une nouvelle situation de sur-charge est detectee. La frequence des notifications est configurable (temps reel, quotidien, hebdomadaire).
8. **CA-08** : L'utilisateur peut directement depuis le panneau d'alertes acceder a l'affectation problematique pour la modifier (rediriger vers le formulaire d'edition de l'affectation).

---

## 6. Hors Perimetre

Les elements suivants sont explicitement exclus du perimetre de cet EPIC :

| # | Element exclu | Justification |
|---|---|---|
| 1 | **Gestion des conges** (demande, validation, solde) | Traite dans EPIC-009 Collaborateurs. Le present EPIC consomme les donnees de conges mais ne les gere pas. |
| 2 | **Saisie des temps** (timesheet) | Traite dans EPIC-005 Temps. Le present EPIC consomme les heures realisees pour comparaison avec les heures planifiees. |
| 3 | **Gestion des competences et profils de poste** | Pourra faire l'objet d'un EPIC dedie. Le planning n'integre pas de filtre par competence dans cette version. |
| 4 | **Planning automatique / optimisation algorithmique** | L'affectation des ressources est manuelle. Pas d'algorithme d'optimisation automatique dans cette version. |
| 5 | **Gestion multi-agences** | Le planning couvre une seule agence. La consolidation multi-agences n'est pas prevue dans cette version. |
| 6 | **Integration calendrier externe** (Google Calendar, Outlook) | Pourra etre ajoutee dans une version ulterieure. |
| 7 | **Gestion des dependances inter-projets** | Les dependances sont gerees au sein d'un meme projet (entre phases). Les dependances entre projets differents sont hors perimetre. |
| 8 | **Application mobile dediee au planning** | Le module est accessible via le navigateur web (responsive). Une application mobile native n'est pas prevue. |
| 9 | **Planification financiere** (facturation, honoraires) | Traite dans EPIC-003 Honoraires. La vue Budget du planning ne couvre que la consommation en heures, pas la facturation. |

---

## 7. Regles Metier

### RM-01 : Calcul de la capacite disponible

La capacite disponible d'un collaborateur pour une periode donnee est calculee selon la formule :

```
Capacite disponible = (Jours ouvrables de la periode - Jours d'absence) x Heures par jour contractuelles
```

- **Jours ouvrables** : jours de la semaine (lundi-vendredi) moins les jours feries applicables.
- **Jours d'absence** : conges payes, RTT, maladie, formation, et toute autre absence validee.
- **Heures par jour contractuelles** : definies par le contrat du collaborateur (ex. 7h pour un temps plein a 35h/semaine, 8h pour 40h/semaine). Pour un temps partiel, le prorata s'applique.

### RM-02 : Seuils de charge

| Seuil | Valeur par defaut | Configurable | Comportement |
|---|---|---|---|
| Sous-charge | < 50% de la capacite | Oui (0-100%) | Indicateur visuel informatif (bleu/vert pale) |
| Charge normale | 50% - 100% de la capacite | Non (derive des seuils) | Pas d'alerte |
| Sur-charge | > 100% de la capacite | Oui (100-200%) | Alerte visuelle + notification |
| Sur-charge critique | > 120% de la capacite | Oui (100-200%) | Alerte rouge + notification urgente |

### RM-03 : Granularite des affectations

- L'unite minimale d'affectation est de **0.5 heure par semaine**.
- Une affectation ne peut pas etre inferieure a **1 semaine** de duree.
- Les affectations sont definies en **heures par semaine** et s'appliquent uniformement sur toute la duree de l'affectation (sauf jours d'absence).

### RM-04 : Coherence des dates

- La date de fin d'une affectation doit etre superieure ou egale a la date de debut.
- La date de fin d'une phase ne peut pas etre anterieure a la date de debut.
- Un jalon ne peut pas etre place avant la date de debut du projet ni apres la date de fin du projet.
- Les dates des phases doivent etre coherentes avec les dates du projet (contenues dans l'intervalle du projet).

### RM-05 : Dependances entre phases

- Seules les dependances de type **Fin-Debut** (FS : Finish-to-Start) et **Debut-Debut** (SS : Start-to-Start) sont supportees dans cette version.
- Lorsqu'une phase amont est decalee, les phases dependantes sont decalees automatiquement (si l'option est activee dans les parametres du projet).
- Le decalage automatique respecte les dependances en cascade (propagation).
- Les dependances circulaires sont interdites : le systeme refuse la creation d'un lien qui creerait un cycle.

### RM-06 : Droits d'acces

| Role | Voir planning global | Modifier affectations | Voir disponibilite | Voir statistiques | Gerer Gantt projet |
|---|---|---|---|---|---|
| Administrateur | Oui | Oui | Oui | Oui | Oui |
| Dirigeant | Oui | Oui | Oui | Oui | Oui |
| Chef de projet | Oui | Oui (ses projets) | Oui | Oui | Oui (ses projets) |
| Collaborateur | Ses affectations | Non | Sa disponibilite | Non | Lecture seule |

### RM-07 : Calcul du taux d'avancement d'une phase

```
Avancement (%) = Heures realisees sur la phase / Budget heures de la phase x 100
```

- Les heures realisees proviennent du module Temps (EPIC-005).
- Si le budget heures est a 0 ou non defini, l'avancement affiche "N/A".
- L'avancement peut depasser 100% (depassement budgetaire).

### RM-08 : Lien de partage securise

- Les liens de partage sont generes avec un token unique (UUID v4).
- L'acces via un lien de partage est en lecture seule : pas de modification possible.
- Le lien expire a la date configuree. Apres expiration, l'acces affiche un message "Ce lien a expire".
- Un lien peut etre revoque manuellement par l'utilisateur qui l'a cree ou par un administrateur.

### RM-09 : Jours feries

- La liste des jours feries est configurable par l'administrateur dans les parametres de l'agence.
- Plusieurs calendriers de jours feries peuvent coexister (ex. France metropolitaine, DOM-TOM, Suisse, Belgique).
- Chaque collaborateur est rattache a un calendrier de jours feries via son profil.
- Les jours feries tombant un samedi ou dimanche ne reduisent pas la capacite (ils ne sont pas travailles de toute facon).

---

## 8. Criteres d'Acceptance Globaux

### 8.1 Performance

| Critere | Cible |
|---|---|
| Temps de chargement du planning global (50 collaborateurs, 100 projets) | < 3 secondes |
| Temps de chargement du Gantt projet (20 phases, 10 jalons) | < 2 secondes |
| Temps de reponse d'une operation de drag & drop (affectation) | < 500 millisecondes |
| Temps de generation d'un export PDF du Gantt | < 5 secondes |
| Temps de calcul des statistiques (1 an de donnees) | < 3 secondes |

### 8.2 Ergonomie et accessibilite

- L'interface du planning est responsive : utilisable sur desktop (resolution minimale 1280x720) et tablette (resolution minimale 1024x768).
- Le drag & drop fonctionne a la souris et au tactile (tablette).
- Les codes couleur sont accompagnes d'icones ou de motifs pour les utilisateurs daltoniens.
- Les raccourcis clavier sont disponibles pour les operations frequentes : zoom (Ctrl + / Ctrl -), plein ecran (F11), aujourd'hui (T), nouvelle phase (N).
- Les tooltips fournissent des informations contextuelles au survol de chaque element du planning.

### 8.3 Coherence des donnees

- Les donnees du planning sont coherentes en temps reel avec les donnees des modules lies (Projets, Temps, Collaborateurs).
- La suppression d'un projet entraine la suppression de toutes les affectations associees (avec confirmation).
- La suppression d'un collaborateur entraine la suppression de toutes ses affectations (avec confirmation et avertissement sur l'impact).
- La modification des dates d'un projet met a jour les contraintes du Gantt (les phases ne peuvent pas depasser les dates du projet).

### 8.4 Securite

- Les liens de partage ne donnent acces qu'aux donnees du planning du projet concerne, pas aux autres donnees du projet ni de l'agence.
- Les droits d'acces sont verifies a chaque requete API (pas uniquement cote interface).
- Les operations sensibles (suppression d'affectation, modification en masse) sont tracees dans les logs d'audit.

---

## 9. Definition of Done

Un item (User Story ou tache technique) est considere comme "Done" lorsque tous les criteres suivants sont satisfaits :

| # | Critere | Detail |
|---|---|---|
| 1 | **Code developpe** | Le code source est ecrit, respecte les conventions du projet et est versionne sur le depot Git. |
| 2 | **Revue de code** | Le code a ete revu par au moins un autre developpeur (merge/pull request approuvee). |
| 3 | **Tests unitaires** | Les tests unitaires couvrent au minimum 80% du code metier (calculs de capacite, seuils, dependances). |
| 4 | **Tests d'integration** | Les interactions avec les modules lies (Projets, Temps, Collaborateurs) sont testees. |
| 5 | **Tests E2E** | Les parcours utilisateur principaux (creation d'affectation, modification sur le Gantt, export) sont couverts par des tests end-to-end. |
| 6 | **Tests de performance** | Les temps de chargement et de reponse respectent les cibles definies (section 8.1). |
| 7 | **Documentation API** | Les endpoints API sont documentes (Swagger / OpenAPI). |
| 8 | **Documentation utilisateur** | Les fonctionnalites sont documentees dans l'aide en ligne / le guide utilisateur. |
| 9 | **Accessibilite** | L'interface respecte les criteres WCAG 2.1 niveau AA. |
| 10 | **Pas de regression** | Les tests de regression passent sans erreur. |
| 11 | **Deploye en recette** | La fonctionnalite est deployee sur l'environnement de recette et validee par le Product Owner. |
| 12 | **Criteres d'acceptance valides** | Tous les criteres d'acceptance de la User Story sont valides et approuves par le Product Owner. |

---

## 10. Dependances

### 10.1 Dependances entrantes (ce dont EPIC-006 a besoin)

| Dependance | Module source | Description | Criticite |
|---|---|---|---|
| Liste des projets et phases | EPIC-002 Projets | Le planning repose sur la structure des projets (phases, dates, budgets). Les projets et phases doivent exister avant de pouvoir les planifier. | **Bloquante** |
| Heures realisees | EPIC-005 Temps | Les heures saisies par les collaborateurs sont necessaires pour calculer l'avancement, le "planifie vs realise" et la consommation budgetaire. | **Importante** (le planning peut fonctionner sans, mais les statistiques seront incompletes) |
| Liste des collaborateurs | EPIC-009 Collaborateurs | Les informations sur les collaborateurs (contrat, equipe, poste) sont necessaires pour le calcul de capacite et l'affectation. | **Bloquante** |
| Conges et absences | EPIC-009 Collaborateurs | Les conges valides doivent etre accessibles pour le calcul de disponibilite. | **Importante** |
| Jours feries | EPIC-009 Collaborateurs (ou parametres globaux) | La liste des jours feries doit etre configuree pour le calcul de capacite. | **Importante** |
| Authentification et roles | Module Authentification | Les droits d'acces au planning dependent des roles utilisateurs. | **Bloquante** |

### 10.2 Dependances sortantes (ce que EPIC-006 fournit)

| Dependance | Module consommateur | Description |
|---|---|---|
| Affectations planifiees | EPIC-002 Projets | Les projets peuvent afficher les ressources planifiees. |
| Previsions de charge | Tableau de bord global | Les previsions de charge alimentent le tableau de bord de l'agence. |
| Taux d'occupation | EPIC-009 Collaborateurs | Le taux d'occupation peut etre affiche sur la fiche collaborateur. |

### 10.3 Dependances techniques

| Composant | Description | Justification |
|---|---|---|
| Librairie Gantt (ex. DHTMLX Gantt, Bryntum, frappe-gantt) | Composant de diagramme de Gantt interactif | Le developpement d'un Gantt from scratch est trop couteux. Une librairie tierce est recommandee. |
| Librairie de graphiques (ex. Chart.js, D3.js, Recharts) | Composant de graphiques pour les statistiques et la vue Budget | Necessaire pour les graphiques de statistiques et la S-curve. |
| Librairie drag & drop (ex. react-dnd, dnd-kit) | Composant de glisser-deposer | Necessaire pour l'affectation de ressources par drag & drop sur le planning. |
| Generation PDF (ex. Puppeteer, jsPDF, html2canvas) | Composant de generation de PDF | Necessaire pour l'export PDF du Gantt et des statistiques. |
| WebSocket ou SSE (optionnel) | Communication temps reel | Pour la mise a jour en temps reel du planning lorsque plusieurs utilisateurs le consultent simultanement. |

---

## 11. Modele de Donnees Principal

### 11.1 Entite : ResourceAllocation (Affectation de ressource)

| Champ | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK, auto-genere | Identifiant unique de l'affectation |
| `employee_id` | UUID | FK vers Employee, NOT NULL | Collaborateur affecte |
| `project_id` | UUID | FK vers Project, NOT NULL | Projet concerne |
| `phase_id` | UUID | FK vers Phase, NULL autorise | Phase du projet (null = affectation au projet sans phase specifique) |
| `start_date` | DATE | NOT NULL | Date de debut de l'affectation |
| `end_date` | DATE | NOT NULL, >= start_date | Date de fin de l'affectation |
| `hours_per_week` | DECIMAL(5,2) | NOT NULL, >= 0.5 | Nombre d'heures planifiees par semaine |
| `status` | ENUM | NOT NULL, defaut 'active' | Statut : 'active', 'completed', 'cancelled' |
| `notes` | TEXT | NULL autorise | Notes libres sur l'affectation |
| `created_by` | UUID | FK vers User, NOT NULL | Utilisateur ayant cree l'affectation |
| `created_at` | TIMESTAMP | NOT NULL, auto | Date de creation |
| `updated_at` | TIMESTAMP | NOT NULL, auto | Date de derniere modification |
| `updated_by` | UUID | FK vers User | Utilisateur ayant effectue la derniere modification |

**Index** : `(employee_id, start_date, end_date)`, `(project_id, phase_id)`, `(status)`

### 11.2 Entite : Milestone (Jalon)

| Champ | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK, auto-genere | Identifiant unique du jalon |
| `project_id` | UUID | FK vers Project, NOT NULL | Projet associe |
| `title` | VARCHAR(255) | NOT NULL | Titre du jalon |
| `date` | DATE | NOT NULL | Date du jalon |
| `description` | TEXT | NULL autorise | Description detaillee du jalon |
| `status` | ENUM | NOT NULL, defaut 'upcoming' | Statut : 'upcoming' (a venir), 'achieved' (atteint), 'overdue' (en retard) |
| `color` | VARCHAR(7) | NULL autorise | Code couleur hexadecimal (ex. #FF5733) |
| `sort_order` | INTEGER | NOT NULL, defaut 0 | Ordre d'affichage |
| `created_by` | UUID | FK vers User, NOT NULL | Utilisateur ayant cree le jalon |
| `created_at` | TIMESTAMP | NOT NULL, auto | Date de creation |
| `updated_at` | TIMESTAMP | NOT NULL, auto | Date de derniere modification |

**Index** : `(project_id, date)`, `(status)`

### 11.3 Entite : Availability (Disponibilite)

| Champ | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK, auto-genere | Identifiant unique de l'enregistrement |
| `employee_id` | UUID | FK vers Employee, NOT NULL | Collaborateur concerne |
| `date` | DATE | NOT NULL | Date du jour |
| `capacity_hours` | DECIMAL(4,2) | NOT NULL, >= 0 | Capacite en heures pour ce jour (apres deduction des absences) |
| `contractual_hours` | DECIMAL(4,2) | NOT NULL, >= 0 | Heures contractuelles pour ce jour (avant deduction des absences) |
| `leave_type` | ENUM | NULL autorise | Type d'absence : 'paid_leave' (conge paye), 'rtt', 'sick_leave' (maladie), 'maternity' (maternite/paternite), 'unpaid_leave' (sans solde), 'training' (formation), 'public_holiday' (jour ferie), 'other' (autre), NULL (pas d'absence) |
| `leave_id` | UUID | FK vers Leave, NULL autorise | Reference vers la demande de conge (si applicable) |
| `is_working_day` | BOOLEAN | NOT NULL, defaut TRUE | Indique si le jour est un jour ouvrable |
| `created_at` | TIMESTAMP | NOT NULL, auto | Date de creation |
| `updated_at` | TIMESTAMP | NOT NULL, auto | Date de derniere modification |

**Index** : `(employee_id, date)` UNIQUE, `(date, leave_type)`

### 11.4 Entite : PhaseDependency (Dependance entre phases)

| Champ | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK, auto-genere | Identifiant unique |
| `project_id` | UUID | FK vers Project, NOT NULL | Projet concerne |
| `predecessor_phase_id` | UUID | FK vers Phase, NOT NULL | Phase predecesseur |
| `successor_phase_id` | UUID | FK vers Phase, NOT NULL | Phase successeur |
| `dependency_type` | ENUM | NOT NULL, defaut 'FS' | Type : 'FS' (Finish-to-Start), 'SS' (Start-to-Start) |
| `lag_days` | INTEGER | NOT NULL, defaut 0 | Delai en jours entre les deux phases (peut etre negatif) |
| `created_at` | TIMESTAMP | NOT NULL, auto | Date de creation |

**Index** : `(project_id)`, `(predecessor_phase_id, successor_phase_id)` UNIQUE

**Contrainte** : `predecessor_phase_id != successor_phase_id`

### 11.5 Entite : PlanningShareLink (Lien de partage)

| Champ | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK, auto-genere | Identifiant unique |
| `project_id` | UUID | FK vers Project, NOT NULL | Projet concerne |
| `token` | VARCHAR(36) | NOT NULL, UNIQUE | Token unique (UUID v4) pour l'acces |
| `expires_at` | TIMESTAMP | NOT NULL | Date d'expiration du lien |
| `is_revoked` | BOOLEAN | NOT NULL, defaut FALSE | Indique si le lien a ete revoque |
| `include_budget` | BOOLEAN | NOT NULL, defaut FALSE | Inclure la vue Budget dans le partage |
| `include_resources` | BOOLEAN | NOT NULL, defaut FALSE | Inclure la vue Ressources dans le partage |
| `created_by` | UUID | FK vers User, NOT NULL | Utilisateur ayant cree le lien |
| `created_at` | TIMESTAMP | NOT NULL, auto | Date de creation |

**Index** : `(token)` UNIQUE, `(project_id)`

### 11.6 Diagramme des relations

```
Employee (EPIC-009)
    |
    |-- 1:N --> ResourceAllocation
    |               |
    |               |-- N:1 --> Project (EPIC-002)
    |               |-- N:1 --> Phase (EPIC-002)
    |
    |-- 1:N --> Availability
    |               |-- N:1 --> Leave (EPIC-009)
    |
Project (EPIC-002)
    |
    |-- 1:N --> Milestone
    |-- 1:N --> PhaseDependency
    |-- 1:N --> PlanningShareLink
    |
Phase (EPIC-002)
    |
    |-- 1:N --> PhaseDependency (predecessor ou successor)
    |-- 1:N --> ResourceAllocation
    |
TimeEntry (EPIC-005)
    |-- N:1 --> Phase (pour le calcul planifie vs realise)
    |-- N:1 --> Employee
```

---

## 12. Estimation & Decoupage

### 12.1 Estimation globale

| Parametre | Valeur |
|---|---|
| **Duree estimee** | 6 a 9 semaines |
| **Nombre de sprints** | 4 a 5 sprints (sprints de 2 semaines) |
| **Effort total estime** | 320 a 480 heures-homme |
| **Taille de l'equipe recommandee** | 2 developpeurs frontend + 1 developpeur backend + 1 QA |

### 12.2 Decoupage en sprints

#### Sprint 1 -- Fondations et modele de donnees (semaines 1-2)

| Tache | User Stories | Estimation |
|---|---|---|
| Conception et creation du modele de donnees (tables, index, migrations) | Toutes | 16h |
| API CRUD ResourceAllocation (creation, lecture, modification, suppression) | US-PL02 | 24h |
| API CRUD Milestone | US-PL07 | 16h |
| API de calcul de disponibilite (Availability) | US-PL03 | 24h |
| API CRUD PhaseDependency | US-PL06 | 12h |
| Tests unitaires et d'integration backend | Toutes | 16h |
| **Total Sprint 1** | | **108h** |

#### Sprint 2 -- Planning global et affectation (semaines 3-4)

| Tache | User Stories | Estimation |
|---|---|---|
| Interface du planning global (grille temporelle, vues par collaborateur et par projet) | US-PL01 | 32h |
| Panneau lateral des collaborateurs + drag & drop d'affectation | US-PL02 | 24h |
| Formulaire d'affectation (creation, edition, suppression) | US-PL02 | 16h |
| Filtres et recherche sur le planning global | US-PL01 | 12h |
| Detection et affichage visuel de la sur-charge / sous-charge | US-PL11 | 16h |
| Tests frontend et E2E | US-PL01, US-PL02, US-PL11 | 12h |
| **Total Sprint 2** | | **112h** |

#### Sprint 3 -- Disponibilite et Gantt projet (semaines 5-6)

| Tache | User Stories | Estimation |
|---|---|---|
| Interface de la vue Disponibilite (tableau, codes couleur, filtres) | US-PL03 | 20h |
| Integration des conges et jours feries dans le planning | US-PL04 | 16h |
| Integration de la librairie Gantt et affichage des phases | US-PL06 | 32h |
| Interactions sur le Gantt (drag & drop, redimensionnement, creation de phase) | US-PL06 | 20h |
| Gestion des jalons sur le Gantt | US-PL07 | 12h |
| Tests frontend et E2E | US-PL03, US-PL04, US-PL06, US-PL07 | 12h |
| **Total Sprint 3** | | **112h** |

#### Sprint 4 -- Budget, Ressources et Statistiques (semaines 7-8)

| Tache | User Stories | Estimation |
|---|---|---|
| Vue Budget du planning projet (graphiques, S-curve, tableau) | US-PL08 | 24h |
| Vue Ressources du planning projet (liste, ajout, barre de charge) | US-PL09 | 20h |
| Tableau de bord Statistiques (taux d'occupation, planifie vs realise, previsions) | US-PL05 | 32h |
| API statistiques et agrégations | US-PL05 | 16h |
| Tests frontend et E2E | US-PL05, US-PL08, US-PL09 | 12h |
| **Total Sprint 4** | | **104h** |

#### Sprint 5 -- Export, partage et finalisation (semaine 9)

| Tache | User Stories | Estimation |
|---|---|---|
| Export PDF, PNG, CSV du Gantt et des statistiques | US-PL10 | 20h |
| Generation de liens de partage securises | US-PL10 | 12h |
| Panneau d'alertes de charge + notifications | US-PL11 | 12h |
| Tests de performance et optimisation | Toutes | 8h |
| Corrections de bugs et polish UI | Toutes | 12h |
| Validation PO et tests de recette | Toutes | 8h |
| **Total Sprint 5** | | **72h** |

### 12.3 Recapitulatif

| Sprint | Duree | Effort | User Stories principales |
|---|---|---|---|
| Sprint 1 | 2 semaines | 108h | Fondations, API backend |
| Sprint 2 | 2 semaines | 112h | US-PL01, US-PL02, US-PL11 |
| Sprint 3 | 2 semaines | 112h | US-PL03, US-PL04, US-PL06, US-PL07 |
| Sprint 4 | 2 semaines | 104h | US-PL05, US-PL08, US-PL09 |
| Sprint 5 | 1 semaine | 72h | US-PL10, finalisation |
| **Total** | **9 semaines** | **508h** | |

### 12.4 Risques identifies

| Risque | Probabilite | Impact | Mitigation |
|---|---|---|---|
| Complexite d'integration de la librairie Gantt | Moyenne | Haut | Prototype technique en amont (spike). Evaluer 2-3 librairies avant de choisir. |
| Performance du planning global avec de nombreux collaborateurs et projets | Moyenne | Moyen | Pagination, virtualisation du DOM, chargement lazy des donnees. |
| Dependance sur les donnees des modules Projets et Collaborateurs | Haute | Haut | Utiliser des donnees mockees en attendant la disponibilite des modules. Definir les contrats d'API en amont. |
| Complexite du drag & drop sur des grilles temporelles | Moyenne | Moyen | Utiliser une librairie eprouvee (dnd-kit, react-dnd). Prevoir du temps supplementaire pour le polish. |
| Calcul de disponibilite incorrect (cas limites : changement de contrat en cours de periode, conge a cheval sur deux mois) | Basse | Haut | Tests unitaires exhaustifs couvrant tous les cas limites. Revue fonctionnelle avec le metier. |

---

*Document redige le 26 fevrier 2026 -- Version 1.0*
*Auteur : Equipe Produit OOTI*
