<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { timesheetApi } from '../api/timesheetApi'
import type { TimeEntry } from '../types/timesheet.types'

// Dashboard data
interface EmployeeRow {
  employee_id: number
  employee_name: string
  employee_initials: string
  project_hours: number
  total_week_hours: number
  trend_4w: number[]
  billable_rate: number
  projects: { project_id: number; hours: number; project_code: string; project_name: string }[]
  approval_id: number | null
  pm_status: string | null
  finance_status: string | null
  approved_by_other: string
}
interface ProjectInfo {
  id: number
  code: string
  name: string
  week_hours: number
  employee_count: number
}
interface KPIs {
  total_hours: number
  billable_rate: number
  billable_hours: number
  pending_count: number
  employee_count: number
}

const employees = ref<EmployeeRow[]>([])
const projects = ref<ProjectInfo[]>([])
const kpis = ref<KPIs>({ total_hours: 0, billable_rate: 0, billable_hours: 0, pending_count: 0, employee_count: 0 })
const weekStart = ref('')
const weekEnd = ref('')
const isLoading = ref(false)
const actionError = ref('')

// Slide-over detail
const detailEmployee = ref<EmployeeRow | null>(null)
const detailEntries = ref<TimeEntry[]>([])
const detailLoading = ref(false)

// Reject form
const rejectingId = ref<number | null>(null)
const rejectReason = ref('')

// Correction form
const correctingId = ref<number | null>(null)
const correctionMessage = ref('')

const weekDays = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']

function getWeekDates(): string[] {
  if (!weekStart.value) return []
  const start = new Date(weekStart.value + 'T00:00:00')
  return Array.from({ length: 7 }, (_, i) => {
    const d = new Date(start)
    d.setDate(d.getDate() + i)
    return d.toISOString().slice(0, 10)
  })
}

function formatDateShort(dateStr: string): string {
  const d = new Date(dateStr + 'T00:00:00')
  return `${d.getDate()}/${d.getMonth() + 1}`
}

// Sparkline: max height 100%, normalized to 40h
function sparkHeight(val: number): string {
  return Math.min(100, Math.round((val / 50) * 100)) + '%'
}
function sparkColor(val: number): string {
  if (val > 45) return 'high'
  if (val > 40) return 'warn'
  return 'ok'
}

const pendingEmployees = computed(() => employees.value.filter(e => e.pm_status === 'PENDING'))
const approvedEmployees = computed(() => employees.value.filter(e => e.pm_status === 'APPROVED'))

async function fetchDashboard() {
  isLoading.value = true
  try {
    const resp = await timesheetApi.pmDashboard()
    const data = resp.data?.data || resp.data
    employees.value = data.employees || []
    projects.value = data.projects || []
    kpis.value = data.kpis || {}
    weekStart.value = data.week_start || ''
    weekEnd.value = data.week_end || ''
  } finally {
    isLoading.value = false
  }
}

// Detail slide-over
async function showDetail(emp: EmployeeRow) {
  if (!emp.approval_id) return
  detailEmployee.value = emp
  detailLoading.value = true
  try {
    const resp = await timesheetApi.approvalEntries(emp.approval_id)
    detailEntries.value = resp.data?.data || resp.data || []
  } finally {
    detailLoading.value = false
  }
}
function hideDetail() {
  detailEmployee.value = null
  detailEntries.value = []
}

// Group detail entries by project — keep entry IDs for per-line actions
interface EntryCell {
  id: number
  hours: number
  status: string
}
interface PhaseGroup {
  phaseId: number | null
  phaseName: string
  entries: Record<string, EntryCell[]>  // date -> entries
  total: number
  entryIds: number[]  // all entry IDs for this phase
}
interface ProjectGroup {
  projectId: number
  projectCode: string
  projectName: string
  pmName: string
  isMyProject: boolean
  approvalColor: string
  phases: PhaseGroup[]
  dailyTotals: Record<string, number>
  total: number
  entryIds: number[]  // all entry IDs for this project
}
const detailGroups = computed<ProjectGroup[]>(() => {
  const map = new Map<number, ProjectGroup>()
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  for (const e of detailEntries.value as any[]) {
    if (!map.has(e.project)) {
      map.set(e.project, {
        projectId: e.project, projectCode: e.project_code, projectName: e.project_name,
        pmName: e.pm_name || '', isMyProject: e.is_my_project || false,
        approvalColor: e.approval_color || 'other',
        phases: [], dailyTotals: {}, total: 0, entryIds: [],
      })
    }
    const g = map.get(e.project)!
    let ph = g.phases.find(p => p.phaseId === e.phase)
    if (!ph) {
      ph = { phaseId: e.phase, phaseName: e.phase_name || 'Sans phase', entries: {}, total: 0, entryIds: [] }
      g.phases.push(ph)
    }
    const hrs = parseFloat(e.hours) || 0
    if (!ph.entries[e.date]) ph.entries[e.date] = []
    ph.entries[e.date].push({ id: e.id, hours: hrs, status: e.status })
    ph.total += hrs
    ph.entryIds.push(e.id)
    g.dailyTotals[e.date] = (g.dailyTotals[e.date] || 0) + hrs
    g.total += hrs
    g.entryIds.push(e.id)
  }
  return Array.from(map.values())
})

// Selected entries for batch actions
const selectedEntryIds = ref<Set<number>>(new Set())
function toggleEntry(id: number) {
  if (selectedEntryIds.value.has(id)) selectedEntryIds.value.delete(id)
  else selectedEntryIds.value.add(id)
  selectedEntryIds.value = new Set(selectedEntryIds.value) // trigger reactivity
}
function selectAllProject(group: ProjectGroup) {
  const submitted = group.entryIds.filter(id => {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const e = (detailEntries.value as any[]).find((x: any) => x.id === id)
    return e?.status === 'SUBMITTED'
  })
  const allSelected = submitted.every(id => selectedEntryIds.value.has(id))
  if (allSelected) submitted.forEach(id => selectedEntryIds.value.delete(id))
  else submitted.forEach(id => selectedEntryIds.value.add(id))
  selectedEntryIds.value = new Set(selectedEntryIds.value)
}

// Get hours total for a phase/date (sum of cells)
function phaseHours(cells: EntryCell[] | undefined): string {
  if (!cells || cells.length === 0) return '—'
  return String(cells.reduce((s, c) => s + c.hours, 0))
}
function cellStatus(cells: EntryCell[] | undefined): string {
  if (!cells || cells.length === 0) return ''
  return cells[0].status
}
function cellIds(cells: EntryCell[] | undefined): number[] {
  return (cells || []).map(c => c.id)
}

// Actions — per-entry
async function approveSelectedEntries() {
  actionError.value = ''
  const ids = Array.from(selectedEntryIds.value)
  if (!ids.length) return
  try {
    await timesheetApi.approveEntries(ids)
    selectedEntryIds.value = new Set()
    // Refresh detail
    if (detailEmployee.value?.approval_id) {
      const resp = await timesheetApi.approvalEntries(detailEmployee.value.approval_id)
      detailEntries.value = resp.data?.data || resp.data || []
    }
    await fetchDashboard()
  } catch (e: unknown) {
    actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur'
  }
}

async function rejectSelectedEntries() {
  actionError.value = ''
  const ids = Array.from(selectedEntryIds.value)
  if (!ids.length) return
  try {
    await timesheetApi.rejectEntries(ids, rejectReason.value)
    selectedEntryIds.value = new Set()
    rejectingId.value = null
    rejectReason.value = ''
    if (detailEmployee.value?.approval_id) {
      const resp = await timesheetApi.approvalEntries(detailEmployee.value.approval_id)
      detailEntries.value = resp.data?.data || resp.data || []
    }
    await fetchDashboard()
  } catch (e: unknown) {
    actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur'
  }
}

async function approveAllProject(group: ProjectGroup) {
  actionError.value = ''
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const ids = group.entryIds.filter(id => (detailEntries.value as any[]).find((x: any) => x.id === id)?.status === 'SUBMITTED')
  if (!ids.length) return
  try {
    await timesheetApi.approveEntries(ids)
    if (detailEmployee.value?.approval_id) {
      const resp = await timesheetApi.approvalEntries(detailEmployee.value.approval_id)
      detailEntries.value = resp.data?.data || resp.data || []
    }
    await fetchDashboard()
  } catch (e: unknown) {
    actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur'
  }
}

// Legacy per-approval actions (kept for batch from list)
async function approvePM(approvalId: number) {
  actionError.value = ''
  try {
    await timesheetApi.approvePM(approvalId)
    hideDetail()
    await fetchDashboard()
  } catch (e: unknown) {
    actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur'
  }
}

async function rejectPM(approvalId: number) {
  actionError.value = ''
  try {
    await timesheetApi.rejectPM(approvalId, rejectReason.value)
    rejectingId.value = null
    rejectReason.value = ''
    hideDetail()
    await fetchDashboard()
  } catch (e: unknown) {
    actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur'
  }
}

async function approveAll() {
  actionError.value = ''
  for (const emp of pendingEmployees.value) {
    if (emp.approval_id) {
      try {
        await timesheetApi.approvePM(emp.approval_id)
      } catch { /* continue */ }
    }
  }
  await fetchDashboard()
}

onMounted(fetchDashboard)
</script>

<template>
  <div>
    <h1 class="page-title">Validation des feuilles de temps</h1>

    <!-- KPI Cards -->
    <div class="kpi-row">
      <div v-for="proj in projects" :key="proj.id" class="kpi-card">
        <div class="kpi-label">{{ proj.code }} — {{ proj.name }}</div>
        <div class="kpi-value">{{ proj.week_hours }}h</div>
        <div class="kpi-sub">cette semaine ({{ proj.employee_count }} pers.)</div>
      </div>
      <div v-if="!projects.length" class="kpi-card">
        <div class="kpi-label">Projets</div>
        <div class="kpi-value">—</div>
        <div class="kpi-sub">Aucun projet gere</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Taux facturable</div>
        <div class="kpi-value text-primary">{{ kpis.billable_rate }}%</div>
        <div class="kpi-sub">{{ kpis.billable_hours }}h fact. / {{ kpis.total_hours }}h total</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-label">Feuilles a valider</div>
        <div class="kpi-value">{{ kpis.pending_count }}</div>
        <div class="kpi-sub">sur {{ kpis.employee_count }} employes</div>
      </div>
    </div>

    <div v-if="actionError" class="alert-error">{{ actionError }}</div>

    <!-- Employee table -->
    <div class="card-table">
      <div class="table-header">
        <h3>Heures a valider — Semaine du {{ weekStart }}</h3>
        <button v-if="pendingEmployees.length > 1" class="btn-batch" @click="approveAll">
          Approuver les {{ pendingEmployees.length }} en lot
        </button>
      </div>

      <table>
        <thead>
          <tr>
            <th class="text-left px-4">Employe</th>
            <th class="text-center">Heures projet</th>
            <th class="text-center">Heures totales sem.</th>
            <th class="text-center">Tendance 4 sem.</th>
            <th class="text-center">Taux fact.</th>
            <th class="text-center">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="emp in employees" :key="emp.employee_id" class="emp-row" :class="{ 'anomaly-row': emp.total_week_hours > 45 }">
            <td class="px-4 py-3">
              <div class="emp-cell">
                <div class="emp-avatar" :class="{ 'avatar-danger': emp.total_week_hours > 45 }">{{ emp.employee_initials }}</div>
                <div>
                  <div class="emp-name">{{ emp.employee_name }}</div>
                  <div v-if="emp.total_week_hours > 45" class="emp-alert">Surcharge detectee</div>
                  <div v-else-if="emp.pm_status === 'APPROVED'" class="emp-ok">Approuve par vous</div>
                  <div v-else-if="emp.pm_status === 'REJECTED'" class="emp-rejected">Rejete</div>
                  <div v-else-if="emp.approved_by_other" class="emp-pending">En attente — approuve par {{ emp.approved_by_other }}</div>
                  <div v-else class="emp-pending">En attente</div>
                </div>
              </div>
            </td>
            <td class="text-center py-3 font-semibold">{{ emp.project_hours }}h</td>
            <td class="text-center py-3">
              <span class="total-badge" :class="{ 'total-danger': emp.total_week_hours > 45, 'total-ok': emp.total_week_hours <= 45 }">
                {{ emp.total_week_hours }}h
              </span>
            </td>
            <td class="text-center py-3">
              <div class="sparkline">
                <div v-for="(val, i) in emp.trend_4w" :key="i" class="bar" :class="sparkColor(val)" :style="{ height: sparkHeight(val) }"></div>
              </div>
              <div class="trend-values">{{ emp.trend_4w.map(v => Math.round(v)).join(' → ') }}</div>
            </td>
            <td class="text-center py-3">
              <span class="font-medium text-primary">{{ emp.billable_rate }}%</span>
            </td>
            <td class="text-center py-3">
              <div class="action-btns">
                <!-- Approuver -->
                <button v-if="emp.pm_status === 'PENDING' && emp.approval_id" class="icon-btn approve" title="Approuver" @click="approvePM(emp.approval_id!)">
                  <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
                </button>
                <!-- Demander correction -->
                <button v-if="emp.pm_status === 'PENDING' && emp.approval_id" class="icon-btn correction" title="Demander modification" @click="rejectingId = rejectingId === emp.approval_id ? null : emp.approval_id!; rejectReason = ''">
                  <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
                </button>
                <!-- Voir detail -->
                <button v-if="emp.approval_id" class="icon-btn detail" title="Voir detail" @click="showDetail(emp)">
                  <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
                </button>
                <!-- Rejeter -->
                <button v-if="emp.pm_status === 'PENDING' && emp.approval_id" class="icon-btn reject" title="Rejeter" @click="rejectPM(emp.approval_id!)">
                  <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
                </button>
                <!-- Approved label -->
                <span v-if="emp.pm_status === 'APPROVED'" class="status-done">Approuve</span>
                <span v-if="emp.pm_status === 'REJECTED'" class="status-rejected">Rejete</span>
              </div>
            </td>
          </tr>
          <tr v-if="!employees.length && !isLoading">
            <td colspan="6" class="empty-state">Aucune feuille soumise sur vos projets cette semaine</td>
          </tr>
        </tbody>
      </table>

      <!-- Reject inline form -->
      <div v-if="rejectingId" class="reject-bar">
        <span class="reject-label">Motif de la demande de modification :</span>
        <input v-model="rejectReason" type="text" placeholder="Motif (optionnel)..." class="reject-input" />
        <button class="btn-danger-sm" @click="rejectPM(rejectingId!)">Confirmer</button>
        <button class="btn-ghost-sm" @click="rejectingId = null; rejectReason = ''">Annuler</button>
      </div>
    </div>

    <!-- ===== SLIDE-OVER DETAIL ===== -->
    <div v-if="detailEmployee" class="slide-overlay" @click="hideDetail">
      <div class="slide-panel" @click.stop>
        <div class="slide-header">
          <div class="flex items-center gap-3">
            <div class="detail-avatar">{{ detailEmployee.employee_initials }}</div>
            <div>
              <h3 class="detail-name">{{ detailEmployee.employee_name }}</h3>
              <div class="detail-sub">Semaine du {{ weekStart }}</div>
            </div>
          </div>
          <button class="close-btn" @click="hideDetail">
            <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
          </button>
        </div>

        <!-- Detail KPIs -->
        <div class="detail-kpis">
          <div class="detail-kpi">
            <div class="detail-kpi-val text-green-600">{{ detailEmployee.total_week_hours }}h</div>
            <div class="detail-kpi-label">Total sem.</div>
          </div>
          <div class="detail-kpi">
            <div class="detail-kpi-val">{{ detailEmployee.project_hours }}h</div>
            <div class="detail-kpi-label">Heures projet</div>
          </div>
          <div class="detail-kpi">
            <div class="detail-kpi-val">{{ Math.round(detailEmployee.total_week_hours - detailEmployee.project_hours) }}h</div>
            <div class="detail-kpi-label">Hors projet</div>
          </div>
          <div class="detail-kpi">
            <div class="detail-kpi-val">{{ detailEmployee.billable_rate }}%</div>
            <div class="detail-kpi-label">Taux fact.</div>
          </div>
        </div>

        <div v-if="detailLoading" class="detail-loading">Chargement...</div>
        <template v-else>
          <!-- Legende couleurs -->
          <div class="color-legend">
            <span class="legend-item"><span class="legend-dot dot-mine"></span> A approuver par vous (SUBMITTED)</span>
            <span class="legend-item"><span class="legend-dot dot-approved"></span> Approuve (PM_APPROVED)</span>
            <span class="legend-item"><span class="legend-dot dot-other"></span> Autre CP</span>
          </div>

          <!-- Per-project grids -->
          <div v-for="group in detailGroups" :key="group.projectId" class="detail-project" :class="'project-' + group.approvalColor">
            <div class="detail-project-header">
              <h4 class="detail-project-title">
                <span class="project-color-dot" :class="'dot-' + group.approvalColor"></span>
                {{ group.projectCode }} — {{ group.projectName }}
                <span v-if="group.pmName" class="pm-label">(CP: {{ group.pmName }})</span>
              </h4>
              <!-- Per-project quick actions -->
              <div v-if="group.isMyProject" class="project-actions">
                <button class="btn-sm-approve" @click="approveAllProject(group)" title="Approuver tout le projet">Approuver tout</button>
                <button class="btn-sm-select" @click="selectAllProject(group)">Tout selectionner</button>
              </div>
            </div>
            <table class="detail-table">
              <thead>
                <tr>
                  <th class="text-left">Tache / Phase</th>
                  <th v-for="(date, i) in getWeekDates()" :key="date" class="text-center day-th">
                    {{ weekDays[i] }}<br><span class="day-num">{{ formatDateShort(date) }}</span>
                  </th>
                  <th class="text-center total-th">Total</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="phase in group.phases" :key="phase.phaseId ?? 'none'">
                  <td class="task-td">{{ phase.phaseName }}</td>
                  <td v-for="date in getWeekDates()" :key="date"
                    class="hour-cell-action"
                    :class="{
                      'cell-submitted': cellStatus(phase.entries[date]) === 'SUBMITTED' && group.isMyProject,
                      'cell-approved': cellStatus(phase.entries[date]) === 'PM_APPROVED',
                      'cell-other': !group.isMyProject && cellStatus(phase.entries[date]) === 'SUBMITTED',
                    }">
                    <template v-if="phase.entries[date] && phase.entries[date].length > 0">
                      <div class="cell-content">
                        <span class="cell-hours">{{ phaseHours(phase.entries[date]) }}</span>
                        <!-- Checkbox on each day cell for my projects, only if SUBMITTED -->
                        <input
                          v-if="group.isMyProject && cellStatus(phase.entries[date]) === 'SUBMITTED'"
                          type="checkbox"
                          :checked="cellIds(phase.entries[date]).every(id => selectedEntryIds.has(id))"
                          class="cell-checkbox"
                          @change="cellIds(phase.entries[date]).forEach(id => toggleEntry(id))"
                        />
                        <!-- Approved indicator -->
                        <span v-if="cellStatus(phase.entries[date]) === 'PM_APPROVED'" class="cell-check-icon" title="Approuve">&#10003;</span>
                      </div>
                    </template>
                    <template v-else>
                      <span class="cell-empty">—</span>
                    </template>
                  </td>
                  <td class="total-td">{{ phase.total }}h</td>
                </tr>
                <tr class="group-total-row">
                  <td class="task-td font-semibold">Total {{ group.projectCode }}</td>
                  <td v-for="date in getWeekDates()" :key="date" class="hour-td font-semibold">
                    {{ group.dailyTotals[date] || '—' }}
                  </td>
                  <td class="total-td font-bold">{{ group.total }}h</td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Selected entries actions -->
          <div v-if="selectedEntryIds.size > 0" class="detail-actions">
            <button class="btn-approve-lg" @click="approveSelectedEntries">
              Approuver {{ selectedEntryIds.size }} ligne(s) selectionnee(s)
            </button>
            <button class="btn-correct-lg" @click="rejectingId = -1">
              Demander modification
            </button>
            <button class="btn-reject-lg" @click="rejectSelectedEntries">
              Rejeter
            </button>
          </div>

          <!-- Reject form for selected entries -->
          <div v-if="rejectingId === -1" class="correction-form">
            <input v-model="rejectReason" type="text" placeholder="Motif de la demande de modification..." class="correction-textarea" style="height:auto" />
            <div class="correction-btns">
              <button class="btn-danger-sm" @click="rejectSelectedEntries">Confirmer le rejet</button>
              <button class="btn-ghost-sm" @click="rejectingId = null; rejectReason = ''">Annuler</button>
            </div>
          </div>

          <div v-if="selectedEntryIds.size === 0 && detailGroups.every(g => !g.isMyProject)" class="detail-approved">
            Aucune ligne a approuver — projets geres par d'autres CP
          </div>

          <!-- Correction form in detail -->
          <div v-if="correctingId === detailEmployee?.approval_id" class="correction-form">
            <textarea v-model="correctionMessage" rows="2" placeholder="Decrivez la correction demandee..." class="correction-textarea"></textarea>
            <div class="correction-btns">
              <button class="btn-danger-sm" @click="rejectPM(correctingId!); correctingId = null; correctionMessage = ''">Envoyer et rejeter</button>
              <button class="btn-ghost-sm" @click="correctingId = null; correctionMessage = ''">Annuler</button>
            </div>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-title { font-size: 20px; font-weight: 700; color: var(--color-gray-900); margin-bottom: 16px; }

/* KPI Cards */
.kpi-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin-bottom: 16px; }
.kpi-card { background: white; border: 1px solid var(--color-gray-200); border-radius: 8px; padding: 16px; }
.kpi-label { font-size: 11px; color: var(--color-gray-500); margin-bottom: 4px; }
.kpi-value { font-size: 26px; font-weight: 700; color: var(--color-gray-900); }
.kpi-value.text-primary { color: var(--color-primary); }
.kpi-sub { font-size: 11px; color: var(--color-gray-500); margin-top: 2px; }

.alert-error { background: #FEE2E2; color: #DC2626; padding: 8px 12px; border-radius: 6px; font-size: 12px; margin-bottom: 12px; }

/* Table */
.card-table { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); overflow: hidden; }
.table-header { display: flex; align-items: center; justify-content: space-between; padding: 12px 16px; border-bottom: 1px solid var(--color-gray-200); background: var(--color-gray-50); }
.table-header h3 { font-size: 14px; font-weight: 600; color: var(--color-gray-900); }
.btn-batch { padding: 6px 14px; border-radius: 6px; font-size: 12px; font-weight: 600; background: var(--color-primary); color: white; border: none; cursor: pointer; }
.btn-batch:hover { opacity: 0.9; }

table { width: 100%; font-size: 13px; border-collapse: collapse; }
thead th { padding: 8px 12px; font-weight: 600; color: var(--color-gray-600); font-size: 11px; border-bottom: 1px solid var(--color-gray-200); background: var(--color-gray-50); }
tbody tr { border-bottom: 1px solid var(--color-gray-100); }
tbody tr:hover { background: var(--color-gray-50); }
.anomaly-row { background: #FEF2F2 !important; }
.anomaly-row:hover { background: #FEE2E2 !important; }

.emp-cell { display: flex; align-items: center; gap: 8px; }
.emp-avatar { width: 32px; height: 32px; border-radius: 50%; background: var(--color-primary-light); color: var(--color-primary); display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; }
.avatar-danger { background: #FEE2E2; color: #DC2626; }
.emp-name { font-size: 13px; font-weight: 600; color: var(--color-gray-900); }
.emp-alert { font-size: 10px; color: #DC2626; font-weight: 600; display: flex; align-items: center; gap: 3px; }
.emp-ok { font-size: 10px; color: #16A34A; }
.emp-rejected { font-size: 10px; color: #DC2626; }
.emp-pending { font-size: 10px; color: var(--color-gray-400); }

.total-badge { display: inline-flex; padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: 600; }
.total-ok { background: #DCFCE7; color: #15803D; }
.total-danger { background: #FEE2E2; color: #DC2626; }

/* Sparkline */
.sparkline { display: flex; align-items: flex-end; gap: 3px; height: 28px; justify-content: center; }
.bar { width: 6px; border-radius: 2px; min-height: 3px; }
.bar.ok { background: #22C55E; }
.bar.warn { background: #F59E0B; }
.bar.high { background: #EF4444; }
.trend-values { font-size: 9px; color: var(--color-gray-400); margin-top: 2px; }

/* Action buttons */
.action-btns { display: flex; align-items: center; gap: 4px; justify-content: center; }
.icon-btn { width: 30px; height: 30px; border-radius: 6px; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; }
.icon-btn.approve { background: #DCFCE7; color: #16A34A; }
.icon-btn.approve:hover { background: #BBF7D0; }
.icon-btn.correction { background: #FEF3C7; color: #D97706; }
.icon-btn.correction:hover { background: #FDE68A; }
.icon-btn.detail { background: var(--color-gray-100); color: var(--color-gray-600); }
.icon-btn.detail:hover { background: var(--color-gray-200); }
.icon-btn.reject { background: #FEE2E2; color: #DC2626; }
.icon-btn.reject:hover { background: #FECACA; }
.status-done { font-size: 11px; color: #16A34A; font-weight: 600; }
.status-rejected { font-size: 11px; color: #DC2626; font-weight: 600; }

/* Reject bar */
.reject-bar { display: flex; align-items: center; gap: 8px; padding: 10px 16px; background: #FEF3C7; border-top: 1px solid #FCD34D; }
.reject-label { font-size: 12px; color: #92400E; font-weight: 600; white-space: nowrap; }
.reject-input { flex: 1; padding: 6px 10px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 12px; }
.btn-danger-sm { padding: 5px 12px; border-radius: 4px; font-size: 11px; font-weight: 600; cursor: pointer; border: none; background: #DC2626; color: white; }
.btn-ghost-sm { padding: 5px 12px; border-radius: 4px; font-size: 11px; cursor: pointer; background: none; border: 1px solid var(--color-gray-300); color: var(--color-gray-600); }

.empty-state { text-align: center; padding: 40px; color: var(--color-gray-400); font-size: 14px; }

/* ===== SLIDE-OVER ===== */
.slide-overlay { position: fixed; inset: 0; z-index: 50; background: rgba(0,0,0,0.3); }
.slide-panel { position: absolute; right: 0; top: 0; bottom: 0; width: 680px; max-width: 90vw; background: white; box-shadow: -4px 0 20px rgba(0,0,0,0.15); overflow-y: auto; padding: 24px; }
.slide-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; }
.detail-avatar { width: 48px; height: 48px; border-radius: 50%; background: #DCFCE7; color: #16A34A; display: flex; align-items: center; justify-content: center; font-size: 14px; font-weight: 700; }
.detail-name { font-size: 18px; font-weight: 600; color: var(--color-gray-900); }
.detail-sub { font-size: 13px; color: var(--color-gray-500); }
.close-btn { padding: 8px; border-radius: 6px; border: none; background: none; cursor: pointer; color: var(--color-gray-500); }
.close-btn:hover { background: var(--color-gray-100); }

/* Detail KPIs */
.detail-kpis { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 20px; }
.detail-kpi { background: var(--color-gray-50); border-radius: 8px; padding: 12px; text-align: center; }
.detail-kpi-val { font-size: 18px; font-weight: 700; color: var(--color-gray-900); }
.detail-kpi-label { font-size: 10px; color: var(--color-gray-500); }

.detail-loading { text-align: center; padding: 30px; color: var(--color-gray-400); }

/* Detail project sections */
.detail-project { margin-bottom: 20px; }
.detail-project-title { font-size: 13px; font-weight: 700; color: var(--color-gray-700); margin-bottom: 8px; }
.detail-table { width: 100%; border-collapse: collapse; font-size: 11px; border: 1px solid var(--color-gray-200); border-radius: 6px; overflow: hidden; }
.detail-table thead { background: var(--color-gray-50); }
.detail-table th { padding: 5px 6px; font-weight: 600; color: var(--color-gray-600); border-bottom: 1px solid var(--color-gray-200); }
.day-th { width: 50px; }
.day-num { font-size: 9px; font-weight: 400; color: var(--color-gray-400); }
.total-th { width: 60px; background: var(--color-gray-100); }
.task-td { padding: 5px 8px; color: var(--color-gray-700); }
.hour-td { padding: 5px 6px; text-align: center; color: var(--color-gray-600); }
.total-td { padding: 5px 6px; text-align: center; font-weight: 600; background: var(--color-gray-50); }
.detail-table tbody tr { border-bottom: 1px solid var(--color-gray-100); }
.group-total-row { background: var(--color-primary-light); }
.group-total-row .task-td { color: var(--color-primary); }
.group-total-row .hour-td { color: var(--color-primary); }
.group-total-row .total-td { color: var(--color-primary); background: rgba(37,99,235,0.1); }

/* Detail actions */
.detail-actions { display: flex; gap: 8px; margin-top: 16px; padding: 12px; background: var(--color-primary-light); border-radius: 8px; border: 1px solid rgba(37,99,235,0.15); }
.btn-approve-lg { flex: 1; padding: 10px; border-radius: 8px; font-size: 13px; font-weight: 600; background: #16A34A; color: white; border: none; cursor: pointer; }
.btn-approve-lg:hover { background: #15803D; }
.btn-correct-lg { padding: 10px 16px; border-radius: 8px; font-size: 13px; font-weight: 600; background: #FEF3C7; color: #92400E; border: 1px solid #FCD34D; cursor: pointer; }
.btn-correct-lg:hover { background: #FDE68A; }
.btn-reject-lg { padding: 10px 16px; border-radius: 8px; font-size: 13px; font-weight: 600; background: #FEE2E2; color: #DC2626; border: 1px solid #FECACA; cursor: pointer; }
.btn-reject-lg:hover { background: #FECACA; }
.detail-approved { padding: 12px; text-align: center; font-size: 14px; font-weight: 600; color: #16A34A; background: #DCFCE7; border-radius: 8px; margin-top: 16px; }

.correction-form { margin-top: 12px; padding: 12px; background: #FEF3C7; border: 1px solid #FCD34D; border-radius: 8px; }
.correction-textarea { width: 100%; padding: 8px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 12px; resize: vertical; margin-bottom: 8px; }
.correction-btns { display: flex; gap: 8px; }

/* Color legend */
.color-legend { display: flex; gap: 16px; margin-bottom: 14px; padding: 8px 12px; background: var(--color-gray-50); border-radius: 6px; border: 1px solid var(--color-gray-200); }
.legend-item { display: flex; align-items: center; gap: 5px; font-size: 11px; color: var(--color-gray-600); }
.legend-dot { width: 10px; height: 10px; border-radius: 50%; }

/* Project color coding */
.dot-mine { background: var(--color-primary); }
.dot-approved { background: #22C55E; }
.dot-other { background: var(--color-gray-400); }

.project-color-dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; margin-right: 4px; vertical-align: middle; }
.pm-label { font-size: 11px; font-weight: 400; color: var(--color-gray-400); margin-left: 4px; }

/* Project section borders by color */
.project-mine { border-left: 3px solid var(--color-primary); padding-left: 12px; }
.project-approved { border-left: 3px solid #22C55E; padding-left: 12px; }
.project-other { border-left: 3px solid var(--color-gray-300); padding-left: 12px; opacity: 0.75; }
.project-other .detail-table { background: var(--color-gray-50); }

/* Project header with actions */
.detail-project-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; }
.project-actions { display: flex; gap: 6px; }
.btn-sm-approve { padding: 3px 10px; border-radius: 4px; font-size: 10px; font-weight: 600; background: #DCFCE7; color: #16A34A; border: none; cursor: pointer; }
.btn-sm-approve:hover { background: #BBF7D0; }
.btn-sm-select { padding: 3px 10px; border-radius: 4px; font-size: 10px; font-weight: 600; background: var(--color-gray-100); color: var(--color-gray-600); border: none; cursor: pointer; }

/* Cell with inline checkbox */
.hour-cell-action { padding: 0; text-align: center; position: relative; }
.cell-content { display: flex; align-items: center; justify-content: center; gap: 3px; padding: 4px 4px; min-height: 28px; }
.cell-hours { font-size: 12px; }
.cell-checkbox { width: 13px; height: 13px; cursor: pointer; accent-color: var(--color-primary); flex-shrink: 0; }
.cell-check-icon { color: #16A34A; font-size: 12px; font-weight: 700; flex-shrink: 0; }
.cell-empty { color: var(--color-gray-300); font-size: 11px; padding: 4px; display: block; }

/* Cell colors */
.cell-submitted { background: rgba(37, 99, 235, 0.08); }
.cell-approved { background: rgba(34, 197, 94, 0.12); }
.cell-approved .cell-hours { color: #15803D; }
.cell-other { background: var(--color-gray-50); }
.cell-other .cell-hours { color: var(--color-gray-400); }
</style>
