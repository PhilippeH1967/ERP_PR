# Recommandations UX/UI — Application de Gestion pour Cabinets d'Architecture

| Champ | Valeur |
|-------|--------|
| **Document** | UX-REC-001 |
| **Version** | 1.0 |
| **Date** | 2026-02-26 |
| **Auteur** | UX Designer Senior |
| **Statut** | Draft pour validation |
| **Périmètre** | 17 EPICs — EPIC-001 à EPIC-017 |

---

## Table des matières

1. [Vision UX et principes directeurs](#1-vision-ux-et-principes-directeurs)
2. [Architecture de l'information](#2-architecture-de-linformation)
3. [Design System — Fondations](#3-design-system--fondations)
4. [Patterns d'interaction transversaux](#4-patterns-dinteraction-transversaux)
5. [Recommandations par module](#5-recommandations-par-module)
6. [Responsive et adaptation mobile](#6-responsive-et-adaptation-mobile)
7. [Accessibilité (WCAG 2.1 AA)](#7-accessibilité-wcag-21-aa)
8. [Performance perçue](#8-performance-perçue)
9. [Bibliothèque de composants](#9-bibliothèque-de-composants)
10. [Wireframes clés](#10-wireframes-clés)
11. [Checklist UX pour les développeurs](#11-checklist-ux-pour-les-développeurs)
12. [Annexes](#12-annexes)

---

## 1. Vision UX et principes directeurs

### 1.1 Contexte utilisateur

Les utilisateurs cibles sont des professionnels de l'architecture :

| Persona | Rôle | Contexte d'usage | Fréquence | Besoins prioritaires |
|---------|------|-------------------|-----------|---------------------|
| **Directeur d'agence** | Pilotage stratégique | Bureau, iPad | 2-3x/jour, 15 min | KPIs, marges, pipeline |
| **Chef de projet** | Gestion opérationnelle | Bureau, double écran | En continu, 4-6h/jour | Planning, coûts, avancement |
| **Architecte/Collaborateur** | Production | Bureau + déplacement | 2x/jour, 30 min | Saisie temps, tâches, notes |
| **Responsable admin/RH** | Administration | Bureau | 1-2h/jour | Facturation, validation, RH |
| **Commercial** | Développement | Mobile + bureau | Ponctuel | Opportunités, propositions |

### 1.2 Cinq principes fondamentaux

#### Principe 1 — Clarté immédiate
> L'utilisateur sait en < 3 secondes où il est, ce qu'il peut faire et quel est l'état du système.

- **Application** : Titres de page explicites, breadcrumbs, badges de statut colorés, compteurs en temps réel.
- **Anti-pattern à éviter** : Icônes seules sans label, menus cachés, statuts textuels ambigus.

#### Principe 2 — Efficacité de la saisie
> Réduire les frictions de saisie. Chaque clic économisé est du temps gagné × 50 utilisateurs × 250 jours/an.

- **Application** : Auto-complétion, valeurs par défaut intelligentes, copie de semaine précédente, pré-remplissage depuis les données liées.
- **Métrique** : Saisie de temps hebdomadaire en < 5 minutes.

#### Principe 3 — Feedback permanent
> Chaque action a une réponse visible. L'utilisateur ne doute jamais que son action a été prise en compte.

- **Application** : Toast de confirmation, états loading/skeleton, badges en temps réel, transitions animées.
- **Anti-pattern à éviter** : Bouton qui ne réagit pas, sauvegarde silencieuse, changement de statut sans retour visuel.

#### Principe 4 — Cohérence totale
> Un pattern appris dans un module fonctionne identiquement dans tous les autres.

- **Application** : Filtres identiques partout, exports identiques, même positionnement des boutons d'action, mêmes couleurs de statut.
- **Métrique** : 0 exception aux patterns définis dans ce document.

#### Principe 5 — Tolérance à l'erreur
> L'utilisateur peut toujours revenir en arrière. Les actions destructrices sont protégées.

- **Application** : Soft-delete systématique, confirmation modale pour les actions irréversibles, undo sur les actions récentes, brouillons auto-sauvegardés.

### 1.3 Lois UX appliquées

| Loi | Principe | Application concrète dans l'app |
|-----|----------|--------------------------------|
| **Hick** | Plus de choix = plus de temps de décision | Sidebar : max 5 sections principales. Formulaires : champs progressifs. |
| **Fitts** | Cibles grandes = plus rapides à atteindre | Bouton principal : min 44×44px. Zone de clic Kanban : toute la carte. |
| **Miller** | 7±2 éléments en mémoire de travail | KPI cards : max 4-5. Onglets : max 7. Colonnes tableau : max 8-10 visibles. |
| **Jakob** | Les utilisateurs préfèrent le familier | Suivre les conventions SaaS B2B : sidebar gauche, header fixe, modales pour création. |
| **Proximité** | Éléments proches = liés | Grouper actions + données associées. Séparer les sections par espacement. |
| **Pareto** | 80% des usages via 20% des fonctions | Mettre en avant : saisie temps, facturation, planning. Cacher : configuration avancée. |

---

## 2. Architecture de l'information

### 2.1 Navigation principale — Sidebar gauche

```
┌─────────────────────────────────────────────────────────────┐
│ [LOGO]  Nom de l'agence            [▼ Entité]              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  GÉNÉRAL                                                    │
│  ├── 🏠 Tableau de bord          ← EPIC-014                │
│  ├── 🎯 Opportunités   ▸        ← EPIC-001                 │
│  │   ├── Résumé                                             │
│  │   ├── Opportunités                                       │
│  │   └── Propositions                                       │
│  └── 📐 Projets        ▸        ← EPIC-002/003             │
│      ├── Résumé                                             │
│      ├── Projets                                            │
│      └── Carte                                              │
│                                                             │
│  ÉQUIPE                                                     │
│  ├── 👥 Collaborateurs  ▸       ← EPIC-009                  │
│  │   ├── Résumé                                             │
│  │   ├── Collaborateurs                                     │
│  │   ├── Rôles                                              │
│  │   └── Compétences                                        │
│  ├── 📅 Planning        ▸       ← EPIC-006                  │
│  │   ├── Planning                                           │
│  │   ├── Disponibilité                                      │
│  │   └── Statistiques                                       │
│  ├── ⏱️ Temps           ▸       ← EPIC-005                  │
│  │   ├── Résumé                                             │
│  │   ├── Saisie                                             │
│  │   ├── Calendrier                                         │
│  │   ├── Déplacements                                       │
│  │   └── Journaux                                           │
│  ├── 🧾 Notes de frais          ← EPIC-013                  │
│  └── ✅ Validation      ▸       ← EPIC-012                  │
│      ├── Temps                                              │
│      ├── Congés                                             │
│      ├── Notes de frais                                     │
│      └── Factures                                           │
│                                                             │
│  GESTION                                                    │
│  ├── 🏢 Clients                 ← EPIC-010                  │
│  ├── 💰 Coûts           ▸       ← EPIC-007                  │
│  │   ├── Résumé                                             │
│  │   ├── Sous-traitants                                     │
│  │   ├── Salaires                                           │
│  │   ├── Frais généraux                                     │
│  │   └── Exports                                            │
│  ├── 📄 Facturation     ▸       ← EPIC-004                  │
│  │   ├── Résumé                                             │
│  │   ├── Planning                                           │
│  │   ├── Factures                                           │
│  │   ├── Relances                                           │
│  │   ├── Paiements                                          │
│  │   └── Exports                                            │
│  ├── 📊 Finances        ▸       ← EPIC-008                  │
│  │   ├── Résumé                                             │
│  │   ├── Chiffre d'affaires                                 │
│  │   ├── Coûts                                              │
│  │   └── Marge                                              │
│  └── 📈 Rapports        ▸       ← EPIC-011                  │
│      ├── Rapports                                           │
│      └── Planifiés                                          │
│                                                             │
│  COLLABORATION                                              │
│  ├── ✔️ Tâches                   ← EPIC-015                  │
│  ├── 📝 Notes                    ← EPIC-015                  │
│  ├── 📰 Blog                     ← EPIC-015                  │
│  └── 🔔 Notifications           ← EPIC-017                  │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  ⚙️ Configuration               ← EPIC-016                  │
│  👤 Mon profil                                              │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Recommandations structurelles

| Recommandation | Justification | Implémentation |
|----------------|---------------|----------------|
| **Sidebar rétractable** | Gain d'espace sur petit écran | Icônes seules en mode rétracté, tooltip au survol |
| **Sections collapsibles** | Réduction de la charge cognitive (loi de Hick) | Sections GÉNÉRAL/ÉQUIPE/GESTION/COLLABORATION repliables |
| **Badge compteur sur Validation** | Feedback immédiat des éléments en attente | Badge rouge avec chiffre, mise à jour temps réel |
| **Badge compteur sur Notifications** | Alerte visuelle non intrusive | Badge rouge sur la cloche, max 99+ |
| **Sélecteur d'entité** | Multi-agence dans le header | Dropdown en haut de sidebar, filtre tout le contenu |
| **Recherche globale** | Accès rapide cross-module | `Cmd+K` ouvre un champ de recherche avec résultats typés |
| **Raccourcis clavier** | Productivité pour les power users | `Cmd+K` recherche, `N` nouveau, `F` filtres, `E` export |

### 2.3 Header fixe

```
┌──────────────────────────────────────────────────────────────────────┐
│  [☰]  Breadcrumb : Gestion > Facturation > Factures    🔍 Cmd+K    │
│                                                                      │
│                                        [🔔 3]  [👤 Philippe H. ▼]  │
└──────────────────────────────────────────────────────────────────────┘
```

| Élément | Comportement |
|---------|-------------|
| **☰ Hamburger** | Rétracte/déploie la sidebar |
| **Breadcrumb** | Navigation contextuelle, chaque segment cliquable |
| **Recherche Cmd+K** | Ouvre overlay de recherche globale |
| **Cloche** | Ouvre dropdown notifications (EPIC-017), badge temps réel |
| **Avatar** | Menu : Mon profil, Préférences, Déconnexion |

---

## 3. Design System — Fondations

### 3.1 Palette de couleurs

| Rôle | Couleur | Code hex | Usage |
|------|---------|----------|-------|
| **Primaire** | Bleu foncé | `#1E3A5F` | Sidebar, header, boutons principaux |
| **Primaire clair** | Bleu moyen | `#3B82F6` | Liens, icônes actives, focus |
| **Secondaire** | Gris ardoise | `#64748B` | Texte secondaire, icônes inactives |
| **Succès** | Vert | `#22C55E` | Validé, payé, dans les temps, marge positive |
| **Alerte** | Orange | `#F59E0B` | En attente, retard modéré, marge faible |
| **Danger** | Rouge | `#EF4444` | Rejeté, en retard, impayé, marge négative |
| **Info** | Bleu clair | `#3B82F6` | Notifications informatives |
| **Surface** | Blanc | `#FFFFFF` | Fond des cartes et contenus |
| **Background** | Gris très clair | `#F8FAFC` | Fond de page |
| **Bordure** | Gris clair | `#E2E8F0` | Séparateurs, bordures de carte |
| **Texte principal** | Quasi-noir | `#1E293B` | Titres, contenus principaux |
| **Texte secondaire** | Gris moyen | `#94A3B8` | Labels, métadonnées |

### 3.2 Couleurs sémantiques — Statuts

Ces couleurs DOIVENT être identiques dans TOUS les modules :

| Statut | Background | Texte | Modules concernés |
|--------|-----------|-------|-------------------|
| **Brouillon** | `#F1F5F9` | `#64748B` | Factures, Notes de frais, Blog |
| **En attente / Soumis** | `#FFF7ED` | `#EA580C` | Validation, Temps, Congés |
| **Validé / Approuvé** | `#F0FDF4` | `#16A34A` | Temps, Congés, Notes de frais, Factures |
| **Rejeté / Refusé** | `#FEF2F2` | `#DC2626` | Temps, Congés, Notes de frais |
| **Envoyé** | `#EFF6FF` | `#2563EB` | Factures, Propositions |
| **Payé / Remboursé** | `#F0FDF4` | `#16A34A` | Factures, Notes de frais |
| **En retard / Impayé** | `#FEF2F2` | `#DC2626` | Factures, Relances |
| **Annulé / Archivé** | `#F1F5F9` | `#94A3B8` | Tous modules |
| **Actif** | `#F0FDF4` | `#16A34A` | Collaborateurs, Clients, Projets |
| **Inactif** | `#F1F5F9` | `#94A3B8` | Collaborateurs, Clients |

### 3.3 Typographie

| Niveau | Font | Taille | Poids | Line-height | Usage |
|--------|------|--------|-------|-------------|-------|
| **H1** | Inter | 28px | 700 | 36px | Titre de page |
| **H2** | Inter | 22px | 600 | 28px | Titre de section |
| **H3** | Inter | 18px | 600 | 24px | Titre de carte/panneau |
| **H4** | Inter | 16px | 600 | 22px | Sous-titre |
| **Body** | Inter | 14px | 400 | 20px | Contenu principal |
| **Body small** | Inter | 13px | 400 | 18px | Tableaux, métadonnées |
| **Caption** | Inter | 12px | 400 | 16px | Labels, timestamps |
| **Mono** | JetBrains Mono | 13px | 400 | 18px | Références, montants, codes |

**Choix de font** : Inter est gratuite, lisible, optimisée pour les écrans, avec un excellent support des chiffres tabulaires (alignement des colonnes de montants).

### 3.4 Espacement et grille

| Token | Valeur | Usage |
|-------|--------|-------|
| `space-xs` | 4px | Espacement interne dense (badge) |
| `space-sm` | 8px | Espacement entre éléments groupés |
| `space-md` | 16px | Padding standard des cartes |
| `space-lg` | 24px | Espacement entre sections |
| `space-xl` | 32px | Marge entre blocs majeurs |
| `space-2xl` | 48px | Espacement de page |

**Grille** : 12 colonnes, gouttière 24px, marge extérieure 32px.

### 3.5 Élévation et ombres

| Niveau | Box-shadow | Usage |
|--------|-----------|-------|
| **Flat** | Aucune | Contenus inline |
| **Card** | `0 1px 3px rgba(0,0,0,0.1)` | Cartes KPI, tableaux |
| **Elevated** | `0 4px 6px rgba(0,0,0,0.1)` | Dropdowns, popovers |
| **Modal** | `0 10px 25px rgba(0,0,0,0.15)` | Modales, overlays |
| **Tooltip** | `0 2px 8px rgba(0,0,0,0.15)` | Tooltips |

### 3.6 Rayon de bordure

| Token | Valeur | Usage |
|-------|--------|-------|
| `radius-sm` | 4px | Badges, inputs |
| `radius-md` | 8px | Cartes, boutons |
| `radius-lg` | 12px | Modales, panneaux |
| `radius-xl` | 16px | Cards KPI |
| `radius-full` | 50% | Avatars, badges circulaires |

---

## 4. Patterns d'interaction transversaux

### 4.1 Pattern : Dashboard KPI

Utilisé dans : EPIC-001, 004, 005, 006, 007, 008, 009, 014.

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────┐ │
│  │ ↗ 125 000 €  │  │ ⚠ 42 300 €  │  │ ✓ 87%       │  │ 12     │ │
│  │ CA Facturé   │  │ Impayé       │  │ Taux factu.  │  │ Projets│ │
│  │ +12% vs N-1  │  │ 3 en retard  │  │ Objectif 90% │  │ actifs │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └────────┘ │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Spécifications** :

| Propriété | Valeur |
|-----------|--------|
| Nombre max de KPI cards | **4-5** par ligne (loi de Miller) |
| Taille du chiffre principal | **28px, font-weight 700** |
| Label | **13px, couleur secondaire** |
| Tendance/sous-info | **12px, couleur verte/rouge selon positif/négatif** |
| Card padding | **16px** |
| Card border-radius | **12px** |
| Click behavior | Navigue vers la vue détaillée filtrée |
| Hover | Léger assombrissement `background: #F8FAFC` |

**Règle obligatoire** : Chaque KPI card doit avoir une **icône de tendance** (↗ hausse, ↘ baisse, → stable) et une **comparaison** (vs période précédente ou vs objectif).

### 4.2 Pattern : Tableau avec filtres

Utilisé dans : EPIC-001, 004, 005, 006, 007, 009, 010, 011, 012, 013.

```
┌──────────────────────────────────────────────────────────────────────┐
│  Factures                                          [+ Nouvelle] [⋯] │
├──────────────────────────────────────────────────────────────────────┤
│  🔍 Rechercher...   [Statut ▼] [Client ▼] [Période ▼] [+ Filtre]  │
│  Filtres actifs : Statut: Envoyée ✕  |  Période: Fév 2026 ✕        │
├────┬────────────┬──────────┬──────────┬────────┬────────┬───────────┤
│ ☐  │ Référence ▲│ Client   │ Montant  │ Statut │ Échéan.│ Actions   │
├────┼────────────┼──────────┼──────────┼────────┼────────┼───────────┤
│ ☐  │ FAC-2026-  │ ACME     │ 12 500 € │ 🟢 Env│ 15/03  │ [👁] [⋯] │
│    │ 0042       │ Corp     │          │        │        │           │
├────┼────────────┼──────────┼──────────┼────────┼────────┼───────────┤
│ ☐  │ FAC-2026-  │ Martin   │  8 200 € │ 🔴 Ret│ 01/02  │ [👁] [⋯] │
│    │ 0038       │ SA       │          │        │        │           │
├────┴────────────┴──────────┴──────────┴────────┴────────┴───────────┤
│  Affichage 1-25 sur 142    [◀ 1 2 3 4 5 ... 6 ▶]   [25 ▼] par page│
└──────────────────────────────────────────────────────────────────────┘
```

**Spécifications obligatoires** :

| Composant | Spécification |
|-----------|---------------|
| **Barre de recherche** | Pleine largeur, recherche sur tous les champs texte, debounce 300ms |
| **Filtres dropdown** | Max 4 visibles + bouton "Plus de filtres" pour les autres |
| **Filtres actifs** | Badges sous la barre, chaque badge avec bouton ✕ pour retirer |
| **Tri** | Click sur header de colonne, indicateur ▲/▼, tri multi-colonnes shift+click |
| **Pagination** | En bas, sélecteur 10/25/50/100 par page, navigation pages |
| **Checkbox** | Colonne gauche, "Sélectionner tout" en header, actions bulk en barre flottante |
| **Actions par ligne** | Icône œil (voir), menu ⋯ (éditer, dupliquer, supprimer, exporter) |
| **Ligne hover** | Background `#F8FAFC` |
| **Ligne sélectionnée** | Background `#EFF6FF` |
| **Colonnes montants** | Alignées à droite, font mono, séparateur de milliers |
| **Colonnes dates** | Format `JJ/MM/AAAA` ou relatif ("il y a 3j") |
| **Colonnes statut** | Badge coloré selon la palette sémantique |
| **État vide** | Illustration + texte + CTA "Créer ma première facture" |
| **État loading** | Skeleton (12 lignes grisées animées) |

**Barre d'actions bulk** (apparaît quand ≥1 ligne sélectionnée) :

```
┌──────────────────────────────────────────────────────────────────────┐
│  3 éléments sélectionnés   [Valider] [Exporter] [Supprimer] [✕]    │
└──────────────────────────────────────────────────────────────────────┘
```

- Position : fixed en bas de page
- Fond : `#1E293B` (dark), texte blanc
- Disparaît quand sélection vide

### 4.3 Pattern : Formulaire de création (Modale)

Utilisé dans : EPIC-001, 003, 004, 005, 009, 010, 013.

```
┌──────────────────────────────────────────────────────┐
│  Nouvelle facture                              [✕]   │
├──────────────────────────────────────────────────────┤
│                                                      │
│  Projet *                                            │
│  ┌────────────────────────────────────────────────┐ │
│  │ 🔍 Rechercher un projet...                     │ │
│  └────────────────────────────────────────────────┘ │
│                                                      │
│  Client                                              │
│  ┌────────────────────────────────────────────────┐ │
│  │ Auto-rempli depuis le projet                   │ │
│  └────────────────────────────────────────────────┘ │
│                                                      │
│  Phase *                 Date d'émission *           │
│  ┌──────────────────┐   ┌──────────────────────┐   │
│  │ ESQ - Esquisse ▼ │   │ 26/02/2026      📅  │   │
│  └──────────────────┘   └──────────────────────┘   │
│                                                      │
│  Montant HT *            TVA                         │
│  ┌──────────────────┐   ┌──────────────────────┐   │
│  │ 12 500,00     €  │   │ 20%              ▼   │   │
│  └──────────────────┘   └──────────────────────┘   │
│                                                      │
│  Montant TTC (calculé)                               │
│  15 000,00 €                                         │
│                                                      │
│  ─────────────────────────────────────────────────── │
│                                                      │
│            [Annuler]          [Créer la facture]      │
│                                                      │
└──────────────────────────────────────────────────────┘
```

**Spécifications obligatoires** :

| Règle | Justification |
|-------|---------------|
| Labels au-dessus des champs | Meilleur scan visuel (étude eye-tracking) |
| 1 champ par ligne (sauf paires logiques) | Lisibilité, compatibilité mobile |
| Champs obligatoires marqués `*` | Convention universelle |
| Auto-remplissage intelligent | Quand on choisit un projet → client auto-rempli |
| Calculs en temps réel | Montant TTC = HT × (1 + TVA) affiché live |
| Bouton principal à droite | Convention SaaS, plus grande cible |
| Bouton secondaire "Annuler" à gauche | Hiérarchie visuelle claire |
| Validation inline | Message d'erreur sous le champ en rouge, dès le blur |
| Taille modale | Max 600px largeur, scroll interne si trop long |
| Overlay | Fond sombre 50% opacité, click extérieur ferme (avec confirmation si modifié) |

### 4.4 Pattern : Vue détail (Fiche)

Utilisé dans : EPIC-001, 002, 004, 009, 010, 015.

```
┌──────────────────────────────────────────────────────────────────────┐
│  ← Retour aux factures                                              │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  FAC-2026-0042                          🟢 Envoyée                   │
│  ACME Corporation — Projet Bureaux      ─────────────────            │
│  Paris                                  Émise le 15/02/2026          │
│                                         Échéance : 15/03/2026        │
│                                                                      │
│  [Enregistrer un paiement] [Envoyer relance] [⋯ Plus]               │
│                                                                      │
├──────────────────────────────────────────────────────────────────────┤
│  [Détails]  [Lignes]  [Paiements]  [Historique]                      │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Contenu de l'onglet actif                                           │
│  ...                                                                 │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

**Spécifications** :

| Élément | Règle |
|---------|-------|
| **Header** | Référence + badge statut + entité liée + dates clés |
| **Actions** | 1-2 boutons principaux + menu "Plus" pour actions secondaires |
| **Onglets** | Max 5-7, horizontal, onglet actif souligné en bleu |
| **Retour** | Lien en haut à gauche, revient à la liste avec les filtres préservés |
| **Édition** | Inline editing (click sur un champ pour le modifier) ou bouton "Modifier" qui bascule en mode édition |

### 4.5 Pattern : Kanban (Drag & Drop)

Utilisé dans : EPIC-001 (Opportunités), EPIC-015 (Tâches).

```
┌──────────────────────────────────────────────────────────────────────┐
│  [Liste]  [Kanban]                  🔍   [Filtres]   [+ Nouveau]    │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Nouveau (4)      │ En cours (7)     │ Gagné (12)    │ Perdu (3)    │
│  ─────────────    │ ─────────────    │ ──────────    │ ──────────   │
│  ┌───────────┐   │ ┌───────────┐   │ ┌──────────┐  │ ┌──────────┐ │
│  │ OPP-0051  │   │ │ OPP-0048  │   │ │ OPP-0045 │  │ │ OPP-0039 │ │
│  │ Bureaux   │   │ │ Logements │   │ │ École    │  │ │ Clinique │ │
│  │ Lyon      │   │ │ Nantes    │   │ │ Lille    │  │ │ Rennes   │ │
│  │           │   │ │           │   │ │          │  │ │          │ │
│  │ ACME Corp │   │ │ Martin SA │   │ │ Mairie   │  │ │ CHU      │ │
│  │ 85 000 €  │   │ │ 120 000 € │   │ │ 95 000 € │  │ │ 45 000 € │ │
│  │ 60%  ●●●○ │   │ │ 80%  ●●●● │   │ │ 100% ✓  │  │ │ 0%  ✕   │ │
│  └───────────┘   │ └───────────┘   │ └──────────┘  │ └──────────┘ │
│  ┌───────────┐   │                  │               │              │
│  │ ...       │   │                  │               │              │
│  └───────────┘   │                  │               │              │
│                   │                  │               │              │
└──────────────────────────────────────────────────────────────────────┘
```

**Spécifications** :

| Propriété | Valeur |
|-----------|--------|
| **Carte** | Min-width 250px, max-width 320px, padding 12px, radius 8px |
| **Drag feedback** | Ombre portée renforcée, opacité 80%, placeholder en pointillés |
| **Drop zone** | Highlight bleu clair de la colonne cible |
| **Compteur** | Nombre d'éléments dans chaque colonne en header |
| **Scroll** | Vertical par colonne, scroll horizontal si > 4 colonnes |
| **Règles de transition** | Certaines transitions interdites → drag refusé avec animation de retour + toast explicatif |
| **Indicateur de progression** | Points ou barre de progression sur chaque carte |

### 4.6 Pattern : Export multi-format

Utilisé dans : EPIC-001, 004, 005, 007, 008, 010, 011.

```
┌──────────────────────────────────────┐
│  Exporter                      [✕]   │
├──────────────────────────────────────┤
│                                      │
│  Format                              │
│  ○ CSV (tableur)                     │
│  ○ Excel (.xlsx)                     │
│  ● PDF                               │
│                                      │
│  Période                             │
│  ┌────────────────────────────────┐ │
│  │ Février 2026              ▼   │ │
│  └────────────────────────────────┘ │
│                                      │
│  ☑ Respecter les filtres actifs      │
│  ☐ Inclure les éléments archivés     │
│                                      │
│  ──────────────────────────────────  │
│  Nom du fichier :                    │
│  Factures_Fev2026_20260226.pdf       │
│                                      │
│         [Annuler]    [Exporter]      │
│                                      │
└──────────────────────────────────────┘
```

**Règles** :
- Formats disponibles : CSV, Excel (.xlsx), PDF
- Nom auto-généré : `[Type]_[Période]_[DateExport].[ext]`
- Les filtres actifs sont respectés par défaut
- Pour les exports > 5 000 lignes : traitement asynchrone + notification quand prêt
- Le PDF utilise le branding de l'agence (logo, couleurs) défini dans EPIC-016

### 4.7 Pattern : Confirmation d'action destructrice

```
┌──────────────────────────────────────────────────────┐
│  ⚠️ Archiver ce collaborateur ?                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│  Martin Dupont sera désactivé et ne pourra plus      │
│  être affecté à de nouveaux projets.                 │
│                                                      │
│  Ses données historiques seront conservées.           │
│  Cette action est réversible.                        │
│                                                      │
│            [Annuler]       [Archiver]                 │
│                                                      │
└──────────────────────────────────────────────────────┘
```

**Règles** :
- Titre : verbe d'action + objet concerné
- Description : conséquences concrètes
- Bouton destructeur : couleur rouge pour suppression, orange pour archive
- Bouton annuler : toujours à gauche
- Pas de "Êtes-vous sûr ?" → décrire ce qui va se passer
- Double confirmation (taper le nom) uniquement pour les suppressions définitives

### 4.8 Pattern : Toast de feedback

| Type | Icône | Couleur | Durée | Position |
|------|-------|---------|-------|----------|
| **Succès** | ✓ | Vert `#22C55E` | 3 secondes, auto-dismiss | En haut à droite |
| **Erreur** | ✕ | Rouge `#EF4444` | Persistant jusqu'au clic | En haut à droite |
| **Info** | ℹ | Bleu `#3B82F6` | 5 secondes | En haut à droite |
| **Warning** | ⚠ | Orange `#F59E0B` | Persistant | En haut à droite |

**Règles** :
- Max 3 toasts empilés (les suivants remplacent les plus anciens)
- Bouton "Annuler" dans le toast succès pour undo (quand applicable)
- Animation : slide-in depuis la droite, fade-out

### 4.9 Pattern : États vides (Empty States)

Chaque module DOIT avoir un état vide défini :

```
┌──────────────────────────────────────────────────────────────────────┐
│                                                                      │
│                     ┌─────────────────────┐                          │
│                     │                     │                          │
│                     │    [Illustration]    │                          │
│                     │                     │                          │
│                     └─────────────────────┘                          │
│                                                                      │
│                  Pas encore de facture                                │
│                                                                      │
│          Créez votre première facture pour                            │
│          commencer à suivre votre facturation.                       │
│                                                                      │
│                  [+ Créer une facture]                                │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

**Règles** :
- Illustration sobre et en rapport avec le module (pas de clip-art)
- Titre court (max 6 mots)
- Description en 1-2 lignes
- CTA principal pour la première action logique
- Ton : encourageant, pas d'accusation ("Aucun résultat trouvé" → "Commencez par...")

### 4.10 Pattern : Skeleton Loading

```
┌──────────────────────────────────────────────────────────────────────┐
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────┐ │
│  │ ░░░░░░░░░░░  │  │ ░░░░░░░░░░░  │  │ ░░░░░░░░░░░  │  │ ░░░░░░ │ │
│  │ ░░░░░░       │  │ ░░░░░░       │  │ ░░░░░░       │  │ ░░░░░░ │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └────────┘ │
├──────────────────────────────────────────────────────────────────────┤
│  ░░░░░░░░░░░  ░░░░░░░░░  ░░░░░░░  ░░░░░░  ░░░░░░  ░░░░░         │
│  ░░░░░░░░░░░  ░░░░░░░░░  ░░░░░░░  ░░░░░░  ░░░░░░  ░░░░░         │
│  ░░░░░░░░░░░  ░░░░░░░░░  ░░░░░░░  ░░░░░░  ░░░░░░  ░░░░░         │
│  ░░░░░░░░░░░  ░░░░░░░░░  ░░░░░░░  ░░░░░░  ░░░░░░  ░░░░░         │
│  ░░░░░░░░░░░  ░░░░░░░░░  ░░░░░░░  ░░░░░░  ░░░░░░  ░░░░░         │
└──────────────────────────────────────────────────────────────────────┘
```

**Règles** :
- Utiliser pour TOUT chargement > 300ms
- Reproduire la structure du contenu attendu (pas un spinner générique)
- Animation : pulse (opacité oscillante) ou shimmer (dégradé qui glisse)
- Le skeleton des KPI cards doit avoir la bonne taille
- Le skeleton du tableau doit avoir le bon nombre de colonnes

---

## 5. Recommandations par module

### 5.1 EPIC-001 — Opportunités

| Écran | Recommandation UX | Priorité |
|-------|-------------------|----------|
| **Résumé** | 4 KPI cards (Actives, Montant pipeline, Taux transfo, CA gagné) + graphe pipeline en entonnoir + top clients | Haute |
| **Liste/Kanban** | Toggle liste/kanban en haut à droite. Mémoriser la dernière vue choisie par utilisateur | Haute |
| **Kanban** | Colonnes = statuts du pipeline. Drag-drop avec règles (pas de retour en arrière "Gagné" → "Nouveau"). Animation de confetti subtile quand une opportunité passe en "Gagné" | Moyenne |
| **Création** | Modale en 1 étape. Auto-ref OPP-XXXX. Champ client avec auto-complétion | Haute |
| **Conversion** | Bouton "Convertir en projet" uniquement visible quand statut = Gagné. Modale de confirmation avec pré-remplissage | Haute |
| **Propositions** | Sous-onglet dans la fiche opportunité. Créer depuis template avec prévisualisation | Moyenne |

**Parcours critique** :
```
Créer opportunité → Qualifier (probabilité) → Créer proposition → Envoyer → Gagner → Convertir en projet
```

**Point d'attention UX** : La probabilité (slider 0-100%) doit s'ajuster automatiquement selon le statut, mais rester éditable manuellement. Feedback visuel : le slider change de couleur (rouge < 30%, orange 30-70%, vert > 70%).

### 5.2 EPIC-002/003 — Projets & Honoraires

| Écran | Recommandation UX | Priorité |
|-------|-------------------|----------|
| **Liste projets** | Vue tableau par défaut. Vue carte (cards avec photo/couleur + KPIs) en alternative. Filtre rapide par statut (pastilles cliquables au-dessus du tableau) | Haute |
| **Fiche projet** | Header persistant avec : nom, référence, client, statut badge, % avancement (barre). Onglets sous le header | Haute |
| **Onglets projet** | Résumé, Honoraires, Planning, Avancement, Facturation, Coûts, Finance, Plus. L'onglet "Plus" regroupe les sous-modules secondaires (Journaux, Fichiers, Notes, Emails, Rapports, Actions) | Haute |
| **Honoraires** | Tableau interactif des phases avec solveur. Édition inline. Totaux auto-calculés en footer | Haute |
| **Avancement** | Slider par phase (0-100%), barre de progression globale agrégée, historique des mises à jour | Moyenne |
| **Paramètres projet** | Sidebar secondaire dans le projet : Détails, Phases, Clients, Membres, Rôles, Facturation | Basse |

**Point d'attention UX** : Le solveur d'honoraires (calcul automatique des montants par phase) doit être visuellement clair. Utiliser un tableau avec colonnes éditables, totaux en gras, et un indicateur "Solveur actif" quand le calcul automatique est en cours.

### 5.3 EPIC-004 — Facturation

| Écran | Recommandation UX | Priorité |
|-------|-------------------|----------|
| **Résumé** | 4 KPI cards : Facturable, Facturé, Impayé (avec barre de progression), En retard (rouge). Graphe CA mensuel. Top 10 clients avec balance | Haute |
| **Planning facturation** | Grille calendrier 12 mois. Chaque cellule = montant planifié, coloré par statut. Drag-drop pour repositionner. Totaux mensuels en footer | Haute |
| **Factures** | Tableau standard avec filtres. Statuts : Brouillon → Envoyée → Payée / En retard. Actions inline : envoyer, relancer, enregistrer paiement | Haute |
| **Création facture** | Modale avec sélection projet/phase → lignes pré-remplies depuis les honoraires. Calcul TVA automatique. Aperçu PDF avant envoi | Haute |
| **Relances** | Vue dédiée : factures impayées triées par ancienneté. Escalade visuelle (Niveau 1, 2, 3 avec couleur croissante). Bouton "Relancer" avec template email pré-rempli | Moyenne |
| **Paiements** | Formulaire rapide : sélectionner facture → montant → date → méthode. Auto-matching suggestion si montant correspond | Moyenne |

**Point d'attention UX** : Le planning facturation sur 12 mois est un écran dense. Utiliser des codes couleur forts et permettre le zoom (clic sur un mois → vue détaillée). Le drag-drop de repositionnement doit avoir un retour visuel clair (fantôme semi-transparent).

### 5.4 EPIC-005 — Temps

| Écran | Recommandation UX | Priorité |
|-------|-------------------|----------|
| **Saisie quotidienne** | Formulaire rapide en haut de page : Projet (autocomplete) → Phase → Durée → Type → Enregistrer. Total du jour affiché en permanence avec alerte < 7h ou > 10h | **Critique** |
| **Grille hebdomadaire** | Tableau : projets en lignes, jours en colonnes. Cellules éditables au clic. Navigation Tab/Enter entre cellules. Totaux par ligne et par colonne. Bouton "Copier semaine précédente" | **Critique** |
| **Calendrier** | Vue mensuelle avec code couleur par jour (vert ≥ 7h, orange 1-7h, rouge 0h, gris congé/férié). Clic sur un jour → sidebar avec détail des entrées | Haute |
| **Navigation semaine** | Flèches ← → pour changer de semaine + affichage "Semaine du 24 au 28 février 2026" | Haute |
| **Timer optionnel** | Bouton Start/Stop discret en haut à droite pour chronomètre. À la pause, propose de créer une entrée de temps | Basse |

**Point d'attention UX** : La saisie de temps est l'écran le plus utilisé quotidiennement. Chaque friction compte ×50 utilisateurs ×250 jours. Optimiser pour la saisie clavier complète (Tab entre champs, Enter pour valider, autocomplete projet en 2-3 caractères). Le feedback de sauvegarde doit être instantané (< 200ms perçu).

### 5.5 EPIC-006 — Planning

| Écran | Recommandation UX | Priorité |
|-------|-------------------|----------|
| **Planning agence** | Grille : collaborateurs en lignes, semaines/mois en colonnes. Cellules colorées par taux d'occupation (vert < 80%, orange 80-100%, rouge > 100%). Toggle collaborateurs/projets | Haute |
| **Affectation** | Drag-drop depuis un panneau latéral de collaborateurs vers une cellule du planning. Modale de détail : projet, phase, heures/semaine, dates | Haute |
| **Disponibilité** | Tableau : collaborateur × période. Colonnes : capacité, absences, net, planifié, disponible. Code couleur sur le solde | Haute |
| **Gantt projet** | Barres horizontales par phase. Drag-resize pour modifier dates. Dépendances en flèches. Zoom : semaine/mois/trimestre. Bouton "Aujourd'hui" | Haute |
| **Jalons** | Losanges sur le Gantt. Statut : À venir (bleu), Atteint (vert), En retard (rouge clignotant). Double-clic pour éditer | Moyenne |
| **Alertes capacité** | Panneau latéral "Alertes" avec liste des sur/sous-capacités. Clic → navigation vers l'affectation problématique | Moyenne |

**Point d'attention UX** : Le planning agence est l'écran le plus dense de l'application. Privilégier un design sobre avec des couleurs uniquement pour les alertes. Le zoom temporel (semaine → mois → trimestre) doit être fluide avec animation de transition. Implémenter un "mini-map" en bas pour les grandes équipes (> 20 personnes).

### 5.6 EPIC-007 — Coûts

| Écran | Recommandation UX | Priorité |
|-------|-------------------|----------|
| **Résumé** | 4 KPI cards : Coûts totaux, Salaires, Sous-traitance, Frais généraux. Pie chart répartition. Évolution mensuelle | Haute |
| **Sous-traitants** | Liste factures sous-traitants avec workflow de validation (Reçue → Validée → Payée). Fiche fournisseur avec historique | Haute |
| **Budget vs réel** | Tableau projet × catégorie avec colonnes Budget / Réel / Écart / %. Barres de progression. Alerte rouge quand écart > 10% | Haute |
| **Frais généraux** | Configuration allocation (prorata temps / prorata CA / fixe). Transparence du calcul : afficher la formule utilisée | Moyenne |
| **Salaires** | Auto-calculé depuis Temps × taux horaire. Lecture seule. Drill-down par collaborateur/projet/phase | Moyenne |

**Point d'attention UX** : Les écrans coûts manipulent beaucoup de chiffres. Utiliser systématiquement le font mono pour les montants, le séparateur de milliers, et l'alignement à droite. Les écarts négatifs en rouge, positifs en vert. Les formules d'allocation doivent être visibles au survol (tooltip avec le calcul).

### 5.7 EPIC-008 — Finances

| Écran | Recommandation UX | Priorité |
|-------|-------------------|----------|
| **Résumé** | Le plus important : graphe barres CA vs Coûts par mois + courbe cumulative de marge en overlay. 4 KPI cards : CA, Coûts, Marge €, Marge %. Tableau projets triés par marge | Haute |
| **Toggle Réalisé/Projeté** | 2 boutons en haut de CHAQUE vue financière. Mode actif visuellement distinct (fond coloré). Transition < 1 seconde. Persiste dans la navigation | **Critique** |
| **Chiffre d'affaires** | Tableau par projet : Planifié / Facturable / Facturé / Encaissé. Indicateurs d'écart entre chaque étape (flèches avec %) | Haute |
| **Marge** | Barres horizontales par projet, triées par marge décroissante. Code couleur : vert ≥ 20%, orange 0-20%, rouge < 0%. Click → fiche projet finance | Haute |

**Point d'attention UX** : Le toggle Réalisé/Projeté est un pattern fondamental. Il doit être visuellement très clair (pas de confusion possible sur le mode actif). Suggestion : fond bleu pour Réalisé, fond orange pour Projeté. Icône différente sur chaque bouton.

### 5.8 EPIC-009 — Collaborateurs & RH

| Écran | Recommandation UX | Priorité |
|-------|-------------------|----------|
| **Liste** | Tableau avec photo avatar, nom, rôle (badge), équipe, projets actifs (compteur), statut. Recherche rapide. Filtre par rôle/équipe/statut | Haute |
| **Fiche collaborateur** | Header : photo (éditable), nom, rôle, statut. Sections en accordéon : Infos perso, Contrat & RH, Projets, Temps (graphe), Compétences (badges) | Haute |
| **Matrice compétences** | Tableau croisé : collaborateurs × compétences. Cellules colorées par niveau (Débutant/Intermédiaire/Avancé/Expert). Filtrable par catégorie de compétence | Moyenne |
| **Rôles & permissions** | Matrice : modules × niveaux de permission. Checkboxes/radio. Changement immédiat avec confirmation | Moyenne |
| **Invitation** | Bouton "Inviter" → modale email → envoi lien d'activation avec token 7 jours | Haute |

**Point d'attention UX** : La fiche collaborateur est un hub d'information. Utiliser des sections en accordéon pour ne pas surcharger. La section "Projets" doit montrer les projets actifs avec lien direct. La section "Temps" doit montrer un mini-graphe des heures du mois en cours.

### 5.9 EPIC-010 — Clients

| Écran | Recommandation UX | Priorité |
|-------|-------------------|----------|
| **Liste clients** | Tableau avec filtre rapide par type (Entreprise/Particulier/Public). Colonne "Balance" avec code couleur (impayé = rouge) | Haute |
| **Fiche client** | Header : nom, type badge, statut. Onglets : Général, Contacts, Projets liés, Financier, Historique | Haute |
| **Contacts** | Sous-section de la fiche. Contact principal marqué par étoile. Ajout inline sans quitter la fiche | Haute |
| **Vue financière** | Dans la fiche : CA cumulé, factures en cours, balance. Mini-graphe évolution. Lien vers relevé de compte | Moyenne |
| **Détection doublons** | À la création : alerte si nom similaire existant (fuzzy match). Permettre de fusionner ou continuer | Moyenne |

### 5.10 EPIC-011 — Rapports

| Écran | Recommandation UX | Priorité |
|-------|-------------------|----------|
| **Bibliothèque** | Grille de cartes par catégorie (Honoraires, Budget, Temps, Facturation, Coûts, Marge, Avancement, Taux d'occupation). Chaque carte avec icône + description courte + bouton "Générer" | Haute |
| **Paramétrage** | Panneau latéral ou modale : période (presets + custom), projets (multi-select), collaborateurs, colonnes. Aperçu en temps réel | Haute |
| **Résultat** | Tableau avec graphe optionnel au-dessus. Boutons export (CSV/Excel/PDF) en haut à droite | Haute |
| **Rapports planifiés** | Liste avec fréquence, destinataires, prochain envoi. Toggle actif/inactif. Édition de la configuration | Moyenne |
| **Rapports récents** | Widget "5 derniers rapports" pour accès rapide avec téléchargement direct | Moyenne |

**Point d'attention UX** : Les rapports sont souvent utilisés en urgence (réunion dans 5 min). L'accès doit être rapide : max 3 clics pour générer un rapport avec les paramètres par défaut. Permettre de sauvegarder des "favoris" de configuration.

### 5.11 EPIC-012 — Validation

| Écran | Recommandation UX | Priorité |
|-------|-------------------|----------|
| **Dashboard** | 4 onglets horizontaux : Temps, Congés, Notes de frais, Factures. Chaque onglet avec badge compteur des éléments en attente | **Critique** |
| **Validation temps** | Tableau par collaborateur/semaine. Actions : Valider ✓ / Rejeter ✕ par ligne ou en bulk. Commentaire obligatoire si rejet | **Critique** |
| **Validation congés** | Liste avec calendrier miniature montrant les conflits d'équipe. Solde de congés visible. Bouton approuver/refuser | Haute |
| **Validation notes de frais** | Liste avec aperçu du justificatif intégré (preview image/PDF sans téléchargement). Montant + catégorie + plafond | Haute |
| **Validation factures** | Liste avec aperçu PDF intégré. Workflow multi-niveau si configuré | Moyenne |

**Point d'attention UX** : C'est un écran de productivité pour les managers. Optimiser pour le traitement rapide en série. Raccourcis clavier : `V` = valider, `R` = rejeter, `↓` = suivant. La barre d'actions bulk est essentielle pour traiter 50 entrées de temps en 2 minutes.

### 5.12 EPIC-013 — Notes de frais

| Écran | Recommandation UX | Priorité |
|-------|-------------------|----------|
| **Liste** | Tableau avec statut, date, catégorie, montant, projet. Filtres rapides : Mes notes / Mon équipe. Badge statut coloré | Haute |
| **Création** | Formulaire : catégorie (dropdown illustré avec icônes), date, montant HT, TVA → TTC auto-calculé, projet, justificatif (upload drag-drop) | Haute |
| **Justificatif** | Zone d'upload avec drag-drop + bouton. Aperçu intégré (image zoomable, PDF inline). Multi-fichiers | Haute |
| **Frais kilométriques** | Sous-formulaire : lieu départ → arrivée, distance, aller-retour toggle, barème auto-appliqué. Montant calculé automatiquement | Moyenne |
| **Soumission** | Bouton "Soumettre" verrouille l'édition et notifie le validateur. Statut passe à "Soumise" | Haute |

**Point d'attention UX** : La création de note de frais est souvent faite en mobilité (taxi, restaurant). Le formulaire doit être optimisé mobile : gros boutons, upload photo depuis caméra, calcul automatique. Le basculement HT ↔ TTC doit être bidirectionnel et instantané.

### 5.13 EPIC-014 — Tableau de bord

| Écran | Recommandation UX | Priorité |
|-------|-------------------|----------|
| **Layout** | 2 colonnes : gauche (70%) pour les graphes principaux, droite (30%) pour "À venir" | **Critique** |
| **KPI cards** | Ligne de 4 cards en haut : Facturable HT, Impayé TTC (avec barre progression), Temps enregistré %, Notes personnelles | **Critique** |
| **Synthèse financière** | Graphe ligne : CA + Coûts projetés vs réalisés sur 12 mois. Légende interactive (clic pour show/hide). Tooltip au survol | Haute |
| **Planning projets** | Gantt simplifié : 10 projets les plus proches de leur échéance. Barre de progression colorée. Lien "Voir tous les projets" | Haute |
| **À venir** | Sidebar : jalons, tâches, congés, événements des 2 prochaines semaines. Groupés par jour. Badge de compteur | Haute |
| **Personnalisation** | Bouton œil pour masquer/afficher chaque widget. Préférences sauvegardées par utilisateur | Moyenne |
| **Notes** | Widget texte libre avec auto-save. Édition inline, pas de modale | Moyenne |

**Point d'attention UX** : Le tableau de bord est la page d'accueil. Il doit charger en < 2 secondes. Utiliser le skeleton loading pour chaque widget indépendamment. L'objectif est que le directeur d'agence obtienne sa "photo" quotidienne en < 30 secondes de lecture.

### 5.14 EPIC-015 — Collaboration

| Écran | Recommandation UX | Priorité |
|-------|-------------------|----------|
| **Tâches (liste)** | Tableau avec filtres : projet, assigné, priorité, statut, date. Groupement par projet ou par statut | Haute |
| **Tâches (Kanban)** | 3 colonnes : À faire, En cours, Terminé. Drag-drop. Cards avec titre, assigné (avatar), date, priorité (badge couleur) | Haute |
| **Tâche détail** | Panneau latéral (pas de page entière) : titre éditable, description riche, assigné, dates, priorité, commentaires, fichiers | Haute |
| **Notes** | Éditeur riche (markdown) avec versionnage. Liste de notes avec recherche full-text. Partage entre collaborateurs | Moyenne |
| **Fichiers** | Gestionnaire avec dossiers, upload drag-drop, preview inline (PDF, images), versionnage | Moyenne |
| **Blog** | Éditeur d'articles avec catégories/tags. Workflow : Brouillon → Publié → Archivé. Vue lecteur séparée | Basse |

**Point d'attention UX** : Les tâches doivent s'ouvrir en panneau latéral (slide-over depuis la droite) et non en page entière, pour garder le contexte de la liste/kanban. Le commentaire doit supporter les mentions `@nom` avec notification.

### 5.15 EPIC-016 — Configuration

| Écran | Recommandation UX | Priorité |
|-------|-------------------|----------|
| **Navigation** | Sidebar secondaire à gauche avec les 12 sections de configuration. Jamais plus de 2 niveaux de profondeur | Haute |
| **Profil** | Formulaire classique avec photo, infos, mot de passe, 2FA, langue | Haute |
| **Général (agence)** | Formulaire avec logo upload + aperçu branding en temps réel (prévisualisation miniature d'une facture avec les couleurs choisies) | Haute |
| **Facturation** | Configuration numérotation (preview du format), conditions, mentions légales, template. Chaque section en accordéon | Haute |
| **Temps** | Horaires, jours ouvrés, calendrier des jours fériés (avec import pays), types de temps | Moyenne |
| **Import données** | Wizard en 4 étapes : 1. Sélection type → 2. Upload fichier → 3. Mapping colonnes → 4. Preview + validation → Import. Barre de progression. Rapport d'erreurs détaillé | Haute |
| **Multi-entités** | Arbre hiérarchique des agences. Toggle "Hériter des paramètres parent" par section. Indication visuelle des valeurs héritées vs personnalisées | Moyenne |
| **Modules** | Grille de cartes : chaque module avec toggle on/off, description, dépendances. Alerte si désactivation impacte d'autres modules | Basse |

**Point d'attention UX** : La configuration est rarement visitée mais doit être parfaitement claire. Chaque section doit expliquer ce qu'elle fait (texte d'aide contextuel). L'onboarding initial (wizard 10 étapes pour les nouvelles agences) est critique pour la première impression — chaque étape doit montrer une barre de progression et permettre de passer (skip) avec des valeurs par défaut.

### 5.16 EPIC-017 — Notifications

| Écran | Recommandation UX | Priorité |
|-------|-------------------|----------|
| **Cloche header** | Badge rouge avec compteur (max 99+). Clic ouvre dropdown avec les 20 dernières. "Tout marquer comme lu" en haut | **Critique** |
| **Dropdown** | Notifications anti-chronologiques. Chaque notification : icône type + texte + timestamp relatif ("il y a 3h"). Non-lues en fond `#EFF6FF` | **Critique** |
| **Page complète** | Accessible depuis "Voir toutes les notifications". Filtres : type, lu/non-lu, période. Pagination | Haute |
| **Préférences** | Matrice : type d'événement × canal (In-app / Email). Checkboxes. Regroupé par module source. "Tout activer / Tout désactiver" par ligne et par colonne | Haute |
| **Navigation contextuelle** | Clic sur notification → navigue vers l'entité (projet, facture, temps). Marque comme lu automatiquement | **Critique** |

**Point d'attention UX** : Les notifications doivent être non-intrusives. Le badge suffit — pas de pop-up, pas de son par défaut. La navigation contextuelle (clic → entité) doit être instantanée. Les notifications email doivent être regroupables (ne pas envoyer 10 emails pour 10 temps validés → 1 email de résumé).

---

## 6. Responsive et adaptation mobile

### 6.1 Breakpoints

| Breakpoint | Largeur | Nom | Adaptation |
|-----------|---------|-----|------------|
| **Mobile** | < 768px | `sm` | 1 colonne, sidebar masquée, bottom nav |
| **Tablette** | 768-1024px | `md` | 2 colonnes, sidebar rétractable |
| **Desktop** | 1024-1440px | `lg` | Layout complet, sidebar déployée |
| **Wide** | > 1440px | `xl` | Layout étendu, panneaux latéraux |

### 6.2 Adaptations par module

| Module | Desktop | Tablette | Mobile |
|--------|---------|----------|--------|
| **Tableau de bord** | 2 colonnes + sidebar | 1 colonne + sidebar repliée | Stack vertical |
| **Saisie temps** | Grille hebdo complète | Grille 3 jours visibles + scroll | Saisie quotidienne uniquement |
| **Planning** | Grille complète | Scroll horizontal | Vue liste (pas de grille) |
| **Gantt** | Interactif complet | Lecture seule + zoom | Non disponible (lien vers desktop) |
| **Kanban** | 4+ colonnes | 2-3 colonnes + scroll | 1 colonne avec filtre statut |
| **Tableaux** | Toutes colonnes | Colonnes prioritaires + scroll | Cards empilées (pas de tableau) |
| **Formulaires** | 2 colonnes de champs | 1 colonne | 1 colonne, clavier adapté |
| **Facturation** | Planning 12 mois | Planning 6 mois + scroll | Liste mensuelle |

### 6.3 Règles mobiles

| Règle | Justification |
|-------|---------------|
| Touch targets min 44×44px | Apple HIG / Material Design |
| Pas d'interactions hover-only | Pas de hover sur mobile |
| Clavier adapté au type d'input | `type="number"` pour montants, `type="email"` pour emails, `type="date"` pour dates |
| Bottom navigation 4-5 items | Tableau de bord, Temps, Projets, Notifications, Plus |
| Pull-to-refresh | Sur les listes et dashboards |
| Swipe left pour actions | Supprimer, archiver (avec confirmation) |
| Upload photo depuis caméra | Notes de frais : prise de photo du justificatif |

---

## 7. Accessibilité (WCAG 2.1 AA)

### 7.1 Contrastes

| Élément | Ratio minimum | Vérification |
|---------|--------------|-------------|
| Texte normal (< 18px) | 4.5:1 | `#1E293B` sur `#FFFFFF` = 12.6:1 ✓ |
| Texte large (≥ 18px bold) | 3:1 | Tous nos titres respectent ce ratio |
| Éléments interactifs | 3:1 | Boutons, liens, inputs |
| Indicateurs non-textuels | 3:1 | Icônes, bordures focus |

### 7.2 Navigation clavier

| Touche | Comportement |
|--------|-------------|
| `Tab` | Parcourir les éléments interactifs dans l'ordre logique |
| `Shift+Tab` | Parcourir en sens inverse |
| `Enter` | Activer l'élément focalisé |
| `Espace` | Cocher/décocher, ouvrir dropdown |
| `Escape` | Fermer modale, annuler action en cours |
| `↑↓` | Naviguer dans les listes, dropdowns |
| `←→` | Naviguer entre onglets |

### 7.3 ARIA et sémantique

| Composant | Attribut requis |
|-----------|----------------|
| Modales | `role="dialog"`, `aria-modal="true"`, `aria-labelledby` |
| Toasts | `role="alert"`, `aria-live="polite"` |
| Badges compteur | `aria-label="3 notifications non lues"` |
| Boutons icône | `aria-label` descriptif (pas seulement l'icône) |
| Tableaux triables | `aria-sort="ascending/descending"` sur le header |
| Onglets | `role="tablist"`, `role="tab"`, `role="tabpanel"` |
| Formulaires | `aria-required`, `aria-invalid`, `aria-describedby` pour erreurs |
| Gantt | `role="img"`, `aria-label` décrivant le contenu, tableau alternatif accessible |

### 7.4 Règles supplémentaires

- Ne jamais communiquer une information uniquement par la couleur (ajouter icône + texte)
- Toutes les images/avatars doivent avoir un `alt` descriptif
- Les animations respectent `prefers-reduced-motion`
- Le zoom 200% ne casse pas le layout
- Le skip-to-content link est présent sur chaque page

---

## 8. Performance perçue

### 8.1 Seuils de réponse

| Action | Seuil | Technique |
|--------|-------|-----------|
| Click sur bouton | < 100ms | Feedback visuel immédiat (état pressed) |
| Navigation entre pages | < 300ms | Transition animée + skeleton |
| Chargement de données | < 1s | Skeleton loading |
| Chargement initial (cold) | < 2s | Code splitting, lazy loading |
| Export petit (< 1000 lignes) | < 3s | Synchrone avec spinner |
| Export gros (> 5000 lignes) | Asynchrone | Toast "Export en cours" + notification quand prêt |
| Recherche/filtre | < 300ms | Debounce input, requête optimisée |
| Auto-save | < 500ms | Background save avec indicateur discret |

### 8.2 Stratégies recommandées

| Stratégie | Application |
|-----------|-------------|
| **Skeleton loading** | Tous les tableaux, dashboards, fiches |
| **Optimistic UI** | Validation temps, changement statut Kanban |
| **Debounce** | Recherche (300ms), filtres (200ms) |
| **Pagination** | Tableaux > 25 lignes (server-side) |
| **Virtualisation** | Listes > 100 éléments (react-window) |
| **Lazy loading** | Onglets non visibles, graphiques below-the-fold |
| **Cache local** | Données de référence (projets, collaborateurs, phases) |
| **Prefetch** | Navigation probable (hover sur lien > 200ms → prefetch) |

---

## 9. Bibliothèque de composants

### 9.1 Composants de base

| Composant | Variantes | Props principales |
|-----------|-----------|------------------|
| **Button** | `primary`, `secondary`, `danger`, `ghost`, `icon` | `size` (sm/md/lg), `loading`, `disabled`, `fullWidth` |
| **Input** | `text`, `number`, `email`, `password`, `search`, `textarea` | `label`, `placeholder`, `error`, `helper`, `required` |
| **Select** | `single`, `multi`, `searchable`, `creatable` | `options`, `value`, `placeholder`, `loading` |
| **DatePicker** | `single`, `range`, `month`, `year` | `value`, `min`, `max`, `format`, `presets` |
| **Badge** | `status`, `count`, `tag` | `color`, `size`, `removable` |
| **Avatar** | `image`, `initials`, `icon` | `src`, `name`, `size` (xs/sm/md/lg/xl) |
| **Tooltip** | `top`, `bottom`, `left`, `right` | `content`, `delay`, `maxWidth` |
| **Toast** | `success`, `error`, `info`, `warning` | `message`, `action`, `duration`, `dismissible` |
| **Modal** | `default`, `confirm`, `destructive` | `title`, `size` (sm/md/lg), `closable` |
| **Dropdown** | `menu`, `select` | `trigger`, `items`, `position`, `closeOnSelect` |

### 9.2 Composants métier

| Composant | Usage | Modules |
|-----------|-------|---------|
| **KPICard** | Carte indicateur avec tendance | Dashboard, Résumés |
| **StatusBadge** | Badge coloré selon le statut sémantique | Tous |
| **DataTable** | Tableau avec tri, filtres, pagination, sélection | Tous |
| **FilterBar** | Barre de filtres avec badges actifs | Tous les tableaux |
| **BulkActionBar** | Barre d'actions flottante (bottom) | Tous les tableaux |
| **EmptyState** | État vide avec illustration et CTA | Tous |
| **SkeletonLoader** | Placeholder de chargement animé | Tous |
| **KanbanBoard** | Tableau Kanban avec drag-drop | Opportunités, Tâches |
| **GanttChart** | Diagramme de Gantt interactif | Planning, Projets |
| **PlanningGrid** | Grille planning collaborateurs/projets × temps | Planning |
| **TimeGrid** | Grille de saisie hebdomadaire | Temps |
| **CalendarView** | Calendrier mensuel avec code couleur | Temps, Congés |
| **FileUploader** | Zone d'upload drag-drop avec preview | Notes de frais, Fichiers |
| **RichTextEditor** | Éditeur texte riche (markdown) | Notes, Blog |
| **NotificationBell** | Cloche avec badge et dropdown | Header |
| **SearchCommand** | Recherche globale Cmd+K | Header |
| **BreadcrumbNav** | Fil d'Ariane cliquable | Header |
| **PermissionMatrix** | Matrice rôles × permissions | Configuration |
| **ColorPicker** | Sélecteur de couleur avec preview | Configuration branding |
| **StepWizard** | Wizard multi-étapes avec progression | Import, Onboarding |

---

## 10. Wireframes clés

### 10.1 Tableau de bord (EPIC-014)

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ [☰]  Général > Tableau de bord                                  🔍  [🔔 3] [👤]│
├────────┬────────────────────────────────────────────────────────────────────────┤
│        │                                                                        │
│ GÉNÉRAL│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐                  │
│ 🏠 TdB │  │ 125 000€ │ │ 42 300€  │ │ 87%      │ │ 3 notes  │                  │
│ 🎯 Opp │  │Facturab. │ │ Impayé   │ │ Temps    │ │          │                  │
│ 📐 Proj│  │ ↗ +12%   │ │ ⚠ 3 ret. │ │ Obj: 90% │ │          │                  │
│        │  └──────────┘ └──────────┘ └──────────┘ └──────────┘                  │
│ ÉQUIPE │                                                                        │
│ 👥 Coll│  ┌─────────────────────────────────────────┐ ┌──────────────────────┐ │
│ 📅 Plan│  │                                         │ │  À VENIR             │ │
│ ⏱ Temps│  │     Synthèse financière 2026            │ │                      │ │
│ 🧾 NdF │  │                                         │ │  Aujourd'hui         │ │
│ ✅ Valid│  │   CA ────────────────                   │ │  • Jalon APS Bureaux │ │
│        │  │   Coûts - - - - - - -                   │ │  • Tâche: Plans PRO  │ │
│ GESTION│  │   Marge ............                     │ │                      │ │
│ 🏢 Clie│  │                                         │ │  Demain              │ │
│ 💰 Coût│  │   J F M A M J J A S O N D               │ │  • Congé M. Dupont   │ │
│ 📄 Fact│  │                                         │ │  • Réunion client    │ │
│ 📊 Fina│  └─────────────────────────────────────────┘ │                      │ │
│ 📈 Rapp│                                              │  28 février           │ │
│        │  ┌─────────────────────────────────────────┐ │  • Échéance FAC-042  │ │
│ COLLAB.│  │                                         │ │  • Jalon EXE École   │ │
│ ✔ Tâche│  │     Planning projets (simplifié)        │ │                      │ │
│ 📝 Note│  │                                         │ │  [Voir tout →]       │ │
│ 📰 Blog│  │  Bureaux ████████░░░  75%   15/04      │ └──────────────────────┘ │
│ 🔔 Noti│  │  École   ██████░░░░░  60%   01/06      │                          │
│        │  │  Mairie  ████░░░░░░░  40%   30/09      │                          │
│────────│  │  Cliniq. █░░░░░░░░░░  10%   15/12      │                          │
│ ⚙ Conf │  │                                         │                          │
│ 👤 Prof│  │  [Voir tous les projets →]              │                          │
│        │  └─────────────────────────────────────────┘                          │
└────────┴───────────────────────────────────────────────────────────────────────┘
```

### 10.2 Saisie temps — Grille hebdomadaire (EPIC-005)

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ [☰]  Équipe > Temps > Saisie                                    🔍  [🔔] [👤] │
├────────┬────────────────────────────────────────────────────────────────────────┤
│        │                                                                        │
│ Sidebar│  Semaine du 24 au 28 février 2026     [◀]  [▶]  [Aujourd'hui]         │
│        │                                                                        │
│        │  [+ Ajouter projet]  [Copier sem. précédente]  [Soumettre]            │
│        │                                                                        │
│        │  ┌──────────────────┬──────┬──────┬──────┬──────┬──────┬──────┐       │
│        │  │ Projet / Phase   │ Lun  │ Mar  │ Mer  │ Jeu  │ Ven  │ Total│       │
│        │  │                  │  24  │  25  │  26  │  27  │  28  │      │       │
│        │  ├──────────────────┼──────┼──────┼──────┼──────┼──────┼──────┤       │
│        │  │ 🟦 Bureaux Paris │      │      │      │      │      │      │       │
│        │  │    ESQ           │ 4:00 │ 3:00 │ 4:00 │ 2:00 │ 0:00 │13:00 │       │
│        │  │    APS           │ 3:00 │ 4:00 │ 3:00 │ 5:00 │ 3:00 │18:00 │       │
│        │  ├──────────────────┼──────┼──────┼──────┼──────┼──────┼──────┤       │
│        │  │ 🟩 École Lille   │      │      │      │      │      │      │       │
│        │  │    PRO           │ 0:00 │ 0:00 │ 0:00 │ 0:00 │ 4:00 │ 4:00 │       │
│        │  ├──────────────────┼──────┼──────┼──────┼──────┼──────┼──────┤       │
│        │  │ ⬜ Interne       │      │      │      │      │      │      │       │
│        │  │    Réunion       │ 1:00 │ 1:00 │ 1:00 │ 1:00 │ 1:00 │ 5:00 │       │
│        │  ├──────────────────┼──────┼──────┼──────┼──────┼──────┼──────┤       │
│        │  │ TOTAL            │ 8:00 │ 8:00 │ 8:00 │ 8:00 │ 8:00 │40:00 │       │
│        │  │                  │  ✓   │  ✓   │  ✓   │  ✓   │  ✓   │  ✓   │       │
│        │  └──────────────────┴──────┴──────┴──────┴──────┴──────┴──────┘       │
│        │                                                                        │
│        │  💡 Astuce : Tab pour naviguer, Enter pour valider, Echap pour annuler │
│        │                                                                        │
└────────┴────────────────────────────────────────────────────────────────────────┘
```

### 10.3 Facturation — Liste avec filtres (EPIC-004)

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│ [☰]  Gestion > Facturation > Factures                            🔍  [🔔] [👤] │
├────────┬─────────────────────────────────────────────────────────────────────────┤
│        │                                                                         │
│ Sidebar│  Factures                                     [+ Nouvelle facture]      │
│        │                                                                         │
│        │  🔍 Rechercher par référence, client...                                │
│        │  [Statut ▼] [Client ▼] [Projet ▼] [Période ▼]  [+ Filtre]            │
│        │  Filtres : Statut: Envoyée ✕  |  Période: 2026 ✕                       │
│        │                                                                         │
│        │  ┌────┬───────────┬───────────┬───────────┬────────┬────────┬────────┐ │
│        │  │ ☐  │ Réf.    ▲ │ Client    │ Montant   │ Statut │ Éch.   │        │ │
│        │  ├────┼───────────┼───────────┼───────────┼────────┼────────┼────────┤ │
│        │  │ ☐  │ FAC-0042  │ ACME Corp │ 12 500 €  │ 🟢 Env │ 15/03  │ [⋯]   │ │
│        │  │ ☐  │ FAC-0041  │ ACME Corp │  8 000 €  │ 🟢 Env │ 10/03  │ [⋯]   │ │
│        │  │ ☐  │ FAC-0038  │ Martin SA │  5 200 €  │ 🔴 Ret │ 01/02  │ [⋯]   │ │
│        │  │ ☐  │ FAC-0035  │ Mairie Li │ 15 800 €  │ 🟢 Env │ 28/02  │ [⋯]   │ │
│        │  │ ☐  │ FAC-0032  │ CHU Renne │  3 400 €  │ 🟡 Bro │ --     │ [⋯]   │ │
│        │  └────┴───────────┴───────────┴───────────┴────────┴────────┴────────┘ │
│        │                                                                         │
│        │  1-25 sur 142 résultats        [◀ 1 2 3 ... 6 ▶]    [25 ▼] par page   │
│        │                                                                         │
└────────┴─────────────────────────────────────────────────────────────────────────┘
```

### 10.4 Validation — Dashboard manager (EPIC-012)

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│ [☰]  Équipe > Validation                                        🔍  [🔔] [👤]  │
├────────┬─────────────────────────────────────────────────────────────────────────┤
│        │                                                                         │
│ Sidebar│  [Temps (12)]  [Congés (3)]  [Notes de frais (5)]  [Factures (2)]      │
│        │                                                                         │
│        │  Temps — Semaine du 17 au 21 février 2026                               │
│        │                                                                         │
│        │  [Semaine ▼]  [Équipe ▼]  [Collaborateur ▼]    [Tout valider]          │
│        │                                                                         │
│        │  ┌──────────────────────────────────────────────────────────────────┐   │
│        │  │ 👤 Martin Dupont                          Total: 38:00  ⚠       │   │
│        │  │    Bureaux Paris / ESQ      Lun 8h  Mar 7h  Mer 8h  ...  32:00 │   │
│        │  │    Interne / Réunion        Lun 1h  Mar 1h  ...           6:00  │   │
│        │  │                                                                  │   │
│        │  │                                      [✓ Valider]  [✕ Rejeter]   │   │
│        │  └──────────────────────────────────────────────────────────────────┘   │
│        │                                                                         │
│        │  ┌──────────────────────────────────────────────────────────────────┐   │
│        │  │ 👤 Sophie Martin                         Total: 40:00  ✓        │   │
│        │  │    École Lille / PRO         Lun 8h  Mar 8h  Mer 8h  ...  35:00 │   │
│        │  │    Interne / Formation       Ven 5h                        5:00  │   │
│        │  │                                                                  │   │
│        │  │                                      [✓ Valider]  [✕ Rejeter]   │   │
│        │  └──────────────────────────────────────────────────────────────────┘   │
│        │                                                                         │
└────────┴─────────────────────────────────────────────────────────────────────────┘
```

### 10.5 Notifications — Dropdown (EPIC-017)

```
                                                              ┌──────────────────────────┐
                                                              │  Notifications       [✓] │
                                                              │  Tout marquer comme lu    │
                                                              ├──────────────────────────┤
                                                              │ 🟦 ⏱ Temps validé        │
                                                              │  Vos heures du 17-21     │
                                                              │  fév. ont été validées   │
                                                              │  par J. Dupont           │
                                                              │  il y a 5 min            │
                                                              ├──────────────────────────┤
                                                              │ 🟦 📄 Facture payée      │
                                                              │  FAC-0035 — Mairie Lille │
                                                              │  Paiement de 15 800 €    │
                                                              │  reçu                    │
                                                              │  il y a 2h               │
                                                              ├──────────────────────────┤
                                                              │    ✔ Tâche assignée      │
                                                              │  "Plans PRO étage 3"     │
                                                              │  assignée par S. Martin  │
                                                              │  hier                    │
                                                              ├──────────────────────────┤
                                                              │  [Voir toutes →]         │
                                                              └──────────────────────────┘
```

---

## 11. Checklist UX pour les développeurs

### 11.1 Avant chaque développement d'écran

```
☐ L'action principale est identifiée et visuellement dominante
☐ La hiérarchie visuelle guide l'œil (titre → KPI → contenu → actions)
☐ Les états sont tous définis : loading, vide, erreur, succès, données
☐ Les textes sont explicites (pas de jargon technique, pas d'anglicisme inutile)
☐ Les icônes sont accompagnées de texte si ambiguës
☐ Le feedback est défini pour chaque action (toast, badge, animation)
```

### 11.2 Avant chaque livraison de composant

```
☐ CONTRASTE : Vérifié WCAG AA (4.5:1 texte, 3:1 éléments)
☐ CLAVIER : Navigable au clavier (Tab, Enter, Escape)
☐ ARIA : Labels et rôles correctement attribués
☐ RESPONSIVE : Testé sur mobile (375px), tablette (768px), desktop (1280px)
☐ LOADING : Skeleton en place pour chargement > 300ms
☐ VIDE : État vide avec illustration et CTA
☐ ERREUR : Messages d'erreur clairs et actionnables
☐ ANIMATION : Respecte prefers-reduced-motion
☐ TOUCH : Targets min 44×44px sur mobile
☐ PERFORMANCE : Temps de réponse < seuils définis (section 8)
```

### 11.3 Avant chaque release

```
☐ COHÉRENCE : Mêmes couleurs de statut dans tous les modules
☐ FILTRES : Même comportement de filtrage partout
☐ EXPORTS : Même interface d'export partout
☐ FEEDBACK : Toasts cohérents (position, durée, style)
☐ NAVIGATION : Breadcrumbs à jour, retour préserve les filtres
☐ RACCOURCIS : Cmd+K, N (nouveau), F (filtre), E (export) fonctionnels
☐ PRINT : Les pages essentielles sont imprimables proprement
☐ I18N : Tous les textes externalisés (français par défaut, anglais prévu)
```

---

## 12. Annexes

### 12.1 Carte des flux inter-modules

```
                    ┌─────────────┐
                    │ Opportunités│
                    │  EPIC-001   │
                    └──────┬──────┘
                           │ Conversion
                           ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Clients    │◄──►│   Projets   │◄──►│ Honoraires  │
│  EPIC-010   │    │  EPIC-002   │    │  EPIC-003   │
└─────────────┘    └──────┬──────┘    └──────┬──────┘
                          │                   │
              ┌───────────┼───────────┐       │
              ▼           ▼           ▼       ▼
       ┌───────────┐ ┌─────────┐ ┌──────────────┐
       │  Planning  │ │  Temps  │ │ Facturation  │
       │ EPIC-006  │ │EPIC-005 │ │  EPIC-004    │
       └─────┬─────┘ └────┬────┘ └──────┬───────┘
             │            │              │
             ▼            ▼              ▼
       ┌───────────────────────────────────────┐
       │              Coûts — EPIC-007         │
       └───────────────────┬───────────────────┘
                           │
                           ▼
       ┌───────────────────────────────────────┐
       │           Finances — EPIC-008         │
       └───────────────────────────────────────┘

  Modules transversaux :
  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐
  │ Validation │ │ Notes frais│ │Collaborat. │ │  Rapports  │
  │ EPIC-012   │ │ EPIC-013   │ │ EPIC-009   │ │ EPIC-011   │
  └────────────┘ └────────────┘ └────────────┘ └────────────┘

  Infrastructure :
  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐
  │Tableau bord│ │Collaborat. │ │  Config.   │ │Notifications│
  │ EPIC-014   │ │ EPIC-015   │ │ EPIC-016   │ │ EPIC-017   │
  └────────────┘ └────────────┘ └────────────┘ └────────────┘
```

### 12.2 Priorisation des écrans (MoSCoW)

| Priorité | Écrans | Justification |
|----------|--------|---------------|
| **Must Have** | Tableau de bord, Saisie temps (quotidien + hebdo), Liste projets, Fiche projet, Facturation (création + liste), Validation, Login/Profil | Usage quotidien par tous |
| **Should Have** | Opportunités (liste + kanban), Planning agence, Finances résumé, Clients, Notes de frais, Collaborateurs, Notifications | Usage hebdomadaire |
| **Could Have** | Rapports (bibliothèque + génération), Gantt projet, Coûts détail, Blog, Import/Export données | Usage mensuel |
| **Won't Have (V1)** | Timer temps réel, App mobile native, Chat intégré, IA prédictive, Marketplace intégrations | V2+ |

### 12.3 Métriques UX à suivre post-lancement

| Métrique | Objectif | Outil de mesure |
|----------|----------|----------------|
| Time to Task (saisie temps) | < 5 min/semaine | Analytics + chrono |
| Time to First Value (onboarding) | < 30 min | Funnel analytics |
| Task Success Rate (création facture) | > 95% | Error tracking |
| System Usability Scale (SUS) | > 75/100 | Questionnaire trimestriel |
| Net Promoter Score (NPS) | > 40 | Enquête semestrielle |
| Taux d'erreur formulaires | < 5% | Error logging |
| Temps de chargement P95 | < 2s | Real User Monitoring |
| Taux d'adoption notifications | > 70% | Feature analytics |

### 12.4 Outils recommandés

| Catégorie | Outil recommandé | Justification |
|-----------|-----------------|---------------|
| **Design** | Figma | Collaboration temps réel, composants, prototypage |
| **Design System** | Figma + Storybook | Single source of truth composants |
| **Prototypage** | Figma Prototyping | Flux interactifs pour validation |
| **Icônes** | Lucide Icons | Open source, cohérent, léger |
| **Illustrations** | unDraw | Illustrations SVG personnalisables, gratuites |
| **Charts** | Recharts ou Chart.js | React-native, performant, accessible |
| **Gantt** | @bryntum/gantt ou custom D3.js | Interactif, performant |
| **Drag-drop** | @dnd-kit | Moderne, accessible, performant |
| **Rich text** | TipTap | Extensible, markdown-compatible |
| **Tableaux** | TanStack Table | Headless, performant, tri/filtre/pagination |
| **Formulaires** | React Hook Form + Zod | Validation performante, type-safe |
| **Animations** | Framer Motion | Fluide, respecte reduced-motion |
| **Tests UX** | Hotjar + PostHog | Heatmaps, session replay, analytics |

---

*Ce document est un livrable vivant. Il doit être mis à jour à chaque sprint pour refléter les décisions UX prises durant le développement.*

*Prochaine étape recommandée : transformer ces wireframes ASCII en maquettes Figma haute fidélité pour validation avec les utilisateurs cibles.*
