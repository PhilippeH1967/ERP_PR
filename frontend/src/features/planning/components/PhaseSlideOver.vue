<script setup lang="ts">
/**
 * PhaseSlideOver — Planning panel for a phase in the Gantt.
 * Shows: identity, budget vs actual, team allocations (editable), mini chart.
 * Opened on click on a Gantt bar.
 */
import { ref, computed, watch, onMounted } from 'vue'
import apiClient from '@/plugins/axios'

const props = defineProps<{
  open: boolean
  projectId: number
  phaseId: number | null
}>()

const emit = defineEmits<{ close: []; updated: [] }>()

interface PhaseData {
  id: number; name: string; code: string; phase_type: string; billing_mode: string
  start_date: string | null; end_date: string | null
  budgeted_hours: string; budgeted_cost: string
  tasks_budgeted_hours: number; planned_hours: number; actual_hours: number
  is_locked: boolean; is_mandatory: boolean
}

interface AllocationData {
  id: number; employee_id: number; employee_name: string
  hours_per_week: number; start_date: string; end_date: string
  status: string
}

interface MonthlyData { month: string; budget: number; planned: number; actual: number }

const phase = ref<PhaseData | null>(null)
const allocations = ref<AllocationData[]>([])
const monthlyChart = ref<MonthlyData[]>([])
const isLoading = ref(false)
const isSaving = ref(false)
const editDates = ref({ start: '', end: '' })
const showAssign = ref(false)
const assignSearch = ref('')
const assignUsers = ref<Array<{ id: number; username: string; email: string }>>([])
const assignHours = ref(20)

async function loadPhase() {
  if (!props.phaseId) return
  isLoading.value = true
  try {
    // Phase details
    const pr = await apiClient.get(`projects/${props.projectId}/phases/${props.phaseId}/`)
    phase.value = pr.data?.data || pr.data
    editDates.value = {
      start: phase.value?.start_date || '',
      end: phase.value?.end_date || '',
    }

    // Allocations for this phase
    const ar = await apiClient.get('allocations/', { params: { project: props.projectId, phase: props.phaseId } })
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
    }))

    // If no employee_name in allocation, try to resolve
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

    // Monthly chart data (simplified: from time entries)
    try {
      const tr = await apiClient.get('time_entries/', {
        params: { project: props.projectId, page_size: 1000 },
      })
      const entries = tr.data?.data || tr.data
      const allEntries = Array.isArray(entries) ? entries : entries?.results || []
      const phaseEntries = allEntries.filter((e: Record<string, unknown>) => e.phase === props.phaseId)

      // Group by month
      const monthMap = new Map<string, number>()
      for (const e of phaseEntries) {
        const m = String(e.date || '').substring(0, 7)
        if (m) monthMap.set(m, (monthMap.get(m) || 0) + Number(e.hours || 0))
      }

      const budget = phase.value?.tasks_budgeted_hours || Number(phase.value?.budgeted_hours || 0)
      const planned = phase.value?.planned_hours || 0
      const months = Array.from(monthMap.entries()).sort((a, b) => a[0].localeCompare(b[0]))
      monthlyChart.value = months.map(([month, actual]) => ({
        month: month.substring(5),
        budget: budget / Math.max(1, months.length),
        planned: planned / Math.max(1, months.length),
        actual,
      }))
    } catch { monthlyChart.value = [] }
  } catch { phase.value = null }
  finally { isLoading.value = false }
}

watch(() => [props.open, props.phaseId], () => {
  if (props.open && props.phaseId) loadPhase()
}, { immediate: true })

// Save dates
async function saveDates() {
  if (!phase.value) return
  isSaving.value = true
  try {
    await apiClient.patch(`projects/${props.projectId}/phases/${phase.value.id}/`, {
      start_date: editDates.value.start || null,
      end_date: editDates.value.end || null,
    })
    emit('updated')
    await loadPhase()
  } catch { /* */ }
  finally { isSaving.value = false }
}

// Update allocation hours
async function updateAllocation(allocId: number, field: string, value: unknown) {
  isSaving.value = true
  try {
    await apiClient.patch(`allocations/${allocId}/`, { [field]: value })
    await loadPhase()
    emit('updated')
  } catch { /* */ }
  finally { isSaving.value = false }
}

// Delete allocation
async function deleteAllocation(allocId: number) {
  try {
    await apiClient.delete(`allocations/${allocId}/`)
    await loadPhase()
    emit('updated')
  } catch { /* */ }
}

// Assign new employee
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
  if (!phase.value) return
  try {
    await apiClient.post('allocations/', {
      employee: userId,
      project: props.projectId,
      phase: phase.value.id,
      hours_per_week: assignHours.value,
      start_date: editDates.value.start || new Date().toISOString().substring(0, 10),
      end_date: editDates.value.end || new Date(Date.now() + 90 * 86400000).toISOString().substring(0, 10),
    })
    showAssign.value = false
    assignSearch.value = ''
    await loadPhase()
    emit('updated')
  } catch { /* */ }
}

// Computed
const advancementPct = computed(() => {
  const budget = phase.value?.tasks_budgeted_hours || Number(phase.value?.budgeted_hours || 0)
  const actual = phase.value?.actual_hours || 0
  return budget > 0 ? Math.min(100, Math.round(actual / budget * 100)) : 0
})

const totalPlannedWeek = computed(() => allocations.value.reduce((s, a) => s + a.hours_per_week, 0))

const maxChartVal = computed(() => Math.max(1, ...monthlyChart.value.map(m => Math.max(m.budget, m.planned, m.actual))))
</script>

<template>
  <Teleport to="body">
    <div v-if="open" class="pso-overlay" @click.self="emit('close')">
      <div class="pso-panel">
        <!-- Header -->
        <div class="pso-header">
          <div>
            <h3 class="pso-title">{{ phase?.name || 'Phase' }}</h3>
            <span class="pso-code">{{ phase?.code }} &middot; {{ phase?.phase_type === 'SUPPORT' ? 'Support' : 'Realisation' }} &middot; {{ phase?.billing_mode }}</span>
          </div>
          <button class="pso-close" @click="emit('close')">&times;</button>
        </div>

        <div v-if="isLoading" class="pso-loading">Chargement...</div>

        <div v-else-if="phase" class="pso-body">
          <!-- Section 1: Dates -->
          <div class="pso-section">
            <h4 class="pso-section-title">Dates</h4>
            <div class="pso-dates">
              <div>
                <label>Debut</label>
                <input v-model="editDates.start" type="date" class="pso-input" />
              </div>
              <div>
                <label>Fin</label>
                <input v-model="editDates.end" type="date" class="pso-input" />
              </div>
              <button class="pso-btn-save" :disabled="isSaving" @click="saveDates">{{ isSaving ? '...' : 'Enregistrer' }}</button>
            </div>
          </div>

          <!-- Section 2: Budget -->
          <div class="pso-section">
            <h4 class="pso-section-title">Budget vs Reel</h4>
            <div class="pso-budget-grid">
              <div class="pso-budget-item">
                <span class="pso-budget-label">H. budget</span>
                <span class="pso-budget-value">{{ (phase.tasks_budgeted_hours || Number(phase.budgeted_hours) || 0).toFixed(0) }}h</span>
              </div>
              <div class="pso-budget-item">
                <span class="pso-budget-label">H. planifie</span>
                <span class="pso-budget-value" :class="{ 'text-primary': (phase.planned_hours || 0) > 0, 'text-warning': (phase.planned_hours || 0) === 0 }">{{ (phase.planned_hours || 0).toFixed(0) }}h</span>
              </div>
              <div class="pso-budget-item">
                <span class="pso-budget-label">H. reel</span>
                <span class="pso-budget-value pso-bold">{{ (phase.actual_hours || 0).toFixed(1) }}h</span>
              </div>
              <div class="pso-budget-item">
                <span class="pso-budget-label">Avancement</span>
                <span class="pso-budget-value" :style="{ color: advancementPct > 90 ? '#DC2626' : advancementPct > 70 ? '#D97706' : '#16A34A' }">{{ advancementPct }}%</span>
              </div>
            </div>
            <div class="pso-progress">
              <div class="pso-progress-bg">
                <div class="pso-progress-fill" :style="{ width: advancementPct + '%', background: advancementPct > 90 ? '#DC2626' : advancementPct > 70 ? '#D97706' : '#16A34A' }"></div>
              </div>
            </div>
          </div>

          <!-- Section 3: Equipe -->
          <div class="pso-section">
            <h4 class="pso-section-title">
              Equipe affectee
              <span class="pso-section-badge">{{ allocations.length }} personne{{ allocations.length > 1 ? 's' : '' }} &middot; {{ totalPlannedWeek }}h/sem</span>
            </h4>

            <div v-if="allocations.length" class="pso-team-list">
              <div v-for="alloc in allocations" :key="alloc.id" class="pso-team-item">
                <div class="pso-team-info">
                  <span class="pso-team-avatar">{{ (alloc.employee_name || '??').substring(0, 2).toUpperCase() }}</span>
                  <div>
                    <span class="pso-team-name">{{ alloc.employee_name || `Employe #${alloc.employee_id}` }}</span>
                    <span class="pso-team-period">{{ alloc.start_date }} → {{ alloc.end_date }}</span>
                  </div>
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
            </div>
            <div v-else class="pso-empty">Aucun employe affecte a cette phase</div>

            <!-- Add employee -->
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

          <!-- Section 4: Mini chart -->
          <div v-if="monthlyChart.length" class="pso-section">
            <h4 class="pso-section-title">Historique mensuel</h4>
            <div class="pso-chart">
              <div v-for="m in monthlyChart" :key="m.month" class="pso-chart-col">
                <div class="pso-chart-bars">
                  <div class="pso-chart-bar budget" :style="{ height: (m.budget / maxChartVal * 60) + 'px' }" title="Budget"></div>
                  <div class="pso-chart-bar planned" :style="{ height: (m.planned / maxChartVal * 60) + 'px' }" title="Planifie"></div>
                  <div class="pso-chart-bar actual" :style="{ height: (m.actual / maxChartVal * 60) + 'px' }" title="Reel"></div>
                </div>
                <div class="pso-chart-label">{{ m.month }}</div>
              </div>
            </div>
            <div class="pso-chart-legend">
              <span><span class="pso-leg-dot budget"></span> Budget</span>
              <span><span class="pso-leg-dot planned"></span> Planifie</span>
              <span><span class="pso-leg-dot actual"></span> Reel</span>
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

/* Dates */
.pso-dates { display: flex; gap: 8px; align-items: flex-end; }
.pso-dates label { display: block; font-size: 10px; color: #6B7280; margin-bottom: 3px; }
.pso-input { padding: 5px 8px; border: 1px solid #D1D5DB; border-radius: 4px; font-size: 12px; width: 100%; }
.pso-btn-save { padding: 5px 14px; background: #2563EB; color: white; border: none; border-radius: 4px; font-size: 11px; font-weight: 600; cursor: pointer; white-space: nowrap; }
.pso-btn-save:disabled { opacity: 0.5; }

/* Budget */
.pso-budget-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.pso-budget-item { background: #F9FAFB; border-radius: 6px; padding: 8px 10px; }
.pso-budget-label { display: block; font-size: 9px; color: #9CA3AF; text-transform: uppercase; font-weight: 600; }
.pso-budget-value { font-size: 18px; font-weight: 700; font-family: var(--font-mono, monospace); color: #111827; }
.pso-bold { font-weight: 800; }
.text-primary { color: #2563EB; }
.text-warning { color: #D97706; }
.pso-progress { margin-top: 8px; }
.pso-progress-bg { height: 6px; background: #E5E7EB; border-radius: 3px; overflow: hidden; }
.pso-progress-fill { height: 100%; border-radius: 3px; transition: width 0.3s; }

/* Team */
.pso-team-list { display: flex; flex-direction: column; gap: 6px; }
.pso-team-item { display: flex; align-items: center; gap: 8px; padding: 8px; background: #F9FAFB; border-radius: 6px; }
.pso-team-info { display: flex; align-items: center; gap: 8px; flex: 1; min-width: 0; }
.pso-team-avatar { width: 28px; height: 28px; border-radius: 50%; background: #2563EB; color: white; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 700; flex-shrink: 0; }
.pso-team-name { display: block; font-size: 12px; font-weight: 600; color: #111827; }
.pso-team-period { display: block; font-size: 9px; color: #9CA3AF; }
.pso-team-hours { display: flex; align-items: center; gap: 3px; }
.pso-hours-input { width: 50px; padding: 3px 6px; border: 1px solid #D1D5DB; border-radius: 4px; font-size: 12px; font-family: var(--font-mono, monospace); text-align: right; }
.pso-hours-unit { font-size: 10px; color: #9CA3AF; }
.pso-btn-remove { background: none; border: none; font-size: 18px; color: #9CA3AF; cursor: pointer; padding: 0 4px; }
.pso-btn-remove:hover { color: #DC2626; }
.pso-empty { font-size: 12px; color: #9CA3AF; font-style: italic; padding: 8px 0; }
.pso-add-btn-row { margin-top: 8px; }
.pso-btn-add { background: none; border: 1px dashed #D1D5DB; border-radius: 6px; padding: 8px; width: 100%; font-size: 12px; font-weight: 600; color: #2563EB; cursor: pointer; }
.pso-btn-add:hover { border-color: #2563EB; background: #EFF6FF; }
.pso-btn-cancel { font-size: 11px; color: #6B7280; background: none; border: none; cursor: pointer; margin-top: 6px; }

/* Assign form */
.pso-assign-form { margin-top: 8px; background: #F9FAFB; border-radius: 6px; padding: 10px; }
.pso-assign-list { max-height: 120px; overflow-y: auto; border: 1px solid #E5E7EB; border-radius: 4px; background: white; }
.pso-assign-item { padding: 6px 10px; font-size: 12px; cursor: pointer; }
.pso-assign-item:hover { background: #EFF6FF; }
.pso-assign-email { font-size: 10px; color: #9CA3AF; margin-left: 6px; }
.pso-assign-hours { display: flex; align-items: center; gap: 6px; margin-top: 8px; font-size: 11px; color: #6B7280; }

/* Mini chart */
.pso-chart { display: flex; gap: 6px; align-items: flex-end; height: 70px; }
.pso-chart-col { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 3px; height: 100%; justify-content: flex-end; }
.pso-chart-bars { display: flex; gap: 2px; align-items: flex-end; }
.pso-chart-bar { width: 10px; border-radius: 2px 2px 0 0; min-height: 2px; }
.pso-chart-bar.budget { background: #E5E7EB; }
.pso-chart-bar.planned { background: #93C5FD; }
.pso-chart-bar.actual { background: #2563EB; }
.pso-chart-label { font-size: 9px; color: #9CA3AF; }
.pso-chart-legend { display: flex; gap: 12px; margin-top: 6px; font-size: 9px; color: #6B7280; }
.pso-leg-dot { display: inline-block; width: 8px; height: 8px; border-radius: 2px; margin-right: 3px; vertical-align: middle; }
.pso-leg-dot.budget { background: #E5E7EB; }
.pso-leg-dot.planned { background: #93C5FD; }
.pso-leg-dot.actual { background: #2563EB; }
</style>
