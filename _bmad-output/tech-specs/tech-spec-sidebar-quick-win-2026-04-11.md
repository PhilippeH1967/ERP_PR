---
title: Tech Spec — Sidebar Quick Win (Sprint 1, Proposition A)
project: PR|ERP
sprint: 1
proposition: A
date: 2026-04-11
author: Philippe Haumesser
status: draft
level: 1
duration: 1-2 days
related_brainstorming: _bmad-output/brainstorming/brainstorming-session-2026-04-11-200000.md
related_mockup: _bmad-output/mockups/flux/flux-08-dashboards.html
---

# Tech Spec — Sidebar Quick Win (Sprint 1)

## 1. Problem & Solution

### Problem
Le sidebar actuel de PR|ERP affiche **16 items au même niveau** dans 3 sections plates (Principal / Finance / Gestion). Pour Marie (architecte employée, qui représente **75% des 400 utilisateurs**), 12 de ces 16 items ne la concernent pas. Elle subit un bruit visuel important et doit scanner mentalement chaque item pour trouver les 4 qui lui sont utiles. Le même problème touche les autres rôles spécialisés (PAIE, Proposal Manager, Directeur).

**Diagnostic du brainstorming** : Le menu n'est pas mal pensé — il est trop pensé pour tout le monde à la fois. La solution n'est pas de simplifier, c'est de personnaliser par persona.

### Solution
Refactor frontend du composant `MainLayout.vue` pour produire un sidebar **adaptatif par rôle**, strictement aligné sur le mockup `flux-08-dashboards.html`. Chaque persona ne voit que les sections et items dont il/elle a besoin, avec :
- Sections renommées contextuellement par rôle ("Mes projets" pour Marie, "Gestion de projets" pour PM)
- Préfixes "Mon/Ma" sur les items personnels
- Vocabulaire user-friendly (i18n) — adieu "Period locks", bonjour "Verrouillage paie"
- Section "Référentiels" en bas (zone froide) pour les registres statiques
- Rebranding contextuel léger ("PR | Production", "PR | Paie", "PR | Direction")

**Stratégie :** 100% frontend, 0 changement backend. Quick win immédiat sans risque sur les API.

---

## 2. Requirements

### Fonctionnelles

| ID | Requirement | Critère d'acceptation |
|---|---|---|
| **R1** | Le sidebar doit afficher uniquement les items pour lesquels l'utilisateur a une permission RBAC | Marie (EMPLOYEE) ne voit jamais "Approbations", "Verrouillages paie", "Facturation", "Fournisseurs", "Admin", "Consortiums" |
| **R2** | Les sections doivent être renommées selon le rôle de l'utilisateur courant | Marie voit "Mon travail" + "Mes projets" ; le PM voit "Mon travail" + "Gestion de projets" + "Finance" + "Commercial" |
| **R3** | Les items personnels portent un préfixe "Mon/Ma/Mes" | "Mes feuilles de temps", "Mes congés", "Mes dépenses", "Mes projets" pour les vues filtrées sur self |
| **R4** | Le vocabulaire technique est traduit en langage métier | "Period locks" → "Verrouillage paie", "Approvals" → "À approuver", "Suppliers" → "Fournisseurs ST", "Expenses" → "Notes de frais" |
| **R5** | Les registres (Clients, Fournisseurs, Consortium) sont regroupés sous une section "Référentiels" en bas du sidebar | Section visible uniquement pour les rôles ayant accès aux registres (PM, Finance, Admin, BU Director) |
| **R6** | Le menu Sylvie (PAIE) est ultra-réduit | 4 items maximum : Tableau de bord, À valider (paie), Verrouillage périodes, Aide |
| **R7** | Le menu Marie (EMPLOYEE pur) est ultra-réduit | 4 items maximum : Mon tableau de bord, Mes feuilles de temps, Mes projets, Mes congés (+ Aide) |
| **R8** | Le menu Pierre (BU Director) est minimal | ≤ 6 items, focus sur Portfolio + Approbations + Facturation |
| **R9** | Le menu Proposal Manager est ultra-réduit | 4 items max : Tableau de bord, Propositions, Pipeline (kanban), Convertir → Projet |
| **R10** | Le logo/header de l'app affiche un sous-titre contextuel selon le rôle dominant | "PR \| Production" pour PM/Employé, "PR \| Paie" pour PAIE, "PR \| Direction" pour BU Director, "PR \| Admin" pour Admin, "PR \| Finance" pour Finance |
| **R11** | Aucune régression sur les routes existantes | Tous les router-link continuent de fonctionner. Si un user clique sur un item, il atterrit sur la même vue qu'avant |
| **R12** | Aucune section ne dépasse 6 items au niveau 1 (règle Top 5) | Si un rôle a > 6 items dans une section, on regroupe les moins fréquents sous "Plus..." |

### Hors scope (à reporter au Sprint 2 ou 3)

- ❌ Section "À faire / Aujourd'hui" en tête du sidebar (Sprint 2)
- ❌ Favoris personnalisables par utilisateur (Sprint 2)
- ❌ Recherche universelle ⌘K (Sprint 2)
- ❌ Badges notification fraîcheur (Sprint 2)
- ❌ Indicateurs santé métier sur modules (Sprint 2)
- ❌ Mode App Selector pour multi-casquettes (Sprint 3)
- ❌ Matrice de permissions ABAC (Sprint 3-4)
- ❌ Page admin permissions effectives (Sprint 3-4)
- ❌ Modification des dashboards eux-mêmes (Tech Spec séparé requis)
- ❌ Modification des routes ou de l'API backend
- ❌ Sous-menus déroulants (accordéons) — si nécessaire, indentation visuelle plate

---

## 3. Technical Approach

### Stack
- **Framework :** Vue 3 + Composition API + TypeScript
- **State :** Pinia (lecture seule sur `useAuth`)
- **i18n :** vue-i18n (fichiers `frontend/src/locales/fr.json` et `en.json`)
- **Style :** TailwindCSS + variables CSS custom (déjà en place)
- **Routing :** Vue Router 4 (aucun changement)

### Architecture Overview

Le sidebar actuel est défini dans `MainLayout.vue` via un `computed` `navSections` qui retourne un tableau statique de sections. On va remplacer cette logique par un **service de génération de menu basé sur le rôle**, déporté dans un composable réutilisable.

```
useAuth (currentUser, roles)
       │
       ▼
useSidebarMenu (composable)
       │  - matrice rôle → menu items
       │  - filtrage RBAC
       │  - traduction i18n
       │  - sous-titre contextuel
       ▼
MainLayout.vue (consomme + render)
```

**Flux de données :**
1. `useAuth` expose `currentUser.roles` (array de strings : `['EMPLOYEE']`, `['PM', 'EMPLOYEE']`, etc.)
2. `useSidebarMenu` calcule le rôle dominant + les permissions et retourne :
   - `sections: SidebarSection[]` (sections + items adaptés)
   - `roleSubtitle: string` (ex: "Production")
3. `MainLayout.vue` consomme ces deux valeurs et les rend.

### Nouveau composable : `useSidebarMenu.ts`

```typescript
// frontend/src/shared/composables/useSidebarMenu.ts

import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuth } from './useAuth'

export interface SidebarItem {
  key: string         // i18n key
  path: string        // router path
  icon: string        // emoji or icon
}

export interface SidebarSection {
  label: string       // i18n key
  items: SidebarItem[]
}

// Matrice rôle → configuration sidebar
const ROLE_MENU_MAP: Record<string, {
  subtitle: string
  sections: SidebarSection[]
}> = {
  EMPLOYEE: { /* ... voir section "Matrice détaillée" */ },
  PM: { /* ... */ },
  PROJECT_DIRECTOR: { /* ... */ },
  BU_DIRECTOR: { /* ... */ },
  FINANCE: { /* ... */ },
  PAIE: { /* ... */ },
  DEPT_ASSISTANT: { /* ... */ },
  PROPOSAL_MANAGER: { /* ... */ },
  ADMIN: { /* ... */ },
}

// Priorité des rôles si l'utilisateur en a plusieurs
const ROLE_PRIORITY = ['ADMIN', 'BU_DIRECTOR', 'PROJECT_DIRECTOR', 'FINANCE', 'PAIE', 'PM', 'PROPOSAL_MANAGER', 'DEPT_ASSISTANT', 'EMPLOYEE']

export function useSidebarMenu() {
  const { currentUser } = useAuth()
  const { t } = useI18n()

  const dominantRole = computed(() => {
    const userRoles = currentUser.value?.roles || ['EMPLOYEE']
    for (const r of ROLE_PRIORITY) {
      if (userRoles.includes(r)) return r
    }
    return 'EMPLOYEE'
  })

  const config = computed(() => ROLE_MENU_MAP[dominantRole.value] || ROLE_MENU_MAP.EMPLOYEE)

  return {
    sections: computed(() => config.value.sections),
    roleSubtitle: computed(() => t(`role.subtitle.${config.value.subtitle}`)),
    dominantRole,
  }
}
```

### Matrice détaillée des menus par rôle

#### EMPLOYEE (Marie) — 4 items + Aide
**Sous-titre logo :** "PR | Production"
```
Mon travail
  📊 Mon tableau de bord       /dashboard
  🕐 Mes feuilles de temps     /timesheets
  🏖️ Mes congés               /leaves
  🧾 Mes dépenses              /expenses
Mes projets
  📁 Projets assignés          /projects
Aide
  ❓ Aide                       /help
```

#### PM (Jean-François) — 11 items
**Sous-titre logo :** "PR | Production"
```
Mon travail
  📊 Tableau de bord           /dashboard
  🕐 Mes feuilles de temps     /timesheets
  🏖️ Mes congés               /leaves
  🧾 Mes dépenses              /expenses
Pilotage projets
  📁 Mes projets               /projects
  ✅ À approuver               /approvals
  📅 Planification 2 mois      /planning
Finance projets
  📄 Factures à valider        /billing
  🏭 Factures sous-traitants   /suppliers
Référentiels
  🤝 Clients                   /clients
Aide
  ❓ Aide                       /help
```

#### PROJECT_DIRECTOR (Associé en charge) — 13 items
**Sous-titre logo :** "PR | Direction"
```
Mon travail
  📊 Tableau de bord           /dashboard
  🕐 Mes feuilles de temps     /timesheets
  🏖️ Mes congés               /leaves
  🧾 Mes dépenses              /expenses
Pilotage projets
  📁 Mes projets supervisés    /projects
  ✅ Approbations factures     /approvals
  🧾 Approbations dépenses     /expenses-approval
  📈 Rapports                  /reports
Consortiums
  🏗️ Mes consortiums          /consortiums
  📄 Factures consortium       /consortium-invoices
  🏭 ST consortium             /consortium-suppliers
Référentiels
  🤝 Clients                   /clients
Aide
  ❓ Aide                       /help
```

#### BU_DIRECTOR (Pierre) — 13 items
**Sous-titre logo :** "PR | Direction"
```
Mon travail
  📊 Tableau de bord           /dashboard
  🕐 Mes feuilles de temps     /timesheets
  🏖️ Mes congés               /leaves
  🧾 Mes dépenses              /expenses
Pilotage BU
  📁 Portfolio projets         /projects
  ✅ Approbations              /approvals
  📈 Rapports BU               /reports
Consortiums
  🏗️ Tous les consortiums     /consortiums
  📄 Factures consortium       /consortium-invoices
  🏭 ST consortium             /consortium-suppliers
  💰 Distributions             /consortium-distributions
Référentiels
  🤝 Clients                   /clients
Aide
  ❓ Aide                       /help
```

#### FINANCE (Nathalie) — 17 items
**Sous-titre logo :** "PR | Finance"
```
Mon travail
  📊 Tableau de bord           /dashboard
  🕐 Mes feuilles de temps     /timesheets
  🏖️ Mes congés               /leaves
Production
  ✅ Timesheets à valider      /approvals
  🔒 Verrouillage paie         /period-locks
Finance projets
  📄 Facturation               /billing
  💳 Paiements                 /payments
  🧾 Notes de frais            /expenses
  🏭 Fournisseurs ST           /suppliers
  📈 Rapports                  /reports
Consortiums
  🏗️ Tous les consortiums     /consortiums
  📄 Factures consortium       /consortium-invoices
  🏭 ST consortium             /consortium-suppliers
  💰 Distributions             /consortium-distributions
Imports / Exports Intacct
  📥 Importer depuis Intacct   /intacct/import
  📤 Exporter vers Intacct     /intacct/export
  📋 Historique transferts     /intacct/history
Référentiels
  🤝 Clients                   /clients
Aide
  ❓ Aide                       /help
```
*Note : 17 items au total — exception assumée à la règle Top 5 car le rôle Finance est l'utilisatrice "expert" qui voit le plus de modules. La densité est compensée par un découpage en 6 sections claires (Mon travail / Production / Finance projets / Consortiums / Imports/Exports / Référentiels).*

#### PAIE (Sylvie) — 4 items
**Sous-titre logo :** "PR | Paie"
```
Validation paie
  📊 Tableau de bord           /dashboard
  ✅ À valider                 /approvals
  🔒 Verrouillage périodes     /period-locks
Aide
  ❓ Aide                       /help
```

#### DEPT_ASSISTANT (Sophie) — Variable (mode miroir)
**Sous-titre logo :** "PR | Assistance"

**Comportement Sprint 1 (simplifié, sans ABAC) :** Sophie voit le menu PM par défaut, mais accès limité par les permissions backend existantes. Le mode "miroir" complet sera implémenté en Sprint 3 (ABAC).
```
Mon travail
  📊 Tableau de bord           /dashboard
  🕐 Mes feuilles de temps     /timesheets
  🏖️ Mes congés               /leaves
Assistance
  📁 Projets                   /projects
  ✅ Approbations              /approvals
  📄 Facturation (lecture)     /billing
Délégations
  👥 Mes délégations           /delegations
Aide
  ❓ Aide                       /help
```

#### PROPOSAL_MANAGER — 4 items
**Sous-titre logo :** "PR | Commercial"
```
Commercial
  📊 Tableau de bord           /dashboard
  📋 Propositions              /proposals
  🤝 Clients                   /clients
Aide
  ❓ Aide                       /help
```
*Note : Le module Propositions n'existe pas encore (MVP-1.5). En Sprint 1, ce rôle est traité comme un EMPLOYEE temporairement. Le menu sera activé quand le module sera livré.*

#### ADMIN — 8 items + accès complet via section dédiée
**Sous-titre logo :** "PR | Admin"
```
Mon travail
  📊 Tableau de bord           /dashboard
  🕐 Mes feuilles de temps     /timesheets
Pilotage
  📁 Projets                   /projects
  ✅ Approbations              /approvals
  📅 Planification             /planning
Finance
  📄 Facturation               /billing
  🧾 Notes de frais            /expenses
Référentiels
  🤝 Clients                   /clients
  🏗️ Consortiums              /consortiums
  🏢 Fournisseurs              /suppliers
Administration
  ⚙️ Admin                     /admin
Aide
  ❓ Aide                       /help
```

### Modifications i18n

**Nouveaux libellés à ajouter dans `fr.json` (et en.json) :**

```json
{
  "role": {
    "subtitle": {
      "production": "Production",
      "direction": "Direction",
      "finance": "Finance",
      "paie": "Paie",
      "admin": "Admin",
      "commercial": "Commercial",
      "assistance": "Assistance"
    }
  },
  "sidebar": {
    "section": {
      "my_work": "Mon travail",
      "my_projects": "Mes projets",
      "production": "Production",
      "pilotage": "Pilotage",
      "finance": "Finance",
      "commercial": "Commercial",
      "validation_paie": "Validation paie",
      "assistance": "Assistance",
      "delegations": "Délégations",
      "administration": "Administration",
      "references": "Référentiels",
      "help": "Aide"
    },
    "item": {
      "my_dashboard": "Mon tableau de bord",
      "my_timesheets": "Mes feuilles de temps",
      "my_leaves": "Mes congés",
      "my_expenses": "Mes dépenses",
      "my_projects": "Mes projets",
      "my_delegations": "Mes délégations",
      "assigned_projects": "Projets assignés",
      "to_approve": "À approuver",
      "to_validate": "À valider",
      "period_lock_payroll": "Verrouillage paie",
      "period_lock": "Verrouillage périodes",
      "supplier_invoices": "Fournisseurs ST",
      "expense_reports": "Notes de frais",
      "approval_invoices": "Approbations factures",
      "bu_reports": "Rapports BU",
      "portfolio_projects": "Portfolio projets",
      "billing_readonly": "Facturation (lecture)"
    }
  }
}
```

### Modifications de `MainLayout.vue`

**Avant** (extrait actuel) :
```typescript
const navSections = computed(() => {
  const sections = [
    {
      label: 'nav.main',
      items: [
        { name: 'nav.dashboard', path: '/dashboard', icon: '📊' },
        { name: 'nav.reports', path: '/reports', icon: '📈' },
        // ... 16 items
      ],
    },
    // ...
  ]
  return sections
})
```

**Après :**
```typescript
import { useSidebarMenu } from '@/shared/composables/useSidebarMenu'

const { sections, roleSubtitle } = useSidebarMenu()
// `sections` est déjà filtré par rôle, traduit, et structuré
```

Et dans le template, remplacer `PR | ERP` par `PR | {{ roleSubtitle }}`.

### Tests

**Tests visuels manuels** (5 personas à tester via les comptes seed) :
1. `admin@provencher-roy.com` (Test1234!) → menu ADMIN complet
2. `pm@test.com` → menu PM (8 items)
3. `finance@test.com` → menu FINANCE (12 items)
4. `paie@test.com` → menu PAIE (4 items)
5. `employe@test.com` → menu EMPLOYEE (5 items)

**Tests automatisés (Vitest)** : nouveau fichier `frontend/src/shared/composables/__tests__/useSidebarMenu.test.ts` qui couvre :
- Sélection du rôle dominant pour user multi-rôles
- Filtrage correct par rôle
- Présence de la section "Aide" pour tous les rôles
- Compteur d'items conforme aux requirements R6, R7, R8, R9
- Sous-titre logo correct par rôle

---

## 4. Implementation Plan

### Stories (4 stories pour 1-2 jours)

#### Story 1 : Composable `useSidebarMenu` + matrice rôles
**Durée :** 4h
**Livrable :**
- Création de `frontend/src/shared/composables/useSidebarMenu.ts` avec :
  - Interface `SidebarItem` et `SidebarSection`
  - Constante `ROLE_MENU_MAP` couvrant les 9 rôles
  - Constante `ROLE_PRIORITY` pour résolution multi-rôles
  - Composable exporté avec `sections`, `roleSubtitle`, `dominantRole`
- Tests unitaires Vitest

#### Story 2 : i18n des nouveaux libellés
**Durée :** 1h
**Livrable :**
- Mise à jour de `frontend/src/locales/fr.json` avec les clés `role.subtitle.*`, `sidebar.section.*`, `sidebar.item.*`
- Mise à jour de `frontend/src/locales/en.json` avec les traductions anglaises
- Validation : tous les `t()` du composable retournent des chaînes non vides

#### Story 3 : Refactor `MainLayout.vue`
**Durée :** 3h
**Livrable :**
- Remplacement du `navSections` statique par l'appel à `useSidebarMenu()`
- Mise à jour du template pour utiliser `sections` et `roleSubtitle`
- Affichage du sous-titre logo dynamique
- Suppression de la logique conditionnelle obsolète (`canApprove`, `canLockPeriod`, `isUserAdmin`)
- Vérification que tous les router-link continuent de fonctionner

#### Story 4 : Tests visuels et déploiement
**Durée :** 3h
**Livrable :**
- Tests manuels avec les 5 comptes seed (admin, pm, finance, paie, employe)
- Capture d'écran de chaque sidebar pour validation
- Build production (`npm run build-only`) sans erreur
- Commit + push GitHub
- Déploiement Hostinger (`git pull` + `docker compose build vue`)
- Validation post-déploiement sur `https://srv1248490.hstgr.cloud`

### Order d'implémentation
1 → 2 → 3 → 4 (séquentiel, dépendances directes)

---

## 5. Acceptance Criteria

- [ ] Le composable `useSidebarMenu` existe et expose `sections`, `roleSubtitle`, `dominantRole`
- [ ] Marie (`employe@test.com`) voit exactement 5 items (4 + Aide)
- [ ] Sylvie (`paie@test.com`) voit exactement 4 items (3 + Aide)
- [ ] Pierre (BU_DIRECTOR — à créer ou tester via admin) voit ≤ 7 items
- [ ] Jean-François (`pm@test.com`) voit "Mon travail" + "Pilotage" + "Référentiels" + "Aide" comme sections
- [ ] Nathalie (`finance@test.com`) voit "Mon travail" + "Production" + "Finance" + "Référentiels" + "Aide"
- [ ] Tous les items personnels portent le préfixe "Mon/Ma/Mes"
- [ ] Le sous-titre du logo change selon le rôle ("PR | Paie" pour Sylvie, "PR | Production" pour Marie)
- [ ] Les libellés "Period locks" et "Approvals" n'apparaissent plus tels quels — remplacés par "Verrouillage paie" / "À approuver" / "À valider"
- [ ] La section "Référentiels" apparaît en bas du sidebar pour les rôles concernés (PM, FINANCE, BU_DIRECTOR, ADMIN)
- [ ] Aucune route existante n'est cassée (tous les router-link redirigent correctement)
- [ ] Les tests Vitest du composable passent (`npm run test`)
- [ ] Le build Vite passe sans erreur (`npm run build-only`)
- [ ] L'application est déployée sur Hostinger et fonctionne en HTTPS
- [ ] L'utilisateur peut switcher entre les comptes seed et observer le menu changer dynamiquement

---

## 6. Non-Functional Requirements

### Performance
- **NFR-P1 :** Le calcul du menu via `useSidebarMenu` doit être < 5ms (computed Vue, mémoizé)
- **NFR-P2 :** Aucun appel API additionnel — le menu est calculé entièrement côté client à partir de `currentUser.roles`

### Security
- **NFR-S1 :** Le filtrage du menu par rôle est purement visuel — la sécurité réelle reste appliquée par les **route guards** (`frontend/src/router/guards.ts`) et les **permissions backend** (DRF). Si Marie tente d'accéder à `/billing` en tapant l'URL directement, elle reçoit toujours un 403.
- **NFR-S2 :** Aucune information sensible n'est exposée dans le code du composable — uniquement des chemins de routes et des libellés i18n.

### Accessibilité
- **NFR-A1 :** Tous les items de menu conservent leur `aria-label` actuel
- **NFR-A2 :** La navigation au clavier (Tab) reste fonctionnelle

### Compatibilité
- **NFR-C1 :** Pas de breaking change sur les composants enfants de `MainLayout.vue`
- **NFR-C2 :** Les versions FR et EN sont synchronisées dans les fichiers i18n

---

## 7. Dependencies, Risks, Timeline

### Dependencies
- ✅ `useAuth` composable existant qui expose `currentUser.roles`
- ✅ Vue Router déjà configuré avec toutes les routes
- ✅ vue-i18n configuré et opérationnel
- ✅ Comptes de test seed disponibles (5 rôles couverts)
- ⚠️ Pas de compte seed pour BU_DIRECTOR — à créer manuellement ou ajouter à `seed_test_users` (déjà fait dans `seed_test_users.py` !)
- ⚠️ Pas de compte pour DEPT_ASSISTANT — déjà dans `seed_test_users.py`
- ⚠️ Pas de compte pour PROPOSAL_MANAGER — à ajouter si on veut le tester (optionnel pour Sprint 1)

### Risks

| Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|
| **Casser un router-link** | Faible | Moyen | Tester chaque route avec chaque persona avant déploiement |
| **Oubli d'un libellé i18n** | Moyenne | Faible | Lint i18n + tests Vitest qui vérifient `t()` ne retourne pas la clé brute |
| **Confusion des utilisateurs habitués à l'ancien menu** | Moyenne | Faible | Préparer un changelog visible dans l'app + email aux 8 utilisateurs de test |
| **Incompatibilité avec une feature future (favoris, ABAC)** | Faible | Moyen | Architecturer le composable de manière extensible (matrice = source de vérité unique) |
| **Régression sur la délégation (DEPT_ASSISTANT)** | Moyenne | Moyen | Sprint 1 livre une version simplifiée de Sophie ; le mode miroir complet est explicitement reporté au Sprint 3 |

### Timeline
- **Démarrage :** Immédiat (post-validation de ce tech spec)
- **Story 1 (composable) :** Jour 1 matin (4h)
- **Story 2 (i18n) :** Jour 1 après-midi (1h)
- **Story 3 (MainLayout) :** Jour 1 après-midi (3h)
- **Story 4 (tests + déploiement) :** Jour 2 matin (3h)
- **Total :** ~11h de dev = **1.5 jour ouvré**
- **Cible de livraison :** **2026-04-13**

### Milestones
- **M1 (J1, midi) :** Composable + tests verts
- **M2 (J1, fin) :** MainLayout refactoré, build Vite OK
- **M3 (J2, midi) :** Déployé sur Hostinger, validation visuelle 5 personas

---

## 8. Success Metrics (post-deployment)

À mesurer après 1 semaine d'usage en prod :

1. **Réduction du nombre moyen d'items visibles par session utilisateur** :
   - Baseline actuelle : 16 items (tous rôles confondus)
   - Cible : ≤ 8 items en moyenne pondérée
2. **Satisfaction qualitative** : feedback informel des 5 testeurs initiaux ("Le menu est-il plus clair ?")
3. **Aucun ticket support** lié à "je ne trouve plus X" dans les 7 jours suivant le déploiement
4. **Aucun rollback** nécessaire

---

## 9. Next Steps After This Sprint

Une fois Sprint 1 livré et validé, deux suites possibles :
- **Sprint 2 (Proposition B) :** Smart Adaptive UX — section "À faire" en tête, favoris, ⌘K, badges
- **Sprint 3-4 (Proposition C) :** Full ABAC — matrice de permissions admin, mode miroir Sophie

Voir le brainstorming source pour la roadmap complète : `_bmad-output/brainstorming/brainstorming-session-2026-04-11-200000.md`

---

## 10. Sign-off

| Rôle | Nom | Date | Statut |
|---|---|---|---|
| Product Owner | Philippe Haumesser | 2026-04-11 | À valider |
| Tech Lead | Philippe Haumesser | 2026-04-11 | À valider |

**Prochaine étape :** Validation par Philippe → bascule vers le Sprint 1 Story 1 (`bmad-bmm-create-story` ou implémentation directe).
