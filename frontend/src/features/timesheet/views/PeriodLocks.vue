<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import apiClient from '@/plugins/axios'
import { useAuth } from '@/shared/composables/useAuth'

const { currentUser } = useAuth()
const userRoles = computed(() => currentUser.value?.roles || [])
const canManage = computed(() =>
  userRoles.value.includes('PAIE') || userRoles.value.includes('FINANCE') || userRoles.value.includes('ADMIN')
)

interface WeekSummary {
  week_start: string
  week_end: string
  entry_count: number
  total_hours: number
  employee_count: number
  statuses: string[]
  status: 'open' | 'partial' | 'locked'
}
interface PeriodUnlock {
  id: number
  period_start: string
  period_end: string
  reason: string
  justification: string
  unlocked_by: number
  unlocked_at: string
}
interface TaskLock {
  id: number
  project: number
  project_name: string
  project_code: string
  phase: number | null
  phase_name: string
  lock_type: string
  locked_by: number
  locked_by_name: string
  locked_at: string
}
interface ProjectOption {
  id: number
  code: string
  name: string
}
interface PhaseOption {
  id: number
  name: string
}

const weeks = ref<WeekSummary[]>([])
const unlocks = ref<PeriodUnlock[]>([])
const taskLocks = ref<TaskLock[]>([])
const isLoading = ref(false)
const actionError = ref('')
const actionSuccess = ref('')

// Lock before form
const showLockBefore = ref(false)
const lockBeforeDate = ref('')

// Task lock form
const showTaskLockForm = ref(false)
const taskLockProjectId = ref<number | null>(null)
const taskLockPhaseId = ref<number | null>(null)
const projectOptions = ref<ProjectOption[]>([])
const phaseOptions = ref<PhaseOption[]>([])
const loadingPhases = ref(false)
const projectSearch = ref('')

const filteredProjects = computed(() => {
  if (!projectSearch.value) return projectOptions.value
  const q = projectSearch.value.toLowerCase()
  return projectOptions.value.filter(
    p => p.name.toLowerCase().includes(q) || p.code.toLowerCase().includes(q)
  )
})

// Unlock form
const showUnlockForm = ref(false)
const unlockWeekStart = ref('')
const unlockWeekEnd = computed(() => {
  if (!unlockWeekStart.value) return ''
  const d = new Date(unlockWeekStart.value + 'T00:00:00')
  d.setDate(d.getDate() + 6)
  return d.toISOString().slice(0, 10)
})
const unlockReason = ref('CORRECTION')
const unlockJustification = ref('')

async function fetchData() {
  isLoading.value = true
  try {
    const [weeksResp, unlocksResp, locksResp, projectsResp] = await Promise.all([
      apiClient.get('time_entries/period_summary/'),
      apiClient.get('period_unlocks/'),
      apiClient.get('timesheet_locks/'),
      apiClient.get('projects/', { params: { status: 'ACTIVE' } }),
    ])
    weeks.value = (weeksResp.data?.data || weeksResp.data)?.weeks || []
    unlocks.value = unlocksResp.data?.data || unlocksResp.data || []
    const locksData = locksResp.data?.data || locksResp.data
    taskLocks.value = Array.isArray(locksData) ? locksData : locksData?.results || []
    const projData = projectsResp.data?.data || projectsResp.data
    projectOptions.value = Array.isArray(projData) ? projData : projData?.results || []
  } finally {
    isLoading.value = false
  }
}

async function onProjectSelect(projectId: number) {
  taskLockProjectId.value = projectId
  taskLockPhaseId.value = null
  phaseOptions.value = []
  if (!projectId) return
  loadingPhases.value = true
  try {
    const resp = await apiClient.get(`projects/${projectId}/phases/`)
    const data = resp.data?.data || resp.data
    phaseOptions.value = Array.isArray(data) ? data : data?.results || []
  } finally {
    loadingPhases.value = false
  }
}

async function createTaskLock() {
  actionError.value = ''
  actionSuccess.value = ''
  if (!taskLockProjectId.value) {
    actionError.value = 'Selectionnez un projet'
    return
  }
  try {
    const payload: Record<string, unknown> = {
      project: taskLockProjectId.value,
      lock_type: 'PHASE',
    }
    if (taskLockPhaseId.value) {
      payload.phase = taskLockPhaseId.value
    }
    await apiClient.post('timesheet_locks/', payload)
    actionSuccess.value = 'Verrouillage par tache cree'
    showTaskLockForm.value = false
    taskLockProjectId.value = null
    taskLockPhaseId.value = null
    projectSearch.value = ''
    await fetchData()
  } catch (e: unknown) {
    actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur lors de la creation du verrouillage'
  }
}

async function deleteTaskLock(id: number) {
  actionError.value = ''
  try {
    await apiClient.delete(`timesheet_locks/${id}/`)
    actionSuccess.value = 'Verrouillage supprime'
    await fetchData()
  } catch {
    actionError.value = 'Erreur lors de la suppression du verrouillage'
  }
}

async function lockWeek(week: WeekSummary) {
  actionError.value = ''
  actionSuccess.value = ''
  try {
    await apiClient.post('time_entries/lock_period/', {
      period_start: week.week_start,
      period_end: week.week_end,
    })
    actionSuccess.value = `Semaine du ${week.week_start} verrouillée`
    await fetchData()
  } catch (e: unknown) {
    actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur'
  }
}

async function lockAllBefore() {
  actionError.value = ''
  actionSuccess.value = ''
  if (!lockBeforeDate.value) { actionError.value = 'Selectionnez une date'; return }
  try {
    const resp = await apiClient.post('time_entries/lock_before/', { before_date: lockBeforeDate.value })
    const data = resp.data?.data || resp.data
    actionSuccess.value = `${data.locked_count} entrée(s) verrouillée(s) avant le ${lockBeforeDate.value}`
    showLockBefore.value = false
    lockBeforeDate.value = ''
    await fetchData()
  } catch (e: unknown) {
    actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur'
  }
}

async function createUnlock() {
  actionError.value = ''
  actionSuccess.value = ''
  if (!unlockWeekStart.value) { actionError.value = 'Selectionnez un dimanche'; return }
  const d = new Date(unlockWeekStart.value + 'T00:00:00')
  if (d.getDay() !== 0) { actionError.value = 'La date doit etre un dimanche'; return }
  try {
    // 1. Revert LOCKED entries to PM_APPROVED
    await apiClient.post('time_entries/unlock_period/', {
      period_start: unlockWeekStart.value,
      period_end: unlockWeekEnd.value,
    })
    // 2. Record the unlock for audit trail
    await apiClient.post('period_unlocks/', {
      period_start: unlockWeekStart.value,
      period_end: unlockWeekEnd.value,
      reason: unlockReason.value,
      justification: unlockJustification.value,
    })
    actionSuccess.value = `Semaine du ${unlockWeekStart.value} déverrouillée`
    showUnlockForm.value = false
    unlockWeekStart.value = ''
    unlockJustification.value = ''
    await fetchData()
  } catch (e: unknown) {
    actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur'
  }
}

async function unlockWeekDirect(week: WeekSummary) {
  unlockWeekStart.value = week.week_start
  showUnlockForm.value = true
  showLockBefore.value = false
}

async function deleteUnlock(id: number) {
  try {
    await apiClient.delete(`period_unlocks/${id}/`)
    await fetchData()
  } catch {
    actionError.value = 'Erreur lors de la suppression'
  }
}

function formatDate(d: string) {
  if (!d) return ''
  const dt = new Date(d + 'T00:00:00')
  return dt.toLocaleDateString('fr-CA', { day: 'numeric', month: 'short' })
}
function formatDateTime(d: string) {
  if (!d) return ''
  return new Date(d).toLocaleString('fr-CA', { dateStyle: 'short', timeStyle: 'short' })
}

const openWeeks = computed(() => weeks.value.filter(w => w.status !== 'locked'))
const lockedWeeks = computed(() => weeks.value.filter(w => w.status === 'locked'))

onMounted(fetchData)
</script>

<template>
  <div>
    <div class="page-header">
      <h1>Verrouillage des periodes</h1>
      <div v-if="canManage" class="flex gap-2">
        <button class="btn-lock-all" @click="showLockBefore = !showLockBefore; showUnlockForm = false">
          Fermer les periodes anterieures
        </button>
        <button class="btn-unlock" @click="showUnlockForm = !showUnlockForm; showLockBefore = false">
          Deverrouiller une semaine
        </button>
      </div>
    </div>

    <!-- Messages -->
    <div v-if="actionError" class="alert-error">{{ actionError }}</div>
    <div v-if="actionSuccess" class="alert-success">{{ actionSuccess }}</div>

    <!-- Lock before form -->
    <div v-if="showLockBefore" class="form-card">
      <h3 class="form-title">Fermer toutes les periodes anterieures</h3>
      <p class="form-desc">Toutes les feuilles de temps avant cette date seront verrouillées definitivement.</p>
      <div class="form-row">
        <div class="form-field">
          <label>Verrouiller tout avant le</label>
          <input v-model="lockBeforeDate" type="date" />
        </div>
      </div>
      <div v-if="lockBeforeDate" class="form-preview-danger">
        Toutes les entrees avant le {{ lockBeforeDate }} seront verrouillees ({{ openWeeks.filter(w => w.week_end < lockBeforeDate).length }} semaine(s) concernee(s))
      </div>
      <div class="form-actions">
        <button class="btn-danger" @click="lockAllBefore">Verrouiller</button>
        <button class="btn-ghost" @click="showLockBefore = false">Annuler</button>
      </div>
    </div>

    <!-- Unlock form -->
    <div v-if="showUnlockForm" class="form-card">
      <h3 class="form-title">Deverrouiller une semaine</h3>
      <p class="form-desc">Autorise temporairement les corrections. Choisissez le dimanche de debut.</p>
      <div class="form-row">
        <div class="form-field">
          <label>Dimanche (debut)</label>
          <input v-model="unlockWeekStart" type="date" />
        </div>
        <div class="form-field">
          <label>Samedi (fin)</label>
          <input :value="unlockWeekEnd" type="date" disabled />
        </div>
        <div class="form-field">
          <label>Motif</label>
          <select v-model="unlockReason">
            <option value="CORRECTION">Correction</option>
            <option value="AMENDMENT">Avenant</option>
            <option value="AUDIT">Audit</option>
          </select>
        </div>
      </div>
      <div class="form-field">
        <label>Justification</label>
        <textarea v-model="unlockJustification" rows="2" placeholder="Motif detaille..."></textarea>
      </div>
      <div class="form-actions">
        <button class="btn-success" @click="createUnlock">Deverrouiller</button>
        <button class="btn-ghost" @click="showUnlockForm = false">Annuler</button>
      </div>
    </div>

    <!-- Weeks with entries -->
    <div class="section-card">
      <div class="section-header">
        <h3>Periodes avec feuilles de temps</h3>
        <span class="section-count">{{ weeks.length }} semaine(s)</span>
      </div>
      <table v-if="weeks.length">
        <thead>
          <tr>
            <th>Semaine</th>
            <th class="text-center">Employes</th>
            <th class="text-center">Entrees</th>
            <th class="text-center">Heures</th>
            <th class="text-center">Statut</th>
            <th v-if="canManage" class="text-center">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="week in weeks" :key="week.week_start" :class="{ 'row-locked': week.status === 'locked' }">
            <td class="font-mono">
              <span class="week-range">{{ formatDate(week.week_start) }} → {{ formatDate(week.week_end) }}</span>
            </td>
            <td class="text-center">{{ week.employee_count }}</td>
            <td class="text-center">{{ week.entry_count }}</td>
            <td class="text-center font-semibold">{{ week.total_hours }}h</td>
            <td class="text-center">
              <span v-if="week.status === 'locked'" class="status-badge locked">Verrouillee</span>
              <span v-else-if="week.status === 'partial'" class="status-badge partial">Partiel</span>
              <span v-else class="status-badge open">Ouverte</span>
            </td>
            <td v-if="canManage" class="text-center">
              <button v-if="week.status !== 'locked'" class="btn-sm-lock" @click="lockWeek(week)">Verrouiller</button>
              <button v-else class="btn-sm-unlock" @click="unlockWeekDirect(week)">Deverrouiller</button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="empty">Aucune feuille de temps enregistree</div>
    </div>

    <!-- Unlock history -->
    <div class="section-card">
      <div class="section-header">
        <h3>Historique des deverrouillages</h3>
      </div>
      <table v-if="unlocks.length">
        <thead>
          <tr>
            <th>Periode</th>
            <th>Motif</th>
            <th>Justification</th>
            <th>Date</th>
            <th v-if="canManage">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="u in unlocks" :key="u.id">
            <td class="font-mono">{{ formatDate(u.period_start) }} → {{ formatDate(u.period_end) }}</td>
            <td>
              <span class="reason-badge" :class="'reason-' + u.reason.toLowerCase()">{{ u.reason }}</span>
            </td>
            <td class="text-muted">{{ u.justification || '—' }}</td>
            <td class="text-muted font-mono">{{ formatDateTime(u.unlocked_at) }}</td>
            <td v-if="canManage">
              <button class="btn-sm-revoke" @click="deleteUnlock(u.id)">Revoquer</button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="empty">Aucun deverrouillage enregistre</div>
    </div>

    <!-- Task/Phase locking -->
    <div class="section-card">
      <div class="section-header">
        <h3>Verrouillage par tache</h3>
        <button v-if="canManage" class="btn-add-task-lock" @click="showTaskLockForm = !showTaskLockForm">
          {{ showTaskLockForm ? 'Annuler' : 'Nouveau verrouillage' }}
        </button>
      </div>

      <!-- Create task lock form -->
      <div v-if="showTaskLockForm && canManage" class="form-card form-card-inline">
        <div class="form-row">
          <div class="form-field">
            <label>Projet</label>
            <input
              v-model="projectSearch"
              type="text"
              placeholder="Rechercher un projet..."
              class="search-input"
            />
            <select
              :value="taskLockProjectId"
              @change="onProjectSelect(Number(($event.target as HTMLSelectElement).value))"
              class="project-select"
            >
              <option :value="null" disabled selected>-- Choisir un projet --</option>
              <option v-for="p in filteredProjects" :key="p.id" :value="p.id">
                {{ p.code }} — {{ p.name }}
              </option>
            </select>
          </div>
          <div class="form-field">
            <label>Phase (optionnel)</label>
            <select v-model="taskLockPhaseId" :disabled="!taskLockProjectId || loadingPhases">
              <option :value="null">-- Toutes les phases --</option>
              <option v-for="ph in phaseOptions" :key="ph.id" :value="ph.id">
                {{ ph.name }}
              </option>
            </select>
            <span v-if="loadingPhases" class="text-muted" style="font-size: 10px;">Chargement...</span>
          </div>
        </div>
        <div class="form-actions">
          <button class="btn-danger" @click="createTaskLock">Verrouiller</button>
          <button class="btn-ghost" @click="showTaskLockForm = false">Annuler</button>
        </div>
      </div>

      <!-- Task locks list -->
      <table v-if="taskLocks.length">
        <thead>
          <tr>
            <th>Projet</th>
            <th>Phase</th>
            <th>Verrouille par</th>
            <th>Date</th>
            <th v-if="canManage">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="lock in taskLocks" :key="lock.id">
            <td>
              <span class="font-semibold">{{ lock.project_code }}</span>
              <span class="text-muted"> — {{ lock.project_name }}</span>
            </td>
            <td>{{ lock.phase_name || 'Toutes' }}</td>
            <td class="text-muted">{{ lock.locked_by_name }}</td>
            <td class="text-muted font-mono">{{ formatDateTime(lock.locked_at) }}</td>
            <td v-if="canManage">
              <button class="btn-sm-revoke" @click="deleteTaskLock(lock.id)">Supprimer</button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="empty">Aucun verrouillage par tache</div>
    </div>
  </div>
</template>

<style scoped>
.page-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }
.page-header h1 { font-size: 20px; font-weight: 700; color: var(--color-gray-900); }

.btn-lock-all { padding: 6px 14px; border-radius: 6px; font-size: 12px; font-weight: 600; background: #DC2626; color: white; border: none; cursor: pointer; }
.btn-lock-all:hover { background: #B91C1C; }
.btn-unlock { padding: 6px 14px; border-radius: 6px; font-size: 12px; font-weight: 600; background: #16A34A; color: white; border: none; cursor: pointer; }
.btn-unlock:hover { background: #15803D; }

.alert-error { background: #FEE2E2; color: #DC2626; padding: 8px 12px; border-radius: 6px; font-size: 12px; margin-bottom: 12px; }
.alert-success { background: #DCFCE7; color: #15803D; padding: 8px 12px; border-radius: 6px; font-size: 12px; margin-bottom: 12px; }

/* Forms */
.form-card { background: white; border: 1px solid var(--color-gray-200); border-radius: 8px; padding: 16px; margin-bottom: 16px; }
.form-title { font-size: 14px; font-weight: 600; color: var(--color-gray-900); margin-bottom: 4px; }
.form-desc { font-size: 12px; color: var(--color-gray-500); margin-bottom: 12px; }
.form-row { display: flex; gap: 12px; margin-bottom: 8px; }
.form-field { flex: 1; }
.form-field label { display: block; font-size: 11px; font-weight: 600; color: var(--color-gray-600); margin-bottom: 4px; }
.form-field input, .form-field select, .form-field textarea { width: 100%; padding: 6px 10px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 12px; }
.form-field textarea { resize: vertical; }
.form-preview-danger { padding: 8px 12px; background: #FEF2F2; border: 1px solid #FECACA; color: #DC2626; border-radius: 4px; font-size: 12px; font-weight: 600; margin: 8px 0; }
.form-actions { display: flex; gap: 8px; margin-top: 12px; }
.btn-danger { padding: 6px 14px; border-radius: 6px; font-size: 12px; font-weight: 600; background: #DC2626; color: white; border: none; cursor: pointer; }
.btn-success { padding: 6px 14px; border-radius: 6px; font-size: 12px; font-weight: 600; background: #16A34A; color: white; border: none; cursor: pointer; }
.btn-ghost { padding: 6px 14px; border-radius: 6px; font-size: 12px; font-weight: 600; background: none; border: 1px solid var(--color-gray-300); color: var(--color-gray-600); cursor: pointer; }

/* Sections */
.section-card { background: white; border: 1px solid var(--color-gray-200); border-radius: 8px; overflow: hidden; margin-bottom: 16px; }
.section-header { display: flex; align-items: center; justify-content: space-between; padding: 12px 16px; border-bottom: 1px solid var(--color-gray-200); background: var(--color-gray-50); }
.section-header h3 { font-size: 13px; font-weight: 600; color: var(--color-gray-900); }
.section-count { font-size: 11px; color: var(--color-gray-500); }

table { width: 100%; font-size: 12px; border-collapse: collapse; }
thead th { padding: 8px 12px; font-weight: 600; color: var(--color-gray-600); font-size: 11px; text-align: left; border-bottom: 1px solid var(--color-gray-200); background: var(--color-gray-50); }
tbody tr { border-bottom: 1px solid var(--color-gray-100); }
tbody tr:hover { background: var(--color-gray-50); }
tbody td { padding: 8px 12px; color: var(--color-gray-700); }
.font-mono { font-family: var(--font-mono); font-size: 11px; }
.font-semibold { font-weight: 600; }
.text-center { text-align: center; }
.text-muted { color: var(--color-gray-500); }

.row-locked { background: var(--color-gray-50); opacity: 0.7; }
.week-range { white-space: nowrap; }

.status-badge { display: inline-flex; padding: 2px 10px; border-radius: 10px; font-size: 10px; font-weight: 600; }
.status-badge.locked { background: #FEE2E2; color: #DC2626; }
.status-badge.partial { background: #FEF3C7; color: #92400E; }
.status-badge.open { background: #DCFCE7; color: #15803D; }

.btn-sm-lock { padding: 3px 10px; border-radius: 4px; font-size: 11px; font-weight: 600; background: #DC2626; color: white; border: none; cursor: pointer; }
.btn-sm-lock:hover { background: #B91C1C; }
.btn-sm-unlock { padding: 3px 10px; border-radius: 4px; font-size: 11px; font-weight: 600; background: none; border: 1px solid #16A34A; color: #16A34A; cursor: pointer; }
.btn-sm-unlock:hover { background: #DCFCE7; }
.btn-sm-revoke { padding: 3px 10px; border-radius: 4px; font-size: 11px; font-weight: 600; background: none; border: 1px solid #DC2626; color: #DC2626; cursor: pointer; }
.btn-sm-revoke:hover { background: #FEE2E2; }

.reason-badge { display: inline-flex; padding: 2px 8px; border-radius: 10px; font-size: 10px; font-weight: 600; }
.reason-correction { background: #DBEAFE; color: #1D4ED8; }
.reason-amendment { background: #FEF3C7; color: #92400E; }
.reason-audit { background: #F3E8FF; color: #7C3AED; }

.empty { padding: 24px; text-align: center; color: var(--color-gray-400); font-size: 13px; }

.btn-add-task-lock { padding: 4px 12px; border-radius: 6px; font-size: 11px; font-weight: 600; background: #2563EB; color: white; border: none; cursor: pointer; }
.btn-add-task-lock:hover { background: #1D4ED8; }
.form-card-inline { border-top: 1px solid var(--color-gray-200); border-radius: 0; margin-bottom: 0; }
.search-input { margin-bottom: 4px; }
.project-select { margin-top: 0; }
</style>
