# EPIC -- Audit ChangePoint : Module Gestion de Projets (Projects)

**Application concurrente auditee : Planview ChangePoint**
**URL : https://provencherroy.changepointasp.com/**
**Version du document : 1.0 -- Fevrier 2026**

---

## 1. Identification

| Champ | Valeur |
|---|---|
| **Nom de l'EPIC** | Gestion de Projets (Projects) -- Audit ChangePoint |
| **Reference** | EPIC-CP-PROJETS |
| **Module audite** | Projects (ChangePoint) |
| **Priorite** | Critique |
| **Auteur** | Architecte logiciel senior |
| **Date de creation** | 27 fevrier 2026 |
| **Version du document** | 1.0 |
| **Statut** | Brouillon |
| **Application cible** | Planview ChangePoint (instance Provencher Roy) |
| **Entites concernees** | Provencher_Roy Prod, PRAA |
| **Devise** | CAD |
| **EPICs OOTI lies** | EPIC-002 (Projets), EPIC-003 (Honoraires), EPIC-004 (Facturation), EPIC-005 (Temps), EPIC-006 (Planning), EPIC-010 (Clients), EPIC-016 (Configuration) |

---

## 2. Contexte et Justification

### 2.1 Contexte de l'audit

Le cabinet Provencher Roy utilise actuellement **Planview ChangePoint** comme outil central de gestion de projets (PSA -- Professional Services Automation). Le module Projects de ChangePoint constitue le pilier structurant de l'ensemble du systeme : il definit les projets, leur hierarchie WBS (Work Breakdown Structure), leurs proprietes financieres, et sert de reference pour tous les autres modules (feuilles de temps, contrats, facturation, planification). L'audit de ce module vise a identifier exhaustivement les fonctionnalites existantes, les flux utilisateur, les regles metier et les contraintes techniques afin de concevoir un module equivalent ou superieur dans l'application OOTI.

Le cabinet Provencher Roy opere avec **plusieurs entites juridiques** (Provencher_Roy Prod, PRAA -- Provencher Roy Associes architectes Inc.) ce qui implique une gestion multi-entites des projets avec des conventions de nommage, des regles de facturation et des structures WBS distinctes selon le type de projet. Le systeme heberge **3 types de projets** fondamentalement differents : des projets clients d'architecture (facturables), des projets administratifs internes et des projets departementaux de suivi du temps non facturable.

### 2.2 Problematique identifiee

L'interface actuelle de ChangePoint pour le module Projects presente plusieurs limites fonctionnelles et ergonomiques que l'application OOTI devra depasser :

- **Navigation entre vues fragmentee** : les 3 vues disponibles (Tree View, List View, Worksheet View) sont separees sans possibilite de basculement rapide ni de personnalisation avancee
- **Structure WBS limitee a 3-4 niveaux** : bien que ChangePoint supporte theoriquement jusqu'a 15-20 niveaux, l'instance observee ne va pas au-dela de 3 niveaux, suggerant des contraintes de configuration ou d'usage
- **Absence de templates WBS** : chaque projet doit etre structure manuellement, sans possibilite de reutiliser des modeles de structure pour des projets similaires (phases d'architecture recurrentes)
- **Numerotation WBS semi-manuelle** : la convention XX.Y (01.1, 01.2...) doit etre saisie manuellement dans le nom de la tache, sans renumerotation automatique en cas d'insertion ou de reorganisation
- **Filtres basiques en List View** : les filtres disponibles (Status, Billable, Entity) sont limites et ne permettent pas de recherches multi-criteres avancees
- **Pas de Gantt integre** : aucune vue chronologique de type Gantt n'est disponible directement dans le module Projects de cette instance
- **KPIs financiers statiques** : les indicateurs Revenue, Cost, Profit et Margin% sont affiches au niveau du profil projet mais sans tableaux de bord interactifs ni graphiques de tendance
- **Gestion des statuts binaire** : seuls deux statuts de projet sont observes (Active, Completed), sans workflow intermediaire (En attente, Suspendu, Archive, etc.)
- **Pas de drag & drop** : l'arborescence WBS ne supporte pas la reorganisation par glisser-deposer des taches entre niveaux

### 2.3 Justification strategique

L'application OOTI doit proposer un module Gestion de Projets qui :

1. **Reproduit fidelement** toutes les fonctionnalites essentielles de ChangePoint pour assurer une migration sans perte fonctionnelle, incluant les 3 types de projets, la structure WBS multi-niveaux et les 3 vues de navigation
2. **Ameliore l'ergonomie** de la navigation et de la creation de projets avec une interface moderne, des transitions fluides entre vues et un systeme de drag & drop pour la WBS
3. **Enrichit la structure WBS** avec des templates reutilisables, une numerotation automatique hierarchique et un nombre de niveaux configurable
4. **Offre une flexibilite superieure** en termes de gestion des statuts (workflow configurable), de conventions de nommage (generateur automatique) et de gestion multi-entites
5. **Ajoute des fonctionnalites manquantes** : vue Gantt integree, tableaux de bord financiers interactifs, templates de projets, recherche avancee multi-criteres, historique des modifications

---

## 3. Objectif de l'EPIC

Concevoir et specifier le module **Gestion de Projets** de l'application OOTI en s'appuyant sur l'audit exhaustif du module Projects de Planview ChangePoint. L'objectif est de garantir une **parite fonctionnelle complete** avec ChangePoint tout en apportant des ameliorations significatives en termes d'ergonomie, de flexibilite et de fonctionnalites complementaires.

Les objectifs specifiques sont :

- **Structure de projets** : supporter les 3 types de projets identifies (projets clients numerotes, projets administratifs, projets departementaux) avec leurs conventions de nommage respectives et leurs regles de facturation propres
- **Hierarchie WBS** : implementer une structure WBS multi-niveaux (minimum 4, recommande jusqu'a 6) avec numerotation automatique, distinction entre taches sommaires et taches feuilles, et support du drag & drop pour la reorganisation
- **Vues multiples** : reproduire les 3 vues de ChangePoint (Tree View, List View, Worksheet View) avec des ameliorations ergonomiques et une vue Gantt supplementaire
- **KPIs financiers** : afficher les indicateurs Revenue, Cost, Profit et Margin% au niveau projet avec des tableaux de bord interactifs et des graphiques de tendance
- **Integration contrats et facturation** : maintenir le lien structurant entre projets, contrats (Billing Roles & Rates) et factures (workflow 10 statuts)
- **Integration feuilles de temps** : les taches de projet doivent apparaitre comme assignments dans les feuilles de temps des collaborateurs assignes
- **Multi-entites** : supporter la gestion de projets repartis entre Provencher_Roy Prod et PRAA avec des regles de facturation et des bureaux de facturation distincts
- **Templates et automatisation** : offrir des modeles de structure WBS reutilisables et une numerotation automatique avec renumerotation en cas d'insertion

---

## 4. Perimetre Fonctionnel

| Ref | Fonctionnalite | Source ChangePoint | Statut OOTI | Priorite |
|---|---|---|---|---|
| PF-01 | Creation de projet (3 types : client, administratif, departemental) | Project creation | A reproduire | Critique |
| PF-02 | Proprietes du projet (Project Manager, Status, Customer, Billable, Entity, Currency) | Project properties | A reproduire | Critique |
| PF-03 | Structure WBS multi-niveaux (Projet > WBS/Phase > Tache > Sous-tache) | WBS hierarchy | A reproduire et etendre | Critique |
| PF-04 | Numerotation WBS hierarchique (XX.Y.Z) | Manual WBS numbering | A reproduire et automatiser | Haute |
| PF-05 | Tree View (arborescence hierarchique expandable) | Tree View | A reproduire | Critique |
| PF-06 | List View (liste plate avec colonnes triables et filtrables) | List View | A reproduire | Critique |
| PF-07 | Worksheet View (grille tableur editable) | Worksheet View | A reproduire | Haute |
| PF-08 | Filtres et recherche (Quick filter, Status, Billable, Entity) | List View filters | A reproduire et etendre | Haute |
| PF-09 | Profil de projet et KPIs (Revenue, Cost, Profit, Margin%) | Project Profile | A reproduire | Critique |
| PF-10 | Gestion des statuts (Active, Completed + workflow etendu) | Project status | A reproduire et etendre | Haute |
| PF-11 | Flag Billable (Oui/Non) avec impact sur facturation | Billable toggle | A reproduire | Critique |
| PF-12 | Multi-entites (Provencher_Roy Prod, PRAA) | Entity management | A reproduire | Critique |
| PF-13 | Lien avec les contrats (Billing Roles & Rates) | Contract link | A reproduire | Critique |
| PF-14 | Lien avec la facturation (generation et suivi des factures) | Invoice link | A reproduire | Haute |
| PF-15 | Assignments (lien avec les feuilles de temps) | Time Sheet assignments | A reproduire | Critique |
| PF-16 | Recently viewed (projets recemment consultes) | Recently viewed section | A reproduire | Moyenne |
| PF-17 | Icones et indicateurs visuels (type, facturabilite, statut) | Visual icons | A reproduire | Haute |
| PF-18 | Options Tree View (Expand/Collapse all, Select all, Show levels) | Tree View options | A reproduire | Moyenne |
| PF-19 | Export et impression des donnees projet | Non explore en detail | A ajouter | Moyenne |
| PF-20 | Templates de structure WBS | Non present dans ChangePoint | A ajouter | Haute |
| PF-21 | Vue Gantt integree | Non present dans cette instance | A ajouter | Haute |
| PF-22 | Drag & drop dans l'arborescence WBS | Non present dans ChangePoint | A ajouter | Moyenne |
| PF-23 | Historique des modifications (audit trail) | Non explore en detail | A ajouter | Moyenne |
| PF-24 | Configuration et parametrage du module | Admin settings | A reproduire | Haute |

---

## 5. User Stories detaillees

---

### US-CP-01 -- Creation d'un projet client numerote

**En tant que** chef de projet ou directeur
**Je veux** creer un nouveau projet client avec un numero sequentiel automatique et les proprietes requises
**Afin de** initialiser le suivi d'un nouveau mandat d'architecture dans le systeme avec toutes les informations de reference

| # | Critere d'acceptation |
|---|---|
| 1 | Un formulaire de creation de projet est accessible via un bouton "Nouveau projet" visible dans la barre d'outils du module Projects |
| 2 | Le numero de projet est genere automatiquement selon la convention `AANNNN` (2 chiffres annee + 4 chiffres sequentiels, ex : 250030) ; l'utilisateur peut le modifier avant la creation |
| 3 | Les champs obligatoires du formulaire incluent : Nom du projet, Numero de projet, Type de projet (Client), Customer (liste deroulante des clients existants), Project Manager (liste deroulante des collaborateurs), Entity (Provencher_Roy Prod ou PRAA), Billing Office, Currency (defaut CAD) |
| 4 | Le champ "Billable" est un booleen (Oui/Non) avec la valeur par defaut "Oui" pour les projets de type Client |
| 5 | Le statut initial du projet est "Active" par defaut |
| 6 | Le prefixe d'entite est automatiquement ajoute au nom du projet selon la convention observee (ex : "[PRA]" pour Provencher_Roy Prod) |
| 7 | A la creation, le projet apparait immediatement dans la Tree View, la List View et la Worksheet View |
| 8 | Le systeme verifie l'unicite du numero de projet ; un message d'erreur est affiche si le numero existe deja |
| 9 | Le formulaire propose un champ optionnel "Description" pour decrire le mandat client |
| 10 | Un projet cree est automatiquement ajoute a la section "Recently viewed" de l'utilisateur createur |

---

### US-CP-02 -- Creation d'un projet administratif

**En tant que** administrateur ou directeur
**Je veux** creer un projet administratif avec la convention de nommage "Admin-XX"
**Afin de** mettre en place un projet de suivi des couts internes (administration, conges RH, coordination) sans lien avec un mandat client

| # | Critere d'acceptation |
|---|---|
| 1 | Le formulaire de creation propose le type de projet "Administratif" dans la liste deroulante des types |
| 2 | Le numero de projet est genere automatiquement selon la convention `Admin-NN` (ex : Admin-12) avec un numero sequentiel a 2 chiffres |
| 3 | Le champ "Customer" est optionnel pour les projets administratifs (pas de client associe obligatoire) |
| 4 | Le champ "Billable" est positionne a "Oui" par defaut pour les projets administratifs (coherence ChangePoint : suivi des couts internes refactures) mais modifiable |
| 5 | L'entite de rattachement est obligatoire (Provencher_Roy Prod ou PRAA) |
| 6 | La structure WBS par defaut est simplifiee : le projet est cree avec une tache sommaire racine portant le nom du projet |
| 7 | Les projets administratifs sont visuellement distingues dans les vues List et Tree par une icone ou un badge specifique |
| 8 | Les KPIs financiers du projet administratif affichent uniquement le "Cost" (pas de Revenue ni de Profit pour les projets non lies a un contrat client) |
| 9 | Le projet administratif peut etre associe a un contrat de maniere optionnelle (pour le suivi des taux de couts internes) |
| 10 | Un projet administratif peut etre cree a partir d'un modele de projet administratif existant (copie de structure) |

---

### US-CP-03 -- Creation d'un projet departemental

**En tant que** administrateur ou responsable RH
**Je veux** creer un projet departemental non facturable avec la convention "PRAA - Nom du departement"
**Afin de** mettre en place un conteneur permanent pour le suivi du temps des fonctions support (administration generale, comptabilite, RH, TI)

| # | Critere d'acceptation |
|---|---|
| 1 | Le formulaire de creation propose le type de projet "Departemental" dans la liste deroulante des types |
| 2 | Le nom du projet suit la convention `PRAA - [Nom du departement]` avec suggestion automatique du prefixe d'entite |
| 3 | Le champ "Billable" est automatiquement positionne a "Non" et non modifiable pour les projets departementaux |
| 4 | Le statut initial est "Active" ; les projets departementaux sont consideres comme permanents (pas de date de fin obligatoire) |
| 5 | La structure WBS par defaut inclut des taches generiques : Rencontres/Meetings, Formation/Coaching, Autres/Others |
| 6 | Aucun contrat ni aucune facture ne peut etre associe a un projet departemental (les menus de liaison contrat/facture sont desactives) |
| 7 | Les projets departementaux sont affiches avec une icone rouge/barree dans les vues pour indiquer visuellement leur caractere non facturable |
| 8 | Les KPIs financiers affichent uniquement les heures consommees (pas de Revenue, Cost, Profit, Margin%) |
| 9 | Les taches des projets departementaux sont disponibles comme assignments dans le module Feuilles de Temps pour tous les collaborateurs de l'entite |
| 10 | Un projet departemental ne peut pas etre supprime s'il contient des heures saisies (protection des donnees historiques) |

---

### US-CP-04 -- Structure WBS multi-niveaux (ajout, modification, suppression)

**En tant que** chef de projet
**Je veux** creer et gerer une structure WBS hierarchique a plusieurs niveaux pour un projet
**Afin de** decomposer le mandat en phases, taches sommaires et taches de detail pour le suivi de l'avancement et la saisie du temps

| # | Critere d'acceptation |
|---|---|
| 1 | La structure WBS supporte un minimum de 4 niveaux hierarchiques : Niveau 1 (Projet), Niveau 2 (Phase/WBS summary), Niveau 3 (Tache), Niveau 4 (Sous-tache) ; et jusqu'a 6 niveaux maximum configurables |
| 2 | L'ajout d'un element WBS (phase, tache, sous-tache) se fait via un bouton "+" contextuel ou un clic droit dans la Tree View, avec choix du niveau d'insertion (enfant ou frere) |
| 3 | La numerotation WBS est generee automatiquement selon la convention hierarchique `XX.Y.Z` (ex : 01.1, 01.2, 02.1.1) et se renumerote automatiquement en cas d'insertion ou de suppression |
| 4 | Chaque element WBS possede les proprietes : Nom (obligatoire), Description (optionnel), Type (tache sommaire ou tache feuille), Statut, Date de debut, Date de fin, Effort planifie (heures), Responsable assigne |
| 5 | Les taches sommaires (niveaux intermediaires) ne peuvent pas recevoir de saisie de temps directe ; seules les taches feuilles (niveau le plus bas) sont assignables dans les feuilles de temps |
| 6 | La suppression d'un element WBS affiche une confirmation et n'est possible que si aucune heure n'a ete saisie sur l'element ou ses enfants |
| 7 | La modification du nom, de la description et des dates d'un element WBS est possible en edition inline directement dans la Tree View ou via un panneau de detail |
| 8 | Le deplacement d'un element WBS (changement de parent, changement d'ordre) est possible par drag & drop dans la Tree View avec renumerotation automatique |
| 9 | Chaque type d'element WBS est identifie par une icone distincte : icone bleue livre (projet), icone document avec checkmark (tache sommaire), icone document vert (tache feuille) |
| 10 | Les totaux des taches sommaires (heures planifiees, heures consommees, pourcentage d'avancement) sont calcules automatiquement a partir de la somme des taches enfants |

---

### US-CP-05 -- Navigation Tree View (arborescence hierarchique)

**En tant que** chef de projet ou collaborateur
**Je veux** naviguer dans l'arborescence hierarchique des projets et de leurs taches via une Tree View expandable
**Afin de** visualiser la structure complete d'un projet, explorer ses niveaux de detail et acceder rapidement aux taches recherchees

| # | Critere d'acceptation |
|---|---|
| 1 | La Tree View affiche tous les projets sous forme d'arborescence hierarchique avec des fleches d'expansion (triangle) pour chaque element ayant des enfants |
| 2 | Un clic sur la fleche d'expansion ouvre le niveau suivant ; un second clic le referme (comportement toggle) |
| 3 | Les options suivantes sont disponibles dans une barre d'outils dediee : "Expand all" (ouvrir tous les niveaux), "Collapse all" (fermer tous les niveaux), "Select all" (selectionner tous les elements visibles), "Clear all" (deselectionner tout) |
| 4 | Les options avancees sont disponibles : "Expand levels with selections" (ouvrir les niveaux contenant des elements selectionnes), "Collapse levels with no selections" (fermer les niveaux sans selection), "Show main levels only" (afficher uniquement les niveaux 1 et 2), "Show sublevels only" (afficher uniquement les niveaux 3+), "Show all levels" (afficher tous les niveaux) |
| 5 | Une section "Recently viewed" est affichee en haut de la Tree View, listant les 5 a 10 derniers projets consultes par l'utilisateur |
| 6 | Un clic sur le nom d'un projet ou d'une tache ouvre le detail (profil) de cet element dans un panneau lateral ou une page dediee |
| 7 | L'indentation visuelle reflette le niveau hierarchique : chaque niveau est decale de 20px par rapport a son parent |
| 8 | Chaque element affiche son icone de type (livre bleu, document checkmark, document vert, rouge/barre), son numero WBS et son nom |
| 9 | La Tree View supporte la selection multiple via des cases a cocher pour permettre des actions groupees (suppression, export, changement de statut) |
| 10 | La Tree View est scrollable verticalement et conserve la position de scroll lors de l'expansion/reduction des niveaux |

---

### US-CP-06 -- Navigation List View (liste plate triable et filtrable)

**En tant que** chef de projet, directeur ou administrateur
**Je veux** visualiser la liste de tous les projets sous forme de tableau avec des colonnes triables et des filtres
**Afin de** rechercher rapidement des projets, les trier selon differents criteres et avoir une vue d'ensemble de mon portefeuille de projets

| # | Critere d'acceptation |
|---|---|
| 1 | La List View affiche un tableau avec les colonnes suivantes : Project (nom + numero), Customer, Status, Billable (oui/non), Entity, Project Manager, et un bouton d'action (detail) |
| 2 | Chaque en-tete de colonne est cliquable pour trier la liste en ordre croissant ou decroissant (tri alphabetique pour les textes, tri logique pour les statuts) |
| 3 | Un champ de filtre rapide (Quick filter) avec support du caractere wildcard "%" permet de rechercher un projet par nom ou numero (ex : "250%" affiche tous les projets commencant par 250) |
| 4 | Un filtre "Status" (liste deroulante) permet de filtrer par statut : Active, Completed, All |
| 5 | Un filtre "Billable" (liste deroulante) permet de filtrer par facturabilite : Yes, No, All |
| 6 | Un filtre "Entity" (liste deroulante) permet de filtrer par entite : Provencher_Roy Prod, PRAA, All |
| 7 | Les filtres sont combinables : l'application de plusieurs filtres produit un AND logique (ex : Status=Active ET Billable=Yes ET Entity=PRAA) |
| 8 | Le nombre total de resultats est affiche en haut ou en bas de la liste (ex : "42 projets affiches sur 156") |
| 9 | Un clic sur le nom d'un projet dans la liste ouvre le detail du projet (profil/proprietes) |
| 10 | La liste supporte la pagination ou le scroll infini pour les portefeuilles de grande taille (100+ projets) |

---

### US-CP-07 -- Worksheet View (grille tableur editable)

**En tant que** chef de projet ou administrateur
**Je veux** visualiser et editer les proprietes de mes projets et taches dans une grille de type tableur
**Afin de** modifier en masse les informations de plusieurs projets ou taches sans ouvrir chaque fiche individuellement

| # | Critere d'acceptation |
|---|---|
| 1 | La Worksheet View affiche une grille avec des lignes representant les projets/taches et des colonnes representant les proprietes editables |
| 2 | Les colonnes affichees incluent au minimum : Nom, Numero WBS, Status, Billable, Entity, Project Manager, Date debut, Date fin, Effort planifie, Heures consommees, Budget |
| 3 | Les cellules editables permettent la modification directe (inline editing) par un double-clic ou un clic direct selon le type de champ (texte, liste deroulante, date, nombre) |
| 4 | Les modifications sont sauvegardees automatiquement a la sortie de la cellule (auto-save) avec un indicateur visuel de sauvegarde |
| 5 | Les colonnes sont redimensionnables par drag & drop sur les bordures d'en-tete |
| 6 | Les colonnes sont triables par un clic sur l'en-tete (tri croissant / decroissant) |
| 7 | La grille supporte le copier-coller (Ctrl+C / Ctrl+V) pour les cellules editables |
| 8 | Un indicateur visuel distingue les cellules modifiees (fond surligne) jusqu'a la prochaine sauvegarde |
| 9 | Les lignes de la grille respectent la hierarchie WBS avec indentation visuelle (identique a la Tree View) |
| 10 | L'affichage des colonnes est personnalisable : l'utilisateur peut masquer ou afficher des colonnes via un menu de configuration |

---

### US-CP-08 -- Profil de projet et KPIs financiers

**En tant que** chef de projet ou directeur financier
**Je veux** consulter le profil detaille d'un projet avec ses indicateurs de performance financiere (KPIs)
**Afin de** suivre la sante financiere du projet en temps reel et prendre des decisions eclairees sur l'allocation des ressources

| # | Critere d'acceptation |
|---|---|
| 1 | Le profil de projet est accessible par un clic sur le nom du projet dans n'importe quelle vue (Tree, List, Worksheet) |
| 2 | Le profil affiche les proprietes generales du projet : Nom, Numero, Type, Customer, Project Manager, Entity, Billing Office, Currency, Status, Billable, dates de debut et de fin |
| 3 | Une section "KPIs financiers" affiche les 4 indicateurs principaux : Revenue (revenus generes = heures x taux de facturation), Cost (couts engages = heures x taux de cout interne), Profit (benefice = Revenue - Cost), Margin% (marge = Profit / Revenue x 100) |
| 4 | Les KPIs sont calcules en temps reel a partir des heures saisies dans les feuilles de temps et des taux definis dans le contrat associe |
| 5 | Pour les projets non facturables (Billable = Non), seuls les KPIs Cost et Heures consommees sont affiches (Revenue, Profit et Margin% ne sont pas pertinents) |
| 6 | Une section "Structure WBS" affiche l'arborescence des taches du projet avec pour chaque tache : heures planifiees, heures consommees, pourcentage d'avancement |
| 7 | Une section "Contrat associe" affiche le lien vers le contrat du projet avec un resume des Billing Roles & Rates (role, taux standard, remise, taux effectif) |
| 8 | Une section "Equipe projet" affiche la liste des collaborateurs assignes au projet avec leur role et leur charge planifiee |
| 9 | Les KPIs sont affiches dans la devise du projet (CAD par defaut) avec possibilite de conversion dans une autre devise |
| 10 | Un graphique de type barre ou jauge compare visuellement le budget consomme vs le budget planifie pour chaque KPI |

---

### US-CP-09 -- Gestion des statuts de projet

**En tant que** chef de projet ou directeur
**Je veux** gerer le cycle de vie d'un projet via un systeme de statuts configurable
**Afin de** suivre l'avancement du projet depuis sa creation jusqu'a sa cloture et controler les actions autorisees a chaque etape

| # | Critere d'acceptation |
|---|---|
| 1 | Le systeme propose un workflow de statuts par defaut avec au minimum : Proposed (propose), Active (actif), On Hold (suspendu), Completed (termine), Archived (archive) |
| 2 | Le statut initial d'un nouveau projet est "Proposed" ou "Active" selon le type de projet (Active par defaut pour les projets departementaux permanents) |
| 3 | Les transitions de statut autorisees sont definies dans un workflow configurable : Proposed -> Active, Active -> On Hold, Active -> Completed, On Hold -> Active, Completed -> Archived |
| 4 | Le changement de statut est effectue via un menu deroulant dans les proprietes du projet ou via la Worksheet View |
| 5 | Le passage au statut "Completed" verifie des conditions prealables : toutes les taches doivent etre terminees ou annulees, aucune heure non soumise ne doit rester en attente |
| 6 | Le passage au statut "Archived" verrouille le projet en lecture seule : aucune modification des proprietes, de la structure WBS, ni saisie de temps n'est autorisee |
| 7 | Un indicateur visuel (badge, couleur) dans les vues List et Tree reflete le statut courant du projet |
| 8 | L'historique des changements de statut est conserve avec la date, l'auteur et un commentaire optionnel |
| 9 | Les filtres des vues List et Tree permettent de filtrer par statut (coherence avec les filtres ChangePoint : Active, Completed, et filtres etendus) |
| 10 | Le statut d'un projet departemental ne peut pas etre change en "Completed" ou "Archived" tant que le projet est utilise comme conteneur de temps actif |

---

### US-CP-10 -- Gestion du flag Billable (facturabilite)

**En tant que** chef de projet ou directeur financier
**Je veux** definir et modifier le caractere facturable ou non facturable d'un projet
**Afin de** determiner si les heures saisies sur ce projet generent des revenus facturables et impactent les KPIs financiers

| # | Critere d'acceptation |
|---|---|
| 1 | Chaque projet dispose d'un champ "Billable" de type booleen (Oui/Non) accessible dans les proprietes du projet et dans la Worksheet View |
| 2 | La valeur par defaut du champ Billable depend du type de projet : Oui pour les projets clients et administratifs, Non pour les projets departementaux |
| 3 | La modification du flag Billable d'un projet en cours (de Oui a Non ou inversement) affiche un avertissement indiquant l'impact sur les KPIs financiers et la facturation |
| 4 | Un projet marque comme non facturable est affiche avec une icone rouge/barree dans les vues Tree et List pour une identification visuelle immediate |
| 5 | Un projet marque comme facturable est affiche avec une icone bleue standard |
| 6 | Le flag Billable se propage aux taches enfants : toutes les taches d'un projet non facturable sont automatiquement non facturables |
| 7 | Les heures saisies sur un projet non facturable n'apparaissent pas dans le calcul du Revenue au niveau du portefeuille |
| 8 | Le filtre "Billable" de la List View permet de filtrer rapidement les projets facturables vs non facturables |
| 9 | Un projet non facturable ne peut pas etre associe a un contrat de facturation client (les menus de liaison contrat sont desactives) |
| 10 | Le flag Billable est audite : tout changement est trace dans l'historique des modifications avec la date, l'auteur et l'ancienne/nouvelle valeur |

---

### US-CP-11 -- Filtres et recherche avancee

**En tant que** utilisateur du module Projects (chef de projet, directeur, collaborateur)
**Je veux** filtrer et rechercher des projets selon des criteres multiples et combines
**Afin de** trouver rapidement les projets qui m'interessent dans un portefeuille potentiellement volumineux

| # | Critere d'acceptation |
|---|---|
| 1 | Un champ de recherche rapide (Quick filter) est accessible en permanence en haut de la List View et de la Tree View |
| 2 | Le Quick filter supporte le caractere wildcard "%" pour des recherches partielles (ex : "250%" pour trouver tous les projets de l'annee 2025, "%Architecture%" pour trouver les projets contenant le mot "Architecture") |
| 3 | La recherche s'effectue en temps reel (filtrage au fur et a mesure de la saisie) apres un delai de debounce de 300ms |
| 4 | Les filtres disponibles en List View incluent : Status (Active, Completed, On Hold, Archived, All), Billable (Yes, No, All), Entity (Provencher_Roy Prod, PRAA, All), Project Manager (liste des chefs de projet), Customer (liste des clients), Type de projet (Client, Administratif, Departemental) |
| 5 | Les filtres sont combinables avec un AND logique ; le nombre de resultats est mis a jour en temps reel |
| 6 | Les filtres actifs sont affiches sous forme de "tags" cliquables au-dessus de la liste, permettant de supprimer un filtre individuellement |
| 7 | Les combinaisons de filtres frequentes peuvent etre sauvegardees en tant que "vue personnalisee" par l'utilisateur |
| 8 | Un bouton "Reinitialiser les filtres" supprime tous les filtres actifs et affiche l'ensemble des projets |
| 9 | La recherche couvre le nom du projet, le numero du projet, le nom du client et le nom du chef de projet |
| 10 | Les resultats de recherche sont surlignees dans la liste pour identifier visuellement les correspondances |

---

### US-CP-12 -- Gestion multi-entites

**En tant que** administrateur ou directeur
**Je veux** gerer des projets repartis entre plusieurs entites juridiques (Provencher_Roy Prod, PRAA)
**Afin de** assurer la separation comptable et la traçabilite financiere entre les differentes entites du cabinet

| # | Critere d'acceptation |
|---|---|
| 1 | Chaque projet est obligatoirement rattache a une entite juridique (Provencher_Roy Prod ou PRAA) |
| 2 | L'entite du projet determine le bureau de facturation (Billing Office), les taux de facturation et les regles comptables applicables |
| 3 | Un filtre "Entity" est disponible dans toutes les vues (Tree, List, Worksheet) pour isoler les projets d'une entite specifique |
| 4 | Les KPIs financiers sont calculables par entite : somme des Revenue, Cost, Profit et Margin% pour tous les projets d'une meme entite |
| 5 | Un collaborateur rattache a une entite peut etre assigne a des projets d'une autre entite (gestion inter-entites, coherence avec le projet intercompagnie 130094) |
| 6 | Les factures generees depuis un projet portent automatiquement les informations de l'entite de rattachement (raison sociale, adresse, coordonnees bancaires) |
| 7 | Le prefixe d'entite dans le nom du projet (ex : "[PRA]") est automatiquement gere par le systeme a la creation |
| 8 | Un rapport de synthese multi-entites permet de comparer les performances financieres entre Provencher_Roy Prod et PRAA |
| 9 | Les droits d'acces aux projets peuvent etre restreints par entite (un utilisateur PRAA ne voit par defaut que les projets PRAA, sauf autorisation explicite) |
| 10 | La devise de facturation est definie au niveau de l'entite (CAD par defaut) mais peut etre surchargee au niveau du contrat de projet |

---

### US-CP-13 -- Lien avec les contrats (Billing Roles & Rates)

**En tant que** chef de projet ou directeur financier
**Je veux** associer un contrat a un projet facturable et definir les roles de facturation et les taux applicables
**Afin de** etablir les conditions financieres du mandat et permettre la generation de factures basees sur les heures saisies

| # | Critere d'acceptation |
|---|---|
| 1 | Un projet facturable (Billable = Oui) peut etre associe a un contrat via un lien dans le profil du projet ou un menu "Contrat associe" |
| 2 | Le contrat contient un sous-module "Billing Roles & Rates" qui definit pour chaque role : le nom du role (ex : Architecte, Designer, Technicien), le taux standard (Standard Rate en CAD), le pourcentage de remise (Discount %), le taux de facturation effectif (Billing Rate = Standard Rate x (1 - Discount%)), la devise de facturation (Billing Currency) |
| 3 | Le taux de facturation effectif est calcule automatiquement a la saisie du taux standard et de la remise (ex : 150.00 CAD x (1 - 10%) = 135.00 CAD) |
| 4 | Plusieurs roles de facturation peuvent etre definis dans un meme contrat (au minimum : Architecte, Designer, Technicien, Stagiaire, Directeur) |
| 5 | Le contrat porte les informations generales : nom du contrat, client associe, bureau de facturation, devise, entite juridique |
| 6 | Le lien entre le contrat et le projet est affiche dans le profil du projet avec un lien cliquable vers les details du contrat |
| 7 | Les KPIs Revenue du projet sont calcules a partir des heures saisies par chaque collaborateur multipliees par le taux de facturation de son role dans le contrat |
| 8 | La modification des taux dans le contrat recalcule automatiquement les KPIs Revenue du projet associe |
| 9 | Un projet facturable sans contrat associe affiche un avertissement "Contrat manquant -- facturation impossible" dans le profil du projet |
| 10 | Un contrat peut etre partage entre plusieurs projets du meme client (contrat-cadre) |

---

### US-CP-14 -- Lien avec la facturation

**En tant que** chef de projet ou responsable de facturation
**Je veux** acceder aux factures liees a un projet et suivre leur progression dans le workflow de facturation
**Afin de** controler le flux de facturation du projet et m'assurer que les factures sont emises et reglees en temps voulu

| # | Critere d'acceptation |
|---|---|
| 1 | Le profil de projet affiche une section "Factures" listant toutes les factures associees avec les colonnes : numero de facture, date, montant, statut, lien vers le detail |
| 2 | Le workflow de facturation comporte 10 statuts affiches avec un indicateur visuel (couleur ou badge) : Draft, Pending Approval, Pending Second Approval, Approved, Committed, Sent, Paid, Partially Paid, Credited, Archived |
| 3 | Un lien "Creer une facture" dans le profil du projet permet de lancer la creation d'une nouvelle facture (brouillon) basee sur les heures approuvees non encore facturees |
| 4 | Le montant total facture et le montant total encaisse sont affiches dans les KPIs du projet |
| 5 | Le profil de projet affiche un indicateur "Montant a facturer" correspondant aux heures approuvees non encore incluses dans une facture |
| 6 | Le clic sur une facture dans la liste ouvre le detail de la facture dans le module Facturation (EPIC-004) |
| 7 | Les factures au statut "Credited" (avoir) sont affichees distinctement (couleur differente) et soustraites du total facture |
| 8 | Un historique chronologique des factures du projet est consultable avec les transitions de statut |
| 9 | La double approbation des factures est supportee pour les projets depassant un seuil de montant configurable |
| 10 | Les projets non facturables (Billable = Non) n'affichent pas la section "Factures" dans le profil |

---

### US-CP-15 -- Assignments (lien avec les feuilles de temps)

**En tant que** chef de projet
**Je veux** assigner des collaborateurs aux taches de mon projet pour qu'ils puissent saisir leurs heures via le module Feuilles de Temps
**Afin de** controler qui peut declarer du temps sur chaque tache et suivre la consommation des heures planifiees

| # | Critere d'acceptation |
|---|---|
| 1 | Chaque tache feuille (niveau le plus bas de la WBS) peut etre assignee a un ou plusieurs collaborateurs via un panneau d'assignation |
| 2 | L'assignation d'un collaborateur a une tache fait apparaitre cette tache dans sa feuille de temps (module Time Sheet) comme ligne de saisie disponible |
| 3 | La desassignation d'un collaborateur d'une tache retire cette tache de sa feuille de temps (si aucune heure n'a ete saisie ; sinon, un avertissement est affiche) |
| 4 | Le panneau d'assignation affiche la liste des collaborateurs disponibles avec filtre par nom, entite et role |
| 5 | L'assignation en masse est possible : un meme collaborateur peut etre assigne a plusieurs taches simultanement via une selection multiple |
| 6 | Pour chaque assignation, l'effort planifie (heures prevues) peut etre defini pour la tache et le collaborateur |
| 7 | Le profil de la tache affiche la liste des collaborateurs assignes avec les heures planifiees vs heures consommees pour chacun |
| 8 | Un collaborateur assigne a une tache de projet departemental (PRAA) voit cette tache dans sa feuille de temps comme un temps non-projet |
| 9 | Les taches sommaires (niveaux intermediaires) ne sont pas directement assignables ; seules les taches feuilles le sont |
| 10 | La suppression d'une assignation est tracee dans l'historique des modifications du projet |

---

### US-CP-16 -- Section "Recently viewed" (projets recemment consultes)

**En tant que** utilisateur du module Projects
**Je veux** acceder rapidement aux derniers projets que j'ai consultes via une section "Recently viewed"
**Afin de** retrouver instantanement les projets sur lesquels je travaille sans avoir a naviguer dans l'arborescence ou a utiliser les filtres

| # | Critere d'acceptation |
|---|---|
| 1 | Une section "Recently viewed" est affichee en haut de la Tree View, au-dessus de l'arborescence complete |
| 2 | La section affiche les 5 a 10 derniers projets consultes par l'utilisateur, tries par date de consultation decroissante (le plus recent en premier) |
| 3 | Chaque entree de la section affiche le nom du projet, son numero et son icone de type |
| 4 | Un clic sur une entree de la section "Recently viewed" ouvre directement le profil du projet |
| 5 | La liste est specifique a chaque utilisateur (les projets recemment consultes par un utilisateur A ne sont pas visibles par un utilisateur B) |
| 6 | La consultation d'un projet (ouverture de son profil) ajoute automatiquement ce projet en tete de la liste "Recently viewed" |
| 7 | Si un projet est deja present dans la liste, sa consultation le remonte en premiere position sans creer de doublon |
| 8 | La section "Recently viewed" peut etre reduite (collapse) par l'utilisateur pour liberer de l'espace vertical dans la Tree View |
| 9 | Les projets archives ou supprimes sont automatiquement retires de la liste "Recently viewed" |
| 10 | La liste est persistee cote serveur et restauree a chaque reconnexion de l'utilisateur |

---

### US-CP-17 -- Export et impression

**En tant que** chef de projet ou directeur
**Je veux** exporter les donnees de mes projets (liste, structure WBS, KPIs) et imprimer des rapports de projet
**Afin de** partager les informations projet avec des parties prenantes externes (clients, partenaires) ou archiver des documents de reference

| # | Critere d'acceptation |
|---|---|
| 1 | Un bouton "Exporter" est disponible dans les vues List View et Worksheet View |
| 2 | Les formats d'export disponibles incluent : CSV (donnees tabulaires), Excel (XLSX avec mise en forme), PDF (rapport formate avec en-tete et logo de l'entite) |
| 3 | L'export CSV/Excel de la List View exporte toutes les colonnes affichees avec les filtres actuellement appliques |
| 4 | L'export PDF du profil projet genere un document contenant : les proprietes du projet, la structure WBS, les KPIs financiers, la liste de l'equipe projet, le resume des factures |
| 5 | L'export de la structure WBS est disponible au format PDF avec indentation visuelle refletant la hierarchie |
| 6 | La fonction d'impression utilise un layout d'impression optimise (CSS print) avec en-tete de page, pied de page et mise en page paysage pour les tableaux larges |
| 7 | L'export respecte les droits d'acces : seules les donnees accessibles a l'utilisateur sont incluses dans l'export |
| 8 | Un indicateur de progression est affiche pendant la generation de l'export pour les portefeuilles volumineux |
| 9 | Le nom du fichier exporte suit une convention : `[Entity]_[ProjectNumber]_[ProjectName]_[Date].[Extension]` |
| 10 | L'export multi-projets est possible : l'utilisateur peut selectionner plusieurs projets dans la List View et exporter un rapport consolide |

---

### US-CP-18 -- Templates de structure WBS

**En tant que** chef de projet ou administrateur
**Je veux** creer et utiliser des modeles de structure WBS reutilisables
**Afin de** accelerer la creation de nouveaux projets en appliquant des structures predefinies adaptees aux differents types de mandats d'architecture

| # | Critere d'acceptation |
|---|---|
| 1 | Un catalogue de templates WBS est accessible depuis le formulaire de creation de projet et depuis un menu de configuration dedie |
| 2 | La creation d'un template se fait a partir d'un projet existant : l'utilisateur peut selectionner un projet et "Sauvegarder comme template" pour copier sa structure WBS (sans les donnees de temps et de facturation) |
| 3 | Un template WBS comprend : un nom, une description, le type de projet cible (Client, Administratif, Departemental), la structure hierarchique complete (phases, taches, sous-taches) avec leur numerotation |
| 4 | Lors de la creation d'un nouveau projet, l'utilisateur peut selectionner un template dans une liste deroulante ; la structure WBS du template est automatiquement dupliquee dans le nouveau projet |
| 5 | Les templates peuvent etre modifies (ajout/suppression de niveaux, renommage des taches) sans impacter les projets deja crees a partir de ce template |
| 6 | Des templates par defaut sont fournis pour les types de projets courants d'un cabinet d'architecture (ex : Phases typiques : Programmation, Concept, Preliminaire, Definitif, Plans et devis, Surveillance de chantier) |
| 7 | Un template peut etre partage entre toutes les entites ou restreint a une entite specifique |
| 8 | La gestion des templates (creation, modification, suppression, activation/desactivation) est reservee aux utilisateurs ayant le role administrateur ou chef de projet senior |
| 9 | Le nombre de templates est illimite |
| 10 | L'application d'un template a un projet existant propose deux options : "Remplacer" (supprimer la structure existante) ou "Fusionner" (ajouter les taches du template a la structure existante) |

---

### US-CP-19 -- Configuration et parametrage du module Projects

**En tant que** administrateur systeme
**Je veux** configurer les parametres du module Projects (types de projets, conventions de nommage, workflow de statuts, niveaux WBS)
**Afin de** adapter le module aux besoins specifiques du cabinet et garantir la coherence des donnees saisies

| # | Critere d'acceptation |
|---|---|
| 1 | Un ecran de configuration du module Projects est accessible aux administrateurs depuis un menu "Parametres > Projets" |
| 2 | La configuration des types de projet permet de definir : les types disponibles (Client, Administratif, Departemental + types personnalises), la convention de nommage par type (AANNNN, Admin-NN, PRAA - Xxx), les champs obligatoires par type, les valeurs par defaut par type (Billable, Entity, Status) |
| 3 | La configuration du workflow de statuts permet de definir : les statuts disponibles et leur ordre, les transitions autorisees entre statuts, les conditions de transition (ex : toutes les taches doivent etre terminees pour passer en "Completed"), les actions declenchees par une transition (ex : notification, verrouillage) |
| 4 | La configuration WBS permet de definir : le nombre maximum de niveaux hierarchiques (entre 3 et 10), le format de numerotation (XX.Y.Z, auto-increment, libre), le caractere separateur de niveaux (".", "-", "/") |
| 5 | La configuration des entites permet de definir : les entites disponibles (Provencher_Roy Prod, PRAA + extensible), le bureau de facturation par entite, la devise par defaut par entite, le prefixe de nom de projet par entite |
| 6 | La configuration des icones permet d'associer une icone et une couleur a chaque type de projet et a chaque statut |
| 7 | La configuration des champs personnalises permet d'ajouter des champs supplementaires aux proprietes du projet (texte, nombre, date, liste deroulante, case a cocher) |
| 8 | Les modifications de configuration sont appliquees immediatement aux nouvelles creations de projet ; les projets existants ne sont pas impactes retroactivement sauf demande explicite |
| 9 | Un journal d'audit trace toutes les modifications de configuration avec la date, l'auteur et les valeurs avant/apres |
| 10 | La configuration peut etre exportee et importee (format JSON ou YAML) pour faciliter la migration entre environnements (dev, recette, production) |

---

## 6. Hors Perimetre

Les elements suivants sont explicitement exclus du perimetre de cet EPIC :

- **Saisie des heures (Time Sheet)** : la saisie hebdomadaire des heures par les collaborateurs est couverte par EPIC-CP-TEMPS (Feuilles de Temps). Le module Projets fournit les taches assignables mais ne gere pas la grille de saisie.
- **Module Contrats complet** : la creation et la gestion detaillee des contrats (au-dela du lien avec le projet) sont couverts par un module Contracts dedie. Le present EPIC couvre uniquement l'interface de liaison projet-contrat.
- **Module Facturation complet** : la creation, le workflow et l'envoi des factures sont couverts par EPIC-004 (Facturation). Le present EPIC couvre uniquement la visualisation des factures dans le profil projet.
- **Gestion des ressources et planification** : l'allocation des ressources, la charge de travail et le planning sont couverts par EPIC-006 (Planning).
- **Gestion avancee des clients** : la creation et la gestion des fiches clients sont couverts par EPIC-010 (Clients). Le module Projets consomme ces donnees en lecture.
- **Notes de frais** : la saisie des depenses est couverte par EPIC-013 (Notes de frais) et EPIC-CP-TEMPS.
- **Tableaux de bord transversaux** : les dashboards consolides multi-projets sont couverts par EPIC-014 (Tableau de bord).
- **Rapports avances** : les rapports personnalises et les analyses transversales sont couverts par EPIC-011 (Rapports).
- **Application mobile native** : le responsive design (tablette) est couvert, mais une application mobile native n'est pas dans le perimetre.
- **Migration des donnees depuis ChangePoint** : l'import des projets existants depuis ChangePoint sera couvert par un EPIC de migration separe.
- **Gestion documentaire (GED)** : le stockage et la gestion de documents de projet (plans, devis, correspondance) ne sont pas dans le perimetre de cet EPIC.

---

## 7. Regles Metier

| Ref | Regle |
|---|---|
| **RM-CP-01** | Le numero de projet client suit la convention **AANNNN** (2 chiffres annee + 4 chiffres sequentiels). Le systeme genere automatiquement le prochain numero disponible a la creation. L'utilisateur peut le modifier manuellement mais le systeme verifie l'unicite. |
| **RM-CP-02** | Le numero de projet administratif suit la convention **Admin-NN** (prefixe "Admin-" + 2 chiffres sequentiels). Le prochain numero disponible est calcule automatiquement. |
| **RM-CP-03** | Le nom de projet departemental suit la convention **PRAA - [Nom du departement]**. Le prefixe "PRAA - " est automatiquement ajoute lors de la creation d'un projet de type departemental. |
| **RM-CP-04** | Un projet departemental est **toujours non facturable** (Billable = Non). Ce flag ne peut pas etre modifie pour les projets de type departemental. |
| **RM-CP-05** | Un projet facturable (Billable = Oui) **doit etre associe a un contrat** pour que la facturation soit possible. Un avertissement est affiche dans le profil du projet tant qu'aucun contrat n'est associe. |
| **RM-CP-06** | La **numerotation WBS** suit la convention hierarchique XX.Y.Z : le premier niveau sous le projet utilise un numero a 2 chiffres (01, 02...), le deuxieme niveau ajoute un chiffre separe par un point (01.1, 01.2...), le troisieme niveau ajoute un chiffre supplementaire (01.1.1, 01.1.2...). La renumerotation est automatique en cas d'insertion ou de suppression. |
| **RM-CP-07** | Seules les **taches feuilles** (elements les plus bas de la hierarchie WBS) peuvent recevoir des assignations de collaborateurs et des saisies de temps. Les taches sommaires servent uniquement de regroupement. |
| **RM-CP-08** | Les **KPIs financiers** d'un projet sont calcules en temps reel selon les formules : Revenue = somme(heures approuvees par role x taux de facturation du role dans le contrat), Cost = somme(heures approuvees x taux de cout interne du collaborateur), Profit = Revenue - Cost, Margin% = (Profit / Revenue) x 100. |
| **RM-CP-09** | Le **taux de facturation effectif** (Billing Rate) est calcule selon la formule : Billing Rate = Standard Rate x (1 - Discount%). Exemple : Standard Rate = 150.00 CAD, Discount = 10%, Billing Rate = 135.00 CAD. |
| **RM-CP-10** | Un projet au statut **"Archived"** est verrouille en lecture seule. Aucune modification des proprietes, de la structure WBS, des assignations ou des saisies de temps n'est autorisee. Seul un administrateur peut deverrouiller un projet archive. |
| **RM-CP-11** | Un element WBS (tache ou phase) **ne peut pas etre supprime** s'il contient des heures saisies (directement ou dans ses elements enfants). Un message d'erreur indique le nombre total d'heures saisies et les collaborateurs concernes. |
| **RM-CP-12** | Les **totaux financiers** des taches sommaires sont calcules par roll-up (somme) des valeurs de toutes les taches enfants. Le roll-up est recursif : les totaux remontent a chaque niveau jusqu'au projet. |
| **RM-CP-13** | Chaque projet est rattache a une **entite juridique unique** (Provencher_Roy Prod ou PRAA). L'entite determine le bureau de facturation, la devise par defaut, les conditions contractuelles et les coordonnees de facturation. |
| **RM-CP-14** | Un collaborateur ne peut saisir du temps que sur les taches qui lui sont **explicitement assignees** dans le module Projets. L'assignation cree automatiquement la ligne correspondante dans sa feuille de temps. |
| **RM-CP-15** | Le caractere wildcard **"%"** dans le filtre rapide (Quick filter) remplace toute chaine de caracteres. La recherche "250%" retourne tous les projets dont le numero ou le nom commence par "250". La recherche "%IA%" retourne tous les projets contenant "IA" dans le nom ou le numero. |
| **RM-CP-16** | La section **"Recently viewed"** affiche les 10 derniers projets consultes par l'utilisateur connecte. La consultation d'un projet deja present dans la liste le remonte en premiere position sans creer de doublon. |
| **RM-CP-17** | Les **projets departementaux** sont consideres comme permanents : leur statut ne peut pas etre change en "Completed" ou "Archived" tant qu'ils sont utilises comme conteneurs de temps actifs par des collaborateurs. |
| **RM-CP-18** | Le **prefixe d'entite** dans le nom du projet (ex : "[PRA]") est gere automatiquement par le systeme. Il est ajoute a la creation et mis a jour en cas de changement d'entite. L'utilisateur ne saisit pas manuellement le prefixe. |
| **RM-CP-19** | La devise de reference est le **CAD** (Dollar canadien). Les taux de facturation dans les contrats sont exprimes en CAD. La gestion multi-devises (EUR, USD) est supportee au niveau du contrat avec conversion automatique. |
| **RM-CP-20** | Un projet ne peut etre **supprime definitivement** que s'il ne contient aucune donnee associee (aucune heure saisie, aucune facture, aucun contrat). Dans le cas contraire, le projet doit etre archive (statut "Archived") plutot que supprime. |

---

## 8. Contraintes Techniques

| # | Contrainte |
|---|---|
| 1 | Le module doit supporter un minimum de **500 projets actifs** simultanement sans degradation de performance (temps de chargement < 2 secondes pour la List View avec filtres). |
| 2 | La Tree View doit etre capable d'afficher une arborescence de **100+ elements** avec expansion/reduction fluide (temps de reponse < 300ms par operation). |
| 3 | La Worksheet View doit supporter l'edition simultanee de **50+ lignes** avec sauvegarde automatique et detection de conflits de modification concurrente (verrouillage optimiste). |
| 4 | Les KPIs financiers doivent etre recalcules en temps reel a chaque modification (heures saisies, taux de facturation modifie) avec un delai maximum de **1 seconde**. |
| 5 | L'API de recherche (Quick filter) doit retourner les resultats en moins de **500ms** pour une base de 1000+ projets. |
| 6 | Le systeme doit supporter la **multi-entite** avec isolation des donnees au niveau de la couche d'acces (un utilisateur sans droits sur une entite ne peut pas voir les projets de cette entite). |
| 7 | Le drag & drop dans la Tree View doit fonctionner sans latence perceptible et declencher la renumerotation WBS automatique en arriere-plan. |
| 8 | Les exports CSV/Excel/PDF doivent supporter des volumes de **500+ projets** avec un temps de generation maximum de **30 secondes**. |
| 9 | Le module doit etre responsive : utilisable sur tablette (largeur minimale 768px) avec adaptation automatique des vues (Tree View scrollable, List View avec colonnes prioritaires). |
| 10 | L'audit trail (historique des modifications) doit conserver les 12 derniers mois de modifications avec possibilite d'archivage au-dela. |

---

## 9. Dependances

### Dependances fonctionnelles

| Type | EPIC / Module | Description |
|---|---|---|
| **Depend de** | EPIC-010 (Clients) | Les informations client (nom, coordonnees, conditions) proviennent du module Clients. La creation de projet necessite la selection d'un client existant. |
| **Depend de** | EPIC-009 (Collaborateurs) | Les informations collaborateur (nom, role, entite, taux de cout interne) proviennent du module Collaborateurs. L'assignation aux taches necessite des collaborateurs existants. |
| **Depend de** | EPIC-016 (Configuration) | Les parametres de configuration du module (types de projets, conventions de nommage, workflow de statuts, niveaux WBS, entites) sont geres dans le module Configuration. |
| **Requis par** | EPIC-CP-TEMPS (Feuilles de Temps) | Les taches de projet et les assignations sont consommees par le module Feuilles de Temps pour la saisie des heures. |
| **Requis par** | EPIC-003 (Honoraires) | Les donnees de projet (structure WBS, effort planifie, heures consommees) alimentent le calcul des honoraires. |
| **Requis par** | EPIC-004 (Facturation) | Les projets facturables et leurs contrats associes sont utilises pour la generation des factures. |
| **Requis par** | EPIC-006 (Planning) | Les projets, taches et assignations alimentent la planification des ressources. |
| **Requis par** | EPIC-007 (Couts) | Les heures saisies et les taux de cout interne alimentent le calcul des couts par projet. |
| **Requis par** | EPIC-008 (Finances) | Les KPIs financiers des projets alimentent les etats financiers et les analyses de rentabilite. |
| **Requis par** | EPIC-011 (Rapports) | Les donnees de projet alimentent les rapports transversaux (portefeuille de projets, rentabilite, charge). |
| **Requis par** | EPIC-014 (Tableau de bord) | Les KPIs des projets alimentent les widgets du tableau de bord consolide. |
| **Requis par** | EPIC-017 (Notifications) | Les transitions de statut et les evenements de projet declenchent des notifications. |

### Dependances techniques

| Composant | Description |
|---|---|
| **API Clients** | Lecture des clients et de leurs coordonnees (GET) pour la selection dans le formulaire de creation de projet |
| **API Collaborateurs** | Lecture des collaborateurs, roles et entites (GET) pour l'assignation aux taches et la selection du Project Manager |
| **API Configuration** | Lecture des parametres du module (GET) : types de projets, conventions de nommage, workflow de statuts, niveaux WBS |
| **API Projets** | CRUD complet : creation, lecture, mise a jour, suppression des projets et de leur structure WBS |
| **API Contrats** | Lecture et liaison des contrats avec les projets (GET, PUT) ; lecture des Billing Roles & Rates (GET) |
| **API Factures** | Lecture des factures associees a un projet (GET) pour affichage dans le profil projet |
| **API Temps** | Lecture des heures saisies par projet et par tache (GET) pour le calcul des KPIs financiers et de l'avancement |
| **API Notifications** | Envoi de notifications email et in-app lors des transitions de statut et des evenements de projet |
| **Service de fichiers** | Export de documents (CSV, Excel, PDF) avec mise en forme et mise en page |
| **Service d'audit** | Enregistrement de toutes les modifications de donnees et de configuration dans un journal d'audit |

---

## 10. Criteres d'Acceptation Globaux

| # | Critere |
|---|---|
| 1 | Toutes les User Stories US-CP-01 a US-CP-19 sont developpees, testees et validees par le Product Owner. |
| 2 | Les 3 types de projets (client, administratif, departemental) sont creables avec leurs conventions de nommage respectives et leurs valeurs par defaut. |
| 3 | La structure WBS multi-niveaux (minimum 4 niveaux) est fonctionnelle avec numerotation automatique, ajout, modification, suppression et drag & drop. |
| 4 | Les 3 vues de navigation (Tree View, List View, Worksheet View) sont fonctionnelles et coherentes entre elles (modification dans une vue refletee dans les autres). |
| 5 | Les KPIs financiers (Revenue, Cost, Profit, Margin%) sont calcules en temps reel et affiches correctement dans le profil projet. |
| 6 | Le workflow de statuts (Proposed, Active, On Hold, Completed, Archived) est fonctionnel avec les transitions autorisees et les conditions de transition. |
| 7 | Le flag Billable impacte correctement l'affichage (icone, KPIs) et les fonctionnalites (liaison contrat, generation de factures). |
| 8 | Les filtres (Quick filter avec %, Status, Billable, Entity) fonctionnent correctement en mode combine (AND logique) dans la List View. |
| 9 | La gestion multi-entites est operationnelle : projets rattaches a une entite, filtrage par entite, KPIs par entite. |
| 10 | Le lien projet-contrat est fonctionnel : les Billing Roles & Rates sont accessibles depuis le profil projet et servent au calcul des KPIs Revenue. |
| 11 | Le lien projet-factures est fonctionnel : les factures associees sont visibles dans le profil projet avec leur statut (10 statuts du workflow). |
| 12 | L'assignation des collaborateurs aux taches est fonctionnelle et les taches assignees apparaissent dans les feuilles de temps des collaborateurs concernes. |
| 13 | La section "Recently viewed" affiche correctement les 10 derniers projets consultes, sans doublons, avec persistence entre sessions. |
| 14 | Les exports (CSV, Excel, PDF) sont fonctionnels et respectent les filtres appliques et les droits d'acces. |
| 15 | Les templates WBS sont creables, modifiables et applicables a de nouveaux projets. |
| 16 | Les performances sont acceptables : chargement List View < 2s, expansion Tree View < 300ms, recherche < 500ms, recalcul KPIs < 1s. |
| 17 | Le module est responsive et utilisable sur tablette (largeur minimale 768px). |
| 18 | L'audit trail trace toutes les modifications de projets, taches, statuts, assignations et configuration. |

---

## 11. Metriques de Succes

| # | Metrique | Objectif | Methode de mesure |
|---|---|---|---|
| 1 | **Parite fonctionnelle ChangePoint** | 100% des fonctionnalites auditees reproduites dans OOTI | Checklist de comparaison fonctionnalite par fonctionnalite |
| 2 | **Temps de creation d'un projet** | < 2 minutes pour un projet client avec structure WBS standard | Mesure du temps de bout en bout (formulaire -> validation) |
| 3 | **Temps de navigation inter-vues** | < 1 seconde pour basculer entre Tree, List et Worksheet View | Mesure du temps de chargement de chaque vue |
| 4 | **Taux d'adoption des templates WBS** | > 60% des nouveaux projets crees a partir d'un template | Ratio projets avec template / total projets crees sur 3 mois |
| 5 | **Precision des KPIs financiers** | 100% de coherence entre les KPIs calcules et les donnees source (heures + taux) | Audit mensuel comparant les KPIs affiches avec un calcul manuel |
| 6 | **Taux de completion des profils projet** | > 90% des projets actifs ont tous les champs obligatoires renseignes | Rapport de qualite des donnees genere mensuellement |
| 7 | **Satisfaction utilisateur** | Score > 4/5 sur la facilite de navigation et de creation de projets | Enquete utilisateur post-deploiement (SUS - System Usability Scale) |
| 8 | **Reduction du temps de recherche** | Reduction de 50% du temps moyen pour trouver un projet specifique vs ChangePoint | Mesure comparative (A/B) entre ChangePoint et OOTI |
| 9 | **Disponibilite du module** | 99.5% de disponibilite (uptime) sur les heures ouvrables | Monitoring applicatif (APM) |
| 10 | **Volume de donnees supporte** | 500+ projets actifs et 5000+ taches sans degradation de performance | Test de charge avec donnees synthetiques |

---

## 12. Estimation et Decoupage

### Sprints suggeres

| Sprint | User Stories | Perimetre | Duree estimee |
|---|---|---|---|
| **Sprint 1** | US-CP-01, US-CP-02, US-CP-03 | Creation des 3 types de projets avec conventions de nommage (fondations) | 2 semaines |
| **Sprint 2** | US-CP-04 | Structure WBS multi-niveaux avec numerotation automatique et drag & drop | 2.5 semaines |
| **Sprint 3** | US-CP-05, US-CP-06 | Tree View et List View avec filtres et recherche | 2 semaines |
| **Sprint 4** | US-CP-07, US-CP-11 | Worksheet View editable + Filtres avances | 2 semaines |
| **Sprint 5** | US-CP-08, US-CP-09, US-CP-10 | Profil projet, KPIs financiers, gestion des statuts, flag Billable | 2.5 semaines |
| **Sprint 6** | US-CP-12, US-CP-13, US-CP-14 | Multi-entites, liaison contrats, liaison facturation | 2.5 semaines |
| **Sprint 7** | US-CP-15, US-CP-16 | Assignments (lien feuilles de temps) + Recently viewed | 1.5 semaine |
| **Sprint 8** | US-CP-17, US-CP-18, US-CP-19 | Export/impression, templates WBS, configuration et parametrage | 2.5 semaines |

### Estimation globale

| Indicateur | Valeur |
|---|---|
| **Nombre de User Stories** | 19 |
| **Nombre de criteres d'acceptation** | 190 |
| **Nombre de regles metier** | 20 |
| **Nombre de sprints** | 8 |
| **Duree totale estimee** | 17 a 20 semaines |
| **Complexite** | Elevee (hierarchie WBS multi-niveaux, 3 vues synchronisees, KPIs temps reel, multi-entite, drag & drop, templates) |
| **Risques principaux** | Performance du drag & drop sur grandes arborescences, synchronisation des 3 vues, precision du calcul des KPIs en temps reel, complexite de la renumerotation WBS automatique, gestion des conflits de modification concurrente en Worksheet View |

### Prerequisites avant demarrage

- API Clients disponible en lecture (EPIC-010)
- API Collaborateurs disponible en lecture (EPIC-009)
- Module de configuration operationnel avec les entites et les parametres de base (EPIC-016)
- Charte graphique et composants UI valides (systeme de design : arborescence, grille editable, tableaux triables, filtres, modales, icones)
- Maquettes UX validees pour les 3 vues (Tree View, List View, Worksheet View), le profil projet, le formulaire de creation et les templates WBS
- Infrastructure de notifications operationnelle (EPIC-017)
- API Contrats disponible en lecture (module Contracts)

### Priorite de livraison recommandee

1. **MVP (Sprints 1-3)** : Creation des 3 types de projets + Structure WBS + Tree View + List View. Couvre les besoins fondamentaux de creation et de navigation.
2. **V1 Complete (Sprints 4-6)** : Worksheet View + KPIs financiers + Statuts + Multi-entites + Contrats + Facturation. Module utilisable en production avec parite ChangePoint.
3. **V1.1 Enrichissements (Sprint 7)** : Assignments + Recently viewed. Integration complete avec le module Feuilles de Temps.
4. **V1.2 Valeur ajoutee (Sprint 8)** : Export/impression + Templates WBS + Configuration avancee. Fonctionnalites superieures a ChangePoint.

---

## 13. Annexes

### Annexe A -- Types de projets observes dans ChangePoint

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
| 11 | -- | PRAA - Administration generale | Departemental | Non | PRAA | Active |
| 12 | -- | PRAA - Comptabilite | Departemental | Non | PRAA | Active |
| 13 | -- | PRAA - Ressources humaines | Departemental | Non | PRAA | Active |
| 14 | -- | PRAA - Technologie information | Departemental | Non | PRAA | Active |

### Annexe B -- Structure WBS detaillee (Projet 250029 Intelligence Artificielle)

```
250029 Intelligence Artificielle                      [Niveau 1 -- PROJET]
└── 01. Intelligence Artificielle                     [Niveau 2 -- WBS/Phase]
    ├── 01.1 Comite Intelligence Artificielle          [Niveau 3 -- Tache]
    ├── 01.2 Reflexion et mise en place GPTs           [Niveau 3 -- Tache]
    ├── 01.3 Developpement Application CV/Projet       [Niveau 3 -- Tache]
    ├── 01.4 Outils IA 3D                              [Niveau 3 -- Tache]
    ├── 01.5 Formation                                  [Niveau 3 -- Tache]
    ├── 01.6 Outils IA TI                               [Niveau 3 -- Tache]
    └── 01.7 Reflexion Atelier                          [Niveau 3 -- Tache]
```

### Annexe C -- Structure WBS detaillee (Projet PRAA - Administration generale)

```
PRAA - Administration generale                       [Niveau 1 -- PROJET]
├── Rencontres/Meetings                               [Niveau 2 -- Tache, expandable]
├── Formation/Coaching                                 [Niveau 2 -- Tache, expandable]
├── Autres/Others                                      [Niveau 2 -- Tache, expandable]
└── PRAA - Admin GRC                                   [Niveau 2 -- Sous-projet / Tache sommaire]
```

### Annexe D -- Architecture Projet-Contrat-Facture

```
┌──────────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐
│       PROJET         │────▶│       CONTRAT        │────▶│       FACTURE        │
│     (Project)        │     │     (Contract)       │     │     (Invoice)        │
├──────────────────────┤     ├──────────────────────┤     ├──────────────────────┤
│ • Nom + Numero       │     │ • Billing Roles      │     │ • 10 statuts         │
│ • Type (3 types)     │     │ • Standard Rate      │     │ • Draft → Archived   │
│ • Billable (Y/N)     │     │ • Discount %         │     │ • Double approbation │
│ • Customer           │     │ • Billing Rate       │     │ • Credit note        │
│ • Entity (multi)     │     │ • Currency           │     │ • Multi-entite       │
│ • KPIs financiers    │     │ • Billing Office     │     │ • Envoi client       │
│ • WBS multi-niveaux  │     │ • Client associe     │     │ • Encaissement       │
└──────────────────────┘     └──────────────────────┘     └──────────────────────┘
         │                            │                            │
         ▼                            ▼                            ▼
┌──────────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐
│   FEUILLE DE TEMPS   │     │   ROLES & TAUX       │     │ WORKFLOW 10 STATUTS  │
│   (Time Sheet)       │     │   (Billing Rates)    │     │                      │
├──────────────────────┤     ├──────────────────────┤     │ Draft                │
│ • Assignments taches │     │ • Architecte: 150$   │     │ → Pending Approval   │
│ • Saisie heures      │     │ • Designer: 125$     │     │ → Pending 2nd Approv │
│ • Soumission         │     │ • Technicien: 100$   │     │ → Approved           │
│ • Approbation        │     │ • Stagiaire: 65$     │     │ → Committed          │
│                      │     │ • Directeur: 200$    │     │ → Sent               │
│                      │     │ • Discount: 0-20%    │     │ → Paid / Part. Paid  │
│                      │     │                      │     │ → Credited           │
│                      │     │                      │     │ → Archived           │
└──────────────────────┘     └──────────────────────┘     └──────────────────────┘
```

### Annexe E -- Classification des projets ChangePoint

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        PROJETS CHANGEPOINT                                  │
├───────────────────────┬────────────────────┬────────────────────────────────┤
│  Projets clients      │ Projets admin      │ Projets departementaux         │
│  (NNNNNN)             │ (Admin-XX)         │ (PRAA - Xxx)                   │
├───────────────────────┼────────────────────┼────────────────────────────────┤
│ • Mandats clients     │ • Gestion interne  │ • Fonctions support            │
│ • Facturables/Non     │ • Facturables      │ • Non facturables              │
│ • WBS multi-niveaux   │ • WBS simple       │ • WBS simple                   │
│ • Contrats lies       │ • Pas de contrat   │ • Pas de contrat               │
│ • KPIs financiers     │ • Suivi couts      │ • Suivi temps seul             │
│ • Icone bleue         │ • Icone badge      │ • Icone rouge/barree           │
│ • 10 statuts facture  │ • Pas de facture   │ • Pas de facture               │
│ • Revenue + Cost +    │ • Cost uniquement  │ • Heures uniquement            │
│   Profit + Margin%    │                    │                                │
└───────────────────────┴────────────────────┴────────────────────────────────┘
```

### Annexe F -- Icones et indicateurs visuels

| Element | Icone | Description |
|---|---|---|
| Projet facturable | Livre bleu | Icone standard pour les projets clients facturables |
| Projet non facturable | Livre rouge/barre | Icone avec indicateur visuel de non-facturabilite |
| Tache sommaire (WBS) | Document avec checkmark | Niveau intermediaire de regroupement, non saisissable |
| Tache feuille | Document vert | Tache de saisie de temps, assignable aux collaborateurs |
| Projet actif | Badge vert | Indicateur de statut "Active" |
| Projet termine | Badge gris | Indicateur de statut "Completed" |
| Projet suspendu | Badge orange | Indicateur de statut "On Hold" |
| Projet archive | Badge rouge | Indicateur de statut "Archived" |

### Annexe G -- Niveaux WBS supportes

| Niveau | Designation ChangePoint | Icone | Fonction | Saisie de temps |
|---|---|---|---|---|
| Niveau 1 | Projet (Project) | Livre bleu | Entite racine, KPIs financiers, client, statut global | Non |
| Niveau 2 | Phase / WBS Summary | Document checkmark | Regroupement thematique (phase d'architecture) | Non |
| Niveau 3 | Tache (Task) | Document vert | Tache de detail, saisie de temps, assignation ressources | Oui |
| Niveau 4 | Sous-tache (Sub-task) | Document vert petit | Decomposition fine d'une tache (non observe mais supporte) | Oui |
| Niveau 5-6 | Sous-sous-tache | A definir | Niveaux supplementaires pour projets complexes (cible OOTI) | Oui (feuilles uniquement) |

### Annexe H -- Vues du module Projects

| Vue | Description | Usage principal | Colonnes/informations affichees |
|---|---|---|---|
| **Tree View** | Arborescence hierarchique expandable avec fleches d'expansion | Navigation dans la structure WBS, visualisation de la hierarchie | Icone, numero WBS, nom, fleche d'expansion, section Recently viewed |
| **List View** | Liste plate avec colonnes triables et filtrables | Recherche rapide, filtrage multi-criteres, vue d'ensemble du portefeuille | Project, Customer, Status, Billable, Entity, Project Manager |
| **Worksheet View** | Grille tableur avec cellules editables en inline | Modification en masse, saisie rapide de donnees, mise a jour groupee | Toutes les proprietes editables du projet et des taches |

---

*Document genere le 27 fevrier 2026 -- Audit Planview ChangePoint (instance Provencher Roy)*
*EPIC-CP-PROJETS -- Version 1.0*

---

## ADDENDUM -- Fonctionnalites supplementaires identifiees lors de l'audit approfondi

**Source** : Audit approfondi du profil projet 240008 ESG et du contrat Place des Arts
**Date d'ajout** : 27 fevrier 2026
**Raison** : Fonctionnalites de gestion de projet non couvertes dans l'EPIC initial

---

### US-CP-20 -- Work locations et gestion multi-provinces

**En tant que** chef de projet ou administrateur
**Je veux** configurer les lieux de travail (Work Locations) associes a un projet et definir un lieu de travail par defaut
**Afin de** assurer la conformite fiscale provinciale (taxes, retenues a la source) et suivre la repartition geographique des ressources affectees au projet

| # | Critere d'acceptation |
|---|---|
| 1 | Le profil de projet contient une section "Work Locations" permettant d'ajouter une ou plusieurs provinces canadiennes comme lieux de travail du projet |
| 2 | Les provinces disponibles incluent au minimum : Alberta, Colombie-Britannique, Ile-du-Prince-Edouard, Manitoba, Nouveau-Brunswick, Nouvelle-Ecosse, Ontario, Quebec, Saskatchewan, Terre-Neuve-et-Labrador, Territoires du Nord-Ouest, Nunavut, Yukon |
| 3 | Un champ "Default Work Location" permet de definir le lieu de travail par defaut du projet (ex : Quebec). Ce champ est obligatoire si au moins un work location est configure |
| 4 | Le lieu de travail par defaut est pre-selectionne automatiquement lors de la saisie de temps par les collaborateurs assignes au projet, mais peut etre modifie par le collaborateur |
| 5 | La modification de la liste des work locations ou du lieu par defaut est tracee dans l'historique des modifications du projet |
| 6 | Les implications fiscales sont calculees automatiquement en fonction de la province : taux de TPS/TVH, taux de TVQ (Quebec), retenues a la source provinciales applicables |
| 7 | Un rapport de repartition des heures par province est disponible dans le profil du projet, permettant de visualiser la ventilation geographique du travail |
| 8 | Les work locations configurables incluent egalement un champ "Work Codes" avec une valeur par defaut (Default) applicable a l'ensemble du projet |
| 9 | Lors de la creation d'un projet, le default work location est initialise a la province de l'entite juridique de rattachement (Quebec pour Provencher_Roy Prod) |
| 10 | La section Work Locations est exportable au format PDF/Excel avec le reste du profil projet |
| 11 | Un avertissement est affiche si un collaborateur saisit du temps sur un work location qui n'est pas dans la liste configuree du projet |
| 12 | La configuration des work locations est accessible uniquement aux chefs de projet et aux administrateurs (les collaborateurs standards ne peuvent pas modifier cette section) |

---

### US-CP-21 -- Ventilation par exercice fiscal (Fiscal Year Breakdown)

**En tant que** chef de projet ou directeur financier
**Je veux** consulter la ventilation des donnees financieres et des heures par exercice fiscal dans le profil du projet
**Afin de** suivre la performance du projet annee apres annee, faciliter les clotures comptables et planifier les budgets sur les periodes fiscales pertinentes

| # | Critere d'acceptation |
|---|---|
| 1 | Le profil de projet contient une section "Fiscal Year Breakdown" affichant un tableau de ventilation par exercice fiscal |
| 2 | Chaque ligne du tableau correspond a un exercice fiscal (ex : 2024-2025, 2025-2026) et affiche les colonnes : Revenue, Cost, Profit, Margin%, Heures planifiees, Heures consommees |
| 3 | Le champ "Billing Office for Fiscal Periods" est configurable dans le profil du projet et determine le bureau de facturation applicable pour chaque periode fiscale |
| 4 | Les exercices fiscaux sont calcules automatiquement en fonction des dates de debut et de fin du projet et de la configuration de l'annee fiscale de l'entite (ex : 1er janvier au 31 decembre ou 1er avril au 31 mars) |
| 5 | La ventilation fiscale est recalculee en temps reel lorsque des heures sont saisies ou approuvees, en affectant chaque saisie a l'exercice fiscal correspondant a la date de saisie |
| 6 | Un total cumule "All Years" est affiche en bas du tableau, sommant les valeurs de tous les exercices |
| 7 | La ventilation fiscale distingue les heures facturees des heures non encore facturees pour chaque exercice |
| 8 | Un graphique de type barre empilee permet de visualiser la repartition des revenus et des couts par exercice fiscal |
| 9 | La section est repliable (collapse) pour les projets mono-exercice ou les projets pour lesquels cette information n'est pas pertinente |
| 10 | Les donnees de la ventilation fiscale sont exportables au format CSV et Excel pour integration dans les outils comptables externes |
| 11 | Le changement de billing office pour une periode fiscale est trace dans l'historique des modifications |
| 12 | Pour les projets pluriannuels, un indicateur visuel (icone calendrier) signale les exercices en cours, clos et a venir |

---

### US-CP-22 -- Ressources projetees (Projected Resources)

**En tant que** chef de projet ou directeur des operations
**Je veux** planifier les ressources projetees sur un projet en definissant qui travaillera, quand et combien d'heures sont prevues
**Afin de** anticiper les besoins en personnel, comparer la planification previsionnelle avec la consommation reelle et optimiser l'allocation des ressources entre les projets

| # | Critere d'acceptation |
|---|---|
| 1 | Le profil de projet contient une section "Projected Resources" affichant un tableau des ressources planifiees avec les colonnes : Nom du collaborateur, Role, Periode (mois/semaine), Heures projetees, Heures reelles, Ecart (Delta), Pourcentage de consommation |
| 2 | L'ajout d'une ressource projetee se fait via une modale de selection permettant de choisir un collaborateur existant dans le module Collaborateurs (EPIC-009) et de definir son role dans le projet |
| 3 | Les heures projetees sont saisies par periode (granularite mensuelle ou hebdomadaire, configurable) pour chaque ressource |
| 4 | Les heures reelles sont calculees automatiquement a partir des saisies de temps approuvees du collaborateur sur les taches du projet |
| 5 | L'ecart (Delta) est calcule automatiquement : Delta = Heures projetees - Heures reelles. Un delta positif indique une sous-consommation, un delta negatif indique un depassement |
| 6 | Un code couleur visuel indique le statut de la consommation pour chaque ressource : vert (consommation <= 80% du projete), orange (consommation entre 80% et 100%), rouge (depassement > 100%) |
| 7 | Un total par colonne affiche la somme des heures projetees, des heures reelles et de l'ecart pour l'ensemble des ressources du projet |
| 8 | La vue "Projected Resources" permet de filtrer par periode (mois, trimestre, exercice fiscal) et par role |
| 9 | Un graphique de type ligne ou barre compare les heures projetees vs les heures reelles sur une ligne de temps pour identifier les tendances de consommation |
| 10 | La modification des heures projetees est tracee dans l'historique des modifications du projet avec la date, l'auteur, l'ancienne et la nouvelle valeur |
| 11 | Les donnees des ressources projetees sont exportables au format CSV et Excel pour analyse externe |
| 12 | Un avertissement est affiche lorsqu'un collaborateur est projete sur plus de 40 heures par semaine toutes projets confondus (surallocation), en s'appuyant sur les donnees du module Planning (EPIC-006) |

---

### US-CP-23 -- Rapports integres au projet

**En tant que** chef de projet ou directeur
**Je veux** acceder a des rapports predefinies directement depuis le profil du projet sans avoir a naviguer vers le module Rapports externe
**Afin de** consulter rapidement les indicateurs cles du projet (heures planifiees vs actuelles, heures et salaires, depenses et consultants) en contexte et prendre des decisions eclairees

| # | Critere d'acceptation |
|---|---|
| 1 | Le profil de projet contient une section "Reports" affichant la liste des rapports disponibles pour le projet courant |
| 2 | Les rapports predefinies incluent au minimum : "Heures Planifiees VS Actuelles" (comparaison des heures projetees et des heures reellement consommees par tache et par collaborateur), "Heures et Salaires" (ventilation des heures saisies avec les couts salariaux associes par collaborateur et par periode), "Depenses et Consultants par Projet" (suivi des depenses non salariales et des honoraires de consultants externes imputes au projet) |
| 3 | Chaque rapport est lance par un clic sur son nom dans la section Reports ; le rapport s'ouvre dans un panneau integre au profil projet (mode inline) ou dans un onglet dedie |
| 4 | Les rapports sont automatiquement filtres sur le projet courant (le parametre Project ID est pre-rempli et non modifiable dans le contexte du profil projet) |
| 5 | Chaque rapport offre des filtres supplementaires contextuels : periode (dates de debut et de fin), collaborateur, tache WBS, role |
| 6 | Les rapports sont exportables aux formats PDF et Excel depuis la section Reports du profil projet |
| 7 | Un bouton "Actualiser" permet de forcer le recalcul des donnees du rapport avec les dernieres saisies de temps et de depenses |
| 8 | Les rapports integres respectent les droits d'acces de l'utilisateur : un chef de projet voit les donnees de son projet, un directeur voit les donnees de tous les projets de son entite |
| 9 | La liste des rapports disponibles est configurable par un administrateur dans le module Configuration (EPIC-016) : ajout, suppression ou reordonnancement des rapports affiches dans la section Reports |
| 10 | Un rapport peut etre epingle en favori par l'utilisateur pour le retrouver en haut de la liste dans la section Reports |
| 11 | Les rapports integres sont coherents avec les rapports du module Rapports (EPIC-011) : les memes donnees, les memes calculs et les memes presentations sont utilises |
| 12 | Un indicateur de chargement (spinner) est affiche pendant la generation du rapport, avec un delai maximum de 5 secondes pour les projets de taille standard (< 50 taches, < 20 collaborateurs) |

---

## Regles Metier -- Addendum

| Ref | Regle |
|---|---|
| **RM-CP-21** | Chaque projet peut etre associe a **un ou plusieurs work locations** correspondant a des provinces canadiennes. Le **default work location** est obligatoire des qu'au moins un work location est configure. Il determine la province utilisee par defaut pour le calcul des taxes et retenues a la source lors de la saisie de temps. |
| **RM-CP-22** | Les **implications fiscales** sont calculees par province selon les taux en vigueur : TPS federale (5%), TVQ Quebec (9.975%), TVH Ontario (13%), TVH Colombie-Britannique (12%), etc. Le changement de work location pour une saisie de temps recalcule automatiquement les implications fiscales associees. |
| **RM-CP-23** | La **ventilation par exercice fiscal** repartit automatiquement les revenus, couts et heures en fonction de la date de saisie de temps ou de la date de facturation. La date de reference pour l'affectation a un exercice fiscal est la date de la saisie de temps (et non la date d'approbation ou de facturation). |
| **RM-CP-24** | Le **billing office for fiscal periods** peut etre modifie par exercice fiscal pour un meme projet. Cette fonctionnalite couvre les cas ou un projet est transfere entre bureaux au cours de sa duree de vie. Le billing office determine les coordonnees de facturation et les conditions contractuelles applicables a la periode. |
| **RM-CP-25** | Les **ressources projetees** constituent une planification previsionnelle non contraignante : un collaborateur peut saisir du temps sur un projet meme s'il n'est pas dans la liste des ressources projetees (sous reserve d'etre assigne a une tache via US-CP-15). La comparaison previsionnel vs reel est a titre indicatif uniquement. |
| **RM-CP-26** | Les **rapports integres** au profil projet sont des vues en lecture seule des donnees du module Rapports (EPIC-011). Ils ne constituent pas des rapports independants : toute modification de la logique de calcul dans le module Rapports est automatiquement refletee dans les rapports integres. Le perimetre des rapports integres est limite au projet courant. |
| **RM-CP-27** | Un collaborateur **suraloue** (projete sur plus de 40 heures hebdomadaires toutes projets confondus) declenche un avertissement visuel (icone orange) dans la section Projected Resources de chaque projet concerne. Cet avertissement est informatif et ne bloque pas la planification. |
| **RM-CP-28** | Les **work codes** associes a un projet sont configures dans la section Work Locations. La valeur par defaut est "Default". Les work codes permettent de categoriser les heures saisies selon le type de travail effectue (ex : conception, supervision de chantier, coordination) pour un meme lieu de travail. |

---

### Mise a jour des Criteres d'Acceptation Globaux -- Addendum

| # | Critere |
|---|---|
| 19 | Les User Stories US-CP-20 a US-CP-23 sont developpees, testees et validees par le Product Owner. |
| 20 | La gestion multi-provinces (Work Locations) est operationnelle : ajout/suppression de provinces, default work location, calcul des implications fiscales par province. |
| 21 | La ventilation par exercice fiscal est fonctionnelle : repartition automatique des revenus, couts et heures par exercice, billing office par periode fiscale, total cumule. |
| 22 | La section Projected Resources permet la planification previsionnelle des ressources avec comparaison previsionnel vs reel et indicateurs visuels de consommation. |
| 23 | Les rapports integres au profil projet sont accessibles en contexte, filtres automatiquement sur le projet courant, et exportables en PDF/Excel. |
| 24 | Les regles metier RM-CP-21 a RM-CP-28 sont implementees et validees par des tests fonctionnels. |

---

### Estimation Sprints supplementaires -- Addendum

| Sprint | User Stories | Perimetre | Duree estimee |
|---|---|---|---|
| **Sprint 9** | US-CP-20, US-CP-21 | Work Locations multi-provinces + Ventilation par exercice fiscal | 2.5 semaines |
| **Sprint 10** | US-CP-22, US-CP-23 | Ressources projetees + Rapports integres au projet | 2.5 semaines |

### Mise a jour de l'estimation globale -- Addendum

| Indicateur | Valeur initiale | Valeur mise a jour |
|---|---|---|
| **Nombre de User Stories** | 19 | 23 |
| **Nombre de criteres d'acceptation** | 190 | 238 |
| **Nombre de regles metier** | 20 | 28 |
| **Nombre de sprints** | 8 | 10 |
| **Duree totale estimee** | 17 a 20 semaines | 22 a 25 semaines |

---

*Addendum genere le 27 fevrier 2026 -- Audit approfondi du profil projet 240008 ESG et du contrat Place des Arts*
*EPIC-CP-PROJETS -- Version 1.1*
