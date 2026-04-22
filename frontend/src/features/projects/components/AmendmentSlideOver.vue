<script setup lang="ts">
/**
 * AmendmentSlideOver — contract amendment editor panel.
 * Opens for create (amendmentId=null) or edit (amendmentId=N).
 * Covers description, scope (phases + tasks), budget impact, and
 * status transitions (submit/approve/reject) respecting user role.
 */
import { ref, computed, watch, nextTick } from 'vue'
import { projectApi } from '../api/projectApi'
import Stepper from '@/shared/components/Stepper.vue'

const STEPPER_STEPS = [
  { key: 'DRAFT', label: 'Brouillon' },
  { key: 'SUBMITTED', label: 'Soumis' },
  { key: 'APPROVED', label: 'Approuvé' },
]

interface PhaseOption { id: number; name: string }
interface ScopePhase { id: number; name: string; client_facing_label: string; budgeted_hours: string; budgeted_cost: string }
interface ScopeTask { id: number; wbs_code: string; name: string; phase: number; phase_name?: string; budgeted_hours: string }
interface Amendment {
  id: number
  amendment_number: number
  description: string
  status: 'DRAFT' | 'SUBMITTED' | 'APPROVED' | 'REJECTED'
  budget_impact: string
  created_at: string
}

const props = defineProps<{
  open: boolean
  projectId: number
  amendmentId: number | null
  canApprove: boolean
  phases: PhaseOption[]
}>()

const emit = defineEmits<{ close: []; saved: [] }>()

const loading = ref(false)
const saving = ref(false)
const errorMsg = ref('')

// Form state
const description = ref('')
const amendmentNumber = ref<number | null>(null)
const status = ref<Amendment['status']>('DRAFT')
const createdAt = ref('')

// Budget: auto vs override
const budgetImpactRaw = ref('0')
const overrideBudget = ref(false)

// Scope
const scope = ref<{ phases: ScopePhase[]; tasks: ScopeTask[] }>({ phases: [], tasks: [] })
const scopeLoading = ref(false)
const newPhase = ref({ name: '', client_facing_label: '', budgeted_hours: '0' })
const newTask = ref<{ phase: number | null; name: string; budgeted_hours: string }>({ phase: null, name: '', budgeted_hours: '0' })
const showPhaseForm = ref(false)
const showTaskForm = ref(false)

// Rejection
const rejectMode = ref(false)
const rejectReason = ref('')

// Dirty tracking for close confirmation
const descriptionSnapshot = ref('')
const budgetSnapshot = ref('0')
const isDirty = computed(() =>
  description.value !== descriptionSnapshot.value ||
  (overrideBudget.value && budgetImpactRaw.value !== budgetSnapshot.value)
)
const showDirtyBanner = ref(false)

const isCreate = computed(() => props.amendmentId === null)
const isLocked = computed(() => status.value === 'APPROVED' || status.value === 'REJECTED')

const autoBudgetImpact = computed(() => {
  // Somme heures × taux par défaut (on utilise budgeted_cost comme proxy si disponible, sinon budgeted_hours × 0)
  const phasesSum = scope.value.phases.reduce((s, p) => s + Number(p.budgeted_cost || 0), 0)
  // Pour les tâches, budgeted_hours × hourly_rate n'est pas exposé ici, on utilise 0 par défaut — l'utilisateur peut override
  return phasesSum
})

const displayedBudgetImpact = computed(() =>
  overrideBudget.value ? Number(budgetImpactRaw.value || 0) : autoBudgetImpact.value,
)

const currentStepperKey = computed(() => {
  if (status.value === 'REJECTED') return 'SUBMITTED'
  if (status.value === 'DRAFT') return 'DRAFT'
  if (status.value === 'SUBMITTED') return 'SUBMITTED'
  return 'APPROVED'
})

const rejectedKey = computed(() => (status.value === 'REJECTED' ? 'APPROVED' : null))

function resetState() {
  description.value = ''
  amendmentNumber.value = null
  status.value = 'DRAFT'
  createdAt.value = ''
  budgetImpactRaw.value = '0'
  overrideBudget.value = false
  scope.value = { phases: [], tasks: [] }
  newPhase.value = { name: '', client_facing_label: '', budgeted_hours: '0' }
  newTask.value = { phase: null, name: '', budgeted_hours: '0' }
  showPhaseForm.value = false
  showTaskForm.value = false
  rejectMode.value = false
  rejectReason.value = ''
  errorMsg.value = ''
  showDirtyBanner.value = false
  descriptionSnapshot.value = ''
  budgetSnapshot.value = '0'
}

async function loadAmendment() {
  if (!props.amendmentId) return
  loading.value = true
  errorMsg.value = ''
  try {
    const r = await projectApi.listAmendments(props.projectId)
    const list: Amendment[] = r.data?.data || r.data || []
    const am = list.find(a => a.id === props.amendmentId)
    if (!am) throw new Error('Avenant introuvable')
    description.value = am.description
    amendmentNumber.value = am.amendment_number
    status.value = am.status
    createdAt.value = am.created_at
    budgetImpactRaw.value = String(am.budget_impact || '0')
    descriptionSnapshot.value = description.value
    budgetSnapshot.value = budgetImpactRaw.value
  } catch (e: unknown) {
    errorMsg.value = extractError(e, 'Chargement impossible')
  } finally {
    loading.value = false
  }
}

async function loadScope() {
  if (!props.amendmentId) return
  scopeLoading.value = true
  try {
    const r = await projectApi.amendmentScope(props.projectId, props.amendmentId)
    const d = r.data?.data || r.data
    scope.value = { phases: d?.phases || [], tasks: d?.tasks || [] }
    // Si override non activé et budget manuel différent de auto-calc, activer override
    if (!overrideBudget.value && Number(budgetImpactRaw.value) !== autoBudgetImpact.value && Number(budgetImpactRaw.value) !== 0) {
      overrideBudget.value = true
    }
  } catch {
    scope.value = { phases: [], tasks: [] }
  } finally {
    scopeLoading.value = false
  }
}

function extractError(e: unknown, fallback: string): string {
  const err = e as { response?: { data?: { error?: { message?: string }; detail?: string } }; message?: string }
  return err.response?.data?.error?.message || err.response?.data?.detail || err.message || fallback
}

watch(() => [props.open, props.amendmentId], async ([openNow, amId]) => {
  if (openNow) {
    resetState()
    if (amId) {
      await loadAmendment()
      await loadScope()
    }
    // Auto-focus description
    await nextTick()
    ;(document.querySelector('.aso-description-input') as HTMLTextAreaElement | null)?.focus()
  }
}, { immediate: true })

// Actions — Create / Save
async function save() {
  if (!description.value.trim()) {
    errorMsg.value = 'La description est obligatoire'
    return
  }
  saving.value = true
  errorMsg.value = ''
  try {
    const payload: Record<string, unknown> = {
      description: description.value.trim(),
      budget_impact: overrideBudget.value ? Number(budgetImpactRaw.value || 0) : autoBudgetImpact.value,
    }
    if (isCreate.value) {
      payload.status = 'DRAFT'
      const r = await projectApi.createAmendment(props.projectId, payload)
      const created: Amendment = r.data?.data || r.data
      amendmentNumber.value = created.amendment_number
      status.value = created.status
      createdAt.value = created.created_at
      // Update snapshots
      descriptionSnapshot.value = description.value
      budgetSnapshot.value = budgetImpactRaw.value
      emit('saved')
      // Switch to edit mode: reload scope (empty for new amendment, but consistent)
      // Note: parent will re-pass amendmentId via prop on next open — for this session we keep working on created.id
      // We need to update internal id reference. Easiest: emit saved and let parent re-open with real id.
      emit('close')
    } else {
      await projectApi.updateAmendment(props.projectId, props.amendmentId as number, payload)
      descriptionSnapshot.value = description.value
      budgetSnapshot.value = budgetImpactRaw.value
      emit('saved')
    }
  } catch (e) {
    errorMsg.value = extractError(e, 'Erreur enregistrement')
  } finally {
    saving.value = false
  }
}

async function submitForApproval() {
  if (!props.amendmentId) return
  saving.value = true
  errorMsg.value = ''
  try {
    if (isDirty.value) {
      await projectApi.updateAmendment(props.projectId, props.amendmentId, {
        description: description.value.trim(),
        budget_impact: overrideBudget.value ? Number(budgetImpactRaw.value || 0) : autoBudgetImpact.value,
      })
    }
    await projectApi.submitAmendment(props.projectId, props.amendmentId)
    status.value = 'SUBMITTED'
    emit('saved')
  } catch (e) {
    errorMsg.value = extractError(e, 'Erreur soumission')
  } finally {
    saving.value = false
  }
}

async function approve() {
  if (!props.amendmentId) return
  saving.value = true
  errorMsg.value = ''
  try {
    await projectApi.approveAmendment(props.projectId, props.amendmentId)
    status.value = 'APPROVED'
    emit('saved')
  } catch (e) {
    errorMsg.value = extractError(e, 'Erreur validation')
  } finally {
    saving.value = false
  }
}

async function confirmReject() {
  if (!props.amendmentId) return
  if (!rejectReason.value.trim()) {
    errorMsg.value = 'Motif de rejet obligatoire'
    return
  }
  saving.value = true
  errorMsg.value = ''
  try {
    await projectApi.rejectAmendment(props.projectId, props.amendmentId, rejectReason.value.trim())
    status.value = 'REJECTED'
    rejectMode.value = false
    rejectReason.value = ''
    emit('saved')
    // Reload to get updated description with rejection note
    await loadAmendment()
  } catch (e) {
    errorMsg.value = extractError(e, 'Erreur rejet')
  } finally {
    saving.value = false
  }
}

// Scope actions
async function addPhase() {
  if (!props.amendmentId || !newPhase.value.name.trim()) {
    errorMsg.value = 'Nom de phase obligatoire'
    return
  }
  saving.value = true
  errorMsg.value = ''
  try {
    await projectApi.createPhase(props.projectId, {
      name: newPhase.value.name.trim(),
      client_facing_label: newPhase.value.client_facing_label.trim(),
      budgeted_hours: newPhase.value.budgeted_hours || '0',
      amendment: props.amendmentId,
      billing_mode: 'FORFAIT',
      phase_type: 'REALIZATION',
    })
    newPhase.value = { name: '', client_facing_label: '', budgeted_hours: '0' }
    showPhaseForm.value = false
    await loadScope()
    emit('saved')
  } catch (e) {
    errorMsg.value = extractError(e, 'Erreur création phase')
  } finally {
    saving.value = false
  }
}

async function addTask() {
  if (!props.amendmentId || !newTask.value.phase || !newTask.value.name.trim()) {
    errorMsg.value = 'Phase et nom de tâche obligatoires'
    return
  }
  saving.value = true
  errorMsg.value = ''
  try {
    await projectApi.createTask(props.projectId, {
      phase: newTask.value.phase,
      name: newTask.value.name.trim(),
      budgeted_hours: Number(newTask.value.budgeted_hours || 0),
      amendment: props.amendmentId,
      task_type: 'TASK',
      billing_mode: 'FORFAIT',
    })
    newTask.value = { phase: null, name: '', budgeted_hours: '0' }
    showTaskForm.value = false
    await loadScope()
    emit('saved')
  } catch (e) {
    errorMsg.value = extractError(e, 'Erreur création tâche')
  } finally {
    saving.value = false
  }
}

async function detachPhase(phaseId: number) {
  if (!props.amendmentId) return
  // Optimistic removal
  scope.value.phases = scope.value.phases.filter(p => p.id !== phaseId)
  try {
    await projectApi.updatePhase(props.projectId, phaseId, { amendment: null })
    emit('saved')
  } catch (e) {
    errorMsg.value = extractError(e, 'Erreur détachement')
    await loadScope()
  }
}

async function detachTask(taskId: number) {
  if (!props.amendmentId) return
  scope.value.tasks = scope.value.tasks.filter(t => t.id !== taskId)
  try {
    await projectApi.updateTask(props.projectId, taskId, { amendment: null })
    emit('saved')
  } catch (e) {
    errorMsg.value = extractError(e, 'Erreur détachement')
    await loadScope()
  }
}

function requestClose() {
  if (isDirty.value && !isCreate.value) {
    showDirtyBanner.value = true
    return
  }
  emit('close')
}

function discardAndClose() {
  showDirtyBanner.value = false
  emit('close')
}

async function saveAndClose() {
  await save()
  if (!errorMsg.value) emit('close')
}

function onKeydown(e: KeyboardEvent) {
  if (e.key === 'Escape') {
    e.preventDefault()
    requestClose()
  }
}

const rejectionNotePreview = computed(() => {
  if (status.value !== 'REJECTED') return ''
  const match = description.value.match(/\[Rejet —[^\]]+\]\s*(.+)$/s)
  return match && match[1] ? match[1].trim() : ''
})

function formatAmount(n: number): string {
  return n.toLocaleString('fr-CA', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}
</script>

<template>
  <Teleport to="body">
    <div v-if="open" class="aso-overlay" @click.self="requestClose" @keydown="onKeydown" tabindex="-1">
      <div class="aso-panel" role="dialog" aria-modal="true" :aria-labelledby="'aso-title'">
        <!-- Header -->
        <div class="aso-header">
          <div>
            <h3 id="aso-title" class="aso-title">
              <span v-if="isCreate">Nouvel avenant</span>
              <span v-else>AV-{{ amendmentNumber }}</span>
              <span v-if="isLocked" class="aso-lock" title="Avenant verrouillé">🔒</span>
            </h3>
            <span v-if="!isCreate" class="aso-code">
              {{ createdAt?.substring(0, 10) }}
            </span>
          </div>
          <button class="aso-close" aria-label="Fermer" @click="requestClose">&times;</button>
        </div>

        <!-- Stepper -->
        <div class="aso-stepper-wrap">
          <Stepper
            :steps="STEPPER_STEPS"
            :current-key="currentStepperKey"
            :rejected-key="rejectedKey"
            :rejected-tooltip="rejectionNotePreview || 'Avenant rejeté'"
          />
        </div>

        <!-- Body -->
        <div class="aso-body">
          <div v-if="errorMsg" class="aso-error">{{ errorMsg }}</div>

          <!-- Description -->
          <div class="aso-section">
            <label class="aso-label" for="aso-desc">Description <span class="aso-required">*</span></label>
            <textarea
              id="aso-desc"
              v-model="description"
              class="aso-description-input"
              :disabled="isLocked || saving"
              placeholder="Décrivez le changement contractuel"
              rows="3"
            ></textarea>
          </div>

          <!-- Rejection note (if rejected) -->
          <div v-if="status === 'REJECTED' && rejectionNotePreview" class="aso-section">
            <label class="aso-label">Motif du rejet</label>
            <div class="aso-rejection-note">{{ rejectionNotePreview }}</div>
          </div>

          <!-- Scope (only when amendment exists) -->
          <div v-if="!isCreate" class="aso-section">
            <div class="aso-section-header">
              <h4 class="aso-section-title">Périmètre</h4>
              <span class="aso-section-badge">
                {{ scope.phases.length }} phase{{ scope.phases.length > 1 ? 's' : '' }}
                ·
                {{ scope.tasks.length }} tâche{{ scope.tasks.length > 1 ? 's' : '' }}
              </span>
            </div>

            <div v-if="scopeLoading" class="aso-loading">Chargement…</div>

            <template v-else>
              <!-- Phases -->
              <div class="aso-scope-block">
                <div class="aso-scope-block-header">
                  <span class="aso-scope-block-title">Phases</span>
                  <button
                    v-if="!isLocked"
                    class="aso-btn-inline"
                    :disabled="saving"
                    @click="showPhaseForm = !showPhaseForm; showTaskForm = false"
                  >
                    {{ showPhaseForm ? '× Annuler' : '+ Ajouter phase' }}
                  </button>
                </div>
                <div v-if="showPhaseForm" class="aso-scope-form">
                  <input v-model="newPhase.name" class="aso-input" placeholder="Nom phase *" />
                  <input v-model="newPhase.client_facing_label" class="aso-input" placeholder="Libellé client" />
                  <div class="aso-scope-form-row">
                    <input v-model="newPhase.budgeted_hours" type="number" class="aso-input aso-input-sm" placeholder="Heures" />
                    <button class="aso-btn-primary" :disabled="saving" @click="addPhase">Ajouter</button>
                  </div>
                </div>
                <div v-if="scope.phases.length" class="aso-scope-list">
                  <div v-for="p in scope.phases" :key="'ph-' + p.id" class="aso-scope-item">
                    <div class="aso-scope-info">
                      <span class="aso-scope-name">{{ p.name }}</span>
                      <span v-if="p.client_facing_label" class="aso-scope-sub">{{ p.client_facing_label }}</span>
                    </div>
                    <span class="aso-scope-hours">{{ Number(p.budgeted_hours || 0).toFixed(1) }}h</span>
                    <button
                      v-if="!isLocked"
                      class="aso-btn-detach"
                      :disabled="saving"
                      title="Détacher de l'avenant"
                      @click="detachPhase(p.id)"
                    >✕</button>
                  </div>
                </div>
                <div v-else-if="!showPhaseForm" class="aso-empty">Aucune phase rattachée</div>
              </div>

              <!-- Tasks -->
              <div class="aso-scope-block">
                <div class="aso-scope-block-header">
                  <span class="aso-scope-block-title">Tâches</span>
                  <button
                    v-if="!isLocked"
                    class="aso-btn-inline"
                    :disabled="saving"
                    @click="showTaskForm = !showTaskForm; showPhaseForm = false"
                  >
                    {{ showTaskForm ? '× Annuler' : '+ Ajouter tâche' }}
                  </button>
                </div>
                <div v-if="showTaskForm" class="aso-scope-form">
                  <select v-model.number="newTask.phase" class="aso-input">
                    <option :value="null">— Choisir phase —</option>
                    <option v-for="p in phases" :key="p.id" :value="p.id">{{ p.name }}</option>
                  </select>
                  <input v-model="newTask.name" class="aso-input" placeholder="Nom tâche *" />
                  <div class="aso-scope-form-row">
                    <input v-model="newTask.budgeted_hours" type="number" class="aso-input aso-input-sm" placeholder="Heures" />
                    <button class="aso-btn-primary" :disabled="saving" @click="addTask">Ajouter</button>
                  </div>
                </div>
                <div v-if="scope.tasks.length" class="aso-scope-list">
                  <div v-for="t in scope.tasks" :key="'t-' + t.id" class="aso-scope-item">
                    <div class="aso-scope-info">
                      <span class="aso-scope-name">{{ t.name }}</span>
                      <span class="aso-scope-sub">{{ t.wbs_code }} · {{ t.phase_name || '—' }}</span>
                    </div>
                    <span class="aso-scope-hours">{{ Number(t.budgeted_hours || 0).toFixed(1) }}h</span>
                    <button
                      v-if="!isLocked"
                      class="aso-btn-detach"
                      :disabled="saving"
                      title="Détacher de l'avenant"
                      @click="detachTask(t.id)"
                    >✕</button>
                  </div>
                </div>
                <div v-else-if="!showTaskForm" class="aso-empty">Aucune tâche rattachée</div>
              </div>
            </template>
          </div>

          <!-- Budget impact -->
          <div class="aso-section">
            <label class="aso-label">Impact budget</label>
            <div class="aso-budget-row">
              <div class="aso-budget-display">
                <span class="aso-budget-value">{{ formatAmount(displayedBudgetImpact) }} $</span>
                <span v-if="overrideBudget" class="aso-budget-hint">Valeur technique : {{ formatAmount(autoBudgetImpact) }} $</span>
                <span v-else class="aso-budget-hint">Calculé automatiquement</span>
              </div>
            </div>
            <label v-if="!isLocked" class="aso-checkbox-row">
              <input v-model="overrideBudget" type="checkbox" :disabled="isLocked || saving" />
              <span>Saisir un montant forfaitaire (override)</span>
            </label>
            <input
              v-if="overrideBudget && !isLocked"
              v-model="budgetImpactRaw"
              type="number"
              step="0.01"
              class="aso-input"
              placeholder="0.00"
              :disabled="saving"
            />
          </div>
        </div>

        <!-- Actions footer -->
        <div class="aso-footer">
          <div v-if="showDirtyBanner" class="aso-dirty-banner">
            Modifications non enregistrées — <button class="aso-link" @click="saveAndClose">Enregistrer</button> ou <button class="aso-link" @click="discardAndClose">Fermer sans sauver</button>
          </div>
          <template v-else>
            <!-- REJECT inline form -->
            <template v-if="rejectMode">
              <input v-model="rejectReason" class="aso-input" placeholder="Motif du rejet *" />
              <button class="aso-btn-ghost" :disabled="saving" @click="rejectMode = false; rejectReason = ''">Annuler</button>
              <button class="aso-btn-danger" :disabled="saving" @click="confirmReject">Confirmer le rejet</button>
            </template>
            <template v-else>
              <button class="aso-btn-ghost" :disabled="saving" @click="requestClose">Fermer</button>

              <!-- DRAFT actions -->
              <template v-if="status === 'DRAFT'">
                <button class="aso-btn-primary" :disabled="saving || !description.trim()" @click="save">
                  {{ isCreate ? 'Créer' : 'Enregistrer' }}
                </button>
                <button v-if="!isCreate" class="aso-btn-success" :disabled="saving" @click="submitForApproval">
                  Soumettre pour approbation
                </button>
              </template>

              <!-- SUBMITTED actions -->
              <template v-else-if="status === 'SUBMITTED'">
                <template v-if="canApprove">
                  <button class="aso-btn-danger" :disabled="saving" @click="rejectMode = true">Rejeter…</button>
                  <button class="aso-btn-success" :disabled="saving" @click="approve">Valider</button>
                </template>
                <span v-else class="aso-status-hint">En attente de validation par l'associé en charge</span>
              </template>

              <!-- APPROVED / REJECTED -->
              <template v-else>
                <span class="aso-status-hint">
                  {{ status === 'APPROVED' ? 'Avenant approuvé — lecture seule' : 'Avenant rejeté — lecture seule' }}
                </span>
              </template>
            </template>
          </template>
        </div>

        <div v-if="loading" class="aso-overlay-loader">Chargement…</div>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.aso-overlay { position: fixed; inset: 0; z-index: 9998; background: rgba(0,0,0,0.3); display: flex; justify-content: flex-end; }
.aso-panel { width: 520px; max-width: 92vw; background: white; box-shadow: -4px 0 20px rgba(0,0,0,0.15); display: flex; flex-direction: column; overflow: hidden; }
@media (max-width: 1279px) { .aso-panel { width: 440px; } }

.aso-header { display: flex; align-items: center; justify-content: space-between; padding: 14px 16px; border-bottom: 1px solid var(--color-border); }
.aso-title { font-size: 16px; font-weight: 700; color: var(--color-gray-900); margin: 0; display: flex; align-items: center; gap: 8px; }
.aso-lock { font-size: 13px; }
.aso-code { font-size: 11px; color: var(--color-gray-500); }
.aso-close { background: none; border: none; font-size: 22px; color: var(--color-gray-400); cursor: pointer; padding: 0 4px; }
.aso-close:hover { color: var(--color-gray-900); }

.aso-stepper-wrap { padding: 8px 16px; border-bottom: 1px solid var(--color-gray-100); background: var(--color-surface-alt); }

.aso-body { flex: 1; overflow-y: auto; padding: 14px 16px; }

.aso-error { background: var(--color-danger-light); color: var(--color-danger); border: 1px solid var(--color-danger); border-radius: 4px; padding: 6px 10px; font-size: 12px; margin-bottom: 10px; }

.aso-section { margin-bottom: 18px; }
.aso-section-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px; }
.aso-section-title { font-size: 11px; font-weight: 700; color: var(--color-gray-500); text-transform: uppercase; letter-spacing: 0.3px; margin: 0; }
.aso-section-badge { font-size: 10px; color: var(--color-gray-400); }
.aso-label { display: block; font-size: 11px; font-weight: 600; color: var(--color-gray-700); margin-bottom: 4px; }
.aso-required { color: var(--color-danger); }
.aso-description-input { width: 100%; padding: 8px 10px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 13px; font-family: inherit; resize: vertical; }
.aso-description-input:focus { outline: none; border-color: var(--color-primary); box-shadow: 0 0 0 2px rgba(37,99,235,0.1); }
.aso-rejection-note { background: var(--color-danger-light); color: var(--color-gray-800); border: 1px solid var(--color-danger); border-radius: 4px; padding: 8px 10px; font-size: 12px; white-space: pre-wrap; }

.aso-scope-block { margin-bottom: 14px; }
.aso-scope-block-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px; }
.aso-scope-block-title { font-size: 11px; font-weight: 600; color: var(--color-gray-600); }
.aso-btn-inline { background: none; border: none; color: var(--color-primary); font-size: 11px; font-weight: 600; cursor: pointer; padding: 2px 6px; border-radius: 4px; }
.aso-btn-inline:hover:not(:disabled) { background: var(--color-primary-light); }
.aso-btn-inline:disabled { opacity: 0.5; cursor: not-allowed; }

.aso-scope-form { display: flex; flex-direction: column; gap: 6px; background: var(--color-gray-50); padding: 8px; border-radius: 4px; margin-bottom: 6px; }
.aso-scope-form-row { display: flex; gap: 6px; }
.aso-input { padding: 5px 8px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 12px; font-family: inherit; }
.aso-input:focus { outline: none; border-color: var(--color-primary); box-shadow: 0 0 0 2px rgba(37,99,235,0.1); }
.aso-input-sm { width: 80px; }

.aso-scope-list { display: flex; flex-direction: column; gap: 4px; }
.aso-scope-item { display: flex; align-items: center; gap: 8px; padding: 6px 8px; background: var(--color-gray-50); border-radius: 4px; }
.aso-scope-info { flex: 1; min-width: 0; display: flex; flex-direction: column; }
.aso-scope-name { font-size: 12px; font-weight: 600; color: var(--color-gray-900); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.aso-scope-sub { font-size: 10px; color: var(--color-gray-500); }
.aso-scope-hours { font-size: 11px; font-family: var(--font-mono); color: var(--color-gray-700); white-space: nowrap; }
.aso-btn-detach { background: none; border: none; color: var(--color-gray-400); cursor: pointer; font-size: 12px; padding: 2px 6px; border-radius: 4px; }
.aso-btn-detach:hover:not(:disabled) { color: var(--color-danger); background: var(--color-danger-light); }
.aso-btn-detach:disabled { opacity: 0.4; cursor: not-allowed; }
.aso-empty { font-size: 11px; color: var(--color-gray-400); font-style: italic; padding: 4px 0; }

.aso-budget-row { display: flex; align-items: baseline; gap: 10px; }
.aso-budget-display { display: flex; flex-direction: column; }
.aso-budget-value { font-size: 18px; font-weight: 700; font-family: var(--font-mono); color: var(--color-gray-900); }
.aso-budget-hint { font-size: 10px; color: var(--color-gray-500); }
.aso-checkbox-row { display: flex; align-items: center; gap: 6px; margin-top: 8px; font-size: 12px; color: var(--color-gray-700); cursor: pointer; }

.aso-footer { display: flex; align-items: center; justify-content: flex-end; gap: 8px; padding: 12px 16px; border-top: 1px solid var(--color-border); background: var(--color-surface-alt); }
.aso-btn-ghost { background: transparent; color: var(--color-gray-600); border: 1px solid var(--color-gray-300); padding: 6px 12px; border-radius: 4px; font-size: 12px; font-weight: 600; cursor: pointer; }
.aso-btn-ghost:hover:not(:disabled) { background: var(--color-gray-100); }
.aso-btn-primary { background: var(--color-primary); color: white; border: none; padding: 6px 14px; border-radius: 4px; font-size: 12px; font-weight: 600; cursor: pointer; }
.aso-btn-primary:hover:not(:disabled) { background: var(--color-primary-dark); }
.aso-btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }
.aso-btn-success { background: var(--color-success); color: white; border: none; padding: 6px 14px; border-radius: 4px; font-size: 12px; font-weight: 600; cursor: pointer; }
.aso-btn-success:hover:not(:disabled) { filter: brightness(0.95); }
.aso-btn-success:disabled { opacity: 0.5; cursor: not-allowed; }
.aso-btn-danger { background: var(--color-danger); color: white; border: none; padding: 6px 14px; border-radius: 4px; font-size: 12px; font-weight: 600; cursor: pointer; }
.aso-btn-danger:hover:not(:disabled) { filter: brightness(0.95); }
.aso-btn-danger:disabled { opacity: 0.5; cursor: not-allowed; }
.aso-status-hint { font-size: 11px; color: var(--color-gray-500); font-style: italic; flex: 1; text-align: left; }

.aso-dirty-banner { font-size: 11px; color: var(--color-warning); flex: 1; }
.aso-link { background: none; border: none; color: var(--color-primary); cursor: pointer; font-size: 11px; font-weight: 600; padding: 0 3px; }
.aso-link:hover { text-decoration: underline; }

.aso-loading { font-size: 12px; color: var(--color-gray-400); font-style: italic; padding: 4px 0; }
.aso-overlay-loader { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; background: rgba(255,255,255,0.6); font-size: 12px; color: var(--color-gray-500); }
</style>
