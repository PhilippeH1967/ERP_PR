# Rapport d'écarts Mockup vs Application — Module Projets

**Date d'analyse :** 2026-04-05
**Analyseur :** QA Tester Senior
**Application :** http://localhost:5174 — ERP v1.1.013
**Mockup de référence :** `flux-02-projet.html` (11 mars 2026)
**Référence précédente :** `rapport_test_module_projet_v3.md` (2026-04-04, GO avec 2 anomalies mineures)
**Profil utilisé :** admin@provencher-roy.com (ADMIN)

---

## Résumé exécutif

| Catégorie | Nb d'écarts |
|-----------|-------------|
| **Majeurs** (fonctionnalités absentes ou structurellement différentes) | **14** |
| **Mineurs** (champs, colonnes ou comportements partiellement différents) | **16** |
| **Cosmétiques** (libellés, terminologie) | **5** |
| **TOTAL** | **35** |

| Point positif | Détail |
|---------------|--------|
| BUG-012 corrigé (non signalé en v3) | Les statuts de la liste projets s'affichent maintenant en français (Actif, Terminé) |
| BUG-013 non vérifié dans ce rapport | Nécessite connexion EMPLOYEE |

**Recommandations prioritaires :**
1. La **liste projets** manque 6 colonnes critiques (PM, BU, Phase active, Budget, CA, Santé) et tous ses filtres — impact fort sur l'utilisabilité quotidienne.
2. Les **écrans de Transfert de responsable** (screens 12-13 du mockup) sont entièrement absents — fonctionnalité FR15d/FR15e/FR15g non implémentée.
3. L'onglet **Vue d'ensemble** de la fiche projet est structurellement différent — les KPIs métier attendus (Ratio CA/Salaires, Sous-traitance) ne sont pas sur cette page.
4. Le **wizard de création** manque 3 sections entières (Type Public/Privé, Consortium, Services transversaux) et l'étape 4 n'est pas "Sous-traitants" comme prévu.

---

## Méthodologie

Le mockup `flux-02-projet.html` définit **13 écrans** regroupés en 5 flux :

| Groupe | Screens | Flux |
|--------|---------|------|
| Création (PM) | 1–5 | Wizard 4 étapes + confirmation |
| Dashboard PM | 6–7 | Dashboard + Slide-over |
| Détail projet | 8–10 | Vue d'ensemble, Budget, Équipe |
| Liste projets | 11 | Liste avec filtres |
| Transfert responsables | 12–13 | Changer PM/Dir. + Historique |

Chaque écran a été comparé à l'implémentation réelle observée dans Chrome.

---

## 1. Navigation globale — Sidebar

| ID | Sévérité | Écran mockup | Ce que montre le mockup | Ce que fait l'app | Impact UX |
|----|----------|--------------|------------------------|-------------------|-----------|
| E-01 | Mineur | Tous | Sidebar PM : 5 items (Principal: Tableau de bord, Projets, Feuilles de temps ; Approbations: Temps [badge], Dépenses [badge]) | Sidebar Admin : 3 sections (PRINCIPAL 6 items, FINANCE 4 items, GESTION 1 item) — structure plus riche, multi-rôle | Acceptable car l'app est multiprofile ; la sidebar Admin inclut toutes les fonctionnalités prévues |
| E-02 | Cosmétique | Tous | Logo "PR\|ERP" avec barre verticale | Logo "PR\|ERP" conforme | — |
| E-03 | Mineur | Dashboard (6) | Topbar : icône cloche avec badge rouge (3 notifications), avatar initiales PM | Topbar : icône cloche sans badge, bouton langue "EN", avatar "AD" | Badges de notifications non visibles |

---

## 2. Dashboard PM — Écrans 6 et 7

| ID | Sévérité | Écran mockup | Ce que montre le mockup | Ce que fait l'app | Impact UX |
|----|----------|--------------|------------------------|-------------------|-----------|
| E-04 | **Majeur** | Screen 6 (dash-1) | Dashboard centré PM avec 4 KPIs métier : Heures ce mois, Ratio CA/Salaires, Taux de facturation, Actions requises | Dashboard multi-sections par rôle : CHEF DE PROJET (3 KPIs), DIRECTEUR D'UNITÉ (4 KPIs), ADMINISTRATION (3 KPIs) — aucun des 4 KPIs du mockup n'est présent | Le PM ne voit pas ses indicateurs de performance attendus sur la page d'accueil |
| E-05 | **Majeur** | Screen 6 (dash-1) | Filtres projets + liste de projets directement dans le dashboard (recherche, clients, statuts) | Pas de liste de projets dans le dashboard ; navigation vers /projects requise | Perte d'efficacité : 1 clic supplémentaire pour voir ses projets |
| E-06 | **Majeur** | Screen 7 (dash-2) | Slide-over projet : panneau latéral glissant affichant le résumé d'un projet depuis le dashboard | Non implémenté : clic sur un projet dans le dashboard navigue directement vers la fiche (si liste présente) | Fonctionnalité de prévisualisation rapide absente |
| E-07 | Mineur | Screen 6 (dash-1) | Bouton "+ Nouveau projet" dans le header du dashboard | Bouton absent du dashboard ; accessible uniquement depuis /projects | Légère friction |
| E-08 | Cosmétique | Screen 6 (dash-1) | Libellé : "Bienvenue, Jean-François • Mis à jour il y a 2 min" | "ph.admin — ADMIN" affiché en haut à droite (pas de message d'accueil) | Cosmétique |

---

## 3. Wizard de création de projet — Écrans 1 à 5

### 3.1 Structure du wizard

| ID | Sévérité | Élément | Ce que montre le mockup | Ce que fait l'app | Impact UX |
|----|----------|---------|------------------------|-------------------|-----------|
| E-09 | **Majeur** | Étapes wizard | 4 étapes : **1-Informations & phases** / **2-Budget** / **3-Ressources & Planning** / **4-Sous-traitants** | 4 étapes : **1-Identification** / **2-Budget & Phases** / **3-Ressources** / **4-Confirmation** | L'étape 4 du mockup (Sous-traitants avec formulaire complet) est remplacée par une simple confirmation |
| E-10 | **Majeur** | Étape 4 Sous-traitants | Formulaire complet d'ajout de sous-traitants dans le wizard (fournisseur, phases, honoraires ST, refacturable, absorbé, résumé ST avec 5 KPIs) | Pas d'étape Sous-traitants dans le wizard — l'onglet Sous-traitants existe en fiche projet mais pas en création | Les sous-traitants ne peuvent pas être configurés à la création |
| E-11 | Mineur | Bouton "Sauver brouillon" | Présent à l'étape 2 ("Sauver brouillon" + "Suivant") | Absent — seulement "Suivant ►" | Impossible de sauver un projet en cours de création |

### 3.2 Étape 1 — Champs absents de l'app

| ID | Sévérité | Champ | Ce que montre le mockup | Ce que fait l'app | Impact UX |
|----|----------|-------|------------------------|-------------------|-----------|
| E-12 | **Majeur** | Type de projet | Radio : **Public / Privé** (sélection visible) | Champ absent du formulaire | Information projet non collectée |
| E-13 | **Majeur** | Section Consortium | Bloc complet : radio Oui/Non → si Oui : sélecteur consortium, rôle PR, membres, règles de partage (coefficients, clause, modes de mesure) | Entièrement absent | Projets en consortium non gérables depuis le wizard |
| E-14 | **Majeur** | Services transversaux | Cases à cocher : 3D/Visualisation, BIM, Design d'intérieur, Paysage, Développement durable | Absent | Classification des services non configurée |
| E-15 | Mineur | Lien "+ Créer un nouveau client" | Présent sous le champ Client (en texte bleu) | Absent — le champ Client est une liste déroulante sans lien de création | L'utilisateur doit quitter le wizard pour créer un client |
| E-16 | Mineur | Phases dans l'étape 1 | L'étape 1 inclut la configuration des phases (table dépliable Phase standard / Libellé client / bouton ×) | Phases déplacées en étape 2 "Budget & Phases" | Réorganisation du flux (peut être intentionnel) |

### 3.3 Étape 1 — Champs présents dans l'app mais absents du mockup

| ID | Sévérité | Champ | Présent dans l'app | Impact UX |
|----|----------|----|-------------------|-----------|
| E-17 | NA
| E-18 | NA

### 3.4 Étape 2 — Budget & Phases (app) vs Budget (mockup)

| ID | Sévérité | Élément | Ce que montre le mockup | Ce que fait l'app | Impact UX |
|----|---n-------|---------|------------------------|-------------------|-----------|
| E-19 | NA
| E-20 | Mineur | Colonne "Sous-traitance ($)" | Colonne "Sous-traitance ($)" dans le tableau budget | Absente dans l'app (budget ST géré via onglet dédié) | Saisie du budget ST séparée |
| E-21 | Mineur | Section Taux horaires | Section dédiée avec "Grille de taux" (dropdown) et "Taux moyen estimé ($275/h)" | Non visible dans l'étape Budget | Information de taux manquante à la création |
| E-22 | Cosmétique | "Importer budget depuis Excel" | Lien "📄 Importer budget depuis Excel" | Absent | Import Excel non disponible |

### 3.5 Phase obligatoire "Qualité" absente

| ID | Sévérité | Élément | Ce que montre le mockup | Ce que fait l'app | Impact UX |
|----|----------|---------|------------------------|-------------------|-----------|
| E-23 | **Majeur** | Phase obligatoire "Qualité" | Le mockup définit **8 phases** dont 2 obligatoires : "Gestion de projet" + **"Qualité"** (badge "Obligatoire", icône cadenas, 2 tâches QA.1/QA.2) | L'app déploie **6 phases** via ARCH-STD template (Concept, Préliminaire, Définitif, Appel d'offres, Surveillance, Gestion de projet) — phase "Qualité" absente | Processus qualité non structuré dans les projets |

---

## 4. Fiche Projet — Structure des onglets

### 4.1 Comparaison globale des onglets

| Mockup (6 onglets) | App (10 onglets) | Écart |
|--------------------|-----------------|-------|
| Vue d'ensemble | Vue d'ensemble | ✓ Présent |
| **Temps** | *(absent)* | ❌ Manquant dans l'app |
| Budget | Budget | ✓ Présent (contenu différent) |
| Sous-traitants | Sous-traitants | ✓ Présent |
| Équipe | Équipe | ✓ Présent (contenu différent) |


| ID | Sévérité | Écart |
|----|----------|-------|
| E-24 | **Majeur** | L'onglet **"Temps"** (feuilles de temps du projet) prévu dans le mockup est absent de la fiche projet |
| E-25 | Cosmétique | Libellé "Factures" (mockup) → "Facturation" (app) |

---

## 5. Onglet Vue d'ensemble

| ID | Sévérité | Élément | Ce que montre le mockup | Ce que fait l'app | Impact UX |
|----|----------|---------|------------------------|-------------------|-----------|
| E-26 | **Majeur** | KPIs | 4 KPIs : Heures consommées/budget (avec barre de progression), Honoraires facturés/contrat, **Ratio CA/Salaires** (cible 2.5x), **Sous-traitance** consommée/budget | 3 KPIs : % Utilisation, Heures, Budget — sans ratio financier ni suivi ST | PM ne voit pas ses indicateurs financiers clés depuis la vue principale |
| E-27 | **Majeur** | Table des phases | Table des phases sur la vue d'ensemble : Phase, Mode, Heures plan., Heures réelles, Avancement (barre), Honoraires, Statut (badge) | Table des phases absente de la Vue d'ensemble — déplacée dans l'onglet "Phases" avec structure différente | La vue d'ensemble ne donne plus une vision synthétique de l'état des phases |
| E-28 |NA
| E-29 | Cosmétique | Bouton dans le header | Mockup : badge "Actif" + bouton "⚙️ Paramètres" | App : badge "Terminé" + bouton "Modifier" | "Paramètres" → "Modifier" (libellé différent) |

---

## 6. Onglet Budget

| ID | Sévérité | Élément | Ce que montre le mockup | Ce que fait l'app | Impact UX |
|----|----------|---------|------------------------|-------------------|-----------|
| E-30 | Mineur | KPIs | 3 KPIs : Contrat initial, Avenants (avec nb avenants approuvés), Contrat total | 4 KPIs : Budget total, Facturé à ce jour, % Consommé, Solde Restant | App couvre des KPIs différents (suivi de consommation vs structure contractuelle) |
| E-31 | Mineur | Structure de la table | Table **par discipline** (Architecture, Structure, Mécanique, Électrique) avec Heures budget, Heures réelles, Consommation %, Coût réel, Budget, Écart | Table **par tâche WBS** (WBS, Tâche, Mode, Budget, Heures, Facturé, Solde) | Granularité différente — l'app est orientée WBS, le mockup orienté discipline |
| E-32 | Mineur | Bouton "Bloquer cette phase" | Bouton danger "🔒 Bloquer cette phase" dans le header de la table budget phase active | Absent de l'onglet Budget | Fonctionnalité de blocage de phase non accessible depuis le Budget |

---

## 7. Onglet Équipe

| ID | Sévérité | Élément | Ce que montre le mockup | Ce que fait l'app | Impact UX |
|----|----------|---------|------------------------|-------------------|-----------|
| E-33 | Mineur | Colonnes | Membre, **Profil** (badge rôle), **Phases assignées** (tags multiples), **Heures ce mois**, **Heures total**, Allocation (%), Actions | Employé, Phase (singulier), %, **Période** | Perte de 3 colonnes informatives : Profil, Heures ce mois, Heures total |
| E-34 | Mineur | Profils virtuels | Profils virtuels affichés dans la liste avec badge "À pourvoir" et bouton "Assigner" pour les remplacer par des ressources réelles | Profils virtuels non visibles dans l'onglet Équipe | Impossible de voir les besoins de staffing non couverts |

---

## 8. Liste des projets

| ID | Sévérité | Élément | Ce que montre le mockup | Ce que fait l'app | Impact UX |
|----|----------|---------|------------------------|-------------------|-----------|
| E-35 | **Majeur** | Colonnes | 10 colonnes : Code, Projet, Client, **PM**, **BU**, **Phase active**, **Budget (h)** (barre), **CA**, **Santé** (dot couleur), Statut | 5 colonnes : Code, Nom, Client, **Type**, Statut | 5 colonnes critiques absentes : PM, BU, Phase active, CA, Santé |
| E-36 | **Majeur** | Filtres | 3 filtres : Statut, BU, PM | Barre de recherche textuelle uniquement (pas de filtres dropdown) | Impossible de filtrer par PM ou BU depuis la liste |
| E-37 | Mineur | Pagination | Pagination visible (1-5 sur 142, boutons pages) | Pas de pagination visible (liste complète affichée) | OK si la liste est courte en production |
| E-38 | Cosmétique | Colonne "Nom" vs "Projet" | Libellé colonne : "Projet" | Libellé colonne : "Nom" | Cosmétique |

> **Note :** BUG-012 (v3) — statuts en anglais dans la liste — semble **résolu** : les statuts affichent "Actif" et "Terminé" en français dans la version observée aujourd'hui. À confirmer car non inclus dans le rapport v3 comme corrigé.

---

## 9. Fonctionnalités du mockup entièrement absentes de l'app

| ID | Sévérité | Feature mockup | Screens concernés | Statut dans l'app |
|----|----------|---------------|------------------|-------------------|
| E-39 | **Majeur** | **Transfert de responsable (FR15d/FR15e)** — Formulaire complet : responsables actuels (PM, Associé, Chargé de contrat), rôle à transférer, nouveau responsable, date effective, motif, notes, aperçu d'impact | Screens 12–13 (xfer-1, xfer-2) | **Non implémenté** — pas de section dédiée trouvée dans l'app |
| E-40 | **Majeur** | **Historique des changements de responsables (FR15g)** — Table historique avec filtres (rôle, projet, dates), 4 KPIs (Changements PM, Associé, Chargé, Total), export CSV | Screen 13 (xfer-2) | **Non implémenté** |
| E-41 | NA
| E-42 | Mineur | **Prochaines étapes post-création** — Liste de tâches post-création (ressources virtuelles → réelles, sous-traitants, taux) | Screen 5 (wiz-3) | Absent |

---




