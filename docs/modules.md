# Modules

## Bloc 1 — Projets (apps: projects, clients, consortiums)

### Projets
- **WBS Option B** : Phase (conteneur) → Tâche (unité opérationnelle, code WBS 3.1, 3.2)
- **Wizard 5 étapes** : Identification → Budget & Phases → Ressources → Sous-traitants → Confirmation
- **Templates** : Architecture standard = 7 phases + 23 tâches auto-déployées
- **12 onglets fiche** : Vue d'ensemble, Phases, Tâches, Équipe, Temps, Avenants, Budget, Avancement, Gantt, Finance, Sous-traitants, Factures
- **Gantt interactif** : Barres phases, 3 zooms (mois/trimestre/année), jalons, dépendances FS/SS

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

### Planification
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
