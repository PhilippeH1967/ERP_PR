# EPIC — Module Opportunités

**Application OOTI — Gestion de projets pour cabinets d'architecture**
**Version 1.0 — Février 2026**

---

## 1. Identification de l'EPIC

| Champ | Valeur |
|---|---|
| **Nom de l'EPIC** | Opportunités |
| **Référence** | EPIC-001 |
| **Module parent** | Général |
| **Priorité** | Haute |
| **Statut** | À planifier |
| **Date de création** | Février 2026 |
| **Auteur** | — |
| **EPICs liés** | EPIC-002 (Projets), EPIC-003 (Honoraires), EPIC-004 (Facturation) |

---

## 2. Contexte & Problématique

Dans un cabinet d'architecture, le développement commercial repose sur l'identification, le suivi et la conversion d'opportunités d'affaires en projets signés. Les directeurs d'agence et chargés d'affaires doivent gérer un pipeline commercial souvent composé de dizaines d'opportunités simultanées : concours, appels d'offres, consultations directes, recommandations clients. Chaque opportunité traverse un cycle de vie — de la détection initiale jusqu'à la signature ou l'abandon — et nécessite un suivi rigoureux des montants estimés, des probabilités de succès, des propositions commerciales et des relances.

Sans outil centralisé, les cabinets gèrent ces opportunités dans des fichiers Excel dispersés, des boîtes mail ou des carnets de notes. Cette dispersion entraîne une perte de visibilité sur le pipeline commercial, une impossibilité de prioriser les efforts commerciaux, des oublis de relance, et l'absence totale d'indicateurs fiables pour anticiper le chiffre d'affaires futur. Il devient impossible de répondre à des questions fondamentales : quel est le montant total du pipeline ? Quel est le taux de transformation ? Quels sont les prospects à relancer en priorité ?

Le module Opportunités de OOTI vise à résoudre ces problèmes en offrant un espace dédié au pilotage commercial, avec une vue d'ensemble du pipeline, un suivi individualisé de chaque opportunité et la capacité de produire des propositions commerciales professionnelles directement depuis l'outil.

---

## 3. Objectif de l'EPIC

Permettre aux utilisateurs de OOTI de gérer l'intégralité de leur pipeline commercial à travers un module Opportunités structuré en trois sous-menus :

- **Résumé** : tableau de bord synthétique avec indicateurs clés (KPIs) du pipeline commercial
- **Opportunités** : liste et pipeline visuel (kanban et liste) de toutes les opportunités en cours, gagnées, perdues ou abandonnées
- **Propositions** : gestion centralisée des propositions commerciales liées aux opportunités, avec génération depuis des modèles

L'objectif est de donner aux directeurs d'agence et aux chargés d'affaires une visibilité complète sur leur activité commerciale, de la prospection initiale jusqu'à la conversion en projet signé (lien avec EPIC-002).

---

## 4. Périmètre Fonctionnel

### 4.1 Vue Résumé des opportunités (niveau Agence)

- Tableau de bord avec KPIs synthétiques du pipeline commercial
- Nombre d'opportunités par statut (Nouveau, En cours, Gagné, Perdu, Abandonné)
- Montant total du pipeline (somme des honoraires estimés pondérés par la probabilité)
- Montant total des opportunités gagnées sur la période
- Taux de transformation (nombre d'opportunités gagnées / total clôturées)
- Graphiques de répartition par statut, par source, par mois
- Liens rapides vers les opportunités filtrées par statut

### 4.2 Liste et Pipeline des opportunités

- Vue Liste : tableau filtrable et triable de toutes les opportunités
- Vue Kanban : pipeline visuel avec colonnes par statut (drag & drop)
- Colonnes affichées : Référence, Titre, Client, Statut, Probabilité, Honoraires estimés, Assigné à, Date de création, Tags
- Tri par date, montant, probabilité, statut
- Recherche plein texte

### 4.3 Gestion d'une opportunité (CRUD)

- Création d'une opportunité (modale)
- Édition des informations d'une opportunité
- Archivage / suppression d'une opportunité
- Association à un client existant ou création d'un nouveau client
- Assignation à un ou plusieurs collaborateurs
- Saisie de la description, de la source et des tags

### 4.4 Gestion des statuts et probabilités

- Cycle de vie : Nouveau → En cours → Gagné / Perdu / Abandonné
- Attribution d'une probabilité de succès (0% à 100%)
- Historisation des changements de statut avec date et auteur
- Motif de perte ou d'abandon (champ obligatoire lors du passage au statut Perdu ou Abandonné)

### 4.5 Conversion d'une opportunité en projet

- Conversion d'une opportunité au statut "Gagné" en projet signé (EPIC-002)
- Pré-remplissage des données du projet à partir de l'opportunité (titre, client, honoraires, membres)
- Lien de traçabilité entre le projet créé et l'opportunité d'origine

### 4.6 Propositions commerciales

- Liste centralisée de toutes les propositions commerciales
- Association d'une ou plusieurs propositions à une opportunité
- Création manuelle d'une proposition
- Génération d'une proposition depuis un modèle (modèles personnels ou modèles OOTI)
- Prévisualisation et téléchargement en PDF
- Statut de la proposition : Brouillon, Envoyée, Acceptée, Refusée

### 4.7 Filtrage, recherche et export

- Filtres combinables : statut, client, probabilité, montant, assigné à, source, tags, période
- Recherche plein texte sur titre, description, client, référence
- Export CSV / Excel de la liste des opportunités (filtres appliqués)
- Actions en masse : changement de statut, assignation, suppression, export

---

## 5. User Stories

### US-O01 — Vue Résumé des opportunités

**En tant que** Directeur d'agence / Chargé d'affaires
**Je veux** accéder à une vue résumé de mon pipeline commercial
**Afin de** visualiser en un coup d'oeil les indicateurs clés de mon activité commerciale et prendre des décisions éclairées

**Critères d'acceptance :**
1. Le résumé affiche le nombre total d'opportunités actives (statuts Nouveau + En cours) avec un lien cliquable vers la liste filtrée
2. Le résumé affiche le nombre d'opportunités gagnées sur la période sélectionnée avec le montant total associé
3. Le résumé affiche le nombre d'opportunités perdues sur la période sélectionnée avec le montant total associé
4. Le montant total du pipeline pondéré est affiché (somme des honoraires estimés × probabilité pour chaque opportunité active) dans la devise de l'agence
5. Le taux de transformation est calculé et affiché en pourcentage (opportunités gagnées / (gagnées + perdues) sur la période)
6. Un graphique en barres ou camembert illustre la répartition des opportunités par statut
7. Un graphique d'évolution mensuelle affiche le nombre d'opportunités créées et clôturées par mois
8. Des actions rapides sont disponibles depuis le résumé : "+ Nouvelle opportunité", accès aux favoris et alertes
9. La vue est accessible via le menu latéral > Opportunités > Résumé
10. Un sélecteur de période permet de filtrer les KPIs (mois en cours, trimestre, année, personnalisé)

---

### US-O02 — Liste et Pipeline des opportunités

**En tant que** Chargé d'affaires / Chef de projet
**Je veux** consulter la liste complète de mes opportunités sous forme de liste ou de pipeline visuel (kanban)
**Afin de** avoir une vision claire de l'état de mon pipeline commercial et identifier les opportunités à prioriser

**Critères d'acceptance :**
1. La vue Liste affiche un tableau avec les colonnes : Référence, Titre, Client, Statut (badge coloré), Probabilité (%), Honoraires estimés (devise), Assigné à (avatar), Source, Tags (étiquettes), Date de création
2. La vue Kanban affiche les opportunités dans des colonnes organisées par statut : Nouveau, En cours, Gagné, Perdu, Abandonné
3. En vue Kanban, chaque carte affiche : Titre, Client, Montant estimé, Probabilité, Assigné à
4. Le drag & drop est fonctionnel en vue Kanban pour déplacer une opportunité d'un statut à un autre
5. Un changement de statut par drag & drop déclenche les mêmes validations qu'un changement via le formulaire (ex : motif obligatoire pour Perdu/Abandonné)
6. Un bouton bascule permet de passer de la vue Liste à la vue Kanban et inversement
7. Chaque ligne (liste) ou carte (kanban) est cliquable et ouvre le détail de l'opportunité
8. Le nombre total d'opportunités et le montant total sont affichés en en-tête de la liste
9. Le bouton "+ Nouvelle opportunité" est visible en permanence et ouvre la modale de création (US-O03)
10. Le bouton ACTIONS permet : Export CSV/Excel, Afficher/masquer les colonnes (vue liste), Actions en masse

---

### US-O03 — Création d'une opportunité

**En tant que** Chargé d'affaires / Chef de projet
**Je veux** créer une nouvelle opportunité commerciale
**Afin de** enregistrer un nouveau prospect ou un appel d'offres dans le pipeline et commencer son suivi

**Critères d'acceptance :**
1. Une modale de création s'ouvre via le bouton "+ Nouvelle opportunité"
2. Les champs obligatoires sont : Titre de l'opportunité, Client (existant ou nouveau)
3. Les champs optionnels sont : Référence (auto-générée si non renseignée, format OPP-XXXX), Description, Montant estimé des honoraires (avec devise), Probabilité de succès (slider ou champ numérique, 0-100%), Source (liste déroulante : Concours, Appel d'offres, Recommandation, Prospection directe, Réseau, Autre), Assigné à (un ou plusieurs collaborateurs), Tags (étiquettes libres), Date de clôture estimée
4. La référence est pré-suggérée automatiquement (ex : OPP-0042) basée sur la dernière référence utilisée, mais reste modifiable
5. Le champ Client propose une recherche en autocomplétion parmi les clients existants, avec un lien "+ Nouveau client" pour créer un client à la volée sans quitter la modale
6. Le statut est automatiquement positionné sur "Nouveau" à la création
7. La probabilité par défaut est fixée à 10% pour une nouvelle opportunité et peut être ajustée
8. À la validation, l'opportunité est créée et apparaît dans la liste/kanban ; l'utilisateur est redirigé vers le détail de l'opportunité ou reste sur la liste selon ses préférences
9. Les champs obligatoires non renseignés déclenchent un message d'erreur explicite empêchant la soumission
10. La modale peut être fermée sans sauvegarder (confirmation si des données ont été saisies)

---

### US-O04 — Édition d'une opportunité

**En tant que** Chargé d'affaires / Chef de projet
**Je veux** modifier les informations d'une opportunité existante
**Afin de** mettre à jour les données au fil de l'évolution de la négociation commerciale

**Critères d'acceptance :**
1. Tous les champs de l'opportunité sont éditables depuis la vue détail : Titre, Description, Client, Montant estimé, Probabilité, Source, Assigné à, Tags, Date de clôture estimée
2. La modification du montant estimé des honoraires est enregistrée avec un historique (ancien montant → nouveau montant, date, auteur)
3. La modification du client est possible : remplacement par un autre client existant ou création d'un nouveau client
4. Les tags peuvent être ajoutés ou retirés librement (autocomplétion sur les tags existants dans le système)
5. L'assignation peut être modifiée : ajout ou retrait de collaborateurs
6. Un bouton "Archiver" permet de passer l'opportunité en statut archivé sans la supprimer
7. Un bouton "Supprimer" est disponible avec une modale de confirmation ("Cette action est irréversible. Confirmez-vous la suppression de l'opportunité OPP-XXXX ?")
8. Une opportunité liée à un projet signé (convertie) ne peut pas être supprimée (le bouton est désactivé avec un tooltip explicatif)
9. Les modifications sont sauvegardées automatiquement ou via un bouton "Enregistrer" avec feedback visuel (notification de succès)
10. Un journal d'activité en bas de la fiche affiche l'historique de toutes les modifications (date, auteur, champ modifié, ancienne/nouvelle valeur)

---

### US-O05 — Gestion des statuts et probabilités

**En tant que** Chargé d'affaires / Directeur d'agence
**Je veux** faire évoluer le statut d'une opportunité et ajuster sa probabilité de succès
**Afin de** refléter l'avancement réel de la négociation et fiabiliser les prévisions de chiffre d'affaires

**Critères d'acceptance :**
1. Les statuts disponibles sont : Nouveau, En cours, Gagné, Perdu, Abandonné
2. Le changement de statut se fait via un sélecteur déroulant ou un workflow visuel (barre de progression cliquable) dans la fiche de l'opportunité
3. Le passage au statut "Perdu" déclenche l'affichage d'un champ obligatoire "Motif de perte" (liste prédéfinie : Prix trop élevé, Concurrent retenu, Projet annulé par le client, Délai non respecté, Autre + champ libre)
4. Le passage au statut "Abandonné" déclenche l'affichage d'un champ obligatoire "Motif d'abandon" (liste prédéfinie : Charge de travail insuffisante, Projet non stratégique, Client non fiable, Autre + champ libre)
5. Le passage au statut "Gagné" propose automatiquement la conversion en projet (lien vers US-O06) avec un bouton "Convertir en projet"
6. La probabilité est saisissable de 0% à 100% par pas de 5% via un slider ou un champ numérique
7. Lorsque le statut passe à "Gagné", la probabilité est automatiquement positionnée à 100%
8. Lorsque le statut passe à "Perdu" ou "Abandonné", la probabilité est automatiquement positionnée à 0%
9. Chaque changement de statut est historisé dans le journal d'activité avec la date, l'auteur, l'ancien statut, le nouveau statut et le motif le cas échéant
10. Un retour en arrière est possible : une opportunité "Perdue" ou "Abandonnée" peut être réouverte au statut "En cours" (avec confirmation)

---

### US-O06 — Conversion d'une opportunité en projet

**En tant que** Chef de projet / Directeur d'agence
**Je veux** convertir une opportunité gagnée en projet signé
**Afin de** initier le suivi de projet dans le module Projets (EPIC-002) sans resaisir les informations déjà connues

**Critères d'acceptance :**
1. Le bouton "Convertir en projet" est disponible uniquement pour les opportunités au statut "Gagné"
2. Un clic sur "Convertir en projet" ouvre une modale pré-remplie avec les données de l'opportunité : Titre du projet (= titre de l'opportunité), Client (= client de l'opportunité), Montant des honoraires estimés, Membres assignés
3. Les champs complémentaires obligatoires pour la création du projet sont affichés dans la modale : Devise, ID Projet (pré-suggéré), Date de début, Date de fin
4. Les champs complémentaires optionnels sont disponibles : Adresse, Code postal, Ville, Pays, Langue, Taux de TVA, Étiquettes
5. L'utilisateur peut modifier tous les champs pré-remplis avant validation
6. À la validation, un projet est créé dans le module Projets (EPIC-002) avec le statut "Signé"
7. Un lien de traçabilité bidirectionnel est établi : l'opportunité référence le projet créé, et le projet référence l'opportunité d'origine
8. L'opportunité conserve son statut "Gagné" et affiche un badge "Converti" avec un lien vers le projet
9. Une opportunité déjà convertie ne peut pas être reconvertie (le bouton "Convertir en projet" est désactivé avec un tooltip "Déjà converti — voir projet PR-XXXX")
10. En cas d'erreur lors de la création du projet, un message d'erreur explicite est affiché et l'opportunité reste inchangée

---

### US-O07 — Propositions commerciales liées aux opportunités

**En tant que** Chargé d'affaires / Chef de projet
**Je veux** créer et gérer des propositions commerciales associées à mes opportunités
**Afin de** centraliser les documents commerciaux et suivre leur statut (brouillon, envoyée, acceptée, refusée)

**Critères d'acceptance :**
1. Depuis la fiche d'une opportunité, un onglet "Propositions" affiche la liste des propositions liées
2. Le bouton "+ Nouvelle proposition" permet de créer une proposition rattachée à l'opportunité
3. Chaque proposition possède les champs : Titre, Date de création, Date d'envoi, Montant proposé, Statut (Brouillon, Envoyée, Acceptée, Refusée), Contenu (éditeur riche ou document joint)
4. Le statut de la proposition est modifiable via un sélecteur déroulant
5. Lorsqu'une proposition passe au statut "Acceptée", une suggestion de passage du statut de l'opportunité à "Gagné" est affichée
6. La liste des propositions est également accessible via le sous-menu "Propositions" du module Opportunités, affichant toutes les propositions de toutes les opportunités
7. Un filtre par statut de proposition et par opportunité est disponible dans la vue globale des propositions
8. Chaque proposition peut être dupliquée pour créer une variante
9. Une proposition peut être supprimée (avec confirmation) tant qu'elle est au statut "Brouillon"
10. Le nombre de propositions et leur statut sont visibles en résumé sur la carte/ligne de l'opportunité dans la liste et le kanban

---

### US-O08 — Génération de propositions depuis des modèles

**En tant que** Chargé d'affaires / Chef de projet
**Je veux** générer une proposition commerciale à partir d'un modèle prédéfini
**Afin de** produire rapidement un document professionnel pré-rempli avec les données de l'opportunité et du client

**Critères d'acceptance :**
1. L'écran de création d'une proposition affiche une section "Choisir un modèle" avec deux catégories : "Mes modèles" (personnalisés par l'utilisateur) et "Modèles OOTI" (fournis par défaut)
2. Chaque modèle est affiché avec un aperçu miniature (thumbnail) et son titre
3. Un clic sur un modèle affiche une prévisualisation en taille réelle avant confirmation
4. À la confirmation, une proposition est générée et pré-remplie avec les données de l'opportunité : Titre de l'opportunité, Nom du client, Adresse du client, Montant estimé des honoraires, Description de l'opportunité, Date du jour
5. Les champs pré-remplis sont modifiables dans l'éditeur de la proposition après génération
6. La proposition générée peut être téléchargée en format PDF
7. La proposition générée peut être enregistrée comme nouveau modèle personnalisé ("Sauvegarder comme modèle")
8. Les modèles personnels peuvent être créés, édités et supprimés depuis une interface d'administration des modèles
9. Au minimum 3 modèles OOTI par défaut sont fournis : Proposition standard, Proposition concours, Proposition mission complémentaire
10. Le bouton ACTIONS de la liste des propositions permet un export groupé en PDF

---

### US-O09 — Filtrage et recherche des opportunités

**En tant que** Chargé d'affaires / Directeur d'agence
**Je veux** filtrer et rechercher les opportunités selon plusieurs critères combinables
**Afin de** retrouver rapidement une opportunité ou un ensemble d'opportunités correspondant à des critères précis

**Critères d'acceptance :**
1. Un champ de recherche plein texte est disponible en haut de la liste, permettant une recherche sur : titre, description, nom du client, référence de l'opportunité
2. Un panneau de filtres est accessible via un bouton "Filtres" et reste visible (panneau latéral ou barre de filtres)
3. Les filtres disponibles sont : Statut (multi-sélection : Nouveau, En cours, Gagné, Perdu, Abandonné), Client (autocomplétion), Probabilité (plage min-max), Montant estimé (plage min-max), Assigné à (multi-sélection de collaborateurs), Source (multi-sélection), Tags (multi-sélection), Période de création (date de début / date de fin), Période de clôture estimée (date de début / date de fin)
4. Les filtres sont combinables (ET logique entre filtres de types différents, OU logique au sein d'un même filtre multi-sélection)
5. Le nombre de résultats est affiché et mis à jour en temps réel lors de l'application des filtres
6. Un bouton "Réinitialiser les filtres" supprime tous les filtres actifs
7. Les filtres actifs sont affichés sous forme de badges cliquables (suppression individuelle d'un filtre)
8. Les filtres sont appliqués simultanément à la vue Liste et à la vue Kanban
9. L'URL de la page est mise à jour avec les paramètres de filtre (permettant le partage d'un lien filtré)
10. Les résultats filtrés sont exportables via le bouton ACTIONS (l'export respecte les filtres appliqués)

---

### US-O10 — Export et actions en masse

**En tant que** Directeur d'agence / Chargé d'affaires
**Je veux** exporter les données des opportunités et effectuer des actions en masse sur une sélection
**Afin de** produire des rapports commerciaux, partager des données avec ma direction ou traiter efficacement plusieurs opportunités simultanément

**Critères d'acceptance :**
1. Le bouton ACTIONS dans la barre d'en-tête de la liste propose les options : Export CSV, Export Excel, Afficher/masquer les colonnes
2. L'export CSV/Excel inclut toutes les colonnes visibles et respecte les filtres actifs
3. L'export inclut les champs : Référence, Titre, Client, Statut, Probabilité, Honoraires estimés, Source, Assigné à, Tags, Date de création, Date de clôture estimée, Motif de perte (le cas échéant)
4. Des cases à cocher permettent de sélectionner une ou plusieurs opportunités dans la vue liste
5. Une case à cocher globale ("Tout sélectionner") est disponible en en-tête de colonne, sélectionnant toutes les opportunités de la page courante
6. Lorsqu'une sélection est active, une barre d'actions en masse apparaît avec les options : Changer le statut, Assigner à, Ajouter un tag, Supprimer
7. Le changement de statut en masse applique les mêmes règles de validation que le changement individuel (ex : motif obligatoire pour Perdu)
8. La suppression en masse affiche une modale de confirmation indiquant le nombre d'opportunités sélectionnées
9. Un compteur indique le nombre d'éléments sélectionnés ("X opportunité(s) sélectionnée(s)")
10. Les actions en masse ne sont pas disponibles en vue Kanban (uniquement en vue Liste)

---

## 6. Hors Périmètre (Out of Scope)

- Gestion des projets signés et de leur suivi opérationnel (couvert par EPIC-002 — Projets)
- Calcul détaillé des honoraires par phase et co-traitants (couvert par EPIC-003 — Honoraires)
- Émission et suivi des factures clients (couvert par EPIC-004 — Facturation)
- Saisie des temps collaborateurs (couvert par EPIC-005 — Temps)
- Gestion du planning et du Gantt projet (couvert par EPIC-006 — Planning)
- Gestion des coûts salaires / frais généraux agence (couvert par EPIC-007 — Coûts)
- Reporting et tableaux de bord cross-modules (couvert par EPIC-011 — Rapports)
- CRM avancé : gestion des contacts, campagnes marketing, emailing, lead scoring
- Intégration avec des outils tiers de prospection (LinkedIn, HubSpot, Salesforce)
- Gestion documentaire avancée (GED) pour les pièces jointes des opportunités

---

## 7. Règles Métier

1. Une opportunité doit obligatoirement avoir un titre et un client associé
2. La référence de l'opportunité est unique par entité/agence (format OPP-XXXX, auto-incrémenté)
3. Le statut initial d'une nouvelle opportunité est toujours "Nouveau"
4. La probabilité par défaut est de 10% pour une nouvelle opportunité
5. Le passage au statut "Perdu" ou "Abandonné" exige la saisie d'un motif (champ obligatoire)
6. Le passage au statut "Gagné" positionne automatiquement la probabilité à 100%
7. Le passage au statut "Perdu" ou "Abandonné" positionne automatiquement la probabilité à 0%
8. Une opportunité au statut "Gagné" peut être convertie en projet (une seule fois)
9. Une opportunité convertie en projet ne peut pas être supprimée ni reconvertie
10. Le montant pondéré du pipeline = somme (honoraires estimés × probabilité / 100) pour les opportunités aux statuts Nouveau et En cours
11. Le taux de transformation = nombre d'opportunités gagnées / (gagnées + perdues) sur la période, exprimé en pourcentage
12. Un changement de statut vers "Perdu" ou "Abandonné" est réversible : l'opportunité peut être réouverte au statut "En cours"
13. La devise des honoraires estimés est héritée de la devise de l'agence par défaut, mais peut être modifiée par opportunité
14. Une proposition commerciale au statut "Envoyée" ou "Acceptée" ne peut pas être supprimée
15. Les tags sont partagés au niveau de l'agence : un tag créé sur une opportunité est disponible pour toutes les autres

---

## 8. Critères d'Acceptance Globaux de l'EPIC

1. Toutes les User Stories US-O01 à US-O10 sont développées et validées
2. La navigation entre les sous-menus (Résumé, Opportunités, Propositions) est fluide et cohérente
3. La navigation Résumé → Liste/Kanban → Détail opportunité → Propositions est fluide et sans rechargement complet de page
4. Les KPIs du résumé sont cohérents avec les données de la liste des opportunités (montants, compteurs, taux)
5. Le pipeline pondéré est recalculé en temps réel après toute modification de montant, probabilité ou statut
6. Les droits d'accès sont respectés : un collaborateur ne voit que les opportunités qui lui sont assignées ou celles de son agence (selon configuration admin)
7. Le module fonctionne en mode responsive (desktop, tablette)
8. Les performances sont acceptables : chargement de la liste < 2 secondes pour 200 opportunités, recalcul des KPIs < 1 seconde
9. Tous les formulaires gèrent les cas d'erreur (champs obligatoires, formats invalides, doublons de référence)
10. L'export CSV/Excel produit un fichier valide et lisible dans les outils bureautiques courants (Microsoft Excel, Google Sheets)
11. La conversion en projet (US-O06) crée effectivement un projet fonctionnel dans le module Projets (EPIC-002)

---

## 9. Definition of Done (DoD)

1. Le code est développé, revu (code review par un pair) et mergé sur la branche principale
2. Les tests unitaires couvrent les fonctions critiques : calcul du pipeline pondéré, taux de transformation, validation des changements de statut, génération de références
3. Les tests d'intégration valident les flux principaux : création → modification de statut → conversion en projet
4. Les tests d'intégration valident le flux propositions : création → génération depuis modèle → changement de statut → lien avec opportunité
5. La documentation technique est mise à jour (API endpoints, modèles de données, diagrammes de flux)
6. La fonctionnalité a été testée par le Product Owner et validée sur un environnement de recette
7. Aucun bug bloquant ou critique n'est ouvert sur les User Stories de l'EPIC
8. Les données de démo sont cohérentes et représentatives (au moins 20 opportunités de démonstration avec des statuts variés)
9. Les messages d'erreur et les libellés sont rédigés en français et relus
10. L'accessibilité de base est assurée (navigation clavier, contrastes suffisants, labels sur les champs de formulaire)

---

## 10. Dépendances

| Type | EPIC / Module | Description |
|---|---|---|
| **Requis par** | EPIC-002 (Projets) | Une opportunité gagnée peut être convertie en projet signé |
| **Requis par** | EPIC-003 (Honoraires) | Les honoraires estimés de l'opportunité servent de base aux honoraires du projet |
| **Dépend de** | Module Clients | L'association d'un client à une opportunité nécessite le module de gestion des clients |
| **Dépend de** | Module Collaborateurs | L'assignation d'un collaborateur nécessite le module de gestion des collaborateurs |
| **Dépend de** | Module Modèles | La génération de propositions depuis des modèles nécessite le module de gestion des modèles de documents |
| **Requis par** | EPIC-011 (Rapports) | Les données du pipeline alimentent les rapports commerciaux |

**APIs requises :**
- API Opportunities (CRUD complet : création, lecture, mise à jour, suppression, changement de statut)
- API Proposals (CRUD + génération depuis modèle + export PDF)
- API Clients (lecture + création rapide)
- API Collaborateurs (lecture pour assignation)
- API Templates (lecture des modèles de propositions)
- API Export (génération CSV/Excel)

---

## 11. Modèle de Données Principal

### Objet : Opportunity

| Champ | Type | Description |
|---|---|---|
| `id` | UUID | Identifiant unique interne |
| `reference` | String (unique) | Référence affichée (ex : OPP-0042) |
| `title` | String (obligatoire) | Titre de l'opportunité |
| `client_id` | FK → Client | Référence vers le client associé |
| `status` | Enum | Statut : `new`, `in_progress`, `won`, `lost`, `abandoned` |
| `probability` | Integer (0-100) | Probabilité de succès en pourcentage |
| `estimated_fees` | Decimal | Montant estimé des honoraires |
| `currency` | String | Devise (EUR, CAD, USD, etc.) |
| `description` | Text | Description libre de l'opportunité |
| `source` | Enum | Source : `competition`, `tender`, `referral`, `direct`, `network`, `other` |
| `loss_reason` | String (nullable) | Motif de perte ou d'abandon |
| `assigned_to` | Array[FK → User] | Collaborateurs assignés |
| `tags` | Array[String] | Étiquettes / tags |
| `expected_close_date` | Date (nullable) | Date de clôture estimée |
| `converted_project_id` | FK → Project (nullable) | Référence vers le projet créé en cas de conversion |
| `proposals` | Array[FK → Proposal] | Propositions commerciales liées |
| `created_by` | FK → User | Auteur de la création |
| `created_at` | DateTime | Date de création |
| `updated_at` | DateTime | Date de dernière modification |

### Objet : Proposal (Proposition commerciale)

| Champ | Type | Description |
|---|---|---|
| `id` | UUID | Identifiant unique interne |
| `opportunity_id` | FK → Opportunity | Référence vers l'opportunité parente |
| `title` | String | Titre de la proposition |
| `template_id` | FK → Template (nullable) | Modèle utilisé pour la génération |
| `content` | Text / JSON | Contenu de la proposition |
| `proposed_amount` | Decimal | Montant proposé |
| `status` | Enum | Statut : `draft`, `sent`, `accepted`, `refused` |
| `sent_date` | Date (nullable) | Date d'envoi |
| `created_by` | FK → User | Auteur de la création |
| `created_at` | DateTime | Date de création |
| `updated_at` | DateTime | Date de dernière modification |

### Objet : OpportunityActivity (Journal d'activité)

| Champ | Type | Description |
|---|---|---|
| `id` | UUID | Identifiant unique interne |
| `opportunity_id` | FK → Opportunity | Référence vers l'opportunité |
| `user_id` | FK → User | Auteur de l'action |
| `action_type` | Enum | Type : `created`, `status_changed`, `field_updated`, `proposal_added`, `converted` |
| `field_name` | String (nullable) | Nom du champ modifié |
| `old_value` | String (nullable) | Ancienne valeur |
| `new_value` | String (nullable) | Nouvelle valeur |
| `created_at` | DateTime | Date de l'action |

---

## 12. Estimation & Découpage

### Sprints suggérés

| Sprint | User Stories | Périmètre | Durée estimée |
|---|---|---|---|
| **Sprint 1** | US-O01, US-O02, US-O03 | Vue Résumé + Liste/Pipeline + Création d'opportunité | 2 semaines |
| **Sprint 2** | US-O04, US-O05, US-O06 | Édition + Gestion des statuts/probabilités + Conversion en projet | 2 semaines |
| **Sprint 3** | US-O07, US-O08 | Propositions commerciales + Génération depuis modèles | 1,5 semaine |
| **Sprint 4** | US-O09, US-O10 | Filtrage/recherche avancés + Export et actions en masse | 1,5 semaine |

**Estimation globale : 5 à 7 semaines de développement** (selon taille de l'équipe et maturité technique)

### Prérequis avant démarrage
- API Clients disponible (lecture + création)
- API Collaborateurs disponible (lecture)
- Charte graphique et composants UI validés (système de design)
- Maquettes UX validées pour les vues Résumé, Liste, Kanban et Détail
