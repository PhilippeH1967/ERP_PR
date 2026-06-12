<script setup lang="ts">
/**
 * ProjectSettingsTab — onglet « ⚙️ Paramètres » du projet (mockup 01, F5/F10).
 * Regroupe ce qui relève du paramétrage projet et renvoie vers l'Administration
 * pour les référentiels :
 *  1. Informations du projet (nom, dates, BU, PM, associé, coût de construction)
 *  2. Services transversaux (lecture — définis au wizard, phases SUPPORT)
 *  3. Profils virtuels (CRUD + remplacement par un employé)
 *  4. Blocages de saisie actifs (vue d'ensemble + déblocage)
 *  5. Liens vers les référentiels admin (phases / tâches standard, équipes)
 */
import { computed, ref, watch } from 'vue'
import apiClient from '@/plugins/axios'

interface ProjectInfo {
  id: number; name: string
  start_date?: string | null; end_date?: string | null
  business_unit?: string | null
  pm?: number | null; associate_in_charge?: number | null
  construction_cost?: number | string | null
  is_internal?: boolean
  services_transversaux?: string[]
  client?: number | null
  client_name?: string
  billing_address?: number | null
}
interface UserL { id: number; username: string; email?: string }
interface VirtualR { id: number; name: string; default_hourly_rate: string | number; is_active: boolean }
interface BlockR { id: number; employee: number; employee_name: string; phase: number | null; phase_name: string; task: number | null; task_name: string; task_wbs_code: string }

const props = defineProps<{
  projectId: number
  project: ProjectInfo | null
  users: UserL[]
  businessUnits: Array<{ id: number; name: string }>
}>()
const emit = defineEmits<{ updated: [] }>()

function parseAmount(v: unknown): number {
  return Number(String(v ?? '').replace(/\s/g, '').replace(',', '.')) || 0
}

/* ── 1. Informations du projet ── */
const form = ref({ name: '', start_date: '', end_date: '', business_unit: '', pm: '', associate_in_charge: '', construction_cost: '' })
const infoError = ref('')
const infoSaving = ref(false)
const infoSaved = ref(false)

function hydrate() {
  const p = props.project
  if (!p) return
  form.value = {
    name: p.name || '',
    start_date: p.start_date || '',
    end_date: p.end_date || '',
    business_unit: p.business_unit || '',
    pm: p.pm != null ? String(p.pm) : '',
    associate_in_charge: p.associate_in_charge != null ? String(p.associate_in_charge) : '',
    construction_cost: p.construction_cost != null ? String(p.construction_cost) : '',
  }
}
watch(() => props.project, hydrate, { immediate: true })

async function saveInfo() {
  infoError.value = ''
  infoSaved.value = false
  if (!form.value.name.trim()) { infoError.value = 'Le nom est obligatoire.'; return }
  if (form.value.start_date && form.value.end_date && form.value.end_date < form.value.start_date) {
    infoError.value = 'La date de fin ne peut pas être antérieure à la date de début.'
    return
  }
  infoSaving.value = true
  try {
    const payload: Record<string, unknown> = {
      name: form.value.name.trim(),
      business_unit: form.value.business_unit || '',
      start_date: form.value.start_date || null,
      end_date: form.value.end_date || null,
      pm: form.value.pm ? Number(form.value.pm) : null,
      associate_in_charge: form.value.associate_in_charge ? Number(form.value.associate_in_charge) : null,
    }
    if (!props.project?.is_internal) payload.construction_cost = parseAmount(form.value.construction_cost)
    await apiClient.patch(`projects/${props.projectId}/`, payload)
    infoSaved.value = true
    emit('updated')
  } catch (e: unknown) {
    infoError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur de sauvegarde'
  } finally { infoSaving.value = false }
}

/* ── 2b. Client du projet (changement + adresses) ── */
interface AddressR {
  id: number; address_line_1: string; address_line_2: string; city: string
  province: string; postal_code: string; country: string
  is_billing: boolean; is_primary: boolean
}
const clientsList = ref<Array<{ id: number; name: string }>>([])
const clientSearch = ref('')
const clientId = ref('')
const clientSaving = ref(false)
const clientSaved = ref(false)
const clientError = ref('')
const addresses = ref<AddressR[]>([])
const editingAddressId = ref<number | 'new' | null>(null)
const billingSelect = ref('')
const confirmClientChange = ref(false)
const emptyAddr = () => ({
  address_line_1: '', address_line_2: '', city: '', province: 'QC',
  postal_code: '', country: 'Canada', is_billing: false, is_primary: false,
})
const addrForm = ref(emptyAddr())
const addrSaving = ref(false)

const filteredClients = computed(() => {
  const q = clientSearch.value.trim().toLowerCase()
  return clientsList.value.filter(c => !q || c.name.toLowerCase().includes(q))
})

async function loadClients() {
  try {
    const r = await apiClient.get('clients/', { params: { page_size: '500' } })
    const d = r.data?.data || r.data
    clientsList.value = (Array.isArray(d) ? d : d?.results || []) as Array<{ id: number; name: string }>
  } catch { clientsList.value = [] }
}
async function loadAddresses() {
  const cid = props.project?.client
  if (!cid) { addresses.value = []; return }
  try {
    const r = await apiClient.get(`clients/${cid}/addresses/`)
    const d = r.data?.data || r.data
    addresses.value = (Array.isArray(d) ? d : d?.results || []) as AddressR[]
  } catch { addresses.value = [] }
}

function requestClientChange() {
  if (!clientDirty.value) return
  confirmClientChange.value = true
}

async function saveClient() {
  confirmClientChange.value = false
  clientError.value = ''
  clientSaved.value = false
  clientSaving.value = true
  try {
    await apiClient.patch(`projects/${props.projectId}/`, {
      client: clientId.value ? Number(clientId.value) : null,
    })
    clientSaved.value = true
    emit('updated')
    await loadAddresses()
  } catch (e: unknown) {
    clientError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur de sauvegarde'
  } finally { clientSaving.value = false }
}

function startEditAddress(a: AddressR) {
  editingAddressId.value = a.id
  addrForm.value = {
    address_line_1: a.address_line_1, address_line_2: a.address_line_2,
    city: a.city, province: a.province, postal_code: a.postal_code,
    country: a.country, is_billing: a.is_billing, is_primary: a.is_primary,
  }
  clientError.value = ''
}
function startAddAddress() {
  editingAddressId.value = 'new'
  addrForm.value = emptyAddr()
  clientError.value = ''
}
async function saveAddress() {
  const cid = props.project?.client
  if (!cid || addrSaving.value) return
  if (!addrForm.value.address_line_1.trim() || !addrForm.value.city.trim()) {
    clientError.value = 'Adresse et ville sont obligatoires.'
    return
  }
  addrSaving.value = true
  clientError.value = ''
  try {
    if (editingAddressId.value === 'new') {
      const r = await apiClient.post(`clients/${cid}/addresses/`, addrForm.value)
      const created = r.data?.data || r.data
      // Une adresse créée depuis le projet devient SON adresse de facturation.
      if (created?.id) await setProjectBillingAddress(Number(created.id))
    } else {
      await apiClient.patch(`clients/${cid}/addresses/${editingAddressId.value}/`, addrForm.value)
    }
    editingAddressId.value = null
    await loadAddresses()
  } catch (e: unknown) {
    const err = (e as { response?: { data?: { error?: { message?: string; details?: Array<{ message?: string }> } } } }).response?.data?.error
    clientError.value = err?.details?.[0]?.message || err?.message || 'Erreur de sauvegarde'
  } finally { addrSaving.value = false }
}
function addrLabel(a: AddressR): string {
  return `${a.address_line_1}, ${a.city} (${a.province}) ${a.postal_code}`.trim()
}
// Adresse effectivement utilisée pour la facturation de ce projet :
// désignation explicite, sinon adresse « facturation » du client, sinon
// principale, sinon la première.
const effectiveAddress = computed<AddressR | null>(() => {
  const designated = addresses.value.find(a => a.id === props.project?.billing_address)
  return designated
    || addresses.value.find(a => a.is_billing)
    || addresses.value.find(a => a.is_primary)
    || addresses.value[0]
    || null
})
const clientDirty = computed(() => clientId.value !== String(props.project?.client ?? ''))

function onBillingSelect() {
  setProjectBillingAddress(billingSelect.value ? Number(billingSelect.value) : null)
}

// Désigne l'adresse de facturation de CE projet (null = défaut du client).
async function setProjectBillingAddress(id: number | null) {
  clientError.value = ''
  try {
    await apiClient.patch(`projects/${props.projectId}/`, { billing_address: id })
    emit('updated')
  } catch (e: unknown) {
    clientError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur de sauvegarde'
  }
}

/* ── 3. Profils virtuels ── */
const virtuals = ref<VirtualR[]>([])
const showVirtualForm = ref(false)
const newVirtualName = ref('')
const newVirtualRate = ref('')
const editingVirtualId = ref<number | null>(null)
const editVirtualName = ref('')
const editVirtualRate = ref('')
const confirmDeleteVirtual = ref<number | null>(null)
const replacingVirtualId = ref<number | null>(null)
const replaceEmployeeId = ref<number | null>(null)
const virtualBusy = ref(false)
const virtualError = ref('')

async function loadVirtuals() {
  try {
    const r = await apiClient.get('virtual-resources/', { params: { project: props.projectId } })
    const d = r.data?.data || r.data
    virtuals.value = (Array.isArray(d) ? d : d?.results || []) as VirtualR[]
  } catch { virtuals.value = [] }
}

async function createVirtual() {
  if (!newVirtualName.value.trim() || virtualBusy.value) return
  virtualBusy.value = true
  virtualError.value = ''
  try {
    await apiClient.post('virtual-resources/', {
      project: props.projectId,
      name: newVirtualName.value.trim(),
      default_hourly_rate: parseAmount(newVirtualRate.value),
    })
    showVirtualForm.value = false
    newVirtualName.value = ''
    newVirtualRate.value = ''
    await loadVirtuals()
    emit('updated')
  } catch (e: unknown) {
    virtualError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Création impossible'
  } finally { virtualBusy.value = false }
}

function startEditVirtual(v: VirtualR) {
  editingVirtualId.value = v.id
  editVirtualName.value = v.name
  editVirtualRate.value = v.default_hourly_rate != null ? String(v.default_hourly_rate) : ''
  virtualError.value = ''
}
async function saveEditVirtual(id: number) {
  if (!editVirtualName.value.trim() || virtualBusy.value) return
  virtualBusy.value = true
  try {
    await apiClient.patch(`virtual-resources/${id}/`, {
      name: editVirtualName.value.trim(),
      default_hourly_rate: parseAmount(editVirtualRate.value),
    })
    editingVirtualId.value = null
    await loadVirtuals()
  } catch (e: unknown) {
    virtualError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur de sauvegarde'
  } finally { virtualBusy.value = false }
}
async function deleteVirtual(id: number) {
  confirmDeleteVirtual.value = null
  virtuals.value = virtuals.value.filter(v => v.id !== id) // optimiste
  try { await apiClient.delete(`virtual-resources/${id}/`); emit('updated') } catch { await loadVirtuals() }
}
async function confirmReplace(id: number) {
  if (!replaceEmployeeId.value || virtualBusy.value) return
  virtualBusy.value = true
  virtualError.value = ''
  try {
    await apiClient.post(`virtual-resources/${id}/replace_with_employee/`, { employee: Number(replaceEmployeeId.value) })
    replacingVirtualId.value = null
    replaceEmployeeId.value = null
    await loadVirtuals()
    emit('updated')
  } catch (e: unknown) {
    virtualError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Remplacement impossible'
  } finally { virtualBusy.value = false }
}

/* ── 4. Blocages de saisie ── */
const blocks = ref<BlockR[]>([])
async function loadBlocks() {
  try {
    const r = await apiClient.get('time_entry_blocks/', { params: { project: props.projectId, page_size: '500' } })
    const d = r.data?.data || r.data
    blocks.value = (Array.isArray(d) ? d : d?.results || []) as BlockR[]
  } catch { blocks.value = [] }
}
function blockScope(b: BlockR): string {
  if (b.task) return `${b.task_wbs_code || ''} ${b.task_name || 'Tâche #' + b.task}`.trim()
  if (b.phase) return `Phase ${b.phase_name || '#' + b.phase}`
  return 'Projet entier'
}
async function unblock(id: number) {
  blocks.value = blocks.value.filter(b => b.id !== id) // optimiste
  try { await apiClient.delete(`time_entry_blocks/${id}/`) } catch { await loadBlocks() }
}

watch(() => props.projectId, () => { loadVirtuals(); loadBlocks(); loadClients() }, { immediate: true })
// Synchronise le sélecteur de client + les adresses quand le projet change
// (déclaré après l'état client pour éviter un accès avant initialisation).
watch(() => props.project, (p) => {
  clientId.value = p?.client != null ? String(p.client) : ''
  billingSelect.value = p?.billing_address != null ? String(p.billing_address) : ''
  loadAddresses()
}, { immediate: true })
</script>

<template>
  <div class="ps-wrap">
    <!-- 1. Informations -->
    <div class="card ps-card">
      <h3>Informations du projet</h3>
      <div v-if="infoError" class="alert-error" style="margin-bottom:10px;">{{ infoError }}</div>
      <div class="ps-grid">
        <div class="form-group"><label>Nom *</label><input v-model="form.name" data-ps-name /></div>
        <div class="form-group"><label>Unité d'affaires</label>
          <select v-model="form.business_unit">
            <option value="">—</option>
            <option v-for="b in businessUnits" :key="b.id" :value="b.name">{{ b.name }}</option>
          </select>
        </div>
        <div class="form-group"><label>Date début</label><input v-model="form.start_date" type="date" data-ps-start /></div>
        <div class="form-group"><label>Date fin</label><input v-model="form.end_date" type="date" data-ps-end /></div>
        <div class="form-group"><label>Chef de projet</label>
          <select v-model="form.pm">
            <option value="">— Aucun —</option>
            <option v-for="u in users" :key="u.id" :value="String(u.id)">{{ u.username }}</option>
          </select>
        </div>
        <div class="form-group"><label>Associé en charge</label>
          <select v-model="form.associate_in_charge">
            <option value="">— Aucun —</option>
            <option v-for="u in users" :key="u.id" :value="String(u.id)">{{ u.username }}</option>
          </select>
        </div>
        <div v-if="!project?.is_internal" class="form-group">
          <label>Coût de construction ($)</label>
          <input v-model="form.construction_cost" type="text" inputmode="decimal" data-ps-cc placeholder="Ex. 2 500 000" />
          <p class="ps-hint">Informatif — sert au calcul des honoraires « Coût des travaux % ».</p>
        </div>
      </div>
      <div class="form-actions">
        <span v-if="infoSaved" class="ps-saved">✓ Enregistré</span>
        <button class="btn-primary" :disabled="infoSaving" data-ps-save @click="saveInfo">{{ infoSaving ? 'Sauvegarde…' : 'Enregistrer' }}</button>
      </div>
    </div>

    <!-- 2. Client du projet (changement + adresses) -->
    <div class="card ps-card">
      <h3>Client
        <RouterLink v-if="project?.client" class="ps-go" style="margin-left:auto;" :to="`/clients/${project.client}`">Ouvrir la fiche client complète →</RouterLink>
      </h3>
      <div v-if="clientError" class="alert-error" style="margin-bottom:10px;">{{ clientError }}</div>
      <div class="ps-inline-form">
        <input v-model="clientSearch" placeholder="Filtrer les clients…" style="max-width:200px;" data-ps-client-search />
        <select v-model="clientId" class="ps-select" style="flex:1;" data-ps-client-select>
          <option value="">— Aucun client —</option>
          <option v-for="c in filteredClients" :key="c.id" :value="String(c.id)">{{ c.name }}</option>
        </select>
        <span v-if="clientSaved" class="ps-saved">✓ Enregistré</span>
        <template v-if="confirmClientChange">
          <span class="ps-hint" style="margin:0;">Changer le client de ce projet ?</span>
          <button class="btn-action danger" data-ps-client-confirm @click="saveClient">Confirmer</button>
          <button class="btn-action" @click="confirmClientChange = false; clientId = String(project?.client ?? '')">Annuler</button>
        </template>
        <button v-else class="btn-action primary" :disabled="clientSaving || !clientDirty" data-ps-client-save @click="requestClientChange">{{ clientSaving ? '…' : 'Enregistrer' }}</button>
      </div>
      <p class="ps-hint">Changer le client réaffecte le projet : factures et rapports utiliseront ses coordonnées et son WBS client.</p>

      <template v-if="project?.client">
        <h4 class="ps-subhead">Adresse de facturation de ce projet</h4>
        <div class="ps-inline-form">
          <select v-model="billingSelect" class="ps-select" style="flex:1;" data-ps-billing-select @change="onBillingSelect">
            <option value="">Adresse de facturation par défaut du client</option>
            <option v-for="a in addresses" :key="a.id" :value="String(a.id)">{{ addrLabel(a) }}</option>
          </select>
          <button v-if="effectiveAddress" class="btn-action" data-ps-address-edit @click="startEditAddress(effectiveAddress)">✏️ Modifier cette adresse</button>
          <button class="ps-btn-add" data-ps-address-add @click="startAddAddress">+ Nouvelle adresse</button>
        </div>
        <p class="ps-hint" data-ps-billing-effective>
          Adresse utilisée :
          <strong v-if="effectiveAddress">{{ addrLabel(effectiveAddress) }}</strong>
          <strong v-else>aucune adresse chez ce client — créez-en une</strong>
          <template v-if="effectiveAddress && !project?.billing_address"> (défaut du client)</template>
        </p>

        <div v-if="editingAddressId !== null" class="ps-row">
          <div class="ps-addr-form">
            <input v-model="addrForm.address_line_1" placeholder="Adresse (ligne 1) *" data-ps-addr-line1 />
            <input v-model="addrForm.address_line_2" placeholder="Ligne 2" />
            <input v-model="addrForm.city" placeholder="Ville *" data-ps-addr-city />
            <input v-model="addrForm.province" placeholder="Province" style="max-width:70px;" />
            <input v-model="addrForm.postal_code" placeholder="Code postal" style="max-width:100px;" />
            <input v-model="addrForm.country" placeholder="Pays" style="max-width:100px;" />
            <label class="ps-check"><input v-model="addrForm.is_billing" type="checkbox" data-ps-addr-billing /> Facturation</label>
            <label class="ps-check"><input v-model="addrForm.is_primary" type="checkbox" /> Principale</label>
            <button class="btn-action primary" :disabled="addrSaving" data-ps-addr-save @click="saveAddress">Enregistrer</button>
            <button class="btn-action" @click="editingAddressId = null">Annuler</button>
          </div>
        </div>

        <template v-if="addresses.length">
          <h4 class="ps-subhead">Toutes les adresses du client</h4>
          <div v-for="a in addresses" :key="a.id" class="ps-row" data-ps-address>
            <div style="flex:1;">
              {{ addrLabel(a) }}
              <span v-if="a.is_billing" class="badge badge-blue" style="margin-left:6px;font-size:9px;">Facturation</span>
              <span v-if="a.is_primary" class="badge badge-green" style="margin-left:4px;font-size:9px;">Principale</span>
              <span v-if="project?.billing_address === a.id" class="badge badge-purple" style="margin-left:4px;font-size:9px;">Facturation de ce projet</span>
            </div>
            <button class="btn-action" @click="startEditAddress(a)">Modifier</button>
          </div>
        </template>
        <p class="ps-hint">Une nouvelle adresse créée ici est enregistrée dans la fiche client et devient l'adresse de facturation de ce projet. Les doublons sont refusés. La <strong>suppression</strong> d'une adresse se fait uniquement dans la fiche client.</p>
      </template>
      <p v-else class="ps-hint" data-ps-no-client>Aucun client associé à ce projet — choisissez un client ci-dessus puis « Enregistrer » pour gérer son adresse de facturation.</p>
    </div>

    <!-- 2. Services transversaux -->
    <div class="card ps-card">
      <h3>Services transversaux</h3>
      <div v-if="project?.services_transversaux?.length" class="ps-chips">
        <span v-for="s in project.services_transversaux" :key="s" class="badge badge-blue">{{ s }}</span>
      </div>
      <p v-else class="ps-hint">Aucun service transversal sélectionné.</p>
      <p class="ps-hint">Chaque service est une <strong>phase SUPPORT</strong> avec une tâche imputable (défini au wizard de création).</p>
    </div>

    <!-- 3. Profils virtuels -->
    <div class="card ps-card">
      <h3>Profils virtuels
        <button v-if="!showVirtualForm" class="btn-action primary" style="margin-left:auto;" @click="showVirtualForm = true; virtualError = ''">+ Profil virtuel</button>
      </h3>
      <p class="ps-hint">Ressources non nominatives, affectables comme un employé. Remplacez-les par un employé réel une fois l'équipe connue — les allocations basculent automatiquement.</p>
      <div v-if="virtualError" class="alert-error" style="margin:8px 0;">{{ virtualError }}</div>
      <div v-if="showVirtualForm" class="ps-inline-form">
        <input v-model="newVirtualName" placeholder="Nom du profil (ex. Architecte senior)" @keydown.enter="createVirtual" />
        <input v-model="newVirtualRate" type="number" min="0" step="0.01" placeholder="Taux $/h" style="max-width:110px;" />
        <button class="btn-action primary" :disabled="virtualBusy || !newVirtualName.trim()" @click="createVirtual">Créer</button>
        <button class="btn-action" @click="showVirtualForm = false">Annuler</button>
      </div>
      <div v-for="v in virtuals.filter(v => v.is_active)" :key="v.id" class="ps-row" data-ps-virtual>
        <span class="ps-vava">V</span>
        <template v-if="editingVirtualId === v.id">
          <input v-model="editVirtualName" data-ps-virtual-name style="flex:1;" />
          <input v-model="editVirtualRate" type="number" min="0" step="0.01" style="max-width:100px;" data-ps-virtual-rate />
          <button class="btn-action primary" data-ps-virtual-save :disabled="virtualBusy || !editVirtualName.trim()" @click="saveEditVirtual(v.id)">Enregistrer</button>
          <button class="btn-action" @click="editingVirtualId = null">Annuler</button>
        </template>
        <template v-else-if="replacingVirtualId === v.id">
          <div style="flex:1;"><strong>{{ v.name }}</strong></div>
          <select v-model="replaceEmployeeId" class="ps-select">
            <option :value="null">— Choisir un employé —</option>
            <option v-for="u in users" :key="u.id" :value="u.id">{{ u.username }}</option>
          </select>
          <button class="btn-action primary" :disabled="!replaceEmployeeId || virtualBusy" @click="confirmReplace(v.id)">Confirmer</button>
          <button class="btn-action" @click="replacingVirtualId = null">Annuler</button>
        </template>
        <template v-else>
          <div style="flex:1;"><strong>{{ v.name }}</strong> <span class="ps-hint">— {{ v.default_hourly_rate }} $/h</span></div>
          <button class="btn-action" data-ps-virtual-edit @click="startEditVirtual(v)">Modifier</button>
          <button class="btn-action" @click="replacingVirtualId = v.id; replaceEmployeeId = null">Remplacer…</button>
          <template v-if="confirmDeleteVirtual === v.id">
            <button class="btn-action danger" data-ps-virtual-delete-confirm @click="deleteVirtual(v.id)">Confirmer</button>
            <button class="btn-action" @click="confirmDeleteVirtual = null">Annuler</button>
          </template>
          <button v-else class="btn-action danger" data-ps-virtual-delete @click="confirmDeleteVirtual = v.id">Supprimer…</button>
        </template>
      </div>
      <p v-if="!virtuals.filter(v => v.is_active).length && !showVirtualForm" class="ps-hint">Aucun profil virtuel actif.</p>
    </div>

    <!-- 4. Blocages de saisie -->
    <div class="card ps-card">
      <h3>Blocages de saisie actifs</h3>
      <p class="ps-hint">Vue d'ensemble des personnes bloquées (par tâche, phase ou projet entier). Les blocages se posent dans <strong>Équipe &amp; charge</strong>.</p>
      <table v-if="blocks.length" class="data-table" style="font-size:12px;">
        <thead><tr><th>Personne</th><th>Portée</th><th style="width:100px;"></th></tr></thead>
        <tbody>
          <tr v-for="b in blocks" :key="b.id" data-ps-block>
            <td>{{ b.employee_name || 'Employé #' + b.employee }}</td>
            <td>{{ blockScope(b) }}</td>
            <td><button class="btn-action" data-ps-unblock @click="unblock(b.id)">Débloquer</button></td>
          </tr>
        </tbody>
      </table>
      <p v-else class="ps-hint">Aucun blocage actif.</p>
    </div>

    <!-- 5. Référentiels (admin) -->
    <div class="card ps-card">
      <h3>Référentiels (Administration)</h3>
      <div class="ps-link"><span>📐 Phases standard</span><span class="ps-hint">jeu du cabinet, hérité par tous les projets</span><RouterLink class="ps-go" to="/admin/standard-phases">Ouvrir →</RouterLink></div>
      <div class="ps-link"><span>📋 Tâches standard</span><span class="ps-hint">catalogue proposé au démarrage</span><RouterLink class="ps-go" to="/admin/standard-tasks">Ouvrir →</RouterLink></div>
      <div class="ps-link"><span>👥 Équipes</span><span class="ps-hint">groupes réutilisables (finance/paie/admin)</span><RouterLink class="ps-go" to="/admin/teams">Ouvrir →</RouterLink></div>
    </div>
  </div>
</template>

<style scoped>
.ps-wrap { display: flex; flex-direction: column; gap: 12px; }
.ps-card h3 { display: flex; align-items: center; gap: 8px; }
.ps-grid { display: grid; grid-template-columns: repeat(2, minmax(220px, 1fr)); gap: 10px 16px; max-width: 760px; }
.ps-grid .form-group label { display: block; font-size: 11px; font-weight: 600; color: var(--color-gray-600); margin-bottom: 4px; }
.ps-grid input, .ps-grid select { width: 100%; padding: 6px 10px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 13px; box-sizing: border-box; }
.ps-hint { font-size: 11px; color: var(--color-gray-400); margin: 4px 0 0; }
.ps-saved { font-size: 12px; color: var(--color-success, #15803D); margin-right: 8px; }
.ps-chips { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 6px; }
.ps-inline-form { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin: 8px 0; }
.ps-inline-form input { padding: 6px 10px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 13px; flex: 1; min-width: 180px; }
.ps-row { display: flex; align-items: center; gap: 8px; padding: 8px 0; border-bottom: 1px solid var(--color-gray-100); flex-wrap: wrap; }
.ps-row:last-of-type { border-bottom: none; }
.ps-row input { padding: 5px 9px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 12px; }
.ps-vava { width: 26px; height: 26px; border-radius: 50%; border: 1px dashed #7C3AED; color: #7C3AED; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 11px; flex-shrink: 0; }
.ps-select { padding: 5px 9px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 12px; min-width: 170px; }
.ps-subhead { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.03em; color: var(--color-gray-500); margin: 14px 0 6px; display: flex; align-items: center; gap: 8px; }
.ps-btn-add { background: var(--color-primary); color: #fff; border: none; border-radius: 5px; padding: 4px 10px; font-size: 11px; font-weight: 600; cursor: pointer; text-transform: none; letter-spacing: normal; }
.ps-addr-form { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; flex: 1; }
.ps-addr-form input[type=text], .ps-addr-form input:not([type]) { padding: 5px 9px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 12px; flex: 1; min-width: 110px; }
.ps-check { display: flex; align-items: center; gap: 4px; font-size: 11px; color: var(--color-gray-600); white-space: nowrap; }
.ps-link { display: flex; align-items: center; gap: 10px; padding: 8px 0; border-bottom: 1px solid var(--color-gray-100); font-size: 13px; }
.ps-link:last-child { border-bottom: none; }
.ps-go { margin-left: auto; color: var(--color-primary); font-weight: 600; font-size: 12px; text-decoration: none; }
.ps-go:hover { text-decoration: underline; }
.form-actions { display: flex; justify-content: flex-end; align-items: center; gap: 8px; margin-top: 12px; }
</style>
