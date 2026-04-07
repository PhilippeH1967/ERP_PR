<script setup lang="ts">
import { ref } from 'vue'

const activeSection = ref('overview')

const sections = [
  { key: 'overview', label: 'Vue d\'ensemble', icon: '📋' },
  { key: 'architecture', label: 'Architecture', icon: '🏗️' },
  { key: 'modules', label: 'Modules', icon: '📦' },
  { key: 'api', label: 'API Reference', icon: '🔌' },
  { key: 'install', label: 'Installation', icon: '⚙️' },
  { key: 'tests', label: 'Tests', icon: '🧪' },
  { key: 'deploy', label: 'Déploiement', icon: '🚀' },
]

const version = 'v1.2.000'
const lastUpdate = '2026-04-07'

interface ApiEndpoint { method: string; path: string; desc: string }
interface ApiGroup { name: string; endpoints: ApiEndpoint[] }

const apiGroups: ApiGroup[] = [
  { name: 'Authentification', endpoints: [
    { method: 'POST', path: '/auth/token/', desc: 'Obtenir JWT (access + refresh)' },
    { method: 'POST', path: '/auth/token/refresh/', desc: 'Rafraîchir le token' },
    { method: 'GET', path: '/auth/me/', desc: 'Profil utilisateur courant' },
    { method: 'GET', path: '/auth/config/', desc: 'Configuration SSO' },
  ]},
  { name: 'Projets', endpoints: [
    { method: 'GET', path: '/projects/', desc: 'Liste des projets (filtrable par status, client, BU)' },
    { method: 'POST', path: '/projects/', desc: 'Créer un projet' },
    { method: 'POST', path: '/projects/create_from_template/', desc: 'Créer depuis template (wizard)' },
    { method: 'GET', path: '/projects/{id}/dashboard/', desc: 'KPIs du projet' },
    { method: 'GET', path: '/projects/{id}/phases/', desc: 'Phases du projet' },
    { method: 'GET', path: '/projects/{id}/tasks/', desc: 'Tâches WBS du projet' },
    { method: 'GET', path: '/projects/{id}/assignments/', desc: 'Affectations équipe' },
    { method: 'GET', path: '/projects/{id}/amendments/', desc: 'Avenants' },
  ]},
  { name: 'Feuilles de temps', endpoints: [
    { method: 'GET', path: '/time_entries/', desc: 'Entrées (filtrable date__gte, date__lte, project, employee)' },
    { method: 'POST', path: '/time_entries/', desc: 'Créer une entrée' },
    { method: 'POST', path: '/time_entries/submit_week/', desc: 'Soumettre la semaine' },
    { method: 'GET', path: '/time_entries/weekly_stats/', desc: 'Stats: contrat, moyenne 4 sem, taux facturable' },
    { method: 'POST', path: '/time_entries/approve_entries/', desc: 'PM approuve des entrées' },
    { method: 'POST', path: '/time_entries/reject_entries/', desc: 'PM rejette avec motif' },
    { method: 'POST', path: '/time_entries/bulk_correct/', desc: 'Finance corrige rétroactivement' },
    { method: 'POST', path: '/time_entries/transfer_hours/', desc: 'Transférer heures entre projets' },
    { method: 'GET', path: '/weekly_approvals/pm_dashboard/', desc: 'Dashboard PM approbations' },
    { method: 'GET', path: '/weekly_approvals/finance_dashboard/', desc: 'Dashboard Finance' },
    { method: 'GET', path: '/weekly_approvals/paie_dashboard/', desc: 'Dashboard Paie (11 contrôles)' },
  ]},
  { name: 'Facturation', endpoints: [
    { method: 'GET', path: '/invoices/', desc: 'Liste factures' },
    { method: 'POST', path: '/invoices/create_from_project/', desc: 'Créer facture depuis projet' },
    { method: 'POST', path: '/invoices/{id}/submit/', desc: 'Soumettre (numéro définitif)' },
    { method: 'POST', path: '/invoices/{id}/approve/', desc: 'Approuver (anti-self)' },
    { method: 'POST', path: '/invoices/{id}/mark_hours_invoiced/', desc: 'Marquer heures facturées' },
    { method: 'GET', path: '/invoices/{id}/aging_analysis/', desc: 'Analyse aging 30/60/90j' },
  ]},
  { name: 'Congés', endpoints: [
    { method: 'POST', path: '/leave_types/seed/', desc: 'Seeder 7 types Québec' },
    { method: 'GET', path: '/leave_banks/my_balances/', desc: 'Mes soldes congés' },
    { method: 'POST', path: '/leave_requests/', desc: 'Créer demande' },
    { method: 'POST', path: '/leave_requests/{id}/approve/', desc: 'Approuver (auto-create TimeEntry)' },
    { method: 'POST', path: '/leave_requests/{id}/reject/', desc: 'Refuser avec motif' },
  ]},
  { name: 'Fournisseurs / ST', endpoints: [
    { method: 'POST', path: '/st_invoices/batch_authorize/', desc: 'Autoriser en lot' },
    { method: 'POST', path: '/st_invoices/{id}/dispute/', desc: 'Contester une facture' },
    { method: 'POST', path: '/st_holdbacks/{id}/release/', desc: 'Libérer retenue' },
    { method: 'GET', path: '/st_invoices/summary_by_supplier/', desc: 'Cumul par fournisseur' },
  ]},
  { name: 'Consortium', endpoints: [
    { method: 'GET', path: '/consortiums/', desc: 'Liste consortiums' },
    { method: 'POST', path: '/consortiums/', desc: 'Créer consortium' },
    { method: 'POST', path: '/consortiums/{id}/members/', desc: 'Ajouter membre' },
    { method: 'GET', path: '/consortiums/{id}/validate_coefficients/', desc: 'Vérifier total = 100%' },
  ]},
  { name: 'Planification & Gantt', endpoints: [
    { method: 'GET', path: '/allocations/global_planning/', desc: 'Vue globale ressources' },
    { method: 'GET', path: '/allocations/load_alerts/', desc: 'Alertes surcharge/sous-charge' },
    { method: 'GET', path: '/gantt/project_gantt/?project_id={id}', desc: 'Données Gantt (phases, jalons, deps)' },
    { method: 'POST', path: '/availability/generate/', desc: 'Générer disponibilité (contrat - congés)' },
  ]},
  { name: 'Dashboard & Exports', endpoints: [
    { method: 'GET', path: '/dashboard/', desc: 'KPIs par rôle' },
    { method: 'GET', path: '/dashboard/pm-kpis/', desc: 'KPIs PM (CA/salaires, taux, carnet)' },
    { method: 'GET', path: '/dashboard/hours-report/', desc: 'Rapport heures (group_by=project|employee|bu)' },
    { method: 'GET', path: '/exports/invoices/', desc: 'Export CSV factures' },
    { method: 'GET', path: '/exports/time_entries/', desc: 'Export CSV temps (?month=&year=)' },
  ]},
]

const methodColors: Record<string, string> = {
  GET: 'method-get', POST: 'method-post', PATCH: 'method-patch', DELETE: 'method-delete',
}
</script>

<template>
  <div class="doc-layout">
    <!-- Sidebar -->
    <aside class="doc-sidebar">
      <div class="sidebar-logo">
        <span class="logo-pr">PR</span><span class="logo-sep">|</span><span class="logo-erp">ERP</span>
      </div>
      <p class="sidebar-version">{{ version }} — Documentation</p>
      <nav class="sidebar-nav">
        <button
          v-for="s in sections"
          :key="s.key"
          class="nav-item"
          :class="{ active: activeSection === s.key }"
          @click="activeSection = s.key"
        >
          <span class="nav-icon">{{ s.icon }}</span>
          <span>{{ s.label }}</span>
        </button>
      </nav>
    </aside>

    <!-- Content -->
    <main class="doc-content">
      <!-- Overview -->
      <template v-if="activeSection === 'overview'">
        <h1>Vue d'ensemble</h1>
        <p class="intro">ERP pour <strong>Provencher Roy</strong>, cabinet d'architecture de 400 employés. Gestion complète des projets, feuilles de temps, facturation, dépenses, et planification des ressources.</p>

        <div class="stats-grid">
          <div class="stat-card"><div class="stat-value">15</div><div class="stat-label">Apps Django</div></div>
          <div class="stat-card"><div class="stat-value">80+</div><div class="stat-label">Modèles</div></div>
          <div class="stat-card"><div class="stat-value">60+</div><div class="stat-label">Vues frontend</div></div>
          <div class="stat-card"><div class="stat-value">80+</div><div class="stat-label">Endpoints API</div></div>
          <div class="stat-card"><div class="stat-value">~100</div><div class="stat-label">Tests backend</div></div>
          <div class="stat-card"><div class="stat-value">357</div><div class="stat-label">Tests visuels</div></div>
        </div>

        <h2>Stack technique</h2>
        <table class="doc-table">
          <tbody>
            <tr><td class="font-semibold">Backend</td><td>Django 6.0 + Django REST Framework</td></tr>
            <tr><td class="font-semibold">Frontend</td><td>Vue 3 + TypeScript + Pinia + TailwindCSS</td></tr>
            <tr><td class="font-semibold">Base de données</td><td>PostgreSQL 16</td></tr>
            <tr><td class="font-semibold">Cache / Queue</td><td>Redis 7 + Celery + Celery Beat</td></tr>
            <tr><td class="font-semibold">Conteneurs</td><td>Docker + Docker Compose</td></tr>
            <tr><td class="font-semibold">API docs</td><td>drf-spectacular (OpenAPI 3)</td></tr>
          </tbody>
        </table>

        <h2>Rôles RBAC</h2>
        <table class="doc-table">
          <thead><tr><th>Rôle</th><th>Accès</th></tr></thead>
          <tbody>
            <tr><td class="font-semibold">ADMIN</td><td>Accès total, configuration système</td></tr>
            <tr><td class="font-semibold">FINANCE</td><td>Facturation, paiements, dépenses, exports</td></tr>
            <tr><td class="font-semibold">PM</td><td>Projets gérés, approbations, planification</td></tr>
            <tr><td class="font-semibold">PROJECT_DIRECTOR</td><td>Vision globale projets</td></tr>
            <tr><td class="font-semibold">PAIE</td><td>Validation paie, contrôles, verrouillage</td></tr>
            <tr><td class="font-semibold">EMPLOYEE</td><td>Saisie temps, congés, dépenses</td></tr>
          </tbody>
        </table>
      </template>

      <!-- Architecture -->
      <template v-if="activeSection === 'architecture'">
        <h1>Architecture</h1>

        <h2>Structure du projet</h2>
        <pre class="code-block">ERP/
├── backend/
│   ├── apps/
│   │   ├── core/           # Tenant, RLS, roles, auth, taxes
│   │   ├── projects/       # Projets, phases, tâches, WBS
│   │   ├── clients/        # Clients, contacts, adresses
│   │   ├── time_entries/   # Feuilles de temps, approbations
│   │   ├── billing/        # Facturation, paiements, taxes
│   │   ├── expenses/       # Dépenses, catégories
│   │   ├── suppliers/      # Fournisseurs, factures ST
│   │   ├── consortiums/    # Consortiums, vue duale
│   │   ├── leaves/         # Congés, banque, types
│   │   ├── planning/       # Allocations, Gantt, jalons
│   │   ├── dashboards/     # KPIs, rapports
│   │   ├── data_ops/       # Import/export, Intacct
│   │   └── notifications/  # Notifications in-app
│   └── config/             # Settings, URLs, Celery
├── frontend/
│   └── src/features/       # 12 modules frontend
├── docs/                   # Documentation
└── docker-compose.yml</pre>

        <h2>Multi-tenancy</h2>
        <p>Tous les modèles métier héritent de <code>TenantScopedModel</code>. Le tenant est résolu via le header <code>X-Tenant-Id</code> ou l'association <code>UserTenantAssociation</code>.</p>

        <h2>Schéma de données</h2>
        <pre class="code-block">Tenant ─── Project ─── Phase ─── Task ─── TimeEntry
              │           │                    │
              │           └── PhaseDependency   └── WeeklyApproval
              │
              ├── Invoice ─── InvoiceLine ─── TaxScheme → TaxRate
              ├── Consortium ─── ConsortiumMember
              ├── EmployeeAssignment
              ├── ResourceAllocation
              └── Milestone</pre>
      </template>

      <!-- Modules -->
      <template v-if="activeSection === 'modules'">
        <h1>Modules</h1>

        <div v-for="(bloc, bi) in [
          { title: 'Bloc 1 — Projets', items: [
            'Projets CRUD + WBS Option B (Phase → Tâche → Sous-tâche)',
            'Wizard 5 étapes avec templates (7 phases, 23 tâches)',
            'Gantt interactif (barres phases, 3 zooms, jalons, dépendances)',
            '12 onglets fiche projet',
            'Clients 5 onglets avec recherche live',
            'Consortium FR59 — entity, membres, coefficients, vue duale FR61/FR62',
          ]},
          { title: 'Bloc 2 — Production', items: [
            'Feuilles de temps par tâche WBS, workflow 6 états',
            'Approbation 3 niveaux (PM/Finance/Paie) + 11 contrôles paie',
            'Period locking (gel global, exceptions, phase/personne)',
            'Congés: 7 types Québec, banque soldes, auto-create TimeEntry',
            'Fournisseurs/ST: 6 entités, batch, disputes, holdbacks',
            'Planification: allocations, surcharge/sous-charge, disponibilité',
          ]},
          { title: 'Bloc 3 — Financier', items: [
            'Facturation: 6 schémas fiscaux (QC, ON, AB, BC, FR, Exonéré)',
            'Workflow 5 étapes (Draft → Submit → Approve → Send → Paid)',
            'Dépenses: 15 catégories, upload reçu, refacturation client',
            'Exports Intacct Phase 1: 4 CSV (factures, paiements, dépenses, temps)',
          ]},
          { title: 'Bloc 4 — Pilotage', items: [
            'Dashboard 5 rôles avec KPIs adaptés',
            'Rapports heures groupables (projet/employé/BU) + export CSV',
            'Import 13 types (6 ref data + 7 transactional)',
            'Route guards RBAC (EMPLOYEE bloqué sur billing/admin)',
          ]},
        ]" :key="bi" class="module-bloc">
          <h2>{{ bloc.title }}</h2>
          <ul><li v-for="(item, ii) in bloc.items" :key="ii">{{ item }}</li></ul>
        </div>
      </template>

      <!-- API Reference -->
      <template v-if="activeSection === 'api'">
        <h1>API Reference</h1>
        <p class="intro">Base URL: <code>http://localhost:8000/api/v1/</code></p>

        <div v-for="group in apiGroups" :key="group.name" class="api-group">
          <h2>{{ group.name }}</h2>
          <table class="doc-table api-table">
            <thead><tr><th style="width:70px;">Méthode</th><th>Endpoint</th><th>Description</th></tr></thead>
            <tbody>
              <tr v-for="(ep, i) in group.endpoints" :key="i">
                <td><span class="method-badge" :class="methodColors[ep.method]">{{ ep.method }}</span></td>
                <td class="font-mono text-sm">{{ ep.path }}</td>
                <td>{{ ep.desc }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </template>

      <!-- Installation -->
      <template v-if="activeSection === 'install'">
        <h1>Installation</h1>

        <h2>Prérequis</h2>
        <ul><li>Docker Desktop</li><li>Git</li></ul>

        <h2>Démarrage rapide</h2>
        <pre class="code-block">git clone https://github.com/PhilippeH1967/ERP_PR.git
cd ERP_PR
cp .env.example .env
docker compose up -d
docker compose exec django python manage.py migrate
docker compose exec django python manage.py seed_reference_data
docker compose exec django python manage.py seed_templates
docker compose exec django python manage.py seed_expense_categories
open http://localhost:5174</pre>

        <h2>Comptes de test</h2>
        <table class="doc-table">
          <thead><tr><th>Email</th><th>Mot de passe</th><th>Rôle</th></tr></thead>
          <tbody>
            <tr><td>admin@provencher-roy.com</td><td>Test1234!</td><td>ADMIN</td></tr>
            <tr><td>pm@test.com</td><td>Test1234!</td><td>PM</td></tr>
            <tr><td>finance@test.com</td><td>Test1234!</td><td>FINANCE</td></tr>
            <tr><td>paie@test.com</td><td>Test1234!</td><td>PAIE</td></tr>
            <tr><td>employe@test.com</td><td>Test1234!</td><td>EMPLOYEE</td></tr>
          </tbody>
        </table>

        <h2>Services Docker</h2>
        <table class="doc-table">
          <thead><tr><th>Service</th><th>Port</th><th>URL</th></tr></thead>
          <tbody>
            <tr><td>django</td><td>8000</td><td>http://localhost:8000/api/v1/</td></tr>
            <tr><td>vue</td><td>5174</td><td>http://localhost:5174</td></tr>
            <tr><td>postgres</td><td>5436</td><td>postgres://localhost:5436/erp</td></tr>
            <tr><td>redis</td><td>6379</td><td>redis://localhost:6379</td></tr>
          </tbody>
        </table>
      </template>

      <!-- Tests -->
      <template v-if="activeSection === 'tests'">
        <h1>Tests</h1>

        <h2>Tests backend automatisés (~100)</h2>
        <pre class="code-block">docker compose exec django python -m pytest          # Tous
docker compose exec django python -m pytest apps/projects/  # Par module
docker compose exec django python -m pytest -v --tb=short   # Verbose</pre>

        <table class="doc-table">
          <thead><tr><th>Module</th><th>Tests</th></tr></thead>
          <tbody>
            <tr v-for="(m, i) in [
              { name: 'projects', count: 17 }, { name: 'time_entries', count: 17 },
              { name: 'billing', count: 18 }, { name: 'leaves', count: 8 },
              { name: 'planning', count: 5 }, { name: 'suppliers', count: 11 },
              { name: 'consortiums', count: 6 }, { name: 'expenses', count: 6 },
              { name: 'core', count: 9 },
            ]" :key="i">
              <td class="font-mono">{{ m.name }}</td><td>{{ m.count }}</td>
            </tr>
          </tbody>
        </table>

        <h2>Tests visuels (357 — 13 onglets Excel)</h2>
        <p>Fichier: <code>tests_visuels/plan_tests_complet_v3.xlsx</code></p>
        <table class="doc-table">
          <thead><tr><th>Onglet</th><th>Tests</th></tr></thead>
          <tbody>
            <tr v-for="(t, i) in [
              { tab: '01 — Auth & Navigation', count: 22 }, { tab: '02 — Clients', count: 10 },
              { tab: '03 — Projets', count: 76 }, { tab: '04 — Feuilles de temps', count: 96 },
              { tab: '05 — Congés', count: 10 }, { tab: '06 — Fournisseurs ST', count: 18 },
              { tab: '07 — Planification', count: 9 }, { tab: '08 — Facturation', count: 30 },
              { tab: '09 — Dépenses', count: 14 }, { tab: '10 — Exports Intacct', count: 6 },
              { tab: '11 — Consortium', count: 14 }, { tab: '12 — Dashboard & Admin', count: 41 },
              { tab: '13 — Gantt', count: 11 },
            ]" :key="i">
              <td>{{ t.tab }}</td><td>{{ t.count }}</td>
            </tr>
          </tbody>
        </table>
      </template>

      <!-- Deployment -->
      <template v-if="activeSection === 'deploy'">
        <h1>Déploiement</h1>

        <h2>Celery Beat Schedule</h2>
        <table class="doc-table">
          <thead><tr><th>Tâche</th><th>Fréquence</th><th>Fonction</th></tr></thead>
          <tbody>
            <tr><td>Relance timesheets</td><td>Mercredi 17h</td><td>send_timesheet_reminders</td></tr>
            <tr><td>Relance urgente</td><td>Vendredi 12h</td><td>send_timesheet_reminders</td></tr>
            <tr><td>Escalade PM</td><td>Vendredi 17h</td><td>escalate_missing_timesheets</td></tr>
            <tr><td>Expiration délégations</td><td>Quotidien 1h</td><td>expire_delegations</td></tr>
          </tbody>
        </table>

        <h2>Mise à jour</h2>
        <pre class="code-block">git pull origin main
docker compose up -d --build
docker compose exec django python manage.py migrate
docker compose exec django python manage.py collectstatic --noinput</pre>

        <h2>Sauvegarde</h2>
        <pre class="code-block"># Backup
docker compose exec postgres pg_dump -U erp erp > backup_$(date +%Y%m%d).sql

# Restore
cat backup.sql | docker compose exec -T postgres psql -U erp erp</pre>
      </template>

      <div class="doc-footer">
        <p>PR|ERP {{ version }} — Dernière mise à jour: {{ lastUpdate }}</p>
      </div>
    </main>
  </div>
</template>

<style scoped>
.doc-layout { display: flex; min-height: calc(100vh - 56px); margin: -24px; }
.doc-sidebar { width: 240px; min-width: 240px; background: var(--color-gray-900); color: white; padding: 20px 0; }
.sidebar-logo { padding: 0 20px; font-size: 18px; font-weight: 800; }
.logo-pr { color: #60A5FA; } .logo-sep { color: var(--color-gray-600); margin: 0 4px; } .logo-erp { color: var(--color-gray-400); font-weight: 400; }
.sidebar-version { padding: 4px 20px 16px; font-size: 10px; color: var(--color-gray-500); }
.sidebar-nav { display: flex; flex-direction: column; }
.nav-item { display: flex; align-items: center; gap: 10px; padding: 10px 20px; font-size: 13px; color: var(--color-gray-400); background: none; border: none; text-align: left; cursor: pointer; transition: all 0.15s; }
.nav-item:hover { color: white; background: rgba(255,255,255,0.05); }
.nav-item.active { color: white; background: rgba(59,130,246,0.2); border-right: 3px solid #3B82F6; font-weight: 600; }
.nav-icon { font-size: 16px; width: 20px; text-align: center; }

.doc-content { flex: 1; padding: 32px 40px; max-width: 900px; overflow-y: auto; }
.doc-content h1 { font-size: 24px; font-weight: 700; color: var(--color-gray-900); margin-bottom: 16px; padding-bottom: 12px; border-bottom: 2px solid var(--color-gray-200); }
.doc-content h2 { font-size: 16px; font-weight: 600; color: var(--color-gray-800); margin: 24px 0 12px; }
.intro { font-size: 14px; color: var(--color-gray-600); line-height: 1.6; margin-bottom: 20px; }
.doc-content p { font-size: 13px; color: var(--color-gray-700); line-height: 1.6; margin-bottom: 12px; }
.doc-content ul { padding-left: 20px; margin-bottom: 16px; }
.doc-content li { font-size: 13px; color: var(--color-gray-700); margin-bottom: 6px; }
.doc-content code { background: var(--color-gray-100); padding: 1px 6px; border-radius: 3px; font-size: 12px; font-family: var(--font-mono); }

.stats-grid { display: grid; grid-template-columns: repeat(6, 1fr); gap: 12px; margin-bottom: 24px; }
.stat-card { background: white; border: 1px solid var(--color-gray-200); border-radius: 8px; padding: 16px; text-align: center; }
.stat-value { font-size: 28px; font-weight: 700; color: var(--color-primary); }
.stat-label { font-size: 10px; color: var(--color-gray-500); text-transform: uppercase; font-weight: 600; margin-top: 4px; }

.doc-table { width: 100%; border-collapse: collapse; font-size: 13px; margin-bottom: 20px; }
.doc-table th { padding: 8px 12px; font-size: 11px; font-weight: 600; text-transform: uppercase; color: var(--color-gray-500); background: var(--color-gray-50); border-bottom: 2px solid var(--color-gray-200); text-align: left; }
.doc-table td { padding: 8px 12px; border-bottom: 1px solid var(--color-gray-100); }
.font-semibold { font-weight: 600; }
.font-mono { font-family: var(--font-mono); }

.code-block { background: var(--color-gray-900); color: #E5E7EB; padding: 16px 20px; border-radius: 8px; font-size: 12px; font-family: var(--font-mono); line-height: 1.6; overflow-x: auto; margin-bottom: 20px; white-space: pre; }

.module-bloc { margin-bottom: 20px; }
.module-bloc h2 { font-size: 15px; }

.api-group { margin-bottom: 24px; }
.api-table td { vertical-align: middle; }
.method-badge { display: inline-block; padding: 2px 8px; border-radius: 3px; font-size: 10px; font-weight: 700; font-family: var(--font-mono); }
.method-get { background: #DCFCE7; color: #15803D; }
.method-post { background: #DBEAFE; color: #1D4ED8; }
.method-patch { background: #FEF3C7; color: #92400E; }
.method-delete { background: #FEE2E2; color: #DC2626; }

.doc-footer { margin-top: 40px; padding-top: 16px; border-top: 1px solid var(--color-gray-200); font-size: 11px; color: var(--color-gray-400); }
</style>
