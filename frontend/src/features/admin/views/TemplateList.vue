<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/plugins/axios'

const router = useRouter()

interface ProjectTemplate {
  id: number
  name: string
  code: string
  contract_type: string
  description: string
  is_active: boolean
  phases_config: Array<{ name: string; client_label: string; type: string; billing_mode: string; is_mandatory?: boolean }>
  support_services_config: Array<{ name: string; client_label: string }>
  projects_count: number
}

const templates = ref<ProjectTemplate[]>([])
const isLoading = ref(true)
const showForm = ref(false)
const editingTemplate = ref<ProjectTemplate | null>(null)
const deleteError = ref<string | null>(null)
const showDeleteConfirm = ref<number | null>(null)

// Form fields
const form = ref({
  name: '',
  code: '',
  contract_type: 'FORFAITAIRE',
  description: '',
  phases_config: [] as ProjectTemplate['phases_config'],
  support_services_config: [] as ProjectTemplate['support_services_config'],
})

const contractTypes = [
  { value: 'FORFAITAIRE', label: 'Forfaitaire' },
  { value: 'CONSORTIUM', label: 'Consortium' },
  { value: 'CO_DEV', label: 'Co-développement' },
  { value: 'CONCEPTION_CONSTRUCTION', label: 'Conception-construction' },
]

const phaseTypes = [
  { value: 'REALIZATION', label: 'Réalisation' },
  { value: 'SUPPORT', label: 'Support' },
]

const billingModes = [
  { value: 'FORFAIT', label: 'Forfait' },
  { value: 'HORAIRE', label: 'Horaire' },
]

const isEditing = computed(() => editingTemplate.value !== null)
const formTitle = computed(() => isEditing.value ? 'Modifier le template' : 'Nouveau template')

async function fetchTemplates() {
  isLoading.value = true
  try {
    const resp = await apiClient.get('project_templates/')
    const data = resp.data?.data || resp.data
    templates.value = Array.isArray(data) ? data : data?.results || []
  } catch {
    templates.value = []
  } finally {
    isLoading.value = false
  }
}

function openCreate() {
  editingTemplate.value = null
  form.value = {
    name: '',
    code: '',
    contract_type: 'FORFAITAIRE',
    description: '',
    phases_config: [],
    support_services_config: [],
  }
  showForm.value = true
}

function openEdit(tmpl: ProjectTemplate) {
  editingTemplate.value = tmpl
  form.value = {
    name: tmpl.name,
    code: tmpl.code,
    contract_type: tmpl.contract_type,
    description: tmpl.description,
    phases_config: JSON.parse(JSON.stringify(tmpl.phases_config)),
    support_services_config: JSON.parse(JSON.stringify(tmpl.support_services_config)),
  }
  showForm.value = true
}

function closeForm() {
  showForm.value = false
  editingTemplate.value = null
}

function addPhase() {
  form.value.phases_config.push({
    name: '',
    client_label: '',
    type: 'REALIZATION',
    billing_mode: 'FORFAIT',
    is_mandatory: false,
  })
}

function removePhase(index: number) {
  form.value.phases_config.splice(index, 1)
}

function addService() {
  form.value.support_services_config.push({ name: '', client_label: '' })
}

function removeService(index: number) {
  form.value.support_services_config.splice(index, 1)
}

const saveError = ref('')

async function saveTemplate() {
  saveError.value = ''
  if (!form.value.name.trim()) { saveError.value = 'Le nom est obligatoire.'; return }
  try {
    if (isEditing.value && editingTemplate.value) {
      await apiClient.put(`project_templates/${editingTemplate.value.id}/`, form.value)
    } else {
      await apiClient.post('project_templates/', form.value)
    }
    closeForm()
    await fetchTemplates()
  } catch (e: unknown) {
    const err = e as { response?: { data?: { error?: { message?: string; details?: Array<{ message?: string }> } } } }
    saveError.value = err.response?.data?.error?.details?.[0]?.message || err.response?.data?.error?.message || 'Erreur lors de la sauvegarde'
  }
}

async function deleteTemplate(id: number) {
  deleteError.value = null
  try {
    await apiClient.delete(`project_templates/${id}/`)
    showDeleteConfirm.value = null
    await fetchTemplates()
  } catch (err: unknown) {
    const axiosErr = err as { response?: { data?: { error?: { message?: string } } } }
    deleteError.value = axiosErr.response?.data?.error?.message || 'Erreur lors de la suppression'
    showDeleteConfirm.value = null
  }
}

onMounted(fetchTemplates)
</script>

<template>
  <div>
    <!-- Header -->
    <div class="page-header">
      <div>
        <button class="btn-ghost btn-sm" @click="router.push('/admin')">
          &larr; Administration
        </button>
        <h1>Templates de projet</h1>
      </div>
      <button class="btn-primary" @click="openCreate">
        + Nouveau template
      </button>
    </div>

    <!-- Error -->
    <div v-if="deleteError" class="alert-error">
      {{ deleteError }}
      <button @click="deleteError = null" class="alert-close">&times;</button>
    </div>

    <!-- Loading -->
    <div v-if="isLoading" class="loading">Chargement...</div>

    <!-- Template list -->
    <div v-else class="template-grid">
      <div v-for="tmpl in templates" :key="tmpl.id" class="template-card">
        <div class="template-card-header">
          <div>
            <span class="template-code">{{ tmpl.code }}</span>
            <h3 class="template-name">{{ tmpl.name }}</h3>
          </div>
          <span class="badge" :class="'badge-' + tmpl.contract_type.toLowerCase()">
            {{ contractTypes.find(c => c.value === tmpl.contract_type)?.label }}
          </span>
        </div>

        <p v-if="tmpl.description" class="template-desc">{{ tmpl.description }}</p>

        <!-- Phases -->
        <div class="template-section">
          <span class="template-section-label">Phases ({{ tmpl.phases_config.length }})</span>
          <div class="template-phases">
            <span
              v-for="(phase, i) in tmpl.phases_config"
              :key="i"
              class="phase-tag"
              :class="{ 'phase-support': phase.type === 'SUPPORT' }"
            >
              {{ phase.name }}
              <span class="phase-mode">{{ phase.billing_mode === 'HORAIRE' ? 'H' : 'F' }}</span>
            </span>
          </div>
        </div>

        <!-- Services -->
        <div v-if="tmpl.support_services_config.length" class="template-section">
          <span class="template-section-label">Services ({{ tmpl.support_services_config.length }})</span>
          <div class="template-phases">
            <span v-for="(svc, i) in tmpl.support_services_config" :key="i" class="phase-tag phase-service">
              {{ svc.name }}
            </span>
          </div>
        </div>

        <!-- Footer -->
        <div class="template-footer">
          <span class="template-usage">
            {{ tmpl.projects_count }} projet{{ tmpl.projects_count !== 1 ? 's' : '' }}
          </span>
          <div class="template-actions">
            <button class="btn-ghost btn-sm" @click="openEdit(tmpl)">Modifier</button>
            <template v-if="showDeleteConfirm === tmpl.id">
              <button class="btn-danger btn-sm" @click="deleteTemplate(tmpl.id)">Confirmer</button>
              <button class="btn-ghost btn-sm" @click="showDeleteConfirm = null">Annuler</button>
            </template>
            <button
              v-else
              class="btn-ghost btn-sm btn-delete"
              :disabled="tmpl.projects_count > 0"
              :title="tmpl.projects_count > 0 ? 'Utilisé par des projets' : 'Supprimer'"
              @click="showDeleteConfirm = tmpl.id"
            >
              Supprimer
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty state -->
    <div v-if="!isLoading && templates.length === 0" class="empty-state">
      <p>Aucun template de projet.</p>
      <button class="btn-primary" @click="openCreate">Créer le premier template</button>
    </div>

    <!-- Form modal -->
    <div v-if="showForm" class="modal-overlay" @click.self="closeForm">
      <div class="modal">
        <div class="modal-header">
          <h2>{{ formTitle }}</h2>
          <button class="modal-close" @click="closeForm">&times;</button>
        </div>

        <div class="modal-body">
          <div v-if="saveError" class="alert-error" style="margin-bottom:12px;">{{ saveError }}</div>
          <form @submit.prevent="saveTemplate">
            <!-- Basic info -->
            <div class="form-row">
              <div class="form-group">
                <label>Nom</label>
                <input v-model="form.name" type="text" required placeholder="Ex: Forfaitaire — Standard" />
              </div>
              <div class="form-group">
                <label>Code</label>
                <input v-model="form.code" type="text" placeholder="Ex: TPL-FORFAIT" />
              </div>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>Type de contrat</label>
                <select v-model="form.contract_type">
                  <option v-for="ct in contractTypes" :key="ct.value" :value="ct.value">{{ ct.label }}</option>
                </select>
              </div>
              <div class="form-group">
                <label>Description</label>
                <input v-model="form.description" type="text" placeholder="Description optionnelle" />
              </div>
            </div>

            <!-- Phases -->
            <div class="section-divider">Phases</div>
            <div v-for="(phase, i) in form.phases_config" :key="i" class="phase-row">
              <input v-model="phase.name" placeholder="Nom interne" class="phase-input" />
              <input v-model="phase.client_label" placeholder="Libellé client" class="phase-input" />
              <select v-model="phase.type" class="phase-select">
                <option v-for="pt in phaseTypes" :key="pt.value" :value="pt.value">{{ pt.label }}</option>
              </select>
              <select v-model="phase.billing_mode" class="phase-select-sm">
                <option v-for="bm in billingModes" :key="bm.value" :value="bm.value">{{ bm.label }}</option>
              </select>
              <label class="phase-checkbox">
                <input type="checkbox" v-model="phase.is_mandatory" />
                Oblig.
              </label>
              <button type="button" class="btn-icon-delete" @click="removePhase(i)">&times;</button>
            </div>
            <button type="button" class="btn-ghost btn-sm" @click="addPhase">+ Ajouter une phase</button>

            <!-- Support services -->
            <div class="section-divider">Services de support</div>
            <div v-for="(svc, i) in form.support_services_config" :key="i" class="phase-row">
              <input v-model="svc.name" placeholder="Nom interne" class="phase-input" />
              <input v-model="svc.client_label" placeholder="Libellé client" class="phase-input flex-1" />
              <button type="button" class="btn-icon-delete" @click="removeService(i)">&times;</button>
            </div>
            <button type="button" class="btn-ghost btn-sm" @click="addService">+ Ajouter un service</button>

            <!-- Actions -->
            <div class="form-actions">
              <button type="button" class="btn-ghost" @click="closeForm">Annuler</button>
              <button type="submit" class="btn-primary">{{ isEditing ? 'Enregistrer' : 'Créer' }}</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-header { display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 20px; }
.page-header h1 { font-size: 24px; font-weight: 700; color: var(--color-gray-900); margin-top: 4px; }
.loading { text-align: center; padding: 40px; color: var(--color-gray-500); }

.template-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
.template-card {
  background: white; border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1), 0 1px 2px rgba(0,0,0,0.06);
  padding: 20px; display: flex; flex-direction: column; gap: 12px;
}
.template-card-header { display: flex; align-items: flex-start; justify-content: space-between; }
.template-code { font-size: 11px; font-weight: 600; color: var(--color-gray-400); text-transform: uppercase; letter-spacing: 0.3px; }
.template-name { font-size: 16px; font-weight: 600; color: var(--color-gray-800); margin-top: 2px; }
.template-desc { font-size: 13px; color: var(--color-gray-500); }

.badge { display: inline-flex; padding: 2px 10px; border-radius: 12px; font-size: 11px; font-weight: 600; }
.badge-forfaitaire { background: #DBEAFE; color: #1D4ED8; }
.badge-consortium { background: #EDE9FE; color: #7C3AED; }
.badge-co_dev { background: #FEF3C7; color: #92400E; }
.badge-conception_construction { background: #DCFCE7; color: #15803D; }

.template-section { }
.template-section-label { font-size: 11px; font-weight: 600; color: var(--color-gray-400); text-transform: uppercase; letter-spacing: 0.3px; display: block; margin-bottom: 6px; }
.template-phases { display: flex; flex-wrap: wrap; gap: 4px; }
.phase-tag {
  font-size: 12px; padding: 3px 10px; border-radius: 4px;
  background: var(--color-gray-100); color: var(--color-gray-600);
  display: inline-flex; align-items: center; gap: 4px;
}
.phase-tag.phase-support { background: #FEF3C7; color: #92400E; }
.phase-tag.phase-service { background: #EDE9FE; color: #7C3AED; }
.phase-mode { font-size: 10px; font-weight: 700; opacity: 0.6; }

.template-footer {
  display: flex; align-items: center; justify-content: space-between;
  padding-top: 12px; border-top: 1px solid var(--color-gray-100);
  margin-top: auto;
}
.template-usage { font-size: 12px; color: var(--color-gray-400); }
.template-actions { display: flex; gap: 6px; }

.btn-primary { padding: 6px 12px; border-radius: 4px; font-size: 12px; font-weight: 600; cursor: pointer; border: none; background: var(--color-primary); color: white; transition: all 0.15s; }
.btn-primary:hover { background: var(--color-primary-dark); }
.btn-ghost { padding: 6px 12px; border-radius: 4px; font-size: 12px; font-weight: 500; cursor: pointer; background: transparent; color: var(--color-gray-600); border: 1px solid var(--color-gray-300); transition: all 0.15s; }
.btn-ghost:hover { background: var(--color-gray-100); }
.btn-danger { padding: 6px 12px; border-radius: 4px; font-size: 12px; font-weight: 600; cursor: pointer; border: none; background: var(--color-danger); color: white; }
.btn-sm { padding: 4px 9px; font-size: 11px; }
.btn-delete { color: var(--color-danger); border-color: var(--color-danger); }
.btn-delete:disabled { opacity: 0.3; cursor: not-allowed; }
.btn-delete:hover:not(:disabled) { background: var(--color-danger-light); }

.alert-error { background: var(--color-danger-light); color: var(--color-danger); padding: 12px 16px; border-radius: 8px; margin-bottom: 16px; display: flex; align-items: center; justify-content: space-between; font-size: 13px; }
.alert-close { background: none; border: none; font-size: 18px; cursor: pointer; color: var(--color-danger); }

.empty-state { text-align: center; padding: 60px; color: var(--color-gray-500); }
.empty-state p { margin-bottom: 16px; }

/* Modal */
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.3); z-index: 8000; display: flex; align-items: flex-start; justify-content: center; padding-top: 60px; }
.modal { background: white; border-radius: 8px; box-shadow: 0 10px 15px rgba(0,0,0,0.1); width: 100%; max-width: 720px; max-height: calc(100vh - 120px); display: flex; flex-direction: column; }
.modal-header { padding: 16px 24px; border-bottom: 1px solid var(--color-gray-200); display: flex; align-items: center; justify-content: space-between; }
.modal-header h2 { font-size: 18px; font-weight: 600; color: var(--color-gray-800); }
.modal-close { background: none; border: none; font-size: 24px; cursor: pointer; color: var(--color-gray-400); padding: 4px 8px; }
.modal-close:hover { color: var(--color-gray-800); }
.modal-body { flex: 1; overflow-y: auto; padding: 24px; }

.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.form-group { margin-bottom: 16px; }
.form-group label { display: block; font-size: 13px; font-weight: 600; color: var(--color-gray-700); margin-bottom: 6px; }
.form-group input, .form-group select { width: 100%; padding: 8px 12px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 14px; font-family: inherit; }
.form-group input:focus, .form-group select:focus { outline: none; border-color: var(--color-primary); box-shadow: 0 0 0 3px rgba(37,99,235,0.1); }

.section-divider { font-size: 12px; font-weight: 600; color: var(--color-gray-500); text-transform: uppercase; letter-spacing: 0.5px; margin: 20px 0 12px; padding-bottom: 6px; border-bottom: 1px solid var(--color-gray-200); }

.phase-row { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }
.phase-input { flex: 1; padding: 7px 10px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 13px; }
.phase-input:focus { outline: none; border-color: var(--color-primary); }
.phase-select { width: 120px; padding: 7px 8px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 13px; }
.phase-select-sm { width: 90px; padding: 7px 8px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 13px; }
.phase-checkbox { display: flex; align-items: center; gap: 4px; font-size: 12px; color: var(--color-gray-600); white-space: nowrap; }
.btn-icon-delete { background: none; border: none; font-size: 18px; cursor: pointer; color: var(--color-gray-400); padding: 4px 8px; border-radius: 4px; }
.btn-icon-delete:hover { background: var(--color-danger-light); color: var(--color-danger); }

.form-actions { display: flex; justify-content: flex-end; gap: 8px; margin-top: 24px; padding-top: 16px; border-top: 1px solid var(--color-gray-200); }
</style>
