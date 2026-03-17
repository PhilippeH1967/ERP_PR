# Recommandations UX -- Audit ChangePoint pour l'application OOTI

**Application auditee : Planview ChangePoint**
**URL : https://provencherroy.changepointasp.com/**
**Application cible : OOTI**
**Date : 27 fevrier 2026**
**Version du document : 1.0**
**Auteur : UX/UI Designer Senior**
**Statut : Draft pour validation**

---

## Table des matieres -- Partie 1 (Sections 1 a 5)

1. [Design System](#1-design-system)
2. [Patterns d'interaction](#2-patterns-dinteraction)
3. [Module Gestion de Projets -- Recommandations](#3-module-gestion-de-projets--recommandations)
4. [Module Feuilles de Temps -- Recommandations](#4-module-feuilles-de-temps--recommandations)
5. [Module Facturation -- Recommandations](#5-module-facturation--recommandations)

> **Note** : La partie 2 (sections 6 a 10) couvrant le responsive, l'accessibilite, la performance, les composants avances et les wireframes sera ajoutee dans un second temps.

---

## 1. Design System

Le design system definit les fondations visuelles et interactives de l'application OOTI. Chaque decision s'appuie sur l'analyse des lacunes constatees dans ChangePoint : absence de design system, palette de couleurs incoherente, typographie systeme, absence de composants reutilisables.

### 1.1 Palette de couleurs

#### Mode clair (defaut)

**Couleurs primaires**

| Role | Nom | Code hex | Usage |
|------|-----|----------|-------|
| **Primaire 900** | Bleu marine | `#0F2540` | Sidebar, header compact, texte sur fond clair |
| **Primaire 700** | Bleu professionnel | `#1E3A5F` | Boutons primaires, liens actifs, focus |
| **Primaire 500** | Bleu moyen | `#2563EB` | Liens, icones actives, selection |
| **Primaire 300** | Bleu clair | `#60A5FA` | Bordures focus, surbrillance |
| **Primaire 100** | Bleu tres clair | `#DBEAFE` | Fond de selection, hover clair |
| **Primaire 50** | Bleu pale | `#EFF6FF` | Fond de notification info |

**Couleur secondaire**

| Role | Nom | Code hex | Usage |
|------|-----|----------|-------|
| **Secondaire 700** | Vert fonce | `#15803D` | Texte succes sur fond clair |
| **Secondaire 500** | Vert succes | `#22C55E` | Indicateurs positifs, statuts valides |
| **Secondaire 300** | Vert clair | `#86EFAC` | Bordures succes |
| **Secondaire 100** | Vert pale | `#DCFCE7` | Fond de badge succes |
| **Secondaire 50** | Vert tres pale | `#F0FDF4` | Fond de notification succes |

**Couleur d'accent**

| Role | Nom | Code hex | Usage |
|------|-----|----------|-------|
| **Accent 700** | Indigo fonce | `#4338CA` | Texte accent sur fond clair |
| **Accent 500** | Indigo | `#6366F1` | Boutons secondaires, indicateurs speciaux |
| **Accent 300** | Indigo clair | `#A5B4FC` | Bordures accent |
| **Accent 100** | Indigo pale | `#E0E7FF` | Fond de badge accent |

**Couleurs semantiques**

| Statut | Background | Texte | Bordure | Usage |
|--------|-----------|-------|---------|-------|
| **Succes** | `#F0FDF4` | `#15803D` | `#86EFAC` | Valide, paye, approuve, dans les temps, marge positive |
| **Warning** | `#FFFBEB` | `#B45309` | `#FCD34D` | En attente, retard modere, marge faible, seuil approche |
| **Erreur** | `#FEF2F2` | `#DC2626` | `#FCA5A5` | Rejete, en retard, impaye, marge negative, erreur |
| **Info** | `#EFF6FF` | `#1D4ED8` | `#93C5FD` | Information, notification, aide contextuelle |
| **Neutre** | `#F8FAFC` | `#64748B` | `#E2E8F0` | Brouillon, archive, inactif, desactive |

**Gamme de gris (8 niveaux)**

| Token | Code hex | Usage |
|-------|----------|-------|
| `gray-950` | `#0F172A` | Texte principal, titres |
| `gray-800` | `#1E293B` | Texte de corps, labels importants |
| `gray-700` | `#334155` | Texte secondaire fort |
| `gray-500` | `#64748B` | Texte secondaire, icones inactives, placeholders |
| `gray-400` | `#94A3B8` | Metadonnees, timestamps, texte desactive |
| `gray-300` | `#CBD5E1` | Bordures desactivees, separateurs secondaires |
| `gray-200` | `#E2E8F0` | Bordures de cartes, separateurs, lignes de tableaux |
| `gray-100` | `#F1F5F9` | Fond de tableaux alternes, fond de sidebar |
| `gray-50` | `#F8FAFC` | Fond de page principal |

#### 1.1.1 Comparaison ChangePoint vs OOTI cible

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Palette | Couleurs systeme Windows, bleu generique, pas de palette definie | Palette structuree avec 6 niveaux par couleur, tokens semantiques |
| Statuts | Texte noir simple, pas de code couleur | Badges colores avec background/texte/bordure coherents |
| Contraste | Non conforme WCAG, texte gris sur fond blanc | Ratio minimum 4.5:1 pour tout texte (WCAG AA) |
| Coherence | Couleurs differentes selon les modules | Palette unique appliquee identiquement dans tous les modules |
| Mode sombre | Inexistant | Supporte nativement (voir section 1.6) |

### 1.2 Typographie

**Font family principale : Inter**

Inter est une police gratuite, optimisee pour les interfaces utilisateur, avec un excellent support des chiffres tabulaires (alignement des colonnes de montants) et une lisibilite superieure sur ecran.

| Niveau | Font | Taille | Poids (weight) | Line-height | Letter-spacing | Usage |
|--------|------|--------|-----------------|-------------|----------------|-------|
| **Display** | Inter | 32px | 700 (Bold) | 40px | -0.02em | Titre de page d'accueil, KPI principal |
| **H1** | Inter | 28px | 700 (Bold) | 36px | -0.02em | Titre de page (ex : "Projets", "Facturation") |
| **H2** | Inter | 22px | 600 (Semi-bold) | 28px | -0.01em | Titre de section (ex : "Structure WBS", "Billing Roles") |
| **H3** | Inter | 18px | 600 (Semi-bold) | 24px | 0 | Titre de carte, titre de panneau |
| **H4** | Inter | 16px | 600 (Semi-bold) | 22px | 0 | Sous-titre, label de groupe |
| **Body** | Inter | 14px | 400 (Regular) | 20px | 0 | Contenu principal, paragraphes |
| **Body small** | Inter | 13px | 400 (Regular) | 18px | 0 | Tableaux, metadonnees, grille de temps |
| **Caption** | Inter | 12px | 400 (Regular) | 16px | 0.01em | Labels, timestamps, annotations |
| **Small** | Inter | 11px | 500 (Medium) | 14px | 0.02em | Badges, tags, micro-texte |
| **Mono** | JetBrains Mono | 13px | 400 (Regular) | 18px | 0 | Montants financiers, codes projet, references |

**Font stack CSS :**
```
--font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
--font-mono: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
```

#### 1.2.1 Comparaison ChangePoint vs OOTI cible

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Police | Police systeme (Segoe UI, Arial), variable selon l'OS | Inter, coherente sur tous les OS et navigateurs |
| Echelle | Pas d'echelle definie, tailles arbitraires | Echelle typographique structuree de 11px a 32px |
| Chiffres | Chiffres proportionnels, colonnes de montants desalignees | Chiffres tabulaires (Inter + JetBrains Mono) pour alignement parfait |
| Hierarchie | Hierarchie visuelle faible, titres peu distincts | 10 niveaux de hierarchie clairement differencies |
| Montants | Meme police que le texte courant | Police monospace dediee pour les montants et codes |

### 1.3 Grille et espacement

**Systeme de base 8px** : Tous les espacements sont des multiples de 8px (avec 4px pour les micro-espacements).

**Spacing scale**

| Token | Valeur | Usage |
|-------|--------|-------|
| `space-1` | 4px | Espacement interne dense : padding de badge, gap entre icone et texte |
| `space-2` | 8px | Espacement entre elements groupes, padding de cellule de tableau |
| `space-3` | 12px | Padding de bouton vertical, gap dans un formulaire dense |
| `space-4` | 16px | Padding standard de carte, marge entre champs de formulaire |
| `space-6` | 24px | Espacement entre sections de formulaire, gouttiere de grille |
| `space-8` | 32px | Marge entre blocs majeurs, padding de modale |
| `space-12` | 48px | Espacement entre sections de page |
| `space-16` | 64px | Marge de page, espacement de section majeure |

**Container widths par breakpoint**

| Breakpoint | Nom | Largeur min | Container max | Colonnes | Gouttiere |
|------------|-----|-------------|---------------|----------|-----------|
| `xs` | Mobile | 0px | 100% | 4 | 16px |
| `sm` | Mobile large | 640px | 100% | 4 | 16px |
| `md` | Tablette | 768px | 100% | 8 | 24px |
| `lg` | Desktop | 1024px | 100% | 12 | 24px |
| `xl` | Desktop large | 1280px | 1280px | 12 | 24px |
| `2xl` | Ultra-wide | 1536px | 1440px | 12 | 32px |

**Grille** : 12 colonnes, gouttiere 24px, marge exterieure 32px (desktop) / 16px (mobile).

#### 1.3.1 Comparaison ChangePoint vs OOTI cible

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Systeme de grille | Pas de grille definie, layout fixe en pixels | Systeme 8px avec grille 12 colonnes responsive |
| Espacement | Espacement inconsistant entre les modules | 8 tokens d'espacement appliques uniformement |
| Responsive | Non responsive, largeur fixe ~1000px, pas de mobile | 6 breakpoints, de mobile (320px) a ultra-wide (1536px) |
| Conteneur | Largeur fixe, pas d'adaptation | Conteneur adaptatif avec largeur max de 1440px |

### 1.4 Composants reutilisables

#### 1.4.1 Boutons

**Variantes**

| Variante | Background | Texte | Bordure | Usage |
|----------|-----------|-------|---------|-------|
| **Primaire** | `#1E3A5F` | `#FFFFFF` | aucune | Action principale : "Creer", "Sauvegarder", "Soumettre" |
| **Secondaire** | `#FFFFFF` | `#1E3A5F` | `#E2E8F0` | Action secondaire : "Annuler", "Retour", "Exporter" |
| **Ghost** | transparent | `#1E3A5F` | aucune | Action tertiaire : "En savoir plus", "Voir tout" |
| **Danger** | `#DC2626` | `#FFFFFF` | aucune | Action destructrice : "Supprimer", "Rejeter" |
| **Succes** | `#22C55E` | `#FFFFFF` | aucune | Action de validation : "Approuver", "Valider" |

**Etats**

| Etat | Transformation | Duree |
|------|---------------|-------|
| **Default** | Apparence de base | -- |
| **Hover** | Assombrissement 10%, cursor pointer | transition 150ms |
| **Active / Pressed** | Assombrissement 20%, scale 0.98 | transition 100ms |
| **Focus** | Outline 2px `#60A5FA`, offset 2px | instantane |
| **Disabled** | Opacite 50%, cursor not-allowed | -- |
| **Loading** | Spinner anime remplace le texte, bouton desactive | -- |

**Tailles**

| Taille | Hauteur | Padding H | Font size | Border-radius | Usage |
|--------|---------|-----------|-----------|---------------|-------|
| `sm` | 32px | 12px | 13px | 6px | Actions inline, tableaux |
| `md` | 40px | 16px | 14px | 8px | Actions standard (defaut) |
| `lg` | 48px | 24px | 16px | 8px | CTAs de page, formulaires |

#### 1.4.2 Cards

**Card Projet**

```
┌──────────────────────────────────────────┐
│  [Icone type]  250029 Intelligence Art.  │
│                                          │
│  Client : Provencher Roy     ● Active    │
│  Chef de projet : M. Belanger            │
│                                          │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│  │ Budget  │  │ Effort  │  │ Marge   │ │
│  │ 882K $  │  │ 1565h   │  │ 32.4%   │ │
│  └─────────┘  └─────────┘  └─────────┘ │
│                                          │
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░  72%             │
└──────────────────────────────────────────┘
```

| Propriete | Valeur |
|-----------|--------|
| Padding | 16px |
| Border-radius | 12px |
| Border | 1px solid `#E2E8F0` |
| Shadow | `0 1px 3px rgba(0,0,0,0.1)` |
| Hover | Shadow `0 4px 6px rgba(0,0,0,0.1)`, cursor pointer |
| Click | Navigue vers la fiche projet |

**Card Facture**

```
┌──────────────────────────────────────────┐
│  FAC-2026-0042            🟢 Envoyee     │
│  ACME Corporation                        │
│                                          │
│  Montant :      12 500,00 CAD            │
│  Emise :        15/02/2026               │
│  Echeance :     15/03/2026               │
│                                          │
│  [Enregistrer paiement]   [...]          │
└──────────────────────────────────────────┘
```

**Card Temps (resume hebdomadaire)**

```
┌──────────────────────────────────────────┐
│  Semaine du 24 fevrier 2026              │
│                                          │
│  Lu  Ma  Me  Je  Ve  Sa  Di    Total     │
│  7.5 7.5 8.0 7.5 7.0 0   0    37.50h    │
│  ▓▓  ▓▓  ▓▓  ▓▓  ▓▓  ░░  ░░             │
│                                          │
│  Projet : 30.00h  |  Non-projet : 7.50h  │
│  ● Soumise                               │
└──────────────────────────────────────────┘
```

#### 1.4.3 Tables

| Propriete | Specification |
|-----------|---------------|
| **Header** | Background `#F8FAFC`, texte `#64748B`, font-weight 600, font-size 12px uppercase, padding 12px 16px |
| **Ligne** | Padding 12px 16px, border-bottom 1px `#E2E8F0` |
| **Ligne hover** | Background `#F8FAFC` |
| **Ligne selectionnee** | Background `#EFF6FF`, border-left 3px `#2563EB` |
| **Ligne alternee** | Background `#FAFBFC` (optionnel, desactive par defaut) |
| **Tri** | Icone ▲/▼ a cote du header, tri mono-colonne par defaut, multi-colonnes avec Shift+Click |
| **Filtre** | Dropdown dans le header de colonne ou barre de filtres au-dessus |
| **Actions** | Colonne "Actions" a droite, icone oeil (voir), menu ⋯ (editer, dupliquer, supprimer) |
| **Pagination** | En bas, selecteur 10/25/50/100 par page, navigation pages |
| **Etat vide** | Illustration + texte explicatif + bouton CTA |
| **Etat loading** | Skeleton (12 lignes grisees animees, shimmer effect) |
| **Checkbox** | Colonne gauche, selection multiple, barre d'actions bulk en bas |
| **Montants** | Alignes a droite, font monospace, separateur de milliers |
| **Dates** | Format `DD/MM/YYYY` ou relatif ("il y a 3j") |
| **Statuts** | Badge colore selon la palette semantique |
| **Colonnes redimensionnables** | Drag sur le separateur de header pour ajuster la largeur |
| **Colonnes reordonnables** | Drag sur le header pour deplacer une colonne |

#### 1.4.4 Modals

| Type | Largeur | Usage | Boutons |
|------|---------|-------|---------|
| **Confirmation** | 400px | Confirmer une action (supprimer, rejeter) | "Annuler" (secondaire) + "Confirmer" (danger/primaire) |
| **Formulaire** | 560px | Creer/editer une entite | "Annuler" (secondaire) + "Creer/Sauvegarder" (primaire) |
| **Formulaire large** | 720px | Formulaire complexe (contrat, facture) | "Annuler" + "Sauvegarder brouillon" + "Creer" |
| **Alerte** | 400px | Avertissement non bloquant | "Compris" (primaire) |
| **Detail** | 800px | Vue detail sans quitter la page | "Fermer" (secondaire) |

| Propriete | Specification |
|-----------|---------------|
| Overlay | Background `rgba(0,0,0,0.5)`, click exterieur ferme (avec confirmation si formulaire modifie) |
| Border-radius | 12px |
| Shadow | `0 10px 25px rgba(0,0,0,0.15)` |
| Animation | Fade-in + scale-up 200ms |
| Fermeture | Bouton X en haut a droite, touche Escape, click exterieur |
| Scroll | Scroll interne si contenu depasse 80vh |

#### 1.4.5 Badges / Tags (statuts)

| Statut | Background | Texte | Dot | Modules concernes |
|--------|-----------|-------|-----|-------------------|
| **Active** | `#F0FDF4` | `#15803D` | `#22C55E` | Projets, Clients, Collaborateurs |
| **Completed** | `#EFF6FF` | `#1D4ED8` | `#3B82F6` | Projets |
| **Draft** | `#F1F5F9` | `#64748B` | `#94A3B8` | Factures, Notes de frais |
| **Pending Approval** | `#FFFBEB` | `#B45309` | `#F59E0B` | Factures, Temps, Validation |
| **Pending 2nd Approval** | `#FFF7ED` | `#C2410C` | `#FB923C` | Factures |
| **Approved** | `#F0FDF4` | `#15803D` | `#22C55E` | Factures, Temps, Validation |
| **Committed** | `#EDE9FE` | `#6D28D9` | `#8B5CF6` | Factures |
| **Sent** | `#EFF6FF` | `#1D4ED8` | `#3B82F6` | Factures, Propositions |
| **Paid** | `#F0FDF4` | `#15803D` | `#22C55E` | Factures |
| **Partially Paid** | `#FFFBEB` | `#B45309` | `#F59E0B` | Factures |
| **Credited** | `#FEF2F2` | `#DC2626` | `#EF4444` | Factures (avoir) |
| **Archived** | `#F1F5F9` | `#94A3B8` | `#CBD5E1` | Tous modules |
| **Rejected** | `#FEF2F2` | `#DC2626` | `#EF4444` | Temps, Validation |
| **Overdue** | `#FEF2F2` | `#DC2626` | `#EF4444` | Factures, Relances |

**Structure du badge :**
```
┌─────────────────────┐
│  ● Texte du statut  │
└─────────────────────┘
```
- Padding : 4px 10px
- Border-radius : 9999px (pill)
- Font-size : 12px
- Font-weight : 500
- Dot : cercle 6px a gauche du texte

#### 1.4.6 Tooltips

| Propriete | Specification |
|-----------|---------------|
| Background | `#1E293B` (dark) |
| Texte | `#FFFFFF`, 12px, max 240px largeur |
| Padding | 8px 12px |
| Border-radius | 6px |
| Shadow | `0 2px 8px rgba(0,0,0,0.15)` |
| Fleche | Triangle 6px vers l'element de reference |
| Delai | Apparition apres 500ms de hover, disparition immediate |
| Position | Automatique (haut, bas, gauche, droite) selon l'espace disponible |

### 1.5 Iconographie

**Bibliotheque recommandee : Lucide Icons**

Lucide est une bibliotheque d'icones open source, coherente, legere (SVG), avec un trait uniforme de 2px. Alternative acceptable : Heroicons (Tailwind CSS).

| Propriete | Specification |
|-----------|---------------|
| Style | Stroke (outline), 2px |
| Tailles standard | 16px (inline, badges), 20px (boutons, navigation), 24px (titres, cards) |
| Couleur par defaut | `currentColor` (herite de la couleur du texte parent) |
| Couleur active | `#1E3A5F` (primaire) |
| Couleur inactive | `#94A3B8` (gris 400) |

**Conventions par module**

| Module | Icone principale | Icones secondaires |
|--------|-----------------|-------------------|
| **Projets** | `folder` | `git-branch` (WBS), `calendar` (Gantt), `layout-grid` (Worksheet) |
| **Temps** | `clock` | `pin` (epingle), `calendar-days` (semaine), `copy` (copier) |
| **Facturation** | `file-text` | `check-circle` (approuve), `send` (envoye), `dollar-sign` (paye) |
| **Contrats** | `file-signature` | `users` (roles), `percent` (remise), `calculator` (taux) |
| **Clients** | `building` | `contact` (contact), `globe` (localisation) |
| **Validation** | `check-square` | `thumbs-up` (approuver), `thumbs-down` (rejeter) |
| **Configuration** | `settings` | `sliders` (parametres), `shield` (securite), `palette` (theme) |

### 1.6 Mode sombre

#### 1.6.1 Principes de mapping couleurs clair vers sombre

| Principe | Description |
|----------|-------------|
| **Inversion des surfaces** | Les fonds clairs deviennent sombres, les textes sombres deviennent clairs |
| **Conservation des couleurs semantiques** | Les couleurs de statut (succes, warning, erreur) conservent leur teinte mais ajustent leur luminosite |
| **Elevation par luminosite** | En mode sombre, les elements eleves sont plus clairs (pas plus fonces) |
| **Contrast minimum maintenu** | Ratio minimum 4.5:1 (WCAG AA) maintenu en mode sombre |

#### 1.6.2 Palette mode sombre

**Surfaces et elevations**

| Token | Mode clair | Mode sombre | Usage |
|-------|-----------|-------------|-------|
| `surface-page` | `#F8FAFC` | `#0F172A` | Fond de page |
| `surface-card` | `#FFFFFF` | `#1E293B` | Fond de carte, tableau |
| `surface-elevated` | `#FFFFFF` | `#334155` | Dropdown, popovers, tooltips |
| `surface-overlay` | `rgba(0,0,0,0.5)` | `rgba(0,0,0,0.7)` | Fond de modale overlay |
| `surface-sidebar` | `#0F2540` | `#020617` | Sidebar navigation |
| `surface-header` | `#FFFFFF` | `#1E293B` | Header fixe |
| `surface-input` | `#FFFFFF` | `#1E293B` | Champs de formulaire |
| `surface-hover` | `#F8FAFC` | `#334155` | Fond de ligne hover |
| `surface-selected` | `#EFF6FF` | `#1E3A5F` | Fond de ligne selectionnee |

**Texte**

| Token | Mode clair | Mode sombre |
|-------|-----------|-------------|
| `text-primary` | `#0F172A` | `#F1F5F9` |
| `text-secondary` | `#64748B` | `#94A3B8` |
| `text-disabled` | `#94A3B8` | `#475569` |
| `text-inverse` | `#FFFFFF` | `#0F172A` |

**Bordures**

| Token | Mode clair | Mode sombre |
|-------|-----------|-------------|
| `border-default` | `#E2E8F0` | `#334155` |
| `border-strong` | `#CBD5E1` | `#475569` |
| `border-focus` | `#60A5FA` | `#60A5FA` |

**Couleurs semantiques mode sombre**

| Statut | Background (sombre) | Texte (sombre) |
|--------|-------------------|---------------|
| **Succes** | `#052E16` | `#4ADE80` |
| **Warning** | `#451A03` | `#FCD34D` |
| **Erreur** | `#450A0A` | `#FCA5A5` |
| **Info** | `#172554` | `#93C5FD` |

---

## 2. Patterns d'interaction

### 2.1 Navigation principale

#### 2.1.1 Comparaison ChangePoint vs OOTI cible

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Type | Onglets horizontaux en haut de page | Sidebar verticale retractable a gauche |
| Modules | Onglets : Home, Projects, Time, Expenses, Invoices, Contracts, Reports | Sections : General, Equipe, Gestion, Collaboration (voir structure ci-dessous) |
| Sous-navigation | Onglets secondaires horizontaux sous la barre principale | Sous-menus dans la sidebar avec icones et labels |
| Responsive | Non responsive, tronque sur petit ecran | Sidebar retractable en icones seules sur tablette, hamburger sur mobile |
| Contexte | Pas de breadcrumbs, perte de contexte frequente | Breadcrumbs dans le header + highlight du menu actif dans la sidebar |
| Recherche | Filtre "%" dans chaque module, pas de recherche globale | Recherche globale Cmd+K cross-module |
| Recents | Section "Recently viewed" dans certains modules | Section "Recents" persistante dans la sidebar |

#### 2.1.2 Structure de navigation proposee (sidebar)

```
┌──────────────────────────────────────────┐
│  [Logo OOTI]  Provencher Roy   [▼ PRA]  │
├──────────────────────────────────────────┤
│                                          │
│  GENERAL                                 │
│  ├── Tableau de bord                     │
│  ├── Projets          ▸                  │
│  │   ├── Vue d'ensemble                  │
│  │   ├── Liste des projets               │
│  │   ├── Arborescence (Tree)             │
│  │   ├── Gantt                           │
│  │   └── Carte (Work locations)          │
│  └── Clients                             │
│                                          │
│  EQUIPE                                  │
│  ├── Collaborateurs   ▸                  │
│  ├── Feuilles de temps ▸                 │
│  │   ├── Saisie hebdomadaire             │
│  │   ├── Calendrier                      │
│  │   └── Statistiques                    │
│  ├── Notes de frais                      │
│  └── Validation       ▸  [3]            │
│      ├── Temps                           │
│      ├── Conges                          │
│      ├── Notes de frais                  │
│      └── Factures                        │
│                                          │
│  GESTION                                 │
│  ├── Contrats         ▸                  │
│  ├── Facturation      ▸                  │
│  │   ├── Vue d'ensemble                  │
│  │   ├── Pipeline (Kanban)               │
│  │   ├── Liste des factures              │
│  │   └── Relances                        │
│  ├── Finances         ▸                  │
│  └── Rapports         ▸                  │
│                                          │
│  COLLABORATION                           │
│  ├── Taches                              │
│  ├── Notes                               │
│  └── Notifications    [5]                │
│                                          │
├──────────────────────────────────────────┤
│  Configuration                           │
│  Mon profil                              │
└──────────────────────────────────────────┘
```

#### 2.1.3 Breadcrumbs

| Propriete | Specification |
|-----------|---------------|
| Position | Header fixe, sous le hamburger/logo |
| Format | `Module > Sous-section > Element` |
| Separateur | `>` ou `/` en gris clair |
| Comportement | Chaque segment est cliquable et ramene a la vue correspondante |
| Exemple | `Projets > 250029 Intelligence Artificielle > WBS > 01.1 Comite IA` |

### 2.2 Recherche et filtrage

#### **REC-01 : Remplacer le wildcard "%" par une recherche intelligente**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Syntaxe | Wildcard "%" obligatoire (ex : "%Place%" pour chercher "Place des Arts") | Recherche en texte libre, pas de wildcard necessaire |
| Scope | Recherche limitee au module courant | Recherche globale cross-module (Cmd+K) + recherche locale par module |
| Resultats | Liste plate sans categorisation | Resultats groupes par type (Projets, Factures, Clients, Taches) |
| Temps de reponse | Rechargement de page complet | Resultats en temps reel avec debounce 300ms |
| Filtres | Un seul filtre a la fois | Filtres combinables avec operateurs AND |

**Specification de la recherche globale (Cmd+K) :**

```
┌──────────────────────────────────────────────┐
│  🔍  Rechercher un projet, une facture...    │
├──────────────────────────────────────────────┤
│                                              │
│  PROJETS                                     │
│  ├── 250029 Intelligence Artificielle  Active│
│  └── 200236 Place des Arts - 5eme S.  Compl. │
│                                              │
│  FACTURES                                    │
│  └── FAC-2026-0042 ACME Corp.  12 500 CAD   │
│                                              │
│  CLIENTS                                     │
│  └── Provencher Roy Associes architectes     │
│                                              │
│  ACTIONS RAPIDES                             │
│  ├── + Nouveau projet                        │
│  ├── + Nouvelle facture                      │
│  └── Saisir mes heures                       │
│                                              │
└──────────────────────────────────────────────┘
```

#### **REC-02 : Filtres combinables avec pills**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Filtres | Dropdowns separes, un seul filtre actif | Filtres combinables, multi-selection |
| Affichage | Pas d'indication des filtres actifs | Pills sous la barre de recherche avec bouton X |
| Sauvegarde | Pas de sauvegarde de combinaisons | Filtres favoris enregistrables |
| Reset | Pas de bouton "Reinitialiser" | Bouton "Effacer tous les filtres" |

**Structure des filtres :**
```
🔍 Rechercher...   [Statut ▼] [Client ▼] [Entite ▼] [Periode ▼] [+ Filtre]

Filtres actifs :  [Statut: Active ✕]  [Entite: PRA ✕]  [Effacer tout]
```

### 2.3 Formulaires et saisie

#### **REC-03 : Validation en temps reel**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Validation | Validation au submit uniquement, rechargement de page si erreur | Validation inline en temps reel au blur de chaque champ |
| Messages | Message d'erreur generique en haut de page | Message d'erreur specifique sous le champ concerne, en rouge |
| Indicateurs | Pas d'indicateur de champ obligatoire clair | Asterisque `*` sur le label + bordure rouge si invalide |
| Confirmation | Pas de feedback de succes | Toast de confirmation + transition visuelle |

#### **REC-04 : Auto-save**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Sauvegarde | Bouton "Save" manuel, perte de donnees si navigation | Auto-save toutes les 30 secondes + a chaque changement de champ |
| Indicateur | Pas d'indicateur | Icone de sauvegarde dans le header : "Sauvegarde..." (en cours), "Sauvegarde reussie" (check vert) |
| Brouillons | Pas de gestion de brouillon | Auto-creation de brouillon des la premiere modification |
| Historique | Pas d'historique de versions | Historique des 10 dernieres sauvegardes avec possibilite de restauration |

#### **REC-05 : Inline editing**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Edition | Clic sur une ligne ouvre une nouvelle page/formulaire | Clic sur une cellule bascule en mode edition inline |
| Navigation | Rechargement de page pour chaque modification | Navigation Tab/Enter entre les cellules editables |
| Confirmation | Bouton "Save" explicite | Sauvegarde automatique au blur de la cellule |
| Annulation | Bouton "Cancel" ou retour arriere | Touche Escape annule la modification en cours |

### 2.4 Notifications et feedback

#### **REC-06 : Toast notifications**

| Type | Couleur | Icone | Duree | Position |
|------|---------|-------|-------|----------|
| **Succes** | `#F0FDF4` bordure `#22C55E` | check-circle | 3 secondes, auto-dismiss | Bas-droite |
| **Erreur** | `#FEF2F2` bordure `#EF4444` | alert-circle | Persistant jusqu'au dismiss | Bas-droite |
| **Warning** | `#FFFBEB` bordure `#F59E0B` | alert-triangle | 5 secondes | Bas-droite |
| **Info** | `#EFF6FF` bordure `#3B82F6` | info | 4 secondes | Bas-droite |

| Propriete | Specification |
|-----------|---------------|
| Largeur | 360px max |
| Animation | Slide-in depuis la droite, 200ms |
| Empilement | Max 3 toasts visibles, les plus anciens disparaissent |
| Action | Optionnel : bouton "Annuler" (undo) pour les actions reversibles |
| Fermeture | Bouton X + auto-dismiss (sauf erreur) |

#### **REC-07 : Badges de notification**

| Element | Position | Style | Mise a jour |
|---------|----------|-------|-------------|
| Menu Validation | A droite du label | Badge rouge circulaire, chiffre blanc, max "99+" | Temps reel (WebSocket) |
| Menu Notifications | A droite de l'icone cloche | Badge rouge circulaire | Temps reel |
| Onglet Pending Approval | A droite du titre d'onglet | Badge orange pill | Au chargement + polling 30s |

#### **REC-08 : Indicateur de sauvegarde**

```
Etats de l'indicateur :
  ○ Pas de modification    →  (rien d'affiche)
  ◎ Modifications non      →  ● Modifications non sauvegardees (gris)
     sauvegardees
  ⟳ Sauvegarde en cours    →  ⟳ Sauvegarde... (gris anime)
  ✓ Sauvegarde reussie     →  ✓ Sauvegarde reussie (vert, disparait apres 3s)
  ✕ Erreur de sauvegarde   →  ✕ Erreur de sauvegarde (rouge, persistant)
```

### 2.5 Drag & drop

#### **REC-09 : Drag & drop pour la reorganisation WBS**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Reorganisation WBS | Impossible : pas de drag & drop, modification manuelle des niveaux | Drag & drop natif dans la Tree View pour deplacer taches et phases |
| Feedback visuel | N/A | Ombre portee sur l'element deplace, placeholder en pointilles, zone de drop surlignee |
| Renumerotation | Manuelle | Automatique apres chaque deplacement |
| Multi-niveaux | N/A | Deplacement entre niveaux (promouvoir/retrograder une tache) |
| Annulation | N/A | Ctrl+Z pour annuler le dernier deplacement |

| Propriete | Specification |
|-----------|---------------|
| Handle | Icone grip (6 points) a gauche de chaque element |
| Drag feedback | Opacite 80%, ombre portee renforcee, element "fantome" |
| Drop zone | Ligne bleue horizontale entre les elements pour indiquer la position d'insertion |
| Drop zone niveaux | Indentation visuelle pour indiquer le niveau de destination (enfant ou frere) |
| Animation | Transition 200ms pour le repositionnement des elements |
| Restrictions | Les taches avec heures saisies affichent un avertissement avant deplacement |

#### **REC-10 : Kanban facturation avec drag & drop**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Vue factures | Liste plate avec colonne "Status" en texte | Vue Kanban avec colonnes = statuts, cartes = factures |
| Transition statut | Dropdown pour changer le statut manuellement | Drag & drop d'une carte entre colonnes de statut |
| Contraintes | Pas de contraintes de transition visibles | Transitions non autorisees = drag refuse + toast explicatif |
| Compteurs | Pas de compteur par statut | Compteur + montant total dans le header de chaque colonne |

**Structure du Kanban facturation :**

```
Draft (3)     Pending (2)    Approved (1)   Committed (4)   Sent (8)      Paid (12)
45 200 CAD    28 000 CAD     12 500 CAD     52 800 CAD      186 400 CAD   342 000 CAD
──────────    ──────────     ──────────     ──────────      ──────────    ──────────
┌────────┐   ┌────────┐     ┌────────┐     ┌────────┐      ┌────────┐    ┌────────┐
│FAC-042 │   │FAC-039 │     │FAC-041 │     │FAC-035 │      │FAC-030 │    │FAC-025 │
│ACME    │   │Martin  │     │Ville   │     │SQI     │      │Place A.│    │Poly    │
│12 500$ │   │8 000$  │     │12 500$ │     │22 300$ │      │45 000$ │    │28 500$ │
│        │   │        │     │        │     │        │      │        │    │        │
└────────┘   └────────┘     └────────┘     └────────┘      └────────┘    └────────┘
```

#### **REC-11 : Drag & drop pour le reorder des pins**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Ordre des pins | Ordre d'epinglage fixe (dernier epingle en bas du groupe) | Drag & drop pour reordonner les taches epinglees |
| Groupes | Pas de groupes | Groupes de pins personnalisables (ex : "Projet principal", "Admin") |

### 2.6 Raccourcis clavier

#### **REC-12 : Raccourcis clavier globaux et contextuels**

**Raccourcis globaux**

| Raccourci | Action | Contexte |
|-----------|--------|----------|
| `Cmd+K` / `Ctrl+K` | Ouvrir la recherche globale | Depuis n'importe quelle page |
| `N` | Nouveau (projet, facture, etc. selon le module actif) | Hors champ de saisie |
| `F` | Ouvrir/fermer le panneau de filtres | Pages avec tableaux |
| `E` | Exporter les donnees | Pages avec tableaux |
| `?` | Afficher l'aide des raccourcis (overlay) | Depuis n'importe quelle page |
| `Escape` | Fermer la modale/panneau/overlay actif | Modales, panneaux |

**Raccourcis module Temps**

| Raccourci | Action |
|-----------|--------|
| `←` / `→` | Naviguer a la semaine precedente/suivante |
| `Tab` | Cellule suivante dans la grille |
| `Shift+Tab` | Cellule precedente |
| `Enter` | Valider la cellule et passer a la ligne suivante |
| `Escape` | Annuler la modification en cours |
| `Ctrl+S` / `Cmd+S` | Sauvegarder manuellement |
| `Ctrl+Enter` / `Cmd+Enter` | Soumettre la feuille de temps |

**Raccourcis module Projets**

| Raccourci | Action |
|-----------|--------|
| `←` / `→` | Replier/deplier un noeud WBS |
| `↑` / `↓` | Naviguer entre les noeuds WBS |
| `Enter` | Ouvrir le detail du noeud selectionne |
| `Space` | Selectionner/deselectionner un noeud |
| `Ctrl+Shift+N` | Ajouter une tache enfant au noeud selectionne |

**Help overlay (?) :**

```
┌──────────────────────────────────────────────────────┐
│  Raccourcis clavier                            [✕]   │
├──────────────────────────────────────────────────────┤
│                                                      │
│  NAVIGATION                                          │
│  Cmd+K     Recherche globale                         │
│  ?         Afficher cette aide                       │
│  Escape    Fermer la modale active                   │
│                                                      │
│  ACTIONS                                             │
│  N         Nouveau (selon le module)                 │
│  F         Filtres                                   │
│  E         Exporter                                  │
│                                                      │
│  SAISIE DE TEMPS                                     │
│  ← / →     Semaine precedente/suivante               │
│  Tab        Cellule suivante                         │
│  Enter      Valider et passer a la ligne             │
│  Cmd+Enter  Soumettre la feuille de temps            │
│                                                      │
└──────────────────────────────────────────────────────┘
```

---

## 3. Module Gestion de Projets -- Recommandations

Ce module couvre les vues de projets (Tree, List, Worksheet), le profil de projet avec KPIs, la structure WBS, et les nouvelles vues (Gantt, Tableau de bord). Chaque recommandation compare l'etat actuel de ChangePoint avec la cible OOTI.

### 3.1 Vue arborescence amelioree (Tree View)

#### **REC-13 : Tree View interactive avec drag & drop**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Arborescence | Arborescence statique HTML, expand/collapse basique | Arborescence interactive avec icones distinctes par niveau, drag & drop, multi-selection |
| Icones | 3 icones generiques (livre, document checkmark, document vert) | Icones contextuelles par type (projet, phase, tache, sous-tache) + icone de facturation |
| Expand/Collapse | Clic sur icone fleche, boutons "Expand All" / "Collapse All" | Clic sur icone OU sur le nom, raccourcis ← / →, boutons Expand/Collapse + "Show Level N" |
| Recherche | Pas de recherche dans l'arborescence | Champ de recherche filtrant l'arborescence en temps reel (highlight des noeuds correspondants) |
| Multi-selection | Pas de multi-selection | Ctrl+Click pour selectionner plusieurs noeuds, Shift+Click pour selection contigue |
| Actions contextuelles | Pas de menu contextuel | Clic-droit : Ajouter enfant, Ajouter frere, Renommer, Deplacer, Supprimer, Dupliquer |
| Indicateurs | Icone facturable (bleu/rouge) | Badges inline : statut, heures consommees/planifiees, indicateur de budget |

**Wireframe Tree View amelioree :**

```
┌──────────────────────────────────────────────────────────────────────┐
│  Projets > 250029 Intelligence Artificielle > Structure WBS         │
├──────────────────────────────────────────────────────────────────────┤
│  🔍 Rechercher dans l'arborescence...                               │
│  [Expand All] [Collapse All] [Show Level ▼] [+ Tache]              │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ⠿ ▼ 📁 250029 Intelligence Artificielle        1565h / 40h  ● Actif│
│  │                                                                   │
│  │  ⠿ ▼ 📋 01. Intelligence Artificielle         1565h / 40h        │
│  │  │                                                                │
│  │  │  ⠿  📝 01.1 Comite Intelligence Artif.       450h     ● Actif │
│  │  │  ⠿  📝 01.2 Reflexion et mise en place GPTs  280h     ● Actif │
│  │  │  ⠿  📝 01.3 Dev Application CV/Projet        520h     ● Actif │
│  │  │  ⠿  📝 01.4 Outils IA 3D                     95h      ● Actif │
│  │  │  ⠿  📝 01.5 Formation                        120h     ● Actif │
│  │  │  ⠿  📝 01.6 Outils IA TI                      60h     ● Actif │
│  │  │  ⠿  📝 01.7 Reflexion Atelier                 40h     ● Actif │
│  │                                                                   │
│  (⠿ = handle de drag & drop)                                        │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

#### **REC-14 : Inline rename dans la Tree View**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Renommer | Ouvrir la fiche de la tache, modifier le champ nom, sauvegarder | Double-clic sur le nom dans l'arborescence pour basculer en mode edition inline |
| Confirmation | Bouton "Save" | Enter pour valider, Escape pour annuler |
| Feedback | Rechargement de page | Transition instantanee + toast "Tache renommee" |

#### **REC-15 : Multi-selection dans la Tree View**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Selection | Selection unitaire uniquement | Multi-selection : Ctrl+Click (individuel), Shift+Click (plage), Cmd+A (tout) |
| Actions groupees | Pas d'actions groupees | Barre d'actions : "Deplacer", "Supprimer", "Changer statut", "Assigner a" |
| Indicateur | Pas d'indicateur | Checkbox a gauche de chaque noeud + compteur "N selectionnes" |

### 3.2 Vue liste modernisee (List View)

#### **REC-16 : Colonnes configurables**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Colonnes | 7 colonnes fixes (All Projects, Status, Customer, Contract, Billable, Project Contact, Updated) | Colonnes configurables par l'utilisateur via un bouton "Colonnes" |
| Configuration | Pas de personnalisation | Panneau de selection des colonnes avec drag & drop pour l'ordre |
| Sauvegarde | N/A | Configuration sauvegardee par utilisateur |
| Colonnes disponibles | Limitees aux 7 visibles | 15+ colonnes : Nom, Code, Statut, Client, Contrat, Facturable, Entite, Chef de projet, Budget, Heures planifiees, Heures consommees, Marge %, Date debut, Date fin, Derniere mise a jour |

#### **REC-17 : Filtres avances avec pills dans la List View**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Filtres | 4 filtres basiques (Quick filter %, Status, Billable, Entity) | 10+ filtres combinables avec pills |
| Operateurs | Filtre simple, pas d'operateurs | Multi-selection par filtre (ex : Status = Active OU Completed) |
| Sauvegarde | Pas de sauvegarde | Filtres favoris enregistrables et partageables |
| Combinaison | Un filtre a la fois | Tous les filtres combinables (AND) |

**Filtres proposes pour la List View Projets :**

| Filtre | Type | Valeurs |
|--------|------|---------|
| Statut | Multi-select | Active, Completed, Suspended, Archived |
| Type | Multi-select | Client, Administratif, Departemental |
| Facturable | Toggle | Oui / Non / Tous |
| Entite | Multi-select | Provencher Roy Prod, PRAA |
| Chef de projet | Recherche + select | Liste des collaborateurs |
| Client | Recherche + select | Liste des clients |
| Periode | Date range | Date debut - Date fin |
| Marge | Range slider | 0% - 100%+ |
| Budget (heures) | Range slider | 0h - 10000h |
| Tags | Multi-select | Tags personnalisables |

#### **REC-18 : Export depuis la List View**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Export | Non observe dans le module Projects | Export CSV, Excel, PDF avec les colonnes et filtres actifs |
| Contenu | N/A | Export des donnees visibles (filtrees) ou de toutes les donnees |
| Format | N/A | CSV (comptabilite), Excel (analyse), PDF (rapport) |

### 3.3 Vue tableur (Worksheet View)

#### **REC-19 : Inline editing ameliore dans le Worksheet**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Edition | Cellules editables mais avec rechargement | Edition inline instantanee, navigation Tab/Enter |
| Types de cellules | Champ texte generique pour toutes les colonnes | Cellules typees : texte, nombre, date (date picker), select (dropdown), toggle |
| Validation | Validation au submit | Validation en temps reel au blur |
| Copier/coller | Basique | Support du copier/coller multi-cellules (type tableur Excel) |
| Formules | Pas de formules | Cellules calculees automatiquement (ex : Marge = Revenue - Cost) |

### 3.4 Profil de projet et KPIs

#### **REC-20 : Dashboard cards pour les KPIs du profil projet**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| KPIs | 4 blocs textuels (BUDGET, EFFORT, BILLINGS, MARGIN) avec sous-valeurs | 4 cards visuelles avec valeur principale, tendance, graphique sparkline |
| Presentation | Texte brut avec labels en majuscules | Cards avec icone, valeur grande, sous-label, indicateur de tendance |
| Interactivite | Statique | Click sur une card navigue vers le detail (ex : click sur "Effort" ouvre la ventilation des heures) |
| Graphiques | Aucun graphique | Sparklines dans chaque card (tendance sur 6 mois) |
| Comparaison | Pas de comparaison temporelle | Indicateur vs periode precedente ou vs budget previsionnel |

**Wireframe des KPI cards projet :**

```
┌──────────────────────────────────────────────────────────────────────┐
│  250029 Intelligence Artificielle                        ● Active   │
│  Client : Provencher Roy  |  Chef de projet : M. Belanger          │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐  ┌───────┐│
│  │ 💰 BUDGET     │  │ ⏱ EFFORT      │  │ 📄 FACTURE    │  │ 📊 MARGE│
│  │               │  │               │  │               │  │       ││
│  │  882 350 CAD  │  │  1 565h       │  │  1 110 469 $  │  │ 32.4% ││
│  │  Cout: 597K   │  │  Plan: 40h    │  │  Dispo: 0 $   │  │       ││
│  │  ▓▓▓▓▓▓▓░ 72% │  │  ↗ +12%      │  │  ↗ +8%        │  │  ↗    ││
│  │  ∿∿∿∿∿∿∿∿     │  │  ∿∿∿∿∿∿∿∿     │  │  ∿∿∿∿∿∿∿∿     │  │∿∿∿∿  ││
│  └───────────────┘  └───────────────┘  └───────────────┘  └───────┘│
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

#### **REC-21 : Work locations UX amelioree**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Presentation | Liste de noms de provinces en texte brut | Carte du Canada interactive avec provinces surlignees |
| Selection | Checkboxes dans un formulaire | Clic sur la province directement sur la carte + recherche textuelle |
| Indicateur visuel | Pas d'indicateur | Provinces colorees selon le volume de travail (heatmap) |
| Tags | Pas de tags visuels | Tags colores sous la carte listant les provinces actives |
| Default | Texte "Default work location: Quebec" | Province par defaut surlignee differemment + badge "Defaut" |

### 3.5 Structure WBS

#### **REC-22 : Numerotation automatique WBS**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Numerotation | Semi-manuelle : "01.", "01.1", "01.2" saisis dans le nom de la tache | Automatique : numerotation generee selon la position dans l'arborescence |
| Renumerotation | Pas de renumerotation : si on insere entre 01.1 et 01.2, il faut renommer manuellement | Renumerotation automatique lors de l'insertion, du deplacement ou de la suppression |
| Format | `XX.Y` (2 niveaux sous le projet) | `XX.Y.Z.W` configurable (separateur configurable : ".", "-", aucun) |
| Prefixe | Pas de prefixe de phase | Prefixe de phase optionnel (ex : "ESQ", "DDE", "DCE" pour les phases d'architecture) |

#### **REC-23 : Niveaux WBS illimites (vs 3 dans ChangePoint)**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Niveaux | 3 niveaux observes (Projet > Phase/WBS > Tache), 4 theoriques | Niveaux illimites (recommande max 6 pour la lisibilite) |
| Indentation | Indentation faible, niveaux difficiles a distinguer | Indentation de 24px par niveau avec ligne verticale de guidage |
| Distinction | Icone differente par niveau (3 icones) | Icone + couleur + indentation + numerotation |

#### **REC-24 : Templates WBS**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Templates | Inexistant : chaque projet est structure manuellement | Bibliotheque de templates WBS reutilisables |
| Types | N/A | Templates par type de projet d'architecture : Batiment neuf, Renovation, Amenagement interieur, Urbanisme |
| Contenu | N/A | Structure WBS pre-definie avec phases standard : Esquisse (ESQ), Avant-Projet Sommaire (APS), Avant-Projet Definitif (APD), Dossier de Consultation des Entreprises (DCE), Visa, Direction de l'Execution des Travaux (DET), Reception |
| Application | N/A | Bouton "Appliquer un template" lors de la creation de projet ou a tout moment |
| Personnalisation | N/A | Templates editables par un administrateur, possibilite de creer des templates a partir de projets existants |

### 3.6 Vue Gantt (NOUVELLE)

#### **REC-25 : Vue Gantt interactive**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Vue Gantt | Inexistante dans l'instance auditee | Vue Gantt native liee a la structure WBS |
| Barres | N/A | Barres de taches colorees selon le statut, redimensionnables par drag & drop |
| Dependances | N/A | Fleches entre les taches pour les dependances (Fin-Debut, Debut-Debut, etc.) |
| Chemin critique | N/A | Surlignage automatique du chemin critique en rouge |
| Echelle de temps | N/A | Jour, Semaine, Mois, Trimestre (zoom) |
| Today | N/A | Ligne verticale rouge pour la date du jour |
| Scroll synchronise | N/A | Panel gauche (liste WBS) et panel droit (barres) avec scroll synchronise |
| Edition | N/A | Drag pour deplacer, drag des extremites pour redimensionner, double-clic pour editer |

**Wireframe Gantt :**

```
┌────────────────────────────────────────────────────────────────────────────┐
│  Projets > 250029 Intelligence Artificielle > Gantt                       │
│  [Jour] [Semaine] [Mois] [Trimestre]          [Aujourd'hui] [Filtres]     │
├──────────────────────────┬─────────────────────────────────────────────────┤
│  Tache                   │  Fev 2026              Mars 2026               │
│                          │  S9    S10   S11   S12  S13   S14   S15        │
├──────────────────────────┼─────────────────────────────────────────────────┤
│  01. Intelligence Art.   │  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   │
│  ├ 01.1 Comite IA        │  ████████████████░░░░░░░░                      │
│  ├ 01.2 Reflexion GPTs   │       ██████████████████░░░░░                  │
│  ├ 01.3 Dev App CV       │            ████████████████████████████████     │
│  ├ 01.4 Outils IA 3D     │                  ████████░░░░░                 │
│  ├ 01.5 Formation        │  ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░    │
│  ├ 01.6 Outils IA TI     │                        ████████                │
│  └ 01.7 Reflexion Atel.  │                              ████              │
│                          │              | (aujourd'hui)                     │
└──────────────────────────┴─────────────────────────────────────────────────┘
```

### 3.7 Tableau de bord projets (NOUVEAU)

#### **REC-26 : Tableau de bord global des projets**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Dashboard | Inexistant : pas de vue d'ensemble consolidee | Tableau de bord avec KPIs agreges, graphiques et alertes |
| KPIs | Disponibles uniquement par projet (profil individuel) | KPIs consolides multi-projets : nombre de projets actifs, budget total, heures totales, marge moyenne |
| Graphiques | Aucun graphique | Graphiques interactifs : repartition par statut (donut), evolution mensuelle (barres), marge par projet (barres horizontales) |
| Alertes | Pas d'alertes | Alertes visuelles : projets en depassement de budget, projets sans activite depuis 30j, projets proches de la date de fin |

**KPIs du tableau de bord projets :**

| KPI | Calcul | Tendance |
|-----|--------|----------|
| **Projets actifs** | Nombre de projets au statut "Active" | vs mois precedent |
| **Budget total** | Somme des budgets de tous les projets actifs | vs trimestre precedent |
| **Heures consommees** | Somme des heures saisies sur tous les projets actifs | vs semaine precedente |
| **Marge moyenne** | Moyenne ponderee des marges de tous les projets actifs | vs mois precedent |

**Graphiques proposes :**

| Graphique | Type | Donnees |
|-----------|------|---------|
| Repartition par statut | Donut / Pie chart | Nombre de projets par statut (Active, Completed, Suspended) |
| Evolution mensuelle | Bar chart empile | Heures consommees par mois, ventilees projet / non-projet |
| Top 10 projets par heures | Bar chart horizontal | Les 10 projets avec le plus d'heures consommees |
| Marge par projet | Bar chart horizontal trie | Marge % par projet, colore vert (>20%), orange (10-20%), rouge (<10%) |
| Burndown budget | Line chart | Budget restant vs temps ecoulé, par projet selectionne |

### 3.8 Work locations UX

#### (Couvert dans REC-21)

Rappel des points cles :
- Carte interactive du Canada avec provinces selectionnables
- Heatmap de repartition du travail par province
- Tags visuels colores sous la carte
- Province par defaut identifiee clairement (Quebec pour Provencher Roy)
- Integration avec les codes de travail (work codes) via un dropdown contextuel

---

## 4. Module Feuilles de Temps -- Recommandations

Ce module couvre la grille de saisie hebdomadaire, la sidebar Assignments, la navigation temporelle, le systeme de Pin, les notes de frais integrees, et les nouvelles vues (tableau de bord temps, calendrier).

### 4.1 Grille modernisee

#### **REC-27 : Debut de semaine configurable (lundi par defaut)**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Debut de semaine | Dimanche (convention nord-americaine), non configurable | Lundi par defaut (convention quebecoise/europeenne), configurable par l'administrateur |
| Affichage | "Sun 22, Mon 23, Tue 24..." | "Lun 24, Mar 25, Mer 26, Jeu 27, Ven 28, Sam 01, Dim 02" |
| Langue | Anglais uniquement | Francais par defaut, bilingue (FR/EN) configurable |
| Configuration | Pas de configuration | Parametre au niveau entite : lundi ou dimanche |

#### **REC-28 : Separation visuelle temps projet / non-projet**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Melange | Taches projet et temps non-projet melanges dans la meme liste | Deux sections visuellement separees avec en-tete de section |
| Distinction | Pas de distinction visuelle claire | Section "Projets" (fond blanc) et section "Temps non-projet" (fond legerement colore `#F8FAFC`) |
| Separateur | Aucun | Ligne separatrice avec label "Temps non-projet" et sous-total |
| Sous-totaux | Un seul total general | Sous-total "Projets", sous-total "Non-projet", total general |

**Wireframe de la grille modernisee :**

```
┌──────────────────────────────────────────────────────────────────────────┐
│  Feuille de temps -- Philippe Haumesser          Semaine du 24 fev 2026 │
│  [◀ Sem. prec.]  [Aujourd'hui]  [Sem. suiv. ▶]     [Soumettre] [Reset] │
├──────────────────────────────────────────────────────────────────────────┤
│  📌│ Tache               │ Projet        │ Lun │ Mar │ Mer │ Jeu │ Ven │ Sam │ Dim │ Total │
├────┼─────────────────────┼───────────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼───────┤
│  PROJETS                                                                                    │
├────┼─────────────────────┼───────────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼───────┤
│ 📌│ 01.1 Comite IA       │ 250029 Int.AI │ 4.0 │ 3.5 │ 4.0 │ 3.5 │ 4.0 │     │     │ 19.00 │
│ 📌│ 01.3 Dev App CV      │ 250029 Int.AI │ 3.5 │ 4.0 │ 4.0 │ 4.0 │ 3.0 │     │     │ 18.50 │
│   │ Coordination dossier │ 240008 ESG    │     │     │     │     │     │     │     │  0.00 │
├────┼─────────────────────┼───────────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼───────┤
│                                         │ Sous-total projets    │     │     │     │ 37.50 │
├────┼─────────────────────┼───────────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼───────┤
│  TEMPS NON-PROJET                       │     │     │     │     │     │     │     │       │
├────┼─────────────────────┼───────────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼───────┤
│   │ Formation externe    │ Non-projet    │     │     │     │     │     │     │     │  0.00 │
│   │ Vacances             │ Non-projet    │     │     │     │     │     │     │     │  0.00 │
├────┼─────────────────────┼───────────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼───────┤
│                                         │ Sous-total non-projet │     │     │     │  0.00 │
├────┼─────────────────────┼───────────────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼───────┤
│                          │ TOTAL         │ 7.5 │ 7.5 │ 8.0 │ 7.5 │ 7.0 │ 0.0 │ 0.0 │ 37.50 │
└────┴─────────────────────┴───────────────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴───────┘
```

#### **REC-29 : Cellules avec micro-interactions**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Saisie | Clic sur cellule, saisie numerique, pas de feedback | Clic sur cellule avec highlight bleu, saisie numerique avec validation instantanee |
| Feedback | Pas de feedback visuel | Cellule verte brievement apres sauvegarde, cellule rouge si erreur |
| Navigation | Pas de navigation clavier | Tab (suivante), Shift+Tab (precedente), Enter (ligne suivante), Escape (annuler) |
| Format | Nombres decimaux bruts (5.00) | Nombres decimaux avec 2 decimales, arrondi automatique (ex : "7" → "7.00") |
| Indication | Pas d'indication de total | Mini-barre de progression dans la cellule Total (vs objectif hebdomadaire) |

### 4.2 Sidebar Assignments repensee

#### **REC-30 : Sidebar Assignments avec recherche et groupes**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Contenu | Liste plate de toutes les taches assignees + 9 categories non-projet | Liste groupee par projet avec recherche en temps reel |
| Recherche | 3 boutons en haut (filtrer, liste, copier) sans champ de recherche | Champ de recherche en haut de la sidebar avec filtrage instantane |
| Groupes | Pas de groupes | Groupes par projet (expandables/collapsibles) + section "Non-projet" |
| Drag | Pas de drag | Drag depuis la sidebar vers la grille pour ajouter une tache |
| Favoris | Systeme de Pin dans la grille | Pin dans la sidebar + favoris persistants accessibles en haut |
| Recents | Pas de section recents | Section "Recemment utilises" en haut de la sidebar |

**Wireframe sidebar Assignments :**

```
┌────────────────────────────┐
│  Assignments               │
│  🔍 Rechercher...          │
├────────────────────────────┤
│                            │
│  RECEMMENT UTILISES        │
│  ├── 01.1 Comite IA        │
│  └── 01.3 Dev App CV       │
│                            │
│  FAVORIS ★                 │
│  ├── 01.1 Comite IA  📌    │
│  └── 01.3 Dev App CV 📌    │
│                            │
│  250029 INTELLIGENCE AI ▼  │
│  ├── 01.1 Comite IA        │
│  ├── 01.2 Reflexion GPTs   │
│  ├── 01.3 Dev App CV       │
│  ├── 01.4 Outils IA 3D    │
│  ├── 01.5 Formation        │
│  ├── 01.6 Outils IA TI    │
│  └── 01.7 Reflexion Atel.  │
│                            │
│  240008 ESG ▼              │
│  ├── Coordination dossier  │
│  ├── Redaction rapport     │
│  └── Rencontre             │
│                            │
│  TEMPS NON-PROJET ▼       │
│  ├── Formation externe     │
│  ├── Temps en banque       │
│  ├── Conge sans solde      │
│  ├── Vacances              │
│  ├── Maladie               │
│  ├── Ferie                 │
│  ├── Conges sociaux        │
│  ├── Pour RH - ICD         │
│  └── Pour RH - ILD         │
│                            │
└────────────────────────────┘
```

### 4.3 Navigation temporelle

#### **REC-31 : Selecteur de periode (semaine, mois)**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Navigation | Fleches precedent/suivant uniquement | Fleches + selecteur de date + mini-calendrier |
| Periode | Semaine uniquement | Toggle Semaine / Mois (vue mensuelle = nouvelle fonctionnalite) |
| Acces rapide | Pas de bouton "Aujourd'hui" clairement visible | Bouton "Aujourd'hui" en evidence + date picker pour aller a une semaine specifique |
| Plage | Non definie | 2 ans dans le passe, 1 an dans le futur |

**Mini-calendrier :**

```
┌────────────────────────────┐
│  ◀  Fevrier 2026       ▶  │
├────────────────────────────┤
│  Lu  Ma  Me  Je  Ve Sa Di │
│                         1  │
│   2   3   4   5   6  7  8 │
│   9  10  11  12  13 14 15 │
│  16  17  18  19  20 21 22 │
│ [23  24  25  26  27]28  1 │  ← semaine courante surlignee
│   2   3   4   5   6  7  8 │
└────────────────────────────┘
```

### 4.4 Systeme de Pin ameliore

#### **REC-32 : Groupes de pins et favoris persistants**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Pin | Icone bleue simple, un seul niveau | Pin avec drag & drop pour reordonner + groupes de pins |
| Groupes | Pas de groupes | Groupes personnalisables (ex : "Projet principal", "Admin", "Formation") |
| Persistance | Pin persiste entre les semaines | Pin + favoris persistants qui pre-remplissent chaque nouvelle semaine |
| Auto-pin | Pas d'auto-pin | Option "Epingler automatiquement les taches avec heures cette semaine" |
| Raccourci | Pas de raccourci | Clic sur icone pin ou raccourci `P` quand la tache est selectionnee |

### 4.5 Notes de frais integrees

#### **REC-33 : Formulaire inline de notes de frais**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Acces | Module Expenses separe, accessible depuis la barre de navigation | Onglet "Notes de frais" integre dans la feuille de temps de la semaine |
| Formulaire | Page separee avec de nombreux champs | Formulaire inline dans un panneau lateral ou modal |
| Champs | Projet, Categorie de depense, Vendor, Description, Nombre d'unites, Cout par unite, Total, Devise, Taux de change, Entite, Activity | Champs simplifies : Projet, Categorie, Description, Montant, Devise, Recu (upload photo) |
| Upload | Upload fichier carte de credit (batch) | Upload de recu photo (camera mobile ou fichier) + OCR pour pre-remplissage |
| Rapport | Creation de rapport d'expenses dans un formulaire separe | Generation automatique du rapport mensuel a partir des depenses saisies |

### 4.6 Tableau de bord temps (NOUVEAU)

#### **REC-34 : Tableau de bord personnel des temps**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Dashboard | Inexistant | Tableau de bord avec graphiques et statistiques personnelles |
| KPIs | Pas de KPIs temps | Heures cette semaine (vs objectif), heures ce mois, repartition projet/non-projet |
| Graphiques | Aucun | Graphique en barres des heures par semaine (12 dernieres semaines) |
| Alertes | Pas d'alertes | Alerte si total hebdomadaire < objectif, alerte si soumission en retard |

**KPIs du tableau de bord temps :**

| KPI | Calcul | Indicateur |
|-----|--------|------------|
| **Heures cette semaine** | Total heures saisies semaine courante | Barre de progression vs objectif (37.5h ou 40h) |
| **Heures ce mois** | Total heures saisies mois courant | vs moyenne mensuelle |
| **Taux de saisie** | Nombre de semaines soumises / nombre de semaines ecoulees (6 derniers mois) | Pourcentage avec couleur (vert >95%, orange 80-95%, rouge <80%) |
| **Repartition** | % heures projet vs % heures non-projet | Donut chart |
| **Top 5 projets** | 5 projets avec le plus d'heures ce mois | Bar chart horizontal |

### 4.7 Vue calendrier (NOUVELLE)

#### **REC-35 : Vue mensuelle des heures**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Vue calendrier | Inexistante | Vue calendrier mensuelle affichant le total d'heures par jour |
| Contenu par jour | N/A | Total heures + nombre de projets + indicateur de statut (soumis/non soumis) |
| Navigation | N/A | Fleches mois precedent/suivant + selecteur de mois |
| Code couleur | N/A | Vert (>=objectif journalier), Orange (partiel), Rouge (aucune heure), Gris (non ouvrable) |

**Wireframe vue calendrier :**

```
┌──────────────────────────────────────────────────────────────────────┐
│  Calendrier des heures -- Fevrier 2026                  [◀] [▶]    │
├──────┬──────┬──────┬──────┬──────┬──────┬──────┐
│  Lun │  Mar │  Mer │  Jeu │  Ven │  Sam │  Dim │
├──────┼──────┼──────┼──────┼──────┼──────┼──────┤
│      │      │      │      │      │      │  1   │
│      │      │      │      │      │      │  --  │
├──────┼──────┼──────┼──────┼──────┼──────┼──────┤
│  2   │  3   │  4   │  5   │  6   │  7   │  8   │
│ 7.50 │ 7.50 │ 8.00 │ 7.50 │ 7.00 │  --  │  --  │
│  ●●● │  ●●● │  ●●● │  ●●● │  ●●  │      │      │
├──────┼──────┼──────┼──────┼──────┼──────┼──────┤
│  9   │ 10   │ 11   │ 12   │ 13   │ 14   │ 15   │
│ 7.50 │ 7.50 │ 7.50 │ 7.50 │ 7.50 │  --  │  --  │
│  ●●● │  ●●● │  ●●● │  ●●● │  ●●● │      │      │
│  ✓   │  ✓   │  ✓   │  ✓   │  ✓   │      │      │
├──────┼──────┼──────┼──────┼──────┼──────┼──────┤
│ ...  │      │      │      │      │      │      │
└──────┴──────┴──────┴──────┴──────┴──────┴──────┘

Legende : ●●● = 3 projets   ✓ = semaine soumise   -- = non ouvrable
```

### 4.8 Work locations / codes UX

#### **REC-36 : Selection de work location contextualisee**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Selection | Liste deroulante avec noms de provinces en texte | Dropdown avec recherche + icone drapeau provincial |
| Default | "Default work location : Quebec" en texte | Province par defaut pre-selectionnee, modifiable par ligne |
| Granularite | Par projet | Par ligne de la feuille de temps (par tache) |
| Historique | Pas d'historique | Suggestion basee sur le dernier work location utilise pour cette tache |

---

## 5. Module Facturation -- Recommandations

Ce module couvre la liste des factures, le workflow de facturation visuel, les contrats et roles de facturation, la facturation hybride, et le nouveau tableau de bord facturation.

### 5.1 Liste factures modernisee

#### **REC-37 : Badges de statut colores (vs texte simple ChangePoint)**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Affichage statut | Texte noir simple dans une colonne "Status" | Badge pill colore avec dot et texte selon la palette semantique (10 statuts) |
| Lisibilite | Statuts difficiles a distinguer dans une longue liste | Scan visuel rapide grace aux couleurs distinctes par statut |
| Mapping couleurs | Pas de couleur | Draft (gris), Pending (orange), Approved (vert), Committed (violet), Sent (bleu), Paid (vert), Partially Paid (orange), Credited (rouge), Archived (gris), Overdue (rouge) |

**Mapping complet des 10 statuts avec badges :**

| # | Statut | Badge background | Badge texte | Dot | Icone |
|---|--------|-----------------|-------------|-----|-------|
| 1 | Draft | `#F1F5F9` | `#64748B` | `#94A3B8` | file-edit |
| 2 | Pending Approval | `#FFFBEB` | `#B45309` | `#F59E0B` | clock |
| 3 | Pending 2nd Approval | `#FFF7ED` | `#C2410C` | `#FB923C` | clock |
| 4 | Approved | `#F0FDF4` | `#15803D` | `#22C55E` | check-circle |
| 5 | Committed | `#EDE9FE` | `#6D28D9` | `#8B5CF6` | lock |
| 6 | Sent | `#EFF6FF` | `#1D4ED8` | `#3B82F6` | send |
| 7 | Paid | `#F0FDF4` | `#15803D` | `#22C55E` | dollar-sign |
| 8 | Partially Paid | `#FFFBEB` | `#B45309` | `#F59E0B` | dollar-sign |
| 9 | Credited | `#FEF2F2` | `#DC2626` | `#EF4444` | file-minus |
| 10 | Archived | `#F1F5F9` | `#94A3B8` | `#CBD5E1` | archive |

#### **REC-38 : Quick actions sur les factures**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Actions | Clic sur la facture pour ouvrir le detail, puis actions depuis le detail | Actions rapides directement depuis la liste via un menu "..." |
| Menu | Pas de menu contextuel | Menu contextuel (3 dots) par facture : Voir, Editer, Soumettre, Approuver, Dupliquer, Telecharger PDF, Supprimer |
| Actions conditionnelles | N/A | Actions filtrees selon le statut (ex : "Approuver" visible uniquement si Pending, "Supprimer" uniquement si Draft) |
| Actions bulk | Pas d'actions groupees | Selection multiple + barre d'actions : "Approuver tout", "Exporter", "Archiver" |

### 5.2 Workflow facturation VISUEL

#### **REC-39 : Pipeline kanban avec colonnes = statuts**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Visualisation | Liste plate avec colonne statut en texte | Vue Kanban avec colonnes correspondant aux statuts du workflow |
| Colonnes | N/A | Draft | Pending | Approved | Committed | Sent | Paid (+ Partially Paid, Credited, Archived en colonnes optionnelles) |
| Cartes | N/A | Carte par facture : numero, client, montant, date echeance, responsable |
| Compteurs | Pas de compteur | Nombre de factures + montant total par colonne |

#### **REC-40 : Drag & drop entre statuts dans le Kanban**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Transition statut | Modification manuelle du statut via dropdown dans le formulaire | Drag & drop d'une carte d'une colonne a l'autre |
| Contraintes | Pas de visualisation des transitions autorisees | Transitions non autorisees : drop refuse + animation de retour + toast "Transition non autorisee : une facture Sent ne peut pas revenir a Draft" |
| Workflow | Implicite | Fleches visuelles entre colonnes montrant les transitions possibles |
| Confirmation | Pas de confirmation systematique | Modale de confirmation pour les transitions importantes (ex : Commit, Send) |

**Transitions autorisees (matrice) :**

| De \ Vers | Draft | Pending | Pending 2nd | Approved | Committed | Sent | Paid | Part. Paid | Credited | Archived |
|-----------|-------|---------|-------------|----------|-----------|------|------|------------|----------|----------|
| **Draft** | -- | ✓ | | | | | | | | |
| **Pending** | ✓ (rejet) | -- | ✓ | ✓ | | | | | | |
| **Pending 2nd** | ✓ (rejet) | | -- | ✓ | | | | | | |
| **Approved** | | | | -- | ✓ | | | | | |
| **Committed** | | | | | -- | ✓ | | | ✓ | |
| **Sent** | | | | | | -- | ✓ | ✓ | ✓ | |
| **Paid** | | | | | | | -- | | ✓ | ✓ |
| **Part. Paid** | | | | | | | ✓ | -- | ✓ | |
| **Credited** | | | | | | | | | -- | ✓ |
| **Archived** | | | | | | | | | | -- |

#### **REC-41 : Compteurs par statut dans le Kanban**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Compteurs | Pas de compteur | En-tete de chaque colonne : nombre de factures (N) + montant total ($ CAD) |
| Urgence | Pas d'indicateur d'urgence | Compteur rouge pour les factures en retard, badge "Overdue" sur les cartes depassant l'echeance |

### 5.3 Contrats et roles de facturation

#### **REC-42 : Tableau editable inline pour les Billing Roles**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Presentation | Grille avec colonnes Role, Standard Rate, Discount %, Billing Rate, Currency | Tableau editable inline avec calcul en temps reel |
| Edition | Clic sur une cellule, saisie, sauvegarde par bouton | Clic sur cellule, saisie, calcul automatique du Billing Rate, sauvegarde auto |
| Ajout | Bouton "Add" ouvre un formulaire | Bouton "+ Ajouter un role" ajoute une ligne editable directement dans le tableau |
| Historique | Pas d'historique visible | Icone "Historique" par ligne affichant les modifications de taux avec dates |

**Wireframe tableau Billing Roles :**

```
┌──────────────────────────────────────────────────────────────────────────┐
│  Roles de facturation -- Contrat 200236 Place des Arts [PRA]            │
│                                                        [+ Ajouter role] │
├──────────────────────┬────────────┬──────────┬────────────┬─────┬───────┤
│  Role                │ Taux std.  │ Remise % │ Taux fact. │ Dev │ Hist. │
├──────────────────────┼────────────┼──────────┼────────────┼─────┼───────┤
│  Architecte junior   │   63.40 $  │   0.00%  │   63.40 $  │ CAD │  📋  │
│  Architecte interm.  │   77.00 $  │   0.00%  │   77.00 $  │ CAD │  📋  │
│  Architecte senior   │   92.10 $  │   0.00%  │   92.10 $  │ CAD │  📋  │
│  Architecte patron   │  150.85 $  │   0.00%  │  150.85 $  │ CAD │  📋  │
├──────────────────────┴────────────┴──────────┴────────────┴─────┴───────┤
│  Ratio patron/junior : 2.38x                                           │
└──────────────────────────────────────────────────────────────────────────┘
```

#### **REC-43 : Override par ressource avec indicateur visuel**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Override | Observe (Melissa Belanger : Standard Rate 0.00 mais Billing Rate 150.85) | Systeme d'override structure : taux par defaut du role + surcharge optionnelle par collaborateur |
| Indicateur | Pas d'indicateur visuel de surcharge | Badge "Override" a cote du nom du collaborateur quand un taux specifique est applique |
| Configuration | Configuration obscure | Modale de surcharge : "Ce collaborateur a un taux specifique different du taux du role" avec comparaison cote a cote |

### 5.4 Facturation hybride UX

#### **REC-44 : Toggle Fixed Fee / Hourly / Mixed**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Selection | Champ "Billing Type" dans le formulaire du contrat avec dropdown | Toggle visuel a 3 options avec description et icone pour chaque type |
| Types | Time and Materials, Fixed Fee, Mixed - Fixed Fee/Hourly, Non-billable | Horaire (Time & Materials), Forfait (Fixed Fee), Mixte (Mixed), Non facturable |
| Adaptation UI | Meme formulaire quel que soit le type | Le formulaire s'adapte au type selectionne : section "Taux horaires" pour Horaire, section "Jalons" pour Forfait, les deux pour Mixte |

**Toggle de type de facturation :**

```
┌──────────────────────────────────────────────────────────────────┐
│  Type de facturation                                             │
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌────────┐│
│  │ ⏱ Horaire   │  │ 📋 Forfait  │  │ ⚡ Mixte    │  │ ⊘ N/A  ││
│  │ Time & Mat. │  │ Fixed Fee   │  │ Fee + Hour. │  │ Non    ││
│  │             │  │             │  │ ▇▇▇▇▇       │  │ fact.  ││
│  └─────────────┘  └─────────────┘  └─────────────┘  └────────┘│
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

#### **REC-45 : Section jalons avec timeline visuelle (Fixed Fees)**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Jalons | Liste plate avec dates et montants dans le detail du contrat | Timeline visuelle avec jalons positionnes chronologiquement |
| Statut jalon | Pas d'indicateur de statut par jalon | Badges : "A venir", "Facture", "Paye" pour chaque jalon |
| Progression | Pas d'indicateur de progression | Barre de progression montrant le pourcentage des jalons factures vs total contractuel |
| Ajout | Formulaire separe | Ajout inline de jalon : date, montant, description |

**Wireframe timeline jalons (contrat 200236 Place des Arts) :**

```
┌──────────────────────────────────────────────────────────────────────────┐
│  Jalons de facturation -- Contrat 200236                                 │
│  Total forfaits : 114 294.39 CAD    Facture : 114 294.39 CAD (100%)     │
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ 100%             │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Jan 2023         Sep 2023              Jan 2024                         │
│  ────●──────────────●●──────────────────●●────────────→                  │
│      │              ││                  ││                               │
│  22 573 $       865 $  8 650 $     64 706 $  17 500 $                   │
│  ● Paye         ● Paye  ● Paye    ● Paye    ● Paye                     │
│                                                                          │
│                                                      [+ Ajouter jalon]  │
└──────────────────────────────────────────────────────────────────────────┘
```

### 5.5 Tableau de bord facturation (NOUVEAU)

#### **REC-46 : Tableau de bord facturation avec KPIs et graphiques**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Dashboard | Inexistant : pas de vue consolidee de la facturation | Tableau de bord avec KPIs, graphiques et alertes |
| KPIs | Disperses dans les profils de projets individuels | KPIs consolides : facture total, paye, en retard, marge globale |
| Graphiques | Aucun | Graphiques interactifs : evolution mensuelle, repartition par statut, delai moyen de paiement |
| Alertes | Pas d'alertes | Liste des factures en retard, factures en attente d'approbation, echeances a venir (7 jours) |

**KPIs du tableau de bord facturation :**

| KPI | Calcul | Couleur de tendance |
|-----|--------|---------------------|
| **Facture (YTD)** | Somme des factures emises depuis le 1er janvier | Bleu, comparaison vs N-1 |
| **Paye (YTD)** | Somme des paiements recus depuis le 1er janvier | Vert, comparaison vs N-1 |
| **En retard** | Somme des montants depassant l'echeance de paiement | Rouge, nombre de factures |
| **Marge globale** | (Revenue total - Cost total) / Revenue total x 100 | Vert si >20%, Orange si 10-20%, Rouge si <10% |
| **Delai moyen de paiement** | Moyenne des jours entre envoi et paiement (12 derniers mois) | Jours, comparaison vs objectif (30 jours) |

**Graphiques proposes :**

| Graphique | Type | Donnees |
|-----------|------|---------|
| **Evolution mensuelle** | Bar chart empile | Facture vs Paye par mois (12 derniers mois) |
| **Repartition par statut** | Donut chart | Nombre et montant par statut (Draft, Pending, Sent, Paid, Overdue) |
| **Delai de paiement** | Line chart | Evolution du delai moyen de paiement par mois |
| **Top 10 clients** | Bar chart horizontal | Montant facture par client (top 10) |
| **Aging report** | Stacked bar | Montants impayes ventiles par tranche (0-30j, 31-60j, 61-90j, >90j) |

**Wireframe tableau de bord facturation :**

```
┌──────────────────────────────────────────────────────────────────────────┐
│  Tableau de bord Facturation                                Fev 2026    │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐  ┌───────────┐│
│  │ 💰 FACTURE    │  │ ✓  PAYE       │  │ ⚠ EN RETARD   │  │ 📊 MARGE  ││
│  │               │  │               │  │               │  │           ││
│  │ 1 245 000 $   │  │   982 000 $   │  │   128 500 $   │  │   28.4%   ││
│  │ ↗ +15% vs N-1 │  │ ↗ +12% vs N-1 │  │ 6 factures    │  │ ↗ +2.1%  ││
│  └───────────────┘  └───────────────┘  └───────────────┘  └───────────┘│
│                                                                          │
│  ┌─────────────────────────────────┐  ┌─────────────────────────────────┐│
│  │  Evolution mensuelle            │  │  Repartition par statut         ││
│  │  ┌─┐┌─┐┌─┐┌─┐┌─┐┌─┐           │  │         ┌──────┐                ││
│  │  │ ││ ││ ││ ││ ││ │           │  │      ┌──┤ Paye │──┐             ││
│  │  │ ││ ││ ││ ││ ││ │           │  │   ┌──┤  │ 45%  │  ├──┐          ││
│  │  │ ││ ││ ││ ││ ││ │           │  │   │  └──┤      ├──┘  │          ││
│  │  └─┘└─┘└─┘└─┘└─┘└─┘           │  │   │     └──────┘     │          ││
│  │  Sep Oct Nov Dec Jan Fev        │  │   Sent 25%    Pending 15%      ││
│  └─────────────────────────────────┘  └─────────────────────────────────┘│
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────────┐│
│  │  Factures en retard (6)                                  [Voir tout]││
│  │  FAC-042  ACME Corp       12 500 $  Retard: 15 jours   [Relancer]  ││
│  │  FAC-038  Martin SA        8 200 $  Retard: 32 jours   [Relancer]  ││
│  │  FAC-035  SQI             22 300 $  Retard:  8 jours   [Relancer]  ││
│  └──────────────────────────────────────────────────────────────────────┘│
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

### 5.6 KPIs financiers

#### **REC-47 : Dashboard cards financiers avec tendances**

| Aspect | ChangePoint (avant) | OOTI (cible) |
|--------|---------------------|--------------|
| Presentation | KPIs textuels dans le profil de chaque projet (BUDGET, EFFORT, BILLINGS, MARGIN) | Dashboard cards avec valeur principale, sparkline, indicateur de tendance |
| Agregation | Par projet uniquement, pas de vue consolidee | Par projet + consolide (tous projets, par entite, par client) |
| Comparaison | Pas de comparaison temporelle | Comparaison vs mois precedent, trimestre precedent, annee precedente |
| Alertes | Pas d'alertes | Seuils configurables : alerte si marge < 15%, alerte si depassement budget > 10% |
| Drill-down | Pas de drill-down | Clic sur un KPI ouvre le detail avec ventilation par projet/phase/tache |

---

## Index des recommandations -- Partie 1

| Ref | Recommandation | Module | Section |
|-----|---------------|--------|---------|
| REC-01 | Remplacer le wildcard "%" par une recherche intelligente | Transversal | 2.2 |
| REC-02 | Filtres combinables avec pills | Transversal | 2.2 |
| REC-03 | Validation en temps reel | Transversal | 2.3 |
| REC-04 | Auto-save | Transversal | 2.3 |
| REC-05 | Inline editing | Transversal | 2.3 |
| REC-06 | Toast notifications | Transversal | 2.4 |
| REC-07 | Badges de notification | Transversal | 2.4 |
| REC-08 | Indicateur de sauvegarde | Transversal | 2.4 |
| REC-09 | Drag & drop pour la reorganisation WBS | Transversal | 2.5 |
| REC-10 | Kanban facturation avec drag & drop | Transversal | 2.5 |
| REC-11 | Drag & drop pour le reorder des pins | Transversal | 2.5 |
| REC-12 | Raccourcis clavier globaux et contextuels | Transversal | 2.6 |
| REC-13 | Tree View interactive avec drag & drop | Projets | 3.1 |
| REC-14 | Inline rename dans la Tree View | Projets | 3.1 |
| REC-15 | Multi-selection dans la Tree View | Projets | 3.1 |
| REC-16 | Colonnes configurables dans la List View | Projets | 3.2 |
| REC-17 | Filtres avances avec pills dans la List View | Projets | 3.2 |
| REC-18 | Export depuis la List View | Projets | 3.2 |
| REC-19 | Inline editing ameliore dans le Worksheet | Projets | 3.3 |
| REC-20 | Dashboard cards pour les KPIs du profil projet | Projets | 3.4 |
| REC-21 | Work locations UX amelioree | Projets | 3.4 |
| REC-22 | Numerotation automatique WBS | Projets | 3.5 |
| REC-23 | Niveaux WBS illimites | Projets | 3.5 |
| REC-24 | Templates WBS | Projets | 3.5 |
| REC-25 | Vue Gantt interactive | Projets | 3.6 |
| REC-26 | Tableau de bord global des projets | Projets | 3.7 |
| REC-27 | Debut de semaine configurable | Temps | 4.1 |
| REC-28 | Separation visuelle temps projet / non-projet | Temps | 4.1 |
| REC-29 | Cellules avec micro-interactions | Temps | 4.1 |
| REC-30 | Sidebar Assignments avec recherche et groupes | Temps | 4.2 |
| REC-31 | Selecteur de periode (semaine, mois) | Temps | 4.3 |
| REC-32 | Groupes de pins et favoris persistants | Temps | 4.4 |
| REC-33 | Formulaire inline de notes de frais | Temps | 4.5 |
| REC-34 | Tableau de bord personnel des temps | Temps | 4.6 |
| REC-35 | Vue mensuelle des heures (calendrier) | Temps | 4.7 |
| REC-36 | Selection de work location contextualisee | Temps | 4.8 |
| REC-37 | Badges de statut colores pour les factures | Facturation | 5.1 |
| REC-38 | Quick actions sur les factures | Facturation | 5.1 |
| REC-39 | Pipeline kanban avec colonnes = statuts | Facturation | 5.2 |
| REC-40 | Drag & drop entre statuts dans le Kanban | Facturation | 5.2 |
| REC-41 | Compteurs par statut dans le Kanban | Facturation | 5.2 |
| REC-42 | Tableau editable inline pour les Billing Roles | Facturation | 5.3 |
| REC-43 | Override par ressource avec indicateur visuel | Facturation | 5.3 |
| REC-44 | Toggle Fixed Fee / Hourly / Mixed | Facturation | 5.4 |
| REC-45 | Section jalons avec timeline visuelle | Facturation | 5.4 |
| REC-46 | Tableau de bord facturation avec KPIs et graphiques | Facturation | 5.5 |
| REC-47 | Dashboard cards financiers avec tendances | Facturation | 5.6 |

---

> **Fin de la Partie 1** -- La Partie 2 (sections 6 a 10) couvrira : Responsive et adaptation mobile, Accessibilite (WCAG), Performance percue, Composants avances, et Wireframes cles.

---

*Document genere le 27 fevrier 2026 -- Audit Planview ChangePoint (instance Provencher Roy) -- Application cible OOTI*
