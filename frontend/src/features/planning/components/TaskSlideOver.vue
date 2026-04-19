<script setup lang="ts">
/**
 * TaskSlideOver — Planning panel for a task.
 * Sections: dates + team allocations (mode + Manuelle grid). No budget, no chart.
 */
import { ref, computed, watch } from 'vue'
import apiClient from '@/plugins/axios'
import { isoWeeksBetween, weekLabel } from '../utils/isoWeek'

const props = defineProps<{
  open: boolean
  projectId: number
  taskId: number | null
}>()

const emit = defineEmits<{ close: []; updated: [] }>()

interface TaskData {
  id: number; name: string; client_facing_label: string; wbs_code: string
  phase: number | null; phase_name: string
  start_date: string | null; end_date: string | null
  budgeted_hours: string; progress_pct: number
}

type DistributionMode = 'uniform' | 'standard' | 'manual'
type TimeUnit = 'week' | 'month'

interface AllocationData {
  id: number; employee_id: number; employee_name: string
  hours_per_week: number; start_date: string; end_date: string
  status: string
  distribution_mode: DistributionMode
  time_unit: TimeUnit
  time_breakdown: Record<string, number> | null
}

const task = ref<TaskData | null>(null)
const allocations = ref<AllocationData[]>([])
const isLoading = ref(false)
const isSaving = ref(false)
const editDates = ref({ start: '', end: '' })
const showAssign = ref(false)
const assignSearch = ref('')
const assignUsers = ref<Array<{ id: number; username: string; email: string }>>([])
const assignHours = ref(20)

async function loadTask() {
  if (!props.taskId) return
  isLoading.value = true
  try {
    const tr = await apiClient.get(`projects/${props.projectId}/tasks/${props.taskId}/`)
    task.value = tr.data?.data || tr.data
    editDates.value = {
      start: task.value?.start_date || '',
      end: task.value?.end_date || '',
    }

    const ar = await apiClient.get('allocations/', { params: { project: props.projectId, task: props.taskId } })
    const ad = ar.data?.data || ar.data
    const allocs = Array.isArray(ad) ? ad : ad?.results || []
    allocations.value = allocs.map((a: Record<string, unknown>) => ({
      id: Number(a.id),
      employee_id: Number(a.employee),
      employee_name: String(a.employee_name || a.employee || ''),
      hours_per_week: Number(a.hours_per_week || 0),
      start_date: String(a.start_date || ''),
      end_date: String(a.end_date || ''),
      status: String(a.status || 'ACTIVE'),
      distribution_mode: (a.distribution_mode as DistributionMode) || 'uniform',
      time_unit: (a.time_unit as TimeUnit) || 'week',
      time_breakdown: (a.time_breakdown as Record<string, number> | null) ?? null,
    }))

    if (allocations.value.length && !allocations.value[0].employee_name) {
      try {
        const ur = await apiClient.get('users/search/')
        const users = ur.data?.data || ur.data || []
        const userMap = new Map<number, string>()
        for (const u of (Array.isArray(users) ? users : [])) {
          userMap.set(u.id, `${u.first_name || ''} ${u.last_name || ''}`.trim() || u.username)
        }
        for (const a of allocations.value) {
          if (!a.employee_name && userMap.has(a.employee_id)) a.employee_name = userMap.get(a.employee_id)!
        }
      } catch { /* */ }
    }
  } catch { task.value = null }
  finally { isLoading.value = false }
}

watch(() => [props.open, props.taskId], () => {
  if (props.open && props.taskId) loadTask()
}, { immediate: true })

async function saveDates() {
  if (!task.value) return
  isSaving.value = true
  try {
    await apiClient.patch(`projects/${props.projectId}/tasks/${task.value.id}/`, {
      start_date: editDates.value.start || null,
      end_date: editDates.value.end || null,
    })
    emit('updated')
    await loadTask()
  } catch { /* */ }
  finally { isSaving.value = false }
}

async function updateAllocation(allocId: number, field: string, value: unknown) {
  isSaving.value = true
  try {
    const resp = await apiClient.patch(`allocations/${allocId}/`, { [field]: value })
    const updated = resp.data?.data || resp.data
    const idx = allocations.value.findIndex(a => a.id === allocId)
    if (idx >= 0 && updated) {
      const cur = allocations.value[idx]
      allocations.value[idx] = {
        ...cur,
        hours_per_week: Number(updated.hours_per_week ?? cur.hours_per_week),
        start_date: updated.start_date ?? cur.start_date,
        end_date: updated.end_date ?? cur.end_date,
        status: updated.status ?? cur.status,
        distribution_mode: (updated.distribution_mode as DistributionMode) || cur.distribution_mode,
        time_unit: (updated.time_unit as TimeUnit) || cur.time_unit,
        time_breakdown: (updated.time_breakdown ?? null) as Record<string, number> | null,
      }
    }
    emit('updated')
  } catch { /* */ }
  finally { isSaving.value = false }
}

async function deleteAllocation(allocId: number) {
  try {
    await apiClient.delete(`allocations/${allocId}/`)
    await loadTask()
    emit('updated')
  } catch { /* */ }
}

function onAllocDateChange(alloc: AllocationData, field: 'start_date' | 'end_date', ev: Event) {
  const val = (ev.target as HTMLInputElement).value
  const next = { start: alloc.start_date, end: alloc.end_date, [field === 'start_date' ? 'start' : 'end']: val }
  if (next.start && next.end && next.end < next.start) {
    ;(ev.target as HTMLInputElement).value = alloc[field]
    return
  }
  updateAllocation(alloc.id, field, val)
}

function setAllocMode(alloc: AllocationData, mode: DistributionMode) {
  if (mode === 'standard') return
  if (alloc.distribution_mode === mode) return
  updateAllocation(alloc.id, 'distribution_mode', mode)
}

function allocWeeks(alloc: AllocationData): string[] {
  return isoWeeksBetween(alloc.start_date, alloc.end_date)
}
function manualCellValue(alloc: AllocationData, weekKey: string): number {
  const bd = alloc.time_breakdown || {}
  return Number(bd[weekKey] || 0)
}
function manualTotal(alloc: AllocationData): number {
  const bd = alloc.time_breakdown || {}
  return Object.values(bd).reduce((s, v) => s + Number(v || 0), 0)
}
async function onManualCellChange(alloc: AllocationData, weekKey: string, ev: Event) {
  const raw = (ev.target as HTMLInputElement).value
  const n = Number(raw)
  const next: Record<string, number> = { ...(alloc.time_breakdown || {}) }
  if (raw === '' || !Number.isFinite(n) || n <= 0) {
    delete next[weekKey]
  } else {
    next[weekKey] = n
  }
  alloc.time_breakdown = next
  await updateAllocation(alloc.id, 'time_breakdown', next)
}

async function loadAssignUsers() {
  try {
    const r = await apiClient.get('users/search/')
    assignUsers.value = Array.isArray(r.data?.data || r.data) ? (r.data?.data || r.data) : []
  } catch { assignUsers.value = [] }
}

const filteredAssignUsers = computed(() => {
  const q = assignSearch.value.toLowerCase()
  return assignUsers.value.filter(u => !q || u.username.toLowerCase().includes(q) || u.email.toLowerCase().includes(q)).slice(0, 10)
})

async function assignEmployee(userId: number) {
  if (!task.value) return
  try {
    await apiClient.post('allocations/', {
      employee: userId,
      project: props.projectId,
      task: task.value.id,
      hours_per_week: assignHours.value,
      start_date: editDates.value.start || new Date().toISOString().substring(0, 10),
      end_date: editDates.value.end || new Date(Date.now() + 90 * 86400000).toISOString().substring(0, 10),
      distribution_mode: 'uniform',
      time_unit: 'week',
    })
    showAssign.value = false
    assignSearch.value = ''
    await loadTask()
    emit('updated')
  } catch { /* */ }
}

const totalPlannedWeek = computed(() => allocations.value.reduce((s, a) => s + a.hours_per_week, 0))
</script>

<template>
  <Teleport to="body">
    <div v-if="open" class="pso-overlay" @click.self="emit('close')">
      <div class="pso-panel">
        <div class="pso-header">
          <div>
            <h3 class="pso-title">{{ task?.client_facing_label || task?.name || 'Tache' }}</h3>
            <span class="pso-code">{{ task?.wbs_code }} &middot; {{ task?.phase_name }}</span>
          </div>
          <button class="pso-close" @click="emit('close')">&times;</button>
        </div>

        <div v-if="isLoading" class="pso-loading">Chargement...</div>

        <div v-else-if="task" class="pso-body">
          <!-- Dates (auto-save on change) -->
          <div class="pso-section">
            <h4 class="pso-section-title">
              Dates
              <span v-if="isSaving" class="pso-section-badge">enregistrement…</span>
            </h4>
            <div class="pso-dates">
              <div>
                <label>Debut</label>
                <input v-model="editDates.start" type="date" class="pso-input" @change="saveDates" />
              </div>
              <div>
                <label>Fin</label>
                <input v-model="editDates.end" type="date" class="pso-input" @change="saveDates" />
              </div>
            </div>
          </div>

          <!-- Equipe -->
          <div class="pso-section">
            <h4 class="pso-section-title">
              Equipe affectee
              <span class="pso-section-badge">{{ allocations.length }} personne{{ allocations.length > 1 ? 's' : '' }} &middot; {{ totalPlannedWeek }}h/sem</span>
            </h4>

            <div v-if="allocations.length" class="pso-team-list">
              <div v-for="alloc in allocations" :key="alloc.id" class="pso-team-item">
                <div class="pso-team-row">
                  <div class="pso-team-info">
                    <span class="pso-team-avatar">{{ (alloc.employee_name || '??').substring(0, 2).toUpperCase() }}</span>
                    <span class="pso-team-name">{{ alloc.employee_name || `Employe #${alloc.employee_id}` }}</span>
                  </div>
                  <div class="pso-team-hours">
                    <input
                      type="number" min="0" max="50" step="0.5"
                      class="pso-hours-input"
                      :value="alloc.hours_per_week"
                      @change="(e: Event) => updateAllocation(alloc.id, 'hours_per_week', Number((e.target as HTMLInputElement).value))"
                    />
                    <span class="pso-hours-unit">h/sem</span>
                  </div>
                  <button class="pso-btn-remove" @click="deleteAllocation(alloc.id)" title="Retirer">&times;</button>
                </div>
                <div class="pso-team-dates">
                  <input
                    type="date" class="pso-date-input"
                    :value="alloc.start_date"
                    @change="(e: Event) => onAllocDateChange(alloc, 'start_date', e)"
                  />
                  <span class="pso-date-sep">→</span>
                  <input
                    type="date" class="pso-date-input"
                    :value="alloc.end_date"
                    @change="(e: Event) => onAllocDateChange(alloc, 'end_date', e)"
                  />
                </div>
                <div class="pso-mode-segmented">
                  <button
                    type="button" class="pso-mode-btn"
                    :class="{ active: alloc.distribution_mode === 'uniform' }"
                    @click="setAllocMode(alloc, 'uniform')"
                  >Uniforme</button>
                  <button
                    type="button" class="pso-mode-btn"
                    :class="{ active: alloc.distribution_mode === 'standard' }"
                    disabled title="Disponible en Sprint 2"
                  >Standard</button>
                  <button
                    type="button" class="pso-mode-btn"
                    :class="{ active: alloc.distribution_mode === 'manual' }"
                    @click="setAllocMode(alloc, 'manual')"
                  >Manuelle</button>
                </div>
                <div v-if="alloc.distribution_mode === 'manual'" class="pso-manual-grid-wrap">
                  <div v-if="!allocWeeks(alloc).length" class="pso-manual-empty">
                    Renseignez des dates valides pour afficher la grille.
                  </div>
                  <div v-else class="pso-manual-grid">
                    <div v-for="wk in allocWeeks(alloc)" :key="wk" class="pso-manual-cell">
                      <span class="pso-manual-label">{{ weekLabel(wk) }}</span>
                      <input
                        type="number" min="0" step="0.5"
                        class="pso-manual-input"
                        :value="manualCellValue(alloc, wk) || ''"
                        @change="(e: Event) => onManualCellChange(alloc, wk, e)"
                      />
                    </div>
                  </div>
                  <div class="pso-manual-total">Total: <strong>{{ manualTotal(alloc).toFixed(1) }}h</strong></div>
                </div>
              </div>
            </div>
            <div v-else class="pso-empty">Aucun employe affecte a cette tache</div>

            <div v-if="!showAssign" class="pso-add-btn-row">
              <button class="pso-btn-add" @click="showAssign = true; loadAssignUsers()">+ Affecter un employe</button>
            </div>
            <div v-else class="pso-assign-form">
              <input v-model="assignSearch" type="text" placeholder="Rechercher..." class="pso-input" style="margin-bottom:6px;" />
              <div class="pso-assign-list">
                <div v-for="u in filteredAssignUsers" :key="u.id" class="pso-assign-item" @click="assignEmployee(u.id)">
                  {{ u.username }} <span class="pso-assign-email">{{ u.email }}</span>
                </div>
                <div v-if="!filteredAssignUsers.length" class="pso-empty" style="padding:8px;">Aucun resultat</div>
              </div>
              <div class="pso-assign-hours">
                <label>Heures/semaine:</label>
                <input v-model.number="assignHours" type="number" min="1" max="50" class="pso-hours-input" />
              </div>
              <button class="pso-btn-cancel" @click="showAssign = false">Annuler</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.pso-overlay { position: fixed; inset: 0; z-index: 9998; background: rgba(0,0,0,0.3); display: flex; justify-content: flex-end; }
.pso-panel { width: 450px; max-width: 90vw; background: white; box-shadow: -4px 0 20px rgba(0,0,0,0.15); display: flex; flex-direction: column; overflow: hidden; }
.pso-header { display: flex; align-items: center; justify-content: space-between; padding: 16px; border-bottom: 1px solid #E5E7EB; }
.pso-title { font-size: 16px; font-weight: 700; color: #111827; margin: 0; }
.pso-code { font-size: 11px; color: #6B7280; }
.pso-close { background: none; border: none; font-size: 24px; color: #9CA3AF; cursor: pointer; padding: 0 4px; }
.pso-close:hover { color: #111827; }
.pso-loading { padding: 40px; text-align: center; color: #9CA3AF; }
.pso-body { flex: 1; overflow-y: auto; }

.pso-section { padding: 16px; border-bottom: 1px solid #F3F4F6; }
.pso-section-title { font-size: 11px; font-weight: 700; color: #6B7280; text-transform: uppercase; letter-spacing: 0.3px; margin: 0 0 10px; display: flex; align-items: center; gap: 8px; }
.pso-section-badge { font-size: 10px; font-weight: 400; color: #9CA3AF; text-transform: none; }

.pso-dates { display: flex; gap: 8px; align-items: flex-end; }
.pso-dates label { display: block; font-size: 10px; color: #6B7280; margin-bottom: 3px; }
.pso-input { padding: 5px 8px; border: 1px solid #D1D5DB; border-radius: 4px; font-size: 12px; width: 100%; }
.pso-btn-save { padding: 5px 14px; background: #2563EB; color: white; border: none; border-radius: 4px; font-size: 11px; font-weight: 600; cursor: pointer; white-space: nowrap; }
.pso-btn-save:disabled { opacity: 0.5; }

.pso-team-list { display: flex; flex-direction: column; gap: 8px; }
.pso-team-item { display: flex; flex-direction: column; gap: 6px; padding: 8px; background: #F9FAFB; border-radius: 6px; }
.pso-team-row { display: flex; align-items: center; gap: 8px; }
.pso-team-info { display: flex; align-items: center; gap: 8px; flex: 1; min-width: 0; }
.pso-team-avatar { width: 28px; height: 28px; border-radius: 50%; background: #2563EB; color: white; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 700; flex-shrink: 0; }
.pso-team-name { display: block; font-size: 12px; font-weight: 600; color: #111827; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.pso-team-hours { display: flex; align-items: center; gap: 3px; }
.pso-hours-input { width: 50px; padding: 3px 6px; border: 1px solid #D1D5DB; border-radius: 4px; font-size: 12px; font-family: var(--font-mono, monospace); text-align: right; -moz-appearance: textfield; appearance: textfield; }
.pso-hours-input::-webkit-outer-spin-button, .pso-hours-input::-webkit-inner-spin-button { -webkit-appearance: none; margin: 0; }
.pso-hours-unit { font-size: 10px; color: #9CA3AF; }
.pso-btn-remove { background: none; border: none; font-size: 18px; color: #9CA3AF; cursor: pointer; padding: 0 4px; }
.pso-btn-remove:hover { color: #DC2626; }
.pso-empty { font-size: 12px; color: #9CA3AF; font-style: italic; padding: 8px 0; }
.pso-add-btn-row { margin-top: 8px; }
.pso-btn-add { background: none; border: 1px dashed #D1D5DB; border-radius: 6px; padding: 8px; width: 100%; font-size: 12px; font-weight: 600; color: #2563EB; cursor: pointer; }
.pso-btn-add:hover { border-color: #2563EB; background: #EFF6FF; }
.pso-btn-cancel { font-size: 11px; color: #6B7280; background: none; border: none; cursor: pointer; margin-top: 6px; }

.pso-team-dates { display: flex; align-items: center; gap: 6px; padding-left: 36px; }
.pso-date-input { padding: 3px 6px; border: 1px solid #D1D5DB; border-radius: 4px; font-size: 11px; font-family: var(--font-mono, monospace); background: white; }
.pso-date-sep { font-size: 11px; color: #9CA3AF; }
.pso-mode-segmented { display: flex; padding-left: 36px; gap: 0; }
.pso-mode-btn { flex: 1; padding: 4px 8px; font-size: 10px; font-weight: 600; color: #6B7280; background: white; border: 1px solid #D1D5DB; cursor: pointer; }
.pso-mode-btn:first-child { border-radius: 4px 0 0 4px; }
.pso-mode-btn:last-child { border-radius: 0 4px 4px 0; }
.pso-mode-btn:not(:first-child) { border-left: none; }
.pso-mode-btn.active { background: #2563EB; color: white; border-color: #2563EB; }
.pso-mode-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.pso-mode-btn:not(:disabled):not(.active):hover { background: #F3F4F6; }

.pso-manual-grid-wrap { padding-left: 36px; }
.pso-manual-empty { font-size: 10px; color: #9CA3AF; font-style: italic; padding: 4px 0; }
.pso-manual-grid { display: flex; gap: 4px; overflow-x: auto; padding: 4px 0; }
.pso-manual-cell { display: flex; flex-direction: column; align-items: center; flex-shrink: 0; gap: 2px; }
.pso-manual-label { font-size: 9px; font-weight: 600; color: #6B7280; font-family: var(--font-mono, monospace); }
.pso-manual-input { width: 42px; padding: 3px 4px; border: 1px solid #D1D5DB; border-radius: 3px; font-size: 11px; font-family: var(--font-mono, monospace); text-align: center; background: white; -moz-appearance: textfield; appearance: textfield; }
.pso-manual-input::-webkit-outer-spin-button, .pso-manual-input::-webkit-inner-spin-button { -webkit-appearance: none; margin: 0; }
.pso-manual-input:focus { outline: 2px solid #2563EB; outline-offset: -1px; border-color: #2563EB; }
.pso-manual-total { font-size: 10px; color: #6B7280; padding-top: 4px; }
.pso-manual-total strong { color: #111827; font-family: var(--font-mono, monospace); }

.pso-assign-form { margin-top: 8px; background: #F9FAFB; border-radius: 6px; padding: 10px; }
.pso-assign-list { max-height: 120px; overflow-y: auto; border: 1px solid #E5E7EB; border-radius: 4px; background: white; }
.pso-assign-item { padding: 6px 10px; font-size: 12px; cursor: pointer; }
.pso-assign-item:hover { background: #EFF6FF; }
.pso-assign-email { font-size: 10px; color: #9CA3AF; margin-left: 6px; }
.pso-assign-hours { display: flex; align-items: center; gap: 6px; margin-top: 8px; font-size: 11px; color: #6B7280; }
</style>
