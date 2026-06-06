# Audit `testarch-framework` (lecture seule)

**Date**: 2026-06-06
**Mode**: AUDIT — aucune initialisation/scaffold effectué (à la demande)
**Auteur**: BMad Master (TEA framework, mode audit)

> Ce workflow *initialise* normalement un framework de test. Ici, **audit uniquement** : état du framework existant + recommandations, sans écrire de code.

## Verdict : **Framework DÉJÀ EN PLACE — aucune initialisation requise**

| Couche | Outil | Version | État |
|---|---|---|---|
| Unit / composant (front) | **Vitest** | ^3.0.0 | ✅ 18 specs |
| Rendu composant (front) | **@vue/test-utils** | ^2.4.0 | ✅ installé |
| E2E (front) | **Playwright** | ^1.49.0 | ✅ configuré, 1 spec |
| Unit / intégration (back) | **pytest + factory_boy** | — | ✅ très couvrant |
| Scripts | `test` (vitest), `test:e2e` (playwright) | — | ✅ |

## Config Playwright (`playwright.config.ts`)

Solide pour un MVP :
- `testDir: ./e2e`, projet **chromium**, `webServer` auto (`npm run dev`, port 5173), `reporter: html`.
- CI-aware : `forbidOnly`, `retries: 2` en CI, `workers: 1` en CI, `trace: 'on-first-retry'`.
- Pattern E2E établi : **route interception** (mock API) — cf. `e2e/virtualResources.spec.ts`.

## Findings

| Sév. | Constat | Reco |
|---|---|---|
| ⚠️ Medium | **Doublon de config** : `playwright.config.js` **et** `.ts` (quasi identiques). Playwright charge `.ts` en priorité → le `.js` est mort et prête à confusion. | **Supprimer `playwright.config.js`** (1 fichier mort). |
| ℹ️ Low | Pattern E2E = **mock total des API** (contract-only) → ne détecte pas les régressions backend réelles. | Garder pour la vitesse ; envisager qq E2E « full-stack » sur les flux critiques. |
| ℹ️ Low | 1 seul navigateur (chromium). | Suffisant MVP ; ajouter webkit/firefox plus tard si besoin. |
| ⚠️ Medium | Exécution **CI** de `test:e2e` non confirmée (pas de pipeline détecté côté repo). | Vérifier que la CI lance vitest **et** playwright (sinon les E2E ne gardent rien). |

## Recommandation
**Ne rien initialiser.** Une seule action utile (hors audit) : retirer le `.js` dupliqué. Le framework est prêt à accueillir de nouveaux tests (→ voir l'audit `testarch-automate`).

---
*Audit lecture seule — aucun fichier de test/config modifié.*
