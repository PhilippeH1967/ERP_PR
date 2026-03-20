<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import BaseModal from '@/shared/components/BaseModal.vue'
import { projectApi } from '../api/projectApi'
import apiClient from '@/plugins/axios'

const props = defineProps<{
  open: boolean
  projectId: number
  phaseId: number | null
  phaseName: string
}>()

const emit = defineEmits<{
  close: []
  assigned: []
}>()

const isSubmitting = ref(false)
const error = ref('')

const form = ref({
  employee: null as number | null,
  percentage: 100,
  start_date: '',
  end_date: '',
})

// User search
interface UserOption { id: number; username: string; email: string }
const allUsers = ref<UserOption[]>([])
const userSearch = ref('')
const selectedUser = ref<UserOption | null>(null)

const filteredUsers = computed(() => {
  const q = userSearch.value.toLowerCase()
  if (!q) return allUsers.value.slice(0, 10)
  return allUsers.value
    .filter(u => u.username.toLowerCase().includes(q) || u.email.toLowerCase().includes(q))
    .slice(0, 10)
})

function selectUser(user: UserOption) {
  selectedUser.value = user
  userSearch.value = user.username
  form.value.employee = user.id
}

function clearUser() {
  selectedUser.value = null
  userSearch.value = ''
  form.value.employee = null
}

// Phase names lookup
interface PhaseOption { id: number; name: string }
const phases = ref<PhaseOption[]>([])

const resolvedPhaseName = computed(() => {
  if (props.phaseName) return props.phaseName
  if (props.phaseId) {
    const phase = phases.value.find(p => p.id === props.phaseId)
    return phase ? phase.name : `Phase #${props.phaseId}`
  }
  return 'Global'
})

// Load users and phases when modal opens
watch(() => props.open, async (isOpen) => {
  if (isOpen) {
    // Reset form
    form.value = { employee: null, percentage: 100, start_date: '', end_date: '' }
    selectedUser.value = null
    userSearch.value = ''
    error.value = ''

    try {
      const [uResp, pResp] = await Promise.all([
        apiClient.get('users/search/', { params: { q: '' } }),
        projectApi.listPhases(props.projectId),
      ])
      const uData = uResp.data?.data || uResp.data
      allUsers.value = Array.isArray(uData) ? uData : uData?.results || []
      const pData = pResp.data?.data || pResp.data
      phases.value = Array.isArray(pData) ? pData : pData?.results || []
    } catch { /* silent */ }
  }
})

async function onSubmit() {
  if (!form.value.employee) {
    error.value = 'Sélectionnez un employé'
    return
  }
  error.value = ''
  isSubmitting.value = true
  try {
    await projectApi.createAssignment(props.projectId, {
      employee: Number(form.value.employee),
      phase: props.phaseId,
      percentage: form.value.percentage,
      start_date: form.value.start_date || null,
      end_date: form.value.end_date || null,
    })
    emit('assigned')
    emit('close')
  } catch {
    error.value = "Erreur lors de l'affectation"
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <BaseModal
    :open="open"
    :title="`Affecter — ${resolvedPhaseName}`"
    @close="emit('close')"
  >
    <form
      class="space-y-4"
      @submit.prevent="onSubmit"
    >
      <div
        v-if="error"
        class="rounded bg-danger/10 p-2 text-sm text-danger"
      >
        {{ error }}
      </div>

      <div>
        <label class="text-xs font-medium text-text-muted">Employé *</label>
        <div class="relative mt-1">
          <template v-if="!selectedUser">
            <input
              v-model="userSearch"
              type="text"
              class="w-full rounded-md border border-border px-3 py-2 text-sm"
              placeholder="Rechercher par nom ou email..."
            >
            <div v-if="filteredUsers.length || userSearch" class="absolute left-0 right-0 top-full z-50 mt-1 max-h-48 overflow-y-auto rounded-md border border-border bg-white shadow-lg">
              <div
                v-for="u in filteredUsers"
                :key="u.id"
                class="cursor-pointer px-3 py-2 text-sm hover:bg-primary/10"
                @click="selectUser(u)"
              >
                <span class="font-medium">{{ u.username }}</span>
                <span class="ml-2 text-xs text-text-muted">{{ u.email }}</span>
              </div>
              <div v-if="userSearch && !filteredUsers.length" class="px-3 py-2 text-center text-xs text-text-muted">Aucun utilisateur trouvé</div>
            </div>
          </template>
          <div v-else class="flex items-center justify-between rounded-md bg-primary/10 px-3 py-2 text-sm font-medium text-primary">
            <span>{{ selectedUser.username }} <span class="text-xs font-normal text-text-muted">({{ selectedUser.email }})</span></span>
            <button type="button" class="ml-2 text-base font-bold hover:text-danger" @click="clearUser">&times;</button>
          </div>
        </div>
      </div>

      <div>
        <label class="text-xs font-medium text-text-muted">Pourcentage d'affectation</label>
        <div class="mt-1 flex items-center gap-2">
          <input
            v-model="form.percentage"
            type="range"
            min="0"
            max="100"
            step="5"
            class="flex-1"
          >
          <span class="w-12 text-right font-mono text-sm font-medium">{{ form.percentage }}%</span>
        </div>
      </div>

      <div class="grid grid-cols-2 gap-3">
        <div>
          <label class="text-xs font-medium text-text-muted">Date début</label>
          <input
            v-model="form.start_date"
            type="date"
            class="mt-1 w-full rounded-md border border-border px-3 py-2 text-sm"
          >
        </div>
        <div>
          <label class="text-xs font-medium text-text-muted">Date fin</label>
          <input
            v-model="form.end_date"
            type="date"
            class="mt-1 w-full rounded-md border border-border px-3 py-2 text-sm"
          >
        </div>
      </div>
    </form>

    <template #actions>
      <button
        class="rounded-md px-4 py-2 text-sm text-text-muted hover:bg-surface-alt"
        @click="emit('close')"
      >
        Annuler
      </button>
      <button
        class="rounded-md bg-primary px-4 py-2 text-sm font-medium text-white disabled:opacity-50"
        :disabled="isSubmitting"
        @click="onSubmit"
      >
        Affecter
      </button>
    </template>
  </BaseModal>
</template>
