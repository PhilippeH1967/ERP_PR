<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { timesheetApi } from '../api/timesheetApi'
import type { WeeklyApproval } from '../types/timesheet.types'

const approvals = ref<WeeklyApproval[]>([])
const isLoading = ref(false)
const filter = ref<'pending' | 'all'>('pending')

async function fetchApprovals() {
  isLoading.value = true
  try {
    const params: Record<string, string> = filter.value === 'pending' ? { pm_status: 'PENDING' } : {}
    const response = await timesheetApi.listApprovals(params)
    approvals.value = response.data?.data || response.data || []
  } finally {
    isLoading.value = false
  }
}

async function approvePM(id: number) {
  await timesheetApi.approvePM(id)
  await fetchApprovals()
}

async function approveFinance(id: number) {
  await timesheetApi.approveFinance(id)
  await fetchApprovals()
}

onMounted(fetchApprovals)
</script>

<template>
  <div>
    <div class="mb-6 flex items-center justify-between">
      <h1 class="text-2xl font-semibold text-text">
        Approbation des feuilles de temps
      </h1>
      <div class="flex gap-2">
        <button
          class="rounded-md px-3 py-1.5 text-sm"
          :class="filter === 'pending' ? 'bg-primary text-white' : 'bg-surface-alt text-text-muted'"
          @click="filter = 'pending'; fetchApprovals()"
        >
          En attente
        </button>
        <button
          class="rounded-md px-3 py-1.5 text-sm"
          :class="filter === 'all' ? 'bg-primary text-white' : 'bg-surface-alt text-text-muted'"
          @click="filter = 'all'; fetchApprovals()"
        >
          Toutes
        </button>
      </div>
    </div>

    <div class="rounded-lg border border-border bg-surface">
      <table class="w-full text-left text-sm">
        <thead class="border-b border-border text-xs font-medium uppercase tracking-wide text-text-muted">
          <tr>
            <th class="px-4 py-3">
              Employé
            </th>
            <th class="px-4 py-3">
              Semaine
            </th>
            <th class="px-4 py-3">
              Statut PM
            </th>
            <th class="px-4 py-3">
              Statut Finance
            </th>
            <th class="px-4 py-3">
              Actions
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="approval in approvals"
            :key="approval.id"
            class="border-b border-border last:border-0"
          >
            <td class="px-4 py-3">
              Employé #{{ approval.employee }}
            </td>
            <td class="px-4 py-3 font-mono text-text-muted">
              {{ approval.week_start }}
            </td>
            <td class="px-4 py-3">
              <span
                class="rounded-full px-2 py-0.5 text-xs"
                :class="{
                  'bg-warning/10 text-warning': approval.pm_status === 'PENDING',
                  'bg-success/10 text-success': approval.pm_status === 'APPROVED',
                  'bg-danger/10 text-danger': approval.pm_status === 'REJECTED',
                }"
              >
                {{ approval.pm_status }}
              </span>
            </td>
            <td class="px-4 py-3">
              <span
                class="rounded-full px-2 py-0.5 text-xs"
                :class="{
                  'bg-warning/10 text-warning': approval.finance_status === 'PENDING',
                  'bg-success/10 text-success': approval.finance_status === 'APPROVED',
                  'bg-danger/10 text-danger': approval.finance_status === 'REJECTED',
                }"
              >
                {{ approval.finance_status }}
              </span>
            </td>
            <td class="px-4 py-3">
              <div class="flex gap-2">
                <button
                  v-if="approval.pm_status === 'PENDING'"
                  class="rounded bg-success px-3 py-1 text-xs font-medium text-white"
                  @click="approvePM(approval.id)"
                >
                  Approuver PM
                </button>
                <button
                  v-if="approval.pm_status === 'APPROVED' && approval.finance_status === 'PENDING'"
                  class="rounded bg-primary px-3 py-1 text-xs font-medium text-white"
                  @click="approveFinance(approval.id)"
                >
                  Approuver Finance
                </button>
                <span
                  v-if="approval.pm_status === 'APPROVED' && approval.finance_status === 'APPROVED'"
                  class="text-xs text-success"
                >
                  ✓ Complété
                </span>
              </div>
            </td>
          </tr>
          <tr v-if="!approvals.length && !isLoading">
            <td
              colspan="5"
              class="px-4 py-8 text-center text-text-muted"
            >
              Aucune feuille en attente d'approbation
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
