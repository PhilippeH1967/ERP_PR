<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { supplierApi } from '../api/supplierApi'
import type { ExternalOrganization } from '../types/supplier.types'
import OrgCreateModal from '../components/OrgCreateModal.vue'

const router = useRouter()

const organizations = ref<ExternalOrganization[]>([])
const search = ref('')
const showCreateModal = ref(false)

async function fetchOrgs() {
  try {
    const params: Record<string, string> = {}
    if (search.value) params.search = search.value
    const response = await supplierApi.listOrganizations(params)
    const data = response.data?.data || response.data
    organizations.value = Array.isArray(data) ? data : data?.results || []
  } catch { organizations.value = [] }
}

let searchTimeout: ReturnType<typeof setTimeout> | null = null
watch(search, () => {
  if (searchTimeout) clearTimeout(searchTimeout)
  searchTimeout = setTimeout(fetchOrgs, 300)
})

async function onCreated() {
  showCreateModal.value = false
  await fetchOrgs()
}

const tagLabels: Record<string, string> = { st: 'Sous-traitant', partner: 'Partenaire', competitor: 'Concurrent' }
const tagColors: Record<string, string> = { st: 'bg-primary/10 text-primary', partner: 'bg-purple-100 text-purple-700', competitor: 'bg-gray-100 text-gray-500' }

onMounted(fetchOrgs)
</script>

<template>
  <div>
    <div class="page-header">
      <h1>Organisations externes</h1>
      <button class="btn-primary" @click="showCreateModal = true">+ Nouvelle organisation</button>
    </div>

    <div class="mb-4">
      <input v-model="search" type="text" placeholder="Rechercher par nom ou NEQ..." class="search-input" />
    </div>

    <div class="card-table">
      <table>
        <thead><tr><th>Nom</th><th>NEQ</th><th>Ville</th><th>Rôles</th></tr></thead>
        <tbody>
          <tr v-for="org in organizations" :key="org.id" class="row-link" @click="router.push(`/suppliers/${org.id}`)">
            <td class="font-semibold">{{ org.name }}</td>
            <td class="font-mono text-muted">{{ org.neq || '—' }}</td>
            <td>{{ org.city }}</td>
            <td>
              <span v-for="tag in org.type_tags" :key="tag" class="tag" :class="tagColors[tag] || 'bg-gray-100 text-gray-500'">{{ tagLabels[tag] || tag }}</span>
            </td>
          </tr>
          <tr v-if="!organizations.length"><td colspan="4" class="empty">Aucune organisation</td></tr>
        </tbody>
      </table>
    </div>

    <OrgCreateModal :open="showCreateModal" @close="showCreateModal = false" @created="onCreated" />
  </div>
</template>

<style scoped>
.page-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }
.page-header h1 { font-size: 20px; font-weight: 700; color: var(--color-gray-900); }
.search-input { width: 100%; max-width: 350px; padding: 8px 12px; border: 1px solid var(--color-gray-300); border-radius: 6px; font-size: 13px; }
.search-input:focus { outline: none; border-color: var(--color-primary); box-shadow: 0 0 0 3px rgba(37,99,235,0.1); }
.card-table { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); overflow: hidden; }
.row-link { cursor: pointer; } .row-link:hover { background: var(--color-gray-50); }
.font-mono { font-family: var(--font-mono); font-size: 12px; } .text-muted { color: var(--color-gray-500); }
.tag { display: inline-flex; padding: 1px 8px; border-radius: 10px; font-size: 10px; font-weight: 600; margin-right: 4px; }
.empty { text-align: center; padding: 30px; color: var(--color-gray-400); }
</style>
