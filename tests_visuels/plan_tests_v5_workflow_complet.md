# Plan de tests visuels — ERP Provencher-Roy
**Version 5 — 2026-06-13**  
Suit l'intégration des PR #73 (discipline de soumission + heures facturées) et PR #74 (durcissement invariants tous chemins).

---

## Légende

| Symbole | Signification |
|---------|---------------|
| ☐ | À tester |
| ✅ | PASS |
| ❌ | FAIL |
| ⏭ | SKIP (non applicable) |
| 🆕 | Nouveau — PR #73/#74 |

**Priorités** : `P1` blocant (doit passer avant mise en prod) · `P2` important · `P3` optionnel  
**Rôles** : `EMP` Employé · `PM` Project Manager · `DIR` Associé en charge · `FIN` Finance · `PAI` Paie · `ADM` Admin

---

## Résumé — Comptage par module

| # | Module | TC | P1 | P2 | P3 |
|---|--------|----|----|----|-----|
| M01 | Authentification et navigation | 12 | 7 | 4 | 1 |
| M02 | Administration — paramétrage | 22 | 10 | 8 | 4 |
| M03 | Clients | 15 | 7 | 6 | 2 |
| M04 | Projets — création wizard | 16 | 9 | 5 | 2 |
| M05 | Projets — structure WBS | 20 | 10 | 7 | 3 |
| M06 | Projets — Gantt et planification | 14 | 7 | 5 | 2 |
| M07 | Projets — Équipe et blocages | 13 | 7 | 4 | 2 |
| M08 | Projets — Pilotage et finances | 14 | 7 | 5 | 2 |
| M09 | Avenants | 11 | 6 | 4 | 1 |
| M10 | Feuilles de temps — saisie et navigation | 24 | 12 | 8 | 4 |
| M11 | 🆕 FdT — Discipline de soumission | 15 | 12 | 3 | 0 |
| M12 | 🆕 FdT — Heures facturées intouchables | 15 | 13 | 2 | 0 |
| M13 | FdT — Approbation PM | 20 | 10 | 7 | 3 |
| M14 | FdT — Finance et Paie | 18 | 10 | 6 | 2 |
| M15 | Congés et absences | 14 | 8 | 4 | 2 |
| M16 | Occupation des ressources | 12 | 6 | 4 | 2 |
| M17 | Facturation | 20 | 10 | 7 | 3 |
| M18 | Dépenses | 12 | 6 | 4 | 2 |
| M19 | Fournisseurs et sous-traitants | 14 | 7 | 5 | 2 |
| M20 | Consortium | 11 | 5 | 4 | 2 |
| M21 | Dashboard et rapports | 9 | 5 | 3 | 1 |
| M22 | Sécurité et permissions | 13 | 10 | 3 | 0 |
| **Total** | | **338** | **172** | **117** | **49** |

---

## Données de test minimales

### Comptes (serveur Hostinger)

| Alias | Identifiant | Rôle | Usage |
|-------|-------------|------|-------|
| ALICE | `employe@test.com` / `Test1234!` | EMPLOYEE | Saisie temps, congés |
| BOB | `amonty@provencher-roy.com` / `Test1234!` | EMPLOYEE | 2e employé (multi-scenarios) |
| CAROL | `pm@test.com` / `Test1234!` | PM | Approbation PM |
| EVE | `finance@test.com` / `Test1234!` | FINANCE | Facturation, approbation Finance |
| FRANK | `paie@test.com` / `Test1234!` | PAIE | Validation paie |
| GRACE | `admin@provencher-roy.com` / `Test1234!` | ADMIN | Paramétrage, verrouillage |

### Projets de référence (à créer ou utiliser existants)

| Alias | Code | Type | PM | Notes |
|-------|------|------|----|-------|
| PROJ-A | PRJ-TST-A | Externe | CAROL | Projet de test principal |
| PROJ-B | PRJ-TST-B | Externe | CAROL | 2e projet (multi-PM, multi-projet) |
| PROJ-INT | PRJ-INT | Interne | CAROL | Congés / tâches obligatoires |

---

## M01 — Authentification et navigation

### TC-M01-001 — Connexion identifiants valides
> **Rôle** : Tous | **P1** | **Préconditions** : Serveur accessible

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Naviguer vers `/login` | Formulaire email + mot de passe, pas d'erreur | ☐ |
| 2 | Saisir `employe@test.com` / `Test1234!`, cliquer Connexion | Redirection vers `/` (tableau de bord) | ☐ |
| 3 | Vérifier la barre latérale | Menu « Mon travail » visible, pas de menu Admin | ☐ |

### TC-M01-002 — Connexion identifiants invalides
> **Rôle** : Tous | **P1** | **Préconditions** : Page login

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Saisir mot de passe incorrect, cliquer Connexion | Message d'erreur explicite, pas de redirection | ☐ |
| 2 | Champ email vide, cliquer Connexion | Validation inline, envoi bloqué | ☐ |

### TC-M01-003 — Menu selon le rôle ADMIN
> **Rôle** : GRACE (ADM) | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Se connecter en tant que GRACE | Menu « Administration » visible dans la barre latérale | ☐ |
| 2 | Naviguer vers `/admin` | Page admin avec tous les sous-menus | ☐ |
| 3 | Se connecter en tant que ALICE | Menu Administration absent | ☐ |

### TC-M01-004 — Menu selon le rôle EMPLOYEE
> **Rôle** : ALICE (EMP) | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Se connecter en tant que ALICE | Visible : Mon travail, Projets, Congés. Absent : Facturation, Admin, Paie | ☐ |
| 2 | Tenter `/admin` en URL directe | Redirection ou 403 | ☐ |

### TC-M01-005 — Déconnexion
> **Rôle** : Tous | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Cliquer sur l'avatar → Déconnexion | Redirection vers `/login`, session invalidée | ☐ |
| 2 | Tenter d'accéder à `/timesheets` après logout | Redirection vers `/login` | ☐ |

### TC-M01-006 — Aide contextuelle « ? »
> **Rôle** : Tous | **P2**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Sur `/timesheets`, cliquer « ? » | Panneau d'aide avec titre « Feuilles de temps » et rubriques discipline, blocages, fériés | ☐ |
| 2 | Sur un onglet de la fiche projet, cliquer « ? » | Contenu spécifique à l'onglet (ex. « Tâches » ≠ « Gantt ») | ☐ |

### TC-M01-007 — Notifications
> **Rôle** : Tous | **P2**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Icône cloche avec badge rouge → cliquer | Liste des notifications (rejets, validations) | ☐ |
| 2 | Naviguer vers `/notifications/preferences` | Préférences de notification par type | ☐ |

### TC-M01-008 — Navigation par URL directe
> **Rôle** : Tous | **P2** | Vérifie que les routes protégées redirigent sans session

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Sans session, aller sur `/projects` | Redirection `/login` | ☐ |
| 2 | Après login, vérifier la redirection vers la page initiale | Revient à `/projects` | ☐ |

### TC-M01-009 — Responsive mobile
> **Rôle** : Tous | **P3** | Tester sur mobile (ou DevTools 375px)

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Charger `/timesheets` en 375px de large | Menu hamburger, grille scrollable horizontalement | ☐ |

---

## M02 — Administration — paramétrage

### TC-M02-001 — Phases standard : création (admin seulement)
> **Rôle** : GRACE (ADM) | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Naviguer `/admin/standard-phases` → « + Nouvelle phase » | Formulaire de création | ☐ |
| 2 | Saisir nom « Phase Test », ordre 99, sauvegarder | Phase créée, apparaît dans la liste | ☐ |
| 3 | Se connecter en tant que CAROL (PM), tenter `/admin/standard-phases` | Accès refusé ou page vide | ☐ |

### TC-M02-002 — Phases standard : les nouvelles phases s'instancient sur les nouveaux projets
> **Rôle** : GRACE (ADM) | **P1** | **Préconditions** : Phase « Phase Test » créée (TC-M02-001)

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Créer un nouveau projet externe | Dans l'onglet Phases, « Phase Test » apparaît (vide) | ☐ |
| 2 | Vérifier que les projets existants n'ont pas cette phase automatiquement | Les anciens projets ne sont pas affectés | ☐ |

### TC-M02-003 — Tâches standard : création (admin seulement)
> **Rôle** : GRACE (ADM) | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Naviguer `/admin/standard-tasks` → « + Nouvelle tâche » | Formulaire : nom, phase parente, ordre | ☐ |
| 2 | Créer « Tâche Std Test » associée à « Phase Test » | Tâche créée, apparaît dans le catalogue | ☐ |
| 3 | Créer une sous-tâche avec parent = « Tâche Std Test » | Hiérarchie visible dans le catalogue | ☐ |
| 4 | Se connecter en tant que CAROL (PM), tenter de créer une tâche standard | Accès refusé | ☐ |

### TC-M02-004 — Équipes : création (Finance/Paie/Admin uniquement)
> **Rôle** : EVE (FIN) / GRACE (ADM) | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Naviguer `/admin/teams` → « + Nouvelle équipe » | Formulaire nom + membres | ☐ |
| 2 | Ajouter ALICE et BOB, sauvegarder | Équipe créée avec 2 membres | ☐ |
| 3 | Se connecter en tant que CAROL (PM), tenter de créer une équipe | Accès refusé | ☐ |
| 4 | Se connecter en tant que FRANK (PAI), créer une équipe | Succès (Paie a le droit) | ☐ |

### TC-M02-005 — Jours fériés : paramétrage par régime
> **Rôle** : GRACE (ADM) | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Naviguer `/admin/holidays` → « + Nouveau férié » | Formulaire : date, nom, régime (province/tous) | ☐ |
| 2 | Créer un férié national (tous régimes) | Apparaît dans la liste avec régime « Tous » | ☐ |
| 3 | Créer un férié Québec uniquement | Régime « Québec » | ☐ |
| 4 | Naviguer vers `/timesheets` en tant que ALICE (régime Québec) | Le férié Québec est surligné dans la grille | ☐ |

### TC-M02-006 — Périodes : verrouillage global
> **Rôle** : GRACE (ADM) | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Naviguer `/admin/timesheet` → « Verrouiller période » | Formulaire semaine start/end | ☐ |
| 2 | Verrouiller la semaine précédente | Confirmation nombre d'entrées verrouillées | ☐ |
| 3 | En tant que ALICE, tenter de modifier une entrée de cette semaine | Message « Période verrouillée », refus | ☐ |

### TC-M02-007 — Périodes : gel global (freeze_before)
> **Rôle** : GRACE (ADM) | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Naviguer `/admin/timesheet` → « Geler avant le » | Formulaire date | ☐ |
| 2 | Geler avant le 1er du mois précédent | Confirmation | ☐ |
| 3 | En tant que ALICE, tenter de saisir des heures avant la date de gel | 400 « Période gelée » | ☐ |
| 4 | Saisir des heures après la date → OK | 201 Créé | ☐ |

### TC-M02-008 — Schémas fiscaux
> **Rôle** : GRACE (ADM) | **P2**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Naviguer `/admin/billing` | Liste des schémas fiscaux (Québec TPS+TVQ, Ontario TVH, etc.) | ☐ |
| 2 | Voir le schéma Québec | TPS 5% + TVQ 9,975% avec taux CTI/RTI | ☐ |
| 3 | Assigner le schéma Québec à un client | Client met à jour son schéma par défaut | ☐ |

### TC-M02-009 — Résumé périodes (admin)
> **Rôle** : GRACE (ADM) | **P2**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Naviguer `/admin/timesheet` → tableau de bord périodes | Semaines avec statut locked/partial/open | ☐ |
| 2 | Semaine entièrement verrouillée | Statut « Verrouillée » en vert | ☐ |
| 3 | Semaine mixte | Statut « Partielle » en orange | ☐ |

### TC-M02-010 — Unlock exception (déverrouillage ciblé)
> **Rôle** : GRACE (ADM) | **P2** | **Préconditions** : Semaine gelée

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Créer une exception de déverrouillage pour une semaine spécifique (motif CORRECTION) | PeriodUnlock créé | ☐ |
| 2 | En tant que ALICE, saisir une heure dans cette semaine gelée | 201 Créé (exception active) | ☐ |
| 3 | Supprimer l'exception | Semaine re-gelée, saisie bloquée à nouveau | ☐ |

### TC-M02-011 — Gestion des utilisateurs
> **Rôle** : GRACE (ADM) | **P2**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Naviguer `/admin/users` | Liste de tous les utilisateurs | ☐ |
| 2 | Modifier le rôle d'un utilisateur | Changement effectif immédiatement | ☐ |
| 3 | Désactiver un compte | L'utilisateur ne peut plus se connecter | ☐ |

### TC-M02-012 — Types de congés
> **Rôle** : GRACE (ADM) | **P2**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Naviguer `/admin/leave-types` | 7 types listés (Vacances, Maladie, Personnel…) | ☐ |
| 2 | Modifier le libellé d'un type | Changement visible dans la saisie de congés | ☐ |

---

## M03 — Clients

### TC-M03-001 — Création client
> **Rôle** : GRACE (ADM) / EVE (FIN) | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Naviguer `/clients` → « + Nouveau client » | Formulaire nom, alias, secteur, schéma fiscal | ☐ |
| 2 | Remplir les champs obligatoires, sauvegarder | Client créé, redirigé vers fiche client | ☐ |
| 3 | Vérifier les 5 onglets : Informations, Contacts, Adresses, Financier, Projets | Tous les onglets présents | ☐ |

### TC-M03-002 — Recherche live client
> **Rôle** : Tous | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Naviguer `/clients`, taper les 3 premières lettres du client | Résultats filtrés en temps réel (sans appuyer Entrée) | ☐ |
| 2 | Taper un alias | Client trouvé via l'alias aussi | ☐ |

### TC-M03-003 — Adresses client : ajout et anti-doublon
> **Rôle** : ADM / FIN | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Onglet Adresses → « + Adresse » | Formulaire ligne 1, ville, province, code postal | ☐ |
| 2 | Ajouter « 123 rue Principale, Montréal » | Adresse créée | ☐ |
| 3 | Ajouter à nouveau « 123 rue principale, montreal » (casse différente) | Refus : doublon détecté (même ligne 1 + ville normalisés) | ☐ |
| 4 | Ajouter « 456 rue Secondaire, Montréal » | Succès (adresse différente) | ☐ |

### TC-M03-004 — Adresse de facturation par défaut client
> **Rôle** : ADM / FIN | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Onglet Adresses, désigner une adresse comme « Par défaut facturation » | Badge « Par défaut » visible | ☐ |
| 2 | Créer une facture sur un projet sans adresse projet désignée | Adresse par défaut du client utilisée | ☐ |

### TC-M03-005 — Suppression adresse (depuis fiche client seulement)
> **Rôle** : ADM | **P1** | **Préconditions** : Adresse non utilisée par un projet

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Onglet Adresses → supprimer une adresse | Confirmation demandée, puis suppression | ☐ |
| 2 | Sur la fiche projet (onglet Paramètres), tenter de supprimer une adresse du client | Pas de bouton de suppression disponible (suppression réservée à la fiche client) | ☐ |

### TC-M03-006 — Contacts client
> **Rôle** : ADM / FIN / PM | **P2**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Onglet Contacts → « + Contact » | Formulaire nom, prénom, email, téléphone, rôle | ☐ |
| 2 | Ajouter un contact, sauvegarder | Contact visible dans la liste | ☐ |
| 3 | Modifier le contact | Changements sauvegardés | ☐ |

### TC-M03-007 — Schéma fiscal client
> **Rôle** : ADM / FIN | **P2**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Onglet Financier → assigner schéma « Québec TPS+TVQ » | Schéma sauvegardé | ☐ |
| 2 | Créer une facture sur un projet de ce client | Taxes TPS+TVQ calculées automatiquement | ☐ |

---

## M04 — Projets — création wizard

### TC-M04-001 — Wizard 5 étapes : flux complet
> **Rôle** : PM / ADM | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Naviguer `/projects/new` | Étape 1 : Identification (nom, code, client, dates, PM, Associé en charge) | ☐ |
| 2 | Remplir étape 1, cliquer Suivant | Étape 2 : WBS (WBS client ou standard) | ☐ |
| 3 | Choisir services transversaux : BIM, Développement durable | Étape 3 (ou suivante) | ☐ |
| 4 | Étape Ressources : affecter ALICE au projet | Membre ajouté | ☐ |
| 5 | Étape Confirmation : vérifier le récapitulatif | Toutes les informations présentes, bouton Créer | ☐ |
| 6 | Cliquer Créer | Projet créé, redirigé vers la fiche projet | ☐ |

### TC-M04-002 — Services transversaux → phases SUPPORT imputables
> **Rôle** : PM / ADM | **P1** | **Préconditions** : Projet créé avec BIM et DD sélectionnés

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Onglet Phases de la fiche projet | Phases « BIM » et « Développement durable » présentes de type SUPPORT | ☐ |
| 2 | Onglet Tâches | Chaque phase SUPPORT a une tâche feuille imputable du même nom | ☐ |
| 3 | En tant que ALICE, saisir des heures sur la tâche « BIM » | 201 Créé — imputation possible | ☐ |

### TC-M04-003 — Phases standard instanciées automatiquement
> **Rôle** : PM / ADM | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Créer un projet | Onglet Phases : toutes les phases standard du cabinet sont présentes (vides) | ☐ |
| 2 | Vérifier qu'aucune phase n'est modifiable/supprimable par le PM | Actions Créer/Modifier/Supprimer phase absentes | ☐ |
| 3 | En tant que GRACE (ADM), onglet Phases | Les phases sont modifiables (réservé admin) | ☐ |

### TC-M04-004 — Validation dates wizard (fin ≥ début)
> **Rôle** : PM | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Étape 1 : saisir date fin = date début - 1 | Erreur inline « Date de fin doit être ≥ date de début », bouton Suivant désactivé | ☐ |

### TC-M04-005 — Vocabulaire : « Associé en charge »
> **Rôle** : PM / ADM | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Dans le wizard et dans la fiche projet, observer les libellés | « Associé en charge » utilisé partout — jamais « Directeur de projet » | ☐ |

### TC-M04-006 — WBS client
> **Rôle** : PM | **P2**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Étape WBS : choisir « WBS client » | Champs pour saisir les libellés client des phases/tâches | ☐ |
| 2 | Saisir « Phase 1 — Étude de faisabilité » comme libellé client pour une phase | Libellé client sauvegardé sur la phase | ☐ |
| 3 | Ouvrir les feuilles de temps sur ce projet | Libellé « Phase 1 — Étude de faisabilité » affiché (pas le nom interne) | ☐ |

### TC-M04-007 — Coût de construction (projets externes seulement)
> **Rôle** : PM / ADM | **P2**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Projet externe → onglet Paramètres → champ « Coût de construction » visible | Champ présent | ☐ |
| 2 | Projet interne (`is_internal`) → onglet Paramètres | Champ « Coût de construction » absent | ☐ |
| 3 | Saisir 5 000 000 $ sur un projet externe | Valeur sauvegardée, utilisable dans le calcul des honoraires | ☐ |

### TC-M04-008 — Numérotation auto avenant
> **Rôle** : PM | **P2** | Voir M09

---

## M05 — Projets — structure WBS

### TC-M05-001 — Ajout de tâche libre
> **Rôle** : PM | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Onglet Tâches → « + Tâche » | Formulaire : nom, libellé client, phase, dates, budget | ☐ |
| 2 | Remplir les champs, sauvegarder | Tâche créée sous la phase choisie, code WBS auto-généré | ☐ |
| 3 | Vérifier le code WBS (ex. 1.1) | Format `{phase}.{séquence}` | ☐ |

### TC-M05-002 — Ajout depuis le catalogue standard (sans doublon)
> **Rôle** : PM | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Onglet Tâches → « + depuis le modèle » | Picker affiche les tâches du catalogue groupées par phase | ☐ |
| 2 | Sélectionner une tâche, confirmer | Tâche instanciée sur le projet | ☐ |
| 3 | Rouvrir le picker | La tâche déjà présente est absente du picker (déduplication) | ☐ |

### TC-M05-003 — Sous-tâches
> **Rôle** : PM | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Fiche tâche (clic sur le nom) → « + Sous-tâche » | Formulaire de sous-tâche | ☐ |
| 2 | Créer la sous-tâche, sauvegarder | Code WBS : `1.1.1`, hiérarchie dans la liste | ☐ |
| 3 | Vérifier que la tâche-mère est en lecture seule pour budget/heures | Pas de saisie budget sur la tâche-mère ; agrégat affiché | ☐ |

### TC-M05-004 — Dates inline : édition et validation
> **Rôle** : PM | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Cliquer sur la date début d'une tâche dans la liste | Champ date éditable | ☐ |
| 2 | Saisir une date de fin antérieure à la date de début | Erreur inline, sauvegarde bloquée | ☐ |
| 3 | Saisir une date de fin valide, Tab | Sauvegarde automatique, dates mise à jour | ☐ |
| 4 | Vérifier les dates de la phase parente | Dates dérivées recalculées (min/max des tâches) | ☐ |

### TC-M05-005 — Budget sur la tâche feuille (pas la phase)
> **Rôle** : PM | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Fiche tâche feuille (sans sous-tâche) → champ budget heures et budget $ | Éditables | ☐ |
| 2 | Sur une tâche-mère (avec sous-tâches) → champ budget | En lecture seule — agrégat | ☐ |
| 3 | Onglet Finances → Budget | Synthèse par tâche en lecture seule ; pas de saisie budget ici | ☐ |

### TC-M05-006 — Décalage d'échéancier
> **Rôle** : PM | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Onglet Tâches → « ↔️ Décaler l'échéancier… » | Formulaire : nombre de jours (positif/négatif) | ☐ |
| 2 | Décaler de +14 jours | Toutes les tâches datées décalées, dates phases recalculées | ☐ |
| 3 | Décaler de -7 jours | Décalage vers l'avant | ☐ |

### TC-M05-007 — Fiche tâche unique (panneau slide-over)
> **Rôle** : PM | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Cliquer sur le nom d'une tâche (onglet Tâches ou Gantt) | Slide-over : nom, libellé client, phase, dates, budget, affectations | ☐ |
| 2 | Modifier le libellé client, sauvegarder | Changement visible dans les feuilles de temps | ☐ |
| 3 | Cliquer « Fermer la tâche » | Confirmation, tâche fermée (saisie bloquée pour tous) | ☐ |
| 4 | Cliquer « Rouvrir » | Tâche réouverte | ☐ |

### TC-M05-008 — Suppression tâche sans heures facturées
> **Rôle** : PM | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Fiche tâche → « Supprimer… » | Confirmation inline (pas de `confirm()` natif) | ☐ |
| 2 | Confirmer | Tâche supprimée, agrégats recalculés | ☐ |

### TC-M05-009 — Suppression tâche bloquée si heures facturées 🆕
> **Rôle** : PM | **P1** | **Préconditions** : Tâche avec des entrées `is_invoiced=True`

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Fiche tâche → « Supprimer… » → Confirmer | 400 : « Suppression impossible : des heures de cette tâche ont été facturées au client. » | ☐ |
| 2 | Tâche toujours présente dans la liste | Non supprimée | ☐ |

### TC-M05-010 — Phases masquées sans tâche
> **Rôle** : PM / EMP | **P2**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Onglet Tâches : phase sans aucune tâche | Phase absente de la liste des tâches (masquée dans l'opérationnel) | ☐ |
| 2 | Onglet Phases | Phase visible avec mention « Sans tâche » | ☐ |

---

## M06 — Projets — Gantt et planification

### TC-M06-001 — Affichage Gantt
> **Rôle** : PM | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Onglet Gantt d'un projet avec tâches datées | Barres affichées pour chaque tâche ayant ses propres dates | ☐ |
| 2 | Phase et tâches-mères | Pas de barre cliquable (agrégats non cliquables) | ☐ |
| 3 | Tâche sans dates | Pas de barre | ☐ |

### TC-M06-002 — Clic sur barre → fiche tâche
> **Rôle** : PM | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Cliquer sur une barre de tâche | Slide-over fiche tâche s'ouvre | ☐ |

### TC-M06-003 — Jalons
> **Rôle** : PM | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Gantt → « + Jalon » | Formulaire : nom, date, couleur | ☐ |
| 2 | Créer un jalon à une date passée | Jalon en rouge (retard auto-détecté) | ☐ |
| 3 | Créer un jalon futur | Jalon en couleur choisie | ☐ |
| 4 | Modifier un jalon | Changements sauvegardés | ☐ |
| 5 | Supprimer un jalon | Confirmation inline, jalon supprimé | ☐ |

### TC-M06-004 — Allocations depuis la fiche tâche
> **Rôle** : PM | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Fiche tâche → « + Affectation » | Dialogue : Qui (employé / équipe / profil virtuel) → Où (tâche) → Combien (h/sem, période) | ☐ |
| 2 | Affecter ALICE, 8h/sem, 4 semaines | Allocation créée, visible dans le Gantt | ☐ |
| 3 | Heures planifiées dépassent le budget | Signalé en rouge — sans bloquer la saisie | ☐ |

### TC-M06-005 — Contrôle budget non bloquant
> **Rôle** : PM | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Créer une allocation dont total planifié > budget de la tâche | Avertissement rouge visible, allocation quand même créée | ☐ |

### TC-M06-006 — Zooms Gantt
> **Rôle** : PM | **P2**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Changer de zoom (semaine / mois / trimestre) | Affichage Gantt adapté | ☐ |

### TC-M06-007 — Dépendances
> **Rôle** : PM | **P2**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Créer une dépendance Fin-Début entre deux tâches | Flèche de dépendance visible | ☐ |
| 2 | Déplacer la tâche source | La dépendance reste cohérente | ☐ |

---

## M07 — Projets — Équipe et blocages

### TC-M07-001 — Vue par phase et par personne
> **Rôle** : PM | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Onglet Équipe → « Par phase » | Arbre Phase → Tâche → Sous-tâche avec personnes affectées | ☐ |
| 2 | Basculer sur « Par personne » | Liste d'employés avec leurs affectations | ☐ |

### TC-M07-002 — Dialogue d'affectation unifié (Qui → Où → Combien)
> **Rôle** : PM | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | « + Affectation » | Étape 1 : Qui (dropdown employé / équipe / profil virtuel) | ☐ |
| 2 | Sélectionner ALICE → Suivant | Étape 2 : Où (projet / phase / tâche) | ☐ |
| 3 | Sélectionner une tâche → Suivant | Étape 3 : Combien (h/sem, période) | ☐ |
| 4 | Confirmer | Allocation créée | ☐ |

### TC-M07-003 — Affecter une équipe entière
> **Rôle** : PM | **P1** | **Préconditions** : Équipe créée avec ALICE et BOB

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | « + Affectation » → choisir l'équipe → Suivant | L'équipe est sélectionnée | ☐ |
| 2 | Confirmer | ALICE et BOB ajoutés aux membres du projet | ☐ |

### TC-M07-004 — Blocage global de tâche (vue par phase)
> **Rôle** : PM | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Vue par phase → cadenas sur une tâche → « 🔒 Fermer » | Confirmation, saisie bloquée pour tous | ☐ |
| 2 | En tant que ALICE, saisir des heures sur cette tâche | Refus avec message « Tâche fermée » | ☐ |
| 3 | PM → Rouvrir la tâche | Saisie autorisée à nouveau | ☐ |

### TC-M07-005 — Blocage ciblé (TimeEntryBlock — vue par personne)
> **Rôle** : PM | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Vue par personne → ALICE → cadenas sur une tâche | Blocage ciblé ALICE×tâche créé | ☐ |
| 2 | En tant que ALICE, saisir des heures sur cette tâche | Refus | ☐ |
| 3 | En tant que BOB, saisir des heures sur cette même tâche | Autorisé (blocage ciblé, pas global) | ☐ |
| 4 | Débloquer | Saisie ALICE autorisée à nouveau | ☐ |

### TC-M07-006 — Blocage ciblé sur tout le projet (TimeEntryBlock — niveau projet)
> **Rôle** : PM | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Vue par personne → ALICE → « Bloquer (projet) » | Blocage ALICE sur tout le projet | ☐ |
| 2 | En tant que ALICE, saisir des heures sur n'importe quelle tâche du projet | Refus | ☐ |

### TC-M07-007 — Profils virtuels
> **Rôle** : PM | **P2**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Onglet Paramètres → Profils virtuels → « + Profil virtuel » | Formulaire nom, rôle, disponibilité | ☐ |
| 2 | Affecter le profil virtuel à une tâche | Visible dans le Gantt | ☐ |
| 3 | Remplacer le profil virtuel par ALICE | Les allocations basculent sur ALICE | ☐ |

---

## M08 — Projets — Pilotage et finances

### TC-M08-001 — KPIs vue d'ensemble (onglet Pilotage)
> **Rôle** : PM / DIR | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Onglet 📊 Pilotage | Budget total, facturé, % consommé, solde, heures consommées/budget/planifiées | ☐ |
| 2 | Avancement par phase | % heures, % coût, % honoraires, total facturé par phase | ☐ |

### TC-M08-002 — Alertes centralisées
> **Rôle** : PM | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Projet avec une tâche sans budget | Alerte « Tâche sans budget » avec lien vers Tâches | ☐ |
| 2 | Projet avec dates incohérentes | Alerte « Dates incohérentes » | ☐ |

### TC-M08-003 — Budget en lecture seule dans Finances
> **Rôle** : PM / FIN | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Onglet Finances → Budget | Tableau budget par tâche : budget $, heures, facturé, solde — en lecture seule | ☐ |
| 2 | Tenter de modifier le budget depuis cet onglet | Pas de champ éditable (lecture seule confirmée) | ☐ |
| 3 | Modifier le budget depuis la fiche tâche | Changement reflété dans Finances > Budget | ☐ |

### TC-M08-004 — Honoraires
> **Rôle** : PM / FIN | **P2**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Onglet Finances → Honoraires | Modes : Forfait, T&M, Coût des travaux % | ☐ |
| 2 | Mode « Coût des travaux % » : saisir le taux | Calcul automatique basé sur `construction_cost` du projet | ☐ |

### TC-M08-005 — Adresse de facturation par projet
> **Rôle** : PM / FIN | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Onglet Paramètres → Adresses → « Utiliser pour ce projet » sur une adresse | Badge mauve « Ce projet » visible | ☐ |
| 2 | Créer une facture sur ce projet | L'adresse désignée est utilisée (pas l'adresse par défaut client) | ☐ |
| 3 | Changer le client du projet | L'adresse de facturation désignée est purgée (invalide) | ☐ |

### TC-M08-006 — Statut et clôture projet
> **Rôle** : PM / ADM | **P2**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Onglet Pilotage → changer statut → « En pause » | Statut mis à jour | ☐ |
| 2 | Cliquer « Clôturer » | Checklist de clôture présentée (profils virtuels remplacés, etc.) | ☐ |
| 3 | Checklist non complète → confirmer | Avertissements bloquants | ☐ |

---

## M09 — Avenants

### TC-M09-001 — Création avenant
> **Rôle** : PM / DIR | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Onglet Avenants → « + Avenant » | Formulaire : titre, numéro externe, montant, description | ☐ |
| 2 | Sauvegarder | Numéro auto-généré : `{code projet}-AV-1` | ☐ |

### TC-M09-002 — Tâches d'avenant (badge AV-n)
> **Rôle** : PM | **P1** | **Préconditions** : Avenant créé

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Slide-over avenant → ajouter des tâches sur des phases existantes | Tâches créées avec badge « AV-1 » visible | ☐ |
| 2 | Vérifier que l'avenant ne crée pas de nouvelle phase | Uniquement sur les phases standard existantes | ☐ |
| 3 | Onglet Tâches du projet | Tâches d'avenant apparaissent avec badge | ☐ |

### TC-M09-003 — Pas d'affectation dans le slide-over avenant
> **Rôle** : PM | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Slide-over avenant | Pas de section « Affectations » ni « Planification » | ☐ |
| 2 | Pour affecter des ressources aux tâches d'avenant | Utiliser le Gantt (fiche tâche) | ☐ |

### TC-M09-004 — Workflow avenant
> **Rôle** : PM / DIR | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Avenant → « Soumettre » | Statut : SOUMIS | ☐ |
| 2 | En tant que DIR → « Approuver » | Statut : APPROUVÉ | ☐ |
| 3 | En tant que DIR → « Rejeter » | Statut : REJETÉ | ☐ |

### TC-M09-005 — Numérotation séquentielle
> **Rôle** : PM | **P2**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Créer 3 avenants sur le même projet | Numéros : `PRJ-AV-1`, `PRJ-AV-2`, `PRJ-AV-3` | ☐ |

---

## M10 — Feuilles de temps — saisie et navigation

### TC-M10-001 — Affichage grille hebdomadaire
> **Rôle** : ALICE (EMP) | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Naviguer `/timesheets` | Grille semaine courante : projets en lignes, jours Lun-Dim en colonnes | ☐ |
| 2 | Navigation semaine précédente (←) | Semaine affichée change, entrées rechargées | ☐ |
| 3 | Navigation semaine suivante (→) | Semaine suivante affichée | ☐ |
| 4 | Changer de semaine avec le sélecteur de date | Grille rechargée pour cette semaine | ☐ |

### TC-M10-002 — Saisie et sauvegarde d'heures
> **Rôle** : ALICE (EMP) | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Cliquer sur une cellule, saisir « 7.5 » | Valeur visible dans la cellule | ☐ |
| 2 | Quitter la cellule (Tab ou clic ailleurs) | Sauvegarde auto, flash vert fugace | ☐ |
| 3 | Recharger la page | Valeur « 7.5 » toujours présente | ☐ |
| 4 | Saisir « 16 » (>15h) | Erreur inline « Maximum 15h par cellule », valeur rejetée | ☐ |
| 5 | Saisir « -1 » | Erreur inline « Valeur négative », valeur rejetée | ☐ |

### TC-M10-003 — Tâches obligatoires (Congés, Formation, Maladie)
> **Rôle** : ALICE (EMP) | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Grille de saisie | Tâches « Congés », « Formation », « Maladie » toujours affichées (même sans entrée) | ☐ |
| 2 | Saisir des heures sur « Maladie » | Entrée créée | ☐ |
| 3 | Supprimer l'entrée de « Maladie » | Ligne réapparaît vide (tâche obligatoire toujours visible) | ☐ |

### TC-M10-004 — Favoris
> **Rôle** : ALICE (EMP) | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Épingler PROJ-A comme favori | Icône étoile active | ☐ |
| 2 | Naviguer vers une autre semaine | PROJ-A présent dans la grille (même sans entrée) | ☐ |
| 3 | Désépingler | PROJ-A disparaît s'il n'y a pas d'entrée | ☐ |

### TC-M10-005 — Pré-remplissage jours fériés
> **Rôle** : ALICE (EMP) | **P1** | **Préconditions** : Férié paramétré pour aujourd'hui ou cette semaine

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Charger la grille d'une semaine contenant un férié | Jour surligné, tâche « Férié » pré-remplie avec `daily_hours` max | ☐ |
| 2 | Modifier la valeur pré-remplie | La modification est conservée (pas d'écrasement) | ☐ |

### TC-M10-006 — Copie semaine précédente
> **Rôle** : ALICE (EMP) | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Semaine courante vide → « Copier la semaine précédente » | Entrées copiées avec les mêmes projets/tâches/heures, dates décalées | ☐ |
| 2 | Recliquer « Copier » | `copied_count = 0` — pas de doublon | ☐ |

### TC-M10-007 — Soumission de semaine
> **Rôle** : ALICE (EMP) | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Semaine avec entrées DRAFT → cliquer « Soumettre » | Confirmation nombre d'entrées | ☐ |
| 2 | Confirmer | Entrées passent en SUBMITTED, cellules grisées non éditables | ☐ |
| 3 | Tenter de modifier une cellule SUBMITTED | Cellule verrouillée | ☐ |

### TC-M10-008 — Erreur backend affichée dans la cellule 🆕
> **Rôle** : ALICE (EMP) | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Provoquer un refus backend (saisie sur tâche fermée) | Tooltip rouge sur la cellule avec le message du serveur | ☐ |
| 2 | Valeur de la cellule | Revient à la valeur précédente | ☐ |
| 3 | Pas de flash vert | Aucun feedback de succès | ☐ |

### TC-M10-009 — Badge $ sur heures facturées 🆕
> **Rôle** : ALICE (EMP) | **P1** | **Préconditions** : Entrée `is_invoiced=True`

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Grille de la semaine contenant des heures facturées | Badge « $ » vert visible en coin de cellule | ☐ |
| 2 | Tenter de modifier la cellule avec le badge | Refus, tooltip « Modification impossible : heure facturée » | ☐ |
| 3 | Cellule grisée | Cellule non éditable (locked) | ☐ |

### TC-M10-010 — Blocage tâche fermée
> **Rôle** : ALICE (EMP) | **P1** | **Préconditions** : Tâche fermée (TC-M05-007)

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Tenter de saisir des heures sur une tâche fermée | Cellule grisée ou message explicite | ☐ |

### TC-M10-011 — Navigation semaine : vide immédiate
> **Rôle** : ALICE (EMP) | **P2** | **Préconditions** : Grille avec entrées chargées

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Cliquer ← (semaine précédente) | La grille se vide immédiatement, puis se repeuuple avec les nouvelles entrées | ☐ |
| 2 | Observer : aucune ligne « périmée » pendant le chargement | Pas d'affichage de lignes de l'ancienne semaine | ☐ |

### TC-M10-012 — Navigation touches clavier (flèches haut/bas)
> **Rôle** : ALICE (EMP) | **P2**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Dans une cellule → flèche bas | Focus déplacé à la cellule suivante de la même colonne | ☐ |
| 2 | Cellule disabled (verrouillée) au milieu | Saut à la prochaine cellule active | ☐ |

---

## M11 — 🆕 Feuilles de temps — Discipline de soumission (PR #74)

> **Principe** : si une semaine en retard de ≥ 2 semaines est non soumise,
> TOUS les chemins d'écriture sur la semaine courante sont bloqués.
> La régularisation des semaines en retard reste toujours possible.

### TC-M11-001 — Avertissement semaine précédente non soumise
> **Rôle** : ALICE (EMP) | **P1** | **Préconditions** : Semaine N-1 avec entrées DRAFT non soumises

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Ouvrir `/timesheets` sur la semaine courante | Bandeau jaune d'avertissement : « Semaine précédente non soumise » avec lien direct | ☐ |
| 2 | La saisie sur la semaine courante est-elle bloquée ? | Non — avertissement uniquement (1 seule semaine de retard) | ☐ |

### TC-M11-002 — Blocage à 2 semaines de retard : saisie
> **Rôle** : ALICE (EMP) | **P1** | **Préconditions** : Semaine N-2 ou plus ancienne avec entrées DRAFT

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Ouvrir `/timesheets` sur la semaine courante | Bandeau rouge de blocage avec liste des semaines en retard et liens directs | ☐ |
| 2 | Tenter de saisir des heures sur la semaine courante | Cellules verrouillées, tooltip « Saisie bloquée : soumettez vos feuilles en retard » | ☐ |
| 3 | Saisir des heures sur la semaine en retard (N-2) | Autorisé — régularisation possible | ☐ |

### TC-M11-003 — Blocage : tous les chemins d'écriture bloqués (semaine courante)
> **Rôle** : ALICE (EMP) | **P1** | **Préconditions** : En situation de blocage (≥ 2 semaines retard)

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Modifier une entrée existante de la semaine courante | 400 `LATE_TIMESHEETS` | ☐ |
| 2 | « Copier la semaine précédente » pour la semaine courante | 400 `LATE_TIMESHEETS`, aucune copie | ☐ |
| 3 | Pré-remplissage fériés pour la semaine courante | Bloqué, pas d'appel POST | ☐ |

### TC-M11-004 — Blocage : uniquement la semaine courante/future
> **Rôle** : ALICE (EMP) | **P1** | **Préconditions** : En situation de blocage

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Naviguer sur une semaine passée en retard (semaine N-2) | Cellules éditables | ☐ |
| 2 | Modifier une heure de la semaine N-2 | Sauvegarde OK (régularisation autorisée) | ☐ |
| 3 | Naviguer sur la semaine N+1 (future) | Cellules verrouillées (discipline aussi sur le futur) | ☐ |

### TC-M11-005 — Déblocage après soumission des retards
> **Rôle** : ALICE (EMP) | **P1** | **Préconditions** : En situation de blocage

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Naviguer vers la semaine N-2 via le lien direct du bandeau | Semaine N-2 chargée | ☐ |
| 2 | Soumettre la semaine N-2 | `submitted_count > 0` | ☐ |
| 3 | Naviguer sur la semaine courante | Bandeau de blocage disparu, saisie autorisée | ☐ |

### TC-M11-006 — Bandeau lateBlocked uniquement sur semaine courante
> **Rôle** : ALICE (EMP) | **P2** | **Préconditions** : En situation de blocage

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Afficher une semaine passée non impactée | Pas de bandeau de blocage sur cette semaine | ☐ |
| 2 | Revenir sur la semaine courante | Bandeau de blocage réapparaît | ☐ |

### TC-M11-007 — Texte d'aide : « À partir de 2 semaines »
> **Rôle** : ALICE (EMP) | **P2**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | `/timesheets` → aide contextuelle « ? » | Texte : « À partir de 2 semaines de retard → la saisie est bloquée » (pas « Au-delà ») | ☐ |

---

## M12 — 🆕 Feuilles de temps — Heures facturées intouchables (PR #74)

> **Principe** : une entrée `is_invoiced=True` est protégée à tous les niveaux
> (cellule UI, API create/update/delete, bulk_correct, transfer_hours, rejets).

### TC-M12-001 — Cellule facturée : badge et verrou UI
> **Rôle** : ALICE (EMP) | **P1** | **Préconditions** : Entrée `is_invoiced=True` dans la semaine

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Grille feuilles de temps | Cellule avec badge « $ » vert | ☐ |
| 2 | Tenter de modifier la valeur | Cellule grisée (disabled) — saisie impossible | ☐ |

### TC-M12-002 — Message erreur ENTRY_INVOICED affiché
> **Rôle** : ALICE (EMP) | **P1** | **Préconditions** : Entrée facturée accessible (non disabled)

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Forcer une tentative de modification (ex. via API directe ou entrée non grisée) | Tooltip rouge : « Modification impossible : cette heure a été facturée au client. » | ☐ |

### TC-M12-003 — Verrou modèle : modification heures refusée
> **Rôle** : ADM / FIN | **P1** | **Préconditions** : Entrée facturée (via admin Django ou API)

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Tenter PATCH sur `/api/v1/time_entries/{id}/` avec `hours` modifié | 400 `ENTRY_INVOICED` | ☐ |

### TC-M12-004 — Verrou modèle : modification date refusée
> **Rôle** : ADM / FIN | **P1** | **Préconditions** : Entrée facturée

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | PATCH avec `date` modifiée | 400 `ENTRY_INVOICED` | ☐ |

### TC-M12-005 — Verrou modèle : modification projet refusée
> **Rôle** : ADM / FIN | **P1** | **Préconditions** : Entrée facturée

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | PATCH avec `project` modifié | 400 `ENTRY_INVOICED` | ☐ |

### TC-M12-006 — Transition de statut autorisée sur entrée facturée
> **Rôle** : PM | **P1** | **Préconditions** : Entrée `is_invoiced=True`, statut PM_APPROVED

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Verrouiller la période (admin) | Entrée passe en LOCKED — transition autorisée | ☐ |

### TC-M12-007 — Suppression directe refusée
> **Rôle** : EMP / PM | **P1** | **Préconditions** : Entrée facturée

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | DELETE `/api/v1/time_entries/{id}/` | 400 ou 405 — refus | ☐ |
| 2 | Entrée toujours présente en base | Non supprimée | ☐ |

### TC-M12-008 — bulk_correct ignore les entrées facturées
> **Rôle** : EVE (FIN) | **P1** | **Préconditions** : Entrée facturée + entrée non facturée

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | `POST /api/v1/time_entries/bulk_correct/` avec les deux entrées | `corrected_count = 1` (non facturée corrigée) | ☐ |
| 2 | Entrée facturée | Non modifiée, message d'erreur dans la réponse | ☐ |

### TC-M12-009 — transfer_hours refusé si entrée facturée
> **Rôle** : EVE (FIN) | **P1** | **Préconditions** : Entrée facturée

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | `POST /api/v1/time_entries/transfer_hours/` avec l'entrée facturée | 400 `ENTRY_INVOICED` | ☐ |
| 2 | Entrée toujours sur le projet original | Non transférée | ☐ |

### TC-M12-010 — reject_entries ignore les entrées facturées
> **Rôle** : CAROL (PM) | **P1** | **Préconditions** : Entrée facturée + entrée non facturée SUBMITTED

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | `POST /api/v1/time_entries/reject_entries/` avec les deux | `rejected_count = 1` (non facturée rejetée) | ☐ |
| 2 | Entrée facturée | Toujours SUBMITTED — non repassée en DRAFT | ☐ |

### TC-M12-011 — reject_pm (WeeklyApproval) ignore les entrées facturées
> **Rôle** : CAROL (PM) | **P1**

| # | Action | Attendu | ☐ |
|---|--------|------oordes---|
| 1 | Rejeter une semaine via `reject_pm` contenant des entrées facturées | Entrées non facturées → DRAFT, facturées → inchangées | ☐ |

### TC-M12-012 — Suppression tâche bloquée (cascade)
> Voir TC-M05-009

### TC-M12-013 — Entrée facturée visible dans le texte d'aide
> **Rôle** : EMP | **P2**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Panneau d'aide feuilles de temps | Mention : « Les heures FACTURÉES au client sont définitivement intouchables » | ☐ |

---

## M13 — Feuilles de temps — Approbation PM

### TC-M13-001 — Dashboard PM
> **Rôle** : CAROL (PM) | **P1** | **Préconditions** : ALICE et BOB ont des semaines SUBMITTED

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Naviguer `/approvals` | KPIs : total heures, ratio CA/salaires, en attente PM | ☐ |
| 2 | Liste des employés | ALICE et BOB visibles avec `pm_status=PENDING` | ☐ |
| 3 | Tendance 4 semaines | `trend_4w` : 4 valeurs affichées | ☐ |
| 4 | Détail par projet | Heures par projet pour chaque employé | ☐ |

### TC-M13-002 — Approbation par entrée
> **Rôle** : CAROL (PM) | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Sélectionner des entrées de ALICE sur PRJ-A → « Approuver » | `approved_count = N`, entrées passent en PM_APPROVED | ☐ |
| 2 | Toutes les entrées d'ALICE sont PM_APPROVED | `WeeklyApproval.pm_status = APPROVED` | ☐ |

### TC-M13-003 — Approbation globale semaine
> **Rôle** : CAROL (PM) | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | « Approuver tout » pour BOB (semaine W) | Toutes les entrées BOB sur projets CAROL → PM_APPROVED | ☐ |

### TC-M13-004 — Rejet avec raison
> **Rôle** : CAROL (PM) | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Sélectionner des entrées → « Rejeter » | Champ raison obligatoire | ☐ |
| 2 | Saisir « Mauvais code projet », confirmer | Entrées → DRAFT, `rejection_reason` rempli | ☐ |
| 3 | En tant que ALICE, voir le rejet | Entrées DRAFT avec raison visible | ☐ |

### TC-M13-005 — Anti-self-approval PM
> **Rôle** : PM qui est aussi EMPLOYEE | **P1** | **Préconditions** : Compte avec rôle PM+EMPLOYEE

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Tenter d'approuver ses propres entrées | 403 `SELF_APPROVAL` | ☐ |

### TC-M13-006 — Multi-PM : approbation partielle
> **Rôle** : CAROL (PM) + DAVE (PM différent) | **P1** | **Préconditions** : ALICE a des entrées sur PRJ-A (CAROL) et PRJ-B (DAVE)

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | CAROL approuve les entrées PRJ-A d'ALICE | PRJ-A → PM_APPROVED, PRJ-B → SUBMITTED | ☐ |
| 2 | Dashboard CAROL : statut ALICE | `pm_status=PENDING` (PRJ-B pas encore approuvé) | ☐ |
| 3 | DAVE approuve les entrées PRJ-B d'ALICE | Tous PM_APPROVED | ☐ |
| 4 | `WeeklyApproval.pm_status` | APPROVED | ☐ |

### TC-M13-007 — Rejet via WeeklyApproval
> **Rôle** : CAROL (PM) | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Dashboard → fiche ALICE → « Rejeter la semaine » avec raison | `pm_status = REJECTED`, toutes les SUBMITTED → DRAFT | ☐ |
| 2 | Vérifier les entrées facturées (is_invoiced=True) si présentes | Restent inchangées (non repassées en DRAFT) 🆕 | ☐ |

### TC-M13-008 — PM ne peut pas approuver le projet d'un autre PM
> **Rôle** : CAROL (PM) | **P2** | **Préconditions** : BOB a des entrées sur PRJ-B (PM=DAVE)

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | CAROL tente d'approuver les entrées PRJ-B de BOB | `approved_count = 0` (filtre automatique) | ☐ |

---

## M14 — Feuilles de temps — Finance et Paie

### TC-M14-001 — Dashboard Paie
> **Rôle** : FRANK (PAI) | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Naviguer `/approvals` en tant que FRANK | Vue paie : tous les employés avec alertes de contrôle paie | ☐ |
| 2 | Employé sans entrée | Alerte `MISSING_TIMESHEET` (sévérité erreur) | ☐ |
| 3 | Employé 32h, pas d'absence | Alerte `INCOMPLETE_HOURS` (warning) | ☐ |
| 4 | Tri par sévérité | Erreurs d'abord, puis warnings, puis OK | ☐ |

### TC-M14-002 — Contrôle paie : overtime + maladie même semaine
> **Rôle** : FRANK (PAI) | **P1** | **Préconditions** : ALICE a 42h + heures maladie

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Dashboard Paie | Alerte `OVERTIME_WITH_SICK` (erreur) pour ALICE | ☐ |

### TC-M14-003 — Contrôle paie : jour > 10h
> **Rôle** : FRANK (PAI) | **P2**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | ALICE avec 12h un même jour | Alerte `DAY_OVER_10H` (warning) | ☐ |

### TC-M14-004 — Contrôle paie : weekend
> **Rôle** : FRANK (PAI) | **P2**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | ALICE avec heures samedi | Alerte `WEEKEND_WORK` (warning) | ☐ |

### TC-M14-005 — Validation paie individuelle
> **Rôle** : FRANK (PAI) | **P1** | **Préconditions** : ALICE tout PM_APPROVED

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Dashboard → ALICE → « Valider paie » | 200, `paie_status=APPROVED`, entrées → PAIE_VALIDATED | ☐ |

### TC-M14-006 — Validation paie refusée si pas tout PM_APPROVED
> **Rôle** : FRANK (PAI) | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | ALICE avec mélange SUBMITTED/PM_APPROVED → « Valider paie » | 400 `NOT_ALL_PM_APPROVED` | ☐ |

### TC-M14-007 — Validation paie en masse
> **Rôle** : FRANK (PAI) | **P1** | **Préconditions** : ALICE et BOB tout PM_APPROVED

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Sélectionner ALICE et BOB → « Valider en masse » | `{validated_count: 2, skipped_count: 0}` | ☐ |

### TC-M14-008 — Anti-self-approval paie
> **Rôle** : FRANK (PAI) | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | FRANK tente de valider sa propre semaine paie | 403 `SELF_APPROVAL` | ☐ |

### TC-M14-009 — Rejet paie
> **Rôle** : FRANK (PAI) | **P2**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | ALICE en `paie_status=APPROVED` → « Rejeter » | `paie_status=REJECTED`, entrées → PM_APPROVED | ☐ |

### TC-M14-010 — Dashboard Finance
> **Rôle** : EVE (FIN) | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Naviguer `/approvals` en tant que EVE | Vue finance : employés avec `pm_status=APPROVED` en attente | ☐ |
| 2 | Approuver finance pour ALICE | `finance_status=APPROVED` | ☐ |
| 3 | Anti-self-approval Finance | EVE ne peut pas approuver ses propres entrées | ☐ |

---

## M15 — Congés et absences

### TC-M15-001 — Demande de congé
> **Rôle** : ALICE (EMP) | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Naviguer `/leaves` → « + Nouvelle demande » | Formulaire : type, date début, date fin, motif | ☐ |
| 2 | Sélectionner type « Vacances », 5 jours | Demande créée en statut PENDING | ☐ |
| 3 | Vérifier les soldes | Jours demandés déduits de l'affichage | ☐ |

### TC-M15-002 — Chevauchement refusé
> **Rôle** : ALICE (EMP) | **P1** | **Préconditions** : Demande vacances semaine X

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Créer une 2e demande chevauchant la semaine X | Refus : « Chevauchement avec une demande existante » | ☐ |

### TC-M15-003 — Validation RH
> **Rôle** : GRACE (ADM) / RH | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Voir la demande d'ALICE → « Approuver » | `status=APPROVED` | ☐ |
| 2 | Entrées de temps créées automatiquement | Entrées Congé créées pour les jours ouvrables | ☐ |
| 3 | Ces entrées apparaissent dans la grille feuilles de temps | Jours de congé visibles | ☐ |

### TC-M15-004 — Refus RH
> **Rôle** : ADM / RH | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Refuser une demande avec motif | `status=REJECTED`, soldes non débités | ☐ |

### TC-M15-005 — 7 types de congé disponibles
> **Rôle** : ALICE (EMP) | **P2**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Liste des types dans le formulaire | Vacances, Maladie, Personnel, Férié, Parental, Sans solde, Deuil | ☐ |

### TC-M15-006 — Congé validé → impact sur planification
> **Rôle** : ADM | **P2** | **Préconditions** : Congé ALICE approuvé

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Naviguer `/planning` | ALICE avec disponibilité réduite pendant les jours de congé | ☐ |

---

## M16 — Occupation des ressources

### TC-M16-001 — Vue occupation (libellé UI correct)
> **Rôle** : PM / DIR | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Naviguer `/planning` | Titre de la page : « Occupation des ressources » (pas « Planification ») | ☐ |
| 2 | Menu de navigation | Libellé « Occupation » | ☐ |

### TC-M16-002 — Vue Gantt occupation par employé
> **Rôle** : PM | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Vue par employé | Barres d'allocation par projet/tâche pour chaque semaine | ☐ |
| 2 | Heures planifiées vs contrat | Affichées avec indicateur de charge | ☐ |
| 3 | Surcharge (>100%) | Rouge | ☐ |
| 4 | Sous-charge (<50%) | Orange ou gris | ☐ |
| 5 | Critique (>120%) | Rouge foncé | ☐ |

### TC-M16-003 — Alertes 4 prochaines semaines
> **Rôle** : PM / DIR | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Bandeau d'alertes | Surcharges et sous-charges des 4 prochaines semaines listées | ☐ |

### TC-M16-004 — Disponibilité = contrat - congés
> **Rôle** : PM | **P2**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | ALICE avec congé approuvé d'une semaine | Sa disponibilité cette semaine = contrat - heures congé | ☐ |

---

## M17 — Facturation

### TC-M17-001 — Création facture depuis un projet
> **Rôle** : EVE (FIN) | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Onglet Finances d'un projet → « + Facture » | Formulaire avec lignes WBS client, montant, taxes | ☐ |
| 2 | Vérifier les libellés des lignes | Libellés WBS client (pas les noms internes) | ☐ |
| 3 | Sauvegarder comme brouillon | Statut DRAFT, numéro auto-incrémenté | ☐ |

### TC-M17-002 — Workflow facture : 5 étapes
> **Rôle** : EVE (FIN) | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | DRAFT → Soumettre | Statut SUBMITTED | ☐ |
| 2 | SUBMITTED → Approuver | Statut APPROVED | ☐ |
| 3 | APPROVED → Envoyer | Statut SENT | ☐ |
| 4 | SENT → Marquer payée | Statut PAID | ☐ |

### TC-M17-003 — Facture émise : non modifiable
> **Rôle** : EVE (FIN) | **P1** | **Préconditions** : Facture au statut SENT ou PAID

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Tenter de modifier le montant | Champs en lecture seule, message explicite | ☐ |
| 2 | Bouton « Modifier » absent ou désactivé | Pas d'accès à l'édition | ☐ |

### TC-M17-004 — Avoir ou facture rectificative
> **Rôle** : EVE (FIN) | **P1** | **Préconditions** : Facture émise

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | « + Avoir » sur la facture émise | Nouvelle note de crédit liée à la facture | ☐ |

### TC-M17-005 — Calcul taxes automatique
> **Rôle** : EVE (FIN) | **P1** | **Préconditions** : Client avec schéma Québec TPS+TVQ

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Créer une facture pour ce client | TPS 5% + TVQ 9,975% calculées automatiquement | ☐ |
| 2 | Modifier le montant HT | Taxes recalculées en temps réel | ☐ |

### TC-M17-006 — Anti-self-approval facturation
> **Rôle** : EVE (FIN) | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | EVE tente d'approuver une facture qu'elle a créée | 403 (anti-self-approval) | ☐ |

### TC-M17-007 — mark_hours_invoiced : heures → is_invoiced=True 🆕
> **Rôle** : EVE (FIN) | **P1** | **Préconditions** : Facture avec des lignes liées à des entrées de temps

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Après approbation facture → « Marquer heures facturées » | Entrées de temps liées : `is_invoiced=True` | ☐ |
| 2 | Ces entrées dans les feuilles de temps | Badge « $ » visible, cellules verrouillées | ☐ |
| 3 | Tenter de modifier ces entrées (PATCH API) | 400 `ENTRY_INVOICED` | ☐ |

### TC-M17-008 — Paiements et retenues
> **Rôle** : EVE (FIN) | **P2**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Enregistrer un paiement partiel | Montant restant dû mis à jour | ☐ |
| 2 | Ajouter une retenue client | Retenue visible sur la facture | ☐ |

### TC-M17-009 — Liste des factures
> **Rôle** : EVE (FIN) | **P2**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Naviguer `/billing` | Liste avec filtres statut, client, date | ☐ |
| 2 | Analyse des impayés (aging analysis) | Répartition par tranche de retard | ☐ |

---

## M18 — Dépenses

### TC-M18-001 — Création dépense
> **Rôle** : ALICE (EMP) / PM | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Naviguer `/expenses` → « + Dépense » | Formulaire : catégorie, montant, date, projet, description | ☐ |
| 2 | Catégorie « Transport », 45 $ | Dépense créée en SUBMITTED | ☐ |
| 3 | Upload d'un reçu (photo/PDF) | Fichier joint à la dépense | ☐ |

### TC-M18-002 — Workflow dépense
> **Rôle** : CAROL (PM) / EVE (FIN) | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | PM → approuver la dépense | Statut PM_APPROVED | ☐ |
| 2 | Finance → valider | Statut FINANCE_VALIDATED | ☐ |
| 3 | Finance → marquer payée | Statut PAID | ☐ |

### TC-M18-003 — Refacturation client
> **Rôle** : EVE (FIN) | **P2**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Cocher « Refacturable client » sur une dépense | Option cochée, visible sur la facture | ☐ |

### TC-M18-004 — 15 catégories disponibles
> **Rôle** : ALICE (EMP) | **P2**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Dropdown catégorie | Transport, Repas, Hébergement, Fournitures… (≥ 10 catégories) | ☐ |

---

## M19 — Fournisseurs et sous-traitants

### TC-M19-001 — Fiche fournisseur
> **Rôle** : EVE (FIN) | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Naviguer `/suppliers` → « + Fournisseur » | Formulaire nom, type (ST/fournisseur), contact, conditions paiement | ☐ |
| 2 | Créer, sauvegarder | Fiche fournisseur créée | ☐ |

### TC-M19-002 — Facture ST : création et workflow
> **Rôle** : EVE (FIN) | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Fiche fournisseur → « + Facture ST » | Formulaire montant, projet, phase, date | ☐ |
| 2 | Créer en statut RECEIVED | Facture créée | ☐ |
| 3 | PM → Autoriser | Statut AUTHORIZED | ☐ |
| 4 | Finance → Payer | Statut PAID | ☐ |

### TC-M19-003 — Batch authorize
> **Rôle** : PM | **P2**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Sélectionner plusieurs factures ST en RECEIVED → « Autoriser en masse » | Toutes → AUTHORIZED | ☐ |

### TC-M19-004 — Litige
> **Rôle** : EVE (FIN) | **P2**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Facture ST → « Ouvrir litige » | Statut DISPUTED, champ description du litige | ☐ |
| 2 | Résoudre le litige | Statut revient à AUTHORIZED | ☐ |

### TC-M19-005 — Retenue ST
> **Rôle** : EVE (FIN) | **P2**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Appliquer une retenue à une facture ST | Montant retenue déduit du paiement | ☐ |
| 2 | Libérer la retenue | Paiement de la retenue enregistré | ☐ |

---

## M20 — Consortium

### TC-M20-001 — Création consortium
> **Rôle** : EVE (FIN) / ADM | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Naviguer `/consortiums/new` | Formulaire : nom, projet, membres et coefficients | ☐ |
| 2 | Ajouter cabinet (60%) + partenaire (40%) | Total = 100% | ☐ |
| 3 | Tenter 60% + 50% | Refus : total ≠ 100% | ☐ |
| 4 | Confirmer avec 60%+40% | Consortium créé | ☐ |

### TC-M20-002 — Vue duale (bleu/jaune)
> **Rôle** : EVE (FIN) | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Onglet « Vue duale » | Panneau bleu (consortium global) + panneau jaune (part Provencher-Roy) | ☐ |
| 2 | Heures saisies par les équipes | Réparties selon les coefficients | ☐ |

### TC-M20-003 — Les 6 onglets du consortium
> **Rôle** : EVE (FIN) | **P2**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Vérifier les onglets | Overview, Vue duale, Projets, Factures partenaires, Distributions, Taxes | ☐ |

### TC-M20-004 — Distributions
> **Rôle** : EVE (FIN) | **P2**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Onglet Distributions → calculer la distribution | Montants calculés selon les coefficients | ☐ |

---

## M21 — Dashboard et rapports

### TC-M21-001 — KPIs par rôle : PM
> **Rôle** : CAROL (PM) | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Naviguer `/` en tant que CAROL | KPIs PM : heures ce mois, ratio CA/salaires (cible 2,5x), taux de facturation, carnet de commandes | ☐ |

### TC-M21-002 — KPIs par rôle : Finance
> **Rôle** : EVE (FIN) | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Dashboard Finance | Factures impayées par tranche, dépenses en attente de validation | ☐ |

### TC-M21-003 — KPIs par rôle : Admin
> **Rôle** : GRACE (ADM) | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Dashboard Admin | System health : projets actifs, approbations en attente, factures en retard | ☐ |

### TC-M21-004 — Rapport heures : groupement et export
> **Rôle** : PM / FIN / ADM | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Naviguer `/reports` | Rapport heures groupable par projet / employé / BU | ☐ |
| 2 | Filtrer par période | Données filtrées | ☐ |
| 3 | Exporter CSV | Fichier téléchargé avec les données filtrées | ☐ |

### TC-M21-005 — Libellés WBS client dans les rapports
> **Rôle** : PM / FIN | **P2**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Rapport destiné au client (pivot par phase) | Libellés WBS client affichés (pas les noms internes) | ☐ |

---

## M22 — Sécurité et permissions

### TC-M22-001 — Projet interne masqué pour les non-admins
> **Rôle** : ALICE (EMP) | **P1** | **Préconditions** : Projet `is_internal=True` existe

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Naviguer `/projects` en tant que ALICE | Projet interne absent de la liste | ☐ |
| 2 | En tant que GRACE (ADM) | Projet interne visible | ☐ |

### TC-M22-002 — Isolation des données employé
> **Rôle** : ALICE (EMP) | **P1** | **Préconditions** : BOB a des entrées de temps

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | ALICE GET `/api/v1/time_entries/` | Uniquement les entrées d'ALICE | ☐ |
| 2 | ALICE GET `/api/v1/time_entries/{bob_entry_id}/` | 404 Not Found | ☐ |

### TC-M22-003 — Paramétrage standard réservé admin
> **Rôle** : CAROL (PM) | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | POST `/api/v1/standard_phases/` en tant que CAROL | 403 Forbidden | ☐ |
| 2 | POST `/api/v1/standard_tasks/` en tant que CAROL | 403 Forbidden | ☐ |
| 3 | POST `/api/v1/teams/` en tant que CAROL | 403 Forbidden | ☐ |

### TC-M22-004 — Isolation tenant
> **Rôle** : Tous | **P1** | **Préconditions** : Environnement multi-tenant

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Requête sans header `X-Tenant-ID` | 400 ou 403 | ☐ |
| 2 | Header avec tenant inconnu | 400 ou 403 | ☐ |
| 3 | Accès croisé (données tenant A pour un utilisateur tenant B) | Données absentes ou 404 | ☐ |

### TC-M22-005 — Concurrence optimiste (version field)
> **Rôle** : ALICE (EMP) | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | PATCH avec `version=1` (version actuelle) | 200 OK, version passe à 2 | ☐ |
| 2 | PATCH avec `version=1` à nouveau (périmé) | 409 Conflict | ☐ |

### TC-M22-006 — HTTPS obligatoire en prod
> **Rôle** : ADM | **P2**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Tenter d'accéder en HTTP sur srv1248490.hstgr.cloud | Redirection vers HTTPS | ☐ |

### TC-M22-007 — Pas de données personnelles dans les URLs
> **Rôle** : Tous | **P2**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Observer les URLs lors de la navigation | Pas de NAS, salaire, ou donnée sensible dans les query strings | ☐ |

### TC-M22-008 — Coût construction absent des projets internes
> **Rôle** : ADM | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Projet interne → onglet Paramètres | Champ « Coût de construction » absent | ☐ |
| 2 | Projet externe → onglet Paramètres | Champ présent et éditable | ☐ |

### TC-M22-009 — Budget non saisissable sur les phases
> **Rôle** : PM | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Cliquer sur une phase dans l'onglet Phases | Pas de champ budget, dates ou mode de facturation | ☐ |
| 2 | Ces champs sont sur la tâche feuille | Vérifier fiche tâche | ☐ |

### TC-M22-010 — Libellé « Occupation » (pas « Planification »)
> **Rôle** : Tous | **P1**

| # | Action | Attendu | ☐ |
|---|--------|---------|---|
| 1 | Menu de navigation | Libellé « Occupation » (jamais « Planification ») | ☐ |
| 2 | Titre de la page `/planning` | « Occupation des ressources » | ☐ |

---

## Annexe A — Matrice de transition de statut (feuilles de temps)

```
DRAFT ──[submit_week]──────────────────────────> SUBMITTED
SUBMITTED ──[approve_entries / approve_all]────> PM_APPROVED
SUBMITTED ──[reject_entries / reject_pm]───────> DRAFT (+ rejection_reason)
PM_APPROVED ──[validate_paie]──────────────────> PAIE_VALIDATED
PAIE_VALIDATED ──[reject_paie]─────────────────> PM_APPROVED
Tout (sauf LOCKED) ──[lock_period / lock_before]> LOCKED
LOCKED ──[unlock_period]───────────────────────> SUBMITTED

Invariants PR #73/#74 :
- is_invoiced=True : champs INVOICED_PROTECTED_FIELDS gelés à tout statut
- ≥ 2 semaines retard non soumises : saisie semaine courante bloquée
```

## Annexe B — Chemins d'écriture couverts (discipline + is_invoiced)

| Chemin | Discipline LATE | is_invoiced |
|--------|-----------------|-------------|
| POST /time_entries/ | ✅ bloqué si semaine courante | ✅ n/a (création) |
| PATCH /time_entries/{id}/ | ✅ bloqué si semaine courante | ✅ refus si champ protégé |
| DELETE /time_entries/{id}/ | — | ✅ ProtectedError signal |
| POST copy_previous_week | ✅ bloqué si semaine courante | — |
| POST prefill_holidays | ✅ bloqué si semaine courante | — |
| POST bulk_correct | — | ✅ skip silencieux + erreur |
| POST transfer_hours | — | ✅ 400 refus |
| POST reject_entries | — | ✅ filtre is_invoiced=False |
| POST reject_pm (WeeklyApproval) | — | ✅ filtre is_invoiced=False |
| DELETE Task (API) | — | ✅ 400 si heures facturées |
| Task.delete() (ORM/cascade) | — | ✅ ProtectedError signal |

---

*Généré le 2026-06-13 — ERP v5 (post-PR #74)*
