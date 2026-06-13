# Modules

## Bloc 1 — Projets (apps: projects, clients, consortiums)

### Projets
- **WBS** : Phase → Tâche → Sous-tâche. La **phase** est un **regroupement standard** (paramétrage `StandardPhase`, admin) ; la **tâche/sous-tâche feuille** porte budget, dates, planif, facturation, temps ; phase et tâche-mère = **agrégats lecture seule**. Voir [changelog-structure-v1.2.md](changelog-structure-v1.2.md).
- **Wizard** : Identification (dont services transversaux) → **Phases** (toutes les phases standard instanciées vides, sans saisie manuelle) → Ressources → Sous-traitants → Confirmation
- **Services transversaux** (BIM, DD, Paysage…) : chaque service sélectionné devient une **phase de type SUPPORT** contenant **une tâche feuille imputable** du même nom (on impute du temps dessus). Remplace l'ancien `SupportService` non imputable (migration `projects 0016`).
- **Démarrage des tâches** : sur une phase sans tâche (ou pour compléter une phase), l'utilisateur ajoute des **tâches/sous-tâches depuis le catalogue standard** (`StandardTask`) ; les tâches déjà présentes sont exclues (dédup).
- **Coût de construction** : champ informatif `construction_cost` sur les **projets externes** (sert au calcul d'honoraires, masqué pour les projets internes).
- **Paramétrage** (*Administration*) : *Phases standard* (`StandardPhase`, admin), *Tâches standard* (`StandardTask`, catalogue tâches/sous-tâches par phase, admin), *Équipes* (`Team`, groupes réutilisables, finance/paie/admin)
- **Projet interne** : masqué pour tous sauf **admin** (queryset filtré sur `is_internal`)
- **Fiche projet — 7 onglets par intention** : 📊 Pilotage (KPI, alertes centralisées, avancement par phase % heures/coût/honoraires + facturé) · 📅 Échéancier (Phases / Tâches / Gantt) · 👥 Équipe & charge · ⏱ Temps · 💰 Finances · 📝 Avenants · ⚙️ Paramètres. Aide contextuelle « ? » dans la barre du haut (contenu par écran/onglet).
- **Fiche tâche unique** : clic sur le nom d'une tâche (Tâches ou Gantt) → un seul panneau pour tout éditer (identité, libellé client, phase, dates, budget/facturation, affectations, ouverture/fermeture de la saisie, suppression).
- **Échéancier** : dates Début/Fin **éditables inline** sur les tâches feuilles (fin ≥ début à la frappe, dates dérivées sur les tâches-mères) + **« Décaler l'échéancier »** de N jours en masse.
- **Affectation unifiée** : dialogue **Qui ? (employé / équipe / profil virtuel) → Où ? (projet / phase / tâche) → Combien ? (h-sem, période)** — remplace les canaux parallèles ; avertissement non bloquant si dépassement du budget de la tâche.
- **Équipe & charge** : vues « Par phase » (arbre + personnes, recherche « où est X ») et « Par personne » ; **blocages de saisie** : fermeture globale d'une tâche/phase (tout le monde) ou ciblée `TimeEntryBlock` (personne × tâche / phase / **projet entier**), réversibles, grisé/barré.
- **Budget = une seule porte d'entrée** : il se saisit sur la **tâche** (Échéancier ou fiche tâche) ; Finances › Budget est une **synthèse en lecture seule**.
- **⚙️ Paramètres du projet** : infos (nom, dates, responsables, coût de construction), **carte Client** (changement de client, adresses — ajout/édition au projet, **suppression réservée à la fiche client**, anti-doublon backend ; **adresse de facturation propre au projet** `Project.billing_address`, repli sur le défaut client), profils virtuels (CRUD + remplacement), blocages actifs, liens vers les référentiels admin.
- **Gantt interactif** : planification au niveau **tâche/sous-tâche** (tâche-mère/phase non cliquables = agrégats), contrôle budget non bloquant, 3 zooms, **jalons éditables (slide-over)**, dépendances FS/SS
- **Rattrapage** : commande `backfill_support_phases` (services transversaux → phases SUPPORT + tâche imputable pour les projets antérieurs à la conversion).

### Clients
- CRUD avec 5 onglets : Informations, Contacts, Adresses, Financier, Projets
- Recherche live (nom, alias, secteur)
- Schéma fiscal assignable (TPS+TVQ, TVH, etc.)

### Consortium (FR59-FR64)
- Entity avec membres + coefficients (= 100%)
- Vue duale : panneau bleu (consortium) + jaune (Provencher)
- 6 onglets : Overview, Vue duale, Projets, Factures partenaires, Distributions, Taxes

## Bloc 2 — Production (apps: time_entries, leaves, suppliers, planning)

### Feuilles de temps
- Grille hebdomadaire par tâche WBS
- Workflow 6 états : DRAFT → SUBMITTED → PM_APPROVED → FINANCE_APPROVED → PAIE_VALIDATED → LOCKED
- 11 contrôles paie automatisés (overtime+sick, 50h max, weekend, trend)
- Period locking : gel global, exceptions, verrouillage phase/personne
- Heures contrat dynamiques (LaborRule)
- Relances Wed/Fri + escalade PM
- **Discipline de soumission** (PR #74) : si une semaine a ≥ 2 semaines de retard sans
  soumission, tous les chemins d'écriture sont bloqués pour la semaine courante/future
  (`create`, `update`, `copy_previous_week`, `prefill_holidays`) via un helper unique
  `_check_submission_discipline()`. La régularisation des semaines en retard reste
  toujours possible. Code retour : `400 LATE_TIMESHEETS`.
- **Heures facturées intouchables** (PR #74) : une entrée avec `is_invoiced=True` est
  protégée à deux niveaux :
  - **modèle** : `TimeEntry.save()` refuse toute modification des champs
    `INVOICED_PROTECTED_FIELDS` (`hours`, `date`, `project_id`, `task_id`,
    `employee_id`) ; les transitions de statut (ex. PM_APPROVED → LOCKED) restent
    permises.
  - **signal** `pre_delete` : déclenche un `ProtectedError` à la suppression directe
    ou en cascade (suppression de la tâche parente).
  - **API** : `bulk_correct`, `transfer_hours`, `reject_entries`, `reject_pm` ignorent
    ou refusent silencieusement les entrées facturées. La suppression d'une tâche via
    l'API (`TaskViewSet.perform_destroy`) retourne `400` si des entrées facturées
    existent. Code retour : `400 ENTRY_INVOICED`.
- **Frontend** : `TimesheetCell` affiche le message d'erreur backend (LATE_TIMESHEETS,
  ENTRY_INVOICED…) et revient à la valeur précédente. `getMondayOfWeek` / `getDatesForWeek`
  calculent en heure locale (pas UTC) — correction dérive soirée en fuseaux ouest.
  `lateBlocked` ne s'applique qu'à la semaine courante/future ; `goToWeek` vide
  immédiatement les entrées avant le fetch suivant.

### Congés / Absences
- 7 types Québec : Vacances, Maladie, Personnel, Férié, Parental, Sans solde, Deuil
- Workflow : PENDING → APPROVED/REJECTED/CANCELLED
- Banque de soldes (accrued, used, carried_over, manual_adjustment)
- Auto-create TimeEntry sur approbation

### Fournisseurs / ST
- 6 entités : ExternalOrganization, STInvoice, STPayment, STCreditNote, STDispute, STHoldback
- Workflow : received → authorized → paid / disputed
- Batch authorize, holdback release, summary par fournisseur

### Occupation des ressources
> Anciennement « Planification » (libellé UI renommé — page `/planning` et menu).
> Le concept interne (allocation, Gantt) est inchangé.

- ResourceAllocation (employé → projet, hours/week)
- Détection surcharge (>100%) / sous-charge (<50%) / critique (>120%)
- Milestones avec auto-détection retards
- Disponibilité = contract - congés

## Bloc 3 — Financier (apps: billing, expenses, data_ops)

### Facturation
- **6 schémas fiscaux** : Québec TPS+TVQ, Ontario TVH, Alberta TPS, BC GST+PST, France TVA, Exonéré
- Calcul taxes dynamique via TaxScheme → TaxRate
- 7 colonnes : livrable, budget, facturé, % avancement, % heures, à facturer, % après
- Workflow : DRAFT → SUBMITTED → APPROVED → SENT → PAID
- Notes de crédit, paiements, retenues client, write-offs

### Dépenses
- 15 catégories standard (Transport, Repas, Hébergement, Fournitures...)
- Workflow : SUBMITTED → PM_APPROVED → FINANCE_VALIDATED → PAID
- Upload reçu, refacturation client

### Exports Intacct Phase 1
- 4 exports CSV : factures, paiements, dépenses, feuilles de temps
- Filtrable par mois/année pour les temps

## Bloc 4 — Pilotage (apps: dashboards, data_ops)

### Dashboard
- 5 rôles avec KPIs adaptés
- PM : heures ce mois, ratio CA/salaires (cible 2.5x), taux facturation, carnet commandes
- Finance : factures impayées, dépenses en attente
- Admin : system health (actifs, approbations, factures en retard)

### Rapports
- Heures groupables par projet / employé / BU
- Export CSV intégré
- Filtres par période

### Import / Migration
- 13 types d'import (6 ref data + 7 transactional)
- Handler spécialisé ST invoices
- Command `import_changepoint`
