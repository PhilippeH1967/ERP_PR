<script setup lang="ts">
import { onMounted, ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useLocale } from '@/shared/composables/useLocale'
import { useAuth } from '@/shared/composables/useAuth'
import apiClient from '@/plugins/axios'
import { projectApi } from '../api/projectApi'
import { billingApi } from '@/features/billing/api/billingApi'
import { consortiumApi } from '@/features/consortiums/api/consortiumApi'
import { useProjectStore } from '../stores/useProjectStore'
import GanttChart from '@/features/planning/components/GanttChart.vue'
import AmendmentSlideOver from '../components/AmendmentSlideOver.vue'
import ProjectCloseModal from '../components/ProjectCloseModal.vue'
import TaskEditModal from '../components/TaskEditModal.vue'
import TaskSlideOver from '@/features/planning/components/TaskSlideOver.vue'
import AssignResourceDialog from '../components/AssignResourceDialog.vue'
import ProjectSettingsTab from '../components/ProjectSettingsTab.vue'
import TaskTemplatePicker from '../components/TaskTemplatePicker.vue'
import TeamMembersPanel from '../components/TeamMembersPanel.vue'
import TabGroup from '@/shared/components/TabGroup.vue'
import { planningApi } from '@/features/planning/api/planningApi'
import { visibleTaskGroups, isTaskReadOnly, taskClosureIds } from '../utils/taskStructure'
import { buildPhasePeopleTree, filterTreeByPerson, visiblePhaseNodes, type PhaseTreeNode } from '../utils/phasePeopleTree'
import { derivedDates, shiftIsoDate } from '../utils/scheduleHelpers'
import { progressHoursPct, progressCostPct, progressFeesPct } from '../utils/phaseProgress'

const route = useRoute()
const router = useRouter()
const store = useProjectStore()
const { fmt } = useLocale()
const { currentUser } = useAuth()
const projectId = Number(route.params.id)
const activeTab = ref('overview')
const actionError = ref('')
const showEditStatus = ref(false)
const showActionsMenu = ref(false)
const showDeleteConfirm = ref(false)
const confirmDeletePhase = ref<number | null>(null)
const confirmDeleteAssignment = ref<number | null>(null)

interface DashboardData { hours_consumed: string; budget_hours: string; budget_utilization_percent: number; health: 'green' | 'yellow' | 'red' }
interface Assignment { id: number; employee: number; employee_name: string; virtual_resource?: number | null; virtual_resource_name?: string; phase: number | null; phase_name: string; task: number | null; task_name: string; hours_per_week: string; start_date: string | null; end_date: string | null }
interface Amendment { id: number; amendment_number: number; description: string; status: string; budget_impact: string; created_at: string }

const dashboard = ref<DashboardData | null>(null)
const assignments = ref<Assignment[]>([])
const amendments = ref<Amendment[]>([])

// WBS edit state (form refs dropped — legacy WBS tab replaced by tasks-per-phase)
const editingWBSId = ref<number | null>(null)

// Budget tab
const budgetSaving = ref<number | null>(null)
const budgetError = ref('')
const creatingInvoice = ref(false)

// Client info
interface ClientContact { id: number; name: string; role: string; email: string; phone: string }
interface ClientData { id: number; name: string; contacts: ClientContact[] }
const clientData = ref<ClientData | null>(null)

const clientName = computed(() => store.currentProject?.client_name || clientData.value?.name || '—')
const clientContact = computed(() => clientData.value?.contacts?.[0] || null)

async function loadClientData() {
  const clientId = store.currentProject?.client
  if (!clientId) { clientData.value = null; return }
  try {
    const resp = await apiClient.get(`clients/${clientId}/`)
    clientData.value = resp.data?.data || resp.data
  } catch { clientData.value = null }
}

// Consortium data
interface ConsortiumData {
  id: number; name: string; client_name: string; pr_role: string;
  contract_reference: string; status: string;
  members: Array<{ id: number; display_name: string; coefficient: string; specialty: string; is_pr: boolean }>
  total_coefficient: string
}
const consortiumData = ref<ConsortiumData | null>(null)

async function loadConsortiumData() {
  const consortiumId = store.currentProject?.consortium
  if (!consortiumId) { consortiumData.value = null; return }
  try {
    const resp = await consortiumApi.get(consortiumId)
    consortiumData.value = resp.data?.data || resp.data
  } catch { consortiumData.value = null }
}

// ST tab
interface STInvoiceItem { id: number; supplier_name: string; invoice_number: string; invoice_date: string; amount: string; status: string; budget_refacturable: string }
const stInvoices = ref<STInvoiceItem[]>([])
const stLoading = ref(false)

async function loadSTInvoices() {
  if (!store.currentProject) return
  stLoading.value = true
  try {
    const resp = await apiClient.get('st_invoices/', { params: { project: store.currentProject.id } })
    const data = resp.data?.data || resp.data
    stInvoices.value = Array.isArray(data) ? data : data?.results || []
  } catch { stInvoices.value = [] }
  finally { stLoading.value = false }
}

// Invoices tab
interface InvoiceItem { id: number; invoice_number: string; status: string; total_amount: string; date_created: string; date_sent: string | null }
const projectInvoices = ref<InvoiceItem[]>([])
const invoicesLoading = ref(false)

async function loadProjectInvoices() {
  if (!store.currentProject) return
  invoicesLoading.value = true
  try {
    const resp = await apiClient.get('invoices/', { params: { project: store.currentProject.id } })
    const data = resp.data?.data || resp.data
    projectInvoices.value = Array.isArray(data) ? data : data?.results || []
  } catch { projectInvoices.value = [] }
  finally { invoicesLoading.value = false }
}

const stStatusLabels: Record<string, string> = { received: 'Reçue', authorized: 'Autorisée', paid: 'Payée', disputed: 'En litige', credited: 'Créditée' }
const stStatusColors: Record<string, string> = { received: 'badge-amber', authorized: 'badge-blue', paid: 'badge-green', disputed: 'badge-red', credited: 'badge-gray' }
const amendmentStatusLabels: Record<string, string> = { DRAFT: 'Brouillon', SUBMITTED: 'Soumis', APPROVED: 'Approuvé', REJECTED: 'Rejeté' }
const invStatusLabels: Record<string, string> = { DRAFT: 'Brouillon', SUBMITTED: 'Soumise', APPROVED: 'Approuvée', SENT: 'Envoyée', PAID: 'Payée' }
const invStatusColors: Record<string, string> = { DRAFT: 'badge-gray', SUBMITTED: 'badge-blue', APPROVED: 'badge-green', SENT: 'badge-amber', PAID: 'badge-green-solid' }

async function createInvoiceFromProject() {
  budgetError.value = ''
  creatingInvoice.value = true
  try {
    const resp = await billingApi.createFromProject(projectId)
    const data = resp.data?.data || resp.data
    router.push(`/billing/${data.id}`)
  } catch (e: unknown) {
    const err = e as { response?: { data?: { error?: { message?: string } } } }
    budgetError.value = err.response?.data?.error?.message || 'Erreur lors de la création de la facture'
  } finally {
    creatingInvoice.value = false
  }
}

const canEdit = computed(() => {
  const roles = currentUser.value?.roles || []
  return roles.includes('ADMIN') || roles.includes('FINANCE') || roles.includes('PM') || roles.includes('PROJECT_DIRECTOR') || roles.includes('DEPT_ASSISTANT')
})

// isEditing is now equivalent to canEdit — no more global mode toggle.
// Users with rights always see edit affordances; each card manages its own local edit state.
const isEditing = canEdit

// Les phases relèvent du paramétrage (jeu standard du cabinet) : seul un
// administrateur peut les créer/modifier/supprimer sur un projet. Le backend
// (PhaseViewSet) reste la source de vérité (403 sinon).
const isAdmin = computed(() => (currentUser.value?.roles || []).includes('ADMIN'))

const canEditBudget = computed(() => {
  const roles = currentUser.value?.roles || []
  // PM et Associé en charge négocient les honoraires : ils peuvent modifier.
  // Le backend (CostFieldFilterMixin) reste la source de vérité de sécurité.
  return roles.includes('ADMIN')
    || roles.includes('FINANCE')
    || roles.includes('PM')
    || roles.includes('PROJECT_DIRECTOR')
})

const canApproveAmendment = computed(() => {
  const roles = currentUser.value?.roles || []
  return roles.includes('PROJECT_DIRECTOR') || roles.includes('ADMIN')
})

const budgetTotal = computed(() => {
  const phases = (store.currentProject?.phases || []).filter(Boolean)
  return phases.reduce((sum: number, p: { budgeted_cost: string | number }) => sum + Number(p?.budgeted_cost || 0), 0)
})

// Facturé réel : Σ des montants facturés par phase (factures finalisées).
const budgetInvoiced = computed(() => {
  const phases = (store.currentProject?.phases || []).filter(Boolean)
  return phases.reduce(
    (sum: number, p: { invoiced_amount?: number | string }) => sum + Number(p?.invoiced_amount || 0),
    0,
  )
})

// « Consommé » = avancement en heures (réelles / budgétées), fourni par le
// dashboard dont budget_hours vient désormais des tâches (et non du champ
// legacy Phase.budgeted_hours qui valait 0 depuis la refonte v1.2).
const budgetConsumedPercent = computed(() => dashboard.value?.budget_utilization_percent ?? 0)

const budgetRemaining = computed(() => (taskBudgetTotal?.value ?? budgetTotal.value) - budgetInvoiced.value)

function formatAmount(value: number | string): string {
  const n = Number(value)
  if (isNaN(n)) return '0,00'
  return n.toLocaleString('fr-CA', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

// Business Units + Users for dropdowns
const businessUnits = ref<Array<{ id: number; name: string }>>([])
const allUsers = ref<Array<{ id: number; username: string; email: string }>>([])

// Membres de l'équipe — l'appartenance autorise la saisie de temps même sans
// planification (allocation). Gérée via l'endpoint dédié `members`.
const teamMembers = ref<Array<{ id: number; name: string }>>([])
const memberError = ref('')
const memberSaving = ref(false)

const canManageMembers = computed(() => {
  const roles = currentUser.value?.roles || []
  return roles.includes('ADMIN') || roles.includes('PM')
    || roles.includes('PROJECT_DIRECTOR') || roles.includes('DEPT_ASSISTANT')
})

const memberIds = computed(() => new Set(teamMembers.value.map(m => m.id)))
const addableUsers = computed(() => allUsers.value.filter(u => !memberIds.value.has(u.id)))

function syncTeamMembers() {
  teamMembers.value = store.currentProject?.team_members_detail || []
}

async function addTeamMember(userId: number) {
  memberError.value = ''
  memberSaving.value = true
  try {
    const r = await projectApi.addMember(projectId, userId)
    const list = (r.data as { data?: { team_members?: Array<{ id: number; name: string }> } })?.data?.team_members
    if (list) teamMembers.value = list
  } catch (e: unknown) {
    const msg = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message
    memberError.value = msg || "Impossible d'ajouter ce membre."
  } finally {
    memberSaving.value = false
  }
}

// Affectation d'une équipe (paramétrage) en entier sur le projet.
const teams = ref<Array<{ id: number; name: string; member_details: Array<{ id: number }> }>>([])
const assignTeamId = ref<number | null>(null)
const assigningTeam = ref(false)
async function loadTeams() {
  try {
    const r = await apiClient.get('teams/')
    const d = (r.data as { data?: unknown })?.data ?? r.data
    teams.value = Array.isArray(d) ? d : ((d as { results?: unknown })?.results as typeof teams.value) ?? []
  } catch { teams.value = [] }
}
async function assignTeam() {
  if (!assignTeamId.value) return
  memberError.value = ''
  assigningTeam.value = true
  try {
    const r = await projectApi.assignTeam(projectId, assignTeamId.value)
    const list = (r.data as { data?: { team_members?: Array<{ id: number; name: string }> } })?.data?.team_members
    if (list) teamMembers.value = list
    assignTeamId.value = null
  } catch (e: unknown) {
    const msg = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message
    memberError.value = msg || "Impossible d'affecter l'équipe."
  } finally {
    assigningTeam.value = false
  }
}

async function removeTeamMember(userId: number) {
  memberError.value = ''
  const prev = teamMembers.value
  teamMembers.value = teamMembers.value.filter(m => m.id !== userId) // optimiste
  try {
    await projectApi.removeMember(projectId, userId)
  } catch (e: unknown) {
    teamMembers.value = prev // rollback
    const msg = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message
    memberError.value = msg || 'Impossible de retirer ce membre.'
  }
}

// Ajout de phase (réservé admin — onglet Phases)
const showAddPhaseForm = ref(false)
const newPhase = ref({ name: '', client_facing_label: '', phase_type: 'REALIZATION', order: 0 })

async function addPhase() {
  actionError.value = ''
  if (!newPhase.value.name.trim()) { actionError.value = 'Le nom de la phase est obligatoire.'; return }
  try {
    await projectApi.createPhase(projectId, newPhase.value as Record<string, unknown>)
    showAddPhaseForm.value = false
    newPhase.value = { name: '', client_facing_label: '', phase_type: 'REALIZATION', order: 0 }
    await reload()
  } catch (e: unknown) {
    actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur'
  }
}

// Inline edit phase
const editingPhaseId = ref<number | null>(null)
const phaseForm = ref({ name: '', client_facing_label: '', phase_type: 'REALIZATION', order: 0 })

function startEditPhase(phase: { id: number; name: string; client_facing_label?: string; phase_type?: string; order?: number }) {
  editingPhaseId.value = phase.id
  phaseForm.value = {
    name: phase.name,
    client_facing_label: phase.client_facing_label || '',
    phase_type: phase.phase_type || 'REALIZATION',
    order: phase.order ?? 0,
  }
}

async function savePhase() {
  if (!editingPhaseId.value) return
  actionError.value = ''
  try {
    await projectApi.updatePhase(projectId, editingPhaseId.value, phaseForm.value as Record<string, unknown>)
    editingPhaseId.value = null
    await reload()
  } catch (e: unknown) { actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur' }
}

// Tasks
interface TaskItem {
  id: number; project: number; phase: number | null; phase_name: string; parent: number | null;
  wbs_code: string; name: string; client_facing_label: string; display_label: string;
  task_type: 'TASK' | 'SUBTASK'; billing_mode: 'FORFAIT' | 'HORAIRE'; order: number;
  budgeted_hours: string | number; budgeted_cost: string | number; hourly_rate: string | number;
  is_billable: boolean; is_active: boolean; progress_pct: number | string;
  start_date?: string | null; end_date?: string | null;
  planned_hours?: number; actual_hours?: number;
  is_chargeable?: boolean; effective_budgeted_hours?: number; effective_budgeted_cost?: number;
  amendment?: number | null; amendment_number?: number | null;
}
const tasks = ref<TaskItem[]>([])
const collapsedPhases = ref<Set<string>>(new Set())
const confirmDeleteTask = ref<number | null>(null)
const showAddTaskPhase = ref<number | null>(null)
const newTaskName = ref('')
const showAddSubtask = ref<number | null>(null)
const newSubtaskName = ref('')
const editingTaskNameId = ref<number | null>(null)
const editTaskNameValue = ref('')

function commitEditTaskName(taskId: number) {
  const name = editTaskNameValue.value.trim()
  const original = tasks.value.find(t => t.id === taskId)?.name ?? ''
  if (name && name !== original) {
    saveTaskField(taskId, 'name', name)
  }
  editingTaskNameId.value = null
}
function cancelEditTaskName() {
  editingTaskNameId.value = null
}
function enterInlineNameEdit(task: TaskItem) {
  editingTaskNameId.value = task.id
  editTaskNameValue.value = task.name
}

// Task edit modal (F3.7 — édition WBS / libellé client / budgets)
// Échéancier : édition inline des dates + décalage en masse.
const showShiftBand = ref(false)
const shiftDays = ref(10)
const shifting = ref(false)
function derivedFor(task: TaskItem) { return derivedDates(task, tasks.value) }
function onTaskDateInline(task: TaskItem, field: 'start_date' | 'end_date', ev: Event) {
  const val = (ev.target as HTMLInputElement).value || null
  const next = {
    start: field === 'start_date' ? val : (task.start_date || null),
    end: field === 'end_date' ? val : (task.end_date || null),
  }
  if (next.start && next.end && next.end < next.start) {
    actionError.value = 'La date de fin ne peut pas être antérieure à la date de début.'
    ;(ev.target as HTMLInputElement).value = (task[field] as string) || ''
    return
  }
  actionError.value = ''
  saveTaskField(task.id, field, val)
}
async function applyShift() {
  const n = Number(shiftDays.value || 0)
  if (!n || shifting.value) return
  shifting.value = true
  actionError.value = ''
  try {
    const leafTasks = tasks.value.filter(
      t => !tasks.value.some(x => x.parent === t.id) && (t.start_date || t.end_date),
    )
    for (const t of leafTasks) {
      await projectApi.updateTask(projectId, t.id, {
        start_date: shiftIsoDate(t.start_date || null, n),
        end_date: shiftIsoDate(t.end_date || null, n),
      })
    }
    showShiftBand.value = false
    await loadTasks()
    await store.fetchProject(projectId)
  } catch (e: unknown) {
    actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Décalage impossible.'
  } finally { shifting.value = false }
}

// Fiche tâche unique (slide-over) — ouverte au clic sur le nom d'une tâche.
const sheetTaskId = ref<number | null>(null)
function openTaskSheet(id: number) { sheetTaskId.value = id }
async function onTaskSheetUpdated() {
  await loadTasks()
  await store.fetchProject(projectId)
}
const showTaskEditModal = ref(false)
const taskBeingEdited = ref<TaskItem | null>(null)
const taskEditLoading = ref(false)
const taskEditError = ref('')

function openTaskEditModal(task: TaskItem) {
  taskBeingEdited.value = task
  taskEditError.value = ''
  showTaskEditModal.value = true
}

async function saveTaskEdit(payload: {
  name: string
  wbs_code: string
  client_facing_label: string
  budgeted_hours: string
  budgeted_cost?: string
  billing_mode: string
  is_billable: boolean
}) {
  if (!taskBeingEdited.value) return
  taskEditLoading.value = true
  taskEditError.value = ''
  try {
    await projectApi.updateTask(projectId, taskBeingEdited.value.id, payload as unknown as Record<string, unknown>)
    showTaskEditModal.value = false
    taskBeingEdited.value = null
    await loadTasks()
    await store.fetchProject(projectId)
  } catch (e: unknown) {
    taskEditError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur de sauvegarde'
  } finally {
    taskEditLoading.value = false
  }
}

const tasksByPhase = computed(() => {
  const grouped: Record<string, { phase_name: string; phase_id: number | null; tasks: TaskItem[] }> = {}

  // 1. Initialiser une entrée pour CHAQUE phase du projet (même sans tâche).
  //    Permet d'afficher le bouton '+ Tâche' sur chaque phase, y compris vide.
  const projectPhases = (store.currentProject?.phases || []) as Array<{ id: number; name: string }>
  for (const p of projectPhases) {
    if (!p?.id) continue
    grouped[p.name] = { phase_name: p.name, phase_id: p.id, tasks: [] }
  }

  // 2. Distribuer les tâches existantes dans leurs phases
  for (const t of tasks.value) {
    if (!t || !t.id) continue
    const key = t.phase_name || 'Sans phase'
    if (!grouped[key]) grouped[key] = { phase_name: key, phase_id: t.phase, tasks: [] }
    grouped[key].tasks.push(t)
  }

  // 3. Trier les tâches par ordre dans chaque phase
  for (const g of Object.values(grouped)) {
    g.tasks.sort((a, b) => (a.order ?? 0) - (b.order ?? 0))
  }
  return Object.values(grouped)
})

// Onglet Tâches : on n'affiche que les phases qui ont des tâches (les phases
// standard vides sont masquées, mais restent ciblables via « + Tâche »).
const visibleTaskPhaseGroups = computed(() => visibleTaskGroups(tasksByPhase.value))

// Toutes les phases du projet, pour les sélecteurs « + Tâche » et « Déplacer ».
const allProjectPhases = computed(
  () => ((store.currentProject?.phases || []) as Array<{ id: number; name: string }>).filter(p => p?.id),
)

// Ajout global d'une tâche : choisir une phase cible (même vide)
const showGlobalAddTask = ref(false)
const newTaskPhaseId = ref<number | null>(null)

// Déplacement d'une tâche vers une autre phase (ré-imputation)
const movingTaskId = ref<number | null>(null)
const moveTargetPhaseId = ref<number | null>(null)

function startMoveTask(task: TaskItem) {
  movingTaskId.value = task.id
  moveTargetPhaseId.value = task.phase
}

async function moveTask(taskId: number) {
  if (!moveTargetPhaseId.value) return
  actionError.value = ''
  try {
    await projectApi.updateTask(projectId, taskId, { phase: moveTargetPhaseId.value })
    movingTaskId.value = null
    await loadTasks()
    await store.fetchProject(projectId)
  } catch (e: unknown) {
    actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur'
  }
}

const taskBudgetTotal = computed(() => tasks.value.reduce((sum, t) => sum + Number(t.budgeted_cost || 0), 0))
const taskHoursTotal = computed(() => tasks.value.reduce((sum, t) => sum + Number(t.budgeted_hours || 0), 0))
const taskPlannedTotal = computed(() => tasks.value.reduce((sum, t) => sum + Number((t as Record<string, unknown>).planned_hours || 0), 0))
const tasksWithoutBudget = computed(() => tasks.value.filter(t => Number(t.budgeted_hours || 0) === 0 && Number(t.budgeted_cost || 0) === 0))
// Alertes Pilotage : tâches dont la fin précède le début (données héritées/erreurs).
const badDateTasks = computed(() => tasks.value.filter(t => t.start_date && t.end_date && t.end_date < t.start_date))

// Phase-level alerts
const phaseBudgetTotal = computed(() => {
  const phases = (store.currentProject?.phases || []).filter(Boolean)
  return phases.reduce((sum: number, p: Record<string, unknown>) => {
    const taskBudget = Number(p.tasks_budgeted_hours || 0)
    const phaseBudget = Number(p.budgeted_hours || 0)
    return sum + (taskBudget || phaseBudget)
  }, 0)
})
const phasesWithoutBudget = computed(() => {
  return (store.currentProject?.phases || []).filter(Boolean).filter((p: Record<string, unknown>) => {
    return Number(p.tasks_budgeted_hours || 0) === 0 && Number(p.budgeted_hours || 0) === 0 && Number(p.budgeted_cost || 0) === 0
  })
})
const phasePlannedTotal = computed(() => {
  return (store.currentProject?.phases || []).filter(Boolean).reduce((sum: number, p: Record<string, unknown>) => sum + Number(p.planned_hours || 0), 0)
})
const phaseFuturePlannedTotal = computed(() => {
  // Check if any ResourceAllocation has end_date >= today
  // Approximation: if planned > 0 and project active, check teamStats
  if (!teamStats.value) return phasePlannedTotal.value // assume OK if no stats loaded
  const planning = teamStats.value.employees_planning || {}
  return Object.values(planning).reduce((sum: number, h) => sum + (h as number), 0)
})

async function loadTasks() {
  try {
    const r = await projectApi.listTasks(projectId)
    const d = r.data?.data || r.data
    const arr = Array.isArray(d) ? d : d?.results || []
    tasks.value = arr.filter((t: unknown) => t && typeof t === 'object' && 'id' in (t as Record<string, unknown>)) as TaskItem[]
  } catch { tasks.value = [] }
}

async function saveTaskField(taskId: number, field: string, value: unknown) {
  try {
    await projectApi.updateTask(projectId, taskId, { [field]: value })
    await loadTasks()
    // Rafraîchir les agrégats de phase (budget/heures/dates = Σ des tâches).
    await store.fetchProject(projectId)
  } catch (e: unknown) {
    actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur de sauvegarde'
  }
}

// Fermer / rouvrir une tâche : bloque (ou rétablit) la saisie de temps. Fermer
// une tâche-mère ferme tout son groupe (ses sous-tâches saisissables). Réversible.
async function setTaskClosed(task: TaskItem, closed: boolean) {
  const ids = taskClosureIds(task, tasks.value)
  try {
    for (const id of ids) {
      await projectApi.updateTask(projectId, id, { is_active: !closed })
    }
    await loadTasks()
    await store.fetchProject(projectId)
  } catch (e: unknown) {
    actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur de sauvegarde'
  }
}

// Après création des tâches depuis le modèle (picker à l'état vide) : recharger
// les tâches + les agrégats de phase. Le picker disparaît (tasks.length > 0).
async function onTemplateTasksCreated() {
  await loadTasks()
  await store.fetchProject(projectId)
}

// Picker par phase : ajout ciblé depuis le catalogue (phases vides OU non, les
// tâches déjà présentes sont exclues côté backend).
const showTemplatePhase = ref<number | null>(null)
async function onPhaseTemplateCreated() {
  showTemplatePhase.value = null
  await loadTasks()
  await store.fetchProject(projectId)
}

async function addTask(phaseId: number | null) {
  if (!newTaskName.value.trim()) return
  try {
    // Auto-generate wbs_code: "{phase_code}.{next_number}"
    const phase = store.currentProject?.phases?.find((p: { id: number }) => p.id === phaseId)
    const phaseCode = phase?.code || String(phaseId || '0')
    const existingInPhase = tasks.value.filter(t => t.phase === phaseId)
    const nextNum = existingInPhase.length + 1
    const wbs_code = `${phaseCode}.${nextNum}`
    await projectApi.createTask(projectId, { phase: phaseId, name: newTaskName.value.trim(), task_type: 'TASK', billing_mode: 'FORFAIT', wbs_code })
    newTaskName.value = ''
    showAddTaskPhase.value = null
    showGlobalAddTask.value = false
    newTaskPhaseId.value = null
    await loadTasks()
    await store.fetchProject(projectId)
  } catch (e: unknown) {
    actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur'
  }
}

async function addSubtask(parentTaskId: number) {
  if (!newSubtaskName.value.trim()) return
  const parentTask = tasks.value.find(t => t.id === parentTaskId)
  if (!parentTask) return
  try {
    const existingSubs = tasks.value.filter(t => t.parent === parentTaskId)
    const nextNum = existingSubs.length + 1
    const wbs_code = `${parentTask.wbs_code}.${nextNum}`
    await projectApi.createTask(projectId, {
      phase: parentTask.phase,
      parent: parentTaskId,
      name: newSubtaskName.value.trim(),
      task_type: 'SUBTASK',
      billing_mode: parentTask.billing_mode,
      wbs_code,
    })
    newSubtaskName.value = ''
    showAddSubtask.value = null
    await loadTasks()
    await store.fetchProject(projectId)
  } catch (e: unknown) {
    actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur'
  }
}

async function removeTask(taskId: number) {
  // Clear any pending edit state to prevent blur-triggered PATCH with invalid data (BUG-006)
  confirmDeleteTask.value = null
  editingWBSId.value = null
  budgetSaving.value = null
  // Optimistic removal from local state
  tasks.value = tasks.value.filter(t => t.id !== taskId)
  try {
    await projectApi.deleteTask(projectId, taskId)
    await store.fetchProject(projectId)
  } catch { /* ok */ }
}

function togglePhaseCollapse(phaseName: string) {
  if (collapsedPhases.value.has(phaseName)) collapsedPhases.value.delete(phaseName)
  else collapsedPhases.value.add(phaseName)
}

// Amendment SlideOver (Sprint B)
const slideOverOpen = ref(false)
const slideOverAmendmentId = ref<number | null>(null)

function openAmendmentSlideOver(amendmentId: number | null) {
  slideOverAmendmentId.value = amendmentId
  slideOverOpen.value = true
}

async function onAmendmentSaved() {
  await reload()
  if (activeTab.value === 'budget') await loadBudgetSummary()
}

function onAmendmentSlideOverClose() {
  slideOverOpen.value = false
  slideOverAmendmentId.value = null
}

// Honoraires form state
const honorairesForm = ref({
  total_fees: '',
  fee_calculation_method: 'FORFAIT',
  fee_rate_pct: '',
  construction_cost: '',
})
const honorairesSaving = ref(false)

function initHonoraires() {
  const p = store.currentProject
  if (!p) return
  honorairesForm.value = {
    total_fees: p.total_fees ?? '',
    fee_calculation_method: p.fee_calculation_method || 'FORFAIT',
    fee_rate_pct: p.fee_rate_pct ?? '',
    construction_cost: p.construction_cost != null ? String(p.construction_cost) : '',
  }
}

function parseAmount(v: unknown): number {
  return Number(String(v ?? '').replace(/\s/g, '').replace(',', '.')) || 0
}

const computedFees = computed(() => {
  if (honorairesForm.value.fee_calculation_method !== 'COUT_TRAVAUX') return null
  const cost = parseAmount(honorairesForm.value.construction_cost)
  const rate = parseAmount(honorairesForm.value.fee_rate_pct)
  return cost * rate / 100
})

async function saveHonoraires() {
  honorairesSaving.value = true
  budgetError.value = ''
  try {
    const payload: Record<string, unknown> = {
      fee_calculation_method: honorairesForm.value.fee_calculation_method,
    }
    if (honorairesForm.value.total_fees !== '') payload.total_fees = parseFloat(String(honorairesForm.value.total_fees).replace(/\s/g, '').replace(',', '.'))
    else payload.total_fees = null
    if (honorairesForm.value.fee_rate_pct !== '') payload.fee_rate_pct = parseFloat(String(honorairesForm.value.fee_rate_pct).replace(/\s/g, '').replace(',', '.'))
    else payload.fee_rate_pct = null
    // construction_cost : géré sur la Vue d'ensemble (plus envoyé ici).
    await projectApi.update(projectId, payload)
    await reload()
    initHonoraires()
  } catch (e: unknown) {
    budgetError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur de sauvegarde'
  } finally {
    honorairesSaving.value = false
  }
}

// Team tab — grouped by employee with hours + monthly chart + budget health
const expandedTeamMembers = ref(new Set<number>())
function toggleTeamMember(empId: number) {
  if (expandedTeamMembers.value.has(empId)) expandedTeamMembers.value.delete(empId)
  else expandedTeamMembers.value.add(empId)
}

interface TeamStats {
  budget_status: string
  over_budget_phases: number
  total_phases: number
  phases_health: Array<{ phase_id: number; phase_name: string; budget_hours: number; planned_hours: number; actual_hours: number; over_budget: boolean }>
  employees_monthly: Array<{ employee_id: number; employee_name: string; months: Array<{ month: string; hours: number }> }>
  employees_planning: Record<string, number>
}
const teamStats = ref<TeamStats | null>(null)
const teamStatsLoading = ref(false)

async function loadTeamStats() {
  teamStatsLoading.value = true
  try {
    const r = await projectApi.teamStats(projectId)
    teamStats.value = r.data?.data || r.data
  } catch { teamStats.value = null }
  finally { teamStatsLoading.value = false }
}

interface TeamMember {
  employee: number
  employee_name: string
  assignments: Assignment[]
  totalPlanned: number
  totalActual: number
  monthlyHours: Array<{ month: string; hours: number }>
  hasPlanning: boolean
}

const teamByEmployee = computed<TeamMember[]>(() => {
  const map = new Map<number, TeamMember>()
  for (const a of assignments.value) {
    if (!map.has(a.employee)) {
      map.set(a.employee, {
        employee: a.employee,
        employee_name: a.employee_name || `Employé #${a.employee}`,
        assignments: [],
        totalPlanned: 0,
        totalActual: 0,
        monthlyHours: [],
        hasPlanning: false,
      })
    }
    map.get(a.employee)!.assignments.push(a)
  }
  // Actual hours from time entries
  for (const entry of projectTimeEntries.value) {
    const member = map.get(entry.employee)
    if (member) member.totalActual += Number(entry.hours || 0)
  }
  // Planning + monthly from teamStats
  if (teamStats.value) {
    const planning = teamStats.value.employees_planning || {}
    const monthly = teamStats.value.employees_monthly || []
    for (const [, member] of map) {
      member.totalPlanned = planning[String(member.employee)] || 0
      member.hasPlanning = member.totalPlanned > 0
      const empMonthly = monthly.find(m => m.employee_id === member.employee)
      if (empMonthly) member.monthlyHours = empMonthly.months
    }
  }
  return Array.from(map.values()).sort((a, b) => a.employee_name.localeCompare(b.employee_name))
})

// ── Vue « Par phase » de l'onglet Équipe (accordéons + recherche) ──────────
const teamViewMode = ref<'person' | 'phase'>('phase')
const teamSearch = ref('')
const expandedPhaseKeys = ref<Set<number>>(new Set())
const expandedTaskKeys = ref<Set<number>>(new Set())

const phasePeopleTree = computed<PhaseTreeNode[]>(() =>
  visiblePhaseNodes(buildPhasePeopleTree(tasksByPhase.value, assignments.value)),
)
// Recherche active → arbre filtré (toujours déplié).
const teamPhaseTree = computed<PhaseTreeNode[]>(() =>
  filterTreeByPerson(phasePeopleTree.value, teamSearch.value),
)
const isTeamSearching = computed(() => teamSearch.value.trim().length > 0)

function isPhaseOpen(id: number | null): boolean {
  return isTeamSearching.value || id == null || expandedPhaseKeys.value.has(id)
}
function isTaskOpen(id: number): boolean {
  return isTeamSearching.value || expandedTaskKeys.value.has(id)
}
function togglePhaseOpen(id: number | null) {
  if (id == null) return
  const s = new Set(expandedPhaseKeys.value)
  if (s.has(id)) s.delete(id)
  else s.add(id)
  expandedPhaseKeys.value = s
}
function toggleTaskOpen(id: number) {
  const s = new Set(expandedTaskKeys.value)
  if (s.has(id)) s.delete(id)
  else s.add(id)
  expandedTaskKeys.value = s
}
function expandAllTeamPhases() {
  const ph = new Set<number>()
  const tk = new Set<number>()
  const walk = (nodes: PhaseTreeNode['tasks']) => {
    for (const n of nodes) { tk.add(n.id); walk(n.subtasks) }
  }
  for (const p of phasePeopleTree.value) {
    if (p.phase_id != null) ph.add(p.phase_id)
    walk(p.tasks)
  }
  expandedPhaseKeys.value = ph
  expandedTaskKeys.value = tk
}
function collapseAllTeamPhases() {
  expandedPhaseKeys.value = new Set()
  expandedTaskKeys.value = new Set()
}

// ── Blocage de saisie par personne (Lot 2) ─────────────────────────────────
interface TimeBlock { id: number; employee: number; employee_name: string; phase: number | null; task: number | null }
const timeBlocks = ref<TimeBlock[]>([])

async function loadTimeBlocks() {
  try {
    const r = await apiClient.get('time_entry_blocks/', { params: { project: String(projectId), page_size: '500' } })
    const d = r.data?.data || r.data
    timeBlocks.value = Array.isArray(d) ? d : d?.results || []
  } catch { timeBlocks.value = [] }
}

// ── Fermeture GLOBALE (tout le monde) d'un nœud — vue « Par phase » ──────────
function isPhaseClosed(phaseId: number): boolean {
  const ts = tasks.value.filter(t => t.phase === phaseId)
  return ts.length > 0 && ts.every(t => !t.is_active)
}
async function setPhaseClosed(phaseId: number, closed: boolean) {
  const ids = tasks.value.filter(t => t.phase === phaseId).map(t => t.id)
  try {
    for (const id of ids) await projectApi.updateTask(projectId, id, { is_active: !closed })
    await loadTasks()
    await store.fetchProject(projectId)
  } catch (e: unknown) {
    actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur'
  }
}
function toggleNodeClosed(taskId: number) {
  const t = tasks.value.find(x => x.id === taskId)
  if (t) setTaskClosed(t, t.is_active) // is_active=true → fermer ; false → rouvrir
}

// ── Blocage PAR PERSONNE — vue « Par personne » (sur une affectation) ────────
function assignmentBlock(employeeId: number, a: Assignment): TimeBlock | null {
  return timeBlocks.value.find(
    b => b.employee === employeeId && (a.task ? b.task === a.task : b.phase === a.phase),
  ) || null
}
function toggleAssignmentBlock(employeeId: number, a: Assignment) {
  const blk = assignmentBlock(employeeId, a)
  if (blk) return unblockTime(blk.id)
  return blockMember(a.task ? { task: a.task } : { phase: a.phase as number }, employeeId)
}

// Blocage NIVEAU PROJET : la personne ne peut imputer sur AUCUNE tâche du projet.
function personBlock(employeeId: number): TimeBlock | null {
  return timeBlocks.value.find(b => b.employee === employeeId && b.task == null && b.phase == null) || null
}
function isPersonFullyBlocked(employeeId: number): boolean {
  return personBlock(employeeId) != null
}
async function togglePersonBlock(employeeId: number) {
  const blk = personBlock(employeeId)
  if (blk) return unblockTime(blk.id)
  try {
    await apiClient.post('time_entry_blocks/', { project: projectId, employee: employeeId })
    await loadTimeBlocks()
  } catch (e: unknown) {
    actionError.value = (e as { response?: { data?: { detail?: string } } }).response?.data?.detail || 'Blocage impossible (droits gestionnaire requis).'
  }
}

async function blockMember(target: { phase: number } | { task: number }, employeeId: number) {
  try {
    await apiClient.post('time_entry_blocks/', { project: projectId, employee: employeeId, ...target })
    await loadTimeBlocks()
  } catch (e: unknown) {
    actionError.value = (e as { response?: { data?: { detail?: string } } }).response?.data?.detail || 'Blocage impossible (droits gestionnaire requis).'
  }
}
async function unblockTime(blockId: number) {
  timeBlocks.value = timeBlocks.value.filter(b => b.id !== blockId)
  try { await apiClient.delete(`time_entry_blocks/${blockId}/`) } catch { await loadTimeBlocks() }
}

// Dialogue unifié « Affecter une ressource » (Qui / Où / Combien).
const assignDialogOpen = ref(false)
const assignDialogScope = ref<{ type: 'project' | 'phase' | 'task'; id?: number | null } | undefined>(undefined)
function openAssignDialog(scope?: { type: 'project' | 'phase' | 'task'; id?: number | null }) {
  assignDialogScope.value = scope
  assignDialogOpen.value = true
}
async function onAssigned() {
  try {
    const r = await apiClient.get('allocations/', { params: { project: String(projectId), page_size: '500' } })
    const d = r.data?.data || r.data
    assignments.value = Array.isArray(d) ? d : d?.results || []
  } catch { /* ignore */ }
  syncTeamMembers()
  loadTeamStats()
}

// Time entries for Temps tab
interface ProjectTimeEntry { id: number; employee: number; employee_name?: string; user_name: string; date: string; hours: string; task_name: string; phase_name: string; status: string }
const projectTimeEntries = ref<ProjectTimeEntry[]>([])
const timeLoading = ref(false)

async function loadProjectTime() {
  if (!store.currentProject) return
  timeLoading.value = true
  try {
    const resp = await apiClient.get('time_entries/', { params: { project: store.currentProject.id, page_size: 1000 } })
    const data = resp.data?.data || resp.data
    projectTimeEntries.value = Array.isArray(data) ? data : data?.results || []
  } catch { projectTimeEntries.value = [] }
  finally { timeLoading.value = false }
}

const projectTotalHours = computed(() => projectTimeEntries.value.reduce((s, e) => s + Number(e.hours || 0), 0))
const timeViewMode = ref<'employee' | 'phase'>('employee')
const expandedTimeMonths = ref(new Set<string>())
function toggleTimeMonth(month: string) {
  if (expandedTimeMonths.value.has(month)) {
    expandedTimeMonths.value.delete(month)
  } else {
    expandedTimeMonths.value.add(month)
  }
}

// Unique sorted months from time entries
const timeMonths = computed(() => {
  const months = new Set<string>()
  for (const e of projectTimeEntries.value) {
    if (e.date) months.add(e.date.substring(0, 7))
  }
  return Array.from(months).sort()
})

// Unique sorted days per month
const timeDaysByMonth = computed(() => {
  const map = new Map<string, string[]>()
  for (const e of projectTimeEntries.value) {
    if (!e.date) continue
    const month = e.date.substring(0, 7)
    if (!map.has(month)) map.set(month, [])
    const day = e.date.substring(8, 10)
    if (!map.get(month)!.includes(day)) map.get(month)!.push(day)
  }
  for (const [, days] of map) days.sort()
  return map
})

// Rows: grouped by employee or phase
interface TimePivotRow {
  key: string
  label: string
  totalHours: number
  hoursByMonth: Record<string, number>
  hoursByDay: Record<string, number> // key: "YYYY-MM-DD"
}

const timePivotRows = computed<TimePivotRow[]>(() => {
  const map = new Map<string, TimePivotRow>()
  for (const e of projectTimeEntries.value) {
    const key = timeViewMode.value === 'employee'
      ? String(e.employee)
      : (e.phase_name || 'Sans phase')
    const label = timeViewMode.value === 'employee'
      ? (e.employee_name || `Employé #${e.employee}`)
      : (e.phase_name || 'Sans phase')
    if (!map.has(key)) {
      map.set(key, { key, label, totalHours: 0, hoursByMonth: {}, hoursByDay: {} })
    }
    const row = map.get(key)!
    const hours = Number(e.hours || 0)
    row.totalHours += hours
    const month = e.date?.substring(0, 7) || ''
    row.hoursByMonth[month] = (row.hoursByMonth[month] || 0) + hours
    if (e.date) row.hoursByDay[e.date] = (row.hoursByDay[e.date] || 0) + hours
  }
  return Array.from(map.values()).sort((a, b) => b.totalHours - a.totalHours)
})

// Column totals per month and per day
const monthTotals = computed(() => {
  const t: Record<string, number> = {}
  for (const row of timePivotRows.value) {
    for (const [m, h] of Object.entries(row.hoursByMonth)) t[m] = (t[m] || 0) + h
  }
  return t
})
const dayTotals = computed(() => {
  const t: Record<string, number> = {}
  for (const row of timePivotRows.value) {
    for (const [d, h] of Object.entries(row.hoursByDay)) t[d] = (t[d] || 0) + h
  }
  return t
})

// Grouped tabs — 5 root groups, some with sub-tabs (Sprint C)
const rootTabs = computed(() => [
  { key: 'overview', label: '📊 Pilotage' },
  {
    key: 'structure',
    label: '📅 Échéancier',
    subTabs: [
      { key: 'phases', label: 'Phases' },
      { key: 'tasks', label: 'Tâches' },
      { key: 'gantt', label: 'Gantt' },
    ],
  },
  { key: 'team', label: '👥 Équipe & charge' },
  { key: 'time', label: '⏱ Temps' },
  {
    key: 'finances',
    label: '💰 Finances',
    subTabs: [
      { key: 'budget', label: 'Budget' },
      { key: 'invoices', label: 'Factures' },
      { key: 'st', label: 'Sous-traitants' },
    ],
  },
  {
    key: 'amendments',
    label: `📝 Avenants${amendments.value.length ? ` (${amendments.value.length})` : ''}`,
  },
  { key: 'params', label: '⚙️ Paramètres' },
])

// Map an activeTab key back to its root (for TabGroup binding)
const tabToRoot: Record<string, string> = {
  overview: 'overview',
  phases: 'structure', tasks: 'structure', gantt: 'structure',
  // « team »/« time » étaient des sous-onglets de « execution » — promus au
  // 1er niveau (audit UX, mockup 01). Les vieux liens ?tab=execution/team
  // continuent de résoudre via la clé du sous-onglet.
  team: 'team', time: 'time',
  budget: 'finances', invoices: 'finances', st: 'finances',
  amendments: 'amendments', params: 'params',
}
const rootTab = computed(() => tabToRoot[activeTab.value] || 'overview')
const currentSubTab = computed(() => {
  const root = rootTabs.value.find(r => r.key === rootTab.value)
  return root?.subTabs ? activeTab.value : null
})

function onTabGroupUpdate(payload: { rootTab: string; subTab: string | null }) {
  activeTab.value = payload.subTab || payload.rootTab
}

// URL sync — ?tab=structure/phases or ?tab=overview
function parseTabQuery(q: unknown): string {
  if (typeof q !== 'string' || !q) return 'overview'
  const [, sub] = q.split('/')
  const candidate = sub || q
  return Object.prototype.hasOwnProperty.call(tabToRoot, candidate) ? candidate : 'overview'
}
activeTab.value = parseTabQuery(route.query.tab)
watch(activeTab, (tab) => {
  const root = tabToRoot[tab] || 'overview'
  const encoded = root === tab ? root : `${root}/${tab}`
  if (route.query.tab !== encoded) {
    router.replace({ query: { ...route.query, tab: encoded } })
  }
})

const statuses = [
  { value: 'ACTIVE', label: 'Actif', color: 'badge-green' },
  { value: 'ON_HOLD', label: 'En pause', color: 'badge-amber' },
  { value: 'COMPLETED', label: 'Terminé', color: 'badge-gray' },
  { value: 'CANCELLED', label: 'Annulé', color: 'badge-red' },
]

// BUG-UX-001: Only show valid status transitions
const validTransitions: Record<string, string[]> = {
  'ACTIVE': ['ON_HOLD', 'COMPLETED', 'CANCELLED'],
  'ON_HOLD': ['ACTIVE', 'CANCELLED'],
  'COMPLETED': [],
  'CANCELLED': [],
}

const availableStatuses = computed(() => {
  const current = store.currentProject?.status || ''
  const allowed = validTransitions[current] || []
  return statuses.filter(s => allowed.includes(s.value))
})

const statusColors: Record<string, string> = { ACTIVE: 'badge-green', ON_HOLD: 'badge-amber', COMPLETED: 'badge-gray', CANCELLED: 'badge-red' }

async function reload() {
  await store.fetchProject(projectId)
  try { const r = await apiClient.get('business_units/'); const d = r.data?.data || r.data; businessUnits.value = Array.isArray(d) ? d : d?.results || [] } catch { businessUnits.value = [] }
  try { const r = await apiClient.get('users/search/'); const d = r.data?.data || r.data; allUsers.value = Array.isArray(d) ? d : [] } catch { allUsers.value = [] }
  try { const r = await projectApi.dashboard(projectId); dashboard.value = r.data?.data || r.data } catch { dashboard.value = null }
  try {
    const r = await apiClient.get('allocations/', { params: { project: String(projectId), page_size: '500' } })
    const d = r.data?.data || r.data
    assignments.value = Array.isArray(d) ? d : d?.results || []
  } catch { assignments.value = [] }
  await loadTimeBlocks()
  await loadTasks()
  try { const r = await projectApi.listAmendments(projectId); amendments.value = r.data?.data || r.data || [] } catch { amendments.value = [] }
  await loadClientData()
  await loadConsortiumData()
  await loadTasks()
}

async function changeStatus(newStatus: string) {
  actionError.value = ''
  // Clôture → checklist obligatoire via modal dédié
  if (newStatus === 'COMPLETED') {
    showEditStatus.value = false
    await openCloseModal()
    return
  }
  try {
    await projectApi.update(projectId, { status: newStatus } as Record<string, unknown>)
    showEditStatus.value = false
    await reload()
  } catch (e: unknown) { actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur' }
}

// Clôture projet — F3.8
interface ClosureCheck { code: string; label: string; passed: boolean; detail: string; severity?: string }
// Milestone creation (Gantt tab) — S-053
const showMilestoneForm = ref(false)
const ganttRefresh = ref(0)
const creatingMilestone = ref(false)
const milestoneError = ref('')
const milestoneForm = ref({
  name: '',
  date: '',
  color: '#2563EB',
  description: '',
})

function openCreateMilestone() {
  milestoneForm.value = {
    name: '',
    date: new Date().toISOString().slice(0, 10),
    color: '#2563EB',
    description: '',
  }
  milestoneError.value = ''
  showMilestoneForm.value = true
}

async function createMilestone() {
  milestoneError.value = ''
  if (!milestoneForm.value.name.trim() || !milestoneForm.value.date) {
    milestoneError.value = 'Nom et date sont obligatoires.'
    return
  }
  creatingMilestone.value = true
  try {
    await planningApi.createMilestone({
      project: projectId,
      title: milestoneForm.value.name.trim(),  // ← le modèle utilise 'title', pas 'name'
      date: milestoneForm.value.date,
      color: milestoneForm.value.color,
      description: milestoneForm.value.description,
    })
    showMilestoneForm.value = false
    ganttRefresh.value++
  } catch (e: unknown) {
    const data = (e as { response?: { data?: unknown } }).response?.data
    const obj = (data as Record<string, unknown>) || {}
    const errObj = obj.error as { message?: string } | undefined
    if (errObj?.message) milestoneError.value = errObj.message
    else {
      const parts: string[] = []
      for (const [field, val] of Object.entries(obj)) {
        if (Array.isArray(val)) parts.push(`${field}: ${val.join(', ')}`)
      }
      milestoneError.value = parts.length ? parts.join(' · ') : 'Erreur lors de la création'
    }
  } finally {
    creatingMilestone.value = false
  }
}

const showCloseModal = ref(false)
const closureChecks = ref<ClosureCheck[]>([])
const canClose = ref(false)
const closeLoading = ref(false)
const closeError = ref('')

async function openCloseModal() {
  closeError.value = ''
  closureChecks.value = []
  canClose.value = false
  showCloseModal.value = true
  try {
    const r = await apiClient.get(`projects/${projectId}/closure_checklist/`)
    const d = r.data?.data || r.data
    closureChecks.value = d?.checks || []
    canClose.value = Boolean(d?.can_close)
  } catch (e: unknown) {
    closeError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur lors du chargement'
  }
}

async function confirmClose() {
  closeError.value = ''
  closeLoading.value = true
  try {
    await projectApi.update(projectId, { status: 'COMPLETED' } as Record<string, unknown>)
    showCloseModal.value = false
    await reload()
  } catch (e: unknown) {
    closeError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur lors de la clôture'
  } finally {
    closeLoading.value = false
  }
}

async function deleteProject() {
  showDeleteConfirm.value = false
  try {
    await projectApi.delete(projectId)
  } catch { /* ok */ }
  router.push('/projects')
}

function openActionsMenu() {
  showActionsMenu.value = !showActionsMenu.value
}
function onAction(name: 'archive' | 'duplicate' | 'export' | 'delete') {
  showActionsMenu.value = false
  if (name === 'delete') {
    showDeleteConfirm.value = true
    return
  }
  actionError.value = `${name === 'archive' ? 'Archivage' : name === 'duplicate' ? 'Duplication' : 'Export'} — fonctionnalité à venir`
  setTimeout(() => { actionError.value = '' }, 3000)
}

async function deletePhase(phaseId: number) {
  confirmDeletePhase.value = null
  if (store.currentProject) {
    store.currentProject.phases = store.currentProject.phases.filter((p: { id: number }) => p.id !== phaseId)
  }
  try { await projectApi.deletePhase(projectId, phaseId) } catch { /* ok */ }
}

async function deleteAssignment(assignId: number) {
  confirmDeleteAssignment.value = null
  assignments.value = assignments.value.filter(a => a.id !== assignId)
  try { await apiClient.delete(`allocations/${assignId}/`) } catch { /* ok */ }
}

// Budget summary (original + current contract + approved amendments breakdown)
interface BudgetSummary {
  project_id: number
  original_contract_value: string
  current_contract_value: string
  total_approved_impact: string
  amendments: Array<{
    id: number
    amendment_number: number
    description: string
    budget_impact: string
    status: string
    approval_date: string | null
    approved_by_id: number | null
  }>
}
const budgetSummary = ref<BudgetSummary | null>(null)

async function loadBudgetSummary() {
  try {
    const r = await projectApi.budgetSummary(projectId)
    budgetSummary.value = r.data?.data || r.data || null
  } catch {
    budgetSummary.value = null
  }
}

onMounted(reload)

// Lazy load tab data (immediate: true → également au mount si URL pointe déjà sur l'onglet)
watch(activeTab, (tab) => {
  if (tab === 'tasks' && !tasks.value.length) loadTasks()
  if (tab === 'budget') { initHonoraires(); loadBudgetSummary() }
  if (tab === 'team') { if (!projectTimeEntries.value.length) loadProjectTime(); loadTeamStats(); syncTeamMembers(); loadTeams() }
  if (tab === 'time') loadProjectTime()
  if (tab === 'st') loadSTInvoices()
  if (tab === 'invoices') loadProjectInvoices()
}, { immediate: true })
</script>

<template>
  <div v-if="store.currentProject">
    <!-- Header -->
    <div class="page-header">
      <div>
        <button class="btn-back" @click="router.push('/projects')">&larr; Projets</button>
        <h1><span class="code">{{ store.currentProject.code }}</span> {{ store.currentProject.name }}</h1>
      </div>
      <div class="header-actions">
        <span v-if="store.currentProject.is_internal" class="badge-internal">Interne</span>
        <span v-if="!store.currentProject.is_public" class="badge badge-amber" style="cursor:default;">Privé</span>
        <template v-if="store.currentProject.is_consortium">
          <span class="badge badge-blue" style="cursor:default;">Consortium</span>
          <span v-if="consortiumData" class="badge badge-amber" style="cursor:default;">{{ consortiumData.pr_role === 'MANDATAIRE' ? 'Mandataire' : 'Partenaire' }} — {{ (consortiumData.members.find((m: Record<string, unknown>) => m.is_pr) as Record<string, unknown>)?.coefficient || '?' }}%</span>
          <button v-if="store.currentProject.consortium" class="btn-link" @click="router.push(`/consortiums/${store.currentProject.consortium}`)">Voir consortium →</button>
        </template>
        <!-- Status badge (clickable when user has edit rights) -->
        <div class="relative">
          <button class="badge" :class="statusColors[store.currentProject.status]" @click="canEdit && (showEditStatus = !showEditStatus)" :style="canEdit ? 'cursor:pointer' : 'cursor:default'">
            {{ statuses.find(s => s.value === store.currentProject?.status)?.label || store.currentProject.status }} <span v-if="canEdit">&#x25BE;</span>
          </button>
          <div v-if="showEditStatus && canEdit" class="status-dropdown">
            <button v-for="s in availableStatuses" :key="s.value" class="status-option" @click="changeStatus(s.value)">
              <span class="badge" :class="s.color">{{ s.label }}</span>
            </button>
            <div v-if="!availableStatuses.length" class="status-option" style="color:var(--color-gray-400);font-size:11px;cursor:default;">Aucune transition possible</div>
          </div>
        </div>
        <!-- Actions menu (replaces Paramètres/Terminer/Supprimer buttons) -->
        <div v-if="canEdit" class="relative">
          <button class="btn-ghost actions-trigger" @click="openActionsMenu" title="Actions du projet">⋮</button>
          <div v-if="showActionsMenu" class="actions-menu">
            <button class="actions-menu-item" @click="onAction('archive')">Archiver</button>
            <button class="actions-menu-item" @click="onAction('duplicate')">Dupliquer</button>
            <button class="actions-menu-item" @click="onAction('export')">Exporter</button>
            <div class="actions-menu-separator"></div>
            <button class="actions-menu-item danger" @click="onAction('delete')">Supprimer...</button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="actionError" class="alert-error">{{ actionError }}</div>

    <!-- Delete confirm banner -->
    <div v-if="showDeleteConfirm" class="alert-danger-banner">
      Supprimer définitivement ce projet ?
      <div class="banner-actions">
        <button class="btn-danger" @click="deleteProject">Confirmer la suppression</button>
        <button class="btn-ghost" @click="showDeleteConfirm = false">Annuler</button>
      </div>
    </div>

    <!-- Tabs (Sprint C — 5 root groups + sub-tabs) -->
    <TabGroup
      :tabs="rootTabs"
      :root-tab="rootTab"
      :sub-tab="currentSubTab"
      :storage-key="`project-${projectId}-tabs`"
      @update="onTabGroupUpdate"
    />

    <!-- ═══ Overview ═══ -->
    <template v-if="activeTab === 'overview'">
        <!-- KPIs unifiés (finance + heures) — 7 cards -->
        <div class="kpi-grid-7">
          <div class="kpi-card" title="Somme des budgets des tâches (Heures × Taux)"><div class="kpi-value mono">{{ formatAmount(taskBudgetTotal) }}&nbsp;$</div><div class="kpi-label">Budget tâches</div></div>
          <div class="kpi-card"><div class="kpi-value mono">{{ formatAmount(budgetInvoiced) }}&nbsp;$</div><div class="kpi-label">Facturé</div></div>
          <div class="kpi-card"><div class="kpi-value" :class="{ success: budgetConsumedPercent < 75, warning: budgetConsumedPercent >= 75, danger: budgetConsumedPercent >= 90 }">{{ budgetConsumedPercent }}&nbsp;%</div><div class="kpi-label">Consommé</div></div>
          <div class="kpi-card"><div class="kpi-value mono" :class="{ danger: budgetRemaining < 0 }">{{ formatAmount(budgetRemaining) }}&nbsp;$</div><div class="kpi-label">Solde restant</div></div>
          <div class="kpi-card"><div class="kpi-value mono">{{ dashboard ? fmt.hours(dashboard.hours_consumed) : '0' }}</div><div class="kpi-label">Heures consommées</div></div>
          <div class="kpi-card"><div class="kpi-value mono">{{ dashboard ? fmt.hours(dashboard.budget_hours) : '0' }}</div><div class="kpi-label">Heures budget</div></div>
          <div class="kpi-card" title="Somme des heures planifiées (allocations) sur les tâches"><div class="kpi-value mono text-primary">{{ fmt.hours(phasePlannedTotal) }}</div><div class="kpi-label">Heures planifiées</div></div>
        </div>

        <!-- Alertes centralisées (mockup 01) : un seul endroit, liens vers l'onglet concerné -->
        <div v-if="badDateTasks.length || tasksWithoutBudget.length || (taskPlannedTotal <= 0 && tasks.length > 0)" class="info-card" style="margin-bottom:12px;">
          <h3>⚠ Alertes</h3>
          <div class="alert-lines">
            <div v-for="t in badDateTasks" :key="'bd' + t.id" class="alert-line">
              🔴 <strong>{{ t.wbs_code }} {{ t.display_label || t.name }}</strong> — dates incohérentes (fin avant début)
              <button class="btn-link-inline" @click="activeTab = 'tasks'">Corriger dans l'Échéancier →</button>
            </div>
            <div v-if="tasksWithoutBudget.length" class="alert-line">
              🟠 <strong>{{ tasksWithoutBudget.length }} tâche{{ tasksWithoutBudget.length > 1 ? 's' : '' }} sans budget</strong> sur {{ tasks.length }}
              <button class="btn-link-inline" @click="activeTab = 'tasks'">Définir les budgets →</button>
            </div>
            <div v-if="taskPlannedTotal <= 0 && tasks.length > 0" class="alert-line">
              🟡 <strong>Aucune planification</strong> — aucune ressource n'est planifiée sur les tâches
              <button class="btn-link-inline" @click="activeTab = 'team'">Affecter l'équipe →</button>
            </div>
          </div>
        </div>
        <div class="info-grid">
          <div class="info-card"><h3>Informations <button v-if="isEditing" class="btn-action" @click="activeTab = 'params'">Modifier le projet</button></h3><div class="info-pairs"><div><span>Type de contrat</span><p>{{ store.currentProject.contract_type }}</p></div><div><span>Unité d'affaires</span><p>{{ store.currentProject.business_unit || '—' }}</p></div><div><span>Date début</span><p>{{ store.currentProject.start_date ? fmt.date(store.currentProject.start_date) : '—' }}</p></div><div><span>Date fin</span><p>{{ store.currentProject.end_date ? fmt.date(store.currentProject.end_date) : '—' }}</p></div><div><span>Public/Privé</span><p>{{ store.currentProject.is_public ? 'Public' : 'Privé' }}</p></div><div><span>Consortium</span><p>{{ store.currentProject.is_consortium ? 'Oui' : 'Non' }}</p></div><div v-if="!store.currentProject.is_internal"><span>Coût de construction</span><p>{{ store.currentProject.construction_cost != null && Number(store.currentProject.construction_cost) > 0 ? formatAmount(store.currentProject.construction_cost) + ' $' : '—' }}</p></div></div></div>
          <div class="info-card"><h3>Direction</h3><div class="info-pairs single"><div><span>Chef de projet</span><p>{{ allUsers.find(u => u.id === store.currentProject?.pm)?.username || store.currentProject.pm || '—' }}</p></div><div><span>Associé en charge</span><p>{{ allUsers.find(u => u.id === store.currentProject?.associate_in_charge)?.username || store.currentProject.associate_in_charge || '—' }}</p></div></div></div>
        </div>
        <div class="info-card" style="margin-top: 12px;">
          <h3>Client</h3>
          <div class="info-pairs"><div><span>Nom</span><p>{{ clientName }}</p></div><div v-if="clientContact"><span>Contact</span><p>{{ clientContact.name }}</p></div><div v-if="clientContact && clientContact.email"><span>Courriel</span><p>{{ clientContact.email }}</p></div><div v-if="clientContact && clientContact.phone"><span>Téléphone</span><p>{{ clientContact.phone }}</p></div></div>
        </div>
        <!-- Services transversaux (E-14) -->
        <div v-if="store.currentProject.services_transversaux?.length" class="info-card" style="margin-top: 12px;">
          <h3>Services transversaux</h3>
          <div class="flex flex-wrap gap-2" style="margin-top:8px;">
            <span v-for="svc in store.currentProject.services_transversaux" :key="svc" class="badge badge-blue">{{ svc }}</span>
          </div>
        </div>
        <!-- Consortium section (FR59) -->
        <div v-if="consortiumData" class="info-card" style="margin-top: 12px;">
          <h3>Consortium — {{ consortiumData.name }}</h3>
          <div class="info-pairs" style="margin-bottom:12px;">
            <div><span>Client (donneur d'ouvrage)</span><p>{{ consortiumData.client_name }}</p></div>
            <div><span>Rôle PR</span><p>{{ consortiumData.pr_role === 'MANDATAIRE' ? 'Mandataire (responsable)' : 'Partenaire' }}</p></div>
            <div v-if="consortiumData.contract_reference"><span>Réf. contrat</span><p>{{ consortiumData.contract_reference }}</p></div>
            <div><span>Statut</span><p><span class="badge" :class="consortiumData.status === 'ACTIVE' ? 'badge-green' : 'badge-gray'">{{ consortiumData.status === 'ACTIVE' ? 'Actif' : consortiumData.status }}</span></p></div>
          </div>
          <div v-if="consortiumData.members.length">
            <h4 style="font-size:11px;font-weight:600;color:var(--color-gray-500);text-transform:uppercase;margin-bottom:8px;">Membres ({{ consortiumData.members.length }})</h4>
            <table class="data-table" style="font-size:12px;">
              <thead><tr><th>Membre</th><th>Spécialité</th><th class="text-right">Coefficient</th></tr></thead>
              <tbody>
                <tr v-for="m in consortiumData.members" :key="m.id" :class="{ 'font-semibold': m.is_pr }">
                  <td>
                    <span v-if="m.is_pr" class="badge badge-blue" style="font-size:9px;margin-right:4px;">PR</span>
                    {{ m.display_name }}
                  </td>
                  <td class="text-muted">{{ m.specialty || '—' }}</td>
                  <td class="text-right font-mono">{{ m.coefficient }}%</td>
                </tr>
              </tbody>
              <tfoot>
                <tr>
                  <td colspan="2" class="font-semibold">Total</td>
                  <td class="text-right font-mono font-semibold" :class="{ danger: Number(consortiumData.total_coefficient) !== 100 }">
                    {{ consortiumData.total_coefficient }}%
                    <span v-if="Number(consortiumData.total_coefficient) !== 100" style="font-size:10px;color:var(--color-danger);margin-left:4px;">
                      (doit = 100%)
                    </span>
                  </td>
                </tr>
              </tfoot>
            </table>
          </div>
          <p v-else class="text-muted" style="font-size:12px;">Aucun membre — ajoutez des membres au consortium</p>
        </div>

        <!-- Phases summary table (E-27) -->
        <div v-if="store.currentProject.phases?.length" style="margin-top: 12px;">
          <p class="phase-form-hint" style="margin:0 0 6px;">Heures et budget = <strong>somme des tâches</strong>. <strong>%</strong> = avancement (réel / budget) ; <strong>Facturé</strong> = factures finalisées (envoyées / payées).</p>
          <table class="data-table">
            <thead>
              <tr>
                <th>Phase</th>
                <th style="width:100px;">Type</th>
                <th class="text-right" style="width:84px;">H. budget</th>
                <th class="text-right" style="width:84px;">H. planif.</th>
                <th class="text-right" style="width:84px;">H. réelles</th>
                <th class="text-right" style="width:64px;" title="Avancement en heures (réelles / budgétées)">% h.</th>
                <th class="text-right" style="width:110px;">Budget ($)</th>
                <th class="text-right" style="width:64px;" title="Avancement en coût (heures réelles × taux tâche / coût budgété)">% coût</th>
                <th class="text-right" style="width:110px;">Facturé ($)</th>
                <th class="text-right" style="width:64px;" title="Avancement honoraires (facturé / honoraires contractés)">% hon.</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="phase in (store.currentProject.phases || []).filter(Boolean)" :key="phase.id">
                <td class="font-semibold">
                  {{ phase.name }}
                  <span v-if="!phase.has_tasks" class="badge badge-gray" style="font-size:9px; margin-left:6px;">Sans tâche</span>
                </td>
                <td><span class="badge badge-gray">{{ phase.phase_type === 'SUPPORT' ? 'Support' : 'Réalisation' }}</span></td>
                <td class="text-right font-mono">{{ phase.has_tasks ? (phase.tasks_budgeted_hours || 0).toFixed(1) : '—' }}</td>
                <td class="text-right font-mono" :class="{ 'text-primary': (phase.planned_hours || 0) > 0 }">{{ phase.has_tasks ? (phase.planned_hours || 0).toFixed(1) : '—' }}</td>
                <td class="text-right font-mono" :class="{ 'font-semibold': (phase.actual_hours || 0) > 0 }">{{ phase.has_tasks ? (phase.actual_hours || 0).toFixed(1) : '—' }}</td>
                <td class="text-right font-mono" :class="{ 'text-danger': progressHoursPct(phase) > 100, 'text-success': progressHoursPct(phase) > 0 && progressHoursPct(phase) <= 100 }" :title="`${(phase.actual_hours || 0).toFixed(1)} / ${(phase.tasks_budgeted_hours || 0).toFixed(1)} h`">{{ phase.has_tasks && (phase.tasks_budgeted_hours || 0) > 0 ? progressHoursPct(phase).toFixed(0) + ' %' : '—' }}</td>
                <td class="text-right font-mono">{{ phase.has_tasks ? formatAmount(phase.tasks_budgeted_cost || 0) + ' $' : '—' }}</td>
                <td class="text-right font-mono" :class="{ 'text-danger': progressCostPct(phase) > 100, 'text-success': progressCostPct(phase) > 0 && progressCostPct(phase) <= 100 }" :title="`${formatAmount(phase.actual_cost || 0)} / ${formatAmount(phase.tasks_budgeted_cost || 0)} $`">{{ phase.has_tasks && (phase.tasks_budgeted_cost || 0) > 0 ? progressCostPct(phase).toFixed(0) + ' %' : '—' }}</td>
                <td class="text-right font-mono" :class="{ 'font-semibold': (phase.invoiced_amount || 0) > 0 }">{{ phase.has_tasks ? formatAmount(phase.invoiced_amount || 0) + ' $' : '—' }}</td>
                <td class="text-right font-mono" :class="{ 'text-primary': progressFeesPct(phase) > 0 }" :title="`${formatAmount(phase.invoiced_amount || 0)} / ${formatAmount(phase.fees_contract_amount || 0)} $`">{{ phase.has_tasks && (phase.fees_contract_amount || 0) > 0 ? progressFeesPct(phase).toFixed(0) + ' %' : '—' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
    </template>

    <!-- ═══ ⚙️ Paramètres ═══ -->
    <template v-if="activeTab === 'params'">
      <ProjectSettingsTab
        :project-id="Number(projectId)"
        :project="store.currentProject"
        :users="allUsers"
        :business-units="businessUnits"
        @updated="reload"
      />
    </template>

    <!-- ═══ Phases ═══ -->
    <template v-if="activeTab === 'phases'">
      <!-- Alertes budget + planification -->
      <div v-if="phaseBudgetTotal <= 0 && (store.currentProject.phases || []).length > 0" class="phase-alert alert-orange">
        &#9888;&#65039; <strong>Aucun budget defini</strong> — aucune phase n'a de budget en heures ou en dollars. Definissez les budgets pour suivre l'avancement.
      </div>
      <div v-else-if="phasesWithoutBudget.length > 0" class="phase-alert alert-amber">
        &#9888;&#65039; <strong>{{ phasesWithoutBudget.length }} phase{{ phasesWithoutBudget.length > 1 ? 's' : '' }} sans budget</strong> : {{ phasesWithoutBudget.map(p => p.name).join(', ') }}
      </div>
      <div v-if="phasePlannedTotal <= 0 && store.currentProject?.status === 'ACTIVE'" class="phase-alert alert-orange">
        &#128197; <strong>Aucune planification</strong> — aucune allocation de ressources n'est definie. <button class="btn-link-inline" @click="activeTab = 'gantt'">Aller a la planification &rarr;</button>
      </div>
      <div v-else-if="phaseFuturePlannedTotal <= 0 && store.currentProject?.status === 'ACTIVE'" class="phase-alert alert-red">
        &#128680; <strong>Pas de planification a venir</strong> — toutes les allocations sont dans le passe. Le projet est actif mais aucune ressource n'est planifiee pour les prochaines semaines. <button class="btn-link-inline" @click="activeTab = 'gantt'">Planifier &rarr;</button>
      </div>
      <div v-if="isAdmin" class="section-actions" style="margin-bottom:10px;">
        <button class="btn-primary" @click="showAddPhaseForm = !showAddPhaseForm">+ Ajouter une phase</button>
      </div>
      <p v-else class="phase-form-hint" style="margin-bottom:10px;">
        Les phases sont définies dans le <strong>paramétrage</strong> du cabinet (administrateur). Vous pouvez y rattacher des tâches dans l'onglet Tâches.
      </p>
      <div v-if="showAddPhaseForm && isAdmin" class="card" style="margin-bottom:10px;">
        <p class="phase-form-hint">Une phase est un regroupement standard. Le budget, les heures et le mode de facturation se définissent sur ses <strong>tâches</strong>.</p>
        <div class="form-row-2">
          <div class="form-group"><label>Nom interne *</label><input v-model="newPhase.name" placeholder="Concept" /></div>
          <div class="form-group"><label>Libellé client</label><input v-model="newPhase.client_facing_label" placeholder="Phase 1 — Concept" /></div>
        </div>
        <div class="form-row-2">
          <div class="form-group"><label>Type</label>
            <select v-model="newPhase.phase_type"><option value="REALIZATION">Réalisation</option><option value="SUPPORT">Support</option></select>
          </div>
          <div class="form-group"><label>Ordre</label><input v-model.number="newPhase.order" type="number" min="0" /></div>
        </div>
        <div class="form-actions"><button class="btn-ghost" @click="showAddPhaseForm = false">Annuler</button><button class="btn-primary" @click="addPhase">Ajouter</button></div>
      </div>
      <div class="card-table" style="overflow-x:auto;">
        <table style="table-layout:auto; width:100%; min-width:1080px;">
          <thead><tr>
            <th style="min-width:180px;">Phase</th><th style="width:95px; white-space:nowrap;">Type</th>
            <th class="text-right" style="width:115px; white-space:nowrap;">Budget ($) <span class="agg-mark" title="Somme des tâches">Σ</span></th>
            <th class="text-right" style="width:100px; white-space:nowrap;">H. budget <span class="agg-mark" title="Somme des tâches">Σ</span></th>
            <th class="text-right" style="width:100px; white-space:nowrap;">H. planif. <span class="agg-mark" title="Somme des tâches">Σ</span></th>
            <th class="text-right" style="width:100px; white-space:nowrap;">H. réelles <span class="agg-mark" title="Somme des tâches">Σ</span></th>
            <th class="text-right" style="width:85px; white-space:nowrap;">Écart</th>
            <th style="width:110px; white-space:nowrap;">Statut</th>
            <th v-if="isEditing" class="text-right" style="white-space:nowrap;">Actions</th>
          </tr></thead>
          <tbody>
            <tr v-for="phase in (store.currentProject.phases || []).filter(Boolean)" :key="phase.id" :class="{ 'phase-empty-row': !phase.has_tasks }">
              <template v-if="editingPhaseId === phase.id">
                <td><input v-model="phaseForm.name" class="inline-input" /></td>
                <td><select v-model="phaseForm.phase_type" class="inline-select"><option value="REALIZATION">Réalisation</option><option value="SUPPORT">Support</option></select></td>
                <td class="text-right">—</td>
                <td class="text-right">—</td>
                <td class="text-right">—</td>
                <td class="text-right">—</td>
                <td class="text-right">—</td>
                <td>—</td>
                <td class="text-right actions-cell">
                  <button class="btn-action" @click="savePhase">OK</button>
                  <button class="btn-action" @click="editingPhaseId = null">×</button>
                </td>
              </template>
              <template v-else>
                <td class="font-semibold" style="max-width:220px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;" :title="(phase.client_facing_label ? phase.client_facing_label + ' — ' : '') + phase.name">
                  {{ phase.name }}
                  <span v-if="!phase.has_tasks" class="badge badge-gray" style="margin-left:6px; font-size:9px;" title="Phase standard sans tâche — masquée dans les écrans de saisie">Sans tâche</span>
                  <span v-if="phase.amendment_number" class="badge badge-purple" style="margin-left:6px; font-size:9px;" :title="'Phase ajoutée via avenant #' + phase.amendment_number">AV-{{ phase.amendment_number }}</span>
                </td>
                <td><span class="badge badge-gray">{{ phase.phase_type === 'SUPPORT' ? 'Support' : 'Réalisation' }}</span></td>
                <td class="text-right font-mono agg-cell" style="font-size:11px;">{{ phase.has_tasks ? formatAmount(phase.tasks_budgeted_cost || 0) + ' $' : '—' }}</td>
                <td class="text-right font-mono agg-cell" style="font-size:11px;">{{ phase.has_tasks ? (phase.tasks_budgeted_hours || 0).toFixed(1) : '—' }}</td>
                <td class="text-right font-mono agg-cell" style="font-size:11px;" :class="{ 'text-primary': (phase.planned_hours || 0) > 0 }">{{ phase.has_tasks ? (phase.planned_hours || 0).toFixed(1) : '—' }}</td>
                <td class="text-right font-mono agg-cell" style="font-size:11px;" :class="{ 'font-semibold': (phase.actual_hours || 0) > 0 }">{{ phase.has_tasks ? (phase.actual_hours || 0).toFixed(1) : '—' }}</td>
                <td class="text-right font-mono" style="font-size:11px;" :class="{
                  'text-success': (phase.actual_hours || 0) <= (phase.tasks_budgeted_hours || 0),
                  'text-danger': (phase.actual_hours || 0) > (phase.tasks_budgeted_hours || 0) && (phase.tasks_budgeted_hours || 0) > 0,
                }">{{ phase.has_tasks ? ((phase.actual_hours || 0) - (phase.tasks_budgeted_hours || 0)).toFixed(1) : '—' }}</td>
                <td>
                  <span v-if="phase.is_locked" class="badge badge-gray">🔒 Verrouillée</span>
                  <span v-else class="badge badge-green">Active</span>
                </td>
                <td v-if="isEditing" class="text-right actions-cell">
                    <button v-if="isAdmin" class="btn-action" @click="startEditPhase(phase)">Modifier</button>
                    <template v-if="isAdmin">
                      <span v-if="phase.is_mandatory" class="badge badge-amber" style="font-size:9px;cursor:default;">&#x1F512; Obligatoire</span>
                      <template v-else-if="confirmDeletePhase === phase.id">
                        <button class="btn-action danger" @click="deletePhase(phase.id)">Confirmer</button>
                        <button class="btn-action" @click="confirmDeletePhase = null">Annuler</button>
                      </template>
                      <button v-else class="btn-action danger" @click="confirmDeletePhase = phase.id">Supprimer...</button>
                    </template>
                </td>
              </template>
            </tr>
            <tr v-if="!store.currentProject.phases?.length"><td colspan="9" class="empty">Aucune phase</td></tr>
          </tbody>
        </table>
      </div>
    </template>

    <!-- ═══ Tâches ═══ -->
    <template v-if="activeTab === 'tasks'">
      <!-- Démarrage depuis un modèle : uniquement si le projet n'a aucune tâche -->
      <TaskTemplatePicker v-if="!tasks.length" :project-id="projectId" @created="onTemplateTasksCreated" />
      <!-- Alertes budget + planification -->
      <div v-if="taskBudgetTotal <= 0 && tasks.length > 0" class="phase-alert alert-orange">
        &#9888;&#65039; <strong>Aucun budget sur les taches</strong> — definissez les heures et couts budgetes pour chaque tache.
      </div>
      <div v-else-if="tasksWithoutBudget.length > 0 && tasksWithoutBudget.length < tasks.length" class="phase-alert alert-amber">
        &#9888;&#65039; <strong>{{ tasksWithoutBudget.length }} tache{{ tasksWithoutBudget.length > 1 ? 's' : '' }} sans budget</strong> sur {{ tasks.length }}
      </div>
      <div v-if="taskPlannedTotal <= 0 && tasks.length > 0 && store.currentProject?.status === 'ACTIVE'" class="phase-alert alert-orange">
        &#128197; <strong>Aucune planification sur les taches</strong> — les ressources ne sont pas encore planifiees. <button class="btn-link-inline" @click="activeTab = 'gantt'">Planifier &rarr;</button>
      </div>
      <!-- Ajout global d'une tâche : choisir n'importe quelle phase (même vide) -->
      <div v-if="isEditing && allProjectPhases.length" class="tasks-toolbar">
        <button v-if="!showGlobalAddTask" class="btn-primary btn-sm" @click="showGlobalAddTask = true; newTaskPhaseId = null; newTaskName = ''">+ Tâche</button>
        <div v-else class="task-add-row">
          <select v-model.number="newTaskPhaseId" class="inline-select" style="min-width:160px;">
            <option :value="null">— Choisir une phase —</option>
            <option v-for="p in allProjectPhases" :key="p.id" :value="p.id">{{ p.name }}</option>
          </select>
          <input v-model="newTaskName" class="inline-input" placeholder="Nom de la tâche" @keydown.enter="newTaskPhaseId && addTask(newTaskPhaseId)" />
          <button class="btn-primary btn-sm" :disabled="!newTaskPhaseId || !newTaskName.trim()" @click="addTask(newTaskPhaseId)">Ajouter</button>
          <button class="btn-ghost btn-sm" @click="showGlobalAddTask = false">Annuler</button>
        </div>
        <button class="btn-ghost btn-sm" style="margin-left:auto;" title="Décaler toutes les dates de tâches de N jours (échéancier qui glisse)" @click="showShiftBand = !showShiftBand">↔️ Décaler l'échéancier…</button>
      </div>
      <div v-if="showShiftBand && isEditing" class="shift-band" data-shift-band>
        ↔️ <strong>Décaler l'échéancier</strong> : déplacer toutes les tâches datées de
        <input v-model.number="shiftDays" type="number" class="inline-input" style="width:64px;" /> jours
        (négatif = avancer)
        <button class="btn-primary btn-sm" :disabled="shifting || !shiftDays" @click="applyShift">{{ shifting ? 'Décalage…' : 'Appliquer' }}</button>
        <button class="btn-ghost btn-sm" :disabled="shifting" @click="showShiftBand = false">Annuler</button>
        <span class="text-muted" style="font-size:11px;">Les dates de phase suivent automatiquement (dérivées).</span>
      </div>

      <div v-if="visibleTaskPhaseGroups.length">
        <div v-for="group in visibleTaskPhaseGroups" :key="group.phase_name" class="task-phase-group">
          <!-- Phase header -->
          <div class="task-phase-header" @click="togglePhaseCollapse(group.phase_name)">
            <span class="task-phase-toggle">{{ collapsedPhases.has(group.phase_name) ? '&#9654;' : '&#9660;' }}</span>
            <span class="font-semibold">{{ group.phase_name }}</span>
            <span class="text-muted" style="margin-left:8px;">({{ group.tasks.length }} tâche{{ group.tasks.length > 1 ? 's' : '' }})</span>
            <button v-if="isEditing" class="btn-action" style="margin-left:auto;" @click.stop="showAddTaskPhase = group.phase_id; newTaskName = ''">+ Tâche</button>
            <button v-if="isEditing" class="btn-action" style="margin-left:6px;" @click.stop="showTemplatePhase = showTemplatePhase === group.phase_id ? null : group.phase_id">+ depuis le modèle</button>
          </div>

          <!-- Add task form -->
          <div v-if="showAddTaskPhase === group.phase_id && isEditing" class="task-add-row">
            <input v-model="newTaskName" class="inline-input" placeholder="Nom de la tâche" @keydown.enter="addTask(group.phase_id)" />
            <button class="btn-primary btn-sm" @click="addTask(group.phase_id)">Ajouter</button>
            <button class="btn-ghost btn-sm" @click="showAddTaskPhase = null">Annuler</button>
          </div>

          <!-- Ajout depuis le catalogue standard (ciblé sur la phase, dédup) -->
          <TaskTemplatePicker
            v-if="showTemplatePhase === group.phase_id && isEditing"
            :project-id="projectId"
            :phase-id="group.phase_id"
            @created="onPhaseTemplateCreated"
          />

          <!-- Tasks table -->
          <table v-if="!collapsedPhases.has(group.phase_name)" class="data-table task-table" style="table-layout:auto; width:100%; min-width:1150px;">
            <thead>
              <tr>
                <th style="width:85px;">WBS</th>
                <th style="width:170px;">Nom</th>
                <th style="width:112px;">Début</th>
                <th style="width:112px;">Fin</th>
                <th style="width:35px;">Mode</th>
                <th class="text-right" style="width:75px;">Budget ($)</th>
                <th class="text-right" style="width:60px;">H. budg.</th>
                <th class="text-right" style="width:60px;">H. planif.</th>
                <th class="text-right" style="width:60px;">H. réel</th>
                <th class="text-right" style="width:55px;">Écart</th>
                <th style="width:40px;">Fact.</th>
                <th v-if="isEditing" style="width:200px;">Actions</th>
              </tr>
            </thead>
            <tbody>
              <template v-for="task in group.tasks" :key="task.id">
              <tr :class="{ 'subtask-row': task.task_type === 'SUBTASK' }" :style="!task.is_active ? 'opacity:0.6;' : ''">
                <td style="font-size:11px; color:var(--color-gray-500);">{{ task.wbs_code || '—' }}</td>
                <td
                  style="max-width:180px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;"
                  :title="'Ouvrir la fiche tâche — ' + (task.display_label || task.name)"
                >
                  <span v-if="task.task_type === 'SUBTASK'" class="subtask-indent"></span>
                  <template v-if="editingTaskNameId === task.id">
                    <input
                      v-model="editTaskNameValue"
                      class="budget-input"
                      style="width: 100%; font-size:13px;"
                      autofocus
                      @keydown.enter="commitEditTaskName(task.id)"
                      @keydown.esc="cancelEditTaskName"
                      @blur="commitEditTaskName(task.id)" />
                  </template>
                  <template v-else>
                    <span class="task-name-link" @click="openTaskSheet(task.id)">{{ task.display_label || task.name }}</span>
                    <span v-if="task.amendment_number" class="badge badge-purple" style="margin-left:6px; font-size:9px;" :title="'Tâche ajoutée via avenant #' + task.amendment_number">AV-{{ task.amendment_number }}</span>
                    <span v-if="!task.is_active" class="badge badge-gray" style="margin-left:6px; font-size:9px;" title="Tâche fermée : saisie de temps bloquée">Fermée</span>
                  </template>
                </td>
                <td>
                  <input v-if="!isTaskReadOnly(task)" type="date" class="date-inline" :value="task.start_date || ''" :disabled="!isEditing" @change="(e: Event) => onTaskDateInline(task, 'start_date', e)" />
                  <span v-else class="date-derived" title="Dérivé des sous-tâches">{{ derivedFor(task).start || '—' }}</span>
                </td>
                <td>
                  <input v-if="!isTaskReadOnly(task)" type="date" class="date-inline" :value="task.end_date || ''" :disabled="!isEditing" @change="(e: Event) => onTaskDateInline(task, 'end_date', e)" />
                  <span v-else class="date-derived" title="Dérivé des sous-tâches">{{ derivedFor(task).end || '—' }}</span>
                </td>
                <td><span class="badge" :class="task.billing_mode === 'HORAIRE' ? 'badge-amber' : 'badge-blue'" style="font-size:10px;">{{ task.billing_mode === 'HORAIRE' ? 'H' : 'F' }}</span></td>
                <td class="text-right">
                  <template v-if="canEditBudget && !isTaskReadOnly(task)">
                    <input class="budget-input" :value="task.budgeted_cost" type="text" inputmode="decimal"
                      @blur="(e: Event) => { const v = parseFloat(((e.target as HTMLInputElement).value || '0').replace(/\\s/g, '').replace(',', '.')); if (!isNaN(v)) saveTaskField(task.id, 'budgeted_cost', v) }"
                      @keydown.enter="(e: Event) => (e.target as HTMLInputElement).blur()" />
                  </template>
                  <template v-else><span class="font-mono" :class="{ 'agg-cell': isTaskReadOnly(task) }" style="font-size:11px;" :title="isTaskReadOnly(task) ? 'Somme des sous-tâches' : ''">{{ formatAmount(task.effective_budgeted_cost ?? task.budgeted_cost) }}</span></template>
                </td>
                <td class="text-right">
                  <template v-if="canEditBudget && !isTaskReadOnly(task)">
                    <input class="budget-input" :value="task.budgeted_hours" type="text" inputmode="decimal"
                      @blur="(e: Event) => { const v = parseFloat(((e.target as HTMLInputElement).value || '0').replace(/\\s/g, '').replace(',', '.')); if (!isNaN(v)) saveTaskField(task.id, 'budgeted_hours', v) }"
                      @keydown.enter="(e: Event) => (e.target as HTMLInputElement).blur()" />
                  </template>
                  <template v-else><span class="font-mono" :class="{ 'agg-cell': isTaskReadOnly(task) }" style="font-size:11px;" :title="isTaskReadOnly(task) ? 'Somme des sous-tâches' : ''">{{ Number(task.effective_budgeted_hours ?? task.budgeted_hours ?? 0).toFixed(1) }}</span></template>
                </td>
                <td class="text-right font-mono" style="font-size:11px;" :class="{ 'text-primary': (task.planned_hours || 0) > 0 }">{{ (task.planned_hours || 0).toFixed(1) }}</td>
                <td class="text-right font-mono" style="font-size:11px;" :class="{ 'font-semibold': (task.actual_hours || 0) > 0 }">{{ (task.actual_hours || 0).toFixed(1) }}</td>
                <td class="text-right font-mono" style="font-size:11px;" :class="{
                  'text-success': (task.actual_hours || 0) <= Number(task.effective_budgeted_hours ?? task.budgeted_hours ?? 0),
                  'text-danger': (task.actual_hours || 0) > Number(task.effective_budgeted_hours ?? task.budgeted_hours ?? 0) && Number(task.effective_budgeted_hours ?? task.budgeted_hours ?? 0) > 0,
                }">{{ ((task.actual_hours || 0) - Number(task.effective_budgeted_hours ?? task.budgeted_hours ?? 0)).toFixed(1) }}</td>
                <td>
                  <span v-if="task.is_billable" class="badge badge-green" style="font-size:9px;">Oui</span>
                  <span v-else class="badge badge-gray" style="font-size:9px;">Non</span>
                </td>
                <td v-if="isEditing" class="actions-cell">
                  <template v-if="isTaskReadOnly(task)">
                    <span class="badge badge-amber" style="font-size:9px;" title="Tâche-mère : regroupement de sous-tâches, en lecture seule">Regroupement</span>
                    <button class="btn-action" @click="enterInlineNameEdit(task)">Renommer</button>
                    <button class="btn-action" @click="showAddSubtask = task.id; newSubtaskName = ''">+ Sous-tâche</button>
                    <button v-if="task.is_active" class="btn-action" @click="setTaskClosed(task, true)" title="Fermer la tâche et ses sous-tâches : bloque la saisie de temps">Fermer</button>
                    <button v-else class="btn-action" @click="setTaskClosed(task, false)" title="Rouvrir la tâche et ses sous-tâches">Rouvrir</button>
                  </template>
                  <template v-else>
                    <button class="btn-action" @click="openTaskEditModal(task)">Modifier</button>
                    <button v-if="task.is_active" class="btn-action" @click="setTaskClosed(task, true)" title="Fermer : bloque la saisie de temps sur cette tâche">Fermer</button>
                    <button v-else class="btn-action" @click="setTaskClosed(task, false)" title="Rouvrir : autorise à nouveau la saisie">Rouvrir</button>
                    <button v-if="task.task_type !== 'SUBTASK'" class="btn-action" @click="showAddSubtask = task.id; newSubtaskName = ''">+ Sous-tâche</button>
                    <template v-if="movingTaskId === task.id">
                      <select v-model.number="moveTargetPhaseId" class="inline-select">
                        <option v-for="p in allProjectPhases" :key="p.id" :value="p.id">{{ p.name }}</option>
                      </select>
                      <button class="btn-action primary" @click="moveTask(task.id)">OK</button>
                      <button class="btn-action" @click="movingTaskId = null">×</button>
                    </template>
                    <button v-else-if="task.task_type !== 'SUBTASK'" class="btn-action" @click="startMoveTask(task)" title="Ré-imputer cette tâche à une autre phase">Déplacer…</button>
                    <template v-if="confirmDeleteTask === task.id">
                      <button class="btn-action danger" @click="removeTask(task.id)">Confirmer</button>
                      <button class="btn-action" @click="confirmDeleteTask = null">Annuler</button>
                    </template>
                    <button v-else class="btn-action danger" @click="confirmDeleteTask = task.id">Supprimer</button>
                  </template>
                </td>
              </tr>
              <!-- Inline subtask form (inside template v-for scope) -->
              <tr v-if="showAddSubtask === task.id && isEditing" class="subtask-add-row">
                <td></td>
                <td colspan="5">
                  <div class="flex items-center gap-2" style="padding:4px 0;">
                    <span class="subtask-indent"></span>
                    <input v-model="newSubtaskName" class="inline-input" style="flex:1;" placeholder="Nom de la sous-tâche" @keydown.enter="addSubtask(task.id)" />
                    <button class="btn-primary btn-sm" @click="addSubtask(task.id)">Ajouter</button>
                    <button class="btn-ghost btn-sm" @click="showAddSubtask = null">Annuler</button>
                  </div>
                </td>
                <td v-if="isEditing"></td>
              </tr>
              </template>
            </tbody>
          </table>
        </div>
      </div>
      <div v-else-if="!allProjectPhases.length" class="card empty-card">
        Ce projet n'a pas encore de phase. Ajoute une phase dans
        <a href="#" class="link" @click.prevent="activeTab = 'phases'">l'onglet Phases</a>
        pour pouvoir y créer des tâches.
      </div>
      <div v-else class="card empty-card">
        Aucune tâche pour l'instant. Utilise <strong>+ Tâche</strong> ci-dessus pour en créer une dans une phase (même une phase encore vide).
      </div>
    </template>

    <!-- ═══ Team ═══ -->
    <template v-if="activeTab === 'team'">
      <!-- Budget health banner -->
      <div v-if="teamStats" class="team-budget-banner" :class="{
        'banner-green': teamStats.budget_status === 'green',
        'banner-orange': teamStats.budget_status === 'orange',
        'banner-red': teamStats.budget_status === 'red',
      }">
        <span v-if="teamStats.budget_status === 'green'">&#9989; Projet dans le budget — aucune phase en depassement</span>
        <span v-else-if="teamStats.budget_status === 'orange'">&#9888;&#65039; {{ teamStats.over_budget_phases }} phase{{ teamStats.over_budget_phases > 1 ? 's' : '' }} en depassement sur {{ teamStats.total_phases }}</span>
        <span v-else>&#128680; {{ teamStats.over_budget_phases }} phases en depassement sur {{ teamStats.total_phases }} — attention budget critique</span>
        <button class="btn-action" style="margin-left:auto; font-size:10px; color:inherit;" @click="activeTab = 'phases'">Voir phases &#8594;</button>
      </div>

      <!-- Team summary KPIs — toujours visibles (même si équipe vide pour orienter l'utilisateur) -->
      <div class="kpi-grid-4" style="margin-bottom:16px;">
        <div class="kpi-card">
          <div class="kpi-value">{{ teamByEmployee.length }}</div>
          <div class="kpi-label">Membres</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-value mono">{{ assignments.length }}</div>
          <div class="kpi-label">Affectations</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-value mono" :class="{ 'text-primary': teamByEmployee.length && teamByEmployee.some(m => m.hasPlanning), 'text-danger': teamByEmployee.length && !teamByEmployee.some(m => m.hasPlanning) }">
            {{ teamByEmployee.filter(m => m.hasPlanning).length }} / {{ teamByEmployee.length }}
          </div>
          <div class="kpi-label">Planifiés</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-value mono">{{ projectTotalHours.toFixed(1) }}h</div>
          <div class="kpi-label">H. réelles totales</div>
        </div>
      </div>

      <!-- Affecter une équipe (paramétrage) en entier sur le projet -->
      <div v-if="canManageMembers && teams.length" data-team-assign style="display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-bottom:12px; padding:10px 12px; background:var(--color-gray-50); border:1px solid var(--color-gray-200); border-radius:6px;">
        <span style="font-size:12px; font-weight:600; color:var(--color-gray-600);">Affecter une équipe :</span>
        <select v-model.number="assignTeamId" class="select-sm" data-team-assign-select style="min-width:200px; padding:4px 8px; border:1px solid var(--color-gray-300); border-radius:4px; font-size:12px;">
          <option :value="null">— Choisir une équipe —</option>
          <option v-for="t in teams" :key="t.id" :value="t.id">{{ t.name }} ({{ t.member_details.length }} membre{{ t.member_details.length > 1 ? 's' : '' }})</option>
        </select>
        <button class="btn-action primary" :disabled="!assignTeamId || assigningTeam" data-team-assign-confirm @click="assignTeam">{{ assigningTeam ? '…' : "Affecter l'équipe" }}</button>
      </div>

      <!-- Membres de l'équipe — autorise la saisie de temps sans planification -->
      <TeamMembersPanel
        :members="teamMembers"
        :addable-users="addableUsers"
        :can-manage="canManageMembers"
        :saving="memberSaving"
        :error="memberError"
        @add="addTeamMember"
        @remove="removeTeamMember"
      />


      <!-- Barre d'outils : mode (Par phase / Par personne) + recherche -->
      <div class="team-toolbar">
        <div class="team-view-toggle">
          <button class="time-view-btn" :class="{ active: teamViewMode === 'phase' }" @click="teamViewMode = 'phase'">Par phase</button>
          <button class="time-view-btn" :class="{ active: teamViewMode === 'person' }" @click="teamViewMode = 'person'">Par personne</button>
        </div>
        <input v-model="teamSearch" class="team-search" type="text" placeholder="Rechercher où une personne est affectée…" />
        <button v-if="canEditBudget" class="btn-action primary" data-open-assign @click="openAssignDialog()">+ Affectation</button>
        <div v-if="teamViewMode === 'phase'" class="team-expand-actions">
          <button class="btn-action" @click="expandAllTeamPhases">Tout étendre</button>
          <button class="btn-action" @click="collapseAllTeamPhases">Tout réduire</button>
        </div>
      </div>

      <!-- ── Vue « Par phase » : accordéons Phase → Tâche → Sous-tâche + personnes ── -->
      <template v-if="teamViewMode === 'phase'">
        <div v-if="teamPhaseTree.length" class="phase-tree">
          <div v-for="ph in teamPhaseTree" :key="ph.phase_id ?? ph.phase_name" class="phase-acc">
            <div class="phase-acc-head" @click="togglePhaseOpen(ph.phase_id)">
              <span class="acc-caret">{{ isPhaseOpen(ph.phase_id) ? '▼' : '▶' }}</span>
              <span class="phase-acc-name">{{ ph.phase_name }}</span>
              <span class="acc-count">{{ ph.tasks.length }} tâche{{ ph.tasks.length > 1 ? 's' : '' }}</span>
              <span class="people-chips">
                <span v-for="p in ph.people" :key="p.key" class="person-chip" :class="{ 'person-chip--virtual': p.kind === 'virtual' }">{{ p.name }}</span>
              </span>
              <span v-if="canEditBudget && ph.phase_id != null && ph.tasks.length" class="node-close" @click.stop>
                <button v-if="!isPhaseClosed(Number(ph.phase_id))" class="btn-action danger" title="Fermer toutes les tâches de la phase (bloque la saisie pour tout le monde)" @click="setPhaseClosed(Number(ph.phase_id), true)">🔒 Fermer la phase</button>
                <button v-else class="btn-action" title="Rouvrir toutes les tâches de la phase" @click="setPhaseClosed(Number(ph.phase_id), false)">Rouvrir la phase</button>
              </span>
              <span v-if="canEditBudget && ph.phase_id != null" class="phase-team-assign" @click.stop>
                <button class="btn-action" title="Affecter un employé, une équipe ou un profil virtuel à cette phase" @click="openAssignDialog({ type: 'phase', id: Number(ph.phase_id) })">+ Affecter</button>
              </span>
            </div>
            <div v-if="isPhaseOpen(ph.phase_id)" class="phase-acc-body">
              <div v-for="t in ph.tasks" :key="t.id" class="tpn">
                <div class="tpn-head" @click="t.subtasks.length && toggleTaskOpen(t.id)">
                  <span v-if="t.subtasks.length" class="acc-caret">{{ isTaskOpen(t.id) ? '▼' : '▶' }}</span>
                  <span v-else class="acc-dot">•</span>
                  <span class="tpn-wbs">{{ t.wbs_code }}</span>
                  <span class="tpn-name" :class="{ 'tpn-closed': !t.is_active }">{{ t.name }}</span>
                  <span v-if="!t.is_active" class="badge badge-gray tpn-badge">Fermée</span>
                  <span class="people-chips">
                    <span v-for="p in t.people" :key="p.key" class="person-chip" :class="{ 'person-chip--virtual': p.kind === 'virtual' }">{{ p.name }}</span>
                    <span v-if="!t.people.length && !t.subtasks.length" class="tpn-noone">aucune personne</span>
                  </span>
                  <span v-if="canEditBudget" class="node-close" @click.stop>
                    <button v-if="t.is_active" class="btn-action danger" :title="t.subtasks.length ? 'Fermer la tâche et ses sous-tâches (tout le monde)' : 'Fermer : bloque la saisie pour tout le monde'" @click="toggleNodeClosed(t.id)">🔒 Fermer</button>
                    <button v-else class="btn-action" title="Rouvrir" @click="toggleNodeClosed(t.id)">Rouvrir</button>
                  </span>
                </div>
                <div v-if="t.subtasks.length && isTaskOpen(t.id)" class="tpn-children">
                  <div v-for="s in t.subtasks" :key="s.id" class="tpn tpn-sub">
                    <div class="tpn-head">
                      <span class="acc-dot">•</span>
                      <span class="tpn-wbs">{{ s.wbs_code }}</span>
                      <span class="tpn-name" :class="{ 'tpn-closed': !s.is_active }">{{ s.name }}</span>
                      <span v-if="!s.is_active" class="badge badge-gray tpn-badge">Fermée</span>
                      <span class="people-chips">
                        <span v-for="p in s.people" :key="p.key" class="person-chip" :class="{ 'person-chip--virtual': p.kind === 'virtual' }">{{ p.name }}</span>
                        <span v-if="!s.people.length" class="tpn-noone">aucune personne</span>
                      </span>
                      <span v-if="canEditBudget" class="node-close" @click.stop>
                        <button v-if="s.is_active" class="btn-action danger" title="Fermer : bloque la saisie pour tout le monde" @click="toggleNodeClosed(s.id)">🔒 Fermer</button>
                        <button v-else class="btn-action" title="Rouvrir" @click="toggleNodeClosed(s.id)">Rouvrir</button>
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="card empty-card">
          {{ isTeamSearching ? 'Aucune personne trouvée pour cette recherche.' : 'Aucune phase avec tâche — créez des tâches dans l’onglet Structure.' }}
        </div>
      </template>

      <!-- Team list by employee (accordion) -->
      <div v-else-if="teamByEmployee.length" class="team-list">
        <div v-for="member in teamByEmployee" :key="member.employee" class="team-member-card">
          <!-- Employee header (clickable) -->
          <div class="team-member-header" @click="toggleTeamMember(member.employee)">
            <div class="team-member-left">
              <span class="team-toggle">{{ expandedTeamMembers.has(member.employee) ? '&#9660;' : '&#9654;' }}</span>
              <span class="team-avatar" :class="{ 'avatar-noplanning': !member.hasPlanning }">{{ member.employee_name.substring(0, 2).toUpperCase() }}</span>
              <div>
                <div class="team-name" :class="{ 'name-blocked': isPersonFullyBlocked(member.employee) }">
                  {{ member.employee_name }}
                  <span v-if="isPersonFullyBlocked(member.employee)" class="badge badge-red" style="font-size:9px;margin-left:6px;">Bloqué</span>
                </div>
                <div class="team-sub">
                  {{ member.assignments.length }} phase{{ member.assignments.length > 1 ? 's' : '' }}
                  <span v-if="!member.hasPlanning" class="team-no-planning">&#9888; Pas de planification</span>
                </div>
              </div>
            </div>
            <div class="team-member-right">
              <button v-if="canEditBudget" class="btn-action" :class="{ danger: !isPersonFullyBlocked(member.employee) }" style="font-size:10px;" :title="isPersonFullyBlocked(member.employee) ? 'Rouvrir la saisie sur tout le projet' : 'Bloquer la saisie de cette personne sur tout le projet'" @click.stop="togglePersonBlock(member.employee)">
                {{ isPersonFullyBlocked(member.employee) ? 'Rouvrir (projet)' : '🔒 Bloquer (projet)' }}
              </button>
              <div class="team-hours">
                <span class="team-hours-label">Planifié</span>
                <span class="team-hours-value" :class="member.hasPlanning ? 'text-primary' : 'team-no-planning'">{{ member.totalPlanned.toFixed(1) }}h</span>
              </div>
              <div class="team-hours">
                <span class="team-hours-label">Réel</span>
                <span class="team-hours-value" :class="{ 'font-semibold': member.totalActual > 0 }">{{ member.totalActual.toFixed(1) }}h</span>
              </div>
            </div>
          </div>

          <!-- Accordion content -->
          <div v-if="expandedTeamMembers.has(member.employee)" class="team-member-detail">
            <!-- Monthly chart (6 months) -->
            <div v-if="member.monthlyHours.length" class="team-chart">
              <div class="team-chart-title">Historique mensuel (heures reelles)</div>
              <div class="team-chart-bars">
                <div v-for="m in member.monthlyHours" :key="m.month" class="team-chart-bar">
                  <div class="team-chart-val">{{ m.hours.toFixed(0) }}</div>
                  <div class="team-chart-fill" :style="{ height: `${Math.min(100, m.hours / (Math.max(...member.monthlyHours.map(x => x.hours)) || 1) * 100)}%` }"></div>
                  <div class="team-chart-label">{{ m.month.substring(5) }}</div>
                </div>
              </div>
            </div>
            <div v-else class="team-chart-empty">Pas encore d'historique mensuel</div>

            <!-- Assignments table -->
            <table class="data-table" style="font-size:12px; margin:0;">
              <thead>
                <tr>
                  <th>Phase / Tâche</th>
                  <th class="text-right" style="width:60px;">%</th>
                  <th style="width:130px;">Période</th>
                  <th style="width:120px;">Saisie</th>
                  <th style="width:150px;">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="a in member.assignments" :key="a.id" :class="{ 'assign-blocked': isPersonFullyBlocked(member.employee) || assignmentBlock(member.employee, a) }">
                  <td>{{ a.task ? (a.task_name || `Tâche #${a.task}`) : (a.phase ? (a.phase_name || `Phase #${a.phase}`) : 'Global') }}</td>
                  <td class="text-right"><span class="badge badge-blue" style="font-size:10px;">{{ a.hours_per_week }}h/sem</span></td>
                  <td class="text-muted" style="font-size:11px;">{{ a.start_date || '—' }} → {{ a.end_date || '...' }}</td>
                  <td>
                    <span v-if="isPersonFullyBlocked(member.employee)" class="text-muted" style="font-size:10px;" title="Personne bloquée sur tout le projet">🔒 Projet</span>
                    <template v-else-if="canEditBudget">
                      <button v-if="assignmentBlock(member.employee, a)" class="btn-action danger" style="font-size:10px;" title="Saisie bloquée pour cette personne — cliquer pour débloquer" @click="toggleAssignmentBlock(member.employee, a)">🔒 Bloqué</button>
                      <button v-else class="btn-action" style="font-size:10px;" title="Bloquer la saisie de temps de cette personne sur ce nœud" @click="toggleAssignmentBlock(member.employee, a)">🔓 Bloquer</button>
                    </template>
                    <span v-else class="text-muted" style="font-size:10px;">—</span>
                  </td>
                  <td>
                    <button class="btn-action" style="font-size:10px;" @click="activeTab = 'gantt'">Planifier</button>
                    <template v-if="confirmDeleteAssignment === a.id">
                      <button class="btn-action danger" style="font-size:10px;" @click="deleteAssignment(a.id)">OK</button>
                      <button class="btn-action" style="font-size:10px;" @click="confirmDeleteAssignment = null">×</button>
                    </template>
                    <button v-else class="btn-action danger" style="font-size:10px;" @click="confirmDeleteAssignment = a.id">Retirer</button>
                  </td>
                </tr>
              </tbody>
            </table>
            <div style="padding:8px 12px; border-top:1px solid var(--color-gray-100); display:flex; gap:8px;">
              <button class="btn-action" @click="activeTab = 'gantt'">&#128197; Planifier (Gantt — au niveau des tâches)</button>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="card empty-card">Aucune affectation — utilisez "Affecter" dans l'onglet Phases</div>
    </template>

    <!-- ═══ Temps (E-24) ═══ -->
    <template v-if="activeTab === 'time'">
      <div class="tab-header">
        <h3>Feuilles de temps du projet</h3>
        <div class="flex items-center gap-3">
          <div class="time-view-toggle">
            <button class="time-view-btn" :class="{ active: timeViewMode === 'employee' }" @click="timeViewMode = 'employee'; expandedTimeMonths.clear()">Par employe</button>
            <button class="time-view-btn" :class="{ active: timeViewMode === 'phase' }" @click="timeViewMode = 'phase'; expandedTimeMonths.clear()">Par phase</button>
          </div>
          <span class="text-sm font-mono font-semibold">Total: {{ projectTotalHours.toFixed(1) }}h</span>
        </div>
      </div>
      <div v-if="timeLoading" class="empty">Chargement...</div>
      <div v-else-if="!projectTimeEntries.length" class="empty">Aucune entree de temps pour ce projet</div>

      <!-- Pivot table: rows = employees/phases, columns = months (expandable to days) -->
      <div v-else class="card-table" style="overflow-x:auto;">
        <table class="data-table time-pivot" style="min-width:600px;">
          <thead>
            <tr>
              <th class="time-pivot-label" style="min-width:180px; position:sticky; left:0; background:var(--color-gray-50); z-index:2;">
                {{ timeViewMode === 'employee' ? 'Employe' : 'Phase' }}
              </th>
              <template v-for="month in timeMonths" :key="month">
                <!-- Month column (always visible) -->
                <th class="text-right time-pivot-month" @click="toggleTimeMonth(month)" style="cursor:pointer; user-select:none; min-width:70px;">
                  <span class="time-pivot-month-toggle">{{ expandedTimeMonths.has(month) ? '&#9660;' : '&#9654;' }}</span>
                  {{ month.substring(5) }}/{{ month.substring(2, 4) }}
                </th>
                <!-- Day columns (only if month expanded) -->
                <template v-if="expandedTimeMonths.has(month)">
                  <th v-for="day in (timeDaysByMonth.get(month) || [])" :key="month + '-' + day" class="text-right time-pivot-day" style="min-width:40px;">
                    {{ day }}
                  </th>
                </template>
              </template>
              <th class="text-right time-pivot-total" style="min-width:70px; position:sticky; right:0; background:var(--color-gray-50); z-index:2;">Total</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in timePivotRows" :key="row.key">
              <td class="font-semibold time-pivot-label-cell" style="position:sticky; left:0; background:white; z-index:1; max-width:180px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;" :title="row.label">
                {{ row.label }}
              </td>
              <template v-for="month in timeMonths" :key="month">
                <!-- Month total cell -->
                <td class="text-right font-mono time-pivot-month-cell" :class="{ 'has-hours': (row.hoursByMonth[month] || 0) > 0 }">
                  {{ (row.hoursByMonth[month] || 0) > 0 ? (row.hoursByMonth[month] || 0).toFixed(1) : '' }}
                </td>
                <!-- Day cells (only if month expanded) -->
                <template v-if="expandedTimeMonths.has(month)">
                  <td v-for="day in (timeDaysByMonth.get(month) || [])" :key="month + '-' + day" class="text-right font-mono time-pivot-day-cell" :class="{ 'has-hours': (row.hoursByDay[month + '-' + day] || 0) > 0 }">
                    {{ (row.hoursByDay[month + '-' + day] || 0) > 0 ? (row.hoursByDay[month + '-' + day] || 0).toFixed(1) : '' }}
                  </td>
                </template>
              </template>
              <td class="text-right font-mono font-semibold time-pivot-total-cell" style="position:sticky; right:0; background:white; z-index:1;">
                {{ row.totalHours.toFixed(1) }}
              </td>
            </tr>
          </tbody>
          <tfoot>
            <tr class="time-pivot-footer">
              <td class="font-semibold" style="position:sticky; left:0; background:var(--color-gray-100); z-index:2;">Total</td>
              <template v-for="month in timeMonths" :key="'t-' + month">
                <td class="text-right font-mono font-semibold">{{ (monthTotals[month] || 0).toFixed(1) }}</td>
                <template v-if="expandedTimeMonths.has(month)">
                  <td v-for="day in (timeDaysByMonth.get(month) || [])" :key="'t-' + month + '-' + day" class="text-right font-mono" style="font-size:10px;">
                    {{ (dayTotals[month + '-' + day] || 0) > 0 ? (dayTotals[month + '-' + day] || 0).toFixed(1) : '' }}
                  </td>
                </template>
              </template>
              <td class="text-right font-mono font-semibold" style="position:sticky; right:0; background:var(--color-gray-100); z-index:2;">{{ projectTotalHours.toFixed(1) }}</td>
            </tr>
          </tfoot>
        </table>
      </div>

      <div class="time-total" style="margin-top:8px;">
        <span class="text-muted" style="font-size:11px;">{{ projectTimeEntries.length }} entrees &middot; {{ timePivotRows.length }} {{ timeViewMode === 'employee' ? 'employes' : 'phases' }} &middot; {{ timeMonths.length }} mois &middot; Cliquer sur un mois pour voir les jours</span>
      </div>
    </template>

    <!-- ═══ Amendments ═══ -->
    <template v-if="activeTab === 'amendments'">
      <div v-if="isEditing" class="section-actions">
        <button class="btn-primary" @click="openAmendmentSlideOver(null)">+ Nouvel avenant</button>
      </div>

      <div class="card-table" v-if="amendments.length">
        <table>
          <thead>
            <tr>
              <th>Avenant</th>
              <th>Description</th>
              <th class="text-right">Impact ($)</th>
              <th>Statut</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="am in amendments"
              :key="am.id"
              class="amendment-row-clickable"
              @click="openAmendmentSlideOver(am.id)"
            >
              <td><span class="badge badge-purple" style="font-size:11px;font-weight:700;">AV-{{ am.amendment_number }}</span></td>
              <td>{{ am.description }}</td>
              <td class="text-right font-mono">{{ fmt.currency(am.budget_impact) }}</td>
              <td><span class="badge" :class="am.status === 'APPROVED' ? 'badge-green' : am.status === 'SUBMITTED' ? 'badge-amber' : am.status === 'REJECTED' ? 'badge-red' : 'badge-gray'">{{ amendmentStatusLabels[am.status] || am.status }}</span></td>
              <td class="text-muted">{{ am.created_at?.substring(0, 10) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="card empty-card">Aucun avenant</div>

      <AmendmentSlideOver
        :open="slideOverOpen"
        :project-id="projectId"
        :amendment-id="slideOverAmendmentId"
        :can-approve="canApproveAmendment"
        :phases="store.currentProject?.phases || []"
        @close="onAmendmentSlideOverClose"
        @saved="onAmendmentSaved"
      />
    </template>

    <!-- ═══ Budget ═══ -->
    <template v-if="activeTab === 'budget'">
      <!-- Honoraires du projet -->
      <div v-if="canEditBudget" class="card" style="margin-bottom: 16px;">
        <h3 class="card-title-edit">Honoraires du projet</h3>
        <div class="edit-grid" style="grid-template-columns: repeat(3, 1fr);">
          <div class="form-group">
            <label>Honoraires totaux HT ($)</label>
            <input
              v-model="honorairesForm.total_fees"
              type="text"
              inputmode="decimal"
              class="inline-input"
              :disabled="!canEditBudget"
              placeholder="0.00"
            />
          </div>
          <div class="form-group">
            <label>Méthode de calcul</label>
            <select v-model="honorairesForm.fee_calculation_method" class="inline-select" :disabled="!canEditBudget" style="width:100%;padding:6px 8px;">
              <option value="FORFAIT">Forfait</option>
              <option value="COUT_TRAVAUX">Coût des travaux %</option>
              <option value="HORAIRE">Horaire</option>
            </select>
          </div>
          <div class="form-group" v-if="honorairesForm.fee_calculation_method === 'COUT_TRAVAUX'">
            <label>Taux (%)</label>
            <input
              v-model="honorairesForm.fee_rate_pct"
              type="text"
              inputmode="decimal"
              class="inline-input"
              :disabled="!canEditBudget"
              placeholder="0.00"
            />
          </div>
        </div>
        <div v-if="honorairesForm.fee_calculation_method === 'COUT_TRAVAUX'" class="text-xs text-text-muted" style="margin-top:6px;">
          Coût de construction: {{ formatAmount(parseAmount(honorairesForm.construction_cost)) }} $ &times; {{ honorairesForm.fee_rate_pct || 0 }}% = <strong>{{ formatAmount(computedFees || 0) }} $</strong>
          <span style="margin-left:6px;">(coût de construction modifiable sur la <strong>Vue d'ensemble</strong>)</span>
        </div>
        <div v-if="canEditBudget" class="form-actions" style="margin-top:8px;">
          <button class="btn-primary btn-sm" :disabled="honorairesSaving" @click="saveHonoraires">
            {{ honorairesSaving ? 'Sauvegarde...' : 'Enregistrer les honoraires' }}
          </button>
        </div>
      </div>

      <!-- Contrat original / courant / avenants approuvés -->
      <div v-if="budgetSummary" class="card" style="margin-bottom: 16px;">
        <h3 class="card-title-edit">Valeur du contrat</h3>
        <div class="kpi-grid-3">
          <div class="kpi-card">
            <div class="kpi-value mono">{{ formatAmount(parseFloat(budgetSummary.original_contract_value) || 0) }}&nbsp;$</div>
            <div class="kpi-label">Contrat original</div>
          </div>
          <div class="kpi-card">
            <div class="kpi-value mono">{{ formatAmount(parseFloat(budgetSummary.current_contract_value) || 0) }}&nbsp;$</div>
            <div class="kpi-label">Contrat courant</div>
          </div>
          <div class="kpi-card">
            <div
              class="kpi-value mono"
              :class="{ success: parseFloat(budgetSummary.total_approved_impact) > 0, danger: parseFloat(budgetSummary.total_approved_impact) < 0 }"
            >
              {{ parseFloat(budgetSummary.total_approved_impact) >= 0 ? '+' : '' }}{{ formatAmount(parseFloat(budgetSummary.total_approved_impact) || 0) }}&nbsp;$
            </div>
            <div class="kpi-label">Impact avenants approuvés</div>
          </div>
        </div>
        <div v-if="budgetSummary.amendments.length" style="margin-top: 12px;">
          <table class="budget-table">
            <thead>
              <tr>
                <th>Avenant</th>
                <th>Description</th>
                <th>Date approbation</th>
                <th class="text-right">Impact ($)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="amd in budgetSummary.amendments" :key="amd.id">
                <td class="font-mono">AV-{{ amd.amendment_number }}</td>
                <td>{{ amd.description }}</td>
                <td>{{ amd.approval_date ? new Date(amd.approval_date).toLocaleDateString('fr-CA') : '—' }}</td>
                <td class="text-right mono" :class="{ success: parseFloat(amd.budget_impact) > 0, danger: parseFloat(amd.budget_impact) < 0 }">
                  {{ parseFloat(amd.budget_impact) >= 0 ? '+' : '' }}{{ formatAmount(parseFloat(amd.budget_impact) || 0) }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else class="text-xs text-text-muted" style="margin-top: 8px;">
          Aucun avenant approuvé pour ce projet.
        </div>
      </div>

      <!-- Header with create invoice button -->
      <div v-if="canEditBudget" class="budget-header">
        <div>
          <span v-if="!store.currentProject?.client" class="text-muted" style="font-size:11px;color:var(--color-danger);">Client requis pour créer une facture</span>
          <span v-else-if="taskBudgetTotal <= 0" class="text-muted" style="font-size:11px;color:var(--color-danger);">Budget requis pour créer une facture (ajoutez des tâches avec un budget)</span>
        </div>
        <button class="btn-primary" :disabled="creatingInvoice || taskBudgetTotal <= 0 || !store.currentProject?.client" @click="createInvoiceFromProject">
          {{ creatingInvoice ? 'Création...' : 'Créer une facture' }}
        </button>
      </div>

      <!-- Summary cards -->
      <div class="kpi-grid-4">
        <div class="kpi-card">
          <div class="kpi-value mono">{{ formatAmount(taskBudgetTotal) }}&nbsp;$</div>
          <div class="kpi-label">Budget total</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-value mono">{{ formatAmount(budgetInvoiced) }}&nbsp;$</div>
          <div class="kpi-label">Facturé à ce jour</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-value" :class="{ success: budgetConsumedPercent < 75, warning: budgetConsumedPercent >= 75 && budgetConsumedPercent < 90, danger: budgetConsumedPercent >= 90 }">{{ budgetConsumedPercent }}&nbsp;%</div>
          <div class="kpi-label">% consommé</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-value mono" :class="{ danger: (taskBudgetTotal - budgetInvoiced) < 0 }">{{ formatAmount(taskBudgetTotal - budgetInvoiced) }}&nbsp;$</div>
          <div class="kpi-label">Solde restant</div>
        </div>
      </div>

      <div v-if="budgetError" class="alert-error">{{ budgetError }}</div>

      <!-- Task budget table grouped by phase (lecture seule) -->
      <p class="phase-form-hint" style="margin:0 0 6px;">
        Vue de synthèse en <strong>lecture seule</strong> — le budget ($ et heures) se définit sur chaque tâche dans
        <button class="btn-link-inline" @click="activeTab = 'tasks'">Échéancier › Tâches &rarr;</button>
        (ou via la fiche tâche).
      </p>
      <div class="card-table">
        <table class="budget-table">
          <thead>
            <tr>
              <th>WBS</th>
              <th>Tâche</th>
              <th>Mode</th>
              <th class="text-right">Budget ($)</th>
              <th class="text-right">Heures</th>
              <th class="text-right">Facturé ($)</th>
              <th class="text-right">Solde ($)</th>
            </tr>
          </thead>
          <tbody v-if="tasksByPhase.length">
            <template v-for="group in tasksByPhase" :key="group.phase_name">
              <tr class="budget-phase-row">
                <td colspan="7" class="font-semibold">{{ group.phase_name }}</td>
              </tr>
              <tr v-for="task in group.tasks" :key="task.id">
                <td class="font-mono text-muted">{{ task.wbs_code || '—' }}</td>
                <td>
                  <span v-if="task.task_type === 'SUBTASK'" class="subtask-indent"></span>
                  {{ task.display_label || task.name }}
                </td>
                <td><span class="badge" :class="task.billing_mode === 'HORAIRE' ? 'badge-amber' : 'badge-blue'">{{ task.billing_mode }}</span></td>
                <!-- Budget en lecture seule : une seule porte d'entrée, la tâche
                     (Échéancier › Tâches ou fiche tâche). Évite la double saisie. -->
                <td class="text-right"><span class="font-mono">{{ formatAmount(task.budgeted_cost) }}</span></td>
                <td class="text-right"><span class="font-mono">{{ task.budgeted_hours }}</span></td>
                <td class="text-right font-mono">{{ formatAmount(0) }}</td>
                <td class="text-right font-mono">{{ formatAmount(task.budgeted_cost) }}</td>
              </tr>
            </template>
          </tbody>
          <tbody v-else>
            <tr><td colspan="7" class="empty">Aucune tâche — ajoutez des tâches dans l'onglet Tâches</td></tr>
          </tbody>
          <tfoot v-if="tasks.length">
            <tr class="budget-total-row">
              <td class="font-semibold" colspan="3">Total</td>
              <td class="text-right font-mono font-semibold">{{ formatAmount(taskBudgetTotal) }}</td>
              <td class="text-right font-mono font-semibold">{{ taskHoursTotal }}</td>
              <td class="text-right font-mono font-semibold">{{ formatAmount(budgetInvoiced) }}</td>
              <td class="text-right font-mono font-semibold">{{ formatAmount(taskBudgetTotal - budgetInvoiced) }}</td>
            </tr>
          </tfoot>
        </table>
      </div>

      <p class="budget-hint">Les lignes de facturation référenceront le budget de chaque tâche (défini dans Échéancier › Tâches).</p>
    </template>

    <!-- ═══ Gantt (US-PL06) ═══ -->
    <template v-if="activeTab === 'gantt'">
      <div class="section-actions" style="display:flex; justify-content:flex-end; margin-bottom: 12px;">
        <button class="btn-primary" data-add-milestone-gantt @click="openCreateMilestone">
          + Jalon
        </button>
      </div>
      <GanttChart :key="ganttRefresh" :project-id="projectId" />

      <!-- Milestone creation modal (inline) -->
      <div v-if="showMilestoneForm" class="modal-overlay" @click.self="showMilestoneForm = false">
        <div class="modal-panel" role="dialog" aria-modal="true">
          <header class="modal-header">
            <h3 class="modal-title">Nouveau jalon</h3>
            <button class="modal-close" aria-label="Fermer" @click="showMilestoneForm = false">×</button>
          </header>
          <div class="modal-body">
            <div class="milestone-grid">
              <div class="form-group">
                <label>Nom *</label>
                <input v-model="milestoneForm.name" data-milestone-name placeholder="ex. Livraison concept" />
              </div>
              <div class="form-group">
                <label>Date *</label>
                <input v-model="milestoneForm.date" type="date" data-milestone-date />
              </div>
              <div class="form-group">
                <label>Couleur</label>
                <input v-model="milestoneForm.color" type="color" style="height: 36px; width: 100%;" />
              </div>
              <div class="form-group" style="grid-column: 1 / -1;">
                <label>Description (optionnelle)</label>
                <textarea v-model="milestoneForm.description" rows="2" placeholder="Notes complémentaires…" />
              </div>
            </div>
            <div v-if="milestoneError" class="form-error">{{ milestoneError }}</div>
          </div>
          <footer class="modal-footer">
            <button class="btn-ghost" :disabled="creatingMilestone" @click="showMilestoneForm = false">Annuler</button>
            <button class="btn-primary" data-create-milestone :disabled="creatingMilestone" @click="createMilestone">
              {{ creatingMilestone ? 'Création…' : 'Créer le jalon' }}
            </button>
          </footer>
        </div>
      </div>
    </template>

    <!-- ===== SOUS-TRAITANTS TAB ===== -->
    <template v-if="activeTab === 'st'">
      <div class="tab-header">
        <h3>Factures sous-traitants</h3>
        <button class="btn-primary btn-sm" @click="router.push('/st-invoices')">+ Nouvelle facture ST</button>
      </div>
      <div v-if="stLoading" class="empty">Chargement...</div>
      <div v-else-if="!stInvoices.length" class="empty">Aucune facture sous-traitant pour ce projet</div>
      <table v-else class="data-table">
        <thead>
          <tr>
            <th>Fournisseur</th>
            <th>No facture</th>
            <th>Date</th>
            <th class="text-right">Montant</th>
            <th class="text-right">Refacturable</th>
            <th>Statut</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="st in stInvoices" :key="st.id">
            <td class="font-semibold">{{ st.supplier_name }}</td>
            <td class="font-mono">{{ st.invoice_number }}</td>
            <td class="text-muted">{{ st.invoice_date }}</td>
            <td class="text-right font-mono">{{ formatAmount(Number(st.amount)) }}</td>
            <td class="text-right font-mono">{{ formatAmount(Number(st.budget_refacturable)) }}</td>
            <td><span class="badge" :class="stStatusColors[st.status] || 'badge-gray'">{{ stStatusLabels[st.status] || st.status }}</span></td>
          </tr>
        </tbody>
        <tfoot>
          <tr>
            <td colspan="3" class="font-semibold">Total</td>
            <td class="text-right font-mono font-semibold">{{ formatAmount(stInvoices.reduce((s, i) => s + Number(i.amount), 0)) }}</td>
            <td class="text-right font-mono font-semibold">{{ formatAmount(stInvoices.reduce((s, i) => s + Number(i.budget_refacturable), 0)) }}</td>
            <td></td>
          </tr>
        </tfoot>
      </table>
    </template>

    <!-- ===== FACTURATION TAB ===== -->
    <template v-if="activeTab === 'invoices'">
      <div class="tab-header">
        <h3>Factures du projet</h3>
        <div v-if="canEditBudget" style="display:flex;align-items:center;gap:8px;">
          <span v-if="!store.currentProject?.client" class="text-muted" style="font-size:11px;color:var(--color-danger);">Client requis</span>
          <span v-else-if="taskBudgetTotal <= 0" class="text-muted" style="font-size:11px;color:var(--color-danger);">Budget requis</span>
          <button class="btn-primary btn-sm" :disabled="creatingInvoice || taskBudgetTotal <= 0 || !store.currentProject?.client" @click="createInvoiceFromProject">+ Créer une facture</button>
        </div>
      </div>
      <div v-if="invoicesLoading" class="empty">Chargement...</div>
      <div v-else-if="!projectInvoices.length" class="empty">Aucune facture pour ce projet</div>
      <table v-else class="data-table">
        <thead>
          <tr>
            <th>No facture</th>
            <th>Statut</th>
            <th class="text-right">Montant</th>
            <th>Date creation</th>
            <th>Date envoi</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="inv in projectInvoices" :key="inv.id">
            <td class="font-mono font-semibold">{{ inv.invoice_number }}</td>
            <td><span class="badge" :class="invStatusColors[inv.status] || 'badge-gray'">{{ invStatusLabels[inv.status] || inv.status }}</span></td>
            <td class="text-right font-mono">{{ formatAmount(Number(inv.total_amount)) }}</td>
            <td class="text-muted">{{ inv.date_created }}</td>
            <td class="text-muted">{{ inv.date_sent || '—' }}</td>
            <td><button class="btn-sm-link" @click="router.push(`/billing/${inv.id}`)">Voir</button></td>
          </tr>
        </tbody>
        <tfoot>
          <tr>
            <td colspan="2" class="font-semibold">Total</td>
            <td class="text-right font-mono font-semibold">{{ formatAmount(projectInvoices.reduce((s, i) => s + Number(i.total_amount), 0)) }}</td>
            <td colspan="3"></td>
          </tr>
        </tfoot>
      </table>
    </template>

    <!-- ═══ Modal clôture projet (F3.8) ═══ -->
    <ProjectCloseModal
      :open="showCloseModal"
      :can-close="canClose"
      :checks="closureChecks"
      :loading="closeLoading"
      :error-message="closeError"
      @close="showCloseModal = false"
      @confirm="confirmClose"
    />

    <!-- ═══ Modal édition tâche (F3.7 — WBS / libellé client / budgets) ═══ -->
    <TaskSlideOver
      :open="sheetTaskId !== null"
      :project-id="Number(projectId)"
      :task-id="sheetTaskId"
      @close="sheetTaskId = null"
      @updated="onTaskSheetUpdated"
    />
    <AssignResourceDialog
      :open="assignDialogOpen"
      :project-id="Number(projectId)"
      :initial-scope="assignDialogScope"
      @close="assignDialogOpen = false"
      @assigned="onAssigned"
    />
    <TaskEditModal
      :open="showTaskEditModal"
      :task="taskBeingEdited"
      :can-see-costs="canEditBudget"
      :loading="taskEditLoading"
      :error-message="taskEditError"
      @close="showTaskEditModal = false; taskBeingEdited = null"
      @save="saveTaskEdit"
    />

  </div>
</template>

<style scoped>
.page-header { display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 16px; }
.page-header h1 { font-size: 20px; font-weight: 700; color: var(--color-gray-900); margin-top: 2px; }
.code { font-family: var(--font-mono); color: var(--color-gray-400); font-weight: 400; }
.btn-back { background: none; border: none; font-size: 12px; color: var(--color-gray-500); cursor: pointer; padding: 0; }
.header-actions { display: flex; align-items: center; gap: 8px; position: relative; }
.btn-danger { padding: 4px 10px; border-radius: 4px; font-size: 11px; font-weight: 600; cursor: pointer; border: none; background: var(--color-danger); color: white; }
.btn-link { background: none; border: none; font-size: 11px; color: var(--color-primary); font-weight: 600; cursor: pointer; padding: 2px 6px; }
.btn-link:hover { text-decoration: underline; }

.badge { display: inline-flex; padding: 2px 10px; border-radius: 10px; font-size: 10px; font-weight: 600; cursor: pointer; border: none; background: var(--color-gray-100); }
.badge-internal { display: inline-flex; padding: 2px 10px; border-radius: 10px; font-size: 10px; font-weight: 700; background: #EDE9FE; color: #7C3AED; }
.badge-green { background: #DCFCE7; color: #15803D; } .badge-amber { background: #FEF3C7; color: #92400E; }
.badge-gray { background: var(--color-gray-100); color: var(--color-gray-500); } .badge-red { background: #FEE2E2; color: #DC2626; }
.badge-blue { background: #DBEAFE; color: #1D4ED8; }

.status-dropdown { position: absolute; top: 100%; right: 0; z-index: 50; margin-top: 4px; background: white; border-radius: 6px; box-shadow: 0 4px 12px rgba(0,0,0,0.12); padding: 4px; min-width: 140px; }
.status-option { display: block; width: 100%; padding: 6px 8px; border: none; background: none; cursor: pointer; text-align: left; border-radius: 4px; }
.status-option:hover { background: var(--color-gray-50); }
.status-option.active { background: var(--color-primary-light); }
.actions-trigger { font-size: 18px; padding: 2px 10px; line-height: 1; }
.actions-menu { position: absolute; top: 100%; right: 0; z-index: 50; margin-top: 4px; background: white; border: 1px solid var(--color-border); border-radius: 6px; box-shadow: 0 4px 12px rgba(0,0,0,0.12); padding: 4px; min-width: 160px; }
.actions-menu-item { display: block; width: 100%; padding: 6px 10px; border: none; background: none; cursor: pointer; text-align: left; border-radius: 4px; font-size: 12px; color: var(--color-text); }
.actions-menu-item:hover { background: var(--color-gray-50); }
.actions-menu-item.danger { color: var(--color-danger); }
.actions-menu-item.danger:hover { background: var(--color-danger-light); }
.actions-menu-separator { height: 1px; background: var(--color-border); margin: 4px 0; }

.alert-error { background: var(--color-danger-light); color: var(--color-danger); padding: 8px 12px; border-radius: 6px; font-size: 12px; margin-bottom: 12px; }
.alert-danger-banner { background: #FEE2E2; color: #DC2626; padding: 12px 16px; border-radius: 6px; font-size: 13px; font-weight: 600; margin-bottom: 12px; }
.banner-actions { display: flex; gap: 8px; margin-top: 8px; }


.kpi-grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 16px; }
.kpi-grid-7 { display: grid; grid-template-columns: repeat(7, minmax(0, 1fr)); gap: 10px; margin-bottom: 16px; }
.alert-lines { display: flex; flex-direction: column; gap: 6px; margin-top: 6px; }
.alert-line { font-size: 12px; color: var(--color-gray-700); }
@media (max-width: 1100px) { .kpi-grid-7 { grid-template-columns: repeat(4, minmax(0, 1fr)); } }
.kpi-card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 14px; text-align: center; }
.kpi-value { font-size: 24px; font-weight: 700; color: var(--color-gray-900); }
.kpi-value.mono { font-family: var(--font-mono); font-size: 20px; }
.kpi-value.success { color: var(--color-success); } .kpi-value.warning { color: var(--color-warning); } .kpi-value.danger { color: var(--color-danger); }
.kpi-label { font-size: 10px; color: var(--color-gray-500); text-transform: uppercase; font-weight: 600; }

.info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.info-card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 16px; }
.info-card h3 { font-size: 11px; font-weight: 600; color: var(--color-gray-400); text-transform: uppercase; margin-bottom: 12px; }
.info-pairs { display: grid; grid-template-columns: 1fr 1fr; gap: 12px 24px; font-size: 13px; }
.info-pairs.single { grid-template-columns: 1fr; }
.info-pairs > div { min-width: 0; overflow: hidden; }
.info-pairs span { display: block; color: var(--color-gray-500); font-size: 11px; margin-bottom: 2px; }
.info-pairs p { font-weight: 600; margin: 0; word-wrap: break-word; }

.card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 16px; margin-bottom: 12px; }
.card-table { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); overflow: hidden; }
.amendment-row-clickable { cursor: pointer; transition: background 0.12s; }
.amendment-row-clickable:hover { background: var(--color-gray-50); }
.empty { text-align: center; padding: 24px; color: var(--color-gray-400); } .empty-card { text-align: center; color: var(--color-gray-400); font-size: 13px; padding: 24px; }
.empty-phase-row td { background: var(--color-gray-50); }
.phase-form-hint { font-size: 12px; color: var(--color-gray-600); margin: 0 0 10px; }
.agg-mark { font-size: 9px; color: var(--color-gray-400); font-weight: 600; }
.agg-cell { color: var(--color-gray-700); background: var(--color-gray-50); }
.phase-empty-row td { opacity: 0.62; }
.tasks-toolbar { display: flex; align-items: center; gap: 6px; margin-bottom: 10px; }
.shift-band { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 8px; padding: 8px 12px; margin-bottom: 10px; font-size: 12px; }
.date-inline { padding: 2px 4px; font-size: 11px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-family: inherit; color: var(--color-gray-700); max-width: 108px; }
.date-inline:disabled { border-color: transparent; background: transparent; }
.date-derived { font-size: 11px; color: var(--color-gray-400); font-style: italic; }
.empty-phase-cell { padding: 12px 16px; text-align: center; color: var(--color-gray-500); font-size: 12px; font-style: italic; }
.empty-card .link { color: var(--color-primary); text-decoration: underline; cursor: pointer; }

.text-right { text-align: right !important; } .text-muted { color: var(--color-gray-500); font-size: 12px; }
.font-mono { font-family: var(--font-mono); font-size: 12px; } .font-semibold { font-weight: 600; }
.actions-cell { white-space: nowrap; }
.btn-action { background: none; border: none; font-size: 11px; cursor: pointer; color: var(--color-primary); padding: 2px 6px; font-weight: 600; }
.task-name-link { cursor: pointer; }
.task-name-link:hover { color: var(--color-primary); text-decoration: underline; }
.btn-action:hover { text-decoration: underline; } .btn-action.danger { color: var(--color-danger); }

.section-actions { margin-bottom: 12px; }
.form-row-3 { display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 10px; }
.form-group label { display: block; font-size: 11px; font-weight: 600; color: var(--color-gray-600); margin-bottom: 4px; }

.wbs-node { border: 1px solid var(--color-gray-200); border-radius: 6px; padding: 10px 14px; margin-bottom: 8px; }
.wbs-row { display: flex; align-items: center; justify-content: space-between; }
.wbs-children { margin-left: 24px; margin-top: 8px; }
.wbs-child { display: flex; align-items: center; justify-content: space-between; padding: 6px 10px; background: var(--color-gray-50); border-radius: 4px; margin-bottom: 4px; font-size: 13px; }

.progress-row { display: flex; align-items: center; gap: 12px; margin-bottom: 16px; }
.progress-bar { flex: 1; height: 10px; background: var(--color-gray-200); border-radius: 5px; overflow: hidden; }
.progress-fill { height: 100%; border-radius: 5px; } .progress-fill.green { background: var(--color-success); } .progress-fill.amber { background: var(--color-warning); } .progress-fill.red { background: var(--color-danger); }
.budget-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; font-size: 13px; }
.budget-grid span { color: var(--color-gray-500); font-size: 11px; } .budget-grid p { margin-top: 2px; }

.card-title-edit { font-size: 14px; font-weight: 600; color: var(--color-gray-800); margin-bottom: 12px; }
.edit-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
.inline-input { width: 100%; padding: 4px 8px; border: 1px solid var(--color-primary); border-radius: 3px; font-size: 12px; }
.inline-input-sm { width: 70px; padding: 4px 6px; border: 1px solid var(--color-primary); border-radius: 3px; font-size: 12px; text-align: right; font-family: var(--font-mono); }
.inline-select { padding: 4px 6px; border: 1px solid var(--color-primary); border-radius: 3px; font-size: 11px; }
.wbs-edit-form { width: 100%; }
.wbs-edit-row { display: flex; gap: 8px; align-items: flex-end; flex-wrap: wrap; }
.wbs-edit-field { display: flex; flex-direction: column; }
.wbs-edit-field label { font-size: 10px; font-weight: 600; color: var(--color-gray-500); margin-bottom: 2px; }
.wbs-info { display: flex; align-items: center; gap: 6px; }

/* Budget tab */
.kpi-grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 16px; }
.kpi-grid-6 { display: grid; grid-template-columns: repeat(6, 1fr); gap: 12px; margin-bottom: 16px; }
@media (max-width: 1200px) { .kpi-grid-6 { grid-template-columns: repeat(3, 1fr); } }

.budget-table { width: 100%; }
.budget-table th, .budget-table td { padding: 8px 12px; border-bottom: 1px solid var(--color-gray-200); font-size: 12px; }
.budget-table thead th { font-size: 10px; font-weight: 600; color: var(--color-gray-500); text-transform: uppercase; background: var(--color-gray-50); }
.budget-table tbody td { font-size: 13px; }
.budget-table tfoot td { border-top: 2px solid var(--color-gray-300); border-bottom: none; background: var(--color-gray-50); }

.budget-total-row td { padding: 10px 12px; }

.budget-input {
  width: 110px;
  padding: 4px 8px;
  border: 1px solid var(--color-gray-300);
  border-radius: 3px;
  font-size: 12px;
  font-family: var(--font-mono);
  text-align: right;
  background: white;
  transition: border-color 0.15s;
  -moz-appearance: textfield;
}
.budget-input::-webkit-outer-spin-button,
.budget-input::-webkit-inner-spin-button { -webkit-appearance: none; margin: 0; }
.budget-input:focus { outline: none; border-color: var(--color-primary); box-shadow: 0 0 0 2px rgba(59,130,246,0.15); }
.budget-input.saving { opacity: 0.5; pointer-events: none; }

.budget-hint { font-size: 11px; color: var(--color-gray-400); margin-top: 12px; font-style: italic; }

/* Tab header */
.tab-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
.tab-header h3 { font-size: 15px; font-weight: 600; color: var(--color-gray-800); }
.btn-sm { padding: 5px 12px; font-size: 12px; }

/* Data table */
.data-table { width: 100%; border-collapse: collapse; font-size: 13px; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.data-table thead th { padding: 8px 12px; font-size: 11px; font-weight: 600; text-transform: uppercase; color: var(--color-gray-500); background: var(--color-gray-50); border-bottom: 2px solid var(--color-gray-200); text-align: left; white-space: nowrap; }
.data-table tbody td { padding: 8px 12px; border-bottom: 1px solid var(--color-gray-100); text-align: left; vertical-align: middle; }
.data-table tbody tr:hover { background: var(--color-gray-50); }
.data-table tfoot td { padding: 8px 12px; background: var(--color-gray-50); border-top: 2px solid var(--color-gray-200); }
.font-semibold { font-weight: 600; }
.btn-sm-link { background: none; border: none; color: var(--color-primary); font-size: 12px; font-weight: 600; cursor: pointer; padding: 2px 6px; }
.btn-sm-link:hover { text-decoration: underline; }
.badge-green-solid { background: #15803D; color: white; }

.budget-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }

/* Tasks tab */
.task-phase-group { margin-bottom: 12px; }
.task-phase-header {
  display: flex; align-items: center; gap: 6px; padding: 8px 12px;
  background: var(--color-gray-50); border-radius: 6px 6px 0 0; cursor: pointer;
  font-size: 13px; border: 1px solid var(--color-gray-200); border-bottom: none;
  user-select: none;
}
.task-phase-toggle { font-size: 10px; color: var(--color-gray-400); width: 14px; }
.task-table { font-size: 12px; border-radius: 0 0 8px 8px; }
.task-table-fixed { table-layout: fixed; }
.task-table thead th { font-size: 10px; padding: 6px 10px; }
.task-table tbody td { padding: 5px 10px; font-size: 12px; }
.subtask-row { background: var(--color-gray-50); }
.subtask-indent { display: inline-block; width: 18px; }
.task-type-badge { font-size: 9px; padding: 1px 5px; }
.task-add-row {
  display: flex; gap: 6px; align-items: center; padding: 6px 12px;
  background: white; border: 1px solid var(--color-gray-200); border-bottom: none;
}
.task-add-row .inline-input { flex: 1; }
.subtask-add-row td { background: var(--color-gray-50); padding: 4px 10px !important; }

/* Budget phase group row */
.budget-phase-row td {
  background: var(--color-gray-50); font-size: 11px; text-transform: uppercase;
  color: var(--color-gray-600); padding: 6px 12px; border-bottom: 1px solid var(--color-gray-200);
}

.form-actions { display: flex; gap: 6px; justify-content: flex-end; }
.form-row-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
/* Phase/Task alerts */
.phase-alert { padding: 10px 16px; border-radius: 6px; font-size: 12px; margin-bottom: 10px; display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }
.alert-orange { background: #FEF3C7; color: #92400E; border-left: 4px solid #D97706; }
.alert-amber { background: #FEF9C3; color: #854D0E; border-left: 4px solid #EAB308; }
.alert-red { background: #FEE2E2; color: #991B1B; border-left: 4px solid #DC2626; }
.btn-link-inline { background: none; border: none; color: inherit; font-weight: 700; cursor: pointer; text-decoration: underline; font-size: 12px; padding: 0; }

/* Team budget banner */
.team-budget-banner { display: flex; align-items: center; gap: 10px; padding: 10px 16px; border-radius: 8px; font-size: 13px; font-weight: 600; margin-bottom: 16px; }
.banner-green { background: #DCFCE7; color: #166534; border-left: 4px solid #16A34A; }
.banner-orange { background: #FEF3C7; color: #92400E; border-left: 4px solid #D97706; }
.banner-red { background: #FEE2E2; color: #991B1B; border-left: 4px solid #DC2626; }

/* Team tab — accordion */
.team-list { display: flex; flex-direction: column; gap: 8px; }
.team-member-card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); overflow: hidden; }
.team-member-header { display: flex; align-items: center; justify-content: space-between; padding: 12px 16px; cursor: pointer; transition: background 0.1s; }
.team-member-header:hover { background: var(--color-gray-50); }
.team-member-left { display: flex; align-items: center; gap: 10px; flex: 0 1 200px; min-width: 0; }
.team-toggle { font-size: 10px; color: var(--color-gray-400); width: 14px; }
.team-avatar { width: 32px; height: 32px; border-radius: 50%; background: var(--color-primary); color: white; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; flex-shrink: 0; }
.team-name { font-size: 13px; font-weight: 600; color: var(--color-gray-800); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 140px; }
.team-name.name-blocked { text-decoration: line-through; color: var(--color-gray-400); }
.assign-blocked { opacity: 0.5; }
.assign-blocked td:first-child { text-decoration: line-through; }
.team-sub { font-size: 11px; color: var(--color-gray-500); }
.team-member-right { display: flex; gap: 20px; flex: 1; justify-content: flex-end; }
.team-hours { text-align: right; }
.team-hours-label { display: block; font-size: 9px; color: var(--color-gray-400); text-transform: uppercase; letter-spacing: 0.3px; }
.team-hours-value { font-size: 14px; font-weight: 600; font-family: var(--font-mono); color: var(--color-gray-800); }
.team-member-detail { border-top: 1px solid var(--color-gray-200); }
.avatar-noplanning { background: #D97706 !important; }
.team-no-planning { color: #D97706; font-weight: 600; font-size: 10px; margin-left: 6px; }

/* Team monthly chart */
.team-chart { padding: 12px 16px; background: var(--color-gray-50); }
.team-chart-title { font-size: 10px; font-weight: 600; color: var(--color-gray-500); text-transform: uppercase; letter-spacing: 0.3px; margin-bottom: 8px; }
.team-chart-bars { display: flex; gap: 6px; align-items: flex-end; height: 80px; }
.team-chart-bar { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 3px; height: 100%; justify-content: flex-end; }
.team-chart-fill { width: 100%; border-radius: 3px 3px 0 0; background: var(--color-primary); min-height: 3px; }
.team-chart-val { font-size: 9px; font-weight: 600; font-family: var(--font-mono); color: var(--color-gray-700); }
.team-chart-label { font-size: 9px; color: var(--color-gray-500); }
.team-chart-empty { padding: 12px 16px; font-size: 11px; color: var(--color-gray-400); font-style: italic; background: var(--color-gray-50); }

/* Time tab — pivot table */
.time-view-toggle { display: flex; border: 1px solid var(--color-gray-200); border-radius: 6px; overflow: hidden; }
.time-view-btn { padding: 4px 12px; font-size: 11px; font-weight: 600; background: white; border: none; cursor: pointer; color: var(--color-gray-500); transition: all 0.1s; }
.time-view-btn.active { background: var(--color-primary); color: white; }
/* ── Onglet Équipe : vue « Par phase » (accordéons + recherche) ── */
.team-toolbar { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; flex-wrap: wrap; }
.team-view-toggle { display: flex; border: 1px solid var(--color-gray-200); border-radius: 6px; overflow: hidden; }
.team-search { flex: 1; min-width: 220px; padding: 6px 10px; border: 1px solid var(--color-gray-300); border-radius: 6px; font-size: 12px; }
.team-expand-actions { display: flex; gap: 4px; }
.phase-tree { display: flex; flex-direction: column; gap: 6px; }
.phase-acc { background: white; border: 1px solid var(--color-gray-200); border-radius: 8px; overflow: hidden; }
.phase-acc-head { display: flex; align-items: center; gap: 8px; padding: 8px 12px; background: var(--color-gray-50); cursor: pointer; }
.phase-acc-head:hover { background: var(--color-gray-100); }
.acc-caret { font-size: 9px; color: var(--color-gray-500); width: 12px; flex-shrink: 0; }
.acc-dot { color: var(--color-gray-300); width: 12px; flex-shrink: 0; text-align: center; }
.phase-acc-name { font-weight: 700; font-size: 13px; color: var(--color-gray-800); }
.acc-count { font-size: 10px; color: var(--color-gray-400); }
.phase-acc-body { padding: 4px 0; }
.phase-team-assign { display: inline-flex; align-items: center; gap: 4px; margin-left: 6px; flex-shrink: 0; }
.node-close { display: inline-flex; align-items: center; gap: 4px; margin-left: 8px; flex-shrink: 0; }
.tpn { padding: 0 12px; }
.tpn-head { display: flex; align-items: center; gap: 8px; padding: 5px 0; border-bottom: 1px solid var(--color-gray-100); }
.tpn-sub .tpn-head { padding-left: 18px; }
.tpn-children { background: #FCFCFD; }
.tpn-wbs { font-family: var(--font-mono, monospace); font-size: 10px; color: var(--color-gray-400); flex-shrink: 0; }
.tpn-name { font-size: 12px; color: var(--color-gray-800); }
.tpn-sub .tpn-name { font-size: 11px; color: var(--color-gray-600); }
.tpn-closed { text-decoration: line-through; color: var(--color-gray-400); }
.tpn-badge { font-size: 9px; }
.tpn-noone { font-size: 10px; color: var(--color-gray-300); font-style: italic; }
.people-chips { display: flex; flex-wrap: wrap; gap: 4px; margin-left: auto; }
.person-chip { font-size: 10px; background: #EFF6FF; color: var(--color-primary); border-radius: 10px; padding: 1px 8px; white-space: nowrap; }
.person-chip--virtual { background: #F3E8FF; color: #7C3AED; border: 1px dashed #C4B5FD; }
.time-pivot { border-collapse: collapse; font-size: 11px; }
.time-pivot th { padding: 6px 8px; font-size: 10px; white-space: nowrap; }
.time-pivot td { padding: 5px 8px; }
.time-pivot-month { background: var(--color-gray-50); }
.time-pivot-month-toggle { font-size: 8px; margin-right: 3px; color: var(--color-gray-400); }
.time-pivot-day { background: var(--color-primary-light, #EFF6FF); font-size: 9px; color: var(--color-gray-500); }
.time-pivot-month-cell { font-size: 11px; }
.time-pivot-month-cell.has-hours { color: var(--color-primary); font-weight: 600; }
.time-pivot-day-cell { font-size: 10px; }
.time-pivot-day-cell.has-hours { background: var(--color-primary-light, #EFF6FF); color: var(--color-gray-800); }
.time-pivot-total { background: var(--color-gray-100); }
.time-pivot-total-cell { background: var(--color-gray-50); }
.time-pivot-footer td { background: var(--color-gray-100); border-top: 2px solid var(--color-gray-300); }
.time-pivot-label-cell { font-size: 12px; }
.time-total { display: flex; align-items: center; gap: 16px; padding: 8px 16px; }

/* Virtual resources panel (Équipe) */
.virtuals-panel { background: var(--color-gray-50); border: 1px solid var(--color-gray-200); border-radius: 6px; padding: 12px; margin-bottom: 16px; }
.virtuals-header { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }
.virtuals-title { font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.4px; color: var(--color-gray-700); }
.virtuals-count { background: var(--color-primary-light); color: var(--color-primary); font-size: 11px; font-weight: 600; padding: 1px 6px; border-radius: 10px; }
.virtuals-count-muted { background: var(--color-gray-200); color: var(--color-gray-600); }
.virtuals-hint { font-size: 11px; color: var(--color-gray-500); margin: 0 0 10px; }
.virtuals-empty { font-size: 12px; color: var(--color-gray-500); font-style: italic; padding: 10px 6px; line-height: 1.5; }
.virtuals-empty-hint { font-size: 11px; color: var(--color-gray-400); }
.virtuals-history-sep { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.4px; color: var(--color-gray-500); margin: 12px 0 6px; padding-top: 8px; border-top: 1px dashed var(--color-gray-200); }
.virtual-row-replaced { opacity: 0.75; background: var(--color-gray-50); }
.virtual-avatar-muted { background: var(--color-gray-400); }
.virtual-name-muted { color: var(--color-gray-600); text-decoration: line-through; text-decoration-color: var(--color-gray-400); }
.virtual-row { display: flex; align-items: center; gap: 10px; padding: 8px 10px; background: white; border: 1px solid var(--color-gray-200); border-radius: 4px; margin-bottom: 6px; flex-wrap: wrap; }
.virtual-info { display: flex; align-items: center; gap: 10px; flex: 1; min-width: 200px; }
.virtual-avatar { width: 28px; height: 28px; border-radius: 50%; background: var(--color-gray-300); color: white; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 700; }
.virtual-name { font-size: 13px; font-weight: 600; color: var(--color-gray-800); }
.virtual-sub { font-size: 11px; color: var(--color-gray-500); font-family: var(--font-mono); }
.virtual-replace-form { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }
.virtual-actions { display: flex; align-items: center; gap: 6px; margin-left: auto; flex-wrap: wrap; }
.virtual-replace-form .select-sm { padding: 4px 8px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 12px; min-width: 180px; }
.virtual-error { flex-basis: 100%; font-size: 11px; color: var(--color-danger); }

/* Milestone modal (Gantt tab) */
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.45); display: flex; align-items: center; justify-content: center; z-index: 1000; padding: 16px; }
.modal-panel { background: white; border-radius: 8px; max-width: 520px; width: 100%; max-height: 90vh; display: flex; flex-direction: column; box-shadow: 0 10px 40px rgba(0,0,0,0.2); }
.modal-header { display: flex; justify-content: space-between; padding: 14px 18px; border-bottom: 1px solid var(--color-gray-200); }
.modal-title { font-size: 16px; font-weight: 700; color: var(--color-gray-800); margin: 0; }
.modal-close { background: none; border: none; font-size: 22px; color: var(--color-gray-500); cursor: pointer; line-height: 1; }
.modal-body { padding: 18px; overflow-y: auto; }
.milestone-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; }
.milestone-grid .form-group { display: flex; flex-direction: column; gap: 4px; }
.milestone-grid .form-group label { font-size: 11px; font-weight: 600; color: var(--color-gray-600); text-transform: uppercase; letter-spacing: 0.3px; }
.milestone-grid .form-group input, .milestone-grid .form-group textarea { padding: 6px 10px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 13px; }
.form-error { margin-top: 12px; padding: 8px 12px; background: #FEE2E2; color: #B91C1C; border-radius: 4px; font-size: 12px; }
.modal-footer { display: flex; justify-content: flex-end; gap: 8px; padding: 12px 18px; border-top: 1px solid var(--color-gray-200); background: var(--color-gray-50); border-radius: 0 0 8px 8px; }
</style>
