# EPIC -- Audit ChangePoint : Module Facturation (Invoices & Contracts)

**Application concurrente auditee : Planview ChangePoint**
**URL : https://provencherroy.changepointasp.com/**
**Version du document : 1.0 -- Fevrier 2026**

---

## 1. Identification

| Champ | Valeur |
|---|---|
| **Nom de l'EPIC** | Facturation (Invoices & Contracts) -- Audit ChangePoint |
| **Reference** | EPIC-CP-FACTURATION |
| **Module audite** | Invoices + Contracts (ChangePoint) |
| **Priorite** | Critique |
| **Auteur** | Architecte logiciel senior |
| **Date de creation** | 27 fevrier 2026 |
| **Version du document** | 1.0 |
| **Statut** | Brouillon |
| **Application cible** | Planview ChangePoint (instance Provencher Roy) |
| **Entites concernees** | Provencher Roy Prod, PRAA (Provencher Roy Associes architectes Inc.) |
| **Devise** | CAD (Dollar canadien) |
| **EPICs OOTI lies** | EPIC-004 (Facturation), EPIC-002 (Projets), EPIC-003 (Honoraires), EPIC-005 (Temps), EPIC-008 (Finances), EPIC-010 (Clients), EPIC-012 (Validation) |

---

## 2. Contexte et Justification

### 2.1 Contexte de l'audit

Le cabinet Provencher Roy utilise actuellement **Planview ChangePoint** comme outil de gestion de la facturation et des contrats. Les modules Invoices et Contracts de ChangePoint constituent le coeur financier de l'activite du cabinet : ils permettent de gerer le cycle de vie complet d'une facture, de la creation du contrat client jusqu'a la reception du paiement, en passant par un workflow d'approbation rigoureux et un suivi comptable precis.

L'audit de ces modules vise a identifier exhaustivement les fonctionnalites existantes, les flux utilisateur, les regles metier et les contraintes techniques afin de concevoir un module equivalent ou superieur dans l'application OOTI. Le cabinet Provencher Roy opere avec **plusieurs entites juridiques** (Provencher Roy Prod pour la production, PRAA -- Provencher Roy Associes architectes Inc. pour la holding/administration), ce qui implique une gestion multi-entites des contrats, des factures et des bureaux de facturation. Des mecanismes de facturation intercompagnie sont egalement en place pour les transferts financiers entre entites (ex : Projet 130094 -- Provencher Roy Design Inc. Interco).

Les projets du cabinet se declinent en trois categories ayant chacune un traitement de facturation distinct :
- **Projets clients numerotes** : facturables, un contrat est obligatoire pour emettre des factures
- **Projets administratifs** : facturables dans certains cas (suivi des couts uniquement)
- **Projets departementaux PRAA** : non facturables, usage interne exclusivement

### 2.2 Problematique identifiee

L'interface actuelle de ChangePoint pour les modules Invoices et Contracts presente plusieurs limites fonctionnelles et ergonomiques que l'application OOTI devra depasser :

- **Workflow d'approbation rigide** : le systeme de double approbation est present mais la configuration des niveaux d'approbation (simple, double, triple) n'est pas flexible par type de facture ou par montant
- **Absence de tableau de bord facturation** : pas de vue synthetique consolidee des factures en cours, des montants dus, des retards de paiement ou de l'evolution du chiffre d'affaires
- **Gestion des avoirs limitee** : le statut "Credited" (avoir) existe mais le processus de creation d'avoir partiel ou de liaison entre une facture et son avoir n'est pas suffisamment automatise
- **Suivi des paiements partiels basique** : le statut "Partially Paid" existe mais il manque un echeancier de paiement detaille avec suivi des echeances
- **KPIs financiers disperses** : les indicateurs Revenue, Cost, Profit et Margin % sont disponibles au niveau projet mais ne sont pas consolides dans une vue transversale accessible depuis le module facturation
- **Export et impression limites** : les options d'export de factures ne couvrent pas tous les formats requis (PDF personnalise avec logo, CSV pour import comptable, XML pour EDI)
- **Intercompagnie peu visible** : les mecanismes de transfert intercompagnie existent (projet 130094) mais ne sont pas clairement distingues dans l'interface des factures regulieres
- **Filtres de recherche sommaires** : les filtres disponibles (Status, Customer, Project, Date range) sont fonctionnels mais ne permettent pas de combinaisons avancees ni de sauvegarde de filtres favoris

### 2.3 Justification strategique

L'application OOTI doit proposer un module Facturation (Invoices & Contracts) qui :

1. **Reproduit fidelement** toutes les fonctionnalites essentielles de ChangePoint pour assurer une migration sans perte fonctionnelle, y compris les 10 statuts de facture, le workflow de double approbation et la gestion des Billing Roles & Rates
2. **Ameliore l'ergonomie** avec une interface moderne offrant une meilleure visibilite sur le cycle de vie des factures
3. **Enrichit le workflow d'approbation** avec une configuration flexible du nombre de niveaux d'approbation, des seuils de montant declenchant la double approbation, et des notifications proactives
4. **Ajoute un tableau de bord facturation** avec des KPIs consolides (chiffre d'affaires, encours, retards, marges) absents de ChangePoint
5. **Ameliore la gestion des paiements** avec un suivi des echeances, une gestion fine des paiements partiels et des relances automatiques
6. **Renforce le module intercompagnie** avec une separation claire entre les factures clients et les ecritures intercompagnie
7. **Offre des exports avances** : PDF personnalise, CSV comptable, integration avec les logiciels de comptabilite

---

## 3. Objectif de l'EPIC

Concevoir et specifier le module **Facturation (Invoices & Contracts)** de l'application OOTI en s'appuyant sur l'audit exhaustif des modules Invoices et Contracts de Planview ChangePoint. L'objectif est de garantir une **parite fonctionnelle complete** avec ChangePoint tout en apportant des ameliorations significatives en termes d'ergonomie, de flexibilite et de fonctionnalites complementaires.

Les objectifs specifiques sont :

- **Gestion des contrats** : permettre la creation, la modification et le suivi des contrats clients, avec configuration des roles de facturation (Billing Roles), des taux horaires standards, des remises et des taux effectifs de facturation
- **Cycle de vie complet des factures** : implementer les 10 statuts de facture identifies dans ChangePoint (Draft, Pending Approval, Pending Second Approval, Approved, Committed, Sent, Paid, Partially Paid, Credited, Archived) avec les transitions autorisees entre statuts
- **Workflow d'approbation configurable** : implementer un flux d'approbation simple (un niveau) et double (deux niveaux) conforme aux pratiques de ChangePoint, avec la possibilite d'etendre a des configurations personnalisees
- **KPIs financiers** : reproduire et consolider les indicateurs Revenue, Cost, Profit et Margin % existants au niveau projet dans ChangePoint, et les rendre accessibles depuis le module facturation
- **Multi-entites** : supporter la gestion multi-entites (Provencher Roy Prod, PRAA) avec des bureaux de facturation distincts par entite et une traçabilite des factures par entite emettrice
- **Intercompagnie** : gerer les ecritures de facturation intercompagnie entre les entites du groupe
- **Recherche et filtrage avances** : offrir des filtres combines avec sauvegarde de filtres favoris, au-dela des filtres basiques de ChangePoint
- **Export et impression** : generer des factures au format PDF personnalise (avec logo, mentions legales, coordonnees bancaires) et des exports CSV pour import comptable
- **Tableau de bord facturation** : ajouter une vue synthetique absente de ChangePoint avec les indicateurs cles de la facturation

---

## 4. Perimetre Fonctionnel

| Ref | Fonctionnalite | Source ChangePoint | Statut OOTI | Priorite |
|---|---|---|---|---|
| PF-01 | Creation et gestion de contrats | Onglet Contracts | A reproduire | Critique |
| PF-02 | Configuration des Billing Roles & Rates par contrat | Sous-onglet Billing Roles & Rates | A reproduire | Critique |
| PF-03 | Gestion des taux (Standard Rate, Discount %, Billing Rate) | Billing Roles & Rates grid | A reproduire | Critique |
| PF-04 | Liaison contrat-projet-client | Contract header fields | A reproduire | Critique |
| PF-05 | Liste des factures avec colonnes (Invoice #, Project, Customer, Amount, Status, Date) | Onglet Invoices | A reproduire | Critique |
| PF-06 | Creation de facture en mode Draft | Invoice creation form | A reproduire | Critique |
| PF-07 | Workflow d'approbation simple (Pending Approval -> Approved) | Approval workflow | A reproduire | Critique |
| PF-08 | Workflow de double approbation (Pending Approval -> Pending Second Approval -> Approved) | Double approval workflow | A reproduire | Haute |
| PF-09 | Engagement comptable (Committed) | Status transition | A reproduire | Haute |
| PF-10 | Envoi de facture au client (Sent) | Status transition + notification | A reproduire | Haute |
| PF-11 | Enregistrement de paiement (Paid) | Status transition | A reproduire | Critique |
| PF-12 | Gestion des paiements partiels (Partially Paid) | Status transition | A reproduire | Haute |
| PF-13 | Emission d'avoir / note de credit (Credited) | Status transition | A reproduire | Haute |
| PF-14 | Archivage de facture (Archived) | Status transition | A reproduire | Moyenne |
| PF-15 | Filtrage et recherche de factures (Status, Customer, Project, Date range) | Filter panel | A reproduire et etendre | Haute |
| PF-16 | KPIs financiers (Revenue, Cost, Profit, Margin %) | Project financial view | A reproduire et consolider | Haute |
| PF-17 | Multi-entites et bureaux de facturation | Entity management + Billing Office | A reproduire | Critique |
| PF-18 | Facturation intercompagnie | Projet 130094 Interco | A reproduire et ameliorer | Haute |
| PF-19 | Export de facture en PDF | Export function | A reproduire et ameliorer | Haute |
| PF-20 | Export de donnees de facturation en CSV | Non present ou limite dans ChangePoint | A ajouter | Moyenne |
| PF-21 | Impression de facture | Print function | A reproduire | Moyenne |
| PF-22 | Tableau de bord facturation | Non present dans ChangePoint | A ajouter | Haute |
| PF-23 | Numerotation sequentielle automatique des factures | Invoice # auto-increment | A reproduire | Critique |
| PF-24 | Devise de facturation (CAD par defaut) | Billing Currency | A reproduire | Critique |
| PF-25 | Historique des actions sur une facture (audit trail) | Non present ou limite dans ChangePoint | A ajouter | Moyenne |

---

## 5. User Stories detaillees

---

### US-CF-01 -- Creation et configuration d'un contrat

**En tant que** gestionnaire de projets ou directeur financier
**Je veux** creer un contrat lie a un projet et a un client, en configurant les informations contractuelles essentielles
**Afin de** formaliser les conditions de facturation avant d'emettre la premiere facture du projet

| # | Critere d'acceptation |
|---|---|
| 1 | Un bouton "Nouveau contrat" est accessible depuis le module Contracts dans la barre de navigation principale |
| 2 | Le formulaire de creation de contrat comprend les champs obligatoires : nom du contrat, projet associe (selection dans une liste), client associe (pre-rempli a partir du projet), entite emettrice (Provencher Roy Prod ou PRAA), bureau de facturation (Billing Office), devise de facturation (defaut : CAD), date de debut, date de fin previsionnelle |
| 3 | Le contrat ne peut etre cree que si un projet valide et un client valide sont selectionnes ; une erreur explicite est affichee si l'un des deux est manquant |
| 4 | A la creation, le contrat recoit un identifiant unique genere automatiquement selon le format de numerotation configure par entite |
| 5 | Le contrat cree est automatiquement associe au projet selectionne ; cette association est visible dans le module Projets (EPIC-002) |
| 6 | Le bureau de facturation (Billing Office) est pre-selectionne en fonction de l'entite emettrice mais modifiable par l'utilisateur |
| 7 | Un contrat peut etre sauvegarde en mode "Brouillon" sans que tous les champs facultatifs soient remplis |
| 8 | Le formulaire de creation affiche un recapitulatif avant la sauvegarde avec tous les champs renseignes |
| 9 | Un contrat sauvegarde est immediatement visible dans la liste des contrats avec son statut, son projet et son client |
| 10 | Les champs de date (debut, fin) sont valides : la date de fin doit etre posterieure ou egale a la date de debut |

---

### US-CF-02 -- Configuration des Billing Roles & Rates

**En tant que** gestionnaire de projets ou directeur financier
**Je veux** configurer les roles de facturation (Billing Roles) et leurs taux horaires dans un contrat
**Afin de** definir les taux de facturation applicables pour chaque type de collaborateur intervenant sur le projet

| # | Critere d'acceptation |
|---|---|
| 1 | Un sous-onglet "Billing Roles & Rates" est accessible depuis la fiche detaillee d'un contrat |
| 2 | Le sous-onglet affiche une grille editable avec les colonnes : Role, Standard Rate (CAD), Discount %, Billing Rate (CAD), Billing Currency |
| 3 | Les roles disponibles incluent au minimum : Architecte, Designer, Technicien, Chef de projet, Directeur, Stagiaire, Consultant ; la liste des roles est configurable par un administrateur |
| 4 | Le Standard Rate (taux horaire standard) est saisi manuellement en valeur decimale positive (ex : 125.00 CAD) |
| 5 | Le Discount % (pourcentage de remise) est saisi en valeur decimale entre 0 et 100 (ex : 10, 15, 20.5) |
| 6 | Le Billing Rate (taux effectif de facturation) est calcule automatiquement selon la formule : Billing Rate = Standard Rate x (1 - Discount% / 100) ; il est affiche en temps reel a chaque modification du Standard Rate ou du Discount % |
| 7 | La devise de facturation (Billing Currency) est pre-remplie avec la devise du contrat (CAD) et modifiable exceptionnellement |
| 8 | Plusieurs roles peuvent etre configures dans un meme contrat ; chaque role ne peut apparaitre qu'une seule fois par contrat |
| 9 | Un bouton "Ajouter un role" permet d'ajouter une nouvelle ligne dans la grille des Billing Roles & Rates |
| 10 | Un role peut etre supprime de la grille uniquement s'il n'a pas encore ete utilise pour une facturation ; un message d'avertissement est affiche si une tentative de suppression concerne un role deja facture |
| 11 | Les modifications des taux sont sauvegardees avec un historique des versions (date de modification, ancien taux, nouveau taux, utilisateur ayant effectue la modification) |

---

### US-CF-03 -- Gestion des taux de facturation (Standard Rate, Discount, Billing Rate)

**En tant que** directeur financier ou associe
**Je veux** ajuster les taux horaires standards, les pourcentages de remise et visualiser les taux effectifs de facturation pour chaque role d'un contrat
**Afin de** adapter les conditions tarifaires aux negociations commerciales avec le client tout en conservant la traçabilite des modifications

| # | Critere d'acceptation |
|---|---|
| 1 | Le Standard Rate est modifiable a tout moment tant que le contrat n'est pas cloture ; la modification est effective pour les futures factures uniquement (pas d'effet retroactif sur les factures deja emises) |
| 2 | Le Discount % est modifiable a tout moment ; la modification est effective pour les futures factures uniquement |
| 3 | Le Billing Rate est recalcule automatiquement et instantanement a chaque modification du Standard Rate ou du Discount % |
| 4 | Une modification de taux est tracee dans l'historique du contrat avec : la date de modification, l'utilisateur ayant effectue la modification, l'ancien taux, le nouveau taux, le motif de la modification (champ optionnel) |
| 5 | Un taux a zero (Standard Rate = 0.00 ou Billing Rate = 0.00) est autorise pour les roles pro bono ou les interventions gratuites, avec un avertissement visuel ("Taux a zero : facturation gratuite") |
| 6 | Un Discount % de 100% est autorise, entrainant un Billing Rate de 0.00 ; un avertissement est affiche pour confirmer l'intention |
| 7 | Le Standard Rate ne peut pas etre negatif ; une erreur de validation est affichee si une valeur negative est saisie |
| 8 | Les taux sont affiches avec deux decimales systematiquement (ex : 125.00, 0.50, 99.99) |
| 9 | Un recapitulatif des taux est accessible depuis la fiche contrat, affichant pour chaque role le taux standard, la remise et le taux effectif dans un format lisible |
| 10 | Lors de la creation d'une facture, les taux effectifs (Billing Rate) du contrat sont automatiquement appliques aux lignes de facturation correspondant a chaque role |

---

### US-CF-04 -- Creation d'une facture (Draft)

**En tant que** gestionnaire de projets, comptable ou directeur financier
**Je veux** creer une nouvelle facture en mode brouillon (Draft) a partir d'un contrat existant
**Afin de** preparer une facture avant de la soumettre au workflow d'approbation

| # | Critere d'acceptation |
|---|---|
| 1 | Un bouton "Nouvelle facture" est accessible depuis le module Invoices dans la barre de navigation principale et depuis la sous-section "Invoices" d'un contrat |
| 2 | Le formulaire de creation de facture comprend les champs obligatoires : contrat associe (selection dans une liste), projet (pre-rempli a partir du contrat), client (pre-rempli a partir du contrat), entite emettrice (pre-remplie a partir du contrat), date de facturation, periode de facturation (du/au), objet de la facture (description libre) |
| 3 | Le numero de facture (Invoice #) est genere automatiquement selon la sequence de numerotation de l'entite emettrice ; il est affiche en lecture seule |
| 4 | La facture est creee avec le statut initial "Draft" (Brouillon) |
| 5 | Les lignes de facture sont ajoutees manuellement ou generees automatiquement a partir des heures approuvees de la periode selectionnee, en appliquant les Billing Rates du contrat |
| 6 | Chaque ligne de facture comprend : role (Billing Role), nombre d'heures, taux horaire (Billing Rate), montant total de la ligne (heures x taux), description |
| 7 | Le montant total de la facture est calcule automatiquement comme la somme des lignes de facture ; il est affiche en temps reel |
| 8 | Une facture en mode Draft est entierement editable : ajout, modification et suppression de lignes, modification des champs d'en-tete |
| 9 | La facture en Draft peut etre sauvegardee et reprise ulterieurement sans perte de donnees |
| 10 | Une facture ne peut etre creee que si le contrat associe est actif et si le projet associe est un projet client facturable |

---

### US-CF-05 -- Workflow d'approbation simple

**En tant que** gestionnaire de projets
**Je veux** soumettre une facture Draft pour approbation aupres d'un approbateur designe
**Afin de** obtenir la validation necessaire avant l'engagement comptable et l'envoi de la facture au client

| # | Critere d'acceptation |
|---|---|
| 1 | Un bouton "Soumettre pour approbation" est visible sur une facture en statut "Draft" |
| 2 | La soumission change le statut de la facture de "Draft" a "Pending Approval" (En attente d'approbation) |
| 3 | Une notification (email et/ou in-app) est envoyee automatiquement a l'approbateur designe, contenant le numero de facture, le client, le montant et un lien direct vers la facture |
| 4 | Une facture en statut "Pending Approval" est verrouillee en edition : les champs et les lignes ne sont plus modifiables tant que la facture n'est pas rejetee ou ramenee en Draft |
| 5 | L'approbateur peut effectuer trois actions sur une facture en "Pending Approval" : Approuver, Rejeter (avec motif obligatoire), ou Demander des modifications (avec commentaire) |
| 6 | L'approbation change le statut de la facture de "Pending Approval" a "Approved" (Approuvee) |
| 7 | Le rejet change le statut de la facture de "Pending Approval" a "Draft" avec le motif de rejet enregistre et visible par l'emetteur |
| 8 | Une notification de rejet est envoyee a l'emetteur de la facture avec le motif du rejet |
| 9 | L'emetteur d'une facture rejetee peut la modifier puis la resoumettre pour approbation |
| 10 | L'historique des actions d'approbation (soumission, approbation, rejet) est conserve avec la date, l'heure, l'utilisateur et le commentaire eventuel |

---

### US-CF-06 -- Workflow de double approbation

**En tant que** directeur financier ou associe
**Je veux** configurer un workflow de double approbation pour certaines factures (par montant ou par type de projet)
**Afin de** garantir un controle supplementaire sur les factures a fort enjeu financier avant leur engagement comptable

| # | Critere d'acceptation |
|---|---|
| 1 | Un parametre de configuration permet d'activer la double approbation par entite, par projet ou par seuil de montant (ex : double approbation obligatoire pour les factures > 50 000 CAD) |
| 2 | Lorsque la double approbation est activee, l'approbation du premier niveau change le statut de "Pending Approval" a "Pending Second Approval" (En attente de seconde approbation) |
| 3 | Le second approbateur est distinct du premier approbateur ; un meme utilisateur ne peut pas approuver les deux niveaux d'une meme facture |
| 4 | Une notification est envoyee au second approbateur lorsque le premier niveau d'approbation est accorde |
| 5 | Le second approbateur peut Approuver ou Rejeter la facture ; l'approbation du second niveau change le statut a "Approved" |
| 6 | Le rejet au second niveau ramene la facture au statut "Draft" avec le motif de rejet ; l'emetteur et le premier approbateur sont notifies |
| 7 | L'interface affiche clairement a quel niveau d'approbation se trouve la facture (indicateur visuel : "Approbation 1/2" ou "Approbation 2/2") |
| 8 | L'historique d'approbation distingue les deux niveaux avec les informations de chaque approbateur |
| 9 | La configuration de la double approbation est geree par un administrateur dans les parametres de l'entite ou du projet |
| 10 | Si la double approbation est desactivee apres avoir ete active, les factures deja en "Pending Second Approval" conservent leur statut et doivent toujours etre approuvees au second niveau |

---

### US-CF-07 -- Engagement comptable (Committed)

**En tant que** comptable ou directeur financier
**Je veux** engager comptablement une facture approuvee
**Afin de** enregistrer la facture dans le systeme comptable et la rendre eligible a l'envoi au client

| # | Critere d'acceptation |
|---|---|
| 1 | Un bouton "Engager" (Commit) est visible sur une facture en statut "Approved" |
| 2 | L'engagement change le statut de la facture de "Approved" a "Committed" (Engagee) |
| 3 | Une facture en statut "Committed" est definitivement verrouillee en edition : aucune modification des lignes ou des montants n'est possible |
| 4 | L'engagement comptable enregistre la date d'engagement et l'utilisateur ayant effectue l'action |
| 5 | La facture engagee est incluse dans les ecritures comptables de la periode correspondante et visible dans les rapports financiers |
| 6 | Une facture engagee ne peut pas revenir au statut "Approved" ou "Draft" sauf par annulation via l'emission d'un avoir (Credit Note) |
| 7 | L'engagement met a jour les KPIs financiers du projet : le Revenue reconnu est incremente du montant de la facture |
| 8 | Un message de confirmation est demande avant l'engagement, rappelant que l'action est irreversible (hors avoir) |
| 9 | Seuls les utilisateurs ayant le role "Comptable" ou "Directeur financier" peuvent engager une facture |
| 10 | Un numero d'ecriture comptable peut etre associe a la facture engagee (champ optionnel pour lien avec le systeme comptable externe) |

---

### US-CF-08 -- Envoi de facture au client

**En tant que** comptable ou gestionnaire administratif
**Je veux** envoyer une facture engagee au client par email ou la marquer comme envoyee
**Afin de** declencher le processus de recouvrement et tracer la date d'envoi

| # | Critere d'acceptation |
|---|---|
| 1 | Un bouton "Envoyer" (Send) est visible sur une facture en statut "Committed" |
| 2 | L'envoi change le statut de la facture de "Committed" a "Sent" (Envoyee) |
| 3 | L'envoi peut se faire de deux manieres : envoi automatique par email (avec la facture PDF en piece jointe) ou marquage manuel comme "Envoyee" (pour les envois postaux ou manuels) |
| 4 | En cas d'envoi par email, le formulaire d'envoi pre-remplit l'adresse email du contact facturation du client et propose un objet et un corps de message par defaut personnalisables |
| 5 | La date d'envoi est enregistree automatiquement et affichee sur la fiche de la facture |
| 6 | L'adresse email du destinataire, la date et l'heure d'envoi sont tracees dans l'historique de la facture |
| 7 | La facture envoyee reste en lecture seule ; aucune modification n'est possible |
| 8 | Un rappel peut etre envoye (re-envoi) sans changer le statut ; chaque rappel est trace avec sa date |
| 9 | Le delai de paiement (echeance) est calcule automatiquement a partir de la date d'envoi et des conditions de paiement du contrat (ex : 30 jours net) |
| 10 | Une alerte est generee automatiquement si le paiement n'est pas recu a l'echeance |

---

### US-CF-09 -- Reception de paiement (Paid)

**En tant que** comptable
**Je veux** enregistrer la reception du paiement complet d'une facture
**Afin de** cloturer la facture et mettre a jour les indicateurs financiers du projet

| # | Critere d'acceptation |
|---|---|
| 1 | Un bouton "Enregistrer un paiement" est visible sur une facture en statut "Sent" ou "Partially Paid" |
| 2 | Le formulaire de paiement comprend : montant recu, date de reception, mode de paiement (virement, cheque, carte), reference de paiement (numero de cheque, reference virement) |
| 3 | Si le montant recu correspond au montant total de la facture (a une tolerance de 0.01 CAD pres), le statut passe a "Paid" (Payee) |
| 4 | La date de paiement est enregistree et affichee sur la fiche de la facture |
| 5 | Le paiement met a jour les KPIs financiers du projet : les encaissements sont incrementes du montant recu |
| 6 | Un historique des paiements est conserve avec le detail de chaque paiement recu (montant, date, mode, reference) |
| 7 | La facture payee est definitivement fermee ; seul un avoir (Credit Note) peut annuler ou corriger le montant |
| 8 | Le delai de paiement effectif (nombre de jours entre la date d'envoi et la date de paiement) est calcule et stocke pour les statistiques de recouvrement |
| 9 | Un recapitulatif du paiement est affiche apres enregistrement, confirmant le passage au statut "Paid" |
| 10 | Le montant du paiement ne peut pas etre negatif ni exceder le solde restant du (montant facture - paiements anterieurs) |

---

### US-CF-10 -- Gestion des paiements partiels (Partially Paid)

**En tant que** comptable
**Je veux** enregistrer un paiement partiel sur une facture envoyee
**Afin de** tracer les paiements echelonnes et suivre le solde restant du

| # | Critere d'acceptation |
|---|---|
| 1 | Si le montant recu est inferieur au montant total de la facture, le statut passe a "Partially Paid" (Partiellement payee) |
| 2 | Le solde restant du est calcule automatiquement : Solde = Montant total - Somme des paiements recus |
| 3 | Le solde restant du est affiche en evidence sur la fiche de la facture en statut "Partially Paid" |
| 4 | Plusieurs paiements partiels peuvent etre enregistres sur une meme facture ; chaque paiement est trace individuellement |
| 5 | Lorsque la somme des paiements partiels atteint le montant total de la facture (a une tolerance de 0.01 CAD pres), le statut passe automatiquement a "Paid" |
| 6 | Un historique detaille des paiements partiels est accessible depuis la fiche de la facture, avec pour chaque paiement : numero d'ordre, montant, date, mode, reference, solde restant apres paiement |
| 7 | Le pourcentage de paiement recu est affiche visuellement (barre de progression ou pourcentage) |
| 8 | Les KPIs financiers du projet sont mis a jour incrementalement a chaque paiement partiel recu |
| 9 | Un montant de paiement partiel de 0.00 est interdit ; une validation empeche la saisie |
| 10 | L'alerte d'echeance depassee reste active pour le solde restant du d'une facture partiellement payee |

---

### US-CF-11 -- Emission d'avoir / note de credit (Credit Note)

**En tant que** comptable ou directeur financier
**Je veux** emettre un avoir (Credit Note) sur une facture existante
**Afin de** corriger une erreur de facturation, accorder une remise exceptionnelle ou annuler une facture deja engagee

| # | Critere d'acceptation |
|---|---|
| 1 | Un bouton "Emettre un avoir" est accessible depuis une facture en statut "Committed", "Sent", "Paid" ou "Partially Paid" |
| 2 | Le formulaire d'avoir comprend : facture de reference (pre-remplie), montant de l'avoir (total ou partiel), motif de l'avoir (champ obligatoire), date de l'avoir |
| 3 | L'avoir recoit un numero unique genere automatiquement, distinct de la numerotation des factures (prefixe "AV-" ou "CN-" selon la configuration) |
| 4 | Un avoir total (montant egal au montant de la facture) change le statut de la facture de reference a "Credited" (Avoir emis) |
| 5 | Un avoir partiel (montant inferieur au montant de la facture) cree une note de credit sans changer le statut de la facture de reference, mais ajuste le solde du |
| 6 | L'avoir est lie a la facture de reference ; un lien bidirectionnel est visible (depuis l'avoir vers la facture et depuis la facture vers l'avoir) |
| 7 | L'avoir suit le meme workflow d'approbation que les factures (Draft -> Pending Approval -> Approved -> Committed) |
| 8 | L'emission d'un avoir met a jour les KPIs financiers du projet : le Revenue est decremente du montant de l'avoir |
| 9 | L'avoir est exportable et imprimable au format PDF, avec les mentions legales requises et la reference a la facture d'origine |
| 10 | Le montant de l'avoir ne peut pas exceder le montant total de la facture de reference ; une validation empeche la saisie d'un montant superieur |

---

### US-CF-12 -- Archivage de factures

**En tant que** comptable ou administrateur
**Je veux** archiver les factures cloturees (payees ou creditees) au-dela d'une certaine anciennete
**Afin de** alleger la liste des factures actives tout en conservant un acces a l'historique complet

| # | Critere d'acceptation |
|---|---|
| 1 | Un bouton "Archiver" est visible sur les factures en statut "Paid" ou "Credited" |
| 2 | L'archivage change le statut de la facture de "Paid" ou "Credited" a "Archived" |
| 3 | Les factures archivees ne sont plus affichees dans la liste par defaut des factures actives |
| 4 | Un filtre "Archivees" ou un onglet "Archives" permet d'acceder aux factures archivees |
| 5 | Les factures archivees sont en lecture seule ; aucune action (modification, suppression, changement de statut) n'est possible |
| 6 | Les factures archivees restent accessibles pour consultation, export et impression |
| 7 | Un archivage en masse est possible : selection multiple de factures + bouton "Archiver la selection" |
| 8 | L'archivage est reversible : un bouton "Desarchiver" permet de ramener une facture archivee a son statut precedent ("Paid" ou "Credited") |
| 9 | Les factures archivees sont conservees indefiniment dans le systeme (aucune suppression automatique) |
| 10 | Les KPIs financiers du projet continuent d'inclure les factures archivees dans les calculs (pas d'impact sur les indicateurs) |

---

### US-CF-13 -- Filtrage et recherche de factures

**En tant que** comptable, gestionnaire de projets ou directeur financier
**Je veux** filtrer et rechercher des factures selon des criteres combines (statut, client, projet, periode, montant)
**Afin de** retrouver rapidement une facture specifique ou obtenir une vue filtree de la facturation

| # | Critere d'acceptation |
|---|---|
| 1 | Un panneau de filtres est accessible en haut de la liste des factures, avec les criteres : Status (selection multiple), Customer (liste deroulante avec recherche), Project (liste deroulante avec recherche), Date range (du/au avec date picker), Entite emettrice, Montant (min/max) |
| 2 | Les filtres sont combinables : plusieurs criteres peuvent etre actifs simultanement (logique AND) |
| 3 | La liste des factures se met a jour en temps reel a chaque modification d'un filtre (sans rechargement de page) |
| 4 | Un bouton "Reinitialiser les filtres" efface tous les criteres et affiche la liste complete |
| 5 | Le nombre de resultats correspondant aux filtres actifs est affiche (ex : "42 factures trouvees") |
| 6 | Une barre de recherche textuelle permet de rechercher par numero de facture, nom de client ou nom de projet (recherche partielle) |
| 7 | Les filtres actifs sont affiches sous forme de "tags" cliquables permettant de retirer un critere individuellement |
| 8 | Les combinaisons de filtres frequentes peuvent etre sauvegardees comme "filtres favoris" par l'utilisateur |
| 9 | Le tri de la liste est possible sur chaque colonne (ascendant / descendant) : Invoice #, Project, Customer, Amount, Status, Date |
| 10 | La liste filtree peut etre exportee en CSV pour exploitation dans un tableur |

---

### US-CF-14 -- KPIs financiers au niveau projet (Revenue, Cost, Profit, Margin %)

**En tant que** chef de projet, directeur financier ou associe
**Je veux** consulter les indicateurs financiers cles d'un projet (Revenue, Cost, Profit, Margin %) depuis le module facturation
**Afin de** evaluer la rentabilite du projet et prendre des decisions eclairees sur la suite de la facturation

| # | Critere d'acceptation |
|---|---|
| 1 | Un panneau "KPIs financiers" est visible sur la fiche projet accessible depuis le module facturation, affichant quatre indicateurs : Revenue, Cost, Profit, Margin % |
| 2 | Le **Revenue** (Revenu) est calcule comme la somme des heures facturees multipliees par les taux de facturation (Billing Rate) : Revenue = Somme(heures x Billing Rate) |
| 3 | Le **Cost** (Cout) est calcule comme la somme des heures consommees multipliees par les taux de cout interne de chaque collaborateur : Cost = Somme(heures x Taux cout interne) |
| 4 | Le **Profit** est calcule comme la difference entre le Revenue et le Cost : Profit = Revenue - Cost |
| 5 | Le **Margin %** est calcule comme le ratio du Profit sur le Revenue, exprime en pourcentage : Margin % = (Profit / Revenue) x 100 ; si le Revenue est nul, la marge est affichee comme "N/A" |
| 6 | Les KPIs sont affiches avec un code couleur : vert si la marge est >= au seuil configure (ex : 30%), orange si la marge est entre le seuil bas et le seuil configure (ex : 15-30%), rouge si la marge est < au seuil bas (ex : < 15%) |
| 7 | Les KPIs sont recalcules en temps reel a chaque engagement comptable de facture ou enregistrement de paiement |
| 8 | Un graphique d'evolution des KPIs dans le temps (mois par mois) est disponible pour suivre la tendance de rentabilite du projet |
| 9 | Les KPIs distinguent le Revenue "reconnu" (factures engagees) du Revenue "previsionnel" (heures saisies mais non encore facturees) |
| 10 | Les montants sont affiches en CAD avec le format de nombre canadien (separateur de milliers : espace, separateur decimal : virgule ou point selon la configuration) |

---

### US-CF-15 -- Multi-entites et bureaux de facturation

**En tant que** directeur financier ou administrateur
**Je veux** gerer la facturation par entite juridique (Provencher Roy Prod, PRAA) avec des bureaux de facturation distincts
**Afin de** assurer la conformite comptable et la separation des flux financiers entre les entites du groupe

| # | Critere d'acceptation |
|---|---|
| 1 | Chaque facture est emise par une entite juridique identifiee (Provencher Roy Prod ou PRAA) ; l'entite emettrice est affichee en evidence sur la fiche de la facture |
| 2 | Chaque entite possede son propre bureau de facturation (Billing Office) avec ses coordonnees, son logo et ses mentions legales |
| 3 | La numerotation des factures est independante par entite (chaque entite a sa propre sequence de numerotation) |
| 4 | Le filtre "Entite emettrice" dans la liste des factures permet de visualiser les factures d'une seule entite ou de toutes les entites |
| 5 | Les KPIs financiers (Revenue, Cost, Profit, Margin %) peuvent etre consultes par entite ou en consolide inter-entites |
| 6 | Les templates de facture PDF sont personnalisables par entite (logo, coordonnees, mentions legales, pied de page) |
| 7 | Un utilisateur peut etre autorise a operer sur une ou plusieurs entites ; les droits d'acces sont configures par entite |
| 8 | Le tableau de bord facturation distingue visuellement les donnees par entite (onglets, colonnes ou filtres) |
| 9 | Les rapports financiers (export CSV, PDF) incluent une colonne "Entite emettrice" pour permettre la ventilation comptable |
| 10 | La configuration des entites (nom, adresse, coordonnees bancaires, numero de TVA, logo) est geree dans le module Configuration (EPIC-016) |

---

### US-CF-16 -- Facturation intercompagnie

**En tant que** directeur financier ou comptable
**Je veux** gerer les ecritures de facturation intercompagnie entre les entites du groupe (Provencher Roy Prod, PRAA, Provencher Roy Design Inc.)
**Afin de** tracer les transferts financiers internes et assurer l'equilibre comptable entre les entites

| # | Critere d'acceptation |
|---|---|
| 1 | Un type de facture "Intercompagnie" est disponible en plus du type "Client" ; il est identifie visuellement par un badge ou un code couleur specifique |
| 2 | Les factures intercompagnie sont liees a un projet intercompagnie dedie (ex : Projet 130094 -- Provencher Roy Design Inc. Interco) |
| 3 | L'entite emettrice et l'entite destinataire sont toutes deux des entites internes du groupe ; le champ "Client" est remplace par "Entite destinataire" |
| 4 | Les factures intercompagnie suivent le meme workflow d'approbation que les factures clients (Draft -> Pending Approval -> Approved -> Committed -> Sent -> Paid) |
| 5 | Un rapprochement automatique est propose : lorsqu'une facture intercompagnie est creee par l'entite emettrice, une ecriture miroir (credit) est automatiquement suggeree dans l'entite destinataire |
| 6 | Les factures intercompagnie sont exclues du chiffre d'affaires consolide du groupe pour eviter la double comptabilisation |
| 7 | Un rapport de reconciliation intercompagnie est disponible, affichant les soldes entre entites |
| 8 | Les factures intercompagnie sont filtrees separement dans la liste des factures (filtre "Type : Intercompagnie" ou onglet dedie) |
| 9 | La devise de facturation intercompagnie est la meme que la devise de reference du groupe (CAD) |
| 10 | L'historique des transactions intercompagnie est consultable avec la date, l'entite emettrice, l'entite destinataire, le montant et le statut de rapprochement |

---

### US-CF-17 -- Export et impression de factures

**En tant que** comptable ou gestionnaire administratif
**Je veux** exporter et imprimer des factures dans differents formats (PDF, CSV)
**Afin de** transmettre les factures aux clients, les archiver physiquement ou les integrer dans le systeme comptable

| # | Critere d'acceptation |
|---|---|
| 1 | Un bouton "Exporter en PDF" est accessible depuis la fiche de chaque facture ; le PDF est genere avec le template de l'entite emettrice (logo, coordonnees, mentions legales) |
| 2 | Le PDF de facture comprend : en-tete avec logo et coordonnees de l'entite emettrice, coordonnees du client, numero de facture, date de facturation, periode, tableau des lignes de facture (role, heures, taux, montant), sous-total, taxes le cas echeant, total TTC, conditions de paiement, coordonnees bancaires |
| 3 | Un bouton "Imprimer" ouvre la boite de dialogue d'impression du navigateur avec un apercu de la facture formatee |
| 4 | Un export CSV est disponible depuis la liste des factures (bouton "Exporter en CSV") pour exporter toutes les factures visibles (filtrees) en un seul fichier |
| 5 | Le fichier CSV comprend les colonnes : Invoice #, Date, Project, Customer, Entity, Amount, Status, Payment Date, Payment Status |
| 6 | Un export en masse (PDF) est possible : selection de plusieurs factures + bouton "Exporter la selection en PDF" genere un fichier ZIP contenant un PDF par facture |
| 7 | Le template PDF est personnalisable par entite depuis le module Configuration (EPIC-016) : position du logo, polices, couleurs, mentions legales |
| 8 | Le nom du fichier PDF exporte suit une convention de nommage : "FACTURE_{InvoiceNumber}_{CustomerName}_{Date}.pdf" |
| 9 | Le fichier CSV exporte est encode en UTF-8 avec separateur point-virgule (convention comptable francophone) pour compatibilite avec les logiciels comptables |
| 10 | L'export PDF inclut un pied de page avec le numero de page (ex : "Page 1/2") et la date d'impression |

---

### US-CF-18 -- Tableau de bord facturation

**En tant que** directeur financier, associe ou gestionnaire de projets
**Je veux** acceder a un tableau de bord synthetique de la facturation avec des indicateurs cles et des graphiques
**Afin de** piloter l'activite de facturation, identifier les retards de paiement et suivre l'evolution du chiffre d'affaires

| # | Critere d'acceptation |
|---|---|
| 1 | Un tableau de bord "Facturation" est accessible depuis le module Invoices via un onglet ou un bouton dedie |
| 2 | Les indicateurs cles affiches sont : Chiffre d'affaires de la periode (somme des factures Committed, Sent et Paid), Encours clients (somme des factures Sent non payees), Retards de paiement (somme des factures Sent dont l'echeance est depassee), Taux de recouvrement (% des factures Sent qui sont Paid dans les delais), Nombre de factures par statut (histogramme), Delai moyen de paiement (en jours) |
| 3 | Un graphique en barres affiche l'evolution du chiffre d'affaires mensuel sur les 12 derniers mois |
| 4 | Un graphique camembert affiche la repartition des factures par statut |
| 5 | Un tableau "Top 10 clients" affiche les clients classes par montant total facture, avec le montant paye et le solde du |
| 6 | Un tableau "Factures en retard" liste les factures dont le delai de paiement est depasse, triees par anciennete du retard |
| 7 | Un selecteur de periode permet de filtrer les indicateurs (mois, trimestre, annee, personnalise) |
| 8 | Un filtre par entite permet de visualiser les indicateurs d'une seule entite ou en consolide |
| 9 | Les donnees du tableau de bord sont exportables en PDF (rapport synthetique) ou CSV (donnees brutes) |
| 10 | Le tableau de bord se charge en moins de 3 secondes et les donnees sont rafraichies en temps reel ou a intervalle configurable (toutes les 5 minutes par defaut) |

---

### US-CF-19 -- Liste des factures liees a un contrat

**En tant que** gestionnaire de projets ou directeur financier
**Je veux** visualiser toutes les factures liees a un contrat depuis la fiche du contrat
**Afin de** avoir une vue complete de l'historique de facturation d'un contrat et suivre l'avancement de la facturation par rapport au budget contractuel

| # | Critere d'acceptation |
|---|---|
| 1 | Une sous-section "Factures" est visible dans la fiche detaillee d'un contrat, affichant la liste de toutes les factures liees |
| 2 | La liste affiche les colonnes : Invoice #, Date, Montant, Statut, Date de paiement |
| 3 | Le total facture est affiche en bas de la liste : somme de toutes les factures (hors avoirs) |
| 4 | Le total paye est affiche : somme des paiements recus |
| 5 | Le solde restant a facturer est affiche : montant total du contrat - total facture |
| 6 | Un bouton "Nouvelle facture" est accessible directement depuis cette sous-section, pre-remplissant le contrat dans le formulaire de creation |
| 7 | Chaque ligne de facture est cliquable et ouvre la fiche detaillee de la facture |
| 8 | Les factures sont triees par defaut par date decroissante (la plus recente en premier) |
| 9 | Un indicateur de progression visuel (barre de progression) affiche le pourcentage du montant contractuel deja facture |
| 10 | Les avoirs (Credit Notes) sont affiches dans la meme liste avec une distinction visuelle (couleur rouge, prefixe "AV-") |

---

### US-CF-20 -- Gestion des transitions de statut de facture

**En tant que** comptable, gestionnaire ou directeur financier
**Je veux** que les transitions de statut de facture respectent un enchainement precis et controle
**Afin de** garantir l'integrite du processus de facturation et eviter les etats incoherents

| # | Critere d'acceptation |
|---|---|
| 1 | Les transitions de statut autorisees sont strictement definies : Draft -> Pending Approval, Pending Approval -> Approved (ou Pending Second Approval si double approbation), Pending Approval -> Draft (rejet), Pending Second Approval -> Approved, Pending Second Approval -> Draft (rejet), Approved -> Committed, Committed -> Sent, Sent -> Paid, Sent -> Partially Paid, Partially Paid -> Paid, Paid -> Credited, Sent -> Credited, Committed -> Credited, Paid -> Archived, Credited -> Archived |
| 2 | Toute tentative de transition non autorisee est bloquee avec un message d'erreur explicite (ex : "Impossible de passer une facture de Draft a Committed sans approbation") |
| 3 | Chaque transition est tracee dans l'historique de la facture avec : statut precedent, statut suivant, date et heure, utilisateur, commentaire optionnel |
| 4 | Les boutons d'action visibles sur une facture sont dynamiques et n'affichent que les actions correspondant aux transitions autorisees depuis le statut actuel |
| 5 | Un diagramme de flux des statuts est disponible dans l'aide en ligne pour guider les utilisateurs |
| 6 | Les transitions de statut declenchent les notifications appropriees (email et/ou in-app) aux utilisateurs concernes |
| 7 | Un retour en arriere exceptionnel (ex : de "Committed" a "Approved") n'est possible que par un administrateur avec une justification obligatoire tracee |
| 8 | Chaque statut est associe a un code couleur visible dans la liste des factures et sur la fiche de la facture pour une identification rapide |
| 9 | Les roles utilisateur requis pour chaque transition sont configures : par exemple, seul un "Approbateur" peut effectuer la transition Pending Approval -> Approved |
| 10 | Les transitions en masse (selection de plusieurs factures + action groupee) sont possibles pour les transitions simples (ex : archivage en masse) mais interdites pour les transitions sensibles (approbation, engagement) |

---

### US-CF-21 -- Historique et audit trail des factures

**En tant que** auditeur, directeur financier ou administrateur
**Je veux** consulter l'historique complet de toutes les actions effectuees sur une facture
**Afin de** disposer d'une piste d'audit (audit trail) conforme aux exigences reglementaires et de traçabilite comptable

| # | Critere d'acceptation |
|---|---|
| 1 | Un onglet ou une section "Historique" est visible sur la fiche detaillee de chaque facture |
| 2 | L'historique affiche chronologiquement toutes les actions : creation, modification de lignes, modification de montant, soumission, approbation, rejet, engagement, envoi, paiement, emission d'avoir, archivage |
| 3 | Chaque entree de l'historique comprend : date et heure, utilisateur ayant effectue l'action, type d'action, detail de la modification (ancienne valeur -> nouvelle valeur pour les modifications), commentaire eventuel |
| 4 | L'historique est en lecture seule : il est impossible de modifier ou supprimer une entree de l'historique |
| 5 | L'historique est exportable en PDF pour les besoins d'audit externe |
| 6 | Les modifications de montant sont tracees avec le detail : ancienne valeur, nouvelle valeur, ecart, motif |
| 7 | Les actions d'approbation et de rejet sont clairement identifiees avec le nom de l'approbateur et le motif le cas echeant |
| 8 | L'historique est filtre par type d'action pour retrouver rapidement une information specifique |
| 9 | La date et l'heure sont affichees en fuseau horaire local (EST/EDT pour Montreal) |
| 10 | L'historique des factures est conserve indefiniment, meme apres archivage de la facture |

---

## 6. Hors Perimetre

Les elements suivants sont explicitement exclus du perimetre de cet EPIC :

- **Gestion des projets et des taches** : la creation, modification et suppression des projets et taches sont couvertes par EPIC-002 (Projets). Le module Facturation consomme ces donnees en lecture.
- **Saisie des heures** : la saisie et l'approbation des feuilles de temps sont couvertes par EPIC-005 (Temps). Le module Facturation consomme les heures approuvees pour generer les lignes de facture.
- **Gestion des honoraires et du budget previsionnel** : la definition des honoraires par phase de projet est couverte par EPIC-003 (Honoraires). Le module Facturation consomme ces donnees pour le suivi budgetaire.
- **Comptabilite generale** : la tenue des livres comptables, le grand livre, les ecritures de journal et les etats financiers complets sont couverts par EPIC-008 (Finances) ou par un logiciel comptable externe.
- **Gestion avancee des devis et propositions commerciales** : le module Facturation couvre les contrats et factures, pas les devis en amont (couverts par EPIC-001 Opportunites).
- **Relance automatique des impays** : les relances par email sont mentionnees comme alertes, mais un module de relance automatique complet (avec escalade et mise en demeure) n'est pas dans le perimetre.
- **Module de paiement en ligne** : l'integration avec des passerelles de paiement en ligne (Stripe, PayPal, etc.) n'est pas dans le perimetre. Seul l'enregistrement manuel des paiements est couvert.
- **Gestion de la TVA multi-taux** : la gestion de la TVA est mentionnee dans les exports PDF mais une gestion multi-taux complexe (TVA intracommunautaire, reverse charge) n'est pas dans le perimetre.
- **Application mobile native** : le responsive design (tablette) est couvert, mais une application mobile native n'est pas dans le perimetre.
- **Import/export de donnees depuis ChangePoint** : la migration des donnees historiques depuis ChangePoint n'est pas couverte par cet EPIC (un EPIC de migration separe sera necessaire).

---

## 7. Regles Metier

| Ref | Regle |
|---|---|
| **RM-CF-01** | Un contrat est **obligatoire** pour emettre une facture sur un projet client. Aucune facture ne peut etre creee sans contrat associe. Les projets administratifs et departementaux ne necessitent pas de contrat. |
| **RM-CF-02** | Le **numero de facture** est genere automatiquement selon une sequence chronologique continue par entite. La numerotation ne doit presenter aucun trou (conformite comptable). Le format de numerotation est configurable par entite (ex : "PRO-2026-001", "PRAA-2026-001"). |
| **RM-CF-03** | Le **Billing Rate** (taux effectif de facturation) est calcule selon la formule : `Billing Rate = Standard Rate x (1 - Discount% / 100)`. Le resultat est arrondi a deux decimales (arrondi au centime le plus proche). |
| **RM-CF-04** | Une facture ne peut progresser dans le workflow que selon les **transitions de statut autorisees**. Les transitions sont : Draft -> Pending Approval -> [Pending Second Approval ->] Approved -> Committed -> Sent -> Paid/Partially Paid -> Archived. Le rejet ramene au statut Draft. L'emission d'un avoir est possible depuis Committed, Sent, Paid ou Partially Paid. |
| **RM-CF-05** | Une facture en statut **"Committed" ou superieur** (Sent, Paid, Partially Paid) est definitivement verrouillee en edition. Seule l'emission d'un avoir permet de corriger ou d'annuler une facture engagee. |
| **RM-CF-06** | Le **Revenue** (revenu) d'un projet est calcule comme la somme des heures facturees multipliees par le Billing Rate applicable : `Revenue = Somme(heures x Billing Rate)`. Le Revenue est mis a jour a chaque engagement comptable de facture. |
| **RM-CF-07** | Le **Cost** (cout) d'un projet est calcule comme la somme des heures consommees multipliees par le taux de cout interne du collaborateur : `Cost = Somme(heures x Taux cout interne)`. Le taux de cout interne est defini dans le module Collaborateurs (EPIC-009). |
| **RM-CF-08** | Le **Profit** est calcule comme la difference entre le Revenue et le Cost : `Profit = Revenue - Cost`. Un Profit negatif indique une perte sur le projet. |
| **RM-CF-09** | Le **Margin %** est calcule comme : `Margin % = (Profit / Revenue) x 100`. Si le Revenue est egal a zero, la marge est affichee comme "N/A" pour eviter la division par zero. |
| **RM-CF-10** | La **devise de facturation** par defaut est le CAD (Dollar canadien). Chaque contrat peut specifier une devise de facturation differente, mais la devise de reference pour les KPIs est toujours le CAD. |
| **RM-CF-11** | La **double approbation** est declenchee selon les regles configurees par l'administrateur : seuil de montant (ex : > 50 000 CAD), type de projet, ou entite emettrice. En l'absence de regle specifique, l'approbation simple s'applique. |
| **RM-CF-12** | Un **avoir** (Credit Note) ne peut pas exceder le montant de la facture de reference. Le montant de l'avoir est soustrait du Revenue du projet au moment de l'engagement comptable de l'avoir. |
| **RM-CF-13** | Les **paiements partiels** sont enregistres individuellement. Le solde restant du est calcule automatiquement : `Solde = Montant facture - Somme(paiements recus) - Somme(avoirs)`. Lorsque le solde atteint 0 (a une tolerance de 0.01 CAD), le statut passe automatiquement a "Paid". |
| **RM-CF-14** | Les **factures intercompagnie** sont identifiees par le type "Intercompagnie" et liees a un projet intercompagnie dedie. Elles sont exclues du chiffre d'affaires consolide du groupe pour eviter la double comptabilisation. |
| **RM-CF-15** | Chaque entite (Provencher Roy Prod, PRAA) possede sa propre **sequence de numerotation** de factures, son propre bureau de facturation (Billing Office) et son propre template de facture PDF. |
| **RM-CF-16** | Un **role de facturation** (Billing Role) ne peut apparaitre qu'une seule fois par contrat. Si un meme role intervient avec des taux differents selon la periode, une nouvelle version du contrat ou un avenant doit etre cree. |
| **RM-CF-17** | Les **modifications de taux** (Standard Rate, Discount %, Billing Rate) dans un contrat ne sont pas retroactives : elles s'appliquent uniquement aux factures creees apres la date de modification. Les factures deja emises conservent les taux en vigueur au moment de leur creation. |
| **RM-CF-18** | Le **delai de paiement** est calcule a partir de la date d'envoi de la facture. Le nombre de jours est defini dans les conditions de paiement du contrat (ex : 30 jours net, 45 jours net, 60 jours net). Un depassement du delai declenche une alerte automatique. |
| **RM-CF-19** | Un utilisateur ne peut approuver une facture que s'il possede le **role d'approbateur** configure pour l'entite ou le projet concerne. Un utilisateur ne peut pas approuver une facture qu'il a lui-meme creee (separation des roles emetteur/approbateur). |
| **RM-CF-20** | Les **projets departementaux PRAA** (non facturables) ne peuvent pas avoir de contrat associe et ne peuvent pas generer de factures. Les couts sont suivis mais aucun Revenue n'est enregistre. |
| **RM-CF-21** | L'**archivage** d'une facture n'a aucun impact sur les KPIs financiers du projet ni sur les calculs comptables. Les factures archivees sont incluses dans tous les calculs de Revenue, Profit et Margin %. |
| **RM-CF-22** | Les **montants** sont affiches et stockes avec une precision de deux decimales (centimes). Les calculs intermediaires sont effectues avec une precision superieure (4 decimales minimum) et le resultat final est arrondi au centime le plus proche. |

---

## 8. Contraintes Techniques

| # | Contrainte |
|---|---|
| 1 | **Performance** : la liste des factures doit se charger en moins de 2 secondes pour un volume de 10 000 factures avec filtres appliques. La generation d'un PDF de facture doit prendre moins de 3 secondes. |
| 2 | **Scalabilite** : le systeme doit supporter un volume de 5 000 contrats actifs et 50 000 factures (tous statuts confondus) sans degradation de performance. |
| 3 | **Integrite transactionnelle** : les operations de changement de statut et d'enregistrement de paiement doivent etre atomiques (transactions ACID). En cas d'echec, aucune donnee ne doit etre partiellement modifiee. |
| 4 | **Concurrence** : le systeme doit gerer les acces concurrents sur une meme facture (verrouillage optimiste ou pessimiste) pour eviter les modifications simultanees conflictuelles. |
| 5 | **Securite** : les acces aux factures sont controles par role (RBAC). Les roles minimaux sont : Emetteur (creation, modification Draft), Approbateur (approbation/rejet), Comptable (engagement, paiement), Administrateur (toutes actions). |
| 6 | **Audit** : toutes les actions sur les factures sont tracees dans un journal d'audit immutable. Le journal est consultable par les administrateurs et exportable pour les audits externes. |
| 7 | **Export PDF** : le moteur de generation PDF doit supporter les caracteres accentues (UTF-8), les logos en haute resolution (300 DPI minimum), et les tableaux multiligne. |
| 8 | **API REST** : le module Facturation expose des API REST pour permettre l'integration avec des systemes comptables externes (GET, POST, PUT sur les factures, contrats, paiements). |
| 9 | **Sauvegarde** : les donnees de facturation sont sauvegardees quotidiennement avec une retention de 7 ans minimum (conformite comptable). |
| 10 | **Responsive** : l'interface est utilisable sur tablette (largeur minimale 768px). L'edition de factures complexes (nombreuses lignes) reste ergonomique sur ecran reduit. |
| 11 | **Multi-navigateurs** : le module est compatible avec les navigateurs Chrome (2 dernieres versions), Firefox (2 dernieres versions), Safari (2 dernieres versions) et Edge (2 dernieres versions). |
| 12 | **Disponibilite** : le module doit etre disponible 99.5% du temps (hors fenetres de maintenance planifiees). |

---

## 9. Dependances

### Dependances fonctionnelles

| Type | EPIC / Module | Description |
|---|---|---|
| **Depend de** | EPIC-002 (Projets) | Les projets associes aux contrats et factures proviennent du module Projets. Le type de projet (client, administratif, departemental) determine la possibilite de facturer. |
| **Depend de** | EPIC-003 (Honoraires) | Le budget previsionnel et les phases de projet alimentent le calcul du solde restant a facturer. |
| **Depend de** | EPIC-005 (Temps) | Les heures approuvees alimentent les lignes de facture pour la facturation au temps passe. |
| **Depend de** | EPIC-009 (Collaborateurs) | Les taux de cout interne des collaborateurs sont necessaires pour le calcul du Cost et de la marge. Les roles de facturation (Billing Roles) correspondent aux roles des collaborateurs. |
| **Depend de** | EPIC-010 (Clients) | Les informations client (nom, adresse, contact facturation, conditions de paiement) sont consommees par le module Facturation. |
| **Depend de** | EPIC-016 (Configuration) | La configuration des entites, des bureaux de facturation, des sequences de numerotation, des templates PDF et des seuils de double approbation est geree dans le module Configuration. |
| **Requis par** | EPIC-008 (Finances) | Les factures engagees alimentent les ecritures comptables et les etats financiers. |
| **Requis par** | EPIC-011 (Rapports) | Les donnees de facturation alimentent les rapports transversaux (chiffre d'affaires, encours, recouvrement). |
| **Requis par** | EPIC-012 (Validation) | Le workflow d'approbation des factures s'appuie sur le module de validation pour la gestion des approbateurs et des niveaux d'approbation. |
| **Requis par** | EPIC-014 (Tableau de bord) | Les indicateurs de facturation (CA, encours, retards) alimentent le tableau de bord global. |
| **Requis par** | EPIC-017 (Notifications) | Les notifications de soumission, d'approbation, de rejet, d'envoi et d'alerte d'echeance sont envoyees via le module Notifications. |

### Dependances techniques

| Composant | Description |
|---|---|
| **API Projets** | Lecture des projets, types de projets et phases (GET) |
| **API Collaborateurs** | Lecture des collaborateurs, roles et taux de cout interne (GET) |
| **API Clients** | Lecture des clients, contacts, conditions de paiement (GET) |
| **API Temps** | Lecture des heures approuvees par periode et par collaborateur (GET) |
| **API Honoraires** | Lecture du budget previsionnel et de l'avancement de facturation (GET) |
| **API Configuration** | Lecture des entites, bureaux de facturation, sequences de numerotation, templates PDF, seuils de double approbation (GET) |
| **API Facturation** | CRUD complet : creation, lecture, mise a jour des contrats, factures, lignes de facture, paiements, avoirs |
| **API Approbation** | Soumission, approbation, rejet des factures ; gestion des niveaux d'approbation |
| **API Notifications** | Envoi de notifications email et in-app pour chaque transition de statut |
| **Service PDF** | Generation de factures au format PDF avec templates personnalisables par entite |
| **Service Export** | Generation de fichiers CSV pour export comptable |

---

## 10. Criteres d'Acceptation Globaux

| # | Critere |
|---|---|
| 1 | Toutes les User Stories US-CF-01 a US-CF-21 sont developpees, testees et validees par le Product Owner. |
| 2 | Les 10 statuts de facture de ChangePoint (Draft, Pending Approval, Pending Second Approval, Approved, Committed, Sent, Paid, Partially Paid, Credited, Archived) sont implementes avec les transitions autorisees. |
| 3 | Le workflow d'approbation simple (un niveau) et double (deux niveaux) est fonctionnel et configurable. |
| 4 | Les Billing Roles & Rates sont configurables par contrat avec le calcul automatique du Billing Rate. |
| 5 | Les KPIs financiers (Revenue, Cost, Profit, Margin %) sont calcules correctement et mis a jour en temps reel. |
| 6 | La gestion multi-entites est operationnelle : factures emises par entite, numerotation independante, bureaux de facturation distincts. |
| 7 | La facturation intercompagnie est implementee avec un type de facture distinct et l'exclusion du CA consolide. |
| 8 | L'export PDF de facture est fonctionnel avec le template personnalise par entite (logo, mentions legales, coordonnees). |
| 9 | L'export CSV de la liste des factures est fonctionnel et compatible avec les logiciels comptables. |
| 10 | Le tableau de bord facturation affiche les indicateurs cles (CA, encours, retards, recouvrement) avec des graphiques interactifs. |
| 11 | Le filtrage et la recherche de factures sont fonctionnels avec tous les criteres (Status, Customer, Project, Date, Entite, Montant) et la sauvegarde de filtres favoris. |
| 12 | L'historique complet des actions (audit trail) est consultable et exportable pour chaque facture. |
| 13 | Les performances sont acceptables : chargement de la liste < 2 secondes, generation PDF < 3 secondes. |
| 14 | Les notifications sont envoyees correctement a chaque transition de statut (email et/ou in-app). |
| 15 | L'interface est responsive et utilisable sur tablette (largeur minimale 768px). |

---

## 11. Metriques de Succes

| # | Metrique | Objectif | Methode de mesure |
|---|---|---|---|
| 1 | **Parite fonctionnelle** | 100% des fonctionnalites de ChangePoint reproduites | Checklist de validation fonctionnelle |
| 2 | **Temps de creation d'une facture** | < 3 minutes (de la selection du contrat a la sauvegarde du Draft) | Mesure UX sur un echantillon de 10 utilisateurs |
| 3 | **Delai moyen du workflow d'approbation** | < 24 heures (de la soumission a l'approbation) | Moyenne calculee sur 3 mois d'utilisation |
| 4 | **Taux de rejet des factures** | < 10% (indicateur de qualite des factures emises) | Ratio factures rejetees / factures soumises |
| 5 | **Precision des KPIs** | 100% de coherence entre les KPIs du module et les donnees comptables | Reconciliation trimestrielle avec le systeme comptable |
| 6 | **Adoption du tableau de bord** | > 80% des directeurs et gestionnaires consultent le tableau de bord au moins une fois par semaine | Analytics d'utilisation |
| 7 | **Reduction du delai de facturation** | -30% par rapport au processus actuel dans ChangePoint | Comparaison du delai moyen entre fin de periode et emission de la facture |
| 8 | **Satisfaction utilisateur** | Score de satisfaction >= 4/5 | Sondage NPS apres 3 mois d'utilisation |
| 9 | **Volume de facturation gere** | >= 500 factures par an par entite sans degradation de performance | Monitoring de la charge et des temps de reponse |
| 10 | **Taux de recouvrement** | >= 95% des factures payees dans les delais contractuels | Suivi automatique dans le tableau de bord |

---

## 12. Annexes

### Annexe A -- Diagramme de flux des statuts de facture

```
                                    +------------------+
                                    |                  |
                                    |      DRAFT       |
                                    |   (Brouillon)    |
                                    |                  |
                                    +--------+---------+
                                             |
                                    Soumettre pour approbation
                                             |
                                             v
                                    +------------------+
                                    |                  |
                           +------->  PENDING APPROVAL |
                           |        |(En attente appr.)|
                           |        |                  |
                           |        +----+--------+----+
                           |             |        |
                           |       Approuver   Rejeter
                           |             |        |
                           |             |        +---------> Retour a DRAFT
                           |             |                    (avec motif)
                           |             v
                           |    [Double approbation ?]
                           |        /          \
                           |      NON          OUI
                           |       |            |
                           |       |            v
                           |       |   +------------------+
                           |       |   | PENDING SECOND   |
                           |       |   |    APPROVAL      |
                           |       |   |(2e approbation)  |
                           |       |   +----+--------+----+
                           |       |        |        |
                           |       |  Approuver   Rejeter
                           |       |        |        |
                           |       |        |        +-----> Retour a DRAFT
                           |       |        |                (avec motif)
                           |       |        |
                           |       v        v
                           |    +------------------+
                           |    |                  |
                           |    |     APPROVED     |
                           |    |   (Approuvee)    |
                           |    |                  |
                           |    +--------+---------+
                           |             |
                           |        Engager (Commit)
                           |             |
                           |             v
                           |    +------------------+
                           |    |                  |
                           |    |    COMMITTED     |<----+
                           |    |    (Engagee)     |     |
                           |    |                  |     |
                           |    +--------+---------+     |
                           |             |               |
                           |     Envoyer au client       |
                           |             |               |
                           |             v               |
                           |    +------------------+     |
                           |    |                  |     |
                           |    |      SENT        |     |
                           |    |   (Envoyee)      |     |
                           |    |                  |     |
                           |    +---+-----+---+----+     |
                           |        |     |   |          |
                           |  Paiement  Paiement  Avoir  |
                           |  complet   partiel          |
                           |        |     |   |          |
                           |        v     |   +---+      |
                           |  +----------+|       |      |
                           |  |          ||       v      |
                           |  |   PAID   ||  +---------+ |
                           |  | (Payee)  ||  |CREDITED | |
                           |  |          ||  | (Avoir) | |
                           |  +----+-----+|  +----+----+ |
                           |       |      |       |      |
                           |       |      v       |      |
                           |       | +----------+ |      |
                           |       | |PARTIALLY | |      |
                           |       | |  PAID    | |      |
                           |       | |(Partiel) | |      |
                           |       | +----+-----+ |      |
                           |       |      |       |      |
                           |       |   Paiement   |      |
                           |       |   restant    |      |
                           |       |      |       |      |
                           |       |      v       |      |
                           |       |   -> PAID    |      |
                           |       |              |      |
                           |       v              v      |
                           |    +------------------+     |
                           |    |                  |     |
                           |    |    ARCHIVED      |     |
                           |    |   (Archivee)     |     |
                           |    |                  |     |
                           |    +------------------+     |
                           |                             |
                           +---- Retour exceptionnel ----+
                                 (admin uniquement)
```

### Annexe B -- Modele de Donnees

#### Objet : Contract (Contrat)

| Champ | Type | Description |
|---|---|---|
| `id` | UUID | Identifiant unique du contrat |
| `contract_number` | String | Numero de contrat genere automatiquement |
| `name` | String | Nom du contrat (obligatoire) |
| `project_id` | FK -> Project | Projet associe (obligatoire) |
| `client_id` | FK -> Client | Client associe (obligatoire) |
| `entity_id` | FK -> Entity | Entite emettrice (Provencher Roy Prod, PRAA) |
| `billing_office_id` | FK -> BillingOffice | Bureau de facturation |
| `billing_currency` | String | Devise de facturation (defaut : CAD) |
| `start_date` | Date | Date de debut du contrat |
| `end_date` | Date | Date de fin previsionnelle du contrat |
| `total_amount` | Decimal(12,2) | Montant total contractuel (optionnel) |
| `payment_terms` | String | Conditions de paiement (ex : "30 jours net") |
| `payment_terms_days` | Integer | Nombre de jours de delai de paiement |
| `status` | Enum | Statut : `draft`, `active`, `completed`, `cancelled` |
| `double_approval_required` | Boolean | Double approbation requise pour les factures de ce contrat |
| `notes` | Text | Notes et commentaires internes |
| `created_by` | FK -> User | Utilisateur ayant cree le contrat |
| `created_at` | DateTime | Date de creation |
| `updated_at` | DateTime | Date de derniere modification |

#### Objet : BillingRole (Role de facturation)

| Champ | Type | Description |
|---|---|---|
| `id` | UUID | Identifiant unique |
| `contract_id` | FK -> Contract | Contrat associe |
| `role_name` | String | Nom du role (Architecte, Designer, Technicien, etc.) |
| `standard_rate` | Decimal(10,2) | Taux horaire standard (CAD) |
| `discount_percent` | Decimal(5,2) | Pourcentage de remise (0 a 100) |
| `billing_rate` | Decimal(10,2) | Taux effectif = Standard Rate x (1 - Discount% / 100) |
| `billing_currency` | String | Devise de facturation |
| `effective_from` | Date | Date d'entree en vigueur du taux |
| `created_at` | DateTime | Date de creation |
| `updated_at` | DateTime | Date de derniere modification |

#### Objet : Invoice (Facture)

| Champ | Type | Description |
|---|---|---|
| `id` | UUID | Identifiant unique de la facture |
| `invoice_number` | String | Numero de facture genere automatiquement (unique par entite) |
| `contract_id` | FK -> Contract | Contrat associe (obligatoire) |
| `project_id` | FK -> Project | Projet associe |
| `client_id` | FK -> Client | Client associe |
| `entity_id` | FK -> Entity | Entite emettrice |
| `billing_office_id` | FK -> BillingOffice | Bureau de facturation |
| `invoice_type` | Enum | Type : `client`, `intercompany`, `credit_note` |
| `status` | Enum | Statut : `draft`, `pending_approval`, `pending_second_approval`, `approved`, `committed`, `sent`, `paid`, `partially_paid`, `credited`, `archived` |
| `invoice_date` | Date | Date de facturation |
| `period_start` | Date | Debut de la periode facturee |
| `period_end` | Date | Fin de la periode facturee |
| `description` | Text | Objet de la facture |
| `subtotal` | Decimal(12,2) | Sous-total (somme des lignes) |
| `tax_amount` | Decimal(10,2) | Montant des taxes (le cas echeant) |
| `total_amount` | Decimal(12,2) | Montant total TTC |
| `amount_paid` | Decimal(12,2) | Montant total recu (somme des paiements) |
| `amount_due` | Decimal(12,2) | Solde restant du (total - paye - avoirs) |
| `billing_currency` | String | Devise de facturation |
| `payment_due_date` | Date | Date d'echeance de paiement |
| `sent_at` | DateTime (nullable) | Date d'envoi au client |
| `committed_at` | DateTime (nullable) | Date d'engagement comptable |
| `committed_by` | FK -> User (nullable) | Utilisateur ayant engage la facture |
| `accounting_reference` | String (nullable) | Reference comptable externe |
| `credit_note_for` | FK -> Invoice (nullable) | Facture de reference (pour les avoirs) |
| `created_by` | FK -> User | Utilisateur ayant cree la facture |
| `created_at` | DateTime | Date de creation |
| `updated_at` | DateTime | Date de derniere modification |

#### Objet : InvoiceLine (Ligne de facture)

| Champ | Type | Description |
|---|---|---|
| `id` | UUID | Identifiant unique de la ligne |
| `invoice_id` | FK -> Invoice | Facture parente |
| `billing_role_id` | FK -> BillingRole | Role de facturation |
| `description` | String | Description de la ligne |
| `quantity` | Decimal(8,2) | Nombre d'heures |
| `unit_price` | Decimal(10,2) | Taux horaire (Billing Rate) |
| `amount` | Decimal(12,2) | Montant de la ligne (quantity x unit_price) |
| `sort_order` | Integer | Ordre d'affichage |
| `created_at` | DateTime | Date de creation |
| `updated_at` | DateTime | Date de derniere modification |

#### Objet : Payment (Paiement)

| Champ | Type | Description |
|---|---|---|
| `id` | UUID | Identifiant unique du paiement |
| `invoice_id` | FK -> Invoice | Facture associee |
| `amount` | Decimal(12,2) | Montant recu |
| `payment_date` | Date | Date de reception du paiement |
| `payment_method` | Enum | Mode : `wire_transfer`, `check`, `card`, `other` |
| `reference` | String (nullable) | Reference de paiement (numero de cheque, reference virement) |
| `notes` | Text (nullable) | Notes sur le paiement |
| `recorded_by` | FK -> User | Utilisateur ayant enregistre le paiement |
| `created_at` | DateTime | Date de creation |

#### Objet : InvoiceApproval (Historique d'approbation)

| Champ | Type | Description |
|---|---|---|
| `id` | UUID | Identifiant unique |
| `invoice_id` | FK -> Invoice | Facture concernee |
| `approval_level` | Integer | Niveau d'approbation (1 ou 2) |
| `action` | Enum | Action : `submitted`, `approved`, `rejected`, `recalled` |
| `performed_by` | FK -> User | Utilisateur ayant effectue l'action |
| `comment` | Text (nullable) | Commentaire (obligatoire pour un rejet) |
| `performed_at` | DateTime | Date et heure de l'action |

#### Objet : InvoiceAuditLog (Journal d'audit)

| Champ | Type | Description |
|---|---|---|
| `id` | UUID | Identifiant unique |
| `invoice_id` | FK -> Invoice | Facture concernee |
| `action_type` | String | Type d'action (creation, modification, transition_statut, paiement, avoir, envoi, archivage) |
| `field_changed` | String (nullable) | Champ modifie (pour les modifications) |
| `old_value` | Text (nullable) | Ancienne valeur |
| `new_value` | Text (nullable) | Nouvelle valeur |
| `performed_by` | FK -> User | Utilisateur ayant effectue l'action |
| `performed_at` | DateTime | Date et heure de l'action |
| `comment` | Text (nullable) | Commentaire ou motif |

### Annexe C -- Estimation et Decoupage

#### Sprints suggeres

| Sprint | User Stories | Perimetre | Duree estimee |
|---|---|---|---|
| **Sprint 1** | US-CF-01, US-CF-02, US-CF-03 | Creation de contrats + Billing Roles & Rates + Gestion des taux (fondations) | 2 semaines |
| **Sprint 2** | US-CF-04, US-CF-19 | Creation de factures Draft + Liste des factures liees a un contrat | 2 semaines |
| **Sprint 3** | US-CF-05, US-CF-06, US-CF-20 | Workflow d'approbation simple + double + Gestion des transitions de statut | 2.5 semaines |
| **Sprint 4** | US-CF-07, US-CF-08 | Engagement comptable + Envoi de facture au client | 1.5 semaine |
| **Sprint 5** | US-CF-09, US-CF-10 | Reception de paiement + Paiements partiels | 2 semaines |
| **Sprint 6** | US-CF-11, US-CF-12 | Emission d'avoir + Archivage | 2 semaines |
| **Sprint 7** | US-CF-13, US-CF-14 | Filtrage et recherche + KPIs financiers | 2 semaines |
| **Sprint 8** | US-CF-15, US-CF-16 | Multi-entites et bureaux de facturation + Intercompagnie | 2.5 semaines |
| **Sprint 9** | US-CF-17, US-CF-18 | Export/impression + Tableau de bord facturation | 2 semaines |
| **Sprint 10** | US-CF-21 | Historique et audit trail + Integration finale + Tests de bout en bout | 2 semaines |

#### Estimation globale

| Indicateur | Valeur |
|---|---|
| **Nombre de User Stories** | 21 |
| **Nombre de criteres d'acceptation** | 211 |
| **Nombre de regles metier** | 22 |
| **Nombre de sprints** | 10 |
| **Duree totale estimee** | 20 a 22 semaines |
| **Complexite** | Elevee (workflow multi-niveaux, multi-entites, KPIs financiers, intercompagnie, audit trail) |
| **Risques principaux** | Complexite du workflow d'approbation multi-niveaux, coherence des KPIs avec le systeme comptable, performance avec un grand volume de factures, generation PDF personnalisable |

#### Prerequisites avant demarrage

- API Projets et types de projets disponible en lecture (EPIC-002)
- API Collaborateurs et taux de cout interne disponible en lecture (EPIC-009)
- API Clients et contacts de facturation disponible en lecture (EPIC-010)
- API Temps (heures approuvees) disponible en lecture (EPIC-005)
- Module de configuration des entites et bureaux de facturation operationnel (EPIC-016)
- Charte graphique et composants UI valides (systeme de design : grilles editables, diagrammes, graphiques, modales, notifications)
- Maquettes UX validees pour la liste des factures, la fiche facture, le formulaire de creation, le tableau de bord, l'export PDF
- Infrastructure de notifications email et in-app operationnelle (EPIC-017)
- Moteur de generation PDF operationnel avec support des templates personnalisables

#### Priorite de livraison recommandee

1. **MVP (Sprints 1-4)** : Contrats, Billing Roles & Rates, creation de factures, workflow d'approbation et engagement. Couvre le flux principal de facturation.
2. **V1 Complete (Sprints 5-6)** : Paiements, paiements partiels, avoirs et archivage. Cycle de vie complet de la facture operationnel.
3. **V1.1 Recherche et KPIs (Sprint 7)** : Filtrage avance et KPIs financiers. Exploitation des donnees de facturation.
4. **V1.2 Multi-entites (Sprint 8)** : Multi-entites, bureaux de facturation et intercompagnie. Parite fonctionnelle avec ChangePoint atteinte.
5. **V1.3 Export et Dashboard (Sprint 9)** : Export PDF/CSV et tableau de bord. Valeur ajoutee par rapport a ChangePoint.
6. **V1.4 Audit (Sprint 10)** : Audit trail complet. Conformite reglementaire assuree.

---

## ADDENDUM -- Fonctionnalites supplementaires identifiees lors de l'audit du contrat Place des Arts

**Source** : Audit approfondi du contrat 200236 Place des Arts - 5eme Salle [PRA] (882,350 CAD)
**Date d'ajout** : 27 fevrier 2026
**Raison** : Fonctionnalites critiques non couvertes dans l'EPIC initial

---

### Contexte de l'addendum

L'EPIC Facturation initial couvre 21 User Stories (US-CF-01 a US-CF-21) et 22 regles metier (RM-CF-01 a RM-CF-22). Suite a l'analyse approfondie du contrat **Place des Arts - 5eme Salle** (contrat 200236, 882,350 CAD), des fonctionnalites critiques ont ete identifiees comme manquantes. Ce contrat constitue un cas d'usage representatif de la complexite reelle de la facturation chez Provencher Roy :

- **Billing type** : Mixed - Fixed Fee/Hourly (combinaison de forfaits et de facturation horaire)
- **Montant contractuel** : 882,350 CAD | **Facture** : 1,110,469 CAD | **Paye** : 1,074,651 CAD
- **5 roles de facturation** : Architecte intermediaire (77.00$/h), Architecte junior (63.40$/h), Architecte patron (150.85$/h), Architecte patron override Melissa Belanger (Standard 0.00 -> Billing 150.85$/h), Architecte senior (92.10$/h)
- **Fixed fees/jalons** : 1/28/2023 = 22,573.39 | 9/30/2023 = 865.00 | 9/30/2023 = 8,650.00 | 1/1/2024 = 64,706.00 | 1/1/2024 = 17,500.00
- **Sections specifiques** : Revenue recognition, Vendors, Contract limits, Line of Business

Les 7 User Stories suivantes (US-CF-22 a US-CF-28) et les 8 regles metier additionnelles (RM-CF-23 a RM-CF-30) couvrent ces fonctionnalites manquantes.

---

### US-CF-22 -- Facturation hybride (Mixed - Fixed Fee/Hourly)

**En tant que** gestionnaire de projets ou directeur financier
**Je veux** configurer le type de facturation d'un contrat parmi les modes Fixed Fee, Hourly (Time & Materials) ou Mixed (Fixed Fee/Hourly)
**Afin de** supporter les contrats qui combinent une partie forfaitaire (jalons) et une partie horaire (temps passe), comme le contrat Place des Arts - 5eme Salle

| # | Critere d'acceptation |
|---|---|
| 1 | Un champ "Billing Type" est disponible sur le formulaire de creation et de modification d'un contrat, avec les options : **Fixed Fee** (forfait uniquement), **Hourly / Time & Materials** (temps passe uniquement), **Mixed - Fixed Fee/Hourly** (combinaison des deux modes) |
| 2 | Lorsque le Billing Type est "Fixed Fee", seul le sous-onglet "Fixed Fees" est actif dans le contrat ; le sous-onglet "Billing Roles & Rates" est desactive ou masque |
| 3 | Lorsque le Billing Type est "Hourly / Time & Materials", seul le sous-onglet "Billing Roles & Rates" est actif ; le sous-onglet "Fixed Fees" est desactive ou masque |
| 4 | Lorsque le Billing Type est "Mixed - Fixed Fee/Hourly", les deux sous-onglets "Fixed Fees" et "Billing Roles & Rates" sont actifs et configurables simultanement |
| 5 | En mode Mixed, le montant total du contrat est la somme de la partie forfaitaire (somme des fixed fees) et de la partie horaire (estimee ou plafonnee) ; cette decomposition est affichee sur la fiche contrat |
| 6 | Lors de la creation d'une facture sur un contrat Mixed, l'utilisateur peut choisir de facturer un jalon forfaitaire, des heures au temps passe, ou les deux simultanement dans une meme facture |
| 7 | Le calcul automatique du montant total de la facture en mode Mixed combine : la somme des lignes forfaitaires (jalons selectionnes) + la somme des lignes horaires (heures x Billing Rate) |
| 8 | Les KPIs financiers (Revenue, Cost, Profit, Margin %) integrent les deux composantes de facturation (forfaitaire et horaire) dans leurs calculs |
| 9 | Le Billing Type est modifiable tant qu'aucune facture n'a ete emise sur le contrat ; un avertissement est affiche si des factures existent deja lors d'une tentative de modification |
| 10 | Un indicateur visuel distinct identifie le type de facturation du contrat dans la liste des contrats (icone, badge ou colonne dediee) |
| 11 | Le filtre de la liste des contrats inclut un critere "Billing Type" permettant de filtrer par mode de facturation |
| 12 | Le rapport de suivi contractuel affiche la ventilation du montant facture entre la composante forfaitaire et la composante horaire |

---

### US-CF-23 -- Gestion des forfaits par jalons (Fixed Fees)

**En tant que** gestionnaire de projets ou directeur financier
**Je veux** configurer et suivre les forfaits par jalons (Fixed Fees) dans un contrat de type Fixed Fee ou Mixed
**Afin de** planifier les echeances de facturation forfaitaire, suivre l'avancement des jalons et generer automatiquement les factures a la date prevue

| # | Critere d'acceptation |
|---|---|
| 1 | Un sous-onglet "Fixed Fees" est accessible depuis la fiche detaillee d'un contrat de type Fixed Fee ou Mixed |
| 2 | Le sous-onglet affiche un tableau editable avec les colonnes : **Billing date** (date de facturation prevue), **Billing amount** (montant du jalon en CAD), **Billed** (statut : oui/non), **Revenue recognized** (revenu reconnu : oui/non), **Revenue recognition date** (date de reconnaissance du revenu) |
| 3 | Un bouton "Ajouter un jalon" permet d'ajouter une nouvelle ligne dans le tableau des Fixed Fees avec les champs pre-remplis par defaut (date du jour, montant a zero, Billed = non, Revenue recognized = non) |
| 4 | Un jalon peut etre modifie tant qu'il n'a pas ete facture (Billed = non) ; un jalon facture est verrouille en edition sauf pour les champs Revenue recognized et Revenue recognition date |
| 5 | Un jalon peut etre supprime uniquement s'il n'a pas ete facture (Billed = non) ; une confirmation est demandee avant la suppression |
| 6 | Le total des forfaits est affiche en bas du tableau : somme de tous les Billing amounts ; ce total est compare au montant contractuel forfaitaire avec un indicateur d'ecart |
| 7 | Un mecanisme de facturation manuelle permet de selectionner un ou plusieurs jalons et de generer une facture Draft pre-remplie avec les lignes correspondantes |
| 8 | Un mecanisme de facturation automatique peut etre active : les jalons dont la Billing date est atteinte et dont le statut est "non facture" declenchent automatiquement la creation d'une facture Draft |
| 9 | Lorsqu'un jalon est facture (facture engagee), le champ Billed passe automatiquement a "oui" et la ligne est mise en surbrillance visuelle |
| 10 | Un indicateur de progression visuel (barre de progression) affiche le pourcentage des forfaits deja factures par rapport au total des forfaits prevus |
| 11 | Les donnees reelles du contrat Place des Arts sont supportees : jalons multiples a des dates identiques (ex : 2 jalons au 9/30/2023, 2 jalons au 1/1/2024) avec des montants distincts |
| 12 | L'historique des modifications des jalons (ajout, modification de montant, modification de date) est trace dans l'audit trail du contrat |

---

### US-CF-24 -- Surcharge de taux par ressource (Resource-level Rate Override)

**En tant que** gestionnaire de projets ou directeur financier
**Je veux** definir un taux de facturation specifique pour une personne donnee sur un role de facturation d'un contrat, en remplacement du taux standard du role
**Afin de** gerer les cas ou une ressource specifique doit etre facturee a un taux different du taux standard de son role (ex : Melissa Belanger, Architecte patron, avec un Standard Rate de 0.00 mais un Billing Rate override de 150.85$/h)

| # | Critere d'acceptation |
|---|---|
| 1 | Dans le sous-onglet "Billing Roles & Rates" d'un contrat, un bouton "Ajouter un override par ressource" est disponible pour chaque role configure |
| 2 | Le formulaire d'override comprend les champs : **Ressource** (selection dans la liste des collaborateurs affectes au projet), **Role** (pre-rempli avec le role selectionne), **Standard Rate** (taux standard de la ressource, peut etre 0.00), **Billing Rate** (taux de facturation effectif pour cette ressource), **Date d'effet** (date a partir de laquelle l'override s'applique) |
| 3 | Un meme role peut avoir plusieurs overrides par ressource ; chaque override est affiche sur une ligne distincte, visuellement indentee sous le role parent (ex : "Architecte patron" -> "Override : Melissa Belanger") |
| 4 | Le cas "Standard Rate = 0.00 / Billing Rate > 0" est explicitement supporte, avec un avertissement visuel ("Taux standard a zero, facturation au taux override") ; ce cas correspond a une ressource dont le cout standard n'est pas renseigne mais qui est facturee au taux du role |
| 5 | La **hierarchie de priorite des taux** est respectee lors de la generation des lignes de facture : 1. Override par ressource (si defini) > 2. Taux du role (Billing Rate du role dans le contrat) > 3. Taux par defaut (si aucun role ni override n'est configure) |
| 6 | Lors de la generation d'une facture a partir des heures approuvees, le systeme applique automatiquement le taux override si un override existe pour la ressource et le role concernes ; sinon, il applique le taux standard du role |
| 7 | L'affichage des lignes de facture identifie clairement quand un taux override a ete applique (indicateur visuel, icone ou tooltip) |
| 8 | Un override peut etre modifie tant qu'aucune facture utilisant cet override n'a ete engagee ; les modifications sont tracees dans l'historique du contrat |
| 9 | Un override peut etre desactive (sans suppression) pour revenir au taux standard du role pour les futures factures |
| 10 | La liste des overrides est exportable avec le detail : role, ressource, taux standard, taux override, date d'effet, nombre d'heures facturees avec cet override |
| 11 | Les KPIs financiers (Revenue) prennent en compte les taux override dans le calcul du revenu : `Revenue = Somme(heures x taux applicable)` ou le taux applicable est le taux override s'il existe, sinon le taux du role |
| 12 | Un rapport de comparaison est disponible, affichant l'ecart entre le Revenue calcule avec les taux standard et le Revenue calcule avec les taux override |

---

### US-CF-25 -- Reconnaissance des revenus (Revenue Recognition)

**En tant que** directeur financier ou comptable
**Je veux** gerer la reconnaissance des revenus sur un contrat selon differentes methodes (pourcentage d'avancement, achevement, jalons)
**Afin de** assurer la conformite comptable en reconnaissant les revenus dans les periodes fiscales appropriees, independamment du calendrier de facturation

| # | Critere d'acceptation |
|---|---|
| 1 | Une section "Revenue Recognition" est disponible dans la fiche detaillee d'un contrat, accessible via un sous-onglet dedie |
| 2 | Trois methodes de reconnaissance des revenus sont supportees : **Pourcentage d'avancement** (les revenus sont reconnus au prorata de l'avancement du projet), **Achevement** (les revenus sont reconnus a la livraison finale du projet), **Jalons** (les revenus sont reconnus a chaque jalon atteint) |
| 3 | La methode de reconnaissance est selectionnable par contrat et modifiable par un utilisateur ayant le role "Directeur financier" ou "Comptable" |
| 4 | Pour les contrats de type Fixed Fee ou Mixed, le tableau des Fixed Fees affiche les colonnes **Revenue recognized** (oui/non) et **Revenue recognition date**, permettant de marquer manuellement ou automatiquement la reconnaissance du revenu par jalon |
| 5 | En methode "Pourcentage d'avancement", le revenu reconnu est calcule automatiquement : `Revenu reconnu = Montant total contrat x Pourcentage d'avancement` ; le pourcentage d'avancement est determine par le ratio heures consommees / heures estimees ou par saisie manuelle |
| 6 | En methode "Achevement", aucun revenu n'est reconnu tant que le projet n'est pas marque comme "termine" ; a l'achevement, la totalite du montant contractuel est reconnue en une seule fois |
| 7 | En methode "Jalons", le revenu est reconnu unitairement a chaque jalon marque comme "Revenue recognized = oui" ; le montant reconnu correspond au Billing amount du jalon |
| 8 | Un tableau de synthese affiche la ventilation par exercice fiscal : **Exercice**, **Revenu reconnu**, **Revenu differe** (facture mais non reconnu), **Revenu a facturer** (reconnu mais non facture) |
| 9 | L'ecart entre le montant facture et le montant reconnu est affiche sur la fiche contrat avec un indicateur visuel (positif = revenu differe, negatif = revenu anticipe) |
| 10 | Les ecritures de reconnaissance de revenu sont tracees dans l'audit trail avec : date, montant, methode, utilisateur ayant effectue ou valide la reconnaissance |
| 11 | Un rapport de reconnaissance des revenus par periode est disponible pour les besoins de cloture comptable, exportable en CSV et PDF |
| 12 | La reconnaissance de revenu est reversible (annulation d'une reconnaissance anterieurement validee) uniquement par un utilisateur "Directeur financier" avec une justification obligatoire |

---

### US-CF-26 -- Gestion des sous-traitants (Vendors)

**En tant que** gestionnaire de projets ou directeur financier
**Je veux** gerer les sous-traitants (Vendors) affectes a un contrat, suivre leurs couts et leur impact sur la rentabilite du projet
**Afin de** avoir une vision complete des couts du projet incluant les sous-traitants et calculer des KPIs de rentabilite precis

| # | Critere d'acceptation |
|---|---|
| 1 | Une section "Vendors" est disponible dans la fiche detaillee d'un contrat, accessible via un sous-onglet dedie |
| 2 | Le sous-onglet affiche un tableau editable avec les colonnes : **Vendor name** (nom du sous-traitant), **Contact** (personne-contact), **Service description** (description du service), **Budget amount** (montant budgete en CAD), **Actual cost** (cout reel engage), **Remaining** (solde restant = budget - cout reel), **Status** (actif/termine/annule) |
| 3 | Un bouton "Ajouter un sous-traitant" permet d'ajouter un nouveau vendor au contrat avec les informations requises (nom, contact, description, budget) |
| 4 | Un vendor peut etre modifie (mise a jour du budget, du cout reel, du statut) tant que le contrat est actif ; les modifications sont tracees dans l'historique du contrat |
| 5 | Un vendor peut etre supprime uniquement s'il n'a aucun cout reel enregistre (Actual cost = 0) ; un vendor avec des couts ne peut qu'etre marque comme "annule" |
| 6 | Le total des budgets vendors est affiche en bas du tableau ; une alerte visuelle est declenchee si le total des budgets vendors depasse un pourcentage configurable du montant contractuel (ex : > 30%) |
| 7 | Les couts vendors sont integres dans le calcul des KPIs financiers : **Cost** = Couts internes (heures x taux cout interne) + Couts vendors (somme des Actual costs). Le **Profit** et la **Margin %** sont recalcules en consequence |
| 8 | Un indicateur de depassement de budget vendor est affiche : si l'Actual cost d'un vendor depasse son Budget amount, une alerte rouge est affichee avec l'ecart en montant et en pourcentage |
| 9 | Les couts vendors sont ventilables par periode (mois, trimestre, annee) pour le suivi budgetaire |
| 10 | Un rapport de synthese des vendors par contrat est disponible, affichant pour chaque vendor : budget, cout reel, ecart, statut ; exportable en CSV |
| 11 | La liste des vendors est searchable et filtrable par nom, statut et montant |
| 12 | L'association d'un vendor a un contrat cree un lien avec le referentiel Vendors/Fournisseurs (si existant dans le systeme) pour eviter les doublons de saisie |

---

### US-CF-27 -- Limites contractuelles (Contract Limits)

**En tant que** gestionnaire de projets ou directeur financier
**Je veux** definir des limites contractuelles (plafond par facture, plafond global) sur un contrat et recevoir des alertes en cas de depassement
**Afin de** respecter les engagements contractuels, eviter les surfacturations et piloter le risque financier du contrat

| # | Critere d'acceptation |
|---|---|
| 1 | Une section "Contract Limits" est disponible dans la fiche detaillee d'un contrat, accessible via un sous-onglet dedie |
| 2 | Les champs suivants sont configurables : **Maximum per invoice** (montant maximum autorise par facture en CAD), **Contract ceiling** (plafond global du contrat en CAD, distinct du montant contractuel initial), **Notification threshold %** (pourcentage du plafond a partir duquel une alerte est declenchee, ex : 80%, 90%, 95%) |
| 3 | Le Maximum per invoice, s'il est defini, est valide au moment de la creation d'une facture : si le montant total de la facture Draft depasse le maximum, un avertissement bloquant est affiche et la facture ne peut pas etre soumise pour approbation |
| 4 | Le Contract ceiling, s'il est defini, est compare au cumul des factures engagees (Committed et au-dela) : si le cumul depasse le plafond, une alerte est declenchee et la soumission de nouvelles factures est bloquee sauf autorisation exceptionnelle d'un "Directeur financier" |
| 5 | Un indicateur de progression visuel affiche le ratio montant facture cumule / plafond contractuel, avec un code couleur : vert (< seuil de notification), orange (entre le seuil et 100%), rouge (>= 100%) |
| 6 | Des alertes automatiques (email et/ou in-app) sont envoyees aux gestionnaires et directeurs financiers lorsque le cumul facture atteint chaque seuil de notification configure |
| 7 | Le depassement du contrat Place des Arts (facture 1,110,469 CAD pour un contrat de 882,350 CAD = 126% du contrat) est gere : le systeme autorise le depassement apres validation explicite d'un "Directeur financier" mais maintient l'alerte rouge visible |
| 8 | L'historique des depassements autorises est trace dans l'audit trail avec : date, montant du depassement, utilisateur ayant autorise, justification |
| 9 | Les limites contractuelles sont modifiables par un "Directeur financier" a tout moment ; les modifications sont tracees dans l'historique du contrat |
| 10 | Un rapport des contrats avec depassement ou proche du plafond est disponible, affichant : contrat, plafond, cumul facture, ecart, statut d'alerte ; exportable en CSV |
| 11 | Si aucune limite n'est definie (champs laisses vides), aucune restriction n'est appliquee et aucune alerte n'est declenchee (comportement par defaut) |
| 12 | Les limites s'appliquent au montant total des factures engagees (hors avoirs) ; les avoirs sont soustraits du cumul pour le calcul du plafond |

---

### US-CF-28 -- Ligne de metier et classification (Line of Business)

**En tant que** directeur financier, associe ou gestionnaire de projets
**Je veux** classifier chaque contrat par ligne de metier (Line of Business) et exploiter cette classification pour le reporting et le filtrage
**Afin de** analyser la performance financiere par type de service (architecture, design interieur, urbanisme, etc.) et piloter la strategie commerciale

| # | Critere d'acceptation |
|---|---|
| 1 | Un champ "Line of Business" est disponible sur le formulaire de creation et de modification d'un contrat ; il s'agit d'une liste deroulante configurable par un administrateur |
| 2 | Les valeurs par defaut de la liste incluent au minimum : Architecture, Design interieur, Urbanisme, Paysage, Consultation, Autre ; la liste est extensible par un administrateur via le module Configuration (EPIC-016) |
| 3 | Le champ Line of Business est optionnel a la creation du contrat mais recommande (un avertissement visuel est affiche si le champ est vide lors de la soumission de la premiere facture) |
| 4 | La liste des contrats inclut une colonne "Line of Business" affichant la valeur selectionnee pour chaque contrat |
| 5 | Un filtre "Line of Business" est disponible dans la liste des contrats et dans la liste des factures, permettant de filtrer par ligne de metier (selection simple ou multiple) |
| 6 | Les KPIs financiers (Revenue, Cost, Profit, Margin %) sont consultables par Line of Business : un regroupement ou une vue pivot permet d'afficher les KPIs agreges par ligne de metier |
| 7 | Le tableau de bord facturation (US-CF-18) inclut un graphique de repartition du chiffre d'affaires par Line of Business (camembert ou barres) |
| 8 | Les exports CSV et PDF incluent une colonne "Line of Business" pour permettre l'analyse par ligne de metier dans un tableur |

---

## Regles Metier Additionnelles (Addendum)

| Ref | Regle |
|---|---|
| **RM-CF-23** | Le **Billing Type** d'un contrat determine les modes de facturation disponibles. En mode **Fixed Fee**, seuls les jalons forfaitaires sont facturables. En mode **Hourly / Time & Materials**, seules les heures au temps passe sont facturables. En mode **Mixed - Fixed Fee/Hourly**, les deux modes sont disponibles simultanement. Le Billing Type est defini a la creation du contrat et ne peut etre modifie que si aucune facture n'a ete engagee. |
| **RM-CF-24** | Les **Fixed Fees** (forfaits par jalons) sont definis par un Billing date et un Billing amount. Plusieurs jalons peuvent avoir la meme date de facturation avec des montants differents. Un jalon facture (Billed = oui) ne peut plus etre modifie ni supprime. Le total des jalons n'est pas contraint par le montant contractuel mais un avertissement est affiche en cas d'ecart superieur a 5%. |
| **RM-CF-25** | La **surcharge de taux par ressource** (Resource-level Rate Override) permet de definir un taux de facturation specifique pour une personne donnee, distinct du taux standard du role. La hierarchie de priorite est : 1. Override par ressource > 2. Taux du role > 3. Taux par defaut. Un Standard Rate de 0.00 avec un Billing Rate positif est autorise (cas d'une ressource sans taux standard renseigne mais facturee au taux du role). |
| **RM-CF-26** | La **reconnaissance des revenus** est independante de la facturation. Un revenu peut etre reconnu avant d'etre facture (revenu anticipe) ou apres avoir ete facture (revenu differe). La methode de reconnaissance (pourcentage d'avancement, achevement, jalons) est definie par contrat et appliquee de maniere coherente pour toute la duree du contrat. Un changement de methode en cours de contrat necessite l'approbation du Directeur financier et une justification tracee. |
| **RM-CF-27** | Les **couts des sous-traitants** (Vendors) sont integres dans le calcul du Cost total du projet : `Cost total = Couts internes (heures x taux interne) + Couts vendors`. Le Profit et la Margin % sont recalcules en consequence. Un vendor ne peut pas etre supprime si des couts reels ont ete enregistres ; il ne peut qu'etre desactive (statut "annule"). |
| **RM-CF-28** | Le **Maximum per invoice** constitue un plafond strict : aucune facture ne peut etre soumise pour approbation si son montant total depasse cette limite. Le **Contract ceiling** constitue un plafond souple : une alerte est declenchee mais le depassement peut etre autorise par un Directeur financier avec justification tracee. Les avoirs sont soustraits du cumul facture pour le calcul du plafond. |
| **RM-CF-29** | La **Line of Business** est une classification hierarchique des contrats par type de service. Elle sert de dimension d'analyse pour le reporting financier. La liste des valeurs est configurable par un administrateur. Le champ est optionnel mais un avertissement est emis si non renseigne lors de la premiere facturation du contrat. |
| **RM-CF-30** | En mode **Mixed - Fixed Fee/Hourly**, le montant total facture d'un contrat est la somme de la composante forfaitaire (somme des jalons factures) et de la composante horaire (somme des heures facturees x taux applicable). Les KPIs financiers distinguent les deux composantes dans le detail mais les consolident dans les indicateurs agreges (Revenue total, Profit total, Margin % globale). |

---

### Modele de Donnees Additionnel (Addendum)

#### Objet : FixedFee (Jalon forfaitaire)

| Champ | Type | Description |
|---|---|---|
| `id` | UUID | Identifiant unique du jalon |
| `contract_id` | FK -> Contract | Contrat associe |
| `billing_date` | Date | Date de facturation prevue |
| `billing_amount` | Decimal(12,2) | Montant du jalon en CAD |
| `is_billed` | Boolean | Indique si le jalon a ete facture (defaut : false) |
| `invoice_id` | FK -> Invoice (nullable) | Facture associee (si facture) |
| `revenue_recognized` | Boolean | Indique si le revenu a ete reconnu (defaut : false) |
| `revenue_recognition_date` | Date (nullable) | Date de reconnaissance du revenu |
| `description` | String (nullable) | Description du jalon |
| `sort_order` | Integer | Ordre d'affichage |
| `created_at` | DateTime | Date de creation |
| `updated_at` | DateTime | Date de derniere modification |

#### Objet : BillingRateOverride (Surcharge de taux par ressource)

| Champ | Type | Description |
|---|---|---|
| `id` | UUID | Identifiant unique |
| `contract_id` | FK -> Contract | Contrat associe |
| `billing_role_id` | FK -> BillingRole | Role de facturation associe |
| `user_id` | FK -> User | Collaborateur concerne |
| `standard_rate` | Decimal(10,2) | Taux horaire standard de la ressource (peut etre 0.00) |
| `billing_rate` | Decimal(10,2) | Taux de facturation override |
| `effective_from` | Date | Date d'entree en vigueur de l'override |
| `effective_to` | Date (nullable) | Date de fin de validite (nullable = indefini) |
| `is_active` | Boolean | Indique si l'override est actif (defaut : true) |
| `created_at` | DateTime | Date de creation |
| `updated_at` | DateTime | Date de derniere modification |

#### Objet : RevenueRecognition (Reconnaissance de revenu)

| Champ | Type | Description |
|---|---|---|
| `id` | UUID | Identifiant unique |
| `contract_id` | FK -> Contract | Contrat associe |
| `method` | Enum | Methode : `percentage_of_completion`, `completed_contract`, `milestone` |
| `fiscal_year` | Integer | Exercice fiscal |
| `fiscal_period` | String | Periode fiscale (ex : "Q1 2024", "2024-01") |
| `amount_recognized` | Decimal(12,2) | Montant reconnu dans la periode |
| `amount_deferred` | Decimal(12,2) | Montant differe (facture mais non reconnu) |
| `percentage_complete` | Decimal(5,2) (nullable) | Pourcentage d'avancement (pour la methode percentage_of_completion) |
| `recognized_by` | FK -> User | Utilisateur ayant effectue la reconnaissance |
| `recognized_at` | DateTime | Date de la reconnaissance |
| `notes` | Text (nullable) | Notes ou justification |
| `created_at` | DateTime | Date de creation |

#### Objet : Vendor (Sous-traitant)

| Champ | Type | Description |
|---|---|---|
| `id` | UUID | Identifiant unique |
| `contract_id` | FK -> Contract | Contrat associe |
| `vendor_name` | String | Nom du sous-traitant |
| `contact_name` | String (nullable) | Personne-contact |
| `contact_email` | String (nullable) | Email du contact |
| `service_description` | Text | Description du service fourni |
| `budget_amount` | Decimal(12,2) | Montant budgete (CAD) |
| `actual_cost` | Decimal(12,2) | Cout reel engage (CAD) |
| `status` | Enum | Statut : `active`, `completed`, `cancelled` |
| `created_at` | DateTime | Date de creation |
| `updated_at` | DateTime | Date de derniere modification |

#### Objet : ContractLimit (Limites contractuelles)

| Champ | Type | Description |
|---|---|---|
| `id` | UUID | Identifiant unique |
| `contract_id` | FK -> Contract | Contrat associe |
| `max_per_invoice` | Decimal(12,2) (nullable) | Plafond par facture (CAD) |
| `contract_ceiling` | Decimal(12,2) (nullable) | Plafond global du contrat (CAD) |
| `notification_threshold_pct` | Decimal(5,2) | Seuil d'alerte en pourcentage (defaut : 80.00) |
| `ceiling_override_allowed` | Boolean | Autorisation de depassement du plafond (defaut : false) |
| `ceiling_override_by` | FK -> User (nullable) | Utilisateur ayant autorise le depassement |
| `ceiling_override_reason` | Text (nullable) | Justification du depassement |
| `created_at` | DateTime | Date de creation |
| `updated_at` | DateTime | Date de derniere modification |

#### Modifications a l'objet Contract existant

| Champ ajoute | Type | Description |
|---|---|---|
| `billing_type` | Enum | Type de facturation : `fixed_fee`, `hourly`, `mixed` (defaut : `hourly`) |
| `line_of_business` | String (nullable) | Ligne de metier (reference vers la liste configurable) |

---

### Estimation Complementaire (Addendum)

#### Sprints additionnels suggeres

| Sprint | User Stories | Perimetre | Duree estimee |
|---|---|---|---|
| **Sprint 11** | US-CF-22, US-CF-23 | Facturation hybride Mixed + Gestion des Fixed Fees par jalons | 2.5 semaines |
| **Sprint 12** | US-CF-24, US-CF-25 | Surcharge de taux par ressource + Reconnaissance des revenus | 2.5 semaines |
| **Sprint 13** | US-CF-26, US-CF-27 | Gestion des Vendors + Limites contractuelles | 2 semaines |
| **Sprint 14** | US-CF-28 | Line of Business + Integration avec KPIs et reporting + Tests de bout en bout addendum | 1.5 semaine |

#### Estimation globale mise a jour

| Indicateur | Valeur initiale | Valeur mise a jour |
|---|---|---|
| **Nombre de User Stories** | 21 | 28 |
| **Nombre de criteres d'acceptation** | 211 | 297 |
| **Nombre de regles metier** | 22 | 30 |
| **Nombre de sprints** | 10 | 14 |
| **Duree totale estimee** | 20 a 22 semaines | 28.5 a 31 semaines |
| **Complexite** | Elevee | Tres elevee (ajout de la facturation hybride, revenue recognition, vendors, contract limits) |

#### Priorite de livraison recommandee (addendum)

7. **V2.0 Facturation avancee (Sprints 11-12)** : Facturation hybride Mixed, Fixed Fees, surcharge de taux par ressource, reconnaissance des revenus. Fonctionnalites critiques identifiees dans l'audit Place des Arts.
8. **V2.1 Gestion contractuelle etendue (Sprints 13-14)** : Vendors, limites contractuelles, Line of Business. Couverture complete des fonctionnalites ChangePoint.
