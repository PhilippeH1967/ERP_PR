<script setup lang="ts">
import { ref, watch } from 'vue'

interface Task {
  id: number
  name: string
  wbs_code: string
  client_facing_label: string
  budgeted_hours: string | number
  budgeted_cost?: string | number
  billing_mode: string
  is_billable: boolean
}

interface SavePayload {
  name: string
  wbs_code: string
  client_facing_label: string
  budgeted_hours: string
  budgeted_cost?: string
  billing_mode: string
  is_billable: boolean
}

const props = defineProps<{
  open: boolean
  task: Task | null
  canSeeCosts: boolean
  loading?: boolean
  errorMessage?: string
}>()

const emit = defineEmits<{
  close: []
  save: [SavePayload]
}>()

const form = ref<SavePayload>({
  name: '',
  wbs_code: '',
  client_facing_label: '',
  budgeted_hours: '0',
  budgeted_cost: '0',
  billing_mode: 'FORFAIT',
  is_billable: true,
})
const formError = ref('')

function hydrateFromTask(task: Task | null) {
  if (!task) return
  form.value = {
    name: task.name || '',
    wbs_code: task.wbs_code || '',
    client_facing_label: task.client_facing_label || '',
    budgeted_hours: String(task.budgeted_hours ?? '0'),
    budgeted_cost: String(task.budgeted_cost ?? '0'),
    billing_mode: task.billing_mode || 'FORFAIT',
    is_billable: task.is_billable !== false,
  }
  formError.value = ''
}

watch(() => [props.open, props.task] as const, ([open]) => {
  if (open) hydrateFromTask(props.task)
}, { immediate: true })

function onSave() {
  if (!form.value.name.trim()) {
    formError.value = 'Le nom de la tâche est obligatoire.'
    return
  }
  const payload: SavePayload = {
    ...form.value,
    budgeted_hours: String(form.value.budgeted_hours ?? '0'),
    budgeted_cost: String(form.value.budgeted_cost ?? '0'),
  }
  if (!props.canSeeCosts) delete payload.budgeted_cost
  emit('save', payload)
}
</script>

<template>
  <div v-if="open" class="tem-overlay" @click.self="emit('close')">
    <div class="tem-panel" role="dialog" aria-modal="true">
      <header class="tem-header">
        <h3 class="tem-title">Modifier la tâche</h3>
        <button class="tem-close" aria-label="Fermer" @click="emit('close')">×</button>
      </header>

      <div class="tem-body">
        <div class="tem-grid">
          <div class="tem-field tem-field-full">
            <label>Nom de la tâche *</label>
            <input v-model="form.name" data-tem-name class="tem-input" />
          </div>

          <div class="tem-field">
            <label>Code WBS</label>
            <input v-model="form.wbs_code" data-tem-wbs class="tem-input" placeholder="ex. 3.1.5" />
          </div>

          <div class="tem-field">
            <label>Mode de facturation</label>
            <select v-model="form.billing_mode" data-tem-billing class="tem-input">
              <option value="FORFAIT">Forfait</option>
              <option value="HORAIRE">Horaire</option>
            </select>
          </div>

          <div class="tem-field tem-field-full">
            <label>Libellé client (WBS client, affiché sur factures et rapports)</label>
            <input v-model="form.client_facing_label" data-tem-client-label class="tem-input" placeholder="ex. Phase 1 — Étude de faisabilité" />
          </div>

          <div class="tem-field">
            <label>Heures budgétées</label>
            <input v-model="form.budgeted_hours" data-tem-hours type="number" min="0" step="0.5" class="tem-input" />
          </div>

          <div v-if="canSeeCosts" class="tem-field">
            <label>Coût budgété ($)</label>
            <input v-model="form.budgeted_cost" data-tem-cost type="number" min="0" step="0.01" class="tem-input" />
          </div>

          <div class="tem-field tem-field-full">
            <label class="tem-checkbox">
              <input v-model="form.is_billable" data-tem-billable type="checkbox" />
              Tâche facturable
            </label>
          </div>
        </div>

        <div v-if="formError" data-tem-error class="tem-error">{{ formError }}</div>
        <div v-else-if="errorMessage" class="tem-error">{{ errorMessage }}</div>
      </div>

      <footer class="tem-footer">
        <button data-tem-cancel class="tem-btn" :disabled="loading" @click="emit('close')">
          Annuler
        </button>
        <button data-tem-save class="tem-btn tem-btn-primary" :disabled="loading" @click="onSave">
          {{ loading ? 'Enregistrement…' : 'Enregistrer' }}
        </button>
      </footer>
    </div>
  </div>
</template>

<style scoped>
.tem-overlay { position: fixed; inset: 0; background: rgba(0, 0, 0, 0.45); display: flex; align-items: center; justify-content: center; z-index: 1000; padding: 16px; }
.tem-panel { background: white; border-radius: 8px; max-width: 640px; width: 100%; max-height: 90vh; display: flex; flex-direction: column; box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2); }
.tem-header { display: flex; align-items: center; justify-content: space-between; padding: 14px 18px; border-bottom: 1px solid var(--color-gray-200); }
.tem-title { font-size: 16px; font-weight: 700; color: var(--color-gray-800); margin: 0; }
.tem-close { background: none; border: none; font-size: 22px; color: var(--color-gray-500); cursor: pointer; line-height: 1; }
.tem-body { padding: 18px; overflow-y: auto; }
.tem-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px 16px; }
.tem-field { display: flex; flex-direction: column; gap: 4px; }
.tem-field-full { grid-column: 1 / -1; }
.tem-field label { font-size: 11px; font-weight: 600; color: var(--color-gray-600); text-transform: uppercase; letter-spacing: 0.3px; }
.tem-input { padding: 6px 8px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 13px; }
.tem-input:focus { border-color: var(--color-primary); outline: none; }
.tem-checkbox { display: flex; align-items: center; gap: 8px; font-size: 13px; font-weight: 500; color: var(--color-gray-700); text-transform: none; letter-spacing: 0; cursor: pointer; }
.tem-error { margin-top: 12px; padding: 8px 12px; background: #fef2f2; border: 1px solid #fecaca; border-radius: 4px; color: #b91c1c; font-size: 12px; }
.tem-footer { display: flex; justify-content: flex-end; gap: 8px; padding: 12px 18px; border-top: 1px solid var(--color-gray-200); background: var(--color-gray-50); border-radius: 0 0 8px 8px; }
.tem-btn { padding: 8px 14px; border: 1px solid var(--color-gray-300); background: white; border-radius: 4px; font-size: 13px; font-weight: 600; color: var(--color-gray-700); cursor: pointer; }
.tem-btn:hover:not(:disabled) { background: var(--color-gray-100); }
.tem-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.tem-btn-primary { background: var(--color-primary); border-color: var(--color-primary); color: white; }
.tem-btn-primary:hover:not(:disabled) { filter: brightness(0.95); }
</style>
