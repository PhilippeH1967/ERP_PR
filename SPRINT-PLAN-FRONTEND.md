# Plan de Sprints — Frontend MVP-1 Gaps

**Version**: 1.1.001 → 1.1.010
**Objectif**: Combler 100% des gaps frontend pour atteindre la parité avec le backend MVP-1
**Estimé**: 6 sprints

---

## Sprint F1 — Facturation complète (Priorité critique)
> La facturation est le cœur du revenu. Sans elle, pas de go-live.

| # | Tâche | Fichier | API backend |
|---|-------|---------|-------------|
| F1.1 | Bouton "+ Nouvelle facture" dans InvoiceList | InvoiceList.vue | POST /invoices/ |
| F1.2 | Formulaire création facture (projet, client, lignes) | InvoiceCreate.vue (new) | POST /invoices/ + POST /lines/ |
| F1.3 | Boutons "Envoyer" et "Marquer payée" dans InvoiceDetail | InvoiceDetail.vue | PATCH status |
| F1.4 | Enregistrement paiement (formulaire + liste) | PaymentList.vue | POST /payments/ |
| F1.5 | Page Notes de crédit (CRUD) | CreditNoteList.vue (new) | /credit_notes/ |
| F1.6 | Page Retenues/Holdbacks (CRUD) | HoldbackList.vue (new) | /holdbacks/ |
| F1.7 | Page Write-offs (CRUD) | WriteOffList.vue (new) | /write_offs/ |
| F1.8 | Aging analysis dans InvoiceDetail ou ClientDetail | Existants | GET /aging_analysis/ |
| F1.9 | Routes pour nouvelles pages billing | router/index.ts | — |

**Version cible**: 1.1.002

---

## Sprint F2 — Dépenses + Fournisseurs (Priorité haute)
> Workflows d'approbation critiques pour les opérations quotidiennes.

| # | Tâche | Fichier | API backend |
|---|-------|---------|-------------|
| F2.1 | Upload reçu fonctionnel (PDF/image) | ExpenseCreateForm.vue | POST multipart |
| F2.2 | Détail rapport de dépense (lignes + reçus) | ExpenseDetail.vue (new) | GET /expense_reports/{id}/ |
| F2.3 | Workflow approbation dépenses (PM → Finance) | ExpenseDetail.vue | PATCH status |
| F2.4 | Boutons approbation dans liste dépenses | ExpenseList.vue | PATCH |
| F2.5 | Templates dépenses récurrentes (Taxi, Repas, etc.) | ExpenseList.vue | — |
| F2.6 | Factures ST — CRUD complet | STInvoiceList.vue | Backend à créer si manquant |
| F2.7 | Workflow ST: Reçue → Autorisée → Payée | STInvoiceDetail.vue (new) | PATCH status |
| F2.8 | Suivi budget cumulatif ST par projet | STInvoiceList.vue | Agrégation |

**Version cible**: 1.1.003

---

## Sprint F3 — Projets enrichis (Priorité haute)
> Compléter les interactions projet manquantes.

| # | Tâche | Fichier | API backend |
|---|-------|---------|-------------|
| F3.1 | Boutons Modifier/Supprimer projet | ProjectDetail.vue | PUT/DELETE /projects/{id}/ |
| F3.2 | Changement statut projet (Active→On Hold→Completed) | ProjectDetail.vue | PATCH status |
| F3.3 | Page Avenants (CRUD dans onglet projet) | ProjectDetail.vue (tab) | /amendments/ |
| F3.4 | Affectation employé par nom (recherche) au lieu d'ID | AssignmentModal.vue | — |
| F3.5 | Modifier/Supprimer affectation | ProjectDetail.vue (Team tab) | PUT/DELETE /assignments/ |
| F3.6 | Modifier/Supprimer phase | ProjectDetail.vue (Phases tab) | PUT/DELETE /phases/ |
| F3.7 | Modifier/Supprimer WBS | ProjectDetail.vue (WBS tab) | PUT/DELETE /wbs/ |
| F3.8 | Checklist fermeture projet | ProjectCloseModal.vue (new) | — |
| F3.9 | Supprimer client (bouton dans ClientDetail) | ClientDetail.vue | DELETE /clients/{id}/ |

**Version cible**: 1.1.004

---

## Sprint F4 — Timesheets enrichis + Délégation (Priorité moyenne)
> Compléter les interactions timesheet et activer la délégation.

| # | Tâche | Fichier | API backend |
|---|-------|---------|-------------|
| F4.1 | "+ Ajouter une tâche" fonctionnel dans grille | TimesheetGrid.vue | — |
| F4.2 | Favoris projet (étoile cliquable) | TimesheetGrid.vue | localStorage |
| F4.3 | Indicateur blocage phase/personne | TimesheetGrid.vue | GET /timesheet_locks/ |
| F4.4 | Backend délégation (endpoints CRUD) | Backend: delegation app | Nouveau |
| F4.5 | Délégation UI complète (créer, lister, expirer) | DelegationList.vue | POST/GET /delegations/ |
| F4.6 | Bannière jaune "Par délégation de..." | MainLayout.vue | — |
| F4.7 | Gestion locks timesheet (UI admin) | TimesheetLocks.vue (new) | /timesheet_locks/ |

**Version cible**: 1.1.005

---

## Sprint F5 — Dashboard par rôle + Notifications (Priorité moyenne)
> Tableaux de bord contextuels et centre de notifications.

| # | Tâche | Fichier | API backend |
|---|-------|---------|-------------|
| F5.1 | Dashboard adaptatif par rôle (Employee/PM/Finance/Dir) | DashboardView.vue | GET /dashboard/ (déjà role-adaptatif) |
| F5.2 | Widget PM: santé projets, CA/Salaire, heures sans fact. | DashboardView.vue | GET /dashboard/pm-kpis/ |
| F5.3 | Widget Finance: aging, factures en attente | DashboardView.vue | Agrégation existante |
| F5.4 | Widget "Actions requises" groupées par urgence | DashboardView.vue | Agrégation |
| F5.5 | Centre de notifications fonctionnel | NotificationCenter.vue | Backend notifications existant |
| F5.6 | Badge cloche dynamique (count réel) | MainLayout.vue | GET /notifications/?unread=true |
| F5.7 | Préférences de notification | NotificationPrefs.vue (new) | /notification_preferences/ |

**Version cible**: 1.1.006

---

## Sprint F6 — Admin avancé + Polish (Priorité basse)
> Finalisation administration et qualité.

| # | Tâche | Fichier | API backend |
|---|-------|---------|-------------|
| F6.1 | Organisation: CRUD entités juridiques | OrgSettings.vue | Nouveau endpoint |
| F6.2 | Organisation: CRUD unités d'affaires | OrgSettings.vue | Nouveau endpoint |
| F6.3 | Facturation admin: CRUD templates facture | BillingSettings.vue | /invoice_templates/ |
| F6.4 | Facturation admin: CRUD niveaux de relance | BillingSettings.vue | Nouveau endpoint |
| F6.5 | Utilisateurs: modifier rôle, désactiver | UserList.vue | Nouveau endpoint |
| F6.6 | Audit: journal des opérations consultable | AuditLog.vue | Nouveau endpoint |
| F6.7 | Export Intact (CSV dépenses + factures) | Boutons export | Nouveau endpoint |
| F6.8 | Tests E2E pages critiques | — | — |

**Version cible**: 1.1.007

---

## Résumé

| Sprint | Focus | Tâches | Priorité |
|--------|-------|--------|----------|
| **F1** | Facturation complète | 9 | Critique |
| **F2** | Dépenses + Fournisseurs | 8 | Haute |
| **F3** | Projets enrichis | 9 | Haute |
| **F4** | Timesheets + Délégation | 7 | Moyenne |
| **F5** | Dashboard + Notifications | 7 | Moyenne |
| **F6** | Admin avancé + Polish | 8 | Basse |
| **TOTAL** | | **48 tâches** | |

---

## Convention de versioning

Format: `MAJOR.MINOR.PATCH`
- **MAJOR** (1): Version produit
- **MINOR** (1): MVP-1
- **PATCH** (001→010): Incrémenté par sprint/commit significatif

Incrément après chaque sprint complété:
- Sprint F1 → v1.1.002
- Sprint F2 → v1.1.003
- Sprint F3 → v1.1.004
- Sprint F4 → v1.1.005
- Sprint F5 → v1.1.006
- Sprint F6 → v1.1.007
