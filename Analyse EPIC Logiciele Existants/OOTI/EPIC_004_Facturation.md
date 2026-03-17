# EPIC -- Module Facturation

**Application OOTI -- Gestion de projets pour cabinets d'architecture**
**Version 1.0 -- Fevrier 2026**

---

## 1. Identification de l'EPIC

| Champ | Valeur |
|---|---|
| **Nom** | Facturation |
| **Reference** | EPIC-004 |
| **Module parent** | Gestion |
| **Priorite** | Haute |
| **Statut** | A planifier |
| **Date de creation** | Fevrier 2026 |
| **EPICs lies** | EPIC-002 (Projets), EPIC-003 (Honoraires), EPIC-008 (Finances) |
| **Responsable fonctionnel** | A definir |
| **Equipe estimee** | 3-4 developpeurs, 1 designer UI/UX, 1 QA |

---

## 2. Contexte & Problematique

### 2.1 Contexte metier

Les cabinets d'architecture fonctionnent sur un modele economique ou la facturation est directement liee aux phases de projet et aux honoraires negocies avec les clients. Contrairement a une facturation de produits classique, la facturation en architecture presente des specificites majeures :

- **Facturation par phases de projet** : les honoraires sont decomposes en phases (esquisse, APS, APD, PRO, DCE, DET, AOR, etc.) et chaque phase donne lieu a une ou plusieurs factures selon l'avancement.
- **Echeanciers complexes** : les factures sont planifiees sur des mois voire des annees, avec des montants calcules en pourcentage de l'honoraire global ou de la phase.
- **Multi-intervenants** : les projets impliquent souvent des co-traitants (bureaux d'etudes, paysagistes, economistes) dont la facturation doit etre tracee.
- **Exigences reglementaires** : numerotation sequentielle obligatoire, mentions legales, TVA multi-taux, conformite comptable.
- **Delais de paiement longs** : les clients (maitres d'ouvrage publics ou prives) ont des delais de paiement souvent superieurs a 30 jours, necessitant un suivi rigoureux des relances.

### 2.2 Problematique actuelle

Sans un module de facturation integre, les cabinets d'architecture font face aux difficultes suivantes :

1. **Deconnexion honoraires/facturation** : les factures sont creees manuellement dans des outils externes (Excel, logiciels comptables) sans lien direct avec les honoraires et phases de projet, ce qui entraine des erreurs de montants et des oublis de facturation.
2. **Manque de visibilite sur la tresorerie** : l'absence de tableau de bord consolide empeche de connaitre en temps reel le chiffre d'affaires facture, les montants en attente de paiement et les retards de reglements.
3. **Relances inefficaces** : les relances sont effectuees de maniere ad hoc, sans suivi systematique, ce qui rallonge les delais de paiement et degrade la tresorerie.
4. **Difficulte d'export comptable** : la production des ecritures comptables pour le cabinet comptable necessite des ressaisies manuelles, source d'erreurs et de perte de temps.
5. **Absence de planification** : les dirigeants ne disposent pas d'un planning de facturation previsionnel leur permettant d'anticiper les flux de tresorerie.
6. **Gestion des co-traitants opaque** : le suivi de la facturation des co-traitants est deconnecte de la facturation principale du projet.

### 2.3 Impact

L'absence d'un module de facturation integre genere :
- Un manque a gagner estime entre 5% et 15% du chiffre d'affaires (factures oubliees, retards non relances)
- Une charge administrative disproportionnee pour la gestion financiere
- Un risque de non-conformite comptable et fiscale
- Une incapacite a piloter la tresorerie de maniere proactive

---

## 3. Objectif de l'EPIC

### 3.1 Objectif principal

Concevoir et developper un module de facturation complet, integre au coeur de l'application OOTI, permettant aux cabinets d'architecture de gerer l'ensemble du cycle de facturation -- de la planification a l'encaissement -- en lien direct avec les projets et les honoraires.

### 3.2 Objectifs specifiques

| # | Objectif | Indicateur de succes |
|---|---|---|
| O1 | Automatiser la generation de factures a partir des honoraires par phase | 90% des factures generees automatiquement sans correction manuelle |
| O2 | Fournir une visibilite en temps reel sur la facturation et les paiements | Tableau de bord mis a jour en temps reel avec KPIs cles |
| O3 | Reduire les delais de paiement grace aux relances automatisees | Reduction de 20% du delai moyen de paiement en 6 mois |
| O4 | Garantir la conformite reglementaire et fiscale | 100% des factures conformes aux obligations legales |
| O5 | Simplifier les exports comptables | Export en un clic vers les formats standards (CSV, Excel, FEC) |
| O6 | Offrir un suivi projet-facturation integre | Vue consolidee facturation accessible depuis chaque projet |
| O7 | Gerer la facturation multi-intervenants (co-traitants) | Tracer 100% de la facturation co-traitants par projet |
| O8 | Permettre la personnalisation des documents de facturation | Templates PDF personnalisables avec charte graphique du cabinet |

### 3.3 Valeur metier

- **Pour les dirigeants** : pilotage financier en temps reel, anticipation de la tresorerie, reduction des impay es
- **Pour les chefs de projet** : suivi de la facturation de leurs projets, visibilite sur l'avancement financier
- **Pour l'administration** : gain de temps sur la generation, l'envoi et le suivi des factures
- **Pour la comptabilite** : exports normalises, lettrage automatise, conformite fiscale

---

## 4. Perimetre Fonctionnel

### 4.1 Vue Gestion > Factures (niveau agence)

Le module Facturation est accessible depuis la barre laterale de l'application sous **GESTION > Factures**. Il comprend 8 sous-menus :

#### 4.1.1 Resume

- Tableau de bord synthetique de la facturation au niveau de l'agence
- KPIs principaux :
  - **Montant facturable** : somme des honoraires restant a facturer sur l'ensemble des projets actifs
  - **Montant facture** : cumul des factures emises sur la periode selectionnee
  - **Non paye** : encours client (factures emises non reglees)
  - **En retard** : montant des factures dont la date d'echeance est depassee
  - **Delai de paiement moyen** : nombre de jours moyen entre emission et encaissement
  - **Taux de recouvrement** : pourcentage des factures payees dans les delais
- Graphiques :
  - Evolution mensuelle du chiffre d'affaires facture (barres empilees par statut)
  - Repartition des factures par statut (camembert)
  - Top 10 des clients par encours
  - Courbe du delai de paiement moyen sur 12 mois
- Filtres : periode, client, projet, statut de facture, responsable projet

#### 4.1.2 Planning

- Calendrier previsionnel de facturation sur 12 mois glissants
- Vue mensuelle affichant les factures prevues par projet/phase
- Colonnes : mois, projet, phase, montant prevu HT, montant prevu TTC, statut (prevu / genere / envoye / paye)
- Possibilite de creer une facture directement depuis le planning
- Alimentation automatique du planning depuis les echeanciers definis dans EPIC-003 (Honoraires)
- Drag & drop pour deplacer une facture prevue d'un mois a un autre
- Code couleur par statut : gris (prevu), bleu (genere), orange (envoye), vert (paye), rouge (en retard)
- Totaux mensuels et cumul annuel

#### 4.1.3 Factures

- Liste paginee de toutes les factures de l'agence
- Colonnes : reference, date d'emission, projet, client, montant HT, TVA, montant TTC, statut, date d'echeance, jours de retard
- Filtres avances : statut, client, projet, periode, montant min/max, responsable
- Tri par colonne (ascendant/descendant)
- Actions groupees : envoyer, relancer, exporter, changer de statut
- Acces direct a la creation d'une nouvelle facture
- Recherche textuelle (reference, nom client, nom projet)
- Indicateurs visuels de retard de paiement (badge rouge avec nombre de jours)

#### 4.1.4 Relances

- Liste des factures impayees avec leur statut de relance
- Colonnes : reference facture, client, montant, date d'echeance, jours de retard, nombre de relances, date derniere relance, prochaine relance prevue
- Configuration des regles de relance automatique :
  - Relance 1 : X jours apres echeance (email automatique)
  - Relance 2 : X jours apres relance 1 (email automatique)
  - Relance 3 : X jours apres relance 2 (email + notification au responsable)
  - Mise en contentieux : apres X relances sans reponse
- Templates d'emails de relance personnalisables (par niveau de relance)
- Historique complet des relances par facture
- Envoi manuel de relance avec personnalisation du message
- Marquage "promesse de paiement" avec date previsionnelle

#### 4.1.5 Paiements

- Liste de tous les paiements recus
- Colonnes : date de reception, client, reference facture, montant, mode de paiement, reference bancaire
- Enregistrement d'un nouveau paiement :
  - Selection de la/des factures lettrees
  - Montant recu (paiement partiel ou total)
  - Date de reception
  - Mode de paiement (virement, cheque, especes, prelevement)
  - Reference bancaire / numero de cheque
  - Notes
- Lettrage automatique : rapprochement paiement/facture par montant et reference
- Lettrage manuel : association manuelle d'un paiement a une ou plusieurs factures
- Gestion des paiements partiels (solde restant a payer sur la facture)
- Gestion des trop-percus (creation automatique d'un avoir ou report sur prochaine facture)

#### 4.1.6 Clients

- Vue consolidee par client
- Colonnes : nom du client, nombre de projets, montant total facture, montant paye, solde du (encours), delai de paiement moyen, derniere facture
- Detail par client :
  - Fiche client avec coordonnees
  - Historique complet de facturation
  - Liste des factures en cours
  - Graphique d'evolution de l'encours
  - Delai de paiement moyen historique
  - Notes et commentaires
- Filtres : encours > 0, clients en retard, par responsable commercial

#### 4.1.7 Exports

- Export CSV : lignes de factures avec tous les champs (compatible import comptable)
- Export Excel : factures formatees avec onglets par mois / par client
- Export PDF : liste des factures sur une periode avec totaux
- Export FEC (Fichier des Ecritures Comptables) : format normalise pour la comptabilite francaise
- Parametres d'export : periode, statut, client, projet, format de date, separateur CSV
- Historique des exports realises
- Planification d'exports automatiques (mensuel, trimestriel)
- Export des ecritures de paiement pour rapprochement bancaire

#### 4.1.8 Ajustements

- Creation d'avoirs (factures d'avoir / notes de credit)
- Lien obligatoire avec la facture d'origine
- Motifs d'ajustement predefinisables : erreur de facturation, remise commerciale, annulation partielle, litige
- Ajustements positifs (complement de facturation) et negatifs (avoirs)
- Numerotation specifique des avoirs (prefixe AV-)
- Impact automatique sur l'encours client et les KPIs
- Historique complet des ajustements par facture et par client
- Validation obligatoire des avoirs par un responsable habilite

### 4.2 Vue Projet > Onglet Facturation (niveau projet)

L'onglet FACTURATION au niveau d'un projet individuel comprend 5 sous-sections :

#### 4.2.1 Resume projet

- KPIs specifiques au projet :
  - Honoraires totaux (lien EPIC-003)
  - Montant facture a date
  - Montant paye a date
  - Reste a facturer
  - Reste a encaisser
  - Pourcentage d'avancement financier
- Barre de progression visuelle : facture vs honoraires totaux
- Graphique : comparaison honoraires prevus vs factures vs paiements par phase
- Alerte si ecart entre avancement technique et avancement financier

#### 4.2.2 Planning projet

- Planning de facturation specifique au projet
- Vue par phase avec echeancier previsionnel
- Lien avec les jalons du projet (EPIC-002)
- Possibilite d'ajuster le planning de facturation sans modifier les honoraires

#### 4.2.3 Factures projet

- Liste des factures du projet uniquement
- Memes fonctionnalites que la vue agence (4.1.3) filtree sur le projet
- Creation d'une facture pre-remplie avec les informations du projet

#### 4.2.4 Paiements projet

- Liste des paiements associes au projet
- Enregistrement de paiement pre-contextualise sur le projet

#### 4.2.5 Etat de compte

- Releve complet du projet faisant apparaitre chronologiquement :
  - Les factures emises (debit)
  - Les avoirs emis (credit)
  - Les paiements recus (credit)
  - Le solde courant a chaque ligne
- Solde final du projet
- Exportable en PDF pour communication au client
- Possibilite d'envoyer l'etat de compte par email au client

### 4.3 Workflow de validation (Validation > Factures)

#### 4.3.1 Processus de validation

- Les factures passent par un workflow de validation avant envoi :
  1. **Brouillon** : la facture est creee, modifiable sans restriction
  2. **En attente de validation** : la facture est soumise pour approbation
  3. **Validee** : la facture est approuvee, prete a l'envoi (modifications restreintes)
  4. **Rejetee** : la facture est renvoyee au createur avec commentaires
  5. **Envoyee** : la facture a ete transmise au client
  6. **Payee** : le paiement a ete recu et lettre
  7. **Annulee** : la facture est annulee (avec avoir obligatoire si deja envoyee)

#### 4.3.2 Regles de validation

- Seuils de validation parametrables :
  - Montant < X EUR : validation par le chef de projet
  - Montant >= X EUR : validation par un directeur / associe
  - Avoirs : double validation obligatoire
- Delegation de validation en cas d'absence
- Notifications automatiques aux valideurs
- Tableau de bord des factures en attente de validation
- Historique d'approbation (qui, quand, commentaires)
- Alerte si facture en attente de validation depuis plus de X jours

### 4.4 Generation et personnalisation PDF

#### 4.4.1 Contenu du PDF

- En-tete : logo du cabinet, raison sociale, adresse, SIRET, TVA intracommunautaire
- Informations client : nom, adresse, contact, reference client
- Reference facture et date d'emission
- Objet : nom du projet, phase concernee
- Tableau des lignes de facturation : designation, quantite, prix unitaire HT, montant HT
- Sous-total HT, TVA (detail par taux si multi-taux), montant TTC
- Conditions de paiement, date d'echeance
- Coordonnees bancaires (RIB/IBAN)
- Mentions legales obligatoires (penalites de retard, indemnite forfaitaire de recouvrement, etc.)
- Notes et conditions particulieres
- Pied de page : mention d'assurance professionnelle, inscription a l'Ordre des Architectes

#### 4.4.2 Personnalisation

- Templates de factures parametrables
- Couleurs, polices, mise en page personnalisables
- Upload du logo du cabinet
- Champs personnalises additionnels
- Apercu en temps reel avant generation
- Multi-langues (francais, anglais) pour clients internationaux
- Templates differents par type de document (facture, avoir, etat de compte, proforma)

### 4.5 Facturation co-traitants

#### 4.5.1 Suivi co-traitants

- Enregistrement des factures recues des co-traitants par projet
- Lien avec les lots / phases attribues au co-traitant (definis dans EPIC-003)
- Colonnes : co-traitant, reference facture, date, montant HT, TVA, montant TTC, statut (recue, validee, payee)
- Comparaison facture co-traitant vs montant prevu dans la convention de co-traitance
- Alerte si le cumul facture par un co-traitant depasse le montant prevu

#### 4.5.2 Paiements co-traitants

- Enregistrement des paiements effectues aux co-traitants
- Rapprochement paiement / facture co-traitant
- Impact sur la marge nette du projet

### 4.6 Gestion de la TVA

- Parametrage multi-taux de TVA (20%, 10%, 5,5%, 0% pour export)
- TVA par defaut configurable au niveau de l'agence
- Possibilite de TVA differente par ligne de facture
- Gestion de l'autoliquidation (sous-traitance BTP)
- TVA intracommunautaire
- Recapitulatif TVA sur la facture (ventilation par taux)
- Reporting TVA periodique (mensuel/trimestriel)

---

## 5. User Stories

### US-F01 : Vue resume facturation agence

**En tant que** dirigeant de cabinet d'architecture,
**Je veux** disposer d'un tableau de bord synthetique de la facturation au niveau de l'agence,
**Afin de** piloter en temps reel la sante financiere du cabinet et prendre des decisions eclairees.

**Criteres d'acceptance :**

1. Le tableau de bord affiche les KPIs suivants, calcules en temps reel : montant facturable (somme des honoraires restant a facturer sur les projets actifs), montant facture sur la periode, montant non paye (encours), montant en retard de paiement, delai de paiement moyen (en jours), et taux de recouvrement (en pourcentage).
2. Un filtre de periode est disponible (mois en cours, trimestre, annee, periode personnalisee) et tous les KPIs et graphiques se mettent a jour dynamiquement lorsque la periode change.
3. Un graphique en barres empilees affiche l'evolution mensuelle du chiffre d'affaires facture sur les 12 derniers mois, avec une decomposition par statut (brouillon, envoyee, payee, en retard, annulee).
4. Un graphique circulaire (camembert) affiche la repartition du nombre de factures par statut sur la periode selectionnee.
5. Un classement (Top 10) des clients par encours est affiche sous forme de liste ordonnee, avec pour chaque client : nom, montant de l'encours, nombre de factures en cours, et delai de paiement moyen.
6. Des filtres complementaires permettent d'affiner la vue : par client, par projet, par statut de facture, par responsable de projet.
7. Un clic sur un KPI ou un element de graphique redirige vers la liste des factures correspondantes filtree automatiquement.
8. Le tableau de bord se charge en moins de 3 secondes avec un jeu de donnees de 500 factures et 50 projets actifs.

---

### US-F02 : Planning de facturation

**En tant que** responsable financier du cabinet,
**Je veux** visualiser un planning previsionnel de toutes les factures a emettre sur les prochains mois,
**Afin de** anticiper les flux de tresorerie et m'assurer qu'aucune facturation n'est oubliee.

**Criteres d'acceptance :**

1. Le planning affiche une vue calendaire sur 12 mois glissants, avec en colonnes les mois et en lignes les projets actifs.
2. Chaque cellule du planning indique le montant previsionnel de facturation pour le projet/mois concerne, avec un code couleur selon le statut : gris (prevu, non encore genere), bleu (facture generee en brouillon), orange (facture envoyee), vert (facture payee), rouge (en retard).
3. Le planning est alimente automatiquement a partir des echeanciers definis dans le module Honoraires (EPIC-003) : les montants et dates previsionnelles sont reportes sans saisie manuelle.
4. L'utilisateur peut deplacer une facture prevue d'un mois a un autre par glisser-deposer (drag & drop), ce qui met a jour la date previsionnelle sans modifier le montant des honoraires.
5. Un clic sur une cellule permet de creer directement une facture pre-remplie avec les informations du projet, de la phase et du montant previsionnel.
6. Des totaux mensuels sont affiches en bas de chaque colonne (total prevu, total genere, total paye) ainsi qu'un cumul annuel en fin de ligne.
7. Un filtre par client, par responsable de projet et par statut de facturation est disponible.
8. Le planning affiche une alerte visuelle (icone avertissement) lorsqu'une facturation prevue est en retard de generation (date previsionnelle depassee sans facture creee).

---

### US-F03 : Creation d'une facture

**En tant que** gestionnaire administratif du cabinet,
**Je veux** creer une nouvelle facture en la liant a un projet et a une phase d'honoraires,
**Afin de** formaliser une demande de paiement conforme et tracee.

**Criteres d'acceptance :**

1. Un formulaire de creation de facture est accessible depuis le menu Factures (bouton "Nouvelle facture"), depuis le planning (clic sur une cellule), et depuis l'onglet Facturation d'un projet.
2. Les champs obligatoires sont : projet (selection dans la liste des projets actifs), phase/lot (selection parmi les phases du projet), client (pre-rempli a partir du projet), date d'emission (par defaut la date du jour), date d'echeance (calculee automatiquement selon les conditions de paiement du client).
3. Le formulaire permet d'ajouter une ou plusieurs lignes de facturation avec : designation (texte libre ou pre-remplie depuis la phase), quantite, prix unitaire HT, taux de TVA (par defaut celui configure pour l'agence, modifiable par ligne), et montant HT calcule automatiquement.
4. Lorsque la facture est creee depuis le planning ou liee a une phase d'honoraires, le montant est pre-rempli avec le montant previsionnel et la designation avec le libelle de la phase.
5. Les totaux sont calcules automatiquement en temps reel : sous-total HT, detail TVA par taux, montant TTC.
6. Un champ "Notes" permet d'ajouter des observations internes (non imprimees sur la facture) et un champ "Conditions particulieres" permet d'ajouter des mentions visibles sur le PDF.
7. A la validation du formulaire, la facture est creee avec le statut "Brouillon" et un numero provisoire. Le numero definitif est attribue lors du passage au statut "Validee" ou "Envoyee" selon la configuration.
8. Le systeme empeche la creation d'une facture si le montant cumule des factures d'un projet depasse le montant total des honoraires, avec un avertissement explicite.

---

### US-F04 : Edition et gestion d'une facture

**En tant que** gestionnaire administratif du cabinet,
**Je veux** pouvoir modifier, dupliquer et gerer le statut d'une facture existante,
**Afin de** corriger des erreurs, adapter les factures et suivre leur cycle de vie.

**Criteres d'acceptance :**

1. Une facture au statut "Brouillon" est entierement modifiable : tous les champs (projet, phase, lignes, montants, dates, notes) peuvent etre edites sans restriction.
2. Une facture au statut "Validee" ne peut etre modifiee que sur les champs non financiers (notes, conditions particulieres). Toute modification de montant necessite un retour au statut "Brouillon" avec trace dans l'historique.
3. Une facture au statut "Envoyee" ne peut plus etre modifiee. Toute correction doit passer par la creation d'un avoir (ajustement negatif) et d'une nouvelle facture.
4. La duplication d'une facture cree un nouveau brouillon pre-rempli avec les memes informations (projet, client, lignes) mais une nouvelle date et un nouveau numero provisoire.
5. Le changement de statut est trace dans un historique horodate : chaque transition (brouillon -> en attente -> validee -> envoyee -> payee) enregistre l'utilisateur, la date et un commentaire optionnel.
6. L'annulation d'une facture non envoyee la passe au statut "Annulee" avec un motif obligatoire. L'annulation d'une facture deja envoyee genere automatiquement un avoir du meme montant.
7. Une vue "historique des modifications" affiche toutes les actions effectuees sur la facture (creation, modifications, changements de statut, envois, relances).
8. La suppression physique d'une facture n'est jamais possible (pour des raisons legales et de tracabilite). Seule l'annulation est permise.

---

### US-F05 : Envoi d'une facture par email

**En tant que** gestionnaire administratif du cabinet,
**Je veux** envoyer une facture au client par email directement depuis l'application,
**Afin de** gagner du temps et tracer automatiquement l'envoi.

**Criteres d'acceptance :**

1. Un bouton "Envoyer" est disponible sur toute facture ayant le statut "Validee". Le clic ouvre une boite de dialogue d'envoi par email.
2. Les champs de l'email sont pre-remplis : destinataire(s) (adresses email du client, modifiables), objet (personnalise avec reference facture et nom du projet), corps du message (template personnalisable par l'agence).
3. La facture au format PDF est automatiquement generee et jointe a l'email.
4. L'utilisateur peut ajouter des destinataires en copie (CC) et en copie cachee (BCC).
5. L'utilisateur peut previsualiser le PDF de la facture avant envoi.
6. Apres envoi, le statut de la facture passe automatiquement a "Envoyee", la date d'envoi est enregistree, et un evenement est ajoute a l'historique de la facture.
7. L'envoi groupee est possible : selection de plusieurs factures validees et envoi en lot, chaque facture etant envoyee au client correspondant avec son PDF.
8. En cas d'echec d'envoi (adresse invalide, erreur serveur), un message d'erreur explicite est affiche, le statut n'est pas modifie, et l'utilisateur est invite a corriger et reessayer.

---

### US-F06 : Gestion des relances

**En tant que** responsable financier du cabinet,
**Je veux** configurer et executer des relances automatiques et manuelles pour les factures impayees,
**Afin de** reduire les delais de paiement et limiter les impayes.

**Criteres d'acceptance :**

1. Un ecran de parametrage des relances permet de definir jusqu'a 4 niveaux de relance avec pour chaque niveau : nombre de jours apres echeance (ou apres la relance precedente), canal de relance (email, notification interne), et template d'email associe.
2. Les templates de relance sont personnalisables avec des variables dynamiques : {reference_facture}, {montant}, {date_echeance}, {jours_retard}, {nom_client}, {nom_projet}, {lien_paiement}.
3. Les relances automatiques sont executees quotidiennement par le systeme : chaque facture en retard dont le delai correspond a un niveau de relance declenche l'envoi automatique du mail correspondant.
4. L'ecran "Relances" affiche la liste de toutes les factures en retard avec : reference, client, montant, date d'echeance, jours de retard, niveau de relance atteint, date de la derniere relance, date de la prochaine relance prevue.
5. L'utilisateur peut envoyer une relance manuelle a tout moment, en choisissant le template ou en redigeant un message libre, sans attendre le declenchement automatique.
6. Chaque relance (automatique ou manuelle) est tracee dans l'historique de la facture avec : date, type (auto/manuelle), contenu du message, destinataire.
7. L'utilisateur peut marquer une facture en "promesse de paiement" avec une date previsionnelle, ce qui suspend temporairement les relances automatiques pour cette facture.
8. Une notification est envoyee au responsable de projet lorsqu'une facture atteint le 3eme niveau de relance (alerte escalade).
9. Les factures peuvent etre marquees comme "contentieux" apres epuisement des niveaux de relance, ce qui les fait apparaitre dans une section dediee avec un traitement specifique.

---

### US-F07 : Enregistrement des paiements

**En tant que** gestionnaire administratif du cabinet,
**Je veux** enregistrer les paiements recus et les associer aux factures correspondantes,
**Afin de** suivre les encaissements et maintenir l'encours client a jour.

**Criteres d'acceptance :**

1. Un formulaire d'enregistrement de paiement est accessible depuis le menu "Paiements" (bouton "Nouveau paiement") et depuis le detail d'une facture (bouton "Enregistrer un paiement").
2. Les champs obligatoires sont : date de reception, montant recu, mode de paiement (virement bancaire, cheque, prelevement, especes, carte bancaire, autre), reference bancaire ou numero de cheque.
3. Le lettrage (association paiement-facture) peut etre automatique : le systeme propose les factures correspondantes en se basant sur le montant et la reference, avec un score de confiance.
4. Le lettrage peut etre manuel : l'utilisateur selectionne une ou plusieurs factures a associer au paiement, en repartissant le montant si necessaire.
5. Les paiements partiels sont geres : lorsque le montant recu est inferieur au montant de la facture, le solde restant est affiche sur la facture qui conserve le statut "Partiellement payee".
6. Les trop-percus sont geres : lorsque le montant recu est superieur au montant de la facture, l'utilisateur choisit entre creer un avoir, reporter le surplus sur la prochaine facture du client, ou effectuer un remboursement.
7. Lorsqu'une facture est integralement payee (paiement total ou cumul de paiements partiels = montant TTC), son statut passe automatiquement a "Payee" et la date de paiement est enregistree.
8. L'historique des paiements de chaque facture est consultable avec le detail : date, montant, mode de paiement, reference, utilisateur ayant enregistre le paiement.

---

### US-F08 : Etat de compte client

**En tant que** dirigeant de cabinet,
**Je veux** consulter un etat de compte consolide par client,
**Afin de** connaitre la situation financiere de chaque client et disposer d'un document communicable.

**Criteres d'acceptance :**

1. La vue "Clients" affiche la liste de tous les clients avec : nom, nombre de projets actifs, montant total facture (historique), montant paye, solde du (encours), delai de paiement moyen.
2. Le detail d'un client affiche un releve de compte chronologique presentant toutes les operations : factures emises (debit), avoirs (credit), paiements recus (credit), avec un solde courant progressif.
3. Le releve de compte peut etre filtre par periode (mois, trimestre, annee, periode personnalisee) et par projet.
4. Le releve de compte est exportable en PDF avec l'en-tete du cabinet pour communication officielle au client.
5. L'envoi du releve de compte par email au client est possible directement depuis l'application, avec template d'email personnalisable.
6. Un graphique d'evolution de l'encours du client sur les 12 derniers mois est affiche dans le detail client.
7. Un indicateur de "sante client" est calcule automatiquement (vert = paiements reguliers et dans les delais, orange = retards occasionnels, rouge = retards frequents ou importants) base sur l'historique des paiements.
8. Des notes et commentaires peuvent etre ajoutes sur la fiche client pour documenter les echanges relatifs aux paiements.

---

### US-F09 : Exports comptables

**En tant que** comptable ou responsable administratif du cabinet,
**Je veux** exporter les donnees de facturation dans des formats compatibles avec les logiciels comptables,
**Afin de** alimenter la comptabilite sans ressaisie manuelle.

**Criteres d'acceptance :**

1. L'ecran "Exports" propose les formats suivants : CSV (separateur configurable : virgule, point-virgule, tabulation), Excel (.xlsx avec mise en forme), PDF (liste des factures avec totaux), FEC (Fichier des Ecritures Comptables au format reglementaire francais).
2. Les parametres d'export sont : periode (obligatoire), statut des factures (tous, envoyees uniquement, payees uniquement), client (tous ou selection), projet (tous ou selection), format de date (JJ/MM/AAAA ou AAAA-MM-JJ).
3. L'export CSV contient toutes les colonnes : reference facture, date d'emission, date d'echeance, date de paiement, client (nom, SIRET), projet, designation, montant HT, taux TVA, montant TVA, montant TTC, statut, mode de paiement.
4. L'export FEC respecte le format normalise avec les colonnes reglementaires : JournalCode, JournalLib, EcritureNum, EcritureDate, CompteNum, CompteLib, CompAuxNum, CompAuxLib, PieceRef, PieceDate, EcritureLib, Debit, Credit, EcrtureLet, DateLet, ValidDate, Montantdevise, Idevise.
5. L'export Excel genere un classeur avec des onglets separes : synthese mensuelle, detail des factures, detail des paiements, recapitulatif TVA.
6. Un historique des exports realises est conserve avec : date, utilisateur, format, parametres, nombre de lignes exportees, lien de telechargement (pendant 30 jours).
7. La planification d'exports automatiques est possible : l'utilisateur peut configurer un export periodique (mensuel, trimestriel) envoye par email a une adresse definie.
8. L'export des ecritures de paiement est disponible separement pour faciliter le rapprochement bancaire.

---

### US-F10 : Ajustements et avoirs

**En tant que** gestionnaire administratif du cabinet,
**Je veux** creer des avoirs et des ajustements lies aux factures emises,
**Afin de** corriger les erreurs de facturation et gerer les remises tout en respectant les obligations comptables.

**Criteres d'acceptance :**

1. La creation d'un avoir est accessible depuis le detail d'une facture (bouton "Creer un avoir") et depuis le menu "Ajustements" (bouton "Nouvel ajustement").
2. Un avoir est obligatoirement lie a une facture d'origine. Le formulaire propose la selection de la facture et pre-remplit les informations (client, projet, montant maximum = montant de la facture d'origine).
3. Les types d'ajustement disponibles sont : avoir total (annulation complete de la facture), avoir partiel (montant inferieur a la facture d'origine), complement de facturation (ajustement positif), remise commerciale.
4. Un motif est obligatoire pour chaque ajustement, choisi parmi une liste parametrable : erreur de facturation, remise commerciale, annulation de prestation, litige, modification de commande, autre (avec commentaire libre obligatoire).
5. Les avoirs sont numerotes avec un prefixe distinct (ex: AV-2026-001) et suivent une numerotation sequentielle propre.
6. La validation d'un avoir superieur a un seuil parametre (par defaut 1000 EUR) necessite une double validation (createur + valideur habilite).
7. Apres validation, l'avoir impacte automatiquement l'encours client, les KPIs du tableau de bord, et le solde du projet concerne.
8. Un avoir genere un document PDF avec les memes standards de presentation que les factures, incluant la mention obligatoire "AVOIR" et la reference de la facture d'origine.

---

### US-F11 : Facturation co-traitants

**En tant que** chef de projet,
**Je veux** suivre et enregistrer les factures emises par les co-traitants sur mes projets,
**Afin de** controler les couts des intervenants externes et calculer la marge nette du projet.

**Criteres d'acceptance :**

1. Depuis l'onglet Facturation d'un projet, une section "Co-traitants" liste les co-traitants du projet (definis dans EPIC-003 Honoraires) avec pour chacun : nom, lot/phase attribue, montant prevu dans la convention, montant facture a date, montant paye, solde.
2. L'enregistrement d'une facture co-traitant comprend : reference de la facture, date de reception, co-traitant (selection dans la liste), lot/phase, montant HT, taux de TVA, montant TTC, document numerise (upload PDF).
3. Un statut est associe a chaque facture co-traitant : recue, validee (bon a payer), payee, rejetee (avec motif).
4. Le systeme affiche une alerte lorsque le cumul des factures d'un co-traitant depasse le montant prevu dans la convention de co-traitance (depassement en montant et en pourcentage).
5. L'enregistrement du paiement effectue au co-traitant est possible avec : date, montant, mode de paiement, reference de virement.
6. La marge nette du projet est calculee en temps reel : honoraires recus (paiements clients) - paiements co-traitants = marge nette, affichee en montant et en pourcentage.
7. Un etat recapitulatif de la facturation co-traitants par projet est exportable en PDF et en Excel.
8. Le filtrage et la recherche des factures co-traitants sont possibles par : co-traitant, statut, periode, montant.

---

### US-F12 : Generation PDF personnalisee

**En tant que** dirigeant de cabinet,
**Je veux** personnaliser l'apparence des factures PDF generees par l'application,
**Afin de** produire des documents professionnels a l'image du cabinet.

**Criteres d'acceptance :**

1. Un ecran de parametrage des templates de facturation est accessible depuis les parametres de l'agence, permettant de configurer : logo (upload d'image, position et taille), couleurs principales (couleur d'accent, couleur de texte, couleur d'arriere-plan), polices (selection parmi une liste de polices web-safe).
2. Le template definit la mise en page du PDF : position et contenu de l'en-tete, du corps (tableau des lignes), et du pied de page.
3. Les mentions legales obligatoires sont integrees automatiquement et ne peuvent pas etre supprimees : penalites de retard, indemnite forfaitaire de recouvrement (40 EUR), numero de TVA intracommunautaire, numero d'inscription a l'Ordre des Architectes, reference d'assurance professionnelle.
4. Plusieurs templates peuvent etre crees (ex: template standard, template anglais, template proforma) et le template par defaut est configurable.
5. Un apercu en temps reel du PDF est affiche lors de la configuration du template, avec des donnees fictives.
6. La generation du PDF prend en compte la langue selectionnee (francais ou anglais) pour les libelles fixes (date, reference, montant HT, TVA, TTC, conditions de paiement, etc.).
7. Le PDF genere est au format A4, avec une resolution d'impression de 300 DPI, et pese moins de 2 Mo.
8. Les types de documents personnalisables avec des templates distincts sont : facture, avoir, etat de compte, proforma, situation de travaux.

---

### US-F13 : Numerotation et parametres de facturation

**En tant qu'** administrateur de l'agence,
**Je veux** configurer les regles de numerotation des factures et les parametres generaux de facturation,
**Afin de** garantir la conformite legale et adapter le module aux pratiques du cabinet.

**Criteres d'acceptance :**

1. Les parametres de numerotation configurables sont : prefixe (ex: FA, FACT, le nom abrege du cabinet), format de date integre (AAAA, AAMM), separateur (tiret, slash, point), compteur (nombre de chiffres, ex: 001, 0001), exemple en temps reel : "FA-2026-0042".
2. La numerotation est strictement sequentielle et sans rupture, conformement a la legislation francaise. Le systeme empeche toute modification ou suppression de numero une fois attribue.
3. Les numerotations sont distinctes par type de document : factures (prefixe configurable), avoirs (prefixe configurable, par defaut AV-), proformas (prefixe configurable, par defaut PF-).
4. Les conditions de paiement par defaut sont configurables : delai (30, 45, 60 jours), mode de calcul (jours calendaires, jours fin de mois, jours fin de mois le 10), escompte pour paiement anticipe (pourcentage et nombre de jours).
5. Les coordonnees bancaires de l'agence (IBAN, BIC, nom de la banque, titulaire du compte) sont saisies et apparaissent automatiquement sur les factures.
6. Le taux de TVA par defaut est configurable (20% par defaut) avec possibilite d'ajouter des taux supplementaires utilises frequemment (10%, 5.5%, 0%).
7. Les penalites de retard sont configurables : taux d'interet (par defaut 3 fois le taux d'interet legal), indemnite forfaitaire de recouvrement (par defaut 40 EUR, conformement a l'article L.441-10 du Code de commerce).
8. Une reinitialisation du compteur est possible au debut de chaque annee civile (option activable/desactivable) avec conservation de l'historique des numerotations precedentes.

---

### US-F14 : Tableau de bord facturation par projet

**En tant que** chef de projet,
**Je veux** consulter un tableau de bord de facturation specifique a mon projet,
**Afin de** suivre l'avancement financier du projet et identifier les ecarts par rapport au budget.

**Criteres d'acceptance :**

1. L'onglet Facturation du projet affiche un resume avec les KPIs suivants : honoraires totaux du projet (lien EPIC-003), montant facture a date (cumul HT), montant paye a date, reste a facturer (honoraires - facture), reste a encaisser (facture - paye), pourcentage d'avancement financier.
2. Une barre de progression visuelle a trois segments illustre : le montant paye (vert), le montant facture non paye (orange), le reste a facturer (gris).
3. Un graphique compare, par phase du projet, les honoraires prevus, les factures emises et les paiements recus, sous forme de barres groupees.
4. Une alerte est affichee si l'ecart entre l'avancement technique du projet (pourcentage d'achevement des phases, EPIC-002) et l'avancement financier (pourcentage facture/honoraires) depasse un seuil configurable (par defaut 10%).
5. La liste des factures du projet est affichee avec les memes colonnes et fonctionnalites que la vue agence (reference, date, montant, statut, actions).
6. Le planning de facturation specifique au projet est affiche avec les echeances prevues par phase et la possibilite de les ajuster.
7. L'etat de compte du projet est accessible : releve chronologique (factures, avoirs, paiements) avec solde progressif et solde final.
8. L'etat de compte du projet est exportable en PDF et envoyable par email au client.

---

## 6. Hors Perimetre

Les elements suivants sont explicitement exclus du perimetre de cet EPIC :

| # | Element exclu | Justification | EPIC potentiel |
|---|---|---|---|
| 1 | **Comptabilite generale** (grand livre, bilan, compte de resultat) | Le module Facturation n'est pas un logiciel comptable. Les exports permettent d'alimenter un logiciel comptable tiers. | EPIC-008 (Finances) |
| 2 | **Paiement en ligne** (integration Stripe, PayPal, GoCardless) | Fonctionnalite avancee qui pourra etre ajoutee dans une version ulterieure. | Backlog |
| 3 | **Facturation recurrente automatique** (abonnements) | Non applicable au modele de facturation par projet/phase des cabinets d'architecture. | N/A |
| 4 | **Gestion des depenses** (notes de frais, achats fournisseurs hors co-traitants) | Perimetre distinct de la facturation client. | EPIC-008 (Finances) |
| 5 | **Recouvrement contentieux** (procedures judiciaires, huissier) | Le module gere les relances amiables uniquement. Le passage en contentieux est trace mais le suivi juridique est hors perimetre. | N/A |
| 6 | **Facturation electronique obligatoire** (Chorus Pro, Peppol) | Sera traite dans un EPIC specifique de conformite reglementaire, notamment dans le cadre de la reforme de la facturation electronique en France. | Backlog |
| 7 | **Multi-devises** | Non couvert dans la V1. Les factures sont emises dans la devise de l'agence uniquement. | Backlog |
| 8 | **Previsionnel de tresorerie** | Le planning de facturation apporte une visibilite previsionnelle mais le module complet de gestion de tresorerie est hors perimetre. | EPIC-008 (Finances) |

---

## 7. Regles Metier

### 7.1 Numerotation des factures

| Regle | Description |
|---|---|
| RM-F01 | La numerotation des factures est strictement sequentielle, chronologique et sans rupture, conformement a l'article 242 nonies A du Code general des impots. |
| RM-F02 | Un numero de facture attribue ne peut jamais etre modifie, reutilise ou supprime, meme en cas d'annulation de la facture. |
| RM-F03 | Les avoirs et les factures suivent des sequences de numerotation distinctes mais chacune est sequentielle et sans rupture. |
| RM-F04 | La reinitialisation du compteur en debut d'annee est optionnelle. Si activee, le format inclut obligatoirement l'annee (ex: FA-2026-0001). |

### 7.2 Cycle de vie des factures

| Regle | Description |
|---|---|
| RM-F05 | Une facture ne peut etre envoyee qu'apres validation par un utilisateur habilite (workflow de validation). |
| RM-F06 | Une facture envoyee ne peut pas etre modifiee. Toute correction doit passer par l'emission d'un avoir et la creation d'une nouvelle facture. |
| RM-F07 | L'annulation d'une facture envoyee genere obligatoirement un avoir du meme montant pour respecter la tracabilite comptable. |
| RM-F08 | Une facture passe automatiquement au statut "En retard" lorsque la date d'echeance est depassee sans enregistrement de paiement total. |
| RM-F09 | Le statut "Payee" est attribue automatiquement uniquement lorsque le total des paiements lettres atteint le montant TTC de la facture. |

### 7.3 Calculs financiers

| Regle | Description |
|---|---|
| RM-F10 | Le montant HT de chaque ligne est calcule : quantite x prix unitaire HT, arrondi a 2 decimales. |
| RM-F11 | Le montant de TVA est calcule par taux : somme des montants HT du taux x taux de TVA, arrondi a 2 decimales. |
| RM-F12 | Le montant TTC est egal au montant HT total + somme des montants de TVA. Les arrondis sont effectues par ligne puis additionnes (methode ligne par ligne). |
| RM-F13 | Les penalites de retard sont calculees : montant TTC x taux x (nombre de jours de retard / 365). Elles ne sont pas facturees automatiquement mais affichees a titre indicatif. |
| RM-F14 | Le montant facture sur un projet ne peut pas depasser le montant total des honoraires du projet (sauf ajustement valide explicitement par un administrateur). |

### 7.4 Relances

| Regle | Description |
|---|---|
| RM-F15 | Les relances automatiques ne sont envoyees que pour les factures au statut "Envoyee" dont la date d'echeance est depassee et qui ne sont pas marquees "promesse de paiement". |
| RM-F16 | Le passage au niveau de relance superieur est conditionne au delai configure (ex: Relance 2 envoyee uniquement X jours apres Relance 1). |
| RM-F17 | Une facture marquee "promesse de paiement" est exclue des relances automatiques jusqu'a la date de promesse. Si le paiement n'est pas recu a la date promise, les relances reprennent automatiquement au niveau ou elles avaient ete suspendues. |

### 7.5 TVA

| Regle | Description |
|---|---|
| RM-F18 | Le taux de TVA par defaut est celui configure au niveau de l'agence (20% par defaut pour la France). Il peut etre modifie ligne par ligne sur chaque facture. |
| RM-F19 | En cas d'autoliquidation de TVA (sous-traitance BTP), la mention "Autoliquidation de la TVA - article 283-2 nonies du CGI" est ajoutee automatiquement et le montant de TVA est a 0. |
| RM-F20 | Pour les prestations intracommunautaires, la mention "Exoneration de TVA - article 259-1 du CGI" est ajoutee et le numero de TVA intracommunautaire du client est obligatoire. |

### 7.6 Co-traitants

| Regle | Description |
|---|---|
| RM-F21 | Le montant cumule des factures enregistrees pour un co-traitant sur un projet ne doit pas depasser le montant prevu dans la convention de co-traitance sans alerte explicite. |
| RM-F22 | La marge nette du projet est calculee : somme des paiements clients recus - somme des paiements co-traitants effectues. |

---

## 8. Criteres d'Acceptance Globaux

### 8.1 Fonctionnels

| # | Critere |
|---|---|
| CAG-01 | L'ensemble du cycle de facturation (creation, validation, envoi, paiement, avoir) fonctionne de bout en bout sans erreur pour un scenario nominal. |
| CAG-02 | Les KPIs du tableau de bord (niveau agence et niveau projet) sont coherents avec les donnees des factures et des paiements, a tout instant. |
| CAG-03 | Le planning de facturation est automatiquement alimente par les echeanciers d'honoraires (EPIC-003) et refleter les modifications en temps reel. |
| CAG-04 | Les relances automatiques sont envoyees aux dates prevues selon le parametrage, sans doublon ni oubli. |
| CAG-05 | Les exports comptables (CSV, Excel, FEC) sont importables sans erreur dans au moins 2 logiciels comptables standards (Sage, Cegid, ou equivalent). |
| CAG-06 | La numerotation des factures respecte la sequentialite sans aucune rupture, meme en cas d'operations concurrentes (creation simultanee par plusieurs utilisateurs). |
| CAG-07 | Les calculs de TVA sont exacts a 2 decimales pres, quel que soit le nombre de lignes et de taux differents sur une facture. |

### 8.2 Non-fonctionnels

| # | Critere |
|---|---|
| CAG-08 | Le tableau de bord se charge en moins de 3 secondes avec un jeu de donnees de 1000 factures, 100 projets et 50 clients. |
| CAG-09 | La generation d'un PDF de facture prend moins de 2 secondes. |
| CAG-10 | L'export de 10 000 lignes en CSV prend moins de 10 secondes. |
| CAG-11 | Le module supporte 20 utilisateurs concurrents sans degradation de performance. |
| CAG-12 | Les donnees de facturation sont sauvegardees avec un RPO (Recovery Point Objective) de 1 heure maximum. |
| CAG-13 | Le module est accessible sur les navigateurs Chrome, Firefox, Safari et Edge (2 dernieres versions majeures). |
| CAG-14 | Les ecrans de consultation (tableau de bord, listes) sont consultables sur tablette (responsive design, resolution minimale 768px). |

### 8.3 Securite et conformite

| # | Critere |
|---|---|
| CAG-15 | Seuls les utilisateurs avec le role "Facturation" ou superieur peuvent creer, modifier et envoyer des factures. |
| CAG-16 | Les operations sensibles (annulation, avoir, export) sont tracees dans un journal d'audit horodate non modifiable. |
| CAG-17 | Les donnees de facturation sont chiffrees au repos et en transit (HTTPS/TLS 1.2 minimum). |
| CAG-18 | L'acces aux donnees de facturation respecte les perimetre d'habilitation : un chef de projet ne voit que les factures de ses projets, un dirigeant voit toutes les factures. |

---

## 9. Definition of Done

Une User Story de cet EPIC est consideree comme "Done" lorsque l'ensemble des criteres suivants sont satisfaits :

### 9.1 Developpement

- [ ] Le code est ecrit, revue par un pair (code review approuvee) et merge dans la branche de developpement.
- [ ] Le code respecte les conventions de codage et les standards de l'equipe (linting, formatting).
- [ ] Aucun avertissement (warning) ou erreur de compilation n'est present.
- [ ] Les principes SOLID et les patterns d'architecture definis pour le projet sont respectes.

### 9.2 Tests

- [ ] Les tests unitaires couvrent au minimum 80% du code metier (services, calculs, regles de gestion).
- [ ] Les tests d'integration couvrent les interactions entre les modules (Facturation <-> Honoraires, Facturation <-> Projets).
- [ ] Les tests end-to-end (E2E) couvrent les scenarios critiques : creation de facture, envoi, paiement, avoir, relance.
- [ ] Les tests de non-regression passent sans echec.
- [ ] Les tests de performance valident les criteres CAG-08 a CAG-11.

### 9.3 Fonctionnel

- [ ] Tous les criteres d'acceptance de la User Story sont valides par l'equipe QA.
- [ ] Les regles metier applicables (section 7) sont implementees et verifiees.
- [ ] Les cas aux limites sont testes : facture a 0 EUR, TVA multi-taux, paiement partiel multiple, numerotation concurrente.
- [ ] L'accessibilite WCAG 2.1 niveau AA est respectee sur les ecrans concernes.

### 9.4 Documentation

- [ ] La documentation technique (API, modele de donnees) est a jour.
- [ ] La documentation utilisateur (aide en ligne, tooltips) est redigee pour les fonctionnalites concernees.
- [ ] Les notes de version (changelog) sont mises a jour.

### 9.5 Deploiement

- [ ] La fonctionnalite est deployable independamment (feature flag si necessaire).
- [ ] Les scripts de migration de base de donnees sont testes et reversibles.
- [ ] La fonctionnalite est validee en environnement de staging avant mise en production.

---

## 10. Dependances

### 10.1 Dependances entrantes (ce module depend de)

| EPIC / Module | Nature de la dependance | Impact | Criticite |
|---|---|---|---|
| **EPIC-002 (Projets)** | Les factures sont liees aux projets. Le module Facturation a besoin des donnees projet (nom, reference, client, phases, statut). | Le module Facturation ne peut pas fonctionner sans le module Projets. | **Bloquante** |
| **EPIC-003 (Honoraires)** | Les factures sont generees a partir des honoraires par phase. Le planning de facturation est alimente par les echeanciers d'honoraires. | La generation automatique de factures et le planning dependent entierement d'EPIC-003. | **Bloquante** |
| **Module Authentification / Roles** | Le workflow de validation et les habilitations d'acces dependent du systeme de gestion des roles et permissions. | Le workflow de validation ne peut pas fonctionner sans le systeme de roles. | **Bloquante** |
| **Module Clients / Contacts** | Les factures referencent les clients (raison sociale, adresse, email, conditions de paiement). | Les informations client doivent etre disponibles. | **Bloquante** |
| **Service d'envoi d'emails** | L'envoi de factures et de relances par email necessite un service de messagerie. | L'envoi ne fonctionnera pas sans le service email. | **Majeure** |

### 10.2 Dependances sortantes (d'autres modules dependent de celui-ci)

| EPIC / Module | Nature de la dependance | Impact |
|---|---|---|
| **EPIC-008 (Finances)** | Le module Finances utilisera les donnees de facturation pour le suivi de tresorerie, le previsionnel et les tableaux de bord financiers. | Les donnees de facturation doivent etre exposees via une API interne. |
| **Module Reporting** | Les rapports financiers de l'agence s'appuieront sur les donnees de facturation (CA facture, encours, delais de paiement). | Les agregats de facturation doivent etre disponibles en lecture. |
| **Module Tableau de bord general** | Le dashboard principal de l'application affichera des widgets de facturation (encours, prochaines echeances). | Les KPIs de facturation doivent etre accessibles via une API. |

### 10.3 Dependances techniques

| Composant | Description | Statut |
|---|---|---|
| **Generateur PDF** | Librairie de generation de PDF pour les factures, avoirs et etats de compte (ex: Puppeteer, WeasyPrint, ou PDFKit). | A selectionner |
| **Service SMTP / provider email** | Service d'envoi d'emails transactionnels pour les factures et relances (ex: SendGrid, Amazon SES, Mailgun). | A selectionner |
| **Scheduler / CRON** | Systeme de taches planifiees pour les relances automatiques et les exports periodiques. | A selectionner |
| **Stockage fichiers** | Stockage des PDF generes (ex: Amazon S3, Google Cloud Storage). | A selectionner |

---

## 11. Modele de Donnees Principal

### 11.1 Entite : Invoice (Facture)

```
Invoice
├── id                  : UUID (PK)
├── reference           : VARCHAR(50) UNIQUE NOT NULL -- Numero de facture (ex: FA-2026-0042)
├── type                : ENUM('invoice', 'credit_note', 'proforma') NOT NULL DEFAULT 'invoice'
├── project_id          : UUID FK -> Project.id NOT NULL
├── fee_project_id      : UUID FK -> FeeProject.id -- Lien vers les honoraires du projet
├── phase_id            : UUID FK -> Phase.id -- Phase d'honoraires facturee
├── client_id           : UUID FK -> Client.id NOT NULL
├── status              : ENUM('draft', 'pending_validation', 'validated', 'rejected',
│                              'sent', 'partially_paid', 'paid', 'overdue',
│                              'cancelled') NOT NULL DEFAULT 'draft'
├── amount_ht           : DECIMAL(12,2) NOT NULL DEFAULT 0 -- Montant hors taxes
├── amount_vat          : DECIMAL(12,2) NOT NULL DEFAULT 0 -- Montant total TVA
├── amount_ttc          : DECIMAL(12,2) NOT NULL DEFAULT 0 -- Montant toutes taxes comprises
├── vat_details         : JSONB -- Detail TVA par taux [{rate: 20, base: 1000, amount: 200}]
├── issue_date          : DATE NOT NULL -- Date d'emission
├── due_date            : DATE NOT NULL -- Date d'echeance
├── payment_date        : DATE -- Date effective de paiement complet
├── sent_date           : DATE -- Date d'envoi au client
├── payment_terms       : VARCHAR(100) -- Conditions de paiement appliquees
├── discount_rate       : DECIMAL(5,2) DEFAULT 0 -- Escompte pour paiement anticipe (%)
├── pdf_url             : VARCHAR(500) -- URL du PDF genere
├── template_id         : UUID FK -> InvoiceTemplate.id -- Template PDF utilise
├── language            : ENUM('fr', 'en') DEFAULT 'fr'
├── internal_notes      : TEXT -- Notes internes (non visibles sur le PDF)
├── external_notes      : TEXT -- Conditions particulieres (visibles sur le PDF)
├── validated_by        : UUID FK -> User.id -- Utilisateur ayant valide
├── validated_at        : TIMESTAMP -- Date de validation
├── cancelled_reason    : TEXT -- Motif d'annulation
├── linked_credit_note  : UUID FK -> Invoice.id -- Lien vers l'avoir associe (si annulee)
├── original_invoice_id : UUID FK -> Invoice.id -- Facture d'origine (pour les avoirs)
├── created_by          : UUID FK -> User.id NOT NULL
├── updated_by          : UUID FK -> User.id
├── created_at          : TIMESTAMP NOT NULL DEFAULT NOW()
├── updated_at          : TIMESTAMP NOT NULL DEFAULT NOW()
└── deleted_at          : TIMESTAMP -- Soft delete (jamais de suppression physique)
```

### 11.2 Entite : InvoiceLine (Ligne de facture)

```
InvoiceLine
├── id                  : UUID (PK)
├── invoice_id          : UUID FK -> Invoice.id NOT NULL
├── position            : INTEGER NOT NULL -- Ordre d'affichage
├── designation         : VARCHAR(500) NOT NULL -- Libelle de la ligne
├── description         : TEXT -- Description detaillee (optionnel)
├── quantity            : DECIMAL(10,3) NOT NULL DEFAULT 1
├── unit                : VARCHAR(20) DEFAULT 'forfait' -- Unite (forfait, heure, m2, etc.)
├── unit_price_ht       : DECIMAL(12,2) NOT NULL -- Prix unitaire HT
├── vat_rate            : DECIMAL(5,2) NOT NULL DEFAULT 20.00 -- Taux de TVA (%)
├── amount_ht           : DECIMAL(12,2) NOT NULL -- Montant HT (quantite x prix unitaire)
├── amount_vat          : DECIMAL(12,2) NOT NULL -- Montant TVA
├── amount_ttc          : DECIMAL(12,2) NOT NULL -- Montant TTC
├── phase_id            : UUID FK -> Phase.id -- Phase associee (optionnel)
├── created_at          : TIMESTAMP NOT NULL DEFAULT NOW()
└── updated_at          : TIMESTAMP NOT NULL DEFAULT NOW()
```

### 11.3 Entite : Payment (Paiement)

```
Payment
├── id                  : UUID (PK)
├── reference           : VARCHAR(100) -- Reference bancaire / numero de cheque
├── client_id           : UUID FK -> Client.id NOT NULL
├── amount              : DECIMAL(12,2) NOT NULL -- Montant recu
├── reception_date      : DATE NOT NULL -- Date de reception du paiement
├── payment_method      : ENUM('bank_transfer', 'check', 'cash', 'direct_debit',
│                              'credit_card', 'other') NOT NULL
├── bank_reference      : VARCHAR(200) -- Reference bancaire complementaire
├── notes               : TEXT -- Commentaires
├── created_by          : UUID FK -> User.id NOT NULL
├── created_at          : TIMESTAMP NOT NULL DEFAULT NOW()
└── updated_at          : TIMESTAMP NOT NULL DEFAULT NOW()
```

### 11.4 Entite : PaymentAllocation (Lettrage paiement-facture)

```
PaymentAllocation
├── id                  : UUID (PK)
├── payment_id          : UUID FK -> Payment.id NOT NULL
├── invoice_id          : UUID FK -> Invoice.id NOT NULL
├── amount              : DECIMAL(12,2) NOT NULL -- Montant affecte a cette facture
├── allocation_type     : ENUM('manual', 'automatic') NOT NULL
├── created_by          : UUID FK -> User.id NOT NULL
├── created_at          : TIMESTAMP NOT NULL DEFAULT NOW()
└── UNIQUE(payment_id, invoice_id) -- Un paiement ne peut etre lettre qu'une fois par facture
```

### 11.5 Entite : Reminder (Relance)

```
Reminder
├── id                  : UUID (PK)
├── invoice_id          : UUID FK -> Invoice.id NOT NULL
├── level               : INTEGER NOT NULL -- Niveau de relance (1, 2, 3, 4)
├── type                : ENUM('automatic', 'manual') NOT NULL
├── channel             : ENUM('email', 'notification', 'postal') NOT NULL DEFAULT 'email'
├── sent_at             : TIMESTAMP NOT NULL -- Date d'envoi
├── recipient_email     : VARCHAR(255) -- Email du destinataire
├── subject             : VARCHAR(500) -- Objet de l'email
├── body                : TEXT -- Contenu de l'email
├── status              : ENUM('sent', 'delivered', 'bounced', 'failed') DEFAULT 'sent'
├── created_by          : UUID FK -> User.id -- NULL si automatique
├── created_at          : TIMESTAMP NOT NULL DEFAULT NOW()
└── updated_at          : TIMESTAMP NOT NULL DEFAULT NOW()
```

### 11.6 Entite : Adjustment (Ajustement / Avoir)

```
Adjustment
├── id                  : UUID (PK)
├── reference           : VARCHAR(50) UNIQUE NOT NULL -- Numero de l'avoir (ex: AV-2026-0003)
├── invoice_id          : UUID FK -> Invoice.id NOT NULL -- Facture d'origine
├── type                : ENUM('full_credit', 'partial_credit', 'supplement',
│                              'commercial_discount') NOT NULL
├── reason              : ENUM('billing_error', 'commercial_discount', 'service_cancellation',
│                              'dispute', 'order_modification', 'other') NOT NULL
├── reason_detail       : TEXT -- Detail du motif (obligatoire si reason = 'other')
├── amount_ht           : DECIMAL(12,2) NOT NULL -- Montant HT (negatif pour avoir, positif pour supplement)
├── vat_rate            : DECIMAL(5,2) NOT NULL
├── amount_vat          : DECIMAL(12,2) NOT NULL
├── amount_ttc          : DECIMAL(12,2) NOT NULL
├── status              : ENUM('draft', 'pending_validation', 'validated', 'rejected') NOT NULL DEFAULT 'draft'
├── pdf_url             : VARCHAR(500)
├── validated_by        : UUID FK -> User.id
├── validated_at        : TIMESTAMP
├── second_validated_by : UUID FK -> User.id -- Double validation pour montants eleves
├── second_validated_at : TIMESTAMP
├── created_by          : UUID FK -> User.id NOT NULL
├── created_at          : TIMESTAMP NOT NULL DEFAULT NOW()
└── updated_at          : TIMESTAMP NOT NULL DEFAULT NOW()
```

### 11.7 Entite : SubcontractorInvoice (Facture co-traitant)

```
SubcontractorInvoice
├── id                  : UUID (PK)
├── reference           : VARCHAR(100) NOT NULL -- Reference de la facture du co-traitant
├── project_id          : UUID FK -> Project.id NOT NULL
├── subcontractor_id    : UUID FK -> Subcontractor.id NOT NULL
├── phase_id            : UUID FK -> Phase.id -- Phase/lot concernee
├── reception_date      : DATE NOT NULL -- Date de reception de la facture
├── amount_ht           : DECIMAL(12,2) NOT NULL
├── vat_rate            : DECIMAL(5,2) NOT NULL
├── amount_vat          : DECIMAL(12,2) NOT NULL
├── amount_ttc          : DECIMAL(12,2) NOT NULL
├── status              : ENUM('received', 'validated', 'paid', 'rejected') NOT NULL DEFAULT 'received'
├── rejection_reason    : TEXT -- Motif de rejet
├── document_url        : VARCHAR(500) -- URL du scan de la facture
├── payment_date        : DATE -- Date de paiement au co-traitant
├── payment_reference   : VARCHAR(200) -- Reference du virement
├── payment_method      : ENUM('bank_transfer', 'check', 'other')
├── created_by          : UUID FK -> User.id NOT NULL
├── created_at          : TIMESTAMP NOT NULL DEFAULT NOW()
└── updated_at          : TIMESTAMP NOT NULL DEFAULT NOW()
```

### 11.8 Entite : InvoiceTemplate (Template de facture)

```
InvoiceTemplate
├── id                  : UUID (PK)
├── name                : VARCHAR(100) NOT NULL -- Nom du template
├── type                : ENUM('invoice', 'credit_note', 'statement', 'proforma') NOT NULL
├── is_default          : BOOLEAN DEFAULT FALSE
├── logo_url            : VARCHAR(500) -- URL du logo
├── primary_color       : VARCHAR(7) DEFAULT '#000000' -- Couleur principale (hex)
├── accent_color        : VARCHAR(7) DEFAULT '#0066CC' -- Couleur d'accent (hex)
├── font_family         : VARCHAR(100) DEFAULT 'Helvetica'
├── header_html         : TEXT -- Template HTML de l'en-tete
├── body_html           : TEXT -- Template HTML du corps
├── footer_html         : TEXT -- Template HTML du pied de page
├── language            : ENUM('fr', 'en') DEFAULT 'fr'
├── agency_id           : UUID FK -> Agency.id NOT NULL
├── created_by          : UUID FK -> User.id NOT NULL
├── created_at          : TIMESTAMP NOT NULL DEFAULT NOW()
└── updated_at          : TIMESTAMP NOT NULL DEFAULT NOW()
```

### 11.9 Entite : InvoiceSettings (Parametres de facturation)

```
InvoiceSettings
├── id                  : UUID (PK)
├── agency_id           : UUID FK -> Agency.id UNIQUE NOT NULL
├── invoice_prefix      : VARCHAR(10) DEFAULT 'FA' -- Prefixe factures
├── credit_note_prefix  : VARCHAR(10) DEFAULT 'AV' -- Prefixe avoirs
├── proforma_prefix     : VARCHAR(10) DEFAULT 'PF' -- Prefixe proformas
├── number_format       : VARCHAR(50) DEFAULT '{prefix}-{year}-{counter:4}'
├── counter_reset_yearly: BOOLEAN DEFAULT TRUE -- Reinitialisation annuelle
├── current_counter     : INTEGER DEFAULT 0 -- Compteur courant
├── current_cn_counter  : INTEGER DEFAULT 0 -- Compteur avoirs courant
├── default_vat_rate    : DECIMAL(5,2) DEFAULT 20.00
├── additional_vat_rates: JSONB DEFAULT '[]' -- Taux supplementaires [10, 5.5, 0]
├── default_payment_days: INTEGER DEFAULT 30 -- Delai de paiement par defaut
├── payment_terms_type  : ENUM('calendar_days', 'end_of_month', 'end_of_month_10th') DEFAULT 'calendar_days'
├── early_payment_discount: DECIMAL(5,2) DEFAULT 0 -- Escompte (%)
├── late_payment_rate   : DECIMAL(5,2) DEFAULT 10.00 -- Taux penalites de retard (%)
├── recovery_fee        : DECIMAL(8,2) DEFAULT 40.00 -- Indemnite forfaitaire recouvrement (EUR)
├── bank_name           : VARCHAR(200)
├── bank_iban           : VARCHAR(34)
├── bank_bic            : VARCHAR(11)
├── bank_account_holder : VARCHAR(200)
├── reminder_level1_days: INTEGER DEFAULT 7 -- Relance 1 : X jours apres echeance
├── reminder_level2_days: INTEGER DEFAULT 15 -- Relance 2 : X jours apres R1
├── reminder_level3_days: INTEGER DEFAULT 30 -- Relance 3 : X jours apres R2
├── reminder_level4_days: INTEGER DEFAULT 45 -- Relance 4 : X jours apres R3
├── validation_threshold: DECIMAL(12,2) DEFAULT 5000.00 -- Seuil validation directeur
├── credit_note_double_validation_threshold: DECIMAL(12,2) DEFAULT 1000.00
├── created_at          : TIMESTAMP NOT NULL DEFAULT NOW()
└── updated_at          : TIMESTAMP NOT NULL DEFAULT NOW()
```

### 11.10 Entite : InvoiceHistory (Historique / Audit)

```
InvoiceHistory
├── id                  : UUID (PK)
├── invoice_id          : UUID FK -> Invoice.id NOT NULL
├── action              : ENUM('created', 'updated', 'status_changed', 'sent',
│                              'reminder_sent', 'payment_received', 'validated',
│                              'rejected', 'cancelled', 'pdf_generated') NOT NULL
├── old_status          : VARCHAR(30) -- Statut avant l'action
├── new_status          : VARCHAR(30) -- Statut apres l'action
├── details             : JSONB -- Details de la modification (champs modifies, etc.)
├── comment             : TEXT -- Commentaire de l'utilisateur
├── performed_by        : UUID FK -> User.id NOT NULL
├── performed_at        : TIMESTAMP NOT NULL DEFAULT NOW()
└── ip_address          : VARCHAR(45) -- Adresse IP pour l'audit
```

### 11.11 Diagramme de relations simplifie

```
                                    ┌──────────────────┐
                                    │    Project        │
                                    │    (EPIC-002)     │
                                    └────────┬─────────┘
                                             │ 1
                                             │
                                             │ *
┌──────────────┐    1    *    ┌──────────────────────────┐    *    1    ┌──────────────┐
│   Client     │◄─────────────│       Invoice            │─────────────►│  FeeProject  │
│              │              │                          │              │  (EPIC-003)  │
└──────┬───────┘              └──────┬───────┬───────────┘              └──────────────┘
       │                             │       │
       │ 1                      1    │       │ 1
       │                             │       │
       │ *                      *    │       │ *
┌──────────────┐    ┌──────────────┐ │  ┌─────────────────┐
│   Payment    │    │ InvoiceLine  │ │  │  InvoiceHistory  │
│              │    │              │ │  │                   │
└──────┬───────┘    └──────────────┘ │  └───────────────────┘
       │                             │
       │ *                      1    │
       │                             │
       │ *                      *    │
┌─────────────────────┐   ┌─────────────────┐   ┌──────────────────────┐
│ PaymentAllocation   │   │    Reminder      │   │    Adjustment        │
│                     │   │                  │   │                      │
└─────────────────────┘   └──────────────────┘   └──────────────────────┘

┌───────────────────────┐   ┌──────────────────┐   ┌──────────────────────┐
│ SubcontractorInvoice  │   │ InvoiceTemplate  │   │  InvoiceSettings     │
│                       │   │                  │   │                      │
└───────────────────────┘   └──────────────────┘   └──────────────────────┘
```

---

## 12. Estimation & Decoupage

### 12.1 Estimation globale

| Parametre | Valeur |
|---|---|
| **Duree estimee** | 10 semaines (8 a 12 semaines selon la capacite de l'equipe) |
| **Nombre de sprints** | 5 sprints de 2 semaines |
| **Effort total estime** | 400-500 points de story (reference : equipe de 4 developpeurs) |
| **Complexite** | Elevee (integration multi-modules, reglementaire, generation PDF) |

### 12.2 Decoupage en sprints

#### Sprint 1 — Fondations et modele de donnees (semaines 1-2)

| Tache | User Stories | Story Points | Priorite |
|---|---|---|---|
| Modele de donnees complet (migrations, entites, relations) | Toutes | 20 | P0 |
| API CRUD Invoice (creation, lecture, mise a jour) | US-F03, US-F04 | 25 | P0 |
| API CRUD InvoiceLine | US-F03 | 15 | P0 |
| Parametres de facturation et numerotation | US-F13 | 20 | P0 |
| Interface creation/edition de facture | US-F03, US-F04 | 25 | P0 |
| **Total Sprint 1** | | **105** | |

#### Sprint 2 — Workflow, validation et envoi (semaines 3-4)

| Tache | User Stories | Story Points | Priorite |
|---|---|---|---|
| Workflow de statuts et machine a etats | US-F04 | 20 | P0 |
| Systeme de validation (regles, seuils, notifications) | US-F04 | 25 | P0 |
| Generation PDF (template par defaut) | US-F12 | 30 | P0 |
| Envoi de facture par email | US-F05 | 20 | P0 |
| Historique et audit des factures | US-F04 | 15 | P1 |
| **Total Sprint 2** | | **110** | |

#### Sprint 3 — Paiements, relances et ajustements (semaines 5-6)

| Tache | User Stories | Story Points | Priorite |
|---|---|---|---|
| API et interface paiements (enregistrement, lettrage) | US-F07 | 30 | P0 |
| Gestion des paiements partiels et trop-percus | US-F07 | 15 | P0 |
| Systeme de relances (configuration, execution, historique) | US-F06 | 30 | P1 |
| Relances automatiques (scheduler) | US-F06 | 15 | P1 |
| Ajustements et avoirs (creation, validation, PDF) | US-F10 | 25 | P1 |
| **Total Sprint 3** | | **115** | |

#### Sprint 4 — Tableaux de bord, planning et etats de compte (semaines 7-8)

| Tache | User Stories | Story Points | Priorite |
|---|---|---|---|
| Tableau de bord facturation agence (KPIs, graphiques) | US-F01 | 30 | P0 |
| Tableau de bord facturation projet | US-F14 | 20 | P0 |
| Planning de facturation (vue calendaire, drag & drop) | US-F02 | 25 | P1 |
| Etat de compte client (vue, export PDF, envoi) | US-F08 | 20 | P1 |
| **Total Sprint 4** | | **95** | |

#### Sprint 5 — Co-traitants, exports et personnalisation (semaines 9-10)

| Tache | User Stories | Story Points | Priorite |
|---|---|---|---|
| Facturation co-traitants (enregistrement, suivi, marge) | US-F11 | 25 | P1 |
| Exports comptables (CSV, Excel, FEC) | US-F09 | 25 | P1 |
| Personnalisation des templates PDF | US-F12 | 20 | P2 |
| Gestion TVA multi-taux et autoliquidation | US-F03 | 15 | P1 |
| Tests de bout en bout, corrections, stabilisation | Toutes | 20 | P0 |
| **Total Sprint 5** | | **105** | |

### 12.3 Synthese par priorite

| Priorite | Description | Story Points | Pourcentage |
|---|---|---|---|
| **P0 — Indispensable** | Creation, edition, envoi de factures, paiements, numerotation, tableaux de bord, validation | 300 | 57% |
| **P1 — Important** | Relances, planning, exports, co-traitants, etats de compte, ajustements | 180 | 34% |
| **P2 — Souhaitable** | Personnalisation avancee PDF, multi-langues, exports automatiques | 50 | 9% |
| **Total** | | **530** | 100% |

### 12.4 Risques et mitigations

| Risque | Probabilite | Impact | Mitigation |
|---|---|---|---|
| Complexite de la generation PDF (mise en page, polices, multi-langues) | Haute | Moyen | POC technique en Sprint 0 ; selection precoce de la librairie PDF |
| Integration avec EPIC-003 (Honoraires) non finalisee | Moyenne | Fort | Definir l'API d'interface des le Sprint 1 ; donnees mockees si necessaire |
| Performance des KPIs sur grands volumes | Moyenne | Moyen | Mise en cache des agregats ; vues materialisees en base de donnees |
| Conformite reglementaire (numerotation, mentions legales, FEC) | Moyenne | Fort | Validation par un expert-comptable des les premieres specifications |
| Gestion de la concurrence (numerotation sequentielle) | Moyenne | Fort | Mecanisme de verrou (lock) sur la table de numerotation ; tests de charge |

---

*Document redige en fevrier 2026 — Version 1.0*
*A valider par : Product Owner, Architecte Technique, Expert Metier (comptabilite)*
