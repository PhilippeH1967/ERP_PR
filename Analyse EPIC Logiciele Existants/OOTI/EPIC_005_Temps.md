# EPIC -- Module Temps

**Application OOTI -- Gestion de projets pour cabinets d'architecture**
**Version 1.0 -- Fevrier 2026**

---

## 1. Identification de l'EPIC

| Champ | Valeur |
|---|---|
| **Nom** | Temps (Time Tracking) |
| **Reference** | EPIC-005 |
| **Module parent** | Equipe |
| **Priorite** | Haute |
| **Responsable produit** | Chef de projet / Product Owner |
| **Date de creation** | Fevrier 2026 |
| **Version du document** | 1.0 |
| **EPICs lies** | EPIC-002 Projets, EPIC-003 Honoraires, EPIC-006 Planning, EPIC-012 Validation |

---

## 2. Contexte & Problematique

### 2.1 Contexte metier

Les cabinets d'architecture fonctionnent sur un modele economique ou la rentabilite des projets est directement liee au temps passe par les collaborateurs. Chaque projet est contractualise avec un budget d'honoraires (EPIC-003) qui correspond a une enveloppe d'heures estimee. Le suivi precis du temps reel consomme est donc un enjeu strategique pour la survie economique du cabinet.

Dans un cabinet typique de 10 a 50 collaborateurs, les equipes sont composees d'architectes, de dessinateurs-projeteurs, de chefs de projet et de personnel administratif. Chacun repartit son temps entre plusieurs projets simultanement, avec des phases variees (esquisse, APS, APD, PRO, DCE, DET, AOR). A cela s'ajoutent les temps non productifs (administration, formation, conges) et les deplacements sur site qui generent des frais kilometriques refacturables.

### 2.2 Problematique actuelle

Sans outil de suivi de temps integre, les cabinets d'architecture font face aux problemes suivants :

- **Perte de rentabilite invisible** : Sans suivi precis, les depassements d'heures sur un projet ne sont detectes qu'a posteriori, souvent trop tard pour corriger la trajectoire. Un projet peut consommer 150% de son budget d'heures sans que personne ne s'en rende compte.
- **Saisie fastidieuse et tardive** : Les collaborateurs saisissent leurs temps en fin de semaine ou en fin de mois, de memoire, ce qui entraine des approximations significatives (estimees a 15-25% d'ecart avec la realite).
- **Absence de donnees decisionnelles** : Les dirigeants ne disposent pas de KPIs fiables pour piloter l'activite (taux de facturation, productivite par collaborateur, rentabilite par phase).
- **Deplacements non traces** : Les visites de chantier et reunions exterieures generent des frais kilometriques qui ne sont pas systematiquement enregistres ni refactures aux clients.
- **Validation approximative** : Sans workflow de validation, les managers ne peuvent pas verifier la coherence des temps saisis avant la facturation.
- **Deconnexion honoraires/temps** : Le lien entre les heures consommees et les honoraires contractualises n'est pas automatise, rendant impossible le suivi de la marge en temps reel.

### 2.3 Impact attendu

La mise en place du module Temps doit permettre :

- Une reduction de 80% du temps de saisie administrative grace a l'interface optimisee
- Une amelioration de 30% de la precision des donnees de temps
- Une visibilite en temps reel sur la consommation des budgets d'heures
- La detection precoce des depassements budgetaires (alerte a 80% de consommation)
- L'automatisation du calcul des frais de deplacement
- La fourniture de KPIs fiables pour le pilotage de l'activite

---

## 3. Objectif de l'EPIC

L'EPIC-005 a pour objectif de fournir un module complet de suivi du temps permettant aux collaborateurs de saisir leurs heures de travail de maniere simple et rapide, aux managers de valider et analyser les temps saisis, et aux dirigeants de piloter la rentabilite des projets et la productivite de l'equipe.

Le module doit s'integrer nativement avec les modules Projets (EPIC-002) pour la ventilation par projet/phase, Honoraires (EPIC-003) pour le calcul automatique des montants facturables, Planning (EPIC-006) pour la comparaison previsionnel/realise, et Validation (EPIC-012) pour le workflow d'approbation des feuilles de temps.

Les objectifs mesurables sont :

1. **Taux de saisie** : Atteindre 95% de saisie des temps dans la semaine courante (contre ~60% en saisie manuelle)
2. **Temps de saisie** : Reduire a moins de 5 minutes par jour la saisie des temps pour un collaborateur
3. **Precision** : Garantir une granularite de saisie a 15 minutes minimum
4. **Couverture** : Couvrir 100% des types de temps (production, administration, conges, formation, deplacements)
5. **Delai de validation** : Permettre la validation des temps dans un delai de 48h apres saisie

---

## 4. Perimetre Fonctionnel

### 4.1 Vue Resume des temps

La vue Resume constitue le tableau de bord synthetique du module Temps. Elle presente les indicateurs cles de performance (KPIs) relatifs a la saisie de temps a l'echelle de l'agence.

**Fonctionnalites detaillees :**

- **KPIs principaux affiches :**
  - Heures totales saisies (periode selectionnable : semaine, mois, trimestre, annee)
  - Heures facturables vs non facturables (avec pourcentage)
  - Taux de saisie par collaborateur (heures saisies / heures attendues)
  - Heures par projet (top 10 projets les plus consommateurs)
  - Comparaison budget d'heures previsionnel vs consomme par projet
  - Taux de productivite moyen de l'agence
  - Heures en attente de validation

- **Filtres disponibles :**
  - Periode (semaine courante, mois courant, trimestre, annee, dates personnalisees)
  - Equipe / Service
  - Collaborateur
  - Projet / Phase
  - Type de temps (Production, Administration, Conges, Formation)

- **Graphiques :**
  - Histogramme empile des heures par type de temps sur la periode
  - Camembert de repartition Production / Administration / Conges / Formation
  - Courbe d'evolution du taux de saisie sur les 12 derniers mois
  - Barre de progression par projet (heures consommees / budget heures)

### 4.2 Saisie de temps quotidienne et hebdomadaire

La saisie de temps est le coeur du module. Elle doit offrir deux modes principaux : saisie au jour le jour et saisie en grille hebdomadaire.

**4.2.1 Saisie quotidienne :**

- Formulaire de saisie d'une entree de temps avec les champs :
  - Projet (liste deroulante avec recherche, projets actifs uniquement)
  - Phase du projet (filtree selon le projet selectionne)
  - Date (par defaut : aujourd'hui)
  - Duree (en heures:minutes ou en fraction de journee selon la configuration)
  - Type de temps (Production, Administration, Conges, Formation)
  - Facturable (oui/non, pre-rempli selon le type)
  - Description / commentaire (champ texte libre, 500 caracteres max)
- Affichage du total d'heures saisies pour la journee en cours
- Alerte visuelle si le total journalier depasse 10h ou est inferieur a 7h (configurable)
- Possibilite de dupliquer une entree existante
- Saisie rapide par raccourci clavier

**4.2.2 Saisie hebdomadaire (grille semaine) :**

- Grille avec en lignes : les combinaisons Projet/Phase, et en colonnes : les jours de la semaine (Lundi a Vendredi, Samedi/Dimanche optionnels)
- Ajout d'une nouvelle ligne Projet/Phase dans la grille
- Saisie directe dans les cellules (heures ou jours)
- Total par ligne (total semaine par projet/phase)
- Total par colonne (total jour)
- Total general de la semaine
- Code couleur selon le statut de validation (En attente : orange, Valide : vert, Refuse : rouge)
- Navigation entre semaines (semaine precedente / semaine suivante)
- Fonction de copie de la semaine precedente

**4.2.3 Timer / Chronometre :**

- Bouton de demarrage/arret d'un chronometre
- Possibilite d'associer le chronometre a un Projet/Phase en cours
- Affichage du temps ecoule en temps reel dans la barre de navigation
- Conversion automatique du temps chronometre en entree de temps a l'arret
- Historique des sessions de chronometre non enregistrees (brouillons)
- Notification si le chronometre est actif depuis plus de 2 heures sans pause

### 4.3 Vue Calendrier

La vue Calendrier offre une vision mensuelle des temps saisis, permettant d'identifier rapidement les jours sans saisie ou les anomalies.

**Fonctionnalites detaillees :**

- Affichage sous forme de calendrier mensuel
- Chaque jour affiche :
  - Le total d'heures saisies
  - Un code couleur (vert : journee complete >= 7h, orange : journee partielle, rouge : aucune saisie, gris : jour non ouvrable/conge)
  - La liste resumee des projets travailles
- Navigation entre mois (mois precedent / mois suivant)
- Clic sur un jour pour acceder au detail et ajouter/modifier des entrees
- Vue par collaborateur (pour les managers) ou vue personnelle
- Indication des jours feries et des conges valides
- Filtre par type de temps

### 4.4 Gestion des deplacements

Le sous-module Deplacements permet de tracer les deplacements professionnels lies aux projets (visites de chantier, reunions client, etc.) et de calculer les frais associes.

**Fonctionnalites detaillees :**

- Formulaire de saisie d'un deplacement :
  - Date du deplacement
  - Projet associe (optionnel)
  - Lieu de depart
  - Lieu d'arrivee
  - Distance (km) - saisie manuelle ou calcul automatique
  - Mode de transport (Voiture personnelle, Voiture de societe, Transport en commun, Velo, Autre)
  - Aller-retour (oui/non, si oui : distance doublee automatiquement)
  - Montant des frais (calcul automatique selon bareme kilometrique ou saisie manuelle)
  - Commentaire / motif du deplacement
- Configuration du bareme kilometrique par mode de transport (admin)
- Liste des deplacements avec filtres (date, projet, collaborateur)
- Total des kilometres et des frais par periode
- Liaison avec une entree de temps (le temps de deplacement peut etre comptabilise)
- Export des frais de deplacement pour refacturation

### 4.5 Vue Semaines

La vue Semaines offre une vision consolidee de la saisie hebdomadaire, orientee validation et suivi managerial.

**Fonctionnalites detaillees :**

- Liste des semaines avec pour chaque semaine :
  - Numero de semaine et dates (du lundi au vendredi/dimanche)
  - Total d'heures saisies
  - Statut de validation (Non soumise, En attente de validation, Validee, Refusee)
  - Repartition par type de temps (barre empilee)
- Soumission de la semaine pour validation (action collaborateur)
- Verrouillage de la semaine apres validation (pas de modification sans deverrouillage manager)
- Historique des commentaires de validation/refus
- Possibilite de rouvrir une semaine validee (action manager avec justification)
- Alerte si une semaine passee n'a pas ete soumise (notification au collaborateur et au manager)

### 4.6 Journaux de travail

Les Journaux de travail constituent l'historique complet et detaille de toutes les entrees de temps saisies dans le systeme.

**Fonctionnalites detaillees :**

- Tableau paginable de toutes les entrees de temps
- Colonnes : Date, Collaborateur, Projet, Phase, Heures, Type, Facturable, Statut, Description
- Tri multi-colonnes
- Filtres avances :
  - Periode (dates de/a)
  - Collaborateur (un ou plusieurs)
  - Projet (un ou plusieurs)
  - Phase
  - Type de temps
  - Statut de validation
  - Facturable (oui/non/tous)
- Recherche textuelle dans les descriptions
- Export CSV / Excel / PDF avec les filtres appliques
- Actions en lot (validation, refus, suppression) pour les managers
- Affichage du total d'heures filtre en pied de tableau

### 4.7 Statistiques et indicateurs

Au-dela du resume, des vues statistiques detaillees permettent l'analyse approfondie des donnees de temps.

**Fonctionnalites detaillees :**

- **Statistiques par collaborateur :**
  - Heures totales saisies
  - Taux de saisie (heures saisies / heures ouvrables)
  - Taux de facturation (heures facturables / heures totales)
  - Repartition par projet (tableau + graphique)
  - Evolution mensuelle
  - Comparaison avec la moyenne de l'equipe

- **Statistiques par projet :**
  - Heures consommees vs budget heures
  - Repartition par phase
  - Repartition par collaborateur
  - Cout reel (heures x taux horaire collaborateur) vs honoraires
  - Tendance de consommation (projection de fin de projet)

- **Statistiques par phase :**
  - Heures par phase standard (ESQ, APS, APD, PRO, DCE, DET, AOR)
  - Comparaison inter-projets par phase
  - Ratios moyens par phase

---

## 5. User Stories

### US-T01 : Vue resume des temps (agence)

**En tant que** dirigeant ou chef de projet,
**Je veux** consulter un tableau de bord synthetique des temps saisis a l'echelle de l'agence,
**Afin de** piloter la productivite de l'equipe et la consommation des budgets d'heures des projets.

**Criteres d'acceptance :**

1. Le tableau de bord affiche les KPIs suivants pour la periode selectionnee : heures totales saisies, heures facturables, heures non facturables, taux de saisie moyen (en pourcentage), nombre de collaborateurs ayant saisi leurs temps, nombre de collaborateurs n'ayant pas saisi.
2. Un selecteur de periode permet de choisir parmi : semaine courante, mois courant, trimestre courant, annee courante, et dates personnalisees (champ date debut / date fin). Le changement de periode rafraichit tous les KPIs et graphiques en moins de 2 secondes.
3. Un graphique en barres empilees affiche la repartition des heures par type (Production, Administration, Conges, Formation) sur la periode. Chaque segment est cliquable et filtre le detail sous-jacent.
4. Un tableau liste les 10 projets les plus consommateurs d'heures avec les colonnes : nom du projet, heures consommees, budget heures previsionnel, pourcentage de consommation, ecart. Les projets depassant 80% de consommation sont surlignees en orange, ceux depassant 100% en rouge.
5. Le taux de saisie par collaborateur est affiche sous forme de liste triable. Un collaborateur avec un taux inferieur a 80% est signale par un indicateur visuel d'alerte (icone orange). Un collaborateur a 0% de saisie est signale en rouge.
6. Des filtres permettent de restreindre la vue par equipe/service, par collaborateur specifique, par projet ou par type de temps. Les filtres sont combinables et la mise a jour est instantanee.
7. Un graphique en courbe montre l'evolution du taux de saisie et du taux de facturation sur les 12 derniers mois, permettant d'identifier les tendances.
8. Le tableau de bord est accessible uniquement aux roles manager, chef de projet et administrateur. Un collaborateur standard ne voit que ses propres statistiques resumees.

---

### US-T02 : Saisie de temps quotidienne

**En tant que** collaborateur (architecte, dessinateur, chef de projet),
**Je veux** saisir mes heures de travail au jour le jour de maniere rapide et intuitive,
**Afin de** enregistrer avec precision le temps passe sur chaque projet et phase.

**Criteres d'acceptance :**

1. Le formulaire de saisie contient les champs obligatoires suivants : Projet (liste deroulante avec recherche par nom ou code), Phase (liste deroulante filtree selon le projet selectionne, affichant uniquement les phases actives), Date (champ date, par defaut la date du jour), Duree (champ numerique en heures:minutes ou en fraction de journee selon la configuration de l'agence), Type de temps (liste deroulante : Production, Administration, Conges, Formation).
2. Les champs optionnels sont : Facturable (case a cocher, pre-cochee si le type est "Production" et que la phase du projet est facturable), Description (champ texte libre, maximum 500 caracteres).
3. La liste des projets ne propose que les projets auxquels le collaborateur est affecte et dont le statut est "En cours" ou "Actif". Un champ de recherche avec autocompletion permet de trouver rapidement un projet par son nom ou son code (recherche a partir de 2 caracteres).
4. Apres validation du formulaire, l'entree de temps est enregistree avec le statut "En attente de validation". Un message de confirmation s'affiche pendant 3 secondes. Le total d'heures de la journee est mis a jour instantanement.
5. Un bandeau en haut de la vue affiche le total d'heures saisies pour la journee en cours. Si le total est inferieur a 7h (seuil configurable), le bandeau est orange avec le message "Journee incomplete". Si le total est superieur ou egal a 7h, le bandeau est vert. Si le total depasse 10h, le bandeau est rouge avec un avertissement.
6. L'utilisateur peut modifier une entree de temps existante tant qu'elle n'a pas ete validee (statut "En attente"). Un clic sur l'entree ouvre le formulaire pre-rempli. La modification met a jour la date de derniere modification (updated_at).
7. L'utilisateur peut supprimer une entree de temps non validee. Une confirmation est demandee ("Etes-vous sur de vouloir supprimer cette entree ?"). La suppression est en soft-delete (l'entree est archivee, pas detruite).
8. Un bouton "Dupliquer" sur chaque entree permet de creer une copie avec la date du jour et les memes Projet/Phase/Type, la duree et la description etant vides pour etre renseignees.

---

### US-T03 : Saisie de temps hebdomadaire (grille semaine)

**En tant que** collaborateur,
**Je veux** saisir mes heures de la semaine dans une grille tabulaire avec les projets en lignes et les jours en colonnes,
**Afin de** gagner du temps en saisissant une semaine complete en une seule vue.

**Criteres d'acceptance :**

1. La grille affiche en lignes les combinaisons Projet/Phase sur lesquelles le collaborateur a deja saisi du temps ou qu'il a ajoute manuellement, et en colonnes les jours de la semaine (Lundi a Vendredi par defaut, Samedi et Dimanche affichables selon la configuration).
2. Chaque cellule de la grille est un champ de saisie editable. La saisie peut se faire en heures (format : 2.5 ou 2:30) ou en fraction de journee (format : 0.5 pour une demi-journee) selon la configuration de l'agence. La navigation entre cellules se fait par la touche Tab (horizontale) et Entree (verticale).
3. Un bouton "Ajouter un projet" permet d'inserer une nouvelle ligne dans la grille. Un selecteur Projet puis Phase s'affiche. Une fois selectionnes, la ligne apparait avec des cellules vides pour chaque jour de la semaine.
4. Le total par ligne (total des heures de la semaine pour un projet/phase) est affiche dans une colonne "Total" a droite. Le total par colonne (total des heures de chaque jour) est affiche dans une ligne "Total" en bas. Le total general de la semaine est affiche dans la cellule intersectant la colonne "Total" et la ligne "Total".
5. Les cellules sont colorees selon le statut de validation de l'entree de temps correspondante : blanc/neutre = saisie non soumise, orange = en attente de validation, vert = validee, rouge = refusee. Une cellule validee (verte) n'est pas editable.
6. Les boutons de navigation "<" et ">" permettent de passer a la semaine precedente ou suivante. Le numero de semaine et les dates (ex: "Semaine 09 -- 24/02/2026 au 28/02/2026") sont affiches en en-tete.
7. Un bouton "Enregistrer" sauvegarde toutes les modifications en une seule action. Les entrees creees ou modifiees sont enregistrees avec le statut "En attente de validation". Un message de confirmation s'affiche.
8. Si le total d'un jour depasse 10h ou si le total de la semaine depasse 45h (seuils configurables), un avertissement visuel s'affiche sans bloquer la saisie.

---

### US-T04 : Vue Calendrier des temps

**En tant que** collaborateur ou manager,
**Je veux** visualiser les temps saisis sur un calendrier mensuel,
**Afin de** reperer rapidement les jours sans saisie et avoir une vue d'ensemble de mon activite mensuelle.

**Criteres d'acceptance :**

1. Le calendrier affiche le mois courant par defaut avec une case par jour. Chaque case-jour affiche : le total d'heures saisies (ex: "7.5h"), un code couleur de fond (vert si >= 7h, orange si entre 1h et 7h, rouge si 0h sur un jour ouvrable, gris pour les weekends et jours feries), et la liste des 3 premiers projets travailles (nom abrege) avec leurs heures respectives.
2. Les boutons de navigation "<" et ">" permettent de passer au mois precedent ou suivant. Le nom du mois et l'annee sont affiches en en-tete (ex: "Fevrier 2026"). Un bouton "Aujourd'hui" ramene au mois courant.
3. Un clic sur une case-jour ouvre un panneau lateral (ou une modale) affichant le detail complet des entrees de temps de ce jour : liste des entrees avec Projet, Phase, Heures, Type, Description et Statut. Depuis ce panneau, l'utilisateur peut ajouter, modifier ou supprimer des entrees (sous reserve du statut de validation).
4. Un filtre par type de temps (Production, Administration, Conges, Formation) permet d'afficher uniquement les jours et heures correspondant au type selectionne. Le code couleur et les totaux se recalculent selon le filtre.
5. Les jours feries et les conges valides du collaborateur sont identifies visuellement (icone specifique ou badge). Un jour ferie avec des heures saisies affiche un indicateur d'attention.
6. Pour les managers et administrateurs, un selecteur de collaborateur permet de consulter le calendrier de n'importe quel membre de l'equipe. Le manager peut naviguer entre les calendriers de ses collaborateurs avec des fleches suivant/precedent.
7. Un compteur en haut du calendrier affiche le total d'heures du mois, le nombre de jours ouvrables du mois, le nombre de jours saisis, et le taux de saisie du mois (en pourcentage).
8. Le calendrier est responsive : sur tablette, la case-jour affiche seulement le total d'heures et le code couleur. Sur mobile, la vue bascule en liste chronologique des jours.

---

### US-T05 : Gestion des deplacements

**En tant que** collaborateur,
**Je veux** enregistrer mes deplacements professionnels (visites de chantier, reunions client),
**Afin de** tracer les kilometres parcourus, calculer les frais associes et permettre leur refacturation aux clients.

**Criteres d'acceptance :**

1. Le formulaire de saisie d'un deplacement contient les champs suivants : Date (obligatoire, par defaut aujourd'hui), Projet associe (optionnel, liste deroulante des projets actifs), Lieu de depart (champ texte avec autocompletion d'adresse), Lieu d'arrivee (champ texte avec autocompletion d'adresse), Distance en km (champ numerique, saisie manuelle ou calcul automatique a partir des adresses), Mode de transport (liste deroulante : Voiture personnelle, Voiture de societe, Transport en commun, Velo, Autre), Aller-retour (case a cocher, si coche la distance est doublee automatiquement), Commentaire/Motif (champ texte, 300 caracteres max).
2. Le montant des frais est calcule automatiquement selon la formule : distance (km) x bareme kilometrique du mode de transport. Le bareme est configurable par l'administrateur pour chaque mode de transport (ex: Voiture personnelle = 0.52 EUR/km). Le montant est affiche en temps reel lors de la saisie et peut etre surcharge manuellement si necessaire.
3. La liste des deplacements est presentee dans un tableau paginable avec les colonnes : Date, Collaborateur, Projet, Trajet (depart -> arrivee), Distance, Mode, Montant, Commentaire. Des filtres par date, projet, collaborateur et mode de transport sont disponibles.
4. Le tableau affiche en pied les totaux de la selection : total des kilometres et total des montants.
5. Un deplacement peut etre lie a une entree de temps (temps de transport). L'utilisateur peut, depuis le formulaire de deplacement, creer simultanement une entree de temps associee avec le type "Production" ou "Administration" et la duree du trajet.
6. La modification d'un deplacement est possible tant qu'il n'a pas ete valide et integre a une note de frais. La suppression requiert une confirmation et fonctionne en soft-delete.
7. L'export des deplacements est possible au format CSV et PDF, avec les filtres appliques. L'export PDF est formate pour servir de justificatif de frais kilometriques.
8. L'administrateur peut configurer les baremes kilometriques depuis les parametres du module : taux par kilometre pour chaque mode de transport, plafond mensuel de frais kilometriques par collaborateur (optionnel).

---

### US-T06 : Journaux de travail (historique)

**En tant que** manager ou administrateur,
**Je veux** consulter l'historique complet de toutes les entrees de temps de l'agence avec des filtres avances,
**Afin de** analyser en detail les temps saisis, effectuer des corrections et preparer la facturation.

**Criteres d'acceptance :**

1. Le tableau des journaux affiche toutes les entrees de temps avec les colonnes suivantes : Date, Collaborateur (nom + prenom), Projet (nom + code), Phase, Heures, Type de temps, Facturable (oui/non), Statut de validation, Description. Le tableau est paginable (25, 50, 100 entrees par page) et triable sur chaque colonne (tri ascendant/descendant).
2. Les filtres avances permettent de combiner les criteres suivants : Periode (date de debut et date de fin), Collaborateur (multi-selection), Projet (multi-selection), Phase (multi-selection filtree par projet), Type de temps (multi-selection : Production, Administration, Conges, Formation), Statut de validation (multi-selection : En attente, Valide, Refuse), Facturable (oui/non/tous). Les filtres se cumulent (logique ET) et le tableau se met a jour dynamiquement.
3. Un champ de recherche textuelle permet de filtrer les entrees dont la description contient le texte saisi (recherche insensible a la casse, a partir de 3 caracteres).
4. Le pied de tableau affiche les totaux de la selection filtree : total des heures, total des heures facturables, total des heures non facturables, nombre d'entrees.
5. Les managers peuvent effectuer des actions en lot sur les entrees selectionnees (cases a cocher en debut de ligne + case "tout selectionner") : Valider (passer en statut "Valide"), Refuser (passer en statut "Refuse" avec un commentaire obligatoire), Supprimer (soft-delete avec confirmation). Les actions en lot ne s'appliquent qu'aux entrees modifiables (non verrouillees).
6. L'export est disponible aux formats CSV, Excel (.xlsx) et PDF. L'export respecte les filtres appliques. Le fichier CSV utilise le point-virgule comme separateur et l'encodage UTF-8. Le fichier Excel contient un onglet "Donnees" et un onglet "Resume" avec les totaux. Le PDF est formate en paysage avec en-tete de l'agence.
7. Chaque entree est cliquable pour ouvrir le detail en panneau lateral, affichant l'historique des modifications (date, utilisateur, champ modifie, ancienne valeur, nouvelle valeur) pour assurer la tracabilite complete.
8. Un collaborateur standard ne voit que ses propres entrees dans le journal. Un manager voit les entrees de son equipe. Un administrateur voit toutes les entrees de l'agence.

---

### US-T07 : Types de temps et categorisation

**En tant qu'** administrateur de l'agence,
**Je veux** definir et gerer les types de temps disponibles pour la saisie,
**Afin de** categoriser les heures saisies selon la nature de l'activite et calculer correctement les taux de facturation.

**Criteres d'acceptance :**

1. Quatre types de temps sont disponibles par defaut a l'installation : Production (facturable par defaut, couleur bleue), Administration (non facturable par defaut, couleur grise), Conges (non facturable, couleur verte), Formation (non facturable par defaut, couleur violette). Ces types ne peuvent pas etre supprimes mais peuvent etre renommes et leur couleur modifiee.
2. L'administrateur peut creer des sous-types personnalises rattaches a un type principal. Exemple : sous Production, ajouter "Conception", "Dessin", "Reunion client", "Visite chantier". Chaque sous-type herite des proprietes du type parent (facturable, couleur) mais peut les surcharger.
3. Chaque type/sous-type possede les proprietes suivantes : Nom (unique, 50 caracteres max), Code (identifiant court, 10 caracteres max, unique), Type parent (pour les sous-types), Facturable par defaut (oui/non), Couleur (code hexadecimal pour l'affichage), Actif (oui/non, un type inactif n'apparait plus dans les listes de saisie mais les entrees existantes sont conservees), Ordre d'affichage (numerique, pour ordonner dans les listes deroulantes).
4. Lors de la saisie de temps, le collaborateur selectionne d'abord le type principal puis, si des sous-types existent, selectionne le sous-type dans une seconde liste deroulante. Si aucun sous-type n'existe pour le type choisi, la seconde liste n'apparait pas.
5. La modification d'un type de temps existant ne modifie pas retroactivement les entrees deja saisies. Un message d'information previent l'administrateur : "Les modifications s'appliqueront uniquement aux nouvelles saisies."
6. Un type de temps ne peut pas etre supprime s'il est utilise par au moins une entree de temps. Dans ce cas, il peut uniquement etre desactive (propriete Actif = non).
7. Les statistiques et les exports permettent de filtrer et regrouper par type et sous-type de temps.
8. L'interface d'administration des types de temps est un tableau editable en ligne avec drag-and-drop pour reordonner les types. L'ajout d'un type se fait via un bouton "Ajouter" qui insere une nouvelle ligne editable.

---

### US-T08 : Copie de la semaine precedente

**En tant que** collaborateur,
**Je veux** pouvoir copier la structure de saisie de la semaine precedente vers la semaine courante,
**Afin de** gagner du temps lorsque je travaille sur les memes projets d'une semaine a l'autre.

**Criteres d'acceptance :**

1. Un bouton "Copier la semaine precedente" est disponible dans la vue de saisie hebdomadaire (grille semaine). Le bouton est visible uniquement si la semaine courante est vide ou partiellement remplie.
2. Au clic, une modale de confirmation s'affiche : "Voulez-vous copier la structure de la semaine [N-1] (du [date debut] au [date fin]) ? Les projets et phases seront copies, mais les heures seront mises a zero." Deux options : "Copier la structure uniquement" (projets/phases sans heures) et "Copier structure et heures" (projets/phases avec les memes heures).
3. L'option "Copier la structure uniquement" cree dans la grille de la semaine courante les memes lignes Projet/Phase que la semaine precedente, avec toutes les cellules d'heures a zero. Le collaborateur n'a plus qu'a remplir les heures.
4. L'option "Copier structure et heures" cree les memes lignes Projet/Phase avec les memes valeurs d'heures pour chaque jour. Les entrees copiees ont le statut "En attente de validation" et des descriptions vides.
5. Si la semaine courante contient deja des entrees, la copie ajoute les lignes manquantes sans supprimer ni ecraser les lignes existantes. Un message informe : "Les projets deja presents dans la semaine courante ont ete conserves, seuls les nouveaux projets ont ete ajoutes."
6. Seuls les projets encore actifs sont copies. Si un projet de la semaine precedente est devenu inactif entre-temps, il est ignore et un message informe : "Le projet [nom] n'a pas ete copie car il n'est plus actif."
7. Les entrees copiees ne sont pas automatiquement enregistrees : elles apparaissent dans la grille comme des modifications non sauvegardees (indicateur visuel) et le collaborateur doit cliquer sur "Enregistrer" pour les persister.
8. La fonction de copie est egalement disponible depuis un menu contextuel sur la semaine dans la vue "Semaines", permettant de copier une semaine specifique (pas necessairement la precedente) vers la semaine courante.

---

### US-T09 : Saisie en heures ou en jours (configuration)

**En tant qu'** administrateur de l'agence,
**Je veux** configurer l'unite de saisie du temps (heures ou jours) et les parametres associes,
**Afin d'** adapter le module aux pratiques de saisie de mon agence.

**Criteres d'acceptance :**

1. Dans les parametres du module Temps, l'administrateur peut choisir l'unite de saisie principale : "Heures" (saisie en heures et minutes, ex: 7:30 ou 7.5) ou "Jours" (saisie en fraction de journee, ex: 1, 0.5, 0.25). Ce parametre s'applique a l'ensemble de l'agence.
2. En mode "Heures", la saisie accepte les formats suivants : decimal (7.5), horaire (7:30), et la granularite minimale est de 15 minutes (0.25h). Une saisie inferieure a 15 minutes est arrondie au quart d'heure superieur. Le nombre d'heures attendues par jour (par defaut 7h) et par semaine (par defaut 35h) est configurable.
3. En mode "Jours", la saisie accepte les fractions suivantes : 1 (journee complete), 0.75 (trois quarts de journee), 0.5 (demi-journee), 0.25 (quart de journee). La correspondance heures/jour est configurable (par defaut 1 jour = 7 heures). Les totaux et KPIs sont affiches en jours.
4. Le passage d'un mode a l'autre ne modifie pas les donnees existantes : les entrees restent stockees en heures dans la base de donnees. Seul l'affichage et la saisie changent. La conversion est transparente pour l'utilisateur.
5. L'administrateur peut configurer les horaires de l'agence : nombre d'heures par jour ouvrable (defaut: 7h), nombre de jours ouvrables par semaine (defaut: 5), jours ouvrables (cases a cocher Lundi a Dimanche, par defaut Lundi-Vendredi coches). Ces parametres influencent le calcul du taux de saisie et les alertes de journee incomplete.
6. Un parametre "Saisie obligatoire" peut etre active/desactive. S'il est actif, un collaborateur ne peut pas soumettre sa semaine pour validation si le total d'heures est inferieur a 80% du temps attendu (seuil configurable). Un message d'erreur explicite indique le nombre d'heures manquantes.
7. Un parametre "Saisie retroactive" definit le nombre de jours maximum dans le passe ou un collaborateur peut saisir du temps (par defaut : 30 jours). Au-dela, seul un manager peut saisir ou modifier des temps. Un parametre "0" desactive cette restriction.
8. Les modifications de configuration sont journalisees dans un log d'audit : date, utilisateur, parametre modifie, ancienne valeur, nouvelle valeur.

---

### US-T10 : Export des donnees de temps

**En tant que** manager ou administrateur,
**Je veux** exporter les donnees de temps dans differents formats,
**Afin de** les utiliser dans des outils externes (comptabilite, facturation, reporting).

**Criteres d'acceptance :**

1. L'export est disponible depuis trois emplacements : la vue Journaux de travail (export du tableau filtre), la vue Resume (export du rapport de synthese), la vue Deplacements (export des frais). Un bouton "Exporter" avec un menu deroulant propose les formats disponibles.
2. Les formats d'export disponibles sont : CSV (separateur point-virgule, encodage UTF-8 avec BOM pour compatibilite Excel), Excel (.xlsx avec mise en forme, en-tetes en gras, totaux en pied), PDF (mise en page paysage, logo et nom de l'agence en en-tete, date d'export en pied de page).
3. L'export respecte les filtres actuellement appliques dans la vue. Si aucun filtre n'est actif, toutes les donnees accessibles par l'utilisateur sont exportees. Un compteur affiche le nombre d'entrees qui seront exportees avant le lancement.
4. Le fichier CSV contient les colonnes : Date, Collaborateur, Code Projet, Nom Projet, Phase, Heures, Type de Temps, Facturable (Oui/Non), Statut, Description, Montant Facturable. La premiere ligne est la ligne d'en-tete.
5. Le fichier Excel contient deux onglets : "Donnees" (meme contenu que le CSV avec mise en forme) et "Synthese" (total par projet, total par collaborateur, total par type de temps, total general). Les cellules de type "Heures" sont formatees en nombre avec 2 decimales.
6. Le fichier PDF contient un en-tete avec le nom de l'agence, le titre du rapport ("Journal des temps" ou "Rapport de synthese" ou "Frais de deplacement"), la periode et les filtres appliques. Le tableau est paginable automatiquement. Chaque page affiche le numero de page (Page X/Y).
7. Pour les exports volumineux (plus de 5000 entrees), le traitement est effectue en arriere-plan. L'utilisateur recoit une notification lorsque le fichier est pret a telecharger. Un lien de telechargement est disponible pendant 24 heures.
8. L'historique des exports est conserve pendant 30 jours : date, utilisateur, format, nombre d'entrees, filtres appliques. L'administrateur peut consulter cet historique dans les parametres du module.

---

### US-T11 : Statistiques et indicateurs de temps

**En tant que** dirigeant ou chef de projet,
**Je veux** consulter des statistiques detaillees et des indicateurs de performance sur les temps saisis,
**Afin d'** analyser la rentabilite des projets, la productivite de l'equipe et optimiser l'allocation des ressources.

**Criteres d'acceptance :**

1. La vue statistiques propose trois onglets d'analyse : "Par collaborateur", "Par projet", "Par phase". Chaque onglet presente un tableau de donnees et des graphiques interactifs.
2. L'onglet "Par collaborateur" affiche pour chaque collaborateur : heures totales saisies, heures facturables, taux de facturation (heures facturables / heures totales x 100), taux de saisie (heures saisies / heures ouvrables x 100), nombre de projets, cout salarial impute (heures x taux horaire interne). Un graphique en barres compare les collaborateurs entre eux sur le taux de facturation.
3. L'onglet "Par projet" affiche pour chaque projet : heures consommees, budget heures previsionnel, pourcentage de consommation, ecart en heures (positif = sous-consommation, negatif = depassement), montant facturable associe (heures x taux horaire du projet), marge estimee (honoraires - cout reel). Un graphique en barres horizontales montre la progression de chaque projet (heures consommees vs budget).
4. L'onglet "Par phase" affiche pour chaque phase standard (ESQ, APS, APD, PRO, DCE, DET, AOR) le total d'heures toutes projets confondus, le pourcentage moyen que represente cette phase dans un projet, et un comparatif inter-projets. Un graphique radar compare la repartition reelle des heures par phase avec une repartition de reference configurable.
5. Tous les tableaux sont filtrables par periode (dates de/a), equipe, et projet. Les graphiques se mettent a jour dynamiquement avec les filtres.
6. Un indicateur d'alerte est affiche pour : les projets dont la consommation depasse 80% du budget (orange) ou 100% (rouge), les collaborateurs dont le taux de saisie est inferieur a 80% (orange) ou 50% (rouge), les phases dont la consommation reelle depasse de plus de 20% la repartition de reference.
7. Les donnees statistiques sont exportables au format Excel et PDF. L'export Excel contient les tableaux de donnees. L'export PDF contient les tableaux et les graphiques sous forme d'images integrees.
8. Un comparateur de periodes permet de comparer deux periodes cote a cote (ex: ce trimestre vs trimestre precedent, cette annee vs annee precedente) avec calcul des ecarts absolus et en pourcentage.

---

## 6. Hors Perimetre

Les elements suivants ne sont **pas** couverts par l'EPIC-005 et feront l'objet d'EPICs dedies ou d'evolutions futures :

| Element | Raison / EPIC de rattachement |
|---|---|
| Gestion des conges et absences (demande, validation, soldes) | EPIC-006 Planning -- Le module Temps se limite a l'enregistrement du type "Conges" dans les heures |
| Facturation des temps aux clients | EPIC-003 Honoraires -- Le module Temps fournit les donnees, la facturation est geree dans les Honoraires |
| Workflow de validation complet (multi-niveaux, delegation) | EPIC-012 Validation -- Le module Temps propose un statut de validation simple (En attente/Valide/Refuse) |
| Planning previsionnel des heures par projet | EPIC-006 Planning -- Le module Temps gere le realise, pas le previsionnel |
| Notes de frais generales (hors deplacement) | Hors scope V1 -- Evolution future |
| Integration avec des systemes de pointage physique (badgeuse) | Hors scope V1 -- Evolution future |
| Application mobile native dediee au suivi de temps | Hors scope V1 -- L'application web responsive couvre les usages mobiles en V1 |
| Calcul automatique des itineraires et distances via API cartographique | Hors scope V1 -- La saisie manuelle de la distance est privilegiee en V1 |
| Suivi du temps par tache (niveau infra-phase) | Hors scope V1 -- La granularite s'arrete au niveau Phase |
| Rapprochement automatique temps/facturation | EPIC-003 Honoraires |

---

## 7. Regles Metier

### RM-T01 : Granularite de saisie
La duree minimale d'une entree de temps est de 15 minutes (0.25 heure). Toute saisie inferieure est automatiquement arrondie a 0.25h. La duree maximale d'une entree de temps pour une journee est de 24 heures.

### RM-T02 : Heures journalieres attendues
Le nombre d'heures attendues par jour ouvrable est configurable par l'administrateur (defaut : 7 heures). Ce parametre est utilise pour calculer le taux de saisie et les alertes de journee incomplete.

### RM-T03 : Heures hebdomadaires attendues
Le nombre d'heures attendues par semaine est derive du nombre d'heures journalieres x nombre de jours ouvrables (defaut : 7h x 5j = 35h). Ce parametre est utilise pour les alertes de semaine incomplete et le taux de saisie hebdomadaire.

### RM-T04 : Facturable par defaut
Une entree de temps est facturable par defaut si et seulement si le type de temps est "Production" ET que la phase du projet est marquee comme facturable dans le module Projets (EPIC-002). Tous les autres types (Administration, Conges, Formation) sont non facturables par defaut. L'utilisateur peut surcharger manuellement la propriete "facturable" de chaque entree.

### RM-T05 : Statut de validation
Une entree de temps suit le cycle de vie suivant : Brouillon (cree, non soumis) -> En attente de validation (soumis par le collaborateur) -> Valide (approuve par le manager) ou Refuse (rejete par le manager avec commentaire obligatoire). Une entree validee est verrouillee et ne peut etre modifiee que par un manager ou administrateur. Une entree refusee retourne au statut "Brouillon" et est modifiable par le collaborateur.

### RM-T06 : Validation hebdomadaire
La validation s'effectue a la maille de la semaine. Le collaborateur soumet sa semaine complete pour validation. Le manager valide ou refuse la semaine globalement ou entree par entree. Une semaine partiellement validee reste dans le statut "En attente" jusqu'a ce que toutes les entrees soient traitees.

### RM-T07 : Saisie retroactive
Par defaut, un collaborateur peut saisir du temps jusqu'a 30 jours dans le passe. Au-dela de ce delai, seul un manager ou administrateur peut creer ou modifier des entrees. Ce delai est configurable par l'administrateur.

### RM-T08 : Unicite de saisie
Un collaborateur ne peut pas saisir plus d'une entree pour la meme combinaison Date + Projet + Phase + Type de temps. Si une telle entree existe deja, le systeme propose de modifier l'entree existante plutot que d'en creer une nouvelle.

### RM-T09 : Coherence projet/phase
Seuls les projets auxquels le collaborateur est affecte (via le module Projets EPIC-002) et dont le statut est "En cours" ou "Actif" sont proposables dans la saisie de temps. Seules les phases actives du projet selectionne sont proposees.

### RM-T10 : Calcul du montant facturable
Le montant facturable d'une entree de temps est calcule selon la formule : montant = heures x taux horaire. Le taux horaire peut etre defini a plusieurs niveaux (par ordre de priorite decroissante) : taux specifique du projet/phase (EPIC-003), taux du collaborateur, taux par defaut de l'agence.

### RM-T11 : Calcul des frais de deplacement
Les frais de deplacement sont calcules selon la formule : montant = distance (km) x bareme kilometrique du mode de transport. Si le deplacement est en aller-retour, la distance est doublee avant application du bareme. Le montant peut etre surcharge manuellement.

### RM-T12 : Suppression logique
Toute suppression d'entree de temps ou de deplacement est une suppression logique (soft-delete). L'enregistrement est marque comme supprime (champ deleted_at renseigne) mais reste en base de donnees pour tracabilite et audit. Les entrees supprimees n'apparaissent pas dans les vues et les calculs.

### RM-T13 : Verrouillage des periodes
L'administrateur peut verrouiller une periode (mois) pour empecher toute saisie ou modification, typiquement apres la cloture comptable mensuelle. Les entrees d'une periode verrouillee ne sont ni modifiables ni supprimables, quel que soit le role de l'utilisateur.

---

## 8. Criteres d'Acceptance Globaux

### CAG-T01 : Performance
- Le chargement de la vue Resume (tableau de bord) s'effectue en moins de 2 secondes pour une agence de 50 collaborateurs et 12 mois de donnees.
- La grille de saisie hebdomadaire se charge en moins de 1 seconde et la sauvegarde s'effectue en moins de 1 seconde.
- Le journal des temps avec 10 000 entrees se pagine sans latence perceptible (< 500ms par page).
- L'export CSV de 10 000 entrees s'effectue en moins de 5 secondes. L'export Excel en moins de 10 secondes. L'export PDF en moins de 15 secondes.

### CAG-T02 : Accessibilite et ergonomie
- La saisie de temps quotidienne est realisable en moins de 5 minutes pour un collaborateur travaillant sur 3 a 5 projets.
- La navigation au clavier est complete dans la grille hebdomadaire (Tab, Entree, fleches directionnelles).
- Les raccourcis clavier sont documentes et accessibles via un panneau d'aide (touche "?").
- L'interface est conforme aux standards WCAG 2.1 niveau AA.

### CAG-T03 : Fiabilite des donnees
- Les totaux affiches (jour, semaine, mois) sont toujours coherents avec la somme des entrees sous-jacentes. Aucun ecart d'arrondi n'est tolere au-dela de 0.01h.
- Les modifications concurrentes sont gerees : si deux utilisateurs modifient la meme entree simultanement, le second recoit un message de conflit et doit rafraichir avant de modifier.
- Toute modification d'une entree de temps est tracee dans l'historique d'audit (date, utilisateur, champs modifies, anciennes et nouvelles valeurs).

### CAG-T04 : Securite et droits d'acces
- Un collaborateur ne peut consulter et modifier que ses propres entrees de temps.
- Un manager peut consulter les entrees de temps de son equipe et effectuer des validations/refus.
- Un administrateur a acces a toutes les entrees de temps et a la configuration du module.
- Les exports contiennent uniquement les donnees accessibles par le role de l'utilisateur.

### CAG-T05 : Responsivite
- Le module est utilisable sur ecran desktop (>= 1280px), tablette (>= 768px) et mobile (>= 375px).
- La saisie quotidienne est optimisee pour une utilisation sur tablette (ecrans tactiles).
- La grille hebdomadaire bascule en mode saisie quotidienne sur les ecrans inferieurs a 768px.

### CAG-T06 : Integration
- Les donnees de temps sont accessibles en temps reel par le module Honoraires (EPIC-003) pour le calcul des montants facturables.
- Les projets et phases affiches dans le module Temps sont synchronises avec le module Projets (EPIC-002). La creation ou l'archivage d'un projet dans EPIC-002 se repercute immediatement dans les listes du module Temps.
- Les donnees de temps alimentent les indicateurs du module Planning (EPIC-006) pour la comparaison previsionnel vs realise.

---

## 9. Definition of Done

Une User Story de l'EPIC-005 est consideree comme "Done" lorsque tous les criteres suivants sont satisfaits :

### Developpement
- [ ] Le code source est ecrit, revise (code review par au moins un pair) et merge dans la branche de developpement.
- [ ] Le code respecte les conventions de codage du projet (linting, formatting).
- [ ] Les composants UI sont implementes conformement aux maquettes validees (ecart visuel < 5%).
- [ ] Les appels API sont implementes avec gestion des erreurs (codes HTTP 4xx et 5xx) et messages d'erreur utilisateur explicites.
- [ ] Les traductions francaises de tous les libelles, messages et erreurs sont en place.

### Tests
- [ ] Les tests unitaires couvrent au minimum 80% du code metier (services, calculs, regles de validation).
- [ ] Les tests d'integration couvrent les interactions entre le module Temps et les modules dependants (Projets, Honoraires).
- [ ] Les tests end-to-end (E2E) couvrent les parcours utilisateur principaux : saisie quotidienne, saisie hebdomadaire, validation, export.
- [ ] Les tests de performance valident les seuils definis dans les criteres d'acceptance globaux (CAG-T01).
- [ ] Les tests d'accessibilite (axe, lighthouse) confirment la conformite WCAG 2.1 AA.
- [ ] Les tests de responsivite sont executes sur les trois breakpoints (desktop, tablette, mobile).

### Documentation
- [ ] La documentation technique de l'API est a jour (endpoints, parametres, reponses, codes d'erreur).
- [ ] Le guide utilisateur du module Temps est redige avec captures d'ecran.
- [ ] Les regles metier sont documentees dans le wiki technique.

### Validation
- [ ] La User Story est demontree au Product Owner lors de la sprint review.
- [ ] Les criteres d'acceptance de la User Story sont valides (check-list completee).
- [ ] Le Product Owner a formellement accepte la livraison.
- [ ] Aucun bug bloquant ou majeur n'est ouvert sur les fonctionnalites de la User Story.

### Deploiement
- [ ] Le code est deployable en environnement de staging sans intervention manuelle.
- [ ] Les scripts de migration de base de donnees sont testes et reversibles.
- [ ] Les variables de configuration sont documentees et parametrees pour chaque environnement.

---

## 10. Dependances

### 10.1 Dependances entrantes (modules dont EPIC-005 depend)

| Module | Nature de la dependance | Impact |
|---|---|---|
| **EPIC-002 Projets** | Liste des projets, phases, affectation des collaborateurs aux projets. Le module Temps interroge les donnees de EPIC-002 pour alimenter les listes deroulantes de saisie et valider que le collaborateur est bien affecte au projet. | **Bloquant** -- Impossible de saisir du temps sans la structure projet/phase. |
| **EPIC-003 Honoraires** | Taux horaires (par projet, par collaborateur, par defaut agence) pour le calcul des montants facturables. Budget d'heures previsionnel par projet/phase pour les indicateurs de consommation. | **Important** -- Les montants facturables et les indicateurs de depassement budgetaire ne fonctionnent pas sans ces donnees. |
| **Module Utilisateurs / Equipe** | Liste des collaborateurs, roles (collaborateur, manager, administrateur), rattachement a une equipe/service. | **Bloquant** -- Impossible d'identifier le collaborateur saisissant et de gerer les droits d'acces. |

### 10.2 Dependances sortantes (modules qui dependent de EPIC-005)

| Module | Nature de la dependance | Impact |
|---|---|---|
| **EPIC-003 Honoraires** | Les heures saisies et validees dans le module Temps alimentent le calcul des honoraires a facturer. Le montant facturable d'une entree de temps est utilise pour le suivi de la marge. | Les honoraires ne peuvent pas etre calcules automatiquement sans les donnees de temps. |
| **EPIC-006 Planning** | Les heures realisees dans le module Temps sont comparees aux heures previsionnelles du planning pour mesurer les ecarts et ajuster les previsions. | La comparaison previsionnel/realise est impossible sans les donnees de temps. |
| **EPIC-012 Validation** | Le workflow de validation des feuilles de temps exploite les donnees de EPIC-005. Les statuts de validation (En attente, Valide, Refuse) sont partages entre les deux modules. | Le workflow de validation ne peut pas fonctionner sans les entrees de temps a valider. |

### 10.3 Dependances techniques

| Composant | Description |
|---|---|
| **API REST backend** | Endpoints CRUD pour les entrees de temps, deplacements, configuration. Authentification JWT. |
| **Base de donnees relationnelle** | PostgreSQL pour le stockage des entrees de temps, deplacements, configuration, audit. |
| **Systeme de notifications** | Notifications in-app et email pour les alertes de saisie et les resultats de validation. |
| **Bibliotheque de graphiques** | Chart.js, Recharts ou equivalent pour les graphiques du tableau de bord et des statistiques. |
| **Bibliotheque d'export** | Librairie de generation CSV, Excel (xlsx) et PDF cote serveur. |

---

## 11. Modele de Donnees Principal

### 11.1 Table `time_entries` (Entrees de temps)

| Champ | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK, NOT NULL | Identifiant unique de l'entree de temps |
| `employee_id` | UUID | FK -> users.id, NOT NULL | Collaborateur ayant saisi l'entree |
| `project_id` | UUID | FK -> projects.id, NOT NULL | Projet concerne |
| `phase_id` | UUID | FK -> phases.id, NULL | Phase du projet (nullable si saisie sans phase) |
| `date` | DATE | NOT NULL, INDEX | Date de l'entree de temps |
| `hours` | DECIMAL(5,2) | NOT NULL, CHECK >= 0.25 | Duree en heures (min 0.25, max 24.00) |
| `type` | VARCHAR(50) | NOT NULL | Type de temps (Production, Administration, Conges, Formation) |
| `subtype` | VARCHAR(50) | NULL | Sous-type de temps (ex: Conception, Dessin, Reunion) |
| `description` | TEXT | NULL, MAX 500 chars | Description / commentaire de l'entree |
| `is_billable` | BOOLEAN | NOT NULL, DEFAULT true | Indique si l'entree est facturable |
| `billable_amount` | DECIMAL(10,2) | NULL | Montant facturable calcule (heures x taux horaire) |
| `hourly_rate` | DECIMAL(8,2) | NULL | Taux horaire applique au moment de la saisie |
| `status` | VARCHAR(20) | NOT NULL, DEFAULT 'draft' | Statut de validation (draft, pending, approved, rejected) |
| `validation_comment` | TEXT | NULL | Commentaire du manager en cas de refus |
| `validated_by` | UUID | FK -> users.id, NULL | Manager ayant valide/refuse |
| `validated_at` | TIMESTAMP | NULL | Date/heure de validation |
| `timer_started_at` | TIMESTAMP | NULL | Heure de demarrage du chronometre (si applicable) |
| `timer_stopped_at` | TIMESTAMP | NULL | Heure d'arret du chronometre (si applicable) |
| `source` | VARCHAR(20) | NOT NULL, DEFAULT 'manual' | Source de la saisie (manual, timer, copy, api) |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date de creation |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date de derniere modification |
| `deleted_at` | TIMESTAMP | NULL | Date de suppression logique (soft-delete) |

**Index :**
- `idx_time_entries_employee_date` : (employee_id, date) -- Recherche des entrees par collaborateur et date
- `idx_time_entries_project` : (project_id) -- Recherche des entrees par projet
- `idx_time_entries_status` : (status) -- Filtrage par statut de validation
- `idx_time_entries_type` : (type) -- Filtrage par type de temps
- `idx_time_entries_date` : (date) -- Tri et filtrage par date

**Contrainte d'unicite :**
- `uq_time_entries_unique` : UNIQUE (employee_id, project_id, phase_id, date, type, deleted_at) -- Empeche les doublons

---

### 11.2 Table `travels` (Deplacements)

| Champ | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK, NOT NULL | Identifiant unique du deplacement |
| `employee_id` | UUID | FK -> users.id, NOT NULL | Collaborateur concerne |
| `project_id` | UUID | FK -> projects.id, NULL | Projet associe (optionnel) |
| `time_entry_id` | UUID | FK -> time_entries.id, NULL | Entree de temps liee (optionnel) |
| `date` | DATE | NOT NULL | Date du deplacement |
| `departure_location` | VARCHAR(255) | NOT NULL | Lieu de depart |
| `arrival_location` | VARCHAR(255) | NOT NULL | Lieu d'arrivee |
| `distance_km` | DECIMAL(7,1) | NOT NULL, CHECK > 0 | Distance en kilometres |
| `is_round_trip` | BOOLEAN | NOT NULL, DEFAULT false | Aller-retour (si true, distance effective = distance x 2) |
| `transport_mode` | VARCHAR(50) | NOT NULL | Mode de transport (personal_car, company_car, public_transport, bicycle, other) |
| `mileage_rate` | DECIMAL(5,3) | NOT NULL | Bareme kilometrique applique au moment de la saisie (EUR/km) |
| `amount` | DECIMAL(8,2) | NOT NULL | Montant des frais calcule |
| `amount_override` | BOOLEAN | NOT NULL, DEFAULT false | Indique si le montant a ete saisi manuellement |
| `comment` | TEXT | NULL, MAX 300 chars | Commentaire / motif du deplacement |
| `status` | VARCHAR(20) | NOT NULL, DEFAULT 'draft' | Statut (draft, pending, approved, rejected) |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date de creation |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date de derniere modification |
| `deleted_at` | TIMESTAMP | NULL | Date de suppression logique |

**Index :**
- `idx_travels_employee_date` : (employee_id, date)
- `idx_travels_project` : (project_id)

---

### 11.3 Table `time_types` (Types de temps)

| Champ | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK, NOT NULL | Identifiant unique |
| `name` | VARCHAR(50) | NOT NULL, UNIQUE | Nom du type de temps |
| `code` | VARCHAR(10) | NOT NULL, UNIQUE | Code court |
| `parent_id` | UUID | FK -> time_types.id, NULL | Type parent (pour les sous-types) |
| `is_billable_default` | BOOLEAN | NOT NULL, DEFAULT false | Facturable par defaut |
| `color` | VARCHAR(7) | NOT NULL, DEFAULT '#3B82F6' | Couleur hexadecimale pour l'affichage |
| `is_active` | BOOLEAN | NOT NULL, DEFAULT true | Type actif (visible dans les listes de saisie) |
| `display_order` | INTEGER | NOT NULL, DEFAULT 0 | Ordre d'affichage dans les listes |
| `is_system` | BOOLEAN | NOT NULL, DEFAULT false | Type systeme (non supprimable) |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date de creation |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date de derniere modification |

---

### 11.4 Table `time_settings` (Configuration du module)

| Champ | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK, NOT NULL | Identifiant unique |
| `organization_id` | UUID | FK -> organizations.id, NOT NULL, UNIQUE | Agence concernee |
| `time_unit` | VARCHAR(10) | NOT NULL, DEFAULT 'hours' | Unite de saisie (hours, days) |
| `hours_per_day` | DECIMAL(4,2) | NOT NULL, DEFAULT 7.00 | Nombre d'heures par jour ouvrable |
| `days_per_week` | INTEGER | NOT NULL, DEFAULT 5 | Nombre de jours ouvrables par semaine |
| `working_days` | VARCHAR(20) | NOT NULL, DEFAULT '1,2,3,4,5' | Jours ouvrables (1=Lundi ... 7=Dimanche) |
| `min_granularity_minutes` | INTEGER | NOT NULL, DEFAULT 15 | Granularite minimale en minutes |
| `max_retroactive_days` | INTEGER | NOT NULL, DEFAULT 30 | Delai max de saisie retroactive (jours) |
| `mandatory_submission` | BOOLEAN | NOT NULL, DEFAULT false | Saisie obligatoire avant soumission |
| `mandatory_threshold_pct` | INTEGER | NOT NULL, DEFAULT 80 | Seuil minimum de saisie pour soumission (%) |
| `daily_warning_hours` | DECIMAL(4,2) | NOT NULL, DEFAULT 10.00 | Seuil d'alerte journalier (heures) |
| `weekly_warning_hours` | DECIMAL(5,2) | NOT NULL, DEFAULT 45.00 | Seuil d'alerte hebdomadaire (heures) |
| `show_weekends` | BOOLEAN | NOT NULL, DEFAULT false | Afficher Samedi/Dimanche dans la grille |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date de creation |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date de derniere modification |

---

### 11.5 Table `mileage_rates` (Baremes kilometriques)

| Champ | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK, NOT NULL | Identifiant unique |
| `organization_id` | UUID | FK -> organizations.id, NOT NULL | Agence concernee |
| `transport_mode` | VARCHAR(50) | NOT NULL | Mode de transport |
| `rate_per_km` | DECIMAL(5,3) | NOT NULL | Taux par kilometre (EUR/km) |
| `effective_date` | DATE | NOT NULL | Date d'entree en vigueur du bareme |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date de creation |

**Contrainte d'unicite :**
- `uq_mileage_rates` : UNIQUE (organization_id, transport_mode, effective_date)

---

### 11.6 Table `time_locks` (Verrouillage de periodes)

| Champ | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK, NOT NULL | Identifiant unique |
| `organization_id` | UUID | FK -> organizations.id, NOT NULL | Agence concernee |
| `year` | INTEGER | NOT NULL | Annee verrrouillee |
| `month` | INTEGER | NOT NULL, CHECK 1-12 | Mois verrouille |
| `locked_by` | UUID | FK -> users.id, NOT NULL | Administrateur ayant verrouille |
| `locked_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date de verrouillage |

**Contrainte d'unicite :**
- `uq_time_locks` : UNIQUE (organization_id, year, month)

---

### 11.7 Table `time_audit_log` (Journal d'audit)

| Champ | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK, NOT NULL | Identifiant unique |
| `entity_type` | VARCHAR(50) | NOT NULL | Type d'entite (time_entry, travel, time_settings) |
| `entity_id` | UUID | NOT NULL | Identifiant de l'entite modifiee |
| `action` | VARCHAR(20) | NOT NULL | Action (create, update, delete, validate, reject) |
| `user_id` | UUID | FK -> users.id, NOT NULL | Utilisateur ayant effectue l'action |
| `changes` | JSONB | NULL | Detail des modifications (ancien/nouveau) |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date de l'action |

**Index :**
- `idx_audit_entity` : (entity_type, entity_id)
- `idx_audit_date` : (created_at)

---

### 11.8 Diagramme relationnel simplifie

```
users (EPIC Equipe)
  |
  |-- 1:N --> time_entries
  |             |-- N:1 --> projects (EPIC-002)
  |             |-- N:1 --> phases (EPIC-002)
  |             |-- N:1 --> time_types
  |
  |-- 1:N --> travels
  |             |-- N:1 --> projects (EPIC-002)
  |             |-- N:1 --> time_entries (optionnel)
  |
  |-- 1:N --> time_audit_log

organizations
  |
  |-- 1:1 --> time_settings
  |-- 1:N --> mileage_rates
  |-- 1:N --> time_locks
  |-- 1:N --> time_types
```

---

## 12. Estimation & Decoupage

### 12.1 Estimation globale

| Metrique | Valeur |
|---|---|
| **Duree estimee** | 6 a 9 semaines |
| **Nombre de sprints** | 4 a 5 sprints (sprints de 2 semaines) |
| **Effort total estime** | 320 a 480 heures-homme |
| **Equipe recommandee** | 2 developpeurs frontend, 1 developpeur backend, 1 QA, 1 UX/UI (a temps partiel) |

### 12.2 Decoupage en sprints

#### Sprint 1 -- Fondations et saisie quotidienne (Semaines 1-2)

| User Story | Effort estime | Priorite |
|---|---|---|
| Modele de donnees et API CRUD time_entries | 24h | Critique |
| US-T07 : Types de temps et categorisation (backend + admin) | 16h | Critique |
| US-T02 : Saisie de temps quotidienne (frontend + backend) | 32h | Critique |
| US-T09 : Configuration heures/jours (backend + admin) | 16h | Haute |
| **Total Sprint 1** | **88h** | |

**Objectif Sprint 1 :** Un collaborateur peut saisir, modifier et supprimer des entrees de temps au quotidien. L'administrateur peut configurer les types de temps et l'unite de saisie.

#### Sprint 2 -- Saisie hebdomadaire et calendrier (Semaines 3-4)

| User Story | Effort estime | Priorite |
|---|---|---|
| US-T03 : Saisie hebdomadaire / grille semaine | 40h | Critique |
| US-T08 : Copie de la semaine precedente | 16h | Haute |
| US-T04 : Vue Calendrier des temps | 24h | Haute |
| Timer / Chronometre (sous-fonctionnalite de US-T02) | 16h | Moyenne |
| **Total Sprint 2** | **96h** | |

**Objectif Sprint 2 :** Le collaborateur dispose de trois modes de saisie (quotidien, hebdomadaire, calendrier) et peut copier la structure d'une semaine precedente. Le chronometre est fonctionnel.

#### Sprint 3 -- Deplacements, journaux et validation (Semaines 5-6)

| User Story | Effort estime | Priorite |
|---|---|---|
| US-T05 : Gestion des deplacements | 32h | Haute |
| US-T06 : Journaux de travail (historique) | 24h | Haute |
| Workflow de validation (statuts, soumission, validation/refus) | 24h | Critique |
| Vue Semaines (suivi de validation hebdomadaire) | 16h | Haute |
| **Total Sprint 3** | **96h** | |

**Objectif Sprint 3 :** Les deplacements peuvent etre saisis et les frais calcules. Le journal complet est consultable avec filtres avances. Le workflow de validation est operationnel.

#### Sprint 4 -- Statistiques, export et tableau de bord (Semaines 7-8)

| User Story | Effort estime | Priorite |
|---|---|---|
| US-T01 : Vue resume des temps (KPIs, graphiques) | 32h | Haute |
| US-T11 : Statistiques et indicateurs de temps | 32h | Haute |
| US-T10 : Export CSV, Excel, PDF | 24h | Haute |
| **Total Sprint 4** | **88h** | |

**Objectif Sprint 4 :** Le tableau de bord est fonctionnel avec les KPIs et graphiques. Les statistiques detaillees sont disponibles. Les exports fonctionnent dans les trois formats.

#### Sprint 5 -- Integration, tests et finalisation (Semaines 8-9)

| User Story | Effort estime | Priorite |
|---|---|---|
| Integration EPIC-003 Honoraires (montants facturables, taux horaires) | 24h | Haute |
| Integration EPIC-006 Planning (previsionnel vs realise) | 16h | Moyenne |
| Verrouillage de periodes (time_locks) | 8h | Moyenne |
| Tests end-to-end, tests de performance, corrections | 32h | Critique |
| Responsivite (tablette, mobile) | 16h | Haute |
| Documentation utilisateur et technique | 16h | Haute |
| **Total Sprint 5** | **112h** | |

**Objectif Sprint 5 :** Le module est integre avec les modules dependants, entierement teste, responsive et documente. Pret pour la mise en production.

### 12.3 Risques et mitigations

| Risque | Probabilite | Impact | Mitigation |
|---|---|---|---|
| Retard sur EPIC-002 Projets (dependance bloquante) | Moyenne | Critique | Prevoir des donnees de test (mock) pour demarrer le developpement independamment. Definir un contrat d'API stable des le Sprint 1. |
| Complexite de la grille hebdomadaire (performance, UX) | Haute | Haute | Prototyper l'UI de la grille en Sprint 1. Valider le choix technique (librairie de grid) avant l'implementation. |
| Volume de donnees en production (performance des statistiques) | Moyenne | Moyenne | Implementer la pagination et le chargement paresseux. Prevoir des index de base de donnees optimises. Tester avec des jeux de donnees realistes (50 collaborateurs x 12 mois). |
| Integration des calculs d'honoraires | Moyenne | Haute | Definir les interfaces (taux horaires, budgets) avec l'equipe EPIC-003 des le Sprint 1. |
| Adoption par les utilisateurs (resistance a la saisie de temps) | Haute | Moyenne | Investir dans l'ergonomie (saisie rapide, copie, chronometre). Former les utilisateurs. |

---

*Document redige le 26 fevrier 2026 -- EPIC-005 Module Temps -- Version 1.0*
