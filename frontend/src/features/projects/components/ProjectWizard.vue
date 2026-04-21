<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useProjectStore } from '../stores/useProjectStore'
import { consortiumApi } from '@/features/consortiums/api/consortiumApi'
import apiClient from '@/plugins/axios'

const router = useRouter()
const store = useProjectStore()
const currentStep = ref(1)
const isSubmitting = ref(false)
const error = ref('')

const totalSteps = 5
const stepLabels = ['Identification', 'Budget & Phases', 'Ressources', 'Sous-traitants', 'Confirmation']

// Step 1: Metadata
const form = ref({
  code: '',
  name: '',
  client: null as number | null,
  pm: null as number | null,
  associate_in_charge: null as number | null,
  invoice_approver: null as number | null,
  contract_type: 'FORFAITAIRE' as const,
  business_unit: null as number | null,
  is_internal: false,
  legal_entity: '',
  start_date: '',
  end_date: '',
  template_id: null as number | null,
  address: '',
  city: '',
  country: 'Canada',
  surface: '' as string | number,
  surface_unit: 'm2',
  title_on_invoice: '',
  is_public: true,
  is_consortium: false,
  consortium_id: null as number | null,
  services_transversaux: [] as string[],
})

// Consortium data
interface ConsortiumOption { id: number; name: string; client_name: string; pr_role: string; members_count: number }
const allConsortiums = ref<ConsortiumOption[]>([])

async function loadConsortiums() {
  try {
    const resp = await consortiumApi.list()
    const data = resp.data?.data || resp.data
    allConsortiums.value = Array.isArray(data) ? data : data?.results || []
  } catch { allConsortiums.value = [] }
}

// Step 4: Sous-traitants
interface STEntry { name: string; specialty: string; budgeted_amount: string }
const subcontractors = ref<STEntry[]>([])

function addST() {
  subcontractors.value.push({ name: '', specialty: '', budgeted_amount: '0' })
}

function removeST(index: number) {
  subcontractors.value.splice(index, 1)
}

// Available services transversaux
const AVAILABLE_SERVICES = [
  { code: 'BIM', label: 'BIM / Modélisation' },
  { code: 'PAYSAGE', label: 'Architecture de paysage' },
  { code: 'DD', label: 'Développement durable' },
  { code: 'CIVIL', label: 'Génie civil' },
  { code: 'PATRIMOINE', label: 'Patrimoine' },
  { code: 'DESIGN_INT', label: 'Design intérieur' },
  { code: 'ECLAIRAGE', label: 'Éclairage' },
]

function toggleService(code: string) {
  const idx = form.value.services_transversaux.indexOf(code)
  if (idx >= 0) form.value.services_transversaux.splice(idx, 1)
  else form.value.services_transversaux.push(code)
}

// Template preview (phases + tasks tree)
interface TemplateTask { wbs_code?: string; name: string }
interface TemplatePhasePreview { name: string; is_mandatory?: boolean; tasks: TemplateTask[] }
const templatePreview = ref<TemplatePhasePreview[]>([])

// Client searchable dropdown (same pattern as InvoiceList.vue)
interface ClientOption { id: number; name: string; alias: string; status: string }
const allClients = ref<ClientOption[]>([])
const clientSearch = ref('')
const selectedClientId = ref<number | null>(null)

const filteredClients = computed(() => {
  const q = clientSearch.value.toLowerCase()
  return allClients.value
    .filter(c => c.status === 'active')
    .filter(c => !q || c.name.toLowerCase().includes(q) || (c.alias || '').toLowerCase().includes(q))
    .slice(0, 15)
})

function selectClient(client: ClientOption) {
  selectedClientId.value = client.id
  clientSearch.value = client.name
  form.value.client = client.id
}

function clearClient() {
  selectedClientId.value = null
  clientSearch.value = ''
  form.value.client = null
}

// Business Unit dropdown
interface BUOption { id: number; name: string; code: string }
const businessUnits = ref<BUOption[]>([])

// Users dropdown for PM, Associate, Approver
interface UserOption { id: number; username: string; email: string }
const allUsers = ref<UserOption[]>([])

async function loadLookups() {
  try {
    const [cResp, buResp, uResp] = await Promise.all([
      apiClient.get('clients/', { params: { status: 'active' } }),
      apiClient.get('business_units/'),
      apiClient.get('users/search/'),
    ])
    const cData = cResp.data?.data || cResp.data
    allClients.value = Array.isArray(cData) ? cData : cData?.results || []
    const buData = buResp.data?.data || buResp.data
    businessUnits.value = Array.isArray(buData) ? buData : buData?.results || []
    const uData = uResp.data?.data || uResp.data
    allUsers.value = Array.isArray(uData) ? uData : []
  } catch { /* silent */ }
}

// Step 2: Phases (from template or manual)
const phases = ref<Array<{ name: string; client_facing_label: string; billing_mode: string; budgeted_hours: string; budgeted_cost: string }>>([])

function addPhase() {
  phases.value.push({ name: '', client_facing_label: '', billing_mode: 'FORFAIT', budgeted_hours: '0', budgeted_cost: '0' })
}

function removePhase(index: number) {
  phases.value.splice(index, 1)
}

function nextStep() {
  if (currentStep.value === 1) {
    if (!form.value.code || !form.value.name) {
      error.value = 'Code et nom sont obligatoires'
      return
    }
    if (!form.value.is_internal && !form.value.client) {
      error.value = 'Le client est obligatoire pour un projet externe'
      return
    }
    if (form.value.is_consortium && !form.value.consortium_id) {
      error.value = 'Veuillez sélectionner un consortium ou décocher l\'option Consortium'
      return
    }
    if (form.value.start_date && form.value.end_date && form.value.end_date < form.value.start_date) {
      error.value = 'La date de fin ne peut pas être antérieure à la date de début.'
      return
    }
    error.value = ''
    // If template selected, load phases and preview from it
    if (form.value.template_id) {
      const tmpl = store.templates.find((t) => t.id === form.value.template_id)
      if (tmpl) {
        const phasesConfig = tmpl.phases_config as Array<Record<string, unknown>>
        phases.value = phasesConfig.map((p) => ({
          name: (p.name as string) || '',
          client_facing_label: (p.client_label as string) || '',
          billing_mode: (p.billing_mode as string) || 'FORFAIT',
          budgeted_hours: '0',
          budgeted_cost: '0',
        }))
        // Build preview tree — iterate ALL phases (including GP/SUPPORT)
        templatePreview.value = phasesConfig.map((p) => {
          const rawTasks = p.tasks
          const taskList = Array.isArray(rawTasks)
            ? (rawTasks as Array<Record<string, string>>).map((t) => ({
                wbs_code: t.wbs_code || '',
                name: t.name || '',
              }))
            : []
          return {
            name: (p.name as string) || '',
            is_mandatory: !!p.is_mandatory,
            tasks: taskList,
          }
        })
      }
    }
  }
  if (currentStep.value < totalSteps) currentStep.value++
}

function prevStep() {
  if (currentStep.value > 1) currentStep.value--
}

async function onSubmit() {
  isSubmitting.value = true
  error.value = ''
  try {
    const payload: Record<string, unknown> = {
      code: form.value.code,
      name: form.value.name,
      client: form.value.client,
      contract_type: form.value.contract_type,
      business_unit: businessUnits.value.find((bu: { id: number; name: string }) => bu.id === form.value.business_unit)?.name || '',
      is_internal: form.value.is_internal,
      legal_entity: form.value.legal_entity || '',
      start_date: form.value.start_date || null,
      end_date: form.value.end_date || null,
      address: form.value.address || '',
      city: form.value.city || '',
      country: form.value.country || 'Canada',
      surface: form.value.surface ? Number(form.value.surface) : null,
      surface_unit: form.value.surface_unit || 'm2',
      title_on_invoice: form.value.title_on_invoice || '',
      is_public: form.value.is_public,
      is_consortium: form.value.is_consortium,
      consortium: form.value.is_consortium ? form.value.consortium_id : null,
      services_transversaux: form.value.services_transversaux,
    }
    if (form.value.pm) payload.pm = Number(form.value.pm)
    if (form.value.associate_in_charge) payload.associate_in_charge = Number(form.value.associate_in_charge)
    if (form.value.invoice_approver) payload.invoice_approver = Number(form.value.invoice_approver)
    // Pass phase budgets directly with the template creation
    if (form.value.template_id && phases.value.length) {
      const phaseBudgets: Record<number, { budgeted_hours: number; budgeted_cost: number }> = {}
      phases.value.forEach((p, idx) => {
        const h = parseFloat(String(p.budgeted_hours || '0')) || 0
        const c = parseFloat(String(p.budgeted_cost || '0')) || 0
        if (h > 0 || c > 0) phaseBudgets[idx] = { budgeted_hours: h, budgeted_cost: c }
      })
      if (Object.keys(phaseBudgets).length) {
        payload.phase_budgets = phaseBudgets
      }
    }
    let project
    if (form.value.template_id) {
      project = await store.createFromTemplate(form.value.template_id, payload)
    } else {
      const resp = await store.createProject(payload)
      project = resp
    }
    if (project?.id) {
      if (form.value.template_id) {
        // Template creates phases — update budgets from wizard step 2
        try {
          const phResp = await apiClient.get(`projects/${project.id}/phases/`)
          const createdPhases = phResp.data?.data || phResp.data || []
          const phaseList = Array.isArray(createdPhases) ? createdPhases : createdPhases?.results || []
          for (let i = 0; i < Math.min(phaseList.length, phases.value.length); i++) {
            const wizardPhase = phases.value[i]
            if (!wizardPhase) continue
            const hours = parseFloat(String(wizardPhase.budgeted_hours || '0'))
            const cost = parseFloat(String(wizardPhase.budgeted_cost || '0'))
            if (hours > 0 || cost > 0) {
              await apiClient.patch(`projects/${project.id}/phases/${phaseList[i].id}/`, {
                budgeted_hours: hours,
                budgeted_cost: cost,
              })
            }
          }
        } catch { /* non-blocking */ }
      } else if (phases.value.length) {
        // No template — create phases manually
        for (const phase of phases.value) {
          try {
            await apiClient.post(`projects/${project.id}/phases/`, {
              name: phase.name,
              client_facing_label: phase.client_facing_label,
              billing_mode: phase.billing_mode,
              budgeted_hours: phase.budgeted_hours || 0,
              budgeted_cost: phase.budgeted_cost || 0,
              phase_type: 'REALIZATION',
            })
          } catch { /* continue with other phases */ }
        }
      }
      router.push(`/projects/${project.id}`)
    }
  } catch (e: unknown) {
    const err = e as { response?: { data?: { error?: { message?: string; details?: Array<{ field?: string; message?: string }> } } } }
    const details = err.response?.data?.error?.details
    if (details?.length) {
      error.value = details.map(d => `${d.field}: ${d.message}`).join(', ')
    } else {
      error.value = err.response?.data?.error?.message || 'Erreur lors de la création du projet'
    }
  } finally {
    isSubmitting.value = false
  }
}

// Load template preview when template changes
watch(() => form.value.template_id, (newId) => {
  if (newId) {
    const tmpl = store.templates.find((t) => t.id === newId)
    if (tmpl) {
      const phasesConfig = tmpl.phases_config as Array<Record<string, unknown>>
      // Build preview for ALL phases (including GP/SUPPORT types)
      templatePreview.value = phasesConfig.map((p) => {
        const rawTasks = p.tasks
        const taskList = Array.isArray(rawTasks)
          ? (rawTasks as Array<Record<string, string>>).map((t) => ({
              wbs_code: t.wbs_code || '',
              name: t.name || '',
            }))
          : []
        return {
          name: (p.name as string) || '',
          is_mandatory: !!p.is_mandatory,
          tasks: taskList,
        }
      })
    }
  } else {
    templatePreview.value = []
  }
})

onMounted(() => {
  loadLookups()
  loadConsortiums()
})
</script>

<template>
  <div class="mx-auto max-w-3xl">
    <h1 class="mb-6 text-2xl font-semibold text-text">
      Nouveau projet
    </h1>

    <!-- Step indicator -->
    <div class="mb-8 flex items-center gap-2">
      <div
        v-for="step in totalSteps"
        :key="step"
        class="flex items-center gap-2"
      >
        <div
          class="flex h-8 w-8 items-center justify-center rounded-full text-sm font-medium"
          :class="step <= currentStep ? 'bg-primary text-white' : 'bg-border text-text-muted'"
        >
          {{ step }}
        </div>
        <span
          class="hidden text-sm sm:inline"
          :class="step <= currentStep ? 'text-text font-medium' : 'text-text-muted'"
        >
          {{ stepLabels[step - 1] }}
        </span>
        <div
          v-if="step < totalSteps"
          class="mx-2 h-px w-8 bg-border"
        />
      </div>
    </div>

    <div
      v-if="error"
      class="mb-4 rounded bg-danger/10 p-3 text-sm text-danger"
    >
      {{ error }}
    </div>

    <div class="rounded-lg border border-border bg-surface p-6">
      <!-- Step 1: Identification -->
      <div v-if="currentStep === 1">
        <h2 class="mb-4 text-lg font-medium text-text">
          Identification du projet
        </h2>

        <div
          v-if="store.templates.length"
          class="mb-4"
        >
          <label class="text-xs font-medium text-text-muted">Template</label>
          <select
            v-model="form.template_id"
            class="mt-1 w-full rounded-md border border-border px-3 py-2 text-sm"
          >
            <option :value="null">
              Sans template
            </option>
            <option
              v-for="t in store.templates"
              :key="t.id"
              :value="t.id"
            >
              {{ t.name }} ({{ t.contract_type }})
            </option>
          </select>
        </div>

        <!-- Template preview: phases + tasks tree -->
        <div
          v-if="form.template_id && templatePreview.length"
          class="mb-4 rounded-md border border-border bg-surface-alt p-4"
        >
          <h3 class="mb-2 text-xs font-semibold uppercase text-text-muted">Aperçu du template</h3>
          <div v-for="(phase, pi) in templatePreview" :key="pi" class="mb-2">
            <div class="flex items-center gap-2 text-sm font-medium text-text">
              <span>{{ phase.name }}</span>
              <span v-if="phase.is_mandatory" class="rounded bg-primary/10 px-1.5 py-0.5 text-[10px] font-bold text-primary">Obligatoire</span>
            </div>
            <div v-if="phase.tasks.length" class="ml-4 mt-1 space-y-0.5">
              <div
                v-for="(task, ti) in phase.tasks"
                :key="ti"
                class="flex items-center gap-2 text-xs text-text-muted"
              >
                <span v-if="task.wbs_code" class="font-mono text-[10px]">{{ task.wbs_code }}</span>
                <span>{{ task.name }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="text-xs font-medium text-text-muted">Code *</label>
            <input
              v-model="form.code"
              type="text"
              class="mt-1 w-full rounded-md border border-border px-3 py-2 text-sm"
              placeholder="PRJ-2026-001"
            >
          </div>
          <div>
            <label class="text-xs font-medium text-text-muted">Nom *</label>
            <input
              v-model="form.name"
              type="text"
              class="mt-1 w-full rounded-md border border-border px-3 py-2 text-sm"
              placeholder="Complexe Desjardins"
            >
          </div>

          <!-- Client searchable dropdown (hidden for internal projects) -->
          <div v-if="!form.is_internal" class="col-span-2">
            <label class="text-xs font-medium text-text-muted">Client *</label>
            <div class="relative mt-1">
              <template v-if="!selectedClientId">
                <input
                  v-model="clientSearch"
                  type="text"
                  placeholder="Tapez pour rechercher un client..."
                  class="w-full rounded-md border border-border px-3 py-2 text-sm"
                />
                <div v-if="filteredClients.length || clientSearch" class="absolute left-0 right-0 top-full z-50 mt-1 max-h-48 overflow-y-auto rounded-md border border-border bg-white shadow-lg">
                  <div
                    v-for="c in filteredClients"
                    :key="c.id"
                    class="cursor-pointer px-3 py-2 text-sm hover:bg-primary/10"
                    @click="selectClient(c)"
                  >
                    <span class="font-medium">{{ c.name }}</span>
                    <span v-if="c.alias" class="ml-2 text-xs text-text-muted">({{ c.alias }})</span>
                  </div>
                  <div v-if="clientSearch && !filteredClients.length" class="px-3 py-2 text-center text-xs text-text-muted">Aucun client actif trouvé</div>
                  <div class="border-t border-border px-3 py-2">
                    <button type="button" class="text-xs font-medium text-primary hover:underline" @click="router.push('/clients?action=new')">+ Créer un nouveau client</button>
                  </div>
                </div>
              </template>
              <div v-else class="flex items-center justify-between rounded-md bg-primary/10 px-3 py-2 text-sm font-medium text-primary">
                <span>{{ clientSearch }}</span>
                <button type="button" class="ml-2 text-base font-bold hover:text-danger" @click="clearClient">&times;</button>
              </div>
            </div>
          </div>

          <div>
            <label class="text-xs font-medium text-text-muted">Type de contrat</label>
            <select
              v-model="form.contract_type"
              class="mt-1 w-full rounded-md border border-border px-3 py-2 text-sm"
            >
              <option value="FORFAITAIRE">
                Forfaitaire
              </option>
              <option value="CONSORTIUM">
                Consortium
              </option>
              <option value="CO_DEV">
                Co-développement
              </option>
              <option value="CONCEPTION_CONSTRUCTION">
                Conception-construction
              </option>
            </select>
          </div>
          <div>
            <label class="text-xs font-medium text-text-muted">Unité d'affaires</label>
            <select
              v-model="form.business_unit"
              class="mt-1 w-full rounded-md border border-border px-3 py-2 text-sm"
            >
              <option :value="null">— Sélectionner —</option>
              <option
                v-for="bu in businessUnits"
                :key="bu.id"
                :value="bu.id"
              >
                {{ bu.name }} ({{ bu.code }})
              </option>
            </select>
          </div>
          <div>
            <label class="text-xs font-medium text-text-muted">Chef de projet</label>
            <select
              v-model="form.pm"
              class="mt-1 w-full rounded-md border border-border px-3 py-2 text-sm"
            >
              <option :value="null">— Aucun —</option>
              <option v-for="u in allUsers" :key="u.id" :value="u.id">{{ u.username }} ({{ u.email }})</option>
            </select>
          </div>
          <div>
            <label class="text-xs font-medium text-text-muted">Associé en charge</label>
            <select
              v-model="form.associate_in_charge"
              class="mt-1 w-full rounded-md border border-border px-3 py-2 text-sm"
            >
              <option :value="null">— Aucun —</option>
              <option v-for="u in allUsers" :key="u.id" :value="u.id">{{ u.username }} ({{ u.email }})</option>
            </select>
          </div>
          <div>
            <label class="text-xs font-medium text-text-muted">Approbateur factures</label>
            <select
              v-model="form.invoice_approver"
              class="mt-1 w-full rounded-md border border-border px-3 py-2 text-sm"
            >
              <option :value="null">— Aucun —</option>
              <option v-for="u in allUsers" :key="u.id" :value="u.id">{{ u.username }} ({{ u.email }})</option>
            </select>
          </div>
          <div>
            <label class="text-xs font-medium text-text-muted">Entité juridique</label>
            <input
              v-model="form.legal_entity"
              type="text"
              class="mt-1 w-full rounded-md border border-border px-3 py-2 text-sm"
            >
          </div>
          <div>
            <label class="text-xs font-medium text-text-muted">Date début</label>
            <input
              v-model="form.start_date"
              type="date"
              class="mt-1 w-full rounded-md border border-border px-3 py-2 text-sm"
            >
          </div>
          <div>
            <label class="text-xs font-medium text-text-muted">Date fin</label>
            <input
              v-model="form.end_date"
              type="date"
              class="mt-1 w-full rounded-md border border-border px-3 py-2 text-sm"
            >
          </div>

          <!-- New fields: address, city, country, surface, title_on_invoice -->
          <div class="col-span-2">
            <label class="text-xs font-medium text-text-muted">Adresse</label>
            <input
              v-model="form.address"
              type="text"
              class="mt-1 w-full rounded-md border border-border px-3 py-2 text-sm"
              placeholder="123 rue Exemple"
            >
          </div>
          <div>
            <label class="text-xs font-medium text-text-muted">Ville</label>
            <input
              v-model="form.city"
              type="text"
              class="mt-1 w-full rounded-md border border-border px-3 py-2 text-sm"
              placeholder="Montréal"
            >
          </div>
          <div>
            <label class="text-xs font-medium text-text-muted">Pays</label>
            <input
              v-model="form.country"
              type="text"
              class="mt-1 w-full rounded-md border border-border px-3 py-2 text-sm"
              placeholder="Canada"
            >
          </div>
          <div>
            <label class="text-xs font-medium text-text-muted">Superficie</label>
            <div class="mt-1 flex gap-2">
              <input
                v-model="form.surface"
                type="number"
                class="w-full rounded-md border border-border px-3 py-2 text-sm"
                placeholder="0"
              >
              <select
                v-model="form.surface_unit"
                class="rounded-md border border-border px-2 py-2 text-sm"
              >
                <option value="m2">m²</option>
                <option value="pi2">pi²</option>
              </select>
            </div>
          </div>
          <div>
            <label class="text-xs font-medium text-text-muted">Titre sur facture</label>
            <input
              v-model="form.title_on_invoice"
              type="text"
              class="mt-1 w-full rounded-md border border-border px-3 py-2 text-sm"
              placeholder="Si différent du nom du projet"
            >
          </div>

          <!-- Checkboxes row -->
          <div class="col-span-2 flex flex-wrap items-center gap-6">
            <div class="flex items-center gap-2">
              <input
                id="is_internal"
                v-model="form.is_internal"
                type="checkbox"
                class="h-4 w-4 rounded border-border"
                @change="if (form.is_internal) { form.client = null; selectedClientId = null; clientSearch = '' }"
              >
              <label for="is_internal" class="text-sm text-text">Projet interne</label>
            </div>
            <div class="flex items-center gap-2">
              <input
                id="is_public"
                v-model="form.is_public"
                type="checkbox"
                class="h-4 w-4 rounded border-border"
              >
              <label for="is_public" class="text-sm text-text">Projet public</label>
            </div>
            <div class="flex items-center gap-2">
              <input
                id="is_consortium"
                v-model="form.is_consortium"
                type="checkbox"
                class="h-4 w-4 rounded border-border"
              >
              <label for="is_consortium" class="text-sm text-text">Consortium</label>
            </div>
          </div>

          <!-- Consortium selection (shown when is_consortium=true) -->
          <div v-if="form.is_consortium" class="col-span-2">
            <label class="text-xs font-medium text-text-muted">Consortium *</label>
            <div class="mt-1 flex items-center gap-3">
              <select
                v-model="form.consortium_id"
                class="w-full rounded-md border border-border px-3 py-2 text-sm"
              >
                <option :value="null">— Sélectionner un consortium —</option>
                <option v-for="c in allConsortiums" :key="c.id" :value="c.id">
                  {{ c.name }} ({{ c.client_name }}) — {{ c.pr_role === 'MANDATAIRE' ? 'Mandataire' : 'Partenaire' }}
                </option>
              </select>
              <button
                type="button"
                class="whitespace-nowrap text-xs font-medium text-primary hover:underline"
                @click="router.push('/consortiums/new')"
              >
                + Créer
              </button>
            </div>
            <p v-if="form.is_consortium && !allConsortiums.length" class="mt-1 text-xs text-text-muted">
              Aucun consortium existant — créez-en un d'abord
            </p>
          </div>

          <!-- Services transversaux (E-14) -->
          <div class="col-span-2">
            <label class="text-xs font-medium text-text-muted">Services transversaux</label>
            <div class="mt-2 flex flex-wrap gap-2">
              <button
                v-for="svc in AVAILABLE_SERVICES"
                :key="svc.code"
                type="button"
                class="rounded-full border px-3 py-1 text-xs font-medium transition-colors"
                :class="form.services_transversaux.includes(svc.code)
                  ? 'border-primary bg-primary/10 text-primary'
                  : 'border-border bg-white text-text-muted hover:border-primary/50'"
                @click="toggleService(svc.code)"
              >
                {{ svc.label }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Step 2: Budget & Phases -->
      <div v-if="currentStep === 2">
        <div class="mb-4 flex items-center justify-between">
          <h2 class="text-lg font-medium text-text">
            Phases et budget
          </h2>
          <button
            class="rounded bg-primary px-3 py-1.5 text-xs font-medium text-white"
            @click="addPhase"
          >
            + Ajouter une phase
          </button>
        </div>

        <div class="space-y-3">
          <div
            v-for="(phase, i) in phases"
            :key="i"
            class="rounded border border-border p-3"
          >
            <div class="mb-2 flex items-center justify-between">
              <span class="text-xs font-medium text-text-muted">Phase {{ i + 1 }}</span>
              <button
                class="text-xs text-danger hover:underline"
                @click="removePhase(i)"
              >
                Supprimer
              </button>
            </div>
            <div class="grid grid-cols-3 gap-3">
              <input
                v-model="phase.name"
                type="text"
                placeholder="Nom interne"
                class="rounded border border-border px-2 py-1.5 text-sm"
              >
              <input
                v-model="phase.client_facing_label"
                type="text"
                placeholder="Libellé client"
                class="rounded border border-border px-2 py-1.5 text-sm"
              >
              <select
                v-model="phase.billing_mode"
                class="rounded border border-border px-2 py-1.5 text-sm"
              >
                <option value="FORFAIT">
                  Forfait
                </option>
                <option value="HORAIRE">
                  Horaire
                </option>
              </select>
            </div>
            <div class="mt-2 grid grid-cols-2 gap-3">
              <div>
                <label class="text-[10px] text-text-muted">Heures budgetées</label>
                <input
                  v-model="phase.budgeted_hours"
                  type="number"
                  class="w-full rounded border border-border px-2 py-1.5 text-sm font-mono"
                >
              </div>
              <div>
                <label class="text-[10px] text-text-muted">Coût budgeté ($)</label>
                <input
                  v-model="phase.budgeted_cost"
                  type="number"
                  class="w-full rounded border border-border px-2 py-1.5 text-sm font-mono"
                >
              </div>
            </div>
          </div>
        </div>

        <p
          v-if="!phases.length"
          class="py-8 text-center text-sm text-text-muted"
        >
          Aucune phase — cliquez + ou sélectionnez un template à l'étape 1
        </p>
      </div>

      <!-- Step 3: Resources -->
      <div v-if="currentStep === 3">
        <h2 class="mb-4 text-lg font-medium text-text">
          Ressources et planification
        </h2>
        <p class="text-sm text-text-muted">
          L'affectation des ressources se fait après la création du projet via la fiche projet.
          Vous pourrez assigner des profils virtuels puis des employés réels.
        </p>
      </div>

      <!-- Step 4: Sous-traitants (E-09/E-10) -->
      <div v-if="currentStep === 4">
        <div class="mb-4 flex items-center justify-between">
          <h2 class="text-lg font-medium text-text">
            Sous-traitants
          </h2>
          <button
            type="button"
            class="rounded bg-primary px-3 py-1.5 text-xs font-medium text-white"
            @click="addST"
          >
            + Ajouter un sous-traitant
          </button>
        </div>

        <div class="space-y-3">
          <div
            v-for="(st, i) in subcontractors"
            :key="i"
            class="rounded border border-border p-3"
          >
            <div class="mb-2 flex items-center justify-between">
              <span class="text-xs font-medium text-text-muted">Sous-traitant {{ i + 1 }}</span>
              <button type="button" class="text-xs text-danger hover:underline" @click="removeST(i)">Supprimer</button>
            </div>
            <div class="grid grid-cols-3 gap-3">
              <input
                v-model="st.name"
                type="text"
                placeholder="Nom du sous-traitant"
                class="rounded border border-border px-2 py-1.5 text-sm"
              >
              <input
                v-model="st.specialty"
                type="text"
                placeholder="Spécialité (ex: structure)"
                class="rounded border border-border px-2 py-1.5 text-sm"
              >
              <div>
                <input
                  v-model="st.budgeted_amount"
                  type="number"
                  placeholder="Budget ($)"
                  class="w-full rounded border border-border px-2 py-1.5 text-sm font-mono"
                >
              </div>
            </div>
          </div>
        </div>

        <p v-if="!subcontractors.length" class="py-8 text-center text-sm text-text-muted">
          Aucun sous-traitant — vous pourrez en ajouter après la création du projet
        </p>
      </div>

      <!-- Step 5: Confirmation -->
      <div v-if="currentStep === 5">
        <h2 class="mb-4 text-lg font-medium text-text">
          Confirmation
        </h2>
        <div class="space-y-4">
          <div class="rounded bg-surface-alt p-4">
            <div class="grid grid-cols-2 gap-3 text-sm">
              <div>
                <span class="text-text-muted">Code:</span>
                <span class="ml-2 font-mono font-medium">{{ form.code }}</span>
              </div>
              <div>
                <span class="text-text-muted">Nom:</span>
                <span class="ml-2 font-medium">{{ form.name }}</span>
              </div>
              <div>
                <span class="text-text-muted">Client:</span>
                <span class="ml-2 font-medium">{{ clientSearch || '—' }}</span>
              </div>
              <div>
                <span class="text-text-muted">Type:</span>
                <span class="ml-2">{{ form.contract_type }}</span>
              </div>
              <div>
                <span class="text-text-muted">Unité d'affaires:</span>
                <span class="ml-2">{{ businessUnits.find(bu => bu.id === form.business_unit)?.name || '—' }}</span>
              </div>
              <div>
                <span class="text-text-muted">Entité juridique:</span>
                <span class="ml-2">{{ form.legal_entity || '—' }}</span>
              </div>
              <div>
                <span class="text-text-muted">Projet interne:</span>
                <span class="ml-2">{{ form.is_internal ? 'Oui' : 'Non' }}</span>
              </div>
              <div>
                <span class="text-text-muted">Public/Privé:</span>
                <span class="ml-2">{{ form.is_public ? 'Public' : 'Privé' }}</span>
              </div>
              <div>
                <span class="text-text-muted">Consortium:</span>
                <span class="ml-2">{{ form.is_consortium ? (allConsortiums.find(c => c.id === form.consortium_id)?.name || 'Oui (non assigné)') : 'Non' }}</span>
              </div>
              <div v-if="form.services_transversaux.length" class="col-span-2">
                <span class="text-text-muted">Services transversaux:</span>
                <span class="ml-2">{{ form.services_transversaux.join(', ') }}</span>
              </div>
              <div>
                <span class="text-text-muted">Sous-traitants:</span>
                <span class="ml-2">{{ subcontractors.length }}</span>
              </div>
              <div>
                <span class="text-text-muted">Chef de projet:</span>
                <span class="ml-2">{{ allUsers.find(u => u.id === form.pm)?.username || '—' }}</span>
              </div>
              <div>
                <span class="text-text-muted">Associé en charge:</span>
                <span class="ml-2">{{ allUsers.find(u => u.id === form.associate_in_charge)?.username || '—' }}</span>
              </div>
              <div>
                <span class="text-text-muted">Approbateur factures:</span>
                <span class="ml-2">{{ allUsers.find(u => u.id === form.invoice_approver)?.username || '—' }}</span>
              </div>
              <div>
                <span class="text-text-muted">Phases:</span>
                <span class="ml-2">{{ phases.length }}</span>
              </div>
            </div>
          </div>

          <div
            v-if="phases.length"
            class="rounded border border-border"
          >
            <table class="w-full text-sm">
              <thead class="border-b bg-surface-alt text-xs text-text-muted">
                <tr>
                  <th class="px-3 py-2 text-left">
                    Phase
                  </th>
                  <th class="px-3 py-2 text-left">
                    Mode
                  </th>
                  <th class="px-3 py-2 text-right font-mono">
                    Heures
                  </th>
                  <th class="px-3 py-2 text-right font-mono">
                    Coût
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(phase, i) in phases"
                  :key="i"
                  class="border-b last:border-0"
                >
                  <td class="px-3 py-2">
                    {{ phase.name }}
                  </td>
                  <td class="px-3 py-2 text-text-muted">
                    {{ phase.billing_mode }}
                  </td>
                  <td class="px-3 py-2 text-right font-mono">
                    {{ phase.budgeted_hours }}h
                  </td>
                  <td class="px-3 py-2 text-right font-mono">
                    {{ phase.budgeted_cost }}$
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Navigation -->
    <div class="mt-6 flex justify-between">
      <button
        v-if="currentStep > 1"
        class="rounded-md px-4 py-2 text-sm text-text-muted hover:bg-surface-alt"
        @click="prevStep"
      >
        ◀ Précédent
      </button>
      <div v-else />

      <button
        v-if="currentStep < totalSteps"
        class="rounded-md bg-primary px-6 py-2 text-sm font-medium text-white"
        @click="nextStep"
      >
        Suivant ▶
      </button>
      <button
        v-else
        class="rounded-md bg-success px-6 py-2 text-sm font-medium text-white disabled:opacity-50"
        :disabled="isSubmitting"
        @click="onSubmit"
      >
        {{ isSubmitting ? 'Création...' : 'Créer le projet' }}
      </button>
    </div>
  </div>
</template>
