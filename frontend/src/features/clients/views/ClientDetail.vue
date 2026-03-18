<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useClientStore } from '../stores/useClientStore'
import EditableField from '../components/EditableField.vue'
import ContactForm from '../components/ContactForm.vue'
import AddressForm from '../components/AddressForm.vue'

const route = useRoute()
const store = useClientStore()
const activeTab = ref('identification')
const showContactForm = ref(false)
const showAddressForm = ref(false)

const tabs = [
  { key: 'identification', label: 'Identification' },
  { key: 'contacts', label: 'Contacts' },
  { key: 'addresses', label: 'Adresses' },
  { key: 'billing', label: 'Paramètres facturation' },
  { key: 'crm', label: 'CRM' },
]

const clientId = Number(route.params.id)

onMounted(() => store.fetchClient(clientId))

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
</script>

<template>
  <div v-if="store.currentClient">
    <div class="mb-4 flex items-center justify-between">
      <h1 class="text-2xl font-semibold text-text">
        {{ store.currentClient.name }}
        <span
          v-if="store.currentClient.alias"
          class="ml-2 text-lg text-text-muted"
        >({{ store.currentClient.alias }})</span>
      </h1>
      <span
        class="rounded-full px-3 py-1 text-xs font-medium"
        :class="store.currentClient.status === 'active' ? 'bg-success/10 text-success' : 'bg-text-muted/10 text-text-muted'"
      >
        {{ store.currentClient.status }}
      </span>
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
      <!-- Identification (inline edit) -->
      <div v-if="activeTab === 'identification'">
        <div class="grid grid-cols-2 gap-4">
          <EditableField
            :value="store.currentClient.name"
            label="Nom légal"
            @save="(v) => saveField('name', v)"
          />
          <EditableField
            :value="store.currentClient.alias"
            label="Alias / Acronyme"
            placeholder="Ajouter un alias"
            @save="(v) => saveField('alias', v)"
          />
          <EditableField
            :value="store.currentClient.legal_entity"
            label="Entité juridique"
            placeholder="Corporation, LLC..."
            @save="(v) => saveField('legal_entity', v)"
          />
          <EditableField
            :value="store.currentClient.sector"
            label="Secteur"
            placeholder="Public, Privé..."
            @save="(v) => saveField('sector', v)"
          />
        </div>
      </div>

      <!-- Contacts -->
      <div v-if="activeTab === 'contacts'">
        <div class="mb-4 flex justify-end">
          <button
            class="rounded-md bg-primary px-3 py-1.5 text-xs font-medium text-white"
            @click="showContactForm = !showContactForm"
          >
            + Ajouter un contact
          </button>
        </div>

        <ContactForm
          v-if="showContactForm"
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
            <p class="font-medium">
              {{ contact.name }}
            </p>
            <span class="text-xs text-text-muted">{{ contact.language_preference === 'fr' ? 'FR' : 'EN' }}</span>
          </div>
          <p class="text-sm text-text-muted">
            {{ contact.role }}{{ contact.role && contact.email ? ' · ' : '' }}{{ contact.email }}{{ contact.phone ? ` · ${contact.phone}` : '' }}
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
        <div class="mb-4 flex justify-end">
          <button
            class="rounded-md bg-primary px-3 py-1.5 text-xs font-medium text-white"
            @click="showAddressForm = !showAddressForm"
          >
            + Ajouter une adresse
          </button>
        </div>

        <AddressForm
          v-if="showAddressForm"
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
          <div class="mt-1 flex gap-2">
            <span
              v-if="addr.is_billing"
              class="rounded bg-primary/10 px-2 py-0.5 text-xs text-primary"
            >Facturation</span>
            <span
              v-if="addr.is_primary"
              class="rounded bg-success/10 px-2 py-0.5 text-xs text-success"
            >Principale</span>
          </div>
        </div>
      </div>

      <!-- Billing (inline edit) -->
      <div v-if="activeTab === 'billing'">
        <div class="grid grid-cols-2 gap-4">
          <EditableField
            :value="store.currentClient.payment_terms_days"
            label="Termes de paiement (jours)"
            type="number"
            @save="(v) => saveField('payment_terms_days', v)"
          />
          <EditableField
            :value="store.currentClient.default_invoice_template"
            label="Template de facture"
            placeholder="Standard"
            @save="(v) => saveField('default_invoice_template', v)"
          />
        </div>
      </div>

      <!-- CRM (inline edit) -->
      <div v-if="activeTab === 'crm'">
        <div class="grid grid-cols-2 gap-4">
          <EditableField
            :value="store.currentClient.associe_en_charge"
            label="Associé en charge"
            placeholder="Sélectionner..."
            @save="(v) => saveField('associe_en_charge', v)"
          />
        </div>
        <div class="mt-4">
          <EditableField
            :value="store.currentClient.notes"
            label="Notes"
            type="textarea"
            placeholder="Ajouter des notes..."
            @save="(v) => saveField('notes', v)"
          />
        </div>
      </div>
    </div>
  </div>
</template>
