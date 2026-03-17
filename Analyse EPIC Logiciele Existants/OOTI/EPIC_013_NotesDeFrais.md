# EPIC -- Module Notes de frais

**Application OOTI -- Gestion de projets pour cabinets d'architecture**
**Version 1.0 -- Fevrier 2026**

---

## 1. Identification

| Champ | Valeur |
|---|---|
| **Nom de l'EPIC** | Notes de frais |
| **Reference** | EPIC-013 |
| **Module parent** | Equipe |
| **Priorite** | Moyenne |
| **Auteur** | Architecte logiciel senior |
| **Date de creation** | 26 fevrier 2026 |
| **Version du document** | 1.0 |
| **Statut** | Brouillon |
| **EPICs lies** | EPIC-002 Projets, EPIC-007 Couts, EPIC-012 Validation |

### Points d'acces dans l'application

| Chemin d'acces | Role concerne | Description |
|---|---|---|
| **EQUIPE > Notes de frais** | Collaborateur | Saisie et suivi de ses propres notes de frais |
| **EQUIPE > Validation > Notes de frais** | Manager | Workflow de validation des notes de frais de son equipe |
| **GESTION > Couts > Notes de frais** | Administrateur / Direction | Vue consolidee agence, exports comptables |

---

## 2. Contexte et Problematique

### Contexte

Les cabinets d'architecture engagent regulierement des depenses professionnelles dans le cadre de leurs projets : deplacements sur chantier, repas avec des clients ou partenaires, achats de fournitures techniques, frais d'hebergement lors de missions eloignees, telecommunications, etc. Ces frais sont engages par les collaborateurs (architectes, chefs de projet, dessinateurs, conducteurs de travaux) et doivent etre rembourses par le cabinet.

Dans le cadre d'un cabinet d'architecture, la gestion des notes de frais presente des specificites importantes :

- **Imputation projet** : une grande partie des frais est directement liee a un projet client (deplacement sur site, impression de plans, maquettes). Ces frais doivent pouvoir etre imputes au projet correspondant pour calculer le cout reel du projet et la rentabilite effective.
- **Multi-devises** : les cabinets travaillant a l'international (concours, chantiers a l'etranger) doivent gerer des frais en devises differentes.
- **Frais kilometriques** : les deplacements en vehicule personnel vers les chantiers sont frequents et necessitent un calcul automatise selon un bareme configurable.
- **Justificatifs** : la reglementation comptable et fiscale impose la conservation de justificatifs pour chaque depense.
- **Volume et frequence** : les collaborateurs sur chantier peuvent generer plusieurs notes de frais par semaine.

### Problematique

Actuellement, sans module dedie, les cabinets d'architecture font face aux difficultes suivantes :

1. **Processus manuel et chronophage** : les notes de frais sont gerees via des tableurs Excel, des formulaires papier ou des emails, entrainant des pertes de temps considerables pour les collaborateurs, les managers et le service comptable.
2. **Absence de tracabilite** : il est difficile de suivre le statut d'une note de frais (soumise ? validee ? remboursee ?), ce qui genere de la frustration chez les collaborateurs et des relances inutiles.
3. **Erreurs de saisie et d'imputation** : sans controle automatise, les erreurs de montants, d'affectation de TVA ou d'imputation projet sont frequentes.
4. **Perte de justificatifs** : les tickets et factures papier sont regulierement egares, rendant impossible la justification comptable.
5. **Absence de vision consolidee** : la direction ne dispose pas d'une vue globale des depenses par collaborateur, par projet ou par categorie, empechant toute analyse et tout pilotage budgetaire.
6. **Non-respect des politiques** : sans controle automatise des plafonds et des regles de remboursement, les depassements ne sont detectes qu'a posteriori.
7. **Delais de remboursement** : le processus de validation etant opaque et non structure, les delais de remboursement sont souvent excessifs.

---

## 3. Objectif

### Objectif principal

Fournir un module de gestion des notes de frais integre a l'application OOTI permettant aux collaborateurs de saisir, soumettre et suivre leurs depenses professionnelles, aux managers de valider efficacement les demandes de remboursement, et a l'administration de disposer d'une vision consolidee pour le pilotage financier et l'export comptable.

### Objectifs specifiques

| # | Objectif | Indicateur de succes |
|---|---|---|
| O1 | Digitaliser integralement le processus de saisie des notes de frais | 100% des notes de frais saisies via l'application |
| O2 | Reduire le temps de traitement d'une note de frais | Temps moyen de traitement < 48h (saisie a remboursement) |
| O3 | Assurer la tracabilite complete du cycle de vie d'une note de frais | Chaque note de frais dispose d'un historique d'etats complet |
| O4 | Permettre l'imputation des frais aux projets | 100% des frais projet sont imputes au bon projet |
| O5 | Garantir la conformite comptable et fiscale | 100% des notes validees disposent d'un justificatif numerise |
| O6 | Automatiser les controles de politique de remboursement | Detection automatique de 100% des depassements de plafond |
| O7 | Permettre l'export des donnees pour la comptabilite | Export disponible aux formats CSV et PDF |
| O8 | Fournir une vision consolidee des depenses a la direction | Tableaux de bord disponibles avec filtres multi-criteres |

---

## 4. Perimetre Fonctionnel

### 4.1 Saisie et gestion des notes de frais

- Formulaire de creation d'une note de frais avec les champs obligatoires et optionnels
- Categories de frais predefinies : **Transport**, **Repas**, **Hebergement**, **Fournitures**, **Telecommunications**, **Divers**
- Saisie des montants : montant HT, taux de TVA applicable, calcul automatique du montant TTC (et inversement)
- Selection de la devise parmi les devises configurees pour l'entite
- Champ date de la depense
- Champ description / motif de la depense
- Statut initial : **Brouillon** (modifiable tant que non soumise)
- Possibilite de dupliquer une note de frais existante
- Suppression possible uniquement au statut Brouillon

### 4.2 Justificatifs

- Upload de justificatifs : formats acceptes (JPEG, PNG, PDF)
- Taille maximale par fichier : 10 Mo
- Possibilite d'attacher plusieurs justificatifs a une meme note de frais
- Visualisation des justificatifs en miniature et en plein ecran
- Stockage securise des justificatifs (stockage objet type S3)
- Caractere obligatoire ou optionnel du justificatif configurable par categorie dans la politique de remboursement

### 4.3 Association projet

- Champ optionnel de selection du projet (liste des projets actifs de l'entite)
- Lien avec le module EPIC-002 Projets pour alimenter les couts projet
- Lien avec le module EPIC-007 Couts pour l'imputation dans le suivi des couts du projet
- Recherche du projet par nom ou code projet
- Un frais non associe a un projet est impute aux frais generaux de l'entite

### 4.4 Workflow de validation

- Soumission de la note de frais par le collaborateur (passage de Brouillon a Soumise)
- Notification au manager lors de la soumission
- Le manager peut **valider** ou **refuser** la note de frais
- En cas de refus, un motif de refus est obligatoire
- En cas de refus, la note retourne au statut Brouillon pour modification par le collaborateur
- En cas de validation, la note passe au statut **Validee**
- Passage au statut **Remboursee** lors de la confirmation du remboursement par l'administrateur
- Integration avec le module EPIC-012 Validation pour le workflow generique
- Historique complet des changements de statut avec horodatage et auteur

### Diagramme des statuts

```
[Brouillon] --soumission--> [Soumise] --validation--> [Validee] --remboursement--> [Remboursee]
                               |
                               +---refus---> [Refusee] --modification--> [Brouillon]
```

### 4.5 Vues et consultation

- **Vue collaborateur** (EQUIPE > Notes de frais) : liste de ses propres notes de frais avec filtres et tri
- **Vue manager** (EQUIPE > Validation > Notes de frais) : liste des notes de frais de son equipe en attente de validation, et historique des notes traitees
- **Vue agence** (GESTION > Couts > Notes de frais) : vue consolidee de toutes les notes de frais de l'entite, avec filtres avances et indicateurs agreges

### 4.6 Filtres et recherche

- Filtrage par periode (date debut / date fin)
- Filtrage par collaborateur (vue manager et agence)
- Filtrage par categorie de frais
- Filtrage par statut (Brouillon, Soumise, Validee, Refusee, Remboursee)
- Filtrage par projet
- Filtrage par montant (fourchette min/max)
- Recherche textuelle sur la description
- Combinaison de filtres multiples
- Sauvegarde des filtres favoris (optionnel v2)

### 4.7 Export comptable

- Export de la liste des notes de frais filtrees au format CSV
- Export au format PDF (recapitulatif individuel ou global)
- Contenu de l'export : date, collaborateur, categorie, description, montant HT, TVA, montant TTC, devise, projet, statut
- Inclusion optionnelle des justificatifs dans l'export PDF
- Export conforme aux besoins d'integration avec les logiciels comptables courants

### 4.8 Frais kilometriques

- Sous-formulaire dedie pour la categorie Transport > Frais kilometriques
- Saisie du lieu de depart et du lieu d'arrivee
- Saisie de la distance parcourue (en km)
- Option aller-retour (doublement automatique de la distance)
- Selection de la puissance fiscale du vehicule
- Application automatique du bareme kilometrique configure dans la politique de remboursement
- Calcul automatique du montant a rembourser
- Les frais kilometriques ne sont pas soumis a la TVA (montant HT = montant TTC)

### 4.9 Politique de remboursement

- Configuration par l'administrateur au niveau de l'entite
- Definition de plafonds par categorie de frais (montant maximum par note, par jour, par mois)
- Definition du caractere obligatoire ou non du justificatif par categorie
- Configuration du bareme kilometrique (montant par km selon la puissance fiscale)
- Alerte visuelle lors de la saisie si un plafond est depasse
- Blocage optionnel de la soumission en cas de depassement de plafond (configurable)
- Historisation des modifications de politique (date d'effet)

---

## 5. User Stories

### US-NF01 : Saisie d'une note de frais

**En tant que** collaborateur du cabinet,
**Je veux** pouvoir saisir une note de frais en renseignant la date, la categorie, la description, les montants et la devise,
**Afin de** declarer une depense professionnelle en vue de son remboursement.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---|---|
| CA-01 | Le formulaire de creation est accessible depuis EQUIPE > Notes de frais via un bouton "Nouvelle note de frais" | Le bouton est visible et cliquable pour tout collaborateur actif |
| CA-02 | Les champs obligatoires sont : date, categorie, description, montant (HT ou TTC), devise | La soumission du formulaire echoue si un champ obligatoire est vide, avec message d'erreur explicite |
| CA-03 | La liste des categories propose : Transport, Repas, Hebergement, Fournitures, Telecommunications, Divers | Les 6 categories sont presentes dans le selecteur |
| CA-04 | La saisie du montant HT calcule automatiquement le TTC en fonction du taux de TVA selectionne, et inversement | Le calcul est correct pour tous les taux de TVA standards (0%, 5.5%, 10%, 20%) |
| CA-05 | La devise par defaut est celle de l'entite du collaborateur, mais peut etre changee | La liste des devises est celle configuree pour l'entite |
| CA-06 | La note de frais est creee au statut "Brouillon" | Le statut affiche est "Brouillon" apres la creation |
| CA-07 | Une note de frais au statut "Brouillon" peut etre modifiee ou supprimee | Les boutons Modifier et Supprimer sont presents et fonctionnels |
| CA-08 | Un message de confirmation s'affiche apres la creation reussie de la note de frais | Le toast de confirmation est visible pendant 3 secondes |

---

### US-NF02 : Upload de justificatif

**En tant que** collaborateur du cabinet,
**Je veux** pouvoir joindre un ou plusieurs justificatifs (photo, scan, PDF) a ma note de frais,
**Afin de** fournir la preuve de la depense pour la validation et la conformite comptable.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---|---|
| CA-01 | Un bouton "Ajouter un justificatif" est present sur le formulaire de la note de frais | Le bouton est visible et accessible |
| CA-02 | Les formats acceptes sont JPEG, PNG et PDF | Un message d'erreur s'affiche si un format non supporte est selectionne |
| CA-03 | La taille maximale par fichier est de 10 Mo | Un message d'erreur s'affiche si le fichier depasse 10 Mo |
| CA-04 | Plusieurs justificatifs peuvent etre attaches a une meme note de frais | Le compteur de justificatifs s'incremente apres chaque ajout |
| CA-05 | Les justificatifs sont affiches en miniature sous le formulaire | Les miniatures sont visibles et cliquables pour un apercu en plein ecran |
| CA-06 | Un justificatif peut etre supprime tant que la note est au statut "Brouillon" | Le bouton de suppression est present sur chaque miniature en statut Brouillon |
| CA-07 | Si la politique de remboursement rend le justificatif obligatoire pour la categorie, la soumission est bloquee sans justificatif | Un message d'erreur s'affiche a la soumission indiquant "Justificatif obligatoire pour cette categorie" |
| CA-08 | Le justificatif est stocke de maniere securisee et accessible uniquement par le collaborateur, son manager et les administrateurs | Un collaborateur tiers ne peut pas acceder au justificatif via l'URL directe |

---

### US-NF03 : Association a un projet

**En tant que** collaborateur du cabinet,
**Je veux** pouvoir associer ma note de frais a un projet existant,
**Afin que** le cout soit impute au projet concerne et pris en compte dans le suivi de rentabilite.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---|---|
| CA-01 | Un champ de selection de projet est present sur le formulaire, marque comme optionnel | Le champ est visible avec la mention "(optionnel)" |
| CA-02 | La liste des projets proposes correspond aux projets actifs de l'entite du collaborateur | Seuls les projets au statut "Actif" ou "En cours" de l'entite apparaissent |
| CA-03 | La recherche de projet est possible par nom ou par code projet | La saisie de texte dans le champ filtre les projets en temps reel (autocomplete) |
| CA-04 | Lorsqu'un projet est associe, le montant de la note de frais est integre dans les couts du projet (EPIC-007) apres validation | Le montant apparait dans la section couts du projet dans le module Couts |
| CA-05 | Une note de frais sans projet associe est imputee aux frais generaux de l'entite | La note apparait dans la categorie "Frais generaux" de la vue consolidee |
| CA-06 | Le projet associe peut etre modifie tant que la note est au statut "Brouillon" | Le champ projet est editable en mode modification au statut Brouillon |
| CA-07 | Le nom et le code du projet associe sont affiches dans la liste des notes de frais | La colonne "Projet" est visible dans la vue liste avec le code et le nom du projet |

---

### US-NF04 : Soumission pour validation

**En tant que** collaborateur du cabinet,
**Je veux** pouvoir soumettre ma note de frais pour validation par mon manager,
**Afin de** declencher le processus de validation et obtenir le remboursement de ma depense.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---|---|
| CA-01 | Un bouton "Soumettre" est present sur une note de frais au statut "Brouillon" | Le bouton est visible et actif uniquement au statut Brouillon |
| CA-02 | La soumission fait passer le statut de "Brouillon" a "Soumise" | Le statut affiche est "Soumise" apres la soumission |
| CA-03 | Une notification (in-app et/ou email) est envoyee au manager du collaborateur lors de la soumission | Le manager recoit une notification avec le lien vers la note de frais |
| CA-04 | Apres soumission, la note de frais n'est plus modifiable par le collaborateur | Les champs sont en lecture seule et le bouton Modifier est masque |
| CA-05 | Le manager peut valider la note de frais, ce qui fait passer le statut a "Validee" | Le bouton "Valider" est disponible pour le manager sur une note "Soumise" |
| CA-06 | Le manager peut refuser la note de frais avec un motif obligatoire, ce qui fait passer le statut a "Refusee" | Le champ motif de refus est obligatoire ; la note passe a "Refusee" |
| CA-07 | En cas de refus, la note retourne automatiquement au statut "Brouillon" apres consultation du motif par le collaborateur | Le collaborateur voit le motif de refus et peut modifier la note a nouveau |
| CA-08 | L'historique des changements de statut est enregistre avec la date, l'heure et l'auteur de chaque action | L'onglet "Historique" de la note affiche la chronologie complete des actions |

---

### US-NF05 : Vue consolidee manager et agence

**En tant que** manager (ou administrateur),
**Je veux** disposer d'une vue consolidee des notes de frais de mon equipe (ou de toute l'agence),
**Afin de** piloter les depenses, traiter les validations en attente et detecter les anomalies.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---|---|
| CA-01 | La vue manager est accessible depuis EQUIPE > Validation > Notes de frais | Le lien de menu est present et accessible pour les utilisateurs ayant le role Manager |
| CA-02 | La vue manager affiche uniquement les notes de frais des collaborateurs sous la responsabilite du manager | Aucune note de frais d'un collaborateur d'une autre equipe n'est visible |
| CA-03 | La vue agence est accessible depuis GESTION > Couts > Notes de frais | Le lien de menu est present et accessible pour les utilisateurs ayant le role Administrateur |
| CA-04 | La vue agence affiche toutes les notes de frais de l'entite, tous collaborateurs confondus | Le nombre total de notes correspond au total de l'entite |
| CA-05 | Les deux vues affichent un tableau recapitulatif avec les colonnes : Date, Collaborateur, Categorie, Description, Montant TTC, Devise, Projet, Statut | Toutes les colonnes sont presentes et triables |
| CA-06 | Des indicateurs agreges sont affiches en haut de page : nombre de notes en attente, montant total en attente, montant total valide sur le mois | Les indicateurs sont calcules correctement et mis a jour en temps reel |
| CA-07 | Le manager peut acceder au detail d'une note de frais en cliquant dessus | Le clic ouvre la fiche detaillee de la note de frais |
| CA-08 | Les actions de validation et de refus sont disponibles directement depuis la vue consolidee (action en lot optionnelle) | Les boutons Valider et Refuser sont accessibles pour chaque ligne de note au statut "Soumise" |

---

### US-NF06 : Historique et filtrage

**En tant que** utilisateur (collaborateur, manager ou administrateur),
**Je veux** pouvoir filtrer et rechercher dans l'historique des notes de frais selon plusieurs criteres,
**Afin de** retrouver rapidement une note de frais specifique ou analyser les depenses selon un axe particulier.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---|---|
| CA-01 | Un panneau de filtres est disponible sur chaque vue de notes de frais | Le panneau de filtres est visible ou accessible via un bouton "Filtres" |
| CA-02 | Le filtre par periode permet de selectionner une date de debut et une date de fin | Les champs date sont fonctionnels et le filtrage s'applique correctement |
| CA-03 | Le filtre par collaborateur est disponible dans les vues manager et agence | Le selecteur de collaborateur propose les membres de l'equipe (manager) ou de l'entite (admin) |
| CA-04 | Le filtre par categorie permet de selectionner une ou plusieurs categories | La selection multiple est possible et le filtrage est correct |
| CA-05 | Le filtre par statut permet de selectionner un ou plusieurs statuts | Les 5 statuts sont proposes : Brouillon, Soumise, Validee, Refusee, Remboursee |
| CA-06 | Le filtre par projet permet de selectionner un projet specifique | Le selecteur de projet fonctionne avec autocomplete |
| CA-07 | Les filtres sont combinables entre eux (AND logique) | L'application simultanee de plusieurs filtres retourne l'intersection des resultats |
| CA-08 | Un bouton "Reinitialiser les filtres" permet de revenir a la vue non filtree | Le clic sur le bouton supprime tous les filtres actifs et reaffiche la liste complete |

---

### US-NF07 : Export comptable

**En tant qu'** administrateur ou comptable,
**Je veux** pouvoir exporter les notes de frais validees ou remboursees dans un format exploitable par le logiciel comptable,
**Afin de** faciliter l'integration comptable et reduire les saisies manuelles.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---|---|
| CA-01 | Un bouton "Exporter" est disponible sur les vues manager et agence | Le bouton est visible et accessible pour les roles autorises |
| CA-02 | L'export au format CSV est disponible | Le fichier CSV est genere et telecharge correctement |
| CA-03 | L'export au format PDF est disponible | Le fichier PDF est genere avec une mise en page lisible et professionnelle |
| CA-04 | L'export respecte les filtres actifs (periode, collaborateur, categorie, statut, projet) | Le contenu exporte correspond exactement aux notes de frais filtrees a l'ecran |
| CA-05 | Le fichier CSV contient les colonnes : Date, Collaborateur, Categorie, Description, Montant HT, Taux TVA, Montant TVA, Montant TTC, Devise, Projet, Statut, Date de validation | Toutes les colonnes sont presentes et les donnees sont correctes |
| CA-06 | L'export PDF peut optionnellement inclure les justificatifs en annexe | Une case a cocher "Inclure les justificatifs" est disponible avant l'export |
| CA-07 | Le nom du fichier exporte contient la date et la periode concernee | Le format du nom est : NotesDeFrais_[ENTITE]_[DATE_DEBUT]_[DATE_FIN].[ext] |
| CA-08 | L'encodage du fichier CSV est UTF-8 avec BOM pour la compatibilite Excel | Le fichier s'ouvre correctement dans Excel sans probleme d'accents |

---

### US-NF08 : Frais kilometriques

**En tant que** collaborateur du cabinet,
**Je veux** pouvoir saisir des frais kilometriques avec calcul automatique du montant selon le bareme en vigueur,
**Afin de** declarer mes deplacements professionnels en vehicule personnel de maniere precise et conforme.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---|---|
| CA-01 | Lorsque la categorie "Transport" est selectionnee, un sous-type "Frais kilometriques" est disponible | Le sous-type est accessible dans le formulaire de saisie |
| CA-02 | Le formulaire de frais kilometriques propose les champs : lieu de depart, lieu d'arrivee, distance (km), aller-retour (oui/non), puissance fiscale du vehicule | Tous les champs sont presents et fonctionnels |
| CA-03 | L'option "Aller-retour" double automatiquement la distance saisie | Le champ distance totale affiche le double de la distance saisie quand l'option est cochee |
| CA-04 | La puissance fiscale du vehicule est selectionnable parmi les tranches definies dans la politique (ex : 3CV, 4CV, 5CV, 6CV, 7CV et plus) | Les tranches correspondent a celles configurees dans la politique de remboursement |
| CA-05 | Le montant est calcule automatiquement : distance x taux kilometrique de la tranche | Le montant affiche est correct selon le bareme configure |
| CA-06 | Le montant HT et le montant TTC sont identiques (pas de TVA sur les frais kilometriques) | Le taux de TVA est automatiquement fixe a 0% et non modifiable |
| CA-07 | Le detail du calcul est affiche de maniere transparente (distance x taux = montant) | Le detail est visible sous le champ montant |
| CA-08 | L'historique des deplacements kilometriques est consultable par le collaborateur | Un onglet ou filtre "Frais kilometriques" permet de lister tous les deplacements |

---

### US-NF09 : Politique de remboursement

**En tant qu'** administrateur du cabinet,
**Je veux** pouvoir configurer la politique de remboursement des notes de frais (plafonds, justificatifs obligatoires, baremes),
**Afin de** cadrer les depenses selon les regles internes du cabinet et garantir la conformite.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---|---|
| CA-01 | Un ecran de configuration de la politique est accessible depuis les parametres de l'entite | Le menu Parametres > Politique de remboursement est accessible pour le role Administrateur |
| CA-02 | Pour chaque categorie de frais, un plafond maximum peut etre defini (par note, par jour, par mois) | Les champs de plafond sont disponibles et enregistrables pour chaque categorie |
| CA-03 | Pour chaque categorie, le caractere obligatoire du justificatif peut etre active ou desactive | La case a cocher "Justificatif obligatoire" est fonctionnelle pour chaque categorie |
| CA-04 | Le bareme kilometrique est configurable par tranche de puissance fiscale | Le tableau des tarifs par tranche est editable et enregistrable |
| CA-05 | Une alerte visuelle s'affiche au collaborateur lors de la saisie si le montant depasse le plafond de la categorie | Un avertissement orange ou rouge s'affiche en temps reel sous le champ montant |
| CA-06 | Le blocage de la soumission en cas de depassement de plafond est configurable (actif/inactif) | Le toggle "Bloquer la soumission en cas de depassement" est fonctionnel |
| CA-07 | Les modifications de politique sont historisees avec une date d'effet | L'historique affiche les versions precedentes de la politique avec leurs dates d'effet |
| CA-08 | La politique s'applique a toutes les nouvelles notes de frais de l'entite a compter de la date d'effet | Une note de frais creee apres la date d'effet est soumise aux nouvelles regles |

---

### US-NF10 : Suivi des remboursements

**En tant que** collaborateur du cabinet,
**Je veux** pouvoir suivre le statut de remboursement de mes notes de frais validees,
**Afin de** savoir quand mes depenses seront effectivement remboursees et identifier les retards eventuels.

#### Criteres d'acceptation

| # | Critere | Verification |
|---|---|---|
| CA-01 | La vue collaborateur affiche clairement le statut de chaque note de frais, notamment la distinction entre "Validee" et "Remboursee" | Les badges de statut sont visuellement distincts (couleurs differentes) |
| CA-02 | L'administrateur peut marquer une note de frais validee comme "Remboursee" | Le bouton "Marquer comme remboursee" est disponible sur les notes au statut "Validee" |
| CA-03 | La date de remboursement est enregistree lors du passage au statut "Remboursee" | Le champ reimbursed_at est renseigne avec la date et l'heure du marquage |
| CA-04 | Le collaborateur recoit une notification lorsque sa note de frais est marquee comme remboursee | Une notification in-app et/ou email est envoyee au collaborateur |
| CA-05 | Un recapitulatif mensuel des remboursements est disponible pour le collaborateur | Un widget ou un onglet "Mes remboursements" affiche le total rembourse par mois |
| CA-06 | L'administrateur peut effectuer un marquage en lot de plusieurs notes comme "Remboursees" | La selection multiple et l'action groupee "Marquer comme remboursees" sont fonctionnelles |
| CA-07 | Un indicateur du delai moyen de remboursement est affiche dans la vue agence | L'indicateur est calcule correctement (moyenne entre date de validation et date de remboursement) |
| CA-08 | Les notes validees depuis plus de 30 jours et non remboursees sont signalees visuellement | Un badge ou une icone d'alerte est affiche sur les notes concernees |

---

## 6. Hors Perimetre

Les elements suivants sont explicitement exclus du perimetre de cet EPIC et pourront etre traites dans des evolutions ulterieures :

| # | Element exclu | Justification |
|---|---|---|
| HP-01 | Integration avec les logiciels comptables (Sage, QuickBooks, Cegid, etc.) | Necessite une etude specifique des formats et API de chaque logiciel ; sera traite dans un EPIC dedie |
| HP-02 | Application mobile dediee pour la saisie des notes de frais | Le module sera accessible via le navigateur mobile (responsive) ; une application native pourra etre envisagee ulterieurement |
| HP-03 | OCR (reconnaissance optique de caracteres) sur les justificatifs | Fonctionnalite avancee necessitant l'integration d'un service tiers ; prevue en v2 |
| HP-04 | Carte de paiement d'entreprise et rapprochement automatique | Necessite des partenariats bancaires et une integration complexe |
| HP-05 | Avances sur frais et acomptes | Processus distinct qui sera traite dans un EPIC separe |
| HP-06 | Gestion des indemnites forfaitaires (per diem) | Mecanisme different des notes de frais classiques ; sera traite separement |
| HP-07 | Workflow de validation multi-niveaux (validation hierarchique en cascade) | Le perimetre se limite a une validation a un niveau (manager direct) ; le multi-niveaux sera envisage en v2 |
| HP-08 | Calcul automatique de la distance via API de cartographie (Google Maps, etc.) | La distance est saisie manuellement ; l'integration cartographique est prevue en v2 |
| HP-09 | Gestion des taux de change en temps reel | Les taux de change sont geres manuellement ; l'integration d'un flux de taux est hors perimetre |

---

## 7. Regles Metier

### RM-01 : Gestion des statuts

| Regle | Description |
|---|---|
| RM-01.1 | Une note de frais est creee au statut **Brouillon**. |
| RM-01.2 | Seul le collaborateur proprietaire peut modifier ou supprimer une note au statut Brouillon. |
| RM-01.3 | La soumission fait passer la note de Brouillon a **Soumise**. La note devient non modifiable. |
| RM-01.4 | Le manager peut valider (passage a **Validee**) ou refuser (passage a **Refusee**) une note Soumise. |
| RM-01.5 | Le refus necessite obligatoirement un motif textuel. |
| RM-01.6 | Une note refusee repasse au statut **Brouillon** pour permettre la correction et la resoumission. |
| RM-01.7 | L'administrateur peut marquer une note validee comme **Remboursee**. |
| RM-01.8 | Les transitions de statut sont unidirectionnelles, sauf le retour de Refusee a Brouillon. |

### RM-02 : Calculs de montants

| Regle | Description |
|---|---|
| RM-02.1 | Montant TTC = Montant HT + (Montant HT x Taux TVA / 100). |
| RM-02.2 | Le montant HT et le montant TTC sont lies : la modification de l'un recalcule l'autre. |
| RM-02.3 | Les taux de TVA disponibles sont : 0%, 5.5%, 10%, 20% (configurables par entite). |
| RM-02.4 | Les montants sont arrondis a 2 decimales (arrondi au centime le plus proche). |
| RM-02.5 | La devise par defaut est celle de l'entite ; la conversion de devise n'est pas automatique. |

### RM-03 : Frais kilometriques

| Regle | Description |
|---|---|
| RM-03.1 | Montant = Distance (km) x Taux kilometrique de la tranche de puissance fiscale. |
| RM-03.2 | Si l'option aller-retour est cochee, Distance effective = Distance saisie x 2. |
| RM-03.3 | Les frais kilometriques ne sont pas soumis a TVA (taux = 0%). |
| RM-03.4 | Le bareme kilometrique est defini dans la politique de remboursement de l'entite. |
| RM-03.5 | Le bareme par defaut suit les tranches : 3CV, 4CV, 5CV, 6CV, 7CV et plus. |

### RM-04 : Politique de remboursement

| Regle | Description |
|---|---|
| RM-04.1 | Les plafonds sont verifies au moment de la saisie (alerte) et de la soumission (blocage optionnel). |
| RM-04.2 | Un justificatif est requis pour la soumission si la politique l'exige pour la categorie concernee. |
| RM-04.3 | La politique applicable a une note de frais est celle en vigueur a la date de creation de la note. |
| RM-04.4 | En l'absence de politique configuree, aucun plafond n'est applique et le justificatif n'est pas obligatoire. |

### RM-05 : Droits et visibilite

| Regle | Description |
|---|---|
| RM-05.1 | Un collaborateur ne voit que ses propres notes de frais. |
| RM-05.2 | Un manager voit les notes de frais de tous les collaborateurs sous sa responsabilite directe. |
| RM-05.3 | Un administrateur voit toutes les notes de frais de l'entite. |
| RM-05.4 | Les justificatifs ne sont accessibles qu'au collaborateur proprietaire, a son manager et aux administrateurs. |
| RM-05.5 | L'export comptable est reserve aux roles Administrateur et Comptable. |

### RM-06 : Imputation projet

| Regle | Description |
|---|---|
| RM-06.1 | L'imputation au projet n'est effective qu'apres validation de la note de frais. |
| RM-06.2 | Seuls les projets au statut "Actif" ou "En cours" sont proposables pour l'association. |
| RM-06.3 | Une note de frais non associee a un projet est imputee aux frais generaux de l'entite. |
| RM-06.4 | Le changement de projet sur une note validee est interdit (necessite un refus et une resoumission). |

---

## 8. Criteres Globaux d'Acceptation

### Performance

| # | Critere | Seuil |
|---|---|---|
| CG-01 | Temps de chargement de la liste des notes de frais | < 2 secondes pour 500 notes |
| CG-02 | Temps de creation/modification d'une note de frais | < 1 seconde (hors upload de justificatif) |
| CG-03 | Temps d'upload d'un justificatif de 5 Mo | < 5 secondes en connexion standard |
| CG-04 | Temps de generation d'un export CSV (1000 notes) | < 10 secondes |
| CG-05 | Temps de generation d'un export PDF avec justificatifs (100 notes) | < 30 secondes |

### Accessibilite et ergonomie

| # | Critere | Seuil |
|---|---|---|
| CG-06 | Le module est accessible via un navigateur desktop moderne (Chrome, Firefox, Safari, Edge) | Compatibilite testee et validee sur les 4 navigateurs |
| CG-07 | Le module est utilisable sur tablette et mobile (responsive design) | L'interface s'adapte aux ecrans de 768px et 375px de large |
| CG-08 | Les messages d'erreur sont explicites et guident l'utilisateur vers la correction | Chaque champ en erreur affiche un message contextuel |
| CG-09 | Les actions critiques (suppression, soumission) demandent une confirmation | Une modale de confirmation s'affiche avant l'execution |

### Securite

| # | Critere | Seuil |
|---|---|---|
| CG-10 | Les justificatifs sont stockes de maniere securisee avec acces controle | Les URLs de justificatifs sont signees et expirent apres un delai |
| CG-11 | Les droits d'acces sont verifies cote serveur pour chaque operation | Toute tentative d'acces non autorise retourne une erreur 403 |
| CG-12 | Les donnees sensibles sont transmises via HTTPS | Aucune requete HTTP non securisee n'est emise |

---

## 9. Definition of Done (DoD)

Une User Story est consideree comme terminee ("Done") lorsque l'ensemble des criteres suivants sont remplis :

| # | Critere DoD |
|---|---|
| DoD-01 | Tous les criteres d'acceptation de la User Story sont implementes et verifies |
| DoD-02 | Le code est revise par au moins un pair (code review approuvee) |
| DoD-03 | Les tests unitaires sont ecrits et passent avec un taux de couverture >= 80% |
| DoD-04 | Les tests d'integration sont ecrits et passent |
| DoD-05 | Les tests end-to-end (E2E) couvrent les parcours critiques de la User Story |
| DoD-06 | L'interface utilisateur est conforme aux maquettes validees (design review) |
| DoD-07 | L'interface est responsive et testee sur desktop, tablette et mobile |
| DoD-08 | Les messages d'erreur et les libelles sont conformes au glossaire de l'application |
| DoD-09 | La documentation technique (API, composants) est a jour |
| DoD-10 | La fonctionnalite est deployee et testee sur l'environnement de recette |
| DoD-11 | Aucun bug bloquant ou majeur n'est ouvert sur la User Story |
| DoD-12 | Les criteres de performance sont valides (cf. Criteres Globaux) |
| DoD-13 | Les regles de securite et d'acces sont implementees et testees |

---

## 10. Dependances

### Dependances entrantes (cet EPIC depend de)

| EPIC / Module | Nature de la dependance | Impact |
|---|---|---|
| **EPIC-002 Projets** | Liste des projets actifs pour l'association note de frais / projet | Bloquant : impossible d'associer une note a un projet si le module Projets n'est pas operationnel |
| **EPIC-007 Couts** | Imputation des couts valides au suivi financier du projet | Bloquant pour l'imputation : les notes validees doivent remonter dans les couts projet |
| **EPIC-012 Validation** | Workflow de validation generique (notifications, transitions de statut) | Bloquant : le workflow de validation doit etre disponible pour gerer les transitions de statut |
| **Module Utilisateurs / Equipes** | Organigramme (relation collaborateur/manager), roles et permissions | Bloquant : necessaire pour determiner les droits d'acces et le routage des validations |
| **Module Entites** | Configuration de l'entite (devise, parametres) | Bloquant : la devise par defaut et les parametres d'entite sont prerequis |
| **Infrastructure de stockage** | Stockage objet (S3 ou equivalent) pour les justificatifs | Bloquant : l'upload de justificatifs necessite un service de stockage operationnel |

### Dependances sortantes (d'autres EPICs dependent de cet EPIC)

| EPIC / Module | Nature de la dependance | Impact |
|---|---|---|
| **EPIC-007 Couts** | Alimentation des couts projet avec les notes de frais validees | Les couts projet integrent les notes de frais pour le calcul de rentabilite |
| **Module Comptabilite** (futur) | Export des notes de frais pour integration comptable | L'export CSV servira de base pour l'integration automatique future |
| **Module Reporting** (futur) | Donnees de depenses pour les tableaux de bord et rapports | Les donnees de notes de frais alimenteront les indicateurs de gestion |

### Dependances techniques

| Composant | Description | Statut |
|---|---|---|
| Service de stockage objet | AWS S3, MinIO ou equivalent pour les justificatifs | A confirmer |
| Service de notification | Systeme de notifications in-app et email | Existant (a integrer) |
| Service d'authentification | Gestion des tokens et des sessions utilisateur | Existant |
| Base de donnees | PostgreSQL (ou equivalent) pour le stockage des donnees | Existant |

---

## 11. Modele de Donnees

### 11.1 Table `expense_report` (Note de frais)

| Colonne | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK, NOT NULL | Identifiant unique de la note de frais |
| `employee_id` | UUID | FK -> users.id, NOT NULL | Identifiant du collaborateur declarant |
| `entity_id` | UUID | FK -> entities.id, NOT NULL | Identifiant de l'entite du collaborateur |
| `project_id` | UUID | FK -> projects.id, NULLABLE | Identifiant du projet associe (optionnel) |
| `category` | VARCHAR(50) | NOT NULL, CHECK IN ('transport', 'repas', 'hebergement', 'fournitures', 'telecommunications', 'divers') | Categorie de la depense |
| `description` | TEXT | NOT NULL | Description / motif de la depense |
| `amount_ht` | DECIMAL(12,2) | NOT NULL, >= 0 | Montant hors taxes |
| `vat_rate` | DECIMAL(5,2) | NOT NULL, >= 0 | Taux de TVA applique (en %) |
| `vat_amount` | DECIMAL(12,2) | NOT NULL, >= 0 | Montant de la TVA |
| `amount_ttc` | DECIMAL(12,2) | NOT NULL, >= 0 | Montant toutes taxes comprises |
| `currency` | VARCHAR(3) | NOT NULL, DEFAULT 'EUR' | Code devise ISO 4217 |
| `expense_date` | DATE | NOT NULL | Date de la depense |
| `status` | VARCHAR(20) | NOT NULL, DEFAULT 'draft', CHECK IN ('draft', 'submitted', 'validated', 'rejected', 'reimbursed') | Statut de la note de frais |
| `rejection_reason` | TEXT | NULLABLE | Motif de refus (obligatoire si statut = rejected) |
| `submitted_at` | TIMESTAMP | NULLABLE | Date et heure de soumission |
| `validated_by` | UUID | FK -> users.id, NULLABLE | Identifiant du manager ayant valide/refuse |
| `validated_at` | TIMESTAMP | NULLABLE | Date et heure de validation/refus |
| `reimbursed_at` | TIMESTAMP | NULLABLE | Date et heure de confirmation de remboursement |
| `reimbursed_by` | UUID | FK -> users.id, NULLABLE | Identifiant de l'administrateur ayant confirme le remboursement |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date de creation |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date de derniere modification |

**Index** :
- `idx_expense_report_employee` sur `employee_id`
- `idx_expense_report_entity` sur `entity_id`
- `idx_expense_report_project` sur `project_id`
- `idx_expense_report_status` sur `status`
- `idx_expense_report_date` sur `expense_date`
- `idx_expense_report_category` sur `category`

---

### 11.2 Table `expense_receipt` (Justificatif)

| Colonne | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK, NOT NULL | Identifiant unique du justificatif |
| `expense_report_id` | UUID | FK -> expense_report.id, NOT NULL, ON DELETE CASCADE | Identifiant de la note de frais associee |
| `file_name` | VARCHAR(255) | NOT NULL | Nom original du fichier |
| `file_type` | VARCHAR(10) | NOT NULL, CHECK IN ('jpeg', 'jpg', 'png', 'pdf') | Type de fichier |
| `file_size` | INTEGER | NOT NULL, CHECK <= 10485760 | Taille du fichier en octets (max 10 Mo) |
| `storage_url` | TEXT | NOT NULL | URL de stockage (S3 ou equivalent) |
| `uploaded_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date d'upload |

**Index** :
- `idx_expense_receipt_report` sur `expense_report_id`

---

### 11.3 Table `expense_mileage` (Frais kilometriques)

| Colonne | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK, NOT NULL | Identifiant unique |
| `expense_report_id` | UUID | FK -> expense_report.id, NOT NULL, UNIQUE, ON DELETE CASCADE | Lien vers la note de frais (relation 1:1) |
| `departure` | VARCHAR(255) | NOT NULL | Lieu de depart |
| `arrival` | VARCHAR(255) | NOT NULL | Lieu d'arrivee |
| `distance_km` | DECIMAL(8,1) | NOT NULL, > 0 | Distance parcourue en km (saisie) |
| `is_round_trip` | BOOLEAN | NOT NULL, DEFAULT FALSE | Aller-retour |
| `total_distance_km` | DECIMAL(8,1) | NOT NULL, > 0 | Distance totale (x2 si aller-retour) |
| `fiscal_power` | VARCHAR(10) | NOT NULL | Puissance fiscale du vehicule (ex : '5CV') |
| `rate_applied` | DECIMAL(6,4) | NOT NULL | Taux kilometrique applique (EUR/km) |

**Index** :
- `idx_expense_mileage_report` sur `expense_report_id`

---

### 11.4 Table `expense_policy` (Politique de remboursement)

| Colonne | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK, NOT NULL | Identifiant unique de la politique |
| `entity_id` | UUID | FK -> entities.id, NOT NULL | Identifiant de l'entite |
| `category` | VARCHAR(50) | NOT NULL | Categorie de frais concernee |
| `max_amount_per_expense` | DECIMAL(12,2) | NULLABLE | Plafond par note de frais (NULL = pas de plafond) |
| `max_amount_per_day` | DECIMAL(12,2) | NULLABLE | Plafond par jour (NULL = pas de plafond) |
| `max_amount_per_month` | DECIMAL(12,2) | NULLABLE | Plafond par mois (NULL = pas de plafond) |
| `requires_receipt` | BOOLEAN | NOT NULL, DEFAULT TRUE | Justificatif obligatoire pour cette categorie |
| `block_on_exceed` | BOOLEAN | NOT NULL, DEFAULT FALSE | Bloquer la soumission en cas de depassement de plafond |
| `effective_date` | DATE | NOT NULL | Date d'effet de cette politique |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date de creation |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date de derniere modification |

**Index** :
- `idx_expense_policy_entity` sur `entity_id`
- `idx_expense_policy_category` sur `(entity_id, category, effective_date)`

**Contrainte d'unicite** : `UNIQUE(entity_id, category, effective_date)`

---

### 11.5 Table `expense_mileage_rate` (Bareme kilometrique)

| Colonne | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK, NOT NULL | Identifiant unique |
| `entity_id` | UUID | FK -> entities.id, NOT NULL | Identifiant de l'entite |
| `fiscal_power` | VARCHAR(10) | NOT NULL | Tranche de puissance fiscale (ex : '3CV', '4CV', '5CV', '6CV', '7CV+') |
| `rate_per_km` | DECIMAL(6,4) | NOT NULL, > 0 | Taux par kilometre (en devise de l'entite) |
| `effective_date` | DATE | NOT NULL | Date d'effet du bareme |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date de creation |

**Index** :
- `idx_mileage_rate_entity` sur `entity_id`

**Contrainte d'unicite** : `UNIQUE(entity_id, fiscal_power, effective_date)`

---

### 11.6 Table `expense_status_history` (Historique des statuts)

| Colonne | Type | Contraintes | Description |
|---|---|---|---|
| `id` | UUID | PK, NOT NULL | Identifiant unique |
| `expense_report_id` | UUID | FK -> expense_report.id, NOT NULL, ON DELETE CASCADE | Identifiant de la note de frais |
| `from_status` | VARCHAR(20) | NULLABLE | Statut precedent (NULL pour la creation) |
| `to_status` | VARCHAR(20) | NOT NULL | Nouveau statut |
| `changed_by` | UUID | FK -> users.id, NOT NULL | Utilisateur ayant effectue le changement |
| `comment` | TEXT | NULLABLE | Commentaire (motif de refus, etc.) |
| `changed_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Date et heure du changement |

**Index** :
- `idx_status_history_report` sur `expense_report_id`
- `idx_status_history_date` sur `changed_at`

---

### Diagramme des relations

```
expense_policy ────────────┐
expense_mileage_rate ──────┤
                           ▼
                       [entities]
                           ▲
                           │
expense_report ────────────┘
    │   │   │
    │   │   └──── expense_receipt (1:N)
    │   │
    │   └──────── expense_mileage (1:1, optionnel)
    │
    └──────────── expense_status_history (1:N)
    │
    ├── FK → users (employee_id)
    ├── FK → users (validated_by)
    ├── FK → users (reimbursed_by)
    └── FK → projects (project_id, optionnel)
```

---

## 12. Estimation

### Estimation globale

| Parametre | Valeur |
|---|---|
| **Effort total estime** | 3 a 5 semaines |
| **Nombre de sprints** | 2 a 3 sprints (sprints de 2 semaines) |
| **Taille de l'equipe recommandee** | 2-3 developpeurs (1 backend, 1 frontend, 1 fullstack) + 1 QA |
| **Complexite globale** | Moyenne a elevee |

### Estimation detaillee par User Story

| User Story | Complexite | Effort backend (j) | Effort frontend (j) | Effort QA (j) | Total (j) |
|---|---|---|---|---|---|
| **US-NF01** Saisie d'une note de frais | Moyenne | 2 | 3 | 1 | 6 |
| **US-NF02** Upload de justificatif | Moyenne | 2 | 2 | 1 | 5 |
| **US-NF03** Association a un projet | Faible | 1 | 1 | 0.5 | 2.5 |
| **US-NF04** Soumission pour validation | Elevee | 3 | 2 | 1.5 | 6.5 |
| **US-NF05** Vue consolidee manager/agence | Elevee | 2 | 3 | 1.5 | 6.5 |
| **US-NF06** Historique et filtrage | Moyenne | 2 | 2 | 1 | 5 |
| **US-NF07** Export comptable | Moyenne | 3 | 1 | 1 | 5 |
| **US-NF08** Frais kilometriques | Moyenne | 2 | 2 | 1 | 5 |
| **US-NF09** Politique de remboursement | Elevee | 3 | 2 | 1.5 | 6.5 |
| **US-NF10** Suivi des remboursements | Moyenne | 1.5 | 2 | 1 | 4.5 |
| **Total** | | **21.5** | **20** | **11** | **52.5 jours** |

### Repartition par sprint

#### Sprint 1 (Semaines 1-2) -- Fondations et saisie

| Activite | User Stories | Objectif |
|---|---|---|
| Mise en place du modele de donnees | -- | Creation des tables, migrations, seeders |
| API CRUD de base | US-NF01 | Endpoints de creation, lecture, modification, suppression |
| Formulaire de saisie frontend | US-NF01 | Interface de creation et modification d'une note de frais |
| Upload de justificatifs | US-NF02 | Integration du stockage objet et interface d'upload |
| Association projet | US-NF03 | Champ de selection avec autocomplete |
| Tests et recette Sprint 1 | US-NF01, NF02, NF03 | Tests unitaires, integration, recette fonctionnelle |

#### Sprint 2 (Semaines 3-4) -- Workflow et vues

| Activite | User Stories | Objectif |
|---|---|---|
| Workflow de validation | US-NF04 | Machine a etats, transitions, notifications |
| Vue consolidee manager | US-NF05 | Interface manager avec indicateurs et actions de validation |
| Vue agence administrateur | US-NF05 | Interface administrateur avec vision globale |
| Filtres et recherche | US-NF06 | Panneau de filtres multi-criteres |
| Suivi des remboursements | US-NF10 | Statut rembourse, marquage en lot, notifications |
| Tests et recette Sprint 2 | US-NF04, NF05, NF06, NF10 | Tests unitaires, integration, recette fonctionnelle |

#### Sprint 3 (Semaine 5) -- Fonctionnalites avancees et finalisation

| Activite | User Stories | Objectif |
|---|---|---|
| Export comptable CSV et PDF | US-NF07 | Generation et telechargement des exports |
| Frais kilometriques | US-NF08 | Sous-formulaire dedie et calcul automatique |
| Politique de remboursement | US-NF09 | Interface de configuration et moteur de regles |
| Tests end-to-end | Toutes | Parcours complets de bout en bout |
| Corrections de bugs et ajustements | Toutes | Stabilisation, ajustements UX, optimisation des performances |
| Recette finale et mise en production | Toutes | Validation metier, deploiement |

### Risques identifies

| # | Risque | Probabilite | Impact | Mitigation |
|---|---|---|---|---|
| R1 | Complexite du workflow de validation et interactions avec EPIC-012 | Moyenne | Eleve | Cadrage technique en amont avec l'equipe EPIC-012 |
| R2 | Performance de la vue consolidee agence avec un grand volume de donnees | Faible | Moyen | Pagination, indexation des tables, requetes optimisees |
| R3 | Gestion du stockage des justificatifs (volume, securite) | Faible | Moyen | Dimensionnement du stockage, politique de retention, URLs signees |
| R4 | Compatibilite de l'export CSV avec les differents logiciels comptables | Moyenne | Faible | Tests avec les logiciels les plus courants, encodage UTF-8 BOM |
| R5 | Disponibilite du module Projets (EPIC-002) pour l'association | Faible | Eleve | Developpement en parallele avec des donnees de test ; integration finale en Sprint 2 |

---

*Document redige le 26 fevrier 2026 -- EPIC-013 Notes de frais -- Version 1.0*
