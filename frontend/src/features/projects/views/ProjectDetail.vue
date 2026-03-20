<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useLocale } from '@/shared/composables/useLocale'
import { projectApi } from '../api/projectApi'
import { useProjectStore } from '../stores/useProjectStore'
import AssignmentModal from '../components/AssignmentModal.vue'

const route = useRoute()
const router = useRouter()
const store = useProjectStore()
const { fmt } = useLocale()
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
interface Assignment { id: number; employee: number; phase: number | null; percentage: string; start_date: string | null; end_date: string | null }
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
const editingWBSForm = ref({ standard_label: '', client_facing_label: '', budgeted_hours: '' })

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

async function saveProject() {
  actionError.value = ''
  try {
    await projectApi.update(projectId, projectForm.value as Record<string, unknown>)
    editingProject.value = false
    await reload()
  } catch (e: unknown) { actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur' }
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

// Amendment form
const showAmendmentForm = ref(false)
const amendmentForm = ref({ description: '', budget_impact: '0', status: 'DRAFT' })

const tabs = [
  { key: 'overview', label: 'Vue d\'ensemble' },
  { key: 'phases', label: 'Phases' },
  { key: 'wbs', label: 'WBS' },
  { key: 'team', label: 'Équipe' },
  { key: 'amendments', label: 'Avenants' },
  { key: 'budget', label: 'Budget' },
]

const statuses = [
  { value: 'ACTIVE', label: 'Actif', color: 'badge-green' },
  { value: 'ON_HOLD', label: 'En pause', color: 'badge-amber' },
  { value: 'COMPLETED', label: 'Terminé', color: 'badge-gray' },
  { value: 'CANCELLED', label: 'Annulé', color: 'badge-red' },
]

const statusColors: Record<string, string> = { ACTIVE: 'badge-green', ON_HOLD: 'badge-amber', COMPLETED: 'badge-gray', CANCELLED: 'badge-red' }

async function reload() {
  await store.fetchProject(projectId)
  try { const r = await projectApi.dashboard(projectId); dashboard.value = r.data?.data || r.data } catch { dashboard.value = null }
  try { const r = await projectApi.listWBS(projectId); wbsTree.value = r.data?.data || r.data || [] } catch { wbsTree.value = [] }
  try { const r = await projectApi.listAssignments(projectId); assignments.value = r.data?.data || r.data || [] } catch { assignments.value = [] }
  try { const r = await projectApi.listAmendments(projectId); amendments.value = r.data?.data || r.data || [] } catch { amendments.value = [] }
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
  try {
    await projectApi.delete(projectId)
    router.push('/projects')
  } catch (e: unknown) { actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur' }
}

function openAssignModal(phaseId: number | null, phaseName: string) {
  assignPhaseId.value = phaseId; assignPhaseName.value = phaseName; showAssignModal.value = true
}

async function deletePhase(phaseId: number) {
  await projectApi.deletePhase(projectId, phaseId)
  confirmDeletePhase.value = null
  await reload()
}

async function deleteAssignment(assignId: number) {
  await projectApi.deleteAssignment(projectId, assignId)
  confirmDeleteAssignment.value = null
  await reload()
}

async function deleteWBS(wbsId: number) {
  await projectApi.deleteWBSElement(projectId, wbsId)
  confirmDeleteWBS.value = null
  await reload()
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

async function deleteAmendment(id: number) {
  await projectApi.deleteAmendment(projectId, id)
  confirmDeleteAmendment.value = null
  await reload()
}

onMounted(reload)
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
        <!-- Status badge (clickable only in edit mode) -->
        <div class="relative">
          <button class="badge" :class="statusColors[store.currentProject.status]" @click="isEditing && (showEditStatus = !showEditStatus)" :style="isEditing ? 'cursor:pointer' : 'cursor:default'">
            {{ statuses.find(s => s.value === store.currentProject?.status)?.label || store.currentProject.status }} <span v-if="isEditing">&#x25BE;</span>
          </button>
          <div v-if="showEditStatus && isEditing" class="status-dropdown">
            <button v-for="s in statuses" :key="s.value" class="status-option" :class="{ active: s.value === store.currentProject.status }" @click="changeStatus(s.value)">
              <span class="badge" :class="s.color">{{ s.label }}</span>
            </button>
          </div>
        </div>
        <button v-if="!isEditing" class="btn-primary" @click="isEditing = true">Modifier</button>
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
      <div v-if="!editingProject" class="info-grid">
        <div class="info-card"><h3>Informations <button v-if="isEditing" class="btn-action" @click="startEditProject">Modifier</button></h3><div class="info-pairs"><div><span>Type</span><p>{{ store.currentProject.contract_type }}</p></div><div><span>BU</span><p>{{ store.currentProject.business_unit || '—' }}</p></div><div><span>Début</span><p>{{ store.currentProject.start_date ? fmt.date(store.currentProject.start_date) : '—' }}</p></div><div><span>Fin</span><p>{{ store.currentProject.end_date ? fmt.date(store.currentProject.end_date) : '—' }}</p></div></div></div>
        <div class="info-card"><h3>Direction</h3><div class="info-pairs single"><div><span>Chef de projet</span><p>{{ store.currentProject.pm || '—' }}</p></div><div><span>Associé en charge</span><p>{{ store.currentProject.associate_in_charge || '—' }}</p></div></div></div>
      </div>
      <!-- Edit mode -->
      <div v-else class="card">
        <h3 class="card-title-edit">Modifier le projet</h3>
        <div class="edit-grid">
          <div class="form-group"><label>Nom</label><input v-model="projectForm.name" /></div>
          <div class="form-group"><label>Unité d'affaires</label><input v-model="projectForm.business_unit" /></div>
          <div class="form-group"><label>Date début</label><input v-model="projectForm.start_date" type="date" /></div>
          <div class="form-group"><label>Date fin</label><input v-model="projectForm.end_date" type="date" /></div>
          <div class="form-group"><label>Chef de projet (ID)</label><input v-model="projectForm.pm" type="number" /></div>
          <div class="form-group"><label>Associé en charge (ID)</label><input v-model="projectForm.associate_in_charge" type="number" /></div>
        </div>
        <div class="form-actions"><button class="btn-ghost" @click="editingProject = false">Annuler</button><button class="btn-primary" @click="saveProject">Enregistrer</button></div>
      </div>
    </template>

    <!-- ═══ Phases ═══ -->
    <template v-if="activeTab === 'phases'">
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
                    <template v-if="confirmDeletePhase === phase.id">
                      <button class="btn-action danger" @click="deletePhase(phase.id)">Confirmer</button>
                      <button class="btn-action" @click="confirmDeletePhase = null">Annuler</button>
                    </template>
                    <button v-else class="btn-action danger" @click="confirmDeletePhase = phase.id">Supprimer...</button>
                  </template>
                </td>
              </template>
            </tr>
            <tr v-if="!store.currentProject.phases?.length"><td colspan="6" class="empty">Aucune phase</td></tr>
          </tbody>
        </table>
      </div>
    </template>

    <!-- ═══ WBS ═══ -->
    <template v-if="activeTab === 'wbs'">
      <div v-if="isEditing" class="section-actions"><button class="btn-primary" @click="showWBSForm = !showWBSForm">+ Ajouter un élément WBS</button></div>

      <div v-if="showWBSForm" class="card" style="margin-bottom: 12px;">
        <form @submit.prevent="createWBSElement" class="form-row-3">
          <div class="form-group"><label>Libellé standard</label><input v-model="wbsForm.standard_label" type="text" required placeholder="Libellé interne" /></div>
          <div class="form-group"><label>Libellé client</label><input v-model="wbsForm.client_facing_label" type="text" placeholder="Libellé visible client" /></div>
          <div class="form-group"><label>Type</label>
            <select v-model="wbsForm.element_type">
              <option value="PHASE">Phase</option>
              <option value="TASK">Tâche</option>
              <option value="SUBTASK">Sous-tâche</option>
            </select>
          </div>
          <div class="form-group"><label>Heures budgetées</label><input v-model="wbsForm.budgeted_hours" type="number" step="0.01" /></div>
          <div class="form-group"><label>Phase</label>
            <select v-model="wbsForm.phase">
              <option :value="null">— Aucune —</option>
              <option v-for="phase in store.currentProject?.phases" :key="phase.id" :value="phase.id">{{ phase.name }}</option>
            </select>
          </div>
          <div class="form-group">
            <label>&nbsp;</label>
            <div style="display:flex;gap:4px;">
              <button type="button" class="btn-ghost" @click="showWBSForm=false">Annuler</button>
              <button type="submit" class="btn-primary">Créer</button>
            </div>
          </div>
        </form>
      </div>

      <div class="card" v-if="wbsTree.length">
        <div v-for="node in wbsTree" :key="node.id" class="wbs-node">
          <div class="wbs-row">
            <template v-if="editingWBSId === node.id">
              <div class="flex items-center gap-2" style="flex:1">
                <span class="badge badge-blue">{{ node.element_type }}</span>
                <input v-model="editingWBSForm.standard_label" class="inline-input" placeholder="Libellé standard" />
                <input v-model="editingWBSForm.client_facing_label" class="inline-input" placeholder="Libellé client" />
                <input v-model="editingWBSForm.budgeted_hours" type="number" class="inline-input-sm" />
                <button class="btn-action" @click="saveWBS">OK</button>
                <button class="btn-action" @click="editingWBSId = null">&times;</button>
              </div>
            </template>
            <template v-else>
              <div><span class="badge badge-blue">{{ node.element_type }}</span> <span class="font-semibold">{{ node.client_facing_label || node.standard_label }}</span></div>
              <div class="flex items-center gap-4"><span class="font-mono text-muted">{{ node.budgeted_hours }}h</span>
                <template v-if="isEditing">
                  <button class="btn-action" @click="startEditWBS(node)">Modifier</button>
                  <template v-if="confirmDeleteWBS === node.id">
                    <button class="btn-action danger" @click="deleteWBS(node.id)">Confirmer</button>
                    <button class="btn-action" @click="confirmDeleteWBS = null">Annuler</button>
                  </template>
                  <button v-else class="btn-action danger" @click="confirmDeleteWBS = node.id">Supprimer...</button>
                </template>
              </div>
            </template>
          </div>
          <div v-if="node.children?.length" class="wbs-children">
            <div v-for="child in node.children" :key="child.id" class="wbs-child">
              <span>{{ child.client_facing_label || child.standard_label }}</span>
              <span class="font-mono text-muted">{{ child.budgeted_hours }}h</span>
            </div>
          </div>
        </div>
      </div>
      <div v-else-if="!showWBSForm" class="card empty-card">Aucun élément WBS</div>
    </template>

    <!-- ═══ Team ═══ -->
    <template v-if="activeTab === 'team'">
      <div class="card-table" v-if="assignments.length">
        <table>
          <thead><tr><th>Employé</th><th>Phase</th><th class="text-right">%</th><th>Période</th><th></th></tr></thead>
          <tbody>
            <tr v-for="a in assignments" :key="a.id">
              <td class="font-semibold">Employé #{{ a.employee }}</td>
              <td class="text-muted">{{ a.phase ? `Phase #${a.phase}` : 'Global' }}</td>
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

    <!-- ═══ Amendments ═══ -->
    <template v-if="activeTab === 'amendments'">
      <div v-if="isEditing" class="section-actions"><button class="btn-primary" @click="showAmendmentForm = !showAmendmentForm">+ Nouvel avenant</button></div>

      <div v-if="showAmendmentForm" class="card" style="margin-bottom: 12px;">
        <form @submit.prevent="createAmendment" class="form-row-3">
          <div class="form-group"><label>Description</label><input v-model="amendmentForm.description" type="text" required placeholder="Description de l'avenant" /></div>
          <div class="form-group"><label>Impact budget ($)</label><input v-model="amendmentForm.budget_impact" type="number" step="0.01" /></div>
          <div class="form-group"><label>Statut</label><select v-model="amendmentForm.status"><option value="DRAFT">Brouillon</option><option value="PENDING">En attente</option><option value="APPROVED">Approuvé</option></select>
            <div style="margin-top:6px;display:flex;gap:4px;justify-content:flex-end;"><button type="button" class="btn-ghost" @click="showAmendmentForm=false">Annuler</button><button type="submit" class="btn-primary">Créer</button></div>
          </div>
        </form>
      </div>

      <div class="card-table" v-if="amendments.length">
        <table>
          <thead><tr><th>No</th><th>Description</th><th class="text-right">Impact ($)</th><th>Statut</th><th>Date</th><th></th></tr></thead>
          <tbody>
            <tr v-for="am in amendments" :key="am.id">
              <td class="font-mono font-semibold">#{{ am.amendment_number }}</td>
              <td>{{ am.description }}</td>
              <td class="text-right font-mono">{{ fmt.currency(am.budget_impact) }}</td>
              <td><span class="badge" :class="am.status === 'APPROVED' ? 'badge-green' : am.status === 'PENDING' ? 'badge-amber' : 'badge-gray'">{{ am.status }}</span></td>
              <td class="text-muted">{{ am.created_at?.substring(0, 10) }}</td>
              <td class="text-right">
                <template v-if="isEditing">
                  <template v-if="confirmDeleteAmendment === am.id">
                    <button class="btn-action danger" @click="deleteAmendment(am.id)">Confirmer</button>
                    <button class="btn-action" @click="confirmDeleteAmendment = null">Annuler</button>
                  </template>
                  <button v-else class="btn-action danger" @click="confirmDeleteAmendment = am.id">Supprimer...</button>
                </template>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else-if="!showAmendmentForm" class="card empty-card">Aucun avenant</div>
    </template>

    <!-- ═══ Budget ═══ -->
    <template v-if="activeTab === 'budget'">
      <div class="card" v-if="dashboard">
        <div class="progress-row">
          <div class="progress-bar"><div class="progress-fill" :class="{ green: dashboard.health==='green', amber: dashboard.health==='yellow', red: dashboard.health==='red' }" :style="{ width: Math.min(100, dashboard.budget_utilization_percent) + '%' }" /></div>
          <span class="font-mono font-semibold">{{ dashboard.budget_utilization_percent }}%</span>
        </div>
        <div class="budget-grid">
          <div><span class="text-muted">Heures consommées</span><p class="font-mono font-semibold">{{ fmt.hours(dashboard.hours_consumed) }}</p></div>
          <div><span class="text-muted">Budget total</span><p class="font-mono font-semibold">{{ fmt.hours(dashboard.budget_hours) }}</p></div>
        </div>
      </div>
      <div v-else class="card empty-card">Aucune donnée budgétaire</div>
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
</style>
