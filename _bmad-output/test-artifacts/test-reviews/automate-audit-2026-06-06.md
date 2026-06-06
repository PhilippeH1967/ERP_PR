# Audit `testarch-automate` (lecture seule)

**Date**: 2026-06-06
**Mode**: AUDIT — aucun test généré (à la demande)
**Auteur**: BMad Master (TEA automate, mode audit)

> Ce workflow *génère* normalement des tests d'automatisation. Ici, **audit uniquement** : où en est la couverture automatisée, et quoi automatiser en priorité — **sans écrire de test**.

## État de l'automatisation

| Niveau | Couverture | Détail |
|---|---|---|
| **Backend** (pytest) | ✅ Élevée | projects/planning/time_entries 337 verts, permissions, intégrité, régressions, `assertNumQueries` |
| **Front — unit/logique** (Vitest) | ✅ Bonne (ciblée) | 18 specs ; utils purs testés (`taskStructure`, `ganttHelpers`, formatters, stores…) |
| **Front — rendu composant** (Vue Test Utils) | ⚠️ Faible | composants montés peu testés (gros monolithes) |
| **E2E** (Playwright) | ❌ Très faible | **1 seule** spec (`virtualResources`) |

## Le trou : les flux critiques v1.2 ne sont pas automatisés end-to-end

La refonte d'hier a ajouté des **tests unitaires** (logique) mais **aucun E2E / rendu** sur les parcours suivants :

1. **Création de projet → héritage des phases standard** (wizard sans budget).
2. **Saisie de temps par tâche** : picker = feuilles uniquement, tâche obligatoire, refus tâche-mère, unicité.
3. **Gantt / planification** : tâches/sous-tâches visibles, tâche-mère **non cliquable**, **contrôle budget rouge**, barre seulement si dates, phases vides masquées.
4. **Écrans Structure** : Phases lecture seule (admin), Tâches (Déplacer, agrégat), vue d'ensemble (agrégats, KPI heures planifiées).
5. **Paramétrage** : *Administration › Phases standard* (admin-only).

## Plan d'automatisation recommandé (à exécuter hors audit)

> À lancer via `testarch-automate` en **mode écriture** quand tu donneras le feu vert (génère du code de test). Pattern dispo : route interception (cf. spec existante) ou Vue Test Utils + mock store.

| Prio | Cible | Type conseillé | Pourquoi |
|---|---|---|---|
| **P1** | Saisie de temps par tâche (ajout feuille, refus tâche-mère, total semaine) | E2E Playwright (mock API) | Intégrité métier + workflow paie |
| **P1** | Création projet → 8 phases standard héritées | E2E Playwright | Cœur du nouveau modèle |
| **P2** | Gantt : tâche-mère non cliquable + contrôle budget rouge | Vue Test Utils (montage + mock) | Règles métier visibles (logique déjà testée via `ganttHelpers`) |
| **P2** | Structure Tâches : « Déplacer », masquage phases vides | Vue Test Utils | Parcours fréquent PM |
| **P3** | Paramétrage Phases standard (admin) | E2E | Sécurité (admin-only) déjà couverte côté API |

## Atout pour démarrer
Les utils purs (`taskStructure`, `ganttHelpers`) **déjà testés** réduisent le besoin de monter les gros composants : beaucoup de logique est isolée et verte. L'automatisation restante porte surtout sur le **câblage UI ↔ API** (E2E) et quelques **rendus** (Vue Test Utils).

## Estimation (indicative)
- P1 (2 flux E2E) : ~0,5–1 j.
- P2 (2 rendus) : ~0,5 j.
- P3 : ~0,25 j.

---
*Audit lecture seule — aucun test généré. La génération se fera sur ton autorisation explicite.*
