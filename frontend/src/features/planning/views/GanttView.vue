<script setup lang="ts">
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import GanttChart from '../components/GanttChart.vue'
import { planningApi } from '../api/planningApi'

const route = useRoute()
const projectId = Number(route.params.projectId || route.query.project || 0)

const showMilestoneForm = ref(false)
const milestoneForm = ref({
  name: '',
  date: '',
  color: '#2563EB',
  description: '',
})
const isCreating = ref(false)
const error = ref('')
const ganttRefresh = ref(0)

function openCreateMilestone() {
  milestoneForm.value = {
    name: '',
    date: new Date().toISOString().slice(0, 10),
    color: '#2563EB',
    description: '',
  }
  error.value = ''
  showMilestoneForm.value = true
}

async function createMilestone() {
  error.value = ''
  if (!milestoneForm.value.name.trim() || !milestoneForm.value.date) {
    error.value = 'Nom et date sont obligatoires.'
    return
  }
  isCreating.value = true
  try {
    await planningApi.createMilestone({
      project: projectId,
      name: milestoneForm.value.name.trim(),
      date: milestoneForm.value.date,
      color: milestoneForm.value.color,
      description: milestoneForm.value.description,
    })
    showMilestoneForm.value = false
    ganttRefresh.value++  // force GanttChart to reload
  } catch (e: unknown) {
    const data = (e as { response?: { data?: unknown } }).response?.data
    const obj = (data as Record<string, unknown>) || {}
    const errObj = obj.error as { message?: string } | undefined
    if (errObj?.message) error.value = errObj.message
    else {
      const parts: string[] = []
      for (const [field, val] of Object.entries(obj)) {
        if (Array.isArray(val)) parts.push(`${field}: ${val.join(', ')}`)
      }
      error.value = parts.length ? parts.join(' · ') : 'Erreur lors de la création'
    }
  } finally {
    isCreating.value = false
  }
}
</script>

<template>
  <div>
    <div class="mb-6 flex items-center justify-between">
      <h1 class="text-2xl font-semibold text-text">Gantt projet</h1>
      <button
        v-if="projectId"
        class="btn-primary"
        data-add-milestone
        @click="openCreateMilestone"
      >
        + Jalon
      </button>
    </div>

    <div v-if="!projectId" class="rounded-lg border border-border bg-surface p-8 text-center text-text-muted">
      Sélectionnez un projet pour afficher le diagramme de Gantt
    </div>
    <GanttChart v-else :key="ganttRefresh" :project-id="projectId" />

    <!-- Milestone creation modal -->
    <div v-if="showMilestoneForm" class="modal-overlay" @click.self="showMilestoneForm = false">
      <div class="modal-panel" role="dialog" aria-modal="true">
        <header class="modal-header">
          <h3 class="modal-title">Nouveau jalon</h3>
          <button class="modal-close" aria-label="Fermer" @click="showMilestoneForm = false">×</button>
        </header>
        <div class="modal-body">
          <div class="form-grid">
            <div class="form-group">
              <label>Nom *</label>
              <input
                v-model="milestoneForm.name"
                data-milestone-name
                placeholder="ex. Livraison concept"
              />
            </div>
            <div class="form-group">
              <label>Date *</label>
              <input
                v-model="milestoneForm.date"
                type="date"
                data-milestone-date
              />
            </div>
            <div class="form-group">
              <label>Couleur</label>
              <input
                v-model="milestoneForm.color"
                type="color"
                style="height: 36px;"
              />
            </div>
            <div class="form-group form-group-full">
              <label>Description (optionnelle)</label>
              <textarea
                v-model="milestoneForm.description"
                rows="2"
                placeholder="Notes complémentaires…"
              />
            </div>
          </div>
          <div v-if="error" class="form-error">{{ error }}</div>
        </div>
        <footer class="modal-footer">
          <button class="btn-ghost" :disabled="isCreating" @click="showMilestoneForm = false">Annuler</button>
          <button class="btn-primary" data-create-milestone :disabled="isCreating" @click="createMilestone">
            {{ isCreating ? 'Création…' : 'Créer le jalon' }}
          </button>
        </footer>
      </div>
    </div>
  </div>
</template>

<style scoped>
.btn-primary { background: var(--color-primary); color: white; border: none; padding: 6px 14px; border-radius: 4px; font-size: 13px; font-weight: 600; cursor: pointer; }
.btn-primary:hover:not(:disabled) { filter: brightness(0.95); }
.btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-ghost { background: none; border: 1px solid var(--color-gray-300); color: var(--color-gray-700); padding: 6px 14px; border-radius: 4px; font-size: 13px; cursor: pointer; }

.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.45); display: flex; align-items: center; justify-content: center; z-index: 1000; padding: 16px; }
.modal-panel { background: white; border-radius: 8px; max-width: 520px; width: 100%; max-height: 90vh; display: flex; flex-direction: column; box-shadow: 0 10px 40px rgba(0,0,0,0.2); }
.modal-header { display: flex; justify-content: space-between; padding: 14px 18px; border-bottom: 1px solid var(--color-gray-200); }
.modal-title { font-size: 16px; font-weight: 700; color: var(--color-gray-800); margin: 0; }
.modal-close { background: none; border: none; font-size: 22px; color: var(--color-gray-500); cursor: pointer; line-height: 1; }
.modal-body { padding: 18px; overflow-y: auto; }
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.form-group { display: flex; flex-direction: column; gap: 4px; }
.form-group-full { grid-column: 1 / -1; }
.form-group label { font-size: 11px; font-weight: 600; color: var(--color-gray-600); text-transform: uppercase; letter-spacing: 0.3px; }
.form-group input, .form-group textarea { padding: 6px 10px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 13px; }
.form-error { margin-top: 12px; padding: 8px 12px; background: #FEE2E2; color: #B91C1C; border-radius: 4px; font-size: 12px; }
.modal-footer { display: flex; justify-content: flex-end; gap: 8px; padding: 12px 18px; border-top: 1px solid var(--color-gray-200); background: var(--color-gray-50); border-radius: 0 0 8px 8px; }
</style>
