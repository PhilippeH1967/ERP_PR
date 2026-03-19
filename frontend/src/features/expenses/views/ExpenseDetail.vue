<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useLocale } from '@/shared/composables/useLocale'
import { expenseApi } from '../api/expenseApi'
import type { ExpenseReport } from '../types/expense.types'

const route = useRoute()
const router = useRouter()
const { fmt } = useLocale()
const reportId = Number(route.params.id)
const report = ref<ExpenseReport | null>(null)
const actionError = ref('')

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

async function reload() {
  const resp = await expenseApi.getReport(reportId)
  report.value = resp.data?.data || resp.data
}

async function approveAsPM() {
  actionError.value = ''
  try {
    await expenseApi.updateReport(reportId, { status: 'PM_APPROVED' })
    await reload()
  } catch (e: unknown) {
    actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur'
  }
}

async function validateAsFinance() {
  actionError.value = ''
  try {
    await expenseApi.updateReport(reportId, { status: 'FINANCE_VALIDATED' })
    await reload()
  } catch (e: unknown) {
    actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur'
  }
}

async function markPaid() {
  actionError.value = ''
  try {
    await expenseApi.updateReport(reportId, { status: 'PAID' })
    await reload()
  } catch (e: unknown) {
    actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur'
  }
}

async function reject() {
  actionError.value = ''
  try {
    await expenseApi.updateReport(reportId, { status: 'REJECTED' })
    await reload()
  } catch (e: unknown) {
    actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur'
  }
}

onMounted(reload)
</script>

<template>
  <div v-if="report">
    <div class="page-header">
      <div>
        <button class="btn-back" @click="router.push('/expenses')">&larr; Dépenses</button>
        <h1>Rapport #{{ report.id }}</h1>
        <p class="subtitle">{{ fmt.date(report.submitted_at) }}</p>
      </div>
      <div class="header-actions">
        <span class="badge" :class="statusColors[report.status]">{{ statusLabels[report.status] || report.status }}</span>
        <button v-if="report.status === 'SUBMITTED'" class="btn-primary" @click="approveAsPM">Approuver (PM)</button>
        <button v-if="report.status === 'PM_APPROVED'" class="btn-success" @click="validateAsFinance">Valider (Finance)</button>
        <button v-if="report.status === 'FINANCE_VALIDATED'" class="btn-success" @click="markPaid">Marquer payé</button>
        <button v-if="report.status === 'SUBMITTED' || report.status === 'PM_APPROVED'" class="btn-danger" @click="reject">Refuser</button>
      </div>
    </div>

    <div v-if="actionError" class="alert-error">{{ actionError }}</div>

    <!-- Summary -->
    <div class="summary-banner">
      <div class="summary-item">
        <span class="summary-value">{{ fmt.currency(report.total_amount) }}</span>
        <span class="summary-label">Montant total</span>
      </div>
      <div class="summary-item">
        <span class="summary-value">{{ report.lines?.length || 0 }}</span>
        <span class="summary-label">Lignes</span>
      </div>
    </div>

    <!-- Lines -->
    <div class="card-table">
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th class="text-right">Montant</th>
            <th>Description</th>
            <th>Taxes</th>
            <th>Refacturable</th>
            <th>Reçu</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="line in report.lines" :key="line.id">
            <td class="text-muted">{{ fmt.date(line.expense_date) }}</td>
            <td class="text-right font-mono font-semibold">{{ fmt.currency(line.amount) }}</td>
            <td>{{ line.description || '—' }}</td>
            <td><span class="badge badge-gray">{{ line.tax_type }}</span></td>
            <td>
              <span :class="line.is_refacturable ? 'flag-yes' : 'flag-no'">
                {{ line.is_refacturable ? 'Oui' : 'Non' }}
              </span>
            </td>
            <td>
              <span v-if="line.receipt_path" class="flag-yes">Oui</span>
              <span v-else class="flag-no">Manquant</span>
            </td>
          </tr>
          <tr v-if="!report.lines?.length"><td colspan="6" class="empty">Aucune ligne</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.page-header { display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 16px; }
.page-header h1 { font-size: 20px; font-weight: 700; color: var(--color-gray-900); margin-top: 2px; }
.btn-back { background: none; border: none; font-size: 12px; color: var(--color-gray-500); cursor: pointer; padding: 0; }
.subtitle { font-size: 12px; color: var(--color-gray-500); }
.header-actions { display: flex; align-items: center; gap: 6px; }
.btn-success { padding: 6px 12px; border-radius: 4px; font-size: 12px; font-weight: 600; cursor: pointer; border: none; background: var(--color-success); color: white; }
.btn-danger { padding: 6px 12px; border-radius: 4px; font-size: 12px; font-weight: 600; cursor: pointer; border: none; background: var(--color-danger); color: white; }
.alert-error { background: var(--color-danger-light); color: var(--color-danger); padding: 8px 12px; border-radius: 6px; font-size: 12px; margin-bottom: 12px; }
.badge { display: inline-flex; padding: 2px 10px; border-radius: 10px; font-size: 10px; font-weight: 600; }
.badge-blue { background: #DBEAFE; color: #1D4ED8; } .badge-amber { background: #FEF3C7; color: #92400E; }
.badge-green { background: #DCFCE7; color: #15803D; } .badge-green-solid { background: #15803D; color: white; }
.badge-gray { background: var(--color-gray-100); color: var(--color-gray-500); } .badge-red { background: #FEE2E2; color: #DC2626; }
.summary-banner { display: flex; gap: 24px; padding: 14px 16px; background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 12px; }
.summary-item { display: flex; flex-direction: column; }
.summary-value { font-size: 18px; font-weight: 700; font-family: var(--font-mono); color: var(--color-gray-900); }
.summary-label { font-size: 10px; color: var(--color-gray-500); }
.card-table { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); overflow: hidden; }
.text-right { text-align: right; } .text-muted { color: var(--color-gray-500); }
.font-mono { font-family: var(--font-mono); font-size: 12px; }
.flag-yes { font-size: 11px; font-weight: 600; color: #15803D; } .flag-no { font-size: 11px; color: var(--color-danger); }
.empty { text-align: center; padding: 30px; color: var(--color-gray-400); }
</style>
