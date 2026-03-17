# EPIC -- Module Validation & Approbations

**Application OOTI -- Gestion de projets pour cabinets d'architecture**
**Version 1.0 -- Fevrier 2026**

---

## 1. Identification

| Champ | Valeur |
|---|---|
| **Nom de l'EPIC** | Validation & Approbations |
| **Reference** | EPIC-012 |
| **Module parent** | Equipe |
| **Priorite** | Haute |
| **Auteur** | Equipe Produit OOTI |
| **Date de creation** | 26/02/2026 |
| **Derniere mise a jour** | 26/02/2026 |
| **Statut** | A planifier |
| **EPICs lies** | EPIC-004 Facturation, EPIC-005 Temps, EPIC-013 Notes de frais, EPIC-009 Collaborateurs |

---

## 2. Contexte & Problematique

### 2.1 Contexte metier

Dans un cabinet d'architecture, la gestion quotidienne implique de nombreux flux de validation : les collaborateurs saisissent leurs temps de travail sur les projets, posent des demandes de conges, soumettent des notes de frais et preparent des factures clients. Chacun de ces elements doit etre verifie et approuve par un responsable (chef de projet, manager, directeur ou responsable administratif) avant d'etre pris en compte dans la comptabilite, la paie ou la facturation.

Aujourd'hui, sans module de validation centralise, ces processus sont souvent geres par email, tableurs partages ou echanges informels. Cela engendre :

- **Des retards de traitement** : les demandes se perdent dans les boites mail, les validations trainent en fin de mois, ce qui decale la facturation et la paie.
- **Un manque de tracabilite** : il est difficile de savoir qui a valide quoi, quand, et sur quelle base. En cas de litige ou d'audit, la reconstitution de l'historique est penible et incertaine.
- **Des erreurs et oublis** : sans workflow structure, certaines saisies de temps ne sont jamais verifiees, des notes de frais sont payees sans justificatif, des factures partent sans relecture.
- **Une charge administrative disproportionnee** : les managers passent un temps considerable a relancer, consolider et verifier manuellement les elements soumis par leurs equipes.
- **Une frustration des collaborateurs** : l'absence de visibilite sur l'etat de leurs demandes (conges en attente, notes de frais non traitees) genere de l'incertitude et des relances repetees.

### 2.2 Problematique

Comment offrir aux cabinets d'architecture un systeme de validation transversal, centralise et configurable, qui permette aux managers de traiter rapidement et en toute transparence les demandes de leurs equipes (temps, conges, notes de frais, factures), tout en garantissant la tracabilite complete des decisions et en s'integrant de maniere fluide avec les modules existants de l'application ?

### 2.3 Utilisateurs concernes

| Role | Interaction avec le module |
|---|---|
| **Collaborateur / Architecte** | Soumet des saisies de temps, demandes de conges, notes de frais. Consulte le statut de ses demandes. Recoit des notifications de validation ou de refus. |
| **Chef de projet** | Valide les temps saisis sur ses projets. Peut valider les notes de frais liees a ses projets. Premiere couche d'approbation. |
| **Manager / Directeur d'agence** | Valide les conges de son equipe. Valide les notes de frais. Supervise les temps. Deuxieme couche d'approbation si workflow multi-niveaux. |
| **Responsable administratif / Comptable** | Valide les factures avant envoi. Verifie la coherence des notes de frais. Derniere couche d'approbation pour les elements financiers. |
| **Administrateur** | Configure les workflows de validation (qui valide quoi, seuils, regles d'auto-approbation). Gere les parametres globaux du module. |

---

## 3. Objectif

### 3.1 Objectif principal

Fournir un module de validation transversal et centralise, accessible depuis le menu **Equipe > Validation**, qui regroupe l'ensemble des elements en attente d'approbation (temps, conges, notes de frais, factures) et permet aux responsables de les traiter efficacement, individuellement ou en masse, avec un historique complet et des notifications automatiques.

### 3.2 Objectifs specifiques

| # | Objectif | Indicateur de succes |
|---|---|---|
| O1 | Centraliser toutes les demandes de validation dans un tableau de bord unique avec badge compteur | 100% des elements en attente visibles dans le tableau de bord, badge mis a jour en temps reel |
| O2 | Reduire le temps de traitement des validations | Temps moyen de validation inferieur a 48h (contre 5-7 jours actuellement) |
| O3 | Permettre la validation en masse pour accelerer les traitements recurrents | Un manager peut valider 50 saisies de temps en moins de 30 secondes |
| O4 | Garantir la tracabilite complete de chaque decision | 100% des validations/refus enregistres avec horodatage, auteur et commentaire optionnel |
| O5 | Offrir un workflow de validation configurable adapte a chaque cabinet | Au moins 3 schemas de workflow configurables (simple, double approbation, par seuil) |
| O6 | Automatiser les notifications pour supprimer les relances manuelles | Notifications automatiques a chaque changement de statut (soumission, approbation, refus) |
| O7 | S'integrer de maniere transparente avec les modules existants | Les statuts de validation sont refletes en temps reel dans EPIC-004, EPIC-005, EPIC-013 |

### 3.3 Resultats attendus

- Reduction de 70% du temps administratif consacre aux validations.
- Elimination des oublis de validation en fin de mois.
- Visibilite complete pour les collaborateurs sur l'etat de leurs demandes.
- Donnees fiables pour la facturation et la paie grace a la validation systematique.
- Audit trail complet pour les obligations legales et contractuelles.

---

## 4. Perimetre Fonctionnel

### 4.1 Vue d'ensemble du module

Le module **Validation & Approbations** est accessible via le menu principal : **Equipe > Validation**. Un **badge compteur** affiche en permanence le nombre total d'elements en attente de validation pour l'utilisateur connecte (ex: "46").

Le module est organise en **4 sous-onglets** :

```
EQUIPE > Validation [46]
  |-- Temps
  |-- Conges
  |-- Notes de frais
  |-- Factures
```

### 4.2 Fonctionnalites par sous-onglet

#### 4.2.1 Sous-onglet "Temps"

- Liste des saisies de temps soumises et en attente de validation.
- Informations affichees : collaborateur, projet, phase, date, duree, description de la tache.
- Validation individuelle (bouton "Approuver") ou refus individuel (bouton "Refuser" avec champ commentaire obligatoire).
- Validation en masse : selection multiple via cases a cocher + bouton "Valider la selection" ou "Tout valider".
- Filtres : par collaborateur, par projet, par semaine/mois, par statut.
- Tri par date de soumission, par collaborateur, par projet.
- Lien direct vers la feuille de temps complete du collaborateur pour contexte.
- Resume des heures par collaborateur et par projet.

#### 4.2.2 Sous-onglet "Conges"

- Liste des demandes de conges en attente, approuvees et refusees.
- Types de conges geres : CP (Conges Payes), RTT, Maladie (avec justificatif), Conge sans solde, Conge special (maternite, paternite, deces, mariage), Autres (configurable).
- Informations affichees : collaborateur, type de conge, date de debut, date de fin, nombre de jours, motif, solde restant du type concerne.
- Calendrier des absences de l'equipe (vue mensuelle ou hebdomadaire) pour verifier les chevauchements.
- Affichage du solde de conges du collaborateur (acquis, pris, en attente, solde disponible).
- Validation/refus avec commentaire.
- Alerte automatique si la demande chevauche des periodes critiques (livrables projets, conges d'autres collaborateurs du meme projet).
- Piece jointe pour justificatif (arret maladie, etc.).

#### 4.2.3 Sous-onglet "Notes de frais"

- Liste des notes de frais soumises en attente de validation.
- Informations affichees : collaborateur, date, categorie de frais, montant HT, TVA, montant TTC, projet associe, justificatif (apercu de l'image/PDF).
- Verification du justificatif : apercu integre (image, PDF) sans quitter la page.
- Verification du montant : coherence entre montant declare et justificatif.
- Validation/refus avec commentaire.
- Validation en masse des notes de frais d'un meme collaborateur ou d'un meme projet.
- Filtres : par collaborateur, par projet, par categorie, par periode, par montant.
- Alerte si le montant depasse un seuil configurable.

#### 4.2.4 Sous-onglet "Factures"

- Liste des factures en statut "Brouillon" en attente de validation avant envoi au client.
- Informations affichees : numero de facture, client, projet, montant HT, TVA, montant TTC, date d'echeance, redacteur.
- Apercu de la facture (PDF) depuis la liste.
- Workflow multi-niveaux possible : Brouillon -> Validation Chef de projet -> Validation Direction -> Prete a envoyer.
- Validation/refus avec commentaire et possibilite de demander des modifications.
- Suivi du statut dans le workflow (quelle etape, qui doit valider).
- Lien direct vers le module Facturation (EPIC-004) pour modifier la facture si besoin.

### 4.3 Fonctionnalites transversales

| Fonctionnalite | Description |
|---|---|
| **Badge compteur** | Nombre total d'elements en attente, affiche dans le menu et sur chaque sous-onglet. Mis a jour en temps reel. |
| **Workflow configurable** | Configuration des chaines de validation par type d'element, par equipe, par seuil de montant. |
| **Historique des validations** | Journal complet de toutes les actions : qui a valide/refuse, quand, avec quel commentaire. |
| **Notifications automatiques** | Notifications in-app et par email a chaque soumission, approbation ou refus. |
| **Actions en masse** | Selection multiple + action groupee (valider, refuser) sur tous les sous-onglets. |
| **Filtres et recherche** | Filtres multi-criteres persistants sur chaque sous-onglet. |
| **Delegation** | Possibilite de deleguer ses droits de validation a un autre utilisateur (absence, vacances). |
| **Rappels automatiques** | Relance automatique si un element est en attente depuis plus de X jours (configurable). |

---

## 5. User Stories

### US-V01 : Tableau de bord des validations en attente

**En tant que** manager / chef de projet,
**Je veux** disposer d'un tableau de bord centralise affichant tous les elements en attente de ma validation, avec un badge compteur visible en permanence dans le menu,
**Afin de** savoir en un coup d'oeil combien d'elements requierent mon attention et pouvoir les traiter efficacement sans naviguer entre plusieurs modules.

**Criteres d'acceptation :**

1. Le menu **Equipe > Validation** affiche un badge numerique indiquant le nombre total d'elements en attente de validation pour l'utilisateur connecte.
2. Le badge se met a jour en temps reel (ou au maximum dans les 30 secondes) lorsqu'un nouvel element est soumis ou qu'un element est traite.
3. Le tableau de bord affiche un resume par sous-onglet : nombre de temps en attente, nombre de conges en attente, nombre de notes de frais en attente, nombre de factures en attente.
4. Chaque sous-onglet affiche son propre badge compteur partiel (ex: Temps [12], Conges [3], Notes de frais [8], Factures [23]).
5. Le tableau de bord n'affiche que les elements que l'utilisateur connecte a le droit de valider, selon le workflow configure.
6. Un widget de resume affiche les statistiques cles : nombre d'elements traites cette semaine, temps moyen de traitement, elements en retard (> X jours).
7. Le tableau de bord est accessible depuis un raccourci clavier (Ctrl+Shift+V) et depuis une icone dans la barre de navigation principale.
8. Si aucun element n'est en attente, le badge disparait et le tableau de bord affiche un message "Aucun element en attente de validation".

---

### US-V02 : Validation des temps saisis

**En tant que** chef de projet / manager,
**Je veux** pouvoir consulter les saisies de temps soumises par les collaborateurs de mon equipe ou de mes projets, et les approuver ou les refuser individuellement,
**Afin de** m'assurer que les temps declares sont coherents avec le travail effectivement realise et les budgets alloues aux projets.

**Criteres d'acceptation :**

1. Le sous-onglet "Temps" affiche la liste de toutes les saisies de temps au statut "Soumis" que l'utilisateur a le droit de valider.
2. Chaque ligne affiche : nom du collaborateur, projet, phase du projet, date de la saisie, duree (en heures et minutes), description de la tache.
3. Un bouton "Approuver" (vert) permet de valider la saisie. Le statut passe a "Approuve" et la saisie est prise en compte dans les rapports et la facturation.
4. Un bouton "Refuser" (rouge) ouvre un champ de commentaire obligatoire. Le collaborateur est notifie du refus avec le motif.
5. Un lien "Voir la feuille de temps" permet d'ouvrir la feuille de temps complete du collaborateur pour la semaine concernee, afin de contextualiser la saisie.
6. Les saisies refusees sont renvoyees au collaborateur qui peut les modifier et les resoumettre. Elles reapparaissent alors dans la liste de validation.
7. Le valideur peut modifier la duree directement avant d'approuver (avec trace de la modification dans l'historique).
8. Un resume en bas de page affiche le total des heures en attente par collaborateur et par projet.

---

### US-V03 : Validation en masse des temps

**En tant que** manager,
**Je veux** pouvoir selectionner plusieurs saisies de temps et les valider ou les refuser en une seule action,
**Afin de** gagner du temps lors des periodes de validation recurrentes (fin de semaine, fin de mois) quand le volume de saisies est important.

**Criteres d'acceptation :**

1. Une case a cocher est presente sur chaque ligne de saisie de temps, ainsi qu'une case "Tout selectionner" en en-tete de la liste.
2. Lorsqu'au moins une ligne est selectionnee, une barre d'actions apparait avec les boutons "Valider la selection" et "Refuser la selection".
3. Le bouton "Valider la selection" approuve toutes les saisies selectionnees en une seule operation. Une confirmation est demandee ("Vous etes sur le point de valider X saisies de temps. Confirmer ?").
4. Le bouton "Refuser la selection" ouvre un champ de commentaire unique qui sera applique a toutes les saisies selectionnees. Le commentaire est obligatoire.
5. Un bouton "Tout valider" permet de valider l'ensemble des saisies visibles (apres application des filtres) sans selection prealable, avec confirmation.
6. Apres une action en masse, un message de confirmation affiche le nombre d'elements traites ("12 saisies de temps approuvees avec succes").
7. Si une erreur survient pendant le traitement en masse (ex: conflit de version), les elements en erreur sont signales et les autres sont traites normalement.
8. L'action en masse est enregistree dans l'historique avec le detail de chaque element traite.

---

### US-V04 : Demande et validation de conges

**En tant que** manager,
**Je veux** consulter les demandes de conges de mon equipe, verifier les chevauchements et les soldes, puis approuver ou refuser chaque demande,
**Afin de** garantir la continuite des projets en cours tout en respectant les droits aux conges des collaborateurs.

**Criteres d'acceptation :**

1. Le sous-onglet "Conges" affiche la liste des demandes de conges au statut "En attente" pour les collaborateurs dont l'utilisateur est le valideur designe.
2. Chaque demande affiche : nom du collaborateur, type de conge, date de debut, date de fin, nombre de jours ouvrables, motif (optionnel), piece jointe (si applicable).
3. Le solde de conges du collaborateur pour le type concerne est affiche a cote de la demande (acquis, pris, en attente, disponible).
4. Un calendrier d'equipe est accessible pour visualiser les absences deja planifiees et detecter les chevauchements potentiels.
5. Une alerte est affichee si la demande chevauche avec une echeance projet majeure ou avec les conges d'un autre collaborateur du meme projet.
6. Le bouton "Approuver" valide la demande, deduit les jours du solde et notifie le collaborateur.
7. Le bouton "Refuser" ouvre un champ de commentaire obligatoire. Le collaborateur est notifie avec le motif du refus et peut resoumettre une demande modifiee.
8. Les demandes de conge maladie avec justificatif sont marquees visuellement et le justificatif est consultable directement depuis la liste.

---

### US-V05 : Gestion des types de conges et soldes

**En tant qu'** administrateur RH,
**Je veux** configurer les types de conges disponibles, definir les regles d'acquisition et consulter les soldes de chaque collaborateur,
**Afin de** garantir une gestion rigoureuse des droits aux conges conforme a la legislation et aux accords d'entreprise.

**Criteres d'acceptation :**

1. L'administrateur peut creer, modifier et desactiver des types de conges : CP (Conges Payes), RTT, Maladie, Sans solde, Conge special (maternite, paternite, deces, mariage), et types personnalises.
2. Pour chaque type de conge, les parametres suivants sont configurables : nom, code, nombre de jours annuels (si applicable), report possible (oui/non, plafond), justificatif obligatoire (oui/non), impact sur la paie (deduction ou non).
3. Le solde de chaque collaborateur est calcule automatiquement : jours acquis (au prorata de la date d'entree) - jours pris - jours en attente = solde disponible.
4. Un tableau recapitulatif affiche les soldes de tous les collaborateurs avec filtres par equipe, par type de conge, par annee.
5. Une alerte est generee si un collaborateur demande plus de jours que son solde disponible (la demande peut etre soumise mais est signalee au valideur).
6. L'historique des conges de chaque collaborateur est consultable avec filtres par annee et par type.
7. Les regles de report automatique en fin d'annee sont configurables (ex: report des CP non pris dans une limite de X jours).
8. L'export des soldes de conges est possible au format CSV/Excel pour integration avec les logiciels de paie.

---

### US-V06 : Validation des notes de frais

**En tant que** manager / responsable administratif,
**Je veux** consulter les notes de frais soumises par les collaborateurs, verifier les montants et les justificatifs, puis les approuver ou les refuser,
**Afin de** controler les depenses engagees au nom du cabinet et garantir leur conformite avec la politique de frais en vigueur.

**Criteres d'acceptation :**

1. Le sous-onglet "Notes de frais" affiche la liste des notes de frais au statut "Soumise" que l'utilisateur a le droit de valider.
2. Chaque note de frais affiche : collaborateur, date de la depense, categorie (deplacement, repas, fournitures, hebergement, etc.), description, montant HT, TVA, montant TTC, projet associe (si applicable).
3. Le justificatif (photo, scan, PDF) est consultable directement depuis la liste via un apercu integre (modale ou panneau lateral) sans quitter la page.
4. Un bouton "Approuver" valide la note de frais et la transmet au service comptable pour remboursement.
5. Un bouton "Refuser" ouvre un champ de commentaire obligatoire. Le collaborateur est notifie et peut corriger sa note de frais et la resoumettre.
6. Une alerte visuelle est affichee si le montant depasse le seuil configurable pour la categorie (ex: repas > 25 EUR, deplacement > 500 EUR).
7. Le valideur peut modifier le montant avant approbation (ex: correction d'une erreur de saisie), avec trace de la modification dans l'historique.
8. Un resume affiche le total des notes de frais en attente par collaborateur et par categorie.

---

### US-V07 : Validation des factures (workflow multi-niveaux)

**En tant que** directeur / responsable administratif,
**Je veux** valider les factures preparees par les chefs de projet avant qu'elles ne soient envoyees aux clients, avec un workflow d'approbation multi-niveaux si necessaire,
**Afin de** garantir l'exactitude et la conformite de chaque facture emise par le cabinet et eviter les erreurs qui nuiraient a la relation client et a la tresorerie.

**Criteres d'acceptation :**

1. Le sous-onglet "Factures" affiche la liste des factures au statut "Brouillon - En attente de validation" que l'utilisateur a le droit de valider a l'etape actuelle du workflow.
2. Chaque facture affiche : numero, client, projet, montant HT, TVA, montant TTC, date d'emission, date d'echeance, redacteur.
3. Un apercu PDF de la facture est consultable directement depuis la liste (modale ou panneau lateral).
4. Le workflow multi-niveaux est configurable : Niveau 1 (Chef de projet) -> Niveau 2 (Directeur) -> Niveau 3 (Comptable). Chaque niveau peut etre active ou desactive.
5. A chaque niveau, le valideur peut : Approuver (passer au niveau suivant ou marquer comme "Prete a envoyer"), Refuser (retour au redacteur avec commentaire), Demander des modifications (retour au redacteur sans refus formel, avec annotations).
6. Le statut de la facture dans le workflow est visible : barre de progression montrant les etapes completees et l'etape en cours.
7. Lorsque tous les niveaux ont approuve, la facture passe automatiquement au statut "Validee - Prete a envoyer" dans le module Facturation (EPIC-004).
8. Un lien direct vers le module Facturation permet d'ouvrir et modifier la facture si necessaire.

---

### US-V08 : Refus avec commentaire et circuit de correction

**En tant que** valideur (manager, chef de projet, responsable administratif),
**Je veux** pouvoir refuser un element (temps, conge, note de frais, facture) en indiquant un motif detaille, et permettre au soumetteur de corriger et resoumettre,
**Afin de** communiquer clairement les raisons du refus et offrir une voie de correction sans multiplier les echanges informels.

**Criteres d'acceptation :**

1. Le bouton "Refuser" est disponible sur chaque element en attente de validation, quel que soit le sous-onglet.
2. Le clic sur "Refuser" ouvre un formulaire de refus comprenant : un champ de commentaire (texte libre, obligatoire, minimum 10 caracteres), une liste de motifs predefinies (optionnelle, configurable : "Montant incorrect", "Justificatif manquant", "Projet incorrect", "Duree excessive", "Autre").
3. Le refus est enregistre avec : la date et l'heure, l'identite du valideur, le motif selectionne, le commentaire detaille.
4. Le soumetteur recoit une notification (in-app et email) indiquant le refus avec le commentaire complet.
5. L'element refuse repasse au statut "Brouillon" ou "A corriger" chez le soumetteur. Celui-ci peut modifier l'element et le resoumettre.
6. Lorsqu'un element est resoumis apres refus, il est marque visuellement dans la liste de validation (badge "Resoumission") et l'historique des refus precedents est accessible.
7. Le nombre de refus/resoumissions est visible pour detecter les elements problematiques recurrents.
8. Un element refuse peut etre annule definitivement par le soumetteur s'il ne souhaite pas le corriger.

---

### US-V09 : Historique des validations

**En tant que** manager / administrateur,
**Je veux** consulter l'historique complet de toutes les validations et refus effectues, avec les details de chaque decision,
**Afin de** disposer d'une trace d'audit fiable pour les besoins de reporting, de controle interne et de conformite.

**Criteres d'acceptation :**

1. Un onglet "Historique" (ou section dediee) est accessible depuis le module Validation, affichant l'ensemble des elements traites.
2. Chaque entree de l'historique affiche : type d'element (temps, conge, note de frais, facture), reference de l'element, soumetteur, date de soumission, valideur, date de validation/refus, decision (Approuve/Refuse), commentaire.
3. L'historique est filtrable par : type d'element, valideur, soumetteur, periode (date de debut / date de fin), decision (approuve/refuse), projet.
4. L'historique est triable par date (ascendant/descendant), par type, par valideur, par soumetteur.
5. Un clic sur une entree de l'historique affiche le detail complet de l'element concerne et la chaine de validation (tous les niveaux traverses).
6. L'export de l'historique est possible au format CSV et PDF, avec les filtres appliques.
7. L'historique est conserve sans limitation de duree et n'est pas modifiable (immutabilite de la trace d'audit).
8. Les actions en masse sont detaillees individuellement dans l'historique (chaque element traite a sa propre entree).

---

### US-V10 : Configuration du workflow de validation

**En tant qu'** administrateur,
**Je veux** configurer les workflows de validation pour chaque type d'element (temps, conges, notes de frais, factures), en definissant les valideurs, les niveaux d'approbation et les regles automatiques,
**Afin d'** adapter le processus de validation aux specificites organisationnelles du cabinet et a ses exigences de controle interne.

**Criteres d'acceptation :**

1. Une interface d'administration permet de configurer un workflow pour chaque type d'element : Temps, Conges, Notes de frais, Factures.
2. Pour chaque workflow, l'administrateur peut definir : le nombre de niveaux d'approbation (1 a 3), les valideurs a chaque niveau (par role, par personne, par equipe), les regles d'escalade (si non traite apres X jours, escalader au niveau superieur).
3. Des regles d'auto-approbation sont configurables : saisies de temps inferieures a X heures, notes de frais inferieures a X EUR, conges de type demi-journee.
4. La delegation de validation est configurable : un valideur peut designer un suppleant pour une periode donnee (vacances, absence).
5. Les valideurs peuvent etre determines dynamiquement : par exemple, le chef du projet sur lequel les temps sont imputes, le manager hierarchique du collaborateur.
6. Un mode "preview" permet de tester un workflow configure avec un scenario fictif avant de l'activer.
7. Les modifications de workflow s'appliquent aux nouveaux elements soumis. Les elements deja en cours de validation continuent avec l'ancien workflow.
8. Un journal des modifications de configuration est tenu a jour (qui a modifie quoi, quand).

---

### US-V11 : Notifications de validation

**En tant que** collaborateur ou valideur,
**Je veux** recevoir des notifications automatiques a chaque etape du processus de validation (soumission, approbation, refus, rappel),
**Afin d'** etre informe en temps reel de l'avancement de mes demandes ou des elements necessitant mon action, sans avoir a verifier manuellement.

**Criteres d'acceptation :**

1. Une notification in-app (cloche dans la barre de navigation) est envoyee au valideur designe lorsqu'un nouvel element est soumis pour validation.
2. Une notification in-app est envoyee au soumetteur lorsque son element est approuve ou refuse, avec le commentaire du valideur le cas echeant.
3. Un email de notification est envoye en parallele de la notification in-app, avec un lien direct vers l'element concerne. L'envoi d'email est configurable (actif/inactif par utilisateur).
4. Un rappel automatique est envoye au valideur si un element est en attente depuis plus de X jours (seuil configurable, defaut : 3 jours ouvrables).
5. Un resume quotidien ou hebdomadaire (configurable) est envoye par email aux valideurs, listant tous les elements en attente de leur action.
6. Les notifications in-app sont regroupees pour eviter le spam : "5 saisies de temps soumises par Jean Dupont" plutot que 5 notifications individuelles.
7. Un centre de notifications permet de consulter l'historique de toutes les notifications recues, avec filtres par type et par statut (lu/non lu).
8. Les preferences de notification sont configurables par l'utilisateur : choix des canaux (in-app, email), frequence des resumes, activation/desactivation par type d'element.

---

### US-V12 : Delegation de validation

**En tant que** manager / valideur,
**Je veux** pouvoir deleguer temporairement mes droits de validation a un collegue pendant mes absences,
**Afin de** garantir la continuite du processus de validation meme lorsque je ne suis pas disponible.

**Criteres d'acceptation :**

1. Un valideur peut designer un delegue pour une periode definie (date de debut, date de fin) depuis les parametres de son profil ou depuis le module Validation.
2. Le delegue recoit les memes notifications et les memes droits de validation que le valideur original pendant la periode de delegation.
3. Les validations effectuees par le delegue sont tracees dans l'historique avec la mention "Valide par [delegue] pour le compte de [valideur original]".
4. Le valideur original peut revoquer la delegation a tout moment avant la date de fin.
5. A la fin de la periode de delegation, les droits du delegue sont automatiquement retires.
6. Un valideur ne peut deleguer qu'a un utilisateur ayant un role suffisant (un collaborateur simple ne peut pas devenir valideur par delegation).
7. Un avertissement est affiche si le valideur tente de deleguer a un utilisateur deja surcharge (plus de 50 elements en attente).
8. La delegation est visible dans le tableau de bord du delegue avec une indication claire "Delegation de [nom] jusqu'au [date]".

---

### US-V13 : Filtres et recherche avances

**En tant que** valideur,
**Je veux** pouvoir filtrer et rechercher les elements en attente de validation selon de multiples criteres,
**Afin de** retrouver rapidement les elements qui m'interessent et traiter les validations par lot de maniere organisee.

**Criteres d'acceptation :**

1. Chaque sous-onglet dispose d'une barre de filtres avec les criteres suivants : collaborateur (liste deroulante multi-selection), projet (liste deroulante multi-selection), periode (date debut / date fin ou presets : cette semaine, ce mois, mois dernier), statut (en attente, approuve, refuse, tous).
2. Un champ de recherche textuelle permet de chercher par mot-cle dans la description, le nom du collaborateur, le nom du projet ou le numero de facture.
3. Les filtres sont combinables (ET logique) : par exemple, collaborateur "Jean Dupont" ET projet "Tour Montparnasse" ET periode "Fevrier 2026".
4. Les filtres appliques sont affiches sous forme de badges cliquables permettant de les supprimer individuellement.
5. Les combinaisons de filtres peuvent etre sauvegardees en tant que "Vues" personnalisees (ex: "Mon equipe - Semaine courante").
6. Les filtres persistent lors de la navigation entre les sous-onglets au sein d'une meme session.
7. Un bouton "Reinitialiser les filtres" remet tous les criteres a leur valeur par defaut.
8. Le nombre de resultats correspondant aux filtres est affiche en temps reel.

---

## 6. Hors Perimetre

Les elements suivants sont explicitement **exclus** du perimetre de cet EPIC :

| # | Element hors perimetre | Justification |
|---|---|---|
| HP1 | **Saisie des temps** | Couverte par EPIC-005 (Module Temps). Le present module ne concerne que la validation des temps deja saisis. |
| HP2 | **Creation des notes de frais** | Couverte par EPIC-013 (Module Notes de frais). Le present module ne concerne que la validation des notes de frais soumises. |
| HP3 | **Creation et edition des factures** | Couvertes par EPIC-004 (Module Facturation). Le present module ne concerne que la validation des factures brouillon. |
| HP4 | **Gestion de la paie** | Le module ne calcule pas la paie. Il fournit des donnees validees (conges, notes de frais) qui peuvent etre exportees vers un logiciel de paie externe. |
| HP5 | **Workflow de validation pour les devis** | Les devis et propositions commerciales ont leur propre cycle de vie dans EPIC-003 (Honoraires). Une integration pourra etre envisagee dans une version future. |
| HP6 | **Validation des achats / bons de commande** | La gestion des achats n'est pas couverte par OOTI dans cette version. |
| HP7 | **Signature electronique des documents** | La signature electronique des factures ou des contrats n'est pas incluse. Elle pourra faire l'objet d'un EPIC futur. |
| HP8 | **Application mobile dediee** | Le module est concu en responsive design mais pas comme application mobile native. |
| HP9 | **Integration avec des outils de messagerie externe (Slack, Teams)** | Les notifications sont limitees a l'in-app et a l'email. Les integrations tierces pourront etre ajoutees ulterieurement. |
| HP10 | **Validation des plannings / staffing** | La validation des affectations de ressources sur les projets n'est pas couverte par ce module. |

---

## 7. Regles Metier

### 7.1 Regles generales de validation

| # | Regle | Description |
|---|---|---|
| RM01 | **Principe des quatre yeux** | Aucun element ne peut etre valide par la personne qui l'a soumis. Le valideur doit etre different du soumetteur. |
| RM02 | **Commentaire obligatoire en cas de refus** | Tout refus doit etre accompagne d'un commentaire explicatif d'au moins 10 caracteres. Un refus sans commentaire n'est pas possible. |
| RM03 | **Immutabilite de l'historique** | Les entrees de l'historique des validations ne peuvent etre ni modifiees ni supprimees. Toute correction doit se faire par une nouvelle action tracee. |
| RM04 | **Cascade de validation** | Dans un workflow multi-niveaux, un refus a n'importe quel niveau renvoie l'element au soumetteur. Il ne redescend pas au niveau precedent. |
| RM05 | **Auto-approbation interdite par defaut** | Un utilisateur ne peut pas approuver ses propres soumissions, meme s'il a le role de valideur. Cette regle peut etre assouplie uniquement par configuration administrateur pour des cas specifiques (ex: dirigeant unique). |

### 7.2 Regles specifiques aux temps

| # | Regle | Description |
|---|---|---|
| RM06 | **Coherence des heures** | Une saisie de temps ne peut pas depasser 16 heures par jour pour un meme collaborateur. Au-dela, une alerte est generee pour le valideur. |
| RM07 | **Validation retroactive limitee** | Les saisies de temps datant de plus de 2 mois ne peuvent etre validees qu'avec un commentaire justificatif du valideur. |
| RM08 | **Impact sur la facturation** | Un temps valide est automatiquement disponible pour la facturation dans EPIC-004. Un temps refuse n'est jamais facturable. |

### 7.3 Regles specifiques aux conges

| # | Regle | Description |
|---|---|---|
| RM09 | **Solde insuffisant** | Une demande de conge dont le nombre de jours depasse le solde disponible est soumise avec un avertissement au valideur. Elle peut etre approuvee (passage en solde negatif si autorise par la politique du cabinet) ou refusee. |
| RM10 | **Delai de prevenance** | Les conges payes doivent etre demandes au moins X jours ouvrables a l'avance (configurable, defaut : 5 jours). Les demandes hors delai sont marquees "Urgent" pour le valideur. |
| RM11 | **Conge maladie** | Les conges maladie sont enregistres a titre informatif et peuvent etre approuves sans justificatif dans un premier temps. Le justificatif (arret de travail) doit etre fourni dans les 48 heures. Un rappel automatique est envoye au collaborateur si le justificatif n'est pas recu dans ce delai. |
| RM12 | **Chevauchement** | Deux demandes de conges ne peuvent pas se chevaucher pour un meme collaborateur. La deuxieme demande est rejetee automatiquement a la soumission. |

### 7.4 Regles specifiques aux notes de frais

| # | Regle | Description |
|---|---|---|
| RM13 | **Justificatif obligatoire** | Toute note de frais d'un montant superieur a 10 EUR doit etre accompagnee d'un justificatif numerise (photo ou PDF). Sans justificatif, la soumission est bloquee. |
| RM14 | **Plafonds par categorie** | Des plafonds de montant sont configurables par categorie de frais (ex: repas 25 EUR, nuit d'hotel 150 EUR). Les depassements declenchent une alerte pour le valideur mais n'empechent pas la soumission. |
| RM15 | **Delai de soumission** | Les notes de frais doivent etre soumises dans un delai de 3 mois apres la date de la depense. Au-dela, elles requierent une approbation de niveau superieur. |

### 7.5 Regles specifiques aux factures

| # | Regle | Description |
|---|---|---|
| RM16 | **Coherence avec le contrat** | Le valideur de la facture doit s'assurer que le montant est coherent avec le contrat ou la convention d'honoraires (EPIC-003). Un ecart de plus de 10% declenche une alerte. |
| RM17 | **Numerotation sequentielle** | Le numero de facture n'est attribue definitivement qu'au moment du passage au statut "Validee". Tant que la facture est en brouillon ou en cours de validation, elle porte un numero provisoire. |
| RM18 | **Facture validee non modifiable** | Une facture qui a traverse l'integralite du workflow de validation ne peut plus etre modifiee. Toute correction necessite un avoir ou une facture rectificative. |

### 7.6 Regles de delegation

| # | Regle | Description |
|---|---|---|
| RM19 | **Delegation non transitive** | Un delegue ne peut pas a son tour deleguer les droits qui lui ont ete confies. La delegation est limitee a un seul niveau. |
| RM20 | **Delegation limitee dans le temps** | Une delegation ne peut pas exceder 90 jours. Au-dela, elle doit etre renouvelee explicitement. |

---

## 8. Criteres Globaux

### 8.1 Performance

| Critere | Seuil |
|---|---|
| Temps de chargement du tableau de bord | < 2 secondes pour un valideur ayant jusqu'a 200 elements en attente |
| Temps d'execution d'une validation individuelle | < 500 ms (hors temps reseau) |
| Temps d'execution d'une validation en masse (50 elements) | < 3 secondes |
| Mise a jour du badge compteur | < 30 secondes apres soumission d'un nouvel element |
| Chargement de l'apercu d'un justificatif (image/PDF) | < 1 seconde pour un fichier de moins de 5 Mo |

### 8.2 Securite

| Critere | Description |
|---|---|
| Controle d'acces | Chaque utilisateur ne voit que les elements qu'il a le droit de valider selon le workflow configure. |
| Separation des roles | Le soumetteur ne peut jamais valider son propre element (principe des quatre yeux, RM01). |
| Tracabilite | Toutes les actions (validation, refus, modification, delegation) sont enregistrees avec horodatage et identite de l'auteur. |
| Integrite des donnees | Les donnees de l'historique de validation sont protegees en ecriture (immutabilite). Aucune suppression ou modification n'est possible. |
| Chiffrement | Les justificatifs et documents sont stockes de maniere chiffree. |

### 8.3 Accessibilite

| Critere | Description |
|---|---|
| Conformite WCAG | Le module doit etre conforme au niveau AA des WCAG 2.1 (navigation au clavier, lecteurs d'ecran, contrastes). |
| Navigation clavier | Toutes les actions (validation, refus, filtres, navigation entre onglets) doivent etre realisables au clavier. |
| Responsive design | Le module doit etre utilisable sur tablette (1024px) et sur ecran de bureau (1280px+). |

### 8.4 Compatibilite

| Critere | Description |
|---|---|
| Navigateurs | Chrome (2 dernieres versions), Firefox (2 dernieres versions), Safari (2 dernieres versions), Edge (2 dernieres versions). |
| Integration | Le module doit s'integrer de maniere transparente avec EPIC-004 (Facturation), EPIC-005 (Temps), EPIC-013 (Notes de frais), EPIC-009 (Collaborateurs). |

### 8.5 Disponibilite

| Critere | Description |
|---|---|
| Disponibilite cible | 99,5% de disponibilite mensuelle (hors fenetres de maintenance planifiees). |
| Degradation gracieuse | En cas d'indisponibilite du service de notifications, les validations restent possibles. Les notifications sont envoyees des que le service est retabli. |

---

## 9. Definition of Done (DoD)

Un element du backlog (User Story) est considere comme **termine** lorsque l'ensemble des criteres suivants sont remplis :

### 9.1 Criteres fonctionnels

- [ ] Tous les criteres d'acceptation de la User Story sont implementes et verifies.
- [ ] Les regles metier associees sont correctement appliquees.
- [ ] Les cas limites et cas d'erreur sont geres (formulaire incomplet, erreur reseau, conflit de version, etc.).
- [ ] Les messages d'erreur sont clairs, traduits en francais et orientent l'utilisateur vers la resolution.

### 9.2 Criteres techniques

- [ ] Le code est revise par au moins un pair (code review approuvee).
- [ ] Les tests unitaires couvrent au moins 80% du code nouveau.
- [ ] Les tests d'integration verifient les interactions avec les modules lies (EPIC-004, EPIC-005, EPIC-009, EPIC-013).
- [ ] Les tests end-to-end couvrent les parcours critiques (soumission -> validation -> impact, soumission -> refus -> correction -> resoumission).
- [ ] Aucune regression n'est introduite (suite de tests existante au vert).
- [ ] Le code respecte les conventions et standards du projet (linting, formatage).

### 9.3 Criteres de qualite

- [ ] Les temps de reponse respectent les seuils definis (section 8.1 Performance).
- [ ] L'interface est conforme aux maquettes et au design system de l'application.
- [ ] L'accessibilite est verifiee (navigation clavier, lecteur d'ecran, contrastes).
- [ ] Le responsive design est verifie sur les resolutions cibles (tablette et desktop).
- [ ] Les notifications sont fonctionnelles (in-app et email) et correctement formatees.

### 9.4 Criteres de documentation

- [ ] Les endpoints API sont documentes (Swagger / OpenAPI).
- [ ] Les regles de workflow configurables sont documentees dans le guide administrateur.
- [ ] Les cas d'usage sont decrits dans la documentation utilisateur.

### 9.5 Criteres de deploiement

- [ ] La fonctionnalite est deployable de maniere independante (feature flag si necessaire).
- [ ] Les scripts de migration de base de donnees sont prepares et testes.
- [ ] Le rollback est possible sans perte de donnees.

---

## 10. Dependances

### 10.1 Dependances fonctionnelles (modules OOTI)

| EPIC | Module | Nature de la dependance | Direction |
|---|---|---|---|
| **EPIC-004** | Facturation | Les factures brouillon sont creees dans EPIC-004 et soumises a validation dans EPIC-012. Apres validation, le statut est mis a jour dans EPIC-004. | Bidirectionnelle |
| **EPIC-005** | Temps | Les saisies de temps sont creees dans EPIC-005 et soumises a validation dans EPIC-012. Apres validation, les temps sont marques comme valides dans EPIC-005 et deviennent facturables. | Bidirectionnelle |
| **EPIC-013** | Notes de frais | Les notes de frais sont creees dans EPIC-013 et soumises a validation dans EPIC-012. Apres validation, elles sont transmises au service comptable via EPIC-013. | Bidirectionnelle |
| **EPIC-009** | Collaborateurs | EPIC-009 fournit la structure organisationnelle (equipes, managers, roles) utilisee pour determiner les valideurs dans les workflows. | EPIC-012 depend de EPIC-009 |
| **EPIC-002** | Projets | Les projets et phases sont references dans les saisies de temps, notes de frais et factures. | EPIC-012 depend de EPIC-002 |
| **EPIC-003** | Honoraires | Les conventions d'honoraires sont utilisees pour verifier la coherence des factures lors de la validation. | EPIC-012 depend de EPIC-003 |

### 10.2 Dependances techniques

| Composant | Description | Criticite |
|---|---|---|
| **Systeme de notifications** | Service de notifications in-app (WebSocket ou polling) et envoi d'emails (SMTP ou service tiers). | Haute |
| **Stockage de fichiers** | Service de stockage pour les justificatifs de notes de frais et arrets maladie (S3 ou equivalent). | Haute |
| **Generateur PDF** | Service de generation PDF pour l'apercu des factures et l'export de l'historique. | Moyenne |
| **Service de calendrier** | Composant de calendrier pour la visualisation des absences de l'equipe. | Moyenne |
| **Moteur de workflow** | Composant d'orchestration des workflows de validation multi-niveaux. | Haute |

### 10.3 Ordre de realisation recommande

```
Phase 1 (Sprint 1-2) :
  - Infrastructure : modele de donnees, API de base, moteur de workflow
  - US-V01 : Tableau de bord
  - US-V10 : Configuration du workflow (version initiale)
  - US-V02 : Validation des temps (individuelle)

Phase 2 (Sprint 2-3) :
  - US-V03 : Validation en masse des temps
  - US-V04 : Demande et validation de conges
  - US-V05 : Gestion des types de conges et soldes
  - US-V08 : Refus avec commentaire

Phase 3 (Sprint 3-4) :
  - US-V06 : Validation des notes de frais
  - US-V07 : Validation des factures (workflow multi-niveaux)
  - US-V09 : Historique des validations
  - US-V11 : Notifications de validation
  - US-V12 : Delegation de validation
  - US-V13 : Filtres et recherche avances
```

---

## 11. Modele de Donnees

### 11.1 Diagramme des entites principales

```
+----------------------------+       +----------------------------+
|    ValidationRequest       |       |    ValidationHistory       |
+----------------------------+       +----------------------------+
| id : UUID (PK)            |       | id : UUID (PK)            |
| type : ENUM               |  1..* | validation_request_id : FK |
|   (TIME, LEAVE, EXPENSE,  |<----->| action : ENUM              |
|    INVOICE)                |       |   (SUBMITTED, APPROVED,    |
| reference_id : UUID (FK)  |       |    REFUSED, RESUBMITTED,   |
| submitted_by : UUID (FK)  |       |    CANCELLED, MODIFIED,    |
| submitted_at : TIMESTAMP  |       |    DELEGATED)              |
| status : ENUM             |       | performed_by : UUID (FK)   |
|   (DRAFT, SUBMITTED,      |       | performed_at : TIMESTAMP   |
|    PENDING_APPROVAL,       |       | comment : TEXT             |
|    APPROVED, REFUSED,      |       | previous_status : ENUM     |
|    CANCELLED)              |       | new_status : ENUM          |
| current_level : INTEGER   |       | metadata : JSONB           |
| max_level : INTEGER       |       +----------------------------+
| validated_by : UUID (FK)  |
| validated_at : TIMESTAMP  |       +----------------------------+
| comment : TEXT             |       |    ValidationWorkflow      |
| priority : ENUM           |       +----------------------------+
|   (NORMAL, URGENT)        |       | id : UUID (PK)            |
| due_date : DATE           |       | entity_type : ENUM         |
| metadata : JSONB          |       |   (TIME, LEAVE, EXPENSE,   |
| created_at : TIMESTAMP    |       |    INVOICE)                |
| updated_at : TIMESTAMP    |       | entity_scope : ENUM        |
+----------------------------+       |   (GLOBAL, TEAM, PROJECT)  |
                                     | entity_scope_id : UUID     |
+----------------------------+       | name : VARCHAR(255)        |
|    LeaveRequest            |       | is_active : BOOLEAN        |
+----------------------------+       | created_by : UUID (FK)     |
| id : UUID (PK)            |       | created_at : TIMESTAMP     |
| employee_id : UUID (FK)   |       | updated_at : TIMESTAMP     |
| validation_request_id : FK|       +----------------------------+
| type : ENUM               |              |
|   (CP, RTT, SICK,         |              | 1..*
|    UNPAID, MATERNITY,      |              v
|    PATERNITY, BEREAVEMENT, |       +----------------------------+
|    WEDDING, OTHER)         |       |  WorkflowLevel             |
| start_date : DATE         |       +----------------------------+
| end_date : DATE           |       | id : UUID (PK)            |
| days : DECIMAL(4,1)       |       | workflow_id : UUID (FK)    |
| half_day_start : BOOLEAN  |       | level_order : INTEGER      |
| half_day_end : BOOLEAN    |       | approver_type : ENUM       |
| status : ENUM             |       |   (USER, ROLE, MANAGER,    |
|   (DRAFT, SUBMITTED,      |       |    PROJECT_LEAD)           |
|    APPROVED, REFUSED,      |       | approver_id : UUID         |
|    CANCELLED)              |       | auto_approve : BOOLEAN     |
| comment : TEXT             |       | auto_approve_rules : JSONB |
| attachment_url : VARCHAR   |       | escalation_days : INTEGER  |
| balance_before : DECIMAL   |       +----------------------------+
| created_at : TIMESTAMP    |
| updated_at : TIMESTAMP    |       +----------------------------+
+----------------------------+       |  LeaveBalance              |
                                     +----------------------------+
+----------------------------+       | id : UUID (PK)            |
|  ValidationDelegation      |       | employee_id : UUID (FK)    |
+----------------------------+       | leave_type : ENUM          |
| id : UUID (PK)            |       | year : INTEGER             |
| delegator_id : UUID (FK)  |       | entitled_days : DECIMAL    |
| delegate_id : UUID (FK)   |       | taken_days : DECIMAL       |
| start_date : DATE         |       | pending_days : DECIMAL     |
| end_date : DATE           |       | carried_over : DECIMAL     |
| entity_types : ENUM[]     |       | available : DECIMAL        |
| is_active : BOOLEAN       |       | last_updated : TIMESTAMP   |
| created_at : TIMESTAMP    |       +----------------------------+
+----------------------------+
                                     +----------------------------+
+----------------------------+       |  NotificationPreference    |
|  LeaveType                 |       +----------------------------+
+----------------------------+       | id : UUID (PK)            |
| id : UUID (PK)            |       | user_id : UUID (FK)        |
| code : VARCHAR(20)        |       | channel : ENUM             |
| name : VARCHAR(100)       |       |   (IN_APP, EMAIL)          |
| days_per_year : DECIMAL   |       | entity_type : ENUM         |
| carry_over : BOOLEAN      |       | on_submission : BOOLEAN    |
| carry_over_limit : DECIMAL|       | on_approval : BOOLEAN      |
| requires_attachment : BOOL |       | on_refusal : BOOLEAN       |
| impacts_payroll : BOOLEAN |       | on_reminder : BOOLEAN      |
| is_active : BOOLEAN       |       | digest_frequency : ENUM    |
| color : VARCHAR(7)        |       |   (NONE, DAILY, WEEKLY)    |
| sort_order : INTEGER      |       +----------------------------+
+----------------------------+
```

### 11.2 Description detaillee des entites

#### ValidationRequest

Entite centrale du module. Chaque element soumis pour validation (temps, conge, note de frais, facture) genere un enregistrement `ValidationRequest`.

| Champ | Type | Description |
|---|---|---|
| `id` | UUID | Identifiant unique de la demande de validation |
| `type` | ENUM | Type d'element : `TIME`, `LEAVE`, `EXPENSE`, `INVOICE` |
| `reference_id` | UUID | Identifiant de l'element concerne dans le module source (FK vers Timesheet, LeaveRequest, ExpenseReport, Invoice) |
| `submitted_by` | UUID | Collaborateur ayant soumis l'element (FK vers Employee) |
| `submitted_at` | TIMESTAMP | Date et heure de soumission |
| `status` | ENUM | Statut actuel : `DRAFT`, `SUBMITTED`, `PENDING_APPROVAL`, `APPROVED`, `REFUSED`, `CANCELLED` |
| `current_level` | INTEGER | Niveau actuel dans le workflow (1, 2, 3...) |
| `max_level` | INTEGER | Nombre total de niveaux dans le workflow applicable |
| `validated_by` | UUID | Dernier valideur ayant agi (FK vers Employee) |
| `validated_at` | TIMESTAMP | Date et heure de la derniere action de validation |
| `comment` | TEXT | Commentaire du valideur (obligatoire en cas de refus) |
| `priority` | ENUM | Priorite : `NORMAL`, `URGENT` |
| `due_date` | DATE | Date limite de traitement (calculee selon les regles d'escalade) |
| `metadata` | JSONB | Donnees complementaires specifiques au type (montant, nombre de jours, etc.) |
| `created_at` | TIMESTAMP | Date de creation de l'enregistrement |
| `updated_at` | TIMESTAMP | Date de derniere modification |

#### LeaveRequest

Extension specifique pour les demandes de conge. Liee a une `ValidationRequest` de type `LEAVE`.

| Champ | Type | Description |
|---|---|---|
| `id` | UUID | Identifiant unique de la demande de conge |
| `employee_id` | UUID | Collaborateur concerne (FK vers Employee) |
| `validation_request_id` | UUID | Lien vers la ValidationRequest associee |
| `type` | ENUM | Type de conge : `CP`, `RTT`, `SICK`, `UNPAID`, `MATERNITY`, `PATERNITY`, `BEREAVEMENT`, `WEDDING`, `OTHER` |
| `start_date` | DATE | Date de debut du conge |
| `end_date` | DATE | Date de fin du conge |
| `days` | DECIMAL(4,1) | Nombre de jours ouvrables (calcule automatiquement, supporte les demi-journees) |
| `half_day_start` | BOOLEAN | Vrai si le conge commence l'apres-midi |
| `half_day_end` | BOOLEAN | Vrai si le conge se termine le matin |
| `status` | ENUM | Statut : `DRAFT`, `SUBMITTED`, `APPROVED`, `REFUSED`, `CANCELLED` |
| `comment` | TEXT | Motif ou commentaire du collaborateur |
| `attachment_url` | VARCHAR | URL du justificatif (arret maladie, etc.) |
| `balance_before` | DECIMAL | Solde de conges du type concerne au moment de la demande |

#### ValidationWorkflow

Configuration des workflows de validation. Definit les regles d'approbation pour chaque type d'element.

| Champ | Type | Description |
|---|---|---|
| `id` | UUID | Identifiant unique du workflow |
| `entity_type` | ENUM | Type d'element concerne : `TIME`, `LEAVE`, `EXPENSE`, `INVOICE` |
| `entity_scope` | ENUM | Perimetre d'application : `GLOBAL` (tout le cabinet), `TEAM` (une equipe), `PROJECT` (un projet) |
| `entity_scope_id` | UUID | Identifiant du perimetre (equipe ou projet). NULL si `GLOBAL` |
| `name` | VARCHAR(255) | Nom du workflow (ex: "Validation temps - Equipe Paris") |
| `is_active` | BOOLEAN | Indique si le workflow est actif |

#### WorkflowLevel

Niveaux d'approbation au sein d'un workflow.

| Champ | Type | Description |
|---|---|---|
| `id` | UUID | Identifiant unique du niveau |
| `workflow_id` | UUID | Workflow parent (FK vers ValidationWorkflow) |
| `level_order` | INTEGER | Ordre du niveau dans le workflow (1, 2, 3...) |
| `approver_type` | ENUM | Type de valideur : `USER` (personne specifique), `ROLE` (tous les utilisateurs avec ce role), `MANAGER` (manager hierarchique), `PROJECT_LEAD` (chef du projet concerne) |
| `approver_id` | UUID | Identifiant du valideur ou du role (selon `approver_type`) |
| `auto_approve` | BOOLEAN | Active l'auto-approbation si les regles sont remplies |
| `auto_approve_rules` | JSONB | Regles d'auto-approbation (ex: `{"max_hours": 8, "max_amount": 50}`) |
| `escalation_days` | INTEGER | Nombre de jours avant escalade au niveau superieur |

#### LeaveBalance

Soldes de conges par collaborateur, par type et par annee.

| Champ | Type | Description |
|---|---|---|
| `id` | UUID | Identifiant unique |
| `employee_id` | UUID | Collaborateur concerne (FK vers Employee) |
| `leave_type` | ENUM | Type de conge |
| `year` | INTEGER | Annee de reference |
| `entitled_days` | DECIMAL | Jours acquis pour l'annee (au prorata si entree en cours d'annee) |
| `taken_days` | DECIMAL | Jours pris (conges approuves et passes) |
| `pending_days` | DECIMAL | Jours en attente de validation |
| `carried_over` | DECIMAL | Jours reportes de l'annee precedente |
| `available` | DECIMAL | Solde disponible (calcule : `entitled_days + carried_over - taken_days - pending_days`) |

#### ValidationDelegation

Delegations temporaires de droits de validation.

| Champ | Type | Description |
|---|---|---|
| `id` | UUID | Identifiant unique |
| `delegator_id` | UUID | Valideur original qui delegue ses droits |
| `delegate_id` | UUID | Utilisateur qui recoit les droits de validation |
| `start_date` | DATE | Date de debut de la delegation |
| `end_date` | DATE | Date de fin de la delegation (max 90 jours) |
| `entity_types` | ENUM[] | Types d'elements concernes par la delegation |
| `is_active` | BOOLEAN | Indique si la delegation est active |

### 11.3 Index recommandes

```sql
-- Index pour les requetes frequentes
CREATE INDEX idx_validation_request_status ON validation_request(status);
CREATE INDEX idx_validation_request_type_status ON validation_request(type, status);
CREATE INDEX idx_validation_request_submitted_by ON validation_request(submitted_by);
CREATE INDEX idx_validation_request_validated_by ON validation_request(validated_by);
CREATE INDEX idx_validation_request_submitted_at ON validation_request(submitted_at);

CREATE INDEX idx_leave_request_employee ON leave_request(employee_id);
CREATE INDEX idx_leave_request_dates ON leave_request(start_date, end_date);
CREATE INDEX idx_leave_request_type_status ON leave_request(type, status);

CREATE INDEX idx_leave_balance_employee_type ON leave_balance(employee_id, leave_type, year);

CREATE INDEX idx_validation_history_request ON validation_history(validation_request_id);
CREATE INDEX idx_validation_history_performed_by ON validation_history(performed_by);

CREATE INDEX idx_validation_delegation_delegate ON validation_delegation(delegate_id, is_active);
CREATE INDEX idx_validation_delegation_dates ON validation_delegation(start_date, end_date);

CREATE INDEX idx_workflow_level_workflow ON workflow_level(workflow_id, level_order);
```

---

## 12. Estimation

### 12.1 Synthese

| Parametre | Valeur |
|---|---|
| **Duree totale estimee** | 6 semaines (30 jours ouvrables) |
| **Nombre de sprints** | 3 a 4 sprints de 2 semaines |
| **Effort total estime** | 180 a 220 points de story (echelle Fibonacci) |
| **Equipe recommandee** | 2 developpeurs full-stack, 1 developpeur front-end, 1 QA, 1 designer UI/UX (temps partiel) |

### 12.2 Estimation detaillee par User Story

| User Story | Complexite | Points | Effort (jours/dev) | Sprint |
|---|---|---|---|---|
| **US-V01** : Tableau de bord des validations | Moyenne | 13 | 3-4 j | Sprint 1 |
| **US-V10** : Configuration du workflow | Elevee | 21 | 5-6 j | Sprint 1 |
| **US-V02** : Validation des temps (individuelle) | Moyenne | 13 | 3-4 j | Sprint 1 |
| **US-V03** : Validation en masse des temps | Moyenne | 13 | 3-4 j | Sprint 2 |
| **US-V04** : Demande et validation de conges | Elevee | 21 | 5-6 j | Sprint 2 |
| **US-V05** : Gestion des types de conges et soldes | Elevee | 21 | 5-6 j | Sprint 2 |
| **US-V08** : Refus avec commentaire | Faible | 8 | 2-3 j | Sprint 2 |
| **US-V06** : Validation des notes de frais | Moyenne | 13 | 3-4 j | Sprint 3 |
| **US-V07** : Validation des factures (workflow) | Elevee | 21 | 5-6 j | Sprint 3 |
| **US-V09** : Historique des validations | Moyenne | 13 | 3-4 j | Sprint 3 |
| **US-V11** : Notifications de validation | Elevee | 21 | 5-6 j | Sprint 3-4 |
| **US-V12** : Delegation de validation | Moyenne | 13 | 3-4 j | Sprint 4 |
| **US-V13** : Filtres et recherche avances | Moyenne | 13 | 3-4 j | Sprint 4 |
| **Infrastructure & Socle technique** | Elevee | 21 | 5-6 j | Sprint 1 |
| **Tests d'integration & QA** | - | - | 8-10 j | Transversal |
| **TOTAL** | | **~225** | **~65-75 j/dev** | **4 sprints** |

### 12.3 Repartition par sprint

#### Sprint 1 (Semaines 1-2) : Fondations et temps

| Activite | Effort |
|---|---|
| Mise en place du modele de donnees et des migrations | 2 jours |
| Developpement du moteur de workflow (composant reutilisable) | 3 jours |
| API REST : endpoints de base (CRUD ValidationRequest, workflows) | 2 jours |
| US-V01 : Tableau de bord avec badge compteur | 3 jours |
| US-V10 : Interface de configuration des workflows (version initiale) | 4 jours |
| US-V02 : Validation individuelle des temps | 3 jours |
| Tests unitaires et d'integration Sprint 1 | 3 jours |
| **Total Sprint 1** | **~20 jours/equipe** |

#### Sprint 2 (Semaines 3-4) : Conges et actions en masse

| Activite | Effort |
|---|---|
| US-V03 : Validation en masse des temps | 3 jours |
| US-V04 : Demande et validation de conges (avec calendrier d'equipe) | 5 jours |
| US-V05 : Gestion des types de conges et soldes | 5 jours |
| US-V08 : Refus avec commentaire et circuit de correction | 2 jours |
| Integration avec EPIC-005 (Temps) et EPIC-009 (Collaborateurs) | 2 jours |
| Tests unitaires et d'integration Sprint 2 | 3 jours |
| **Total Sprint 2** | **~20 jours/equipe** |

#### Sprint 3 (Semaines 4-5) : Notes de frais, factures et historique

| Activite | Effort |
|---|---|
| US-V06 : Validation des notes de frais (avec apercu justificatifs) | 4 jours |
| US-V07 : Validation des factures avec workflow multi-niveaux | 5 jours |
| US-V09 : Historique des validations (avec export) | 3 jours |
| US-V11 : Systeme de notifications (in-app et email) | 5 jours |
| Integration avec EPIC-004 (Facturation) et EPIC-013 (Notes de frais) | 2 jours |
| Tests unitaires et d'integration Sprint 3 | 3 jours |
| **Total Sprint 3** | **~22 jours/equipe** |

#### Sprint 4 (Semaine 6) : Finalisation et polish

| Activite | Effort |
|---|---|
| US-V12 : Delegation de validation | 3 jours |
| US-V13 : Filtres et recherche avances | 3 jours |
| Amelioration US-V10 : Configuration avancee des workflows | 2 jours |
| Tests end-to-end complets | 3 jours |
| Corrections de bugs et ajustements UI/UX | 2 jours |
| Documentation technique et utilisateur | 1 jour |
| Revue de securite et performance | 1 jour |
| **Total Sprint 4** | **~15 jours/equipe** |

### 12.4 Risques et mitigations

| Risque | Probabilite | Impact | Mitigation |
|---|---|---|---|
| Complexite du moteur de workflow sous-estimee | Moyenne | Fort | Prevoir un spike technique en amont du Sprint 1. Utiliser une librairie existante si possible. |
| Integrations avec les modules existants plus complexes que prevu | Moyenne | Moyen | Definir les contrats d'API avec les equipes des modules lies avant le demarrage. |
| Performance du tableau de bord avec un grand volume d'elements | Faible | Moyen | Pagination, indexation base de donnees, cache applicatif. Tests de charge des le Sprint 2. |
| Gestion des cas limites dans les calculs de soldes de conges | Moyenne | Faible | Collaboration etroite avec le metier pour documenter tous les cas (temps partiel, entree/sortie en cours d'annee, etc.). |
| Retard lie aux dependances avec les autres EPICs | Moyenne | Fort | Utiliser des mocks et des contrats d'interface pour developper en parallele. |

### 12.5 Hypotheses

- L'equipe est composee de developpeurs familiers avec la stack technique de OOTI.
- Les modules dependants (EPIC-004, EPIC-005, EPIC-009, EPIC-013) exposent des API stables ou des contrats d'interface sont definis.
- Le design system de l'application est etabli et les composants de base (tableaux, formulaires, modales, notifications) sont disponibles.
- L'infrastructure de notifications (WebSocket ou equivalent) est en place ou son developpement est coordonne.
- Les regles metier decrites dans la section 7 sont validees par les parties prenantes avant le demarrage du Sprint 1.

---

*Document redige le 26/02/2026 -- EPIC-012 Validation & Approbations -- Application OOTI v1.0*
