<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useLocale } from '@/shared/composables/useLocale'
import { useBillingStore } from '../stores/useBillingStore'
import { billingApi } from '../api/billingApi'
import apiClient from '@/plugins/axios'

const store = useBillingStore()
const router = useRouter()
const { fmt } = useLocale()

const showCreate = ref(false)
const showCreateChoice = ref(false)
const createMode = ref<'libre' | null>(null)
const createError = ref('')

// Lookup data
interface ClientOption { id: number; name: string; alias: string; status: string }
interface ProjectOption { id: number; code: string; name: string; client: number; status: string; client_name: string }

const allClients = ref<ClientOption[]>([])
const allProjects = ref<ProjectOption[]>([])

const clientSearch = ref('')
const projectSearch = ref('')
const selectedClientId = ref<number | null>(null)
const selectedProjectId = ref<number | null>(null)
const showProjectList = ref(false)

const filteredClients = computed(() => {
  const q = clientSearch.value.toLowerCase()
  return allClients.value
    .filter(c => c.status === 'active')
    .filter(c => !q || c.name.toLowerCase().includes(q) || (c.alias || '').toLowerCase().includes(q))
    .slice(0, 15)
})

const filteredProjects = computed(() => {
  let list = allProjects.value.filter(p => p.status === 'ACTIVE')
  if (selectedClientId.value) {
    list = list.filter(p => p.client === selectedClientId.value)
  }
  const q = projectSearch.value.toLowerCase()
  if (q) {
    list = list.filter(p =>
      p.name.toLowerCase().includes(q) || p.code.toLowerCase().includes(q)
    )
  }
  return list.slice(0, 20)
})

function selectClient(client: ClientOption) {
  selectedClientId.value = client.id
  clientSearch.value = client.name
  // Reset project if doesn't match
  if (selectedProjectId.value) {
    const proj = allProjects.value.find(p => p.id === selectedProjectId.value)
    if (proj && proj.client !== client.id) {
      selectedProjectId.value = null
      projectSearch.value = ''
    }
  }
  // Show project list automatically after selecting client
  showProjectList.value = true
}

function selectProject(project: ProjectOption) {
  selectedProjectId.value = project.id
  projectSearch.value = `${project.code} — ${project.name}`
  showProjectList.value = false
  // Auto-fill client
  if (!selectedClientId.value) {
    const client = allClients.value.find(c => c.id === project.client)
    if (client) {
      selectedClientId.value = client.id
      clientSearch.value = client.name
    }
  }
}

function clearClient() {
  selectedClientId.value = null
  clientSearch.value = ''
  selectedProjectId.value = null
  projectSearch.value = ''
  showProjectList.value = false
}

function clearProject() {
  selectedProjectId.value = null
  projectSearch.value = ''
  showProjectList.value = true
}

async function loadLookups() {
  try {
    const [cResp, pResp] = await Promise.all([
      apiClient.get('clients/', { params: { status: 'active' } }),
      apiClient.get('projects/', { params: { status: 'ACTIVE' } }),
    ])
    const cData = cResp.data?.data || cResp.data
    allClients.value = Array.isArray(cData) ? cData : cData?.results || []
    const pData = pResp.data?.data || pResp.data
    allProjects.value = Array.isArray(pData) ? pData : pData?.results || []
  } catch { /* silent */ }
}

function openCreateChoice() {
  showCreateChoice.value = true
  showCreate.value = false
  createMode.value = null
}

function chooseFactureProjet() {
  showCreateChoice.value = false
  router.push('/projects')
}

function chooseFactureLibre() {
  showCreateChoice.value = false
  createMode.value = 'libre'
  showCreate.value = true
  selectedClientId.value = null
  selectedProjectId.value = null
  clientSearch.value = ''
  projectSearch.value = ''
  createError.value = ''
  loadLookups()
}

const statusColors: Record<string, string> = {
  DRAFT: 'badge-gray',
  SUBMITTED: 'badge-blue',
  APPROVED: 'badge-green',
  SENT: 'badge-amber',
  PAID: 'badge-green-solid',
}

const statusLabels: Record<string, string> = {
  DRAFT: 'Brouillon',
  SUBMITTED: 'Soumise',
  APPROVED: 'Approuvée',
  SENT: 'Envoyée',
  PAID: 'Payée',
}

async function createInvoice() {
  createError.value = ''
  if (!selectedClientId.value) {
    createError.value = 'Sélectionnez un client.'
    return
  }
  try {
    const invoiceNumber = `PROV-${Date.now().toString().slice(-6)}`
    const payload: Record<string, unknown> = {
      client: selectedClientId.value,
      invoice_number: invoiceNumber,
    }
    if (selectedProjectId.value) {
      payload.project = selectedProjectId.value
    }
    const resp = await billingApi.createInvoice(payload)
    const data = resp.data?.data || resp.data
    showCreate.value = false
    router.push(`/billing/${data.id}`)
  } catch (err: unknown) {
    const e = err as { response?: { data?: { error?: { message?: string; details?: Array<{ message?: string }> } } } }
    createError.value = e.response?.data?.error?.details?.[0]?.message || e.response?.data?.error?.message || 'Erreur lors de la création'
  }
}

// Separate drafts from real invoices
const draftInvoices = computed(() => (store.invoices || []).filter((i: { status: string }) => i.status === 'DRAFT'))
const realInvoices = computed(() => (store.invoices || []).filter((i: { status: string }) => i.status !== 'DRAFT'))

async function deleteDraft(id: number) {
  try {
    await billingApi.deleteInvoice(id)
    await store.fetchInvoices()
  } catch { /* silent */ }
}

onMounted(() => store.fetchInvoices())
</script>

<template>
  <div>
    <div class="page-header">
      <h1>Facturation</h1>
      <button class="btn-primary" @click="openCreateChoice">+ Nouvelle facture</button>
    </div>

    <!-- Create choice modal -->
    <div v-if="showCreateChoice" class="card" style="margin-bottom: 12px;">
      <div class="card-title">Nouvelle facture — choisir le type</div>
      <div class="create-choice-grid">
        <button class="choice-card" @click="chooseFactureProjet">
          <div class="choice-icon">P</div>
          <div class="choice-label">Facture projet</div>
          <div class="choice-desc">Depuis un projet existant, avec lignes pré-remplies depuis les phases</div>
        </button>
        <button class="choice-card" @click="chooseFactureLibre">
          <div class="choice-icon">L</div>
          <div class="choice-label">Facture libre</div>
          <div class="choice-desc">Sans lien projet obligatoire, lignes saisies manuellement</div>
        </button>
      </div>
      <div class="form-actions" style="margin-top: 12px;">
        <button type="button" class="btn-ghost" @click="showCreateChoice = false">Annuler</button>
      </div>
    </div>

    <!-- Create free invoice form -->
    <div v-if="showCreate && createMode === 'libre'" class="card" style="margin-bottom: 12px;">
      <div class="card-title">Nouvelle facture libre</div>
      <div v-if="createError" class="alert-error">{{ createError }}</div>
      <form @submit.prevent="createInvoice" class="create-form">
        <div class="form-row-2">
          <!-- Client search -->
          <div class="form-group">
            <label>1. Client (actifs uniquement) *</label>
            <div class="search-dropdown">
              <template v-if="!selectedClientId">
                <input
                  v-model="clientSearch"
                  type="text"
                  placeholder="Tapez pour rechercher un client..."
                  class="search-input"
                />
                <div v-if="filteredClients.length || clientSearch" class="dropdown-list">
                  <div
                    v-for="c in filteredClients"
                    :key="c.id"
                    class="dropdown-item"
                    @click="selectClient(c)"
                  >
                    <span class="dropdown-main">{{ c.name }}</span>
                    <span v-if="c.alias" class="dropdown-sub">({{ c.alias }})</span>
                  </div>
                  <div v-if="clientSearch && !filteredClients.length" class="dropdown-empty">Aucun client actif trouvé</div>
                </div>
              </template>
              <div v-else class="selected-chip">
                <span>{{ clientSearch }}</span>
                <button type="button" class="chip-clear" @click="clearClient">&times;</button>
              </div>
            </div>
          </div>

          <!-- Project list (optional for free invoices) -->
          <div class="form-group">
            <label>2. Projet (optionnel)</label>
            <div class="search-dropdown">
              <template v-if="!selectedProjectId">
                <input
                  v-model="projectSearch"
                  type="text"
                  :placeholder="selectedClientId ? `Rechercher parmi ${filteredProjects.length} projet(s)...` : 'Sélectionnez un client d\'abord'"
                  class="search-input"
                  :disabled="!selectedClientId"
                  @focus="showProjectList = true"
                />
                <!-- Auto-show list when client selected -->
                <div v-if="(showProjectList || projectSearch) && selectedClientId" class="dropdown-list">
                  <div
                    v-for="p in filteredProjects"
                    :key="p.id"
                    class="dropdown-item"
                    @click="selectProject(p)"
                  >
                    <span class="dropdown-code">{{ p.code }}</span>
                    <span class="dropdown-main">{{ p.name }}</span>
                  </div>
                  <div v-if="!filteredProjects.length" class="dropdown-empty">Aucun projet actif pour ce client</div>
                </div>
              </template>
              <div v-else class="selected-chip">
                <span>{{ projectSearch }}</span>
                <button type="button" class="chip-clear" @click="clearProject">&times;</button>
              </div>
            </div>
          </div>
        </div>

        <div class="form-actions">
          <button type="button" class="btn-ghost" @click="showCreate = false">Annuler</button>
          <button type="submit" class="btn-primary" :disabled="!selectedClientId">Créer la facture</button>
        </div>
      </form>
    </div>

    <!-- Brouillons -->
    <div v-if="draftInvoices.length" class="section-card draft-section">
      <div class="section-header">
        <h3>Brouillons ({{ draftInvoices.length }})</h3>
        <span class="section-hint">Les brouillons ne comptent pas dans le facture a ce jour</span>
      </div>
      <table>
        <thead>
          <tr>
            <th>No provisoire</th>
            <th>Projet</th>
            <th>Client</th>
            <th class="text-right">Montant</th>
            <th>Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="invoice in draftInvoices" :key="invoice.id">
            <td class="font-mono text-muted">{{ invoice.invoice_number }}</td>
            <td>{{ invoice.project_code || '—' }}</td>
            <td class="text-muted">{{ invoice.client_name || '—' }}</td>
            <td class="text-right font-mono">{{ fmt.currency(invoice.total_amount) }}</td>
            <td class="text-muted">{{ fmt.date(invoice.date_created) }}</td>
            <td>
              <div style="display: flex; gap: 6px;">
                <button class="btn-sm-edit" @click="router.push(`/billing/${invoice.id}`)">Modifier</button>
                <button class="btn-sm-delete" @click.stop="deleteDraft(invoice.id)">Supprimer</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Factures reelles -->
    <div class="card-table">
      <div class="section-header">
        <h3>Factures ({{ realInvoices.length }})</h3>
      </div>
      <table>
        <thead>
          <tr>
            <th>No facture</th>
            <th>Projet</th>
            <th>Client</th>
            <th class="text-right">Montant</th>
            <th>Statut</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="invoice in realInvoices"
            :key="invoice.id"
            class="row-link"
            @click="router.push(`/billing/${invoice.id}`)"
          >
            <td class="font-mono font-medium">{{ invoice.invoice_number }}</td>
            <td>{{ invoice.project_code || '—' }}</td>
            <td class="text-muted">{{ invoice.client_name || '—' }}</td>
            <td class="text-right font-mono">{{ fmt.currency(invoice.total_amount) }}</td>
            <td>
              <span class="badge" :class="statusColors[invoice.status]">
                {{ statusLabels[invoice.status] || invoice.status }}
              </span>
            </td>
            <td class="text-muted">{{ fmt.date(invoice.date_created) }}</td>
          </tr>
          <tr v-if="!realInvoices.length">
            <td colspan="6" class="empty">Aucune facture soumise</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.page-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }
.page-header h1 { font-size: 20px; font-weight: 700; color: var(--color-gray-900); }
.card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 16px; }
.card-title { font-size: 14px; font-weight: 600; color: var(--color-gray-800); margin-bottom: 12px; }
.card-table { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); overflow: hidden; }
.alert-error { background: var(--color-danger-light); color: var(--color-danger); padding: 8px 12px; border-radius: 6px; font-size: 12px; margin-bottom: 12px; }
.form-row-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }

.search-dropdown { position: relative; }
.search-input { width: 100%; padding: 8px 12px; border: 1px solid var(--color-gray-300); border-radius: 6px; font-size: 13px; }
.search-input:focus { outline: none; border-color: var(--color-primary); box-shadow: 0 0 0 3px rgba(37,99,235,0.1); }
.dropdown-list { position: absolute; top: 100%; left: 0; right: 0; z-index: 50; margin-top: 2px; background: white; border: 1px solid var(--color-gray-200); border-radius: 6px; box-shadow: 0 4px 12px rgba(0,0,0,0.12); max-height: 200px; overflow-y: auto; }
.dropdown-item { padding: 8px 12px; cursor: pointer; display: flex; align-items: center; gap: 8px; font-size: 13px; transition: background 0.1s; }
.dropdown-item:hover { background: var(--color-primary-light); }
.dropdown-main { font-weight: 500; color: var(--color-gray-800); }
.dropdown-sub { font-size: 11px; color: var(--color-gray-400); }
.dropdown-code { font-family: var(--font-mono); font-size: 11px; color: var(--color-primary); font-weight: 600; min-width: 90px; }
.dropdown-empty { padding: 12px; text-align: center; font-size: 12px; color: var(--color-gray-400); }
.selected-chip { display: flex; align-items: center; justify-content: space-between; padding: 7px 12px; background: var(--color-primary-light); color: var(--color-primary); font-size: 13px; font-weight: 500; border-radius: 6px; }
.chip-clear { background: none; border: none; font-size: 16px; cursor: pointer; color: var(--color-primary); padding: 0 0 0 8px; font-weight: 700; }
.chip-clear:hover { color: var(--color-danger); }
.form-group { margin-bottom: 12px; }
.form-group label { display: block; font-size: 11px; font-weight: 600; color: var(--color-gray-600); margin-bottom: 4px; }
.form-actions { display: flex; justify-content: flex-end; gap: 6px; }
.row-link { cursor: pointer; }
.row-link:hover { background: var(--color-gray-50); }
.text-right { text-align: right; }
.text-muted { color: var(--color-gray-500); }
.empty { text-align: center; padding: 30px; color: var(--color-gray-400); }

.badge { display: inline-flex; padding: 1px 8px; border-radius: 10px; font-size: 10px; font-weight: 600; }
.badge-gray { background: var(--color-gray-100); color: var(--color-gray-500); }
.badge-blue { background: #DBEAFE; color: #1D4ED8; }
.badge-green { background: #DCFCE7; color: #15803D; }
.badge-amber { background: #FEF3C7; color: #92400E; }
.badge-green-solid { background: #15803D; color: white; }

.create-choice-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.choice-card { background: var(--color-gray-50); border: 2px solid var(--color-gray-200); border-radius: 8px; padding: 20px 16px; cursor: pointer; text-align: center; transition: border-color 0.15s, box-shadow 0.15s; }
.choice-card:hover { border-color: var(--color-primary); box-shadow: 0 0 0 3px rgba(37,99,235,0.1); }
.choice-icon { width: 36px; height: 36px; border-radius: 50%; background: var(--color-primary-light); color: var(--color-primary); font-weight: 700; font-size: 16px; display: flex; align-items: center; justify-content: center; margin: 0 auto 8px; }
.choice-label { font-size: 14px; font-weight: 600; color: var(--color-gray-800); margin-bottom: 4px; }
.choice-desc { font-size: 11px; color: var(--color-gray-500); line-height: 1.4; }

/* Sections */
.section-card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); overflow: hidden; margin-bottom: 16px; }
.draft-section { border: 1px dashed var(--color-gray-300); }
.section-header { display: flex; align-items: center; justify-content: space-between; padding: 10px 16px; border-bottom: 1px solid var(--color-gray-200); background: var(--color-gray-50); }
.section-header h3 { font-size: 13px; font-weight: 600; color: var(--color-gray-700); }
.section-hint { font-size: 10px; color: var(--color-gray-400); font-style: italic; }

.btn-sm-edit { padding: 3px 10px; border-radius: 4px; font-size: 11px; font-weight: 600; background: var(--color-primary-light); color: var(--color-primary); border: none; cursor: pointer; }
.btn-sm-edit:hover { background: var(--color-primary); color: white; }
.btn-sm-delete { padding: 3px 10px; border-radius: 4px; font-size: 11px; font-weight: 600; background: none; border: 1px solid #DC2626; color: #DC2626; cursor: pointer; }
.btn-sm-delete:hover { background: #FEE2E2; }
</style>
