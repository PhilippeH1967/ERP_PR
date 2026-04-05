<script setup lang="ts">
import { onMounted, ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useLocale } from '@/shared/composables/useLocale'
import { useAuth } from '@/shared/composables/useAuth'
import apiClient from '@/plugins/axios'
import { projectApi } from '../api/projectApi'
import { billingApi } from '@/features/billing/api/billingApi'
import { useProjectStore } from '../stores/useProjectStore'
import AssignmentModal from '../components/AssignmentModal.vue'

const route = useRoute()
const router = useRouter()
const store = useProjectStore()
const { fmt } = useLocale()
const { currentUser } = useAuth()
const projectId = Number(route.params.id)
const activeTab = ref('overview')
const actionError = ref('')
const isEditing = ref(false)
const showEditStatus = ref(false)
const showDeleteConfirm = ref(false)
const confirmDeletePhase = ref<number | null>(null)
const confirmDeleteWBS = ref<number | null>(null)
const confirmDeleteAssignment = ref<number | null>(null)
const confirmDeleteAmendment = ref<number | null>(null)

interface DashboardData { hours_consumed: string; budget_hours: string; budget_utilization_percent: number; health: 'green' | 'yellow' | 'red' }
interface WBSNode { id: number; standard_label: string; client_facing_label: string; element_type: string; budgeted_hours: string; children: WBSNode[] }
interface Assignment { id: number; employee: number; employee_name: string; phase: number | null; phase_name: string; percentage: string; start_date: string | null; end_date: string | null }
interface Amendment { id: number; amendment_number: number; description: string; status: string; budget_impact: string; created_at: string }

const dashboard = ref<DashboardData | null>(null)
const wbsTree = ref<WBSNode[]>([])
const assignments = ref<Assignment[]>([])
const amendments = ref<Amendment[]>([])
const showAssignModal = ref(false)
const assignPhaseId = ref<number | null>(null)
const assignPhaseName = ref('')

// WBS create/edit
const showWBSForm = ref(false)
const wbsForm = ref({ standard_label: '', client_facing_label: '', element_type: 'PHASE', budgeted_hours: '0', phase: null as number | null })
const editingWBSId = ref<number | null>(null)
const editingWBSForm = ref({ standard_label: '', client_facing_label: '', budgeted_hours: '', element_type: 'TASK' })

// Amendment edit
const editingAmendmentId = ref<number | null>(null)
const editAmendmentForm = ref({ description: '', budget_impact: '', status: 'DRAFT' })

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

// ST tab
interface STInvoiceItem { id: number; supplier_name: string; invoice_number: string; invoice_date: string; amount: string; status: string; budget_refacturable: string }
const stInvoices = ref<STInvoiceItem[]>([])
const stLoading = ref(false)

async function loadSTInvoices() {
  if (!project.value) return
  stLoading.value = true
  try {
    const resp = await apiClient.get('st_invoices/', { params: { project: project.value.id } })
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
  if (!project.value) return
  invoicesLoading.value = true
  try {
    const resp = await apiClient.get('invoices/', { params: { project: project.value.id } })
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

const canEditBudget = computed(() => {
  const roles = currentUser.value?.roles || []
  return roles.includes('ADMIN') || roles.includes('FINANCE')
})

const budgetTotal = computed(() => {
  const phases = store.currentProject?.phases || []
  return phases.reduce((sum: number, p: { budgeted_cost: string | number }) => sum + Number(p.budgeted_cost || 0), 0)
})

const budgetInvoiced = computed(() => 0) // placeholder — will come from invoices

const budgetConsumedPercent = computed(() => {
  const total = taskBudgetTotal?.value ?? budgetTotal.value
  if (total <= 0) return 0
  return Math.round((budgetInvoiced.value / total) * 100 * 10) / 10
})

const budgetRemaining = computed(() => (taskBudgetTotal?.value ?? budgetTotal.value) - budgetInvoiced.value)

function formatAmount(value: number | string): string {
  const n = Number(value)
  if (isNaN(n)) return '0,00'
  return n.toLocaleString('fr-CA', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

async function saveBudget(phaseId: number, newValue: string) {
  budgetError.value = ''
  const parsed = parseFloat(newValue.replace(/\s/g, '').replace(',', '.'))
  if (isNaN(parsed) || parsed < 0) { budgetError.value = 'Montant invalide'; return }
  budgetSaving.value = phaseId
  try {
    await projectApi.updatePhase(projectId, phaseId, { budgeted_cost: parsed } as Record<string, unknown>)
    await reload()
  } catch (e: unknown) {
    budgetError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur de sauvegarde'
  } finally {
    budgetSaving.value = null
  }
}

// Business Units + Users for dropdowns
const businessUnits = ref<Array<{ id: number; name: string }>>([])
const allUsers = ref<Array<{ id: number; username: string; email: string }>>([])

// Add phase form
const showAddPhaseForm = ref(false)
const newPhase = ref({ name: '', client_facing_label: '', billing_mode: 'FORFAIT', budgeted_hours: '0', phase_type: 'REALIZATION' })

// Inline edit project
const editingProject = ref(false)
const projectForm = ref({ name: '', start_date: '', end_date: '', business_unit: '', pm: '', associate_in_charge: '' })

function startEditProject() {
  if (!isEditing.value) return
  const p = store.currentProject
  if (!p) return
  projectForm.value = {
    name: p.name || '',
    start_date: p.start_date || '',
    end_date: p.end_date || '',
    business_unit: p.business_unit || '',
    pm: String(p.pm || ''),
    associate_in_charge: String(p.associate_in_charge || ''),
  }
  editingProject.value = true
}

function stopEditing() {
  isEditing.value = false
  editingProject.value = false
  editingPhaseId.value = null
  editingWBSId.value = null
  showWBSForm.value = false
  showDeleteConfirm.value = false
  confirmDeletePhase.value = null
  confirmDeleteWBS.value = null
  confirmDeleteAssignment.value = null
  confirmDeleteAmendment.value = null
}

async function addPhase() {
  actionError.value = ''
  if (!newPhase.value.name.trim()) { actionError.value = 'Le nom de la phase est obligatoire.'; return }
  try {
    await projectApi.createPhase(projectId, newPhase.value as Record<string, unknown>)
    showAddPhaseForm.value = false
    newPhase.value = { name: '', client_facing_label: '', billing_mode: 'FORFAIT', budgeted_hours: '0', phase_type: 'REALIZATION' }
    await reload()
  } catch (e: unknown) {
    actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur'
  }
}

async function saveProject() {
  actionError.value = ''
  if (projectForm.value.start_date && projectForm.value.end_date && projectForm.value.end_date < projectForm.value.start_date) {
    actionError.value = 'La date de fin ne peut pas être antérieure à la date de début.'
    return
  }
  try {
    const payload: Record<string, unknown> = {
      name: projectForm.value.name,
      business_unit: projectForm.value.business_unit || '',
      start_date: projectForm.value.start_date || null,
      end_date: projectForm.value.end_date || null,
    }
    if (projectForm.value.pm) payload.pm = Number(projectForm.value.pm)
    else payload.pm = null
    if (projectForm.value.associate_in_charge) payload.associate_in_charge = Number(projectForm.value.associate_in_charge)
    else payload.associate_in_charge = null
    await projectApi.update(projectId, payload)
    editingProject.value = false
    await reload()
  } catch (e: unknown) {
    const err = e as { response?: { data?: { error?: { message?: string; details?: Array<{ field?: string; message?: string }> } } } }
    actionError.value = err.response?.data?.error?.details?.[0]?.message || err.response?.data?.error?.message || 'Erreur'
  }
}

// Inline edit phase
const editingPhaseId = ref<number | null>(null)
const phaseForm = ref({ name: '', client_facing_label: '', billing_mode: '', budgeted_hours: '' })

function startEditPhase(phase: { id: number; name: string; client_facing_label?: string; billing_mode: string; budgeted_hours: string }) {
  editingPhaseId.value = phase.id
  phaseForm.value = {
    name: phase.name,
    client_facing_label: phase.client_facing_label || '',
    billing_mode: phase.billing_mode,
    budgeted_hours: phase.budgeted_hours,
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

// WBS create
async function createWBSElement() {
  actionError.value = ''
  try {
    await projectApi.createWBSElement(projectId, {
      standard_label: wbsForm.value.standard_label,
      client_facing_label: wbsForm.value.client_facing_label,
      element_type: wbsForm.value.element_type,
      budgeted_hours: wbsForm.value.budgeted_hours,
      phase: wbsForm.value.phase,
    } as Record<string, unknown>)
    showWBSForm.value = false
    wbsForm.value = { standard_label: '', client_facing_label: '', element_type: 'PHASE', budgeted_hours: '0', phase: null }
    await reload()
  } catch (e: unknown) { actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur' }
}

function startEditWBS(node: WBSNode) {
  editingWBSId.value = node.id
  editingWBSForm.value = {
    standard_label: node.standard_label,
    client_facing_label: node.client_facing_label,
    budgeted_hours: node.budgeted_hours,
    element_type: node.element_type,
  }
}

async function saveWBS() {
  if (!editingWBSId.value) return
  actionError.value = ''
  try {
    await projectApi.updateWBSElement(projectId, editingWBSId.value, editingWBSForm.value as Record<string, unknown>)
    editingWBSId.value = null
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
}
const tasks = ref<TaskItem[]>([])
const collapsedPhases = ref<Set<string>>(new Set())
const confirmDeleteTask = ref<number | null>(null)
const showAddTaskPhase = ref<number | null>(null)
const newTaskName = ref('')

const tasksByPhase = computed(() => {
  const grouped: Record<string, { phase_name: string; phase_id: number | null; tasks: TaskItem[] }> = {}
  for (const t of tasks.value) {
    const key = t.phase_name || 'Sans phase'
    if (!grouped[key]) grouped[key] = { phase_name: key, phase_id: t.phase, tasks: [] }
    grouped[key].tasks.push(t)
  }
  // Sort tasks by order within each group
  for (const g of Object.values(grouped)) {
    g.tasks.sort((a, b) => a.order - b.order)
  }
  return Object.values(grouped)
})

const taskBudgetTotal = computed(() => tasks.value.reduce((sum, t) => sum + Number(t.budgeted_cost || 0), 0))
const taskHoursTotal = computed(() => tasks.value.reduce((sum, t) => sum + Number(t.budgeted_hours || 0), 0))

async function loadTasks() {
  try {
    const r = await projectApi.listTasks(projectId)
    const d = r.data?.data || r.data
    tasks.value = Array.isArray(d) ? d : d?.results || []
  } catch { tasks.value = [] }
}

async function saveTaskField(taskId: number, field: string, value: unknown) {
  try {
    await projectApi.updateTask(projectId, taskId, { [field]: value })
    await loadTasks()
  } catch (e: unknown) {
    actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur de sauvegarde'
  }
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
    await loadTasks()
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
  try { await projectApi.deleteTask(projectId, taskId) } catch { /* ok */ }
}

function togglePhaseCollapse(phaseName: string) {
  if (collapsedPhases.value.has(phaseName)) collapsedPhases.value.delete(phaseName)
  else collapsedPhases.value.add(phaseName)
}

// Amendment form
const showAmendmentForm = ref(false)
const amendmentForm = ref({ description: '', budget_impact: '0', status: 'DRAFT' })

// Honoraires form state
const honorairesForm = ref({
  total_fees: '',
  fee_calculation_method: 'FORFAIT',
  fee_rate_pct: '',
})
const honorairesSaving = ref(false)

function initHonoraires() {
  const p = store.currentProject
  if (!p) return
  honorairesForm.value = {
    total_fees: p.total_fees ?? '',
    fee_calculation_method: p.fee_calculation_method || 'FORFAIT',
    fee_rate_pct: p.fee_rate_pct ?? '',
  }
}

const computedFees = computed(() => {
  if (honorairesForm.value.fee_calculation_method !== 'COUT_TRAVAUX') return null
  const cost = Number(store.currentProject?.construction_cost || 0)
  const rate = Number(honorairesForm.value.fee_rate_pct || 0)
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
    await projectApi.update(projectId, payload)
    await reload()
    initHonoraires()
  } catch (e: unknown) {
    budgetError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur de sauvegarde'
  } finally {
    honorairesSaving.value = false
  }
}

// Progress tab helpers
function progressColor(pct: number): string {
  if (pct <= 10) return 'progress-green'
  if (pct <= 25) return 'progress-amber'
  return 'progress-red'
}

async function saveProgressPct(taskId: number, value: string) {
  const parsed = parseFloat(value)
  if (isNaN(parsed) || parsed < 0 || parsed > 100) return
  await saveTaskField(taskId, 'progress_pct', parsed)
}

// Finance tab data (placeholder)
const financeData = ref([
  { year: new Date().getFullYear(), ca: 0, costs: 0, margin: 0, margin_pct: 0 },
])

// Time entries for Temps tab
interface ProjectTimeEntry { id: number; user_name: string; date: string; hours: string; task_name: string; phase_name: string; status: string }
const projectTimeEntries = ref<ProjectTimeEntry[]>([])
const timeLoading = ref(false)

async function loadProjectTime() {
  if (!store.currentProject) return
  timeLoading.value = true
  try {
    const resp = await apiClient.get('time_entries/', { params: { project: store.currentProject.id } })
    const data = resp.data?.data || resp.data
    projectTimeEntries.value = Array.isArray(data) ? data : data?.results || []
  } catch { projectTimeEntries.value = [] }
  finally { timeLoading.value = false }
}

const projectTotalHours = computed(() => projectTimeEntries.value.reduce((s, e) => s + Number(e.hours || 0), 0))

const tabs = [
  { key: 'overview', label: 'Vue d\'ensemble' },
  { key: 'phases', label: 'Phases' },
  { key: 'tasks', label: 'Tâches' },
  { key: 'team', label: 'Équipe' },
  { key: 'time', label: 'Temps' },
  { key: 'amendments', label: 'Avenants' },
  { key: 'budget', label: 'Budget' },
  { key: 'progress', label: 'Avancement' },
  { key: 'finance', label: 'Finance' },
  { key: 'st', label: 'Sous-traitants' },
  { key: 'invoices', label: 'Facturation' },
]

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
  try { const r = await projectApi.listWBS(projectId); wbsTree.value = r.data?.data || r.data || [] } catch { wbsTree.value = [] }
  try { const r = await projectApi.listAssignments(projectId); assignments.value = r.data?.data || r.data || [] } catch { assignments.value = [] }
  try { const r = await projectApi.listAmendments(projectId); amendments.value = r.data?.data || r.data || [] } catch { amendments.value = [] }
  await loadClientData()
  await loadTasks()
}

async function changeStatus(newStatus: string) {
  actionError.value = ''
  try {
    await projectApi.update(projectId, { status: newStatus } as Record<string, unknown>)
    showEditStatus.value = false
    await reload()
  } catch (e: unknown) { actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur' }
}

async function deleteProject() {
  showDeleteConfirm.value = false
  try {
    await projectApi.delete(projectId)
  } catch { /* ok */ }
  router.push('/projects')
}

function openAssignModal(phaseId: number | null, phaseName: string) {
  assignPhaseId.value = phaseId; assignPhaseName.value = phaseName; showAssignModal.value = true
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
  try { await projectApi.deleteAssignment(projectId, assignId) } catch { /* ok */ }
}

async function deleteWBS(wbsId: number) {
  confirmDeleteWBS.value = null
  wbsTree.value = wbsTree.value.filter(w => w.id !== wbsId)
  try { await projectApi.deleteWBSElement(projectId, wbsId) } catch { /* ok */ }
}

async function createAmendment() {
  actionError.value = ''
  try {
    await projectApi.createAmendment(projectId, amendmentForm.value)
    showAmendmentForm.value = false
    amendmentForm.value = { description: '', budget_impact: '0', status: 'DRAFT' }
    await reload()
  } catch (e: unknown) { actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur' }
}

function startEditAmendment(am: Amendment) {
  editingAmendmentId.value = am.id
  editAmendmentForm.value = { description: am.description, budget_impact: am.budget_impact, status: am.status }
}

async function saveAmendment() {
  if (!editingAmendmentId.value) return
  try {
    await projectApi.updateAmendment(projectId, editingAmendmentId.value, editAmendmentForm.value)
    editingAmendmentId.value = null
    await reload()
  } catch (e: unknown) {
    actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur'
  }
}

async function deleteAmendment(id: number) {
  confirmDeleteAmendment.value = null
  amendments.value = amendments.value.filter(a => a.id !== id)
  try { await projectApi.deleteAmendment(projectId, id) } catch { /* ok */ }
}

onMounted(reload)

// Lazy load tab data
watch(activeTab, (tab) => {
  if (tab === 'tasks' && !tasks.value.length) loadTasks()
  if (tab === 'progress' && !tasks.value.length) loadTasks()
  if (tab === 'budget') initHonoraires()
  if (tab === 'time') loadProjectTime()
  if (tab === 'st') loadSTInvoices()
  if (tab === 'invoices') loadProjectInvoices()
})
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
        <span v-if="store.currentProject.is_consortium" class="badge badge-blue" style="cursor:default;">Consortium</span>
        <!-- Status badge (clickable only in edit mode) -->
        <div class="relative">
          <button class="badge" :class="statusColors[store.currentProject.status]" @click="isEditing && (showEditStatus = !showEditStatus)" :style="isEditing ? 'cursor:pointer' : 'cursor:default'">
            {{ statuses.find(s => s.value === store.currentProject?.status)?.label || store.currentProject.status }} <span v-if="isEditing">&#x25BE;</span>
          </button>
          <div v-if="showEditStatus && isEditing" class="status-dropdown">
            <button v-for="s in availableStatuses" :key="s.value" class="status-option" @click="changeStatus(s.value)">
              <span class="badge" :class="s.color">{{ s.label }}</span>
            </button>
            <div v-if="!availableStatuses.length" class="status-option" style="color:var(--color-gray-400);font-size:11px;cursor:default;">Aucune transition possible</div>
          </div>
        </div>
        <button v-if="!isEditing && canEdit" class="btn-primary" @click="isEditing = true">Modifier</button>
        <button v-if="isEditing" class="btn-ghost" @click="stopEditing">Terminer</button>
        <button v-if="isEditing" class="btn-danger btn-sm" @click="showDeleteConfirm = true">Supprimer...</button>
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

    <!-- Tabs -->
    <div class="tabs">
      <button v-for="tab in tabs" :key="tab.key" class="tab" :class="{ active: activeTab === tab.key }" @click="activeTab = tab.key">
        {{ tab.label }}
        <span v-if="tab.key === 'amendments' && amendments.length" class="tab-count">{{ amendments.length }}</span>
      </button>
    </div>

    <!-- ═══ Overview ═══ -->
    <template v-if="activeTab === 'overview'">
      <div v-if="dashboard" class="kpi-grid-3">
        <div class="kpi-card"><div class="kpi-value" :class="{ success: dashboard.health==='green', warning: dashboard.health==='yellow', danger: dashboard.health==='red' }">{{ dashboard.budget_utilization_percent }}%</div><div class="kpi-label">Utilisation</div></div>
        <div class="kpi-card"><div class="kpi-value mono">{{ fmt.hours(dashboard.hours_consumed) }}</div><div class="kpi-label">Heures</div></div>
        <div class="kpi-card"><div class="kpi-value mono">{{ fmt.hours(dashboard.budget_hours) }}</div><div class="kpi-label">Budget</div></div>
      </div>
      <!-- View mode -->
      <template v-if="!editingProject">
        <!-- KPIs financiers (E-26) -->
        <div class="kpi-grid-4" style="margin-bottom:12px;">
          <div class="kpi-card"><div class="kpi-value mono">{{ formatAmount(taskBudgetTotal) }}&nbsp;$</div><div class="kpi-label">Budget total</div></div>
          <div class="kpi-card"><div class="kpi-value mono">{{ formatAmount(budgetInvoiced) }}&nbsp;$</div><div class="kpi-label">Facturé</div></div>
          <div class="kpi-card"><div class="kpi-value" :class="{ success: budgetConsumedPercent < 75, warning: budgetConsumedPercent >= 75, danger: budgetConsumedPercent >= 90 }">{{ budgetConsumedPercent }}&nbsp;%</div><div class="kpi-label">Consommé</div></div>
          <div class="kpi-card"><div class="kpi-value mono" :class="{ danger: budgetRemaining < 0 }">{{ formatAmount(budgetRemaining) }}&nbsp;$</div><div class="kpi-label">Solde restant</div></div>
        </div>

        <div class="info-grid">
          <div class="info-card"><h3>Informations <button v-if="isEditing" class="btn-action" @click="startEditProject">Modifier</button></h3><div class="info-pairs"><div><span>Type de contrat</span><p>{{ store.currentProject.contract_type }}</p></div><div><span>Unité d'affaires</span><p>{{ store.currentProject.business_unit || '—' }}</p></div><div><span>Date début</span><p>{{ store.currentProject.start_date ? fmt.date(store.currentProject.start_date) : '—' }}</p></div><div><span>Date fin</span><p>{{ store.currentProject.end_date ? fmt.date(store.currentProject.end_date) : '—' }}</p></div><div><span>Public/Privé</span><p>{{ store.currentProject.is_public ? 'Public' : 'Privé' }}</p></div><div><span>Consortium</span><p>{{ store.currentProject.is_consortium ? 'Oui' : 'Non' }}</p></div></div></div>
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
        <!-- Phases summary table (E-27) -->
        <div v-if="store.currentProject.phases?.length" class="card-table" style="margin-top: 12px;">
          <table class="data-table">
            <thead><tr><th>Phase</th><th>Type</th><th>Mode</th><th class="text-right">Heures</th><th class="text-right">Budget ($)</th></tr></thead>
            <tbody>
              <tr v-for="phase in store.currentProject.phases" :key="phase.id">
                <td class="font-semibold">{{ phase.name }}</td>
                <td><span class="badge badge-gray">{{ phase.phase_type === 'SUPPORT' ? 'Support' : 'Réalisation' }}</span></td>
                <td><span class="badge" :class="phase.billing_mode === 'HORAIRE' ? 'badge-amber' : 'badge-blue'">{{ phase.billing_mode }}</span></td>
                <td class="text-right font-mono">{{ fmt.hours(phase.budgeted_hours) }}</td>
                <td class="text-right font-mono">{{ formatAmount(phase.budgeted_cost) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </template>
      <!-- Edit mode -->
      <template v-else>
      <div class="card">
        <h3 class="card-title-edit">Modifier le projet</h3>
        <div class="edit-grid">
          <div class="form-group"><label>Nom</label><input v-model="projectForm.name" /></div>
          <div class="form-group"><label>Unité d'affaires</label>
            <select v-model="projectForm.business_unit">
              <option value="">— Aucune —</option>
              <option v-for="bu in businessUnits" :key="bu.id" :value="bu.name">{{ bu.name }}</option>
            </select>
          </div>
          <div class="form-group"><label>Date début</label><input v-model="projectForm.start_date" type="date" /></div>
          <div class="form-group"><label>Date fin</label><input v-model="projectForm.end_date" type="date" /></div>
          <div class="form-group"><label>Chef de projet</label>
            <select v-model="projectForm.pm">
              <option value="">— Aucun —</option>
              <option v-for="u in allUsers" :key="u.id" :value="String(u.id)">{{ u.username }} ({{ u.email }})</option>
            </select>
          </div>
          <div class="form-group"><label>Associé en charge</label>
            <select v-model="projectForm.associate_in_charge">
              <option value="">— Aucun —</option>
              <option v-for="u in allUsers" :key="u.id" :value="String(u.id)">{{ u.username }} ({{ u.email }})</option>
            </select>
          </div>
        </div>
        <div class="form-actions"><button class="btn-ghost" @click="editingProject = false">Annuler</button><button class="btn-primary" @click="saveProject">Enregistrer</button></div>
      </div>
      </template>
    </template>

    <!-- ═══ Phases ═══ -->
    <template v-if="activeTab === 'phases'">
      <div v-if="isEditing" class="section-actions" style="margin-bottom:10px;">
        <button class="btn-primary" @click="showAddPhaseForm = !showAddPhaseForm">+ Ajouter une phase</button>
      </div>
      <div v-if="showAddPhaseForm && isEditing" class="card" style="margin-bottom:10px;">
        <div class="form-row-3">
          <div class="form-group"><label>Nom interne *</label><input v-model="newPhase.name" placeholder="Concept" /></div>
          <div class="form-group"><label>Libellé client</label><input v-model="newPhase.client_facing_label" placeholder="Phase 1 — Concept" /></div>
          <div class="form-group"><label>Mode</label>
            <select v-model="newPhase.billing_mode"><option value="FORFAIT">Forfait</option><option value="HORAIRE">Horaire</option></select>
          </div>
        </div>
        <div class="form-row-2">
          <div class="form-group"><label>Heures budgetées</label><input v-model="newPhase.budgeted_hours" type="number" /></div>
          <div class="form-group"><label>Type</label>
            <select v-model="newPhase.phase_type"><option value="REALIZATION">Réalisation</option><option value="SUPPORT">Support</option></select>
          </div>
        </div>
        <div class="form-actions"><button class="btn-ghost" @click="showAddPhaseForm = false">Annuler</button><button class="btn-primary" @click="addPhase">Ajouter</button></div>
      </div>
      <div class="card-table">
        <table>
          <thead><tr><th>Phase</th><th>Libellé client</th><th>Type</th><th>Mode</th><th class="text-right">Heures</th><th class="text-right">Actions</th></tr></thead>
          <tbody>
            <tr v-for="phase in store.currentProject.phases" :key="phase.id">
              <template v-if="editingPhaseId === phase.id">
                <td><input v-model="phaseForm.name" class="inline-input" /></td>
                <td><input v-model="phaseForm.client_facing_label" class="inline-input" /></td>
                <td><span class="badge badge-gray">{{ phase.phase_type }}</span></td>
                <td><select v-model="phaseForm.billing_mode" class="inline-select"><option value="FORFAIT">Forfait</option><option value="HORAIRE">Horaire</option></select></td>
                <td class="text-right"><input v-model="phaseForm.budgeted_hours" type="number" class="inline-input-sm" /></td>
                <td class="text-right actions-cell">
                  <button class="btn-action" @click="savePhase">OK</button>
                  <button class="btn-action" @click="editingPhaseId = null">×</button>
                </td>
              </template>
              <template v-else>
                <td class="font-semibold">{{ phase.name }}</td>
                <td class="text-muted">{{ phase.client_facing_label || '—' }}</td>
                <td><span class="badge badge-gray">{{ phase.phase_type }}</span></td>
                <td><span class="badge" :class="phase.billing_mode === 'HORAIRE' ? 'badge-amber' : 'badge-blue'">{{ phase.billing_mode }}</span></td>
                <td class="text-right font-mono">{{ fmt.hours(phase.budgeted_hours) }}</td>
                <td class="text-right actions-cell">
                  <template v-if="isEditing">
                    <button class="btn-action" @click="startEditPhase(phase)">Modifier</button>
                    <button class="btn-action" @click="openAssignModal(phase.id, phase.name)">Affecter</button>
                    <template v-if="phase.is_mandatory">
                      <span class="badge badge-amber" style="font-size:9px;cursor:default;">&#x1F512; Obligatoire</span>
                    </template>
                    <template v-else>
                      <template v-if="confirmDeletePhase === phase.id">
                        <button class="btn-action danger" @click="deletePhase(phase.id)">Confirmer</button>
                        <button class="btn-action" @click="confirmDeletePhase = null">Annuler</button>
                      </template>
                      <button v-else class="btn-action danger" @click="confirmDeletePhase = phase.id">Supprimer...</button>
                    </template>
                  </template>
                </td>
              </template>
            </tr>
            <tr v-if="!store.currentProject.phases?.length"><td colspan="6" class="empty">Aucune phase</td></tr>
          </tbody>
        </table>
      </div>
    </template>

    <!-- ═══ Tâches ═══ -->
    <template v-if="activeTab === 'tasks'">
      <div v-if="tasksByPhase.length">
        <div v-for="group in tasksByPhase" :key="group.phase_name" class="task-phase-group">
          <!-- Phase header -->
          <div class="task-phase-header" @click="togglePhaseCollapse(group.phase_name)">
            <span class="task-phase-toggle">{{ collapsedPhases.has(group.phase_name) ? '&#9654;' : '&#9660;' }}</span>
            <span class="font-semibold">{{ group.phase_name }}</span>
            <span class="text-muted" style="margin-left:8px;">({{ group.tasks.length }} tâche{{ group.tasks.length > 1 ? 's' : '' }})</span>
            <button v-if="isEditing" class="btn-action" style="margin-left:auto;" @click.stop="showAddTaskPhase = group.phase_id; newTaskName = ''">+ Tâche</button>
          </div>

          <!-- Add task form -->
          <div v-if="showAddTaskPhase === group.phase_id && isEditing" class="task-add-row">
            <input v-model="newTaskName" class="inline-input" placeholder="Nom de la tâche" @keydown.enter="addTask(group.phase_id)" />
            <button class="btn-primary btn-sm" @click="addTask(group.phase_id)">Ajouter</button>
            <button class="btn-ghost btn-sm" @click="showAddTaskPhase = null">Annuler</button>
          </div>

          <!-- Tasks table -->
          <table v-if="!collapsedPhases.has(group.phase_name)" class="data-table task-table task-table-fixed">
            <thead>
              <tr>
                <th style="width:60px;">WBS</th>
                <th>Nom</th>
                <th style="width:80px;">Mode</th>
                <th class="text-right" style="width:100px;">Budget ($)</th>
                <th class="text-right" style="width:80px;">Heures</th>
                <th style="width:90px;">Facturable</th>
                <th v-if="isEditing" style="width:120px;">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="task in group.tasks" :key="task.id" :class="{ 'subtask-row': task.task_type === 'SUBTASK' }">
                <td class="font-mono">{{ task.wbs_code || '—' }}</td>
                <td>
                  <span v-if="task.task_type === 'SUBTASK'" class="subtask-indent"></span>
                  <span class="badge task-type-badge" :class="task.task_type === 'SUBTASK' ? 'badge-gray' : 'badge-blue'" style="margin-right:4px;">{{ task.task_type === 'SUBTASK' ? 'ST' : 'T' }}</span>
                  {{ task.display_label || task.name }}
                </td>
                <td><span class="badge" :class="task.billing_mode === 'HORAIRE' ? 'badge-amber' : 'badge-blue'">{{ task.billing_mode }}</span></td>
                <td class="text-right">
                  <template v-if="canEditBudget">
                    <input
                      class="budget-input"
                      :value="task.budgeted_cost"
                      type="text"
                      inputmode="decimal"
                      @blur="(e: Event) => { const v = parseFloat(((e.target as HTMLInputElement).value || '0').replace(/\\s/g, '').replace(',', '.')); if (!isNaN(v)) saveTaskField(task.id, 'budgeted_cost', v) }"
                      @keydown.enter="(e: Event) => (e.target as HTMLInputElement).blur()"
                    />
                  </template>
                  <template v-else><span class="font-mono">{{ formatAmount(task.budgeted_cost) }}</span></template>
                </td>
                <td class="text-right">
                  <template v-if="canEditBudget">
                    <input
                      class="budget-input"
                      :value="task.budgeted_hours"
                      type="text"
                      inputmode="decimal"
                      @blur="(e: Event) => { const v = parseFloat(((e.target as HTMLInputElement).value || '0').replace(/\\s/g, '').replace(',', '.')); if (!isNaN(v)) saveTaskField(task.id, 'budgeted_hours', v) }"
                      @keydown.enter="(e: Event) => (e.target as HTMLInputElement).blur()"
                    />
                  </template>
                  <template v-else><span class="font-mono">{{ task.budgeted_hours }}</span></template>
                </td>
                <td>
                  <span v-if="task.is_billable" class="badge badge-green">Facturable</span>
                  <span v-else class="badge badge-gray">Non fact.</span>
                </td>
                <td v-if="isEditing" class="actions-cell">
                  <template v-if="confirmDeleteTask === task.id">
                    <button class="btn-action danger" @click="removeTask(task.id)">Confirmer</button>
                    <button class="btn-action" @click="confirmDeleteTask = null">Annuler</button>
                  </template>
                  <button v-else class="btn-action danger" @click="confirmDeleteTask = task.id">Supprimer...</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div v-else class="card empty-card">Aucune tâche — ajoutez des tâches via les phases</div>
    </template>

    <!-- ═══ Team ═══ -->
    <template v-if="activeTab === 'team'">
      <div class="card-table" v-if="assignments.length">
        <table>
          <thead><tr><th>Employé</th><th>Phase</th><th class="text-right">%</th><th>Période</th><th></th></tr></thead>
          <tbody>
            <tr v-for="a in assignments" :key="a.id">
              <td class="font-semibold">{{ a.employee_name || `Employé #${a.employee}` }}</td>
              <td class="text-muted">{{ a.phase ? (a.phase_name || `Phase #${a.phase}`) : 'Global' }}</td>
              <td class="text-right"><span class="badge badge-blue">{{ a.percentage }}%</span></td>
              <td class="text-muted">{{ a.start_date || '—' }} → {{ a.end_date || '...' }}</td>
              <td class="text-right">
                <template v-if="isEditing">
                  <template v-if="confirmDeleteAssignment === a.id">
                    <button class="btn-action danger" @click="deleteAssignment(a.id)">Confirmer</button>
                    <button class="btn-action" @click="confirmDeleteAssignment = null">Annuler</button>
                  </template>
                  <button v-else class="btn-action danger" @click="confirmDeleteAssignment = a.id">Retirer...</button>
                </template>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="card empty-card">Aucune affectation — utilisez "Affecter" dans l'onglet Phases</div>
    </template>

    <!-- ═══ Temps (E-24) ═══ -->
    <template v-if="activeTab === 'time'">
      <div class="tab-header">
        <h3>Feuilles de temps du projet</h3>
        <div class="flex items-center gap-3">
          <span class="text-sm font-mono font-semibold">Total: {{ projectTotalHours.toFixed(1) }}h</span>
        </div>
      </div>
      <div v-if="timeLoading" class="empty">Chargement...</div>
      <div v-else-if="!projectTimeEntries.length" class="empty">Aucune entrée de temps pour ce projet</div>
      <table v-else class="data-table">
        <thead>
          <tr>
            <th>Employé</th>
            <th>Date</th>
            <th>Phase</th>
            <th>Tâche</th>
            <th class="text-right">Heures</th>
            <th>Statut</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="entry in projectTimeEntries" :key="entry.id">
            <td class="font-semibold">{{ entry.user_name || '—' }}</td>
            <td class="text-muted">{{ entry.date }}</td>
            <td class="text-muted">{{ entry.phase_name || '—' }}</td>
            <td class="text-muted">{{ entry.task_name || '—' }}</td>
            <td class="text-right font-mono">{{ Number(entry.hours).toFixed(1) }}</td>
            <td>
              <span class="badge" :class="entry.status === 'APPROVED' ? 'badge-green' : entry.status === 'SUBMITTED' ? 'badge-amber' : 'badge-gray'">
                {{ entry.status === 'APPROVED' ? 'Approuvé' : entry.status === 'SUBMITTED' ? 'Soumis' : 'Brouillon' }}
              </span>
            </td>
          </tr>
        </tbody>
        <tfoot>
          <tr>
            <td colspan="4" class="font-semibold">Total</td>
            <td class="text-right font-mono font-semibold">{{ projectTotalHours.toFixed(1) }}</td>
            <td></td>
          </tr>
        </tfoot>
      </table>
    </template>

    <!-- ═══ Amendments ═══ -->
    <template v-if="activeTab === 'amendments'">
      <div v-if="isEditing" class="section-actions"><button class="btn-primary" @click="showAmendmentForm = !showAmendmentForm">+ Nouvel avenant</button></div>

      <div v-if="showAmendmentForm" class="card" style="margin-bottom: 12px;">
        <form @submit.prevent="createAmendment" class="form-row-3">
          <div class="form-group"><label>Description</label><input v-model="amendmentForm.description" type="text" required placeholder="Description de l'avenant" /></div>
          <div class="form-group"><label>Impact budget ($)</label><input v-model="amendmentForm.budget_impact" type="number" step="0.01" /></div>
          <div class="form-group"><label>Statut</label><select v-model="amendmentForm.status"><option value="DRAFT">Brouillon</option><option value="SUBMITTED">Soumis</option><option value="APPROVED">Approuvé</option></select>
            <div style="margin-top:6px;display:flex;gap:4px;justify-content:flex-end;"><button type="button" class="btn-ghost" @click="showAmendmentForm=false">Annuler</button><button type="submit" class="btn-primary">Créer</button></div>
          </div>
        </form>
      </div>

      <div class="card-table" v-if="amendments.length">
        <table>
          <thead><tr><th>No</th><th>Description</th><th class="text-right">Impact ($)</th><th>Statut</th><th>Date</th><th></th></tr></thead>
          <tbody>
            <tr v-for="am in amendments" :key="am.id">
              <template v-if="editingAmendmentId === am.id">
                <td class="font-mono font-semibold">#{{ am.amendment_number }}</td>
                <td><input v-model="editAmendmentForm.description" class="inline-input" /></td>
                <td><input v-model="editAmendmentForm.budget_impact" type="number" step="0.01" class="inline-input-sm" /></td>
                <td>
                  <select v-model="editAmendmentForm.status" class="inline-select">
                    <option value="DRAFT">Brouillon</option>
                    <option value="SUBMITTED">Soumis</option>
                    <option value="APPROVED">Approuvé</option>
                    <option value="REJECTED">Rejeté</option>
                  </select>
                </td>
                <td class="text-muted">{{ am.created_at?.substring(0, 10) }}</td>
                <td class="text-right">
                  <button class="btn-action" @click="saveAmendment">OK</button>
                  <button class="btn-action" @click="editingAmendmentId = null">×</button>
                </td>
              </template>
              <template v-else>
                <td class="font-mono font-semibold">#{{ am.amendment_number }}</td>
                <td>{{ am.description }}</td>
                <td class="text-right font-mono">{{ fmt.currency(am.budget_impact) }}</td>
                <td><span class="badge" :class="am.status === 'APPROVED' ? 'badge-green' : am.status === 'SUBMITTED' ? 'badge-amber' : am.status === 'REJECTED' ? 'badge-red' : 'badge-gray'">{{ amendmentStatusLabels[am.status] || am.status }}</span></td>
                <td class="text-muted">{{ am.created_at?.substring(0, 10) }}</td>
                <td class="text-right">
                  <template v-if="isEditing">
                    <button class="btn-action" @click="startEditAmendment(am)">Modifier</button>
                    <template v-if="confirmDeleteAmendment === am.id">
                      <button class="btn-action danger" @click="deleteAmendment(am.id)">Confirmer</button>
                      <button class="btn-action" @click="confirmDeleteAmendment = null">Annuler</button>
                    </template>
                    <button v-else class="btn-action danger" @click="confirmDeleteAmendment = am.id">Supprimer...</button>
                  </template>
                </td>
              </template>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else-if="!showAmendmentForm" class="card empty-card">Aucun avenant</div>
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
          Coût de construction: {{ formatAmount(store.currentProject?.construction_cost || 0) }} $ &times; {{ honorairesForm.fee_rate_pct || 0 }}% = <strong>{{ formatAmount(computedFees || 0) }} $</strong>
        </div>
        <div v-if="canEditBudget" class="form-actions" style="margin-top:8px;">
          <button class="btn-primary btn-sm" :disabled="honorairesSaving" @click="saveHonoraires">
            {{ honorairesSaving ? 'Sauvegarde...' : 'Enregistrer les honoraires' }}
          </button>
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

      <!-- Task budget table grouped by phase -->
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
                <td class="text-right">
                  <template v-if="canEditBudget">
                    <input
                      class="budget-input"
                      :value="task.budgeted_cost"
                      type="text"
                      inputmode="decimal"
                      @blur="(e: Event) => { const v = parseFloat(((e.target as HTMLInputElement).value || '0').replace(/\\s/g, '').replace(',', '.')); if (!isNaN(v)) saveTaskField(task.id, 'budgeted_cost', v) }"
                      @keydown.enter="(e: Event) => (e.target as HTMLInputElement).blur()"
                    />
                  </template>
                  <template v-else><span class="font-mono">{{ formatAmount(task.budgeted_cost) }}</span></template>
                </td>
                <td class="text-right">
                  <template v-if="canEditBudget">
                    <input
                      class="budget-input"
                      :value="task.budgeted_hours"
                      type="text"
                      inputmode="decimal"
                      @blur="(e: Event) => { const v = parseFloat(((e.target as HTMLInputElement).value || '0').replace(/\\s/g, '').replace(',', '.')); if (!isNaN(v)) saveTaskField(task.id, 'budgeted_hours', v) }"
                      @keydown.enter="(e: Event) => (e.target as HTMLInputElement).blur()"
                    />
                  </template>
                  <template v-else><span class="font-mono">{{ task.budgeted_hours }}</span></template>
                </td>
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

      <p class="budget-hint">Les lignes de facturation référenceront le budget de chaque tâche.</p>
    </template>

    <!-- ═══ Avancement ═══ -->
    <template v-if="activeTab === 'progress'">
      <div v-if="tasksByPhase.length">
        <div v-for="group in tasksByPhase" :key="'prog-' + group.phase_name" class="task-phase-group">
          <div class="task-phase-header" @click="togglePhaseCollapse('prog-' + group.phase_name)">
            <span class="task-phase-toggle">{{ collapsedPhases.has('prog-' + group.phase_name) ? '&#9654;' : '&#9660;' }}</span>
            <span class="font-semibold">{{ group.phase_name }}</span>
            <span class="text-muted" style="margin-left:8px;">({{ group.tasks.length }} tâche{{ group.tasks.length > 1 ? 's' : '' }})</span>
          </div>
          <table v-if="!collapsedPhases.has('prog-' + group.phase_name)" class="data-table task-table task-table-fixed">
            <thead>
              <tr>
                <th style="width:60px;">WBS</th>
                <th>Tâche</th>
                <th class="text-right" style="width:100px;">Budget ($)</th>
                <th class="text-right" style="width:80px;">H. planifiées</th>
                <th class="text-right" style="width:80px;">H. réelles</th>
                <th class="text-right" style="width:90px;">% Avancement</th>
                <th class="text-right" style="width:80px;">Écart</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="task in group.tasks" :key="'prog-t-' + task.id">
                <td class="font-mono text-muted">{{ task.wbs_code || '—' }}</td>
                <td>
                  <span v-if="task.task_type === 'SUBTASK'" class="subtask-indent"></span>
                  {{ task.display_label || task.name }}
                </td>
                <td class="text-right font-mono">{{ formatAmount(task.budgeted_cost) }}</td>
                <td class="text-right font-mono">{{ task.budgeted_hours }}</td>
                <td class="text-right font-mono">0</td>
                <td class="text-right">
                  <input
                    class="progress-input"
                    :value="task.progress_pct ?? 0"
                    type="number"
                    min="0"
                    max="100"
                    step="1"
                    @blur="(e: Event) => saveProgressPct(task.id, (e.target as HTMLInputElement).value)"
                    @keydown.enter="(e: Event) => (e.target as HTMLInputElement).blur()"
                  />
                </td>
                <td class="text-right">
                  <span
                    class="badge"
                    :class="progressColor(Number(task.progress_pct ?? 0) - (Number(task.budgeted_hours) > 0 ? (0 / Number(task.budgeted_hours) * 100) : 0))"
                  >
                    {{ (Number(task.progress_pct ?? 0) - (Number(task.budgeted_hours) > 0 ? (0 / Number(task.budgeted_hours) * 100) : 0)).toFixed(1) }}%
                  </span>
                </td>
              </tr>
            </tbody>
            <tfoot>
              <tr class="budget-total-row">
                <td class="font-semibold" colspan="2">{{ group.phase_name }} — Total</td>
                <td class="text-right font-mono font-semibold">{{ formatAmount(group.tasks.reduce((s, t) => s + Number(t.budgeted_cost || 0), 0)) }}</td>
                <td class="text-right font-mono font-semibold">{{ group.tasks.reduce((s, t) => s + Number(t.budgeted_hours || 0), 0) }}</td>
                <td class="text-right font-mono font-semibold">0</td>
                <td class="text-right font-mono font-semibold">{{ (group.tasks.reduce((s, t) => s + Number((t as TaskItem & { progress_pct?: number | string }).progress_pct ?? 0), 0) / (group.tasks.length || 1)).toFixed(1) }}%</td>
                <td></td>
              </tr>
            </tfoot>
          </table>
        </div>
      </div>
      <div v-else class="card empty-card">Aucune tâche — ajoutez des tâches dans l'onglet Tâches</div>
    </template>

    <!-- ═══ Finance ═══ -->
    <template v-if="activeTab === 'finance'">
      <div class="kpi-grid-5">
        <div class="kpi-card"><div class="kpi-value mono">0,00&nbsp;$</div><div class="kpi-label">CA facturé</div></div>
        <div class="kpi-card"><div class="kpi-value mono">0,00&nbsp;$</div><div class="kpi-label">Coûts salaires</div></div>
        <div class="kpi-card"><div class="kpi-value mono">0,00&nbsp;$</div><div class="kpi-label">Coûts ST</div></div>
        <div class="kpi-card"><div class="kpi-value mono">0,00&nbsp;$</div><div class="kpi-label">Marge</div></div>
        <div class="kpi-card"><div class="kpi-value mono">0,0&nbsp;%</div><div class="kpi-label">Marge %</div></div>
      </div>

      <div class="card-table">
        <table class="data-table">
          <thead>
            <tr>
              <th>Année</th>
              <th class="text-right">CA ($)</th>
              <th class="text-right">Coûts ($)</th>
              <th class="text-right">Marge ($)</th>
              <th class="text-right">Marge %</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in financeData" :key="row.year">
              <td class="font-semibold">{{ row.year }}</td>
              <td class="text-right font-mono">{{ formatAmount(row.ca) }}</td>
              <td class="text-right font-mono">{{ formatAmount(row.costs) }}</td>
              <td class="text-right font-mono">{{ formatAmount(row.margin) }}</td>
              <td class="text-right font-mono">{{ row.margin_pct.toFixed(1) }}%</td>
            </tr>
          </tbody>
        </table>
      </div>
      <p class="budget-hint">Les données financières seront calculées automatiquement à partir des factures et des feuilles de temps.</p>
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

    <AssignmentModal :open="showAssignModal" :project-id="projectId" :phase-id="assignPhaseId" :phase-name="assignPhaseName" @close="showAssignModal = false" @assigned="reload" />
  </div>
</template>

<style scoped>
.page-header { display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 16px; }
.page-header h1 { font-size: 20px; font-weight: 700; color: var(--color-gray-900); margin-top: 2px; }
.code { font-family: var(--font-mono); color: var(--color-gray-400); font-weight: 400; }
.btn-back { background: none; border: none; font-size: 12px; color: var(--color-gray-500); cursor: pointer; padding: 0; }
.header-actions { display: flex; align-items: center; gap: 8px; position: relative; }
.btn-danger { padding: 4px 10px; border-radius: 4px; font-size: 11px; font-weight: 600; cursor: pointer; border: none; background: var(--color-danger); color: white; }

.badge { display: inline-flex; padding: 2px 10px; border-radius: 10px; font-size: 10px; font-weight: 600; cursor: pointer; border: none; background: var(--color-gray-100); }
.badge-internal { display: inline-flex; padding: 2px 10px; border-radius: 10px; font-size: 10px; font-weight: 700; background: #EDE9FE; color: #7C3AED; }
.badge-green { background: #DCFCE7; color: #15803D; } .badge-amber { background: #FEF3C7; color: #92400E; }
.badge-gray { background: var(--color-gray-100); color: var(--color-gray-500); } .badge-red { background: #FEE2E2; color: #DC2626; }
.badge-blue { background: #DBEAFE; color: #1D4ED8; }

.status-dropdown { position: absolute; top: 100%; right: 0; z-index: 50; margin-top: 4px; background: white; border-radius: 6px; box-shadow: 0 4px 12px rgba(0,0,0,0.12); padding: 4px; min-width: 140px; }
.status-option { display: block; width: 100%; padding: 6px 8px; border: none; background: none; cursor: pointer; text-align: left; border-radius: 4px; }
.status-option:hover { background: var(--color-gray-50); }
.status-option.active { background: var(--color-primary-light); }

.alert-error { background: var(--color-danger-light); color: var(--color-danger); padding: 8px 12px; border-radius: 6px; font-size: 12px; margin-bottom: 12px; }
.alert-danger-banner { background: #FEE2E2; color: #DC2626; padding: 12px 16px; border-radius: 6px; font-size: 13px; font-weight: 600; margin-bottom: 12px; }
.banner-actions { display: flex; gap: 8px; margin-top: 8px; }

.tabs { display: flex; gap: 0; border-bottom: 2px solid var(--color-gray-200); margin-bottom: 16px; }
.tab { padding: 8px 14px; font-size: 12px; font-weight: 500; color: var(--color-gray-500); cursor: pointer; border: none; background: none; border-bottom: 2px solid transparent; margin-bottom: -2px; display: flex; align-items: center; gap: 4px; }
.tab.active { color: var(--color-primary); border-bottom-color: var(--color-primary); font-weight: 600; }
.tab-count { font-size: 9px; background: var(--color-gray-200); color: var(--color-gray-600); padding: 0 5px; border-radius: 8px; }

.kpi-grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 16px; }
.kpi-card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 14px; text-align: center; }
.kpi-value { font-size: 24px; font-weight: 700; color: var(--color-gray-900); }
.kpi-value.mono { font-family: var(--font-mono); font-size: 20px; }
.kpi-value.success { color: var(--color-success); } .kpi-value.warning { color: var(--color-warning); } .kpi-value.danger { color: var(--color-danger); }
.kpi-label { font-size: 10px; color: var(--color-gray-500); text-transform: uppercase; font-weight: 600; }

.info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.info-card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 16px; }
.info-card h3 { font-size: 11px; font-weight: 600; color: var(--color-gray-400); text-transform: uppercase; margin-bottom: 12px; }
.info-pairs { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 13px; }
.info-pairs.single { grid-template-columns: 1fr; }
.info-pairs span { color: var(--color-gray-500); font-size: 11px; } .info-pairs p { font-weight: 600; margin-top: 1px; }

.card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 16px; margin-bottom: 12px; }
.card-table { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); overflow: hidden; }
.empty { text-align: center; padding: 24px; color: var(--color-gray-400); } .empty-card { text-align: center; color: var(--color-gray-400); font-size: 13px; }

.text-right { text-align: right; } .text-muted { color: var(--color-gray-500); font-size: 12px; }
.font-mono { font-family: var(--font-mono); font-size: 12px; } .font-semibold { font-weight: 600; }
.actions-cell { white-space: nowrap; }
.btn-action { background: none; border: none; font-size: 11px; cursor: pointer; color: var(--color-primary); padding: 2px 6px; font-weight: 600; }
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
.data-table thead th { padding: 8px 12px; font-size: 11px; font-weight: 600; text-transform: uppercase; color: var(--color-gray-500); background: var(--color-gray-50); border-bottom: 2px solid var(--color-gray-200); text-align: left; }
.data-table tbody td { padding: 8px 12px; border-bottom: 1px solid var(--color-gray-100); }
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

/* Budget phase group row */
.budget-phase-row td {
  background: var(--color-gray-50); font-size: 11px; text-transform: uppercase;
  color: var(--color-gray-600); padding: 6px 12px; border-bottom: 1px solid var(--color-gray-200);
}

/* Progress tab */
.progress-input {
  width: 70px; padding: 4px 6px; border: 1px solid var(--color-gray-300); border-radius: 3px;
  font-size: 12px; font-family: var(--font-mono); text-align: right; background: white;
  -moz-appearance: textfield;
}
.progress-input::-webkit-outer-spin-button,
.progress-input::-webkit-inner-spin-button { -webkit-appearance: none; margin: 0; }
.progress-input:focus { outline: none; border-color: var(--color-primary); box-shadow: 0 0 0 2px rgba(59,130,246,0.15); }
.progress-green { background: #DCFCE7; color: #15803D; }
.progress-amber { background: #FEF3C7; color: #92400E; }
.progress-red { background: #FEE2E2; color: #DC2626; }

/* Finance tab */
.kpi-grid-5 { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; margin-bottom: 16px; }

.form-actions { display: flex; gap: 6px; justify-content: flex-end; }
.form-row-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
</style>
