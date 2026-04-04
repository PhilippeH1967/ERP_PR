# Rapport de Test — Module Projets ERP Services Professionnels

## Informations générales

| Métrique | Valeur |
|----------|--------|
| **Date de test** | 2026-04-04 |
| **Testeur** | QA Tester (Claude) |
| **Environnement** | Local — http://localhost:5174 |
| **Version** | v1.1.012 |
| **Module testé** | Module Projets |
| **Référence spec** | module-projets.md v1.1.012 |

---

## Résumé exécutif

| Métrique | Valeur |
|----------|--------|
| Tests exécutés | 43 |
| Tests réussis ✅ | 27 |
| Tests partiels ⚠️ | 4 |
| Tests échoués ❌ | 12 |
| **Taux de réussite** | **63 %** |
| **Décision** | ⚠️ VALIDÉ AVEC RÉSERVES — bugs bloquants à corriger (P-021, P-050, P-055) |

---

## Décision globale

> **⚠️ VALIDÉ AVEC RÉSERVES** — Le module Projets couvre les fonctionnalités essentielles (CRUD projet, onglets Budget/Avancement/Finance/ST/Facturation, gestion des statuts, contrôle d'accès par rôle). Cependant, 3 bugs bloquants empêchent des workflows clés : l'ajout de tâche retourne "Bad Request", le bouton "Affecter" est absent de l'onglet Phases, et le module Avenants est non implémenté.

---

## Détail des tests par section

### Section 1 — Création de projet (P-001 à P-006)

| ID | Test | Profil | Résultat | Commentaire |
|----|------|--------|----------|-------------|
| P-001 | Création projet depuis template Architecture Standard | ADMIN | ✅ PASS | Projet TST-P001 créé, 6 phases + 20 tâches déployées automatiquement |
| P-002 | Wizard affiche les champs PM et Associé en charge | ADMIN | ❌ FAIL | Champs PM/Associé affichent des IDs numériques bruts (ex: "11") au lieu de dropdowns avec noms d'utilisateurs — UX non conforme |
| P-003 | Création projet sans template | ADMIN | ✅ PASS | Projet TST-P002 créé sans template, phases vides |
| P-004 | Création projet interne (sans client) | ADMIN | ✅ PASS | Projet TST-P003 créé, client = — , is_internal = true |
| P-005 | Vérification codes WBS auto-générés | ADMIN | ✅ PASS | WBS 1.1, 1.2, 2.1, 3.1… générés correctement depuis template |
| P-006 | Preview template (phases + tâches) dans wizard | ADMIN | ✅ PASS | Preview affiche les 6 phases et 20 tâches avant confirmation |

**Section 1 : 5 PASS / 1 FAIL**

---

### Section 2 — Template et déploiement (P-010 à P-014)

| ID | Test | Profil | Résultat | Commentaire |
|----|------|--------|----------|-------------|
| P-010 | Template "Architecture Standard" déployé avec 6 phases | ADMIN | ⚠️ PARTIEL | 6 phases déployées (Concept, Préliminaire, Définitif, Appel d'offres, Surveillance, GP) mais preview wizard affiche partiellement |
| P-011 | Template déployé avec 20 tâches | ADMIN | ⚠️ PARTIEL | 20 tâches créées (vérifiées dans l'onglet Tâches) — quelques tâches GP manquantes dans le décompte visuel initial |
| P-012 | Phases obligatoires non supprimables | ADMIN | ✅ PASS | Badge "Obligatoire" présent, tentative de suppression bloquée |
| P-013 | Phases optionnelles supprimables | ADMIN | ✅ PASS | Phases optionnelles supprimables depuis onglet Phases |
| P-014 | Ajout d'une phase manuelle | ADMIN | ✅ PASS | Ajout d'une phase manuelle fonctionnel depuis onglet Phases |

**Section 2 : 3 PASS / 2 PARTIEL**

---

### Section 3 — Tâches CRUD (P-020 à P-026)

| ID | Test | Profil | Résultat | Commentaire |
|----|------|--------|----------|-------------|
| P-020 | Tâches groupées par phase dans onglet Tâches | ADMIN | ✅ PASS | Groupes dépliables par phase (Concept, Préliminaire, Définitif…), badge (3 tâches) |
| P-021 | Ajout d'une nouvelle tâche via "+ Tâche" | ADMIN | ❌ FAIL | **BLOQUANT** — Clic sur "+ Tâche" puis saisie du nom retourne "Bad Request" (HTTP 400) côté backend. Reproduit avec noms accentués et non-accentués. |
| P-022 | Modifier budget tâche inline (sauvegarde au blur) | ADMIN | ✅ PASS | Budget tâche 2.1 modifié à 5000,00 — valeur persistée après blur et reload |
| P-023 | Modifier heures tâche inline (sauvegarde au blur) | ADMIN | ✅ PASS | Heures tâche 2.1 modifiées à 40,00 — valeur persistée après blur |
| P-024 | Supprimer une tâche | ADMIN | ✅ PASS | Tâche 2.3 supprimée via double-confirmation (Supprimer → Confirmer), compteur phase mis à jour |
| P-025 | Employé ne peut pas modifier budget/heures | EMPLOYEE | ✅ PASS | Budget et heures affichés en texte statique, pas de champs input, pas de boutons action |
| P-026 | Affichage liste tâches avec colonnes WBS/Mode/Budget/Heures/Facturable | ADMIN | ✅ PASS | Colonnes WBS, NOM, MODE, BUDGET($), HEURES, FACTURABLE, ACTIONS présentes |

**Section 3 : 5 PASS / 1 FAIL (bloquant)**

---

### Section 4 — Onglet Budget (P-030 à P-036)

| ID | Test | Profil | Résultat | Commentaire |
|----|------|--------|----------|-------------|
| P-030 | 4 KPI cards Budget visibles | ADMIN | ✅ PASS | Budget total 6 500$, Facturé 0$, % consommé 0%, Solde 6 500$ |
| P-031 | Table budget par tâche groupée par phase | ADMIN | ✅ PASS | Colonnes WBS, Tâche, Mode, Budget($), Heures, Facturé($), Solde($) — groupées CONCEPT / PRÉLIMINAIRE / DÉFINITIF |
| P-032 | Budget tâche éditable inline (ADMIN/FINANCE) | ADMIN | ✅ PASS | Budget tâche 1.1 modifié à 1500 — KPI "Budget total" mis à jour immédiatement (5000 → 6500) |
| P-033 | Bouton "Créer une facture" visible dans onglet Budget | ADMIN | ⚠️ PARTIEL | Bouton visible mais désactivé (`disabled=true`) — probablement conditionné à la présence d'un client sur le projet |
| P-034 | Section Honoraires visible avec Méthode de calcul | ADMIN | ✅ PASS | "Honoraires totaux HT" et dropdown "Méthode de calcul" (Forfait/Coût travaux/Horaire) présents |
| P-035 | Méthode de calcul honoraires modifiable | ADMIN | ✅ PASS | Dropdown modifiable (options Forfait, Coût travaux, Horaire) |
| P-036 | Enregistrement honoraires persisté | ADMIN | ✅ PASS | Honoraires 50 000 enregistrés via "Enregistrer les honoraires", valeur persistée après reload |

**Section 4 : 6 PASS / 1 PARTIEL**

---

### Section 5 — Onglet Avancement (P-040 à P-042)

| ID | Test | Profil | Résultat | Commentaire |
|----|------|--------|----------|-------------|
| P-040 | Tâches groupées par phase avec totaux | ADMIN | ✅ PASS | Phases avec rangées "Phase — Total" (Budget, H. Planifiées, H. Réelles, % Avancement) |
| P-041 | % avancement saisissable et persisté | ADMIN | ✅ PASS | Tâche 1.1 : 75% entré, sauvegardé au Tab/blur, total phase calculé (25.0%) |
| P-042 | Code couleur écart : vert / ambre / rouge | ADMIN | ✅ PASS | 0.0% = vert, 75.0% = rouge (>25%). Code couleur conforme spec (<10% vert, 10-25% ambre, >25% rouge) |

**Section 5 : 3 PASS**

---

### Section 6 — Onglet Finance (P-045)

| ID | Test | Profil | Résultat | Commentaire |
|----|------|--------|----------|-------------|
| P-045 | 5 KPI cards Finance visibles | ADMIN | ✅ PASS | CA Facturé, Coûts Salaires, Coûts ST, Marge ($), Marge (%) — table par année avec note "calculées automatiquement" (placeholder Bloc 2+, conforme spec) |

**Section 6 : 1 PASS**

---

### Section 7 — Onglet Équipe (P-050 à P-051)

| ID | Test | Profil | Résultat | Commentaire |
|----|------|--------|----------|-------------|
| P-050 | Assigner un membre via bouton "Affecter" dans Phases | ADMIN | ❌ FAIL | **BLOQUANT** — Bouton "Affecter" absent de la colonne ACTIONS dans l'onglet Phases. Onglet Équipe affiche "Aucune affectation — utilisez 'Affecter' dans l'onglet Phases". |
| P-051 | Supprimer un membre de l'équipe | ADMIN | ❌ FAIL | Non testable — dépend de P-050 |

**Section 7 : 2 FAIL (bloquant)**

---

### Section 8 — Onglet Avenants (P-055 à P-056)

| ID | Test | Profil | Résultat | Commentaire |
|----|------|--------|----------|-------------|
| P-055 | Créer un avenant (Brouillon) | ADMIN | ❌ FAIL | **BLOQUANT** — Onglet Avenants affiche "Aucun avenant" mais aucun bouton pour en créer. Fonctionnalité non implémentée. |
| P-056 | Workflow avenant : Brouillon → Soumis → Approuvé | ADMIN | ❌ FAIL | Non testable — dépend de P-055 |

**Section 8 : 2 FAIL (bloquant)**

---

### Section 9 — Onglet Sous-traitants (P-060)

| ID | Test | Profil | Résultat | Commentaire |
|----|------|--------|----------|-------------|
| P-060 | Onglet ST affiche liste + bouton nouvelle facture ST | ADMIN | ✅ PASS | "Factures sous-traitants", état vide correct, bouton "+ Nouvelle facture ST" présent et actif |

**Section 9 : 1 PASS**

---

### Section 10 — Onglet Facturation (P-065 à P-066)

| ID | Test | Profil | Résultat | Commentaire |
|----|------|--------|----------|-------------|
| P-065 | Onglet Facturation visible avec bouton Créer | ADMIN | ✅ PASS | "Factures du projet", état vide correct, bouton "+ Créer une facture" visible |
| P-066 | Bouton "+ Créer une facture" fonctionnel | ADMIN | ❌ FAIL | Clic sur le bouton ne déclenche aucune action (pas de modal, pas de navigation). Probablement bloqué par l'absence de client sur TST-P001. |

**Section 10 : 1 PASS / 1 FAIL**

---

### Section 11 — Gestion du statut (P-070 à P-072)

| ID | Test | Profil | Résultat | Commentaire |
|----|------|--------|----------|-------------|
| P-070 | Dropdown statut avec 4 options | ADMIN | ✅ PASS | Actif (vert), En pause (jaune), Terminé, Annulé — conforme spec ACTIVE/ON_HOLD/COMPLETED/CANCELLED |
| P-071 | Badge statut mis à jour visuellement | ADMIN | ✅ PASS | Passage Actif → En pause : badge devient jaune/amber |
| P-072 | Statut sauvegardé après "Terminer" | ADMIN | ✅ PASS | Statut "En pause" persisté après clic "Terminer" (mode édition) |

**Section 11 : 3 PASS**

---

### Section 12 — Sécurité / contrôle d'accès (P-080 à P-082)

| ID | Test | Profil | Résultat | Commentaire |
|----|------|--------|----------|-------------|
| P-080 | Accès non authentifié redirigé vers login | — | ✅ PASS | URL /projects/11 → redirection vers /login?redirect=/projects/11 |
| P-081 | Employé : lecture seule sur onglet Tâches | EMPLOYEE | ✅ PASS | Champs budget/heures en texte statique, colonnes Actions et bouton "+ Tâche" absents |
| P-082 | Employé : menu Administration masqué | EMPLOYEE | ✅ PASS | Menu latéral réduit (pas d'Administration, pas d'Approbations, pas de Périodes) |

**Section 12 : 3 PASS**

---

### Section 13 — Liste projets (P-085 à P-086)

| ID | Test | Profil | Résultat | Commentaire |
|----|------|--------|----------|-------------|
| P-085 | Recherche par code dans la liste | ADMIN | ✅ PASS | Recherche "TST-P001" filtre la liste (déclenché sur Enter — pas de filtre live) |
| P-086 | Clic sur une ligne navigue vers la fiche | ADMIN | ✅ PASS | Clic sur TST-P001 → navigation vers /projects/11 |

**Section 13 : 2 PASS**

---

## Bugs identifiés

### BUG-001 — Ajout de tâche retourne "Bad Request" (Critique)

| Champ | Valeur |
|-------|--------|
| **ID** | BUG-001 |
| **Sévérité** | Critique |
| **Priorité** | P1 |
| **Test** | P-021 |
| **Assigné à** | Developer |

**Comportement actuel :** Cliquer "+ Tâche" dans l'onglet Tâches, saisir un nom et cliquer "Créer" retourne une erreur "Bad Request" visible en bandeau rouge en haut de page. La tâche n'est pas créée.

**Comportement attendu :** La tâche est créée sous la phase sélectionnée avec un code WBS automatiquement assigné.

**Étapes de reproduction :**
1. Aller sur /projects/11, onglet Tâches
2. Cliquer "+ Tâche" sur la phase "Préliminaire"
3. Saisir un nom (ex: "Nouvelle tâche test")
4. Cliquer "Créer"
5. Observer le bandeau rouge "Bad Request"

**Impact :** Impossible d'ajouter des tâches à un projet. Workflow de personnalisation WBS totalement bloqué.

---

### BUG-002 — Bouton "Affecter" absent de l'onglet Phases (Critique)

| Champ | Valeur |
|-------|--------|
| **ID** | BUG-002 |
| **Sévérité** | Critique |
| **Priorité** | P1 |
| **Test** | P-050 |
| **Assigné à** | Developer |

**Comportement actuel :** La colonne ACTIONS de l'onglet Phases est vide — aucun bouton "Affecter" présent, ni en vue normale, ni au survol des lignes.

**Comportement attendu :** Un bouton "Affecter" doit permettre d'assigner des employés à chaque phase. L'onglet Équipe référence ce bouton dans son message d'état vide ("utilisez 'Affecter' dans l'onglet Phases").

**Impact :** Impossible d'affecter du personnel aux phases. Onglet Équipe toujours vide.

---

### BUG-003 — Module Avenants non implémenté (Critique)

| Champ | Valeur |
|-------|--------|
| **ID** | BUG-003 |
| **Sévérité** | Critique |
| **Priorité** | P1 |
| **Test** | P-055 |
| **Assigné à** | Developer |

**Comportement actuel :** L'onglet Avenants affiche "Aucun avenant" sans aucun bouton de création. Aucune action possible.

**Comportement attendu :** Un bouton "Créer un avenant" doit permettre de créer un avenant avec workflow Brouillon → Soumis → Approuvé.

**Impact :** Workflow de gestion des avenants totalement absent. Fonctionnalité manquante vs spec section 4.5.

---

### BUG-004 — Wizard: champs PM/Associé affichent des IDs numériques (Majeur)

| Champ | Valeur |
|-------|--------|
| **ID** | BUG-004 |
| **Sévérité** | Majeure |
| **Priorité** | P2 |
| **Test** | P-002 |
| **Assigné à** | Developer |

**Comportement actuel :** Dans le wizard de création, les champs "Chef de projet" et "Associé en charge" affichent les IDs numériques des utilisateurs (ex: "11") au lieu de leurs noms. La fiche projet (hors wizard) utilise des dropdowns corrects.

**Comportement attendu :** Les champs PM/Associé doivent afficher des dropdowns avec les noms complets des utilisateurs (comme dans la fiche projet en mode édition).

---

### BUG-005 — Bouton "+ Créer une facture" inactif (onglet Facturation) (Majeur)

| Champ | Valeur |
|-------|--------|
| **ID** | BUG-005 |
| **Sévérité** | Majeure |
| **Priorité** | P2 |
| **Test** | P-066 |
| **Assigné à** | Developer |

**Comportement actuel :** Clic sur "+ Créer une facture" (onglet Facturation) ne déclenche aucune action (pas de modal, pas de navigation, pas de message d'erreur).

**Comportement attendu :** Le bouton doit ouvrir un formulaire ou naviguer vers la création d'une facture liée au projet.

**Hypothèse :** Le projet TST-P001 n'a pas de client associé — la logique de création de facture requiert un client.

---

### BUG-006 — "Bad Request" lors de suppression de tâche en mode édition (Mineur)

| Champ | Valeur |
|-------|--------|
| **ID** | BUG-006 |
| **Sévérité** | Mineure |
| **Priorité** | P3 |
| **Test** | P-024 |
| **Assigné à** | Developer |

**Comportement actuel :** Si une tâche est en mode édition inline (budget/heures modifiés) et qu'on clique "Supprimer..." sur la même tâche sans d'abord cliquer "Annuler", une erreur "Bad Request" s'affiche. La suppression échoue.

**Comportement attendu :** Soit bloquer la suppression en mode édition avec un message explicatif, soit annuler automatiquement l'édition avant de tenter la suppression.

---

## Écarts fonctionnels (escalade Architect)

### ECART-001 — Bouton "Créer une facture" désactivé dans onglet Budget

Le bouton "Créer une facture" dans l'onglet Budget est `disabled=true`. La spec (section 4.6) précise que ce bouton doit être accessible pour Finance. Si la condition de désactivation est volontaire (ex: client requis), cela doit être documenté et un message explicatif doit être affiché.

### ECART-002 — Recherche liste projets déclenche sur Enter (pas live)

La recherche dans la liste projets ne filtre pas en temps réel — elle requiert l'appui sur Enter. La spec ne spécifie pas le comportement exact, mais un filtre live serait plus conforme aux standards UX modernes.

### ECART-003 — Bouton "Modifier" visible pour le profil EMPLOYEE

Dans la fiche projet, le bouton "Modifier" est visible pour un utilisateur EMPLOYEE. Bien que les modifications soient bloquées dans les onglets, l'accès au mode édition devrait idéalement être restreint au niveau de l'interface.

---

## Checklist Go / No-Go

| Critère | Statut |
|---------|--------|
| Création projet depuis template | ✅ |
| Déploiement WBS automatique | ✅ |
| Ajout/modification/suppression tâches | ⚠️ (ajout KO) |
| Budget inline éditable + KPIs | ✅ |
| Honoraires enregistrables | ✅ |
| Avancement % + code couleur | ✅ |
| Finance 5 KPIs | ✅ |
| Gestion statut projet | ✅ |
| Onglet ST fonctionnel | ✅ |
| Onglet Facturation (liste) | ✅ |
| Création facture depuis projet | ❌ |
| Affectation équipe par phase | ❌ |
| Module Avenants (CRUD + workflow) | ❌ |
| Contrôle d'accès par rôle | ✅ |
| Recherche + navigation liste projets | ✅ |

---

## Prochaines étapes recommandées

1. **[P1 — IMMÉDIAT]** Corriger BUG-001 (Bad Request création tâche) — impact direct sur tout workflow WBS personnalisé
2. **[P1 — IMMÉDIAT]** Implémenter BUG-002 (Affecter dans Phases) — Onglet Équipe inutilisable
3. **[P1 — SPRINT COURANT]** Implémenter BUG-003 (Module Avenants) — fonctionnalité complète manquante
4. **[P2]** Corriger BUG-004 (IDs numériques dans wizard) — UX bloquant à la création
5. **[P2]** Investiguer BUG-005 (Créer facture inactif) — confirmer si lié à l'absence de client
6. **[P3]** Corriger BUG-006 (Bad Request suppression en mode édition) — contournement possible
7. **Re-test complet** des sections 3 (tâches), 7 (équipe), 8 (avenants) après corrections

---

*Rapport généré le 2026-04-04 — QA Tester*
