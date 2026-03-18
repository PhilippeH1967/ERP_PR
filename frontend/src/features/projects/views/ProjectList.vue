<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useProjectStore } from '../stores/useProjectStore'

const router = useRouter()
const store = useProjectStore()
const search = ref('')

onMounted(() => store.fetchProjects())

const statusColors: Record<string, string> = {
  ACTIVE: 'bg-success/10 text-success',
  ON_HOLD: 'bg-warning/10 text-warning',
  COMPLETED: 'bg-text-muted/10 text-text-muted',
  CANCELLED: 'bg-danger/10 text-danger',
}
</script>

<template>
  <div>
    <div class="mb-6 flex items-center justify-between">
      <h1 class="text-2xl font-semibold text-text">
        Projets
      </h1>
      <button
        class="rounded-md bg-primary px-4 py-2 text-sm font-medium text-white"
        @click="router.push('/projects/new')"
      >
        + Nouveau projet
      </button>
    </div>

    <div class="mb-4">
      <input
        v-model="search"
        type="text"
        placeholder="Rechercher par code ou nom..."
        class="w-full max-w-md rounded-md border border-border px-3 py-2 text-sm"
        @keyup.enter="store.fetchProjects({ search })"
      />
    </div>

    <div class="rounded-lg border border-border bg-surface">
      <table class="w-full text-left text-sm">
        <thead class="border-b border-border text-xs font-medium uppercase tracking-wide text-text-muted">
          <tr>
            <th class="px-4 py-3">
              Code
            </th>
            <th class="px-4 py-3">
              Nom
            </th>
            <th class="px-4 py-3">
              Client
            </th>
            <th class="px-4 py-3">
              Type
            </th>
            <th class="px-4 py-3">
              Statut
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="project in store.projects"
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
              {{ project.contract_type }}
            </td>
            <td class="px-4 py-3">
              <span
                class="rounded-full px-2 py-0.5 text-xs"
                :class="statusColors[project.status] || ''"
              >
                {{ project.status }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
