<script setup lang="ts">
import { onMounted, ref } from 'vue'
import apiClient from '@/plugins/axios'
import { useLocale } from '@/shared/composables/useLocale'

const { fmt } = useLocale()

interface KPIs {
  projects_active: number
  timesheets_pending: number
  invoices_outstanding: string
  expenses_pending: number
}

const kpis = ref<KPIs | null>(null)

onMounted(async () => {
  try {
    const response = await apiClient.get('dashboard/')
    kpis.value = response.data?.data?.kpis || response.data?.kpis
  } catch {
    // Dashboard KPIs will be empty until data exists
  }
})
</script>

<template>
  <div>
    <div class="page-header">
      <h1>Tableau de bord</h1>
    </div>

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
        <p class="kpi-label">Factures impay&#233;es</p>
        <p class="kpi-value danger mono">
          {{ kpis?.invoices_outstanding ? fmt.currency(kpis.invoices_outstanding) : '—' }}
        </p>
      </div>
      <div class="kpi-card">
        <p class="kpi-label">D&#233;penses en attente</p>
        <p class="kpi-value">{{ kpis?.expenses_pending ?? '—' }}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}
.page-header h1 {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-gray-900);
}
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}
.kpi-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06);
  padding: 20px;
}
.kpi-label {
  font-size: 12px;
  color: var(--color-gray-500);
  text-transform: uppercase;
  font-weight: 600;
  letter-spacing: 0.3px;
  margin-bottom: 4px;
}
.kpi-value {
  font-size: 28px;
  font-weight: 700;
  color: var(--color-gray-900);
}
.kpi-value.mono {
  font-family: var(--font-mono);
}
.kpi-value.warning {
  color: var(--color-warning);
}
.kpi-value.danger {
  color: var(--color-danger);
}
</style>
