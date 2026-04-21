<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import apiClient from '@/plugins/axios'

const isSubmitting = ref(false)
const success = ref('')
const error = ref('')

// Form
const form = ref({
  project_id: null as number | null,
  transfer_type: 'pm' as 'pm' | 'associate',
  new_responsible: null as number | null,
  reason: '',
  effective_date: new Date().toISOString().slice(0, 10),
})

// Lookups
interface ProjectOption { id: number; code: string; name: string; pm: number | null; associate_in_charge: number | null }
interface UserOption { id: number; username: string; email: string }
const projects = ref<ProjectOption[]>([])
const allUsers = ref<UserOption[]>([])

// Transfer history
interface TransferRecord { id: number; project_code: string; project_name: string; transfer_type: string; from_user: string; to_user: string; reason: string; date: string }
const history = ref<TransferRecord[]>([])

const selectedProject = computed(() => projects.value.find(p => p.id === form.value.project_id))
const currentResponsible = computed(() => {
  if (!selectedProject.value) return '—'
  const userId = form.value.transfer_type === 'pm'
    ? selectedProject.value.pm
    : selectedProject.value.associate_in_charge
  const user = allUsers.value.find(u => u.id === userId)
  return user ? `${user.username} (${user.email})` : '—'
})

async function loadData() {
  try {
    const [pResp, uResp] = await Promise.all([
      apiClient.get('projects/'),
      apiClient.get('users/search/'),
    ])
    const pData = pResp.data?.data || pResp.data
    projects.value = Array.isArray(pData) ? pData : pData?.results || []
    const uData = uResp.data?.data || uResp.data
    allUsers.value = Array.isArray(uData) ? uData : []
  } catch { /* silent */ }
}

async function onSubmit() {
  error.value = ''
  success.value = ''
  if (!form.value.project_id) { error.value = 'Sélectionnez un projet'; return }
  if (!form.value.new_responsible) { error.value = 'Sélectionnez le nouveau responsable'; return }

  isSubmitting.value = true
  try {
    const field = form.value.transfer_type === 'pm' ? 'pm' : 'associate_in_charge'
    await apiClient.patch(`projects/${form.value.project_id}/`, {
      [field]: form.value.new_responsible,
    })

    // Add to local history
    const proj = selectedProject.value
    const newUser = allUsers.value.find(u => u.id === form.value.new_responsible)
    history.value.unshift({
      id: Date.now(),
      project_code: proj?.code || '',
      project_name: proj?.name || '',
      transfer_type: form.value.transfer_type === 'pm' ? 'Chef de projet' : 'Associé en charge',
      from_user: currentResponsible.value,
      to_user: newUser ? `${newUser.username} (${newUser.email})` : '—',
      reason: form.value.reason,
      date: form.value.effective_date,
    })

    success.value = `Transfert effectué — ${form.value.transfer_type === 'pm' ? 'Chef de projet' : 'Associé en charge'} mis à jour`
    // Reload projects to reflect change
    await loadData()
    form.value.reason = ''
    form.value.new_responsible = null
  } catch (e: unknown) {
    error.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur lors du transfert'
  } finally {
    isSubmitting.value = false
  }
}

onMounted(loadData)
</script>

<template>
  <div class="mx-auto max-w-3xl">
    <h1 class="mb-6 text-2xl font-semibold text-text">Transfert de responsable</h1>

    <div v-if="error" class="mb-4 rounded bg-danger/10 p-3 text-sm text-danger">{{ error }}</div>
    <div v-if="success" class="mb-4 rounded bg-success/10 p-3 text-sm" style="color:#15803D;">{{ success }}</div>

    <form class="section-card" @submit.prevent="onSubmit">
      <h2 class="section-title">Nouveau transfert</h2>
      <div class="grid grid-cols-2 gap-4">
        <div class="col-span-2">
          <label class="field-label">Projet *</label>
          <select v-model="form.project_id" class="field-input">
            <option :value="null">— Sélectionner un projet —</option>
            <option v-for="p in projects" :key="p.id" :value="p.id">{{ p.code }} — {{ p.name }}</option>
          </select>
        </div>
        <div>
          <label class="field-label">Type de transfert</label>
          <select v-model="form.transfer_type" class="field-input">
            <option value="pm">Chef de projet (PM)</option>
            <option value="associate">Associé en charge</option>
          </select>
        </div>
        <div>
          <label class="field-label">Responsable actuel</label>
          <div class="current-responsible">{{ currentResponsible }}</div>
        </div>
        <div>
          <label class="field-label">Nouveau responsable *</label>
          <select v-model="form.new_responsible" class="field-input">
            <option :value="null">— Sélectionner —</option>
            <option v-for="u in allUsers" :key="u.id" :value="u.id">{{ u.username }} ({{ u.email }})</option>
          </select>
        </div>
        <div>
          <label class="field-label">Date effective</label>
          <input v-model="form.effective_date" type="date" class="field-input" />
        </div>
        <div class="col-span-2">
          <label class="field-label">Motif du transfert</label>
          <textarea v-model="form.reason" rows="2" class="field-input" placeholder="Raison du changement..."></textarea>
        </div>
      </div>
      <div class="mt-4 flex justify-end">
        <button type="submit" class="rounded-md bg-primary px-6 py-2 text-sm font-medium text-white disabled:opacity-50" :disabled="isSubmitting">
          {{ isSubmitting ? 'Transfert...' : 'Effectuer le transfert' }}
        </button>
      </div>
    </form>

    <!-- Historique -->
    <div class="section-card" style="margin-top:16px;">
      <h2 class="section-title">Historique des transferts</h2>
      <div v-if="!history.length" class="py-6 text-center text-sm text-text-muted">
        Aucun transfert enregistré dans cette session.<br>
        <span style="font-size:11px;">L'historique complet sera disponible via l'audit trail (admin).</span>
      </div>
      <table v-else class="w-full text-sm">
        <thead class="text-xs text-text-muted">
          <tr>
            <th class="px-3 py-2 text-left">Date</th>
            <th class="px-3 py-2 text-left">Projet</th>
            <th class="px-3 py-2 text-left">Type</th>
            <th class="px-3 py-2 text-left">De</th>
            <th class="px-3 py-2 text-left">Vers</th>
            <th class="px-3 py-2 text-left">Motif</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="h in history" :key="h.id" class="border-t border-border">
            <td class="px-3 py-2">{{ h.date }}</td>
            <td class="px-3 py-2 font-medium">{{ h.project_code }}</td>
            <td class="px-3 py-2">{{ h.transfer_type }}</td>
            <td class="px-3 py-2 text-text-muted">{{ h.from_user }}</td>
            <td class="px-3 py-2 font-medium">{{ h.to_user }}</td>
            <td class="px-3 py-2 text-text-muted">{{ h.reason || '—' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.section-card { background: white; border: 1px solid var(--color-gray-200); border-radius: 8px; padding: 20px; }
.section-title { font-size: 15px; font-weight: 600; color: var(--color-gray-800); margin-bottom: 16px; }
.field-label { display: block; font-size: 12px; font-weight: 600; color: var(--color-gray-600); margin-bottom: 4px; }
.field-input { width: 100%; padding: 8px 12px; border: 1px solid var(--color-gray-300); border-radius: 6px; font-size: 14px; }
.field-input:focus { outline: none; border-color: var(--color-primary); box-shadow: 0 0 0 2px rgba(59,130,246,0.15); }
.current-responsible { padding: 8px 12px; background: var(--color-gray-50); border-radius: 6px; font-size: 13px; font-weight: 600; color: var(--color-gray-700); }
</style>
