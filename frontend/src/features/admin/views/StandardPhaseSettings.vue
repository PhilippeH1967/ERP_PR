<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/plugins/axios'

const router = useRouter()

interface StandardPhase {
  id: number
  code: string
  name: string
  client_facing_label: string
  phase_type: 'REALIZATION' | 'SUPPORT'
  order: number
  is_mandatory: boolean
  is_active: boolean
}

const phases = ref<StandardPhase[]>([])
const isLoading = ref(true)
const showForm = ref(false)
const editingId = ref<number | null>(null)

const emptyForm = () => ({
  code: '',
  name: '',
  client_facing_label: '',
  phase_type: 'REALIZATION' as 'REALIZATION' | 'SUPPORT',
  order: 0,
  is_mandatory: false,
  is_active: true,
})
const form = ref(emptyForm())

async function fetchPhases() {
  isLoading.value = true
  try {
    const resp = await apiClient.get('standard_phases/')
    const data = resp.data?.data || resp.data
    phases.value = Array.isArray(data) ? data : data?.results || []
  } catch {
    phases.value = []
  } finally {
    isLoading.value = false
  }
}

function openCreate() {
  editingId.value = null
  const nextOrder = phases.value.reduce((m, p) => Math.max(m, p.order), -1) + 1
  form.value = { ...emptyForm(), order: nextOrder }
  showForm.value = true
}

function openEdit(p: StandardPhase) {
  editingId.value = p.id
  form.value = {
    code: p.code,
    name: p.name,
    client_facing_label: p.client_facing_label,
    phase_type: p.phase_type,
    order: p.order,
    is_mandatory: p.is_mandatory,
    is_active: p.is_active,
  }
  showForm.value = true
}

const saveError = ref('')

async function save() {
  saveError.value = ''
  if (!form.value.code.trim()) { saveError.value = 'Le code est obligatoire.'; return }
  if (!form.value.name.trim()) { saveError.value = 'Le nom est obligatoire.'; return }
  try {
    const payload = { ...form.value }
    if (editingId.value) {
      await apiClient.patch(`standard_phases/${editingId.value}/`, payload)
    } else {
      await apiClient.post('standard_phases/', payload)
    }
    editingId.value = null
    showForm.value = false
    await fetchPhases()
  } catch (e: unknown) {
    const err = e as { response?: { data?: { error?: { message?: string; details?: Array<{ message?: string }> } } } }
    saveError.value = err.response?.data?.error?.details?.[0]?.message || err.response?.data?.error?.message || 'Erreur'
  }
}

const confirmDeleteId = ref<number | null>(null)

async function deletePhase(id: number) {
  confirmDeleteId.value = null
  phases.value = phases.value.filter(p => p.id !== id)
  try { await apiClient.delete(`standard_phases/${id}/`) } catch { /* ok */ }
}

onMounted(fetchPhases)
</script>

<template>
  <div>
    <div class="page-header">
      <div>
        <button class="btn-back" @click="router.push('/admin')">&larr; Administration</button>
        <h1>Phases standard</h1>
      </div>
    </div>

    <p class="hint">
      Jeu de phases <strong>standard du cabinet</strong>. Tout nouveau projet hérite de ces phases.
      Sur un projet, les PM ne peuvent pas les modifier — c'est ici que ça se paramètre.
    </p>

    <div class="actions-bar">
      <span class="count">{{ phases.length }} phase{{ phases.length > 1 ? 's' : '' }}</span>
      <button class="btn-primary" @click="openCreate">+ Nouvelle phase</button>
    </div>

    <div v-if="isLoading" class="loading">Chargement...</div>

    <div v-else class="card">
      <table v-if="phases.length">
        <thead>
          <tr>
            <th style="width:60px;">Ordre</th>
            <th style="width:70px;">Code</th>
            <th>Nom interne</th>
            <th>Libellé client</th>
            <th>Type</th>
            <th>Obligatoire</th>
            <th>Active</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in phases" :key="p.id" :class="{ 'row-inactive': !p.is_active }">
            <td class="mono">{{ p.order }}</td>
            <td class="code-cell">{{ p.code }}</td>
            <td class="name-cell">{{ p.name }}</td>
            <td>{{ p.client_facing_label || '—' }}</td>
            <td>{{ p.phase_type === 'SUPPORT' ? 'Soutien' : 'Réalisation' }}</td>
            <td><span :class="p.is_mandatory ? 'flag-yes' : 'flag-no'">{{ p.is_mandatory ? 'Oui' : 'Non' }}</span></td>
            <td><span :class="p.is_active ? 'flag-yes' : 'flag-no'">{{ p.is_active ? 'Oui' : 'Non' }}</span></td>
            <td class="actions-cell">
              <button class="btn-icon" @click="openEdit(p)">Modifier</button>
              <template v-if="confirmDeleteId === p.id">
                <button class="btn-icon btn-icon-danger" @click="deletePhase(p.id)">Confirmer</button>
                <button class="btn-icon" @click="confirmDeleteId = null">Annuler</button>
              </template>
              <button v-else class="btn-icon btn-icon-danger" @click="confirmDeleteId = p.id">Supprimer</button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="empty">Aucune phase standard. Cliquez « + Nouvelle phase » pour démarrer.</div>
    </div>

    <div v-if="showForm" class="modal-overlay" @click.self="showForm = false">
      <div class="modal">
        <div class="modal-header">
          <h2>{{ editingId ? 'Modifier' : 'Nouvelle' }} phase standard</h2>
          <button class="modal-close" @click="showForm = false">&times;</button>
        </div>
        <div class="modal-body">
          <div v-if="saveError" class="alert-error" style="margin-bottom:10px;">{{ saveError }}</div>
          <form @submit.prevent="save">
            <div class="form-row">
              <div class="form-group">
                <label>Code *</label>
                <input v-model="form.code" type="text" required placeholder="Ex: 1, G, Q" />
              </div>
              <div class="form-group">
                <label>Ordre</label>
                <input v-model.number="form.order" type="number" min="0" />
              </div>
            </div>
            <div class="form-group">
              <label>Nom interne *</label>
              <input v-model="form.name" type="text" required placeholder="Ex: Concept" />
            </div>
            <div class="form-group">
              <label>Libellé client</label>
              <input v-model="form.client_facing_label" type="text" placeholder="Ex: Phase 1 — Concept" />
            </div>
            <div class="form-group">
              <label>Type</label>
              <select v-model="form.phase_type">
                <option value="REALIZATION">Réalisation</option>
                <option value="SUPPORT">Soutien</option>
              </select>
            </div>
            <div class="form-row">
              <label class="checkbox-label">
                <input type="checkbox" v-model="form.is_mandatory" />
                Obligatoire sur chaque projet
              </label>
              <label class="checkbox-label">
                <input type="checkbox" v-model="form.is_active" />
                Active (instanciée sur les nouveaux projets)
              </label>
            </div>
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
.hint { font-size: 12px; color: var(--color-gray-600); margin: 0 0 14px; }

.actions-bar { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
.count { font-size: 12px; color: var(--color-gray-500); }

.btn-primary { padding: 6px 12px; border-radius: 4px; font-size: 12px; font-weight: 600; cursor: pointer; border: none; background: var(--color-primary); color: white; }
.btn-primary:hover { background: var(--color-primary-dark); }
.btn-ghost { padding: 6px 12px; border-radius: 4px; font-size: 12px; font-weight: 500; cursor: pointer; background: transparent; color: var(--color-gray-600); border: 1px solid var(--color-gray-300); }
.loading { text-align: center; padding: 40px; color: var(--color-gray-500); font-size: 13px; }

.card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 0; overflow: hidden; }
table { width: 100%; border-collapse: collapse; }
th { background: var(--color-gray-50); padding: 7px 10px; text-align: left; font-size: 10px; font-weight: 600; color: var(--color-gray-500); text-transform: uppercase; letter-spacing: 0.3px; border-bottom: 2px solid var(--color-gray-200); }
td { padding: 8px 10px; border-bottom: 1px solid var(--color-gray-100); font-size: 13px; }
tr:hover { background: var(--color-gray-50); }
.row-inactive td { opacity: 0.55; }
.code-cell { font-family: var(--font-mono); font-size: 12px; color: var(--color-gray-600); }
.name-cell { font-weight: 600; color: var(--color-gray-800); }
.mono { font-family: var(--font-mono); font-size: 12px; }
.flag-yes { font-size: 11px; font-weight: 600; color: #15803D; }
.flag-no { font-size: 11px; color: var(--color-gray-400); }
.actions-cell { text-align: right; white-space: nowrap; }
.btn-icon { background: none; border: none; font-size: 11px; cursor: pointer; color: var(--color-primary); padding: 2px 6px; }
.btn-icon:hover { text-decoration: underline; }
.btn-icon-danger { color: var(--color-danger); }

.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.3); z-index: 8000; display: flex; align-items: flex-start; justify-content: center; padding-top: 80px; }
.modal { background: white; border-radius: 8px; box-shadow: 0 10px 15px rgba(0,0,0,0.1); width: 100%; max-width: 500px; }
.modal-header { padding: 14px 20px; border-bottom: 1px solid var(--color-gray-200); display: flex; align-items: center; justify-content: space-between; }
.modal-header h2 { font-size: 16px; font-weight: 600; color: var(--color-gray-800); }
.modal-close { background: none; border: none; font-size: 22px; cursor: pointer; color: var(--color-gray-400); }
.modal-body { padding: 20px; }

.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.form-group { margin-bottom: 14px; }
.form-group label { display: block; font-size: 11px; font-weight: 600; color: var(--color-gray-600); margin-bottom: 4px; }
.form-group input, .form-group select { width: 100%; padding: 6px 10px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 13px; }
.checkbox-label { display: flex; align-items: center; gap: 6px; font-size: 13px; color: var(--color-gray-700); cursor: pointer; }
.form-actions { display: flex; justify-content: flex-end; gap: 6px; margin-top: 16px; padding-top: 12px; border-top: 1px solid var(--color-gray-200); }
.empty { text-align: center; padding: 30px; color: var(--color-gray-400); font-size: 13px; }
.alert-error { background: #fde8e4; color: var(--color-danger); padding: 8px 12px; border-radius: 6px; font-size: 12px; }
</style>
