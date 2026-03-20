<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/plugins/axios'

const router = useRouter()

interface ExpenseCategory {
  id: number
  name: string
  // code field removed — not in backend model
  is_refacturable_default: boolean
  requires_receipt: boolean
  gl_account: string
  is_active: boolean
}

const categories = ref<ExpenseCategory[]>([])
const isLoading = ref(true)
const showForm = ref(false)
const editingId = ref<number | null>(null)

const form = ref({
  name: '',
  is_refacturable_default: false,
  requires_receipt: true,
  gl_account: '',
})

async function fetchCategories() {
  isLoading.value = true
  try {
    const resp = await apiClient.get('expense_categories/')
    const data = resp.data?.data || resp.data
    categories.value = Array.isArray(data) ? data : data?.results || []
  } catch {
    categories.value = []
  } finally {
    isLoading.value = false
  }
}

function openCreate() {
  editingId.value = null
  form.value = { name: '', is_refacturable_default: false, requires_receipt: true, gl_account: '' }
  showForm.value = true
}

function openEdit(cat: ExpenseCategory) {
  editingId.value = cat.id
  form.value = {
    name: cat.name,
    is_refacturable_default: cat.is_refacturable_default,
    requires_receipt: cat.requires_receipt,
    gl_account: cat.gl_account,
  }
  showForm.value = true
}

const saveError = ref('')

async function save() {
  saveError.value = ''
  if (!form.value.name.trim()) { saveError.value = 'Le nom est obligatoire.'; return }
  try {
    const payload = {
      name: form.value.name,
      is_refacturable_default: form.value.is_refacturable_default,
      requires_receipt: form.value.requires_receipt,
      gl_account: form.value.gl_account,
    }
    if (editingId.value) {
      await apiClient.patch(`expense_categories/${editingId.value}/`, payload)
    } else {
      await apiClient.post('expense_categories/', payload)
    }
    editingId.value = null
    showForm.value = false
    await fetchCategories()
  } catch (e: unknown) {
    const err = e as { response?: { data?: { error?: { message?: string; details?: Array<{ message?: string }> } } } }
    saveError.value = err.response?.data?.error?.details?.[0]?.message || err.response?.data?.error?.message || 'Erreur'
  }
}

const confirmDeleteCat = ref<number | null>(null)

async function deleteCategory(id: number) {
  confirmDeleteCat.value = null
  categories.value = categories.value.filter(c => c.id !== id)
  try { await apiClient.delete(`expense_categories/${id}/`) } catch { /* ok */ }
}

onMounted(fetchCategories)
</script>

<template>
  <div>
    <div class="page-header">
      <div>
        <button class="btn-back" @click="router.push('/admin')">&larr; Administration</button>
        <h1>Catégories & Listes</h1>
      </div>
    </div>

    <!-- Sub-navigation -->
    <div class="sub-nav">
      <button class="sub-nav-btn active">Catégories de dépenses</button>
      <button class="sub-nav-btn" @click="router.push('/admin/templates')">Templates de projet</button>
    </div>

    <!-- Actions -->
    <div class="actions-bar">
      <span class="count">{{ categories.length }} catégories</span>
      <button class="btn-primary" @click="openCreate">+ Nouvelle catégorie</button>
    </div>

    <div v-if="isLoading" class="loading">Chargement...</div>

    <!-- Table -->
    <div v-else class="card">
      <table v-if="categories.length">
        <thead>
          <tr>
            <!-- code column removed -->
            <th>Nom</th>
            <th>Compte GL</th>
            <th>Refacturable</th>
            <th>Reçu requis</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="cat in categories" :key="cat.id">
            <!-- code removed -->
            <td class="name-cell">{{ cat.name }}</td>
            <td class="mono">{{ cat.gl_account || '—' }}</td>
            <td>
              <span :class="cat.is_refacturable_default ? 'flag-yes' : 'flag-no'">
                {{ cat.is_refacturable_default ? 'Oui' : 'Non' }}
              </span>
            </td>
            <td>
              <span :class="cat.requires_receipt ? 'flag-yes' : 'flag-no'">
                {{ cat.requires_receipt ? 'Oui' : 'Non' }}
              </span>
            </td>
            <td class="actions-cell">
              <button class="btn-icon" @click="openEdit(cat)">Modifier</button>
              <template v-if="confirmDeleteCat === cat.id">
                <button class="btn-icon btn-icon-danger" @click="deleteCategory(cat.id)">Confirmer</button>
                <button class="btn-icon" @click="confirmDeleteCat = null">Annuler</button>
              </template>
              <button v-else class="btn-icon btn-icon-danger" @click="confirmDeleteCat = cat.id">Supprimer</button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="empty">Aucune catégorie de dépenses.</div>
    </div>

    <!-- Inline form -->
    <div v-if="showForm" class="modal-overlay" @click.self="showForm = false">
      <div class="modal">
        <div class="modal-header">
          <h2>{{ editingId ? 'Modifier' : 'Nouvelle' }} catégorie</h2>
          <button class="modal-close" @click="showForm = false">&times;</button>
        </div>
        <div class="modal-body">
          <div v-if="saveError" class="alert-error" style="margin-bottom:10px;">{{ saveError }}</div>
          <form @submit.prevent="save">
            <div class="form-row">
              <div class="form-group">
                <label>Code</label>
                <!-- code field removed -->
              </div>
              <div class="form-group">
                <label>Nom</label>
                <input v-model="form.name" type="text" required placeholder="Ex: Transport" />
              </div>
            </div>
            <div class="form-group">
              <label>Compte GL (Intact)</label>
              <input v-model="form.gl_account" type="text" placeholder="Ex: 5400-001" />
            </div>
            <div class="form-row">
              <label class="checkbox-label">
                <input type="checkbox" v-model="form.is_refacturable_default" />
                Refacturable par défaut
              </label>
              <label class="checkbox-label">
                <input type="checkbox" v-model="form.requires_receipt" />
                Reçu requis
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

.sub-nav { display: flex; gap: 0; border-bottom: 2px solid var(--color-gray-200); margin-bottom: 16px; }
.sub-nav-btn { padding: 8px 16px; font-size: 13px; font-weight: 500; color: var(--color-gray-500); cursor: pointer; border: none; background: none; border-bottom: 2px solid transparent; margin-bottom: -2px; }
.sub-nav-btn.active { color: var(--color-primary); border-bottom-color: var(--color-primary); font-weight: 600; }
.sub-nav-btn:hover:not(.active) { color: var(--color-gray-700); }

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
.form-group input { width: 100%; padding: 6px 10px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 13px; }
.checkbox-label { display: flex; align-items: center; gap: 6px; font-size: 13px; color: var(--color-gray-700); cursor: pointer; }
.form-actions { display: flex; justify-content: flex-end; gap: 6px; margin-top: 16px; padding-top: 12px; border-top: 1px solid var(--color-gray-200); }
.empty { text-align: center; padding: 30px; color: var(--color-gray-400); font-size: 13px; }
</style>
