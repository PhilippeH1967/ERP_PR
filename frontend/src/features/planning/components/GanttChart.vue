<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import apiClient from '@/plugins/axios'

const props = defineProps<{ projectId: number }>()

interface GanttPhase {
  id: number; name: string; client_label: string; code: string; type: string
  start_date: string | null; end_date: string | null
  billing_mode: string; budgeted_hours: number; is_mandatory: boolean; order: number
}
interface GanttMilestone { id: number; title: string; date: string; status: string; color: string }
interface GanttDependency { id: number; from: number; to: number; type: string; lag: number }

const phases = ref<GanttPhase[]>([])
const milestones = ref<GanttMilestone[]>([])
const dependencies = ref<GanttDependency[]>([])
const projectInfo = ref({ code: '', name: '' })
const isLoading = ref(true)
const editingPhase = ref<number | null>(null)
const editDates = ref({ start: '', end: '' })
const zoomLevel = ref<'month' | 'quarter' | 'year'>('quarter')

async function load() {
  isLoading.value = true
  try {
    const resp = await apiClient.get('gantt/project_gantt/', { params: { project_id: props.projectId } })
    const data = resp.data?.data || resp.data
    phases.value = data.phases || []
    milestones.value = data.milestones || []
    dependencies.value = data.dependencies || []
    projectInfo.value = data.project || { code: '', name: '' }
  } catch { /* */ }
  finally { isLoading.value = false }
}

onMounted(load)

// Timeline range
const timelineStart = computed(() => {
  const dates = phases.value.filter(p => p.start_date).map(p => new Date(p.start_date!))
  if (!dates.length) return new Date()
  const min = new Date(Math.min(...dates.map(d => d.getTime())))
  min.setDate(1) // start of month
  return min
})

const timelineEnd = computed(() => {
  const dates = phases.value.filter(p => p.end_date).map(p => new Date(p.end_date!))
  if (!dates.length) {
    const d = new Date()
    d.setFullYear(d.getFullYear() + 2)
    return d
  }
  const max = new Date(Math.max(...dates.map(d => d.getTime())))
  max.setMonth(max.getMonth() + 3)
  return max
})

const totalDays = computed(() => Math.max(1, Math.round((timelineEnd.value.getTime() - timelineStart.value.getTime()) / 86400000)))

// Generate period headers
const periods = computed(() => {
  const result: { label: string; width: number }[] = []
  const start = new Date(timelineStart.value)
  const end = timelineEnd.value

  if (zoomLevel.value === 'quarter') {
    let d = new Date(start)
    while (d < end) {
      const q = Math.floor(d.getMonth() / 3) + 1
      const qStart = new Date(d.getFullYear(), (q - 1) * 3, 1)
      const qEnd = new Date(d.getFullYear(), q * 3, 0)
      const daySpan = Math.round((Math.min(qEnd.getTime(), end.getTime()) - Math.max(qStart.getTime(), start.getTime())) / 86400000)
      result.push({ label: `T${q} ${d.getFullYear()}`, width: (daySpan / totalDays.value) * 100 })
      d = new Date(d.getFullYear(), q * 3, 1)
    }
  } else if (zoomLevel.value === 'month') {
    let d = new Date(start)
    while (d < end) {
      const mEnd = new Date(d.getFullYear(), d.getMonth() + 1, 0)
      const daySpan = Math.round((Math.min(mEnd.getTime(), end.getTime()) - Math.max(d.getTime(), start.getTime())) / 86400000)
      const months = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun', 'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc']
      result.push({ label: `${months[d.getMonth()]} ${d.getFullYear()}`, width: (daySpan / totalDays.value) * 100 })
      d = new Date(d.getFullYear(), d.getMonth() + 1, 1)
    }
  } else {
    let y = start.getFullYear()
    while (y <= end.getFullYear()) {
      const yStart = new Date(y, 0, 1)
      const yEnd = new Date(y, 11, 31)
      const daySpan = Math.round((Math.min(yEnd.getTime(), end.getTime()) - Math.max(yStart.getTime(), start.getTime())) / 86400000)
      result.push({ label: String(y), width: (daySpan / totalDays.value) * 100 })
      y++
    }
  }
  return result
})

function barStyle(phase: GanttPhase) {
  if (!phase.start_date || !phase.end_date) return { display: 'none' }
  const start = new Date(phase.start_date)
  const end = new Date(phase.end_date)
  const left = ((start.getTime() - timelineStart.value.getTime()) / 86400000) / totalDays.value * 100
  const width = ((end.getTime() - start.getTime()) / 86400000) / totalDays.value * 100
  return { left: `${Math.max(0, left)}%`, width: `${Math.max(1, width)}%` }
}

function milestoneStyle(m: GanttMilestone) {
  const d = new Date(m.date)
  const left = ((d.getTime() - timelineStart.value.getTime()) / 86400000) / totalDays.value * 100
  return { left: `${left}%` }
}

const phaseColors: Record<string, string> = {
  REALIZATION: '#3B82F6',
  SUPPORT: '#F59E0B',
}

function startEdit(phase: GanttPhase) {
  editingPhase.value = phase.id
  editDates.value = { start: phase.start_date || '', end: phase.end_date || '' }
}

async function saveEdit(phaseId: number) {
  try {
    await apiClient.patch(`projects/${props.projectId}/phases/${phaseId}/`, {
      start_date: editDates.value.start || null,
      end_date: editDates.value.end || null,
    })
    editingPhase.value = null
    await load()
  } catch { /* */ }
}

function formatDate(d: string | null) {
  if (!d) return '—'
  return new Date(d).toLocaleDateString('fr-CA', { month: 'short', year: 'numeric' })
}

function durationWeeks(start: string | null, end: string | null) {
  if (!start || !end) return '—'
  const days = Math.round((new Date(end).getTime() - new Date(start).getTime()) / 86400000)
  return `${Math.round(days / 7)} sem.`
}
</script>

<template>
  <div class="gantt-container">
    <!-- Header -->
    <div class="gantt-header">
      <h3>Diagramme de Gantt — {{ projectInfo.code }}</h3>
      <div class="gantt-controls">
        <button v-for="z in (['month', 'quarter', 'year'] as const)" :key="z" class="zoom-btn" :class="{ active: zoomLevel === z }" @click="zoomLevel = z">
          {{ z === 'month' ? 'Mois' : z === 'quarter' ? 'Trimestre' : 'Année' }}
        </button>
      </div>
    </div>

    <div v-if="isLoading" class="gantt-loading">Chargement...</div>
    <div v-else-if="!phases.length" class="gantt-empty">Aucune phase avec dates — configurez les dates dans l'onglet Phases</div>

    <div v-else class="gantt-body">
      <!-- Timeline header -->
      <div class="gantt-timeline-header">
        <div class="gantt-label-col"></div>
        <div class="gantt-timeline-periods">
          <div v-for="(p, i) in periods" :key="i" class="gantt-period" :style="{ width: p.width + '%' }">
            {{ p.label }}
          </div>
        </div>
      </div>

      <!-- Phase rows -->
      <div v-for="phase in phases" :key="phase.id" class="gantt-row">
        <div class="gantt-label-col">
          <div class="gantt-phase-label">
            <span class="phase-code">{{ phase.code }}</span>
            <span class="phase-name">{{ phase.client_label || phase.name }}</span>
            <span v-if="phase.is_mandatory" class="mandatory-badge">Obl.</span>
          </div>
        </div>
        <div class="gantt-timeline-area">
          <!-- Bar -->
          <div
            class="gantt-bar"
            :style="{ ...barStyle(phase), backgroundColor: phaseColors[phase.type] || '#3B82F6' }"
            :title="`${phase.name}: ${formatDate(phase.start_date)} → ${formatDate(phase.end_date)}`"
            @dblclick="startEdit(phase)"
          >
            <span class="bar-label">{{ formatDate(phase.start_date) }} → {{ formatDate(phase.end_date) }}</span>
          </div>
          <!-- Milestones on this row (if date falls within phase) -->
          <div
            v-for="m in milestones.filter(ms => phase.start_date && phase.end_date && ms.date >= phase.start_date && ms.date <= phase.end_date)"
            :key="'m-' + m.id"
            class="gantt-milestone"
            :style="milestoneStyle(m)"
            :title="m.title + ' — ' + m.date"
          >
            <span class="milestone-diamond" :style="{ borderBottomColor: m.color }"></span>
          </div>
        </div>
      </div>

      <!-- Milestones row (independent) -->
      <div v-if="milestones.length" class="gantt-row milestone-row">
        <div class="gantt-label-col"><span class="phase-name" style="font-style:italic;">Jalons</span></div>
        <div class="gantt-timeline-area">
          <div v-for="m in milestones" :key="'mrow-' + m.id" class="gantt-milestone" :style="milestoneStyle(m)" :title="m.title">
            <span class="milestone-diamond" :style="{ borderBottomColor: m.color }"></span>
            <span class="milestone-label">{{ m.title }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit date modal (inline) -->
    <div v-if="editingPhase" class="gantt-edit-bar">
      <span>Modifier dates :</span>
      <input v-model="editDates.start" type="date" class="date-input" />
      <span>→</span>
      <input v-model="editDates.end" type="date" class="date-input" />
      <button class="btn-save" @click="saveEdit(editingPhase!)">OK</button>
      <button class="btn-cancel" @click="editingPhase = null">Annuler</button>
    </div>

    <!-- Phase dates table -->
    <div v-if="phases.length" class="gantt-table">
      <table>
        <thead>
          <tr>
            <th>Phase</th>
            <th>Début</th>
            <th>Fin</th>
            <th>Durée</th>
            <th class="text-right">Heures</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="phase in phases" :key="'tbl-' + phase.id" @dblclick="startEdit(phase)">
            <td class="font-semibold">{{ phase.code }} — {{ phase.name }}</td>
            <td>{{ phase.start_date || '—' }}</td>
            <td>{{ phase.end_date || '—' }}</td>
            <td>{{ durationWeeks(phase.start_date, phase.end_date) }}</td>
            <td class="text-right font-mono">{{ phase.budgeted_hours }}h</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.gantt-container { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); overflow: hidden; }
.gantt-header { display: flex; align-items: center; justify-content: space-between; padding: 12px 16px; border-bottom: 1px solid var(--color-gray-200); }
.gantt-header h3 { font-size: 14px; font-weight: 600; color: var(--color-gray-800); }
.gantt-controls { display: flex; gap: 4px; }
.zoom-btn { padding: 3px 10px; border-radius: 4px; font-size: 11px; font-weight: 600; border: 1px solid var(--color-gray-300); background: white; cursor: pointer; color: var(--color-gray-600); }
.zoom-btn.active { background: var(--color-primary); color: white; border-color: var(--color-primary); }
.gantt-loading, .gantt-empty { padding: 40px; text-align: center; color: var(--color-gray-400); font-size: 13px; }

.gantt-body { overflow-x: auto; }
.gantt-timeline-header { display: flex; border-bottom: 2px solid var(--color-gray-200); }
.gantt-label-col { width: 200px; min-width: 200px; padding: 6px 12px; font-size: 12px; }
.gantt-timeline-periods { display: flex; flex: 1; }
.gantt-period { padding: 6px 4px; text-align: center; font-size: 10px; font-weight: 600; color: var(--color-gray-500); text-transform: uppercase; border-left: 1px dashed var(--color-gray-200); }

.gantt-row { display: flex; border-bottom: 1px solid var(--color-gray-100); min-height: 36px; align-items: center; }
.gantt-row:hover { background: var(--color-gray-50); }
.milestone-row { background: var(--color-gray-50); }

.gantt-phase-label { display: flex; align-items: center; gap: 6px; }
.phase-code { font-family: var(--font-mono); font-size: 10px; color: var(--color-gray-400); }
.phase-name { font-size: 11px; font-weight: 500; color: var(--color-gray-700); }
.mandatory-badge { font-size: 8px; font-weight: 700; background: #FEF3C7; color: #92400E; padding: 1px 4px; border-radius: 3px; }

.gantt-timeline-area { flex: 1; position: relative; height: 28px; }
.gantt-bar { position: absolute; top: 4px; height: 20px; border-radius: 4px; cursor: grab; opacity: 0.85; transition: opacity 0.15s; display: flex; align-items: center; overflow: hidden; }
.gantt-bar:hover { opacity: 1; box-shadow: 0 2px 6px rgba(0,0,0,0.15); }
.bar-label { font-size: 9px; color: white; font-weight: 600; padding: 0 6px; white-space: nowrap; overflow: hidden; }

.gantt-milestone { position: absolute; top: 2px; transform: translateX(-6px); }
.milestone-diamond { display: inline-block; width: 0; height: 0; border-left: 6px solid transparent; border-right: 6px solid transparent; border-bottom: 10px solid #3B82F6; }
.milestone-label { font-size: 8px; color: var(--color-gray-600); position: absolute; top: 14px; left: -10px; white-space: nowrap; }

.gantt-edit-bar { display: flex; align-items: center; gap: 8px; padding: 8px 16px; background: #EFF6FF; border-top: 1px solid #BFDBFE; font-size: 12px; }
.date-input { padding: 4px 8px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 12px; }
.btn-save { padding: 4px 12px; background: var(--color-primary); color: white; border: none; border-radius: 4px; font-size: 11px; font-weight: 600; cursor: pointer; }
.btn-cancel { padding: 4px 12px; background: none; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 11px; cursor: pointer; }

.gantt-table { padding: 12px 16px; border-top: 1px solid var(--color-gray-200); }
.gantt-table table { width: 100%; font-size: 12px; border-collapse: collapse; }
.gantt-table th { font-size: 10px; font-weight: 600; text-transform: uppercase; color: var(--color-gray-500); padding: 4px 8px; text-align: left; border-bottom: 1px solid var(--color-gray-200); }
.gantt-table td { padding: 6px 8px; border-bottom: 1px solid var(--color-gray-100); cursor: pointer; }
.gantt-table tr:hover td { background: var(--color-gray-50); }
.text-right { text-align: right; }
.font-mono { font-family: var(--font-mono); }
.font-semibold { font-weight: 600; }
</style>
