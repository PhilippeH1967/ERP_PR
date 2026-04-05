<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import apiClient from '@/plugins/axios'
import { useLocale } from '@/shared/composables/useLocale'
import { useAuth } from '@/shared/composables/useAuth'

const { fmt } = useLocale()
const { currentUser } = useAuth()

interface KPIs {
  projects_active: number
  timesheets_pending: number
  invoices_outstanding: string
  expenses_pending: number
}

interface PMKPIs {
  projects_managed: number
  total_invoiced: string
  total_hours: string
  hours_this_month?: string
  billing_rate?: number
  ca_salary_ratio?: number
  actions_required?: number
}

interface BUKPIs {
  projects_in_bu: number
  total_hours_bu: string
  utilization_percent: number
  budget_consumed_percent: number
}

interface SystemHealth {
  active_users: number
  pending_approvals: number
  overdue_invoices: number
}

const kpis = ref<KPIs | null>(null)
const pmKpis = ref<PMKPIs | null>(null)
const pmProjects = ref<Array<Record<string, unknown>>>([])

const buKpis = ref<BUKPIs | null>(null)
const healthKpis = ref<SystemHealth | null>(null)

const roles = computed(() => currentUser.value?.roles || [])
const isPM = computed(() => roles.value.includes('PM') || roles.value.includes('PROJECT_DIRECTOR'))
const isBUDirector = computed(() => roles.value.includes('BU_DIRECTOR'))
const isFinance = computed(() => roles.value.includes('FINANCE'))
const isAdmin = computed(() => roles.value.includes('ADMIN'))

onMounted(async () => {
  // Base KPIs for all roles
  try {
    const resp = await apiClient.get('dashboard/')
    kpis.value = resp.data?.kpis || resp.data?.data?.kpis
  } catch { /* empty */ }

  // PM KPIs + projects list
  if (isPM.value || isAdmin.value) {
    try {
      const resp = await apiClient.get('dashboard/pm-kpis/')
      pmKpis.value = resp.data?.data || resp.data
    } catch { /* empty */ }
    try {
      const resp = await apiClient.get('projects/', { params: { status: 'ACTIVE' } })
      const data = resp.data?.data || resp.data
      pmProjects.value = (Array.isArray(data) ? data : data?.results || []).slice(0, 10)
    } catch { pmProjects.value = [] }
  }

  // BU Director KPIs
  if (isBUDirector.value || isAdmin.value) {
    try {
      const resp = await apiClient.get('dashboard/bu-kpis/')
      buKpis.value = resp.data?.data || resp.data
    } catch { /* empty */ }
  }

  // Admin health
  if (isAdmin.value || isFinance.value) {
    try {
      const resp = await apiClient.get('dashboard/system-health/')
      healthKpis.value = resp.data?.data || resp.data
    } catch { /* empty */ }
  }
})
</script>

<template>
  <div>
    <div class="page-header">
      <div>
        <h1>Bienvenue, {{ currentUser?.first_name || currentUser?.username || 'Utilisateur' }}</h1>
        <p class="welcome-sub">Tableau de bord — {{ new Date().toLocaleDateString('fr-CA', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }) }}</p>
      </div>
      <span class="role-info">
        {{ roles.join(', ') || 'Employé' }}
      </span>
    </div>

    <!-- Base KPIs (all roles) -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <p class="kpi-label">Projets actifs</p>
        <p class="kpi-value">{{ kpis?.projects_active ?? '—' }}</p>
      </div>
      <div class="kpi-card">
        <p class="kpi-label">Feuilles en attente</p>
        <p class="kpi-value warning">{{ kpis?.timesheets_pending ?? '—' }}</p>
      </div>
      <div class="kpi-card">
        <p class="kpi-label">Factures impayées</p>
        <p class="kpi-value danger mono">{{ kpis?.invoices_outstanding ? fmt.currency(kpis.invoices_outstanding) : '—' }}</p>
      </div>
      <div class="kpi-card">
        <p class="kpi-label">Dépenses en attente</p>
        <p class="kpi-value">{{ kpis?.expenses_pending ?? '—' }}</p>
      </div>
    </div>

    <!-- PM Section (E-04) -->
    <div v-if="(isPM || isAdmin)" class="section">
      <div class="section-header">
        <h2 class="section-title">Chef de projet</h2>
        <router-link to="/projects/new" class="btn-primary-sm">+ Nouveau projet</router-link>
      </div>
      <div class="kpi-grid">
        <div class="kpi-card">
          <p class="kpi-label">Heures ce mois</p>
          <p class="kpi-value mono">{{ pmKpis?.hours_this_month ? fmt.hours(pmKpis.hours_this_month) : '0h' }}</p>
        </div>
        <div class="kpi-card">
          <p class="kpi-label">Ratio CA / Salaires</p>
          <p class="kpi-value" :class="{ primary: (pmKpis?.ca_salary_ratio || 0) >= 2.5, warning: (pmKpis?.ca_salary_ratio || 0) < 2.5 }">
            {{ pmKpis?.ca_salary_ratio?.toFixed(1) || '—' }}x
          </p>
          <p class="kpi-target">Cible: 2.5x</p>
        </div>
        <div class="kpi-card">
          <p class="kpi-label">Taux facturation</p>
          <p class="kpi-value" :class="{ primary: (pmKpis?.billing_rate || 0) >= 75, warning: (pmKpis?.billing_rate || 0) < 75 }">
            {{ pmKpis?.billing_rate?.toFixed(0) || '—' }}%
          </p>
        </div>
        <div class="kpi-card">
          <p class="kpi-label">Actions requises</p>
          <p class="kpi-value" :class="{ danger: (pmKpis?.actions_required || 0) > 0 }">
            {{ pmKpis?.actions_required ?? kpis?.timesheets_pending ?? 0 }}
          </p>
        </div>
      </div>

      <!-- Project list (E-05) -->
      <div v-if="pmProjects.length" class="pm-projects">
        <table class="pm-table">
          <thead>
            <tr>
              <th>Code</th>
              <th>Projet</th>
              <th>Client</th>
              <th>Phase active</th>
              <th class="text-right">Budget h</th>
              <th>Santé</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in pmProjects" :key="Number(p.id)" class="cursor-pointer" @click="$router.push(`/projects/${p.id}`)">
              <td class="font-mono font-semibold">{{ p.code }}</td>
              <td>{{ p.name }}</td>
              <td class="text-muted">{{ p.client_name || '—' }}</td>
              <td class="text-muted">{{ p.active_phase || '—' }}</td>
              <td class="text-right font-mono">{{ Number(p.budget_hours || 0).toFixed(0) }}</td>
              <td>
                <span class="health-dot" :class="p.status === 'ACTIVE' ? 'green' : 'gray'"></span>
              </td>
            </tr>
          </tbody>
        </table>
        <router-link to="/projects" class="see-all">Voir tous les projets →</router-link>
      </div>
    </div>

    <!-- BU Director Section -->
    <div v-if="buKpis && (isBUDirector || isAdmin)" class="section">
      <h2 class="section-title">Directeur d'unité</h2>
      <div class="kpi-grid">
        <div class="kpi-card">
          <p class="kpi-label">Projets unité</p>
          <p class="kpi-value primary">{{ buKpis.projects_in_bu }}</p>
        </div>
        <div class="kpi-card">
          <p class="kpi-label">Heures totales</p>
          <p class="kpi-value mono">{{ fmt.hours(buKpis.total_hours_bu) }}</p>
        </div>
        <div class="kpi-card">
          <p class="kpi-label">Utilisation %</p>
          <p class="kpi-value">{{ buKpis.utilization_percent }}%</p>
        </div>
        <div class="kpi-card">
          <p class="kpi-label">Budget consommé %</p>
          <p class="kpi-value">{{ buKpis.budget_consumed_percent }}%</p>
        </div>
      </div>
    </div>

    <!-- Finance / Admin Section -->
    <div v-if="healthKpis && (isFinance || isAdmin)" class="section">
      <h2 class="section-title">{{ isAdmin ? 'Administration' : 'Finance' }}</h2>
      <div class="kpi-grid-3">
        <div class="kpi-card">
          <p class="kpi-label">Utilisateurs actifs</p>
          <p class="kpi-value">{{ healthKpis.active_users || '—' }}</p>
        </div>
        <div class="kpi-card">
          <p class="kpi-label">Approbations en attente</p>
          <p class="kpi-value warning">{{ healthKpis.pending_approvals }}</p>
        </div>
        <div class="kpi-card">
          <p class="kpi-label">Factures en souffrance</p>
          <p class="kpi-value danger">{{ healthKpis.overdue_invoices }}</p>
        </div>
      </div>
    </div>

    <!-- Quick actions -->
    <div class="section">
      <h2 class="section-title">Actions rapides</h2>
      <div class="actions-grid">
        <router-link to="/timesheets" class="action-card">
          <span class="action-icon">🕐</span>
          <span class="action-label">Saisir mes heures</span>
        </router-link>
        <router-link to="/expenses" class="action-card">
          <span class="action-icon">🧾</span>
          <span class="action-label">Nouvelle dépense</span>
        </router-link>
        <router-link to="/projects" class="action-card">
          <span class="action-icon">📁</span>
          <span class="action-label">Mes projets</span>
        </router-link>
        <router-link v-if="isPM || isAdmin" to="/approvals" class="action-card">
          <span class="action-icon">✅</span>
          <span class="action-label">Approbations</span>
        </router-link>
        <router-link v-if="isFinance || isAdmin" to="/billing" class="action-card">
          <span class="action-icon">📄</span>
          <span class="action-label">Facturation</span>
        </router-link>
        <router-link v-if="isAdmin" to="/admin" class="action-card">
          <span class="action-icon">⚙️</span>
          <span class="action-label">Administration</span>
        </router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }
.page-header h1 { font-size: 20px; font-weight: 700; color: var(--color-gray-900); }
.welcome-sub { font-size: 12px; color: var(--color-gray-500); margin-top: 2px; }
.role-info { font-size: 11px; color: var(--color-gray-500); background: var(--color-gray-100); padding: 3px 10px; border-radius: 10px; }

.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 20px; }
.kpi-grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
.kpi-card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 16px; }
.kpi-label { font-size: 11px; color: var(--color-gray-500); text-transform: uppercase; font-weight: 600; letter-spacing: 0.3px; margin-bottom: 4px; }
.kpi-value { font-size: 24px; font-weight: 700; color: var(--color-gray-900); }
.kpi-value.mono { font-family: var(--font-mono); font-size: 20px; }
.kpi-value.warning { color: var(--color-warning); }
.kpi-value.danger { color: var(--color-danger); }
.kpi-value.primary { color: var(--color-primary); }

.section { margin-top: 20px; }
.section-title { font-size: 13px; font-weight: 600; color: var(--color-gray-500); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 10px; padding-bottom: 6px; border-bottom: 1px solid var(--color-gray-200); }

.actions-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 10px; }
.action-card { display: flex; flex-direction: column; align-items: center; gap: 6px; padding: 16px 12px; background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); text-decoration: none; transition: all 0.15s; border: 1px solid transparent; }
.action-card:hover { border-color: var(--color-primary); box-shadow: 0 4px 6px rgba(0,0,0,0.07); }
.action-icon { font-size: 22px; }
.action-label { font-size: 12px; font-weight: 600; color: var(--color-gray-700); text-align: center; }

.section-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; }
.section-header .section-title { margin-bottom: 0; padding-bottom: 0; border-bottom: none; }
.btn-primary-sm { padding: 5px 14px; border-radius: 6px; font-size: 12px; font-weight: 600; background: var(--color-primary); color: white; text-decoration: none; }
.kpi-target { font-size: 9px; color: var(--color-gray-400); margin-top: 2px; }

.pm-projects { margin-top: 12px; background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); overflow: hidden; }
.pm-table { width: 100%; border-collapse: collapse; font-size: 12px; }
.pm-table thead th { padding: 8px 12px; font-size: 10px; font-weight: 600; text-transform: uppercase; color: var(--color-gray-500); background: var(--color-gray-50); border-bottom: 1px solid var(--color-gray-200); text-align: left; }
.pm-table tbody td { padding: 8px 12px; border-bottom: 1px solid var(--color-gray-100); }
.pm-table tbody tr:hover { background: var(--color-gray-50); }
.cursor-pointer { cursor: pointer; }
.text-muted { color: var(--color-gray-500); }
.text-right { text-align: right; }
.font-mono { font-family: var(--font-mono); }
.font-semibold { font-weight: 600; }
.health-dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; }
.health-dot.green { background: #15803D; }
.health-dot.gray { background: var(--color-gray-400); }
.see-all { display: block; padding: 8px 12px; font-size: 11px; font-weight: 600; color: var(--color-primary); text-decoration: none; text-align: right; border-top: 1px solid var(--color-gray-100); }
.see-all:hover { text-decoration: underline; }
</style>
