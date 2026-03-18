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
    <h1 class="mb-6 text-2xl font-semibold text-text">
      Tableau de bord
    </h1>

    <div class="grid grid-cols-4 gap-4">
      <div class="rounded-lg border border-border bg-surface p-6">
        <p class="text-sm text-text-muted">
          Projets actifs
        </p>
        <p class="mt-1 text-3xl font-semibold text-text">
          {{ kpis?.projects_active ?? '—' }}
        </p>
      </div>
      <div class="rounded-lg border border-border bg-surface p-6">
        <p class="text-sm text-text-muted">
          Feuilles en attente
        </p>
        <p class="mt-1 text-3xl font-semibold text-warning">
          {{ kpis?.timesheets_pending ?? '—' }}
        </p>
      </div>
      <div class="rounded-lg border border-border bg-surface p-6">
        <p class="text-sm text-text-muted">
          Factures impayées
        </p>
        <p class="mt-1 font-mono text-3xl font-semibold text-danger">
          {{ kpis?.invoices_outstanding ? fmt.currency(kpis.invoices_outstanding) : '—' }}
        </p>
      </div>
      <div class="rounded-lg border border-border bg-surface p-6">
        <p class="text-sm text-text-muted">
          Dépenses en attente
        </p>
        <p class="mt-1 text-3xl font-semibold text-text">
          {{ kpis?.expenses_pending ?? '—' }}
        </p>
      </div>
    </div>
  </div>
</template>
