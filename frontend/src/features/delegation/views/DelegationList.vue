<script setup lang="ts">
import { ref } from 'vue'
import BaseModal from '@/shared/components/BaseModal.vue'

interface Delegation {
  id: number
  delegator: string
  delegate: string
  scope: string
  start_date: string
  end_date: string | null
  is_active: boolean
}

const delegations = ref<Delegation[]>([])
const showCreateModal = ref(false)

const createForm = ref({
  delegate_id: '',
  scope: 'project',
  start_date: '',
  end_date: '',
})

function onCreate() {
  // Will call API when delegation endpoints exist
  showCreateModal.value = false
}
</script>

<template>
  <div>
    <div class="mb-6 flex items-center justify-between">
      <h1 class="text-2xl font-semibold text-text">
        Délégations
      </h1>
      <button
        class="rounded-md bg-primary px-4 py-2 text-sm font-medium text-white"
        @click="showCreateModal = true"
      >
        + Nouvelle délégation
      </button>
    </div>

    <!-- Active delegations banner -->
    <div class="mb-4 rounded-lg border border-warning/30 bg-warning/5 p-3">
      <span class="text-sm text-warning">
        Les délégations actives permettent à un collègue d'agir en votre nom.
      </span>
    </div>

    <!-- Delegations list -->
    <div class="rounded-lg border border-border bg-surface">
      <div
        v-for="d in delegations"
        :key="d.id"
        class="flex items-center justify-between border-b border-border p-4 last:border-0"
      >
        <div>
          <p class="text-sm font-medium">
            {{ d.delegator }} → {{ d.delegate }}
          </p>
          <p class="text-xs text-text-muted">
            {{ d.scope }} · {{ d.start_date }} — {{ d.end_date || 'Indéfini' }}
          </p>
        </div>
        <span
          class="rounded-full px-2 py-0.5 text-xs"
          :class="d.is_active ? 'bg-success/10 text-success' : 'bg-text-muted/10 text-text-muted'"
        >
          {{ d.is_active ? 'Active' : 'Expirée' }}
        </span>
      </div>
      <p
        v-if="!delegations.length"
        class="p-8 text-center text-sm text-text-muted"
      >
        Aucune délégation active
      </p>
    </div>

    <!-- Create delegation modal -->
    <BaseModal
      :open="showCreateModal"
      title="Nouvelle délégation"
      @close="showCreateModal = false"
    >
      <div class="space-y-4">
        <div>
          <label class="text-xs font-medium text-text-muted">Déléguer à (ID employé)</label>
          <input
            v-model="createForm.delegate_id"
            type="number"
            class="mt-1 w-full rounded-md border border-border px-3 py-2 text-sm"
          >
        </div>
        <div>
          <label class="text-xs font-medium text-text-muted">Portée</label>
          <select
            v-model="createForm.scope"
            class="mt-1 w-full rounded-md border border-border px-3 py-2 text-sm"
          >
            <option value="project">
              Projet spécifique
            </option>
            <option value="all">
              Toutes les approbations
            </option>
          </select>
        </div>
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="text-xs font-medium text-text-muted">Début</label>
            <input
              v-model="createForm.start_date"
              type="date"
              class="mt-1 w-full rounded-md border border-border px-3 py-2 text-sm"
            >
          </div>
          <div>
            <label class="text-xs font-medium text-text-muted">Fin</label>
            <input
              v-model="createForm.end_date"
              type="date"
              class="mt-1 w-full rounded-md border border-border px-3 py-2 text-sm"
            >
          </div>
        </div>
      </div>

      <template #actions>
        <button
          class="rounded-md px-4 py-2 text-sm text-text-muted"
          @click="showCreateModal = false"
        >
          Annuler
        </button>
        <button
          class="rounded-md bg-primary px-4 py-2 text-sm font-medium text-white"
          @click="onCreate"
        >
          Créer
        </button>
      </template>
    </BaseModal>
  </div>
</template>
