# Reflexion Party Mode : Saisie initiale des projets et gestion du temps

**Date** : 2026-03-03
**Participants** : Philippe Haumesser + agents BMAD (John PM, Sally UX, Winston Architect, Mary Analyst, Amelia Dev, Bob SM)
**Mockups** : `_bmad-output/mockups/erp-mockups.html` (7 ecrans interactifs)

---

## 1. Contexte et objectif

Lorsqu'un projet est gagne, le PM doit pouvoir le saisir rapidement dans le systeme avec tous les champs importants sans que ce soit complexe ou intimidant. Le systeme doit etre simple pour les PM et administrateurs qui ne sont pas des utilisateurs techniques.

**Principe directeur** : Creer vite, completer au fil de l'eau. Jamais de page blanche.

---

## 2. Mode contractuel

- Le mode principal est **Forfaitaire** (represente la grande majorite des projets)
- Autres modes supportes : Cost Plus, IPD/Alliance, Pain/Gain (GMP), Co-developpement
- **Le mode contractuel est un champ pivot** qui pourra conditionner l'affichage de champs specifiques dans le futur

---

## 3. Cout de construction

- Le cout de construction est **purement informatif**
- Il ne pilote PAS le calcul des honoraires ni les heures du template
- Utile comme **KPI retrospectif** (ratio honoraires/cout construction pour les futures soumissions)
- Saisi des la creation du projet

---

## 4. Structure de projet : deux axes

### Axe 1 — Phases de realisation (sequentielles)

| # | Phase | Nature |
|---|---|---|
| 1 | Etude preparatoire | Analyse / faisabilite |
| 2 | Concept | Creation |
| 3 | Preliminaire | Developpement |
| 4 | Definitif | Finalisation |
| 5 | Appel d'offres | Documentation contractuelle |
| 6 | Surveillance | Chantier |

### Axe 2 — Services support (globaux au projet, transversaux)

- Gestion de projet
- BIM
- 3D / Visualisation
- Paysage
- Design
- (extensible)

**Decision cle** : Les services support sont des **taches autonomes au niveau projet**, pas ventilees par phase. Le PM suit les heures BIM globalement, pas par phase.

---

## 5. Templates de projet

- Les templates pre-configurent les phases (cochees par defaut) et les services support (a cocher)
- Le PM ajuste : active/desactive des phases ou services
- Le template est un **point de depart, pas une contrainte** — modifiable apres creation
- Approche hybride recommandee : quelques templates types comme accelerateur, PM modifie librement

---

## 6. Profils virtuels

### Concept

Les profils virtuels sont des **archetypes de ressources** positionnees sur les taches AVANT d'affecter des employes reels. Ils servent a :
1. **Budgetisation** — chaque profil a un taux horaire moyen
2. **Planification** — positionnement dans le temps
3. **Reservation de capacite** — visibilite de la charge a venir

### Liste des profils types (referentiel entreprise, configurable)

- Charge de projet
- Charge de conception
- Charge d'execution
- Architecte junior / intermediaire / senior
- Technologue junior / intermediaire / senior
- Specialiste BIM
- Specialiste 3D
- (extensible par la firme)

### Positionnement

- Profils virtuels positionnes sur les **taches principales** (phases + services support)
- Sous-taches : profil virtuel **optionnel**, herite du parent par defaut
- Les heures sont la **responsabilite du PM**, pas du systeme

---

## 7. Affectation des ressources (virtuel vers reel)

### Principe multi-affectation

- Un profil virtuel peut etre remplace par **un ou plusieurs employes**
- Repartition en **pourcentage** (ex: Sophie 60% = 90h, Jean 40% = 60h sur 150h totales)
- Le PM peut affecter partiellement (50% couvert) et completer plus tard

### Priorisation dans la liste d'affectation

La modale de selection presente les employes en **3 niveaux de priorite** :
1. **Profil correspondant** — employes avec exactement le meme titre (en premier, avec disponibilite)
2. **Profils similaires** — profils proches (ex: architecte junior ou senior pour un poste intermediaire)
3. **Autres employes** — tout le monde, si le PM veut quelqu'un d'autre

### Indicateurs

- Disponibilite en % pour chaque employe
- Statut par affectation : Complet (100%), Partiel (< 100%), Virtuel (personne affectee)

---

## 8. Saisie de temps des employes

### Principe fondamental

L'employe ne voit **QUE les projets et taches ou il est affecte**. Pas de liste deroulante de 200 projets. Le meilleur controle = l'absence de mauvaise option.

### Mecanique

- L'affectation d'un employe reel **cree automatiquement les permissions de saisie**
- Pas d'affectation = pas visible dans la feuille de temps
- Vue **hebdomadaire** standard (Lun-Ven)
- Regroupement : Projet > Phases | Support

### Format de la feuille de temps

```
Projet Alpha
  > Phases
     Concept           [3] [4] [ ] [2] [ ]  = 9h
     Preliminaire      [2] [ ] [4] [3] [4]  = 13h
  > Support
     Gestion de projet [1] [1] [1] [1] [1]  = 5h
```

- Total journalier avec indicateur si different de la norme (7.5h ou 8h)
- Bouton "Sauvegarder brouillon" + "Soumettre la semaine"

---

## 9. Blocage des phases et personnes

### Deux niveaux de blocage

1. **Phase bloquee** — plus personne ne saisit sur cette phase (ex: Etude preparatoire terminee)
2. **Personne bloquee sur une phase** — un individu specifique ne peut plus saisir, mais les autres oui

### Comportement UX

- Phase bloquee : visible en **gris avec cadenas** dans la feuille de temps, historique consultable
- Blocage en **1 clic** par le PM depuis l'ecran de gestion des acces
- Deblocage possible si necessaire

---

## 10. Tableau de bord PM

- Vue d'ensemble de tous les projets actifs
- Par projet : phase en cours, % budget utilise, indicateur couleur (vert/jaune/rouge)
- Alertes : budget critique, affectations manquantes
- Bouton d'acces rapide "Nouveau projet"

---

## 11. Parcours complet (6 etapes)

| Etape | Qui | Action | Resultat |
|---|---|---|---|
| 1 | PM | Cree le projet, choisit le template | Phases + supports pre-configures |
| 2 | PM | Positionne les profils virtuels avec heures | Budget previsionnel par tache |
| 3 | PM | Affecte des employes reels (1 ou plusieurs par profil) | Permissions de saisie creees |
| 4 | Employe | Saisit son temps (ne voit que ses taches) | Heures imputees correctement |
| 5 | PM | Bloque une phase/personne | Saisie stoppee chirurgicalement |
| 6 | PM | Consulte le reporting | Reel vs budgete, par profil, par tache |

---

## 12. Sous-traitants et consultants externes

### Trois couches budgetaires d'un projet

Le budget d'un projet d'architecture comporte trois couches distinctes :

| Couche | Description | Exemple |
|---|---|---|
| **Honoraires internes** | Travail de la firme (heures × taux) | Architectes, technologues, BIM... |
| **Sous-traitants refactures** | Consultants externes factures au client | Ingenieurs structure, mecanique, electrique... |
| **Sous-traitants absorbes** | Consultants payes par la firme, non refactures | Consultant specialise, LEED... |

### Types de sous-traitants (referentiel configurable)

- Ingenieur en structure
- Ingenieur mecanique
- Ingenieur electrique
- Ingenieur civil
- Consultant acoustique
- Consultant LEED
- (extensible par la firme, comme les profils virtuels)

### Attributs par sous-traitant sur un projet

- **Nom du type** (ex: Ingenieur en structure)
- **Fournisseur** (ex: Groupe SMI) — optionnel a la creation
- **Budget prevu** (montant global, pas en heures)
- **Est refacturable** : oui / non
- **Majoration %** (ex: 10%, 0% pour pass-through)
- **Montant client** = budget × (1 + majoration%) — calcule automatiquement

### Differences avec les honoraires internes

- Pas de profils virtuels — on gere un **budget global par consultant**, pas des heures
- Suivi par **factures recues** vs budget prevu (pas par saisie de temps)
- Les templates de projet peuvent pre-configurer les types de sous-traitants frequents

### Impact sur la vue projet

Troisieme section/onglet dans la vue projet : **[Phases] [Support] [Sous-traitants] [Sommaire]**

Le sommaire consolide :
- Total honoraires internes
- Total sous-traitants
- Total cout projet
- Total refacture au client (avec majorations)
- Distinction refacturable vs absorbe pour calculer la **marge reelle**

### Suivi budgetaire sous-traitants

Pour chaque sous-traitant : Budget prevu → Factures recues → Ecart
La distinction refacturable/absorbe determine la marge reelle du projet.

---

## 13. Cycle de facturation

### Deux couches distinctes

Le projet comporte deux structures paralleles :
- **Couche realisation** (PM) : phases de travail, profils, heures, equipe
- **Couche financiere** (Compta) : phases de facturation, taux contractuels, echeancier

Les phases financieres **ne sont pas identiques** aux phases de realisation. Une phase financiere peut regrouper plusieurs phases de realisation.

### Configuration financiere (Compta, au demarrage du projet)

La Compta definit pour chaque projet :
1. Les **phases financieres** (ex: "Etudes" couvre Etude prep. + Concept)
2. Le **mode de facturation par phase** : forfait OU horaire
3. Les **montants forfaitaires** ou **budgets max** (horaire)
4. Les **taux horaires contractuels** par profil (differents des taux internes)
5. L'**echeancier** par phase

### Modes de facturation dans un meme projet

Un projet forfaitaire peut avoir des phases avec des modes differents :

| Phase financiere | Mode | Montant/Budget | Phases realisation liees |
|---|---|---|---|
| Etudes | Forfait 45 000 $ | Fixe | Etude prep. + Concept |
| Plans | Forfait 120 000 $ | Fixe | Preliminaire + Definitif |
| Appel d'offres | Horaire | Max 35 000 $ | Appel d'offres |
| Surveillance | Horaire | Max 80 000 $ | Surveillance |
| BIM | Forfait 30 000 $ | Fixe | BIM (support) |

### Echeancier de facturation

- **Phases forfaitaires** : facturation par **% d'avancement** (jalons)
  - Exemple : 20% au debut, 50% a mi-phase, 100% a la fin
  - Le PM met a jour le % d'avancement mensuellement (slider simple)
  - Le systeme detecte quand un jalon est atteint → ligne de facturation

- **Phases horaires** : facturation **mensuelle** automatique
  - Le systeme compile les heures saisies du mois
  - Applique les taux horaires contractuels (pas les taux internes)
  - Genere le brouillon de facture

### Taux horaires : deux niveaux

| Type | Usage | Exemple Arch. senior |
|---|---|---|
| **Taux interne** | Cout reel pour la firme | 165 $/h |
| **Taux contractuel** | Facture au client (phases horaires) | 185 $/h |
| **Ecart = marge** | Profit par heure | 20 $/h |

Les taux contractuels sont definis par la Compta au niveau du projet (peuvent varier selon le contrat).

### Cycle mensuel de facturation

```
1. PM met a jour % avancement par phase (10 secondes, slider)
2. Systeme compile les heures du mois (automatique)
3. Systeme genere le brouillon de facture :
   - Phases forfait : jalons atteints ce mois
   - Phases horaires : heures × taux contractuels
   - Sous-traitants : factures recues refacturables + majorations
   - Retenues contractuelles appliquees
4. Compta revise et valide
5. Facture envoyee au client
```

### Structure de la facture mensuelle

```
HONORAIRES
  Phases forfaitaires (jalons atteints)      XX XXX $
  Phases horaires (heures du mois)           XX XXX $
SOUS-TRAITANTS REFACTURABLES
  Factures recues + majorations              XX XXX $
SOUS-TOTAL                                   XX XXX $
  Retenue contractuelle X%                   -X XXX $
TOTAL A FACTURER                             XX XXX $
```

### Rapprochement rentabilite (tableau de bord)

Pour chaque phase financiere :
- Montant contractuel vs facture a date vs cout interne reel → **marge reelle**
- Phases forfait : si le cout interne depasse le forfait, on perd de l'argent
- Phases horaires : marge = (taux contractuel - taux interne) × heures

---

## 14. Taches non facturables

### Principe

Certaines taches d'un projet sont du travail reel mais ne generent aucune facturation au client. Elles consomment des heures et coutent de l'argent a la firme.

### Trois niveaux de facturabilite

| Facturabilite | Lien financier | Impact revenus |
|---|---|---|
| **Facturable (forfait)** | Liee a une phase financiere forfaitaire | Revenus fixes |
| **Facturable (horaire)** | Liee a une phase financiere horaire | Heures × taux contractuel |
| **Non facturable** | Aucune phase financiere | 0$ — cout pur |

### Exemples de taches non facturables

- Concours d'architecture (travail preliminaire avant contrat)
- Reprise de travail (erreur interne)
- Coordination interne non prevue au contrat
- Formations specifiques au projet
- Taches administratives projet

### Modelisation

```
Tache
  - est_facturable     → boolean
  - phase_financiere   → FK (nullable — null si non facturable)
```

Les heures sur taches non facturables sont saisies et suivies normalement, mais ne remontent pas dans le cycle de facturation.

### Impact sur la rentabilite

Les heures non facturables apparaissent comme **cout interne pur** dans le suivi de rentabilite :
- Revenus totaux (factures + a facturer)
- Couts internes facturables
- **Couts internes NON facturables** ← rendu visible
- Sous-traitants absorbes
- = Marge nette reelle

---

## 15. Ecran de preparation de facture

### Vue principale — Tableau de preparation mensuelle

L'ecran cle pour la Compta. Un seul tableau avec toutes les donnees necessaires pour preparer la facture du mois.

### Colonnes du tableau

| # | Colonne | Contenu | Editable? |
|---|---|---|---|
| 1 | **Livrable** | Nom de la phase financiere ou sous-traitant | Non |
| 2 | **Montant total** | Montant contractuel (reference fixe) | Non |
| 3 | **Facture a ce jour** | Cumul de tout ce qui a ete facture | Non |
| 4 | **% Avancement facturation** | Col.3 / Col.2 | Non (calcule) |
| 5 | **% Avancement heures / Factures fournisseurs** | Forfait : heures consommees / heures budgetees. Sous-traitants : montant cumule des factures recues du fournisseur | Non (calcule) |
| 6 | **Facturer ce mois** | Montant a facturer — LA decision de la Compta | **OUI** |
| 7 | **% Avancement apres facturation** | (Col.3 + Col.6) / Col.2 — projection | Non (recalcul temps reel) |

### Regles par type de livrable

- **Forfait** : Colonne 6 saisie manuellement par la Compta, colonne 5 (% heures) visible pour comparaison
- **Horaire** : Colonne 6 pre-remplie automatiquement (heures du mois × taux contractuels), modifiable
- **Sous-traitants** : Colonne 6 = factures recues ce mois + majorations

### Signaux visuels (alertes automatiques)

| Condition | Signal |
|---|---|
| % heures > % facturation + 10pts (forfait) | Fond rouge — on surproduit vs ce qu'on facture |
| % heures < % facturation (forfait) | Fond vert — facturation en avance |
| % apres facturation > 90% | Badge jaune — fin de budget proche |
| Heures > 0 mais facturation = 0$ | Icone attention — travail non facture |

### Sections du tableau

1. **Honoraires forfait** (phases financieres au forfait)
2. **Honoraires horaire** (phases financieres a l'horaire, avec budget max)
3. **Sous-traitants refacturables** (avec majorations)
4. **Total + retenue contractuelle + net a facturer**

Les livrables non facturables et sous-traitants absorbes ne sont PAS dans ce tableau (pas de facturation associee).

### Ratio CA / Salaire (indicateur global)

Bandeau affiche au-dessus du tableau de facturation avec deux valeurs cote a cote :

- **Ratio AVANT facturation** = CA facture a ce jour / Salaires imputes a ce jour
- **Ratio APRES facturation** = (CA facture + facturation ce mois) / Salaires imputes projetes
- **Cible firme** = ratio minimum vise par la firme (configurable, ex: 2.80)

Le ratio CA/Salaire est **global au projet**, pas par phase. Il se recalcule en temps reel quand la Compta modifie les montants a facturer.

C'est l'indicateur de sante financiere du projet :
- Ratio > cible → projet rentable
- Ratio < cible → alerte, le projet perd de la marge
- Evolution du ratio (delta avant/apres facturation) → tendance

### Colonne "% Avanc. heures" pour les sous-traitants

Pour les sous-traitants, cette colonne affiche le **montant cumule des factures recues du fournisseur** (et non un % d'heures, puisqu'on ne gere pas leurs heures). Cela permet de comparer :
- Ce qu'on a facture au client (col. 3) vs ce que le fournisseur nous a facture (col. 5)
- Detecter les ecarts : si on a facture 52 800$ au client mais le fournisseur nous a envoye 66 000$ de factures → on est en retard de refacturation

---

## 16. Suivi des bons a payer et paiements sous-traitants

### Principe

Le suivi des factures fournisseurs et des paiements est un flux **completement independant** de la facturation client. Les deux cycles vivent separement et ne se rejoignent que dans le reporting de rentabilite.

### Cycle de vie d'une facture fournisseur

```
1. RECUE       → La facture est entree dans le systeme (PM ou Compta)
2. AUTORISEE   → Le PM a verifie et approuve le bon a payer
3. PAYEE       → La Compta a effectue le paiement
```

Chaque facture est dans UN de ces trois etats a tout moment.

### Separation des responsabilites

- **PM** : recoit/entre les factures, verifie la conformite, autorise le paiement (bon a payer)
- **Compta** : execute les paiements, tient le registre

### Modelisation

```
FactureFournisseur
  - tache_id            → FK vers Tache (type 'consultant')
  - fournisseur         → nom du sous-traitant
  - numero_facture      → reference du fournisseur
  - date_reception      → date de reception
  - montant             → montant de la facture
  - statut              → 'recue' | 'autorisee' | 'payee'
  - date_autorisation   → date du bon a payer (nullable)
  - autorise_par        → FK employe (PM qui approuve)
  - date_paiement       → date effective du paiement (nullable)
  - commentaire         → note optionnelle
```

### Trois vues necessaires

**Vue 1 : Suivi par sous-traitant (PM)** — dans le contexte d'un projet
- Liste des factures d'un fournisseur sur le projet
- Cumul vs budget prevu
- Indicateurs : total recu / total autorise / total paye / budget restant / autorise non paye
- Action : autoriser une facture recue

**Vue 2 : Bons a payer en attente (Compta)** — multi-projets
- Toutes les factures autorisees mais non payees, tous projets confondus
- Action : marquer comme payee

**Vue 3 : Rapport de paiements a effectuer (Compta)** — multi-projets, groupe par fournisseur
- Liste des paiements a faire, groupes par fournisseur
- Un meme fournisseur peut avoir des factures de plusieurs projets → un seul paiement possible
- Avec montants et dates d'autorisation
- Export possible

### Independance des flux

```
FLUX SORTANT (on paie)              FLUX ENTRANT (on facture)
Facture fournisseur recue           Preparation facture client
  → PM autorise                       → Compta prepare
  → Compta paie                       → Client paie

Aucun lien direct entre les deux.
On peut payer un fournisseur AVANT de l'avoir refacture, ou l'inverse.
Les deux flux se rejoignent uniquement dans le REPORTING de rentabilite.
```

---

## 17. Offres de services

### Concept

Les offres de services sont le pipeline commercial de la firme. Chaque projet commence potentiellement par une offre qui consomme du temps et de l'argent AVANT qu'on sache si on gagne. C'est du temps **non facturable** par nature.

### Cycle de vie d'une offre

```
Creee → En cours → Soumise → Gagnee → Convertie en projet
                          → Perdue → Archivee
                          → Abandonnee → Archivee
```

### Comparaison offre vs projet

| Attribut | Offre de services | Projet |
|---|---|---|
| Code | Code offre (OFF-2026-015) | Code projet (PRJ-2026-047) |
| Client | Client de l'offre (donneur d'ouvrage AO) | Client du projet (peut differer) |
| Saisie de temps | Oui, avec autorisations (meme mecanisme) | Oui, avec autorisations |
| Facturable | **Non** — temps absorbe | Oui (forfait/horaire) |
| Taches | Simples (analyse, conception, redaction, montage, presentation) | Phases + Support + Sous-traitants |
| Profils virtuels | Non | Oui |
| Sous-traitants | **Non** | Oui |
| Couche financiere | **Non** | Oui |
| Budget | Budget interne d'effort (heures) | Budget contractuel |

### Modelisation

```
OffreService
  - code               → "OFF-2026-015"
  - titre              → "Concours Centre sportif Laval"
  - client_offre       → "SQI"
  - date_soumission    → date limite
  - statut             → 'en_cours' | 'soumise' | 'gagnee' | 'perdue' | 'abandonnee' | 'convertie'
  - budget_effort      → heures internes budgetees
  - est_facturable     → false (toujours)
  - projet_lie         → FK vers Projet (nullable, rempli a la conversion)
```

Reutilise les memes modeles Tache, Affectation, EntreeTemps que les projets. Distinction par champ `type_entite` : 'offre' ou 'projet'.

### Autorisations de saisie de temps

Meme mecanisme que les projets : l'employe ne voit l'offre dans sa feuille de temps QUE s'il est affecte. Le PM controle qui peut imputer du temps sur l'offre.

### Taches types d'une offre (modele standard)

- Analyse du programme
- Conception / esquisse
- Redaction technique
- Montage de la soumission
- Presentation / jury
- (extensible)

### Conversion offre → projet

Quand l'offre est gagnee, le PM la convertit en projet :

- **Nouveau code projet** genere (PRJ-2026-047)
- **Client projet** : peut differer du client de l'offre (alerte visuelle si different)
- **Choix du template** projet, mode contractuel, etc.
- **Le projet demarre vierge** : pas de transfert d'equipe, pas de transfert de donnees operationnelles
- **L'offre est fermee** avec statut "convertie" et lien vers le projet
- **L'historique temps de l'offre est conserve** comme reference (non inclus dans le budget projet)

### Suivi client offre vs projet

Quand le client du projet differe du client de l'offre :
- Les deux sont conserves dans le systeme
- Exemple : Offre pour la SQI → Projet pour la Ville de Laval
- Utile pour le reporting : a quel donneur d'ouvrage on repond vs pour qui on travaille

### Reporting commercial

- **Taux de conversion** : offres gagnees / offres totales
- **Cout moyen par offre** : heures et $ investis par offre
- **Cout d'acquisition projet** : si 1 offre sur 4 gagnee et cout moyen 200h, alors cout d'acquisition = 800h
- **Offres perdues** : cout commercial visible, ne disparait pas

### Ecrans necessaires

1. **Tableau de bord PM** — section "Mes offres actives" avec statut et countdown date limite
2. **Creation d'offre** — un seul ecran, 5-6 champs + taches cochables
3. **Vue offre** — suivi temps impute, budget restant, statut
4. **Changement de statut** — boutons contextuels (Soumise, Gagnee, Perdue, Abandonnee)
5. **Conversion en projet** — nouveau code, client confirme/change, template, reference cout offre

---

## 18. Principes UX retenus

- **Regle des 5 minutes** : un nouvel employe saisit son temps sans formation en < 5 min
- **Creation projet en 2 ecrans** : infos de base + structure (phases/services)
- **Formulaire progressif** : creer vite, completer au fil de l'eau
- **Barre de completion** : "Projet configure a X%" avec rappels doux
- **Chaque ecran a UNE action principale evidente**
- **Pas de jargon technique** dans l'interface
- **Le template fait le gros du travail** — le PM ajuste, il ne cree pas de zero

---

## 19. Architecture technique (notes)

### Structure des taches

```
Tache (Task)
  - projet_id       → FK vers Projet
  - type            → 'phase' | 'support' | 'consultant'
  - nom             → "Concept", "BIM", "Ing. structure", etc.
  - ordre           → sequence (pour les phases)
  - is_locked       → boolean (blocage global)

  # Champs specifiques aux sous-traitants (type = 'consultant')
  - fournisseur       → nom du sous-traitant (optionnel)
  - budget_prevu      → montant global en $
  - est_refacturable  → boolean
  - majoration_pct    → pourcentage de majoration
  - montant_client    → calcule (budget × (1 + majoration%))
```

### Affectations

```
Affectation
  - tache_id           → FK vers Tache
  - profil_virtuel_id  → FK (avant affectation reelle)
  - employe_id         → FK (apres affectation reelle, nullable)
  - pourcentage        → % de repartition des heures
  - heures_budgetees   → heures calculees selon %
  - is_locked          → blocage individuel
```

### Entrees de temps

```
EntreeTemps
  - employe_id  → FK
  - tache_id    → FK
  - date        → date
  - heures      → decimal
  - note        → texte optionnel
```

- Controle a l'ecriture : si l'affectation n'existe pas ou est bloquee → rejet
- Un seul modele pour phases et support, distingues par le champ `type`

---

## 20. Mockups HTML

Fichier : `_bmad-output/mockups/erp-mockups.html`

7 ecrans navigables :
1. Tableau de bord PM
2. Nouveau projet (1/2) — Informations
3. Nouveau projet (2/2) — Structure phases/services
4. Profils virtuels — Grille avec heures et couts
5. Affectation ressources — Multi-affectation avec % et priorisation
6. Feuille de temps — Vue hebdomadaire avec phases bloquees
7. Blocage phases — Controle par phase et par personne

**A creer** : ecran Sous-traitants (section/onglet dans la vue projet avec budget, refacturation, majorations)

---

## 21. Gestion des consortiums

Un consortium est une association de plusieurs acteurs (firmes) qui travaillent ensemble pour repondre a un projet client. Le consortium est l'entite qui facture le client final. Les membres facturent leurs activites au consortium.

### Modele de donnees

- **Entite Consortium distincte** : chaque consortium est une entite a part entiere dans le systeme
- **Attributs du consortium** :
  - Nom / Identifiant
  - Liste des membres avec leur coefficient respectif (salaire × coefficient = base de facturation)
  - Regle de partage du profit : fixe (defini dans l'accord) OU proportionnel a l'effort
  - Si proportionnel : base de calcul (heures ou $ factures)
  - Role de Provencher : mandataire (gestionnaire) ou simple partenaire
- **Relation 1-N avec projets** : un consortium peut avoir plusieurs projets, chaque projet est independant pour le calcul du partage de profit
- Chaque membre negocie son propre coefficient dans l'accord de consortium

### Regle comptable critique

- Les revenus du consortium (factures au client final) ne sont **PAS** dans le chiffre d'affaires de Provencher_Roy
- Le CA de Provencher = factures emises par Provencher au consortium + part de profit du consortium
- Cette regle impacte directement le reporting financier et les tableaux de bord

### Operations quotidiennes

- **Saisie de temps** : identique aux projets normaux. Les employes imputent normalement sur le projet
- **Facturation** : meme ecran de preparation de facture que les projets standard. Pas de difference d'interface
- **Cycle de facturation** : identique aux projets traditionnels (cycle mensuel)

### Vues specifiques consortium

1. **Double vision financiere** :
   - Vue consortium : revenus client final, couts des membres (factures recues), marge, partage
   - Vue Provencher : factures emises au consortium + part de profit = CA Provencher
2. **Visibilite** : les PMs, Finance et Directeurs BU voient les couts/heures de Provencher ET des autres membres
3. **Donnees des partenaires** : arrivent via les factures recues des partenaires (saisie manuelle ou API avec la comptabilite)

### Tableau de bord directeur BU

- **Tableau recapitulatif** de tous les consortiums actifs
- Par consortium : liste des projets, ratios, avancement, montant des factures client final impayees
- Donnees alimentees par saisie manuelle ou API comptabilite
- **Separation** : les projets consortium ont leur propre vue, distincte des projets standard, mais la vue projets standard est enrichie de la part de profit

### Creation de projet consortium

- A la creation d'un projet, le PM **coche "Projet consortium"**
- Puis **selectionne un consortium existant** ou **en cree un nouveau**
- Le reste du flux de creation est identique aux projets standard
