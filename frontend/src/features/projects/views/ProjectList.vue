<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '@/shared/composables/useAuth'
import { useProjectStore } from '../stores/useProjectStore'

const router = useRouter()
const store = useProjectStore()
const { currentUser } = useAuth()
const search = ref('')
const filterStatus = ref('')
const filterBU = ref('')
const filterPM = ref('')

const canCreateProject = computed(() => {
  const roles = currentUser.value?.roles || []
  return roles.includes('ADMIN') || roles.includes('FINANCE') || roles.includes('PM') || roles.includes('PROJECT_DIRECTOR') || roles.includes('DEPT_ASSISTANT')
})

// Extract unique values for filters
const uniqueBUs = computed(() => {
  const bus = new Set<string>()
  store.projects.forEach(p => { if (p.business_unit) bus.add(p.business_unit) })
  return Array.from(bus).sort()
})

const uniquePMs = computed(() => {
  const pms = new Map<string, string>()
  store.projects.forEach((p: Record<string, unknown>) => {
    if (p.pm_name) pms.set(String(p.pm), String(p.pm_name))
  })
  return Array.from(pms.entries()).map(([id, name]) => ({ id, name })).sort((a, b) => a.name.localeCompare(b.name))
})

const filteredProjects = computed(() => {
  let list = store.projects
  const q = search.value.trim().toLowerCase()
  if (q) {
    list = list.filter(
      (p) =>
        (p.code || '').toLowerCase().includes(q) ||
        (p.name || '').toLowerCase().includes(q) ||
        (p.client_name || '').toLowerCase().includes(q),
    )
  }
  if (filterStatus.value) list = list.filter(p => p.status === filterStatus.value)
  if (filterBU.value) list = list.filter(p => p.business_unit === filterBU.value)
  if (filterPM.value) list = list.filter(p => String(p.pm) === filterPM.value)
  return list
})

// Health indicator based on project data
function healthIndicator(project: Record<string, unknown>): { label: string; color: string } {
  const status = project.status as string
  if (status === 'COMPLETED') return { label: 'Terminé', color: 'badge-gray' }
  if (status === 'CANCELLED') return { label: 'Annulé', color: 'badge-red' }
  if (status === 'ON_HOLD') return { label: 'Pause', color: 'badge-amber' }
  return { label: 'OK', color: 'badge-green' }
}

onMounted(() => store.fetchProjects())

const statusLabels: Record<string, string> = {
  'ACTIVE': 'Actif',
  'ON_HOLD': 'En pause',
  'COMPLETED': 'Terminé',
  'CANCELLED': 'Annulé',
}

const statusColors: Record<string, string> = {
  'ACTIVE': 'badge-green',
  'ON_HOLD': 'badge-amber',
  'COMPLETED': 'badge-gray',
  'CANCELLED': 'badge-red',
}
</script>

<template>
  <div>
    <div class="mb-6 flex items-center justify-between">
      <h1 class="text-2xl font-semibold text-text">
        Projets
      </h1>
      <button
        v-if="canCreateProject"
        class="rounded-md bg-primary px-4 py-2 text-sm font-medium text-white"
        @click="router.push('/projects/new')"
      >
        + Nouveau projet
      </button>
    </div>

    <!-- Search + Filters -->
    <div class="mb-4 flex flex-wrap items-center gap-3">
      <input
        v-model="search"
        type="text"
        placeholder="Rechercher par code, nom ou client..."
        class="w-full max-w-sm rounded-md border border-border px-3 py-2 text-sm"
      >
      <select v-model="filterStatus" class="filter-select">
        <option value="">Tous les statuts</option>
        <option value="ACTIVE">Actif</option>
        <option value="ON_HOLD">En pause</option>
        <option value="COMPLETED">Terminé</option>
        <option value="CANCELLED">Annulé</option>
      </select>
      <select v-if="uniqueBUs.length" v-model="filterBU" class="filter-select">
        <option value="">Toutes les BU</option>
        <option v-for="bu in uniqueBUs" :key="bu" :value="bu">{{ bu }}</option>
      </select>
      <select v-if="uniquePMs.length" v-model="filterPM" class="filter-select">
        <option value="">Tous les CP</option>
        <option v-for="pm in uniquePMs" :key="pm.id" :value="pm.id">{{ pm.name }}</option>
      </select>
    </div>

    <div class="rounded-lg border border-border bg-surface">
      <table class="w-full text-left text-sm">
        <thead class="border-b border-border text-xs font-medium uppercase tracking-wide text-text-muted">
          <tr>
            <th class="px-4 py-3">Code</th>
            <th class="px-4 py-3">Nom</th>
            <th class="px-4 py-3">Client</th>
            <th class="px-4 py-3">Chef de projet</th>
            <th class="px-4 py-3">BU</th>
            <th class="px-4 py-3">Type</th>
            <th class="px-4 py-3">Statut</th>
            <th class="px-4 py-3">Santé</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="project in filteredProjects"
            :key="project.id"
            class="cursor-pointer border-b border-border last:border-0 hover:bg-surface-alt"
            @click="router.push(`/projects/${project.id}`)"
          >
            <td class="px-4 py-3 font-mono text-sm font-medium">
              {{ project.code }}
            </td>
            <td class="px-4 py-3">
              {{ project.name }}
            </td>
            <td class="px-4 py-3 text-text-muted">
              {{ project.client_name || '—' }}
            </td>
            <td class="px-4 py-3 text-text-muted">
              {{ (project as Record<string, unknown>).pm_name || '—' }}
            </td>
            <td class="px-4 py-3 text-text-muted">
              {{ project.business_unit || '—' }}
            </td>
            <td class="px-4 py-3 text-text-muted">
              {{ project.contract_type }}
            </td>
            <td class="px-4 py-3">
              <span
                class="badge"
                :class="statusColors[project.status] || 'badge-gray'"
              >
                {{ statusLabels[project.status] || project.status }}
              </span>
            </td>
            <td class="px-4 py-3">
              <span class="badge" :class="healthIndicator(project as Record<string, unknown>).color">
                {{ healthIndicator(project as Record<string, unknown>).label }}
              </span>
            </td>
          </tr>
          <tr v-if="!filteredProjects.length">
            <td colspan="8" class="px-4 py-8 text-center text-text-muted">Aucun projet trouvé</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.badge { display: inline-flex; padding: 2px 10px; border-radius: 10px; font-size: 10px; font-weight: 600; border: none; background: var(--color-gray-100); }
.badge-green { background: #DCFCE7; color: #15803D; }
.badge-amber { background: #FEF3C7; color: #92400E; }
.badge-gray { background: var(--color-gray-100, #f3f4f6); color: var(--color-gray-500, #6b7280); }
.badge-red { background: #FEE2E2; color: #DC2626; }
.filter-select {
  padding: 6px 10px;
  border: 1px solid var(--color-gray-300, #d1d5db);
  border-radius: 6px;
  font-size: 12px;
  color: var(--color-gray-700, #374151);
  background: white;
  min-width: 140px;
}
</style>
