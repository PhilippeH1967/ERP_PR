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
- **12 onglets fiche** : Vue d'ensemble, Phases, Tâches, Équipe, Temps, Avenants, Budget, Avancement, Gantt, Finance, Sous-traitants, Factures
- **Vue d'ensemble** : avancement par phase en **% heures / % coût / % honoraires** + total facturé réel
- **Équipe** : ajout de **profils virtuels sans avenant**, dropdown membres **recherchable**, affectation d'une **équipe entière** (paramétrage) sur le projet
- **Gantt interactif** : planification au niveau **tâche/sous-tâche** (tâche-mère/phase non cliquables = agrégats), contrôle budget non bloquant, 3 zooms, **jalons éditables (slide-over)**, dépendances FS/SS

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
