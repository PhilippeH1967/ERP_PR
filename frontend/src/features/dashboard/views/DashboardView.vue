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
}

interface SystemHealth {
  active_users: number
  pending_approvals: number
  overdue_invoices: number
}

const kpis = ref<KPIs | null>(null)
const pmKpis = ref<PMKPIs | null>(null)
const healthKpis = ref<SystemHealth | null>(null)

const roles = computed(() => currentUser.value?.roles || [])
const isPM = computed(() => roles.value.includes('PM') || roles.value.includes('PROJECT_DIRECTOR'))
const isFinance = computed(() => roles.value.includes('FINANCE'))
const isAdmin = computed(() => roles.value.includes('ADMIN'))

onMounted(async () => {
  // Base KPIs for all roles
  try {
    const resp = await apiClient.get('dashboard/')
    kpis.value = resp.data?.kpis || resp.data?.data?.kpis
  } catch { /* empty */ }

  // PM KPIs
  if (isPM.value || isAdmin.value) {
    try {
      const resp = await apiClient.get('dashboard/pm-kpis/')
      pmKpis.value = resp.data?.data || resp.data
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
      <h1>Tableau de bord</h1>
      <span class="role-info">
        {{ currentUser?.username }} — {{ roles.join(', ') || 'Employé' }}
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

    <!-- PM Section -->
    <div v-if="pmKpis && (isPM || isAdmin)" class="section">
      <h2 class="section-title">Chef de projet</h2>
      <div class="kpi-grid-3">
        <div class="kpi-card">
          <p class="kpi-label">Projets gérés</p>
          <p class="kpi-value primary">{{ pmKpis.projects_managed }}</p>
        </div>
        <div class="kpi-card">
          <p class="kpi-label">Total facturé</p>
          <p class="kpi-value mono">{{ fmt.currency(pmKpis.total_invoiced) }}</p>
        </div>
        <div class="kpi-card">
          <p class="kpi-label">Heures totales</p>
          <p class="kpi-value mono">{{ fmt.hours(pmKpis.total_hours) }}</p>
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
</style>
