<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useLocale } from '@/shared/composables/useLocale'
import { expenseApi } from '../api/expenseApi'
import type { ExpenseReport } from '../types/expense.types'

const { fmt } = useLocale()
const reports = ref<ExpenseReport[]>([])

onMounted(async () => {
  try {
    const response = await expenseApi.listReports()
    reports.value = response.data?.data || response.data
  } catch {
    // Handle error
  }
})
</script>

<template>
  <div>
    <div class="mb-6 flex items-center justify-between">
      <h1 class="text-2xl font-semibold text-text">
        Dépenses
      </h1>
      <button class="rounded-md bg-primary px-4 py-2 text-sm font-medium text-white">
        + Nouvelle dépense
      </button>
    </div>

    <div class="rounded-lg border border-border bg-surface">
      <table class="w-full text-left text-sm">
        <thead class="border-b border-border text-xs font-medium uppercase tracking-wide text-text-muted">
          <tr>
            <th class="px-4 py-3">
              ID
            </th>
            <th class="px-4 py-3 text-right font-mono">
              Montant
            </th>
            <th class="px-4 py-3">
              Statut
            </th>
            <th class="px-4 py-3">
              Date
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="report in reports"
            :key="report.id"
            class="border-b border-border last:border-0 hover:bg-surface-alt"
          >
            <td class="px-4 py-3 font-mono">
              #{{ report.id }}
            </td>
            <td class="px-4 py-3 text-right font-mono">
              {{ fmt.currency(report.total_amount) }}
            </td>
            <td class="px-4 py-3">
              <span class="rounded-full bg-primary/10 px-2 py-0.5 text-xs text-primary">
                {{ report.status }}
              </span>
            </td>
            <td class="px-4 py-3 text-text-muted">
              {{ fmt.date(report.submitted_at) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
