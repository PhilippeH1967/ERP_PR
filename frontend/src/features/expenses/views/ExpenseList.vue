<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useLocale } from '@/shared/composables/useLocale'
import { expenseApi } from '../api/expenseApi'
import type { ExpenseReport } from '../types/expense.types'
import ExpenseCreateForm from '../components/ExpenseCreateForm.vue'

const { fmt } = useLocale()
const reports = ref<ExpenseReport[]>([])
const showCreateForm = ref(false)

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
        Mes dépenses
      </h1>
      <div class="flex gap-2">
        <button class="rounded-md border border-border bg-surface px-4 py-2 text-sm font-medium text-text-muted hover:bg-surface-alt">
          Depuis un modèle
        </button>
        <button
          class="rounded-md bg-primary px-4 py-2 text-sm font-medium text-white"
          @click="showCreateForm = true"
        >
          + Nouvelle dépense
        </button>
      </div>
    </div>

    <!-- KPI Cards (Fix #3) -->
    <div class="mb-6 grid grid-cols-4 gap-4">
      <div class="rounded-lg border border-border bg-surface p-4 text-center">
        <div class="text-2xl font-bold text-warning">
          {{ reports.filter(r => r.status === 'SUBMITTED').length }}
        </div>
        <div class="text-xs text-text-muted">
          En cours
        </div>
      </div>
      <div class="rounded-lg border border-border bg-surface p-4 text-center">
        <div class="text-2xl font-bold text-primary">
          {{ reports.filter(r => r.status === 'PM_APPROVED').length }}
        </div>
        <div class="text-xs text-text-muted">
          Soumises
        </div>
      </div>
      <div class="rounded-lg border border-border bg-surface p-4 text-center">
        <div class="text-2xl font-bold text-success">
          {{ reports.filter(r => r.status === 'PAID').length }}
        </div>
        <div class="text-xs text-text-muted">
          Approuvées
        </div>
      </div>
      <div class="rounded-lg border border-border bg-surface p-4 text-center">
        <div class="font-mono text-2xl font-bold text-text">
          {{ fmt.currency(reports.reduce((s, r) => s + parseFloat(r.total_amount || '0'), 0).toString()) }}
        </div>
        <div class="text-xs text-text-muted">
          Total ce mois
        </div>
      </div>
    </div>

    <!-- Reminder banner -->
    <div class="mb-4 rounded-lg border border-primary/20 bg-primary/5 p-3 text-sm text-primary">
      Rappel : une pièce justificative (photo ou PDF) est obligatoire pour chaque dépense.
    </div>

    <!-- Templates section (Fix #5) -->
    <div class="mb-6">
      <h3 class="mb-3 text-sm font-medium text-text-muted">
        Modèles fréquents
      </h3>
      <div class="flex gap-3">
        <div class="cursor-pointer rounded-lg border border-border bg-surface p-3 text-center hover:border-primary/30">
          <div class="text-lg">
            🚕
          </div>
          <div class="mt-1 text-xs font-medium">
            Taxi
          </div>
        </div>
        <div class="cursor-pointer rounded-lg border border-border bg-surface p-3 text-center hover:border-primary/30">
          <div class="text-lg">
            🍽️
          </div>
          <div class="mt-1 text-xs font-medium">
            Repas client
          </div>
        </div>
        <div class="cursor-pointer rounded-lg border border-border bg-surface p-3 text-center hover:border-primary/30">
          <div class="text-lg">
            🅿️
          </div>
          <div class="mt-1 text-xs font-medium">
            Stationnement
          </div>
        </div>
      </div>
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

    <ExpenseCreateForm
      :open="showCreateForm"
      @close="showCreateForm = false"
      @created="$router.go(0)"
    />
  </div>
</template>
