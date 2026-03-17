# EPIC -- Audit ChangePoint : Module Feuilles de Temps (Time Sheet)

**Application concurrente auditee : Planview ChangePoint**
**URL : https://provencherroy.changepointasp.com/**
**Version du document : 1.0 -- Fevrier 2026**

---

## 1. Identification

| Champ | Valeur |
|---|---|
| **Nom de l'EPIC** | Feuilles de Temps (Time Sheet) -- Audit ChangePoint |
| **Reference** | EPIC-CP-TEMPS |
| **Module audite** | Time Sheet + Expenses (ChangePoint) |
| **Priorite** | Critique |
| **Auteur** | Architecte logiciel senior |
| **Date de creation** | 27 fevrier 2026 |
| **Version du document** | 1.0 |
| **Statut** | Brouillon |
| **Application cible** | Planview ChangePoint (instance Provencher Roy) |
| **Entites concernees** | Provencher_Roy Prod, PRAA |
| **Devise** | CAD |
| **EPICs OOTI lies** | EPIC-005 (Temps), EPIC-013 (Notes de frais), EPIC-002 (Projets), EPIC-012 (Validation) |

---

## 2. Contexte et Justification

### 2.1 Contexte de l'audit

Le cabinet Provencher Roy utilise actuellement **Planview ChangePoint** comme outil de gestion du temps et des depenses. Le module Time Sheet de ChangePoint constitue le coeur operationnel de la saisie des heures pour l'ensemble des collaborateurs du cabinet. L'audit de ce module vise a identifier exhaustivement les fonctionnalites existantes, les flux utilisateur, les regles metier et les contraintes techniques afin de concevoir un module equivalent ou superieur dans l'application OOTI.

Le cabinet Provencher Roy opere avec **plusieurs entites** (Provencher_Roy Prod, PRAA) ce qui implique une gestion multi-entites des projets, des assignments et des temps. Les projets sont structures avec des prefixes d'entite (ex : "PRAA - Comptabilite", "PRAA - Technologie information", "PRAA - Administration generale"), et chaque collaborateur peut saisir du temps sur des projets appartenant a differentes entites.

### 2.2 Problematique identifiee

L'interface actuelle de ChangePoint presente plusieurs limites fonctionnelles et ergonomiques que l'application OOTI devra depasser :

- **Navigation hebdomadaire rigide** : la semaine debute le dimanche (convention nord-americaine), sans possibilite de configurer le jour de debut de semaine (lundi pour les conventions europeennes/quebecoises)
- **Grille de saisie dense** : la grille principale melange taches projet et temps non-projet dans une meme vue, sans separation visuelle claire
- **Assignments non-projet fixes** : les categories de temps non-projet (Formation, Vacances, Maladie, Ferie, etc.) sont predefinies et peu flexibles
- **Systeme de pin limité** : l'epinglage de taches permet de les garder en haut de la grille, mais sans possibilite de groupement ou de personnalisation avancee
- **Module Expenses couple** : les notes de frais sont accessibles depuis le meme contexte que les feuilles de temps, mais avec un formulaire separe comprenant de nombreux champs obligatoires
- **Statuts de tache peu lisibles** : les statuts sont representes par de petites icones (effort, pourcentage, date de fin) difficilement lisibles
- **Absence de tableau de bord temps** : pas de vue synthetique des heures saisies, des tendances ou des alertes de depassement

### 2.3 Justification strategique

L'application OOTI doit proposer un module Feuilles de Temps qui :

1. **Reproduit fidelement** toutes les fonctionnalites essentielles de ChangePoint pour assurer une migration sans perte fonctionnelle
2. **Ameliore l'ergonomie** de la saisie hebdomadaire avec une interface moderne et reactive
3. **Integre nativement** les notes de frais dans le meme flux utilisateur
4. **Offre une flexibilite superieure** en termes de configuration (jour de debut de semaine, categories de temps non-projet personnalisables, multi-devises)
5. **Ajoute des fonctionnalites manquantes** : tableau de bord temps, statistiques de saisie, alertes proactives, workflow d'approbation configurable

---

## 3. Objectif de l'EPIC

Concevoir et specifier le module **Feuilles de Temps** de l'application OOTI en s'appuyant sur l'audit exhaustif du module Time Sheet de Planview ChangePoint. L'objectif est de garantir une **parite fonctionnelle complete** avec ChangePoint tout en apportant des ameliorations significatives en termes d'ergonomie, de flexibilite et de fonctionnalites complementaires.

Les objectifs specifiques sont :

- **Saisie hebdomadaire** : permettre a chaque collaborateur de saisir ses heures sur une grille hebdomadaire editable, avec distinction entre temps projet et temps non-projet
- **Gestion des assignments** : reproduire le systeme d'assignments de ChangePoint (taches projet et categories de temps non-projet) avec une flexibilite accrue
- **Navigation temporelle** : offrir une navigation semaine par semaine avec la possibilite de configurer le jour de debut de semaine
- **Workflow de soumission et approbation** : implementer un flux Submit / Approve / Reject conforme aux pratiques de ChangePoint
- **Notes de frais integrees** : coupler la saisie des depenses a la feuille de temps avec un formulaire complet (projet, categorie, type, montant, devise, taux de change)
- **Rapports de depenses** : permettre la creation, la consultation et l'export de rapports de depenses
- **Copie de temps** : reproduire les fonctionnalites de copie de temps (Copy time, Copy selected time)
- **Statistiques et tableau de bord** : ajouter une vue synthetique absente de ChangePoint

---

## 4. Perimetre Fonctionnel

| Ref | Fonctionnalite | Source ChangePoint | Statut OOTI | Priorite |
|---|---|---|---|---|
| PF-01 | Grille de saisie hebdomadaire (7 jours + total) | Time sheet grid | A reproduire | Critique |
| PF-02 | Saisie horaire par cellule (heures decimales) | Editable cells (5.00, 2.75, etc.) | A reproduire | Critique |
| PF-03 | Ligne de total par colonne et par ligne | Total row + Total column | A reproduire | Critique |
| PF-04 | Assignments non-projet (9 categories) | Sidebar Assignments | A reproduire et etendre | Haute |
| PF-05 | Pin / epingle de taches (priorite visuelle) | Pin icon (blue pin) | A reproduire | Haute |
| PF-06 | Navigation hebdomadaire (semaine precedente/suivante) | Week navigation arrows | A reproduire | Critique |
| PF-07 | Bouton Submit (soumission de la feuille de temps) | Submit button | A reproduire | Critique |
| PF-08 | Bouton Reset (reinitialisation) | Reset button | A reproduire | Haute |
| PF-09 | Copie de temps (Copy time / Copy selected time) | Copy time dropdown + Copy selected | A reproduire | Haute |
| PF-10 | Toggle "Display description" (afficher/masquer descriptions) | Display description toggle | A reproduire | Moyenne |
| PF-11 | Toggle "Hide status" (masquer les statuts de tache) | Hide status toggle | A reproduire | Moyenne |
| PF-12 | Toggle "Hide activities" (masquer les activites) | Hide activities checkbox | A reproduire | Moyenne |
| PF-13 | Statut de tache (effort, pourcentage, date de fin) | Task status icons | A reproduire et ameliorer | Haute |
| PF-14 | Lien cliquable vers tache et projet | Task link + Project link | A reproduire | Haute |
| PF-15 | Dropdown "Non-project time" (ajout temps non-projet) | Non-project time dropdown | A reproduire | Haute |
| PF-16 | Grisage des jours non-ouvrables | Weekend greyed out | A reproduire | Haute |
| PF-17 | Module Expenses (saisie de depenses) | Expense form | A reproduire | Haute |
| PF-18 | Rapports de depenses (creation, consultation) | Create/View expense reports | A reproduire | Haute |
| PF-19 | Upload fichier carte de credit | Upload credit card file | A reproduire | Moyenne |
| PF-20 | Approbation des feuilles de temps (Time approver) | Workflow d'approbation | A reproduire | Critique |
| PF-21 | Calendrier / vue calendrier des temps | Non present dans ChangePoint | A ajouter | Moyenne |
| PF-22 | Statistiques et tableau de bord temps | Non present dans ChangePoint | A ajouter | Moyenne |
| PF-23 | Multi-entites (Provencher Roy, PRAA) | Entity management | A reproduire | Critique |

---

## 5. User Stories detaillees

---

### US-CT-01 -- Grille de saisie hebdomadaire

**En tant que** collaborateur (architecte, dessinateur, chef de projet)
**Je veux** visualiser et utiliser une grille de saisie hebdomadaire affichant mes taches assignees sur 7 jours
**Afin de** saisir mes heures de travail de maniere structuree et avoir une vision complete de ma semaine

| # | Critere d'acceptation |
|---|---|
| 1 | La grille affiche 7 colonnes de jours (du jour de debut de semaine configure au dernier jour) plus une colonne Total |
| 2 | Chaque ligne represente une tache ou un temps non-projet avec les colonnes : Pin, Tache (lien cliquable), Projet (lien cliquable), Statut de tache (effort, pourcentage d'avancement, date de fin), cellules horaires par jour, Total de la ligne |
| 3 | Une ligne "Total" en bas de la grille affiche la somme des heures par colonne (par jour) et le total global de la semaine |
| 4 | Les jours non-ouvrables (samedi, dimanche ou selon la configuration du calendrier) sont visuellement distingues par un fond grise |
| 5 | Le titre de la page affiche "Feuille de temps" suivi du nom complet de l'utilisateur connecte (ex : "Feuille de temps -- Philippe Haumesser") |
| 6 | Les taches sans heures saisies pour la semaine en cours sont affichees avec des cellules vides (0.00 ou vide selon preference utilisateur) |
| 7 | La grille est scrollable verticalement si le nombre de taches depasse la hauteur visible de l'ecran |
| 8 | Les en-tetes de colonnes de jours affichent le jour de la semaine et la date (ex : "Lun 24", "Mar 25") |
| 9 | La grille supporte un minimum de 50 lignes de taches simultanees sans degradation de performance |
| 10 | Un indicateur visuel (couleur, icone) distingue les lignes de temps projet des lignes de temps non-projet |

---

### US-CT-02 -- Saisie des heures par jour

**En tant que** collaborateur
**Je veux** saisir mes heures travaillees dans chaque cellule de la grille (intersection tache/jour)
**Afin de** enregistrer precisement le temps passe sur chaque tache pour chaque jour de la semaine

| # | Critere d'acceptation |
|---|---|
| 1 | Chaque cellule horaire est editable par un clic direct (mode inline editing) |
| 2 | Les valeurs acceptees sont des nombres decimaux positifs avec une precision de deux decimales (ex : 0.25, 0.50, 1.00, 2.75, 5.00, 7.50) |
| 3 | La saisie de valeurs negatives est interdite ; un message d'erreur est affiche si l'utilisateur tente de saisir une valeur negative |
| 4 | Le total de la ligne est recalcule en temps reel a chaque modification d'une cellule de la ligne |
| 5 | Le total de la colonne (jour) est recalcule en temps reel a chaque modification d'une cellule de la colonne |
| 6 | Le total global de la semaine (coin bas-droite de la grille) est recalcule en temps reel |
| 7 | La navigation entre cellules est possible au clavier (Tab pour la cellule suivante, Shift+Tab pour la precedente, Entree pour valider et passer a la ligne suivante) |
| 8 | Les cellules des jours non-ouvrables sont editables (possibilite de saisir des heures supplementaires le week-end) mais visuellement grisees |
| 9 | La sauvegarde des heures saisies est automatique (auto-save) a chaque changement de cellule ou a intervalle regulier (toutes les 30 secondes) |
| 10 | Un indicateur visuel confirme la sauvegarde automatique (icone de sauvegarde ou message discret "Sauvegarde automatique") |

---

### US-CT-03 -- Assignments non-projet (temps non facturable)

**En tant que** collaborateur
**Je veux** saisir du temps sur des categories de temps non-projet (formation, vacances, maladie, feries, etc.)
**Afin de** declarer l'ensemble de mon temps de travail, y compris les periodes non facturables

| # | Critere d'acceptation |
|---|---|
| 1 | Une sidebar ou un panneau lateral affiche la liste des assignments non-projet disponibles, groupes par categorie |
| 2 | Les categories de temps non-projet incluent au minimum : 01. Formation externe, 02. Temps en banque, 03. Conge sans solde, 04. Vacances, 05. Maladie, 06. Ferie, 07. Conges sociaux, 08. Pour RH - ICD, 09. Pour RH - ILD |
| 3 | Chaque assignment non-projet affiche : un numero d'ordre, un nom bilingue (francais/anglais), une description, l'entite associee (ex : Provencher_Roy Prod) |
| 4 | Un dropdown "Temps non-projet" dans la barre d'outils permet d'ajouter rapidement une ligne de temps non-projet a la grille |
| 5 | Lorsqu'une ligne de temps non-projet est ajoutee a la grille, la colonne "Projet" affiche "Temps non-projet" (ou "Non-project time") |
| 6 | Les lignes de temps non-projet sont visuellement distinguees des lignes de temps projet (couleur, icone, ou separateur) |
| 7 | La sidebar des assignments dispose de trois actions en haut : filtrer, afficher en liste, copier |
| 8 | La liste des assignments est scrollable si elle depasse la hauteur visible du panneau |
| 9 | Les categories de temps non-projet sont configurables par un administrateur (ajout, modification, desactivation) |
| 10 | Un assignment non-projet ajoute a la grille peut etre retire si aucune heure n'a ete saisie dessus pour la semaine courante |

---

### US-CT-04 -- Pin / Epinglage de taches

**En tant que** collaborateur
**Je veux** epingler certaines taches en haut de ma grille de saisie
**Afin de** garder mes taches les plus frequentes ou prioritaires toujours visibles et accessibles rapidement

| # | Critere d'acceptation |
|---|---|
| 1 | Chaque ligne de la grille dispose d'une icone "Pin" (epingle) dans la premiere colonne |
| 2 | Un clic sur l'icone Pin epingle la tache : elle remonte en haut de la grille et l'icone passe en couleur bleue (etat actif) |
| 3 | Un second clic sur l'icone Pin desepingle la tache : elle retourne a sa position naturelle et l'icone revient en couleur grise (etat inactif) |
| 4 | Les taches epinglees restent en haut de la grille meme lors de la navigation entre semaines |
| 5 | L'etat d'epinglage est persiste cote serveur et restaure a chaque connexion de l'utilisateur |
| 6 | Plusieurs taches peuvent etre epinglees simultanement ; elles sont affichees dans l'ordre d'epinglage (derniere epinglee en dernier dans le groupe epingle) |
| 7 | Un separateur visuel (ligne, espacement) distingue les taches epinglees des taches non epinglees |
| 8 | L'epinglage est propre a chaque utilisateur (ne modifie pas l'affichage des autres utilisateurs) |

---

### US-CT-05 -- Navigation hebdomadaire

**En tant que** collaborateur
**Je veux** naviguer d'une semaine a l'autre dans ma feuille de temps
**Afin de** saisir ou consulter mes heures pour n'importe quelle semaine passee ou future

| # | Critere d'acceptation |
|---|---|
| 1 | La barre d'outils affiche la semaine courante avec le format "Debut de semaine : [Jour], [Date complete]" (ex : "Debut de semaine : Dim. 22 fev. 2026") |
| 2 | Deux fleches de navigation (precedent et suivant) permettent de passer a la semaine precedente ou suivante |
| 3 | Un clic sur la fleche gauche charge la feuille de temps de la semaine precedente avec toutes les donnees sauvegardees |
| 4 | Un clic sur la fleche droite charge la feuille de temps de la semaine suivante |
| 5 | Un bouton "Aujourd'hui" ou un clic sur la date permet de revenir rapidement a la semaine courante |
| 6 | Le chargement de la nouvelle semaine conserve l'ordre des taches, l'etat d'epinglage et les preferences d'affichage (toggles) |
| 7 | Les heures de la semaine precedente ne sont pas perdues lors de la navigation (sauvegarde automatique avant navigation) |
| 8 | Le jour de debut de semaine est configurable au niveau administrateur (dimanche ou lundi) ; par defaut : dimanche (coherence ChangePoint) |
| 9 | Un selecteur de date (date picker) permet de naviguer directement a une semaine specifique sans utiliser les fleches |
| 10 | La navigation est possible sur une plage d'au moins 2 ans dans le passe et 1 an dans le futur |

---

### US-CT-06 -- Soumission de la feuille de temps (Submit)

**En tant que** collaborateur
**Je veux** soumettre ma feuille de temps de la semaine pour validation
**Afin de** signaler a mon responsable que mes heures sont completes et pretes a etre approuvees

| # | Critere d'acceptation |
|---|---|
| 1 | Un bouton "Soumettre" (Submit) est visible dans la barre d'outils en haut a droite de la grille |
| 2 | Un clic sur "Soumettre" declenche une validation prealable : verification que le total hebdomadaire atteint le minimum requis (ex : 37.5h ou 40h selon la configuration) |
| 3 | Si la validation echoue, un message d'avertissement est affiche avec le detail de l'ecart (ex : "Votre total hebdomadaire est de 35.00h. Le minimum requis est de 37.50h. Voulez-vous soumettre quand meme ?") |
| 4 | Si la validation reussit ou si l'utilisateur confirme malgre l'avertissement, la feuille de temps passe au statut "Soumise" (Submitted) |
| 5 | Une fois soumise, les cellules horaires deviennent non editables (lecture seule) et un indicateur visuel "Soumise" est affiche |
| 6 | L'approbateur designe (Time approver) recoit une notification (email et/ou notification in-app) l'informant qu'une feuille de temps est en attente d'approbation |
| 7 | Le bouton "Soumettre" est remplace par un indicateur de statut (ex : "Soumise le [date]" ou "En attente d'approbation") |
| 8 | L'utilisateur peut rappeler (retirer la soumission) une feuille de temps soumise tant qu'elle n'a pas ete approuvee |
| 9 | La soumission concerne la semaine entiere (les 7 jours) et non des jours individuels |
| 10 | Un historique des soumissions est accessible (date de soumission, date d'approbation/rejet, commentaire de l'approbateur) |

---

### US-CT-07 -- Reinitialisation de la feuille de temps (Reset)

**En tant que** collaborateur
**Je veux** reinitialiser ma feuille de temps de la semaine courante
**Afin de** annuler toutes les modifications non soumises et revenir a l'etat de la derniere sauvegarde validee

| # | Critere d'acceptation |
|---|---|
| 1 | Un bouton "Reinitialiser" (Reset) est visible dans la barre d'outils en haut a droite, a cote du bouton "Soumettre" |
| 2 | Un clic sur "Reinitialiser" affiche une modale de confirmation : "Etes-vous sur de vouloir reinitialiser votre feuille de temps ? Toutes les modifications non sauvegardees seront perdues." |
| 3 | Si l'utilisateur confirme, toutes les heures modifiees depuis la derniere soumission validee ou la derniere sauvegarde officielle sont restaurees a leur etat precedent |
| 4 | Si l'utilisateur annule, la modale se ferme et la grille reste inchangee |
| 5 | Le bouton "Reinitialiser" est desactive (grise) si aucune modification n'a ete effectuee depuis la derniere sauvegarde |
| 6 | La reinitialisation ne s'applique qu'a la semaine actuellement affichee |
| 7 | Les taches epinglees et les preferences d'affichage ne sont pas affectees par la reinitialisation |

---

### US-CT-08 -- Copie de temps (Copy time / Copy selected time)

**En tant que** collaborateur
**Je veux** copier mes entrees de temps d'une semaine a une autre ou copier des entrees selectionnees
**Afin de** gagner du temps lors de la saisie de semaines recurrentes ou similaires

| # | Critere d'acceptation |
|---|---|
| 1 | Un bouton "Copier le temps" (Copy time) est disponible en bas de la grille avec un menu deroulant proposant les options de copie |
| 2 | Les options de copie incluent : "Copier la semaine precedente" (reprend toutes les lignes et heures de la semaine N-1), "Copier la structure" (reprend les lignes de taches sans les heures), "Copier vers la semaine suivante" (duplique la semaine courante vers N+1) |
| 3 | Un bouton "Copier les entrees selectionnees" (Copy selected time) permet de copier uniquement les lignes selectionnees via des cases a cocher |
| 4 | La copie de la semaine precedente pre-remplit les cellules avec les heures de la semaine precedente ; l'utilisateur peut modifier les valeurs avant de sauvegarder |
| 5 | Si la semaine cible contient deja des donnees, une modale de confirmation demande a l'utilisateur s'il souhaite "Ecraser" ou "Fusionner" (ajouter les heures aux valeurs existantes) |
| 6 | La copie ne concerne que les heures ; les statuts de soumission et d'approbation ne sont pas copies |
| 7 | La copie fonctionne pour les lignes de temps projet et les lignes de temps non-projet |
| 8 | Un message de confirmation est affiche apres une copie reussie (ex : "X lignes copiees avec succes") |
| 9 | Des cases a cocher sont disponibles sur chaque ligne de la grille pour permettre la selection multiple avant la copie selective |

---

### US-CT-09 -- Statut de tache dans la grille

**En tant que** collaborateur ou chef de projet
**Je veux** visualiser le statut de chaque tache directement dans la grille de saisie des temps
**Afin de** connaitre l'etat d'avancement de mes taches (effort prevu, pourcentage d'avancement, date de fin) sans quitter la feuille de temps

| # | Critere d'acceptation |
|---|---|
| 1 | Une colonne "Statut de tache" (Task status) est affichee dans la grille entre la colonne "Projet" et les colonnes de jours |
| 2 | Le statut de tache affiche trois informations : l'effort planifie (en heures, ex : "1.00"), le pourcentage d'avancement (ex : "99%"), la date de fin prevue (ex : "28/02/2026") |
| 3 | Chaque information est representee par une icone et une valeur lisible (icone effort, icone pourcentage, icone calendrier) |
| 4 | Le pourcentage d'avancement est mis a jour dynamiquement en fonction des heures saisies par rapport a l'effort planifie |
| 5 | Les taches dont la date de fin est depassee sont signalees visuellement (couleur rouge ou icone d'alerte) |
| 6 | Les taches dont le pourcentage d'avancement depasse 100% sont signalees visuellement (depassement de budget temps) |
| 7 | Un survol (hover) sur la colonne statut affiche un tooltip avec les details complets de la tache |
| 8 | La colonne "Statut de tache" peut etre masquee via le toggle "Hide status" (US-CT-11) |
| 9 | Les lignes de temps non-projet n'affichent pas de statut de tache (cellule vide) |

---

### US-CT-10 -- Toggle "Display description" (affichage des descriptions)

**En tant que** collaborateur
**Je veux** activer ou desactiver l'affichage des descriptions detaillees des taches dans la grille
**Afin de** adapter l'affichage selon mes besoins : vue compacte pour la saisie rapide ou vue detaillee pour le contexte

| # | Critere d'acceptation |
|---|---|
| 1 | Un toggle "Afficher les descriptions" (Display description) est disponible dans la barre d'outils de la grille |
| 2 | Lorsque le toggle est active (ON), une sous-ligne de description est affichee sous chaque tache, contenant la description textuelle de la tache |
| 3 | Lorsque le toggle est desactive (OFF), seul le nom de la tache est affiche (vue compacte) |
| 4 | L'etat du toggle est persiste dans les preferences utilisateur et restaure a la prochaine connexion |
| 5 | La description affichee est la description de la tache telle que definie dans le module Projets (EPIC-002) |
| 6 | Le basculement du toggle est instantane (pas de rechargement de page) |
| 7 | La description est tronquee si elle depasse une longueur maximale (ex : 150 caracteres) avec un lien "Voir plus" |

---

### US-CT-11 -- Toggle "Hide status" (masquage des statuts)

**En tant que** collaborateur
**Je veux** masquer ou afficher la colonne de statut des taches dans la grille
**Afin de** simplifier l'affichage de ma feuille de temps quand les informations de statut ne me sont pas utiles

| # | Critere d'acceptation |
|---|---|
| 1 | Un toggle "Masquer les statuts" (Hide status) est disponible dans la barre d'outils de la grille |
| 2 | Lorsque le toggle est active (ON), la colonne "Statut de tache" (effort, pourcentage, date de fin) est masquee |
| 3 | Lorsque le toggle est desactive (OFF), la colonne "Statut de tache" est affichee normalement |
| 4 | Le masquage de la colonne libere de l'espace horizontal, permettant aux colonnes de jours d'etre plus larges |
| 5 | L'etat du toggle est persiste dans les preferences utilisateur |
| 6 | Le basculement est instantane (pas de rechargement de page) |

---

### US-CT-12 -- Approbation des feuilles de temps (Time Approver)

**En tant que** responsable / approbateur de temps (Time Approver)
**Je veux** consulter, approuver ou rejeter les feuilles de temps soumises par les membres de mon equipe
**Afin de** valider les heures declarees et garantir la fiabilite des donnees de temps pour la facturation et le suivi budgetaire

| # | Critere d'acceptation |
|---|---|
| 1 | Une vue "Approbation des temps" est accessible aux utilisateurs ayant le role "Time Approver" |
| 2 | La vue affiche la liste des feuilles de temps soumises par les collaborateurs de l'equipe, avec : nom du collaborateur, semaine concernee, total d'heures, date de soumission, statut (En attente, Approuvee, Rejetee) |
| 3 | Un clic sur une feuille de temps ouvre la grille en lecture seule avec le detail des heures par tache et par jour |
| 4 | L'approbateur peut approuver la feuille de temps en un clic via un bouton "Approuver" |
| 5 | L'approbateur peut rejeter la feuille de temps via un bouton "Rejeter" qui ouvre un champ de commentaire obligatoire pour justifier le rejet |
| 6 | Apres approbation, la feuille de temps passe au statut "Approuvee" et les heures sont verrouillees definitivement |
| 7 | Apres rejet, le collaborateur recoit une notification avec le motif du rejet et peut modifier et resoumettre sa feuille de temps |
| 8 | L'approbateur peut approuver ou rejeter plusieurs feuilles de temps en masse (selection multiple + action groupee) |
| 9 | Des filtres permettent de trier les feuilles de temps par : statut, collaborateur, semaine, equipe |
| 10 | Un indicateur visuel affiche le nombre de feuilles de temps en attente d'approbation (badge sur le menu ou notification) |
| 11 | L'historique des approbations et rejets est conserve et consultable |

---

### US-CT-13 -- Notes de frais (Expenses)

**En tant que** collaborateur
**Je veux** saisir des notes de frais (depenses) associees a mes projets depuis le module Feuilles de Temps
**Afin de** declarer mes depenses professionnelles (deplacements, repas, hebergement, fournitures) dans le meme contexte que mes heures de travail

| # | Critere d'acceptation |
|---|---|
| 1 | Un onglet ou un lien "Depenses" (Expenses) est accessible depuis l'interface de la feuille de temps |
| 2 | Le formulaire de saisie d'une depense comprend les champs de la section "Project information" : Client (obligatoire), Contrat (obligatoire), Projet (obligatoire), Tache associee (optionnel), Forfait fixe (optionnel), Groupe de lieu d'engagement (obligatoire), Lieu d'engagement (obligatoire) |
| 3 | Le formulaire comprend les champs de la section "Expense information" : Date de la depense (obligatoire), Categorie (obligatoire), Type (obligatoire), Case a cocher "Facturable" (Billable), Description (obligatoire), Devise (obligatoire, defaut CAD), Quantite (obligatoire), Prix unitaire (obligatoire), Total (calcule automatiquement = Quantite x Prix unitaire), Taux de change (obligatoire si devise differente), Total converti (calcule automatiquement), Type de taxe incluse (optionnel) |
| 4 | Les actions disponibles sont : Nouveau (New), Sauvegarder (Save), Sauvegarder et Nouveau (Save & New), Sauvegarder et Copier (Save & Copy) |
| 5 | La liste des depenses saisies est affichee sous le formulaire avec les colonnes : Projet, Date, Description, Type, Total, Facturable (oui/non), Piece jointe |
| 6 | Chaque ligne de depense peut etre editee ou supprimee |
| 7 | Le total est calcule automatiquement et en temps reel a la modification de la quantite ou du prix unitaire |
| 8 | Le total converti est recalcule automatiquement a la modification du taux de change |
| 9 | Une piece jointe (justificatif) peut etre ajoutee a chaque depense (photo, scan PDF, image) |
| 10 | La devise par defaut est CAD (Dollar canadien) ; d'autres devises sont selectionnables avec taux de change configurable |

---

### US-CT-14 -- Rapports de depenses (Expense Reports)

**En tant que** collaborateur
**Je veux** creer des rapports de depenses regroupant plusieurs notes de frais et consulter les rapports existants
**Afin de** soumettre mes depenses de maniere organisee pour remboursement et suivi comptable

| # | Critere d'acceptation |
|---|---|
| 1 | Un bouton "Creer un rapport de depenses" (Create expense report) est disponible dans le module Depenses |
| 2 | La creation d'un rapport de depenses permet de selectionner les depenses a inclure parmi les depenses non encore associees a un rapport |
| 3 | Le rapport de depenses genere comprend : un titre, une periode, la liste des depenses incluses, le total general, le total facturable, le total non facturable |
| 4 | Un bouton "Voir les rapports de depenses" (View expense reports) affiche la liste de tous les rapports crees par l'utilisateur |
| 5 | Chaque rapport peut etre consulte en detail, modifie (ajout/retrait de depenses) ou soumis pour approbation |
| 6 | Un rapport soumis suit le meme workflow d'approbation que les feuilles de temps (approbation par un responsable) |
| 7 | Les rapports de depenses peuvent etre exportes en PDF |
| 8 | Un bouton "Telecharger fichier carte de credit" (Upload credit card file) permet d'importer un releve de carte de credit (format CSV) pour pre-remplir des lignes de depenses |
| 9 | Le fichier carte de credit importe est parse et les lignes de depenses sont pre-creees avec les montants et dates, en attente de categorisation manuelle par l'utilisateur |

---

### US-CT-15 -- Vue calendrier des temps

**En tant que** collaborateur ou chef de projet
**Je veux** visualiser mes heures saisies sur une vue calendrier mensuelle
**Afin de** avoir une vision d'ensemble de ma charge de travail sur le mois et identifier rapidement les jours sans saisie ou en surcharge

| # | Critere d'acceptation |
|---|---|
| 1 | Une vue "Calendrier" est accessible via un onglet ou un bouton bascule depuis la vue grille hebdomadaire |
| 2 | Le calendrier affiche un mois complet avec le total d'heures saisies pour chaque jour |
| 3 | Chaque jour du calendrier est cliquable et affiche le detail des heures par tache dans un panneau lateral ou une modale |
| 4 | Les jours sans aucune heure saisie sont signales visuellement (fond rouge ou icone d'alerte) pour les jours ouvrables |
| 5 | Les jours feries et les jours de conge (vacances, maladie) sont affiches avec un code couleur distinct |
| 6 | Les jours ou le total depasse le nombre d'heures attendu (ex : > 8h) sont signales visuellement (fond orange) |
| 7 | Le calendrier affiche le total mensuel et le compare au nombre d'heures attendu pour le mois |
| 8 | La navigation entre mois est possible via des fleches (mois precedent / mois suivant) |
| 9 | Un clic sur un jour permet de basculer vers la vue grille hebdomadaire de la semaine correspondante |

---

### US-CT-16 -- Statistiques et tableau de bord des temps

**En tant que** collaborateur, chef de projet ou directeur
**Je veux** acceder a un tableau de bord synthetique de mes heures (ou des heures de mon equipe)
**Afin de** suivre mes tendances de saisie, identifier les ecarts par rapport aux objectifs et piloter la charge de travail

| # | Critere d'acceptation |
|---|---|
| 1 | Un tableau de bord "Statistiques temps" est accessible depuis le module Feuilles de Temps |
| 2 | Les indicateurs suivants sont affiches pour le collaborateur connecte : total d'heures saisies cette semaine vs objectif hebdomadaire, total d'heures saisies ce mois vs objectif mensuel, repartition du temps entre projet et non-projet (graphique camembert), top 5 des projets par heures consommees (graphique barres), taux de saisie (nombre de jours avec saisie vs nombre de jours ouvrables) |
| 3 | Pour un chef de projet : total d'heures consommees sur ses projets vs budget planifie, repartition par collaborateur, alerte de depassement de budget |
| 4 | Pour un directeur / administrateur : total d'heures saisies par l'ensemble des collaborateurs, taux de soumission des feuilles de temps, collaborateurs en retard de saisie, repartition temps projet vs temps non-projet a l'echelle de l'agence |
| 5 | Un selecteur de periode permet de filtrer les statistiques (semaine, mois, trimestre, annee, personnalise) |
| 6 | Les donnees sont exportables en CSV ou PDF |
| 7 | Les graphiques sont interactifs (survol pour details, clic pour filtrer) |
| 8 | Le tableau de bord se charge en moins de 3 secondes pour un historique de 12 mois |

---

## 6. Hors Perimetre

Les elements suivants sont explicitement exclus du perimetre de cet EPIC :

- **Gestion des projets et des taches** : la creation, modification et suppression des projets et taches sont couvertes par EPIC-002 (Projets). Le module Feuilles de Temps consomme ces donnees en lecture seule.
- **Calcul des honoraires et de la rentabilite** : le lien entre heures saisies et rentabilite financiere est couvert par EPIC-003 (Honoraires) et EPIC-008 (Finances).
- **Facturation des heures** : la generation de factures a partir des heures saisies est couverte par EPIC-004 (Facturation).
- **Planning et assignation des ressources** : la planification des collaborateurs sur les projets est couverte par EPIC-006 (Planning).
- **Gestion des conges et absences avancee** : un module dedie de gestion des conges (soldes, demandes, approbation RH) n'est pas dans le perimetre de cet EPIC. Seule la declaration de temps non-projet (vacances, maladie, ferie) est couverte.
- **Paie et calcul salarial** : aucun traitement de paie ni calcul de remuneration n'est dans le perimetre.
- **Integration avec des systemes de pointage physique** : pas d'integration avec des badgeuses ou des systemes biometriques.
- **Gestion documentaire avancee (GED)** : seule la piece jointe de justificatif de depense est couverte ; pas de GED complete.
- **Application mobile native** : le responsive design (tablette) est couvert, mais une application mobile native n'est pas dans le perimetre.
- **Import/export de donnees depuis ChangePoint** : la migration des donnees historiques depuis ChangePoint n'est pas couverte par cet EPIC (un EPIC de migration separé sera necessaire).

---

## 7. Regles Metier

| Ref | Regle |
|---|---|
| **RG-01** | Le total hebdomadaire par defaut attendu est de **37.50 heures** (configurable par entite : 35h, 37.5h, 40h). Un avertissement est affiche si le total soumis est inferieur au minimum configure. |
| **RG-02** | Les heures sont saisies en **format decimal** avec une precision de deux decimales (0.25 = 15 min, 0.50 = 30 min, 0.75 = 45 min, 1.00 = 1h). La granularite minimale est de 0.25h (15 minutes). |
| **RG-03** | La **devise par defaut** est le CAD (Dollar canadien). Les taux de change pour les depenses en devise etrangere doivent etre configures par un administrateur ou saisis manuellement. |
| **RG-04** | Une feuille de temps ne peut etre soumise que pour une **semaine complete** (7 jours). La soumission partielle (jour par jour) n'est pas autorisee. |
| **RG-05** | Une feuille de temps **soumise** est verrouillee en edition. Elle ne peut etre modifiee qu'apres un rappel (retrait de la soumission) par le collaborateur ou un rejet par l'approbateur. |
| **RG-06** | Une feuille de temps **approuvee** est definitivement verrouillee. Seul un administrateur peut la deverrouiller dans des cas exceptionnels (avec justification tracee). |
| **RG-07** | Les **jours feries** sont determines par le calendrier de l'entite. Les heures saisies sur un jour ferie sont automatiquement classees comme "heures supplementaires" ou "feries" selon la configuration. |
| **RG-08** | Les **assignments non-projet** sont lies a une entite (ex : Provencher_Roy Prod). Un collaborateur ne peut saisir du temps non-projet que sur les categories autorisees pour son entite de rattachement. |
| **RG-09** | Le **statut d'une tache** (effort planifie, pourcentage d'avancement, date de fin) est en lecture seule dans la grille des temps. La modification de ces valeurs se fait dans le module Projets (EPIC-002). |
| **RG-10** | La **copie de temps** d'une semaine a une autre ne copie pas les statuts de soumission ni d'approbation. La semaine cible est creee avec le statut "Brouillon". |
| **RG-11** | Un collaborateur ne peut saisir du temps que sur les **taches qui lui sont assignees** dans le module Projets. Les taches non assignees n'apparaissent pas dans la grille. |
| **RG-12** | Les **depenses** saisies doivent etre associees a un projet et un contrat valides. Le champ "Facturable" (Billable) determine si la depense sera refacturee au client. |
| **RG-13** | Le **taux de change** applique aux depenses en devise etrangere est celui en vigueur a la date de la depense. Le total converti est recalcule automatiquement si le taux est modifie. |
| **RG-14** | Le **rapport de depenses** ne peut etre soumis que si toutes les depenses incluses ont les champs obligatoires renseignes (projet, date, categorie, type, description, montant). |
| **RG-15** | Un collaborateur peut saisir du temps retroactivement sur les **4 semaines precedentes** sans restriction. Au-dela de 4 semaines, une approbation administrative est requise. |
| **RG-16** | Les heures saisies sur un jour ne peuvent pas depasser **24.00 heures** pour un meme collaborateur. Une alerte est affichee si le total journalier depasse 12.00 heures. |
| **RG-17** | Le systeme doit supporter la **multi-entite** : un collaborateur rattache a l'entite "Provencher_Roy Prod" peut saisir du temps sur des projets de l'entite "PRAA" s'il y est assigne. |
| **RG-18** | Les noms de taches et de projets doivent etre affiches en **format bilingue** (francais/anglais) lorsque les deux versions existent (ex : "Reunions/Meetings", "Rencontre d'equipe/Team meeting"). |

---

## 8. Criteres d'Acceptance Globaux

| # | Critere |
|---|---|
| 1 | Toutes les User Stories US-CT-01 a US-CT-16 sont developpees, testees et validees par le Product Owner. |
| 2 | La grille de saisie hebdomadaire est fonctionnelle avec saisie inline, calcul des totaux en temps reel et sauvegarde automatique. |
| 3 | Les 9 categories de temps non-projet de ChangePoint sont reproduites et fonctionnelles. |
| 4 | Le workflow complet Saisie -> Soumission -> Approbation / Rejet -> Ressoumission est operationnel. |
| 5 | La navigation hebdomadaire (fleches, date picker, bouton "Aujourd'hui") est fluide et charge les donnees en moins de 2 secondes. |
| 6 | La copie de temps (semaine complete et selection) fonctionne sans perte de donnees et avec confirmation en cas de conflit. |
| 7 | Le module Depenses est fonctionnel avec tous les champs du formulaire ChangePoint (Project information + Expense information). |
| 8 | Les rapports de depenses peuvent etre crees, consultes, soumis et exportes en PDF. |
| 9 | L'upload de fichier carte de credit (CSV) est fonctionnel et pre-remplit les lignes de depenses. |
| 10 | Les toggles (Display description, Hide status) fonctionnent instantanement et leur etat est persiste dans les preferences utilisateur. |
| 11 | Le systeme multi-entite est respecte : les projets et assignments affichent l'entite de rattachement. |
| 12 | La grille de saisie est responsive et utilisable sur tablette (largeur minimale 768px). |
| 13 | Les performances sont acceptables : chargement de la grille < 2 secondes, calcul des totaux < 200ms, sauvegarde automatique < 1 seconde. |
| 14 | Les notifications d'approbation sont envoyees correctement (email et/ou in-app). |
| 15 | Le calendrier mensuel et le tableau de bord statistiques sont fonctionnels et coherents avec les donnees de la grille. |

---

## 9. Definition of Done

| # | Critere |
|---|---|
| 1 | Le code est developpe, revu par un pair (code review) et merge sur la branche principale. |
| 2 | Les tests unitaires couvrent au minimum 80% des fonctions critiques : calcul des totaux, validation de soumission, conversion de devises, parsing de fichier CSV, regles de verrouillage. |
| 3 | Les tests d'integration valident les flux principaux : saisie -> sauvegarde automatique -> soumission -> approbation / rejet. |
| 4 | Les tests d'integration valident le flux de depenses : saisie -> creation rapport -> soumission -> approbation. |
| 5 | Les tests de performance valident le chargement de la grille avec 50+ lignes de taches en moins de 2 secondes. |
| 6 | La documentation technique est mise a jour (API endpoints, modele de donnees, diagrammes de flux). |
| 7 | La fonctionnalite a ete testee et validee sur un environnement de recette par le Product Owner. |
| 8 | Aucun bug bloquant ou critique n'est ouvert sur les User Stories de l'EPIC. |
| 9 | Les messages d'erreur, les libelles et les tooltips sont rediges en francais et relus. |
| 10 | L'accessibilite de base est assuree : navigation clavier complete dans la grille, contrastes suffisants, labels ARIA sur les champs de formulaire. |
| 11 | Les donnees de demonstration sont coherentes et representatives (au moins 10 projets, 30 taches, 4 semaines d'historique de temps, 15 depenses). |
| 12 | Le guide utilisateur (aide en ligne) est redige pour les fonctionnalites principales (saisie, soumission, approbation, depenses). |

---

## 10. Dependances

### Dependances fonctionnelles

| Type | EPIC / Module | Description |
|---|---|---|
| **Depend de** | EPIC-002 (Projets) | Les taches et projets affiches dans la grille proviennent du module Projets. La creation et la modification des taches ne sont pas dans le perimetre de cet EPIC. |
| **Depend de** | EPIC-003 (Honoraires) | L'effort planifie et le budget heures par tache proviennent des honoraires. |
| **Depend de** | EPIC-006 (Planning) | Les assignations de collaborateurs aux taches proviennent du planning. |
| **Depend de** | EPIC-009 (Collaborateurs) | Les informations utilisateur (nom, entite, role, equipe) proviennent du module Collaborateurs. |
| **Depend de** | EPIC-010 (Clients) | Les informations client (pour les depenses) proviennent du module Clients. |
| **Depend de** | EPIC-016 (Configuration) | Le calendrier des jours feries, le jour de debut de semaine, le nombre d'heures attendu, les categories de temps non-projet sont geres dans la configuration. |
| **Requis par** | EPIC-004 (Facturation) | Les heures approuvees alimentent la facturation des honoraires au temps passe. |
| **Requis par** | EPIC-007 (Couts) | Les heures saisies alimentent le calcul des couts de main-d'oeuvre et la rentabilite des projets. |
| **Requis par** | EPIC-008 (Finances) | Les donnees de temps alimentent les etats financiers et les analyses de rentabilite. |
| **Requis par** | EPIC-011 (Rapports) | Les donnees de temps alimentent les rapports transversaux (heures par projet, par collaborateur, par periode). |
| **Requis par** | EPIC-012 (Validation) | Le workflow d'approbation des feuilles de temps s'appuie sur le module de validation. |
| **Requis par** | EPIC-013 (Notes de frais) | Les depenses saisies dans le module Temps sont liees au module Notes de frais pour le workflow complet. |
| **Requis par** | EPIC-017 (Notifications) | Les notifications de soumission, d'approbation et de rejet sont envoyees via le module Notifications. |

### Dependances techniques

| Composant | Description |
|---|---|
| **API Projets** | Lecture des projets, taches et assignations (GET) |
| **API Collaborateurs** | Lecture des informations utilisateur, entite, role (GET) |
| **API Clients** | Lecture des clients et contrats pour les depenses (GET) |
| **API Configuration** | Lecture du calendrier, jours feries, parametres de temps (GET) |
| **API Temps** | CRUD complet : creation, lecture, mise a jour, suppression des entrees de temps |
| **API Depenses** | CRUD complet : creation, lecture, mise a jour, suppression des depenses |
| **API Rapports de depenses** | Creation, lecture, soumission, approbation des rapports |
| **API Approbation** | Soumission, approbation, rejet des feuilles de temps |
| **API Notifications** | Envoi de notifications email et in-app |
| **Service de fichiers** | Upload de pieces jointes (justificatifs) et fichiers CSV (releves carte de credit) |
| **Service de taux de change** | Recuperation des taux de change pour la conversion de devises |

---

## 11. Modele de Donnees

### Objet : TimeSheet (Feuille de temps)

| Champ | Type | Description |
|---|---|---|
| `id` | UUID | Identifiant unique de la feuille de temps |
| `user_id` | FK -> User | Collaborateur proprietaire de la feuille de temps |
| `entity_id` | FK -> Entity | Entite de rattachement (Provencher_Roy Prod, PRAA) |
| `week_start_date` | Date | Date du premier jour de la semaine (ex : 2026-02-22) |
| `week_end_date` | Date | Date du dernier jour de la semaine (ex : 2026-02-28) |
| `status` | Enum | Statut : `draft`, `submitted`, `approved`, `rejected` |
| `total_hours` | Decimal(6,2) | Total des heures de la semaine (calcule) |
| `submitted_at` | DateTime (nullable) | Date et heure de soumission |
| `approved_at` | DateTime (nullable) | Date et heure d'approbation |
| `approved_by` | FK -> User (nullable) | Approbateur |
| `rejection_reason` | Text (nullable) | Motif de rejet |
| `created_at` | DateTime | Date de creation |
| `updated_at` | DateTime | Date de derniere modification |

### Objet : TimeEntry (Entree de temps)

| Champ | Type | Description |
|---|---|---|
| `id` | UUID | Identifiant unique de l'entree de temps |
| `timesheet_id` | FK -> TimeSheet | Feuille de temps parente |
| `user_id` | FK -> User | Collaborateur |
| `task_id` | FK -> Task (nullable) | Tache projet (null si temps non-projet) |
| `project_id` | FK -> Project (nullable) | Projet (null si temps non-projet) |
| `non_project_category_id` | FK -> NonProjectCategory (nullable) | Categorie de temps non-projet (null si temps projet) |
| `entry_date` | Date | Date du jour concerne |
| `hours` | Decimal(4,2) | Nombre d'heures (ex : 7.50) |
| `description` | Text (nullable) | Description / commentaire libre |
| `is_pinned` | Boolean | Tache epinglee par l'utilisateur (defaut : false) |
| `created_at` | DateTime | Date de creation |
| `updated_at` | DateTime | Date de derniere modification |

### Objet : NonProjectCategory (Categorie de temps non-projet)

| Champ | Type | Description |
|---|---|---|
| `id` | UUID | Identifiant unique |
| `code` | String | Code numerote (ex : "01", "02", ..., "09") |
| `name_fr` | String | Nom en francais (ex : "Formation externe") |
| `name_en` | String | Nom en anglais (ex : "External training") |
| `description` | Text (nullable) | Description de la categorie |
| `entity_id` | FK -> Entity | Entite de rattachement |
| `is_active` | Boolean | Categorie active/inactive (defaut : true) |
| `sort_order` | Integer | Ordre d'affichage |
| `created_at` | DateTime | Date de creation |
| `updated_at` | DateTime | Date de derniere modification |

### Objet : Expense (Depense / Note de frais)

| Champ | Type | Description |
|---|---|---|
| `id` | UUID | Identifiant unique de la depense |
| `user_id` | FK -> User | Collaborateur ayant engage la depense |
| `project_id` | FK -> Project | Projet associe (obligatoire) |
| `contract_id` | FK -> Contract | Contrat associe (obligatoire) |
| `client_id` | FK -> Client | Client associe (obligatoire) |
| `task_id` | FK -> Task (nullable) | Tache associee (optionnel) |
| `expense_report_id` | FK -> ExpenseReport (nullable) | Rapport de depenses parent |
| `expense_date` | Date | Date de la depense (obligatoire) |
| `category` | String | Categorie de depense (ex : Transport, Repas, Hebergement) |
| `type` | String | Type de depense (sous-categorie) |
| `description` | String | Description de la depense (obligatoire) |
| `currency` | String | Devise (defaut : CAD) |
| `quantity` | Decimal(8,2) | Quantite |
| `unit_price` | Decimal(10,2) | Prix unitaire |
| `total` | Decimal(10,2) | Total (calcule : quantite x prix unitaire) |
| `exchange_rate` | Decimal(8,4) | Taux de change (defaut : 1.0000 pour CAD) |
| `converted_total` | Decimal(10,2) | Total converti dans la devise de reference |
| `is_billable` | Boolean | Depense facturable au client (defaut : false) |
| `is_fixed_fee` | Boolean | Forfait fixe |
| `tax_type` | String (nullable) | Type de taxe incluse |
| `location_group` | String | Groupe de lieu d'engagement |
| `location` | String | Lieu d'engagement |
| `attachment_url` | String (nullable) | URL de la piece jointe (justificatif) |
| `created_at` | DateTime | Date de creation |
| `updated_at` | DateTime | Date de derniere modification |

### Objet : ExpenseReport (Rapport de depenses)

| Champ | Type | Description |
|---|---|---|
| `id` | UUID | Identifiant unique du rapport |
| `user_id` | FK -> User | Collaborateur auteur du rapport |
| `title` | String | Titre du rapport |
| `period_start` | Date | Debut de la periode couverte |
| `period_end` | Date | Fin de la periode couverte |
| `status` | Enum | Statut : `draft`, `submitted`, `approved`, `rejected` |
| `total_amount` | Decimal(10,2) | Montant total du rapport (calcule) |
| `total_billable` | Decimal(10,2) | Montant total facturable (calcule) |
| `total_non_billable` | Decimal(10,2) | Montant total non facturable (calcule) |
| `currency` | String | Devise de reference |
| `submitted_at` | DateTime (nullable) | Date de soumission |
| `approved_at` | DateTime (nullable) | Date d'approbation |
| `approved_by` | FK -> User (nullable) | Approbateur |
| `rejection_reason` | Text (nullable) | Motif de rejet |
| `created_at` | DateTime | Date de creation |
| `updated_at` | DateTime | Date de derniere modification |

### Objet : UserTimePreference (Preferences utilisateur pour le temps)

| Champ | Type | Description |
|---|---|---|
| `id` | UUID | Identifiant unique |
| `user_id` | FK -> User | Collaborateur |
| `display_description` | Boolean | Etat du toggle "Afficher les descriptions" (defaut : false) |
| `hide_status` | Boolean | Etat du toggle "Masquer les statuts" (defaut : false) |
| `hide_activities` | Boolean | Etat du toggle "Masquer les activites" (defaut : false) |
| `pinned_task_ids` | Array[UUID] | Liste ordonnee des taches epinglees |
| `week_start_day` | Enum | Jour de debut de semaine : `sunday`, `monday` (herite de la config entite si non defini) |
| `created_at` | DateTime | Date de creation |
| `updated_at` | DateTime | Date de derniere modification |

### Objet : TimeApproval (Historique d'approbation)

| Champ | Type | Description |
|---|---|---|
| `id` | UUID | Identifiant unique |
| `timesheet_id` | FK -> TimeSheet | Feuille de temps concernee |
| `action` | Enum | Action : `submitted`, `approved`, `rejected`, `recalled` |
| `performed_by` | FK -> User | Utilisateur ayant effectue l'action |
| `comment` | Text (nullable) | Commentaire (obligatoire pour un rejet) |
| `performed_at` | DateTime | Date et heure de l'action |

---

## 12. Estimation et Decoupage

### Sprints suggeres

| Sprint | User Stories | Perimetre | Duree estimee |
|---|---|---|---|
| **Sprint 1** | US-CT-01, US-CT-02 | Grille de saisie hebdomadaire + Saisie des heures par jour (fondations) | 2 semaines |
| **Sprint 2** | US-CT-03, US-CT-04, US-CT-05 | Assignments non-projet + Epinglage de taches + Navigation hebdomadaire | 2 semaines |
| **Sprint 3** | US-CT-06, US-CT-07, US-CT-08 | Soumission + Reinitialisation + Copie de temps | 2 semaines |
| **Sprint 4** | US-CT-09, US-CT-10, US-CT-11 | Statut de tache + Toggle descriptions + Toggle statuts | 1.5 semaine |
| **Sprint 5** | US-CT-12 | Approbation des feuilles de temps (workflow complet) | 2 semaines |
| **Sprint 6** | US-CT-13, US-CT-14 | Notes de frais + Rapports de depenses + Upload carte de credit | 2.5 semaines |
| **Sprint 7** | US-CT-15, US-CT-16 | Vue calendrier + Statistiques et tableau de bord | 2 semaines |

### Estimation globale

| Indicateur | Valeur |
|---|---|
| **Nombre de User Stories** | 16 |
| **Nombre de criteres d'acceptation** | 144 |
| **Nombre de sprints** | 7 |
| **Duree totale estimee** | 14 a 16 semaines |
| **Complexite** | Elevee (grille interactive, workflow d'approbation, multi-entite, multi-devise) |
| **Risques principaux** | Performance de la grille avec beaucoup de lignes, complexite du workflow d'approbation, integration multi-entite, gestion des taux de change |

### Prerequisites avant demarrage

- API Projets et Taches disponible en lecture (EPIC-002)
- API Collaborateurs disponible en lecture (EPIC-009)
- API Clients disponible en lecture (EPIC-010)
- Module de configuration des calendriers et jours feries operationnel (EPIC-016)
- Charte graphique et composants UI valides (systeme de design : grille editable, toggles, modales, notifications)
- Maquettes UX validees pour la grille hebdomadaire, la sidebar assignments, le formulaire de depenses, la vue calendrier et le tableau de bord
- Infrastructure de notifications email et in-app operationnelle (EPIC-017)

### Priorite de livraison recommandee

1. **MVP (Sprints 1-3)** : Grille de saisie fonctionnelle avec navigation, assignments, copie et soumission. Couvre 80% des usages quotidiens des collaborateurs.
2. **V1 Complete (Sprints 4-5)** : Ajout des statuts, toggles et workflow d'approbation. Module utilisable en production.
3. **V1.1 Depenses (Sprint 6)** : Module de depenses integre. Parite fonctionnelle avec ChangePoint atteinte.
4. **V1.2 Ameliorations (Sprint 7)** : Calendrier et statistiques. Valeur ajoutee par rapport a ChangePoint.

---

## ADDENDUM -- Fonctionnalites supplementaires identifiees lors de l'audit approfondi

**Source** : Audit approfondi du contrat Place des Arts et du profil projet
**Date d'ajout** : 27 fevrier 2026
**Raison** : Fonctionnalites de saisie de temps non couvertes dans l'EPIC initial

---

### Contexte de l'addendum

L'analyse approfondie du contrat **Place des Arts** (Provencher Roy) et de son profil projet a revele des fonctionnalites de ChangePoint non couvertes dans les 16 User Stories initiales (US-CT-01 a US-CT-16). Trois axes majeurs ont ete identifies :

1. **Work locations** : Le projet Place des Arts implique des lieux de travail multi-provinces (Alberta, Colombie-Britannique, Ile-du-Prince-Edouard, Quebec). Chaque entree de temps doit pouvoir etre associee a une province pour les implications fiscales (retenues a la source provinciales).
2. **Work codes** : Le projet utilise des codes de travail configurables (Default, et autres codes personnalisables) pour la classification fine du temps.
3. **Chaine d'approbation hierarchique** : Le contrat definit une chaine d'approbation a deux niveaux -- Time approver (Melissa Belanger) puis Approver for time approver (Audrey Monty) -- non couverte par l'approbation simple de US-CT-12. La meme logique s'applique aux depenses avec Expense approver et Approver for expense approver.

---

### US-CT-17 -- Work locations sur les entrees de temps

**En tant que** collaborateur travaillant sur un projet multi-provinces
**Je veux** associer un lieu de travail (province) a chaque entree de temps
**Afin de** declarer correctement ma province de travail effective pour chaque journee, garantissant la conformite fiscale (retenues a la source provinciales) et la tracabilite des deplacements inter-provinciaux

| # | Critere d'acceptation |
|---|---|
| 1 | Chaque entree de temps dispose d'un champ "Work location" (Lieu de travail) editable, affiche sous forme de dropdown dans la grille ou dans un panneau de detail |
| 2 | La liste des work locations disponibles est determinee par la configuration du projet/contrat. Pour le contrat Place des Arts, les provinces disponibles sont : Quebec, Alberta, Colombie-Britannique, Ile-du-Prince-Edouard |
| 3 | Un "Default work location" (lieu de travail par defaut) est configure au niveau du projet/contrat. Toute nouvelle entree de temps est automatiquement associee a ce lieu par defaut |
| 4 | Le collaborateur peut modifier le work location d'une entree de temps specifique pour refleter un deplacement (ex : passage temporaire en Alberta pour supervision de chantier) |
| 5 | Le work location est affiche dans la grille sous forme d'un indicateur compact (code province abrege ou icone) pour ne pas surcharger l'affichage |
| 6 | Un toggle "Afficher les lieux de travail" (Display work locations) permet de masquer ou afficher la colonne/indicateur de work location dans la grille |
| 7 | L'administrateur peut configurer la liste des work locations disponibles par contrat/projet via le module de configuration (EPIC-016) |
| 8 | Le changement de work location est possible sur les entrees de temps en statut "Brouillon" uniquement ; les entrees soumises ou approuvees sont verrouillees |
| 9 | L'export des feuilles de temps (CSV, PDF) inclut le work location de chaque entree de temps |
| 10 | Le systeme conserve un historique des changements de work location pour chaque entree de temps (audit trail) |
| 11 | Lors de la copie de temps d'une semaine a une autre (US-CT-08), les work locations sont copies avec les heures |
| 12 | Un rapport de synthese par work location est disponible dans le tableau de bord statistiques (US-CT-16), affichant la repartition des heures par province |

---

### US-CT-18 -- Work codes sur les entrees de temps

**En tant que** collaborateur ou chef de projet
**Je veux** associer un code de travail (work code) a chaque entree de temps
**Afin de** classifier finement le type d'activite realisee (conception, supervision, administration, etc.) pour le suivi budgetaire, la facturation et l'analyse de la repartition du temps par categorie de cout

| # | Critere d'acceptation |
|---|---|
| 1 | Chaque entree de temps dispose d'un champ "Work code" (Code de travail) editable, affiche sous forme de dropdown dans la grille ou dans un panneau de detail |
| 2 | Un work code "Default" est pre-selectionne pour toute nouvelle entree de temps. Ce code par defaut est configurable au niveau du projet/contrat |
| 3 | La liste des work codes disponibles est configurable par l'administrateur via le module de configuration (EPIC-016) |
| 4 | Chaque work code comprend : un identifiant unique, un nom court (ex : "CONC", "SUPV", "ADMIN"), un libelle complet bilingue (francais/anglais), une description, un indicateur actif/inactif |
| 5 | Le collaborateur peut modifier le work code d'une entree de temps a tout moment tant que la feuille de temps n'est pas soumise |
| 6 | Le work code est affiche dans la grille sous forme de code abrege dans une colonne dediee ou dans un panneau de detail |
| 7 | Un toggle "Afficher les codes de travail" (Display work codes) permet de masquer ou afficher la colonne de work codes dans la grille |
| 8 | Les work codes peuvent etre associes a des taux de facturation differents pour permettre une facturation differenciee selon le type d'activite |
| 9 | L'export des feuilles de temps (CSV, PDF) inclut le work code de chaque entree de temps |
| 10 | Lors de la copie de temps d'une semaine a une autre (US-CT-08), les work codes sont copies avec les heures |
| 11 | Un rapport de synthese par work code est disponible dans le tableau de bord statistiques (US-CT-16), affichant la repartition des heures par type d'activite |
| 12 | L'administrateur peut desactiver un work code sans supprimer les entrees de temps historiques qui l'utilisent |

---

### US-CT-19 -- Chaine d'approbation hierarchique (Approval Chain)

**En tant que** administrateur ou responsable de projet
**Je veux** configurer et executer une chaine d'approbation hierarchique a plusieurs niveaux pour les feuilles de temps et les rapports de depenses
**Afin de** garantir un controle multi-niveaux conforme a la gouvernance du cabinet, ou un premier approbateur (Time Approver) valide les heures puis un second approbateur (Approver for Time Approver) confirme l'approbation

| # | Critere d'acceptation |
|---|---|
| 1 | La chaine d'approbation des temps est configurable par contrat/projet avec deux niveaux : Niveau 1 -- Time Approver (ex : Melissa Belanger), Niveau 2 -- Approver for Time Approver (ex : Audrey Monty) |
| 2 | La chaine d'approbation des depenses est configurable par contrat/projet avec deux niveaux : Niveau 1 -- Expense Approver (ex : Melissa Belanger), Niveau 2 -- Approver for Expense Approver (ex : Audrey Monty) |
| 3 | Le workflow d'approbation suit un flux en cascade : Collaborateur soumet -> Time Approver (N1) recoit une notification et approuve/rejette -> si approuve, Approver for Time Approver (N2) recoit une notification et approuve/rejette definitivement |
| 4 | Si le Time Approver (N1) rejette, la feuille de temps retourne au collaborateur avec le motif de rejet, sans passer par le N2 |
| 5 | Si l'Approver for Time Approver (N2) rejette, la feuille de temps retourne au collaborateur avec le motif de rejet (le rejet au N2 annule l'approbation N1) |
| 6 | La feuille de temps passe au statut "Approuvee" uniquement apres l'approbation du dernier niveau de la chaine (N2). Des statuts intermediaires sont visibles : "Soumise", "Approuvee N1 -- En attente N2", "Approuvee" |
| 7 | Un seuil configurable (Expenses approval limit) est defini par contrat/projet (ex : 0.00 CAD pour le contrat Place des Arts). Les depenses depassant ce seuil necessitent obligatoirement l'approbation N2, meme si le N1 a approuve |
| 8 | Un delai d'escalade configurable est defini (ex : 48h, 72h). Si le Time Approver N1 ne repond pas dans le delai, la demande est automatiquement escaladee au N2 avec une notification d'escalade |
| 9 | L'historique d'approbation (TimeApproval) enregistre chaque etape de la chaine : soumission, approbation N1, approbation N2, rejet N1, rejet N2, escalade |
| 10 | La vue d'approbation (US-CT-12) est enrichie pour afficher le niveau d'approbation courant et l'identite de l'approbateur a chaque niveau |
| 11 | Un approbateur N2 peut consulter la decision et le commentaire de l'approbateur N1 avant de prendre sa propre decision |
| 12 | L'administrateur peut modifier la chaine d'approbation d'un contrat/projet a tout moment. Les feuilles de temps deja en cours d'approbation suivent la chaine configuree au moment de leur soumission |
| 13 | En l'absence d'un Approver for Time Approver configure (chaine a un seul niveau), le workflow se comporte comme l'approbation simple existante (US-CT-12) -- retrocompatibilite |

---

## Regles Metier supplementaires (Addendum)

| Ref | Regle |
|---|---|
| **RM-CT-19** | Le **work location par defaut** d'une entree de temps est herite du "Default work location" configure sur le contrat/projet. Si aucun work location par defaut n'est configure, le champ est vide et le collaborateur doit le renseigner manuellement avant soumission. |
| **RM-CT-20** | Le **work location** d'une entree de temps a des implications fiscales : les heures travaillees dans une province differente de la province de rattachement du collaborateur declenchent un signalement au module Paie/RH pour ajustement des retenues a la source provinciales. Le module Feuilles de Temps ne calcule pas les retenues mais transmet l'information. |
| **RM-CT-21** | Le **work code "Default"** est un code systeme qui ne peut pas etre supprime ni desactive. Il sert de valeur par defaut pour toutes les entrees de temps sans code specifique. Les autres work codes sont entierement configurables par l'administrateur. |
| **RM-CT-22** | La **chaine d'approbation** est definie au niveau du contrat/projet. Si un collaborateur saisit du temps sur plusieurs contrats/projets dans la meme semaine, chaque bloc de temps suit la chaine d'approbation de son contrat/projet respectif. La feuille de temps globale n'est consideree "Approuvee" que lorsque tous les blocs ont ete approuves a tous les niveaux. |
| **RM-CT-23** | Le **delai d'escalade** par defaut est de **72 heures ouvrees**. Passe ce delai sans action de l'approbateur de niveau N, la demande est escaladee au niveau N+1 et une notification d'escalade est envoyee aux deux parties (approbateur en retard et approbateur de niveau superieur). Le delai est configurable par contrat/projet (minimum 24h, maximum 168h). |
| **RM-CT-24** | Le seuil **Expenses approval limit** (limite d'approbation des depenses) est configurable par contrat/projet. Lorsque le seuil est de **0.00 CAD**, toutes les depenses -- quel que soit leur montant -- necessitent l'approbation complete de la chaine (N1 + N2). Lorsque le seuil est superieur a 0.00 CAD, seules les depenses dont le montant depasse le seuil necessitent l'approbation N2 ; les depenses en dessous du seuil peuvent etre approuvees definitivement par le N1 seul. |
| **RM-CT-25** | Lorsqu'un **approbateur N1 est absent** (conge, maladie) et qu'un delegataire est configure dans le module Collaborateurs (EPIC-009), le delegataire herite temporairement du role d'approbateur N1 pour la duree de l'absence. Les feuilles de temps approuvees par le delegataire sont tracees avec mention de la delegation. |
| **RM-CT-26** | Les **work locations** et **work codes** sont des attributs de l'entree de temps (`TimeEntry`), et non de la feuille de temps (`TimeSheet`). Un collaborateur peut avoir des work locations et work codes differents pour chaque ligne/jour de sa feuille de temps hebdomadaire. |

---

## Modele de Donnees supplementaire (Addendum)

### Modifications a l'objet TimeEntry

Les champs suivants sont ajoutes a l'objet `TimeEntry` existant (section 11) :

| Champ | Type | Description |
|---|---|---|
| `work_location_id` | FK -> WorkLocation (nullable) | Lieu de travail (province) associe a l'entree de temps |
| `work_code_id` | FK -> WorkCode (nullable) | Code de travail associe a l'entree de temps |

### Nouvel objet : WorkLocation (Lieu de travail)

| Champ | Type | Description |
|---|---|---|
| `id` | UUID | Identifiant unique |
| `name_fr` | String | Nom en francais (ex : "Quebec", "Alberta") |
| `name_en` | String | Nom en anglais (ex : "Quebec", "Alberta") |
| `province_code` | String | Code de province normalise (ex : "QC", "AB", "BC", "PE") |
| `country` | String | Pays (defaut : "CA" -- Canada) |
| `is_default` | Boolean | Lieu de travail par defaut pour le contrat/projet (defaut : false) |
| `contract_id` | FK -> Contract (nullable) | Contrat associe (si specifique a un contrat) |
| `project_id` | FK -> Project (nullable) | Projet associe (si specifique a un projet) |
| `is_active` | Boolean | Lieu actif/inactif (defaut : true) |
| `created_at` | DateTime | Date de creation |
| `updated_at` | DateTime | Date de derniere modification |

### Nouvel objet : WorkCode (Code de travail)

| Champ | Type | Description |
|---|---|---|
| `id` | UUID | Identifiant unique |
| `code` | String | Code court (ex : "DEFAULT", "CONC", "SUPV") |
| `name_fr` | String | Libelle en francais (ex : "Par defaut", "Conception", "Supervision") |
| `name_en` | String | Libelle en anglais (ex : "Default", "Design", "Supervision") |
| `description` | Text (nullable) | Description du code de travail |
| `is_system` | Boolean | Code systeme non supprimable (true pour "DEFAULT") |
| `billing_rate_multiplier` | Decimal(4,2) (nullable) | Multiplicateur de taux de facturation (ex : 1.00, 1.50 pour heures supplementaires) |
| `is_active` | Boolean | Code actif/inactif (defaut : true) |
| `sort_order` | Integer | Ordre d'affichage |
| `created_at` | DateTime | Date de creation |
| `updated_at` | DateTime | Date de derniere modification |

### Nouvel objet : ApprovalChain (Chaine d'approbation)

| Champ | Type | Description |
|---|---|---|
| `id` | UUID | Identifiant unique |
| `contract_id` | FK -> Contract | Contrat associe |
| `project_id` | FK -> Project (nullable) | Projet associe (si la chaine est specifique a un projet) |
| `approval_type` | Enum | Type : `time`, `expense` |
| `level` | Integer | Niveau dans la chaine (1, 2, ...) |
| `approver_id` | FK -> User | Approbateur a ce niveau |
| `delegate_id` | FK -> User (nullable) | Delegataire en cas d'absence |
| `escalation_delay_hours` | Integer | Delai d'escalade en heures ouvrees (defaut : 72) |
| `expense_approval_limit` | Decimal(10,2) (nullable) | Seuil de montant pour approbation depenses (applicable au type `expense` uniquement) |
| `is_active` | Boolean | Chaine active/inactive (defaut : true) |
| `created_at` | DateTime | Date de creation |
| `updated_at` | DateTime | Date de derniere modification |

### Modifications a l'objet TimeApproval

Le champ suivant est ajoute a l'objet `TimeApproval` existant (section 11) :

| Champ | Type | Description |
|---|---|---|
| `approval_level` | Integer | Niveau d'approbation dans la chaine (1 = N1, 2 = N2) |
| `is_escalated` | Boolean | Indique si l'action resulte d'une escalade automatique (defaut : false) |

---

## Criteres d'Acceptance Globaux supplementaires (Addendum)

| # | Critere |
|---|---|
| 16 | Les work locations sont fonctionnels : assignation par defaut depuis le contrat/projet, modification par entree de temps, affichage dans la grille et dans les exports. |
| 17 | Les work codes sont fonctionnels : code "Default" pre-selectionne, configuration par l'administrateur, assignation par entree de temps, affichage dans la grille et dans les exports. |
| 18 | La chaine d'approbation hierarchique est operationnelle : workflow Collaborateur -> N1 -> N2 fonctionnel pour les temps et les depenses. |
| 19 | L'escalade automatique fonctionne correctement : depassement du delai configurable declenche l'escalade au niveau superieur avec notifications. |
| 20 | Le seuil Expenses approval limit est respecte : les depenses sous le seuil peuvent etre approuvees au N1, celles au-dessus necessitent le N2. |
| 21 | La retrocompatibilite est assuree : les contrats/projets sans chaine d'approbation multi-niveaux fonctionnent avec l'approbation simple existante (US-CT-12). |
| 22 | Les statuts intermediaires d'approbation ("Approuvee N1 -- En attente N2") sont correctement affiches dans l'interface collaborateur et dans la vue d'approbation. |

---

## Estimation supplementaire (Addendum)

### Sprints supplementaires

| Sprint | User Stories | Perimetre | Duree estimee |
|---|---|---|---|
| **Sprint 8** | US-CT-17, US-CT-18 | Work locations + Work codes sur les entrees de temps | 2 semaines |
| **Sprint 9** | US-CT-19 | Chaine d'approbation hierarchique (Approval Chain) -- temps et depenses | 2.5 semaines |

### Impact sur l'estimation globale

| Indicateur | Valeur initiale | Valeur mise a jour |
|---|---|---|
| **Nombre de User Stories** | 16 | 19 |
| **Nombre de regles metier** | 18 (RG-01 a RG-18) | 26 (+ RM-CT-19 a RM-CT-26) |
| **Nombre de sprints** | 7 | 9 |
| **Duree totale estimee** | 14 a 16 semaines | 18.5 a 21 semaines |

### Priorite de livraison mise a jour

5. **V1.3 Work locations et Work codes (Sprint 8)** : Ajout des lieux de travail et codes de travail sur les entrees de temps. Necessite pour la conformite fiscale multi-provinces.
6. **V1.4 Chaine d'approbation (Sprint 9)** : Workflow d'approbation multi-niveaux. Necessite pour les contrats avec gouvernance avancee (ex : Place des Arts).
