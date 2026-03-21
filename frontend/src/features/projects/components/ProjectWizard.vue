<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useProjectStore } from '../stores/useProjectStore'
import apiClient from '@/plugins/axios'

const router = useRouter()
const store = useProjectStore()
const currentStep = ref(1)
const isSubmitting = ref(false)
const error = ref('')

const totalSteps = 4
const stepLabels = ['Identification', 'Budget & Phases', 'Ressources', 'Confirmation']

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
})

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

async function loadLookups() {
  try {
    const [cResp, buResp] = await Promise.all([
      apiClient.get('clients/', { params: { status: 'active' } }),
      apiClient.get('business_units/'),
    ])
    const cData = cResp.data?.data || cResp.data
    allClients.value = Array.isArray(cData) ? cData : cData?.results || []
    const buData = buResp.data?.data || buResp.data
    businessUnits.value = Array.isArray(buData) ? buData : buData?.results || []
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
    if (form.value.start_date && form.value.end_date && form.value.end_date < form.value.start_date) {
      error.value = 'La date de fin ne peut pas être antérieure à la date de début.'
      return
    }
    error.value = ''
    // If template selected, load phases from it
    if (form.value.template_id && phases.value.length === 0) {
      const tmpl = store.templates.find((t) => t.id === form.value.template_id)
      if (tmpl) {
        phases.value = (tmpl.phases_config as Array<Record<string, string>>).map((p) => ({
          name: p.name || '',
          client_facing_label: p.client_label || '',
          billing_mode: p.billing_mode || 'FORFAIT',
          budgeted_hours: '0',
          budgeted_cost: '0',
        }))
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
    }
    if (form.value.pm) payload.pm = Number(form.value.pm)
    if (form.value.associate_in_charge) payload.associate_in_charge = Number(form.value.associate_in_charge)
    if (form.value.invoice_approver) payload.invoice_approver = Number(form.value.invoice_approver)
    let project
    if (form.value.template_id) {
      project = await store.createFromTemplate(form.value.template_id, payload)
    } else {
      const resp = await store.createProject(payload)
      project = resp
    }
    if (project?.id) {
      // Create phases if not from template (template creates them automatically)
      if (!form.value.template_id && phases.value.length) {
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

onMounted(loadLookups)
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

          <!-- Client searchable dropdown -->
          <div class="col-span-2">
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
            <label class="text-xs font-medium text-text-muted">Chef de projet (ID utilisateur)</label>
            <input
              v-model="form.pm"
              type="number"
              class="mt-1 w-full rounded-md border border-border px-3 py-2 text-sm"
              placeholder="ID"
            >
          </div>
          <div>
            <label class="text-xs font-medium text-text-muted">Associé en charge (ID utilisateur)</label>
            <input
              v-model="form.associate_in_charge"
              type="number"
              class="mt-1 w-full rounded-md border border-border px-3 py-2 text-sm"
              placeholder="ID"
            >
          </div>
          <div>
            <label class="text-xs font-medium text-text-muted">Approbateur factures (ID utilisateur)</label>
            <input
              v-model="form.invoice_approver"
              type="number"
              class="mt-1 w-full rounded-md border border-border px-3 py-2 text-sm"
              placeholder="ID"
            >
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
          <div class="col-span-2 flex items-center gap-2">
            <input
              id="is_internal"
              v-model="form.is_internal"
              type="checkbox"
              class="h-4 w-4 rounded border-border"
            >
            <label for="is_internal" class="text-sm text-text">Projet interne (non facturable)</label>
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

      <!-- Step 4: Confirmation -->
      <div v-if="currentStep === 4">
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
                <span class="text-text-muted">Chef de projet:</span>
                <span class="ml-2">{{ form.pm || '—' }}</span>
              </div>
              <div>
                <span class="text-text-muted">Associé en charge:</span>
                <span class="ml-2">{{ form.associate_in_charge || '—' }}</span>
              </div>
              <div>
                <span class="text-text-muted">Approbateur factures:</span>
                <span class="ml-2">{{ form.invoice_approver || '—' }}</span>
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
