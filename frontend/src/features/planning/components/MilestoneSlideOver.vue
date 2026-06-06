<script setup lang="ts">
/**
 * MilestoneSlideOver — panneau d'édition d'un jalon dans le Gantt projet.
 * Mode lecture par défaut → « Modifier » ; suppression sécurisée (confirmation
 * inline, jamais de confirm() natif). Le backend MilestoneViewSet est la source
 * de vérité (permissions + validation).
 */
import { ref, reactive, watch } from 'vue'
import { planningApi } from '../api/planningApi'

const props = defineProps<{
  open: boolean
  milestoneId: number | null
}>()

const emit = defineEmits<{ close: []; updated: [] }>()

interface Milestone {
  id: number
  title: string
  date: string
  status: string
  color: string
  description: string
}

const STATUS_OPTIONS = [
  { value: 'UPCOMING', label: 'À venir' },
  { value: 'ACHIEVED', label: 'Atteint' },
  { value: 'OVERDUE', label: 'En retard' },
]
function statusLabel(s: string): string {
  return STATUS_OPTIONS.find((o) => o.value === s)?.label || s
}

const milestone = ref<Milestone | null>(null)
const isLoading = ref(false)
const editing = ref(false)
const saving = ref(false)
const confirmingDelete = ref(false)
const error = ref('')

const form = reactive({
  title: '',
  date: '',
  status: 'UPCOMING',
  color: '#3B82F6',
  description: '',
})

async function loadMilestone() {
  if (!props.milestoneId) return
  isLoading.value = true
  error.value = ''
  editing.value = false
  confirmingDelete.value = false
  try {
    const r = await planningApi.getMilestone(props.milestoneId)
    milestone.value = r.data?.data || r.data
  } catch {
    milestone.value = null
    error.value = "Impossible de charger le jalon."
  } finally {
    isLoading.value = false
  }
}

watch(
  () => [props.open, props.milestoneId],
  () => {
    if (props.open && props.milestoneId) loadMilestone()
  },
  { immediate: true },
)

function startEdit() {
  if (!milestone.value) return
  form.title = milestone.value.title
  form.date = milestone.value.date
  form.status = milestone.value.status
  form.color = milestone.value.color || '#3B82F6'
  form.description = milestone.value.description || ''
  error.value = ''
  editing.value = true
}

function cancelEdit() {
  editing.value = false
  error.value = ''
}

async function save() {
  error.value = ''
  if (!form.title.trim()) {
    error.value = 'Le titre est obligatoire.'
    return
  }
  if (!form.date) {
    error.value = 'La date est obligatoire.'
    return
  }
  if (!props.milestoneId) return
  saving.value = true
  try {
    await planningApi.updateMilestone(props.milestoneId, {
      title: form.title.trim(),
      date: form.date,
      status: form.status,
      color: form.color,
      description: form.description,
    })
    await loadMilestone()
    editing.value = false
    emit('updated')
  } catch (e: unknown) {
    error.value = extractError(e)
  } finally {
    saving.value = false
  }
}

async function confirmDelete() {
  if (!props.milestoneId) return
  saving.value = true
  error.value = ''
  try {
    await planningApi.deleteMilestone(props.milestoneId)
    emit('updated')
    emit('close')
  } catch (e: unknown) {
    error.value = extractError(e)
    confirmingDelete.value = false
  } finally {
    saving.value = false
  }
}

function extractError(e: unknown): string {
  const resp = (e as { response?: { data?: Record<string, unknown> } })?.response
  const data = resp?.data
  if (data && typeof data === 'object') {
    const first = Object.values(data)[0]
    if (Array.isArray(first)) return String(first[0])
    if (typeof first === 'string') return first
  }
  return "Échec de l'opération. Réessayez."
}

function frDate(iso: string): string {
  // "YYYY-MM-DD" → "DD/MM/YYYY" (sans souci de fuseau horaire)
  const p = (iso || '').split('-')
  return p.length === 3 ? `${p[2]}/${p[1]}/${p[0]}` : iso
}
</script>

<template>
  <Teleport to="body">
    <div v-if="open" class="pso-overlay" @click.self="emit('close')">
      <div class="pso-panel" data-milestone-panel>
        <div class="pso-header">
          <div>
            <h3 class="pso-title">{{ milestone?.title || 'Jalon' }}</h3>
            <span class="pso-code">Jalon</span>
          </div>
          <button class="pso-close" aria-label="Fermer" @click="emit('close')">&times;</button>
        </div>

        <div v-if="isLoading" class="pso-loading">Chargement…</div>

        <div v-else-if="milestone" class="pso-body">
          <!-- Mode LECTURE -->
          <div v-if="!editing" class="pso-section">
            <div class="ms-read-row">
              <span class="ms-diamond" :style="{ borderBottomColor: milestone.color }"></span>
              <div class="ms-read-main">
                <div class="ms-read-title">{{ milestone.title }}</div>
                <div class="ms-read-meta">
                  {{ frDate(milestone.date) }}
                  &middot; <span class="ms-badge">{{ statusLabel(milestone.status) }}</span>
                </div>
              </div>
            </div>
            <p v-if="milestone.description" class="ms-read-desc">{{ milestone.description }}</p>

            <div class="ms-actions">
              <button class="pso-btn-save" data-edit @click="startEdit">Modifier</button>
            </div>

            <!-- Suppression sécurisée : pas de bouton rouge direct, confirmation inline -->
            <div class="ms-delete">
              <button
                v-if="!confirmingDelete"
                class="ms-delete-trigger"
                data-delete
                @click="confirmingDelete = true"
              >Supprimer…</button>
              <div v-else class="ms-delete-confirm">
                <span>Supprimer ce jalon ?</span>
                <button class="ms-btn-danger" :disabled="saving" data-delete-confirm @click="confirmDelete">Confirmer</button>
                <button class="pso-btn-cancel" :disabled="saving" @click="confirmingDelete = false">Annuler</button>
              </div>
            </div>
          </div>

          <!-- Mode ÉDITION -->
          <div v-else class="pso-section">
            <label class="ms-label">Titre <span class="ms-req">*</span></label>
            <input v-model="form.title" class="pso-input" type="text" data-input-title maxlength="255" />

            <label class="ms-label">Date <span class="ms-req">*</span></label>
            <input v-model="form.date" class="pso-input" type="date" data-input-date />

            <label class="ms-label">Statut</label>
            <select v-model="form.status" class="pso-input" data-input-status>
              <option v-for="o in STATUS_OPTIONS" :key="o.value" :value="o.value">{{ o.label }}</option>
            </select>

            <label class="ms-label">Couleur</label>
            <input v-model="form.color" class="ms-color" type="color" data-input-color />

            <label class="ms-label">Description</label>
            <textarea v-model="form.description" class="pso-input" rows="2" data-input-desc></textarea>

            <p v-if="error" class="ms-error" data-error>{{ error }}</p>

            <div class="ms-actions">
              <button class="pso-btn-save" :disabled="saving" data-save @click="save">Enregistrer</button>
              <button class="pso-btn-cancel" :disabled="saving" @click="cancelEdit">Annuler</button>
            </div>
          </div>

          <p v-if="error && !editing" class="ms-error" data-error>{{ error }}</p>
        </div>

        <div v-else class="pso-loading">{{ error || 'Jalon introuvable.' }}</div>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.pso-overlay { position: fixed; inset: 0; z-index: 9998; background: rgba(0,0,0,0.3); display: flex; justify-content: flex-end; }
.pso-panel { width: 420px; max-width: 90vw; background: white; box-shadow: -4px 0 20px rgba(0,0,0,0.15); display: flex; flex-direction: column; overflow: hidden; }
.pso-header { display: flex; align-items: center; justify-content: space-between; padding: 16px; border-bottom: 1px solid #E5E7EB; }
.pso-title { font-size: 16px; font-weight: 700; color: #111827; margin: 0; }
.pso-code { font-size: 11px; color: #6B7280; }
.pso-close { background: none; border: none; font-size: 24px; color: #9CA3AF; cursor: pointer; padding: 0 4px; }
.pso-close:hover { color: #111827; }
.pso-loading { padding: 40px; text-align: center; color: #9CA3AF; }
.pso-body { flex: 1; overflow-y: auto; }
.pso-section { padding: 16px; }
.pso-input { padding: 6px 8px; border: 1px solid #D1D5DB; border-radius: 4px; font-size: 13px; width: 100%; box-sizing: border-box; margin-bottom: 4px; }
.pso-btn-save { padding: 6px 16px; background: #2563EB; color: white; border: none; border-radius: 4px; font-size: 12px; font-weight: 600; cursor: pointer; }
.pso-btn-save:disabled { opacity: 0.5; }
.pso-btn-cancel { font-size: 12px; color: #6B7280; background: none; border: none; cursor: pointer; padding: 6px 8px; }

.ms-label { display: block; font-size: 11px; font-weight: 600; color: #6B7280; margin: 10px 0 3px; }
.ms-req { color: #DC2626; }
.ms-color { width: 48px; height: 28px; padding: 0; border: 1px solid #D1D5DB; border-radius: 4px; cursor: pointer; }
.ms-error { color: #DC2626; font-size: 12px; margin: 8px 0 0; }

.ms-read-row { display: flex; align-items: flex-start; gap: 10px; }
.ms-diamond { display: inline-block; width: 0; height: 0; border-left: 7px solid transparent; border-right: 7px solid transparent; border-bottom: 12px solid #3B82F6; margin-top: 4px; flex-shrink: 0; }
.ms-read-main { flex: 1; min-width: 0; }
.ms-read-title { font-size: 14px; font-weight: 600; color: #111827; }
.ms-read-meta { font-size: 12px; color: #6B7280; margin-top: 2px; }
.ms-badge { background: #EFF6FF; color: #2563EB; border-radius: 4px; padding: 1px 6px; font-size: 11px; font-weight: 600; }
.ms-read-desc { font-size: 12px; color: #374151; margin: 12px 0 0; white-space: pre-wrap; }

.ms-actions { display: flex; align-items: center; gap: 8px; margin-top: 16px; }
.ms-delete { margin-top: 20px; padding-top: 12px; border-top: 1px solid #F3F4F6; }
.ms-delete-trigger { background: none; border: none; color: #9CA3AF; font-size: 12px; cursor: pointer; padding: 0; }
.ms-delete-trigger:hover { color: #DC2626; text-decoration: underline; }
.ms-delete-confirm { display: flex; align-items: center; gap: 8px; font-size: 12px; color: #374151; }
.ms-btn-danger { background: #DC2626; color: white; border: none; border-radius: 4px; padding: 5px 12px; font-size: 12px; font-weight: 600; cursor: pointer; }
.ms-btn-danger:disabled { opacity: 0.5; }
</style>
