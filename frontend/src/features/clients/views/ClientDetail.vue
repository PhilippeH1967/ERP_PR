<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useClientStore } from '../stores/useClientStore'

const route = useRoute()
const store = useClientStore()
const activeTab = ref('identification')

const tabs = [
  { key: 'identification', label: 'Identification' },
  { key: 'contacts', label: 'Contacts' },
  { key: 'addresses', label: 'Adresses' },
  { key: 'billing', label: 'Paramètres facturation' },
  { key: 'crm', label: 'CRM' },
]

onMounted(() => {
  const id = Number(route.params.id)
  store.fetchClient(id)
})
</script>

<template>
  <div v-if="store.currentClient">
    <h1 class="mb-4 text-2xl font-semibold text-text">
      {{ store.currentClient.name }}
    </h1>

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
      <div v-if="activeTab === 'identification'">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="text-xs font-medium text-text-muted">Nom légal</label>
            <p class="text-sm">
              {{ store.currentClient.name }}
            </p>
          </div>
          <div>
            <label class="text-xs font-medium text-text-muted">Alias</label>
            <p class="text-sm">
              {{ store.currentClient.alias || '—' }}
            </p>
          </div>
          <div>
            <label class="text-xs font-medium text-text-muted">Entité juridique</label>
            <p class="text-sm">
              {{ store.currentClient.legal_entity || '—' }}
            </p>
          </div>
          <div>
            <label class="text-xs font-medium text-text-muted">Secteur</label>
            <p class="text-sm">
              {{ store.currentClient.sector || '—' }}
            </p>
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'contacts'">
        <div
          v-for="contact in store.currentClient.contacts"
          :key="contact.id"
          class="mb-3 rounded border border-border p-3"
        >
          <p class="font-medium">
            {{ contact.name }}
          </p>
          <p class="text-sm text-text-muted">
            {{ contact.role }} · {{ contact.email }} · {{ contact.phone }}
          </p>
        </div>
        <p
          v-if="!store.currentClient.contacts?.length"
          class="text-sm text-text-muted"
        >
          Aucun contact
        </p>
      </div>

      <div v-if="activeTab === 'addresses'">
        <div
          v-for="addr in store.currentClient.addresses"
          :key="addr.id"
          class="mb-3 rounded border border-border p-3"
        >
          <p class="font-medium">
            {{ addr.address_line_1 }}
          </p>
          <p class="text-sm text-text-muted">
            {{ addr.city }}, {{ addr.province }} {{ addr.postal_code }}
          </p>
          <span
            v-if="addr.is_billing"
            class="mt-1 inline-block rounded bg-primary/10 px-2 py-0.5 text-xs text-primary"
          >Facturation</span>
        </div>
      </div>

      <div v-if="activeTab === 'billing'">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="text-xs font-medium text-text-muted">Termes de paiement</label>
            <p class="text-sm">
              {{ store.currentClient.payment_terms_days }} jours
            </p>
          </div>
          <div>
            <label class="text-xs font-medium text-text-muted">Template facture</label>
            <p class="text-sm">
              {{ store.currentClient.default_invoice_template || 'Standard' }}
            </p>
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'crm'">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="text-xs font-medium text-text-muted">Associé en charge</label>
            <p class="text-sm">
              {{ store.currentClient.associe_en_charge || '—' }}
            </p>
          </div>
        </div>
        <div class="mt-4">
          <label class="text-xs font-medium text-text-muted">Notes</label>
          <p class="whitespace-pre-wrap text-sm">
            {{ store.currentClient.notes || 'Aucune note' }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
