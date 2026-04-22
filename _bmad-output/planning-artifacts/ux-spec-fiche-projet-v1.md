# UX Design Specification — Fiche Projet (ProjectDetail)

**Auteur :** Philippe Haumesser (facilitation UX : Sally)
**Date :** 2026-04-22
**Version :** 1.0
**Scope :** Refonte ciblée de la fiche projet ERP — frictions Paramètres, Avenants, Architecture d'information
**Statut :** Draft pour revue

---

## 1. Contexte & Problème

### 1.1 Constat

La fiche projet (`ProjectDetail.vue`, ~2350 lignes) est devenue **le cœur fonctionnel** de l'ERP pour les PM et Associés en charge. Depuis les sprints UX 1 et 2 (avril 2026), elle a gagné en richesse (12 onglets, KPIs, Gantt, avenants avec state machine) mais a accumulé plusieurs frictions :

1. **Bouton « ⚙️ Paramètres »** mal nommé, mode édition global bloquant
2. **Avenants** — workflow multi-écrans, budget/périmètre dissociés, état machine invisible
3. **Architecture d'information** — 12 onglets, redondances sémantiques (Budget/Finance/Factures)

### 1.2 Source de vérité UX

Cette refonte doit respecter **[frontend/CLAUDE.md](../../frontend/CLAUDE.md)** §10 patterns UX obligatoires. En particulier :

- Pattern 1 — Mode lecture/édition avec boutons explicites Modifier/Enregistrer/Annuler
- Pattern 2 — Suppression sécurisée inline (pas de `confirm()` natif)
- Pattern 5 — Erreurs backend toujours affichées
- Pattern 7 — Boutons Enregistrer/Annuler cohérents
- Pattern 10 — Dates : date fin ≥ date début

---

## 2. Objectifs & Non-Objectifs

### 2.1 Objectifs mesurables

| # | Objectif | Métrique | Cible |
|---|---|---|---|
| G1 | Réduire les clics pour créer un avenant complet (2 phases + 3 tâches) | Clics mesurés parcours nominal | **−50 %** (de ~18 à ~9) |
| G2 | Rendre le workflow avenant compréhensible sans formation | Taux de compréhension post-test | ≥ 80 % (5 PM testés) |
| G3 | Diminuer la charge cognitive de navigation | Nombre d'onglets racine | **12 → 5** |
| G4 | Aligner la fiche projet sur les 10 patterns UX charte | Audit pattern par pattern | **10/10** (aujourd'hui 6/10) |
| G5 | Pas de régression sur les parcours lecture existants | Temps de consultation Vue d'ensemble | Inchangé ou meilleur |

### 2.2 Non-objectifs (hors scope v1)

- Refonte visuelle complète (tokens, palette) — conservés
- Internationalisation (tous les libellés restent FR pour cette itération)
- Mobile first — la fiche projet reste prioritairement desktop (>1280px)
- Dashboards et rapports transverses — hors fiche projet
- Gantt refonte — récent, considéré OK

---

## 3. Personas ciblés

| Persona | Rôle applicatif | Ce qu'il fait sur la fiche projet | Douleur actuelle |
|---|---|---|---|
| **PM (Aude)** | `PM` | Consulte quotidiennement ; modifie phases/tâches ; crée avenants | 6 clics pour éditer, ne sait pas où ajouter une phase d'avenant |
| **Associé en charge (Jean)** | `PROJECT_DIRECTOR` | Supervise 10+ projets ; valide avenants ; revue budget | Scan difficile avec 12 onglets, workflow avenant opaque |
| **Finance (Claire)** | `FINANCE` | Consulte budgets ; crée factures à partir du projet | Overlap Budget/Finance/Factures prête à confusion |
| **Employé technique (Marc)** | `EMPLOYEE` | Lecture seule (sauf ses propres heures sur onglet Temps) | — peu affecté par cette refonte |

---

## 4. Parcours utilisateurs — Avant / Après

### 4.1 Parcours critique — « Créer un avenant avec 2 phases »

**AVANT (18 clics)**
```
1. Clic « ⚙️ Paramètres »
2. Clic onglet « Avenants »
3. Clic « + Nouvel avenant »
4. Saisir Description
5. Saisir Impact budget
6. Choisir Statut (3 options exposées)
7. Clic « Créer »
8. Clic ▶ pour déplier périmètre
9. Clic « + Nouvelle phase »
10. Saisir nom phase 1, heures, libellé
11. Clic « Ajouter »
12. Clic « + Nouvelle phase » (2e fois)
13. Saisir phase 2
14. Clic « Ajouter »
15. Clic « Soumettre »
16. Basculer onglet Phases pour voir badge
17. Revenir onglet Avenants
18. Clic « Terminer »
```

**APRÈS (9 clics — cible G1)**
```
1. Clic « + Nouvel avenant »                    → ouvre SlideOver DRAFT
2. Saisir Description
3. Clic « + Ajouter phase » (dans SlideOver)
4. Saisir phase 1 (auto-submit sur Enter)
5. Clic « + Ajouter phase »
6. Saisir phase 2
7. (Impact budget auto-calculé, override si forfait)
8. Clic « Soumettre pour approbation »          → stepper passe à SUBMITTED
9. Fermer SlideOver (ou Esc)
```

**Badge AV-X visible immédiatement dans onglets Phases/Tâches** — pas de switch requis car le SlideOver reste ancré à droite.

### 4.2 Parcours critique — « Modifier le nom et la date de fin du projet »

**AVANT (5 clics)**
1. Clic « ⚙️ Paramètres »
2. Onglet « Vue d'ensemble »
3. Clic « Modifier » dans info-card
4. Modifier champs
5. Clic « Enregistrer »
6. Clic « Terminer »

**APRÈS (3 clics)**
1. Onglet « Vue d'ensemble » (par défaut)
2. Clic icône ✏️ à côté du bloc « Informations »
3. Modifier + « Enregistrer » (ou Esc/Annuler)

---

## 5. Architecture de l'information — 12 → 5 onglets

### 5.1 Mapping proposé

| Nouvel onglet | Sous-vue / ancien onglet | Contenu |
|---|---|---|
| **1. Vue d'ensemble** | — | KPIs fusionnés (4 cards), infos projet, client, direction, consortium |
| **2. Structure** | Phases • Tâches • Gantt | 3 sous-onglets internes ; Gantt reste accessible, Phases par défaut |
| **3. Exécution** | Équipe • Temps • Avancement | 3 sous-onglets ; Équipe par défaut |
| **4. Finances** | Budget • Factures • Sous-traitants | 3 sous-onglets ; Budget par défaut |
| **5. Avenants** | — | Autonome (flux d'approbation spécifique) |

### 5.2 Règles

- **Onglet racine = catégorie de travail**, sous-onglet = outil précis
- **Persistance du sous-onglet** dans `sessionStorage` par projet (reprise au même endroit)
- **Badge numérique** sur onglet Avenants (déjà en place) conservé
- **URL routée** : `/projects/:id/structure/phases`, `/projects/:id/executions/temps`, etc. (deep-linking)

### 5.3 Écarts et risques

- L'onglet « Finance » actuel n'a pas été audité — **action préalable requise** : inventaire exact de son contenu. Si redondant avec Budget, le fusionner. Sinon, positionner au bon niveau.
- L'onglet « Avancement » peut doublonner avec Gantt — **audit d'usage** recommandé.

---

## 6. Specifications des composants

### 6.1 Header projet — Refonte

#### 6.1.1 Maquette ASCII

```
┌──────────────────────────────────────────────────────────────────────┐
│ 📁 PR-2026-042 — Tour Résidentielle Centre-Ville              ⋮     │
│    Client Acme Immo • BU Québec • 2026-01-15 → 2026-12-31            │
│    [Actif ▾]  [Privé]  [Consortium — Mandataire 60%]                │
└──────────────────────────────────────────────────────────────────────┘
```

#### 6.1.2 Changements

| Élément | Avant | Après |
|---|---|---|
| Bouton principal | `⚙️ Paramètres` (active isEditing) | **Suppression** |
| Menu Actions | — | **`⋮`** en haut à droite ouvrant un menu : *Archiver, Dupliquer, Exporter PDF, Supprimer* |
| Statut | Badge cliquable uniquement en mode édition | **Toujours cliquable si `canEdit`** (dropdown avec transitions valides) |
| Bouton Supprimer | Caché tant que `isEditing`, puis `btn-danger` exposé | **Déplacé dans menu ⋮ > Supprimer…** (pattern suppression sécurisée) |

#### 6.1.3 Menu ⋮ — spec

```
Actions
├─ 📋 Dupliquer le projet
├─ 📄 Exporter en PDF
├─ 🗄️ Archiver…           (si Actif)
├─ ▶️ Réactiver            (si Archivé)
├─ ───
└─ 🗑️ Supprimer…           (rouge, confirmation inline)
```

- Raccourci clavier `Cmd+K` → CommandPalette existante (Sprint 2) couvre déjà ces actions
- Menu accessible au clavier (flèches, Enter, Esc)

---

### 6.2 Mode édition — Abandon du flag global

#### 6.2.1 Règle centrale

**`isEditing` global supprimé.** Chaque bloc éditable a son propre mode lecture/édition.

#### 6.2.2 Patterns à appliquer

**A. Édition par carte** (Vue d'ensemble → Informations, Direction, Client)

```
┌─ Informations ─────────────────────  ✏️ ─┐
│ Type de contrat   FORFAITAIRE            │
│ Unité d'affaires  Québec                 │
│ Date début        2026-01-15             │
│ Date fin          2026-12-31             │
└──────────────────────────────────────────┘
```

Clic sur ✏️ → carte passe en mode édition avec formulaire et actions `Annuler / Enregistrer`.

**B. Édition inline** (Phases, Tâches — cellule par cellule)

- Déjà en place sur budget/heures des tâches via `saveTaskField`
- **Étendre** aux colonnes Nom, Mode, Phase (sous réserve de validation)
- Raccourci : `Enter` sauvegarde, `Esc` annule, `Tab` passe au champ suivant

**C. Renommer sans `prompt()` natif** — bug actuel [L1324](../../frontend/src/features/projects/views/ProjectDetail.vue#L1324)

Remplacer `promptRename(task.name)` (prompt natif) par :
- Clic sur « Modifier » → cellule Nom passe en `<input>` inline
- Blur ou Enter = save, Esc = annuler

**D. Suppression sécurisée** (pattern déjà en place sur phases/tâches)

- Cohérent ; à étendre au projet (aujourd'hui c'est un banner plein écran — acceptable)

---

### 6.3 AmendmentSlideOver — Composant clé

#### 6.3.1 Wireframe

```
                                        ┌───── SlideOver (width: 520px) ─────┐
                                        │                                    │
 [Onglet Avenants]                      │ AV-3  •  Création avenant     [×] │
 ┌──────────────────────┐               │                                    │
 │ No │ Desc │ $ │ Stat │               │ Workflow                           │
 │────┼──────┼───┼──────┤               │ ● DRAFT — ○ SUBMITTED — ○ APPROV   │
 │ #1 │ ...  │...│ ✅   │               │                                    │
 │ #2 │ ...  │...│ ⏳   │               │ Description *                      │
 │ #3 │ ...  │...│ ✏️   │  ← clic       │ [ Refonte façade sud.............] │
 │────┴──────┴───┴──────│               │                                    │
 │  [+ Nouvel avenant]  │               │ Périmètre                          │
 └──────────────────────┘               │ ┌──────────────────────────────┐   │
                                        │ │ Phases (2)  [+ Ajouter phase]│   │
                                        │ │ • Ph-E: Plans dwg • 40h      │   │
                                        │ │ • Ph-F: Permis • 20h         │   │
                                        │ │                              │   │
                                        │ │ Tâches (3)  [+ Ajouter tâche]│   │
                                        │ │ • T-E.1 Étude sol • 8h       │   │
                                        │ │ • T-E.2 Plan coupe • 16h     │   │
                                        │ │ • T-E.3 Métré • 16h          │   │
                                        │ └──────────────────────────────┘   │
                                        │                                    │
                                        │ Impact budget                      │
                                        │ Calculé automatiquement : 12 500 $ │
                                        │ ☐ Override forfait : [_______] $   │
                                        │                                    │
                                        │ ─────────────────────────────────  │
                                        │ [Annuler]    [Enregistrer brouill] │
                                        │              [Soumettre pour app…] │
                                        └────────────────────────────────────┘
```

#### 6.3.2 Spec comportementale

**Ouverture**
- Clic sur ligne d'avenant existant
- Clic sur `+ Nouvel avenant`
- Tous 2 ouvrent le même composant ; le mode est `create` ou `edit`

**Stepper**
- 4 états : `DRAFT → SUBMITTED → APPROVED | REJECTED`
- Étape en cours : **pleine** (couleur primary)
- Étapes futures : **vides** (gris)
- Étape REJECTED : remplace APPROVED en rouge si rejeté, avec tooltip sur le motif

**Périmètre**
- Sections Phases et Tâches côte à côte
- Clic `+ Ajouter phase` → formulaire inline sous la liste (cohérent avec pattern existant)
- Clic `+ Ajouter tâche` → formulaire inline avec dropdown phase
- Détacher via icône discrète (`🔗✕`) à droite de chaque ligne, **désactivée si avenant APPROVED**

**Impact budget — logique**
```
Calcul auto = Σ (phase.budgeted_hours × taux horaire par défaut)
              + Σ (task.budgeted_hours × task.hourly_rate)
```
- Affiché en lecture seule par défaut
- Checkbox « Override forfait » expose un champ manuel
- Si override, le calcul auto reste visible en note (« Valeur technique : 12 500 $ »)

**Actions contextuelles au statut**

| Statut | Actions disponibles |
|---|---|
| `DRAFT` (créateur = PM) | Enregistrer brouillon • Soumettre pour approbation • Supprimer (confirmation inline) |
| `SUBMITTED` (viewer = PM) | Lecture seule • bouton « Rappeler au brouillon » (si pas encore traité) |
| `SUBMITTED` (viewer = Associé) | Valider • Rejeter (inline, motif obligatoire) |
| `APPROVED` | Lecture seule (lock icon) • Bouton « Voir facture(s) liée(s) » |
| `REJECTED` | Lecture seule + motif rejet • Bouton « Dupliquer en nouveau brouillon » |

**Fermeture**
- Clic `×` ou `Esc`
- Si modifications non sauvegardées → banner discret « Modifications non enregistrées — [Enregistrer] [Annuler] »

#### 6.3.3 API — ce qui existe déjà

Le backend couvre le flux (confirmé par audit code du 21 avril) :
- `POST /projects/<pk>/amendments/` — create DRAFT
- `PATCH .../<id>/` — edit
- `POST .../<id>/submit/` — DRAFT → SUBMITTED
- `POST .../<id>/approve/` — SUBMITTED → APPROVED
- `POST .../<id>/reject/` — SUBMITTED → REJECTED + motif
- `GET .../<id>/scope/` — liste phases + tâches
- `GET /projects/<pk>/budget-summary/` — contrat courant
- Phase/Task serializers exposent `amendment` + `amendment_number`

**→ Aucune modif backend requise pour cette refonte.**

---

### 6.4 Vue d'ensemble — Fusion des 2 grilles KPI

#### 6.4.1 Avant
```
┌─ KPI Grid 3 (dashboard) ──────────────────────────┐
│ Utilisation %    Heures     Budget                │
└───────────────────────────────────────────────────┘
┌─ KPI Grid 4 (financier) ──────────────────────────┐
│ Budget total $   Facturé $  Consommé %   Solde $  │
└───────────────────────────────────────────────────┘
```

Problème : « Utilisation % » et « Consommé % » sont la même chose calculée différemment.

#### 6.4.2 Après — 1 seule grille 4 cards

```
┌───────────────────────────────────────────────────┐
│  Budget total      Facturé        Consommé        │
│  150 000 $         95 000 $       63 %            │
│                                                    │
│  Solde restant     Heures         État            │
│  55 000 $          1 250 / 2 000  🟢 Sain         │
└───────────────────────────────────────────────────┘
```

- 6 cards au lieu de 7 (−1 redondance)
- Indicateur santé projet intégré (vert/orange/rouge déjà calculé côté API)
- Unifié visuellement avec l'onglet Équipe (même KPI grid)

---

## 7. Patterns d'interaction transverses

### 7.1 Raccourcis clavier

| Action | Raccourci | Contexte |
|---|---|---|
| Ouvrir CommandPalette | `Cmd+K` / `Ctrl+K` | Global (existe déjà) |
| Passer au sous-onglet suivant | `Tab` dans la barre d'onglets | Focus onglets |
| Fermer SlideOver | `Esc` | SlideOver ouvert |
| Enregistrer inline | `Enter` | Input en édition |
| Annuler édition inline | `Esc` | Input en édition |
| Suivant champ (tableau) | `Tab` | Édition cellule tableau |

### 7.2 Feedback utilisateur

| Action | Feedback |
|---|---|
| Sauvegarde en cours | Spinner 14px à côté du champ, opacité 0.7 |
| Sauvegarde OK | Checkmark vert 1s puis disparaît (pas de toast intrusif) |
| Sauvegarde échec | Bordure rouge sur champ + message sous le champ (pattern 5) |
| Statut avenant change | Toast discret en bas à droite « Avenant AV-3 soumis » |

### 7.3 États vides

Chaque liste doit afficher un état vide actionnable :

| Liste vide | Message + CTA |
|---|---|
| Pas de phases | « Aucune phase — commence par en ajouter une » [+ Ajouter phase] |
| Pas d'avenants | « Aucun avenant — les modifications contractuelles apparaîtront ici » [+ Nouvel avenant] |
| Pas d'équipe | « Aucune affectation — utilise « Affecter » depuis l'onglet Phases » |

---

## 8. Responsive & Accessibilité

### 8.1 Points d'arrêt

| Plage | Comportement fiche projet |
|---|---|
| `≥ 1280px` | Layout complet, SlideOver 520px |
| `1024–1279px` | SlideOver 440px, KPI grid 4 → 2×2 |
| `< 1024px` | Hors scope v1 — bandeau « Optimisé pour tablette/desktop » |

### 8.2 Accessibilité (AA WCAG 2.1)

- **Contraste** : conservé via tokens existants (source [main.css](../../frontend/src/assets/styles/main.css))
- **Focus visible** : tous les boutons, onglets et inputs ont un `:focus-visible` (règle globale déjà présente)
- **ARIA** :
  - `role="tablist"` sur barre d'onglets
  - `aria-selected` sur onglet actif
  - SlideOver : `role="dialog" aria-modal="true"` + trap focus
  - Stepper : `role="progressbar"` + `aria-valuenow`
- **Labels explicites** sur toutes les icônes cliquables (`aria-label="Supprimer"`, `aria-label="Modifier"`, etc.)
- **Navigation clavier** : tous les parcours testables au clavier, ordre de tabulation logique

---

## 9. Design tokens & composants partagés

### 9.1 Réutilisation obligatoire (charte)

| Composant | Source |
|---|---|
| SlideOver | `src/shared/components/SlideOver.vue` — **vérifier existence**, sinon baser sur `PhaseSlideOver.vue` |
| Stepper | **À créer** : `src/shared/components/Stepper.vue` |
| Menu ⋮ | **À créer** ou utiliser un dropdown existant |
| Badge | Classes `.badge`, `.badge-green`, `.badge-red`, `.badge-purple` (déjà en place) |
| Boutons | `.btn-primary`, `.btn-ghost`, `.btn-danger`, `.btn-action` (existants) |

### 9.2 Nouveaux tokens sémantiques (optionnels)

```css
--amendment-draft-color: var(--color-gray-500);
--amendment-submitted-color: var(--color-warning);
--amendment-approved-color: var(--color-success);
--amendment-rejected-color: var(--color-danger);
```

---

## 10. Plan d'implémentation & critères d'acceptation

### 10.1 Sprint A — Quick wins (2 jours)

| Story | Fichier | Critères d'acceptation |
|---|---|---|
| S-A1 Supprimer bouton « ⚙️ Paramètres » + menu ⋮ | `ProjectDetail.vue` | Aucun clic préalable pour voir les actions ⋮ ; menu accessible clavier ; actions identiques à l'existant |
| S-A2 Abandonner `isEditing` global | `ProjectDetail.vue` | Chaque carte/bloc a son toggle local ; tests Vitest sur le pattern |
| S-A3 Remplacer `prompt()` rename tâche | `ProjectDetail.vue` L1324 | Édition inline avec Enter/Esc ; 0 appel à `prompt()` dans le fichier |
| S-A4 Fusionner les 2 KPI grids Overview | `ProjectDetail.vue` L1013-1026 | 1 seule grille `.kpi-grid-6` ; test snapshot ; KPI « Utilisation » retiré |
| S-A5 Retirer dropdown statut à la création d'avenant | `ProjectDetail.vue` L1560 | Nouvel avenant toujours créé en DRAFT ; choix de statut absent du formulaire |

**Tests obligatoires** — ajouter 5 tests E2E Playwright dans `tests/e2e/project-detail.spec.ts` :
- t1. Rename tâche sans `prompt()`
- t2. Menu ⋮ ouvre/ferme + raccourcis clavier
- t3. Édition inline info projet
- t4. Overview KPI grid fusionnée
- t5. Création avenant sans dropdown statut

### 10.2 Sprint B — AmendmentSlideOver (5 jours)

| Story | Fichier | Critères d'acceptation |
|---|---|---|
| S-B1 Composant `AmendmentSlideOver.vue` | nouveau | Props : `projectId`, `amendmentId?` (null = create) ; émet `@close`, `@saved` |
| S-B2 Stepper workflow | nouveau `Stepper.vue` | 4 étapes affichées ; responsive ; accessible |
| S-B3 Intégration périmètre (phases + tâches) | `AmendmentSlideOver.vue` | Utilise API `/scope/` existante ; ajout/détachement optimiste + rollback |
| S-B4 Impact budget auto + override | `AmendmentSlideOver.vue` | Calcul = Σ heures×taux ; toggle override visible |
| S-B5 Actions contextuelles au statut | `AmendmentSlideOver.vue` | Boutons filtrés selon `status` + `currentUser.role` ; tests permissions |
| S-B6 Clic ligne avenant → ouvre SlideOver | `ProjectDetail.vue` | Onglet Avenants devient lecture seule (lignes simples) ; double clic réservé (pas d'inline) |
| S-B7 Remplacer ancien formulaire + expand | `ProjectDetail.vue` | Retrait des 110 lignes actuelles ; ligne de table minimaliste |

**Tests Playwright (critiques)** :
- t6. Parcours complet « Créer avenant + 2 phases + soumettre » ≤ 9 clics
- t7. Associé voit Valider/Rejeter, PM ne les voit pas
- t8. Rejet avec motif obligatoire (erreur si vide)
- t9. APPROVED : pas de boutons Modifier/Détacher
- t10. Esc ferme le SlideOver (avec confirmation si changements non sauvegardés)

### 10.3 Sprint C — Refonte IA onglets (7-10 jours)

Précédé d'un **audit d'usage** (1 sprint court) :
- Ajouter tracking events `tab_view` avec `{tab_name, project_id, user_role, duration}` pendant 2 semaines
- Analyser : quels onglets consultés, combien de temps, par qui
- Décider Finance/Avancement/Factures : fusionner, garder, supprimer

Puis :
| Story | Critères d'acceptation |
|---|---|
| S-C1 Prototype Figma 5 onglets + sous-onglets | Validé par 3 PM + 1 Associé |
| S-C2 Test utilisateur modéré (5 participants) | Taux de réussite parcours avenant > 80 % ; satisfaction > 4/5 |
| S-C3 Implémentation onglets groupés | Routes mises à jour, deep-linking fonctionnel, `sessionStorage` persistance |
| S-C4 Migration visuelle progressive | Feature flag ; rollback possible sous 1h |

---

## 11. Risques & mitigations

| Risque | Impact | Mitigation |
|---|---|---|
| Utilisateurs habitués au mode édition global (Sprint A) | Moyen — re-formation 1 réunion de 30min | Release notes + vidéo courte (2 min) |
| SlideOver sur écrans < 1024px mal géré | Faible — pas d'utilisateur prod en < 1024px à date | Banner responsive + lien vers doc |
| Refonte IA (Sprint C) casse les bookmarks URL | Moyen | Redirections 301 de l'ancienne route vers la nouvelle |
| Calcul auto budget impact diverge du forfait négocié | Élevé pour contrats FORFAITAIRE | Override explicite obligatoire sur `billing_mode=FORFAIT` |
| Performance SlideOver avec beaucoup de phases (>50) | Faible | Virtualisation tableau si > 30 items (composant existant) |

---

## 12. Métriques post-release

À instrumenter côté frontend (PostHog / Plausible) pour valider la refonte :

| Métrique | Source | Cible |
|---|---|---|
| Temps moyen « créer avenant complet » | Event `amendment_created` + timer | Baseline − 50 % |
| Clics médians sur fiche projet / session PM | Event `click` filtré par route | Baseline − 30 % |
| Taux d'avenants en DRAFT > 7 jours | Backend report quotidien | < 10 % |
| Onglets consultés / session (médiane) | Event `tab_view` | 2-3 onglets (vs 4-5 aujourd'hui estimé) |
| Plaintes support liées à la fiche projet | Ticket tag `project-detail` | −60 % |

Revue à **M+1** post-release Sprint B, à **M+3** post-release Sprint C.

---

## 13. Prochaines étapes

1. **Philippe** : revue de cette spec, feedback sur les partis pris (notamment IA 12→5)
2. **Sally** : ajustement spec si besoin
3. **Architecte** (agent BMAD `/bmad-agent-bmm-architect`) : décomposition technique des 3 sprints en user stories
4. **Scrum Master** (agent BMAD `/bmad-agent-bmm-sm`) : sprint backlog + priorisation
5. **Dev + QA** (BMAD `/bmad-bmm-dev-story` + `/bmad-agent-bmm-qa`) : TDD puis revue
6. **Mesure** : instrumenter Sprint A dès la release pour nourrir Sprint B/C

---

*Fin du document. Ce spec est un contrat d'intention — il peut évoluer au gré des retours PM/Associé et des tests utilisateur.*
