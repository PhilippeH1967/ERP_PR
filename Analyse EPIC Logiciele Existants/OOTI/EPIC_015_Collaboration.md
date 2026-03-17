# EPIC -- Module Collaboration

**Application OOTI -- Gestion de projets pour cabinets d'architecture**
**Version 1.0 -- Fevrier 2026**

---

## 1. Identification

| Champ              | Valeur                                                                       |
|--------------------|------------------------------------------------------------------------------|
| **Nom**            | Collaboration                                                                |
| **Reference**      | EPIC-015                                                                     |
| **Module parent**  | Collaboration                                                                |
| **Priorite**       | Basse                                                                        |
| **EPICs lies**     | EPIC-002 Projets, EPIC-009 Collaborateurs, EPIC-017 Notifications            |
| **Version**        | 1.0                                                                          |
| **Date de creation** | 26/02/2026                                                                 |
| **Auteur**         | Equipe Produit OOTI                                                          |
| **Statut**         | Brouillon                                                                    |

---

## 2. Contexte et Problematique

### 2.1 Contexte general

Les cabinets d'architecture operent dans un environnement de travail hautement collaboratif ou la reussite d'un projet depend de la coordination etroite entre de multiples intervenants : architectes, chefs de projet, dessinateurs, ingenieurs structure, economistes de la construction, bureaux d'etudes techniques, maitres d'ouvrage et entreprises de construction. Chaque projet architectural genere un volume considerable d'echanges, de documents, de decisions et de taches qui doivent etre traces, partages et suivis de maniere rigoureuse.

Dans la pratique quotidienne d'une agence d'architecture, les equipes jonglent entre plusieurs outils disconnectes : emails pour la communication, tableurs pour le suivi des taches, serveurs de fichiers pour les documents, applications de messagerie pour les echanges informels, et parfois meme des notes papier pour les comptes rendus de reunion. Cette fragmentation des outils engendre une perte d'information significative, des doublons, des versions contradictoires de documents et une difficulte a reconstituer l'historique d'un projet.

### 2.2 Problematique identifiee

Les principaux problemes constates dans les cabinets d'architecture en matiere de collaboration sont les suivants :

- **Dispersion de l'information** : les echanges relatifs a un projet sont eparpilles entre les boites email individuelles des collaborateurs, les messages instantanes, les notes de reunion et les appels telephoniques. Lorsqu'un collaborateur quitte le projet ou l'agence, une partie de la memoire du projet disparait avec lui.

- **Absence de tracabilite des actions** : il est difficile de retracer qui a pris quelle decision, quand et pourquoi. Les modifications apportees aux documents ou aux plans ne sont pas systematiquement journalisees, ce qui complique la gestion des responsabilites et la resolution des litiges.

- **Gestion artisanale des taches** : le suivi des taches est souvent realise via des to-do lists informelles ou des tableurs partages qui manquent de structure, ne permettent pas de filtrage avance et ne sont pas relies aux projets et phases de l'agence.

- **Difficulte de partage documentaire** : les fichiers (plans DWG, PDF de permis, images de chantier, rapports techniques) sont stockes sur des serveurs locaux ou dans des arborescences cloud sans lien direct avec le projet dans l'application de gestion. Le versioning est manuel et source d'erreurs.

- **Communication interne defaillante** : les agences manquent d'un canal structure pour diffuser les informations internes (actualites de l'agence, bonnes pratiques, retours d'experience). Les emails internes se perdent dans le flux des messages externes.

### 2.3 Positionnement dans l'application OOTI

Le module Collaboration constitue le ciment qui relie les differents modules fonctionnels de l'application OOTI. Il s'articule autour de deux niveaux d'acces :

1. **Niveau global (sidebar Collaboration)** : accessible depuis la barre laterale principale, il offre une vue transversale sur les elements collaboratifs de tous les projets. Ce niveau comprend quatre rubriques : **Taches**, **Notes**, **Blog** et **Notifications**.

2. **Niveau projet (menu PLUS du projet)** : accessible depuis la fiche d'un projet specifique, il expose les elements collaboratifs propres a ce projet. Ce niveau comprend quatre rubriques : **Fichiers**, **Notes**, **Emails** et **Actions**.

Cette architecture a deux niveaux permet aux collaborateurs de travailler soit dans une vision globale multi-projets (pour les chefs de projet et la direction), soit dans une vision focalisee sur un projet particulier (pour les equipes operationnelles).

---

## 3. Objectif

### 3.1 Objectif principal

Fournir un ensemble integre d'outils de collaboration permettant aux equipes des cabinets d'architecture de centraliser l'ensemble de leurs echanges, taches, documents et activites au sein d'une plateforme unique, directement reliee aux projets et aux phases de l'agence.

### 3.2 Objectifs specifiques

| # | Objectif | Indicateur de succes |
|---|----------|---------------------|
| O1 | Centraliser la gestion des taches de tous les projets dans une interface unique avec vues liste et kanban | 100% des taches creees dans l'application sont associees a un projet ou a un collaborateur |
| O2 | Permettre la creation et le partage de notes collaboratives riches liees aux projets | Reduction de 60% des emails internes relatifs aux notes de reunion et comptes rendus |
| O3 | Offrir un systeme de gestion de fichiers integre avec versioning et previsualisation | Zero perte de document et tracabilite complete des versions |
| O4 | Mettre en place un blog interne pour la communication d'agence | Au moins 2 articles publies par mois par agence |
| O5 | Integrer l'historique des emails lies aux projets | 100% des emails projet accessibles depuis la fiche projet |
| O6 | Journaliser automatiquement les actions significatives sur les projets | Couverture de 100% des actions critiques (creation, modification, suppression) |
| O7 | Permettre une recherche et un filtrage transversaux sur l'ensemble des elements collaboratifs | Temps d'acces a une information inferieur a 10 secondes |

### 3.3 Benefices attendus

- **Pour les architectes et dessinateurs** : acces rapide aux fichiers, notes et taches de leurs projets depuis une interface unifiee.
- **Pour les chefs de projet** : vision globale de l'avancement des taches sur l'ensemble de leurs projets, avec possibilite de filtrer et prioriser.
- **Pour la direction de l'agence** : journal d'activite complet pour le suivi des projets et communication interne structuree via le blog.
- **Pour l'agence dans son ensemble** : reduction de la perte d'information, amelioration de la tracabilite et gain de productivite.

---

## 4. Perimetre Fonctionnel

### 4.1 Vue d'ensemble

Le module Collaboration se decompose en six sous-modules fonctionnels repartis sur deux niveaux d'acces :

```
COLLABORATION (Sidebar)              PROJET (Menu PLUS)
+---------------------------+        +---------------------------+
|  Taches (vue globale)     |        |  Fichiers                 |
|  Notes (vue globale)      |        |  Notes (vue projet)       |
|  Blog                     |        |  Emails                   |
|  Notifications            |        |  Actions                  |
+---------------------------+        +---------------------------+
```

### 4.2 Sous-module A -- Taches

#### A.1 Liste de taches globale
- Affichage de toutes les taches de l'utilisateur connecte, tous projets confondus
- Regroupement possible par projet, par date d'echeance, par priorite ou par statut
- Compteur de taches par statut (a faire, en cours, termine)
- Pagination et chargement progressif pour les listes volumineuses

#### A.2 Creation et gestion de taches
- Formulaire de creation avec les champs : titre (obligatoire), description (optionnel, texte riche), projet associe (optionnel), phase associee (optionnel, dependant du projet selectionne), collaborateur assigne (optionnel), date d'echeance (optionnel), priorite (Basse, Normale, Haute, Urgente)
- Edition inline des champs principaux (titre, statut, priorite, assignation, date d'echeance)
- Suppression d'une tache avec confirmation
- Duplication d'une tache existante
- Ajout de commentaires sur une tache
- Ajout de pieces jointes a une tache
- Sous-taches (un niveau de profondeur)

#### A.3 Statuts des taches
- Trois statuts disponibles : **A faire**, **En cours**, **Termine**
- Transition libre entre les statuts (pas de workflow impose)
- Horodatage automatique des changements de statut
- Notification au collaborateur assigne lors d'un changement de statut

#### A.4 Vue Kanban
- Affichage des taches sous forme de colonnes correspondant aux statuts
- Drag-and-drop pour changer le statut d'une tache
- Filtrage applicable sur la vue kanban (memes filtres que la vue liste)
- Personnalisation des colonnes (ajout de colonnes intermediaires en version future)
- Affichage de l'avatar de l'assigne, de la priorite et de la date d'echeance sur chaque carte

#### A.5 Filtres et recherche
- Filtre par projet
- Filtre par collaborateur assigne
- Filtre par statut
- Filtre par priorite
- Filtre par date d'echeance (en retard, aujourd'hui, cette semaine, ce mois)
- Recherche textuelle sur le titre et la description
- Combinaison de filtres multiples
- Sauvegarde de filtres favoris

### 4.3 Sous-module B -- Notes

#### B.1 Notes collaboratives
- Creation de notes globales (non liees a un projet) ou de notes liees a un projet specifique
- Editeur de texte riche (gras, italique, listes, titres, liens, images inline, tableaux)
- Partage d'une note avec un ou plusieurs membres du projet ou de l'agence
- Acces en lecture seule ou en edition selon les droits definis par le createur

#### B.2 Organisation des notes
- Liste des notes avec tri par date de modification, date de creation, titre
- Filtrage par projet, par auteur, par date
- Recherche en texte integral sur le titre et le contenu
- Epinglage de notes importantes en haut de la liste

#### B.3 Historique des modifications
- Enregistrement automatique de chaque modification avec horodatage et auteur
- Consultation de l'historique des versions d'une note
- Restauration d'une version anterieure
- Indication visuelle des modifications recentes (surlignage des changements)

### 4.4 Sous-module C -- Fichiers (niveau projet)

#### C.1 Upload de fichiers
- Upload par glisser-deposer (drag-and-drop) ou via selecteur de fichiers
- Upload multiple simultane
- Barre de progression pour les fichiers volumineux
- Types de fichiers supportes : PDF, images (JPG, PNG, TIFF), documents (DOC, DOCX, XLS, XLSX), fichiers CAO (DWG, DXF), fichiers BIM (IFC, RVT), archives (ZIP, RAR)
- Limite de taille par fichier configurable (par defaut : 100 Mo)

#### C.2 Organisation en dossiers
- Creation de dossiers et sous-dossiers (arborescence libre)
- Deplacement de fichiers entre dossiers
- Renommage de fichiers et dossiers
- Dossiers par defaut suggeres a la creation d'un projet : Plans, Documents administratifs, Photos chantier, Rapports, Correspondance

#### C.3 Versioning des fichiers
- Upload d'une nouvelle version d'un fichier existant
- Conservation de l'historique des versions (numero de version automatique)
- Consultation et telechargement des versions anterieures
- Indication de la version courante
- Commentaire obligatoire lors de l'upload d'une nouvelle version

#### C.4 Previsualisation
- Previsualisation integree pour les formats PDF, JPG, PNG, GIF
- Zoom et navigation dans les documents previsualises
- Mode plein ecran pour la previsualisation
- Affichage des metadonnees du fichier (taille, date d'upload, auteur, version)

#### C.5 Partage et telechargement
- Telechargement individuel ou par lot (ZIP)
- Partage de fichiers avec les membres du projet
- Lien de partage temporaire pour les intervenants externes (avec date d'expiration)
- Notification aux membres lors de l'ajout d'un nouveau fichier

### 4.5 Sous-module D -- Blog

#### D.1 Creation et edition d'articles
- Editeur de texte riche pour la redaction d'articles (gras, italique, titres, listes, images, liens, videos embarquees)
- Brouillons : sauvegarde automatique et manuelle avant publication
- Previsualisation avant publication
- Planification de la date de publication

#### D.2 Publication et gestion
- Statuts des articles : Brouillon, Publie, Archive
- Publication immediate ou programmee
- Modification d'un article publie (avec indicateur "modifie le")
- Archivage des anciens articles
- Suppression avec confirmation

#### D.3 Categorisation et tags
- Creation et gestion de categories (ex : Actualites, Bonnes pratiques, Projets remarquables, Formation)
- Ajout de tags libres sur les articles
- Filtrage par categorie et par tag
- Nuage de tags

#### D.4 Consultation et interaction
- Liste des articles avec pagination
- Affichage en mode carte avec image de couverture, titre, extrait, auteur et date
- Page de lecture d'un article
- Commentaires sur les articles (optionnel, activable par l'administrateur)
- Compteur de vues

### 4.6 Sous-module E -- Emails (niveau projet)

#### E.1 Historique des emails
- Liste chronologique de tous les emails lies au projet
- Affichage de l'expediteur, du destinataire, de l'objet, de la date et d'un extrait du contenu
- Consultation du contenu complet d'un email
- Affichage des pieces jointes des emails

#### E.2 Envoi d'emails depuis le projet
- Formulaire d'envoi d'email avec champs : destinataire(s), objet, corps (texte riche), pieces jointes
- Modeles d'email predefinissables
- Association automatique de l'email envoye au projet
- Historique des emails envoyes et recus

#### E.3 Association automatique
- Mecanisme d'association d'emails au projet via une adresse email dediee par projet (ex : projet-xxx@ooti.app) ou via une extension navigateur
- Transfert d'emails vers l'adresse du projet pour archivage
- Detection automatique du projet destinataire sur la base de mots-cles ou de l'adresse de transfert

### 4.7 Sous-module F -- Actions (niveau projet)

#### F.1 Journal des actions
- Affichage chronologique de toutes les actions realisees sur le projet
- Types d'actions tracees : creation/modification/suppression de documents, changements de statut, ajout/retrait de collaborateurs, modifications de planning, modifications budgetaires, upload de fichiers, envoi d'emails
- Filtrage par type d'action, par collaborateur, par periode
- Recherche textuelle dans le journal

#### F.2 Log automatique
- Enregistrement automatique et transparent des actions (sans intervention de l'utilisateur)
- Horodatage precis (date et heure avec fuseau horaire)
- Identification du collaborateur ayant realise l'action
- Description structuree de l'action (action, objet concerne, valeur avant/apres pour les modifications)
- Retention des logs configurable (par defaut : duree de vie du projet + 2 ans)

---

## 5. User Stories

### US-CB01 : Liste des taches globale

**En tant que** chef de projet ou collaborateur de l'agence,
**Je veux** acceder a une liste globale de toutes mes taches, tous projets confondus, depuis la barre laterale de l'application,
**Afin de** avoir une vision d'ensemble de ma charge de travail et de prioriser mes actions quotidiennes sans avoir a naviguer projet par projet.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---------|--------------|
| 1 | L'entree "Taches" est accessible depuis la section "Collaboration" de la barre laterale principale | Navigation directe en un clic |
| 2 | La liste affiche par defaut toutes les taches assignees a l'utilisateur connecte, triees par date d'echeance croissante | Verification avec un utilisateur ayant des taches sur 3+ projets |
| 3 | Chaque ligne de tache affiche : titre, nom du projet associe, statut (badge colore), priorite (icone), date d'echeance, avatar de l'assigne | Verification visuelle de tous les champs |
| 4 | Un compteur synthetique en haut de page affiche le nombre de taches par statut : "X a faire | Y en cours | Z terminees" | Verification de la coherence des compteurs avec la liste |
| 5 | L'utilisateur peut basculer le regroupement entre : par projet, par date d'echeance, par priorite, par statut via un selecteur | Test de chaque mode de regroupement |
| 6 | La liste supporte la pagination avec 25 taches par page par defaut et un chargement fluide | Test avec 100+ taches |
| 7 | Les taches en retard (date d'echeance depassee et statut different de "Termine") sont visuellement mises en evidence par une couleur rouge sur la date | Verification avec des taches en retard |
| 8 | Un clic sur une tache ouvre le panneau de detail de la tache sans quitter la page de liste | Test de navigation |

---

### US-CB02 : Creation et gestion de taches

**En tant que** collaborateur de l'agence,
**Je veux** creer, modifier et supprimer des taches avec un ensemble complet d'attributs (titre, description, projet, phase, assigne, echeance, priorite),
**Afin de** structurer et suivre precisement le travail a realiser sur mes projets et ceux de l'agence.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---------|--------------|
| 1 | Un bouton "Nouvelle tache" est visible en permanence sur la page de liste des taches et ouvre un formulaire de creation | Verification de l'accessibilite du bouton |
| 2 | Le formulaire de creation comporte les champs : titre (obligatoire, max 200 caracteres), description (optionnel, editeur texte riche), projet associe (liste deroulante des projets actifs), phase associee (liste deroulante dynamique filtree par projet selectionne), collaborateur assigne (liste deroulante des collaborateurs actifs), date d'echeance (selecteur de date), priorite (Basse, Normale, Haute, Urgente -- defaut : Normale) | Test de chaque champ du formulaire |
| 3 | La sauvegarde d'une tache declenche une notification au collaborateur assigne (si different du createur) via le systeme de notifications (EPIC-017) | Verification de la reception de la notification |
| 4 | L'edition inline permet de modifier le titre, le statut, la priorite, l'assignation et la date d'echeance directement depuis la ligne de la tache dans la liste | Test de modification inline de chaque champ |
| 5 | La suppression d'une tache requiert une confirmation via une modale ("Etes-vous sur de vouloir supprimer cette tache ?") et la suppression est definitive | Test du flux de suppression |
| 6 | L'utilisateur peut ajouter des sous-taches (un seul niveau de profondeur) avec un titre et un statut (a faire / termine). Les sous-taches sont affichees sous la tache parente avec un indicateur de progression (ex : "3/5 terminees") | Test de creation et completion de sous-taches |
| 7 | L'utilisateur peut dupliquer une tache existante via un menu contextuel. La tache dupliquee reprend tous les attributs sauf le statut (reinitialise a "A faire") et les commentaires | Test de la duplication |
| 8 | L'utilisateur peut ajouter des commentaires textuels sur une tache. Chaque commentaire affiche l'auteur, la date et l'heure. Les commentaires sont tries du plus recent au plus ancien | Test d'ajout et de consultation des commentaires |

---

### US-CB03 : Vue Kanban des taches

**En tant que** chef de projet,
**Je veux** visualiser les taches sous forme de tableau kanban avec des colonnes correspondant aux statuts,
**Afin de** piloter visuellement l'avancement du travail et reorganiser les priorites par simple glisser-deposer.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---------|--------------|
| 1 | Un bouton de basculement permet de passer de la vue liste a la vue kanban et inversement. Le choix de vue est memorise dans les preferences de l'utilisateur | Test de basculement et persistance |
| 2 | La vue kanban affiche trois colonnes par defaut : "A faire", "En cours", "Termine". Chaque colonne affiche un compteur du nombre de taches qu'elle contient | Verification visuelle des colonnes et compteurs |
| 3 | Chaque carte de tache dans le kanban affiche : titre, nom du projet (badge colore), priorite (indicateur visuel), date d'echeance, avatar de l'assigne | Verification du contenu des cartes |
| 4 | Le glisser-deposer (drag-and-drop) d'une carte d'une colonne a une autre met a jour le statut de la tache en temps reel, avec une animation fluide et un retour visuel (zone de depot mise en surbrillance) | Test de drag-and-drop entre toutes les colonnes |
| 5 | Tous les filtres disponibles en vue liste (projet, assigne, priorite, echeance) sont egalement applicables en vue kanban et produisent un filtrage coherent des cartes affichees | Test de chaque filtre en vue kanban |
| 6 | Un clic sur une carte ouvre le panneau de detail de la tache (meme panneau qu'en vue liste) | Test d'ouverture du detail |
| 7 | Les cartes sont ordonnees au sein de chaque colonne par priorite decroissante puis par date d'echeance croissante | Verification de l'ordre des cartes |
| 8 | La vue kanban est responsive : sur les ecrans de petite taille, les colonnes s'empilent verticalement avec la possibilite de scroller horizontalement | Test sur tablette et mobile |

---

### US-CB04 : Notes collaboratives

**En tant que** collaborateur de l'agence,
**Je veux** creer et partager des notes collaboratives avec un editeur de texte riche, pouvant etre liees a un projet ou globales,
**Afin de** documenter les decisions, les comptes rendus de reunion et les reflexions de maniere structuree et accessible a toute l'equipe.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---------|--------------|
| 1 | L'utilisateur peut creer une note depuis deux points d'acces : la section "Notes" de la sidebar Collaboration (note globale ou liee a un projet au choix) et la section "Notes" du menu PLUS d'un projet (note automatiquement liee au projet) | Test des deux points de creation |
| 2 | L'editeur de texte riche supporte les fonctionnalites suivantes : gras, italique, souligne, titres (H1, H2, H3), listes a puces et numerotees, insertion de liens hypertextes, insertion d'images inline, insertion de tableaux simples (lignes, colonnes), blocs de citation | Test de chaque fonctionnalite de l'editeur |
| 3 | Le createur d'une note peut definir les droits de partage : selectionner les collaborateurs avec qui partager et definir pour chacun un droit de "lecture seule" ou "edition" | Test des droits d'acces |
| 4 | La sauvegarde automatique de la note intervient toutes les 30 secondes lorsque des modifications sont en cours, avec un indicateur visuel "Sauvegarde en cours..." puis "Sauvegarde effectuee" | Test de la sauvegarde automatique |
| 5 | L'historique des modifications est accessible depuis la note : chaque entree de l'historique indique la date, l'heure, l'auteur et un resume des modifications. L'utilisateur peut restaurer une version anterieure de la note | Test de l'historique et de la restauration |
| 6 | La liste des notes est filtrable par projet, par auteur et par date de modification. Une recherche en texte integral permet de trouver une note par son contenu | Test des filtres et de la recherche |
| 7 | L'utilisateur peut epingler une note pour qu'elle apparaisse en haut de la liste des notes, independamment du tri applique | Test de l'epinglage |
| 8 | La suppression d'une note requiert une confirmation et n'est possible que par le createur de la note ou un administrateur | Test des droits de suppression |

---

### US-CB05 : Gestion de fichiers projet

**En tant que** collaborateur travaillant sur un projet,
**Je veux** organiser les fichiers du projet dans une arborescence de dossiers avec possibilite de creer, renommer, deplacer et supprimer des dossiers et des fichiers,
**Afin de** maintenir une organisation documentaire claire et retrouver facilement les plans, documents et photos lies au projet.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---------|--------------|
| 1 | La section "Fichiers" est accessible depuis le menu PLUS du projet et affiche l'arborescence des dossiers et fichiers du projet sous forme de vue liste avec colonnes : nom, taille, type, date d'upload, uploade par | Verification de l'affichage et des colonnes |
| 2 | L'utilisateur peut creer un dossier a la racine ou en sous-dossier (profondeur maximale : 5 niveaux). Le nom du dossier accepte les caracteres alphanumeriques, espaces, tirets et underscores (max 100 caracteres) | Test de creation de dossiers a differents niveaux |
| 3 | A la creation d'un projet, cinq dossiers par defaut sont automatiquement crees : "Plans", "Documents administratifs", "Photos chantier", "Rapports", "Correspondance" | Verification lors de la creation d'un nouveau projet |
| 4 | L'utilisateur peut renommer un fichier ou un dossier via un double-clic sur le nom ou via le menu contextuel (clic droit). Le renommage est valide par la touche Entree ou annule par Echap | Test du renommage |
| 5 | L'utilisateur peut deplacer un fichier ou un dossier par glisser-deposer vers un autre dossier, ou via le menu contextuel "Deplacer vers..." qui propose un selecteur d'arborescence | Test du deplacement par les deux methodes |
| 6 | La suppression d'un fichier ou dossier (et son contenu) requiert une confirmation. La suppression est definitive (pas de corbeille dans la version 1.0) | Test du flux de suppression |
| 7 | Un fil d'Ariane (breadcrumb) en haut de la zone de fichiers indique le chemin du dossier courant et permet la navigation rapide vers les dossiers parents | Test de la navigation via le breadcrumb |
| 8 | Une barre de recherche permet de retrouver un fichier par son nom dans l'arborescence complete du projet. Les resultats affichent le chemin du dossier contenant le fichier | Test de la recherche de fichiers |

---

### US-CB06 : Upload et versioning de fichiers

**En tant que** collaborateur travaillant sur un projet,
**Je veux** uploader des fichiers dans le projet avec un systeme de versioning automatique et pouvoir previsualiser les fichiers courants,
**Afin de** partager les documents de travail avec l'equipe tout en conservant un historique complet des versions successives.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---------|--------------|
| 1 | L'upload de fichiers est possible par glisser-deposer sur la zone de fichiers ou via un bouton "Uploader" qui ouvre le selecteur de fichiers natif du systeme d'exploitation. L'upload multiple est supporte (selection de plusieurs fichiers simultanement) | Test des deux methodes d'upload et de l'upload multiple |
| 2 | Une barre de progression est affichee pour chaque fichier en cours d'upload, indiquant le pourcentage d'avancement. L'utilisateur peut annuler un upload en cours | Test avec des fichiers volumineux (>10 Mo) |
| 3 | Les types de fichiers acceptes sont : PDF, JPG, PNG, TIFF, GIF, DOC, DOCX, XLS, XLSX, PPT, PPTX, DWG, DXF, IFC, RVT, ZIP, RAR. La taille maximale par fichier est de 100 Mo (configurable). Un message d'erreur clair est affiche si le type ou la taille ne sont pas conformes | Test avec des fichiers valides et invalides |
| 4 | Lorsqu'un fichier portant le meme nom qu'un fichier existant est uploade dans le meme dossier, le systeme propose deux options : "Remplacer (nouvelle version)" ou "Garder les deux (renommer)". Le choix "Remplacer" incremente le numero de version du fichier | Test du conflit de nommage |
| 5 | L'historique des versions d'un fichier est accessible depuis le menu contextuel du fichier. Il affiche pour chaque version : le numero de version, la date d'upload, l'auteur, le commentaire de version et la taille. L'utilisateur peut telecharger ou restaurer une version anterieure | Test de l'historique et de la restauration |
| 6 | La previsualisation integree est disponible pour les formats PDF (rendu page par page avec navigation), JPG, PNG et GIF (affichage avec zoom). Un clic sur le fichier ouvre la previsualisation dans un panneau lateral ou en mode plein ecran | Test de la previsualisation pour chaque format supporte |
| 7 | Le telechargement est possible pour un fichier individuel ou pour une selection de fichiers (telechargement en archive ZIP). Un bouton "Tout telecharger" permet de telecharger l'integralite du dossier courant | Test du telechargement individuel et par lot |
| 8 | Lors de l'upload d'un fichier, une notification est envoyee aux membres du projet (configurable : notification activee/desactivee par dossier) | Test de la notification |

---

### US-CB07 : Blog interne agence

**En tant que** directeur d'agence ou responsable communication,
**Je veux** creer, editer et publier des articles de blog internes accessibles a tous les collaborateurs de l'agence,
**Afin de** diffuser les actualites de l'agence, les bonnes pratiques, les retours d'experience et les informations importantes de maniere structuree et perenne.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---------|--------------|
| 1 | La section "Blog" est accessible depuis la sidebar Collaboration. La page d'accueil du blog affiche la liste des articles publies sous forme de cartes avec : image de couverture (optionnelle), titre, extrait (200 premiers caracteres), nom de l'auteur, date de publication, categorie et nombre de vues | Verification de l'affichage des cartes |
| 2 | La creation d'un article est reservee aux utilisateurs disposant du role "Redacteur" ou "Administrateur". Le formulaire de creation comprend : titre (obligatoire, max 250 caracteres), contenu (editeur texte riche), image de couverture (upload), categorie (selection), tags (saisie libre avec autocompletion) | Test de creation avec les differents champs |
| 3 | L'auteur peut sauvegarder un article en brouillon, le previsualiser tel qu'il apparaitra une fois publie, puis le publier immediatement ou programmer sa publication a une date et heure futures | Test des trois actions : brouillon, previsualisation, publication |
| 4 | Les articles publies peuvent etre modifies (avec affichage de la mention "Modifie le [date]") ou archives (retrait de la page d'accueil mais accessibles via les filtres). La suppression d'un article requiert une confirmation | Test de la modification, de l'archivage et de la suppression |
| 5 | Le systeme de categories permet de creer et gerer des categories (CRUD). Chaque article est associe a une seule categorie. Les categories par defaut sont : "Actualites", "Bonnes pratiques", "Projets remarquables", "Formation" | Test du CRUD des categories |
| 6 | Les tags sont des mots-cles libres associes aux articles. Un nuage de tags est affiche dans la barre laterale du blog. Un clic sur un tag filtre les articles correspondants | Test des tags et du filtrage |
| 7 | Chaque article dispose d'une page de lecture complete avec mise en forme riche, affichage de l'auteur, de la date, de la categorie et des tags. Un compteur de vues est incremente a chaque consultation unique | Test de la page de lecture et du compteur |
| 8 | L'administrateur peut activer ou desactiver les commentaires sur le blog. Lorsqu'ils sont actifs, les collaborateurs peuvent commenter les articles. Les commentaires sont moderes par l'auteur de l'article ou les administrateurs | Test de l'activation/desactivation et de la moderation |

---

### US-CB08 : Historique emails projet

**En tant que** chef de projet,
**Je veux** consulter l'historique complet des emails echanges dans le cadre d'un projet et pouvoir envoyer des emails directement depuis la fiche du projet,
**Afin de** centraliser toute la correspondance liee au projet et eviter la perte d'information dans les boites email individuelles.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---------|--------------|
| 1 | La section "Emails" est accessible depuis le menu PLUS du projet. Elle affiche une liste chronologique (du plus recent au plus ancien) de tous les emails associes au projet, avec les colonnes : expediteur, destinataire(s), objet, date/heure, presence de pieces jointes (icone) | Verification de l'affichage de la liste |
| 2 | Un clic sur un email de la liste ouvre le detail de l'email dans un panneau lateral affichant : l'en-tete complet (de, a, cc, date, objet), le corps du message en texte riche, et la liste des pieces jointes avec possibilite de telechargement | Test de consultation d'un email |
| 3 | L'utilisateur peut envoyer un email depuis le projet via un formulaire comportant : destinataire(s) (saisie avec autocompletion sur les contacts du projet et de l'agence), CC (optionnel), objet (pre-rempli avec le nom du projet entre crochets), corps du message (editeur texte riche), pieces jointes (upload) | Test d'envoi d'un email |
| 4 | L'email envoye depuis le projet est automatiquement associe au projet et apparait dans l'historique des emails du projet | Verification apres envoi |
| 5 | Le systeme fournit une adresse email unique par projet (format : projet-[reference]@ooti.app). Tout email transfere a cette adresse est automatiquement archive dans l'historique du projet | Test de transfert d'email vers l'adresse du projet |
| 6 | L'utilisateur peut filtrer les emails par periode (date de debut / date de fin), par expediteur et par presence de pieces jointes. Une recherche textuelle permet de trouver un email par son objet ou son contenu | Test des filtres et de la recherche |
| 7 | L'utilisateur peut creer et gerer des modeles d'email reutilisables (objet + corps pre-remplis). Lors de la redaction d'un email, un selecteur permet de charger un modele existant | Test des modeles d'email |
| 8 | Les pieces jointes des emails sont accessibles individuellement et comptabilisees dans le stockage du projet. Les pieces jointes les plus courantes (PDF, images) sont previsualisables sans telechargement | Test d'acces aux pieces jointes |

---

### US-CB09 : Journal des actions projet

**En tant que** chef de projet ou directeur d'agence,
**Je veux** consulter un journal automatique de toutes les actions significatives realisees sur un projet,
**Afin de** avoir une tracabilite complete des modifications, identifier les responsabilites et disposer d'un audit trail en cas de litige ou de questionnement.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---------|--------------|
| 1 | La section "Actions" est accessible depuis le menu PLUS du projet. Elle affiche un fil chronologique (timeline) des actions realisees sur le projet, de la plus recente a la plus ancienne | Verification de l'affichage de la timeline |
| 2 | Chaque entree du journal affiche : icone representant le type d'action, description de l'action (ex : "Paul Martin a uploade le fichier Plan_RDC_v3.pdf dans le dossier Plans"), nom du collaborateur ayant realise l'action (avec avatar), date et heure exactes (avec fuseau horaire) | Verification du format des entrees |
| 3 | Les types d'actions automatiquement traces sont : creation/modification/suppression d'elements du projet (phases, livrables), upload/suppression/modification de fichiers, changements de statut du projet ou des phases, ajout/retrait de collaborateurs sur le projet, modifications budgetaires (honoraires, depenses), envoi d'emails depuis le projet, creation/modification/suppression de notes du projet, modifications de planning | Test de la generation de log pour chaque type d'action |
| 4 | Pour les actions de modification, le journal enregistre la valeur avant et la valeur apres modification (ex : "Statut du projet modifie de 'En cours' a 'En pause'") | Verification des valeurs avant/apres |
| 5 | L'utilisateur peut filtrer le journal par type d'action (via des checkboxes), par collaborateur (liste deroulante) et par periode (selecteur de dates debut/fin) | Test de chaque filtre |
| 6 | Une recherche textuelle permet de trouver des actions specifiques dans le journal | Test de la recherche |
| 7 | Le journal d'actions est en lecture seule : aucun utilisateur ne peut modifier ou supprimer des entrees du journal. Seul un administrateur systeme peut configurer la duree de retention des logs (par defaut : duree du projet + 2 ans) | Verification de l'impossibilite de modification |
| 8 | L'export du journal est possible au format CSV ou PDF, avec application des filtres actifs au moment de l'export. L'export inclut toutes les colonnes : date, heure, collaborateur, type d'action, description, valeur avant, valeur apres | Test de l'export aux deux formats |

---

### US-CB10 : Recherche et filtres transversaux

**En tant que** collaborateur de l'agence,
**Je veux** effectuer des recherches transversales sur l'ensemble des elements collaboratifs (taches, notes, fichiers, articles de blog, emails) depuis un point d'acces unique,
**Afin de** retrouver rapidement une information quel que soit son type ou le projet auquel elle est rattachee.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---------|--------------|
| 1 | Une barre de recherche globale est accessible en permanence dans l'en-tete de l'application (ou via un raccourci clavier Ctrl/Cmd + K). La recherche s'effectue sur l'ensemble des elements collaboratifs : taches, notes, fichiers (nom), articles de blog, emails (objet et contenu) | Test de la recherche sur chaque type d'element |
| 2 | Les resultats de recherche sont affiches par type d'element, avec un compteur par type (ex : "3 taches, 2 notes, 5 fichiers, 1 article"). L'utilisateur peut filtrer les resultats par type d'element | Verification de l'affichage et du filtrage par type |
| 3 | Chaque resultat affiche : le type d'element (icone), le titre ou le nom, un extrait contextuel avec mise en surbrillance du terme recherche, le projet associe, la date de derniere modification | Verification du format des resultats |
| 4 | Un clic sur un resultat de recherche navigue directement vers l'element concerne dans son contexte d'affichage natif (ex : clic sur une tache ouvre la tache dans la vue taches du projet) | Test de la navigation depuis les resultats |
| 5 | La recherche supporte la recherche partielle (autocomplete apres 3 caracteres minimum) et la recherche insensible a la casse et aux accents | Test avec des termes partiels, majuscules/minuscules, et accents |
| 6 | Les filtres avances permettent de restreindre la recherche par : projet specifique, collaborateur (auteur ou assigne), periode (date de debut / date de fin) | Test des filtres avances |
| 7 | L'historique des 10 dernieres recherches est conserve et accessible via un clic sur la barre de recherche vide | Test de l'historique de recherche |
| 8 | Les resultats sont tries par pertinence par defaut, avec possibilite de trier par date de modification. Le temps de reponse de la recherche est inferieur a 2 secondes pour une base de 10 000 elements | Test de performance et de tri |

---

## 6. Hors Perimetre

Les elements suivants sont explicitement exclus du perimetre de l'EPIC-015 dans sa version 1.0 :

| # | Element exclu | Justification | Version cible |
|---|---------------|---------------|---------------|
| 1 | **Edition collaborative en temps reel des notes** (type Google Docs) | Complexite technique elevee (WebSocket, CRDT). L'edition collaborative sera sequentielle dans la V1 (un seul editeur a la fois avec verrouillage) | V2.0 |
| 2 | **Integration avec des outils de stockage cloud externes** (Google Drive, Dropbox, OneDrive) | Necessite des connecteurs API specifiques et des accords de partenariat. Le stockage est interne dans la V1 | V2.0 |
| 3 | **Application mobile native pour la collaboration** | La V1 se concentre sur l'application web responsive. Une application mobile dediee sera developpee ulterieurement | V2.0 |
| 4 | **Visioconference integree** | La V1 se limite a la collaboration asynchrone. L'integration de la visioconference (type Jitsi/WebRTC) est prevue en V2 | V2.0 |
| 5 | **Intelligence artificielle pour la categorisation automatique** | La categorisation et le tagging des fichiers et notes restent manuels dans la V1 | V3.0 |
| 6 | **Gestion avancee des permissions de fichiers** (ACL par fichier/dossier) | La V1 applique des permissions au niveau du projet. Les permissions granulaires par dossier/fichier seront ajoutees en V2 | V2.0 |
| 7 | **Integration email bidirectionnelle avec les clients de messagerie** (IMAP/SMTP natif) | La V1 utilise un mecanisme de transfert d'email vers une adresse dediee. L'integration directe avec les boites email est prevue en V2 | V2.0 |
| 8 | **Workflows de validation pour les taches** | La V1 propose une gestion libre des statuts. Les workflows de validation configurables seront ajoutes en V2 | V2.0 |
| 9 | **Systeme de mentions (@utilisateur) dans les commentaires et notes** | Sera ajoute dans une version ulterieure avec integration aux notifications | V1.1 |
| 10 | **Gestion des notifications** | Le systeme de notifications est couvert par l'EPIC-017 dedie. Le present EPIC se limite a emettre les evenements declencheurs | EPIC-017 |

---

## 7. Regles Metier

### 7.1 Regles generales

| Code | Regle | Description |
|------|-------|-------------|
| RM-CB-001 | **Visibilite des elements collaboratifs** | Un collaborateur ne peut voir que les elements (taches, notes, fichiers, emails, actions) des projets auxquels il est affecte (cf. EPIC-009 Collaborateurs) ou les elements explicitement partages avec lui. Les administrateurs ont acces a l'ensemble des elements. |
| RM-CB-002 | **Association au projet** | Tout element collaboratif (tache, note, fichier, email) peut etre associe a un projet. L'association est optionnelle pour les taches et les notes (elements globaux possibles), mais obligatoire pour les fichiers, les emails et les actions (qui n'existent qu'au niveau projet). |
| RM-CB-003 | **Suppression en cascade** | La suppression d'un projet entraine la suppression de tous les elements collaboratifs qui lui sont lies : taches, notes, fichiers, emails et actions. Cette suppression est irreversible et requiert une double confirmation. |

### 7.2 Regles specifiques aux taches

| Code | Regle | Description |
|------|-------|-------------|
| RM-CB-010 | **Unicite de l'assignation** | Une tache ne peut etre assignee qu'a un seul collaborateur a la fois. Pour les taches necessitant plusieurs intervenants, utiliser les sous-taches. |
| RM-CB-011 | **Coherence projet-phase** | Si une tache est associee a une phase, cette phase doit appartenir au projet selectionne. Le changement de projet reinitialise la phase. |
| RM-CB-012 | **Taches en retard** | Une tache est consideree en retard si sa date d'echeance est depassee et que son statut est different de "Termine". Les taches en retard generent une notification quotidienne a l'assigne et au chef de projet. |
| RM-CB-013 | **Completion automatique** | Lorsque toutes les sous-taches d'une tache sont marquees comme "Termine", le systeme propose automatiquement de passer la tache parente au statut "Termine" (sans l'imposer). |
| RM-CB-014 | **Priorites par defaut** | Toute nouvelle tache est creee avec la priorite "Normale" sauf indication contraire de l'utilisateur. |

### 7.3 Regles specifiques aux notes

| Code | Regle | Description |
|------|-------|-------------|
| RM-CB-020 | **Verrouillage en edition** | Lorsqu'un collaborateur edite une note, celle-ci est verrouillee pour les autres utilisateurs (mode lecture seule). Le verrou est relache apres sauvegarde ou apres 5 minutes d'inactivite. |
| RM-CB-021 | **Retention de l'historique** | L'historique des versions d'une note conserve les 50 dernieres versions. Au-dela, les versions les plus anciennes sont purgees automatiquement. |
| RM-CB-022 | **Droit de suppression** | Seul le createur d'une note ou un administrateur peut supprimer une note. Les collaborateurs avec droit d'edition peuvent modifier le contenu mais pas supprimer la note. |

### 7.4 Regles specifiques aux fichiers

| Code | Regle | Description |
|------|-------|-------------|
| RM-CB-030 | **Quota de stockage** | Chaque projet dispose d'un quota de stockage configurable (par defaut : 5 Go). Un avertissement est affiche a 80% d'utilisation. L'upload est bloque a 100%. |
| RM-CB-031 | **Versioning obligatoire** | L'upload d'un fichier portant le meme nom dans le meme dossier cree obligatoirement une nouvelle version (pas d'ecrasement silencieux). L'utilisateur est informe du numero de version cree. |
| RM-CB-032 | **Integrite des fichiers** | Un hash SHA-256 est calcule a l'upload de chaque fichier pour garantir l'integrite. La verification d'integrite est effectuee au telechargement. |
| RM-CB-033 | **Liens de partage externes** | Les liens de partage temporaires ont une duree de validite maximale de 30 jours. Le nombre de telechargements via un lien de partage est limite a 50. Le lien est automatiquement desactive apres expiration ou depassement du quota. |

### 7.5 Regles specifiques au blog

| Code | Regle | Description |
|------|-------|-------------|
| RM-CB-040 | **Droits de publication** | Seuls les utilisateurs ayant le role "Redacteur" ou "Administrateur" peuvent creer et publier des articles de blog. Tous les collaborateurs de l'agence peuvent consulter les articles publies. |
| RM-CB-041 | **Articles publies** | Un article publie ne peut pas etre remis en brouillon. Il peut etre modifie (avec mention de la date de modification) ou archive. |
| RM-CB-042 | **Compteur de vues** | Une vue n'est comptabilisee qu'une seule fois par utilisateur par article par jour (pas de comptage multiple en cas de consultations repetees le meme jour). |

### 7.6 Regles specifiques aux emails

| Code | Regle | Description |
|------|-------|-------------|
| RM-CB-050 | **Immutabilite des emails** | Les emails archives dans le projet ne peuvent pas etre modifies ou supprimes par les utilisateurs. Seul un administrateur peut purger les emails d'un projet. |
| RM-CB-051 | **Adresse email de projet** | L'adresse email dediee au projet est generee automatiquement a la creation du projet et reste active tant que le projet n'est pas supprime. |
| RM-CB-052 | **Taille des pieces jointes** | La taille maximale des pieces jointes pour l'envoi d'email depuis le projet est de 25 Mo au total par email. |

### 7.7 Regles specifiques au journal des actions

| Code | Regle | Description |
|------|-------|-------------|
| RM-CB-060 | **Immutabilite du journal** | Le journal des actions est strictement en lecture seule. Aucun utilisateur, y compris les administrateurs, ne peut modifier ou supprimer des entrees du journal. |
| RM-CB-061 | **Exhaustivite** | Toute action de creation, modification ou suppression d'un element du projet genere une entree dans le journal. Les consultations (lecture seule) ne sont pas tracees. |
| RM-CB-062 | **Retention** | Les logs sont conserves pendant la duree de vie du projet plus 2 ans apres l'archivage du projet. Passe ce delai, les logs peuvent etre purges automatiquement. |

---

## 8. Criteres Globaux

### 8.1 Performance

| Critere | Exigence |
|---------|----------|
| Temps de chargement de la liste des taches (100 taches) | < 1 seconde |
| Temps de chargement de la vue kanban (100 taches) | < 1.5 secondes |
| Temps de reponse de la recherche globale (10 000 elements) | < 2 secondes |
| Temps d'upload d'un fichier de 50 Mo | < 30 secondes (hors debit reseau) |
| Temps de generation de la previsualisation PDF (10 pages) | < 3 secondes |
| Temps de chargement du journal des actions (1000 entrees) | < 2 secondes |

### 8.2 Securite

| Critere | Exigence |
|---------|----------|
| Controle d'acces | Verification des droits a chaque requete (pas de securite uniquement cote client) |
| Chiffrement des fichiers au repos | AES-256 |
| Chiffrement des communications | TLS 1.2 minimum |
| Validation des fichiers uploades | Verification du type MIME reel (pas uniquement l'extension) |
| Protection contre les injections | Sanitization de tous les contenus texte riche (XSS prevention) |
| Audit trail | Journal des actions non modifiable et non suppressible |

### 8.3 Accessibilite

| Critere | Exigence |
|---------|----------|
| Conformite WCAG | Niveau AA minimum |
| Navigation clavier | Toutes les fonctionnalites accessibles au clavier |
| Lecteur d'ecran | Tous les elements interactifs disposent d'attributs ARIA |
| Contraste | Ratio de contraste minimum de 4.5:1 pour le texte |

### 8.4 Compatibilite

| Critere | Exigence |
|---------|----------|
| Navigateurs | Chrome 90+, Firefox 90+, Safari 15+, Edge 90+ |
| Responsive | Adapte aux ecrans de 320px a 2560px de largeur |
| Systemes d'exploitation | Windows 10+, macOS 11+, iOS 15+, Android 12+ |

### 8.5 Fiabilite

| Critere | Exigence |
|---------|----------|
| Disponibilite | 99.5% hors fenetres de maintenance planifiees |
| Sauvegarde automatique des notes | Toutes les 30 secondes en cas de modification |
| Perte de donnees | Zero perte de donnees sur les fichiers uploades (stockage redondant) |
| Recovery Point Objective (RPO) | 1 heure maximum |
| Recovery Time Objective (RTO) | 4 heures maximum |

---

## 9. Definition of Done (DoD)

Un element du module Collaboration est considere comme termine lorsque toutes les conditions suivantes sont remplies :

### 9.1 Developpement

- [ ] Le code source est ecrit en respectant les conventions de codage du projet (linting, formatage)
- [ ] Le code a ete revu par au moins un autre developpeur (code review approuvee)
- [ ] Les tests unitaires couvrent au minimum 80% du code applicatif de la fonctionnalite
- [ ] Les tests d'integration couvrent les principaux flux fonctionnels (creation, modification, suppression, consultation)
- [ ] Les tests end-to-end couvrent les scenarios critiques identifies dans les criteres d'acceptation
- [ ] Aucune regression n'est introduite sur les fonctionnalites existantes (suite de tests CI verte)

### 9.2 Qualite

- [ ] Tous les criteres d'acceptation de la user story sont verifies et valides
- [ ] Les tests de performance respectent les seuils definis dans les criteres globaux (section 8.1)
- [ ] Les validations de securite sont en place (controle d'acces, sanitization, chiffrement)
- [ ] Aucun bug bloquant ou critique n'est ouvert sur la fonctionnalite
- [ ] Les cas limites ont ete testes (champs vides, valeurs maximales, caracteres speciaux, fichiers corrompus)

### 9.3 UX/UI

- [ ] Les maquettes validees par l'equipe design sont fidelement implementees
- [ ] L'interface est responsive et testee sur les resolutions cibles (mobile, tablette, desktop)
- [ ] Les criteres d'accessibilite WCAG AA sont respectes
- [ ] Les messages d'erreur sont clairs, contextuels et en francais
- [ ] Les etats de chargement (spinners, skeletons) sont implementes pour toutes les operations asynchrones
- [ ] Les confirmations sont affichees pour toutes les actions destructives (suppression)

### 9.4 Documentation

- [ ] La documentation technique de l'API est mise a jour (Swagger/OpenAPI)
- [ ] Les eventuels changements de schema de base de donnees sont documentes et les migrations sont preparees
- [ ] Le changelog est mis a jour avec les nouvelles fonctionnalites
- [ ] Les guides utilisateurs sont mis a jour si necessaire

### 9.5 Deploiement

- [ ] La fonctionnalite est deployable via le pipeline CI/CD existant
- [ ] Les migrations de base de donnees sont reversibles
- [ ] Les feature flags sont en place si un deploiement progressif est necessaire
- [ ] Les metriques de monitoring sont configurees (logs applicatifs, alertes)

---

## 10. Dependances

### 10.1 Dependances entrantes (ce dont l'EPIC-015 a besoin)

| EPIC / Module | Dependance | Description | Criticite |
|---------------|------------|-------------|-----------|
| **EPIC-002 Projets** | Modele de donnees Projet et Phase | Les taches, notes, fichiers, emails et actions sont lies aux projets et phases. Le module Collaboration necessite l'existence des entites Projet et Phase pour les associations | **Bloquante** |
| **EPIC-009 Collaborateurs** | Modele de donnees Collaborateur et droits d'acces | L'assignation des taches, le partage des notes, le controle d'acces aux fichiers et l'identification des auteurs dans le journal d'actions dependent du module Collaborateurs | **Bloquante** |
| **EPIC-017 Notifications** | Systeme de notifications | Les evenements du module Collaboration (assignation de tache, partage de note, upload de fichier, commentaire) declenchent des notifications gerees par le module Notifications | **Majeure** |
| **Infrastructure** | Service de stockage de fichiers | Un service de stockage objet (type S3/MinIO) est necessaire pour le stockage des fichiers uploades | **Bloquante** |
| **Infrastructure** | Service d'envoi d'emails | Un service SMTP/API email (type SendGrid/SES) est necessaire pour l'envoi d'emails depuis les projets et la reception sur les adresses dediees | **Bloquante** |
| **Infrastructure** | Service de recherche | Un moteur de recherche (type Elasticsearch/Meilisearch) est recommande pour la recherche en texte integral sur les notes, emails et fichiers | **Majeure** |

### 10.2 Dependances sortantes (ce que l'EPIC-015 fournit)

| EPIC / Module | Element fourni | Description |
|---------------|----------------|-------------|
| **EPIC-017 Notifications** | Evenements declencheurs | Le module Collaboration emettra des evenements pour les notifications : tache assignee, tache en retard, note partagee, fichier uploade, commentaire ajoute, article de blog publie |
| **EPIC-002 Projets** | Widgets de synthese | Le module Collaboration fournira des widgets integrables dans le tableau de bord du projet : resume des taches, derniers fichiers, derniere activite |
| **Tous les modules** | Journal d'actions | Le systeme de journalisation des actions pourra etre reutilise par d'autres modules pour tracer leurs propres activites |

### 10.3 Dependances techniques

| Composant | Technologie recommandee | Justification |
|-----------|------------------------|---------------|
| Editeur de texte riche | TipTap (ProseMirror) ou Quill.js | Editeur riche extensible et compatible avec les navigateurs cibles |
| Drag-and-drop (Kanban) | dnd-kit ou react-beautiful-dnd | Librairie performante et accessible pour le drag-and-drop |
| Previsualisation PDF | PDF.js (Mozilla) | Standard de facto pour le rendu PDF dans le navigateur |
| Stockage fichiers | AWS S3 / MinIO | Stockage objet scalable avec versioning natif |
| Recherche texte integral | Meilisearch / Elasticsearch | Indexation et recherche rapide sur de gros volumes de texte |
| Envoi d'emails | SendGrid / AWS SES | Delivrabilite et gestion des bounces |

---

## 11. Modele de Donnees

### 11.1 Diagramme des entites

```
+----------------+       +----------------+       +----------------+
|     Task       |       |     Note       |       |     File       |
+----------------+       +----------------+       +----------------+
| id (PK)        |       | id (PK)        |       | id (PK)        |
| title          |       | title          |       | name           |
| description    |       | content        |       | project_id (FK)|
| project_id (FK)|       | project_id (FK)|       | folder_id (FK) |
| phase_id (FK)  |       | author_id (FK) |       | url            |
| assigned_to(FK)|       | shared_with[]  |       | version        |
| status         |       | is_pinned      |       | size           |
| priority       |       | created_at     |       | mime_type      |
| due_date       |       | updated_at     |       | hash_sha256    |
| parent_task_id |       +----------------+       | uploaded_by(FK)|
| created_by (FK)|                                 | uploaded_at    |
| created_at     |       +----------------+       | comment        |
| updated_at     |       |   BlogPost     |       +----------------+
+----------------+       +----------------+
                          | id (PK)        |       +----------------+
+----------------+       | title          |       | ActivityLog    |
|    Folder      |       | content        |       +----------------+
+----------------+       | author_id (FK) |       | id (PK)        |
| id (PK)        |       | status         |       | project_id (FK)|
| name           |       | category_id(FK)|       | user_id (FK)   |
| project_id (FK)|       | published_at   |       | action         |
| parent_id (FK) |       | scheduled_at   |       | entity_type    |
| created_at     |       | tags[]         |       | entity_id      |
+----------------+       | view_count     |       | details (JSON) |
                          | created_at     |       | old_value      |
+----------------+       | updated_at     |       | new_value      |
|  TaskComment   |       +----------------+       | created_at     |
+----------------+                                 +----------------+
| id (PK)        |       +----------------+
| task_id (FK)   |       |   BlogCategory |       +----------------+
| author_id (FK) |       +----------------+       | ProjectEmail   |
| content        |       | id (PK)        |       +----------------+
| created_at     |       | name           |       | id (PK)        |
+----------------+       | slug           |       | project_id (FK)|
                          | created_at     |       | from_address   |
+----------------+       +----------------+       | to_addresses[] |
| NoteVersion    |                                 | cc_addresses[] |
+----------------+       +----------------+       | subject        |
| id (PK)        |       |  NoteShare     |       | body           |
| note_id (FK)   |       +----------------+       | direction      |
| content        |       | id (PK)        |       | has_attachments|
| author_id (FK) |       | note_id (FK)   |       | sent_at        |
| created_at     |       | user_id (FK)   |       | created_at     |
+----------------+       | permission     |       +----------------+
                          | created_at     |
                          +----------------+       +----------------+
                                                   | EmailTemplate  |
+----------------+       +----------------+       +----------------+
| FileVersion    |       | BlogComment    |       | id (PK)        |
+----------------+       +----------------+       | name           |
| id (PK)        |       | id (PK)        |       | subject        |
| file_id (FK)   |       | post_id (FK)   |       | body           |
| version_number |       | author_id (FK) |       | created_by (FK)|
| url            |       | content        |       | created_at     |
| size           |       | created_at     |       +----------------+
| uploaded_by(FK)|       +----------------+
| comment        |
| created_at     |
+----------------+
```

### 11.2 Description detaillee des entites

#### Task (Tache)

| Champ | Type | Contraintes | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Identifiant unique de la tache |
| title | VARCHAR(200) | NOT NULL | Titre de la tache |
| description | TEXT | NULLABLE | Description detaillee (texte riche, stocke en HTML) |
| project_id | UUID | FK -> Project.id, NULLABLE | Projet associe (null si tache globale) |
| phase_id | UUID | FK -> Phase.id, NULLABLE | Phase associee (null si non associee a une phase) |
| assigned_to | UUID | FK -> User.id, NULLABLE | Collaborateur assigne |
| status | ENUM | NOT NULL, DEFAULT 'todo' | Statut : 'todo', 'in_progress', 'done' |
| priority | ENUM | NOT NULL, DEFAULT 'normal' | Priorite : 'low', 'normal', 'high', 'urgent' |
| due_date | DATE | NULLABLE | Date d'echeance |
| parent_task_id | UUID | FK -> Task.id, NULLABLE | Tache parente (pour les sous-taches) |
| created_by | UUID | FK -> User.id, NOT NULL | Createur de la tache |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date de creation |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date de derniere modification |

**Index** : (project_id), (assigned_to), (status), (due_date), (parent_task_id)

#### Note

| Champ | Type | Contraintes | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Identifiant unique de la note |
| title | VARCHAR(300) | NOT NULL | Titre de la note |
| content | TEXT | NULLABLE | Contenu de la note (texte riche, stocke en HTML) |
| project_id | UUID | FK -> Project.id, NULLABLE | Projet associe (null si note globale) |
| author_id | UUID | FK -> User.id, NOT NULL | Auteur de la note |
| is_pinned | BOOLEAN | NOT NULL, DEFAULT FALSE | Epinglage en haut de la liste |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date de creation |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date de derniere modification |
| locked_by | UUID | FK -> User.id, NULLABLE | Utilisateur detenant le verrou d'edition |
| locked_at | TIMESTAMP | NULLABLE | Date d'acquisition du verrou |

**Index** : (project_id), (author_id), (updated_at)

#### NoteShare (Partage de note)

| Champ | Type | Contraintes | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Identifiant unique du partage |
| note_id | UUID | FK -> Note.id, NOT NULL | Note partagee |
| user_id | UUID | FK -> User.id, NOT NULL | Utilisateur destinataire du partage |
| permission | ENUM | NOT NULL, DEFAULT 'read' | Niveau de permission : 'read', 'edit' |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date du partage |

**Index** : (note_id, user_id) UNIQUE

#### NoteVersion (Version de note)

| Champ | Type | Contraintes | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Identifiant unique de la version |
| note_id | UUID | FK -> Note.id, NOT NULL | Note concernee |
| content | TEXT | NOT NULL | Contenu de la note a cette version |
| author_id | UUID | FK -> User.id, NOT NULL | Auteur de la modification |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date de la version |

**Index** : (note_id, created_at)

#### Folder (Dossier)

| Champ | Type | Contraintes | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Identifiant unique du dossier |
| name | VARCHAR(100) | NOT NULL | Nom du dossier |
| project_id | UUID | FK -> Project.id, NOT NULL | Projet proprietaire |
| parent_id | UUID | FK -> Folder.id, NULLABLE | Dossier parent (null si racine) |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date de creation |

**Index** : (project_id, parent_id)
**Contrainte** : profondeur maximale de 5 niveaux (verifiee en applicatif)

#### File (Fichier)

| Champ | Type | Contraintes | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Identifiant unique du fichier |
| name | VARCHAR(255) | NOT NULL | Nom du fichier (avec extension) |
| project_id | UUID | FK -> Project.id, NOT NULL | Projet proprietaire |
| folder_id | UUID | FK -> Folder.id, NULLABLE | Dossier contenant le fichier (null si racine) |
| url | VARCHAR(2048) | NOT NULL | URL du fichier dans le stockage objet |
| version | INTEGER | NOT NULL, DEFAULT 1 | Numero de version courant |
| size | BIGINT | NOT NULL | Taille du fichier en octets |
| mime_type | VARCHAR(127) | NOT NULL | Type MIME du fichier |
| hash_sha256 | VARCHAR(64) | NOT NULL | Hash SHA-256 du fichier pour verification d'integrite |
| uploaded_by | UUID | FK -> User.id, NOT NULL | Utilisateur ayant uploade le fichier |
| uploaded_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date d'upload |
| comment | VARCHAR(500) | NULLABLE | Commentaire de version |

**Index** : (project_id, folder_id), (name, folder_id), (uploaded_by)

#### FileVersion (Version de fichier)

| Champ | Type | Contraintes | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Identifiant unique de la version |
| file_id | UUID | FK -> File.id, NOT NULL | Fichier concerne |
| version_number | INTEGER | NOT NULL | Numero de version |
| url | VARCHAR(2048) | NOT NULL | URL de cette version dans le stockage objet |
| size | BIGINT | NOT NULL | Taille de cette version en octets |
| uploaded_by | UUID | FK -> User.id, NOT NULL | Utilisateur ayant uploade cette version |
| comment | VARCHAR(500) | NULLABLE | Commentaire de version |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date de creation de cette version |

**Index** : (file_id, version_number) UNIQUE

#### BlogPost (Article de blog)

| Champ | Type | Contraintes | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Identifiant unique de l'article |
| title | VARCHAR(250) | NOT NULL | Titre de l'article |
| content | TEXT | NOT NULL | Contenu de l'article (texte riche) |
| excerpt | VARCHAR(500) | NULLABLE | Extrait (genere automatiquement si non fourni) |
| cover_image_url | VARCHAR(2048) | NULLABLE | URL de l'image de couverture |
| author_id | UUID | FK -> User.id, NOT NULL | Auteur de l'article |
| category_id | UUID | FK -> BlogCategory.id, NULLABLE | Categorie de l'article |
| status | ENUM | NOT NULL, DEFAULT 'draft' | Statut : 'draft', 'published', 'archived' |
| published_at | TIMESTAMP | NULLABLE | Date de publication effective |
| scheduled_at | TIMESTAMP | NULLABLE | Date de publication programmee |
| tags | TEXT[] | DEFAULT '{}' | Liste des tags (tableau de chaines) |
| view_count | INTEGER | NOT NULL, DEFAULT 0 | Nombre de vues |
| comments_enabled | BOOLEAN | NOT NULL, DEFAULT TRUE | Commentaires actives sur cet article |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date de creation |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date de derniere modification |

**Index** : (author_id), (status, published_at), (category_id)

#### BlogCategory (Categorie de blog)

| Champ | Type | Contraintes | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Identifiant unique de la categorie |
| name | VARCHAR(100) | NOT NULL, UNIQUE | Nom de la categorie |
| slug | VARCHAR(100) | NOT NULL, UNIQUE | Identifiant URL-friendly |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date de creation |

#### BlogComment (Commentaire de blog)

| Champ | Type | Contraintes | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Identifiant unique du commentaire |
| post_id | UUID | FK -> BlogPost.id, NOT NULL | Article commente |
| author_id | UUID | FK -> User.id, NOT NULL | Auteur du commentaire |
| content | TEXT | NOT NULL | Contenu du commentaire |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date du commentaire |

**Index** : (post_id, created_at)

#### TaskComment (Commentaire de tache)

| Champ | Type | Contraintes | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Identifiant unique du commentaire |
| task_id | UUID | FK -> Task.id, NOT NULL | Tache commentee |
| author_id | UUID | FK -> User.id, NOT NULL | Auteur du commentaire |
| content | TEXT | NOT NULL | Contenu du commentaire |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date du commentaire |

**Index** : (task_id, created_at)

#### ProjectEmail (Email de projet)

| Champ | Type | Contraintes | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Identifiant unique de l'email |
| project_id | UUID | FK -> Project.id, NOT NULL | Projet associe |
| from_address | VARCHAR(320) | NOT NULL | Adresse de l'expediteur |
| to_addresses | TEXT[] | NOT NULL | Adresses des destinataires |
| cc_addresses | TEXT[] | DEFAULT '{}' | Adresses en copie |
| subject | VARCHAR(500) | NOT NULL | Objet de l'email |
| body | TEXT | NOT NULL | Corps de l'email (HTML) |
| direction | ENUM | NOT NULL | Direction : 'inbound', 'outbound' |
| has_attachments | BOOLEAN | NOT NULL, DEFAULT FALSE | Indicateur de presence de pieces jointes |
| sent_at | TIMESTAMP | NOT NULL | Date d'envoi/reception |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date d'archivage dans le systeme |

**Index** : (project_id, sent_at), (from_address)

#### EmailTemplate (Modele d'email)

| Champ | Type | Contraintes | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Identifiant unique du modele |
| name | VARCHAR(200) | NOT NULL | Nom du modele |
| subject | VARCHAR(500) | NOT NULL | Objet pre-rempli |
| body | TEXT | NOT NULL | Corps pre-rempli (HTML) |
| created_by | UUID | FK -> User.id, NOT NULL | Createur du modele |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date de creation |

#### ActivityLog (Journal des actions)

| Champ | Type | Contraintes | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, NOT NULL | Identifiant unique de l'entree |
| project_id | UUID | FK -> Project.id, NOT NULL | Projet concerne |
| user_id | UUID | FK -> User.id, NOT NULL | Utilisateur ayant realise l'action |
| action | VARCHAR(50) | NOT NULL | Type d'action : 'create', 'update', 'delete', 'upload', 'status_change', 'assign', 'send_email' |
| entity_type | VARCHAR(50) | NOT NULL | Type d'entite concernee : 'project', 'phase', 'task', 'file', 'note', 'email', 'collaborator' |
| entity_id | UUID | NOT NULL | Identifiant de l'entite concernee |
| details | JSONB | NULLABLE | Details supplementaires de l'action (format JSON libre) |
| old_value | TEXT | NULLABLE | Valeur avant modification |
| new_value | TEXT | NULLABLE | Valeur apres modification |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date et heure de l'action |

**Index** : (project_id, created_at), (user_id), (entity_type, entity_id), (action)
**Partitionnement** : partitionnement par mois sur le champ created_at recommande pour les volumes importants

---

## 12. Estimation

### 12.1 Vue d'ensemble

| Parametre | Valeur |
|-----------|--------|
| **Duree totale estimee** | 7 semaines |
| **Nombre de sprints** | 4 sprints de 2 semaines (dont 1 semaine de stabilisation) |
| **Taille de l'equipe recommandee** | 2 developpeurs full-stack + 1 developpeur front-end + 1 QA |
| **Complexite globale** | Moyenne a elevee |

### 12.2 Decomposition par sprint

#### Sprint 1 (Semaines 1-2) -- Taches et fondations

| Element | Story Points | Jours/homme | Details |
|---------|-------------|-------------|---------|
| Modele de donnees Task, TaskComment, sous-taches | 5 | 2 | Creation des tables, migrations, API CRUD |
| API REST Taches (CRUD, filtres, recherche) | 8 | 3 | Endpoints RESTful avec pagination, filtrage et tri |
| Interface liste des taches (vue liste) | 8 | 3 | Composant liste avec edition inline, compteurs, regroupements |
| Interface creation/edition de tache | 5 | 2 | Formulaire avec validation, selecteurs dynamiques |
| Vue Kanban | 8 | 3 | Colonnes, cartes, drag-and-drop, synchronisation statut |
| Filtres et recherche des taches | 5 | 2 | Filtres combines, recherche textuelle, sauvegarde des filtres |
| Tests unitaires et d'integration Sprint 1 | 3 | 1.5 | Couverture des endpoints et composants |
| **Total Sprint 1** | **42** | **16.5** | |

#### Sprint 2 (Semaines 3-4) -- Notes et Fichiers

| Element | Story Points | Jours/homme | Details |
|---------|-------------|-------------|---------|
| Modele de donnees Note, NoteVersion, NoteShare | 3 | 1.5 | Creation des tables, migrations, API CRUD |
| API REST Notes (CRUD, partage, versioning) | 5 | 2 | Endpoints avec gestion du verrouillage et des permissions |
| Interface notes avec editeur de texte riche | 8 | 3.5 | Integration TipTap/Quill, formatage, sauvegarde auto |
| Historique des versions des notes | 5 | 2 | Liste des versions, comparaison, restauration |
| Modele de donnees File, Folder, FileVersion | 3 | 1.5 | Creation des tables, migrations |
| API REST Fichiers (CRUD, upload, versioning) | 8 | 3 | Endpoints avec upload multipart, gestion du stockage S3 |
| Interface gestion de fichiers (arborescence, upload) | 8 | 3 | Vue arborescence, drag-and-drop, barre de progression |
| Previsualisation de fichiers (PDF, images) | 5 | 2 | Integration PDF.js, viewer d'images |
| Tests unitaires et d'integration Sprint 2 | 5 | 2 | Couverture des endpoints et composants |
| **Total Sprint 2** | **50** | **20.5** | |

#### Sprint 3 (Semaines 5-6) -- Blog, Emails, Actions

| Element | Story Points | Jours/homme | Details |
|---------|-------------|-------------|---------|
| Modele de donnees BlogPost, BlogCategory, BlogComment | 3 | 1.5 | Creation des tables, migrations |
| API REST Blog (CRUD, publication, categories, tags) | 5 | 2 | Endpoints avec gestion des statuts et planification |
| Interface Blog (liste, creation, lecture, commentaires) | 8 | 3.5 | Pages liste, editeur, page de lecture, commentaires |
| Modele de donnees ProjectEmail, EmailTemplate | 3 | 1 | Creation des tables, migrations |
| API REST Emails (historique, envoi, templates) | 8 | 3 | Endpoints avec integration service email |
| Interface Emails projet (historique, envoi, templates) | 5 | 2.5 | Liste, detail, formulaire d'envoi, gestion templates |
| Adresse email dediee par projet (reception) | 5 | 2 | Configuration du service de reception et routage |
| Modele de donnees ActivityLog | 2 | 1 | Creation de la table, partitionnement |
| API REST Journal des actions (lecture, filtres, export) | 5 | 2 | Endpoints avec filtrage et export CSV/PDF |
| Interface journal des actions (timeline, filtres) | 5 | 2 | Timeline, filtres, recherche |
| Middleware de journalisation automatique | 5 | 2 | Intercepteurs pour enregistrement automatique des actions |
| Tests unitaires et d'integration Sprint 3 | 5 | 2 | Couverture des endpoints et composants |
| **Total Sprint 3** | **59** | **24.5** | |

#### Sprint 4 (Semaine 7) -- Recherche transversale, integration, stabilisation

| Element | Story Points | Jours/homme | Details |
|---------|-------------|-------------|---------|
| Moteur de recherche transversale | 8 | 3 | Integration Meilisearch, indexation multi-entites |
| Interface recherche globale (barre, resultats, filtres) | 5 | 2 | Composant recherche, page resultats, filtres avances |
| Integration avec EPIC-017 Notifications (evenements) | 5 | 2 | Emission des evenements declencheurs |
| Tests end-to-end (scenarios critiques) | 5 | 2 | Cypress/Playwright sur les parcours cles |
| Tests de performance | 3 | 1 | Validation des seuils de performance (section 8.1) |
| Corrections de bugs et stabilisation | 5 | 2 | Resolution des anomalies remontees par la QA |
| Revue de securite (droits d'acces, sanitization) | 3 | 1 | Audit des controles d'acces et de la protection XSS |
| Documentation API et guides utilisateurs | 3 | 1.5 | Swagger/OpenAPI, guide fonctionnel |
| **Total Sprint 4** | **37** | **14.5** | |

### 12.3 Synthese

| Sprint | Duree | Story Points | Jours/homme | Livrables cles |
|--------|-------|-------------|-------------|-----------------|
| Sprint 1 | 2 semaines | 42 | 16.5 | Taches (liste + kanban + filtres) |
| Sprint 2 | 2 semaines | 50 | 20.5 | Notes collaboratives + Fichiers (upload, versioning, preview) |
| Sprint 3 | 2 semaines | 59 | 24.5 | Blog + Emails projet + Journal des actions |
| Sprint 4 | 1 semaine | 37 | 14.5 | Recherche transversale + Integration + Stabilisation |
| **Total** | **7 semaines** | **188** | **76** | **Module Collaboration complet** |

### 12.4 Risques identifies

| Risque | Probabilite | Impact | Mitigation |
|--------|-------------|--------|------------|
| Complexite de l'editeur de texte riche (bugs, compatibilite navigateurs) | Moyenne | Moyen | Utiliser une librairie mature (TipTap), limiter les fonctionnalites dans la V1 |
| Performance de la recherche transversale sur gros volumes | Moyenne | Eleve | Utiliser un moteur dedie (Meilisearch), indexation asynchrone |
| Integration du service d'email (delivrabilite, reception) | Elevee | Eleve | Prototyper l'integration email des le Sprint 1, prevoir un plan de secours avec transfert manuel |
| Volume de stockage des fichiers (couts infrastructure) | Faible | Moyen | Implementer les quotas par projet, compression des fichiers archives |
| Dependance a l'EPIC-002 (Projets) et EPIC-009 (Collaborateurs) | Faible | Eleve | S'assurer que ces EPICs sont livres ou au minimum que les modeles de donnees sont disponibles |

### 12.5 Hypotheses et prerequis

- Les modules Projets (EPIC-002) et Collaborateurs (EPIC-009) sont livres ou en cours de livraison avant le demarrage du Sprint 1.
- L'infrastructure de stockage objet (S3/MinIO) est provisionee et accessible.
- Le service d'envoi d'emails (SendGrid/SES) est configure et operationnel.
- L'equipe dispose des competences necessaires sur les librairies front-end identifiees (editeur riche, drag-and-drop, viewer PDF).
- La capacite de l'equipe est de 8 jours/homme par developpeur par sprint de 2 semaines (en tenant compte des ceremonies agiles, des interruptions et du support).

---

*Document genere le 26/02/2026 -- Version 1.0*
*Application OOTI -- Module Collaboration (EPIC-015)*
