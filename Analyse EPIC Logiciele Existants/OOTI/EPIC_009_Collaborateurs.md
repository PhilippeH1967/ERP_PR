**EPIC — Module Collaborateurs & RH**

Application OOTI — Gestion de projets pour cabinets d'architecture

Version 1.0 — Février 2026

# **1. Identification de l'EPIC**

**Nom de l'EPIC :** Collaborateurs & RH

**Référence :** EPIC-009

**Module parent :** Équipe

**Priorité :** Haute

**Statut :** À planifier

**Date de création :** Février 2026

**Auteur :** —

**EPICs liés :** EPIC-002 (Projets), EPIC-005 (Temps), EPIC-006 (Planning), EPIC-007 (Coûts), EPIC-012 (Validation)

# **2. Contexte & Problématique**

Dans un cabinet d'architecture, les collaborateurs constituent la ressource principale de l'activité. La gestion des équipes — architectes, chefs de projet, directeurs, chargés d'affaires, stagiaires — nécessite un suivi rigoureux des compétences, des rôles, des contrats, des taux horaires et de la disponibilité de chacun. Sans outil centralisé, ces informations sont dispersées entre des fichiers Excel, des dossiers RH papier et des échanges informels, ce qui engendre :

- **Une perte de visibilité** sur les ressources disponibles et leurs compétences réelles ;
- **Des erreurs d'affectation** : un collaborateur assigné à un projet sans disposer des compétences requises (BIM, Revit, AutoCAD) ;
- **Une impossibilité de piloter les coûts salariaux** en temps réel, faute de connaître les taux horaires et le temps de travail contractuel de chaque collaborateur ;
- **Un processus d'onboarding laborieux** : invitations manuelles, création de comptes dispersée, absence de workflow structuré ;
- **Une gestion des permissions approximative** : droits d'accès attribués de manière informelle, sans matrice claire par rôle.

Les cabinets d'architecture de taille moyenne (10 à 100 collaborateurs) ont besoin d'un module dédié qui centralise l'ensemble des données collaborateurs, permet une gestion fine des rôles et permissions, offre une vision consolidée des compétences de l'agence et s'intègre nativement avec les modules de projets, de saisie des temps, de planning et de coûts.

# **3. Objectif de l'EPIC**

Permettre aux utilisateurs de OOTI de gérer l'ensemble du cycle de vie de leurs collaborateurs depuis le module **Équipe > Collaborateurs** : créer et administrer les fiches collaborateurs, définir les rôles et permissions, gérer les compétences techniques, configurer les paramètres RH (contrat, taux horaire, temps de travail), inviter de nouveaux membres par email, et visualiser des indicateurs clés sur les ressources humaines de l'agence.

Ce module doit offrir quatre sous-vues principales — **Résumé**, **Collaborateurs**, **Rôles**, **Compétences** — et s'intégrer avec les modules Projets, Temps, Planning et Coûts pour garantir la cohérence des données de ressources dans toute l'application.

# **4. Périmètre Fonctionnel**

## **4.1 Résumé des collaborateurs (niveau Agence)**

- Vue tableau de bord avec indicateurs clés (KPIs) sur l'ensemble des collaborateurs
- Nombre total de collaborateurs, collaborateurs actifs, collaborateurs inactifs
- Taux d'occupation global de l'agence
- Répartition des collaborateurs par rôle (graphique)
- Répartition par type de contrat (CDI, CDD, Freelance)
- Accès rapide aux actions principales (ajout d'un collaborateur, alertes)

## **4.2 Liste et fiches des collaborateurs**

- Liste tabulaire de tous les collaborateurs avec recherche et filtres
- Fiche collaborateur détaillée (informations personnelles, contrat, projets, temps, compétences)
- Création d'un nouveau collaborateur (formulaire complet)
- Édition des informations d'un collaborateur existant
- Archivage et désactivation d'un collaborateur
- Invitation par email d'un nouveau collaborateur

## **4.3 Gestion des rôles et permissions**

- Création, édition et suppression de rôles
- Rôles prédéfinis : Architecte, Chef de projet, Directeur, Administrateur, Chargé d'affaires, Stagiaire
- Matrice de permissions par rôle (lecture, écriture, validation, administration)
- Attribution d'un rôle à chaque collaborateur

## **4.4 Gestion des compétences**

- Catalogue de compétences de l'agence (BIM, Revit, AutoCAD, SketchUp, ArchiCAD, Rhino, etc.)
- Création, édition et suppression de compétences
- Catégorisation des compétences (Logiciels, Métier, Langues, Certifications)
- Attribution de compétences aux collaborateurs avec niveau de maîtrise
- Matrice de compétences de l'agence (vue croisée collaborateurs × compétences)

## **4.5 Paramètres RH**

- Type de contrat : CDI, CDD, Freelance, Stage
- Taux horaire interne (coût pour l'agence)
- Temps de travail hebdomadaire contractuel (heures/semaine)
- Date de début et date de fin de contrat
- Gestion des congés et absences (solde, historique)
- Rattachement à une équipe/entité

# **5. User Stories**

## **US-CO01 — Vue résumé des collaborateurs**

**En tant que** Directeur d'agence / Responsable RH

**Je veux** accéder à une vue résumé de l'ensemble des collaborateurs de mon agence

**Afin de** visualiser en un coup d'oeil les indicateurs clés de mes ressources humaines et détecter les déséquilibres

**Critères d'acceptance :**

- Le résumé affiche le KPI « Nombre total de collaborateurs » avec distinction actifs / inactifs
- Le résumé affiche le KPI « Taux d'occupation moyen » de l'agence, calculé à partir des temps saisis et du temps de travail contractuel de chaque collaborateur actif
- Un graphique de répartition par rôle est affiché (diagramme en barres ou camembert) montrant le nombre de collaborateurs par rôle (Architecte, Chef de projet, Directeur, etc.)
- Un graphique de répartition par type de contrat est affiché (CDI, CDD, Freelance, Stage)
- Le KPI « Coût salarial mensuel estimé » est calculé à partir des taux horaires × heures hebdomadaires × 4,33 semaines pour tous les collaborateurs actifs
- Des actions rapides sont disponibles : « + Nouveau collaborateur », « Alertes RH », « Exporter »
- La vue est accessible via le menu latéral > Équipe > Collaborateurs > Résumé
- Les données affichées se mettent à jour en temps réel lors de l'ajout, de la modification ou de l'archivage d'un collaborateur

## **US-CO02 — Liste des collaborateurs**

**En tant que** Chef de projet / Directeur d'agence

**Je veux** consulter la liste complète de tous les collaborateurs de l'agence

**Afin de** trouver rapidement un collaborateur, vérifier son rôle, ses projets et son statut

**Critères d'acceptance :**

- La liste affiche les colonnes : Photo (avatar), Nom complet, Email, Téléphone, Rôle, Équipe/Entité, Projets assignés (nombre), Statut (actif/inactif), Type de contrat
- Un filtre par statut est disponible (Tous, Actifs, Inactifs)
- Un filtre par rôle est disponible (Tous les rôles, Architecte, Chef de projet, etc.)
- Un filtre par équipe/entité est disponible
- Une recherche plein texte par nom ou email est disponible
- Le bouton ACTIONS permet : Export CSV/Excel, Afficher/masquer les colonnes, Import de collaborateurs
- Chaque ligne est cliquable et redirige vers la fiche détaillée du collaborateur
- Le tri est possible sur chaque colonne (ordre alphabétique, nombre de projets, etc.)
- Le bouton « + Nouveau collaborateur » est visible en haut de la liste

## **US-CO03 — Création d'un collaborateur**

**En tant que** Directeur d'agence / Administrateur

**Je veux** créer un nouveau collaborateur dans le système

**Afin d'** enregistrer ses informations et lui permettre d'accéder à l'application selon son rôle

**Critères d'acceptance :**

- Un formulaire de création s'ouvre via le bouton « + Nouveau collaborateur »
- Les champs obligatoires sont : Prénom, Nom, Email, Rôle
- Les champs optionnels sont : Téléphone, Photo de profil, Équipe/Entité, Type de contrat (CDI/CDD/Freelance/Stage), Taux horaire (€/h), Temps de travail hebdomadaire (heures), Date de début de contrat, Date de fin de contrat (si CDD/Stage), Compétences
- L'email doit être unique dans le système ; un message d'erreur explicite s'affiche si l'email est déjà utilisé
- Le rôle est sélectionnable dans la liste des rôles existants (dropdown)
- La photo de profil peut être uploadée (formats acceptés : JPG, PNG ; taille max : 2 Mo)
- À la validation, le collaborateur est créé avec le statut « Actif » et l'utilisateur est redirigé vers sa fiche détaillée
- Un message de confirmation s'affiche après la création
- Les champs obligatoires non remplis déclenchent un message d'erreur inline

## **US-CO04 — Fiche collaborateur détaillée**

**En tant que** Chef de projet / Directeur d'agence / le collaborateur lui-même

**Je veux** accéder à la fiche détaillée d'un collaborateur

**Afin de** consulter l'ensemble de ses informations personnelles, contractuelles, ses projets, ses temps et ses compétences

**Critères d'acceptance :**

- La fiche affiche l'en-tête avec : Photo de profil (modifiable), Nom complet, Rôle, Statut (badge Actif/Inactif), Équipe/Entité
- La section « Informations personnelles » affiche : Prénom, Nom, Email, Téléphone, tous modifiables en mode édition
- La section « Contrat & RH » affiche : Type de contrat, Taux horaire, Temps de travail hebdomadaire, Date de début, Date de fin, Coût mensuel estimé (calculé)
- La section « Projets » liste tous les projets auxquels le collaborateur est assigné avec le rôle occupé dans chaque projet, le statut du projet et un lien cliquable vers le résumé du projet
- La section « Temps » affiche un résumé des heures saisies : total heures du mois en cours, total heures de l'année, graphique d'évolution mensuelle
- La section « Compétences » liste les compétences attribuées avec leur niveau de maîtrise (Débutant, Intermédiaire, Avancé, Expert)
- Un bouton « Modifier » active le mode édition de la fiche
- Un bouton « Archiver » permet de désactiver le collaborateur (avec confirmation)

## **US-CO05 — Invitation par email**

**En tant que** Directeur d'agence / Administrateur

**Je veux** inviter un nouveau collaborateur par email

**Afin qu'** il reçoive un lien d'invitation pour créer son compte, compléter son profil et accéder à l'application

**Critères d'acceptance :**

- Un bouton « Inviter par email » est disponible depuis la liste des collaborateurs ou depuis le formulaire de création
- L'utilisateur saisit l'adresse email du collaborateur à inviter
- Un email d'invitation est envoyé contenant : le nom de l'agence, un message de bienvenue personnalisable, un lien unique sécurisé d'activation (valide 7 jours)
- Le collaborateur invité apparaît dans la liste avec le statut « Invitation envoyée » (badge distinct)
- Le lien d'invitation permet au collaborateur de créer son mot de passe et de compléter son profil (prénom, nom, téléphone, photo)
- Si le lien expire, un bouton « Renvoyer l'invitation » est disponible dans la liste des collaborateurs
- Un historique des invitations envoyées est consultable (date d'envoi, statut : envoyée, acceptée, expirée)
- Le rôle et l'équipe peuvent être prédéfinis lors de l'invitation

## **US-CO06 — Gestion des rôles**

**En tant que** Administrateur

**Je veux** créer, modifier et supprimer les rôles de l'agence

**Afin de** structurer l'organisation de mon cabinet et définir les niveaux de responsabilité

**Critères d'acceptance :**

- La vue « Rôles » est accessible via le sous-menu Équipe > Collaborateurs > Rôles
- Les rôles prédéfinis sont disponibles par défaut : Administrateur, Directeur, Chef de projet, Architecte, Chargé d'affaires, Stagiaire
- Les rôles prédéfinis ne peuvent pas être supprimés mais peuvent être renommés et leurs permissions modifiées
- Un bouton « + Nouveau rôle » permet de créer un rôle personnalisé avec un nom unique
- Chaque rôle affiche le nombre de collaborateurs qui y sont rattachés
- Un rôle personnalisé ne peut être supprimé que s'il n'est attribué à aucun collaborateur ; un message d'erreur s'affiche sinon
- L'ordre des rôles peut être réorganisé par glisser-déposer (drag & drop) pour définir la hiérarchie
- Chaque rôle possède une description optionnelle

## **US-CO07 — Gestion des permissions par rôle**

**En tant que** Administrateur

**Je veux** définir les permissions accordées à chaque rôle

**Afin de** contrôler finement les droits d'accès de chaque collaborateur en fonction de son rôle dans l'agence

**Critères d'acceptance :**

- Chaque rôle dispose d'une matrice de permissions configurable
- Les catégories de permissions sont : Projets, Honoraires, Facturation, Temps, Planning, Collaborateurs, Coûts, Finances, Rapports, Paramètres
- Pour chaque catégorie, les niveaux de permission sont : Aucun accès, Lecture seule, Lecture + Écriture, Lecture + Écriture + Validation, Administration complète
- Le rôle « Administrateur » possède par défaut toutes les permissions en « Administration complète » et ce réglage ne peut pas être réduit (au moins un administrateur doit conserver tous les droits)
- Les modifications de permissions sont appliquées immédiatement à tous les collaborateurs du rôle concerné
- Un aperçu en temps réel montre les modules accessibles en fonction des permissions sélectionnées
- Un bouton « Réinitialiser aux valeurs par défaut » permet de restaurer les permissions d'usine d'un rôle prédéfini
- Les modifications de permissions sont historisées (log de modification avec date, auteur, ancien/nouveau réglage)

## **US-CO08 — Gestion des compétences**

**En tant que** Directeur d'agence / Responsable RH

**Je veux** gérer le catalogue de compétences de l'agence

**Afin de** disposer d'un référentiel structuré des savoir-faire disponibles et pouvoir les attribuer aux collaborateurs

**Critères d'acceptance :**

- La vue « Compétences » est accessible via le sous-menu Équipe > Collaborateurs > Compétences
- Le catalogue affiche la liste de toutes les compétences avec : Nom, Catégorie, Nombre de collaborateurs possédant cette compétence
- Les catégories de compétences prédéfinies sont : Logiciels (Revit, AutoCAD, SketchUp, ArchiCAD, Rhino, Grasshopper, Photoshop, InDesign), BIM (BIM Management, BIM Coordination, IFC), Métier (Conception architecturale, Urbanisme, Design intérieur, Paysage), Langues, Certifications
- Un bouton « + Nouvelle compétence » permet d'ajouter une compétence personnalisée avec nom et catégorie
- Chaque compétence peut être modifiée (nom, catégorie) ou supprimée via le menu contextuel
- Une compétence ne peut pas être supprimée si elle est attribuée à au moins un collaborateur ; un message d'erreur s'affiche proposant de la retirer d'abord des collaborateurs concernés
- Un filtre par catégorie permet de filtrer la liste des compétences
- Une recherche plein texte par nom de compétence est disponible

## **US-CO09 — Attribution de compétences aux collaborateurs et matrice**

**En tant que** Directeur d'agence / Chef de projet

**Je veux** attribuer des compétences aux collaborateurs et visualiser la matrice de compétences de l'agence

**Afin de** connaître les savoir-faire de chaque collaborateur et identifier les profils adaptés lors de la constitution d'une équipe projet

**Critères d'acceptance :**

- Depuis la fiche collaborateur, une section « Compétences » permet d'ajouter des compétences via un sélecteur multi-choix (dropdown avec recherche)
- Pour chaque compétence attribuée, un niveau de maîtrise est sélectionnable : Débutant, Intermédiaire, Avancé, Expert
- Les compétences attribuées sont affichées sous forme de badges colorés selon le niveau de maîtrise
- La suppression d'une compétence attribuée est possible via un bouton de suppression sur le badge
- La vue « Matrice de compétences » est accessible depuis le sous-menu Compétences
- La matrice affiche un tableau croisé : en lignes les collaborateurs actifs, en colonnes les compétences
- Chaque cellule de la matrice affiche le niveau de maîtrise (code couleur : gris = non acquis, jaune = débutant, orange = intermédiaire, bleu = avancé, vert = expert)
- La matrice est filtrable par rôle, par équipe et par catégorie de compétence
- La matrice est exportable en CSV/Excel via le bouton ACTIONS

## **US-CO10 — Paramètres RH du collaborateur**

**En tant que** Directeur d'agence / Responsable RH

**Je veux** configurer les paramètres RH de chaque collaborateur

**Afin de** disposer des données contractuelles nécessaires au calcul des coûts, de la disponibilité et de la rentabilité des projets

**Critères d'acceptance :**

- La section « Contrat & RH » de la fiche collaborateur permet de saisir et modifier : Type de contrat (CDI, CDD, Freelance, Stage), Taux horaire interne (€/h ou devise de l'agence), Temps de travail hebdomadaire (en heures, valeur par défaut : 35h ou 39h configurable), Date de début de contrat, Date de fin de contrat (obligatoire si CDD ou Stage)
- Le coût mensuel estimé est calculé automatiquement : Taux horaire × Heures hebdomadaires × 4,33
- Le coût annuel estimé est calculé automatiquement : Coût mensuel × 12
- Un historique des modifications des paramètres RH est conservé (date de modification, ancien/nouveau taux horaire, auteur)
- Le taux horaire est utilisé par le module Coûts (EPIC-007) pour calculer le coût salarial des temps saisis sur les projets
- Le temps de travail hebdomadaire est utilisé par le module Planning (EPIC-006) pour calculer la disponibilité du collaborateur
- Si le type de contrat est « Freelance », le champ « Taux journalier » remplace le champ « Taux horaire » avec calcul automatique du taux horaire équivalent (Taux journalier / heures par jour configurable)
- Les champs sont validés : le taux horaire doit être positif, le temps de travail doit être compris entre 1h et 60h/semaine, la date de fin doit être postérieure à la date de début

## **US-CO11 — Archivage et désactivation d'un collaborateur**

**En tant que** Administrateur / Directeur d'agence

**Je veux** archiver ou désactiver un collaborateur qui a quitté l'agence ou est en congé longue durée

**Afin de** conserver son historique (temps saisis, projets, compétences) tout en le retirant des listes actives et des affectations disponibles

**Critères d'acceptance :**

- Un bouton « Archiver » est disponible sur la fiche collaborateur (accessible uniquement aux rôles Administrateur et Directeur)
- L'archivage nécessite une confirmation via une modale explicite : « Êtes-vous sûr de vouloir archiver [Prénom Nom] ? Ce collaborateur sera retiré des listes actives mais son historique sera conservé. »
- Un collaborateur archivé passe au statut « Inactif » et n'apparaît plus dans les listes par défaut (filtre « Actifs »)
- Un collaborateur archivé ne peut plus être assigné à de nouveaux projets
- Un collaborateur archivé conserve son historique complet : temps saisis, projets passés, compétences, paramètres RH
- Les temps saisis par un collaborateur archivé restent comptabilisés dans les projets auxquels il était assigné
- Un collaborateur archivé peut être réactivé via un bouton « Réactiver » accessible depuis sa fiche (filtre « Inactifs »)
- Un collaborateur ne peut pas être archivé s'il est le seul administrateur de l'agence ; un message d'erreur s'affiche

# **6. Hors Périmètre (Out of Scope)**

- Gestion de la paie et des bulletins de salaire (non couvert par OOTI)
- Gestion des entretiens annuels et des objectifs individuels (hors scope V1)
- Saisie des temps collaborateur (couvert par EPIC-005 — Temps)
- Planning d'affectation des ressources aux projets (couvert par EPIC-006 — Planning)
- Calcul des coûts salariaux sur les projets (couvert par EPIC-007 — Coûts)
- Gestion des formations et du développement professionnel (hors scope V1)
- Rapports RH avancés et analytics (couvert par EPIC-011 — Rapports)
- Workflow de validation des congés et absences (couvert par EPIC-012 — Validation)
- Gestion des notes de frais et remboursements (hors scope V1)
- Intégration avec des logiciels de paie externes (hors scope V1)

# **7. Règles Métier**

- Un collaborateur doit obligatoirement avoir un prénom, un nom, un email unique et un rôle attribué
- L'email d'un collaborateur est unique à l'échelle de toute l'application (cross-agence)
- Un collaborateur ne peut avoir qu'un seul rôle principal à l'échelle de l'agence (mais peut avoir des rôles différents au niveau de chaque projet via EPIC-002)
- Le taux horaire doit être un nombre positif strictement supérieur à zéro pour les collaborateurs actifs (sauf stagiaires où il peut être à zéro)
- Le temps de travail hebdomadaire est exprimé en heures et doit être compris entre 1 et 60 heures
- Un collaborateur de type CDD ou Stage doit obligatoirement avoir une date de fin de contrat renseignée
- Le taux d'occupation est calculé selon la formule : (Heures saisies sur la période / Heures contractuelles sur la période) × 100
- Le coût mensuel estimé = Taux horaire × Heures hebdomadaires × 4,33 (nombre moyen de semaines par mois)
- Un collaborateur archivé (statut Inactif) ne peut pas être assigné à de nouveaux projets ni être planifié dans le module Planning
- La suppression définitive d'un collaborateur est interdite : seul l'archivage est autorisé afin de préserver l'intégrité des données historiques
- Il doit toujours exister au moins un collaborateur avec le rôle « Administrateur » dans l'agence
- Les permissions sont héritées du rôle : toute modification des permissions d'un rôle s'applique immédiatement à tous les collaborateurs de ce rôle
- Une compétence ne peut être supprimée du catalogue que si elle n'est attribuée à aucun collaborateur
- L'invitation par email génère un lien unique sécurisé avec une durée de validité de 7 jours ; passé ce délai, une nouvelle invitation doit être envoyée
- Les niveaux de maîtrise des compétences sont au nombre de 4 : Débutant, Intermédiaire, Avancé, Expert

# **8. Critères d'Acceptance Globaux de l'EPIC**

- Toutes les User Stories US-CO01 à US-CO11 sont développées et validées
- La navigation entre les sous-vues (Résumé → Collaborateurs → Fiche → Rôles → Compétences) est fluide et cohérente
- Les données affichées sont cohérentes entre le résumé, la liste des collaborateurs, les fiches individuelles et la matrice de compétences
- Les droits d'accès sont respectés : seuls les administrateurs et directeurs peuvent créer, modifier ou archiver des collaborateurs ; les chefs de projet peuvent consulter les fiches en lecture seule
- Un collaborateur peut consulter et modifier sa propre fiche (informations personnelles, photo de profil) mais pas ses paramètres RH (taux horaire, contrat)
- Le module fonctionne en mode responsive (desktop, tablette)
- Les performances sont acceptables : chargement < 2 secondes pour une liste de 100 collaborateurs, chargement de la matrice de compétences < 3 secondes
- Tous les formulaires gèrent les cas d'erreur : champs obligatoires non remplis, format email invalide, doublon d'email, taux horaire négatif, dates incohérentes
- L'invitation par email fonctionne de bout en bout : envoi, réception, clic sur le lien, création du mot de passe, accès à l'application
- L'intégration avec le module Projets (EPIC-002) est fonctionnelle : un collaborateur créé ici est disponible dans la liste des membres d'un projet
- L'intégration avec le module Coûts (EPIC-007) est fonctionnelle : le taux horaire d'un collaborateur est utilisé pour le calcul des coûts salariaux

# **9. Définition of Done (DoD)**

- Le code est développé, revu (code review) et mergé sur la branche principale
- Les tests unitaires couvrent les fonctions critiques : calcul du taux d'occupation, calcul du coût mensuel/annuel, validation des champs obligatoires, unicité de l'email, vérification des permissions par rôle
- Les tests d'intégration valident les flux principaux : création collaborateur → attribution rôle → attribution compétences → assignation projet → saisie de temps → calcul des coûts
- Les tests d'intégration valident le flux d'invitation : envoi email → clic lien → création mot de passe → accès application
- La documentation technique est mise à jour (API endpoints, modèle de données, matrice de permissions)
- La fonctionnalité a été testée par le Product Owner et validée sur un jeu de données représentatif (agence de 20+ collaborateurs avec des rôles, compétences et contrats variés)
- Aucun bug bloquant ou critique n'est ouvert
- Les données de démonstration sont cohérentes et représentatives d'un cabinet d'architecture réel
- Les messages d'erreur et les libellés de l'interface sont rédigés en français (et prêts pour l'internationalisation)

# **10. Dépendances**

**Dépend de :**

- Module d'authentification et de gestion des comptes utilisateurs — le collaborateur est lié à un compte utilisateur de l'application
- EPIC-002 (Projets) — les collaborateurs sont assignés comme membres des projets ; la liste des collaborateurs actifs doit être disponible dans le sélecteur de membres d'un projet

**Requis par :**

- EPIC-002 (Projets) — l'assignation de membres aux projets s'appuie sur la liste des collaborateurs et leurs rôles
- EPIC-005 (Temps) — la saisie des temps est liée au collaborateur connecté ; le temps de travail contractuel est nécessaire au calcul du taux d'occupation
- EPIC-006 (Planning) — la planification des ressources utilise la liste des collaborateurs actifs, leur disponibilité (heures contractuelles) et leurs compétences
- EPIC-007 (Coûts) — le calcul des coûts salariaux sur les projets utilise le taux horaire de chaque collaborateur
- EPIC-012 (Validation) — les workflows de validation (temps, congés) sont liés aux rôles et permissions des collaborateurs

**APIs requises :**

- API Employees (CRUD) : création, lecture, mise à jour, archivage des collaborateurs
- API Roles (CRUD) : gestion des rôles et de leurs permissions
- API Skills (CRUD) : gestion du catalogue de compétences
- API Employee Skills (CRUD) : attribution de compétences aux collaborateurs avec niveau de maîtrise
- API Invitations : envoi, renvoi, annulation et suivi des invitations par email
- API Teams : gestion des équipes/entités de l'agence
- API Upload : upload de la photo de profil (avatar)

# **11. Modèle de Données Principal**

## **Objet : Employee (Collaborateur)**

- id : identifiant unique interne (UUID)
- first_name : prénom (string, obligatoire)
- last_name : nom de famille (string, obligatoire)
- email : adresse email (string, obligatoire, unique)
- phone : numéro de téléphone (string, optionnel)
- role_id : référence vers le rôle attribué (FK → Role.id, obligatoire)
- team_id : référence vers l'équipe/entité (FK → Team.id, optionnel)
- status : statut du collaborateur (enum : active, inactive, invited)
- contract_type : type de contrat (enum : cdi, cdd, freelance, stage)
- weekly_hours : temps de travail hebdomadaire en heures (decimal, défaut : 35.0)
- hourly_rate : taux horaire interne en devise de l'agence (decimal, défaut : 0.00)
- daily_rate : taux journalier pour les freelances (decimal, optionnel)
- start_date : date de début de contrat (date, optionnel)
- end_date : date de fin de contrat (date, optionnel, obligatoire si CDD/Stage)
- avatar_url : URL de la photo de profil (string, optionnel)
- skills : compétences attribuées (relation many-to-many via EmployeeSkill)
- projects : projets assignés (relation many-to-many via ProjectMember)
- created_at : date de création (timestamp)
- updated_at : date de dernière modification (timestamp)

## **Objet : Role (Rôle)**

- id : identifiant unique interne (UUID)
- name : nom du rôle (string, obligatoire, unique)
- description : description du rôle (string, optionnel)
- is_default : indique si c'est un rôle prédéfini (boolean, défaut : false)
- permissions : liste des permissions (relation one-to-many via RolePermission)
- sort_order : ordre d'affichage / hiérarchie (integer)
- created_at : date de création (timestamp)
- updated_at : date de dernière modification (timestamp)

## **Objet : RolePermission (Permission par rôle)**

- id : identifiant unique interne (UUID)
- role_id : référence vers le rôle (FK → Role.id)
- module : module concerné (enum : projects, fees, invoicing, time, planning, employees, costs, finances, reports, settings)
- level : niveau de permission (enum : none, read, read_write, read_write_validate, admin)

## **Objet : Skill (Compétence)**

- id : identifiant unique interne (UUID)
- name : nom de la compétence (string, obligatoire, unique)
- category : catégorie (enum : software, bim, profession, language, certification)
- created_at : date de création (timestamp)
- updated_at : date de dernière modification (timestamp)

## **Objet : EmployeeSkill (Compétence attribuée)**

- id : identifiant unique interne (UUID)
- employee_id : référence vers le collaborateur (FK → Employee.id)
- skill_id : référence vers la compétence (FK → Skill.id)
- proficiency_level : niveau de maîtrise (enum : beginner, intermediate, advanced, expert)
- created_at : date de création (timestamp)
- updated_at : date de dernière modification (timestamp)

## **Objet : Team (Équipe / Entité)**

- id : identifiant unique interne (UUID)
- name : nom de l'équipe (string, obligatoire)
- description : description (string, optionnel)
- created_at : date de création (timestamp)
- updated_at : date de dernière modification (timestamp)

## **Objet : Invitation**

- id : identifiant unique interne (UUID)
- email : adresse email du collaborateur invité (string, obligatoire)
- employee_id : référence vers le collaborateur pré-créé (FK → Employee.id)
- token : jeton unique sécurisé (string, unique)
- status : statut de l'invitation (enum : sent, accepted, expired, cancelled)
- role_id : rôle prédéfini pour le collaborateur invité (FK → Role.id)
- team_id : équipe prédéfinie (FK → Team.id, optionnel)
- sent_at : date d'envoi (timestamp)
- expires_at : date d'expiration (timestamp, sent_at + 7 jours)
- accepted_at : date d'acceptation (timestamp, optionnel)
- created_at : date de création (timestamp)

# **12. Estimation & Découpage**

## **Sprints suggérés :**

### **Sprint 1 — Fondations (2 semaines)**

| User Story | Description | Estimation |
|---|---|---|
| US-CO06 | Gestion des rôles (CRUD rôles prédéfinis + personnalisés) | 3 jours |
| US-CO07 | Gestion des permissions par rôle (matrice de permissions) | 3 jours |
| US-CO03 | Création d'un collaborateur (formulaire complet) | 2 jours |
| — | Modèle de données Employee, Role, RolePermission, Team | 2 jours |

**Objectif Sprint 1 :** Disposer des briques fondamentales (rôles, permissions, modèle de données) et pouvoir créer des collaborateurs.

### **Sprint 2 — Liste, fiche et résumé (2 semaines)**

| User Story | Description | Estimation |
|---|---|---|
| US-CO02 | Liste des collaborateurs (tableau, filtres, recherche, tri) | 3 jours |
| US-CO04 | Fiche collaborateur détaillée (toutes les sections) | 4 jours |
| US-CO01 | Vue résumé des collaborateurs (KPIs, graphiques) | 3 jours |

**Objectif Sprint 2 :** Disposer des trois vues principales du module (résumé, liste, fiche détaillée) pleinement fonctionnelles.

### **Sprint 3 — Compétences et paramètres RH (2 semaines)**

| User Story | Description | Estimation |
|---|---|---|
| US-CO08 | Gestion des compétences (catalogue, CRUD, catégories) | 3 jours |
| US-CO09 | Attribution de compétences + matrice de compétences | 4 jours |
| US-CO10 | Paramètres RH du collaborateur (contrat, taux, calculs) | 3 jours |

**Objectif Sprint 3 :** Disposer du référentiel de compétences complet, de la matrice de compétences et des paramètres RH configurés.

### **Sprint 4 — Invitation, archivage et intégrations (1 à 2 semaines)**

| User Story | Description | Estimation |
|---|---|---|
| US-CO05 | Invitation par email (envoi, lien, onboarding) | 3 jours |
| US-CO11 | Archivage et désactivation (workflow complet) | 2 jours |
| — | Intégrations avec EPIC-002 (Projets), EPIC-005 (Temps), EPIC-007 (Coûts) | 2 jours |
| — | Tests d'intégration end-to-end, corrections, polish UI | 2 jours |

**Objectif Sprint 4 :** Finaliser le module avec le flux d'invitation, l'archivage et les intégrations inter-modules.

## **Récapitulatif de l'estimation**

| Élément | Estimation |
|---|---|
| Nombre total de User Stories | 11 |
| Nombre de sprints | 3 à 4 sprints (sprints de 2 semaines) |
| Durée totale estimée | 5 à 7 semaines |
| Effort de développement | ~40 à 55 jours-homme |
| Répartition Front-end / Back-end | 55% Front-end / 45% Back-end |
| Complexité dominante | Matrice de permissions (US-CO07), matrice de compétences (US-CO09), flux d'invitation (US-CO05) |

**Risques identifiés :**

- **Intégration permissions :** La matrice de permissions par rôle impacte tous les autres modules de l'application ; un soin particulier doit être apporté à la conception de l'API de vérification des droits (middleware d'autorisation)
- **Flux d'invitation email :** Nécessite un service d'envoi d'emails transactionnels (SendGrid, SES, etc.) et un mécanisme de tokens sécurisés avec expiration
- **Performance matrice de compétences :** Pour une agence de 50+ collaborateurs et 30+ compétences, la matrice (1500+ cellules) doit être rendue de manière performante (virtualisation ou pagination)
- **Cohérence inter-modules :** Le taux horaire et le temps de travail hebdomadaire sont des données critiques utilisées par les modules Coûts et Planning ; toute modification doit être propagée correctement
