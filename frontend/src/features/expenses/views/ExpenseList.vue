<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useLocale } from '@/shared/composables/useLocale'
import { expenseApi } from '../api/expenseApi'
import type { ExpenseReport } from '../types/expense.types'
import ExpenseCreateForm from '../components/ExpenseCreateForm.vue'

const router = useRouter()
const { fmt } = useLocale()
const reports = ref<ExpenseReport[]>([])
const showCreateForm = ref(false)

const statusLabels: Record<string, string> = {
  SUBMITTED: 'Soumis',
  PM_APPROVED: 'Approuvé PM',
  FINANCE_VALIDATED: 'Validé Finance',
  PAID: 'Payé',
  REVERSED: 'Annulé',
  REJECTED: 'Refusé',
}
const statusColors: Record<string, string> = {
  SUBMITTED: 'badge-blue',
  PM_APPROVED: 'badge-amber',
  FINANCE_VALIDATED: 'badge-green',
  PAID: 'badge-green-solid',
  REVERSED: 'badge-gray',
  REJECTED: 'badge-red',
}

const templates = [
  { icon: '🚕', label: 'Taxi', defaults: { description: 'Course taxi', tax_type: 'TPS' } },
  { icon: '🍽️', label: 'Repas client', defaults: { description: 'Repas affaires', tax_type: 'TPS' } },
  { icon: '🅿️', label: 'Stationnement', defaults: { description: 'Stationnement', tax_type: 'HT' } },
]

async function fetch() {
  try {
    const response = await expenseApi.listReports()
    const data = response.data?.data || response.data
    reports.value = Array.isArray(data) ? data : data?.results || []
  } catch { reports.value = [] }
}

function openFromTemplate(tmpl: typeof templates[0]) {
  // Open create form — template defaults will be applied later
  showCreateForm.value = true
}

async function onCreated() {
  showCreateForm.value = false
  await fetch()
}

onMounted(fetch)
</script>

<template>
  <div>
    <div class="page-header">
      <h1>Mes dépenses</h1>
      <button class="btn-primary" @click="showCreateForm = true">+ Nouvelle dépense</button>
    </div>

    <!-- KPIs -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-value warning">{{ reports.filter(r => r.status === 'SUBMITTED').length }}</div>
        <div class="kpi-label">Soumis</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-value primary">{{ reports.filter(r => r.status === 'PM_APPROVED').length }}</div>
        <div class="kpi-label">Approuvés PM</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-value success">{{ reports.filter(r => r.status === 'PAID').length }}</div>
        <div class="kpi-label">Payés</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-value mono">{{ fmt.currency(reports.reduce((s, r) => s + parseFloat(r.total_amount || '0'), 0).toString()) }}</div>
        <div class="kpi-label">Total</div>
      </div>
    </div>

    <!-- Templates -->
    <div class="templates-section">
      <span class="templates-label">Modèles fréquents</span>
      <div class="templates-row">
        <button v-for="tmpl in templates" :key="tmpl.label" class="template-btn" @click="openFromTemplate(tmpl)">
          <span class="template-icon">{{ tmpl.icon }}</span>
          <span class="template-name">{{ tmpl.label }}</span>
        </button>
      </div>
    </div>

    <!-- Table -->
    <div class="card-table">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th class="text-right">Montant</th>
            <th>Statut</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="report in reports"
            :key="report.id"
            class="row-link"
            @click="router.push(`/expenses/${report.id}`)"
          >
            <td class="font-mono">#{{ report.id }}</td>
            <td class="text-right font-mono font-semibold">{{ fmt.currency(report.total_amount) }}</td>
            <td>
              <span class="badge" :class="statusColors[report.status]">{{ statusLabels[report.status] || report.status }}</span>
            </td>
            <td class="text-muted">{{ fmt.date(report.submitted_at) }}</td>
          </tr>
          <tr v-if="!reports.length"><td colspan="4" class="empty">Aucune dépense</td></tr>
        </tbody>
      </table>
    </div>

    <ExpenseCreateForm :open="showCreateForm" @close="showCreateForm = false" @created="onCreated" />
  </div>
</template>

<style scoped>
.page-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }
.page-header h1 { font-size: 20px; font-weight: 700; color: var(--color-gray-900); }
.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 16px; }
.kpi-card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 14px; text-align: center; }
.kpi-value { font-size: 22px; font-weight: 700; color: var(--color-gray-900); }
.kpi-value.warning { color: var(--color-warning); } .kpi-value.primary { color: var(--color-primary); }
.kpi-value.success { color: var(--color-success); } .kpi-value.mono { font-family: var(--font-mono); font-size: 18px; }
.kpi-label { font-size: 10px; color: var(--color-gray-500); text-transform: uppercase; font-weight: 600; }

.templates-section { margin-bottom: 16px; }
.templates-label { font-size: 12px; font-weight: 600; color: var(--color-gray-500); margin-bottom: 8px; display: block; }
.templates-row { display: flex; gap: 8px; }
.template-btn { display: flex; align-items: center; gap: 6px; padding: 6px 14px; border-radius: 6px; border: 1px solid var(--color-gray-200); background: white; cursor: pointer; font-size: 12px; transition: all 0.15s; }
.template-btn:hover { border-color: var(--color-primary); background: rgba(37,99,235,0.03); }
.template-icon { font-size: 16px; } .template-name { font-weight: 500; color: var(--color-gray-700); }

.card-table { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); overflow: hidden; }
.row-link { cursor: pointer; } .row-link:hover { background: var(--color-gray-50); }
.text-right { text-align: right; } .text-muted { color: var(--color-gray-500); }
.font-mono { font-family: var(--font-mono); font-size: 12px; }
.badge { display: inline-flex; padding: 1px 8px; border-radius: 10px; font-size: 10px; font-weight: 600; }
.badge-blue { background: #DBEAFE; color: #1D4ED8; } .badge-amber { background: #FEF3C7; color: #92400E; }
.badge-green { background: #DCFCE7; color: #15803D; } .badge-green-solid { background: #15803D; color: white; }
.badge-gray { background: var(--color-gray-100); color: var(--color-gray-500); } .badge-red { background: #FEE2E2; color: #DC2626; }
.empty { text-align: center; padding: 30px; color: var(--color-gray-400); }
</style>
