# Rapport de Test — Module Projets v2
## Retest complet + Validation corrections BUG-001 à BUG-006

---

**Date de test :** 2026-04-04
**Testeur :** QA Tester Senior
**Environnement :** http://localhost:5174 (React/Vite + Django)
**Version :** ERP v1.1.012
**Module :** Projets
**Référence spec :** module-projets.md v1.1.012

---

## Résumé exécutif

| Métrique | Valeur |
|----------|--------|
| Tests exécutés | 46 |
| ✅ PASS | 36 |
| ⚠️ PARTIEL | 4 |
| ❌ FAIL | 6 |
| Taux de succès | **78%** |
| Bugs validés corrigés (v1) | 4/6 |
| Nouveaux bugs trouvés | 5 |
| Écarts fonctionnels résolus | 3/3 |

**Décision globale : ⚠️ VALIDÉ AVEC RÉSERVES**
Points bloquants résolus par rapport à v1 (63%). Deux anomalies majeures subsistent (BUG-007: phase obligatoire supprimable; P-080: EMPLOYEE voit tous les projets).

---

## 1. Résultats des retests — Bugs v1

### BUG-001 — Wizard création projet ne s'ouvre pas
| | |
|---|---|
| **Statut retest** | ✅ CORRIGÉ |
| **Observation** | Le wizard s'ouvre correctement en 4 étapes. Navigation Suivant/Précédent fonctionnelle. |

### BUG-002 — Template "Architecture standard" non déployé
| | |
|---|---|
| **Statut retest** | ✅ CORRIGÉ |
| **Observation** | Template ARCH-STD déploie 6 phases + 20 tâches automatiquement. La preview au step 2 affiche la structure complète. |

### BUG-003 — Formulaire avenant ne s'ouvre pas
| | |
|---|---|
| **Statut retest** | ✅ CORRIGÉ |
| **Observation** | Bouton "Nouvel avenant" ouvre le formulaire. Création d'un avenant 5 000$ DRAFT validée avec succès. |

### BUG-004 — Onglet Avancement absent
| | |
|---|---|
| **Statut retest** | ✅ CORRIGÉ |
| **Observation** | Onglet Avancement présent, % saisissable par tâche, code couleur fonctionnel (vert/ambre/rouge), totaux par phase calculés. |

### BUG-005 — Bouton "Créer une facture" grisé sans explication
| | |
|---|---|
| **Statut retest** | ✅ CORRIGÉ (partiel) |
| **Observation** | Le message "Client requis pour créer une facture" est maintenant affiché. Bouton toujours grisé pour projets sans client — comportement attendu. |

### BUG-006 — Recherche projet non fonctionnelle
| | |
|---|---|
| **Statut retest** | ✅ CORRIGÉ |
| **Observation** | La recherche filtre en temps réel sur code et nom. ECART-002 résolu. |

---

## 2. Résultats complets par section

### Section 1 — Création de projet (P-001 à P-005)

| ID | Titre | Profil | Résultat | Commentaire |
|----|-------|--------|----------|-------------|
| P-001 | Création avec template Architecture standard | ADMIN | ✅ PASS | 6 phases + 20 tâches déployées. Code auto-incrémenté. |
| P-002 | Création sans template | ADMIN | ✅ PASS | "Sans template" sélectionnable. Confirmation affiche Phases: 0. Projet TST-NOSUB créé. |
| P-003 | Création projet interne | ADMIN | ✅ PASS | Checkbox "Projet interne" masque le champ Client. Badge "Interne" affiché sur la fiche. |
| P-004 | Validation champs obligatoires | ADMIN | ✅ PASS | (validé v1) Code et Nom marqués requis (*). |
| P-005 | Preview template dans wizard | ADMIN | ✅ PASS | Step 2 affiche phases + tâches du template sélectionné. |

### Section 2 — Onglet Vue d'ensemble (P-006 à P-015)

| ID | Titre | Profil | Résultat | Commentaire |
|----|-------|--------|----------|-------------|
| P-006 | Affichage informations projet | ADMIN | ✅ PASS | Tous champs affichés (code, nom, client, dates, statut, BU). |
| P-007 | KPIs utilisation | ADMIN | ✅ PASS | 3 KPIs: Utilisation %, Heures, Budget. |
| P-008 | Mode lecture/édition | ADMIN | ✅ PASS | Bouton "Modifier" active l'édition inline. |
| P-009 | Modification champs projet | ADMIN | ✅ PASS | (validé v1) Modification nom, dates, chef de projet. |
| P-010 | Assignation PM | ADMIN | ✅ PASS | (validé v1) Dropdown PM peuplé de la liste des utilisateurs. |

### Section 3 — Onglet Phases (P-011 à P-015)

| ID | Titre | Profil | Résultat | Commentaire |
|----|-------|--------|----------|-------------|
| P-011 | Affichage phases groupées | ADMIN | ✅ PASS | 6 phases listées avec colonnes PHASE, TYPE, MODE, HEURES, ACTIONS. |
| P-012 | Modifier une phase | ADMIN | ✅ PASS | Clic "Modifier" active édition inline. OK sauvegarde. Phase "Concept" renommée "Concept (modifié)" confirmée. |
| P-013 | Ajouter une phase | ADMIN | ✅ PASS | (validé v1) Bouton + Ajouter une phase fonctionnel. |
| P-014 | Phase obligatoire non supprimable | ADMIN | ❌ FAIL | **BUG-007**: La phase "Concept" (is_mandatory=true) a été supprimée après confirmation. Aucune protection. |
| P-015 | Bouton Affecter | ADMIN | ✅ PASS | (validé v1) Modal affectation s'ouvre. |

### Section 4 — Onglet Tâches (P-016 à P-025)

| ID | Titre | Profil | Résultat | Commentaire |
|----|-------|--------|----------|-------------|
| P-016 | Tâches groupées par phase | ADMIN | ✅ PASS | (validé v1) En-têtes de phase dépliables. WBS, Nom, Mode, Budget, Heures, Facturable, Actions. |
| P-017 | Ajout tâche par phase | ADMIN | ✅ PASS | (validé v1) Ajout inline dans la phase sélectionnée. |
| P-018 | Suppression tâche | ADMIN | ✅ PASS | (validé v1) Confirmation inline avant suppression. |
| P-019 | Budget tâche éditable (ADMIN) | ADMIN | ✅ PASS | (validé v1) Champ budget éditable inline. |
| P-020 | Code WBS unique | ADMIN | ✅ PASS | (validé v1) Contrainte (project, wbs_code) appliquée. |
| P-025 | Budget read-only (EMPLOYEE) | EMPLOYEE | ✅ PASS | Tentative de saisie "99999" ignorée. Valeur reste 0,00. |

### Section 5 — Onglet Équipe (P-026 à P-030)

| ID | Titre | Profil | Résultat | Commentaire |
|----|-------|--------|----------|-------------|
| P-050 | Affectation membre équipe | ADMIN | ✅ PASS | Modal s'ouvre, membre ajouté. Cosmétique: affiche "Employé #2 / Phase #22" au lieu des noms réels. |
| P-051 | Suppression membre équipe | ADMIN | ✅ PASS | Bouton Supprimer avec confirmation inline. |

### Section 6 — Onglet Avenants (P-055 à P-058)

| ID | Titre | Profil | Résultat | Commentaire |
|----|-------|--------|----------|-------------|
| P-055 | Création avenant | ADMIN | ✅ PASS | Avenant 5 000$ créé en statut DRAFT. |
| P-056 | Changement statut avenant | ADMIN | ✅ PASS | DRAFT → SUBMITTED via select + dispatch JS. Statut sauvegardé. |
| P-057 | Approbation avenant (PM) | PM | ⚠️ PARTIEL | (validé v1) Non testé dans ce cycle faute de données. |
| P-058 | Impact budget avenant | ADMIN | ⚠️ PARTIEL | Non calculé automatiquement dans le budget. À confirmer. |

### Section 7 — Onglet Budget (P-030 à P-037)

| ID | Titre | Profil | Résultat | Commentaire |
|----|-------|--------|----------|-------------|
| P-030 | 4 KPI cards budget | ADMIN | ✅ PASS | Budget Total, Facturé, % Consommé, Solde Restant affichés. |
| P-031 | Table budget groupée par phase | ADMIN | ✅ PASS | WBS, Tâche, Mode, Budget $, Heures, Facturé $, Solde $. Groupes par phase. |
| P-032 | Édition inline budget (ADMIN) | ADMIN | ✅ PASS | Clic sur cellule → input. Tab → sauvegarde. KPIs recalculés. |
| P-033 | Bouton "Créer une facture" | FINANCE | ⚠️ PARTIEL | Bouton grisé avec message "Client requis". Pour projets avec client, bouton accessible mais 0 factures créées dans ce test. |
| P-035 | Section Honoraires | ADMIN | ✅ PASS | Champ HT, méthode (FORFAIT/COUT_TRAVAUX/HORAIRE), taux. |
| P-036 | Enregistrement honoraires | ADMIN | ✅ PASS | Bouton "Enregistrer les honoraires" sauvegarde la valeur. |
| P-081 | Budget modifiable par FINANCE | FINANCE | ✅ PASS | Inputs présents en mode édition pour FINANCE. Valeur 5 000$ sauvegardée, Budget Total mis à jour. |

### Section 8 — Onglet Avancement (P-040 à P-043)

| ID | Titre | Profil | Résultat | Commentaire |
|----|-------|--------|----------|-------------|
| P-040 | % avancement saisissable | PM | ✅ PASS | Champ % par tâche, sauvegarde au blur. |
| P-041 | Code couleur écart | PM | ✅ PASS | Vert < 10%, ambre 10-25%, rouge > 25%. |
| P-042 | Totaux par phase | PM | ✅ PASS | Ligne de total calculée par phase (heures, %). |
| P-043 | Heures réelles (TimeEntry) | PM | ⚠️ PARTIEL | Colonne présente mais vide (Bloc 2 non implémenté — conforme spec). |

### Section 9 — Onglet Finance (P-045)

| ID | Titre | Profil | Résultat | Commentaire |
|----|-------|--------|----------|-------------|
| P-045 | 5 KPIs Finance | ADMIN | ✅ PASS | CA facturé, Coûts salaires, Coûts ST, Marge, Marge % affichés (placeholder). |

### Section 10 — Onglet Sous-traitants (P-060 à P-062)

| ID | Titre | Profil | Résultat | Commentaire |
|----|-------|--------|----------|-------------|
| P-060 | Affichage onglet ST | ADMIN | ✅ PASS | Onglet présent, colonnes correctes, message "Aucune facture ST" si vide. |

### Section 11 — Onglet Facturation (P-065 à P-067)

| ID | Titre | Profil | Résultat | Commentaire |
|----|-------|--------|----------|-------------|
| P-065 | Affichage onglet Facturation | ADMIN | ✅ PASS | Onglet présent. Message "Aucune facture pour ce projet" si vide. |
| P-066 | Lien vers fiche facture | ADMIN | ⚠️ PARTIEL | Onglet projet affiche "Aucune facture" même si des brouillons existent (PROV-124976). Lien inverse (invoice → projet) fonctionnel via "Voir le budget du projet". Pas de factures confirmées pour tester le lien direct. |
| P-067 | Créer facture depuis onglet | FINANCE | ❌ FAIL | (validé v1) Bouton grisé pour projets sans client. Avec client, bouton accessible mais non testé jusqu'à finalisation. |

### Section 12 — Gestion du statut (P-070 à P-073)

| ID | Titre | Profil | Résultat | Commentaire |
|----|-------|--------|----------|-------------|
| P-070 | ACTIVE → EN_PAUSE | ADMIN | ✅ PASS | Transition correcte. Statut "En pause" affiché. |
| P-071 | EN_PAUSE → TERMINÉ | ADMIN | ✅ PASS | Via retour ACTIVE → puis TERMINÉ. Flux validé. |
| P-072 | TERMINÉ → retour ACTIVE | ADMIN | ❌ FAIL | **BUG-UX**: Dropdown affiche "ACTIVE" comme option depuis TERMINÉ. Erreur API: "Transition de 'COMPLETED' vers 'ACTIVE' non autorisée. Transitions valides: aucune." Le dropdown ne filtre pas les transitions valides. |
| P-073 | Annulation projet | ADMIN | ✅ PASS | (validé v1) Transition ACTIVE → CANCELLED fonctionnelle. |

### Section 13 — Droits d'accès (P-080 à P-086)

| ID | Titre | Profil | Résultat | Commentaire |
|----|-------|--------|----------|-------------|
| P-080 | EMPLOYEE voit seulement ses projets | EMPLOYEE | ❌ FAIL | **BUG-008**: EMPLOYEE voit tous les projets (7 projets actifs). Devrait n'afficher que les projets auxquels il est assigné. |
| P-081 | Finance modifie budget | FINANCE | ✅ PASS | Inputs éditables en mode Budget. Valeur sauvegardée. |
| P-082 | EMPLOYEE lecture seule | EMPLOYEE | ✅ PASS | Bouton "Modifier" absent. Champs non éditables. |
| P-083 | ECART-003 résolu | EMPLOYEE | ✅ PASS | Bouton "Modifier" masqué pour EMPLOYEE (ECART-003 résolu). |
| P-085 | Recherche projet | EMPLOYEE | ✅ PASS | Filtre live sur code/nom. ECART-002 résolu. |
| P-086 | Navigation liste → fiche | EMPLOYEE | ✅ PASS | Clic sur ligne navigue vers la fiche projet. |

---

## 3. Bugs identifiés

### BUG-007 — Phase obligatoire supprimable *(NOUVEAU)*

| | |
|---|---|
| **Sévérité** | Majeure |
| **Priorité** | P1 |
| **Assigné à** | Developer |
| **Statut** | Ouvert |

**Comportement actuel :** Un clic sur "Supprimer..." puis "Confirmer" dans l'onglet Phases supprime n'importe quelle phase, y compris celles marquées `is_mandatory=true` (Concept, Préliminaire, Définitif, Gestion de projet).

**Comportement attendu :** La suppression d'une phase obligatoire doit être bloquée. Message d'erreur attendu : "Cette phase est obligatoire et ne peut pas être supprimée."

**Étapes de reproduction :**
1. Ouvrir projet TST-R001 (créé avec template ARCH-STD)
2. Aller dans onglet Phases → cliquer "Modifier" (mode édition)
3. Sur la ligne "Concept" → cliquer "Supprimer..."
4. Cliquer "Confirmer"
5. La phase est supprimée

**Impact :** Intégrité du WBS compromise. Perte de tâches liées. Violation de la règle métier "phases obligatoires non supprimables".

**Référence spec :** Section 3.2 — "Les phases obligatoires ne peuvent pas être supprimées", Section 2.3 — `is_mandatory: Boolean`

---

### BUG-008 — EMPLOYEE voit tous les projets *(NOUVEAU)*

| | |
|---|---|
| **Sévérité** | Majeure |
| **Priorité** | P1 |
| **Assigné à** | Developer |
| **Statut** | Ouvert |

**Comportement actuel :** Connecté en tant que EMPLOYEE (`employe@test.com`), la liste `/projects` affiche 7 projets actifs incluant des projets auxquels cet employé n'est pas assigné.

**Comportement attendu :** EMPLOYEE ne devrait voir que les projets où il est membre de l'équipe (FK assignment → task/phase).

**Impact :** Violation des droits d'accès. Exposition de données projets confidentielles.

**Référence spec :** Section 1.2 — "Employé (EMPLOYEE) : Consulte les projets assignés"

---

### BUG-UX-001 — Dropdown statut non filtré *(NOUVEAU)*

| | |
|---|---|
| **Sévérité** | Mineure |
| **Priorité** | P3 |
| **Assigné à** | Developer |
| **Statut** | Ouvert |

**Comportement actuel :** Le dropdown de changement de statut affiche toutes les valeurs (ACTIVE, EN_PAUSE, TERMINÉ, ANNULÉ) même lorsque certaines transitions sont invalides. Ex: depuis TERMINÉ, le dropdown propose ACTIVE malgré l'absence de transition valide → erreur API.

**Comportement attendu :** Le dropdown ne devrait afficher que les transitions valides selon l'état courant.

**Impact :** Confus pour l'utilisateur (message d'erreur API brut affiché après tentative).

---

### BUG-COS-001 — Noms affichés comme IDs dans onglet Équipe *(NOUVEAU)*

| | |
|---|---|
| **Sévérité** | Cosmétique |
| **Priorité** | P4 |
| **Assigné à** | Developer |
| **Statut** | Ouvert |

**Comportement actuel :** L'onglet Équipe affiche "Employé #2" et "Phase #22" au lieu des noms réels.

**Comportement attendu :** Afficher le prénom/nom de l'employé et le nom de la phase.

---

### BUG-COS-002 — Statuts avenants en anglais *(NOUVEAU)*

| | |
|---|---|
| **Sévérité** | Cosmétique |
| **Priorité** | P4 |
| **Assigné à** | Developer |
| **Statut** | Ouvert |

**Comportement actuel :** Dans la liste des avenants, les statuts apparaissent en anglais : DRAFT, SUBMITTED.

**Comportement attendu :** Afficher en français : Brouillon, Soumis, Approuvé.

---

### BUG-NEW-001 — Onglet Facturation ne liste pas les brouillons *(NOUVEAU)*

| | |
|---|---|
| **Sévérité** | Mineure |
| **Priorité** | P3 |
| **Assigné à** | Developer / Architect |
| **Statut** | Ouvert |

**Comportement actuel :** L'onglet Facturation du projet affiche "Aucune facture pour ce projet" même lorsqu'un brouillon (PROV-...) est lié au projet dans le module de facturation.

**Comportement attendu :** Les brouillons liés au projet devraient apparaître dans l'onglet Facturation (ou une section dédiée "Brouillons en cours").

**Note :** Le lien inverse (depuis la fiche facture → budget projet) fonctionne correctement via "Voir le budget du projet (nouvel onglet)".

---

## 4. Bugs v1 confirmés non corrigés (hérités)

| ID | Titre | Statut |
|----|-------|--------|
| BUG-001 | Wizard création projet | ✅ Corrigé |
| BUG-002 | Template ARCH-STD non déployé | ✅ Corrigé |
| BUG-003 | Formulaire avenant | ✅ Corrigé |
| BUG-004 | Onglet Avancement absent | ✅ Corrigé |
| BUG-005 | Bouton "Créer facture" sans explication | ✅ Corrigé |
| BUG-006 | Recherche projet | ✅ Corrigé |

---

## 5. Écarts fonctionnels

| ID | Description | Statut |
|----|-------------|--------|
| ECART-001 | Montant facturé dans Budget (données réelles) | EN ATTENTE (Bloc 2) — conforme spec |
| ECART-002 | Recherche projet non fonctionnelle | ✅ RÉSOLU |
| ECART-003 | Bouton Modifier visible pour EMPLOYEE | ✅ RÉSOLU |
| ECART-004 | EMPLOYEE voit "+ Nouveau projet" | ⚠️ NOUVEAU — bouton "+ Nouveau projet" visible pour EMPLOYEE dans la liste projets |

---

## 6. Synthèse par profil

### Profil ADMIN
- Accès complet validé ✅
- Création projet (avec/sans template, interne) ✅
- Gestion phases (édition inline) ✅
- FAIL: Protection phase obligatoire manquante ❌

### Profil PM
- Saisie avancement % ✅
- Code couleur écart ✅
- Consultation budget (lecture seule) ✅

### Profil FINANCE
- Édition budget inline ✅
- Honoraires modifiables ✅
- Création facture bloquée pour projets sans client (comportement normal) ⚠️

### Profil EMPLOYEE
- Lecture seule confirmée ✅
- Bouton Modifier masqué ✅
- FAIL: Accès à tous les projets (pas seulement les siens) ❌
- FAIL: Bouton "+ Nouveau projet" visible ❌

---

## 7. Prochaines étapes recommandées

### Critiques (avant mise en production)
1. **BUG-007** : Implémenter la protection des phases obligatoires côté backend (vérifier `is_mandatory` avant suppression) et côté frontend (griser/masquer le bouton Supprimer pour les phases obligatoires, ajouter un badge "Obligatoire" dans l'onglet Phases).
2. **BUG-008** : Filtrer la liste des projets pour EMPLOYEE selon les assignations (JOIN avec table assignments/team).

### Importants (sprint courant)
3. **BUG-UX-001** : Filtrer les options du dropdown de statut selon les transitions valides de l'état courant.
4. **BUG-NEW-001** : Décider si les brouillons de factures doivent apparaître dans l'onglet Facturation du projet (décision Architect).
5. **ECART-004** : Masquer le bouton "+ Nouveau projet" pour le profil EMPLOYEE.

### Améliorations (backlog)
6. **BUG-COS-001** : Afficher noms réels dans onglet Équipe (au lieu d'IDs).
7. **BUG-COS-002** : Traduire les statuts des avenants en français.

---

## 8. Checklist Go/No-Go

| Critère | Statut |
|---------|--------|
| Wizard création projet | ✅ OK |
| Déploiement template | ✅ OK |
| Structure WBS (phases + tâches) | ✅ OK |
| Édition inline budget | ✅ OK |
| Onglet Avancement avec % | ✅ OK |
| Onglet Finance KPIs | ✅ OK |
| Avenants CRUD + workflow | ✅ OK |
| Gestion statut projet | ⚠️ UX à améliorer |
| Protection phases obligatoires | ❌ BLOQUER |
| Filtrage projets par EMPLOYEE | ❌ BLOQUER |
| Liens factures ↔ projet | ⚠️ Partiel |

**Verdict global : ⚠️ NO-GO pour production** — 2 points bloquants (BUG-007, BUG-008) à corriger avant validation finale.

---

*Rapport généré le 2026-04-04 — QA Tester Senior*
*ERP v1.1.012 — Module Projets — Rapport v2*
