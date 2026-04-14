<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { planningApi } from '../api/planningApi'
import ResourceGantt from '../components/ResourceGantt.vue'

const viewMode = ref<'gantt' | 'table'>('gantt')

const isLoading = ref(false)
const employees = ref<Array<Record<string, unknown>>>([])
const alerts = ref<Array<Record<string, unknown>>>([])
const startDate = ref(new Date().toISOString().slice(0, 7) + '-01')
const endDate = ref('')

// Set default end to end of month
const today = new Date()
const lastDay = new Date(today.getFullYear(), today.getMonth() + 1, 0)
endDate.value = lastDay.toISOString().slice(0, 10)

async function load() {
  isLoading.value = true
  try {
    const [planResp, alertResp] = await Promise.all([
      planningApi.globalPlanning({ start_date: startDate.value, end_date: endDate.value }),
      planningApi.loadAlerts(),
    ])
    const planData = planResp.data?.data || planResp.data
    employees.value = planData?.employees || []
    const alertData = alertResp.data?.data || alertResp.data
    alerts.value = alertData?.alerts || []
  } catch { employees.value = []; alerts.value = [] }
  finally { isLoading.value = false }
}

onMounted(load)

const totalEmployees = computed(() => employees.value.length)
const overloaded = computed(() => employees.value.filter(e => e.load_status === 'overload' || e.load_status === 'critical').length)
const underloaded = computed(() => employees.value.filter(e => e.load_status === 'underload').length)

function loadColor(status: unknown): string {
  if (status === 'critical') return 'bg-danger'
  if (status === 'overload') return 'bg-warning'
  if (status === 'underload') return 'bg-blue'
  return 'bg-success'
}
function loadBadge(status: unknown): string {
  if (status === 'critical') return 'badge-red'
  if (status === 'overload') return 'badge-amber'
  if (status === 'underload') return 'badge-blue'
  return 'badge-green'
}
function loadLabel(status: unknown): string {
  if (status === 'critical') return 'Critique'
  if (status === 'overload') return 'Surcharge'
  if (status === 'underload') return 'Sous-charge'
  return 'Normal'
}
</script>

<template>
  <div>
    <!-- View toggle -->
    <div class="mb-4 flex items-center gap-3">
      <button class="rounded-md px-3 py-1.5 text-sm font-semibold" :class="viewMode === 'gantt' ? 'bg-primary text-white' : 'bg-surface border border-border text-text-muted'" @click="viewMode = 'gantt'">Vue Gantt</button>
      <button class="rounded-md px-3 py-1.5 text-sm font-semibold" :class="viewMode === 'table' ? 'bg-primary text-white' : 'bg-surface border border-border text-text-muted'" @click="viewMode = 'table'">Vue tableau</button>
    </div>

    <!-- Resource Gantt (new) -->
    <ResourceGantt v-if="viewMode === 'gantt'" />

    <!-- Original table view -->
    <template v-if="viewMode === 'table'">
    <div class="mb-6 flex items-center justify-between">
      <h1 class="text-2xl font-semibold text-text">Planification des ressources</h1>
      <div class="flex items-center gap-3">
        <input v-model="startDate" type="date" class="rounded border border-border px-2 py-1.5 text-sm" />
        <span class="text-text-muted">→</span>
        <input v-model="endDate" type="date" class="rounded border border-border px-2 py-1.5 text-sm" />
        <button class="rounded bg-primary px-3 py-1.5 text-sm font-medium text-white" @click="load">Actualiser</button>
      </div>
    </div>

    <!-- KPIs -->
    <div class="mb-6 grid grid-cols-4 gap-4">
      <div class="kpi-card"><div class="kpi-value">{{ totalEmployees }}</div><div class="kpi-label">Employés planifiés</div></div>
      <div class="kpi-card"><div class="kpi-value text-danger">{{ overloaded }}</div><div class="kpi-label">En surcharge</div></div>
      <div class="kpi-card"><div class="kpi-value text-blue">{{ underloaded }}</div><div class="kpi-label">Sous-charge</div></div>
      <div class="kpi-card"><div class="kpi-value text-amber">{{ alerts.length }}</div><div class="kpi-label">Alertes actives</div></div>
    </div>

    <!-- Alerts panel -->
    <div v-if="alerts.length" class="mb-4 rounded-lg border border-warning/30 bg-warning/5 p-3">
      <h3 class="mb-2 text-xs font-semibold uppercase text-warning">Alertes de charge (4 prochaines semaines)</h3>
      <div v-for="(a, i) in alerts" :key="i" class="flex items-center gap-3 py-1 text-sm">
        <span class="badge" :class="loadBadge(a.alert_type)">{{ loadLabel(a.alert_type) }}</span>
        <span class="font-medium">{{ a.employee_name }}</span>
        <span class="font-mono text-text-muted">{{ a.planned_hours_week }}h/{{ a.contract_hours }}h ({{ a.load_percent }}%)</span>
      </div>
    </div>

    <!-- Planning grid -->
    <div v-if="isLoading" class="py-8 text-center text-text-muted">Chargement...</div>
    <div v-else-if="!employees.length" class="rounded-lg border border-border bg-surface p-8 text-center text-text-muted">
      Aucune allocation active pour cette période
    </div>
    <div v-else class="rounded-lg border border-border bg-surface">
      <table class="w-full text-left text-sm">
        <thead class="border-b border-border text-xs font-medium uppercase tracking-wide text-text-muted">
          <tr>
            <th class="px-4 py-3">Employé</th>
            <th class="px-4 py-3">Projets</th>
            <th class="px-4 py-3 text-right">Planifié</th>
            <th class="px-4 py-3 text-right">Contrat</th>
            <th class="px-4 py-3" style="width:200px;">Charge</th>
            <th class="px-4 py-3">Statut</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="emp in employees" :key="Number(emp.employee_id)" class="border-b border-border last:border-0">
            <td class="px-4 py-3 font-medium">{{ emp.employee_name }}</td>
            <td class="px-4 py-3">
              <div v-for="(alloc, ai) in (emp.allocations as Array<Record<string, unknown>>)" :key="ai" class="text-xs text-text-muted">
                {{ alloc.project_code }} <span v-if="alloc.phase_name">/ {{ alloc.phase_name }}</span> — {{ alloc.hours_per_week }}h/sem
              </div>
            </td>
            <td class="px-4 py-3 text-right font-mono font-semibold">{{ emp.total_planned_hours_week }}h</td>
            <td class="px-4 py-3 text-right font-mono text-text-muted">{{ emp.contract_hours }}h</td>
            <td class="px-4 py-3">
              <div class="h-3 w-full overflow-hidden rounded-full bg-gray-200">
                <div class="h-3 rounded-full transition-all" :class="loadColor(emp.load_status)" :style="{ width: Math.min(100, Number(emp.load_percent)) + '%' }"></div>
              </div>
              <div class="mt-1 text-xs text-text-muted text-right">{{ emp.load_percent }}%</div>
            </td>
            <td class="px-4 py-3">
              <span class="badge" :class="loadBadge(emp.load_status)">{{ loadLabel(emp.load_status) }}</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    </template>
  </div>
</template>

<style scoped>
.badge { display: inline-flex; padding: 2px 10px; border-radius: 10px; font-size: 10px; font-weight: 600; }
.badge-green { background: #DCFCE7; color: #15803D; }
.badge-amber { background: #FEF3C7; color: #92400E; }
.badge-blue { background: #DBEAFE; color: #1D4ED8; }
.badge-red { background: #FEE2E2; color: #DC2626; }
.kpi-card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 14px; text-align: center; }
.kpi-value { font-size: 28px; font-weight: 700; color: var(--color-gray-900); }
.kpi-label { font-size: 11px; color: var(--color-gray-500); text-transform: uppercase; font-weight: 600; margin-top: 4px; }
.text-danger { color: #DC2626; }
.text-blue { color: #1D4ED8; }
.text-amber { color: #92400E; }
.bg-danger { background: #DC2626; }
.bg-warning { background: #F59E0B; }
.bg-success { background: #15803D; }
.bg-blue { background: #3B82F6; }
</style>
