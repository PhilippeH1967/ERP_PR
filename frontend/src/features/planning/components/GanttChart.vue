<script setup lang="ts">
/**
 * GanttChart — Project Gantt with today line, % advancement, tooltips, tasks.
 * Enriched version (Sprint UX — Alternative #1).
 */
import { ref, computed, onMounted } from 'vue'
import apiClient from '@/plugins/axios'
import PhaseSlideOver from './PhaseSlideOver.vue'
import TaskSlideOver from './TaskSlideOver.vue'

const props = defineProps<{ projectId: number }>()

const selectedPhaseId = ref<number | null>(null)
const showSlideOver = ref(false)
const selectedTaskId = ref<number | null>(null)
const showTaskSlideOver = ref(false)

function openPhasePanel(phaseId: number) {
  selectedPhaseId.value = phaseId
  showSlideOver.value = true
}

function openTaskPanel(taskId: number) {
  selectedTaskId.value = taskId
  showTaskSlideOver.value = true
}

function onSlideOverUpdated() {
  load() // refresh Gantt after changes
}

interface GanttPhase {
  id: number; name: string; client_label: string; code: string; type: string
  start_date: string | null; end_date: string | null
  billing_mode: string; budgeted_hours: number; is_mandatory: boolean; order: number
  tasks_budgeted_hours?: number; planned_hours?: number; actual_hours?: number
}
interface GanttMilestone { id: number; title: string; date: string; status: string; color: string }
interface GanttDependency { id: number; from: number; to: number; type: string; lag: number }
interface GanttTask {
  id: number; name: string; client_facing_label: string; wbs_code: string
  phase: number; budgeted_hours: number; actual_hours?: number; planned_hours?: number
  progress_pct?: number
  start_date: string | null; end_date: string | null
}

const phases = ref<GanttPhase[]>([])
const tasks = ref<GanttTask[]>([])
const milestones = ref<GanttMilestone[]>([])
const dependencies = ref<GanttDependency[]>([])
const projectInfo = ref({ code: '', name: '', start_date: '', end_date: '' })
const isLoading = ref(true)
const zoomLevel = ref<'month' | 'quarter' | 'year'>('quarter')
const showTasks = ref(false)
const hoveredItem = ref<{ id: number; type: string } | null>(null)
const tooltipPos = ref({ x: 0, y: 0 })

async function load() {
  isLoading.value = true
  try {
    const resp = await apiClient.get('gantt/project_gantt/', { params: { project_id: props.projectId } })
    const data = resp.data?.data || resp.data
    phases.value = data.phases || []
    milestones.value = data.milestones || []
    dependencies.value = data.dependencies || []
    projectInfo.value = data.project || { code: '', name: '', start_date: '', end_date: '' }
    // Load tasks with actual hours
    try {
      const tr = await apiClient.get(`projects/${props.projectId}/tasks/`)
      const td = tr.data?.data || tr.data
      tasks.value = Array.isArray(td) ? td : td?.results || []
    } catch { tasks.value = [] }
    // Load phase actual hours
    try {
      const pr = await apiClient.get(`projects/${props.projectId}/phases/`)
      const pd = pr.data?.data || pr.data
      const phaseData = Array.isArray(pd) ? pd : pd?.results || []
      for (const p of phases.value) {
        const match = phaseData.find((ph: Record<string, unknown>) => ph.id === p.id)
        if (match) {
          p.tasks_budgeted_hours = Number(match.tasks_budgeted_hours || 0)
          p.planned_hours = Number(match.planned_hours || 0)
          p.actual_hours = Number(match.actual_hours || 0)
        }
      }
    } catch { /* */ }
  } catch { /* */ }
  finally { isLoading.value = false }
}

onMounted(load)

const today = new Date()
const todayStr = today.toISOString().substring(0, 10)

// Timeline range
const timelineStart = computed(() => {
  const dates = phases.value.filter(p => p.start_date).map(p => new Date(p.start_date!))
  if (!dates.length) return new Date()
  const min = new Date(Math.min(...dates.map(d => d.getTime())))
  min.setDate(1)
  return min
})

const timelineEnd = computed(() => {
  const dates = phases.value.filter(p => p.end_date).map(p => new Date(p.end_date!))
  if (!dates.length) {
    const d = new Date(); d.setFullYear(d.getFullYear() + 2); return d
  }
  const max = new Date(Math.max(...dates.map(d => d.getTime())))
  max.setMonth(max.getMonth() + 3)
  return max
})

const totalDays = computed(() => Math.max(1, Math.round((timelineEnd.value.getTime() - timelineStart.value.getTime()) / 86400000)))

// Today marker position
const todayPosition = computed(() => {
  const t = today.getTime()
  if (t < timelineStart.value.getTime() || t > timelineEnd.value.getTime()) return -1
  return ((t - timelineStart.value.getTime()) / 86400000) / totalDays.value * 100
})

// Period headers
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
      const months = ['Jan', 'Fev', 'Mar', 'Avr', 'Mai', 'Jun', 'Jul', 'Aou', 'Sep', 'Oct', 'Nov', 'Dec']
      result.push({ label: `${months[d.getMonth()]} ${d.getFullYear()}`, width: (daySpan / totalDays.value) * 100 })
      d = new Date(d.getFullYear(), d.getMonth() + 1, 1)
    }
  } else {
    let y = start.getFullYear()
    while (y <= end.getFullYear()) {
      const yStart = new Date(y, 0, 1); const yEnd = new Date(y, 11, 31)
      const daySpan = Math.round((Math.min(yEnd.getTime(), end.getTime()) - Math.max(yStart.getTime(), start.getTime())) / 86400000)
      result.push({ label: String(y), width: (daySpan / totalDays.value) * 100 })
      y++
    }
  }
  return result
})

function barStyle(startDate: string | null, endDate: string | null) {
  if (!startDate || !endDate) return { display: 'none' }
  const s = new Date(startDate); const e = new Date(endDate)
  const left = ((s.getTime() - timelineStart.value.getTime()) / 86400000) / totalDays.value * 100
  const width = ((e.getTime() - s.getTime()) / 86400000) / totalDays.value * 100
  return { left: `${Math.max(0, left)}%`, width: `${Math.max(0.5, width)}%` }
}

function milestoneStyle(m: GanttMilestone) {
  const d = new Date(m.date)
  const left = ((d.getTime() - timelineStart.value.getTime()) / 86400000) / totalDays.value * 100
  return { left: `${left}%` }
}

// Phase advancement %
function phaseAdvancement(phase: GanttPhase): number {
  const budget = phase.tasks_budgeted_hours || phase.budgeted_hours || 0
  const actual = phase.actual_hours || 0
  if (budget <= 0) return 0
  return Math.min(100, Math.round((actual / budget) * 100))
}

function advancementColor(pct: number): string {
  if (pct < 50) return '#3B82F6'
  if (pct < 80) return '#16A34A'
  if (pct < 100) return '#D97706'
  return '#DC2626'
}

const phaseColors: Record<string, string> = { REALIZATION: '#3B82F6', SUPPORT: '#F59E0B' }

// Tasks for a phase
function phaseTasks(phaseId: number) {
  return tasks.value.filter(t => t.phase === phaseId)
}

function formatDate(d: string | null) {
  if (!d) return '—'
  return new Date(d).toLocaleDateString('fr-CA', { day: 'numeric', month: 'short', year: 'numeric' })
}

function durationWeeks(start: string | null, end: string | null) {
  if (!start || !end) return '—'
  return `${Math.round((new Date(end).getTime() - new Date(start).getTime()) / 86400000 / 7)} sem.`
}

function showTooltip(e: MouseEvent, id: number, type: string) {
  hoveredItem.value = { id, type }
  tooltipPos.value = { x: e.clientX + 10, y: e.clientY - 10 }
}
function hideTooltip() { hoveredItem.value = null }

const tooltipData = computed(() => {
  if (!hoveredItem.value) return null
  if (hoveredItem.value.type === 'phase') {
    const p = phases.value.find(ph => ph.id === hoveredItem.value!.id)
    if (!p) return null
    return {
      title: p.client_label || p.name,
      lines: [
        `${formatDate(p.start_date)} → ${formatDate(p.end_date)}`,
        `Duree: ${durationWeeks(p.start_date, p.end_date)}`,
        `Budget: ${(p.tasks_budgeted_hours || p.budgeted_hours || 0).toFixed(0)}h`,
        `Planifie: ${(p.planned_hours || 0).toFixed(0)}h`,
        `Reel: ${(p.actual_hours || 0).toFixed(1)}h`,
        `Avancement: ${phaseAdvancement(p)}%`,
      ],
    }
  }
  if (hoveredItem.value.type === 'task') {
    const t = tasks.value.find(tk => tk.id === hoveredItem.value!.id)
    if (!t) return null
    return {
      title: t.client_facing_label || t.name,
      lines: [
        `WBS: ${t.wbs_code}`,
        `Budget: ${(t.budgeted_hours || 0).toFixed(0)}h`,
        `Planifie: ${(t.planned_hours || 0).toFixed(0)}h`,
        `Reel: ${(t.actual_hours || 0).toFixed(1)}h`,
        `Avancement: ${t.progress_pct || 0}%`,
      ],
    }
  }
  return null
})
</script>

<template>
  <div class="gantt-container">
    <!-- Header -->
    <div class="gantt-header">
      <div>
        <h3>Gantt — {{ projectInfo.code }}</h3>
        <span class="gantt-subtitle">{{ projectInfo.name }}</span>
      </div>
      <div class="gantt-controls">
        <label class="gantt-toggle">
          <input v-model="showTasks" type="checkbox" />
          <span>Taches</span>
        </label>
        <button v-for="z in (['month', 'quarter', 'year'] as const)" :key="z" class="zoom-btn" :class="{ active: zoomLevel === z }" @click="zoomLevel = z">
          {{ z === 'month' ? 'Mois' : z === 'quarter' ? 'Trim.' : 'Annee' }}
        </button>
      </div>
    </div>

    <div v-if="isLoading" class="gantt-loading">Chargement...</div>
    <div v-else-if="!phases.length" class="gantt-empty">Aucune phase avec dates — configurez les dates dans l'onglet Phases</div>

    <div v-else class="gantt-body">
      <!-- Timeline header -->
      <div class="gantt-timeline-header">
        <div class="gantt-label-col gantt-label-header">Phase / Tache</div>
        <div class="gantt-timeline-periods">
          <div v-for="(p, i) in periods" :key="i" class="gantt-period" :style="{ width: p.width + '%' }">{{ p.label }}</div>
        </div>
      </div>

      <!-- Phase rows + task rows -->
      <template v-for="phase in phases" :key="phase.id">
        <!-- Phase bar -->
        <div class="gantt-row" :class="{ 'gantt-row-noDates': !phase.start_date }">
          <div class="gantt-label-col">
            <div class="gantt-phase-label">
              <span class="phase-code">{{ phase.code }}</span>
              <span class="phase-name">{{ phase.client_label || phase.name }}</span>
              <span class="phase-pct" :style="{ color: advancementColor(phaseAdvancement(phase)) }">{{ phaseAdvancement(phase) }}%</span>
            </div>
          </div>
          <div class="gantt-timeline-area">
            <!-- Today line -->
            <div v-if="todayPosition >= 0" class="gantt-today" :style="{ left: todayPosition + '%' }"></div>
            <!-- Phase bar with advancement fill -->
            <div
              class="gantt-bar"
              :style="{ ...barStyle(phase.start_date, phase.end_date), backgroundColor: '#E5E7EB' }"
              @mouseenter="showTooltip($event, phase.id, 'phase')"
              @mouseleave="hideTooltip"
              @click="openPhasePanel(phase.id)"
            >
              <!-- Advancement fill -->
              <div class="gantt-bar-fill" :style="{ width: phaseAdvancement(phase) + '%', backgroundColor: phaseColors[phase.type] || '#3B82F6' }"></div>
              <span class="bar-label">{{ phaseAdvancement(phase) }}%</span>
            </div>
            <!-- Milestones -->
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

        <!-- Task rows (if expanded) -->
        <template v-if="showTasks">
          <div v-for="task in phaseTasks(phase.id)" :key="'t-' + task.id" class="gantt-row gantt-task-row">
            <div class="gantt-label-col">
              <div class="gantt-task-label">
                <span class="task-wbs">{{ task.wbs_code }}</span>
                <span class="task-name">{{ task.client_facing_label || task.name }}</span>
              </div>
            </div>
            <div class="gantt-timeline-area">
              <div v-if="todayPosition >= 0" class="gantt-today" :style="{ left: todayPosition + '%' }"></div>
              <!-- Task bar: task dates preferred, phase dates as fallback -->
              <div
                v-if="(task.start_date || phase.start_date) && (task.end_date || phase.end_date)"
                class="gantt-bar gantt-bar-task"
                :style="{ ...barStyle(task.start_date || phase.start_date, task.end_date || phase.end_date), backgroundColor: '#E5E7EB' }"
                @mouseenter="showTooltip($event, task.id, 'task')"
                @mouseleave="hideTooltip"
                @click="openTaskPanel(task.id)"
              >
                <div class="gantt-bar-fill" :style="{ width: (task.progress_pct || 0) + '%', backgroundColor: advancementColor(task.progress_pct || 0) }"></div>
              </div>
            </div>
          </div>
        </template>
      </template>

      <!-- Milestones row -->
      <div v-if="milestones.length" class="gantt-row milestone-row">
        <div class="gantt-label-col"><span class="phase-name" style="font-style:italic;">Jalons</span></div>
        <div class="gantt-timeline-area">
          <div v-if="todayPosition >= 0" class="gantt-today" :style="{ left: todayPosition + '%' }"></div>
          <div v-for="m in milestones" :key="'mrow-' + m.id" class="gantt-milestone" :style="milestoneStyle(m)" :title="m.title">
            <span class="milestone-diamond" :style="{ borderBottomColor: m.color }"></span>
            <span class="milestone-label">{{ m.title }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Tooltip -->
    <div v-if="tooltipData" class="gantt-tooltip" :style="{ left: tooltipPos.x + 'px', top: tooltipPos.y + 'px' }">
      <div class="tooltip-title">{{ tooltipData.title }}</div>
      <div v-for="(line, i) in tooltipData.lines" :key="i" class="tooltip-line">{{ line }}</div>
    </div>

    <!-- Summary table -->
    <div v-if="phases.length" class="gantt-table">
      <table>
        <thead>
          <tr>
            <th>Phase</th>
            <th>Debut</th>
            <th>Fin</th>
            <th>Duree</th>
            <th class="text-center">H. budget</th>
            <th class="text-center">H. planif.</th>
            <th class="text-center">H. reel</th>
            <th class="text-center">Avanc.</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="phase in phases" :key="'tbl-' + phase.id" style="cursor:pointer;" @click="openPhasePanel(phase.id)">
            <td class="font-semibold" style="max-width:200px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">{{ phase.code }} — {{ phase.name }}</td>
            <td>{{ phase.start_date || '—' }}</td>
            <td>{{ phase.end_date || '—' }}</td>
            <td>{{ durationWeeks(phase.start_date, phase.end_date) }}</td>
            <td class="text-center font-mono">{{ (phase.tasks_budgeted_hours || phase.budgeted_hours || 0).toFixed(0) }}</td>
            <td class="text-center font-mono" :class="{ 'text-primary': (phase.planned_hours || 0) > 0 }">{{ (phase.planned_hours || 0).toFixed(0) }}</td>
            <td class="text-center font-mono" :class="{ 'font-semibold': (phase.actual_hours || 0) > 0 }">{{ (phase.actual_hours || 0).toFixed(1) }}</td>
            <td class="text-center">
              <span :style="{ color: advancementColor(phaseAdvancement(phase)), fontWeight: 600, fontSize: '12px' }">{{ phaseAdvancement(phase) }}%</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <!-- Phase planning slide-over -->
    <PhaseSlideOver
      :open="showSlideOver"
      :project-id="props.projectId"
      :phase-id="selectedPhaseId"
      @close="showSlideOver = false"
      @updated="onSlideOverUpdated"
    />
    <!-- Task planning slide-over -->
    <TaskSlideOver
      :open="showTaskSlideOver"
      :project-id="props.projectId"
      :task-id="selectedTaskId"
      @close="showTaskSlideOver = false"
      @updated="onSlideOverUpdated"
    />
  </div>
</template>

<style scoped>
.gantt-container { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); overflow: hidden; }
.gantt-header { display: flex; align-items: center; justify-content: space-between; padding: 12px 16px; border-bottom: 1px solid var(--color-gray-200); }
.gantt-header h3 { font-size: 14px; font-weight: 600; color: var(--color-gray-800); margin: 0; }
.gantt-subtitle { font-size: 11px; color: var(--color-gray-500); }
.gantt-controls { display: flex; align-items: center; gap: 8px; }
.gantt-toggle { display: flex; align-items: center; gap: 4px; font-size: 11px; color: var(--color-gray-600); cursor: pointer; margin-right: 8px; }
.gantt-toggle input { cursor: pointer; }
.zoom-btn { padding: 3px 10px; border-radius: 4px; font-size: 11px; font-weight: 600; border: 1px solid var(--color-gray-300); background: white; cursor: pointer; color: var(--color-gray-600); }
.zoom-btn.active { background: var(--color-primary); color: white; border-color: var(--color-primary); }
.gantt-loading, .gantt-empty { padding: 40px; text-align: center; color: var(--color-gray-400); font-size: 13px; }

.gantt-body { overflow-x: auto; }
.gantt-timeline-header { display: flex; border-bottom: 2px solid var(--color-gray-200); position: sticky; top: 0; background: white; z-index: 3; }
.gantt-label-col { width: 220px; min-width: 220px; padding: 6px 12px; font-size: 12px; }
.gantt-label-header { font-size: 10px; font-weight: 600; color: var(--color-gray-500); text-transform: uppercase; display: flex; align-items: center; }
.gantt-timeline-periods { display: flex; flex: 1; }
.gantt-period { padding: 6px 4px; text-align: center; font-size: 10px; font-weight: 600; color: var(--color-gray-500); text-transform: uppercase; border-left: 1px dashed var(--color-gray-200); }

.gantt-row { display: flex; border-bottom: 1px solid var(--color-gray-100); min-height: 34px; align-items: center; }
.gantt-row:hover { background: var(--color-gray-50); }
.gantt-row-noDates { opacity: 0.5; }
.gantt-task-row { min-height: 26px; background: var(--color-gray-50); }
.milestone-row { background: var(--color-gray-50); }

.gantt-phase-label { display: flex; align-items: center; gap: 6px; }
.phase-code { font-family: var(--font-mono); font-size: 9px; color: var(--color-gray-400); }
.phase-name { font-size: 11px; font-weight: 500; color: var(--color-gray-700); flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.phase-pct { font-size: 10px; font-weight: 700; font-family: var(--font-mono); }
.mandatory-badge { font-size: 8px; font-weight: 700; background: #FEF3C7; color: #92400E; padding: 1px 4px; border-radius: 3px; }

.gantt-task-label { display: flex; align-items: center; gap: 6px; padding-left: 20px; }
.task-wbs { font-family: var(--font-mono); font-size: 9px; color: var(--color-gray-400); }
.task-name { font-size: 10px; color: var(--color-gray-600); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

.gantt-timeline-area { flex: 1; position: relative; height: 28px; }
.gantt-task-row .gantt-timeline-area { height: 20px; }

/* Today line */
.gantt-today { position: absolute; top: 0; bottom: 0; width: 2px; background: #DC2626; z-index: 2; opacity: 0.7; }
.gantt-today::after { content: ''; position: absolute; top: -3px; left: -3px; width: 8px; height: 8px; background: #DC2626; border-radius: 50%; }

/* Bars */
.gantt-bar { position: absolute; top: 4px; height: 20px; border-radius: 4px; cursor: pointer; overflow: hidden; transition: box-shadow 0.15s; }
.gantt-bar:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.2); }
.gantt-bar-task { top: 3px; height: 14px; border-radius: 3px; }
.gantt-bar-fill { height: 100%; border-radius: 4px 0 0 4px; transition: width 0.3s; }
.bar-label { position: absolute; right: 4px; top: 50%; transform: translateY(-50%); font-size: 9px; color: var(--color-gray-600); font-weight: 700; z-index: 1; }

.gantt-milestone { position: absolute; top: 2px; transform: translateX(-6px); z-index: 1; }
.milestone-diamond { display: inline-block; width: 0; height: 0; border-left: 6px solid transparent; border-right: 6px solid transparent; border-bottom: 10px solid #3B82F6; }
.milestone-label { font-size: 8px; color: var(--color-gray-600); position: absolute; top: 14px; left: -10px; white-space: nowrap; }

/* Tooltip */
.gantt-tooltip { position: fixed; background: var(--color-gray-900); color: white; padding: 8px 12px; border-radius: 6px; font-size: 11px; z-index: 100; pointer-events: none; box-shadow: 0 4px 12px rgba(0,0,0,0.3); max-width: 280px; }
.tooltip-title { font-weight: 700; margin-bottom: 4px; font-size: 12px; }
.tooltip-line { color: #D1D5DB; line-height: 1.4; }

/* Summary table */
.gantt-table { padding: 12px 16px; border-top: 1px solid var(--color-gray-200); overflow-x: auto; }
.gantt-table table { width: 100%; font-size: 11px; border-collapse: collapse; min-width: 700px; }
.gantt-table th { font-size: 10px; font-weight: 600; text-transform: uppercase; color: var(--color-gray-500); padding: 4px 8px; text-align: left; border-bottom: 1px solid var(--color-gray-200); }
.gantt-table td { padding: 5px 8px; border-bottom: 1px solid var(--color-gray-100); cursor: pointer; }
.gantt-table tr:hover td { background: var(--color-gray-50); }
.text-right { text-align: right; }
.text-center { text-align: center; }
.text-primary { color: var(--color-primary); }
.font-mono { font-family: var(--font-mono); }
.font-semibold { font-weight: 600; }
</style>
