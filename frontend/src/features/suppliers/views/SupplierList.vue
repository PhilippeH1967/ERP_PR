<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { supplierApi } from '../api/supplierApi'
import type { ExternalOrganization } from '../types/supplier.types'
import OrgCreateModal from '../components/OrgCreateModal.vue'

const router = useRouter()

const organizations = ref<ExternalOrganization[]>([])
const search = ref('')
const showCreateModal = ref(false)

onMounted(async () => {
  const response = await supplierApi.listOrganizations()
  organizations.value = response.data?.data || response.data
})

async function onSearch() {
  const response = await supplierApi.listOrganizations({ search: search.value })
  organizations.value = response.data?.data || response.data
}
</script>

<template>
  <div>
    <div class="mb-6 flex items-center justify-between">
      <h1 class="text-2xl font-semibold text-text">
        Organisations externes
      </h1>
      <button
        class="rounded-md bg-primary px-4 py-2 text-sm font-medium text-white"
        @click="showCreateModal = true"
      >
        + Nouvelle organisation
      </button>
    </div>

    <div class="mb-4">
      <input
        v-model="search"
        type="text"
        placeholder="Rechercher par nom ou NEQ..."
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
              NEQ
            </th>
            <th class="px-4 py-3">
              Ville
            </th>
            <th class="px-4 py-3">
              Rôles
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="org in organizations"
            :key="org.id"
            class="border-b border-border last:border-0 hover:bg-surface-alt cursor-pointer"
            @click="router.push(`/suppliers/${org.id}`)"
          >
            <td class="px-4 py-3 font-medium">
              {{ org.name }}
            </td>
            <td class="px-4 py-3 font-mono text-text-muted">
              {{ org.neq || '—' }}
            </td>
            <td class="px-4 py-3">
              {{ org.city }}
            </td>
            <td class="px-4 py-3">
              <span
                v-for="tag in org.type_tags"
                :key="tag"
                class="mr-1 rounded bg-surface-alt px-2 py-0.5 text-xs text-text-muted"
              >
                {{ tag }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <OrgCreateModal
      :open="showCreateModal"
      @close="showCreateModal = false"
      @created="onSearch"
    />
  </div>
</template>
