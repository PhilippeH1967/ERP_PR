<script setup lang="ts">
import { ref } from 'vue'
import BaseModal from '@/shared/components/BaseModal.vue'
import { projectApi } from '../api/projectApi'

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
  employee: '' as string | number,
  percentage: 100,
  start_date: '',
  end_date: '',
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
    form.value = { employee: '', percentage: 100, start_date: '', end_date: '' }
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
    :title="`Affecter — ${phaseName}`"
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
        <label class="text-xs font-medium text-text-muted">ID Employé *</label>
        <input
          v-model="form.employee"
          type="number"
          class="mt-1 w-full rounded-md border border-border px-3 py-2 text-sm"
          placeholder="ID de l'employé"
        >
        <p class="mt-1 text-[10px] text-text-muted">
          La recherche par nom sera disponible quand le module Employés sera complet
        </p>
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
