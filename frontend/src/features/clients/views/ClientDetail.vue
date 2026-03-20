<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useLocale } from '@/shared/composables/useLocale'
import { clientApi } from '../api/clientApi'
import { useClientStore } from '../stores/useClientStore'
import EditableField from '../components/EditableField.vue'
import ContactForm from '../components/ContactForm.vue'
import AddressForm from '../components/AddressForm.vue'

const route = useRoute()
const router = useRouter()
const store = useClientStore()
const { fmt } = useLocale()
const activeTab = ref('identification')
const showContactForm = ref(false)
const showAddressForm = ref(false)
const isEditing = ref(false)
const showDeleteConfirm = ref(false)

interface FinancialData {
  total_ca: string
  total_paid: string
  invoices_outstanding: string
  projects_count: number
  aging: { '0_30': string; '31_60': string; '61_90': string; '90_plus': string }
}

interface LinkedProject {
  id: number
  code: string
  name: string
  status: string
  client_name: string
}

const financial = ref<FinancialData | null>(null)
const linkedProjects = ref<LinkedProject[]>([])

const tabs = [
  { key: 'identification', label: 'Identification' },
  { key: 'contacts', label: 'Contacts' },
  { key: 'addresses', label: 'Adresses' },
  { key: 'financial', label: 'Financier' },
  { key: 'billing', label: 'Paramètres facturation' },
  { key: 'crm', label: 'CRM' },
]

const clientId = Number(route.params.id)

onMounted(async () => {
  await store.fetchClient(clientId)
  // Fetch financial data
  try {
    const resp = await clientApi.financialSummary(clientId)
    financial.value = resp.data?.data || resp.data
  } catch {
    financial.value = null
  }
  // Fetch linked projects
  try {
    const { default: apiClient } = await import('@/plugins/axios')
    const resp = await apiClient.get('projects/', { params: { client: String(clientId) } })
    linkedProjects.value = resp.data?.data || resp.data || []
  } catch {
    linkedProjects.value = []
  }
})

function saveField(field: string, value: string | number) {
  store.updateClient(clientId, { [field]: value })
}

async function onAddContact(data: Record<string, unknown>) {
  await store.addContact(clientId, data)
  showContactForm.value = false
}

async function onAddAddress(data: Record<string, unknown>) {
  await store.addAddress(clientId, data)
  showAddressForm.value = false
}

async function deleteContact(contactId: number) {
  if (!confirm('Supprimer ce contact ?')) return
  await clientApi.deleteContact(clientId, contactId)
  await store.fetchClient(clientId)
}

async function deleteAddress(addressId: number) {
  if (!confirm('Supprimer cette adresse ?')) return
  await clientApi.deleteAddress(clientId, addressId)
  await store.fetchClient(clientId)
}

async function deleteClient() {
  if (!confirm('Supprimer définitivement ce client ?')) return
  try {
    await clientApi.delete(clientId)
    router.push('/clients')
  } catch {
    // error
  }
}
</script>

<template>
  <div v-if="store.currentClient">
    <div class="mb-4">
      <div class="flex items-center justify-between">
        <div>
          <button class="text-xs text-text-muted hover:text-primary" style="background:none;border:none;padding:0;cursor:pointer;" @click="router.push('/clients')">&larr; Clients</button>
          <h1 class="text-xl font-semibold text-text">
            {{ store.currentClient.name }}
            <span v-if="store.currentClient.alias" class="ml-1 text-base text-text-muted">({{ store.currentClient.alias }})</span>
          </h1>
        </div>
        <div class="flex items-center gap-2">
          <span class="rounded-full px-2 py-0.5 text-xs font-medium" :class="store.currentClient.status === 'active' ? 'bg-success/10 text-success' : 'bg-text-muted/10 text-text-muted'">{{ store.currentClient.status }}</span>
          <button v-if="!isEditing" class="btn-primary" @click="isEditing = true">Modifier</button>
          <button v-if="isEditing" class="btn-primary" @click="isEditing = false">Terminer</button>
          <button v-if="!showDeleteConfirm" class="btn-ghost" style="color:var(--color-gray-400);font-size:11px;" @click="showDeleteConfirm = true">Supprimer...</button>
        </div>
      </div>
      <div v-if="showDeleteConfirm" class="mt-2 flex items-center gap-3 rounded-md bg-danger/5 border border-danger/20 p-3">
        <span class="text-xs text-danger">Supprimer définitivement ce client et toutes ses données ?</span>
        <button class="btn-danger" style="font-size:11px;padding:4px 10px;" @click="deleteClient">Confirmer la suppression</button>
        <button class="btn-ghost" style="font-size:11px;padding:4px 10px;" @click="showDeleteConfirm = false">Annuler</button>
      </div>
    </div>

    <!-- Tabs -->
    <div class="mb-6 flex gap-1 border-b border-border">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        class="px-4 py-2 text-sm font-medium transition-colors"
        :class="activeTab === tab.key ? 'border-b-2 border-primary text-primary' : 'text-text-muted hover:text-text'"
        @click="activeTab = tab.key"
      >
        {{ tab.label }}
      </button>
    </div>

    <!-- Tab content -->
    <div class="rounded-lg border border-border bg-surface p-6">
      <!-- Identification -->
      <div v-if="activeTab === 'identification'">
        <!-- Read mode -->
        <div v-if="!isEditing" class="grid grid-cols-2 gap-4">
          <div><label class="text-xs font-medium text-text-muted">Nom légal</label><p class="mt-0.5 text-sm font-medium">{{ store.currentClient.name || '—' }}</p></div>
          <div><label class="text-xs font-medium text-text-muted">Alias / Acronyme</label><p class="mt-0.5 text-sm font-medium">{{ store.currentClient.alias || '—' }}</p></div>
          <div><label class="text-xs font-medium text-text-muted">Entité juridique</label><p class="mt-0.5 text-sm font-medium">{{ store.currentClient.legal_entity || '—' }}</p></div>
          <div><label class="text-xs font-medium text-text-muted">Secteur</label><p class="mt-0.5 text-sm font-medium">{{ store.currentClient.sector || '—' }}</p></div>
        </div>
        <!-- Edit mode -->
        <div v-else class="grid grid-cols-2 gap-4">
          <EditableField :value="store.currentClient.name" label="Nom légal" @save="(v) => saveField('name', v)" />
          <EditableField :value="store.currentClient.alias" label="Alias / Acronyme" placeholder="Ajouter un alias" @save="(v) => saveField('alias', v)" />
          <EditableField :value="store.currentClient.legal_entity" label="Entité juridique" placeholder="Corporation, LLC..." @save="(v) => saveField('legal_entity', v)" />
          <EditableField :value="store.currentClient.sector" label="Secteur" placeholder="Public, Privé..." @save="(v) => saveField('sector', v)" />
        </div>
      </div>

      <!-- Contacts -->
      <div v-if="activeTab === 'contacts'">
        <div v-if="isEditing" class="mb-4 flex justify-end">
          <button
            class="rounded-md bg-primary px-3 py-1.5 text-xs font-medium text-white"
            @click="showContactForm = !showContactForm"
          >
            + Ajouter un contact
          </button>
        </div>

        <ContactForm
          v-if="showContactForm && isEditing"
          class="mb-4"
          @submit="onAddContact"
          @cancel="showContactForm = false"
        />

        <div
          v-for="contact in store.currentClient.contacts"
          :key="contact.id"
          class="mb-3 rounded border border-border p-3"
        >
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <p class="font-medium">
                {{ contact.name }}
              </p>
              <span
                v-if="contact.role"
                class="rounded-full bg-primary/10 px-2 py-0.5 text-[10px] font-medium text-primary"
              >{{ contact.role }}</span>
            </div>
            <div class="flex items-center gap-2">
              <span class="text-xs text-text-muted">{{ contact.language_preference === 'fr' ? 'FR' : 'EN' }}</span>
              <button v-if="isEditing" class="text-xs text-danger hover:underline" @click="deleteContact(contact.id)">Supprimer</button>
            </div>
          </div>
          <p class="mt-1 text-sm text-text-muted">
            {{ contact.email }}{{ contact.phone ? ` · ${contact.phone}` : '' }}
          </p>
        </div>
        <p
          v-if="!store.currentClient.contacts?.length && !showContactForm"
          class="text-sm text-text-muted"
        >
          Aucun contact — cliquez + pour ajouter
        </p>
      </div>

      <!-- Addresses -->
      <div v-if="activeTab === 'addresses'">
        <div v-if="isEditing" class="mb-4 flex justify-end">
          <button
            class="rounded-md bg-primary px-3 py-1.5 text-xs font-medium text-white"
            @click="showAddressForm = !showAddressForm"
          >
            + Ajouter une adresse
          </button>
        </div>

        <AddressForm
          v-if="showAddressForm && isEditing"
          class="mb-4"
          @submit="onAddAddress"
          @cancel="showAddressForm = false"
        />

        <div
          v-for="addr in store.currentClient.addresses"
          :key="addr.id"
          class="mb-3 rounded border border-border p-3"
        >
          <p class="font-medium">
            {{ addr.address_line_1 }}
          </p>
          <p
            v-if="addr.address_line_2"
            class="text-sm text-text-muted"
          >
            {{ addr.address_line_2 }}
          </p>
          <p class="text-sm text-text-muted">
            {{ addr.city }}, {{ addr.province }} {{ addr.postal_code }}
          </p>
          <div class="mt-1 flex items-center justify-between">
           <div class="flex gap-2">
            <span
              v-if="addr.is_primary"
              class="rounded bg-success/10 px-2 py-0.5 text-xs text-success"
            >Siège social</span>
            <span
              v-if="addr.is_billing && addr.is_primary"
              class="rounded bg-warning/10 px-2 py-0.5 text-xs text-warning"
            >Facturation principale</span>
            <span
              v-else-if="addr.is_billing"
              class="rounded bg-warning/10 px-2 py-0.5 text-xs text-warning"
            >Facturation</span>
            <span
              v-if="!addr.is_billing && !addr.is_primary"
              class="rounded bg-text-muted/10 px-2 py-0.5 text-xs text-text-muted"
            >Bureau</span>
           </div>
            <button v-if="isEditing" class="text-xs text-danger hover:underline" @click="deleteAddress(addr.id)">Supprimer</button>
          </div>
        </div>
      </div>

      <!-- Financial History -->
      <div v-if="activeTab === 'financial'">
        <div
          v-if="financial"
          class="space-y-6"
        >
          <!-- KPI Cards -->
          <div class="grid grid-cols-4 gap-4">
            <div class="rounded-lg border border-border p-4 text-center">
              <div class="text-2xl font-bold font-mono text-text">
                {{ fmt.currency(financial.total_ca) }}
              </div>
              <div class="text-xs text-text-muted">
                CA total
              </div>
            </div>
            <div class="rounded-lg border border-border p-4 text-center">
              <div class="text-2xl font-bold font-mono text-success">
                {{ fmt.currency(financial.total_paid) }}
              </div>
              <div class="text-xs text-text-muted">
                Total payé
              </div>
            </div>
            <div class="rounded-lg border border-border p-4 text-center">
              <div class="text-2xl font-bold font-mono text-danger">
                {{ fmt.currency(financial.invoices_outstanding) }}
              </div>
              <div class="text-xs text-text-muted">
                Impayé
              </div>
            </div>
            <div class="rounded-lg border border-border p-4 text-center">
              <div class="text-2xl font-bold text-text">
                {{ financial.projects_count }}
              </div>
              <div class="text-xs text-text-muted">
                Projets
              </div>
            </div>
          </div>

          <!-- Aging Analysis -->
          <div>
            <h3 class="mb-3 text-sm font-medium uppercase text-text-muted">
              Ancienneté des créances
            </h3>
            <div class="grid grid-cols-4 gap-3">
              <div class="rounded border border-success/30 bg-success/5 p-3 text-center">
                <div class="font-mono text-lg font-bold text-success">
                  {{ fmt.currency(financial.aging['0_30']) }}
                </div>
                <div class="text-xs text-text-muted">
                  0-30 jours
                </div>
              </div>
              <div class="rounded border border-warning/30 bg-warning/5 p-3 text-center">
                <div class="font-mono text-lg font-bold text-warning">
                  {{ fmt.currency(financial.aging['31_60']) }}
                </div>
                <div class="text-xs text-text-muted">
                  31-60 jours
                </div>
              </div>
              <div class="rounded border border-warning/30 bg-warning/5 p-3 text-center">
                <div class="font-mono text-lg font-bold text-warning">
                  {{ fmt.currency(financial.aging['61_90']) }}
                </div>
                <div class="text-xs text-text-muted">
                  61-90 jours
                </div>
              </div>
              <div class="rounded border border-danger/30 bg-danger/5 p-3 text-center">
                <div class="font-mono text-lg font-bold text-danger">
                  {{ fmt.currency(financial.aging['90_plus']) }}
                </div>
                <div class="text-xs text-text-muted">
                  90+ jours
                </div>
              </div>
            </div>
          </div>

          <!-- Linked Projects -->
          <div>
            <h3 class="mb-3 text-sm font-medium uppercase text-text-muted">
              Projets liés
            </h3>
            <div
              v-if="linkedProjects.length"
              class="space-y-2"
            >
              <div
                v-for="project in linkedProjects"
                :key="project.id"
                class="flex cursor-pointer items-center justify-between rounded border border-border p-3 hover:bg-surface-alt"
                @click="router.push(`/projects/${project.id}`)"
              >
                <div>
                  <span class="font-mono text-xs text-text-muted">{{ project.code }}</span>
                  <span class="ml-2 text-sm font-medium">{{ project.name }}</span>
                </div>
                <span
                  class="rounded-full px-2 py-0.5 text-xs"
                  :class="project.status === 'ACTIVE' ? 'bg-success/10 text-success' : 'bg-text-muted/10 text-text-muted'"
                >
                  {{ project.status }}
                </span>
              </div>
            </div>
            <p
              v-else
              class="text-sm text-text-muted"
            >
              Aucun projet lié
            </p>
          </div>
        </div>
        <p
          v-else
          class="text-sm text-text-muted"
        >
          Chargement des données financières...
        </p>
      </div>

      <!-- Billing (inline edit) -->
      <div v-if="activeTab === 'billing'">
        <div v-if="!isEditing" class="grid grid-cols-2 gap-4">
          <div><label class="text-xs font-medium text-text-muted">Termes de paiement (jours)</label><p class="mt-0.5 text-sm font-medium">{{ store.currentClient.payment_terms_days || '—' }}</p></div>
          <div><label class="text-xs font-medium text-text-muted">Template de facture</label><p class="mt-0.5 text-sm font-medium">{{ store.currentClient.default_invoice_template || 'Standard' }}</p></div>
        </div>
        <div v-else class="grid grid-cols-2 gap-4">
          <EditableField :value="store.currentClient.payment_terms_days" label="Termes de paiement (jours)" type="number" @save="(v) => saveField('payment_terms_days', v)" />
          <EditableField :value="store.currentClient.default_invoice_template" label="Template de facture" placeholder="Standard" @save="(v) => saveField('default_invoice_template', v)" />
        </div>
      </div>

      <!-- CRM (inline edit) -->
      <div v-if="activeTab === 'crm'">
        <div v-if="!isEditing">
          <div class="grid grid-cols-2 gap-4"><div><label class="text-xs font-medium text-text-muted">Associé en charge</label><p class="mt-0.5 text-sm font-medium">{{ store.currentClient.associe_en_charge || '—' }}</p></div></div>
          <div class="mt-4"><label class="text-xs font-medium text-text-muted">Notes</label><p class="mt-0.5 text-sm whitespace-pre-wrap">{{ store.currentClient.notes || '—' }}</p></div>
        </div>
        <div v-else>
          <div class="grid grid-cols-2 gap-4">
            <EditableField :value="store.currentClient.associe_en_charge" label="Associé en charge" placeholder="Sélectionner..." @save="(v) => saveField('associe_en_charge', v)" />
          </div>
          <div class="mt-4">
            <EditableField :value="store.currentClient.notes" label="Notes" type="textarea" placeholder="Ajouter des notes..." @save="(v) => saveField('notes', v)" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
