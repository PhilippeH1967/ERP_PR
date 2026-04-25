<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import apiClient from '@/plugins/axios'

interface InternalProject {
  id: number
  code: string
  name: string
  is_internal: boolean
  status: string
}
interface ProjectTask {
  id: number
  wbs_code: string
  name: string
  client_facing_label: string
  display_label: string
  always_display_in_timesheet: boolean
  is_active: boolean
  phase: number | null
  phase_name: string
}

const projects = ref<InternalProject[]>([])
const tasksByProject = ref<Record<number, ProjectTask[]>>({})
const isLoading = ref(false)
const expandedProjects = ref<Set<number>>(new Set())
const actionError = ref('')
const actionSuccess = ref('')

// Add internal project form
const showAddProject = ref(false)
const newProject = ref({ code: '', name: '' })
const creatingProject = ref(false)

async function loadProjects() {
  isLoading.value = true
  try {
    const resp = await apiClient.get('projects/', { params: { is_internal: 'true', status: 'ACTIVE' } })
    const data = resp.data?.data || resp.data
    const list = Array.isArray(data) ? data : data?.results || []
    projects.value = list as InternalProject[]
  } finally {
    isLoading.value = false
  }
}

async function loadTasks(projectId: number) {
  if (tasksByProject.value[projectId]) return
  try {
    const resp = await apiClient.get(`projects/${projectId}/tasks/`)
    const data = resp.data?.data || resp.data
    tasksByProject.value[projectId] = (Array.isArray(data) ? data : data?.results || []) as ProjectTask[]
  } catch {
    tasksByProject.value[projectId] = []
  }
}

async function toggleExpand(projectId: number) {
  if (expandedProjects.value.has(projectId)) {
    expandedProjects.value.delete(projectId)
  } else {
    expandedProjects.value.add(projectId)
    await loadTasks(projectId)
  }
}

async function toggleAlwaysDisplay(projectId: number, task: ProjectTask) {
  actionError.value = ''
  actionSuccess.value = ''
  const newValue = !task.always_display_in_timesheet
  try {
    await apiClient.patch(`projects/${projectId}/tasks/${task.id}/`, {
      always_display_in_timesheet: newValue,
    })
    task.always_display_in_timesheet = newValue
    actionSuccess.value = newValue
      ? `« ${task.name} » affichée dans toutes les feuilles de temps`
      : `« ${task.name} » retirée des feuilles de temps obligatoires`
  } catch (e: unknown) {
    actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur de sauvegarde'
  }
}

function extractErrorMessage(e: unknown): string {
  const resp = (e as { response?: { data?: unknown } }).response
  const data = resp?.data
  if (!data || typeof data !== 'object') return 'Erreur de création'
  // DRF format 1 : { error: { message: "..." } }
  const dataObj = data as Record<string, unknown>
  const errorObj = dataObj.error as { message?: string } | undefined
  if (errorObj?.message) return errorObj.message
  // DRF format 2 : { field_a: ["msg"], field_b: ["msg"] }
  const parts: string[] = []
  for (const [field, val] of Object.entries(dataObj)) {
    if (Array.isArray(val)) parts.push(`${field}: ${val.join(', ')}`)
    else if (typeof val === 'string') parts.push(`${field}: ${val}`)
  }
  return parts.length ? parts.join(' · ') : 'Erreur de création'
}

async function createInternalProject() {
  actionError.value = ''
  actionSuccess.value = ''
  if (!newProject.value.code.trim() || !newProject.value.name.trim()) {
    actionError.value = 'Code et nom sont obligatoires.'
    return
  }
  creatingProject.value = true
  try {
    const resp = await apiClient.post('projects/', {
      code: newProject.value.code.trim(),
      name: newProject.value.name.trim(),
      contract_type: 'FORFAITAIRE',
      is_internal: true,
      status: 'ACTIVE',
    })
    const created = resp.data?.data || resp.data
    // Auto-créer une phase par défaut "Tâches obligatoires" pour pouvoir
    // ensuite ajouter des tâches sans passer par la fiche projet
    try {
      await apiClient.post(`projects/${created.id}/phases/`, {
        code: 'OBL',
        name: 'Tâches obligatoires',
        billing_mode: 'FORFAIT',
        phase_type: 'SUPPORT',
        is_mandatory: false,
      })
    } catch {
      /* La phase est optionnelle ici — si la création échoue on continuera */
    }
    actionSuccess.value = `Projet interne « ${created.name} » créé`
    showAddProject.value = false
    newProject.value = { code: '', name: '' }
    await loadProjects()
    // Étendre automatiquement le projet créé pour que l'utilisateur voie le formulaire de tâche
    expandedProjects.value.add(created.id)
    await loadTasks(created.id)
  } catch (e: unknown) {
    actionError.value = extractErrorMessage(e)
  } finally {
    creatingProject.value = false
  }
}

// ─── Création / suppression inline de tâches obligatoires ─────────────────
const newTaskNameByProject = ref<Record<number, string>>({})
const creatingTaskByProject = ref<Record<number, boolean>>({})
const confirmDeleteTaskId = ref<number | null>(null)

async function createMandatoryTask(projectId: number) {
  actionError.value = ''
  actionSuccess.value = ''
  const taskName = (newTaskNameByProject.value[projectId] || '').trim()
  if (!taskName) {
    actionError.value = 'Le nom de la tâche est obligatoire.'
    return
  }
  creatingTaskByProject.value[projectId] = true
  try {
    // Récupérer la première phase du projet (auto-créée à la création du projet)
    let phaseId: number | null = null
    try {
      const phResp = await apiClient.get(`projects/${projectId}/phases/`)
      const phData = phResp.data?.data || phResp.data
      const phases = Array.isArray(phData) ? phData : phData?.results || []
      phaseId = phases[0]?.id || null
    } catch { /* ignore */ }

    // Si aucune phase, en créer une à la volée
    if (!phaseId) {
      const phResp = await apiClient.post(`projects/${projectId}/phases/`, {
        code: 'OBL',
        name: 'Tâches obligatoires',
        billing_mode: 'FORFAIT',
        phase_type: 'SUPPORT',
        is_mandatory: false,
      })
      phaseId = (phResp.data?.data || phResp.data)?.id
    }

    await apiClient.post(`projects/${projectId}/tasks/`, {
      project: projectId,
      phase: phaseId,
      name: taskName,
      task_type: 'TASK',
      billing_mode: 'FORFAIT',
      always_display_in_timesheet: true, // ← auto-marquée obligatoire
    })
    actionSuccess.value = `« ${taskName} » créée et marquée obligatoire`
    newTaskNameByProject.value[projectId] = ''
    // Reload des tâches pour voir la nouvelle
    delete tasksByProject.value[projectId]
    await loadTasks(projectId)
  } catch (e: unknown) {
    actionError.value = extractErrorMessage(e)
  } finally {
    creatingTaskByProject.value[projectId] = false
  }
}

async function deleteTask(projectId: number, task: ProjectTask) {
  if (confirmDeleteTaskId.value !== task.id) {
    confirmDeleteTaskId.value = task.id
    return
  }
  confirmDeleteTaskId.value = null
  actionError.value = ''
  actionSuccess.value = ''
  try {
    await apiClient.delete(`projects/${projectId}/tasks/${task.id}/`)
    actionSuccess.value = `« ${task.name} » supprimée`
    delete tasksByProject.value[projectId]
    await loadTasks(projectId)
  } catch (e: unknown) {
    actionError.value = extractErrorMessage(e)
  }
}

async function toggleAllMandatory(projectId: number, makeAllOn: boolean) {
  actionError.value = ''
  actionSuccess.value = ''
  const tasks = tasksByProject.value[projectId] || []
  if (!tasks.length) return
  try {
    await Promise.all(tasks.map(t =>
      apiClient.patch(`projects/${projectId}/tasks/${t.id}/`, {
        always_display_in_timesheet: makeAllOn,
      }),
    ))
    tasks.forEach(t => { t.always_display_in_timesheet = makeAllOn })
    actionSuccess.value = makeAllOn
      ? `${tasks.length} tâche(s) marquée(s) obligatoire(s)`
      : `${tasks.length} tâche(s) retirée(s) des obligatoires`
  } catch (e: unknown) {
    actionError.value = extractErrorMessage(e)
  }
}

const totalMandatory = computed(() => {
  let count = 0
  for (const list of Object.values(tasksByProject.value)) {
    count += list.filter(t => t.always_display_in_timesheet).length
  }
  return count
})

onMounted(loadProjects)
</script>

<template>
  <div>
    <div class="page-header">
      <h1>Feuilles de temps — Tâches obligatoires</h1>
      <button class="btn-primary" data-add-project @click="showAddProject = !showAddProject">
        {{ showAddProject ? 'Annuler' : '+ Nouveau projet interne' }}
      </button>
    </div>

    <p class="page-intro">
      Crée des projets internes et leurs tâches obligatoires <strong>directement ici</strong>.
      Les tâches obligatoires apparaîtront dans la grille hebdomadaire de chaque employé même sans
      heures saisies. Idéal pour <em>Congés</em>, <em>Maladie</em>, <em>Administration</em>,
      <em>Formation</em>, etc.
    </p>

    <div v-if="actionError" class="alert-error">{{ actionError }}</div>
    <div v-if="actionSuccess" class="alert-success">{{ actionSuccess }}</div>

    <!-- New project form -->
    <div v-if="showAddProject" class="form-card">
      <div class="form-row">
        <div class="form-field">
          <label>Code *</label>
          <input v-model="newProject.code" data-new-project-code placeholder="ex. INT-001" />
        </div>
        <div class="form-field" style="flex:2;">
          <label>Nom *</label>
          <input v-model="newProject.name" data-new-project-name placeholder="ex. Interne — Congés et absences" />
        </div>
        <button class="btn-primary" :disabled="creatingProject" data-create-project @click="createInternalProject">
          {{ creatingProject ? 'Création…' : 'Créer' }}
        </button>
      </div>
      <p class="form-desc">
        Le projet sera créé en tant que <strong>projet interne</strong> (non facturable). Tu pourras
        ensuite y ajouter des tâches via la fiche projet, puis revenir ici pour activer
        <em>« Affichage obligatoire »</em>.
      </p>
    </div>

    <!-- Projects list -->
    <div class="section-card">
      <div class="section-header">
        <h3>Projets internes ({{ projects.length }})</h3>
        <span v-if="totalMandatory > 0" class="section-count">{{ totalMandatory }} tâche(s) obligatoire(s)</span>
      </div>

      <div v-if="isLoading" class="empty">Chargement…</div>
      <div v-else-if="!projects.length" class="empty">
        Aucun projet interne. Créez-en un avec <em>+ Nouveau projet interne</em>.
      </div>

      <div v-for="p in projects" :key="p.id" class="project-block" data-project-block>
        <div class="project-header" @click="toggleExpand(p.id)">
          <span class="toggle">{{ expandedProjects.has(p.id) ? '▼' : '▶' }}</span>
          <span class="font-mono font-semibold">{{ p.code }}</span>
          <span class="text-muted"> — {{ p.name }}</span>
        </div>

        <div v-if="expandedProjects.has(p.id)" class="project-tasks">
          <!-- Add task inline -->
          <div class="add-task-row">
            <input
              v-model="newTaskNameByProject[p.id]"
              type="text"
              placeholder="ex. Congés, Maladie, Administration, Formation…"
              class="task-input"
              data-new-task-name
              @keydown.enter="createMandatoryTask(p.id)"
            />
            <button
              class="btn-primary btn-sm"
              :disabled="creatingTaskByProject[p.id] || !newTaskNameByProject[p.id]?.trim()"
              data-create-task
              @click="createMandatoryTask(p.id)"
            >
              {{ creatingTaskByProject[p.id] ? '…' : '+ Tâche obligatoire' }}
            </button>
          </div>
          <p class="add-task-hint">
            Les tâches créées ici sont automatiquement marquées <strong>obligatoires</strong> —
            elles apparaîtront dans la grille hebdomadaire de chaque employé.
          </p>

          <!-- Tasks table -->
          <div v-if="!(tasksByProject[p.id]?.length)" class="empty-tasks">
            Aucune tâche pour l'instant. Ajoute la première ci-dessus.
          </div>
          <template v-else>
            <div class="task-actions-bar">
              <span class="text-muted" style="font-size: 11px;">{{ tasksByProject[p.id]!.length }} tâche(s)</span>
              <div class="flex gap-2">
                <button
                  class="btn-sm-secondary"
                  data-toggle-all-on
                  @click="toggleAllMandatory(p.id, true)"
                >Tout marquer obligatoire</button>
                <button
                  class="btn-sm-secondary"
                  data-toggle-all-off
                  @click="toggleAllMandatory(p.id, false)"
                >Tout retirer</button>
              </div>
            </div>
            <table>
              <thead>
                <tr>
                  <th>WBS</th>
                  <th>Tâche</th>
                  <th class="text-center">Affichage obligatoire</th>
                  <th class="text-right" style="width: 120px;">Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="t in tasksByProject[p.id]" :key="t.id" data-task-row>
                  <td class="font-mono">{{ t.wbs_code }}</td>
                  <td>{{ t.display_label || t.name }}</td>
                  <td class="text-center">
                    <button
                      type="button"
                      class="toggle-btn"
                      :class="t.always_display_in_timesheet ? 'on' : 'off'"
                      data-toggle-mandatory
                      @click="toggleAlwaysDisplay(p.id, t)"
                    >
                      {{ t.always_display_in_timesheet ? '✓ Activé' : '— Désactivé' }}
                    </button>
                  </td>
                  <td class="text-right">
                    <template v-if="confirmDeleteTaskId === t.id">
                      <button class="btn-sm-danger" data-delete-task-confirm @click="deleteTask(p.id, t)">Confirmer</button>
                      <button class="btn-sm-secondary" @click="confirmDeleteTaskId = null">Annuler</button>
                    </template>
                    <button
                      v-else
                      class="btn-sm-link"
                      data-delete-task
                      @click="deleteTask(p.id, t)"
                    >Supprimer…</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; }
.page-header h1 { font-size: 20px; font-weight: 700; color: var(--color-gray-900); }
.page-intro { font-size: 13px; color: var(--color-gray-600); margin-bottom: 16px; line-height: 1.5; }

.btn-primary { padding: 6px 14px; border-radius: 6px; font-size: 12px; font-weight: 600; background: var(--color-primary); color: white; border: none; cursor: pointer; }
.btn-primary:hover:not(:disabled) { filter: brightness(0.95); }
.btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }

.alert-error { background: #FEE2E2; color: #DC2626; padding: 8px 12px; border-radius: 6px; font-size: 12px; margin-bottom: 12px; }
.alert-success { background: #DCFCE7; color: #15803D; padding: 8px 12px; border-radius: 6px; font-size: 12px; margin-bottom: 12px; }

.form-card { background: white; border: 1px solid var(--color-gray-200); border-radius: 8px; padding: 16px; margin-bottom: 16px; }
.form-row { display: flex; gap: 12px; align-items: flex-end; }
.form-field { flex: 1; display: flex; flex-direction: column; gap: 4px; }
.form-field label { font-size: 11px; font-weight: 600; color: var(--color-gray-600); }
.form-field input { padding: 6px 8px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 13px; }
.form-desc { font-size: 11px; color: var(--color-gray-500); margin-top: 8px; }

.section-card { background: white; border: 1px solid var(--color-gray-200); border-radius: 8px; overflow: hidden; }
.section-header { display: flex; align-items: center; justify-content: space-between; padding: 12px 16px; border-bottom: 1px solid var(--color-gray-200); background: var(--color-gray-50); }
.section-header h3 { font-size: 13px; font-weight: 600; color: var(--color-gray-900); }
.section-count { font-size: 11px; color: var(--color-gray-500); }

.project-block { border-bottom: 1px solid var(--color-gray-100); }
.project-block:last-child { border-bottom: none; }
.project-header { display: flex; align-items: center; gap: 6px; padding: 10px 16px; cursor: pointer; font-size: 13px; }
.project-header:hover { background: var(--color-gray-50); }
.toggle { color: var(--color-gray-400); font-size: 10px; min-width: 12px; }
.font-mono { font-family: var(--font-mono); }
.font-semibold { font-weight: 600; }
.text-muted { color: var(--color-gray-500); }

.project-tasks { padding: 0 16px 12px 32px; }
.empty-tasks { padding: 12px 0; color: var(--color-gray-400); font-size: 12px; font-style: italic; }
.empty { padding: 24px; text-align: center; color: var(--color-gray-400); font-size: 13px; }

table { width: 100%; font-size: 12px; border-collapse: collapse; }
thead th { padding: 6px 10px; font-weight: 600; color: var(--color-gray-600); font-size: 11px; text-align: left; border-bottom: 1px solid var(--color-gray-200); }
tbody tr { border-bottom: 1px solid var(--color-gray-100); }
tbody td { padding: 6px 10px; color: var(--color-gray-700); }
.text-center { text-align: center; }

.toggle-btn { padding: 3px 12px; border-radius: 12px; font-size: 11px; font-weight: 600; border: 1px solid; cursor: pointer; transition: all 0.15s; }
.toggle-btn.on { background: #DCFCE7; color: #15803D; border-color: #BBF7D0; }
.toggle-btn.on:hover { background: #BBF7D0; }
.toggle-btn.off { background: white; color: var(--color-gray-500); border-color: var(--color-gray-300); }
.toggle-btn.off:hover { background: var(--color-gray-50); }

.add-task-row { display: flex; gap: 8px; align-items: center; padding: 8px 0; }
.task-input { flex: 1; padding: 6px 10px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 13px; }
.task-input:focus { border-color: var(--color-primary); outline: none; }
.add-task-hint { font-size: 11px; color: var(--color-gray-500); margin: 0 0 12px; font-style: italic; }
.btn-sm { padding: 5px 12px; border-radius: 4px; font-size: 11px; font-weight: 600; border: none; cursor: pointer; }

.task-actions-bar { display: flex; align-items: center; justify-content: space-between; padding: 6px 0; border-top: 1px dashed var(--color-gray-200); border-bottom: 1px dashed var(--color-gray-200); margin: 8px 0; }
.btn-sm-secondary { padding: 3px 10px; border-radius: 4px; font-size: 11px; font-weight: 600; background: white; border: 1px solid var(--color-gray-300); color: var(--color-gray-700); cursor: pointer; }
.btn-sm-secondary:hover { background: var(--color-gray-50); }
.btn-sm-danger { padding: 3px 10px; border-radius: 4px; font-size: 11px; font-weight: 600; background: #DC2626; color: white; border: none; cursor: pointer; }
.btn-sm-link { padding: 3px 10px; border-radius: 4px; font-size: 11px; font-weight: 600; background: none; border: none; color: var(--color-danger); cursor: pointer; }
.btn-sm-link:hover { background: #FEE2E2; }
.text-right { text-align: right; }
.flex { display: flex; }
.gap-2 { gap: 8px; }
</style>
