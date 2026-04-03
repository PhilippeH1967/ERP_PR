---
stepsCompleted: [1, 2, 3, 4]
inputDocuments: []
session_topic: 'Restructuration méthodologie ERP — module-complet vertical'
session_goals: 'Ordre modules, définition complet, dépendances, validation, tests'
selected_approach: 'ai-recommended'
techniques_used: ['five-whys', 'morphological-analysis', 'role-playing']
ideas_generated: ['root-cause-analysis', 'module-blocks', 'wbs-refactoring', 'option-b-architecture', 'role-matrix', 'planning-module', 'leave-module']
context_file: ''
---

# Brainstorming Session Results

**Facilitator:** Philippe Haumesser
**Date:** 2026-04-02 / 2026-04-03
**Durée:** ~90 minutes sur 2 jours

## Session Overview

**Topic:** Restructuration de la méthodologie de développement de l'ERP — passer d'une approche MVP horizontale à une approche module-complet verticale
**Goals:** Ordre de modules prioritaire, définition de "complet", gestion dépendances croisées, processus de validation, intégration tests

---

## Technique 1 : Five Whys — Cause Racine

### Découvertes

**Root Cause #1** : Le MVP-1 ne couvre pas le minimum viable pour remplacer l'existant (ChangePoint)
- Les items reportés au MVP-1.5 sont les raisons du changement elles-mêmes
- Le MVP-1 tel que découpé ne justifie pas la migration

**Root Cause #2** : L'approche horizontale empêche la validation module par module
- Philippe a une vision précise par module mais voit des morceaux incomplets
- Chaque correction repousse autre chose → le MVP se vide de sa substance

**Root Cause #3** : La découverte itérative déforme le périmètre
- Plus Philippe voit le résultat, plus il identifie des trous
- L'existant (ChangePoint) sert de benchmark de complétude

**Conclusion** : Le problème n'est pas la vitesse de développement mais la DÉFINITION DU PÉRIMÈTRE.

---

## Technique 2 : Morphological Analysis — Nouvelle Structure

### 12 Modules identifiés

| # | Module | Description | Dépend de |
|---|--------|-------------|-----------|
| G | Admin/Config | Users, rôles, taxes, BU, positions | — |
| A | Projets | Création → Phases → Tâches → Budget → Équipe → ST → Suivi → Clôture | G, Clients |
| J | Congés/Absences | Banque (import paie mensuel) → Demande → Approbation → Contrôle paie | G |
| L | Planification | Heures/personnel planifiés par projet/tâche vs réels | A |
| B | Feuilles de temps | Saisie par tâche → Approbation PM → Paie → Verrouillage | A, J, L |
| E | Fournisseurs/ST | Organisations → Factures ST → Autorisation → Paiement → Lien projet | A |
| K | Comptes de dépenses | Rapport → Reçus → Lien projet → Approbation → Refacturation client | A |
| C | Facturation | Par tâche depuis projet → Lignes → Workflow → Paiement → Aging | A, B, E, K |
| I | Intégration Intacct | Phase 1: Export CSV. Phase 2: Import. Phase 3: API | C, K, E |
| H | Import/Export | Migration ChangePoint + Import/Export récurrent | Tous |
| F | Dashboard/Rapports | KPI par rôle, rapports financiers, suivi global | Tous |

### 4 Blocs de développement

**BLOC 1 — Le socle (Projets COMPLET)**
- G: Admin/Config (80% fait)
- Clients (fait)
- A: Projets (refonte WBS Option B + templates + budget complet)

**BLOC 2 — Le cycle de production**
- J: Congés/Absences (NOUVEAU — banque, approbation, contrôle paie)
- L: Planification (NOUVEAU — heures/personnel, assistante + PM)
- B: Feuilles de temps (compléter — lien tâche, congés)
- E: Fournisseurs/ST (compléter — mandats, lien projet)

**BLOC 3 — Le cycle financier**
- K: Comptes de dépenses (refonte — lien projet, refacturation)
- C: Facturation (compléter — par tâche, workflow Finance→PM→envoi)
- I: Intégration Intacct Phase 1 (exports CSV)

**BLOC 4 — Pilotage et migration**
- F: Dashboard/Rapports
- H: Import/Export (migration ChangePoint)
- I: Intégration Intacct Phase 2-3 (API)

---

## Technique 2b : Architecture WBS — Décision Option B

### Problème
3 modèles confus : Phase + WBSElement + FinancialPhase

### Structure métier réelle (Provencher Roy)
- Phases standards adaptables (Concept, Préliminaire, Définitif, AO, Surveillance)
- Tâches standards adaptables sous chaque phase (WBS = 3.1, 3.2)
- **Facturation PAR TÂCHE**
- **Feuilles de temps PAR TÂCHE**

### Décision : Option B

```
Phase (conteneur) : "3 — Définitif"
└── Task (facturable, WBS) : "3.1 — Plans architecturaux détaillés"
    ├── budget, billing_mode, taux horaire
    ├── feuilles de temps saisies ICI
    ├── facturation ICI
    └── Sous-tâche (optionnel) : "3.1.1 — Plans RDC"
```

### Templates projet

```
Template "Architecture standard"
├── Phase 1: Concept
│   ├── 1.1 Analyse conditions existantes
│   ├── 1.2 Esquisse et options
│   └── 1.3 Estimation classe D
├── Phase 2: Préliminaire
│   ├── 2.1 Plans préliminaires
│   └── 2.2 Devis préliminaires
├── Phase 3: Définitif
│   ├── 3.1 Plans architecturaux détaillés
│   ├── 3.2 Plans structure et fondations
│   └── 3.3 Plans et devis MEP
├── Phase 4: Appel d'offres
└── Phase 5: Surveillance
```

---

## Technique 3 : Role Playing — Validation

### Matrice des rôles définitive

| Action | Assistante | PM | Finance | Employé | Paie | Directeur |
|--------|:-:|:-:|:-:|:-:|:-:|:-:|
| Créer projet | ✅ | — | — | — | — | — |
| Assigner personnel | ✅ | — | — | — | — | — |
| Planifier heures | ✅ | ✅ | — | — | — | — |
| Saisir heures | — | — | — | ✅ | — | — |
| Valider heures | — | ✅ | — | — | — | — |
| Contrôler paie | — | — | — | — | ✅ | — |
| Préparer facture | — | — | ✅ | — | — | — |
| Valider facture | — | ✅ | — | — | — | ✅ |
| Envoyer facture | — | — | ✅ | — | — | — |
| Demander congé | ✅ | ✅ | ✅ | ✅ | — | ✅ |
| Approuver congé | — | ✅ | — | — | — | ✅ |
| Contrôler congés | — | — | — | — | ✅ | — |

### Workflows validés

**Projet :** Assistante crée (template) → Assigne PM + Associé → Assigne personnel
**Feuille de temps :** Employé saisit par tâche → PM valide → Paie contrôle → Verrouillage
**Facturation :** Finance prépare (par tâche) → PM valide → Finance envoie
**Congés :** Employé demande → PM/Directeur approuve → Paie contrôle règles
**Dépenses :** Employé soumet → PM approuve → Finance approuve → Refacturation si applicable

---

## Décisions clés

| # | Décision | Validé |
|---|----------|--------|
| D1 | Méthodologie module-complet vertical (pas MVP horizontal) | ✅ |
| D2 | Architecture WBS Option B : Phase + Task | ✅ |
| D3 | 12 modules en 4 blocs | ✅ |
| D4 | Templates projet (phases + tâches) | ✅ |
| D5 | Rôles : Assistante crée, Finance facture, PM valide, Paie contrôle | ✅ |
| D6 | Intacct : Export CSV d'abord, API plus tard | ✅ |
| D7 | Module Planification (heures/personnel) | ✅ |
| D8 | Module Congés (banque + approbation + contrôle paie) | ✅ |
| D9 | Facturation par TÂCHE (pas par phase) | ✅ |
| D10 | Feuilles de temps par TÂCHE (pas par phase) | ✅ |

---

## Processus de développement par module

```
1. WORKFLOW  → Tour rapide du workflow avec Philippe
2. SPEC     → Philippe valide le mockup + workflow complet
3. DEV      → Module complet, aucun "plus tard"
4. TESTS    → TDD, écrits AVANT le code
5. VALIDATE → Philippe teste bout en bout
6. FIX      → Corrections AVANT module suivant
7. SIGN-OFF → "Ce module est complet"
8. NEXT     → On ne touche plus (sauf bug critique)
```

---

## Prochaines étapes

1. Tour rapide workflow Bloc 1 (Projets)
2. Tour rapide workflow Bloc 2 (Production)
3. Tour rapide workflow Bloc 3 (Financier)
4. Tour rapide workflow Bloc 4 (Pilotage)
5. Commencer développement Bloc 1 : Refonte WBS Option B
