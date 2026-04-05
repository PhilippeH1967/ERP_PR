<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useAuth } from '@/shared/composables/useAuth'
import { leaveApi } from '../api/leaveApi'

const { currentUser } = useAuth()
const requests = ref<Array<Record<string, unknown>>>([])
const balances = ref<Array<Record<string, unknown>>>([])
const leaveTypes = ref<Array<Record<string, unknown>>>([])
const isLoading = ref(false)
const showForm = ref(false)
const formError = ref('')
const actionMsg = ref('')

// Form
const form = ref({
  leave_type: null as number | null,
  start_date: '',
  end_date: '',
  total_days: '' as string | number,
  hours_per_day: '8',
  reason: '',
})

const roles = computed(() => currentUser.value?.roles || [])
const canApprove = computed(() => roles.value.some((r: string) => ['ADMIN', 'PM', 'PROJECT_DIRECTOR'].includes(r)))

async function load() {
  isLoading.value = true
  try {
    const [reqResp, balResp, typeResp] = await Promise.all([
      leaveApi.listRequests(),
      leaveApi.myBalances(),
      leaveApi.listTypes(),
    ])
    requests.value = (reqResp.data?.data || reqResp.data?.results || reqResp.data || []) as Array<Record<string, unknown>>
    balances.value = (balResp.data?.data || balResp.data || []) as Array<Record<string, unknown>>
    const tData = typeResp.data?.data || typeResp.data
    leaveTypes.value = (Array.isArray(tData) ? tData : tData?.results || []) as Array<Record<string, unknown>>
  } catch { /* silent */ }
  finally { isLoading.value = false }
}

async function submitRequest() {
  formError.value = ''
  if (!form.value.leave_type || !form.value.start_date || !form.value.end_date || !form.value.total_days) {
    formError.value = 'Tous les champs sont obligatoires'
    return
  }
  try {
    await leaveApi.createRequest({
      leave_type: form.value.leave_type,
      start_date: form.value.start_date,
      end_date: form.value.end_date,
      total_days: Number(form.value.total_days),
      hours_per_day: Number(form.value.hours_per_day),
      reason: form.value.reason,
    })
    showForm.value = false
    form.value = { leave_type: null, start_date: '', end_date: '', total_days: '', hours_per_day: '8', reason: '' }
    await load()
  } catch (e: unknown) {
    formError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur'
  }
}

async function approveRequest(id: number) {
  actionMsg.value = ''
  try {
    await leaveApi.approve(id)
    actionMsg.value = 'Demande approuvée'
    await load()
  } catch (e: unknown) {
    actionMsg.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur'
  }
}

async function rejectRequest(id: number) {
  const reason = prompt('Motif du refus :')
  if (reason === null) return
  try {
    await leaveApi.reject(id, reason)
    await load()
  } catch { /* */ }
}

async function cancelRequest(id: number) {
  try {
    await leaveApi.cancel(id)
    await load()
  } catch { /* */ }
}

onMounted(load)

const statusLabels: Record<string, string> = { PENDING: 'En attente', APPROVED: 'Approuvé', REJECTED: 'Rejeté', CANCELLED: 'Annulé' }
const statusColors: Record<string, string> = { PENDING: 'badge-amber', APPROVED: 'badge-green', REJECTED: 'badge-red', CANCELLED: 'badge-gray' }
</script>

<template>
  <div>
    <div class="mb-6 flex items-center justify-between">
      <h1 class="text-2xl font-semibold text-text">Congés & Absences</h1>
      <button class="rounded-md bg-primary px-4 py-2 text-sm font-medium text-white" @click="showForm = !showForm">
        + Nouvelle demande
      </button>
    </div>

    <div v-if="actionMsg" class="mb-4 rounded bg-success/10 p-3 text-sm" style="color:#15803D;">{{ actionMsg }}</div>

    <!-- Balances -->
    <div v-if="balances.length" class="mb-6 grid grid-cols-4 gap-4">
      <div v-for="b in balances" :key="Number(b.id)" class="kpi-card">
        <div class="kpi-value" :class="Number(b.balance) <= 0 ? 'text-danger' : ''">{{ b.balance }}j</div>
        <div class="kpi-label">{{ b.leave_type_name }}</div>
        <div class="kpi-sub">{{ b.used }}/{{ b.accrued }}j utilisés</div>
      </div>
    </div>

    <!-- Request form -->
    <div v-if="showForm" class="mb-4 rounded-lg border border-primary/20 bg-primary/5 p-4">
      <h3 class="mb-3 text-sm font-semibold">Nouvelle demande de congé</h3>
      <div v-if="formError" class="mb-3 rounded bg-danger/10 p-2 text-sm text-danger">{{ formError }}</div>
      <div class="grid grid-cols-4 gap-3">
        <div>
          <label class="text-xs font-medium text-text-muted">Type *</label>
          <select v-model="form.leave_type" class="mt-1 block w-full rounded border border-border px-2 py-1.5 text-sm">
            <option :value="null">— Choisir —</option>
            <option v-for="t in leaveTypes" :key="Number(t.id)" :value="t.id">{{ t.name }}</option>
          </select>
        </div>
        <div>
          <label class="text-xs font-medium text-text-muted">Du *</label>
          <input v-model="form.start_date" type="date" class="mt-1 block w-full rounded border border-border px-2 py-1.5 text-sm" />
        </div>
        <div>
          <label class="text-xs font-medium text-text-muted">Au *</label>
          <input v-model="form.end_date" type="date" class="mt-1 block w-full rounded border border-border px-2 py-1.5 text-sm" />
        </div>
        <div>
          <label class="text-xs font-medium text-text-muted">Jours *</label>
          <input v-model="form.total_days" type="number" step="0.5" min="0.5" class="mt-1 block w-full rounded border border-border px-2 py-1.5 text-sm font-mono" placeholder="5" />
        </div>
      </div>
      <div class="mt-3">
        <label class="text-xs font-medium text-text-muted">Motif</label>
        <input v-model="form.reason" type="text" class="mt-1 block w-full rounded border border-border px-2 py-1.5 text-sm" placeholder="Optionnel" />
      </div>
      <div class="mt-3 flex justify-end gap-2">
        <button class="rounded px-3 py-1.5 text-sm text-text-muted hover:bg-surface-alt" @click="showForm = false">Annuler</button>
        <button class="rounded bg-primary px-4 py-1.5 text-sm font-medium text-white" @click="submitRequest">Soumettre</button>
      </div>
    </div>

    <!-- Requests table -->
    <div v-if="isLoading" class="py-8 text-center text-text-muted">Chargement...</div>
    <div v-else-if="!requests.length" class="rounded-lg border border-border bg-surface p-8 text-center text-text-muted">
      Aucune demande de congé
    </div>
    <div v-else class="rounded-lg border border-border bg-surface">
      <table class="w-full text-left text-sm">
        <thead class="border-b border-border text-xs font-medium uppercase tracking-wide text-text-muted">
          <tr>
            <th class="px-4 py-3">Employé</th>
            <th class="px-4 py-3">Type</th>
            <th class="px-4 py-3">Période</th>
            <th class="px-4 py-3 text-right">Jours</th>
            <th class="px-4 py-3">Statut</th>
            <th class="px-4 py-3">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in requests" :key="Number(r.id)" class="border-b border-border last:border-0">
            <td class="px-4 py-3 font-medium">{{ r.employee_name }}</td>
            <td class="px-4 py-3">{{ r.leave_type_name }}</td>
            <td class="px-4 py-3 text-text-muted">{{ r.start_date }} → {{ r.end_date }}</td>
            <td class="px-4 py-3 text-right font-mono">{{ r.total_days }}</td>
            <td class="px-4 py-3">
              <span class="badge" :class="statusColors[String(r.status)] || 'badge-gray'">{{ statusLabels[String(r.status)] || r.status }}</span>
            </td>
            <td class="px-4 py-3">
              <template v-if="r.status === 'PENDING'">
                <template v-if="canApprove && Number(r.employee) !== currentUser?.id">
                  <button class="action-btn text-success" @click="approveRequest(Number(r.id))">Approuver</button>
                  <button class="action-btn text-danger" @click="rejectRequest(Number(r.id))">Refuser</button>
                </template>
                <button v-if="Number(r.employee) === currentUser?.id" class="action-btn text-text-muted" @click="cancelRequest(Number(r.id))">Annuler</button>
              </template>
              <span v-else-if="r.status === 'APPROVED' && r.approved_by_name" class="text-xs text-text-muted">par {{ r.approved_by_name }}</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.badge { display: inline-flex; padding: 2px 10px; border-radius: 10px; font-size: 10px; font-weight: 600; }
.badge-green { background: #DCFCE7; color: #15803D; }
.badge-amber { background: #FEF3C7; color: #92400E; }
.badge-red { background: #FEE2E2; color: #DC2626; }
.badge-gray { background: var(--color-gray-100); color: var(--color-gray-500); }
.kpi-card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 14px; text-align: center; }
.kpi-value { font-size: 24px; font-weight: 700; color: var(--color-gray-900); }
.kpi-label { font-size: 11px; color: var(--color-gray-500); text-transform: uppercase; font-weight: 600; margin-top: 2px; }
.kpi-sub { font-size: 10px; color: var(--color-gray-400); margin-top: 2px; }
.text-danger { color: #DC2626; }
.text-success { color: #15803D; }
.action-btn { background: none; border: none; font-size: 11px; font-weight: 600; cursor: pointer; padding: 2px 6px; }
.action-btn:hover { text-decoration: underline; }
</style>
