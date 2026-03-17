# EPIC — Module Notifications

**Application OOTI** — Gestion de projets pour cabinets d'architecture
**Version 1.0** — Fevrier 2026

---

## 1. Identification

| Champ | Valeur |
|---|---|
| **Nom** | Notifications |
| **Reference** | EPIC-017 |
| **Module parent** | Transversal |
| **Priorite** | Basse |
| **Responsable produit** | Chef de produit OOTI |
| **Date de creation** | 26/02/2026 |
| **Version du document** | 1.0 |
| **Statut** | Brouillon |

### EPICs lies

| EPIC | Nom | Nature de la dependance |
|---|---|---|
| EPIC-004 | Facturation | Notifications de factures (en attente, envoyees, paiements, retards) |
| EPIC-005 | Temps | Notifications de saisie de temps (rappels, validation, refus) |
| EPIC-012 | Validation | Notifications de workflows de validation (conges, notes de frais, temps) |
| EPIC-015 | Collaboration | Notifications de commentaires, fichiers partages, mentions |
| EPIC-016 | Configuration | Parametrage des preferences de notifications utilisateur |

---

## 2. Contexte et Problematique

### Contexte

Dans un cabinet d'architecture, les equipes travaillent de maniere transversale sur de multiples projets simultanement. Les collaborateurs doivent suivre un grand nombre d'evenements : validation de leurs feuilles de temps, approbation de conges, avancements de projets, echéances de facturation, nouvelles taches assignees, commentaires sur des livrables, etc. Sans un systeme de notifications centralise, les utilisateurs sont contraints de verifier manuellement chaque module de l'application pour detecter les changements qui les concernent.

### Problematique

Les cabinets d'architecture font face a plusieurs defis lies a la communication interne et au suivi des evenements :

- **Perte d'information** : les collaborateurs ne sont pas informes en temps reel des evenements qui les concernent (validation de temps, approbation de conges, nouvelles taches). Cela genere des retards dans les processus de travail et des oublis frequents.
- **Saisie de temps incomplete** : sans rappels automatises, les collaborateurs oublient de saisir leurs temps, ce qui impacte directement la facturation et la rentabilite des projets.
- **Delais de validation** : les responsables ne sont pas alertes lorsqu'une demande de validation (conges, notes de frais, feuilles de temps) est en attente, ce qui ralentit les processus d'approbation et frustre les demandeurs.
- **Suivi de facturation defaillant** : les gestionnaires ne sont pas notifies des factures en retard de paiement, des factures en attente d'envoi ou des paiements recus, ce qui nuit a la tresorerie du cabinet.
- **Manque de visibilite sur les projets** : les chefs de projet ne sont pas alertes des jalons proches, des taches en retard ou des phases terminees, ce qui complique le pilotage operationnel.
- **Communication fragmentee** : les mentions, commentaires et partages de fichiers ne generent pas de notification, obligeant les utilisateurs a consulter manuellement les espaces de collaboration.
- **Surcharge informationnelle** : a l'inverse, un systeme de notifications non configurable genere un bruit excessif qui conduit les utilisateurs a ignorer l'ensemble des alertes, y compris les plus critiques.

### Enjeux

Le module Notifications doit repondre a un double enjeu :

1. **Reactivite** : garantir que chaque utilisateur est informe en temps reel des evenements qui le concernent, via le canal le plus adapte (in-app, email).
2. **Pertinence** : permettre a chaque utilisateur de configurer finement ses preferences pour ne recevoir que les notifications utiles, en evitant la surcharge informationnelle.

---

## 3. Objectif

### Objectif principal

Mettre en place un systeme de notifications centralise, configurable et temps reel, permettant a chaque utilisateur de l'application OOTI d'etre informe des evenements pertinents a travers deux canaux de diffusion (in-app et email), avec la possibilite de personnaliser finement ses preferences par type de notification et par canal.

### Objectifs specifiques

| # | Objectif | Indicateur de succes |
|---|---|---|
| O1 | Centraliser l'ensemble des notifications dans un centre unique accessible via l'icone cloche | 100% des types de notifications affiches dans le centre de notifications |
| O2 | Informer les utilisateurs en temps reel des evenements qui les concernent | Delai de reception d'une notification in-app < 3 secondes apres l'evenement declencheur |
| O3 | Proposer des notifications par email pour les evenements critiques | Taux de delivrabilite des emails de notification > 98% |
| O4 | Permettre a chaque utilisateur de configurer ses preferences de notification | 100% des types de notifications configurables par canal (in-app, email) |
| O5 | Reduire les oublis de saisie de temps grace aux rappels automatiques | Augmentation du taux de completion des feuilles de temps de 20% |
| O6 | Accelerer les processus de validation grace aux alertes temps reel | Reduction du delai moyen de validation de 30% |
| O7 | Ameliorer le suivi de facturation grace aux notifications d'echeance | Reduction des factures en retard de paiement de 15% |
| O8 | Permettre aux administrateurs de communiquer efficacement avec l'ensemble des utilisateurs | Capacite d'envoi de notifications en masse a tous les utilisateurs ou a des groupes cibles |

---

## 4. Perimetre Fonctionnel

### 4.1 Centre de notifications in-app

- Icone cloche dans la barre de navigation principale (header) avec badge compteur indiquant le nombre de notifications non lues
- Panneau deroulant affichant la liste des notifications recentes au clic sur l'icone cloche
- Page dediee « Notifications » accessible via la section COLLABORATION > Notifications
- Affichage des notifications par ordre anti-chronologique (plus recentes en haut)
- Distinction visuelle entre notifications lues et non lues (mise en surbrillance, indicateur de point)
- Chargement pagine des notifications (scroll infini ou pagination)

### 4.2 Types de notifications

#### Temps (EPIC-005)
- Rappel de saisie de temps (quotidien/hebdomadaire, configurable)
- Temps valide par le responsable
- Temps refuse par le responsable (avec motif)
- Feuille de temps soumise pour validation (pour le valideur)

#### Conges (EPIC-012)
- Demande de conge soumise (pour le valideur)
- Conge approuve (pour le demandeur)
- Conge refuse (pour le demandeur, avec motif)
- Rappel de demande de conge en attente (pour le valideur)

#### Notes de frais (EPIC-012)
- Note de frais soumise pour validation (pour le valideur)
- Note de frais validee (pour le demandeur)
- Note de frais refusee (pour le demandeur, avec motif)

#### Facturation (EPIC-004)
- Facture en attente de validation
- Facture envoyee au client
- Paiement recu sur une facture
- Facture en retard de paiement (avec nombre de jours de retard)
- Avoir emis

#### Projets
- Nouveau projet assigne
- Jalon proche (alerte configurable : 7 jours, 3 jours, 1 jour avant)
- Phase terminee
- Budget de projet depasse ou proche du seuil d'alerte
- Changement de statut d'un projet

#### Taches
- Tache assignee
- Tache en retard (date d'echeance depassee)
- Tache terminee (pour le responsable du projet)
- Changement de priorite d'une tache

#### Collaboration (EPIC-015)
- Nouveau commentaire sur un element (projet, tache, facture)
- Fichier partage dans un espace de projet
- Mention (@utilisateur) dans un commentaire
- Reponse a un commentaire de l'utilisateur

#### Systeme
- Mise a jour de l'application
- Maintenance planifiee
- Annonces administrateur (notifications en masse)
- Modification des droits/roles de l'utilisateur

### 4.3 Canaux de diffusion

| Canal | Description | Temps reel | Configurable |
|---|---|---|---|
| In-app | Notification affichee dans le centre de notifications de l'application | Oui (WebSocket/SSE) | Oui, par type |
| Email | Email envoye a l'adresse de l'utilisateur | Non (quasi temps reel, delai possible) | Oui, par type |

### 4.4 Preferences de notifications

- Page de configuration accessible via Parametres > Profil > Notifications
- Matrice de configuration : type de notification x canal (in-app, email)
- Activation/desactivation par type et par canal
- Frequence des rappels configurable (quotidien, hebdomadaire) pour les rappels de saisie de temps
- Option « Ne pas deranger » avec plages horaires
- Desactivation globale par canal (ex : desactiver tous les emails)
- Preferences par defaut definies par l'administrateur (EPIC-016)

### 4.5 Actions sur les notifications

- Marquage lu/non lu (individuel)
- Marquage « tout lu » (marquer toutes les notifications comme lues)
- Suppression d'une notification
- Suppression en masse (toutes les notifications lues)
- Filtrage par type de notification
- Filtrage par date (aujourd'hui, cette semaine, ce mois, personnalise)
- Filtrage par statut (lues, non lues, toutes)

### 4.6 Navigation contextuelle

- Clic sur une notification : redirection vers l'element concerne (projet, tache, facture, feuille de temps, demande de conge, etc.)
- Marquage automatique comme lu lors du clic
- Ouverture dans le contexte correct (bon onglet, bonne section)

### 4.7 Notifications administrateur en masse

- Interface d'envoi de notification en masse (COLLABORATION > Notifications ou Administration)
- Selection des destinataires : tous les utilisateurs, par equipe, par role, par bureau
- Redaction du titre et du message
- Choix des canaux de diffusion (in-app, email, ou les deux)
- Planification de l'envoi (immediat ou differe)
- Historique des notifications en masse envoyees

---

## 5. User Stories

### US-N01 : Centre de notifications in-app

**En tant que** utilisateur de l'application OOTI,
**Je veux** acceder a un centre de notifications centralise via une icone cloche dans la barre de navigation,
**Afin de** consulter rapidement l'ensemble des evenements et alertes qui me concernent sans avoir a naviguer dans chaque module de l'application.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---|---|
| C01 | Une icone cloche est affichee en permanence dans la barre de navigation principale (header), visible sur toutes les pages de l'application | Visuel : l'icone est presente et reconnaissable (forme de cloche standard) |
| C02 | Au clic sur l'icone cloche, un panneau deroulant s'affiche avec la liste des 20 dernieres notifications, triees par ordre anti-chronologique | Fonctionnel : le panneau s'ouvre immediatement, les notifications sont dans le bon ordre |
| C03 | Chaque notification dans le panneau affiche : icone de type, titre, message resume (max 100 caracteres), date/heure relative (ex : « il y a 5 min ») | Visuel : toutes les informations sont presentes et lisibles |
| C04 | Un lien « Voir toutes les notifications » en bas du panneau redirige vers la page complete COLLABORATION > Notifications | Fonctionnel : la redirection fonctionne correctement |
| C05 | La page complete COLLABORATION > Notifications affiche l'ensemble des notifications avec pagination (20 par page) ou scroll infini | Fonctionnel : le chargement pagine fonctionne sans erreur |
| C06 | Les notifications non lues sont visuellement distinguees des notifications lues (fond de couleur differente, indicateur de point colore) | Visuel : la distinction est claire et immediate |
| C07 | Le panneau de notifications se ferme automatiquement lorsque l'utilisateur clique en dehors de celui-ci | Fonctionnel : le panneau se ferme correctement |
| C08 | Le centre de notifications est accessible et fonctionnel sur les ecrans de taille tablette et superieure (responsive design) | Fonctionnel : test sur les resolutions 768px, 1024px, 1440px |

---

### US-N02 : Badge compteur de notifications non lues

**En tant que** utilisateur de l'application OOTI,
**Je veux** voir un badge numerique sur l'icone cloche indiquant le nombre de notifications non lues,
**Afin de** savoir immediatement si de nouveaux evenements requierent mon attention sans avoir a ouvrir le panneau de notifications.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---|---|
| C01 | Un badge circulaire de couleur rouge est affiche sur l'icone cloche lorsqu'il y a au moins une notification non lue | Visuel : le badge est visible et positionne en haut a droite de l'icone |
| C02 | Le badge affiche le nombre exact de notifications non lues pour les valeurs de 1 a 99 | Fonctionnel : le compteur correspond au nombre reel de notifications non lues |
| C03 | Pour les valeurs superieures a 99, le badge affiche « 99+ » | Fonctionnel : verification avec 100+ notifications non lues |
| C04 | Le badge disparait lorsque toutes les notifications sont marquees comme lues | Fonctionnel : apres marquage global « tout lu », le badge n'est plus visible |
| C05 | Le compteur se met a jour en temps reel lorsqu'une nouvelle notification arrive (sans rechargement de page) | Fonctionnel : envoi d'une notification depuis un autre contexte, le compteur s'incremente en moins de 3 secondes |
| C06 | Le compteur se decremente en temps reel lorsqu'une notification est marquee comme lue | Fonctionnel : clic sur une notification, le compteur decremente immediatement |
| C07 | Le badge est visible et lisible quelle que soit la taille de l'ecran (responsive) | Visuel : test sur differentes resolutions |

---

### US-N03 : Notifications par email

**En tant que** utilisateur de l'application OOTI,
**Je veux** recevoir des notifications par email pour les evenements importants,
**Afin de** etre informe meme lorsque je ne suis pas connecte a l'application et pouvoir reagir rapidement aux evenements critiques.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---|---|
| C01 | Les emails de notification sont envoyes a l'adresse email du profil utilisateur pour chaque type de notification ou le canal email est active | Fonctionnel : reception de l'email dans la boite de reception |
| C02 | Chaque email contient : le nom de l'application (OOTI) en expediteur, un objet clair et descriptif, le detail de la notification, un bouton/lien « Voir dans OOTI » qui redirige vers l'element concerne | Visuel/Fonctionnel : verification du contenu et du lien de redirection |
| C03 | Les emails utilisent un template HTML responsive, coherent avec la charte graphique de l'application | Visuel : test de rendu sur Gmail, Outlook, Apple Mail |
| C04 | Les emails de notification ne sont pas envoyes pour les types de notification ou le canal email est desactive dans les preferences de l'utilisateur | Fonctionnel : desactivation d'un type en email, verification de non-reception |
| C05 | Un lien de desabonnement rapide est present en bas de chaque email de notification, permettant de desactiver le type de notification correspondant | Fonctionnel : clic sur le lien, verification de la mise a jour des preferences |
| C06 | Les emails de rappel de saisie de temps respectent la frequence configuree par l'utilisateur (quotidien ou hebdomadaire) | Fonctionnel : verification de la frequence d'envoi |
| C07 | Les emails sont envoyes dans la langue de l'interface utilisateur (francais ou anglais selon le profil) | Fonctionnel : verification du contenu dans la bonne langue |
| C08 | Le systeme gere les echecs d'envoi d'email (adresse invalide, boite pleine) avec un mecanisme de retry (3 tentatives) et une journalisation des erreurs | Technique : simulation d'echec, verification du retry et des logs |

---

### US-N04 : Preferences de notifications utilisateur

**En tant que** utilisateur de l'application OOTI,
**Je veux** configurer mes preferences de notifications par type et par canal de diffusion,
**Afin de** ne recevoir que les notifications pertinentes pour mon role et mes besoins, et eviter la surcharge informationnelle.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---|---|
| C01 | Une page « Preferences de notifications » est accessible via Parametres > Profil > Notifications | Fonctionnel : navigation vers la page |
| C02 | La page affiche une matrice de configuration avec en lignes les types de notifications (regroupes par categorie : Temps, Conges, Notes de frais, Facturation, Projets, Taches, Collaboration, Systeme) et en colonnes les canaux (In-app, Email) | Visuel : la matrice est complete et lisible |
| C03 | Chaque cellule de la matrice contient un interrupteur (toggle) permettant d'activer ou de desactiver le type de notification pour le canal concerne | Fonctionnel : les toggles sont cliquables et changent d'etat |
| C04 | Les modifications sont sauvegardees automatiquement (auto-save) avec une confirmation visuelle (ex : « Preferences mises a jour ») | Fonctionnel : modification d'un toggle, verification de la sauvegarde et de la confirmation |
| C05 | Des boutons « Tout activer » et « Tout desactiver » sont disponibles pour chaque canal (colonne) | Fonctionnel : clic sur « Tout activer email », verification que tous les toggles email sont actives |
| C06 | L'administrateur peut definir des preferences par defaut pour les nouveaux utilisateurs via EPIC-016 Configuration | Fonctionnel : creation d'un nouvel utilisateur, verification que les preferences par defaut sont appliquees |
| C07 | Certaines notifications systeme critiques (maintenance, modification des droits) ne peuvent pas etre desactivees pour le canal in-app | Fonctionnel : verification que les toggles in-app des notifications systeme critiques sont desactives (grises) |
| C08 | La frequence des rappels de saisie de temps est configurable : quotidien (avec heure configurable) ou hebdomadaire (avec jour et heure configurables) | Fonctionnel : configuration de la frequence, verification de l'envoi aux horaires configures |

---

### US-N05 : Notifications de validation (temps, conges, notes de frais)

**En tant que** collaborateur ou responsable dans un cabinet d'architecture,
**Je veux** recevoir des notifications automatiques lors des evenements de validation (soumission, approbation, refus) pour les feuilles de temps, les conges et les notes de frais,
**Afin de** etre immediatement informe de l'avancement des processus de validation et pouvoir reagir rapidement.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---|---|
| C01 | Lorsqu'un collaborateur soumet sa feuille de temps pour validation, le(s) valideur(s) designe(s) recoivent une notification in-app et/ou email (selon preferences) avec le nom du collaborateur, la periode concernee et le nombre d'heures | Fonctionnel : soumission d'une feuille de temps, verification de reception par le valideur |
| C02 | Lorsqu'un valideur approuve une feuille de temps, le collaborateur recoit une notification de confirmation avec la periode concernee | Fonctionnel : validation d'une feuille de temps, verification de reception par le collaborateur |
| C03 | Lorsqu'un valideur refuse une feuille de temps, le collaborateur recoit une notification avec le motif de refus et un lien vers la feuille de temps a corriger | Fonctionnel : refus d'une feuille de temps avec motif, verification du contenu de la notification |
| C04 | Lorsqu'un collaborateur soumet une demande de conge, le(s) valideur(s) recoivent une notification avec le type de conge, les dates et la duree | Fonctionnel : soumission d'une demande de conge, verification de reception par le valideur |
| C05 | Lorsqu'une demande de conge est approuvee ou refusee, le collaborateur recoit une notification avec le resultat et le motif en cas de refus | Fonctionnel : approbation et refus de conge, verification des deux scenarios |
| C06 | Lorsqu'une note de frais est soumise, le valideur recoit une notification avec le montant total et le nombre de lignes de depense | Fonctionnel : soumission d'une note de frais, verification de reception par le valideur |
| C07 | Lorsqu'une note de frais est validee ou refusee, le collaborateur recoit une notification avec le resultat, le montant et le motif en cas de refus | Fonctionnel : validation et refus de note de frais, verification des deux scenarios |
| C08 | Un rappel automatique est envoye au valideur si une demande de validation (temps, conge, note de frais) est en attente depuis plus de 48 heures (configurable) | Fonctionnel : creation d'une demande, attente de 48h, verification de l'envoi du rappel |

---

### US-N06 : Notifications de facturation

**En tant que** gestionnaire ou administrateur du cabinet d'architecture,
**Je veux** recevoir des notifications relatives aux evenements de facturation (factures en attente, envoyees, paiements recus, retards),
**Afin de** assurer un suivi rigoureux de la facturation et maintenir une tresorerie saine pour le cabinet.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---|---|
| C01 | Lorsqu'une facture est creee et mise en attente de validation, les valideurs de facturation recoivent une notification avec le numero de facture, le client, le montant HT et TTC | Fonctionnel : creation d'une facture en attente, verification de reception par le valideur |
| C02 | Lorsqu'une facture est envoyee au client, le createur et les gestionnaires du projet recoivent une notification de confirmation avec le numero de facture et le client | Fonctionnel : envoi d'une facture, verification de reception |
| C03 | Lorsqu'un paiement est enregistre sur une facture, les gestionnaires de facturation recoivent une notification avec le numero de facture, le montant paye et le solde restant | Fonctionnel : enregistrement d'un paiement, verification de la notification |
| C04 | Lorsqu'une facture depasse son echeance de paiement, une notification d'alerte est envoyee aux gestionnaires de facturation avec le nombre de jours de retard, le montant du et le nom du client | Fonctionnel : creation d'une facture avec echeance depassee, verification de la notification |
| C05 | Les notifications de facture en retard sont renvoyees a intervalles reguliers (configurable : 7, 14, 30 jours de retard) avec le nombre de jours de retard mis a jour | Fonctionnel : verification des notifications de relance a J+7, J+14, J+30 |
| C06 | Lorsqu'un avoir est emis, les gestionnaires de facturation et le createur de la facture d'origine recoivent une notification avec le numero d'avoir, la facture d'origine et le montant | Fonctionnel : emission d'un avoir, verification de reception |
| C07 | Les notifications de facturation incluent un lien direct vers la facture ou l'avoir concerne dans le module Facturation (EPIC-004) | Fonctionnel : clic sur la notification, verification de la redirection vers le bon document |

---

### US-N07 : Notifications de projets et taches

**En tant que** chef de projet ou collaborateur assigne a un projet,
**Je veux** recevoir des notifications automatiques lors des evenements de projet (assignation, jalons, phases) et de taches (assignation, retard, completion),
**Afin de** suivre l'avancement des projets et reagir proactivement aux echeances et aux retards.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---|---|
| C01 | Lorsqu'un utilisateur est assigne a un nouveau projet, il recoit une notification avec le nom du projet, le client, le chef de projet et la date de debut | Fonctionnel : assignation d'un collaborateur a un projet, verification de la notification |
| C02 | Lorsqu'un jalon de projet approche (7 jours, 3 jours, 1 jour avant selon la configuration), le chef de projet et les collaborateurs assignes recoivent une notification d'alerte avec le nom du jalon, la date d'echeance et le nombre de jours restants | Fonctionnel : creation d'un jalon a J+3, verification de la notification 3 jours avant |
| C03 | Lorsqu'une phase de projet est marquee comme terminee, le chef de projet et les gestionnaires recoivent une notification avec le nom de la phase et le pourcentage d'avancement du projet | Fonctionnel : completion d'une phase, verification de la notification |
| C04 | Lorsqu'une tache est assignee a un collaborateur, celui-ci recoit une notification avec le nom de la tache, le projet associe, la priorite et la date d'echeance | Fonctionnel : assignation d'une tache, verification de la notification avec toutes les informations |
| C05 | Lorsqu'une tache depasse sa date d'echeance, le responsable de la tache et le chef de projet recoivent une notification d'alerte avec le nom de la tache, le nombre de jours de retard et le projet associe | Fonctionnel : creation d'une tache avec echeance depassee, verification de la notification |
| C06 | Lorsqu'une tache est marquee comme terminee, le chef de projet recoit une notification avec le nom de la tache, le collaborateur qui l'a completee et la date de completion | Fonctionnel : completion d'une tache, verification de la notification au chef de projet |
| C07 | Les notifications de projet et de tache incluent un lien direct vers le projet ou la tache concerne | Fonctionnel : clic sur la notification, verification de la redirection |
| C08 | Lorsque le budget d'un projet depasse un seuil d'alerte (80% par defaut, configurable), le chef de projet et le directeur financier recoivent une notification d'alerte avec le pourcentage consomme et le montant restant | Fonctionnel : depassement du seuil de budget, verification de la notification |

---

### US-N08 : Marquage lu/non lu et suppression

**En tant que** utilisateur de l'application OOTI,
**Je veux** pouvoir marquer mes notifications comme lues ou non lues, et supprimer celles qui ne sont plus pertinentes,
**Afin de** gerer efficacement mon centre de notifications et me concentrer sur les evenements qui requierent encore mon attention.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---|---|
| C01 | Un bouton ou une icone permet de marquer individuellement une notification comme lue ou non lue depuis le panneau deroulant et la page complete | Fonctionnel : clic sur le bouton, verification du changement de statut visuel |
| C02 | Un bouton « Tout marquer comme lu » est disponible en haut de la liste des notifications et marque l'ensemble des notifications non lues comme lues en une seule action | Fonctionnel : clic sur le bouton, verification que toutes les notifications passent a l'etat lu et que le badge compteur est remis a zero |
| C03 | Un bouton ou une icone permet de supprimer individuellement une notification depuis le panneau deroulant ou la page complete | Fonctionnel : clic sur supprimer, verification de la disparition de la notification |
| C04 | Une confirmation est demandee avant la suppression en masse (« Supprimer toutes les notifications lues ? ») | Fonctionnel : clic sur suppression en masse, verification de la modale de confirmation |
| C05 | Un bouton « Supprimer toutes les notifications lues » est disponible et supprime uniquement les notifications marquees comme lues | Fonctionnel : suppression en masse, verification que seules les notifications lues sont supprimees |
| C06 | Les actions de marquage et de suppression sont accessibles via un menu contextuel (clic droit ou icone « ... ») sur chaque notification | Fonctionnel : clic droit ou clic sur l'icone, verification de l'affichage du menu |
| C07 | Les suppressions sont definitives et les notifications supprimees ne peuvent pas etre recuperees (pas de corbeille) | Fonctionnel : suppression, verification que la notification n'est plus accessible |

---

### US-N09 : Lien direct vers l'element concerne

**En tant que** utilisateur de l'application OOTI,
**Je veux** pouvoir cliquer sur une notification pour etre redirige directement vers l'element concerne (projet, tache, facture, feuille de temps, etc.),
**Afin de** acceder immediatement au contexte de la notification et pouvoir agir sans avoir a naviguer manuellement dans l'application.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---|---|
| C01 | Chaque notification contient un lien interne vers l'element concerne (reference_type et reference_id) | Technique : verification de la presence du lien dans les donnees de la notification |
| C02 | Le clic sur une notification dans le panneau deroulant redirige l'utilisateur vers la page de detail de l'element concerne (projet, tache, facture, feuille de temps, demande de conge, note de frais, commentaire) | Fonctionnel : clic sur chaque type de notification, verification de la redirection correcte |
| C03 | La notification est automatiquement marquee comme lue lors du clic (avant ou au moment de la redirection) | Fonctionnel : clic sur une notification non lue, verification du changement de statut |
| C04 | Si l'element reference a ete supprime ou n'est plus accessible, un message d'erreur explicite est affiche (ex : « Cet element n'est plus disponible ») au lieu d'une page d'erreur 404 | Fonctionnel : suppression d'un element reference, clic sur la notification, verification du message |
| C05 | Le lien dans les emails de notification (bouton « Voir dans OOTI ») redirige vers la page de detail de l'element concerne apres authentification si necessaire | Fonctionnel : clic sur le lien email, verification de la redirection (avec et sans session active) |
| C06 | La redirection s'effectue dans le bon contexte de navigation : le bon onglet, la bonne section, le bon element est affiche et mis en evidence | Fonctionnel : verification que l'utilisateur arrive sur la bonne page avec le bon element visible |

---

### US-N10 : Notifications administrateur en masse

**En tant que** administrateur de l'application OOTI,
**Je veux** pouvoir envoyer des notifications en masse a l'ensemble des utilisateurs ou a des groupes specifiques,
**Afin de** communiquer efficacement les annonces importantes, les changements organisationnels ou les informations relatives a la vie du cabinet.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---|---|
| C01 | Une interface d'envoi de notification en masse est accessible dans la section Administration ou COLLABORATION > Notifications (onglet « Envoi en masse ») et reservee aux utilisateurs ayant le role administrateur | Fonctionnel : verification de l'acces pour un admin et du blocage pour un non-admin |
| C02 | L'interface permet de saisir un titre (max 150 caracteres) et un message (max 2000 caracteres, avec mise en forme basique : gras, italique, liens) | Fonctionnel : saisie d'un titre et d'un message avec mise en forme |
| C03 | L'administrateur peut selectionner les destinataires : tous les utilisateurs, par equipe/departement, par role, par bureau/agence | Fonctionnel : selection de chaque type de filtre, verification de la liste de destinataires |
| C04 | L'administrateur peut choisir les canaux de diffusion : in-app uniquement, email uniquement, ou les deux | Fonctionnel : selection de chaque combinaison de canaux |
| C05 | L'administrateur peut planifier l'envoi : immediat ou differe (date et heure specifiees) | Fonctionnel : planification d'un envoi differe, verification de l'envoi a l'heure prevue |
| C06 | Une previsualisation du message est disponible avant l'envoi, affichant le rendu in-app et le rendu email | Fonctionnel : clic sur « Previsualiser », verification du rendu sur les deux canaux |
| C07 | Un historique des notifications en masse envoyees est disponible avec la date d'envoi, l'expediteur, le nombre de destinataires et le statut (envoyee, planifiee, en cours) | Fonctionnel : envoi de plusieurs notifications, verification de l'historique |
| C08 | Les notifications en masse ne peuvent pas etre desactivees dans les preferences utilisateur (canal in-app obligatoire pour les annonces administrateur) | Fonctionnel : verification que les preferences utilisateur ne permettent pas de bloquer les annonces admin in-app |

---

## 6. Hors Perimetre

Les elements suivants sont explicitement exclus du perimetre de l'EPIC-017 et pourront faire l'objet d'evolutions futures :

| # | Element exclu | Justification |
|---|---|---|
| HP01 | Notifications push mobile (PWA/app native) | Necessite une application mobile dediee ou une PWA avec support des notifications push, hors perimetre de la V1 |
| HP02 | Notifications SMS | Cout eleve par envoi, complexite d'integration avec les operateurs telephoniques, faible valeur ajoutee par rapport a l'email |
| HP03 | Notifications Slack/Teams/integrations tierces | Integration avec des outils tiers a traiter dans un EPIC dedie (integrations) |
| HP04 | Chatbot ou assistant conversationnel pour les notifications | Fonctionnalite avancee, hors perimetre V1 |
| HP05 | Regles de notification personnalisees par l'utilisateur (ex : « me notifier si le budget depasse X euros ») | Complexite elevee, a traiter dans une version ulterieure |
| HP06 | Digest (resume periodique des notifications) | Synthese quotidienne ou hebdomadaire des notifications, a envisager en V2 |
| HP07 | Notifications sonores | Accessibilite et preferences utilisateur, a evaluer en V2 |
| HP08 | Traduction automatique des notifications | Les notifications sont fournies dans la langue de l'interface de l'utilisateur (francais ou anglais), pas de traduction automatique supplementaire |
| HP09 | Archivage des notifications | Les notifications supprimees ne sont pas archivees, pas de systeme de corbeille |

---

## 7. Regles Metier

### RM-N01 : Generation des notifications

| Regle | Description |
|---|---|
| RM-N01.1 | Une notification est generee automatiquement par le systeme lors de chaque evenement declencheur defini dans le perimetre fonctionnel (section 4.2) |
| RM-N01.2 | L'utilisateur a l'origine de l'action ne recoit pas de notification pour sa propre action (ex : un valideur qui approuve une feuille de temps ne recoit pas de notification d'approbation) |
| RM-N01.3 | Les notifications sont generees uniquement si le canal correspondant est active dans les preferences de l'utilisateur destinataire, sauf pour les notifications systeme critiques (maintenance, modification des droits) |
| RM-N01.4 | Un evenement unique ne peut generer qu'une seule notification par utilisateur et par canal (pas de doublons) |

### RM-N02 : Diffusion des notifications

| Regle | Description |
|---|---|
| RM-N02.1 | Les notifications in-app sont diffusees en temps reel via WebSocket ou Server-Sent Events (SSE), avec un delai maximal de 3 secondes entre l'evenement declencheur et la reception par l'utilisateur |
| RM-N02.2 | Les notifications email sont envoyees de maniere asynchrone via une file d'attente (queue) pour ne pas bloquer les processus metier. Le delai maximal d'envoi est de 5 minutes apres l'evenement declencheur |
| RM-N02.3 | En cas d'echec d'envoi d'email, le systeme effectue jusqu'a 3 tentatives avec un intervalle de 5 minutes entre chaque tentative. Apres 3 echecs, l'erreur est journalisee et aucune autre tentative n'est effectuee |
| RM-N02.4 | Les notifications en masse (administrateur) sont envoyees de maniere progressive (batch) pour eviter la surcharge du systeme d'envoi d'emails (maximum 100 emails par minute) |

### RM-N03 : Rappels de saisie de temps

| Regle | Description |
|---|---|
| RM-N03.1 | Les rappels quotidiens de saisie de temps sont envoyes a l'heure configuree par l'utilisateur (defaut : 17h00, fuseau horaire de l'utilisateur) uniquement les jours ouvrables (lundi au vendredi, hors jours feries) |
| RM-N03.2 | Les rappels hebdomadaires de saisie de temps sont envoyes le jour et a l'heure configures par l'utilisateur (defaut : vendredi 16h00) |
| RM-N03.3 | Un rappel de saisie de temps n'est pas envoye si l'utilisateur a deja saisi la totalite de ses heures pour la periode concernee |
| RM-N03.4 | Un rappel de saisie de temps n'est pas envoye si l'utilisateur est en conge approuve pour la journee entiere |

### RM-N04 : Notifications de retard

| Regle | Description |
|---|---|
| RM-N04.1 | Les notifications de facture en retard sont envoyees automatiquement a J+1, J+7, J+14 et J+30 apres la date d'echeance de paiement (intervalles configurables par l'administrateur) |
| RM-N04.2 | Les notifications de tache en retard sont envoyees a J+1 apres la date d'echeance, puis tous les 3 jours tant que la tache n'est pas completee (maximum 5 rappels) |
| RM-N04.3 | Les notifications de jalon proche sont envoyees a J-7, J-3 et J-1 avant la date du jalon (intervalles configurables) |
| RM-N04.4 | Les rappels de demande de validation en attente sont envoyes toutes les 48 heures (configurable) tant que la demande n'a pas ete traitee, avec un maximum de 5 rappels |

### RM-N05 : Conservation et nettoyage

| Regle | Description |
|---|---|
| RM-N05.1 | Les notifications in-app sont conservees pendant 90 jours apres leur creation. Au-dela, elles sont automatiquement supprimees par un processus de nettoyage nocturne |
| RM-N05.2 | Les notifications supprimees manuellement par l'utilisateur sont immediatement et definitivement supprimees (pas d'archivage, pas de corbeille) |
| RM-N05.3 | Les logs d'envoi d'emails de notification sont conserves pendant 12 mois a des fins d'audit et de depannage |
| RM-N05.4 | L'historique des notifications en masse (administrateur) est conserve indefiniment |

### RM-N06 : Droits et visibilite

| Regle | Description |
|---|---|
| RM-N06.1 | Un utilisateur ne peut voir que ses propres notifications. Aucun utilisateur ne peut consulter les notifications d'un autre utilisateur, y compris les administrateurs |
| RM-N06.2 | Seuls les utilisateurs ayant le role « Administrateur » peuvent acceder a l'interface d'envoi de notifications en masse |
| RM-N06.3 | Les notifications de facturation ne sont envoyees qu'aux utilisateurs ayant les droits de gestion de facturation (roles : administrateur, gestionnaire de facturation, chef de projet selon la configuration) |
| RM-N06.4 | Les notifications de validation ne sont envoyees qu'aux utilisateurs concernes (demandeur et valideur(s) designe(s) dans le workflow de validation EPIC-012) |

---

## 8. Criteres Globaux

### 8.1 Performance

| Critere | Seuil |
|---|---|
| Delai de reception d'une notification in-app apres l'evenement declencheur | < 3 secondes |
| Delai d'envoi d'un email de notification apres l'evenement declencheur | < 5 minutes |
| Temps d'ouverture du panneau de notifications | < 500 ms |
| Temps de chargement de la page complete COLLABORATION > Notifications | < 2 secondes |
| Nombre maximal de notifications in-app simultanees par utilisateur | 10 000 (avant nettoyage automatique) |
| Temps de marquage « tout lu » pour 1000+ notifications | < 2 secondes |
| Debit d'envoi de notifications en masse (email) | 100 emails/minute minimum |

### 8.2 Fiabilite

| Critere | Seuil |
|---|---|
| Taux de delivrabilite des emails de notification | > 98% |
| Taux de disponibilite du systeme de notifications in-app | > 99,5% |
| Aucune perte de notification en cas de deconnexion temporaire de l'utilisateur | Les notifications sont stockees et delivrees a la reconnexion |
| Idempotence des notifications | Un evenement unique ne genere jamais de doublon de notification |

### 8.3 Securite

| Critere | Description |
|---|---|
| Isolation des donnees | Un utilisateur ne peut acceder qu'a ses propres notifications |
| Authentification | Les liens de redirection dans les emails requierent une session authentifiee |
| Protection contre les abus | Limitation du nombre de notifications en masse par administrateur (maximum 5 par jour) |
| Validation des donnees | Les contenus des notifications en masse sont assainis (sanitization) pour prevenir les injections XSS |

### 8.4 Accessibilite

| Critere | Description |
|---|---|
| ARIA | Le centre de notifications utilise les attributs ARIA appropriés (aria-live, aria-label, role="alert") |
| Clavier | Le panneau de notifications est entierement navigable au clavier |
| Contraste | Les indicateurs visuels (badge, point non lu) respectent les ratios de contraste WCAG 2.1 AA |
| Lecteur d'ecran | Les nouvelles notifications sont annoncees par les lecteurs d'ecran via aria-live="polite" |

### 8.5 Compatibilite

| Critere | Description |
|---|---|
| Navigateurs | Chrome, Firefox, Safari, Edge (2 dernieres versions majeures) |
| Emails | Rendu correct sur Gmail, Outlook (web et desktop), Apple Mail, Thunderbird |
| Responsive | Interface fonctionnelle sur les ecrans de 768px et plus |
| Temps reel | WebSocket avec fallback SSE et long-polling pour les navigateurs/proxys ne supportant pas WebSocket |

---

## 9. Definition of Done (DoD)

Une User Story de l'EPIC-017 est consideree comme terminee lorsque l'ensemble des criteres suivants sont remplis :

| # | Critere DoD | Description |
|---|---|---|
| DoD-01 | Criteres d'acceptation | Tous les criteres d'acceptation de la User Story sont verifies et valides |
| DoD-02 | Tests unitaires | Couverture minimale de 80% sur le code du module Notifications |
| DoD-03 | Tests d'integration | Tests d'integration couvrant les interactions avec les modules lies (Facturation, Temps, Validation, Collaboration, Configuration) |
| DoD-04 | Tests end-to-end | Scenarios E2E validant le parcours complet : evenement declencheur → generation → diffusion → reception → action |
| DoD-05 | Tests de performance | Verification des seuils de performance (section 8.1) sous charge simulee (100 utilisateurs simultanes, 1000 notifications/minute) |
| DoD-06 | Tests email | Verification du rendu des emails sur les clients de messagerie cibles (Gmail, Outlook, Apple Mail) |
| DoD-07 | Tests temps reel | Verification du fonctionnement WebSocket/SSE avec scenarios de deconnexion/reconnexion |
| DoD-08 | Revue de code | Code revise par au moins un pair (peer review) et approuve |
| DoD-09 | Documentation technique | Documentation de l'architecture du systeme de notifications, des evenements declencheurs et des templates |
| DoD-10 | Documentation utilisateur | Guide utilisateur decrivant le centre de notifications et la configuration des preferences |
| DoD-11 | Accessibilite | Verification des criteres d'accessibilite (section 8.4) avec un outil d'audit (Axe, Lighthouse) |
| DoD-12 | Securite | Aucune faille XSS dans les contenus de notification, isolation des donnees verifiee |
| DoD-13 | Deploiement | Code deploye sur l'environnement de staging et valide par l'equipe QA |
| DoD-14 | Acceptance Product Owner | Demonstration et validation par le Product Owner |

---

## 10. Dependances

### 10.1 Dependances techniques

| # | Dependance | Description | Type | Impact |
|---|---|---|---|---|
| DT-01 | Serveur WebSocket/SSE | Infrastructure de communication temps reel pour les notifications in-app | Technique | Bloquant pour les notifications temps reel (US-N01, US-N02) |
| DT-02 | Service d'envoi d'emails (SMTP/API) | Service de messagerie pour l'envoi des notifications email (ex : SendGrid, Amazon SES, Mailgun) | Technique | Bloquant pour les notifications email (US-N03) |
| DT-03 | File d'attente de messages (Message Queue) | Systeme de file d'attente pour le traitement asynchrone des notifications (ex : Redis Queue, RabbitMQ, Celery) | Technique | Bloquant pour la fiabilite et la scalabilite de l'envoi |
| DT-04 | Moteur de templates email | Systeme de rendu de templates HTML pour les emails de notification | Technique | Bloquant pour US-N03 |
| DT-05 | Planificateur de taches (CRON/Scheduler) | Systeme de planification pour les rappels periodiques et le nettoyage automatique | Technique | Bloquant pour les rappels (RM-N03, RM-N04) et le nettoyage (RM-N05) |

### 10.2 Dependances fonctionnelles (EPICs)

| # | EPIC | Dependance | Type | Impact |
|---|---|---|---|---|
| DF-01 | EPIC-004 Facturation | Evenements de facturation (creation, envoi, paiement, retard, avoir) | Fonctionnelle | Necessaire pour US-N06 |
| DF-02 | EPIC-005 Temps | Evenements de saisie de temps (soumission, validation, refus) et donnees de completion | Fonctionnelle | Necessaire pour US-N05 et les rappels RM-N03 |
| DF-03 | EPIC-012 Validation | Workflows de validation (conges, notes de frais, temps) et identification des valideurs | Fonctionnelle | Necessaire pour US-N05 |
| DF-04 | EPIC-015 Collaboration | Evenements de collaboration (commentaires, mentions, fichiers partages) | Fonctionnelle | Necessaire pour les notifications de collaboration (section 4.2) |
| DF-05 | EPIC-016 Configuration | Gestion des roles, des droits et des preferences par defaut | Fonctionnelle | Necessaire pour US-N04 (preferences par defaut) et US-N10 (droits administrateur) |

### 10.3 Dependances d'equipe

| # | Equipe | Contribution | Timing |
|---|---|---|---|
| DE-01 | Backend | Implementation du systeme de notifications, API REST, WebSocket/SSE, file d'attente | Sprints 1 et 2 |
| DE-02 | Frontend | Interface du centre de notifications, panneau deroulant, page preferences, badge compteur | Sprints 1 et 2 |
| DE-03 | DevOps | Mise en place de l'infrastructure WebSocket, service d'email, file d'attente, scheduler | Sprint 1 (prerequis) |
| DE-04 | Design/UX | Maquettes du centre de notifications, des templates email, de la page preferences | Avant Sprint 1 (prerequis) |
| DE-05 | QA | Tests fonctionnels, tests de performance, tests de rendu email | Sprint 2 |

---

## 11. Modele de Donnees

### 11.1 Entite : Notification

Table principale stockant les notifications generees par le systeme.

| Champ | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK, NOT NULL, UNIQUE | Identifiant unique de la notification |
| `user_id` | UUID | FK → User.id, NOT NULL, INDEX | Identifiant de l'utilisateur destinataire |
| `type` | VARCHAR(50) | NOT NULL, INDEX | Type de notification (enum : `time_reminder`, `time_validated`, `time_refused`, `leave_submitted`, `leave_approved`, `leave_refused`, `expense_submitted`, `expense_validated`, `expense_refused`, `invoice_pending`, `invoice_sent`, `payment_received`, `invoice_overdue`, `credit_note`, `project_assigned`, `milestone_approaching`, `phase_completed`, `budget_alert`, `task_assigned`, `task_overdue`, `task_completed`, `comment_new`, `file_shared`, `mention`, `comment_reply`, `system_update`, `system_maintenance`, `admin_announcement`) |
| `category` | VARCHAR(30) | NOT NULL, INDEX | Categorie de la notification (enum : `time`, `leave`, `expense`, `invoice`, `project`, `task`, `collaboration`, `system`) |
| `title` | VARCHAR(200) | NOT NULL | Titre de la notification |
| `message` | TEXT | NOT NULL | Message detaille de la notification |
| `reference_type` | VARCHAR(50) | NULL, INDEX | Type de l'entite referencee (ex : `project`, `task`, `invoice`, `timesheet`, `leave_request`, `expense_report`, `comment`, `file`) |
| `reference_id` | UUID | NULL, INDEX | Identifiant de l'entite referencee |
| `reference_url` | VARCHAR(500) | NULL | URL relative de redirection vers l'element concerne |
| `read` | BOOLEAN | NOT NULL, DEFAULT FALSE | Indicateur de lecture (true = lu, false = non lu) |
| `read_at` | TIMESTAMP | NULL | Date et heure de lecture de la notification |
| `metadata` | JSONB | NULL | Donnees supplementaires specifiques au type de notification (ex : montant, periode, nombre de jours de retard) |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW(), INDEX | Date et heure de creation de la notification |
| `expires_at` | TIMESTAMP | NULL | Date d'expiration automatique (defaut : created_at + 90 jours) |

**Index** :
- `idx_notification_user_read` : (`user_id`, `read`) — pour le compteur de notifications non lues
- `idx_notification_user_created` : (`user_id`, `created_at` DESC) — pour la liste paginee
- `idx_notification_user_category` : (`user_id`, `category`) — pour le filtrage par type
- `idx_notification_expires` : (`expires_at`) — pour le nettoyage automatique

---

### 11.2 Entite : NotificationPreference

Table stockant les preferences de notification de chaque utilisateur.

| Champ | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK, NOT NULL, UNIQUE | Identifiant unique de la preference |
| `user_id` | UUID | FK → User.id, NOT NULL, INDEX | Identifiant de l'utilisateur |
| `notification_type` | VARCHAR(50) | NOT NULL | Type de notification concerne (meme enum que `Notification.type`) |
| `channel_inapp` | BOOLEAN | NOT NULL, DEFAULT TRUE | Activation du canal in-app pour ce type |
| `channel_email` | BOOLEAN | NOT NULL, DEFAULT TRUE | Activation du canal email pour ce type |
| `enabled` | BOOLEAN | NOT NULL, DEFAULT TRUE | Activation globale de ce type de notification |
| `frequency` | VARCHAR(20) | NULL | Frequence pour les rappels (enum : `daily`, `weekly`, null pour les autres types) |
| `frequency_day` | SMALLINT | NULL | Jour de la semaine pour les rappels hebdomadaires (1=lundi, 7=dimanche) |
| `frequency_time` | TIME | NULL | Heure d'envoi pour les rappels (defaut : 17:00) |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date de creation |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date de derniere modification |

**Contrainte unique** : (`user_id`, `notification_type`) — une seule preference par type et par utilisateur.

**Index** :
- `idx_pref_user` : (`user_id`) — pour le chargement des preferences d'un utilisateur

---

### 11.3 Entite : NotificationTemplate

Table stockant les templates de notifications (contenu et mise en forme).

| Champ | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK, NOT NULL, UNIQUE | Identifiant unique du template |
| `type` | VARCHAR(50) | NOT NULL, UNIQUE | Type de notification concerne (meme enum que `Notification.type`) |
| `locale` | VARCHAR(5) | NOT NULL, DEFAULT 'fr' | Langue du template (ex : `fr`, `en`) |
| `subject_template` | VARCHAR(300) | NOT NULL | Template de l'objet de l'email (supporte les variables avec syntaxe `{{variable}}`) |
| `body_template_inapp` | TEXT | NOT NULL | Template du message in-app (supporte les variables) |
| `body_template_email` | TEXT | NOT NULL | Template du corps de l'email en HTML (supporte les variables) |
| `variables` | JSONB | NOT NULL | Liste des variables disponibles pour ce template (ex : `["user_name", "project_name", "amount", "due_date"]`) |
| `is_active` | BOOLEAN | NOT NULL, DEFAULT TRUE | Indique si le template est actif |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date de creation |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date de derniere modification |

**Contrainte unique** : (`type`, `locale`) — un seul template par type et par langue.

---

### 11.4 Entite : NotificationBroadcast

Table stockant les notifications en masse envoyees par les administrateurs.

| Champ | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK, NOT NULL, UNIQUE | Identifiant unique de la diffusion |
| `sender_id` | UUID | FK → User.id, NOT NULL | Identifiant de l'administrateur expediteur |
| `title` | VARCHAR(150) | NOT NULL | Titre de la notification en masse |
| `message` | TEXT | NOT NULL | Contenu du message (supporte la mise en forme basique) |
| `target_type` | VARCHAR(30) | NOT NULL | Type de ciblage (enum : `all`, `team`, `role`, `office`) |
| `target_filter` | JSONB | NULL | Criteres de filtrage des destinataires (ex : `{"team_ids": ["uuid1", "uuid2"]}`) |
| `channels` | JSONB | NOT NULL | Canaux de diffusion (ex : `{"inapp": true, "email": true}`) |
| `status` | VARCHAR(20) | NOT NULL, DEFAULT 'draft' | Statut de la diffusion (enum : `draft`, `scheduled`, `sending`, `sent`, `failed`) |
| `scheduled_at` | TIMESTAMP | NULL | Date et heure d'envoi planifie (null = envoi immediat) |
| `sent_at` | TIMESTAMP | NULL | Date et heure d'envoi effectif |
| `recipient_count` | INTEGER | NULL | Nombre de destinataires |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date de creation |

---

### 11.5 Entite : NotificationEmailLog

Table de journalisation des envois d'emails de notification.

| Champ | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK, NOT NULL, UNIQUE | Identifiant unique du log |
| `notification_id` | UUID | FK → Notification.id, NOT NULL | Identifiant de la notification associee |
| `user_id` | UUID | FK → User.id, NOT NULL | Identifiant du destinataire |
| `email_address` | VARCHAR(255) | NOT NULL | Adresse email du destinataire |
| `status` | VARCHAR(20) | NOT NULL | Statut de l'envoi (enum : `pending`, `sent`, `delivered`, `bounced`, `failed`) |
| `attempts` | SMALLINT | NOT NULL, DEFAULT 0 | Nombre de tentatives d'envoi |
| `last_attempt_at` | TIMESTAMP | NULL | Date de la derniere tentative |
| `error_message` | TEXT | NULL | Message d'erreur en cas d'echec |
| `external_id` | VARCHAR(255) | NULL | Identifiant du message chez le fournisseur d'email (SendGrid, SES, etc.) |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date de creation |

---

### 11.6 Schema relationnel

```
User (1) ──────── (N) Notification
  │                      │
  │                      │ reference_type + reference_id
  │                      │ → Project / Task / Invoice / Timesheet / ...
  │
  ├──── (N) NotificationPreference
  │           │
  │           └── notification_type (enum)
  │
  └──── (N) NotificationBroadcast (sender)

Notification (1) ──── (0..1) NotificationEmailLog

NotificationTemplate (independant, reference par type + locale)
```

---

## 12. Estimation

### 12.1 Synthese

| Parametre | Valeur |
|---|---|
| **Duree totale estimee** | 3 a 4 semaines |
| **Nombre de sprints** | 2 sprints de 2 semaines |
| **Effort total estime** | 120 a 160 points d'effort (story points) |
| **Taille de l'equipe recommandee** | 2 developpeurs backend + 1 developpeur frontend + 1 QA |
| **Complexite globale** | Moyenne a elevee (temps reel, multi-canal, integrations transversales) |

### 12.2 Estimation par User Story

| User Story | Intitule | Complexite | Effort (SP) | Sprint |
|---|---|---|---|---|
| US-N01 | Centre de notifications in-app | Elevee | 13 | Sprint 1 |
| US-N02 | Badge compteur de notifications non lues | Moyenne | 8 | Sprint 1 |
| US-N03 | Notifications par email | Elevee | 21 | Sprint 1 |
| US-N04 | Preferences de notifications utilisateur | Moyenne | 13 | Sprint 1 |
| US-N05 | Notifications de validation | Elevee | 13 | Sprint 2 |
| US-N06 | Notifications de facturation | Moyenne | 13 | Sprint 2 |
| US-N07 | Notifications de projets et taches | Moyenne | 13 | Sprint 2 |
| US-N08 | Marquage lu/non lu et suppression | Faible | 5 | Sprint 1 |
| US-N09 | Lien direct vers l'element concerne | Faible | 5 | Sprint 1 |
| US-N10 | Notifications administrateur en masse | Elevee | 13 | Sprint 2 |
| **Total** | | | **117 SP** | |

### 12.3 Repartition par sprint

#### Sprint 1 — Infrastructure et Centre de notifications (Semaines 1-2)

| Activite | Description | Effort |
|---|---|---|
| **Infrastructure** | Mise en place du serveur WebSocket/SSE, de la file d'attente (Celery/Redis), du service d'email, du scheduler | 16 SP |
| **US-N01** | Centre de notifications in-app : panneau deroulant, page COLLABORATION > Notifications, API REST (CRUD notifications) | 13 SP |
| **US-N02** | Badge compteur : implementation du compteur temps reel avec WebSocket, mise a jour reactive | 8 SP |
| **US-N03** | Notifications email : templates HTML, integration service d'envoi, mecanisme de retry, queue asynchrone | 21 SP |
| **US-N04** | Preferences utilisateur : page de configuration, matrice de preferences, API de sauvegarde | 13 SP |
| **US-N08** | Marquage lu/non lu : actions individuelles et en masse, API | 5 SP |
| **US-N09** | Navigation contextuelle : liens de redirection, gestion des elements supprimes | 5 SP |
| **Total Sprint 1** | | **81 SP** |

#### Sprint 2 — Evenements metier et fonctionnalites avancees (Semaines 3-4)

| Activite | Description | Effort |
|---|---|---|
| **US-N05** | Notifications de validation : integration EPIC-005 et EPIC-012, evenements temps/conges/notes de frais, rappels de validation en attente | 13 SP |
| **US-N06** | Notifications de facturation : integration EPIC-004, evenements factures/paiements/retards, rappels d'echeance | 13 SP |
| **US-N07** | Notifications de projets et taches : evenements d'assignation, jalons, phases, alertes de budget et retards | 13 SP |
| **US-N10** | Notifications en masse : interface d'envoi, selection des destinataires, planification, historique | 13 SP |
| **Tests et stabilisation** | Tests de performance, tests de rendu email multi-clients, tests de charge, correction de bugs | 8 SP |
| **Documentation** | Documentation technique et utilisateur | 3 SP |
| **Total Sprint 2** | | **63 SP** |

### 12.4 Risques et mitigations

| # | Risque | Probabilite | Impact | Mitigation |
|---|---|---|---|---|
| R01 | Complexite de l'infrastructure temps reel (WebSocket/SSE) | Moyenne | Eleve | Prevoir un fallback SSE/long-polling ; utiliser une librairie eprouvee (ex : Django Channels, Socket.io) |
| R02 | Delivrabilite des emails (spam, bounces) | Moyenne | Moyen | Utiliser un service d'envoi d'email professionnel (SendGrid, SES) ; configurer SPF, DKIM, DMARC |
| R03 | Performance sous charge (notifications en masse) | Moyenne | Eleve | Traitement par batch avec file d'attente ; limitation du debit ; tests de charge en amont |
| R04 | Dependances avec les autres EPICs non termines | Elevee | Moyen | Definir des interfaces/contrats d'evenements ; utiliser des mocks pour les EPICs non encore developpes |
| R05 | Compatibilite des templates email multi-clients | Faible | Faible | Utiliser un framework de templates email eprouve (MJML, Foundation for Emails) ; tests sur Litmus |
| R06 | Surcharge de notifications pour les utilisateurs | Moyenne | Moyen | Preferences granulaires des le Sprint 1 ; valeurs par defaut raisonnables ; respect du « ne pas deranger » |

### 12.5 Hypotheses de planification

- Les maquettes UX/UI du centre de notifications et des templates email sont livrees avant le debut du Sprint 1.
- L'infrastructure technique (serveur, base de donnees) est disponible pour le developpement.
- Les evenements declencheurs des EPICs lies (EPIC-004, EPIC-005, EPIC-012, EPIC-015) sont soit deja implementes, soit peuvent etre simules via des mocks.
- L'equipe DevOps est disponible pour la mise en place de l'infrastructure temps reel et du service d'email en debut de Sprint 1.
- La charge de travail est repartie sur une equipe de 4 personnes (2 backend, 1 frontend, 1 QA) a temps plein.

---

*Document redige dans le cadre du projet OOTI — Application de gestion de projets pour cabinets d'architecture.*
*Version 1.0 — Fevrier 2026*
