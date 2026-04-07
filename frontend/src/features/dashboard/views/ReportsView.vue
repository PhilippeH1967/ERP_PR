<script setup lang="ts">
import { ref, onMounted } from 'vue'
import apiClient from '@/plugins/axios'

const groupBy = ref('project')
const startDate = ref(new Date().toISOString().slice(0, 7) + '-01')
const endDate = ref(new Date().toISOString().slice(0, 10))
const reportData = ref<Array<Record<string, unknown>>>([])
const isLoading = ref(false)

async function loadReport() {
  isLoading.value = true
  try {
    const resp = await apiClient.get('dashboard/hours-report/', {
      params: { group_by: groupBy.value, start_date: startDate.value, end_date: endDate.value }
    })
    reportData.value = resp.data?.data || []
  } catch { reportData.value = [] }
  finally { isLoading.value = false }
}

onMounted(loadReport)

function exportCSV() {
  const type = groupBy.value === 'project' ? 'time_entries' : 'time_entries'
  window.open(`/api/v1/exports/${type}/?month=${new Date(startDate.value).getMonth() + 1}&year=${new Date(startDate.value).getFullYear()}`, '_blank')
}
</script>

<template>
  <div>
    <div class="mb-6 flex items-center justify-between">
      <h1 class="text-2xl font-semibold text-text">Rapports d'heures</h1>
      <button class="rounded-md bg-primary/10 px-4 py-2 text-sm font-medium text-primary" @click="exportCSV">
        Exporter CSV
      </button>
    </div>

    <!-- Filters -->
    <div class="mb-4 flex flex-wrap items-center gap-3">
      <select v-model="groupBy" class="filter-select" @change="loadReport">
        <option value="project">Par projet</option>
        <option value="employee">Par employé</option>
        <option value="bu">Par unité d'affaires</option>
      </select>
      <input v-model="startDate" type="date" class="filter-select" />
      <span class="text-text-muted">→</span>
      <input v-model="endDate" type="date" class="filter-select" />
      <button class="rounded bg-primary px-3 py-1.5 text-sm font-medium text-white" @click="loadReport">Actualiser</button>
    </div>

    <div v-if="isLoading" class="py-8 text-center text-text-muted">Chargement...</div>
    <div v-else-if="!reportData.length" class="rounded-lg border border-border bg-surface p-8 text-center text-text-muted">
      Aucune donnée pour cette période
    </div>

    <!-- Project report -->
    <div v-else-if="groupBy === 'project'" class="rounded-lg border border-border bg-surface">
      <table class="w-full text-left text-sm">
        <thead class="border-b border-border text-xs font-medium uppercase tracking-wide text-text-muted">
          <tr>
            <th class="px-4 py-3">Code</th>
            <th class="px-4 py-3">Projet</th>
            <th class="px-4 py-3 text-right">Heures</th>
            <th class="px-4 py-3">Facturable</th>
            <th class="px-4 py-3 text-right">Entrées</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in reportData" :key="String(r.group)" class="border-b border-border last:border-0">
            <td class="px-4 py-3 font-mono font-semibold">{{ r.group }}</td>
            <td class="px-4 py-3">{{ r.label }}</td>
            <td class="px-4 py-3 text-right font-mono">{{ Number(r.total_hours).toFixed(1) }}</td>
            <td class="px-4 py-3">
              <span class="badge" :class="r.billable ? 'badge-green' : 'badge-gray'">{{ r.billable ? 'Oui' : 'Non' }}</span>
            </td>
            <td class="px-4 py-3 text-right font-mono">{{ r.entries }}</td>
          </tr>
        </tbody>
        <tfoot class="border-t-2 border-border bg-surface-alt">
          <tr>
            <td colspan="2" class="px-4 py-3 font-semibold">Total</td>
            <td class="px-4 py-3 text-right font-mono font-semibold">{{ reportData.reduce((s, r) => s + Number(r.total_hours || 0), 0).toFixed(1) }}</td>
            <td></td>
            <td class="px-4 py-3 text-right font-mono font-semibold">{{ reportData.reduce((s, r) => s + Number(r.entries || 0), 0) }}</td>
          </tr>
        </tfoot>
      </table>
    </div>

    <!-- Employee report -->
    <div v-else-if="groupBy === 'employee'" class="rounded-lg border border-border bg-surface">
      <table class="w-full text-left text-sm">
        <thead class="border-b border-border text-xs font-medium uppercase tracking-wide text-text-muted">
          <tr>
            <th class="px-4 py-3">Employé</th>
            <th class="px-4 py-3 text-right">Total heures</th>
            <th class="px-4 py-3 text-right">Heures facturables</th>
            <th class="px-4 py-3 text-right">Taux facturation</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in reportData" :key="String(r.group)" class="border-b border-border last:border-0">
            <td class="px-4 py-3 font-semibold">{{ r.label }}</td>
            <td class="px-4 py-3 text-right font-mono">{{ Number(r.total_hours).toFixed(1) }}</td>
            <td class="px-4 py-3 text-right font-mono">{{ Number(r.billable_hours).toFixed(1) }}</td>
            <td class="px-4 py-3 text-right">
              <span class="font-mono" :class="Number(r.billing_rate) >= 75 ? 'text-success' : 'text-warning'">{{ r.billing_rate }}%</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- BU report -->
    <div v-else class="rounded-lg border border-border bg-surface">
      <table class="w-full text-left text-sm">
        <thead class="border-b border-border text-xs font-medium uppercase tracking-wide text-text-muted">
          <tr>
            <th class="px-4 py-3">Unité d'affaires</th>
            <th class="px-4 py-3 text-right">Total heures</th>
            <th class="px-4 py-3 text-right">Heures facturables</th>
            <th class="px-4 py-3 text-right">Projets</th>
            <th class="px-4 py-3 text-right">Employés</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in reportData" :key="String(r.group)" class="border-b border-border last:border-0">
            <td class="px-4 py-3 font-semibold">{{ r.group }}</td>
            <td class="px-4 py-3 text-right font-mono">{{ Number(r.total_hours).toFixed(1) }}</td>
            <td class="px-4 py-3 text-right font-mono">{{ Number(r.billable_hours).toFixed(1) }}</td>
            <td class="px-4 py-3 text-right font-mono">{{ r.projects }}</td>
            <td class="px-4 py-3 text-right font-mono">{{ r.employees }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.filter-select { padding: 6px 10px; border: 1px solid var(--color-gray-300); border-radius: 6px; font-size: 12px; }
.badge { display: inline-flex; padding: 2px 10px; border-radius: 10px; font-size: 10px; font-weight: 600; }
.badge-green { background: #DCFCE7; color: #15803D; }
.badge-gray { background: var(--color-gray-100); color: var(--color-gray-500); }
.text-success { color: #15803D; }
.text-warning { color: #92400E; }
</style>
