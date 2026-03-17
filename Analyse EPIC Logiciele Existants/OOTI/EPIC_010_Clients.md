# EPIC — Module Clients

**Application OOTI — Gestion de projets pour cabinets d'architecture**
**Version 1.0 — Fevrier 2026**

---

## 1. Identification

| Champ | Valeur |
|---|---|
| **Nom** | Clients |
| **Reference** | EPIC-010 |
| **Module parent** | Gestion |
| **Priorite** | Moyenne |
| **Proprietaire** | Chef de projet / Responsable administratif |
| **EPICs lies** | EPIC-001 Opportunites, EPIC-002 Projets, EPIC-004 Facturation |
| **Statut** | A planifier |
| **Date de creation** | 26/02/2026 |
| **Derniere mise a jour** | 26/02/2026 |

---

## 2. Contexte & Problematique

Les cabinets d'architecture entretiennent des relations commerciales avec une grande diversite de clients : maitres d'ouvrage prives ou publics, promoteurs immobiliers, entreprises, collectivites territoriales ou encore particuliers. La gestion efficace de ces relations est un levier fondamental pour la perennite et la croissance de l'activite du cabinet.

**Problematiques identifiees :**

- **Dispersion de l'information client** : les donnees relatives aux clients (coordonnees, informations legales, contacts, historique des projets) sont souvent reparties entre plusieurs outils (tableurs, messagerie, logiciels comptables), ce qui entraine des pertes d'information, des doublons et des erreurs de saisie.
- **Absence de vision consolidee** : les dirigeants et chefs de projet ne disposent pas d'une vue synthetique sur chaque client, regroupant a la fois les informations administratives, les projets en cours ou passes, et la situation financiere (CA genere, factures impayees, solde).
- **Difficulte de suivi des contacts** : un client peut impliquer plusieurs interlocuteurs (directeur technique, responsable de programme, assistant de maitrise d'ouvrage). L'absence de gestion structuree de ces contacts complique la communication et le suivi operationnel.
- **Categorisation insuffisante** : sans systeme de groupes ou d'etiquettes, il est difficile de segmenter la base clients pour des analyses ciblees (clients publics vs prives, clients recurrents, clients par zone geographique).
- **Manque de tracabilite financiere** : le lien entre un client et ses factures n'est pas toujours immediat, rendant complexe le suivi des encaissements, des retards de paiement et du chiffre d'affaires par client.
- **Processus d'import/export inexistants** : lors de la migration depuis un autre outil ou pour des besoins de reporting externe, l'absence de fonctionnalites d'import et d'export de la base clients constitue un frein operationnel.

Ces problematiques impactent directement la productivite administrative du cabinet, la qualite du suivi commercial et la fiabilite des indicateurs financiers.

---

## 3. Objectif

L'objectif de cet EPIC est de concevoir et implementer un **module Clients complet et centralise** au sein de l'application OOTI, permettant aux cabinets d'architecture de :

1. **Centraliser** l'ensemble des informations relatives a chaque client dans un referentiel unique et fiable.
2. **Structurer** les donnees clients avec des informations legales completes (raison sociale, SIRET/SIREN, numero de TVA, adresse de facturation).
3. **Gerer les contacts multiples** rattaches a chaque client, avec leurs coordonnees et leurs fonctions.
4. **Categoriser et segmenter** la base clients grace a un systeme de groupes et d'etiquettes.
5. **Visualiser la situation financiere** de chaque client (CA total, factures emises, montants payes, solde impaye).
6. **Assurer la tracabilite** des associations entre clients, projets et opportunites commerciales.
7. **Faciliter l'import et l'export** de donnees clients pour la migration et le reporting.
8. **Offrir des outils de recherche et de filtrage** performants pour exploiter efficacement la base clients.

Le module sera accessible depuis deux points d'entree dans l'application :
- **Gestion > Clients** : vue principale et complete du referentiel clients.
- **Factures > Clients** : vue financiere centree sur la facturation par client.

---

## 4. Perimetre Fonctionnel

### 4.1 Liste des clients

- Affichage tabulaire de l'ensemble des clients du cabinet.
- Colonnes affichees : nom du client, type (Prive, Public, Promoteur, Entreprise, Particulier), contact principal, nombre de projets associes, chiffre d'affaires total, solde impaye.
- Tri possible sur chaque colonne (ascendant/descendant).
- Pagination configurable (10, 25, 50, 100 elements par page).
- Selection multiple pour actions groupees (archivage, ajout d'etiquettes, export).

### 4.2 Creation, edition et archivage d'un client

- Formulaire de creation avec champs obligatoires et optionnels.
- Edition en ligne ou via la fiche client detaillee.
- Archivage logique (le client n'est pas supprime mais masque de la liste active).
- Possibilite de reactiver un client archive.
- Validation des donnees saisies (format SIRET, format TVA, email, telephone).

### 4.3 Fiche client detaillee

- Vue consolidee avec onglets ou sections :
  - **Informations generales** : nom, type, groupe, etiquettes.
  - **Informations legales** : raison sociale, SIRET/SIREN, numero de TVA intracommunautaire, adresse de facturation complete.
  - **Contacts** : liste des contacts rattaches au client.
  - **Projets associes** : liste des projets lies au client avec statut et montant.
  - **Opportunites associees** : liste des opportunites commerciales liees au client.
  - **Vue financiere** : synthese financiere (CA, factures, paiements, solde).
  - **Historique** : historique des interactions, des projets et des modifications.

### 4.4 Types de clients

- Classification des clients en cinq categories predefinies :
  - **Prive** : maitre d'ouvrage prive (societe, association).
  - **Public** : collectivite territoriale, etablissement public, Etat.
  - **Promoteur** : promoteur immobilier.
  - **Entreprise** : entreprise generale, sous-traitant, partenaire.
  - **Particulier** : personne physique.
- Possibilite d'ajouter des types personnalises par le cabinet (parametrage administrateur).

### 4.5 Informations legales

- Raison sociale / denomination sociale.
- Numero SIRET (14 chiffres) et SIREN (9 chiffres).
- Numero de TVA intracommunautaire.
- Adresse de facturation complete : rue, complement, code postal, ville, pays.
- Adresse de correspondance (si differente de l'adresse de facturation).

### 4.6 Contacts multiples par client

- Ajout, modification et suppression de contacts rattaches a un client.
- Informations par contact : prenom, nom, email, telephone fixe, telephone mobile, fonction/role.
- Designation d'un contact principal.
- Un contact ne peut etre rattache qu'a un seul client.

### 4.7 Groupes de clients et categorisation

- Creation et gestion de groupes de clients (ex : « Clients recurrents », « Collectivites IDF », « Grands comptes »).
- Attribution d'etiquettes (tags) libres a chaque client.
- Un client peut appartenir a plusieurs groupes et porter plusieurs etiquettes.
- Filtrage de la liste des clients par groupe ou par etiquette.

### 4.8 Associations client-projets et client-opportunites

- Association d'un ou plusieurs projets a un client.
- Association d'une ou plusieurs opportunites commerciales a un client.
- Visualisation bidirectionnelle : depuis la fiche client vers les projets/opportunites et inversement.
- Compteur du nombre de projets et d'opportunites sur la liste des clients.

### 4.9 Vue financiere par client

- Chiffre d'affaires total genere par le client (somme des montants factures).
- Nombre et montant total des factures emises.
- Montant total des paiements recus.
- Solde impaye (factures emises - paiements recus).
- Liste detaillee des factures avec statut (brouillon, emise, payee, en retard, annulee).
- Indicateur visuel pour les clients ayant des factures en retard de paiement.

### 4.10 Historique des interactions et projets

- Journal chronologique des evenements lies au client :
  - Creation du client.
  - Modification des informations.
  - Ajout/suppression de contacts.
  - Association/dissociation de projets.
  - Emission de factures.
  - Reception de paiements.
- Filtrage de l'historique par type d'evenement et par periode.

### 4.11 Import et export de clients

- **Import CSV** : import de clients depuis un fichier CSV avec mapping des colonnes, detection des doublons, rapport d'import (lignes importees, erreurs, doublons ignores).
- **Export CSV** : export de la liste des clients (tous ou selection filtree) au format CSV avec choix des colonnes a exporter.
- **Export PDF** : export de la fiche client individuelle au format PDF.

### 4.12 Recherche et filtrage

- Barre de recherche textuelle (recherche sur nom, raison sociale, SIRET, email de contact).
- Filtres combinables : par type de client, par groupe, par etiquette, par statut (actif/archive), par tranche de CA, par solde impaye (> 0).
- Sauvegarde des filtres favoris.
- Reinitialisation rapide des filtres.

---

## 5. User Stories

### US-CL01 : Liste des clients

**En tant que** gestionnaire du cabinet,
**je veux** visualiser la liste complete de tous les clients dans un tableau synthetique,
**afin de** disposer d'une vue d'ensemble rapide de la base clients et de pouvoir identifier les informations cles de chaque client.

**Criteres d'acceptation :**

1. Le tableau affiche les colonnes suivantes : nom du client, type (Prive/Public/Promoteur/Entreprise/Particulier), contact principal (nom + email), nombre de projets associes, CA total (en euros, formate avec separateur de milliers), solde impaye (en euros).
2. Chaque colonne est triable par ordre croissant et decroissant en cliquant sur l'en-tete de colonne. Un indicateur visuel (fleche) indique le sens du tri actif.
3. La pagination est configurable avec les options 10, 25, 50 et 100 elements par page. Le nombre total de clients et la page courante sont affiches.
4. Les clients archives sont masques par defaut de la liste. Un filtre permet d'afficher uniquement les clients archives ou tous les clients (actifs + archives).
5. Un clic sur le nom d'un client ouvre sa fiche detaillee (US-CL03).
6. Un bouton « Nouveau client » est present en haut de la liste et declenche le formulaire de creation (US-CL02).
7. La selection multiple de clients est possible via des cases a cocher. Les actions groupees disponibles sont : archiver, ajouter une etiquette, exporter la selection.
8. Le solde impaye est affiche en rouge lorsqu'il est superieur a zero, et une icone d'alerte est presente pour les clients ayant au moins une facture en retard de paiement de plus de 30 jours.

---

### US-CL02 : Creation d'un client

**En tant que** gestionnaire du cabinet,
**je veux** pouvoir creer un nouveau client en renseignant ses informations administratives et legales,
**afin de** l'integrer dans le referentiel clients et pouvoir l'associer ulterieurement a des projets et des factures.

**Criteres d'acceptation :**

1. Le formulaire de creation contient les champs suivants : nom du client (obligatoire), type de client (obligatoire, liste deroulante), raison sociale (obligatoire pour les types Prive, Public, Promoteur, Entreprise), SIRET (optionnel, 14 chiffres), SIREN (optionnel, 9 chiffres, auto-calcule a partir du SIRET si renseigne), numero de TVA intracommunautaire (optionnel, format valide selon le pays), adresse de facturation (rue, code postal, ville, pays).
2. La validation du SIRET verifie le format (14 chiffres) et la coherence avec le SIREN (les 9 premiers chiffres du SIRET correspondent au SIREN). Un message d'erreur explicite est affiche en cas de format invalide.
3. La validation du numero de TVA intracommunautaire verifie le format selon le pays selectionne (ex : FR suivi de 11 chiffres pour la France). Un message d'erreur explicite est affiche en cas de format invalide.
4. Le formulaire permet l'ajout immediat d'un premier contact principal (prenom, nom, email, telephone, fonction). Ce contact est marque comme contact principal du client.
5. Le formulaire permet l'attribution de groupes et d'etiquettes au moment de la creation.
6. Apres validation et enregistrement, le systeme redirige l'utilisateur vers la fiche client detaillee du client nouvellement cree.
7. En cas de doublon potentiel (nom ou SIRET identique a un client existant), le systeme affiche un avertissement et demande confirmation avant de poursuivre la creation.
8. Tous les champs obligatoires sont marques visuellement (asterisque rouge). Le bouton « Enregistrer » est desactive tant que les champs obligatoires ne sont pas remplis et valides.

---

### US-CL03 : Fiche client detaillee

**En tant que** chef de projet ou gestionnaire,
**je veux** acceder a une fiche client detaillee regroupant toutes les informations relatives a un client,
**afin de** disposer d'une vue complete et centralisee pour le suivi administratif, operationnel et financier de ce client.

**Criteres d'acceptation :**

1. La fiche client est organisee en sections ou onglets clairement identifies : Informations generales, Informations legales, Contacts, Projets, Opportunites, Finances, Historique.
2. La section « Informations generales » affiche le nom, le type, le groupe, les etiquettes et le statut (actif/archive) du client. Tous ces champs sont editables en ligne.
3. La section « Informations legales » affiche la raison sociale, le SIRET, le SIREN, le numero de TVA, l'adresse de facturation et l'adresse de correspondance. Tous ces champs sont editables en ligne avec les memes validations que le formulaire de creation.
4. La section « Contacts » affiche la liste des contacts rattaches au client avec leurs informations (prenom, nom, email, telephone, fonction, indicateur de contact principal). Des boutons permettent d'ajouter, modifier ou supprimer un contact.
5. La section « Projets » affiche la liste des projets associes au client sous forme de tableau (nom du projet, reference, statut, montant des honoraires). Un clic sur un projet redirige vers la fiche projet (EPIC-002).
6. La section « Opportunites » affiche la liste des opportunites commerciales liees au client (nom, statut, montant estime). Un clic redirige vers la fiche opportunite (EPIC-001).
7. La section « Finances » presente la synthese financiere du client conformement a US-CL06.
8. La section « Historique » affiche le journal chronologique de tous les evenements lies au client (creation, modifications, factures, paiements), avec filtrage par type d'evenement et par periode.

---

### US-CL04 : Gestion des contacts client

**En tant que** gestionnaire du cabinet,
**je veux** pouvoir ajouter, modifier et supprimer des contacts rattaches a un client,
**afin de** maintenir a jour la liste des interlocuteurs et faciliter la communication sur les projets.

**Criteres d'acceptation :**

1. Depuis la fiche client, un bouton « Ajouter un contact » ouvre un formulaire contenant les champs : prenom (obligatoire), nom (obligatoire), email (obligatoire, format email valide), telephone fixe (optionnel), telephone mobile (optionnel), fonction/role au sein de l'organisation du client (optionnel, texte libre ou liste predefinies : Directeur, Chef de projet, Responsable technique, Comptable, Autre).
2. Un client peut avoir un nombre illimite de contacts. Un et un seul contact doit etre designe comme contact principal. Lors de l'ajout du premier contact, celui-ci est automatiquement designe comme contact principal.
3. La modification d'un contact existant est possible en cliquant sur le contact dans la liste. Les memes validations que lors de la creation s'appliquent.
4. La suppression d'un contact demande une confirmation. Si le contact supprime etait le contact principal, le systeme demande a l'utilisateur de designer un nouveau contact principal parmi les contacts restants.
5. Le contact principal du client est affiche en premier dans la liste des contacts et est visuellement identifiable (badge ou icone « Principal »).
6. L'adresse email de chaque contact est unique au sein de la base de donnees (un meme email ne peut pas etre utilise pour deux contacts differents). Un message d'erreur explicite est affiche en cas de doublon.
7. Les informations du contact principal sont automatiquement reprises dans la colonne « Contact » de la liste des clients (US-CL01).
8. Un lien « Envoyer un email » est disponible sur chaque contact, ouvrant le client de messagerie par defaut de l'utilisateur avec l'adresse email pre-remplie.

---

### US-CL05 : Groupes et categorisation de clients

**En tant que** directeur du cabinet ou responsable commercial,
**je veux** pouvoir creer des groupes de clients et attribuer des etiquettes a chaque client,
**afin de** segmenter et organiser la base clients pour des analyses ciblees et un suivi personnalise.

**Criteres d'acceptation :**

1. Un ecran de gestion des groupes de clients est accessible depuis les parametres du module Clients ou directement depuis la liste des clients. Il permet de creer, modifier, renommer et supprimer des groupes.
2. Chaque groupe a un nom (obligatoire, unique) et une description (optionnelle). La suppression d'un groupe n'entraine pas la suppression des clients qui y sont rattaches ; ceux-ci sont simplement dissocies du groupe.
3. Un client peut etre rattache a un ou plusieurs groupes simultanement. L'attribution ou le retrait d'un groupe s'effectue depuis la fiche client ou par action groupee depuis la liste des clients.
4. Les etiquettes (tags) sont des mots-cles libres attribues a un client. L'ajout d'une etiquette se fait par saisie libre avec autocompletion sur les etiquettes existantes. Plusieurs etiquettes peuvent etre attribuees a un meme client.
5. La liste des clients est filtrable par groupe et/ou par etiquette. Les filtres sont combinables entre eux et avec les autres filtres disponibles (type, statut, CA, solde).
6. Le nombre de clients dans chaque groupe est affiche dans la liste des groupes.
7. Les groupes et etiquettes sont visibles sur la fiche client (section Informations generales) et sont editables en ligne.
8. L'ajout ou le retrait d'un groupe ou d'une etiquette est trace dans l'historique du client.

---

### US-CL06 : Vue financiere par client

**En tant que** gestionnaire administratif et financier du cabinet,
**je veux** visualiser la synthese financiere de chaque client,
**afin de** suivre le chiffre d'affaires genere, l'etat des factures et les eventuels impayes pour optimiser le suivi de tresorerie.

**Criteres d'acceptation :**

1. La vue financiere est accessible depuis la fiche client (onglet ou section « Finances ») et depuis le menu Factures > Clients (vue listant tous les clients avec leurs indicateurs financiers).
2. Les indicateurs affiches pour chaque client sont : chiffre d'affaires total (somme des montants HT factures), montant total des factures emises (TTC), montant total des paiements recus, solde impaye (factures emises TTC - paiements recus), nombre de factures par statut (brouillon, emise, payee, en retard, annulee).
3. La liste detaillee des factures du client est affichee sous les indicateurs, avec pour chaque facture : numero, date d'emission, date d'echeance, montant HT, montant TTC, statut, montant paye. Un clic sur une facture redirige vers le detail de la facture (EPIC-004).
4. Un code couleur permet d'identifier rapidement le statut de chaque facture : vert (payee), orange (emise, en attente), rouge (en retard), gris (brouillon), barre (annulee).
5. Un indicateur visuel d'alerte (icone et couleur rouge) est affiche lorsque le client a un solde impaye et/ou des factures en retard de paiement de plus de 30 jours.
6. La vue « Factures > Clients » affiche un tableau listant tous les clients avec les colonnes : nom du client, CA total, total facture, total paye, solde impaye, nombre de factures en retard. Ce tableau est triable et filtrable.
7. Les montants sont affiches en euros, formates avec deux decimales et separateur de milliers (espace insecable). Le symbole de la devise est affiche.
8. Un graphique optionnel (histogramme ou courbe) permet de visualiser l'evolution du CA par client sur les 12 derniers mois.

---

### US-CL07 : Association clients-projets

**En tant que** chef de projet,
**je veux** pouvoir associer un client a un ou plusieurs projets et visualiser ces associations,
**afin de** maintenir la coherence du referentiel et retrouver facilement les projets d'un client donne.

**Criteres d'acceptation :**

1. Depuis la fiche client, la section « Projets » affiche la liste de tous les projets associes au client. Un bouton « Associer un projet » permet de lier un projet existant au client via une recherche par nom ou reference de projet.
2. Depuis la fiche projet (EPIC-002), le champ « Client » permet de selectionner un client existant dans le referentiel. La modification du client associe a un projet est possible et tracee dans l'historique.
3. Un projet ne peut etre associe qu'a un seul client. Un client peut etre associe a un nombre illimite de projets.
4. La dissociation d'un projet d'un client est possible depuis la fiche client. Une confirmation est demandee avant la dissociation. L'evenement est trace dans l'historique du client et du projet.
5. Le nombre de projets associes a un client est affiche dans la liste des clients (colonne « Nb projets ») et est mis a jour en temps reel lors de l'ajout ou de la suppression d'une association.
6. Les projets associes sont affiches dans la fiche client avec les informations suivantes : nom du projet, reference, statut (en cours, termine, archive), montant des honoraires, date de debut et date de fin prevue.
7. De la meme maniere, les opportunites commerciales (EPIC-001) peuvent etre associees a un client. La logique est identique : une opportunite est liee a un seul client, un client peut avoir plusieurs opportunites.
8. Un filtre dans la liste des clients permet de filtrer les clients ayant au moins un projet actif, les clients sans projet, ou les clients dont tous les projets sont termines.

---

### US-CL08 : Import et export de clients

**En tant que** administrateur du cabinet,
**je veux** pouvoir importer des clients depuis un fichier CSV et exporter la base clients vers un fichier CSV ou PDF,
**afin de** faciliter la migration depuis un autre outil et de produire des rapports exploitables en dehors de l'application.

**Criteres d'acceptation :**

1. **Import CSV** : un bouton « Importer » dans la liste des clients ouvre un assistant d'import en 3 etapes : (1) selection du fichier CSV, (2) mapping des colonnes du CSV vers les champs du systeme (nom, type, raison sociale, SIRET, TVA, adresse, contact principal), (3) apercu et validation avant import.
2. L'assistant d'import detecte les doublons potentiels (basee sur le nom ou le SIRET) et propose trois options pour chaque doublon : ignorer la ligne, creer un nouveau client, mettre a jour le client existant.
3. A l'issue de l'import, un rapport est affiche indiquant : le nombre de clients importes avec succes, le nombre de doublons detectes (et le traitement choisi), le nombre de lignes en erreur avec le detail des erreurs (format invalide, champ obligatoire manquant). Le rapport est telechargeble en CSV.
4. Les encodages UTF-8 et ISO-8859-1 (Latin-1) sont supportes pour les fichiers CSV importes. Le separateur (virgule, point-virgule, tabulation) est detecte automatiquement ou selectionnable manuellement.
5. **Export CSV** : un bouton « Exporter » dans la liste des clients permet d'exporter l'ensemble des clients affiches (selon les filtres actifs) au format CSV. L'utilisateur peut selectionner les colonnes a inclure dans l'export.
6. **Export PDF** : depuis la fiche client, un bouton « Exporter en PDF » genere un document PDF contenant toutes les informations du client (informations generales, legales, contacts, liste des projets, synthese financiere).
7. L'import et l'export sont accessibles uniquement aux utilisateurs ayant le role administrateur ou gestionnaire. Les utilisateurs avec un role « Lecture seule » ne voient pas ces boutons.
8. L'import de plus de 500 clients declenche un traitement asynchrone (en arriere-plan). L'utilisateur est notifie par une notification dans l'application lorsque l'import est termine.

---

### US-CL09 : Recherche et filtrage

**En tant que** utilisateur de l'application,
**je veux** pouvoir rechercher et filtrer les clients selon differents criteres,
**afin de** retrouver rapidement un client specifique ou un sous-ensemble de clients correspondant a des criteres particuliers.

**Criteres d'acceptation :**

1. Une barre de recherche textuelle est presente en haut de la liste des clients. La recherche s'effectue en temps reel (debounce de 300 ms) sur les champs suivants : nom du client, raison sociale, SIRET, SIREN, email du contact principal.
2. La recherche est insensible a la casse et aux accents (ex : « ecole » trouve « Ecole » et « Ecole »). Les resultats sont mis en surbrillance dans le tableau.
3. Des filtres sont disponibles sous forme de menus deroulants ou de panneaux lateraux et sont combinables entre eux : type de client (multi-selection), groupe (multi-selection), etiquette (multi-selection), statut (Actif / Archive / Tous), tranche de CA (< 10k euros, 10k-50k euros, 50k-100k euros, > 100k euros, personnalise), solde impaye (= 0, > 0, > seuil personnalise).
4. Les filtres actifs sont affiches sous forme de badges en haut de la liste. Chaque badge est supprimable individuellement en cliquant sur une croix.
5. Un bouton « Reinitialiser les filtres » permet de supprimer tous les filtres actifs en un clic et de revenir a l'affichage par defaut (tous les clients actifs).
6. L'utilisateur peut sauvegarder une combinaison de filtres en tant que « Vue enregistree » (nom personnalise). Les vues enregistrees sont accessibles depuis un menu deroulant et permettent de retrouver rapidement un jeu de filtres frequemment utilise.
7. Le nombre de resultats correspondant aux filtres actifs est affiche en temps reel (ex : « 42 clients trouves sur 156 »).
8. L'URL de la page integre les parametres de recherche et de filtrage, permettant de partager un lien direct vers une vue filtree de la liste des clients.

---

## 6. Hors Perimetre

Les elements suivants sont explicitement **hors du perimetre** de cet EPIC et pourront faire l'objet d'evolutions ulterieures :

| Element | Raison de l'exclusion |
|---|---|
| **CRM complet (pipeline commercial, relances automatiques, scoring)** | Necessite un module CRM dedie, hors du scope d'un referentiel clients |
| **Gestion des contrats et conventions** | Releve d'un module contractuel distinct (EPIC futur) |
| **Portail client en ligne (acces externe)** | Necessite une architecture specifique (portail web, authentification externe) |
| **Synchronisation avec des annuaires externes (LDAP, Google Contacts)** | Pourra etre ajoute en phase 2 selon les besoins identifies |
| **Gestion des litiges et contentieux** | Releve d'un module juridique distinct |
| **Envoi d'emails ou de SMS depuis l'application** | L'application fournit uniquement un lien vers le client de messagerie |
| **Geolocalisation des clients sur une carte** | Fonctionnalite de confort envisageable en phase 2 |
| **Fusion de doublons de clients** | Fonctionnalite avancee planifiee dans un sprint ulterieur |
| **Historique des appels telephoniques** | Necessite une integration telephonique (CTI) hors perimetre |
| **Gestion des mandataires / sous-traitants du client** | Complexite elevee, a traiter dans une evolution future |

---

## 7. Regles Metier

### RM-CL01 : Unicite du client
Un client est identifie de maniere unique par son identifiant technique (UUID). Le couple (nom + SIRET) doit etre unique dans la base de donnees. En cas de tentative de creation d'un doublon, un avertissement est affiche mais la creation n'est pas bloquee (l'utilisateur peut confirmer la creation apres avertissement).

### RM-CL02 : Types de clients
Les types de clients predefinis sont : Prive, Public, Promoteur, Entreprise, Particulier. Le type est obligatoire a la creation. Un administrateur peut ajouter des types personnalises depuis les parametres du module. Le type d'un client peut etre modifie apres creation.

### RM-CL03 : Informations legales obligatoires
Pour les clients de type Prive, Public, Promoteur et Entreprise, la raison sociale est obligatoire. Pour les clients de type Particulier, le nom suffit (la raison sociale est optionnelle). Le SIRET et le numero de TVA sont optionnels quel que soit le type, mais leur format est valide s'ils sont renseignes.

### RM-CL04 : Validation du SIRET
Le SIRET est compose de 14 chiffres. Les 9 premiers chiffres correspondent au SIREN. La validation s'effectue sur le format uniquement (pas de verification aupres de l'INSEE). Si le SIRET est renseigne, le SIREN est deduit automatiquement (9 premiers chiffres).

### RM-CL05 : Validation du numero de TVA
Le numero de TVA intracommunautaire est valide selon le format du pays selectionne. Pour la France : « FR » suivi de 2 chiffres (cle) et du SIREN (9 chiffres), soit 13 caracteres au total. Pour les autres pays de l'UE, la validation s'appuie sur les formats officiels.

### RM-CL06 : Contact principal
Chaque client doit avoir au maximum un contact principal. Le premier contact ajoute est automatiquement designe comme contact principal. Si le contact principal est supprime, l'utilisateur doit en designer un nouveau parmi les contacts restants. Si le client n'a plus aucun contact, le champ « Contact principal » de la liste des clients est vide.

### RM-CL07 : Archivage d'un client
L'archivage d'un client est une operation logique (soft delete). Le client archive n'apparait plus dans la liste par defaut, mais reste accessible via le filtre « Archives ». Un client archive ne peut plus etre associe a un nouveau projet ou une nouvelle facture. Les projets et factures existants conservent leur association au client archive. Un client archive peut etre reactive a tout moment.

### RM-CL08 : Suppression d'un client
La suppression definitive d'un client n'est pas autorisee si des projets ou des factures lui sont associes. Seuls les clients sans aucune association (projets, opportunites, factures) peuvent etre supprimes definitivement. La suppression definitive est reservee aux administrateurs.

### RM-CL09 : Calcul du CA total
Le chiffre d'affaires total d'un client est calcule comme la somme des montants HT de toutes les factures ayant le statut « Emise » ou « Payee ». Les factures en brouillon ou annulees ne sont pas comptabilisees. Le CA est recalcule en temps reel a chaque changement de statut d'une facture.

### RM-CL10 : Calcul du solde impaye
Le solde impaye est calcule comme la somme des montants TTC des factures emises (statut « Emise » ou « En retard ») moins la somme des paiements recus. Un solde impaye negatif (trop-percu) est affiche en vert avec la mention « Avoir ».

### RM-CL11 : Facture en retard
Une facture est consideree « En retard » lorsque la date d'echeance est depassee et que le paiement integral n'a pas ete recu. Le statut passe automatiquement de « Emise » a « En retard » lors du depassement de la date d'echeance (traitement quotidien ou temps reel).

### RM-CL12 : Etiquettes et groupes
Les etiquettes (tags) sont des chaines de caracteres libres, limitees a 50 caracteres, en minuscules, sans caracteres speciaux (lettres, chiffres, tirets uniquement). Les groupes ont un nom unique, limite a 100 caracteres. La suppression d'un groupe ne supprime pas les clients associes.

### RM-CL13 : Droits d'acces
Tous les utilisateurs authentifies peuvent consulter la liste des clients et les fiches clients (lecture). La creation, la modification et l'archivage de clients sont reserves aux roles « Gestionnaire » et « Administrateur ». L'import/export et la suppression definitive sont reserves au role « Administrateur ».

---

## 8. Criteres Globaux

### 8.1 Performance

- Le chargement de la liste des clients (jusqu'a 10 000 clients) doit s'effectuer en moins de 2 secondes.
- La recherche textuelle doit retourner des resultats en moins de 500 ms apres la fin de la saisie (debounce de 300 ms inclus).
- L'import de 500 clients depuis un fichier CSV doit s'effectuer en moins de 30 secondes.
- L'export CSV de 10 000 clients doit s'effectuer en moins de 10 secondes.
- La generation d'un PDF de fiche client doit s'effectuer en moins de 3 secondes.

### 8.2 Securite

- Toutes les operations de creation, modification, archivage et suppression sont soumises au controle des droits d'acces (RM-CL13).
- Les donnees sensibles (SIRET, TVA, adresses) sont transmises via HTTPS uniquement.
- Les operations sensibles (suppression, archivage groupes, import) sont tracees dans un journal d'audit.
- La validation cote serveur est systematique (ne pas se fier uniquement a la validation cote client).
- Protection contre les injections SQL et XSS sur tous les champs de saisie.

### 8.3 Accessibilite

- Conformite WCAG 2.1 niveau AA.
- Navigation complete au clavier dans le tableau et les formulaires.
- Labels associes a tous les champs de formulaire.
- Contrastes de couleurs suffisants pour les indicateurs visuels (alertes, badges).
- Messages d'erreur accessibles aux lecteurs d'ecran (role="alert").

### 8.4 Compatibilite

- Navigateurs supportes : Chrome (2 dernieres versions), Firefox (2 dernieres versions), Safari (2 dernieres versions), Edge (2 dernieres versions).
- Design responsive : le module doit etre utilisable sur tablette (largeur >= 768px). L'usage sur mobile (< 768px) est en mode consultation uniquement (pas de creation/edition).

### 8.5 Internationalisation

- L'interface utilisateur est en francais par defaut.
- Les formats de donnees respectent les conventions locales : dates (JJ/MM/AAAA), montants (1 234,56 euros), separateurs (espace insecable pour les milliers, virgule pour les decimales).
- Les validations de format (SIRET, TVA) s'adaptent au pays selectionne.

---

## 9. Definition of Done (DoD)

Un User Story est considere comme **termine** lorsque l'ensemble des conditions suivantes sont remplies :

- [ ] Tous les criteres d'acceptation du User Story sont implementes et verifies.
- [ ] Le code est revise par au moins un pair (code review approuvee).
- [ ] Les tests unitaires sont ecrits et couvrent au minimum 80 % du code metier.
- [ ] Les tests d'integration sont ecrits et couvrent les principaux flux fonctionnels.
- [ ] Les tests de bout en bout (E2E) couvrent le parcours utilisateur principal du User Story.
- [ ] Les validations cote client et cote serveur sont implementees et coherentes.
- [ ] La gestion des erreurs est implementee avec des messages utilisateur explicites et localises.
- [ ] Les regles metier associees au User Story sont implementees et testees.
- [ ] Le User Story est deploye sur l'environnement de recette et valide par le Product Owner.
- [ ] La documentation technique (API, modele de donnees) est a jour.
- [ ] Les criteres de performance sont respectes (temps de chargement, temps de reponse).
- [ ] L'accessibilite (WCAG 2.1 AA) est verifiee sur les composants concernes.
- [ ] La compatibilite navigateurs est verifiee (Chrome, Firefox, Safari, Edge).
- [ ] Aucune regression n'est detectee sur les fonctionnalites existantes.
- [ ] Le journal d'audit trace les operations sensibles conformement aux regles metier.

---

## 10. Dependances

### 10.1 Dependances entrantes (ce dont le module Clients depend)

| Dependance | Module / EPIC | Description |
|---|---|---|
| **Authentification et gestion des roles** | Module Utilisateurs | Le controle des droits d'acces (RM-CL13) necessite un systeme d'authentification et de gestion des roles fonctionnel. |
| **Module Facturation** | EPIC-004 | La vue financiere par client (US-CL06) s'appuie sur les donnees de facturation (factures emises, paiements recus, statuts de factures). |
| **Module Projets** | EPIC-002 | L'association client-projets (US-CL07) necessite que le module Projets soit operationnel et expose les donnees de projets. |
| **Module Opportunites** | EPIC-001 | L'association client-opportunites necessite que le module Opportunites soit operationnel. |
| **Infrastructure technique** | Architecture generale | Base de donnees relationnelle, API REST, systeme de fichiers pour l'import/export, generateur de PDF. |

### 10.2 Dependances sortantes (modules qui dependent du module Clients)

| Dependance | Module / EPIC | Description |
|---|---|---|
| **Module Projets** | EPIC-002 | La creation ou l'edition d'un projet necessite la selection d'un client existant dans le referentiel. |
| **Module Facturation** | EPIC-004 | La creation d'une facture necessite la selection d'un client et la reprise de ses informations legales et d'adresse de facturation. |
| **Module Opportunites** | EPIC-001 | La creation d'une opportunite commerciale necessite la selection d'un client existant. |
| **Module Reporting / Tableaux de bord** | EPIC futur | Les indicateurs de CA par client, repartition par type, clients actifs/archives alimentent les tableaux de bord. |

### 10.3 Dependances techniques

| Composant | Technologie / Outil | Usage |
|---|---|---|
| **Base de donnees** | PostgreSQL | Stockage des entites Client, Contact, ClientGroup, associations. |
| **API REST** | Backend (Django REST / Node.js) | Endpoints CRUD pour clients, contacts, groupes, import/export. |
| **Generateur PDF** | Librairie PDF (WeasyPrint, Puppeteer) | Generation de la fiche client en PDF (US-CL08). |
| **Parseur CSV** | Librairie CSV | Parsing et generation de fichiers CSV pour l'import/export. |
| **Frontend** | React / Vue.js | Interface utilisateur du module Clients. |
| **Recherche** | PostgreSQL Full-Text Search ou Elasticsearch | Recherche textuelle performante sur la base clients. |

---

## 11. Modele de Donnees

### 11.1 Entite `Client`

| Champ | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK, auto-genere | Identifiant unique du client |
| `name` | VARCHAR(255) | NOT NULL | Nom du client |
| `type` | ENUM | NOT NULL, valeurs : 'private', 'public', 'promoter', 'company', 'individual' | Type de client |
| `legal_name` | VARCHAR(255) | NULL | Raison sociale / denomination sociale |
| `siret` | CHAR(14) | NULL, format valide (14 chiffres) | Numero SIRET |
| `siren` | CHAR(9) | NULL, auto-calcule depuis SIRET | Numero SIREN |
| `vat_number` | VARCHAR(20) | NULL, format valide selon pays | Numero de TVA intracommunautaire |
| `billing_address_street` | VARCHAR(500) | NULL | Adresse de facturation — rue |
| `billing_address_complement` | VARCHAR(255) | NULL | Adresse de facturation — complement |
| `billing_address_postal_code` | VARCHAR(10) | NULL | Adresse de facturation — code postal |
| `billing_address_city` | VARCHAR(255) | NULL | Adresse de facturation — ville |
| `billing_address_country` | VARCHAR(100) | NULL, defaut : 'France' | Adresse de facturation — pays |
| `correspondence_address` | JSONB | NULL | Adresse de correspondance (si differente) |
| `tags` | JSONB / TEXT[] | NULL, defaut : [] | Liste des etiquettes (tags) |
| `status` | ENUM | NOT NULL, defaut : 'active', valeurs : 'active', 'archived' | Statut du client |
| `primary_contact_id` | UUID | FK → Contact(id), NULL | Reference vers le contact principal |
| `created_by` | UUID | FK → User(id), NOT NULL | Utilisateur ayant cree le client |
| `created_at` | TIMESTAMP | NOT NULL, auto-genere | Date de creation |
| `updated_at` | TIMESTAMP | NOT NULL, auto-maj | Date de derniere modification |

**Index :**
- Index unique sur `(name, siret)` WHERE `siret IS NOT NULL`
- Index sur `type`
- Index sur `status`
- Index GIN sur `tags` (pour la recherche par etiquette)
- Index full-text sur `(name, legal_name)`

---

### 11.2 Entite `Contact`

| Champ | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK, auto-genere | Identifiant unique du contact |
| `client_id` | UUID | FK → Client(id), NOT NULL, ON DELETE CASCADE | Client rattache |
| `first_name` | VARCHAR(100) | NOT NULL | Prenom |
| `last_name` | VARCHAR(100) | NOT NULL | Nom |
| `email` | VARCHAR(255) | NOT NULL, UNIQUE, format email valide | Adresse email |
| `phone_fixed` | VARCHAR(20) | NULL | Telephone fixe |
| `phone_mobile` | VARCHAR(20) | NULL | Telephone mobile |
| `role` | VARCHAR(100) | NULL | Fonction / role au sein du client |
| `is_primary` | BOOLEAN | NOT NULL, defaut : FALSE | Indicateur de contact principal |
| `created_at` | TIMESTAMP | NOT NULL, auto-genere | Date de creation |
| `updated_at` | TIMESTAMP | NOT NULL, auto-maj | Date de derniere modification |

**Index :**
- Index unique sur `email`
- Index sur `client_id`
- Index sur `(client_id, is_primary)` WHERE `is_primary = TRUE`

**Contrainte :** au maximum un contact avec `is_primary = TRUE` par `client_id` (contrainte applicative ou trigger).

---

### 11.3 Entite `ClientGroup`

| Champ | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK, auto-genere | Identifiant unique du groupe |
| `name` | VARCHAR(100) | NOT NULL, UNIQUE | Nom du groupe |
| `description` | TEXT | NULL | Description du groupe |
| `created_at` | TIMESTAMP | NOT NULL, auto-genere | Date de creation |
| `updated_at` | TIMESTAMP | NOT NULL, auto-maj | Date de derniere modification |

---

### 11.4 Table d'association `ClientGroupMembership`

| Champ | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK, auto-genere | Identifiant unique |
| `client_id` | UUID | FK → Client(id), NOT NULL, ON DELETE CASCADE | Client membre |
| `group_id` | UUID | FK → ClientGroup(id), NOT NULL, ON DELETE CASCADE | Groupe |
| `created_at` | TIMESTAMP | NOT NULL, auto-genere | Date d'ajout au groupe |

**Contrainte :** Unicite sur `(client_id, group_id)`.

---

### 11.5 Table d'association `ClientProject`

| Champ | Type | Contraintes | Description |
|---|---|---|---|
| `client_id` | UUID | FK → Client(id), NOT NULL | Client |
| `project_id` | UUID | FK → Project(id), NOT NULL | Projet (EPIC-002) |

**Contrainte :** PK composite sur `(client_id, project_id)`.

> **Note :** Si la regle metier impose qu'un projet n'a qu'un seul client, alors `client_id` est directement un champ de la table `Project` (FK → Client). La table d'association n'est necessaire que si un projet peut avoir plusieurs clients (co-maitrise d'ouvrage). Le choix final sera confirme lors du design technique.

---

### 11.6 Table `ClientHistory`

| Champ | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK, auto-genere | Identifiant unique de l'evenement |
| `client_id` | UUID | FK → Client(id), NOT NULL, ON DELETE CASCADE | Client concerne |
| `event_type` | ENUM | NOT NULL, valeurs : 'created', 'updated', 'contact_added', 'contact_removed', 'project_associated', 'project_dissociated', 'invoice_created', 'payment_received', 'archived', 'reactivated' | Type d'evenement |
| `event_data` | JSONB | NULL | Donnees complementaires (champs modifies, ancien/nouveau valeur) |
| `performed_by` | UUID | FK → User(id), NOT NULL | Utilisateur ayant effectue l'action |
| `performed_at` | TIMESTAMP | NOT NULL, auto-genere | Date et heure de l'evenement |

**Index :**
- Index sur `client_id`
- Index sur `event_type`
- Index sur `performed_at`

---

### 11.7 Diagramme relationnel (representation textuelle)

```
┌──────────────────┐       ┌──────────────────┐
│    ClientGroup    │       │      Client       │
├──────────────────┤       ├──────────────────┤
│ id (PK)          │       │ id (PK)          │
│ name             │       │ name             │
│ description      │       │ type             │
└────────┬─────────┘       │ legal_name       │
         │                 │ siret            │
         │ N:M             │ siren            │
         │                 │ vat_number       │
┌────────┴─────────┐       │ billing_address  │
│ ClientGroup      │       │ tags[]           │
│ Membership       │       │ status           │
├──────────────────┤       │ primary_contact  │───┐
│ client_id (FK)   │───────│ created_by       │   │
│ group_id (FK)    │       │ created_at       │   │
└──────────────────┘       │ updated_at       │   │
                           └──────┬───────────┘   │
                                  │               │
                        1:N       │          1:1  │
                                  │               │
                           ┌──────┴───────────┐   │
                           │     Contact       │◄──┘
                           ├──────────────────┤
                           │ id (PK)          │
                           │ client_id (FK)   │
                           │ first_name       │
                           │ last_name        │
                           │ email            │
                           │ phone_fixed      │
                           │ phone_mobile     │
                           │ role             │
                           │ is_primary       │
                           └──────────────────┘

┌──────────────────┐       ┌──────────────────┐
│  ClientProject   │       │  ClientHistory   │
├──────────────────┤       ├──────────────────┤
│ client_id (FK)   │       │ id (PK)          │
│ project_id (FK)  │       │ client_id (FK)   │
└──────────────────┘       │ event_type       │
                           │ event_data       │
                           │ performed_by     │
                           │ performed_at     │
                           └──────────────────┘
```

---

## 12. Estimation

### 12.1 Estimation globale

| Indicateur | Valeur |
|---|---|
| **Duree totale estimee** | 3 a 4 semaines (15 a 20 jours ouvrables) |
| **Nombre de sprints** | 2 sprints de 2 semaines |
| **Complexite globale** | Moyenne |
| **Taille de l'equipe recommandee** | 2 developpeurs full-stack + 1 QA |

### 12.2 Estimation par User Story

| User Story | Ref | Complexite | Story Points | Estimation (jours) | Sprint |
|---|---|---|---|---|---|
| Liste des clients | US-CL01 | Moyenne | 5 | 2 | Sprint 1 |
| Creation d'un client | US-CL02 | Moyenne | 5 | 2,5 | Sprint 1 |
| Fiche client detaillee | US-CL03 | Elevee | 8 | 3 | Sprint 1 |
| Gestion des contacts client | US-CL04 | Moyenne | 5 | 2 | Sprint 1 |
| Groupes et categorisation | US-CL05 | Faible | 3 | 1,5 | Sprint 1 |
| Vue financiere par client | US-CL06 | Elevee | 8 | 3 | Sprint 2 |
| Association clients-projets | US-CL07 | Moyenne | 5 | 2 | Sprint 2 |
| Import/export de clients | US-CL08 | Elevee | 8 | 3 | Sprint 2 |
| Recherche et filtrage | US-CL09 | Moyenne | 5 | 2 | Sprint 2 |
| **Total** | | | **52** | **21 jours** | |

### 12.3 Repartition par sprint

**Sprint 1 (semaines 1-2) — Fondations et CRUD**

| Tache | Jours |
|---|---|
| Mise en place du modele de donnees (Client, Contact, ClientGroup, associations, historique) | 1,5 |
| Developpement des endpoints API (CRUD clients, contacts, groupes) | 2 |
| US-CL01 : Liste des clients (frontend) | 2 |
| US-CL02 : Formulaire de creation/edition (frontend + validations) | 2,5 |
| US-CL03 : Fiche client detaillee (frontend, onglets, edition en ligne) | 3 |
| US-CL04 : Gestion des contacts (frontend + API) | 2 |
| US-CL05 : Groupes et etiquettes (frontend + API) | 1,5 |
| Tests unitaires et d'integration Sprint 1 | 1,5 |
| **Total Sprint 1** | **16 jours-homme** |

**Sprint 2 (semaines 3-4) — Fonctionnalites avancees et finalisation**

| Tache | Jours |
|---|---|
| US-CL06 : Vue financiere par client (integration facturation, indicateurs, graphiques) | 3 |
| US-CL07 : Associations clients-projets et clients-opportunites (frontend + API) | 2 |
| US-CL08 : Import CSV (assistant, mapping, detection doublons, rapport) | 2 |
| US-CL08 : Export CSV et PDF | 1,5 |
| US-CL09 : Recherche textuelle et filtrage avance (frontend + API + indexation) | 2 |
| Vue « Factures > Clients » (integration dans le module Facturation) | 1 |
| Tests unitaires, d'integration et E2E Sprint 2 | 2 |
| Recette fonctionnelle, corrections de bugs, ajustements UI | 1,5 |
| **Total Sprint 2** | **15 jours-homme** |

### 12.4 Risques et hypotheses

| Risque | Impact | Probabilite | Mitigation |
|---|---|---|---|
| Indisponibilite des API Facturation (EPIC-004) | La vue financiere sera incomplete | Moyenne | Developper US-CL06 avec des donnees mockees ; integrer les API reelles des qu'elles sont disponibles |
| Volume important de clients a l'import (> 5 000) | Problemes de performance a l'import | Faible | Implementer le traitement asynchrone et la pagination des lors du Sprint 2 |
| Complexite du mapping CSV lors de l'import | Retard sur US-CL08 | Moyenne | Limiter le mapping a un ensemble de colonnes predefinies en v1 ; le mapping libre sera une evolution |
| Changements dans le modele de donnees Projets (EPIC-002) | Impact sur les associations client-projet | Faible | Definir une interface (contrat API) stable avec l'equipe Projets avant le debut du Sprint 2 |

### 12.5 Hypotheses

- Le module Utilisateurs (authentification, roles) est operationnel avant le debut du Sprint 1.
- Le module Projets (EPIC-002) expose a minima un endpoint de liste des projets (id, nom, reference, statut) avant le Sprint 2.
- Le module Facturation (EPIC-004) expose a minima les endpoints de consultation des factures et paiements par client avant la fin du Sprint 2.
- L'equipe dispose d'un environnement de developpement et de recette fonctionnel.
- La charte graphique et le design system de l'application sont definis et disponibles.

---

*Document redige le 26 fevrier 2026 — Version 1.0*
*EPIC-010 — Module Clients — Application OOTI*
