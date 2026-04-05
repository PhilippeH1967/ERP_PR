<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { consortiumApi } from '../api/consortiumApi'
import apiClient from '@/plugins/axios'

const router = useRouter()
const route = useRoute()
const isEdit = computed(() => !!route.params.id)
const consortiumId = computed(() => Number(route.params.id) || null)

const isSubmitting = ref(false)
const error = ref('')
const successMsg = ref('')

// Form
const form = ref({
  name: '',
  client: null as number | null,
  pr_role: 'MANDATAIRE',
  contract_reference: '',
  description: '',
})

// Client dropdown
interface ClientOption { id: number; name: string; alias: string }
const allClients = ref<ClientOption[]>([])
const clientSearch = ref('')
const selectedClientId = ref<number | null>(null)

const filteredClients = computed(() => {
  const q = clientSearch.value.toLowerCase()
  return allClients.value
    .filter(c => !q || c.name.toLowerCase().includes(q) || (c.alias || '').toLowerCase().includes(q))
    .slice(0, 15)
})

function selectClient(c: ClientOption) {
  selectedClientId.value = c.id
  clientSearch.value = c.name
  form.value.client = c.id
}

function clearClient() {
  selectedClientId.value = null
  clientSearch.value = ''
  form.value.client = null
}

// External organizations dropdown
interface OrgOption { id: number; name: string; neq: string }
const allOrgs = ref<OrgOption[]>([])

// Members
interface MemberRow {
  id?: number
  is_pr: boolean
  organization: number | null
  name_override: string
  coefficient: string
  specialty: string
  contact_name: string
  contact_email: string
}
const members = ref<MemberRow[]>([])

const totalCoefficient = computed(() =>
  members.value.reduce((s, m) => s + Number(m.coefficient || 0), 0)
)

function addPR() {
  if (members.value.some(m => m.is_pr)) return
  members.value.unshift({
    is_pr: true,
    organization: null,
    name_override: 'Provencher Roy',
    coefficient: '',
    specialty: '',
    contact_name: '',
    contact_email: '',
  })
}

function addMember() {
  members.value.push({
    is_pr: false,
    organization: null,
    name_override: '',
    coefficient: '',
    specialty: '',
    contact_name: '',
    contact_email: '',
  })
}

function removeMember(index: number) {
  members.value.splice(index, 1)
}

// Load data
async function loadLookups() {
  try {
    const [cResp, oResp] = await Promise.all([
      apiClient.get('clients/'),
      apiClient.get('external_organizations/'),
    ])
    const cData = cResp.data?.data || cResp.data
    allClients.value = Array.isArray(cData) ? cData : cData?.results || []
    const oData = oResp.data?.data || oResp.data
    allOrgs.value = Array.isArray(oData) ? oData : oData?.results || []
  } catch { /* silent */ }
}

async function loadConsortium() {
  if (!consortiumId.value) return
  try {
    const resp = await consortiumApi.get(consortiumId.value)
    const data = resp.data?.data || resp.data
    form.value = {
      name: data.name || '',
      client: data.client || null,
      pr_role: data.pr_role || 'MANDATAIRE',
      contract_reference: data.contract_reference || '',
      description: data.description || '',
    }
    // Set client display
    if (data.client) {
      selectedClientId.value = data.client
      clientSearch.value = data.client_name || ''
    }
    // Load members
    members.value = (data.members || []).map((m: Record<string, unknown>) => ({
      id: m.id,
      is_pr: !!m.is_pr,
      organization: m.organization as number | null,
      name_override: (m.name_override as string) || '',
      coefficient: String(m.coefficient || ''),
      specialty: (m.specialty as string) || '',
      contact_name: (m.contact_name as string) || '',
      contact_email: (m.contact_email as string) || '',
    }))
  } catch {
    error.value = 'Consortium introuvable'
  }
}

onMounted(async () => {
  await loadLookups()
  if (isEdit.value) await loadConsortium()
  // Auto-add PR row for new consortiums
  if (!isEdit.value && !members.value.length) addPR()
})

// Submit
async function onSubmit() {
  error.value = ''
  if (!form.value.name.trim()) { error.value = 'Le nom est obligatoire'; return }
  if (!form.value.client) { error.value = 'Le client (donneur d\'ouvrage) est obligatoire'; return }

  isSubmitting.value = true
  try {
    let csrtId: number

    if (isEdit.value && consortiumId.value) {
      await consortiumApi.update(consortiumId.value, form.value as Record<string, unknown>)
      csrtId = consortiumId.value
    } else {
      const resp = await consortiumApi.create(form.value as Record<string, unknown>)
      const data = resp.data?.data || resp.data
      csrtId = data.id
    }

    // Save members
    for (const member of members.value) {
      const payload: Record<string, unknown> = {
        is_pr: member.is_pr,
        organization: member.organization || null,
        name_override: member.name_override || '',
        coefficient: Number(member.coefficient || 0),
        specialty: member.specialty || '',
        contact_name: member.contact_name || '',
        contact_email: member.contact_email || '',
      }
      if (member.id) {
        await consortiumApi.updateMember(csrtId, member.id, payload)
      } else {
        await consortiumApi.addMember(csrtId, payload)
      }
    }

    router.push(`/consortiums/${csrtId}`)
  } catch (e: unknown) {
    const err = e as { response?: { data?: { error?: { message?: string; details?: Array<{ message?: string }> } } } }
    error.value = err.response?.data?.error?.details?.[0]?.message || err.response?.data?.error?.message || 'Erreur lors de la sauvegarde'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="mx-auto max-w-3xl">
    <button class="mb-4 text-xs text-text-muted hover:text-primary" @click="router.push('/consortiums')">&larr; Retour aux consortiums</button>
    <h1 class="mb-6 text-2xl font-semibold text-text">
      {{ isEdit ? 'Modifier le consortium' : 'Nouveau consortium' }}
    </h1>

    <div v-if="error" class="mb-4 rounded bg-danger/10 p-3 text-sm text-danger">{{ error }}</div>
    <div v-if="successMsg" class="mb-4 rounded bg-success/10 p-3 text-sm text-success">{{ successMsg }}</div>

    <form @submit.prevent="onSubmit">
      <!-- Section 1: Identification -->
      <div class="section-card">
        <h2 class="section-title">Identification du consortium</h2>
        <div class="grid grid-cols-2 gap-4">
          <div class="col-span-2">
            <label class="field-label">Nom du consortium *</label>
            <input v-model="form.name" type="text" class="field-input" placeholder="Ex: Consortium Place Ville-Marie" />
          </div>

          <!-- Client (donneur d'ouvrage) -->
          <div class="col-span-2">
            <label class="field-label">Client (donneur d'ouvrage) *</label>
            <div class="relative">
              <template v-if="!selectedClientId">
                <input v-model="clientSearch" type="text" placeholder="Rechercher un client..." class="field-input" />
                <div v-if="filteredClients.length || clientSearch" class="dropdown-list">
                  <div v-for="c in filteredClients" :key="c.id" class="dropdown-item" @click="selectClient(c)">
                    <span class="font-medium">{{ c.name }}</span>
                    <span v-if="c.alias" class="ml-2 text-xs text-text-muted">({{ c.alias }})</span>
                  </div>
                  <div v-if="clientSearch && !filteredClients.length" class="dropdown-empty">Aucun client trouvé</div>
                </div>
              </template>
              <div v-else class="selected-pill">
                <span>{{ clientSearch }}</span>
                <button type="button" @click="clearClient">&times;</button>
              </div>
            </div>
          </div>

          <div>
            <label class="field-label">Rôle de Provencher Roy</label>
            <select v-model="form.pr_role" class="field-input">
              <option value="MANDATAIRE">Mandataire (responsable)</option>
              <option value="PARTENAIRE">Partenaire</option>
            </select>
          </div>
          <div>
            <label class="field-label">Référence contrat</label>
            <input v-model="form.contract_reference" type="text" class="field-input" placeholder="CT-2026-001" />
          </div>
          <div class="col-span-2">
            <label class="field-label">Description / notes</label>
            <textarea v-model="form.description" rows="2" class="field-input" placeholder="Notes sur le consortium..."></textarea>
          </div>
        </div>
      </div>

      <!-- Section 2: Membres -->
      <div class="section-card">
        <div class="flex items-center justify-between">
          <h2 class="section-title">Membres du consortium</h2>
          <div class="flex gap-2">
            <button v-if="!members.some(m => m.is_pr)" type="button" class="btn-sm-outline" @click="addPR">+ Provencher Roy</button>
            <button type="button" class="btn-sm-primary" @click="addMember">+ Ajouter partenaire</button>
          </div>
        </div>

        <div v-if="!members.length" class="py-6 text-center text-sm text-text-muted">
          Ajoutez Provencher Roy et les partenaires du consortium
        </div>

        <div v-for="(member, i) in members" :key="i" class="member-card">
          <div class="member-header">
            <span v-if="member.is_pr" class="badge badge-blue">PR — Provencher Roy</span>
            <span v-else class="text-xs font-medium text-text-muted">Partenaire {{ i }}</span>
            <button type="button" class="text-xs text-danger hover:underline" @click="removeMember(i)">Retirer</button>
          </div>
          <div class="grid grid-cols-3 gap-3">
            <div v-if="!member.is_pr">
              <label class="field-label-sm">Organisation *</label>
              <select v-model="member.organization" class="field-input-sm">
                <option :value="null">— Sélectionner —</option>
                <option v-for="org in allOrgs" :key="org.id" :value="org.id">
                  {{ org.name }} <template v-if="org.neq">({{ org.neq }})</template>
                </option>
              </select>
            </div>
            <div v-else>
              <label class="field-label-sm">Nom</label>
              <input v-model="member.name_override" class="field-input-sm" disabled value="Provencher Roy" />
            </div>
            <div>
              <label class="field-label-sm">Coefficient (%)</label>
              <input v-model="member.coefficient" type="number" step="0.01" min="0" max="100" class="field-input-sm font-mono" placeholder="0.00" />
            </div>
            <div>
              <label class="field-label-sm">Spécialité</label>
              <input v-model="member.specialty" class="field-input-sm" placeholder="Architecture, Structure..." />
            </div>
          </div>
        </div>

        <!-- Coefficient total -->
        <div v-if="members.length" class="coefficient-bar">
          <span>Total des coefficients :</span>
          <span class="font-mono font-semibold" :class="totalCoefficient === 100 ? 'text-success' : 'text-danger'">
            {{ totalCoefficient.toFixed(2) }}%
          </span>
          <span v-if="totalCoefficient !== 100" class="text-xs text-danger">(doit = 100%)</span>
          <span v-else class="text-xs text-success">✓ Valide</span>
        </div>
      </div>

      <!-- Actions -->
      <div class="mt-6 flex justify-between">
        <button type="button" class="rounded-md px-4 py-2 text-sm text-text-muted hover:bg-surface-alt" @click="router.push('/consortiums')">
          Annuler
        </button>
        <button
          type="submit"
          class="rounded-md bg-primary px-6 py-2 text-sm font-medium text-white disabled:opacity-50"
          :disabled="isSubmitting"
        >
          {{ isSubmitting ? 'Sauvegarde...' : (isEdit ? 'Enregistrer' : 'Créer le consortium') }}
        </button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.section-card { background: white; border: 1px solid var(--color-gray-200); border-radius: 8px; padding: 20px; margin-bottom: 16px; }
.section-title { font-size: 15px; font-weight: 600; color: var(--color-gray-800); margin-bottom: 16px; }
.field-label { display: block; font-size: 12px; font-weight: 600; color: var(--color-gray-600); margin-bottom: 4px; }
.field-label-sm { display: block; font-size: 10px; font-weight: 600; color: var(--color-gray-500); margin-bottom: 2px; }
.field-input { width: 100%; padding: 8px 12px; border: 1px solid var(--color-gray-300); border-radius: 6px; font-size: 14px; }
.field-input:focus { outline: none; border-color: var(--color-primary); box-shadow: 0 0 0 2px rgba(59,130,246,0.15); }
.field-input-sm { width: 100%; padding: 6px 8px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 13px; }
.field-input-sm:focus { outline: none; border-color: var(--color-primary); }

.dropdown-list { position: absolute; left: 0; right: 0; top: 100%; z-index: 50; margin-top: 2px; max-height: 200px; overflow-y: auto; border-radius: 6px; border: 1px solid var(--color-gray-200); background: white; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
.dropdown-item { padding: 8px 12px; cursor: pointer; font-size: 13px; }
.dropdown-item:hover { background: rgba(59,130,246,0.08); }
.dropdown-empty { padding: 8px 12px; text-align: center; font-size: 12px; color: var(--color-gray-400); }
.selected-pill { display: flex; align-items: center; justify-content: space-between; background: rgba(59,130,246,0.08); border-radius: 6px; padding: 8px 12px; font-size: 14px; font-weight: 500; color: var(--color-primary); }
.selected-pill button { font-size: 18px; font-weight: 700; color: var(--color-gray-400); background: none; border: none; cursor: pointer; }
.selected-pill button:hover { color: var(--color-danger); }

.member-card { border: 1px solid var(--color-gray-200); border-radius: 6px; padding: 12px; margin-top: 10px; }
.member-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; }

.badge { display: inline-flex; padding: 2px 10px; border-radius: 10px; font-size: 10px; font-weight: 600; }
.badge-blue { background: #DBEAFE; color: #1D4ED8; }

.coefficient-bar { display: flex; align-items: center; gap: 8px; padding: 10px 14px; margin-top: 12px; background: var(--color-gray-50); border-radius: 6px; font-size: 13px; }
.text-success { color: #15803D; }
.text-danger { color: #DC2626; }

.btn-sm-primary { padding: 5px 12px; border-radius: 6px; font-size: 12px; font-weight: 600; background: var(--color-primary); color: white; border: none; cursor: pointer; }
.btn-sm-outline { padding: 5px 12px; border-radius: 6px; font-size: 12px; font-weight: 600; background: white; color: var(--color-primary); border: 1px solid var(--color-primary); cursor: pointer; }
</style>
