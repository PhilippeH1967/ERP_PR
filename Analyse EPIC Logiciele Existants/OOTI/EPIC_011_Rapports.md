# EPIC -- Module Rapports

**Application OOTI -- Gestion de projets pour cabinets d'architecture**
**Version 1.0 -- Fevrier 2026**

---

## 1. Identification

| Champ | Valeur |
|---|---|
| **Nom de l'EPIC** | Rapports |
| **Reference** | EPIC-011 |
| **Module parent** | Gestion |
| **Priorite** | Moyenne |
| **Responsable produit** | A definir |
| **Date de creation** | 26/02/2026 |
| **Derniere mise a jour** | 26/02/2026 |
| **Statut** | A faire |
| **EPICs lies** | EPIC-002 Projets, EPIC-003 Honoraires, EPIC-004 Facturation, EPIC-005 Temps, EPIC-007 Couts, EPIC-008 Finances |

---

## 2. Contexte et Problematique

### 2.1 Contexte

Les cabinets d'architecture gerent simultanement de nombreux projets, chacun impliquant des dimensions financieres (honoraires, facturation, couts), temporelles (temps passes, taux d'occupation) et operationnelles (avancement, phases, livrables). Les dirigeants, chefs de projet et responsables administratifs ont besoin d'une vision synthetique et transversale de l'ensemble de ces donnees pour piloter efficacement leur activite.

Actuellement, dans OOTI, les donnees sont reparties dans plusieurs modules (Projets, Honoraires, Facturation, Temps, Couts, Finances). Le module Rapports constitue la couche d'agregation et de restitution qui permet de croiser, synthetiser et presenter ces donnees sous forme de tableaux, graphiques et documents exportables.

Le module est accessible via le menu **GESTION > Rapports** (avec deux sous-menus : Rapports et Rapports planifies) ainsi qu'au niveau de chaque projet via l'onglet **PLUS > Rapports** pour des rapports specifiques au projet consulte.

### 2.2 Problematique

Sans un module de rapports centralise, les cabinets d'architecture rencontrent les difficultes suivantes :

- **Absence de vision consolidee** : les donnees financieres, temporelles et operationnelles sont dispersees dans differents modules, obligeant les utilisateurs a naviguer entre de multiples ecrans pour reconstituer manuellement une vue d'ensemble.
- **Perte de temps dans la preparation de reportings** : les dirigeants et responsables administratifs passent un temps considerable a extraire, compiler et mettre en forme des donnees pour produire des rapports de suivi destines aux associes, aux clients ou aux partenaires.
- **Manque de recurrence et d'automatisation** : sans mecanisme de planification, les rapports periodiques (hebdomadaires, mensuels) doivent etre regeneres manuellement a chaque echeance, avec un risque d'oubli ou d'incoherence.
- **Difficulte a identifier les derives** : sans indicateurs agreges et graphiques de tendance, les alertes sur les depassements de budget, les retards de facturation ou les taux d'occupation insuffisants arrivent trop tard pour permettre des actions correctives.
- **Formats non standardises** : les exports ad hoc produisent des documents heterogenes, compliquant la communication interne et externe.

---

## 3. Objectif

### 3.1 Objectif principal

Fournir aux utilisateurs de l'application OOTI un module de rapports complet, flexible et automatisable, permettant de generer, personnaliser, exporter et planifier des rapports couvrant l'ensemble des dimensions de gestion d'un cabinet d'architecture (honoraires, budgets, temps, facturation, couts, marges, avancement, taux d'occupation).

### 3.2 Objectifs specifiques

| # | Objectif | Indicateur de succes |
|---|---|---|
| O1 | Centraliser l'acces aux rapports dans une bibliotheque unique et structuree | 100% des types de rapports accessibles depuis GESTION > Rapports |
| O2 | Permettre la generation de rapports a la demande avec filtres personnalisables | Temps de generation d'un rapport < 10 secondes pour les rapports standard |
| O3 | Proposer des exports multi-formats (PDF, Excel, CSV) | 3 formats d'export disponibles pour chaque type de rapport |
| O4 | Automatiser l'envoi recurrent de rapports par email | Configuration d'un rapport planifie en moins de 2 minutes |
| O5 | Offrir des rapports projet detailles accessibles depuis le contexte du projet | Acces au rapport projet en 2 clics maximum depuis la fiche projet |
| O6 | Integrer des visualisations graphiques pour faciliter l'analyse | Au moins 3 types de graphiques disponibles (barres, lignes, camemberts) |
| O7 | Conserver un historique des rapports generes pour tracabilite | Historique consultable sur 24 mois minimum |

---

## 4. Perimetre Fonctionnel

### 4.1 Sous-menus et navigation

| Acces | Emplacement | Description |
|---|---|---|
| Rapports globaux | GESTION > Rapports > Rapports | Bibliotheque de rapports predefinis, generation a la demande, historique |
| Rapports planifies | GESTION > Rapports > Rapports planifies | Configuration et gestion des rapports automatiques recurrents |
| Rapports projet | Fiche projet > Onglet PLUS > Rapports | Rapports specifiques au projet selectionne |

### 4.2 Types de rapports disponibles

| Type de rapport | Description | Donnees sources (EPIC) |
|---|---|---|
| **Honoraires signes** | Montant des honoraires signes par projet, par client, par periode | EPIC-003 Honoraires |
| **Budgets facturables** | Budgets alloues et consommes, ecarts, projections | EPIC-003 Honoraires, EPIC-004 Facturation |
| **Temps saisis** | Temps passes par collaborateur, par projet, par phase, par periode | EPIC-005 Temps |
| **Facturation** | Factures emises, montants encaisses, impayes, retards de paiement | EPIC-004 Facturation |
| **Couts** | Couts par categorie (sous-traitants, salaires, frais generaux), par projet | EPIC-007 Couts |
| **Marge** | Marge par projet, par annee, comparaison previsionnel/reel | EPIC-003, EPIC-004, EPIC-007 |
| **Avancement des projets** | Etat d'avancement, phases en cours, jalons, retards | EPIC-002 Projets |
| **Taux d'occupation** | Taux d'occupation des collaborateurs, repartition par projet | EPIC-005 Temps |

### 4.3 Fonctionnalites principales

1. **Bibliotheque de rapports predefinis** : catalogue structure par type (Honoraires, Budget, Temps, Facturation, Couts, Marge, Avancement) avec description et apercu.
2. **Generation a la demande** : selection d'un type de rapport, application de filtres (periode, projet, collaborateur, client), generation instantanee.
3. **Filtres personnalisables** : selection multi-criteres sur periode, projet(s), collaborateur(s), client(s), phase(s), statut(s).
4. **Personnalisation de l'affichage** : choix des colonnes visibles, regroupements (par projet, par client, par mois...), tri (ascendant/descendant).
5. **Visualisations graphiques** : graphiques a barres, courbes de tendance, diagrammes circulaires, tableaux croises.
6. **Exports multi-formats** : PDF (mise en page professionnelle avec en-tete cabinet), Excel (donnees exploitables avec formules), CSV (donnees brutes).
7. **Rapports planifies** : configuration de la frequence (quotidien, hebdomadaire, mensuel), selection des destinataires (emails), activation/desactivation.
8. **Envoi automatique par email** : generation automatique du rapport au format choisi et envoi aux destinataires configures selon le planning defini.
9. **Rapports projet** : rapport detaille consolide pour un projet specifique, regroupant honoraires, temps, couts, marge et avancement.
10. **Historique des rapports** : conservation de chaque rapport genere avec date, auteur, parametres utilises et lien de telechargement.

---

## 5. User Stories

### US-R01 : Bibliotheque des rapports disponibles

**En tant que** utilisateur de l'application (dirigeant, chef de projet, responsable administratif),
**je veux** acceder a une bibliotheque structuree de rapports predefinis depuis le menu GESTION > Rapports,
**afin de** visualiser l'ensemble des rapports disponibles, comprendre leur contenu et selectionner rapidement le rapport adapte a mon besoin.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---|---|
| CA-01 | La page GESTION > Rapports affiche la liste de tous les types de rapports disponibles, organises par categorie (Honoraires, Budget, Temps, Facturation, Couts, Marge, Avancement, Taux d'occupation) | Verification visuelle : toutes les categories sont presentes et correctement nommees |
| CA-02 | Chaque rapport dans la bibliotheque affiche un nom, une description courte, une icone representative de la categorie et un bouton "Generer" | Verification visuelle : les 4 elements sont presents pour chaque rapport |
| CA-03 | Un champ de recherche permet de filtrer la liste des rapports par mot-cle (nom ou description) | Test : saisie de "marge" filtre et affiche uniquement les rapports contenant ce terme |
| CA-04 | Les rapports sont filtrables par categorie via des onglets ou des tags cliquables | Test : clic sur la categorie "Temps" affiche uniquement les rapports lies au temps |
| CA-05 | Un clic sur "Generer" ouvre l'ecran de parametrage du rapport selectionne avec les filtres pre-remplis par defaut | Test : clic sur "Generer" pour le rapport "Honoraires signes" ouvre le formulaire avec la periode par defaut (mois en cours) |
| CA-06 | La page affiche un compteur du nombre total de rapports disponibles et du nombre affiche apres filtrage | Verification : le compteur se met a jour dynamiquement lors du filtrage |
| CA-07 | Les rapports recemment generes par l'utilisateur sont mis en avant dans une section "Rapports recents" en haut de page (5 derniers) | Verification : apres generation de rapports, la section "Rapports recents" affiche les 5 derniers avec date et lien de telechargement |
| CA-08 | L'acces a la bibliotheque est restreint selon les permissions de l'utilisateur : un collaborateur standard ne voit que les rapports de type Temps et Avancement, un dirigeant voit tous les rapports | Test avec 2 profils differents : verification du filtrage par role |

---

### US-R02 : Generation d'un rapport a la demande

**En tant que** utilisateur autorise,
**je veux** pouvoir generer un rapport a la demande en selectionnant un type de rapport et en lancant la generation,
**afin de** obtenir instantanement un rapport a jour contenant les donnees les plus recentes du systeme.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---|---|
| CA-01 | L'utilisateur peut selectionner un type de rapport parmi la liste disponible et lancer la generation via un bouton "Generer le rapport" | Test : selection du rapport "Temps saisis" + clic sur "Generer le rapport" |
| CA-02 | Un indicateur de progression (spinner ou barre de progression) s'affiche pendant la generation du rapport | Verification visuelle : l'indicateur est visible pendant le traitement |
| CA-03 | Le rapport genere s'affiche a l'ecran sous forme de tableau avec les donnees correspondantes, dans un delai inferieur a 10 secondes pour les rapports standard (moins de 10 000 lignes) | Test de performance : chronometrage de la generation |
| CA-04 | Le rapport genere affiche un en-tete contenant le nom du rapport, la date de generation, la periode couverte et le nom de l'utilisateur qui l'a genere | Verification visuelle des 4 elements dans l'en-tete |
| CA-05 | Le rapport genere est automatiquement enregistre dans l'historique avec ses parametres (type, filtres, date, auteur) | Test : verification de l'apparition du rapport dans l'historique apres generation |
| CA-06 | En cas d'absence de donnees pour les criteres selectionnes, un message explicite "Aucune donnee ne correspond aux criteres selectionnes" s'affiche avec la possibilite de modifier les filtres | Test : generation d'un rapport avec des filtres ne retournant aucun resultat |
| CA-07 | L'utilisateur peut relancer la generation du meme rapport avec les memes parametres via un bouton "Actualiser" sans avoir a reconfigurer les filtres | Test : clic sur "Actualiser" regenere le rapport avec les donnees a jour |
| CA-08 | Si la generation echoue (timeout, erreur serveur), un message d'erreur clair s'affiche avec la possibilite de reessayer | Test : simulation d'une erreur serveur et verification du message |

---

### US-R03 : Filtrage et personnalisation d'un rapport

**En tant que** utilisateur autorise,
**je veux** pouvoir appliquer des filtres (periode, projet, collaborateur, client, phase) et personnaliser l'affichage d'un rapport (colonnes, regroupements, tri),
**afin de** obtenir un rapport cible correspondant exactement a mon besoin d'analyse et ne contenant que les informations pertinentes.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---|---|
| CA-01 | L'ecran de parametrage propose des filtres adaptes au type de rapport : periode (date debut/fin), projet(s), collaborateur(s), client(s), phase(s) avec selection multiple | Test : ouverture du parametrage pour chaque type de rapport et verification de la presence des filtres pertinents |
| CA-02 | Les filtres de type "entite" (projet, collaborateur, client) proposent une recherche auto-complete avec selection multiple et affichage du nombre d'elements selectionnes | Test : saisie de 3 caracteres dans le filtre "Projet" et verification de l'auto-complete, selection de 3 projets |
| CA-03 | Le filtre de periode propose des raccourcis predefinis (Mois en cours, Trimestre en cours, Annee en cours, Mois precedent, Annee precedente) en plus de la selection manuelle de dates | Test : clic sur "Trimestre en cours" et verification que les dates sont correctement pre-remplies |
| CA-04 | L'utilisateur peut choisir les colonnes visibles dans le rapport via un panneau de selection avec cases a cocher, avec un minimum de 2 colonnes obligatoires | Test : desactivation de colonnes et verification de leur disparition dans le rapport |
| CA-05 | L'utilisateur peut definir un regroupement des donnees (par projet, par client, par mois, par collaborateur, par phase) avec un ou deux niveaux de regroupement | Test : regroupement par "Client" puis sous-regroupement par "Projet" et verification de la hierarchie |
| CA-06 | L'utilisateur peut definir le tri du rapport (colonne de tri + ordre ascendant/descendant) en cliquant sur l'en-tete de colonne | Test : clic sur l'en-tete "Montant" pour trier par montant decroissant |
| CA-07 | Les parametres de filtrage et de personnalisation peuvent etre sauvegardes comme "configuration favorite" avec un nom personnalise pour reutilisation ulterieure | Test : sauvegarde d'une configuration, fermeture du rapport, reouverture et chargement de la configuration sauvegardee |
| CA-08 | Un bouton "Reinitialiser les filtres" permet de revenir aux valeurs par defaut du rapport en un clic | Test : modification de plusieurs filtres, clic sur "Reinitialiser" et verification du retour aux valeurs par defaut |

---

### US-R04 : Export de rapports (PDF, Excel, CSV)

**En tant que** utilisateur autorise,
**je veux** pouvoir exporter un rapport genere aux formats PDF, Excel ou CSV,
**afin de** partager le rapport avec des collaborateurs, clients ou partenaires, ou l'exploiter dans des outils externes (tableur, logiciel comptable).

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---|---|
| CA-01 | Un bouton "Exporter" est present sur chaque rapport genere, proposant un menu deroulant avec les trois formats : PDF, Excel (.xlsx), CSV | Verification visuelle : le bouton et les 3 options sont presents |
| CA-02 | L'export PDF genere un document mis en page de maniere professionnelle avec en-tete (logo du cabinet si configure, nom du rapport, date, periode), tableau de donnees, et pied de page (pagination) | Verification du PDF genere : presence de l'en-tete, du tableau et du pied de page |
| CA-03 | L'export PDF inclut les graphiques presents dans le rapport a l'ecran (barres, courbes, camemberts) en haute resolution | Verification du PDF : les graphiques sont presents et lisibles |
| CA-04 | L'export Excel genere un fichier .xlsx avec les donnees structurees en colonnes, les en-tetes de colonnes en gras, et les formules de totaux en bas de tableau | Verification du fichier Excel : structure, formatage et formules |
| CA-05 | L'export CSV genere un fichier encodage UTF-8 avec separateur point-virgule, compatible avec les outils comptables et les tableurs francais | Test : ouverture du CSV dans un tableur et verification de l'encodage des caracteres accentues et du separateur |
| CA-06 | Le nom du fichier exporte suit la convention : [TypeRapport]_[Periode]_[DateGeneration].[extension] (ex : Honoraires_2026-01_20260226.pdf) | Verification du nom du fichier telecharge |
| CA-07 | L'export d'un rapport volumineux (plus de 5 000 lignes) est realise en traitement asynchrone avec notification a l'utilisateur une fois le fichier pret au telechargement | Test : export d'un rapport volumineux et verification de la notification |
| CA-08 | L'utilisateur peut exporter un rapport directement depuis l'historique sans avoir a le regenerer | Test : clic sur "Exporter" depuis l'historique, selection du format et verification du telechargement |

---

### US-R05 : Rapports planifies (recurrents)

**En tant que** dirigeant ou responsable administratif,
**je veux** pouvoir planifier la generation et l'envoi automatique de rapports a une frequence definie (hebdomadaire, mensuel) vers une liste de destinataires par email,
**afin de** recevoir automatiquement les rapports de suivi sans intervention manuelle et garantir un reporting regulier et fiable.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---|---|
| CA-01 | La page GESTION > Rapports > Rapports planifies affiche la liste de tous les rapports planifies avec colonnes : Nom, Type de rapport, Frequence, Prochaine execution, Derniere execution, Destinataires, Statut (Actif/Inactif) | Verification visuelle de la presence de toutes les colonnes |
| CA-02 | Un bouton "Nouveau rapport planifie" permet de creer un rapport planifie en selectionnant : un modele de rapport (type), des filtres, un format d'export (PDF, Excel, CSV), une frequence (quotidien, hebdomadaire, mensuel), un jour/heure d'execution, et une liste de destinataires (emails) | Test : creation complete d'un rapport planifie avec tous les champs |
| CA-03 | La frequence "Hebdomadaire" permet de choisir le jour de la semaine et l'heure d'envoi ; la frequence "Mensuel" permet de choisir le jour du mois (1-28 ou "Dernier jour") et l'heure | Test : configuration d'un rapport hebdomadaire le lundi a 8h et d'un rapport mensuel le 1er a 9h |
| CA-04 | Les destinataires peuvent etre ajoutes par adresse email (utilisateurs internes et externes) avec validation du format email et possibilite d'ajouter plusieurs destinataires | Test : ajout de 3 destinataires dont 1 externe et verification de la validation |
| CA-05 | Un rapport planifie peut etre active ou desactive via un toggle sans supprimer la configuration | Test : desactivation d'un rapport planifie et verification que la prochaine execution est suspendue |
| CA-06 | Le systeme genere automatiquement le rapport a la date/heure prevue et l'envoie par email aux destinataires avec le rapport en piece jointe au format configure | Test : planification d'un rapport a execution imminente et verification de la reception de l'email avec piece jointe |
| CA-07 | En cas d'echec d'envoi (erreur email, echec generation), le systeme enregistre l'erreur dans un journal et retente l'envoi une fois apres 15 minutes ; un indicateur visuel "Echec" apparait dans la liste des rapports planifies | Test : simulation d'un echec et verification du mecanisme de retry et de l'indicateur |
| CA-08 | L'utilisateur peut modifier ou supprimer un rapport planifie existant ; la suppression demande une confirmation | Test : modification de la frequence d'un rapport existant + suppression d'un autre avec confirmation |

---

### US-R06 : Rapport de temps par collaborateur/projet

**En tant que** chef de projet ou dirigeant,
**je veux** generer un rapport detaille des temps saisis par collaborateur et/ou par projet sur une periode donnee,
**afin de** analyser la repartition du temps de travail, identifier les surcharges ou sous-utilisations, et verifier la coherence entre le temps passe et le budget alloue.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---|---|
| CA-01 | Le rapport "Temps saisis" permet de filtrer par periode, par un ou plusieurs collaborateurs, par un ou plusieurs projets, et par phase de projet | Test : application de filtres combines (2 collaborateurs + 1 projet + phase "Conception") |
| CA-02 | Le rapport affiche un tableau avec les colonnes : Collaborateur, Projet, Phase, Date, Heures saisies, Heures facturables, Heures non facturables, Taux horaire, Montant valorise | Verification de la presence de toutes les colonnes |
| CA-03 | Le rapport propose un regroupement par collaborateur (avec sous-total d'heures par collaborateur) ou par projet (avec sous-total d'heures par projet), au choix de l'utilisateur | Test : basculement entre regroupement par collaborateur et par projet |
| CA-04 | Le rapport inclut un graphique a barres empilees montrant la repartition du temps par projet pour chaque collaborateur (ou par collaborateur pour chaque projet selon le regroupement choisi) | Verification visuelle du graphique avec les donnees correctes |
| CA-05 | Le rapport calcule et affiche le taux d'occupation de chaque collaborateur sur la periode : (heures saisies / heures ouvrables) x 100, avec code couleur (vert >= 80%, orange 60-79%, rouge < 60%) | Test : verification du calcul sur un collaborateur dont les heures sont connues |
| CA-06 | Les totaux generaux sont affiches en pied de tableau : total heures saisies, total heures facturables, total heures non facturables, montant total valorise | Verification des totaux et de leur coherence avec les donnees detaillees |
| CA-07 | Le rapport permet de comparer le temps reel saisi avec le temps budgete par projet/phase, en affichant l'ecart en heures et en pourcentage | Test : verification de l'ecart calcule sur un projet dont le budget temps est connu |
| CA-08 | Un lien cliquable sur chaque ligne permet d'acceder au detail des saisies de temps (drill-down vers le module Temps) | Test : clic sur une ligne et verification de la navigation vers le detail correspondant |

---

### US-R07 : Rapport financier (CA, Couts, Marge)

**En tant que** dirigeant ou associe,
**je veux** generer un rapport financier consolide presentant le chiffre d'affaires, les couts et la marge par projet et/ou par periode,
**afin de** piloter la rentabilite du cabinet, identifier les projets deficitaires et prendre des decisions strategiques eclairees.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---|---|
| CA-01 | Le rapport "Marge" affiche un tableau avec les colonnes : Projet, Client, Honoraires signes, Montant facture, Montant encaisse, Couts totaux (ventiles : sous-traitants, salaires, frais generaux), Marge brute (montant), Marge brute (%) | Verification de la presence et du bon calcul de toutes les colonnes |
| CA-02 | Le rapport permet de filtrer par periode (annee, trimestre, mois), par projet, par client, par statut de projet (en cours, termine, archive) | Test : application de filtres combines |
| CA-03 | Le rapport inclut un graphique a barres comparant pour chaque projet le chiffre d'affaires facture et les couts totaux, avec une ligne horizontale indiquant le seuil de rentabilite | Verification visuelle du graphique |
| CA-04 | Un graphique d'evolution (courbe) montre la marge mensuelle sur les 12 derniers mois avec ligne de tendance | Verification du graphique de tendance |
| CA-05 | Le rapport propose une vue "par annee" permettant de comparer les performances financieres sur plusieurs exercices (N, N-1, N-2) avec calcul des ecarts en valeur et en pourcentage | Test : generation du rapport en vue annuelle et verification des ecarts |
| CA-06 | Les couts sont ventiles par categorie (sous-traitants, salaires imputes, frais generaux) avec possibilite de voir le detail de chaque categorie | Test : clic sur une categorie de couts pour voir le detail |
| CA-07 | Le rapport affiche des indicateurs agreges en haut de page : CA total facture, Couts totaux, Marge brute globale (montant et %), Nombre de projets rentables vs deficitaires | Verification des indicateurs et de leur coherence |
| CA-08 | Les projets dont la marge est negative sont mis en evidence visuellement (ligne en rouge ou icone d'alerte) pour faciliter l'identification rapide des projets deficitaires | Test : verification du surlignage sur un projet dont la marge est connue comme negative |

---

### US-R08 : Rapport d'avancement des projets

**En tant que** chef de projet ou dirigeant,
**je veux** generer un rapport d'avancement global de l'ensemble des projets (ou d'une selection de projets) presentant l'etat d'avancement, les phases en cours et les ecarts par rapport au planning,
**afin de** suivre la progression globale du portefeuille de projets et identifier les projets en retard necessitant une attention particuliere.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---|---|
| CA-01 | Le rapport "Avancement des projets" affiche un tableau avec : Nom du projet, Client, Chef de projet, Phase en cours, Pourcentage d'avancement, Date de debut, Date de fin prevue, Ecart (en jours), Statut (En avance, Dans les temps, En retard) | Verification de la presence de toutes les colonnes |
| CA-02 | Le pourcentage d'avancement est calcule automatiquement sur la base de l'avancement des phases du projet (moyenne ponderee par le poids de chaque phase) | Test : verification du calcul sur un projet dont l'avancement par phase est connu |
| CA-03 | Le rapport permet de filtrer par chef de projet, par statut (en cours, termine, en pause), par client et par periode de date de fin prevue | Test : filtre par chef de projet + statut "en cours" |
| CA-04 | Un code couleur est applique au statut : vert (dans les temps ou en avance), orange (retard < 2 semaines), rouge (retard >= 2 semaines) | Verification visuelle des codes couleur sur des projets aux statuts differents |
| CA-05 | Le rapport inclut un diagramme de Gantt simplifie montrant les phases de chaque projet sur une timeline horizontale avec indication de la progression | Verification visuelle du diagramme de Gantt |
| CA-06 | Le rapport affiche des indicateurs synthetiques en haut de page : Nombre total de projets, Projets dans les temps, Projets en retard, Avancement moyen du portefeuille | Verification des indicateurs |
| CA-07 | Un clic sur le nom d'un projet dans le rapport ouvre la fiche projet correspondante (navigation vers EPIC-002) | Test : clic sur un nom de projet et verification de la navigation |
| CA-08 | Le rapport peut etre trie par ecart (retard decroissant en premier) pour prioriser les projets necessitant une intervention | Test : tri par ecart et verification de l'ordre |

---

### US-R09 : Rapport d'honoraires signes et facturables

**En tant que** dirigeant ou responsable administratif,
**je veux** generer un rapport detaille des honoraires signes et des budgets facturables par projet et par periode,
**afin de** suivre le volume d'affaires signe, anticiper les revenus facturables et piloter le plan de charge du cabinet.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---|---|
| CA-01 | Le rapport "Honoraires signes" affiche un tableau avec : Projet, Client, Date de signature, Montant des honoraires signes (HT), Montant deja facture, Reste a facturer, Pourcentage facture | Verification de toutes les colonnes et des calculs |
| CA-02 | Le rapport permet de filtrer par periode de signature, par client, par projet, par tranche de montant (ex : > 50 000 EUR) | Test : filtre par periode + client |
| CA-03 | Le rapport "Budgets facturables" affiche par projet et par phase : Budget total, Budget consomme (base sur les temps valorises), Budget restant, Pourcentage de consommation | Verification de la presence et du calcul correct des colonnes |
| CA-04 | Un graphique a barres montre la repartition des honoraires signes par mois/trimestre sur la periode selectionnee avec comparaison N vs N-1 | Verification du graphique avec donnees correctes |
| CA-05 | Le rapport affiche des indicateurs de synthese : Total des honoraires signes sur la periode, Montant total facturable restant, Pipe commercial (honoraires en cours de negociation si disponible) | Verification des indicateurs |
| CA-06 | Le rapport permet de regrouper par client pour voir le total des honoraires signes par client avec sous-totaux | Test : regroupement par client et verification des sous-totaux |
| CA-07 | Une alerte visuelle (icone ou couleur) signale les projets dont le budget est consomme a plus de 90% sans que la phase correspondante soit terminee | Test : verification de l'alerte sur un projet dont le budget est consomme a 95% |
| CA-08 | Le rapport permet l'export dans les 3 formats (PDF, Excel, CSV) en conservant la mise en forme, les graphiques (PDF) et les formules (Excel) | Test : export dans chaque format et verification du contenu |

---

### US-R10 : Rapports au niveau projet

**En tant que** chef de projet,
**je veux** acceder a des rapports specifiques au projet que je consulte via l'onglet PLUS > Rapports de la fiche projet,
**afin de** disposer d'une vue consolidee de toutes les dimensions du projet (temps, couts, honoraires, facturation, avancement, marge) sans quitter le contexte du projet.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---|---|
| CA-01 | L'onglet PLUS > Rapports de la fiche projet affiche une page dediee proposant les rapports disponibles pour ce projet specifique : Synthese projet, Temps passes, Budget et Honoraires, Facturation, Couts, Marge | Verification de la presence de tous les types de rapports projet |
| CA-02 | Le rapport "Synthese projet" affiche un tableau de bord consolide du projet avec les indicateurs cles : avancement (%), honoraires signes, montant facture, reste a facturer, total heures passees, budget heures restant, couts totaux, marge brute (montant et %) | Verification de tous les indicateurs |
| CA-03 | Les rapports projet sont automatiquement filtres sur le projet en cours (le filtre projet est pre-selectionne et non modifiable depuis cette vue) | Test : ouverture d'un rapport projet et verification que le filtre est verrouille sur le projet courant |
| CA-04 | Le rapport "Synthese projet" inclut un graphique d'evolution mensuelle montrant les heures passees vs heures budgetees et les couts cumules vs honoraires cumules | Verification du graphique |
| CA-05 | Chaque rapport au niveau projet peut etre exporte aux formats PDF, Excel et CSV avec l'en-tete specifique au projet (nom du projet, reference, client, chef de projet) | Test : export PDF d'un rapport projet et verification de l'en-tete |
| CA-06 | Un bouton "Envoyer par email" permet d'envoyer directement le rapport projet a un ou plusieurs destinataires sans passer par la planification | Test : envoi d'un rapport projet par email et verification de la reception |
| CA-07 | Le rapport projet affiche l'historique des rapports precedemment generes pour ce projet, avec possibilite de les retelecharger | Verification de la presence de l'historique et du telechargement |
| CA-08 | Les donnees du rapport projet sont coherentes avec les donnees affichees dans les autres onglets du projet (Honoraires, Temps, Facturation) a la meme date | Test : comparaison croisee des montants entre le rapport et les onglets du projet |

---

## 6. Hors Perimetre

Les elements suivants sont explicitement exclus du perimetre de cet EPIC :

| # | Element exclu | Justification |
|---|---|---|
| HP-01 | **Tableaux de bord (dashboards) en temps reel** | Les dashboards interactifs avec rafraichissement en temps reel relevent d'un EPIC dedie (Dashboard). Le module Rapports produit des documents a un instant T. |
| HP-02 | **Rapports de type Business Intelligence (BI) avances** | Les analyses multidimensionnelles (OLAP, cubes de donnees) et les rapports ad hoc avec langage de requete ne sont pas dans le perimetre. Seuls les rapports predefinis et personnalisables par filtres sont couverts. |
| HP-03 | **Constructeur de rapports personnalises (Report Builder)** | La creation de rapports entierement sur mesure par l'utilisateur (drag & drop de champs, creation de formules) est exclue. Les rapports sont bases sur des modeles predefinis. |
| HP-04 | **Rapports de paie et declarations sociales** | Les rapports lies a la gestion de la paie (fiches de paie, declarations URSSAF, DSN) sont hors perimetre et relevent d'un logiciel de paie dedie. |
| HP-05 | **Rapports de conformite reglementaire** | Les rapports specifiques aux obligations reglementaires (BIM, RE2020, accessibilite) sont hors perimetre. |
| HP-06 | **Integration avec des outils de BI externes** | Les connecteurs vers Power BI, Tableau, Looker ou d'autres outils de BI sont hors perimetre V1. |
| HP-07 | **Rapports multi-agences** | La consolidation de rapports entre plusieurs agences ou entites juridiques distinctes est exclue en V1. |
| HP-08 | **Rapports avec saisie de donnees** | Les rapports sont en lecture seule. La saisie ou modification de donnees depuis un rapport n'est pas prevue. |

---

## 7. Regles Metier

### 7.1 Regles de gestion des rapports

| # | Regle | Description |
|---|---|---|
| RM-01 | **Perimetre de donnees** | Un rapport ne peut afficher que les donnees auxquelles l'utilisateur a acces selon ses permissions (projets assignes, equipe geree). Un chef de projet ne voit que les donnees de ses projets ; un dirigeant voit l'ensemble des donnees. |
| RM-02 | **Fraicheur des donnees** | Les donnees d'un rapport sont extraites au moment de la generation. La date et l'heure de generation sont systematiquement affichees. Un rapport genere n'est pas mis a jour retroactivement. |
| RM-03 | **Coherence des periodes** | La date de fin de periode doit etre superieure ou egale a la date de debut. La periode maximale autorisee est de 5 ans. La periode par defaut est le mois en cours. |
| RM-04 | **Calcul de la marge** | Marge brute = Montant facture - Couts totaux. Marge brute (%) = (Marge brute / Montant facture) x 100. Si le montant facture est 0, la marge n'est pas calculable et affiche "N/A". |
| RM-05 | **Calcul du taux d'occupation** | Taux d'occupation = (Heures saisies / Heures ouvrables sur la periode) x 100. Les heures ouvrables sont basees sur le calendrier de travail du collaborateur (par defaut : 7h/jour, 5 jours/semaine, hors jours feries). |
| RM-06 | **Devise et formatage** | Tous les montants sont affiches dans la devise par defaut du cabinet (EUR). Les montants sont formates avec separateur de milliers (espace) et 2 decimales. Les pourcentages sont affiches avec 1 decimale. |
| RM-07 | **Retention des rapports** | Les rapports generes sont conserves dans l'historique pendant 24 mois. Au-dela, les fichiers sont archives et ne sont plus directement telechargeables (mais les metadonnees restent visibles). |
| RM-08 | **Planification et fuseau horaire** | Les horaires de planification des rapports sont definis dans le fuseau horaire du cabinet (configure dans les parametres). L'execution est declenchee a l'heure configuree +/- 5 minutes. |
| RM-09 | **Limite de destinataires** | Un rapport planifie peut avoir au maximum 20 destinataires. Les adresses email doivent etre valides (format RFC 5322). |
| RM-10 | **Limite de volume** | Un rapport est limite a 50 000 lignes. Au-dela, l'utilisateur doit affiner ses filtres ou le rapport est tronque avec un avertissement. Les rapports depassant 10 000 lignes sont generes en traitement asynchrone. |
| RM-11 | **Unicite du nom de rapport planifie** | Le nom d'un rapport planifie doit etre unique au sein du cabinet pour eviter les confusions. |
| RM-12 | **Arrondi des montants** | Les montants financiers sont arrondis au centime (2 decimales). Les arrondis sont effectues selon la methode "half-up" (arrondi au superieur si la decimale suivante est >= 5). |

### 7.2 Regles de permissions

| Role | Rapports accessibles | Actions autorisees |
|---|---|---|
| **Collaborateur** | Temps saisis (ses propres temps), Avancement (ses projets) | Generer, Exporter |
| **Chef de projet** | Tous les rapports pour ses projets : Temps, Avancement, Honoraires, Facturation, Couts, Marge | Generer, Exporter, Rapports projet |
| **Responsable administratif** | Tous les rapports pour l'ensemble des projets | Generer, Exporter, Planifier, Rapports projet |
| **Dirigeant / Associe** | Tous les rapports sans restriction | Generer, Exporter, Planifier, Rapports projet, Gerer les rapports planifies |

---

## 8. Criteres Globaux

### 8.1 Criteres de performance

| # | Critere | Seuil |
|---|---|---|
| PERF-01 | Temps de chargement de la bibliotheque de rapports | < 2 secondes |
| PERF-02 | Temps de generation d'un rapport standard (< 10 000 lignes) | < 10 secondes |
| PERF-03 | Temps de generation d'un rapport volumineux (10 000 - 50 000 lignes) | < 60 secondes (traitement asynchrone) |
| PERF-04 | Temps de generation d'un export PDF | < 15 secondes pour un rapport standard |
| PERF-05 | Temps de generation d'un export Excel/CSV | < 10 secondes pour un rapport standard |
| PERF-06 | Taille maximale d'un fichier export PDF | 20 Mo |
| PERF-07 | Taille maximale d'un fichier export Excel/CSV | 50 Mo |

### 8.2 Criteres d'accessibilite et d'ergonomie

| # | Critere | Description |
|---|---|---|
| UX-01 | Les rapports sont lisibles sur ecran desktop (resolution minimale 1280x720) | Mise en page responsive pour les ecrans larges |
| UX-02 | Les graphiques utilisent des couleurs distinctes et accessibles (contraste WCAG AA) | Palette de couleurs testee pour le daltonisme |
| UX-03 | Les tableaux de rapports supportent le defilement horizontal pour les rapports a nombreuses colonnes | Scroll horizontal fluide avec en-tetes de colonnes fixes |
| UX-04 | Les filtres sont regroupes dans un panneau retractable pour maximiser l'espace d'affichage du rapport | Panneau de filtres retractable |
| UX-05 | Les rapports affiches a l'ecran supportent la pagination (50 lignes par page par defaut, configurable : 25, 50, 100, 200) | Pagination fonctionnelle avec navigation |

### 8.3 Criteres de fiabilite

| # | Critere | Description |
|---|---|---|
| FIAB-01 | Les totaux affiches dans les rapports sont verifiables par recalcul a partir des donnees detaillees | Coherence des totaux garantie |
| FIAB-02 | Les rapports planifies sont executes avec un taux de reussite >= 99% sur un mois glissant | Monitoring des executions |
| FIAB-03 | Les donnees des rapports sont coherentes avec les donnees affichees dans les modules sources (a la meme date/heure) | Tests de coherence croisee |
| FIAB-04 | Les exports reproduisent fidelement les donnees affichees a l'ecran (aucune perte de donnees ni transformation involontaire) | Verification systematique des exports |

---

## 9. Definition of Done (DoD)

Un item du backlog est considere comme "Done" lorsque l'ensemble des criteres suivants sont satisfaits :

### 9.1 Developpement

- [ ] Le code est developpe conformement aux criteres d'acceptation de la User Story
- [ ] Le code respecte les conventions de codage et les standards de l'equipe
- [ ] Le code est factorise et ne contient pas de duplication inutile
- [ ] Les requetes de generation de rapports sont optimisees (index, pagination, mise en cache le cas echeant)
- [ ] Les traitements asynchrones (rapports volumineux, envois email) sont implementes avec file d'attente (job queue)
- [ ] Le code gere les cas d'erreur (donnees manquantes, timeout, echec email) avec messages explicites

### 9.2 Tests

- [ ] Les tests unitaires couvrent au minimum 80% du code des services de generation de rapports
- [ ] Les tests d'integration verifient la coherence des donnees entre les modules sources et les rapports generes
- [ ] Les tests de performance valident les seuils definis dans les criteres globaux (PERF-01 a PERF-07)
- [ ] Les tests fonctionnels couvrent les criteres d'acceptation de chaque User Story
- [ ] Les exports (PDF, Excel, CSV) sont testes avec des jeux de donnees representatifs (cas nominaux, cas limites, donnees volumineuses)
- [ ] Les rapports planifies sont testes avec simulation d'horloge pour valider la frequence d'execution

### 9.3 Qualite

- [ ] Le code a ete revu par au moins un pair (code review)
- [ ] Aucune anomalie bloquante ou majeure n'est ouverte
- [ ] Les anomalies mineures identifiees sont documentees dans le backlog
- [ ] Les metriques de qualite (SonarQube ou equivalent) sont conformes aux seuils definis

### 9.4 Documentation

- [ ] La documentation technique est mise a jour (API, schemas de donnees, architecture des traitements asynchrones)
- [ ] La documentation utilisateur est mise a jour (guide d'utilisation des rapports, FAQ)
- [ ] Les modeles de rapports predefinis sont documentes (description, champs, filtres, calculs)

### 9.5 Deploiement

- [ ] La fonctionnalite est deployee sur l'environnement de staging et validee
- [ ] Les migrations de base de donnees sont testees et reversibles
- [ ] Les jobs planifies (cron) sont configures et testes sur l'environnement cible
- [ ] La fonctionnalite est deployable independamment des autres EPICs (pas de couplage fort au deploiement)

---

## 10. Dependances

### 10.1 Dependances entrantes (ce dont le module Rapports a besoin)

| Dependance | EPIC source | Description | Impact |
|---|---|---|---|
| Donnees projets | EPIC-002 Projets | Informations sur les projets (nom, client, phases, dates, avancement, chef de projet) | **Bloquant** : sans les donnees projets, aucun rapport ne peut etre genere |
| Donnees honoraires | EPIC-003 Honoraires | Montants des honoraires signes, budgets facturables, phases facturables | **Bloquant** : necessaire pour les rapports Honoraires, Budgets, Marge |
| Donnees facturation | EPIC-004 Facturation | Factures emises, montants, statuts (payee, impayee, en retard) | **Bloquant** : necessaire pour les rapports Facturation et Marge |
| Donnees temps | EPIC-005 Temps | Saisies de temps par collaborateur, par projet, par phase | **Bloquant** : necessaire pour les rapports Temps et Taux d'occupation |
| Donnees couts | EPIC-007 Couts | Couts par categorie (sous-traitants, salaires, frais) par projet | **Bloquant** : necessaire pour les rapports Couts et Marge |
| Donnees finances | EPIC-008 Finances | Chiffre d'affaires, encaissements, tresorerie | **Non bloquant** : enrichit les rapports financiers mais les rapports de base fonctionnent sans |

### 10.2 Dependances sortantes (ce que le module Rapports fournit)

| Dependance | EPIC cible | Description |
|---|---|---|
| Rapports projet | EPIC-002 Projets | Les rapports projet sont affiches dans l'onglet PLUS > Rapports de la fiche projet |

### 10.3 Dependances techniques

| Dependance | Description | Impact |
|---|---|---|
| Service d'email (SMTP) | Necessaire pour l'envoi des rapports planifies par email | **Bloquant** pour US-R05 (Rapports planifies) |
| Librairie de generation PDF | Librairie de generation de documents PDF avec support des graphiques (ex : WeasyPrint, ReportLab, Puppeteer) | **Bloquant** pour US-R04 (Export PDF) |
| Librairie de generation Excel | Librairie de generation de fichiers .xlsx (ex : openpyxl, xlsxwriter) | **Bloquant** pour US-R04 (Export Excel) |
| Librairie de graphiques | Librairie de rendu de graphiques cote serveur ou cote client (ex : Chart.js, D3.js, Matplotlib) | **Bloquant** pour les visualisations dans les rapports |
| Systeme de jobs planifies | Scheduler pour l'execution automatique des rapports planifies (ex : Celery, cron, Bull) | **Bloquant** pour US-R05 (Rapports planifies) |
| Stockage fichiers | Stockage des fichiers de rapports generes (S3, stockage local, etc.) | **Bloquant** pour l'historique des rapports |

---

## 11. Modele de Donnees

### 11.1 Diagramme des entites

```
+--------------------+       +------------------------+       +---------------------+
|   ReportTemplate   |       |    ScheduledReport     |       |       Report        |
+--------------------+       +------------------------+       +---------------------+
| id (PK)            |<------| report_template_id (FK)|       | id (PK)             |
| name               |       | id (PK)                |       | name                |
| type               |       | name                   |       | type                |
| description        |       | frequency              |       | report_template_id  |
| default_filters    |       | day_of_week            |  +--->| filters             |
| columns[]          |       | day_of_month           |  |    | format              |
| grouping           |       | execution_time         |  |    | generated_at        |
| sorting            |       | recipients[]           |  |    | file_url            |
| category           |       | export_format          |  |    | file_size           |
| permissions[]      |       | filters                |  |    | row_count           |
| is_active          |       | next_run_at            |  |    | created_by (FK)     |
| created_at         |       | last_run_at            |  |    | scheduled_report_id |
| updated_at         |       | last_status            |  |    | project_id (FK)     |
+--------------------+       | active                 |  |    | organization_id(FK) |
                              | created_by (FK)        |  |    | status              |
                              | organization_id (FK)   |  |    | error_message       |
                              | created_at             |  |    | created_at          |
                              | updated_at             |  |    | updated_at          |
                              +------------------------+  |    +---------------------+
                                                          |
                              +------------------------+  |
                              | SavedReportConfig      |--+
                              +------------------------+
                              | id (PK)                |
                              | name                   |
                              | report_template_id(FK) |
                              | user_id (FK)           |
                              | filters                |
                              | columns[]              |
                              | grouping               |
                              | sorting                |
                              | created_at             |
                              | updated_at             |
                              +------------------------+
```

### 11.2 Description des entites

#### ReportTemplate (Modele de rapport)

Definit les modeles de rapports predefinis disponibles dans la bibliotheque.

| Champ | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK, auto-genere | Identifiant unique du modele |
| `name` | VARCHAR(200) | NOT NULL | Nom du modele de rapport (ex : "Honoraires signes par projet") |
| `type` | ENUM | NOT NULL | Type de rapport : `HONORAIRES`, `BUDGET`, `TEMPS`, `FACTURATION`, `COUTS`, `MARGE`, `AVANCEMENT`, `OCCUPATION` |
| `description` | TEXT | NULL | Description detaillee du contenu et de l'utilite du rapport |
| `default_filters` | JSONB | NOT NULL, default `{}` | Filtres par defaut sous forme JSON (ex : `{"period": "current_month", "status": "active"}`) |
| `columns` | JSONB | NOT NULL | Liste ordonnee des colonnes disponibles avec nom, cle, type de donnee et visibilite par defaut |
| `grouping` | JSONB | NULL | Regroupement par defaut (ex : `{"level1": "project", "level2": null}`) |
| `sorting` | JSONB | NULL | Tri par defaut (ex : `{"column": "amount", "order": "desc"}`) |
| `category` | VARCHAR(50) | NOT NULL | Categorie pour le classement dans la bibliotheque |
| `permissions` | JSONB | NOT NULL | Roles autorises a acceder a ce modele (ex : `["dirigeant", "chef_projet", "admin"]`) |
| `is_active` | BOOLEAN | NOT NULL, default `true` | Indique si le modele est actif et visible dans la bibliotheque |
| `created_at` | TIMESTAMP | NOT NULL, auto | Date de creation |
| `updated_at` | TIMESTAMP | NOT NULL, auto | Date de derniere mise a jour |

#### Report (Rapport genere)

Represente un rapport effectivement genere, avec ses parametres et son fichier resultat.

| Champ | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK, auto-genere | Identifiant unique du rapport genere |
| `name` | VARCHAR(300) | NOT NULL | Nom du rapport genere (auto-genere : `[Type]_[Periode]_[Date]`) |
| `type` | ENUM | NOT NULL | Type de rapport (repris du modele) |
| `report_template_id` | UUID | FK -> ReportTemplate.id, NULL | Reference vers le modele utilise (NULL si rapport ad hoc) |
| `filters` | JSONB | NOT NULL | Filtres effectivement appliques lors de la generation |
| `format` | ENUM | NOT NULL | Format du fichier genere : `SCREEN`, `PDF`, `EXCEL`, `CSV` |
| `generated_at` | TIMESTAMP | NOT NULL | Date et heure exactes de la generation |
| `file_url` | VARCHAR(500) | NULL | URL du fichier genere (NULL si affichage ecran uniquement) |
| `file_size` | INTEGER | NULL | Taille du fichier en octets |
| `row_count` | INTEGER | NOT NULL, default 0 | Nombre de lignes dans le rapport |
| `created_by` | UUID | FK -> User.id, NOT NULL | Utilisateur ayant declenche la generation |
| `scheduled_report_id` | UUID | FK -> ScheduledReport.id, NULL | Reference vers le rapport planifie (NULL si rapport a la demande) |
| `project_id` | UUID | FK -> Project.id, NULL | Projet concerne (pour les rapports au niveau projet, NULL pour les rapports globaux) |
| `organization_id` | UUID | FK -> Organization.id, NOT NULL | Cabinet/organisation proprietaire |
| `status` | ENUM | NOT NULL | Statut : `PENDING`, `GENERATING`, `COMPLETED`, `FAILED` |
| `error_message` | TEXT | NULL | Message d'erreur en cas d'echec de generation |
| `created_at` | TIMESTAMP | NOT NULL, auto | Date de creation de l'enregistrement |
| `updated_at` | TIMESTAMP | NOT NULL, auto | Date de derniere mise a jour |

#### ScheduledReport (Rapport planifie)

Definit un rapport a execution automatique et recurrente.

| Champ | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK, auto-genere | Identifiant unique du rapport planifie |
| `name` | VARCHAR(200) | NOT NULL, UNIQUE per org | Nom du rapport planifie (unique par organisation) |
| `report_template_id` | UUID | FK -> ReportTemplate.id, NOT NULL | Modele de rapport a generer |
| `frequency` | ENUM | NOT NULL | Frequence : `DAILY`, `WEEKLY`, `MONTHLY` |
| `day_of_week` | INTEGER | NULL, 1-7 | Jour de la semaine pour la frequence hebdomadaire (1=lundi, 7=dimanche) |
| `day_of_month` | INTEGER | NULL, 1-28 ou -1 | Jour du mois pour la frequence mensuelle (-1 = dernier jour) |
| `execution_time` | TIME | NOT NULL | Heure d'execution (dans le fuseau horaire du cabinet) |
| `recipients` | JSONB | NOT NULL | Liste des adresses email des destinataires (max 20) |
| `export_format` | ENUM | NOT NULL | Format du fichier envoye : `PDF`, `EXCEL`, `CSV` |
| `filters` | JSONB | NOT NULL | Filtres a appliquer (la periode est relative : "mois precedent", "semaine precedente") |
| `next_run_at` | TIMESTAMP | NOT NULL | Date et heure de la prochaine execution prevue |
| `last_run_at` | TIMESTAMP | NULL | Date et heure de la derniere execution effectuee |
| `last_status` | ENUM | NULL | Statut de la derniere execution : `SUCCESS`, `FAILED`, `PARTIAL` |
| `active` | BOOLEAN | NOT NULL, default `true` | Indique si le rapport planifie est actif |
| `created_by` | UUID | FK -> User.id, NOT NULL | Utilisateur ayant cree le rapport planifie |
| `organization_id` | UUID | FK -> Organization.id, NOT NULL | Cabinet/organisation proprietaire |
| `created_at` | TIMESTAMP | NOT NULL, auto | Date de creation |
| `updated_at` | TIMESTAMP | NOT NULL, auto | Date de derniere mise a jour |

#### SavedReportConfig (Configuration de rapport sauvegardee)

Permet aux utilisateurs de sauvegarder leurs configurations de filtres et d'affichage preferees.

| Champ | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK, auto-genere | Identifiant unique |
| `name` | VARCHAR(200) | NOT NULL | Nom de la configuration sauvegardee |
| `report_template_id` | UUID | FK -> ReportTemplate.id, NOT NULL | Modele de rapport associe |
| `user_id` | UUID | FK -> User.id, NOT NULL | Utilisateur proprietaire de la configuration |
| `filters` | JSONB | NOT NULL | Filtres sauvegardes |
| `columns` | JSONB | NOT NULL | Colonnes visibles et leur ordre |
| `grouping` | JSONB | NULL | Regroupement sauvegarde |
| `sorting` | JSONB | NULL | Tri sauvegarde |
| `created_at` | TIMESTAMP | NOT NULL, auto | Date de creation |
| `updated_at` | TIMESTAMP | NOT NULL, auto | Date de derniere mise a jour |

### 11.3 Index recommandes

| Table | Index | Colonnes | Justification |
|---|---|---|---|
| Report | `idx_report_org_type` | `organization_id`, `type` | Recherche de rapports par organisation et type |
| Report | `idx_report_created_by` | `created_by`, `generated_at DESC` | Historique des rapports d'un utilisateur |
| Report | `idx_report_project` | `project_id`, `generated_at DESC` | Rapports au niveau projet |
| Report | `idx_report_generated_at` | `generated_at` | Tri chronologique et purge |
| Report | `idx_report_scheduled` | `scheduled_report_id` | Lien avec les rapports planifies |
| ScheduledReport | `idx_scheduled_next_run` | `next_run_at`, `active` | Selection des rapports a executer par le scheduler |
| ScheduledReport | `idx_scheduled_org` | `organization_id`, `active` | Liste des rapports planifies d'une organisation |
| SavedReportConfig | `idx_config_user_template` | `user_id`, `report_template_id` | Configurations d'un utilisateur pour un modele |

---

## 12. Estimation

### 12.1 Synthese de l'estimation

| Parametre | Valeur |
|---|---|
| **Duree totale estimee** | 5 semaines (25 jours ouvrables) |
| **Nombre de sprints** | 3 sprints de 2 semaines (le 3e sprint inclut stabilisation et tests) |
| **Equipe recommandee** | 2 developpeurs back-end, 1 developpeur front-end, 1 QA, 1 UX/UI (partiel) |
| **Effort total estime** | 85 - 110 points de story (en story points, base 1 SP = 1 jour/homme ideal) |

### 12.2 Estimation par User Story

| User Story | Complexite | Story Points | Sprint |
|---|---|---|---|
| US-R01 : Bibliotheque des rapports | Moyenne | 8 | Sprint 1 |
| US-R02 : Generation a la demande | Elevee | 13 | Sprint 1 |
| US-R03 : Filtrage et personnalisation | Elevee | 13 | Sprint 1 |
| US-R04 : Export PDF, Excel, CSV | Elevee | 13 | Sprint 2 |
| US-R05 : Rapports planifies | Tres elevee | 21 | Sprint 2 |
| US-R06 : Rapport temps | Moyenne | 8 | Sprint 1 |
| US-R07 : Rapport financier (CA, Couts, Marge) | Elevee | 13 | Sprint 2 |
| US-R08 : Rapport avancement | Moyenne | 8 | Sprint 2 |
| US-R09 : Rapport honoraires et facturables | Moyenne | 8 | Sprint 3 |
| US-R10 : Rapports au niveau projet | Moyenne | 8 | Sprint 3 |
| **Total** | | **113 SP** | |

### 12.3 Repartition par sprint

#### Sprint 1 (Semaines 1-2) : Fondations et rapports de base

| Tache | Contenu | Points |
|---|---|---|
| Infrastructure | Mise en place du modele de donnees (ReportTemplate, Report, SavedReportConfig), API de generation, service de requetage | 8 |
| US-R01 | Bibliotheque de rapports : interface, recherche, filtrage par categorie, section "recents" | 8 |
| US-R02 | Generation de rapports a la demande : moteur de generation, affichage ecran, gestion des erreurs | 13 |
| US-R03 | Filtres et personnalisation : panneau de filtres, selection de colonnes, regroupements, tri, sauvegarde de configurations | 13 |
| US-R06 | Rapport de temps : implementation du type de rapport "Temps saisis" avec ses specificites (taux d'occupation, comparaison budgete/reel) | 8 |
| **Total Sprint 1** | | **50 SP** |

**Objectif Sprint 1** : Un utilisateur peut acceder a la bibliotheque de rapports, generer un rapport de temps a la demande avec des filtres personnalises, et visualiser le resultat a l'ecran.

#### Sprint 2 (Semaines 3-4) : Exports, planification et rapports financiers

| Tache | Contenu | Points |
|---|---|---|
| US-R04 | Exports multi-formats : generation PDF (avec graphiques, mise en page), Excel (avec formules), CSV (encodage UTF-8), nommage des fichiers, export asynchrone pour gros volumes | 13 |
| US-R05 | Rapports planifies : modele ScheduledReport, scheduler (job queue), envoi email avec piece jointe, mecanisme de retry, interface de gestion (CRUD, activation/desactivation) | 21 |
| US-R07 | Rapport financier : marge par projet, ventilation des couts, graphiques de comparaison CA/couts, vue multi-exercice, indicateurs agreges | 13 |
| US-R08 | Rapport avancement : avancement par phase, code couleur, diagramme de Gantt simplifie, indicateurs synthetiques | 8 |
| **Total Sprint 2** | | **55 SP** |

**Objectif Sprint 2** : Les rapports peuvent etre exportes en PDF/Excel/CSV, les rapports planifies fonctionnent de bout en bout (creation, execution automatique, envoi email), et les rapports financiers et d'avancement sont operationnels.

#### Sprint 3 (Semaine 5) : Rapports complementaires, integration projet et stabilisation

| Tache | Contenu | Points |
|---|---|---|
| US-R09 | Rapport honoraires et facturables : implementation, graphiques, alertes sur budgets consommes | 8 |
| US-R10 | Rapports au niveau projet : integration dans la fiche projet (onglet PLUS > Rapports), rapport de synthese projet, envoi par email | 8 |
| Stabilisation | Tests de non-regression, correction d'anomalies, tests de performance, tests d'integration avec les modules sources | - |
| Documentation | Documentation technique, guide utilisateur, documentation des modeles de rapports | - |
| **Total Sprint 3** | | **16 SP** |

**Objectif Sprint 3** : Tous les types de rapports sont implementes, les rapports projet sont integres, et la qualite globale est validee.

### 12.4 Risques et mitigations

| # | Risque | Probabilite | Impact | Mitigation |
|---|---|---|---|---|
| R1 | Les modules sources (EPIC-002 a EPIC-008) ne sont pas encore developpes ou leurs API ne sont pas stabilisees | Elevee | Bloquant | Utiliser des interfaces (contrats d'API) et des donnees mockees pendant le developpement. Prevoir un sprint de buffer pour l'integration reelle. |
| R2 | La generation de rapports volumineux depasse les seuils de performance | Moyenne | Majeur | Implementer la generation asynchrone des le debut, optimiser les requetes SQL, prevoir un mecanisme de mise en cache pour les rapports frequents. |
| R3 | La generation de PDF avec graphiques est complexe et chronophage | Moyenne | Majeur | Evaluer et selectionner la librairie PDF des la phase de conception technique. Prevoir un spike technique de 2 jours en debut de Sprint 2. |
| R4 | Le mecanisme de rapports planifies (scheduler) introduit des problemes de fiabilite (jobs perdus, doublons) | Moyenne | Majeur | Utiliser un systeme de job queue eprouve (Celery, Bull) avec garantie d'execution at-least-once et idempotence. |
| R5 | Les regles de permissions complexifient significativement le developpement | Faible | Moyen | S'appuyer sur le systeme de permissions existant de l'application. Definir les regles de permission de maniere declarative dans les modeles de rapport. |

### 12.5 Hypotheses de planification

- L'equipe est disponible a 80% (20% pour les ceremonies Scrum, support, etc.).
- Les API des modules sources (EPIC-002 a EPIC-008) sont au minimum documentees (contrats d'API), meme si elles ne sont pas encore implementees.
- Le service d'email (SMTP) est disponible et configure dans l'environnement de developpement.
- Le design UX/UI des ecrans de rapports est realise en amont du Sprint 1 ou en parallele.
- L'infrastructure de stockage de fichiers (pour les rapports generes) est disponible.

---

*Document redige le 26/02/2026 -- Version 1.0*
*EPIC-011 -- Module Rapports -- Application OOTI*
