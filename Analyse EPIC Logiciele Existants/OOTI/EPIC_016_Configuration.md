# EPIC — Module Configuration & Administration

**Application OOTI** — Gestion de projets pour cabinets d'architecture
**Version 1.0** — Fevrier 2026

---

## 1. Identification

| Champ | Valeur |
|---|---|
| **Nom de l'EPIC** | Configuration & Administration |
| **Reference** | EPIC-016 |
| **Module parent** | Transversal |
| **Priorite** | Haute |
| **Responsable produit** | Chef de produit OOTI |
| **Date de creation** | 26/02/2026 |
| **Derniere mise a jour** | 26/02/2026 |
| **Statut** | En redaction |
| **EPICs lies** | EPIC-001 (Authentification & Utilisateurs), EPIC-002 (Projets), EPIC-003 (Honoraires), EPIC-004 (Facturation), EPIC-005 (Temps & Activite), EPIC-006 (Equipe & RH), EPIC-007 (Clients & Contacts), EPIC-008 (Budgets & Couts), EPIC-009 (Rapports & Tableaux de bord), EPIC-010 (Documents & GED), EPIC-011 (Planification), EPIC-012 (Notifications), EPIC-013 (API & Integrations), EPIC-014 (Abonnement & Billing), EPIC-015 (Onboarding) |

---

## 2. Contexte & Problematique

Les cabinets d'architecture operent dans un environnement reglementaire et organisationnel complexe. Chaque agence possede ses propres conventions : nomenclature de numerotation des factures, phases de projet specifiques (esquisse, APS, APD, PRO, DCE, DET, AOR, etc.), regles de saisie de temps, jours feries regionaux, taux de TVA applicables, et identite visuelle distincte. Nombre de ces cabinets fonctionnent en multi-entites (plusieurs agences, filiales ou bureaux), chacune avec ses parametres propres.

**Problematiques identifiees :**

- **Rigidite des systemes existants** : Les outils generiques ne permettent pas de personnaliser finement les parametres metier specifiques a l'architecture (phases de loi MOP, types d'honoraires, nomenclature BIM, etc.). Les cabinets doivent alors multiplier les outils ou recourir a des solutions manuelles.
- **Complexite d'administration** : La gestion de multiples entites, collaborateurs, droits d'acces et parametres se fait souvent via des fichiers Excel ou des demandes au support technique, generant des delais et des erreurs.
- **Onboarding laborieux** : Les nouveaux cabinets passent plusieurs semaines a configurer leur environnement, sans guide structure. De nombreux parametres essentiels (conditions de paiement, phases projet, modeles de facturation) restent aux valeurs par defaut, sous-exploitant l'outil.
- **Absence de centralisation** : Les parametres sont disperses entre differents modules, rendant difficile une vision globale de la configuration de l'agence et la coherence inter-modules.
- **Import/export limites** : La migration depuis un ancien systeme ou l'extraction de donnees pour audit/comptabilite necessite des interventions manuelles couteuses.
- **Gestion des integrations fragmentee** : Les connexions avec les outils tiers (logiciels de comptabilite, calendriers, outils BIM) sont gerees au cas par cas, sans tableau de bord centralise.

L'EPIC-016 vise a fournir un module centralise de configuration et d'administration qui permet aux dirigeants et administrateurs de cabinets d'architecture de personnaliser integralement leur environnement OOTI, d'automatiser l'onboarding et de gerer l'ensemble des parametres transversaux depuis une interface unique et intuitive.

---

## 3. Objectif

### 3.1 Objectif principal

Concevoir et developper un module de configuration et d'administration centralise qui permet aux administrateurs de personnaliser l'integralite des parametres de l'application OOTI, de gerer les entites, les collaborateurs, les integrations et l'abonnement depuis une interface unifiee accessible via l'icone engrenage.

### 3.2 Objectifs specifiques

1. **Centraliser tous les parametres** dans une interface unique avec navigation par sidebar structuree (Profil, General, Projets, Facturation, Temps, Equipe, Donnees, Collaborateurs, Integrations, Modules, Abonnement, Assistance).
2. **Permettre la personnalisation complete** de chaque module (phases de projet, conditions de facturation, regles de temps, charte graphique) sans intervention technique.
3. **Offrir un onboarding guide** en 10 etapes pour accompagner les nouveaux cabinets dans la configuration initiale de leur environnement.
4. **Supporter le multi-entites** avec heritage et surcharge de parametres entre entites parentes et filiales.
5. **Fournir des outils d'import/export en masse** pour faciliter la migration de donnees et l'extraction pour audit.
6. **Centraliser la gestion des integrations** API tierces avec monitoring de l'etat de connexion.
7. **Permettre l'activation/desactivation granulaire des modules** pour adapter l'application aux besoins reels de chaque cabinet.
8. **Garantir la securite** avec gestion du profil, authentification 2FA, et controle des sessions actives.

### 3.3 Indicateurs de succes

| Indicateur | Cible |
|---|---|
| Taux de completion de l'onboarding | > 80% des nouveaux comptes |
| Temps moyen de configuration initiale | < 2 heures (vs. plusieurs jours) |
| Nombre de tickets support lies a la configuration | Reduction de 60% |
| Taux d'adoption du 2FA | > 50% des utilisateurs administrateurs |
| Taux de satisfaction des administrateurs sur le module | > 4/5 |
| Temps moyen d'import de donnees en masse | < 10 minutes pour 1000 enregistrements |

---

## 4. Perimetre Fonctionnel

### 4.1 Vue d'ensemble de la sidebar Configuration

L'acces aux parametres globaux se fait via l'icone engrenage dans la barre de navigation principale. La sidebar gauche presente les sections suivantes :

```
Parametres
|
|-- Profil
|   |-- Informations personnelles
|   |-- Securite
|   |-- Notifications
|
|-- General
|   |-- Informations de l'entite/agence
|   |-- Adresse et coordonnees
|   |-- Logo et charte graphique
|   |-- Devises et langues
|   |-- TVA et reglementation
|
|-- Projets
|   |-- Phases par defaut
|   |-- Etiquettes
|   |-- Statuts personnalises
|
|-- Facturation
|   |-- Numerotation
|   |-- Conditions de paiement
|   |-- Mentions legales
|   |-- Modeles de facture (PDF)
|
|-- Temps
|   |-- Jours ouvres
|   |-- Heures par jour
|   |-- Types de temps
|   |-- Jours feries
|
|-- Equipe
|   |-- Entites / Agences
|   |-- Departements
|
|-- Donnees
|   |-- Import en masse
|   |-- Export en masse
|
|-- Collaborateurs
|   |-- Gestion des comptes utilisateurs
|
|-- Integrations
|   |-- Connexions API tierces
|
|-- Modules
|   |-- Activation / Desactivation
|
|-- Abonnement
|   |-- Plan et facturation
|
|-- Assistance
|   |-- Support et centre d'aide
```

### 4.2 Fonctionnalites detaillees

#### 4.2.1 Profil utilisateur
- Consultation et modification des informations personnelles (prenom, nom, email, telephone, avatar)
- Changement d'adresse email avec confirmation par double opt-in
- Changement de mot de passe avec verification de l'ancien mot de passe
- Selection de la langue d'interface (francais, anglais, espagnol, allemand, portugais)
- Selection du fuseau horaire
- Upload et recadrage de la photo de profil (avatar)

#### 4.2.2 Securite
- Activation/desactivation de l'authentification a deux facteurs (2FA) via application TOTP (Google Authenticator, Authy)
- Generation de codes de secours pour le 2FA
- Visualisation des sessions actives (appareil, navigateur, IP, date de derniere activite)
- Revocation de sessions individuelles ou de toutes les sessions
- Historique des connexions recentes (30 derniers jours)

#### 4.2.3 Preferences de notifications
- Configuration granulaire par type d'evenement :
  - Projets : nouveau projet, changement de statut, echeance proche, affectation
  - Facturation : facture emise, paiement recu, relance, echeance
  - Temps : rappel de saisie, validation, depassement de budget temps
  - Equipe : nouveau collaborateur, absence, demande de conge
  - Systeme : mise a jour, maintenance, securite
- Choix du canal par evenement : email, notification in-app, les deux, ou aucun
- Frequence des recapitulatifs email (temps reel, quotidien, hebdomadaire)
- Horaires de non-perturbation (ne pas recevoir de notifications entre X et Y)

#### 4.2.4 Parametres generaux agence
- Raison sociale et forme juridique
- Numero SIRET / SIREN (ou equivalent selon le pays)
- Adresse du siege social (avec autocompletion)
- Numero de TVA intracommunautaire
- Coordonnees (telephone, email de contact, site web)
- Devise par defaut (EUR, USD, GBP, CHF, etc.) et devises secondaires autorisees
- Langue par defaut de l'entite
- Configuration des taux de TVA applicables (taux standard, reduit, super-reduit, exonere)

#### 4.2.5 Charte graphique
- Upload du logo de l'agence (formats PNG, SVG, JPG ; taille max 5 Mo)
- Logo en version claire et sombre
- Definition des couleurs de la charte graphique :
  - Couleur principale (primaire)
  - Couleur secondaire
  - Couleur d'accentuation
  - Selecteur de couleur (color picker) + saisie hexadecimale
- Selection des polices de caracteres pour les documents generes (propositions, factures, rapports)
- Apercu en temps reel de la charte sur un modele de document

#### 4.2.6 Configuration des projets par defaut
- Definition des phases de projet par defaut avec possibilite de personnalisation :
  - Phases loi MOP pre-configurees : ESQ, APS, APD, PRO, ACT, VISA, DET, AOR, DOE
  - Phases personnalisees : ajout, renommage, reordonnancement, suppression
  - Pourcentage d'avancement par phase (repartition par defaut)
- Gestion des etiquettes (tags) :
  - Creation d'etiquettes avec nom et couleur
  - Categories d'etiquettes (type de projet, secteur, priorite)
  - Etiquettes partagees entre entites ou specifiques a une entite
- Gestion des statuts de projet personnalises :
  - Statuts par defaut : Brouillon, En cours, En pause, Termine, Archive
  - Ajout de statuts personnalises avec couleur et icone
  - Definition du workflow de transition entre statuts (quels passages sont autorises)

#### 4.2.7 Configuration de la facturation
- Prefixe et format de numerotation des factures (ex: FA-2026-001, ARCH-001)
- Numerotation automatique sequentielle avec remise a zero annuelle optionnelle
- Conditions de paiement par defaut :
  - Delais (30 jours, 45 jours, 60 jours, personnalise)
  - Penalites de retard (taux, indemnite forfaitaire)
  - Escompte pour paiement anticipe
- Mentions legales obligatoires (personnalisables) :
  - Mentions de TVA
  - Assurance professionnelle (numero de police, compagnie)
  - Ordre des architectes (numero d'inscription)
  - Mentions specifiques (IBAN, RIB, conditions generales)
- Modeles de facture PDF :
  - Modeles pre-configures (classique, moderne, minimaliste)
  - Personnalisation de la mise en page (position du logo, colonnes, pied de page)
  - Apercu avant impression
  - Modeles distincts par type de document (facture, avoir, decompte, proforma)

#### 4.2.8 Configuration du temps
- Nombre d'heures par jour ouvre (7h, 7.5h, 8h ou personnalise)
- Nombre d'heures par semaine (35h, 37.5h, 39h, 40h ou personnalise)
- Jours ouvres de la semaine (selection des jours travailles)
- Gestion des jours feries :
  - Calendrier pre-configure par pays (France, Belgique, Suisse, etc.)
  - Ajout de jours feries specifiques a l'entite (ponts, fermetures exceptionnelles)
  - Jours feries recurrents vs. ponctuels
- Types de temps pre-configures :
  - Temps productif (facturable) : conception, etudes techniques, chantier, reunion client
  - Temps non productif (non facturable) : administratif, formation, deplacement, commercial
  - Ajout de types de temps personnalises avec code, nom, categorie et facturable/non facturable
- Arrondi de saisie (au quart d'heure, a la demi-heure, libre)
- Rappel automatique de saisie de temps (frequence et horaire)

#### 4.2.9 Configuration equipe et entites
- **Multi-entites :**
  - Creation et gestion de plusieurs entites/agences au sein d'un meme compte
  - Hierarchie parent-enfant entre entites
  - Heritage de parametres de l'entite parente avec possibilite de surcharge
  - Bascule d'entite active dans l'interface
- **Departements :**
  - Creation de departements au sein de chaque entite (Architecture, Urbanisme, Design interieur, BIM, Administration, etc.)
  - Affectation d'un responsable de departement
  - Codes de departement pour la ventilation comptable

#### 4.2.10 Import de donnees en masse
- Import par type de donnees :
  - Projets (nom, client, phases, budget, dates)
  - Clients et contacts (raison sociale, adresses, contacts)
  - Collaborateurs (nom, email, role, departement)
  - Saisies de temps (collaborateur, projet, date, duree, type)
  - Factures historiques (numero, montant, date, statut)
- Formats supportes : CSV, XLSX
- Televersement du fichier avec detection automatique des colonnes
- Modeles de fichiers d'import telechargeables (templates pre-formates)
- Etape de mapping des colonnes (correspondance entre colonnes du fichier et champs OOTI)
- Apercu des donnees avant import (premieres lignes avec validation)
- Validation des donnees :
  - Detection des doublons (par nom, email, numero de projet)
  - Verification des formats (dates, emails, montants)
  - Identification des champs obligatoires manquants
  - Rapport d'erreurs avec numero de ligne et description de l'erreur
- Import en arriere-plan avec barre de progression
- Rapport d'import final (lignes importees, ignorees, en erreur)
- Possibilite d'annuler un import (rollback) dans les 24 heures

#### 4.2.11 Export de donnees
- Export par type de donnees (memes categories que l'import)
- Filtres d'export : par date, par entite, par statut, par projet
- Formats d'export : CSV, XLSX, PDF (pour rapports)
- Export programme (quotidien, hebdomadaire, mensuel) avec envoi par email
- Export de l'ensemble des donnees du compte (export RGPD / portabilite)

#### 4.2.12 Gestion des collaborateurs
- Liste globale des comptes utilisateurs avec recherche et filtres
- Informations affichees : nom, email, role, entite, departement, statut (actif/inactif), derniere connexion
- Actions : inviter, desactiver, reactiver, modifier le role, changer d'entite/departement
- Invitation par email avec lien d'activation
- Gestion des roles : Administrateur, Manager, Collaborateur, Lecteur, Comptable
- Affectation a une ou plusieurs entites

#### 4.2.13 Gestion des integrations API
- Catalogue des integrations disponibles :
  - Comptabilite : Sage, QuickBooks, Xero, Pennylane
  - Calendrier : Google Calendar, Outlook Calendar
  - Stockage : Google Drive, Dropbox, OneDrive
  - Communication : Slack, Microsoft Teams
  - BIM : Autodesk BIM 360, Revit
  - Autres : Zapier, webhooks personnalises
- Pour chaque integration :
  - Description et fonctionnalites
  - Bouton de connexion / deconnexion (OAuth2 ou cle API)
  - Statut de connexion (connectee, deconnectee, erreur)
  - Date de derniere synchronisation
  - Configuration des parametres de synchronisation (frequence, direction, filtres)
  - Journal des synchronisations avec statut (succes, erreur, avertissement)
- Gestion des webhooks sortants (URL, evenements declencheurs, secret de signature)

#### 4.2.14 Activation/desactivation des modules
- Liste des modules de l'application avec description :
  - Projets, Honoraires, Facturation, Temps, Equipe & RH, Clients, Budgets, Rapports, Documents, Planification
- Toggle d'activation/desactivation pour chaque module
- Avertissement avant desactivation (impact sur les donnees existantes et les fonctionnalites liees)
- Les modules desactives disparaissent de la navigation principale
- Reactivation instantanee sans perte de donnees
- Dependances entre modules signalees (ex: Facturation necessite Projets)

#### 4.2.15 Gestion de l'abonnement
- Affichage du plan actuel (nom du plan, prix, periodicite)
- Nombre d'utilisateurs inclus vs. utilises
- Espace de stockage utilise vs. disponible
- Historique des factures d'abonnement
- Changement de plan (upgrade/downgrade) avec prorata
- Modification du cycle de facturation (mensuel/annuel)
- Mise a jour des informations de paiement
- Annulation de l'abonnement avec periode de retention des donnees

#### 4.2.16 Assistance et support
- Lien vers le centre d'aide (base de connaissances)
- Formulaire de contact support avec categorisation (bug, question, demande de fonctionnalite)
- Chat en direct (si disponible selon le plan)
- Acces a la documentation API
- Changelog et notes de version

#### 4.2.17 Onboarding guide
- Parcours guide en 10 etapes pour les nouveaux comptes :
  1. **Changer le mot de passe** : Inviter l'utilisateur a definir un mot de passe securise
  2. **Personnaliser le compte** : Upload du logo, saisie des informations de l'agence, definition de la charte graphique
  3. **Configurer l'equipe** : Creation des entites, departements, invitation des premiers collaborateurs
  4. **Configurer les projets** : Definition des phases par defaut, etiquettes, statuts
  5. **Configurer la facturation** : Numerotation, conditions de paiement, mentions legales, modele PDF
  6. **Configurer le temps** : Heures/jour, jours ouvres, types de temps, jours feries
  7. **Configurer les couts** : Taux horaires, couts de structure, marges par defaut
  8. **Planifier vos projets** : Creation du premier projet avec l'assistant
  9. **Gestion des donnees** : Import des donnees existantes (projets, clients, collaborateurs)
  10. **Configuration completee** : Resume des parametres, liens vers les ressources d'aide
- Barre de progression globale avec pourcentage de completion
- Possibilite de sauter une etape et d'y revenir plus tard
- Indicateur visuel des etapes completees, en cours et restantes
- Acces a l'onboarding depuis la sidebar a tout moment tant qu'il n'est pas complete
- Tooltips et bulles d'aide contextuelles a chaque etape

---

## 5. User Stories

### US-CF01 : Profil utilisateur

**En tant qu'** utilisateur de OOTI,
**Je veux** pouvoir consulter et modifier mes informations personnelles, ma photo de profil, ma langue d'interface et mon fuseau horaire,
**Afin de** personnaliser mon experience et m'assurer que mes coordonnees sont a jour dans le systeme.

**Criteres d'acceptation :**

1. L'utilisateur accede a la page Profil via l'icone engrenage > section "Profil" > "Informations personnelles" dans la sidebar gauche.
2. Le formulaire affiche les champs : prenom, nom, email, telephone, poste/fonction, et ils sont pre-remplis avec les valeurs actuelles.
3. L'utilisateur peut modifier son prenom, son nom, son telephone et son poste ; les modifications sont sauvegardees au clic sur "Enregistrer" avec un message de confirmation.
4. Le changement d'adresse email declenche l'envoi d'un email de confirmation a la nouvelle adresse ; le changement n'est effectif qu'apres validation du lien dans l'email (double opt-in). L'ancienne adresse reste active tant que la nouvelle n'est pas confirmee.
5. L'utilisateur peut uploader une photo de profil (formats acceptes : JPG, PNG ; taille max : 2 Mo) avec un outil de recadrage circulaire avant la sauvegarde. Un avatar par defaut (initiales) est affiche si aucune photo n'est uploadee.
6. Un selecteur de langue d'interface est disponible avec les options : Francais, English, Espanol, Deutsch, Portugues. Le changement de langue s'applique immediatement a l'ensemble de l'interface sans rechargement complet de la page.
7. Un selecteur de fuseau horaire (liste complete des fuseaux IANA) est disponible avec recherche par ville ou code UTC. Le fuseau selectionne est utilise pour l'affichage de toutes les dates et heures dans l'application.
8. Toutes les validations de formulaire s'effectuent en temps reel cote client (format email, longueur des champs, taille du fichier) avec messages d'erreur explicites sous chaque champ concerne.

---

### US-CF02 : Securite et authentification

**En tant qu'** utilisateur de OOTI,
**Je veux** pouvoir modifier mon mot de passe, activer l'authentification a deux facteurs (2FA) et gerer mes sessions actives,
**Afin de** securiser l'acces a mon compte et proteger les donnees sensibles de l'agence.

**Criteres d'acceptation :**

1. L'utilisateur accede a la page Securite via l'icone engrenage > section "Profil" > "Securite" dans la sidebar gauche.
2. Le changement de mot de passe requiert la saisie de l'ancien mot de passe, du nouveau mot de passe et de sa confirmation. Le nouveau mot de passe doit respecter les regles de complexite : minimum 12 caracteres, au moins une majuscule, une minuscule, un chiffre et un caractere special. Un indicateur de force du mot de passe est affiche en temps reel.
3. L'activation du 2FA s'effectue en 3 etapes : (a) affichage d'un QR code compatible avec les applications TOTP (Google Authenticator, Authy, Microsoft Authenticator), (b) saisie du code a 6 chiffres genere par l'application pour verification, (c) affichage de 10 codes de secours a usage unique que l'utilisateur est invite a telecharger ou copier.
4. La desactivation du 2FA requiert la saisie du mot de passe actuel et d'un code TOTP valide pour confirmation.
5. La section "Sessions actives" affiche la liste de toutes les sessions ouvertes avec : type d'appareil (ordinateur, mobile, tablette), navigateur et version, adresse IP (partiellement masquee), date et heure de la derniere activite, et un indicateur "Session actuelle".
6. L'utilisateur peut revoquer une session individuelle en cliquant sur "Deconnecter cette session" avec une confirmation. Il peut aussi revoquer toutes les sessions sauf la session actuelle via le bouton "Deconnecter toutes les autres sessions".
7. Un historique des 50 dernieres connexions est disponible avec la date, l'heure, l'appareil, l'IP et le statut (succes, echec, 2FA requis). Les tentatives echouees sont mises en evidence visuellement.
8. Si 5 tentatives de connexion echouees consecutives sont detectees, le compte est temporairement verrouille pendant 15 minutes et l'utilisateur est notifie par email.

---

### US-CF03 : Preferences de notifications

**En tant qu'** utilisateur de OOTI,
**Je veux** pouvoir configurer mes preferences de notifications par type d'evenement et par canal de diffusion (email, in-app),
**Afin de** recevoir uniquement les informations pertinentes pour mon role et ne pas etre submerge par des notifications inutiles.

**Criteres d'acceptation :**

1. L'utilisateur accede a la page Notifications via l'icone engrenage > section "Profil" > "Notifications" dans la sidebar gauche.
2. Les notifications sont organisees par categorie dans un tableau : Projets, Facturation, Temps, Equipe, Systeme. Chaque categorie est depliable pour afficher les evenements individuels.
3. Pour chaque type d'evenement, l'utilisateur peut choisir le canal de notification via des cases a cocher : email, notification in-app, les deux, ou aucun. Les modifications sont sauvegardees automatiquement (auto-save) avec un indicateur visuel de sauvegarde.
4. Un selecteur de frequence des recapitulatifs email est disponible : "Temps reel" (envoi immediat), "Quotidien" (resume a 8h00), "Hebdomadaire" (resume le lundi matin). La frequence s'applique globalement a toutes les notifications email non urgentes.
5. Une plage horaire de "Ne pas deranger" est configurable (ex: 20h00 a 8h00) pendant laquelle les notifications in-app sont mises en file d'attente et les emails non urgents sont differes. Les notifications de securite (tentative de connexion suspecte) ignorent cette plage.
6. Un bouton "Tout activer" et un bouton "Tout desactiver" permettent de modifier rapidement l'ensemble des preferences par canal (email ou in-app).
7. L'apercu d'une notification email est disponible pour chaque type d'evenement (bouton "Apercu") afin que l'utilisateur visualise le format du message qu'il recevra.
8. Les notifications critiques (securite, expiration d'abonnement, echec de paiement) ne peuvent pas etre desactivees et sont clairement identifiees comme telles avec un cadenas.

---

### US-CF04 : Parametres generaux agence

**En tant qu'** administrateur d'un cabinet d'architecture,
**Je veux** pouvoir configurer les informations legales, fiscales et generales de mon agence (raison sociale, SIRET, adresse, TVA, devises, langues),
**Afin de** garantir la conformite des documents generes et l'exactitude des informations affichees sur les factures, propositions et rapports.

**Criteres d'acceptation :**

1. L'administrateur accede a la page Parametres generaux via l'icone engrenage > section "General" dans la sidebar gauche.
2. Le formulaire contient les champs : raison sociale, forme juridique (selection parmi SA, SAS, SARL, EURL, SCP, autre), numero SIRET (14 chiffres avec validation du format et de la cle de Luhn), numero SIREN (9 premiers chiffres deduits automatiquement du SIRET), numero de TVA intracommunautaire (format FR + 2 chiffres + SIREN).
3. L'adresse du siege social est saisie avec autocompletion (integration API adresse) et comporte les champs : voie, complement, code postal, ville, pays. L'adresse est stockee de maniere structuree.
4. Les coordonnees comprennent : telephone principal (avec indicatif international), email de contact general, site web (avec validation du format URL).
5. La devise par defaut est selectionnable parmi une liste (EUR, USD, GBP, CHF, CAD, MAD, XOF, etc.) avec le symbole et le format d'affichage correspondants. Des devises secondaires peuvent etre ajoutees pour les projets internationaux.
6. La langue par defaut de l'entite est selectionnable (independamment de la langue d'interface de l'utilisateur) et s'applique aux documents generes (factures, propositions, rapports).
7. La section TVA permet de configurer les taux applicables : taux standard (20% par defaut en France), taux reduit (10%, 5.5%), taux super-reduit (2.1%), exoneration. Chaque taux peut etre renomme et modifie. Un taux par defaut est selectionnable pour les nouvelles factures.
8. Toutes les modifications sont journalisees dans un historique d'audit accessible aux administrateurs, indiquant le champ modifie, l'ancienne valeur, la nouvelle valeur, l'utilisateur et la date/heure.

---

### US-CF05 : Charte graphique (logo, couleurs, polices)

**En tant qu'** administrateur d'un cabinet d'architecture,
**Je veux** pouvoir configurer l'identite visuelle de mon agence (logo, couleurs de la charte, polices de caracteres) dans les parametres,
**Afin que** tous les documents generes par OOTI (factures, propositions, rapports) refletent l'image professionnelle de mon cabinet.

**Criteres d'acceptation :**

1. L'administrateur accede a la section charte graphique via l'icone engrenage > section "General" > sous-section "Charte graphique".
2. L'upload du logo est possible dans les formats PNG, SVG et JPG, avec une taille maximale de 5 Mo. Un outil de recadrage permet d'ajuster le cadrage. Deux versions du logo peuvent etre uploadees : version claire (pour fonds sombres) et version sombre (pour fonds clairs).
3. Un color picker (selecteur de couleur) permet de definir trois couleurs de charte : couleur primaire, couleur secondaire et couleur d'accentuation. Chaque couleur peut etre saisie via le selecteur visuel, en code hexadecimal (#RRGGBB) ou en code RGB. Le contraste entre les couleurs est verifie pour garantir la lisibilite (ratio WCAG AA).
4. Un selecteur de police de caracteres est disponible avec un catalogue de polices professionnelles adaptees aux documents d'architecture (minimum 15 polices). L'administrateur peut choisir une police pour les titres et une police pour le corps de texte des documents generes.
5. Un apercu en temps reel est affiche a droite du formulaire, montrant un specimen de document (en-tete de facture ou couverture de proposition) avec le logo, les couleurs et les polices selectionnes. L'apercu se met a jour automatiquement a chaque modification.
6. Un bouton "Reinitialiser les valeurs par defaut" permet de revenir a la charte graphique OOTI par defaut avec demande de confirmation.
7. Les parametres de charte graphique sont appliques immediatement a tous les nouveaux documents generes. Les documents deja generes ne sont pas modifies retroactivement (avec mention explicite de ce comportement).
8. En contexte multi-entites, chaque entite peut definir sa propre charte graphique ou heriter de celle de l'entite parente. Un toggle "Heriter de l'entite parente" permet de basculer entre les deux modes.

---

### US-CF06 : Configuration des projets par defaut

**En tant qu'** administrateur ou chef de projet,
**Je veux** pouvoir configurer les phases de projet par defaut, les etiquettes et les statuts personnalises applicables aux projets,
**Afin de** standardiser la gestion de projet au sein de l'agence et gagner du temps lors de la creation de nouveaux projets.

**Criteres d'acceptation :**

1. L'administrateur accede a la page Configuration des projets via l'icone engrenage > section "Projets" dans la sidebar gauche.
2. La section "Phases par defaut" affiche la liste ordonnee des phases de projet avec pour chacune : code (ex: ESQ, APS), nom complet (ex: Esquisse, Avant-Projet Sommaire), et pourcentage de repartition par defaut. Les phases de la loi MOP sont pre-configurees (ESQ, DIAG, APS, APD, PRO, ACT, VISA, DET, AOR, DOE) et peuvent etre modifiees.
3. L'administrateur peut ajouter une nouvelle phase (code + nom + pourcentage), renommer une phase existante, modifier son pourcentage, reordonner les phases par glisser-deposer (drag & drop), et supprimer une phase (avec confirmation si des projets l'utilisent deja). La somme des pourcentages est affichee et un avertissement est affiche si elle ne fait pas 100%.
4. La section "Etiquettes" permet de creer, modifier et supprimer des etiquettes (tags). Chaque etiquette a un nom et une couleur (palette de 20 couleurs ou couleur personnalisee). Les etiquettes peuvent etre regroupees en categories (ex: "Type de projet", "Secteur", "Priorite"). Le nombre de projets utilisant chaque etiquette est affiche.
5. La section "Statuts de projet" affiche les statuts par defaut (Brouillon, En cours, En pause, Termine, Archive) et permet d'ajouter des statuts personnalises avec un nom, une couleur et une icone. L'ordre des statuts est modifiable par glisser-deposer.
6. Un editeur visuel de workflow de transition permet de definir quels passages entre statuts sont autorises (ex: "Brouillon" peut passer a "En cours" mais pas directement a "Termine"). Le workflow est represente graphiquement.
7. Les modifications des phases, etiquettes et statuts s'appliquent aux nouveaux projets crees apres la modification. Les projets existants conservent leur configuration actuelle avec possibilite de migration manuelle.
8. En contexte multi-entites, chaque entite peut definir ses propres parametres de projet ou heriter de l'entite parente. Un indicateur visuel montre clairement si les parametres sont herites ou personnalises.

---

### US-CF07 : Configuration de la facturation

**En tant qu'** administrateur ou responsable financier,
**Je veux** pouvoir configurer les parametres de facturation (numerotation, conditions de paiement, mentions legales, modeles de facture PDF),
**Afin de** garantir la conformite legale des factures emises et automatiser leur generation selon les standards de mon cabinet.

**Criteres d'acceptation :**

1. L'administrateur accede a la page Configuration de la facturation via l'icone engrenage > section "Facturation" dans la sidebar gauche.
2. La section "Numerotation" permet de definir : un prefixe (texte libre, ex: "FA", "ARCH"), un format (annee-numero, numero sequentiel, etc.), le numero de depart (par defaut 1), et l'option de remise a zero annuelle (le compteur repart a 1 au 1er janvier de chaque annee). Un apercu du prochain numero de facture est affiche en temps reel.
3. La section "Conditions de paiement" permet de definir : le delai de paiement par defaut (selection parmi 30, 45, 60, 90 jours ou valeur personnalisee), le taux de penalites de retard (par defaut : 3 fois le taux d'interet legal, modifiable), l'indemnite forfaitaire pour frais de recouvrement (40 EUR par defaut), et un taux d'escompte pour paiement anticipe (optionnel).
4. La section "Mentions legales" contient un editeur de texte riche pour chaque bloc de mentions : mentions obligatoires (pre-remplies selon la legislation francaise), numero d'assurance professionnelle (police + compagnie), numero d'inscription a l'Ordre des Architectes, coordonnees bancaires (IBAN, BIC), conditions generales de vente. Un systeme de variables dynamiques (ex: {{raison_sociale}}, {{siret}}, {{tva_intra}}) est disponible pour inserer automatiquement les informations de l'agence.
5. La section "Modeles de facture" propose au moins 3 modeles pre-configures (Classique, Moderne, Minimaliste). Chaque modele est previsualise en miniature. L'administrateur peut selectionner un modele par defaut et personnaliser : la position du logo (gauche, centre, droite), les colonnes du tableau (description, quantite, prix unitaire, TVA, total), le contenu du pied de page, la taille de la police.
6. Un bouton "Apercu" genere un PDF d'exemple avec les parametres actuels, permettant de visualiser le rendu final avant validation. L'apercu s'ouvre dans une modale ou un nouvel onglet.
7. Des modeles distincts peuvent etre configures pour chaque type de document : facture, avoir, facture proforma, decompte d'honoraires. Chaque type a son propre prefixe de numerotation.
8. Les parametres de facturation sont specifiques a chaque entite en contexte multi-entites. Les modifications sont journalisees dans l'historique d'audit avec horodatage et identification de l'auteur.

---

### US-CF08 : Configuration du temps

**En tant qu'** administrateur ou responsable RH,
**Je veux** pouvoir configurer les parametres de saisie de temps (heures/jour, jours ouvres, jours feries, types de temps),
**Afin de** refleter fidelement l'organisation du travail de mon cabinet et garantir la fiabilite des donnees de temps saisies.

**Criteres d'acceptation :**

1. L'administrateur accede a la page Configuration du temps via l'icone engrenage > section "Temps" dans la sidebar gauche.
2. Le champ "Heures par jour" est un champ numerique avec selection possible parmi les valeurs courantes (7h, 7.5h, 8h) ou saisie libre (precision au quart d'heure). Le champ "Heures par semaine" est calcule automatiquement en fonction du nombre de jours ouvres selectionnes, mais peut etre surcharge manuellement.
3. Les "Jours ouvres" sont selectionnables via 7 cases a cocher (Lundi a Dimanche), avec Lundi a Vendredi coches par defaut. La modification met automatiquement a jour le calcul des heures par semaine et le calendrier de saisie des temps.
4. La section "Jours feries" propose un calendrier par pays pre-configure (France metropolitaine par defaut, avec option DOM-TOM, Belgique, Suisse, Luxembourg, etc.). Les jours feries sont affiches dans un calendrier annuel visuel. L'administrateur peut ajouter des jours feries specifiques (ponts, fermetures d'agence) avec un nom, une date, et un caractere recurrent (annuel) ou ponctuel.
5. La section "Types de temps" affiche la liste des types disponibles dans un tableau avec : code, nom, categorie (productif/non productif), facturable (oui/non), et couleur d'affichage. Des types par defaut sont pre-configures : Conception, Etude technique, Reunion client, Chantier, Administratif, Formation, Deplacement.
6. L'administrateur peut ajouter, modifier, desactiver ou supprimer des types de temps. La suppression n'est possible que si aucune saisie de temps n'utilise ce type ; sinon, seule la desactivation est autorisee (le type n'apparait plus dans les selecteurs mais les donnees historiques sont conservees).
7. Le parametre "Arrondi de saisie" est configurable : libre (pas d'arrondi), au quart d'heure (0.25h), a la demi-heure (0.5h), a l'heure (1h). Le mode d'arrondi est applique automatiquement lors de la saisie des temps par les collaborateurs.
8. Le parametre "Rappel de saisie" permet de configurer l'envoi automatique d'un rappel aux collaborateurs n'ayant pas complete leur saisie de temps : frequence (quotidien a 17h, hebdomadaire le vendredi), canal (email, notification in-app), et possibilite de desactiver les rappels.

---

### US-CF09 : Configuration equipe et entites

**En tant qu'** administrateur ou dirigeant de cabinet,
**Je veux** pouvoir gerer les entites (agences, filiales) et les departements de mon organisation dans les parametres,
**Afin de** structurer l'organisation de mon cabinet dans OOTI et permettre une gestion multi-sites avec des parametres adaptes a chaque entite.

**Criteres d'acceptation :**

1. L'administrateur accede a la page Configuration equipe via l'icone engrenage > section "Equipe" dans la sidebar gauche.
2. La section "Entites / Agences" affiche la liste de toutes les entites du compte sous forme arborescente (hierarchie parent-enfant) avec pour chacune : nom, ville, nombre de collaborateurs, et statut (active/inactive).
3. L'administrateur peut creer une nouvelle entite en renseignant : nom de l'entite, raison sociale, adresse, entite parente (optionnel pour creer une filiale), et les parametres specifiques (ou heritage de l'entite parente). La creation d'une entite copie par defaut les parametres de l'entite parente.
4. Le mecanisme d'heritage des parametres fonctionne comme suit : par defaut, une entite enfant herite de tous les parametres de son entite parente (phases projet, conditions de facturation, types de temps, etc.). Pour chaque groupe de parametres, un toggle "Personnaliser pour cette entite" permet de surcharger les valeurs heritees. Les parametres herites sont affiches en grise avec la mention "Herite de [nom de l'entite parente]".
5. La section "Departements" affiche la liste des departements pour l'entite selectionnee avec : nom du departement, code (pour la comptabilite), responsable, et nombre de collaborateurs. L'administrateur peut ajouter, modifier, desactiver ou supprimer un departement.
6. La suppression d'une entite ou d'un departement n'est possible que s'ils ne contiennent aucun collaborateur actif ni aucun projet en cours. Dans le cas contraire, un message indique les elements bloquants a reassigner au prealable.
7. Un selecteur d'entite active est disponible dans la barre de navigation principale, permettant de basculer rapidement entre les entites. Le changement d'entite filtre automatiquement les donnees affichees (projets, factures, collaborateurs) selon l'entite selectionnee.
8. Un tableau de synthese multi-entites est disponible pour les administrateurs globaux, affichant une vue consolidee : nombre total de collaborateurs, nombre de projets actifs, chiffre d'affaires facture, par entite, avec possibilite de driller (navigation vers les details de chaque entite).

---

### US-CF10 : Import de donnees en masse

**En tant qu'** administrateur,
**Je veux** pouvoir importer des donnees en masse (projets, clients, collaborateurs, temps) depuis des fichiers CSV ou XLSX,
**Afin de** migrer rapidement les donnees existantes de mon ancien systeme vers OOTI et eviter la ressaisie manuelle.

**Criteres d'acceptation :**

1. L'administrateur accede a la page Import via l'icone engrenage > section "Donnees" > "Import" dans la sidebar gauche.
2. L'ecran d'import presente un selecteur du type de donnees a importer : Projets, Clients & Contacts, Collaborateurs, Saisies de temps, Factures historiques. Chaque type affiche les champs attendus et un lien pour telecharger le modele de fichier (template CSV/XLSX pre-formate avec en-tetes et exemples de donnees).
3. L'upload du fichier accepte les formats CSV (encodage UTF-8, separateur point-virgule ou virgule avec detection automatique) et XLSX (premiere feuille uniquement). La taille maximale est de 50 Mo. Un indicateur de progression s'affiche pendant l'upload.
4. L'etape de mapping des colonnes affiche les colonnes detectees dans le fichier et les champs OOTI correspondants. Le systeme propose un mapping automatique basee sur les noms de colonnes (correspondance exacte ou proche). L'administrateur peut modifier manuellement le mapping via des listes deroulantes. Les champs obligatoires non mappes sont signales en rouge.
5. L'etape d'apercu et de validation affiche les 10 premieres lignes du fichier avec le mapping applique. Un rapport de validation est genere indiquant : nombre total de lignes, nombre de lignes valides, nombre de lignes en erreur (avec le numero de ligne et la description de l'erreur : format invalide, champ obligatoire manquant, doublon detecte, reference inexistante).
6. L'import est execute en arriere-plan avec une barre de progression en temps reel. L'administrateur peut naviguer dans l'application pendant l'import. Une notification (in-app et email) est envoyee a la completion.
7. Le rapport d'import final indique : nombre de lignes importees avec succes, nombre de lignes ignorees (doublons), nombre de lignes en erreur (avec possibilite de telecharger un fichier des erreurs). Un bouton "Annuler l'import" permet de faire un rollback complet de l'import dans les 24 heures suivant la completion.
8. L'import gere intelligemment les doublons : detection par cle naturelle (email pour les collaborateurs, numero pour les projets, raison sociale + SIRET pour les clients). En cas de doublon, trois options sont proposees : ignorer la ligne, mettre a jour l'enregistrement existant, ou creer un nouvel enregistrement.

---

### US-CF11 : Export de donnees

**En tant qu'** administrateur ou responsable financier,
**Je veux** pouvoir exporter les donnees de OOTI (projets, clients, temps, factures) dans differents formats,
**Afin de** realiser des analyses externes, satisfaire aux obligations d'audit, ou transmettre des donnees a mon expert-comptable.

**Criteres d'acceptation :**

1. L'administrateur accede a la page Export via l'icone engrenage > section "Donnees" > "Export" dans la sidebar gauche.
2. L'ecran d'export presente un selecteur du type de donnees a exporter : Projets, Clients & Contacts, Collaborateurs, Saisies de temps, Factures, Budget & Couts. La selection du type affiche les champs disponibles avec des cases a cocher pour selectionner/deselectionner les colonnes a inclure dans l'export.
3. Des filtres contextuels sont disponibles selon le type de donnees : plage de dates (du/au), entite, statut (actif/archive/tous), projet specifique, collaborateur specifique. Les filtres se combinent (ET logique). Un compteur affiche le nombre d'enregistrements correspondant aux filtres appliques avant le lancement de l'export.
4. Les formats d'export disponibles sont : CSV (UTF-8 avec BOM pour compatibilite Excel), XLSX (avec mise en forme basique : en-tetes en gras, largeur de colonnes ajustee), et PDF (pour les rapports avec mise en page professionnelle).
5. L'export est execute en arriere-plan si le nombre d'enregistrements depasse 1000. Une notification est envoyee a l'utilisateur lorsque le fichier est pret a etre telecharge. Les fichiers d'export sont conserves pendant 7 jours.
6. Une fonctionnalite d'export programme permet de configurer un export recurrent : frequence (quotidien, hebdomadaire le lundi, mensuel le 1er), type de donnees, filtres, format, et adresse email de destination. L'export programme est execute automatiquement et le fichier est envoye par email.
7. Un export RGPD complet est disponible via le bouton "Exporter toutes mes donnees", generant une archive ZIP contenant l'ensemble des donnees personnelles de l'utilisateur ou de l'entite au format JSON, conformement a l'article 20 du RGPD (droit a la portabilite).
8. Chaque export est journalise dans un historique accessible a l'administrateur, indiquant : date, type de donnees, format, nombre d'enregistrements, utilisateur ayant effectue l'export, et lien de telechargement (disponible pendant 7 jours).

---

### US-CF12 : Gestion des integrations

**En tant qu'** administrateur,
**Je veux** pouvoir connecter, configurer et surveiller les integrations API tierces (comptabilite, calendrier, stockage, communication) depuis les parametres,
**Afin de** synchroniser les donnees de OOTI avec les autres outils utilises par mon cabinet et eliminer les doubles saisies.

**Criteres d'acceptation :**

1. L'administrateur accede a la page Integrations via l'icone engrenage > section "Integrations" dans la sidebar gauche.
2. La page affiche un catalogue d'integrations disponibles sous forme de cartes (grille), chacune avec : logo du service, nom, description courte, categorie (Comptabilite, Calendrier, Stockage, Communication, BIM, Autre), et statut (Connectee avec indicateur vert, Deconnectee avec indicateur gris, Erreur avec indicateur rouge).
3. La connexion a une integration s'effectue soit par flux OAuth2 (redirection vers le service tiers pour autorisation, puis retour vers OOTI), soit par saisie d'une cle API (champ masque avec bouton "Afficher"). Un bouton "Tester la connexion" permet de verifier la validite des identifiants avant la sauvegarde.
4. Chaque integration connectee dispose d'une page de configuration detaillee affichant : la date de connexion, la date de derniere synchronisation, la frequence de synchronisation (temps reel, toutes les heures, quotidienne, manuelle), la direction de synchronisation (OOTI vers service, service vers OOTI, bidirectionnelle), et des filtres de synchronisation (quelles donnees synchroniser).
5. Un journal de synchronisation est disponible pour chaque integration, affichant les 100 derniers evenements avec : date/heure, type d'action (creation, mise a jour, suppression), nombre d'enregistrements traites, statut (succes, erreur, avertissement), et detail de l'erreur le cas echeant.
6. La deconnexion d'une integration requiert une confirmation avec avertissement sur les consequences (arret de la synchronisation, donnees deja synchronisees conservees dans OOTI). La deconnexion ne supprime pas les donnees deja importees.
7. Une section "Webhooks" permet de configurer des webhooks sortants : URL de destination, evenements declencheurs (nouveau projet, nouvelle facture, nouveau temps, etc.), secret de signature HMAC pour la verification de l'authenticite. Un bouton "Envoyer un evenement de test" est disponible.
8. Les cles API et tokens d'authentification sont stockes de maniere chiffree. Seul l'administrateur ayant configure l'integration peut voir (de maniere masquee) ou regenerer les identifiants. Un indicateur d'expiration avertit l'administrateur lorsqu'un token approche de sa date d'expiration.

---

### US-CF13 : Activation/desactivation des modules

**En tant qu'** administrateur,
**Je veux** pouvoir activer ou desactiver individuellement les modules de l'application (Projets, Honoraires, Facturation, Temps, Equipe, etc.),
**Afin d'** adapter l'interface de OOTI aux besoins reels de mon cabinet et simplifier l'experience utilisateur en masquant les fonctionnalites non utilisees.

**Criteres d'acceptation :**

1. L'administrateur accede a la page Modules via l'icone engrenage > section "Modules" dans la sidebar gauche.
2. La page affiche la liste de tous les modules de l'application sous forme de cartes avec pour chacun : nom du module, icone, description courte des fonctionnalites couvertes, et un toggle (interrupteur) d'activation/desactivation. Les modules actuellement actifs ont le toggle en position "On" (couleur primaire).
3. La desactivation d'un module declenche l'affichage d'une modale de confirmation indiquant : les consequences de la desactivation (le module disparait de la navigation principale et n'est plus accessible), les modules dependants qui seront egalement impactes (ex: desactiver "Projets" impacte "Honoraires", "Facturation", "Planification"), et la mention explicite que les donnees existantes sont conservees et seront restaurees a la reactivation.
4. Les dependances entre modules sont clairement visualisees : un module ne peut pas etre desactive si un module dependant est encore actif (ou celui-ci est desactive automatiquement en cascade apres confirmation). Les dependances sont representees graphiquement (arbre ou schema).
5. La reactivation d'un module est instantanee : le module reapparait dans la navigation et toutes les donnees anterieures sont immediatement accessibles, sans perte ni corruption.
6. Un module "coeur" (Projets, par exemple) est identifie comme obligatoire et ne peut pas etre desactive. Il est affiche avec un cadenas et une infobulle explicative.
7. Le changement d'etat d'un module (activation/desactivation) est journalise dans l'historique d'audit avec l'utilisateur, la date/heure et le module concerne. Une notification est envoyee aux administrateurs de l'entite.
8. En contexte multi-entites, l'activation/desactivation des modules peut etre geree au niveau de l'entite parente (appliquee a toutes les filiales) ou individuellement par entite, selon la politique definie par l'administrateur global.

---

### US-CF14 : Gestion de l'abonnement

**En tant qu'** administrateur ou dirigeant de cabinet,
**Je veux** pouvoir consulter et gerer mon abonnement OOTI (plan, facturation, nombre d'utilisateurs, stockage),
**Afin de** controler mes couts et adapter mon abonnement a l'evolution de mon cabinet.

**Criteres d'acceptation :**

1. L'administrateur accede a la page Abonnement via l'icone engrenage > section "Abonnement" dans la sidebar gauche.
2. La page affiche un resume du plan actuel : nom du plan (Starter, Professional, Enterprise), prix par mois/par an, cycle de facturation (mensuel ou annuel), date du prochain renouvellement, et mode de paiement enregistre (type de carte, 4 derniers chiffres, date d'expiration).
3. La section "Utilisation" affiche des jauges visuelles pour : le nombre d'utilisateurs actifs par rapport au nombre inclus dans le plan (ex: 12/15 utilisateurs), l'espace de stockage utilise par rapport au quota (ex: 2.3 Go / 10 Go), et le nombre de projets actifs si le plan est limite. Un avertissement est affiche lorsque 80% du quota est atteint et une alerte a 95%.
4. Le changement de plan (upgrade ou downgrade) est possible via un bouton "Changer de plan" qui affiche un comparatif des plans disponibles avec les fonctionnalites incluses, les quotas et les prix. L'upgrade est immediat avec facturation au prorata de la periode restante. Le downgrade est effectif a la fin de la periode de facturation en cours.
5. La modification du cycle de facturation (mensuel vers annuel ou inversement) est possible. Le passage a l'annuel affiche l'economie realisee (generalement 2 mois gratuits). Le changement est effectif au prochain renouvellement.
6. L'historique des factures d'abonnement est affiche sous forme de tableau avec : date, numero de facture, montant, statut (payee, en attente, echouee), et lien de telechargement du PDF. Les factures sont conservees sans limitation de duree.
7. La mise a jour du moyen de paiement est possible via un formulaire securise (integration Stripe ou equivalent). La saisie des informations de carte bancaire est effectuee directement dans l'iframe du prestataire de paiement (PCI DSS compliant), sans transit par les serveurs OOTI.
8. L'annulation de l'abonnement est possible via un bouton "Annuler l'abonnement" avec un parcours de retention : motif de depart (selection parmi une liste + commentaire libre), proposition d'un plan alternatif ou d'une remise, confirmation finale avec rappel de la date de fin d'acces et de la politique de retention des donnees (donnees conservees 90 jours, puis supprimees).

---

### US-CF15 : Onboarding guide

**En tant que** nouvel administrateur d'un cabinet d'architecture creant son compte OOTI,
**Je veux** etre guide pas a pas dans la configuration initiale de mon environnement via un assistant d'onboarding structure en 10 etapes,
**Afin de** configurer rapidement et completement mon espace de travail sans oublier de parametres essentiels.

**Criteres d'acceptation :**

1. L'onboarding se declenche automatiquement lors de la premiere connexion d'un administrateur apres la creation du compte. Il est egalement accessible a tout moment depuis la sidebar des parametres tant qu'il n'est pas marque comme complete.
2. Une barre de progression horizontale affiche les 10 etapes de l'onboarding avec leur nom, un indicateur visuel (cercle vide = a faire, cercle partiellement rempli = en cours, coche verte = complete), et le pourcentage global de progression.
3. Les 10 etapes sont parcourues sequentiellement mais l'utilisateur peut naviguer librement entre elles (retour a une etape precedente, saut d'une etape). Chaque etape comporte : un titre, une description explicative, le formulaire ou l'action a accomplir, et un bouton "Continuer" pour passer a l'etape suivante et un lien "Passer cette etape".
4. **Etape 1 - Changer le mot de passe** : L'utilisateur est invite a definir un mot de passe securise (memes regles que US-CF02). L'etape est marquee complete lorsque le mot de passe est change avec succes.
5. **Etapes 2 a 8** (Personnaliser compte, Configurer equipe, Configurer projets, Configurer facturation, Configurer temps, Configurer couts, Planifier projets) : Chaque etape presente un formulaire pre-rempli avec des valeurs par defaut intelligentes (basees sur le pays et le secteur). Des bulles d'aide contextuelles expliquent chaque champ. Le formulaire est une version simplifiee de la page de parametres complete (les parametres avances restent accessibles via un lien "Parametres avances"). L'etape est marquee complete lorsque le formulaire est sauvegarde (meme sans modification des valeurs par defaut).
6. **Etape 9 - Gestion des donnees** : L'utilisateur est invite a importer ses donnees existantes (projets, clients, collaborateurs) via l'assistant d'import (meme interface que US-CF10 mais integree dans le flux d'onboarding). L'etape peut etre sautee si l'utilisateur n'a pas de donnees a importer.
7. **Etape 10 - Configuration completee** : Un ecran de felicitations recapitule les parametres configures, affiche des liens rapides vers les actions suivantes (creer un premier projet, inviter des collaborateurs, consulter le centre d'aide), et un bouton "Commencer a utiliser OOTI" qui ferme l'onboarding et redirige vers le tableau de bord.
8. L'etat de progression de l'onboarding est persiste en base de donnees et synchronise en temps reel. Si l'utilisateur quitte l'onboarding en cours de route, il reprend a l'etape ou il s'est arrete lors de sa prochaine connexion. Un widget discret dans le tableau de bord rappelle la progression et invite a completer l'onboarding tant qu'il n'est pas a 100%.

---

## 6. Hors Perimetre

Les elements suivants sont explicitement exclus du perimetre de l'EPIC-016 :

| Element | Raison de l'exclusion | EPIC concerne |
|---|---|---|
| Gestion detaillee des droits et permissions (RBAC granulaire) | Couvert par le module Authentification & Utilisateurs | EPIC-001 |
| Creation et gestion des projets | Seuls les parametres par defaut sont configures ici ; la gestion des projets est dans le module Projets | EPIC-002 |
| Calcul et gestion des honoraires | Seuls les parametres de facturation sont configures ici | EPIC-003 |
| Emission et suivi des factures | Le module Configuration ne genere pas de factures, il definit les modeles et regles | EPIC-004 |
| Saisie et validation des temps | Le module Configuration definit les parametres ; la saisie effective est dans le module Temps | EPIC-005 |
| Gestion RH detaillee (conges, absences, evaluations) | Couvert par le module Equipe & RH | EPIC-006 |
| Fiches clients et contacts detaillees | Couvert par le module Clients & Contacts | EPIC-007 |
| Suivi budgetaire operationnel | Couvert par le module Budgets & Couts | EPIC-008 |
| Generation de rapports et dashboards | Couvert par le module Rapports & Tableaux de bord | EPIC-009 |
| Gestion documentaire (upload, versioning, partage) | Couvert par le module Documents & GED | EPIC-010 |
| Planification operationnelle (Gantt, planning) | Couvert par le module Planification | EPIC-011 |
| Moteur de notifications (envoi effectif) | Le module Configuration definit les preferences ; le moteur d'envoi est dans EPIC-012 | EPIC-012 |
| Developpement des connecteurs API specifiques | Les connecteurs sont developpes dans le module API ; ici on configure leur activation | EPIC-013 |
| Logique de facturation de l'abonnement (Stripe, webhooks) | L'infrastructure de billing est dans EPIC-014 ; ici on fournit l'interface de gestion | EPIC-014 |
| Conception des parcours marketing d'onboarding | Seul l'onboarding technique (configuration) est couvert ici | EPIC-015 |
| Application mobile native | Les parametres sont accessibles uniquement via l'interface web responsive | Hors scope v1 |
| Configuration SSO/SAML pour les entreprises | Prevu pour une version ulterieure (v2) | Backlog |
| Marketplace d'extensions et plugins tiers | Prevu pour une version ulterieure (v2) | Backlog |

---

## 7. Regles Metier

### RM-CF01 : Hierarchie des droits d'acces aux parametres

| Section de parametres | Administrateur global | Administrateur d'entite | Manager | Collaborateur |
|---|---|---|---|---|
| Profil personnel | Lecture/Ecriture | Lecture/Ecriture | Lecture/Ecriture | Lecture/Ecriture |
| Securite personnelle | Lecture/Ecriture | Lecture/Ecriture | Lecture/Ecriture | Lecture/Ecriture |
| Notifications personnelles | Lecture/Ecriture | Lecture/Ecriture | Lecture/Ecriture | Lecture/Ecriture |
| Parametres generaux agence | Lecture/Ecriture | Lecture/Ecriture (son entite) | Lecture seule | Aucun acces |
| Charte graphique | Lecture/Ecriture | Lecture/Ecriture (son entite) | Lecture seule | Aucun acces |
| Configuration projets | Lecture/Ecriture | Lecture/Ecriture (son entite) | Lecture seule | Aucun acces |
| Configuration facturation | Lecture/Ecriture | Lecture/Ecriture (son entite) | Lecture seule | Aucun acces |
| Configuration temps | Lecture/Ecriture | Lecture/Ecriture (son entite) | Lecture seule | Aucun acces |
| Configuration equipe/entites | Lecture/Ecriture | Lecture/Ecriture (son entite) | Aucun acces | Aucun acces |
| Import/Export de donnees | Lecture/Ecriture | Lecture/Ecriture (son entite) | Aucun acces | Aucun acces |
| Collaborateurs | Lecture/Ecriture | Lecture/Ecriture (son entite) | Lecture seule | Aucun acces |
| Integrations | Lecture/Ecriture | Lecture (connectees) | Aucun acces | Aucun acces |
| Modules | Lecture/Ecriture | Lecture seule | Aucun acces | Aucun acces |
| Abonnement | Lecture/Ecriture | Lecture seule | Aucun acces | Aucun acces |
| Assistance | Lecture/Ecriture | Lecture/Ecriture | Lecture/Ecriture | Lecture/Ecriture |

### RM-CF02 : Heritage des parametres multi-entites

- Lorsqu'une entite enfant est creee, elle herite automatiquement de tous les parametres de son entite parente.
- Chaque groupe de parametres (projets, facturation, temps, charte graphique) peut etre personnalise independamment au niveau de l'entite enfant via un toggle "Personnaliser".
- Lorsqu'un parametre est personnalise au niveau de l'entite enfant et que le parametre parent est modifie, l'entite enfant conserve sa valeur personnalisee (pas de propagation automatique en cas de surcharge).
- Lorsqu'un parametre est herite (non personnalise) et que le parametre parent est modifie, la modification est automatiquement propagee a l'entite enfant.
- La remise en mode heritage (desactivation du toggle "Personnaliser") ecrase les valeurs personnalisees par les valeurs de l'entite parente avec confirmation prealable.

### RM-CF03 : Numerotation des factures

- Le numero de facture est genere automatiquement a la creation de la facture selon le format configure.
- Le format de numerotation est de la forme : `[prefixe]-[annee]-[numero_sequentiel]`, ou chaque composant est optionnel.
- Le numero sequentiel est incremente de 1 a chaque nouvelle facture (ou avoir, proforma, etc.) selon le type de document.
- Si l'option "Remise a zero annuelle" est activee, le compteur repart a 1 au 1er janvier de chaque annee.
- Un numero de facture ne peut jamais etre reutilise, meme apres suppression de la facture (conformite legale).
- La numerotation est unique et sequentielle par entite.

### RM-CF04 : Gestion des jours feries

- Les jours feries sont utilises pour le calcul du nombre de jours ouvres dans une periode donnee (impact sur la planification, les budgets temps, et les echeances).
- Un jour ferie est automatiquement exclu du calendrier de saisie des temps (le collaborateur ne peut pas saisir de temps productif un jour ferie, sauf derogation manuelle).
- Les jours feries nationaux sont pre-configures par pays et mis a jour annuellement par l'equipe OOTI.
- Les jours feries personnalises (fermetures d'agence) sont specifiques a l'entite et peuvent etre recurrents (meme date chaque annee) ou ponctuels.

### RM-CF05 : Import de donnees

- Un import ne peut pas etre lance si un autre import du meme type est deja en cours pour la meme entite.
- La taille maximale d'un fichier d'import est de 50 Mo (environ 100 000 lignes pour un CSV standard).
- Les donnees importees sont rattachees a l'entite active de l'administrateur au moment de l'import.
- Le rollback d'un import est possible pendant 24 heures et supprime uniquement les enregistrements crees par cet import (pas les enregistrements mis a jour).
- Les imports sont journalises avec l'horodatage, l'utilisateur, le type de donnees, le nombre d'enregistrements et le statut.

### RM-CF06 : Desactivation de modules

- La desactivation d'un module masque ses entrees dans la navigation et rend ses pages inaccessibles, mais les donnees sont integralement conservees en base.
- Si un module B depend d'un module A, la desactivation de A entraine la desactivation automatique de B (avec confirmation prealable).
- Les modules "coeur" (identites comme indispensables au fonctionnement de base) ne peuvent pas etre desactives.
- La reactivation d'un module restaure immediatement l'acces a toutes les donnees et fonctionnalites.

### RM-CF07 : Securite et sessions

- Un mot de passe doit comporter au minimum 12 caracteres, incluant au moins une majuscule, une minuscule, un chiffre et un caractere special.
- Le 2FA utilise le protocole TOTP (RFC 6238) avec des codes a 6 chiffres et une fenetre de tolerance de 30 secondes.
- Les codes de secours 2FA sont a usage unique et au nombre de 10. Ils sont regenerables a tout moment (les anciens sont alors invalides).
- Une session inactive depuis plus de 30 jours est automatiquement revoquee.
- Apres 5 tentatives de connexion echouees, le compte est temporairement verrouille pour 15 minutes.

### RM-CF08 : Onboarding

- L'onboarding est declenche une seule fois, lors de la premiere connexion de l'administrateur createur du compte.
- Les autres administrateurs ou collaborateurs invites ulterieurement ne declenchent pas l'onboarding complet (mais un mini-onboarding personnel : profil, mot de passe, notifications).
- L'onboarding est considere comme "complete" lorsque les 10 etapes sont marquees comme terminees ou sautees.
- Les etapes sautees restent accessibles et peuvent etre completees plus tard.
- Les donnees saisies dans l'onboarding sont identiques a celles des pages de parametres correspondantes (pas de duplication de stockage).

### RM-CF09 : Audit trail

- Toute modification d'un parametre de configuration est enregistree dans un journal d'audit avec : date/heure, utilisateur, entite, section modifiee, champ modifie, ancienne valeur, nouvelle valeur.
- Le journal d'audit est conserve pendant 5 ans (conformite legale).
- Le journal d'audit est accessible en lecture seule aux administrateurs globaux et aux administrateurs d'entite (pour leur entite uniquement).
- Les evenements critiques (changement de mot de passe, activation/desactivation 2FA, modification des droits, changement de plan) sont mis en evidence dans le journal.

---

## 8. Criteres Globaux

### 8.1 Performance

| Critere | Cible |
|---|---|
| Temps de chargement d'une page de parametres | < 1 seconde |
| Temps de sauvegarde d'un formulaire | < 500 ms (retour visuel) |
| Temps d'upload d'un logo (5 Mo) | < 3 secondes |
| Temps de generation d'un apercu PDF | < 2 secondes |
| Temps d'import de 1 000 lignes CSV | < 30 secondes |
| Temps d'import de 10 000 lignes CSV | < 5 minutes |
| Temps d'export de 10 000 enregistrements | < 1 minute |
| Nombre maximal d'entites par compte | 50 |
| Nombre maximal de departements par entite | 30 |
| Nombre maximal d'integrations simultanees | 20 |

### 8.2 Securite

- Toutes les communications sont chiffrees en HTTPS (TLS 1.2 minimum).
- Les cles API et tokens d'integration sont stockes chiffres en base (AES-256).
- Les mots de passe sont hashes avec bcrypt (cost factor >= 12).
- Les sessions utilisent des tokens JWT avec expiration configurable.
- Les operations sensibles (changement de mot de passe, desactivation 2FA, suppression de compte) requierent une re-authentification.
- Le CSRF protection est active sur tous les formulaires.
- Les inputs sont valides cote client et cote serveur (protection contre les injections SQL et XSS).
- Les fichiers uploades sont scannes (antivirus) et valides (type MIME, extension).

### 8.3 Accessibilite

- Conformite WCAG 2.1 niveau AA.
- Navigation complete au clavier dans tous les formulaires de parametres.
- Labels et attributs ARIA pour tous les champs de formulaire.
- Contrastes de couleurs conformes (ratio minimum 4.5:1 pour le texte normal).
- Messages d'erreur accessibles (aria-live pour les messages dynamiques).
- Support des lecteurs d'ecran (NVDA, VoiceOver, JAWS).

### 8.4 Compatibilite

- Navigateurs : Chrome 90+, Firefox 90+, Safari 15+, Edge 90+.
- Resolution minimale : 1280 x 720 pixels.
- Interface responsive : adaptation pour tablettes (768px) avec degradation gracieuse.
- Pas de support mobile natif en v1 (interface web responsive uniquement).

### 8.5 Internationalisation

- Toutes les chaines de caracteres de l'interface sont externalisees dans des fichiers de traduction (i18n).
- Support des langues : francais, anglais, espagnol, allemand, portugais.
- Gestion des formats de date (JJ/MM/AAAA, MM/DD/YYYY, YYYY-MM-DD) selon la locale.
- Gestion des formats de nombres et devises selon la locale (separateur decimal, symbole de devise).
- Support de la direction LTR (gauche a droite) uniquement en v1.

---

## 9. Definition of Done (DoD)

Un element de backlog (User Story) est considere comme "Done" lorsque l'ensemble des criteres suivants sont remplis :

### 9.1 Developpement

- [ ] Le code source est ecrit en respectant les conventions de codage du projet (linting, formatting).
- [ ] Le code est revue par au moins un autre developpeur (code review approuvee).
- [ ] Les branches de fonctionnalite sont mergees dans la branche de developpement via Pull Request.
- [ ] Aucun warning ni erreur de compilation/build.
- [ ] Les variables d'environnement et secrets sont externalises (pas de valeurs en dur).

### 9.2 Tests

- [ ] Tests unitaires ecrits et passants (couverture > 80% pour le code metier).
- [ ] Tests d'integration ecrits et passants pour les API endpoints.
- [ ] Tests end-to-end (E2E) ecrits pour les parcours critiques (onboarding, import, changement de plan).
- [ ] Tests de securite effectues (injection SQL, XSS, CSRF, validation des droits).
- [ ] Tests de performance effectues (temps de reponse dans les limites definies).
- [ ] Tests d'accessibilite effectues (audit WCAG AA avec outil automatise + verification manuelle).
- [ ] Tests multi-navigateurs effectues (Chrome, Firefox, Safari, Edge).

### 9.3 Documentation

- [ ] Documentation API (endpoints, parametres, reponses) a jour dans Swagger/OpenAPI.
- [ ] Documentation utilisateur redigee pour les nouvelles fonctionnalites (centre d'aide).
- [ ] Changelog mis a jour avec la description des modifications.
- [ ] Schemas de base de donnees et migrations documentes.

### 9.4 Deploiement

- [ ] Les migrations de base de donnees sont creees, testees et reversibles.
- [ ] Les feature flags sont en place pour les fonctionnalites a deploiement progressif.
- [ ] Les metriques de monitoring sont configurees (temps de reponse, taux d'erreur, usage).
- [ ] Les alertes sont configurees pour les seuils critiques.
- [ ] Le deploiement sur l'environnement de staging est valide.

### 9.5 Validation

- [ ] Les criteres d'acceptation de la User Story sont tous verifies et valides.
- [ ] Le Product Owner a valide la fonctionnalite sur l'environnement de staging.
- [ ] Les tests de regression sur les fonctionnalites existantes sont passants.
- [ ] Aucun bug bloquant ou critique ouvert sur la fonctionnalite.

---

## 10. Dependances

### 10.1 Dependances techniques

| Dependance | Description | Impact | Statut |
|---|---|---|---|
| Systeme d'authentification (EPIC-001) | Le module de profil et de securite depend du systeme d'authentification (JWT, 2FA, gestion des sessions). | Bloquant pour US-CF01, US-CF02 | A verifier |
| Base de donnees relationnelle | PostgreSQL 15+ pour le stockage des parametres, l'historique d'audit et les configurations. | Bloquant pour l'ensemble du module | Disponible |
| Service de stockage objet | S3 ou compatible (MinIO) pour le stockage des logos, avatars et fichiers uploades. | Bloquant pour US-CF05 | A provisionner |
| Service d'email transactionnel | SendGrid, Mailgun ou SES pour l'envoi des notifications email, confirmations et recapitulatifs. | Bloquant pour US-CF03, US-CF10, US-CF11 | A configurer |
| Generateur de PDF | Librairie de generation de PDF (Puppeteer, wkhtmltopdf, ou WeasyPrint) pour les aperçus et les modeles de facture. | Bloquant pour US-CF07 | A selectionner |
| Processeur de taches asynchrones | Celery + Redis (ou equivalent) pour les imports/exports en arriere-plan. | Bloquant pour US-CF10, US-CF11 | A configurer |
| Service de paiement | Stripe ou equivalent pour la gestion de l'abonnement (PCI DSS compliant). | Bloquant pour US-CF14 | A integrer |
| Service TOTP | Librairie TOTP (pyotp ou equivalent) pour la generation et verification des codes 2FA. | Bloquant pour US-CF02 | Disponible |

### 10.2 Dependances fonctionnelles inter-EPICs

| EPIC source | Dependance | Nature |
|---|---|---|
| EPIC-001 (Auth) | Le systeme de roles et permissions definit l'acces aux sections de parametres. | Prerequis |
| EPIC-002 (Projets) | Les phases, etiquettes et statuts configures ici sont utilises lors de la creation de projets. | Consommateur |
| EPIC-003 (Honoraires) | Les taux de TVA et conditions de paiement configures ici s'appliquent aux honoraires. | Consommateur |
| EPIC-004 (Facturation) | Les modeles de facture, la numerotation et les mentions legales sont utilises par le module Facturation. | Consommateur |
| EPIC-005 (Temps) | Les types de temps, heures/jour, jours ouvres et jours feries sont utilises par le module Temps. | Consommateur |
| EPIC-006 (Equipe) | Les entites et departements configures ici structurent l'organisation dans le module Equipe. | Consommateur |
| EPIC-009 (Rapports) | Les donnees de configuration (entites, departements) alimentent les filtres et axes d'analyse des rapports. | Consommateur |
| EPIC-012 (Notifications) | Les preferences de notification definies ici sont consommees par le moteur de notifications. | Consommateur |
| EPIC-013 (API) | Les configurations d'integration definies ici sont utilisees par les connecteurs API. | Consommateur |
| EPIC-014 (Abonnement) | L'interface de gestion de l'abonnement interagit avec l'infrastructure de billing. | Bidirectionnel |

### 10.3 Dependances d'equipe

| Role | Responsabilite | Nombre |
|---|---|---|
| Product Owner | Validation des User Stories, priorisation du backlog, recette fonctionnelle | 1 |
| UX/UI Designer | Maquettes des ecrans de parametres, parcours d'onboarding, tests utilisateurs | 1 |
| Developpeur Frontend | Implementation de l'interface (formulaires, sidebar, aperçus, onboarding) | 2 |
| Developpeur Backend | API, logique metier, import/export, integrations, securite | 2 |
| Developpeur Full-stack | Integrations transversales, multi-entites, audit trail | 1 |
| QA Engineer | Tests fonctionnels, tests de performance, tests de securite, tests d'accessibilite | 1 |
| DevOps | Infrastructure (stockage, file de taches, monitoring), deploiement | 0.5 |

---

## 11. Modele de Donnees

### 11.1 Schema des entites principales

```
Entity
----------------------------------------------
id              UUID            PK
name            VARCHAR(255)    NOT NULL
legal_name      VARCHAR(255)    NOT NULL
legal_form      VARCHAR(50)     -- SA, SAS, SARL, etc.
siret           VARCHAR(14)     UNIQUE
siren           VARCHAR(9)      -- Deduit du SIRET
vat_number      VARCHAR(20)     -- TVA intracommunautaire
address_line1   VARCHAR(255)
address_line2   VARCHAR(255)
postal_code     VARCHAR(10)
city            VARCHAR(100)
country         VARCHAR(2)      -- Code ISO 3166-1 alpha-2
phone           VARCHAR(20)
email           VARCHAR(255)
website         VARCHAR(255)
logo_url        VARCHAR(500)
logo_dark_url   VARCHAR(500)
brand_colors    JSONB           -- {primary, secondary, accent}
brand_fonts     JSONB           -- {title_font, body_font}
default_currency VARCHAR(3)    -- Code ISO 4217
secondary_currencies JSONB     -- Liste de codes devise
default_language VARCHAR(5)    -- Code locale (fr_FR, en_US)
parent_entity_id UUID          FK -> Entity(id) NULLABLE
is_active       BOOLEAN        DEFAULT true
created_at      TIMESTAMP      NOT NULL
updated_at      TIMESTAMP      NOT NULL
created_by      UUID           FK -> User(id)
```

```
UserProfile
----------------------------------------------
id              UUID            PK
user_id         UUID            FK -> User(id) UNIQUE NOT NULL
first_name      VARCHAR(100)    NOT NULL
last_name       VARCHAR(100)    NOT NULL
email           VARCHAR(255)    UNIQUE NOT NULL
phone           VARCHAR(20)
job_title       VARCHAR(100)
language        VARCHAR(5)      DEFAULT 'fr_FR'
timezone        VARCHAR(50)     DEFAULT 'Europe/Paris'
avatar_url      VARCHAR(500)
two_factor_enabled BOOLEAN      DEFAULT false
two_factor_secret  VARCHAR(255) -- Chiffre (TOTP secret)
backup_codes    JSONB           -- Codes de secours hashes
entity_id       UUID            FK -> Entity(id)
department_id   UUID            FK -> Department(id) NULLABLE
role            VARCHAR(50)     NOT NULL -- admin_global, admin_entity, manager, collaborator, reader, accountant
is_active       BOOLEAN         DEFAULT true
last_login_at   TIMESTAMP
created_at      TIMESTAMP       NOT NULL
updated_at      TIMESTAMP       NOT NULL
```

```
AppSettings
----------------------------------------------
id              UUID            PK
entity_id       UUID            FK -> Entity(id) NOT NULL
module          VARCHAR(50)     NOT NULL -- projects, billing, time, team, etc.
key             VARCHAR(100)    NOT NULL
value           JSONB           NOT NULL
is_inherited    BOOLEAN         DEFAULT true
overridden_at   TIMESTAMP       NULLABLE
overridden_by   UUID            FK -> User(id) NULLABLE
created_at      TIMESTAMP       NOT NULL
updated_at      TIMESTAMP       NOT NULL
-- UNIQUE CONSTRAINT (entity_id, module, key)
```

```
Department
----------------------------------------------
id              UUID            PK
entity_id       UUID            FK -> Entity(id) NOT NULL
name            VARCHAR(100)    NOT NULL
code            VARCHAR(20)     -- Code comptable
manager_id      UUID            FK -> User(id) NULLABLE
is_active       BOOLEAN         DEFAULT true
created_at      TIMESTAMP       NOT NULL
updated_at      TIMESTAMP       NOT NULL
-- UNIQUE CONSTRAINT (entity_id, name)
```

```
ProjectPhaseTemplate
----------------------------------------------
id              UUID            PK
entity_id       UUID            FK -> Entity(id) NOT NULL
code            VARCHAR(10)     NOT NULL -- ESQ, APS, APD, etc.
name            VARCHAR(100)    NOT NULL
percentage      DECIMAL(5,2)    DEFAULT 0 -- Pourcentage par defaut
sort_order      INTEGER         NOT NULL
is_active       BOOLEAN         DEFAULT true
created_at      TIMESTAMP       NOT NULL
updated_at      TIMESTAMP       NOT NULL
-- UNIQUE CONSTRAINT (entity_id, code)
```

```
ProjectLabel
----------------------------------------------
id              UUID            PK
entity_id       UUID            FK -> Entity(id) NOT NULL
name            VARCHAR(50)     NOT NULL
color           VARCHAR(7)      NOT NULL -- #RRGGBB
category        VARCHAR(50)     NULLABLE
is_active       BOOLEAN         DEFAULT true
created_at      TIMESTAMP       NOT NULL
updated_at      TIMESTAMP       NOT NULL
```

```
ProjectStatus
----------------------------------------------
id              UUID            PK
entity_id       UUID            FK -> Entity(id) NOT NULL
name            VARCHAR(50)     NOT NULL
color           VARCHAR(7)      NOT NULL -- #RRGGBB
icon            VARCHAR(50)     NULLABLE
sort_order      INTEGER         NOT NULL
is_default      BOOLEAN         DEFAULT false
is_system       BOOLEAN         DEFAULT false -- true pour les statuts non supprimables
created_at      TIMESTAMP       NOT NULL
updated_at      TIMESTAMP       NOT NULL
```

```
ProjectStatusTransition
----------------------------------------------
id              UUID            PK
entity_id       UUID            FK -> Entity(id) NOT NULL
from_status_id  UUID            FK -> ProjectStatus(id) NOT NULL
to_status_id    UUID            FK -> ProjectStatus(id) NOT NULL
created_at      TIMESTAMP       NOT NULL
-- UNIQUE CONSTRAINT (entity_id, from_status_id, to_status_id)
```

```
InvoiceTemplate
----------------------------------------------
id              UUID            PK
entity_id       UUID            FK -> Entity(id) NOT NULL
name            VARCHAR(100)    NOT NULL
template_type   VARCHAR(20)     NOT NULL -- invoice, credit_note, proforma, fee_statement
layout          JSONB           NOT NULL -- Configuration de mise en page
is_default      BOOLEAN         DEFAULT false
is_active       BOOLEAN         DEFAULT true
created_at      TIMESTAMP       NOT NULL
updated_at      TIMESTAMP       NOT NULL
```

```
TaxRate
----------------------------------------------
id              UUID            PK
entity_id       UUID            FK -> Entity(id) NOT NULL
name            VARCHAR(50)     NOT NULL
rate            DECIMAL(5,2)    NOT NULL -- en pourcentage
is_default      BOOLEAN         DEFAULT false
is_active       BOOLEAN         DEFAULT true
created_at      TIMESTAMP       NOT NULL
updated_at      TIMESTAMP       NOT NULL
```

```
TimeType
----------------------------------------------
id              UUID            PK
entity_id       UUID            FK -> Entity(id) NOT NULL
code            VARCHAR(20)     NOT NULL
name            VARCHAR(100)    NOT NULL
category        VARCHAR(20)     NOT NULL -- productive, non_productive
is_billable     BOOLEAN         DEFAULT true
color           VARCHAR(7)      -- #RRGGBB
is_active       BOOLEAN         DEFAULT true
sort_order      INTEGER         NOT NULL
created_at      TIMESTAMP       NOT NULL
updated_at      TIMESTAMP       NOT NULL
-- UNIQUE CONSTRAINT (entity_id, code)
```

```
Holiday
----------------------------------------------
id              UUID            PK
entity_id       UUID            FK -> Entity(id) NOT NULL
name            VARCHAR(100)    NOT NULL
date            DATE            NOT NULL
is_recurring    BOOLEAN         DEFAULT false -- Annuel
country_code    VARCHAR(2)      NULLABLE -- NULL = specifique a l'entite
is_custom       BOOLEAN         DEFAULT false
created_at      TIMESTAMP       NOT NULL
updated_at      TIMESTAMP       NOT NULL
```

```
IntegrationConfig
----------------------------------------------
id              UUID            PK
entity_id       UUID            FK -> Entity(id) NOT NULL
provider        VARCHAR(50)     NOT NULL -- sage, quickbooks, google_calendar, etc.
display_name    VARCHAR(100)    NOT NULL
category        VARCHAR(50)     NOT NULL -- accounting, calendar, storage, communication, bim
auth_type       VARCHAR(20)     NOT NULL -- oauth2, api_key, webhook
api_key_encrypted VARCHAR(500)  NULLABLE -- Chiffre AES-256
oauth_token_encrypted TEXT      NULLABLE -- Chiffre AES-256
oauth_refresh_token_encrypted TEXT NULLABLE
token_expires_at TIMESTAMP      NULLABLE
settings        JSONB           DEFAULT '{}' -- Config specifique (frequence sync, direction, filtres)
sync_direction  VARCHAR(20)     DEFAULT 'bidirectional' -- to_ooti, from_ooti, bidirectional
sync_frequency  VARCHAR(20)     DEFAULT 'hourly' -- realtime, hourly, daily, manual
is_active       BOOLEAN         DEFAULT false
last_sync_at    TIMESTAMP       NULLABLE
connected_at    TIMESTAMP       NULLABLE
connected_by    UUID            FK -> User(id) NULLABLE
created_at      TIMESTAMP       NOT NULL
updated_at      TIMESTAMP       NOT NULL
-- UNIQUE CONSTRAINT (entity_id, provider)
```

```
IntegrationSyncLog
----------------------------------------------
id              UUID            PK
integration_id  UUID            FK -> IntegrationConfig(id) NOT NULL
action          VARCHAR(20)     NOT NULL -- create, update, delete, sync
records_processed INTEGER       DEFAULT 0
records_success INTEGER         DEFAULT 0
records_error   INTEGER         DEFAULT 0
status          VARCHAR(20)     NOT NULL -- success, error, warning, in_progress
error_details   TEXT            NULLABLE
started_at      TIMESTAMP       NOT NULL
completed_at    TIMESTAMP       NULLABLE
```

```
WebhookConfig
----------------------------------------------
id              UUID            PK
entity_id       UUID            FK -> Entity(id) NOT NULL
url             VARCHAR(500)    NOT NULL
events          JSONB           NOT NULL -- Liste des evenements declencheurs
secret          VARCHAR(255)    NOT NULL -- HMAC secret
is_active       BOOLEAN         DEFAULT true
last_triggered_at TIMESTAMP     NULLABLE
created_at      TIMESTAMP       NOT NULL
updated_at      TIMESTAMP       NOT NULL
```

```
Subscription
----------------------------------------------
id              UUID            PK
entity_id       UUID            FK -> Entity(id) UNIQUE NOT NULL
plan            VARCHAR(50)     NOT NULL -- starter, professional, enterprise
status          VARCHAR(20)     NOT NULL -- active, past_due, canceled, trialing
billing_cycle   VARCHAR(10)     NOT NULL -- monthly, yearly
price_cents     INTEGER         NOT NULL
currency        VARCHAR(3)      DEFAULT 'EUR'
users_included  INTEGER         NOT NULL
users_count     INTEGER         DEFAULT 0
storage_limit_mb INTEGER       NOT NULL
storage_used_mb  INTEGER        DEFAULT 0
current_period_start DATE       NOT NULL
current_period_end   DATE       NOT NULL
stripe_customer_id   VARCHAR(100) NULLABLE
stripe_subscription_id VARCHAR(100) NULLABLE
canceled_at     TIMESTAMP       NULLABLE
cancel_reason   TEXT            NULLABLE
created_at      TIMESTAMP       NOT NULL
updated_at      TIMESTAMP       NOT NULL
```

```
SubscriptionInvoice
----------------------------------------------
id              UUID            PK
subscription_id UUID            FK -> Subscription(id) NOT NULL
invoice_number  VARCHAR(50)     NOT NULL
amount_cents    INTEGER         NOT NULL
currency        VARCHAR(3)      DEFAULT 'EUR'
status          VARCHAR(20)     NOT NULL -- paid, pending, failed
invoice_date    DATE            NOT NULL
pdf_url         VARCHAR(500)    NULLABLE
stripe_invoice_id VARCHAR(100)  NULLABLE
created_at      TIMESTAMP       NOT NULL
```

```
DataImport
----------------------------------------------
id              UUID            PK
entity_id       UUID            FK -> Entity(id) NOT NULL
import_type     VARCHAR(50)     NOT NULL -- projects, clients, collaborators, time_entries, invoices
file_name       VARCHAR(255)    NOT NULL
file_size_bytes INTEGER         NOT NULL
column_mapping  JSONB           NOT NULL -- Correspondance colonnes fichier -> champs OOTI
status          VARCHAR(20)     NOT NULL -- pending, validating, importing, completed, failed, rolled_back
total_rows      INTEGER         DEFAULT 0
imported_rows   INTEGER         DEFAULT 0
skipped_rows    INTEGER         DEFAULT 0
error_rows      INTEGER         DEFAULT 0
error_report_url VARCHAR(500)   NULLABLE
rollback_available_until TIMESTAMP NULLABLE -- created_at + 24h
started_at      TIMESTAMP       NULLABLE
completed_at    TIMESTAMP       NULLABLE
created_by      UUID            FK -> User(id) NOT NULL
created_at      TIMESTAMP       NOT NULL
updated_at      TIMESTAMP       NOT NULL
```

```
DataExport
----------------------------------------------
id              UUID            PK
entity_id       UUID            FK -> Entity(id) NOT NULL
export_type     VARCHAR(50)     NOT NULL -- projects, clients, collaborators, time_entries, invoices, budget
format          VARCHAR(10)     NOT NULL -- csv, xlsx, pdf
filters         JSONB           DEFAULT '{}' -- Filtres appliques
columns         JSONB           NULLABLE -- Colonnes selectionnees (null = toutes)
status          VARCHAR(20)     NOT NULL -- pending, generating, completed, failed
total_records   INTEGER         DEFAULT 0
file_url        VARCHAR(500)    NULLABLE
file_expires_at TIMESTAMP       NULLABLE -- created_at + 7 jours
is_scheduled    BOOLEAN         DEFAULT false
schedule_frequency VARCHAR(20)  NULLABLE -- daily, weekly, monthly
schedule_email  VARCHAR(255)    NULLABLE
created_by      UUID            FK -> User(id) NOT NULL
created_at      TIMESTAMP       NOT NULL
updated_at      TIMESTAMP       NOT NULL
```

```
NotificationPreference
----------------------------------------------
id              UUID            PK
user_id         UUID            FK -> User(id) NOT NULL
event_category  VARCHAR(50)     NOT NULL -- projects, billing, time, team, system
event_type      VARCHAR(100)    NOT NULL -- project_created, invoice_paid, time_reminder, etc.
channel_email   BOOLEAN         DEFAULT true
channel_in_app  BOOLEAN         DEFAULT true
created_at      TIMESTAMP       NOT NULL
updated_at      TIMESTAMP       NOT NULL
-- UNIQUE CONSTRAINT (user_id, event_category, event_type)
```

```
NotificationGlobalSettings
----------------------------------------------
id              UUID            PK
user_id         UUID            FK -> User(id) UNIQUE NOT NULL
email_frequency VARCHAR(20)     DEFAULT 'realtime' -- realtime, daily, weekly
dnd_start_time  TIME            NULLABLE -- Debut "Ne pas deranger"
dnd_end_time    TIME            NULLABLE -- Fin "Ne pas deranger"
created_at      TIMESTAMP       NOT NULL
updated_at      TIMESTAMP       NOT NULL
```

```
OnboardingProgress
----------------------------------------------
id              UUID            PK
entity_id       UUID            FK -> Entity(id) UNIQUE NOT NULL
user_id         UUID            FK -> User(id) NOT NULL
step_1_password BOOLEAN         DEFAULT false
step_2_account  BOOLEAN         DEFAULT false
step_3_team     BOOLEAN         DEFAULT false
step_4_projects BOOLEAN         DEFAULT false
step_5_billing  BOOLEAN         DEFAULT false
step_6_time     BOOLEAN         DEFAULT false
step_7_costs    BOOLEAN         DEFAULT false
step_8_planning BOOLEAN         DEFAULT false
step_9_data     BOOLEAN         DEFAULT false
step_10_complete BOOLEAN        DEFAULT false
current_step    INTEGER         DEFAULT 1
is_completed    BOOLEAN         DEFAULT false
completed_at    TIMESTAMP       NULLABLE
created_at      TIMESTAMP       NOT NULL
updated_at      TIMESTAMP       NOT NULL
```

```
UserSession
----------------------------------------------
id              UUID            PK
user_id         UUID            FK -> User(id) NOT NULL
token_hash      VARCHAR(255)    NOT NULL
device_type     VARCHAR(20)     -- desktop, mobile, tablet
browser         VARCHAR(50)
browser_version VARCHAR(20)
os              VARCHAR(50)
ip_address      VARCHAR(45)     -- IPv4 ou IPv6 (partiellement masque en affichage)
is_current      BOOLEAN         DEFAULT false
last_activity_at TIMESTAMP      NOT NULL
expires_at      TIMESTAMP       NOT NULL
created_at      TIMESTAMP       NOT NULL
```

```
LoginHistory
----------------------------------------------
id              UUID            PK
user_id         UUID            FK -> User(id) NOT NULL
ip_address      VARCHAR(45)
device_type     VARCHAR(20)
browser         VARCHAR(50)
status          VARCHAR(20)     NOT NULL -- success, failed, two_factor_required, locked
failure_reason  VARCHAR(100)    NULLABLE
created_at      TIMESTAMP       NOT NULL
```

```
AuditLog
----------------------------------------------
id              UUID            PK
entity_id       UUID            FK -> Entity(id) NOT NULL
user_id         UUID            FK -> User(id) NOT NULL
action          VARCHAR(50)     NOT NULL -- create, update, delete, activate, deactivate
section         VARCHAR(50)     NOT NULL -- general, branding, projects, billing, time, team, modules, etc.
resource_type   VARCHAR(50)     NOT NULL -- entity, department, phase_template, tax_rate, etc.
resource_id     UUID            NULLABLE
field_name      VARCHAR(100)    NULLABLE
old_value       TEXT            NULLABLE
new_value       TEXT            NULLABLE
is_critical     BOOLEAN         DEFAULT false
ip_address      VARCHAR(45)
created_at      TIMESTAMP       NOT NULL
-- INDEX on (entity_id, created_at DESC)
-- INDEX on (user_id, created_at DESC)
```

```
ModuleConfig
----------------------------------------------
id              UUID            PK
entity_id       UUID            FK -> Entity(id) NOT NULL
module_name     VARCHAR(50)     NOT NULL -- projects, fees, billing, time, team, clients, budgets, reports, documents, planning
is_enabled      BOOLEAN         DEFAULT true
is_core         BOOLEAN         DEFAULT false -- true = ne peut pas etre desactive
depends_on      JSONB           DEFAULT '[]' -- Liste des modules prerequis
disabled_at     TIMESTAMP       NULLABLE
disabled_by     UUID            FK -> User(id) NULLABLE
created_at      TIMESTAMP       NOT NULL
updated_at      TIMESTAMP       NOT NULL
-- UNIQUE CONSTRAINT (entity_id, module_name)
```

### 11.2 Diagramme des relations

```
Entity (1) ----< (N) Department
Entity (1) ----< (N) UserProfile
Entity (1) ----< (N) AppSettings
Entity (1) ----< (N) ProjectPhaseTemplate
Entity (1) ----< (N) ProjectLabel
Entity (1) ----< (N) ProjectStatus
Entity (1) ----< (N) InvoiceTemplate
Entity (1) ----< (N) TaxRate
Entity (1) ----< (N) TimeType
Entity (1) ----< (N) Holiday
Entity (1) ----< (N) IntegrationConfig
Entity (1) ----< (N) WebhookConfig
Entity (1) ----> (1) Subscription
Entity (1) ----< (N) DataImport
Entity (1) ----< (N) DataExport
Entity (1) ----< (N) ModuleConfig
Entity (1) ----< (N) AuditLog
Entity (1) ----> (0..1) Entity [parent_entity_id, auto-reference]
Entity (1) ----> (1) OnboardingProgress

UserProfile (1) ----< (N) UserSession
UserProfile (1) ----< (N) LoginHistory
UserProfile (1) ----< (N) NotificationPreference
UserProfile (1) ----> (1) NotificationGlobalSettings

IntegrationConfig (1) ----< (N) IntegrationSyncLog
Subscription (1) ----< (N) SubscriptionInvoice

ProjectStatus (N) ----< (N) ProjectStatusTransition
```

---

## 12. Estimation

### 12.1 Synthese globale

| Parametre | Valeur |
|---|---|
| **Duree totale estimee** | 7 semaines |
| **Nombre de sprints** | 5 sprints de 2 semaines (avec chevauchement) |
| **Effort total** | 280-350 points d'effort (story points) |
| **Taille de l'equipe** | 5-6 developpeurs + 1 QA + 1 Designer |
| **Complexite globale** | Elevee (transversalite, multi-entites, integrations) |

### 12.2 Estimation par User Story

| User Story | Complexite | Story Points | Sprint |
|---|---|---|---|
| **US-CF01** : Profil utilisateur | Moyenne | 13 | Sprint 1 |
| **US-CF02** : Securite et authentification | Elevee | 21 | Sprint 1 |
| **US-CF03** : Preferences de notifications | Moyenne | 13 | Sprint 1 |
| **US-CF04** : Parametres generaux agence | Moyenne | 13 | Sprint 2 |
| **US-CF05** : Charte graphique | Moyenne | 13 | Sprint 2 |
| **US-CF06** : Configuration projets par defaut | Elevee | 21 | Sprint 2 |
| **US-CF07** : Configuration facturation | Elevee | 21 | Sprint 3 |
| **US-CF08** : Configuration du temps | Moyenne | 13 | Sprint 3 |
| **US-CF09** : Configuration equipe et entites | Elevee | 21 | Sprint 3 |
| **US-CF10** : Import de donnees en masse | Tres elevee | 34 | Sprint 4 |
| **US-CF11** : Export de donnees | Elevee | 21 | Sprint 4 |
| **US-CF12** : Gestion des integrations | Elevee | 21 | Sprint 4 |
| **US-CF13** : Activation/desactivation modules | Moyenne | 13 | Sprint 5 |
| **US-CF14** : Gestion de l'abonnement | Elevee | 21 | Sprint 5 |
| **US-CF15** : Onboarding guide | Elevee | 21 | Sprint 5 |
| **Transverse** : Audit trail, multi-entites, sidebar | Elevee | 34 | Sprints 1-5 |
| **TOTAL** | | **314 SP** | |

### 12.3 Planning par sprint

#### Sprint 1 (Semaines 1-2) : Fondations et profil utilisateur
- **Objectif** : Mettre en place l'architecture du module, la sidebar de navigation et les fonctionnalites de profil utilisateur.
- **User Stories** : US-CF01, US-CF02, US-CF03
- **Livrables** :
  - Architecture de la sidebar de parametres avec navigation
  - Page Profil (informations personnelles, avatar, langue, fuseau horaire)
  - Page Securite (mot de passe, 2FA, sessions actives, historique de connexion)
  - Page Notifications (preferences par evenement et par canal)
  - Composants transverses : formulaires, color picker, selectors, notifications de sauvegarde
  - Modele de donnees : UserProfile, UserSession, LoginHistory, NotificationPreference, NotificationGlobalSettings
- **Points** : 47 SP

#### Sprint 2 (Semaines 3-4) : Parametres de l'agence
- **Objectif** : Implementer les parametres generaux, la charte graphique et la configuration des projets.
- **User Stories** : US-CF04, US-CF05, US-CF06
- **Livrables** :
  - Page Parametres generaux (raison sociale, SIRET, adresse, TVA, devises, langues)
  - Page Charte graphique (logo, couleurs, polices, apercu en temps reel)
  - Page Configuration projets (phases par defaut, etiquettes, statuts, workflow de transition)
  - Systeme d'heritage multi-entites (debut de l'implementation)
  - Modele de donnees : Entity (complet), AppSettings, ProjectPhaseTemplate, ProjectLabel, ProjectStatus, ProjectStatusTransition, TaxRate
- **Points** : 47 SP

#### Sprint 3 (Semaines 5-6) : Facturation, temps et equipe
- **Objectif** : Implementer les parametres de facturation, de temps et la configuration equipe/entites.
- **User Stories** : US-CF07, US-CF08, US-CF09
- **Livrables** :
  - Page Configuration facturation (numerotation, conditions de paiement, mentions legales, modeles PDF avec apercu)
  - Page Configuration temps (heures/jour, jours ouvres, jours feries, types de temps, arrondi, rappels)
  - Page Configuration equipe (entites en arborescence, departements, heritage de parametres)
  - Generateur d'apercu PDF pour les modeles de facture
  - Modele de donnees : InvoiceTemplate, TimeType, Holiday, Department, ModuleConfig
- **Points** : 55 SP

#### Sprint 4 (Semaines 7-8) : Donnees et integrations
- **Objectif** : Implementer les fonctionnalites d'import/export en masse et la gestion des integrations.
- **User Stories** : US-CF10, US-CF11, US-CF12
- **Livrables** :
  - Page Import (upload, mapping des colonnes, validation, import en arriere-plan, rapport, rollback)
  - Page Export (selection des donnees, filtres, formats, export programme, export RGPD)
  - Page Integrations (catalogue, connexion OAuth2/API key, configuration, journal de synchronisation, webhooks)
  - Processeur de taches asynchrones pour import/export
  - Modele de donnees : DataImport, DataExport, IntegrationConfig, IntegrationSyncLog, WebhookConfig
- **Points** : 76 SP

#### Sprint 5 (Semaines 9-10) : Modules, abonnement, onboarding et finalisation
- **Objectif** : Implementer la gestion des modules, l'abonnement, l'onboarding et finaliser les elements transverses.
- **User Stories** : US-CF13, US-CF14, US-CF15
- **Livrables** :
  - Page Modules (liste, toggle activation/desactivation, dependances, modules coeur)
  - Page Abonnement (plan, utilisation, changement de plan, historique, paiement, annulation)
  - Parcours d'onboarding en 10 etapes (barre de progression, formulaires simplifies, bulles d'aide)
  - Page Assistance (liens centre d'aide, formulaire de contact, documentation API)
  - Audit trail complet et historique des modifications
  - Integration Stripe pour l'abonnement
  - Modele de donnees : Subscription, SubscriptionInvoice, OnboardingProgress, AuditLog
  - Tests de regression globaux, tests de performance, tests d'accessibilite
- **Points** : 89 SP

### 12.4 Risques et mitigations

| Risque | Probabilite | Impact | Mitigation |
|---|---|---|---|
| Complexite du systeme d'heritage multi-entites | Elevee | Eleve | Prototypage en Sprint 1, tests unitaires extensifs, revue d'architecture dediee |
| Integration Stripe et conformite PCI DSS | Moyenne | Eleve | Utiliser Stripe Elements (iframe) pour eviter le contact avec les donnees de carte, audit de securite |
| Performance des imports en masse (> 50 000 lignes) | Moyenne | Moyen | Traitement par lots (batch processing), file de taches asynchrone, tests de charge |
| Coherence des parametres entre les modules consommateurs | Elevee | Moyen | Definir des contrats d'interface clairs (API internes), tests d'integration inter-modules |
| Complexite des modeles de facture PDF personnalises | Moyenne | Moyen | Limiter la personnalisation en v1 (modeles pre-configures avec parametres), iterations ulterieures |
| Regression sur les modules existants lors de l'activation/desactivation | Moyenne | Eleve | Feature flags, tests de regression automatises, deploiement progressif |
| Retard sur les dependances (EPIC-001, EPIC-013, EPIC-014) | Moyenne | Eleve | Stubs et mocks pour les developpements en parallele, points de synchronisation bi-hebdomadaires |

### 12.5 Hypotheses

- L'EPIC-001 (Authentification & Utilisateurs) est au minimum partiellement livre avant le debut du Sprint 1 (systeme de sessions et roles disponible).
- L'infrastructure technique (PostgreSQL, Redis, S3, service d'email) est provisionnee et accessible avant le Sprint 1.
- Les maquettes UX/UI des ecrans principaux sont validees avant le debut de chaque sprint.
- L'integration Stripe est validee sur un compte de test avant le Sprint 5.
- L'equipe dispose d'une expertise prealable sur les librairies de generation PDF et le traitement de fichiers CSV/XLSX.

---

*Document redige dans le cadre du projet OOTI — Module Configuration & Administration*
*EPIC-016 — Version 1.0 — Fevrier 2026*
