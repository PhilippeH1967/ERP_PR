<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { useClientStore } from '../stores/useClientStore'
import ClientCreateModal from '../components/ClientCreateModal.vue'

const { t } = useI18n()
const router = useRouter()
const store = useClientStore()
const search = ref('')
const showCreateModal = ref(false)

onMounted(() => store.fetchClients())

function onSearch() {
  store.fetchClients({ search: search.value })
}
</script>

<template>
  <div>
    <div class="mb-6 flex items-center justify-between">
      <h1 class="text-2xl font-semibold text-text">
        {{ t('nav.clients') || 'Clients' }}
      </h1>
      <button
        class="rounded-md bg-primary px-4 py-2 text-sm font-medium text-white"
        @click="showCreateModal = true"
      >
        + Nouveau client
      </button>
    </div>

    <div class="mb-4">
      <input
        v-model="search"
        type="text"
        placeholder="Rechercher par nom ou alias..."
        class="w-full max-w-md rounded-md border border-border px-3 py-2 text-sm"
        @keyup.enter="onSearch"
      >
    </div>

    <div class="rounded-lg border border-border bg-surface">
      <table class="w-full text-left text-sm">
        <thead class="border-b border-border text-xs font-medium uppercase tracking-wide text-text-muted">
          <tr>
            <th class="px-4 py-3">
              Nom
            </th>
            <th class="px-4 py-3">
              Alias
            </th>
            <th class="px-4 py-3">
              Secteur
            </th>
            <th class="px-4 py-3">
              Statut
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="client in store.clients"
            :key="client.id"
            class="cursor-pointer border-b border-border last:border-0 hover:bg-surface-alt"
            @click="router.push(`/clients/${client.id}`)"
          >
            <td class="px-4 py-3 font-medium">
              {{ client.name }}
            </td>
            <td class="px-4 py-3 text-text-muted">
              {{ client.alias }}
            </td>
            <td class="px-4 py-3">
              {{ client.sector }}
            </td>
            <td class="px-4 py-3">
              <span
                class="rounded-full px-2 py-0.5 text-xs"
                :class="client.status === 'active' ? 'bg-success/10 text-success' : 'bg-text-muted/10 text-text-muted'"
              >
                {{ client.status }}
              </span>
            </td>
          </tr>
          <tr v-if="!store.clients.length && !store.isLoading">
            <td
              colspan="4"
              class="px-4 py-8 text-center text-text-muted"
            >
              Aucun client trouvé
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Pagination -->
      <div
        v-if="store.pagination.count > 0"
        class="flex items-center justify-between border-t border-border px-4 py-3"
      >
        <span class="text-xs text-text-muted">{{ store.pagination.count }} client(s)</span>
        <div class="flex gap-2">
          <button
            class="rounded px-3 py-1 text-sm text-text-muted hover:bg-surface-alt disabled:opacity-30"
            :disabled="!store.pagination.previous"
            @click="store.fetchPage('prev')"
          >
            ◀ Précédent
          </button>
          <button
            class="rounded px-3 py-1 text-sm text-text-muted hover:bg-surface-alt disabled:opacity-30"
            :disabled="!store.pagination.next"
            @click="store.fetchPage('next')"
          >
            Suivant ▶
          </button>
        </div>
      </div>
    </div>

    <ClientCreateModal
      :open="showCreateModal"
      @close="showCreateModal = false"
    />
  </div>
</template>
