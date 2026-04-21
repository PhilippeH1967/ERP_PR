# Sprints — Module Projets Finalization (Epic 12 MVP-1)

**Série sprints** : `MP-FINAL-2026-04` → `MP-FINAL-2026-05` → …
**Date création** : 2026-04-21
**Scrum Master / PM** : Philippe + BMad Master (bmad-master agent)
**Input** : [module-projets.md §9](../planning-artifacts/module-projets.md#9-chantiers-à-finaliser-module-projets) + audit réalité vs PRD/epics

## 🎯 Objectif global

**Consolider le module Projets : tests ≥85%, avenants UX validés, Finance connecté (rentabilité + cash flow + paiements ST), dette WBSElement retirée, temps-réel NFR32 (MVP-1) — avant d'ouvrir de nouveaux chantiers.**

> **Décisions Philippe 2026-04-21** :
> - Epic 12 **bascule MVP-1.5 → MVP-1**
> - Epic 16 (Consortium) **reporté** — non prévu pour cette série de sprints
> - Ordre : **12.2 tests en premier** (pas 12.1), pour protéger contre régressions
> - **Git commit après chaque story** (convention repo)
> - **Déploiement Hostinger en batch final** (après que les 5 stories soient mergées main)

---

## 📦 Backlog — 5 stories renumérotées (Epic 12)

L'ancien 12-1 (contract-amendments backlog) est **fusionné** dans le nouveau 12-1 (UX functional validation). Les anciens 12-2/3/4 (rebaseline, reopening, consortium flag) sont **repoussés en 12-6/7/8** (hors scope série de sprints actuelle).

| # | Story | Taille | Focus | Fichier |
|---|---|---|---|---|
| **1** | **12.2** Tests `apps/projects/` ≥ 85% | L (3-5 j) | Backend | [12-2-projects-app-test-coverage.md](12-2-projects-app-test-coverage.md) |
| **2** | **12.1** Avenants UX validation (phases/Gantt/facturation dédiée) | L (4-6 j) | Full-stack | [12-1-amendment-ux-functional-validation.md](12-1-amendment-ux-functional-validation.md) |
| **3** | **12.4** Nettoyage WBSElement deprecated (B2) | M (2-3 j) | Backend + Frontend | [12-4-wbselement-deprecation-cleanup.md](12-4-wbselement-deprecation-cleanup.md) |
| **4** | **12.3** Finance tab — données réelles + cashflow + ST payments | L (4-6 j) | Full-stack | [12-3-finance-tab-real-data.md](12-3-finance-tab-real-data.md) |
| **5** | **12.5** Dashboard temps réel + presence (NFR32 MVP-1) | XL (6-9 j) | Full-stack + infra | [12-5-realtime-dashboard-presence-nfr32.md](12-5-realtime-dashboard-presence-nfr32.md) |

**Effort total estimé** : 19-29 jours-dev.

---

## 🗓️ Découpage multi-sprints (décision Philippe 2026-04-21)

> **Principe** : sprint court (≤ 2 semaines), 1 finalité claire par sprint, gates atteints à 100% avant de passer au suivant.

### Sprint A — `MP-FINAL-2026-04-A` : Fondations qualité + Avenants
**Finalité** : tests solides + Epic 12 Avenants fonctionnellement validé.

| Story | Effort | Gate de sortie |
|---|---|---|
| **12.2** Tests ≥85% | 3-5 j | `pytest --cov=apps.projects ≥ 85%`, CI fail-under configuré |
| **12.1** Avenants UX | 4-6 j | Création/approbation/Gantt/facturation dédiée validés sur branche |

**Durée estimée** : 7-11 j.
**Sortie** : main a un filet de tests sur `apps/projects/` et un workflow Avenants complet.

### Sprint B — `MP-FINAL-2026-05-A` : Dette + Finance réel
**Finalité** : WBSElement retiré, onglet Finance connecté aux vraies données (rentabilité + cash flow + décisions paiements ST).

| Story | Effort | Gate de sortie |
|---|---|---|
| **12.4** WBSElement cleanup | 2-3 j | `grep -r WBSElement apps/` renvoie 0 résultat ; tests verts |
| **12.3** Finance données réelles | 4-6 j | KPI rentabilité + cashflow + tableau ST payments fonctionnels |

**Durée estimée** : 6-9 j.
**Sortie** : code projet nettoyé + Finance utilisable en démo.

### Sprint C — `MP-FINAL-2026-05-B` : Temps réel NFR32
**Finalité** : Dashboard + presence indicator fonctionnels (infra ASGI + Channels).

| Story | Effort | Gate de sortie |
|---|---|---|
| **12.5** NFR32 MVP-1 | 6-9 j | WebSocket auth OK ; dashboard real-time ; presence badge sur invoice prep + budget projet ; nginx upgrade `/ws/` OK en staging Hostinger |

**Durée estimée** : 6-9 j.
**Sortie** : Epic 12 fully done — prêt pour batch deploy Hostinger.

### 🚀 Batch déploiement Hostinger (post-sprint C)

**Après la merge main des 5 stories**, un **unique déploiement Hostinger** bascule tout :
- `git pull origin main` sur VPS
- Migrations DB (avec backfill WBSElement déjà exécuté en staging préalable)
- Rebuild `django` + `vue` containers
- Vérification nginx `/ws/` + certificat wss
- Tests fumée : login → créer projet → avenant → finance → temps-réel
- **Rollback plan** : tag git `pre-mp-final-2026` pour revert si besoin

---

## 🔗 Dépendances et ordre techniquement correct

```
 12.2 (tests)
    │
    ├─► 12.1 (avenants UX)
    │       │
    │       └─► 12.3 (finance, consomme "contrat courant")
    │
    ├─► 12.4 (WBS cleanup) [peut partir en parallèle après audit]
    │
    └─► 12.5 (NFR32) [démarre après fondations ASGI]
```

- **12.2** est un pré-requis pour **12.1, 12.3, 12.4** : mêmes fichiers touchés.
- **12.1** doit précéder **12.3** : `contrat courant = original + Σ avenants` consommé dans la Finance.
- **12.4** peut démarrer en parallèle de **12.3** **SI** l'audit Phase 3 confirme que l'UI ne dépend plus de `WBSElementViewSet`.
- **12.5** touche peu le code métier projet — démarre après fondations ASGI/nginx prêtes.

---

## 📐 Sizing & Effort (estimation BMAD)

| Story | Taille | Jours-dev estimés* | Risque |
|---|---|---|---|
| 12.2 Tests | L | 3-5 j | 🟢 Bas |
| 12.1 Avenants UX | L | 4-6 j | 🟡 Moyen (UX + facturation + Gantt) |
| 12.4 WBSElement cleanup | M | 2-3 j | 🟡 Moyen (destructif, prudence Hostinger) |
| 12.3 Finance réel | L | 4-6 j | 🟡 Moyen (dépend 12.1, cashflow nouveau) |
| 12.5 NFR32 temps réel | XL | 6-9 j | 🔴 Haut (infra ASGI, nginx, 2 consumers) |
| **Total** | | **19-29 j** | |

_*Claude Code : Sonnet exécute, Opus plane étapes complexes._

---

## 🔀 Workflow Git (convention sprint)

**Décision Philippe** : **un commit par story terminée**, pas de batch intermédiaire.

Pour chaque story :
```bash
# Sur branche main (ou feature/12-X-<slug>)
# Après validation des gates story :
git add <fichiers modifiés précisément listés>
git commit -m "<type>(<scope>): <description>

<Story 12.X réf + changelog court>

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

- **Format** : `<type>(<scope>): <description>` (CLAUDE.md §Conventions de commit)
- **Types** autorisés : `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `perf`
- **Scopes** utiles ici : `projects`, `billing`, `tests`, `api`, `frontend`, `planning`
- **Pas de push remote** tant que Philippe ne confirme pas

---

## 🚦 Gates d'acceptation par story

Story ne bascule `done` que si tous ces gates passent :

### Backend
- [ ] `pytest` passe (nouveaux + régression)
- [ ] `pytest --cov=apps.<app>` ≥ 85% sur le code nouveau
- [ ] `ruff check .` et `ruff format --check .` propres
- [ ] Matrice permissions DRF testée (401/403/200/404 cross-tenant)
- [ ] `assertNumQueries` là où pertinent
- [ ] Migration atomique, `reverse` symétrique si backfill

### Frontend
- [ ] Tests Vitest écrits **avant** le code (TDD — frontend/CLAUDE.md)
- [ ] Charte graphique respectée (composants partagés, variables CSS)
- [ ] Les 10 patterns UX appliqués
- [ ] `npm run type-check` + `npm run lint` + `npm run test:unit` + `npm run test:e2e` passent
- [ ] Validation manuelle sur `npm run dev`

### Documentation
- [ ] `module-projets.md` §9.X mis à jour → ✅ livré avec date
- [ ] `epics.md` Epic concerné mis à jour si applicable
- [ ] `sprint-status.yaml` mis à jour
- [ ] Story `Dev Agent Record` rempli (files, completion notes, change log)
- [ ] **Commit git créé** (convention ci-dessus)

### Déploiement (batch final uniquement — Sprint C + post)
- [ ] Staging Hostinger OK après batch (feuilles de temps, planning, Gantt, facturation, finance, temps-réel non cassés)
- [ ] Philippe valide UX sur Hostinger
- [ ] Migration DB propre (`migrate --plan` inspecté)

---

## 🛡️ Risques multi-sprint & mitigations

| Risque | Prob. | Impact | Mitigation |
|---|---|---|---|
| Régression pendant 12.1/12.3/12.4 sans tests | ⬇️ Bas | ⬇️ Bas | 12.2 en sprint A #1 — neutralisé |
| Migration WBSElement destructive casse prod | Moyenne | Très haut | Tests migration sur dump staging + confirmation Philippe avant `DeleteModel` en Sprint B |
| Passage WSGI → ASGI pour 12.5 déstabilise Hostinger | Moyenne | Haut | Déployer en **batch final** après Sprint C, créneau maintenance annoncé |
| Dépendance 12.3 → 12.1 mal calibrée (contrat courant) | Moyenne | Moyen | Finir 12.1 en Sprint A avant d'attaquer Finance Sprint B |
| Effort XL sur 12.5 explose Sprint C | Moyenne | Haut | Prêt à scinder 12.5 en 12.5a (infra + dashboard) + 12.5b (presence) si débordement |
| Batch deploy Hostinger échoue sur 1 story | Faible | Haut | Tag git pre-batch + plan rollback documenté |

---

## 📋 Définition de "Série de sprints Done"

La série bascule `done` quand :

1. ✅ Les 5 stories Epic 12 ont atteint tous leurs gates
2. ✅ Epic 12 status dans `epics.md` → ✅ validé fonctionnellement (MVP-1)
3. ✅ `module-projets.md` §9 entièrement coché ✅
4. ✅ `sprint-status.yaml` reflète les nouveaux statuts + renumérotation
5. ✅ **5 commits git** (1 par story) sur main
6. ✅ **Batch deploy Hostinger** validé par Philippe (login → créer projet → avenant → finance → temps-réel — aucun crash)
7. ✅ Rétrospective tenue (`/bmad-bmm-retrospective`)

---

## 🔄 Workflow recommandé par story (cycle BMAD)

Pour chaque story, **en mode interactif** :

1. **Opus 4.7** → `/bmad-bmm-create-story` (déjà fait — 5 stories rédigées)
2. **Opus 4.7** → `/bmad-tea-testarch-atdd` — tests d'acceptation avant code
3. **Bascule Sonnet 4.6** (`/model sonnet`) → `/bmad-bmm-dev-story` — implémentation
4. **Opus 4.7** → `/bmad-bmm-code-review` — revue finale
5. **Commit git** (convention sprint)
6. **Sonnet 4.6** → `/bmad-tea-testarch-trace` — traçabilité tests vs AC
7. Merge main + update `sprint-status.yaml`

**Pivot mid-story** : si blocage → `/bmad-bmm-correct-course` (Opus).

---

## 📎 Références

- [module-projets.md](../planning-artifacts/module-projets.md) §9 Chantiers à finaliser
- [epics.md](../planning-artifacts/epics.md) Epic 12 (annoté 2026-04-21 — MVP-1)
- [sprint-status.yaml](sprint-status.yaml) — à mettre à jour après ce plan
- [CLAUDE.md](../../CLAUDE.md) §Workflow BMAD — modèles Opus/Sonnet par phase
- [backend/CLAUDE.md](../../backend/CLAUDE.md) §DoD backend
- [frontend/CLAUDE.md](../../frontend/CLAUDE.md) §DoD frontend + 10 patterns UX
- [.claude/rules/deployment.md](../../.claude/rules/deployment.md) — commandes batch deploy Hostinger
