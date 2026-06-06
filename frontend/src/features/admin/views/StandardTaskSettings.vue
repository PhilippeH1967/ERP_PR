<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/plugins/axios'

const router = useRouter()

interface SPhase { id: number; code: string; name: string; order: number }
interface STask {
  id: number
  standard_phase: number
  parent: number | null
  name: string
  client_facing_label: string
  billing_mode: 'FORFAIT' | 'HORAIRE'
  order: number
  is_active: boolean
}

const phases = ref<SPhase[]>([])
const tasks = ref<STask[]>([])
const isLoading = ref(true)

async function fetchAll() {
  isLoading.value = true
  try {
    const [pr, tr] = await Promise.all([
      apiClient.get('standard_phases/'),
      apiClient.get('standard_tasks/'),
    ])
    const pd = pr.data?.data || pr.data
    const td = tr.data?.data || tr.data
    phases.value = (Array.isArray(pd) ? pd : pd?.results || []).sort(
      (a: SPhase, b: SPhase) => a.order - b.order,
    )
    tasks.value = Array.isArray(td) ? td : td?.results || []
  } catch {
    phases.value = []
    tasks.value = []
  } finally {
    isLoading.value = false
  }
}

// Phases → tâches racines (parent=null) → sous-tâches.
const grouped = computed(() =>
  phases.value.map((ph) => {
    const phaseTasks = tasks.value.filter((t) => t.standard_phase === ph.id)
    const byOrder = (a: STask, b: STask) => a.order - b.order || a.name.localeCompare(b.name)
    const roots = phaseTasks.filter((t) => !t.parent).sort(byOrder)
    return {
      phase: ph,
      roots: roots.map((r) => ({
        task: r,
        subtasks: phaseTasks.filter((t) => t.parent === r.id).sort(byOrder),
      })),
    }
  }),
)

// --- Form (création / édition) ---
const showForm = ref(false)
const editingId = ref<number | null>(null)
const saveError = ref('')
const emptyForm = () => ({
  standard_phase: null as number | null,
  parent: null as number | null,
  name: '',
  client_facing_label: '',
  billing_mode: 'FORFAIT' as 'FORFAIT' | 'HORAIRE',
  order: 0,
  is_active: true,
})
const form = ref(emptyForm())
const formTitle = ref('')

function openAddTask(phase: SPhase) {
  editingId.value = null
  saveError.value = ''
  const count = tasks.value.filter((t) => t.standard_phase === phase.id && !t.parent).length
  form.value = { ...emptyForm(), standard_phase: phase.id, parent: null, order: count }
  formTitle.value = `Nouvelle tâche — ${phase.code} · ${phase.name}`
  showForm.value = true
}

function openAddSubtask(phase: SPhase, parentTask: STask) {
  editingId.value = null
  saveError.value = ''
  const count = tasks.value.filter((t) => t.parent === parentTask.id).length
  form.value = { ...emptyForm(), standard_phase: phase.id, parent: parentTask.id, order: count }
  formTitle.value = `Nouvelle sous-tâche — ${parentTask.name}`
  showForm.value = true
}

function openEdit(t: STask) {
  editingId.value = t.id
  saveError.value = ''
  form.value = {
    standard_phase: t.standard_phase,
    parent: t.parent,
    name: t.name,
    client_facing_label: t.client_facing_label,
    billing_mode: t.billing_mode,
    order: t.order,
    is_active: t.is_active,
  }
  formTitle.value = t.parent ? 'Modifier la sous-tâche' : 'Modifier la tâche'
  showForm.value = true
}

async function save() {
  saveError.value = ''
  if (!form.value.name.trim()) { saveError.value = 'Le nom est obligatoire.'; return }
  try {
    if (editingId.value) {
      await apiClient.patch(`standard_tasks/${editingId.value}/`, form.value)
    } else {
      await apiClient.post('standard_tasks/', form.value)
    }
    showForm.value = false
    editingId.value = null
    await fetchAll()
  } catch (e: unknown) {
    const err = e as { response?: { data?: Record<string, unknown> } }
    const d = err.response?.data
    const first = d ? Object.values(d)[0] : null
    saveError.value = Array.isArray(first) ? String(first[0]) : (typeof first === 'string' ? first : 'Erreur')
  }
}

const confirmDeleteId = ref<number | null>(null)
async function deleteTask(id: number) {
  confirmDeleteId.value = null
  tasks.value = tasks.value.filter((t) => t.id !== id && t.parent !== id)
  try { await apiClient.delete(`standard_tasks/${id}/`) } catch { /* ok */ }
}

onMounted(fetchAll)
</script>

<template>
  <div>
    <div class="page-header">
      <div>
        <button class="btn-back" @click="router.push('/admin')">&larr; Administration</button>
        <h1>Tâches standard</h1>
      </div>
    </div>

    <p class="hint">
      Catalogue de <strong>tâches et sous-tâches standard par phase</strong>. À l'ouverture d'un projet,
      l'utilisateur peut les ajouter par phase (les tâches déjà présentes sont exclues). C'est ici que
      le catalogue se paramètre.
    </p>

    <div v-if="isLoading" class="loading">Chargement…</div>
    <div v-else-if="!phases.length" class="card"><div class="empty">Aucune phase standard. Définissez d'abord les <button class="btn-icon" @click="router.push('/admin/standard-phases')">phases standard</button>.</div></div>

    <div v-else class="groups">
      <div v-for="g in grouped" :key="g.phase.id" class="phase-card">
        <div class="phase-head">
          <span class="phase-code">{{ g.phase.code }}</span>
          <span class="phase-name">{{ g.phase.name }}</span>
          <span class="phase-count">{{ g.roots.length }} tâche{{ g.roots.length > 1 ? 's' : '' }}</span>
          <button class="btn-primary btn-sm" @click="openAddTask(g.phase)">+ Tâche</button>
        </div>
        <div v-if="!g.roots.length" class="phase-empty">Aucune tâche standard pour cette phase.</div>
        <div v-for="r in g.roots" :key="r.task.id" class="task-block">
          <div class="task-row" :class="{ 'row-inactive': !r.task.is_active }">
            <span class="task-name">{{ r.task.name }}</span>
            <span class="badge">{{ r.task.billing_mode === 'HORAIRE' ? 'Horaire' : 'Forfait' }}</span>
            <span v-if="!r.task.is_active" class="badge badge-off">Inactive</span>
            <span class="task-actions">
              <button class="btn-icon" @click="openAddSubtask(g.phase, r.task)">+ Sous-tâche</button>
              <button class="btn-icon" @click="openEdit(r.task)">Modifier</button>
              <template v-if="confirmDeleteId === r.task.id">
                <button class="btn-icon btn-icon-danger" @click="deleteTask(r.task.id)">Confirmer</button>
                <button class="btn-icon" @click="confirmDeleteId = null">Annuler</button>
              </template>
              <button v-else class="btn-icon btn-icon-danger" @click="confirmDeleteId = r.task.id">Supprimer</button>
            </span>
          </div>
          <div v-for="s in r.subtasks" :key="s.id" class="subtask-row" :class="{ 'row-inactive': !s.is_active }">
            <span class="subtask-name">{{ s.name }}</span>
            <span class="badge">{{ s.billing_mode === 'HORAIRE' ? 'Horaire' : 'Forfait' }}</span>
            <span class="task-actions">
              <button class="btn-icon" @click="openEdit(s)">Modifier</button>
              <template v-if="confirmDeleteId === s.id">
                <button class="btn-icon btn-icon-danger" @click="deleteTask(s.id)">Confirmer</button>
                <button class="btn-icon" @click="confirmDeleteId = null">Annuler</button>
              </template>
              <button v-else class="btn-icon btn-icon-danger" @click="confirmDeleteId = s.id">Supprimer</button>
            </span>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showForm" class="modal-overlay" @click.self="showForm = false">
      <div class="modal">
        <div class="modal-header">
          <h2>{{ formTitle }}</h2>
          <button class="modal-close" @click="showForm = false">&times;</button>
        </div>
        <div class="modal-body">
          <div v-if="saveError" class="alert-error" style="margin-bottom:10px;">{{ saveError }}</div>
          <form @submit.prevent="save">
            <div class="form-group">
              <label>Nom *</label>
              <input v-model="form.name" type="text" required placeholder="Ex: Plans préliminaires" />
            </div>
            <div class="form-group">
              <label>Libellé client</label>
              <input v-model="form.client_facing_label" type="text" />
            </div>
            <div class="form-row">
              <div class="form-group">
                <label>Mode</label>
                <select v-model="form.billing_mode">
                  <option value="FORFAIT">Forfait</option>
                  <option value="HORAIRE">Horaire</option>
                </select>
              </div>
              <div class="form-group">
                <label>Ordre</label>
                <input v-model.number="form.order" type="number" min="0" />
              </div>
            </div>
            <label class="checkbox-label">
              <input type="checkbox" v-model="form.is_active" />
              Active (proposée au démarrage d'un projet)
            </label>
            <div class="form-actions">
              <button type="button" class="btn-ghost" @click="showForm = false">Annuler</button>
              <button type="submit" class="btn-primary">{{ editingId ? 'Enregistrer' : 'Créer' }}</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-header { display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 16px; }
.page-header h1 { font-size: 20px; font-weight: 700; color: var(--color-gray-900); margin-top: 2px; }
.btn-back { background: none; border: none; font-size: 12px; color: var(--color-gray-500); cursor: pointer; padding: 0; }
.btn-back:hover { color: var(--color-primary); }
.hint { font-size: 12px; color: var(--color-gray-600); margin: 0 0 14px; max-width: 80ch; }
.loading { text-align: center; padding: 40px; color: var(--color-gray-500); font-size: 13px; }

.groups { display: flex; flex-direction: column; gap: 12px; }
.phase-card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); overflow: hidden; }
.phase-head { display: flex; align-items: center; gap: 10px; padding: 10px 14px; background: var(--color-gray-50); border-bottom: 1px solid var(--color-gray-200); }
.phase-code { font-family: var(--font-mono); font-size: 12px; font-weight: 700; color: var(--color-primary); }
.phase-name { font-weight: 700; color: var(--color-gray-800); font-size: 14px; }
.phase-count { font-size: 11px; color: var(--color-gray-400); }
.phase-head .btn-primary { margin-left: auto; }
.phase-empty { padding: 10px 14px; font-size: 12px; color: var(--color-gray-400); }

.task-block { border-bottom: 1px solid var(--color-gray-100); }
.task-row { display: flex; align-items: center; gap: 8px; padding: 8px 14px; }
.subtask-row { display: flex; align-items: center; gap: 8px; padding: 5px 14px 5px 38px; background: #FCFCFD; }
.task-name { font-weight: 600; color: var(--color-gray-800); font-size: 13px; }
.subtask-name { color: var(--color-gray-600); font-size: 12px; }
.row-inactive { opacity: 0.55; }
.badge { font-size: 9px; font-weight: 600; color: var(--color-gray-500); background: var(--color-gray-100); border-radius: 4px; padding: 1px 6px; }
.badge-off { color: #B45309; background: #FEF3C7; }
.task-actions { margin-left: auto; white-space: nowrap; }

.btn-primary { padding: 5px 11px; border-radius: 4px; font-size: 12px; font-weight: 600; cursor: pointer; border: none; background: var(--color-primary); color: white; }
.btn-sm { padding: 4px 9px; font-size: 11px; }
.btn-ghost { padding: 6px 12px; border-radius: 4px; font-size: 12px; cursor: pointer; background: transparent; color: var(--color-gray-600); border: 1px solid var(--color-gray-300); }
.btn-icon { background: none; border: none; font-size: 11px; cursor: pointer; color: var(--color-primary); padding: 2px 6px; }
.btn-icon:hover { text-decoration: underline; }
.btn-icon-danger { color: var(--color-danger); }

.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.3); z-index: 8000; display: flex; align-items: flex-start; justify-content: center; padding-top: 80px; }
.modal { background: white; border-radius: 8px; box-shadow: 0 10px 15px rgba(0,0,0,0.1); width: 100%; max-width: 480px; }
.modal-header { padding: 14px 20px; border-bottom: 1px solid var(--color-gray-200); display: flex; align-items: center; justify-content: space-between; }
.modal-header h2 { font-size: 15px; font-weight: 600; color: var(--color-gray-800); }
.modal-close { background: none; border: none; font-size: 22px; cursor: pointer; color: var(--color-gray-400); }
.modal-body { padding: 20px; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.form-group { margin-bottom: 14px; }
.form-group label { display: block; font-size: 11px; font-weight: 600; color: var(--color-gray-600); margin-bottom: 4px; }
.form-group input, .form-group select { width: 100%; padding: 6px 10px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 13px; }
.checkbox-label { display: flex; align-items: center; gap: 6px; font-size: 13px; color: var(--color-gray-700); cursor: pointer; }
.form-actions { display: flex; justify-content: flex-end; gap: 6px; margin-top: 16px; padding-top: 12px; border-top: 1px solid var(--color-gray-200); }
.alert-error { background: #fde8e4; color: var(--color-danger); padding: 8px 12px; border-radius: 6px; font-size: 12px; }
.empty { text-align: center; padding: 30px; color: var(--color-gray-400); font-size: 13px; }
.card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }
</style>
