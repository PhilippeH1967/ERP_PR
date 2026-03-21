<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { timesheetApi } from '../api/timesheetApi'
import type { WeeklyApproval } from '../types/timesheet.types'

const approvals = ref<WeeklyApproval[]>([])
const isLoading = ref(false)
const filter = ref<'pending' | 'all'>('pending')
const rejectingId = ref<number | null>(null)
const rejectReason = ref('')
const actionError = ref('')

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
  actionError.value = ''
  try {
    await timesheetApi.approvePM(id)
    await fetchApprovals()
  } catch (e: unknown) {
    actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur'
  }
}

async function approveFinance(id: number) {
  actionError.value = ''
  try {
    await timesheetApi.approveFinance(id)
    await fetchApprovals()
  } catch (e: unknown) {
    actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur'
  }
}

async function rejectPM(id: number) {
  actionError.value = ''
  try {
    await timesheetApi.rejectPM(id, rejectReason.value)
    rejectingId.value = null
    rejectReason.value = ''
    await fetchApprovals()
  } catch (e: unknown) {
    actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur'
  }
}

async function rejectFinance(id: number) {
  actionError.value = ''
  try {
    await timesheetApi.rejectFinance(id)
    await fetchApprovals()
  } catch (e: unknown) {
    actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur'
  }
}

onMounted(fetchApprovals)
</script>

<template>
  <div>
    <div class="page-header">
      <h1>Approbation des feuilles de temps</h1>
      <div class="flex gap-2">
        <button class="filter-btn" :class="{ active: filter === 'pending' }" @click="filter = 'pending'; fetchApprovals()">En attente</button>
        <button class="filter-btn" :class="{ active: filter === 'all' }" @click="filter = 'all'; fetchApprovals()">Toutes</button>
      </div>
    </div>

    <div v-if="actionError" class="alert-error">{{ actionError }}</div>

    <div class="card-table">
      <table>
        <thead>
          <tr>
            <th>Employé</th>
            <th>Semaine</th>
            <th>Statut PM</th>
            <th>Statut Finance</th>
            <th style="text-align:right">Actions</th>
          </tr>
        </thead>
        <tbody>
          <template v-for="approval in approvals" :key="approval.id">
            <tr>
              <td class="font-semibold">Employé #{{ approval.employee }}</td>
              <td class="font-mono text-muted">{{ approval.week_start }}</td>
              <td>
                <span class="badge" :class="{
                  'badge-amber': approval.pm_status === 'PENDING',
                  'badge-green': approval.pm_status === 'APPROVED',
                  'badge-red': approval.pm_status === 'REJECTED',
                }">{{ approval.pm_status === 'PENDING' ? 'En attente' : approval.pm_status === 'APPROVED' ? 'Approuvé' : 'Rejeté' }}</span>
              </td>
              <td>
                <span class="badge" :class="{
                  'badge-amber': approval.finance_status === 'PENDING',
                  'badge-green': approval.finance_status === 'APPROVED',
                  'badge-red': approval.finance_status === 'REJECTED',
                }">{{ approval.finance_status === 'PENDING' ? 'En attente' : approval.finance_status === 'APPROVED' ? 'Approuvé' : 'Rejeté' }}</span>
              </td>
              <td class="actions-cell">
                <!-- PM actions -->
                <template v-if="approval.pm_status === 'PENDING'">
                  <button class="btn-action success" @click="approvePM(approval.id)">Approuver</button>
                  <button class="btn-action danger" @click="rejectingId = rejectingId === approval.id ? null : approval.id">Rejeter</button>
                </template>
                <!-- Finance actions -->
                <template v-if="approval.pm_status === 'APPROVED' && approval.finance_status === 'PENDING'">
                  <button class="btn-action success" @click="approveFinance(approval.id)">Approuver Finance</button>
                  <button class="btn-action danger" @click="rejectFinance(approval.id)">Rejeter Finance</button>
                </template>
                <!-- Completed -->
                <span v-if="approval.pm_status === 'APPROVED' && approval.finance_status === 'APPROVED'" class="completed">✓ Complété</span>
                <!-- Rejected -->
                <span v-if="approval.pm_status === 'REJECTED'" class="rejected">Rejeté — renvoyé pour modification</span>
              </td>
            </tr>
            <!-- Rejection reason row -->
            <tr v-if="rejectingId === approval.id">
              <td colspan="5" class="reject-row">
                <div class="reject-form">
                  <input v-model="rejectReason" type="text" placeholder="Motif du rejet (optionnel)..." class="reject-input" />
                  <button class="btn-danger" @click="rejectPM(approval.id)">Confirmer le rejet</button>
                  <button class="btn-ghost" @click="rejectingId = null; rejectReason = ''">Annuler</button>
                </div>
              </td>
            </tr>
          </template>
          <tr v-if="!approvals.length && !isLoading">
            <td colspan="5" class="empty">Aucune feuille en attente d'approbation</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.page-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }
.page-header h1 { font-size: 20px; font-weight: 700; color: var(--color-gray-900); }
.filter-btn { padding: 4px 12px; border-radius: 4px; font-size: 12px; border: none; cursor: pointer; color: var(--color-gray-500); background: var(--color-gray-100); }
.filter-btn.active { background: var(--color-primary); color: white; }
.alert-error { background: var(--color-danger-light); color: var(--color-danger); padding: 8px 12px; border-radius: 6px; font-size: 12px; margin-bottom: 12px; }
.card-table { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); overflow: hidden; }
.font-mono { font-family: var(--font-mono); font-size: 12px; }
.text-muted { color: var(--color-gray-500); }
.badge { display: inline-flex; padding: 1px 8px; border-radius: 10px; font-size: 10px; font-weight: 600; }
.badge-amber { background: #FEF3C7; color: #92400E; }
.badge-green { background: #DCFCE7; color: #15803D; }
.badge-red { background: #FEE2E2; color: #DC2626; }
.actions-cell { text-align: right; white-space: nowrap; }
.btn-action { background: none; border: none; font-size: 11px; cursor: pointer; padding: 3px 8px; font-weight: 600; border-radius: 4px; }
.btn-action.success { color: var(--color-success); }
.btn-action.success:hover { background: #DCFCE7; }
.btn-action.danger { color: var(--color-danger); }
.btn-action.danger:hover { background: #FEE2E2; }
.completed { font-size: 11px; color: var(--color-success); font-weight: 600; }
.rejected { font-size: 11px; color: var(--color-danger); }
.empty { text-align: center; padding: 30px; color: var(--color-gray-400); }
.reject-row { background: #FEF3C7; }
.reject-form { display: flex; align-items: center; gap: 8px; padding: 4px 0; }
.reject-input { flex: 1; padding: 6px 10px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 12px; }
.btn-danger { padding: 4px 10px; border-radius: 4px; font-size: 11px; font-weight: 600; cursor: pointer; border: none; background: var(--color-danger); color: white; }
.btn-ghost { padding: 4px 10px; border-radius: 4px; font-size: 11px; cursor: pointer; background: none; border: 1px solid var(--color-gray-300); color: var(--color-gray-600); }
</style>
