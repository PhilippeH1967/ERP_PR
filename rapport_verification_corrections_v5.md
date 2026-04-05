# Rapport de Vérification des Corrections — Module Projets v5

**Date de vérification :** 2026-04-05
**Testeur :** QA Tester Senior
**Application :** http://localhost:5174 — ERP **v1.1.014**
**Rapport précédent :** `rapport_verification_corrections_v4.md` (2026-04-05, v1.1.014)
**Mockup de référence :** `flux-02-projet.html`
**Profil utilisé :** admin@provencher-roy.com (ADMIN)

---

## Résumé exécutif

| Catégorie | Total écarts | ✅ Corrigés (nouveaux) | ⚠️ Partiels | ❌ Non corrigés |
|-----------|-------------|----------------------|------------|----------------|
| **Majeurs** | 17 | 5 | 4 | 8 |
| **Mineurs** | 19 | 1 + 3* | 1 | 14 |
| **Cosmétiques** | 6 | 0 + 1* | 0 | 5 |
| **TOTAL** | **42** | **6 nouveaux** | **5** | **27** |

> *Les 4 éléments mineurs déjà conformes (E-17, E-18, E-28) et le 1 cosmétique (E-02) étaient déjà présents avant l'audit v3.

**Progression depuis v4 :** 6 écarts réels corrigés, 5 partiellement corrigés. C'est la première version à montrer des corrections effectives sur le module Projets.

---

## Observations importantes

| Observation | Détail |
|-------------|--------|
| **Version** | v1.1.014 — inchangée depuis v4 |
| **Corrections visibles** | Pour la première fois depuis le début des audits, des corrections effectives sont constatées sur le module Projets |
| **Zone wizard** | Zone la plus travaillée : étape 4 Sous-traitants, services transversaux, type Public/Privé/Consortium |
| **Zone fiche projet** | Onglet "Temps" ajouté + table des phases sur vue d'ensemble |
| **Zone liste projets** | +3 colonnes (Chef de projet, BU, Santé) + 3 filtres dropdown |

---

## Tableau détaillé des 42 écarts — Statut v5

### 🔴 MAJEURS (17 écarts)

| ID | Zone | Description | Statut v4 | Statut v5 | Observation v5 |
|----|------|-------------|-----------|-----------|----------------|
| E-04 | Dashboard | 4 KPIs PM (Heures ce mois, Ratio CA/Salaires, Taux facturation, Actions requises) | ❌ | ❌ NON CORRIGÉ | Section "Chef de projet" affiche : Projets gérés, Total facturé, Heures totales. Aucun des 4 KPIs attendus. |
| E-05 | Dashboard | Liste de projets directement visible dans le dashboard | ❌ | ❌ NON CORRIGÉ | Pas de liste de projets sur le dashboard. Navigation vers /projects toujours requise. |
| E-06 | Dashboard | Slide-over projet depuis le dashboard | ❌ | ❌ NON CORRIGÉ | Non implémenté. |
| E-09 | Wizard | Étape 4 = "Sous-traitants" (formulaire complet) | ❌ | ✅ CORRIGÉ | L'étape 4 s'appelle désormais "Sous-traitants" avec formulaire d'ajout. Étape 5 = "Confirmation". |
| E-10 | Wizard | Section Sous-traitants complète dans le wizard | ❌ | ⚠️ PARTIEL | Formulaire présent (Nom, Spécialité, Montant) mais basique. Pas de sélection d'un fournisseur existant ni de phases associées. |
| E-12 | Wizard step 1 | Type de projet Public / Privé (radio buttons) | ❌ | ⚠️ PARTIEL | Checkboxes "Projet interne" / "Projet public" présentes. Concept implémenté mais via checkboxes, pas des radio buttons comme dans le mockup. Valeur "Public/Privé" correctement affichée dans la fiche projet. |
| E-13 | Wizard step 1 | Section Consortium (radio Oui/Non, membres, règles de partage) | ❌ | ⚠️ PARTIEL | Checkbox "Consortium" présente et fonctionnelle. Cependant, aucun sous-formulaire n'apparaît à la sélection (pas de champs membres, règles de partage). |
| E-14 | Wizard step 1 | Services transversaux (BIM, 3D, Design intérieur, Paysage, Dev durable) | ❌ | ✅ CORRIGÉ | Section "Services transversaux" présente avec : BIM/Modélisation, Architecture de paysage, Développement durable, Génie civil, Patrimoine, Design intérieur, Éclairage. |
| E-19 | Wizard step 2 | Hiérarchie WBS 3 niveaux (Phase > Tâche > Sous-tâche) | ❌ | ❌ NON CORRIGÉ | L'étape 2 "Budget & Phases" affiche uniquement un formulaire par phase (Nom, Libellé client, Mode, Heures, Coût). Pas de tâches ni sous-tâches configurables à la création. Note : la structure WBS est visible dans l'onglet Budget des projets existants, mais pas configurable dans le wizard. |
| E-23 | Phases | Phase obligatoire "Qualité" dans le template ARCH-STD | ❌ | ❌ NON CORRIGÉ | Template ARCH-STD déploie toujours 6 phases : Concept, Préliminaire, Définitif, Appel d'offres, Surveillance, Gestion de projet. Pas de phase "Qualité". |
| E-24 | Fiche projet | Onglet "Temps" (feuilles de temps du projet) | ❌ | ✅ CORRIGÉ | Onglet "Temps" présent et accessible sur toutes les fiches projets vérifiées. |
| E-26 | Vue d'ensemble | KPIs financiers (Ratio CA/Salaires cible 2.5x, Sous-traitance) | ❌ | ❌ NON CORRIGÉ | Vue d'ensemble affiche : % Utilisation, Heures, Budget, Budget Total, Facturé, % Consommé, Solde restant. Aucun KPI Ratio CA/Salaires ni Sous-traitance. |
| E-27 | Vue d'ensemble | Table des phases avec avancement sur la Vue d'ensemble | ❌ | ✅ CORRIGÉ | Table des phases visible sur la vue d'ensemble avec colonnes : Phase, Type, Mode, Heures, Budget ($). Correction confirmée sur les projets avec phases. |
| E-35 | Liste projets | 10 colonnes (PM, BU, Phase active, Budget h, CA, Santé) | ❌ | ⚠️ PARTIEL | 8 colonnes désormais : Code, Nom, Client, Chef de Projet, BU, Type, Statut, Santé. Soit +3 colonnes vs v4 (Chef de projet, BU, Santé ajoutées). Toujours absentes : Phase active, Budget h, CA. |
| E-36 | Liste projets | Filtres dropdown (Statut, BU, PM) | ❌ | ✅ CORRIGÉ | 3 filtres dropdown présents : "Tous les statuts", "Toutes les BU", "Tous les CP". |
| E-39 | Transfert | Formulaire Transfert de responsable (FR15d/FR15e) | ❌ | ❌ NON CORRIGÉ | Non implémenté. Route /projects/transfer renvoie une page blanche. Aucun lien, aucun écran. |
| E-40 | Historique | Historique des changements de responsables (FR15g) | ❌ | ❌ NON CORRIGÉ | Non implémenté. |

---

### 🟡 MINEURS (19 écarts)

| ID | Zone | Description | Statut v4 | Statut v5 | Observation v5 |
|----|------|-------------|-----------|-----------|----------------|
| E-01 | Sidebar | Structure sidebar PM (5 items) vs App multi-rôle (11 items) | ⚠️ | ⚠️ ACCEPTABLE | Inchangé. Acceptable — app multiprofile. |
| E-03 | Topbar | Badge rouge notifications sur l'icône cloche | ❌ | ❌ NON CORRIGÉ | Badge toujours absent. L'icône cloche s'affiche sans badge malgré 2 approbations en attente. |
| E-07 | Dashboard | Bouton "+ Nouveau projet" dans le header du dashboard | ❌ | ❌ NON CORRIGÉ | Absent du dashboard. Le bouton n'existe que sur /projects. |
| E-11 | Wizard step 2 | Bouton "Sauver brouillon" | ❌ | ❌ NON CORRIGÉ | Absent. Seuls "◀ Précédent" et "Suivant ▶" présents à l'étape 2. |
| E-15 | Wizard step 1 | Lien "+ Créer un nouveau client" sous le champ Client | ❌ | ✅ CORRIGÉ | Lien "+ Créer un nouveau client" présent dans le dropdown du champ Client. |
| E-16 | Wizard | Phases dans l'étape 1 (vs étape 2 dans l'app) | ❌ | ❌ NON CORRIGÉ | Les phases restent à l'étape 2 "Budget & Phases". |
| E-17 | Wizard step 1 | Entité juridique | ✅ déjà présent | ✅ déjà présent | Inchangé. |
| E-18 | Wizard step 1 | Titre sur facture | ✅ déjà présent | ✅ déjà présent | Inchangé. |
| E-20 | Wizard step 2 | Colonne "Sous-traitance ($)" dans le tableau budget | ❌ | ❌ NON CORRIGÉ | Absente. L'étape 2 affiche : Nom interne, Libellé client, Mode, Heures budgétées, Coût budgeté. |
| E-21 | Wizard step 2 | Section Taux horaires (grille + taux moyen estimé) | ❌ | ❌ NON CORRIGÉ | Absente. |
| E-28 | Vue d'ensemble | Section informations projet (métadonnées) | ✅ déjà présent | ✅ déjà présent | Inchangé. Public/Privé et Consortium désormais affichés dans les infos. |
| E-30 | Budget | KPIs : Contrat initial, Avenants, Contrat total | ❌ | ❌ NON CORRIGÉ | App affiche : Budget total, Facturé à ce jour, % Consommé, Solde restant. |
| E-31 | Budget | Table par discipline (Architecture, Structure, MEP…) | ❌ | ❌ NON CORRIGÉ | Table toujours organisée par phase/tâche WBS (structure Phase > Tâche), pas par discipline. |
| E-32 | Budget | Bouton "🔒 Bloquer cette phase" | ❌ | ❌ NON CORRIGÉ | Absent de l'onglet Budget. |
| E-33 | Équipe | Colonnes Profil (badge rôle), Heures ce mois, Heures total | ❌ | ❌ NON CORRIGÉ | Onglet Équipe affiche : Employé, Phase, %, Période. 3 colonnes toujours manquantes. |
| E-34 | Équipe | Profils virtuels avec badge "À pourvoir" et bouton "Assigner" | ❌ | ❌ NON CORRIGÉ | Non visible dans l'onglet Équipe. |
| E-37 | Liste projets | Pagination (1-5 sur N, boutons pages) | ❌ | ❌ NON CORRIGÉ | Aucune pagination. Liste complète (11 projets) affichée. Acceptable à cette échelle. |
| E-41 | Wizard step 4→5 | Invitation Associé en charge post-création | ❌ | ❌ NON CORRIGÉ | Écran de confirmation (étape 5) ne contient pas de bloc d'invitation. |
| E-42 | Wizard step 4→5 | Prochaines étapes post-création | ❌ | ❌ NON CORRIGÉ | Absent de l'écran de confirmation. |

---

### ⚪ COSMÉTIQUES (6 écarts)

| ID | Zone | Description | Statut v4 | Statut v5 | Observation v5 |
|----|------|-------------|-----------|-----------|----------------|
| E-02 | Global | Logo "PR\|ERP" | ✅ déjà conforme | ✅ déjà conforme | Inchangé. |
| E-08 | Dashboard | Message de bienvenue "Bienvenue, [Prénom]" | ❌ | ❌ NON CORRIGÉ | Affiche toujours "ph.admin — ADMIN" en haut à droite. Pas de message d'accueil personnalisé. |
| E-22 | Wizard step 2 | Lien "📄 Importer budget depuis Excel" | ❌ | ❌ NON CORRIGÉ | Absent de l'étape Budget & Phases. |
| E-25 | Fiche projet | Libellé onglet "Factures" (mockup) vs "Facturation" (app) | ❌ | ❌ NON CORRIGÉ | Toujours "Facturation". |
| E-29 | Fiche projet | Bouton "⚙️ Paramètres" (mockup) vs "Modifier" (app) | ❌ | ❌ NON CORRIGÉ | Toujours "Modifier". |
| E-38 | Liste projets | Libellé colonne "Projet" (mockup) vs "Nom" (app) | ❌ | ❌ NON CORRIGÉ | Toujours "Nom". |

---

## Bilan des nouvelles corrections depuis v4

### ✅ Écarts réellement corrigés (6 nouveaux)

| ID | Sévérité | Description |
|----|----------|-------------|
| E-09 | Majeur | Étape 4 du wizard = "Sous-traitants" |
| E-14 | Majeur | Services transversaux dans le wizard |
| E-24 | Majeur | Onglet "Temps" dans la fiche projet |
| E-27 | Majeur | Table des phases sur la Vue d'ensemble |
| E-36 | Majeur | Filtres dropdown sur la liste projets |
| E-15 | Mineur | Lien "+ Créer un nouveau client" dans le wizard |

### ⚠️ Écarts partiellement corrigés (5)

| ID | Sévérité | Correction partielle | Ce qui manque encore |
|----|----------|---------------------|----------------------|
| E-10 | Majeur | Formulaire Sous-traitants présent dans le wizard (Nom, Spécialité, Montant) | Sélection fournisseur existant, phases associées, champs complets |
| E-12 | Majeur | Concept Public/Privé implémenté (checkboxes) | Radio buttons comme dans le mockup |
| E-13 | Majeur | Checkbox "Consortium" présente | Sous-formulaire membres et règles de partage |
| E-35 | Majeur | +3 colonnes ajoutées (Chef de projet, BU, Santé) — 8 colonnes au total | Phase active, Budget h, CA (3 colonnes manquantes sur 10 attendues) |
| E-01 | Mineur | Sidebar multiprofile — acceptable | Aucun (acceptable) |

---

## Bilan chiffré global

| Statut | Nb | % des 38 écarts actifs |
|--------|----|------------------------|
| ✅ Corrigés (nouveaux depuis v4) | **6** | 15.8 % |
| ⚠️ Partiellement corrigés | **4** | 10.5 % |
| ❌ Non corrigés | **28** | 73.7 % |
| **TOTAL écarts actifs** | **38** | |

---

## Nouveaux écarts détectés en v5

| ID | Sévérité | Description | Impact |
|----|----------|-------------|--------|
| NEW-03 | Info | Consortium cochable mais sans sous-formulaire : risque de données incomplètes | Un projet peut être marqué "Consortium: Oui" sans avoir aucun membre ni règle de partage définie |
| NEW-04 | Info | La colonne "Santé" dans la liste projets affiche "OK"/"Terminé" — critères de calcul non documentés | Valeur utile mais règles métier à documenter |

---

## Fonctionnalités critiques encore manquantes

1. **Transfert de responsable (E-39/E-40)** — FR15d/FR15e/FR15g : aucun écran, aucune route, fonctionnalité entièrement absente.
2. **Dashboard PM — KPIs métier (E-04)** : Ratio CA/Salaires et Taux de facturation toujours absents.
3. **Liste projets dans le dashboard (E-05)** : navigation séparée toujours requise.
4. **Phase "Qualité" dans le template ARCH-STD (E-23)** : template non mis à jour.
5. **WBS 3 niveaux dans le wizard (E-19)** : création de projet sans tâches/sous-tâches.

---

## Verdict final

### ⚠️ NO-GO — avec progrès significatifs

**Motif :** 8 des 17 écarts Majeurs restent non corrigés, dont les plus critiques (Transfert de responsable, Dashboard PM, WBS hiérarchique). La version v1.1.014 marque un **premier cycle de corrections réelles** sur le module Projets (6 écarts corrigés, dont 5 Majeurs), mais le volume d'écarts restants — en particulier les fonctionnalités entièrement absentes — empêche un GO.

**Progression qualitative :** Le wizard de création a été le plus travaillé et montre des améliorations notables. La liste projets gagne en utilisabilité avec les filtres et colonnes ajoutées.

### Priorités de correction recommandées

| Priorité | Écart(s) | Justification |
|----------|----------|---------------|
| **P1 — Sprint courant** | E-39/E-40 (Transfert responsable) | Fonctionnalité entièrement manquante, critique métier |
| **P1 — Sprint courant** | E-04/E-05 (Dashboard PM KPIs + liste projets) | Impact quotidien fort pour les PMs |
| **P1 — Sprint courant** | E-23 (Phase "Qualité" template) | Correction rapide dans les données de template |
| **P2 — Sprint suivant** | E-13 (Consortium sous-formulaire) | Compléter la correction partielle |
| **P2 — Sprint suivant** | E-35 (3 colonnes manquantes liste) | Phase active, Budget h, CA |
| **P2 — Sprint suivant** | E-26 (KPIs financiers vue d'ensemble) | Visibilité ratio CA/salaires |
| **P3 — Backlog** | E-10, E-19, E-33, E-34 | Formulaires et données complémentaires |
| **P4 — Backlog** | E-08, E-25, E-29, E-38 | Cosmétiques |

### Prochaines étapes

1. **Re-test P1** dès livraison des corrections prioritaires (E-39/E-40, E-04/E-05, E-23)
2. **Escalade Architect** pour E-39/E-40 : la fonctionnalité de transfert nécessite une définition technique complète (routes, modèle de données, historique)
3. **Communication Developer** : confirmer la feuille de route pour les corrections P2 (E-13, E-35, E-26)

---

*Rapport généré le 2026-04-05 — QA Tester Senior*
*ERP v1.1.014 — Vérification corrections post-audit rapport_verification_corrections_v4.md*
