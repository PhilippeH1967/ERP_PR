<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useLocale } from '@/shared/composables/useLocale'
import { useProjectStore } from '../stores/useProjectStore'

const route = useRoute()
const store = useProjectStore()
const { fmt } = useLocale()
const activeTab = ref('overview')

const tabs = [
  { key: 'overview', label: 'Vue d\'ensemble' },
  { key: 'phases', label: 'Phases' },
  { key: 'wbs', label: 'WBS' },
  { key: 'team', label: 'Équipe' },
  { key: 'budget', label: 'Budget' },
]

const statusColors: Record<string, string> = {
  ACTIVE: 'bg-success/10 text-success',
  ON_HOLD: 'bg-warning/10 text-warning',
  COMPLETED: 'bg-text-muted/10 text-text-muted',
  CANCELLED: 'bg-danger/10 text-danger',
}

onMounted(() => {
  store.fetchProject(Number(route.params.id))
})
</script>

<template>
  <div v-if="store.currentProject">
    <div class="mb-6 flex items-center gap-4">
      <h1 class="text-2xl font-semibold text-text">
        <span class="font-mono text-text-muted">{{ store.currentProject.code }}</span>
        {{ store.currentProject.name }}
      </h1>
      <span
        class="rounded-full px-3 py-1 text-xs font-medium"
        :class="statusColors[store.currentProject.status]"
      >
        {{ store.currentProject.status }}
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

    <!-- Overview -->
    <div
      v-if="activeTab === 'overview'"
      class="grid grid-cols-2 gap-6"
    >
      <div class="rounded-lg border border-border bg-surface p-6">
        <h3 class="mb-4 text-sm font-medium uppercase text-text-muted">
          Informations
        </h3>
        <div class="grid grid-cols-2 gap-3 text-sm">
          <div>
            <span class="text-text-muted">Type contrat</span>
            <p class="font-medium">
              {{ store.currentProject.contract_type }}
            </p>
          </div>
          <div>
            <span class="text-text-muted">Unité d'affaires</span>
            <p class="font-medium">
              {{ store.currentProject.business_unit || '—' }}
            </p>
          </div>
          <div>
            <span class="text-text-muted">Début</span>
            <p class="font-medium">
              {{ store.currentProject.start_date ? fmt.date(store.currentProject.start_date) : '—' }}
            </p>
          </div>
          <div>
            <span class="text-text-muted">Fin</span>
            <p class="font-medium">
              {{ store.currentProject.end_date ? fmt.date(store.currentProject.end_date) : '—' }}
            </p>
          </div>
        </div>
      </div>
      <div class="rounded-lg border border-border bg-surface p-6">
        <h3 class="mb-4 text-sm font-medium uppercase text-text-muted">
          Direction
        </h3>
        <div class="grid grid-cols-1 gap-2 text-sm">
          <div>
            <span class="text-text-muted">Chef de projet</span>
            <p class="font-medium">
              {{ store.currentProject.pm || '—' }}
            </p>
          </div>
          <div>
            <span class="text-text-muted">Associé en charge</span>
            <p class="font-medium">
              {{ store.currentProject.associate_in_charge || '—' }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Phases -->
    <div
      v-if="activeTab === 'phases'"
      class="rounded-lg border border-border bg-surface"
    >
      <table class="w-full text-left text-sm">
        <thead class="border-b border-border text-xs font-medium uppercase text-text-muted">
          <tr>
            <th class="px-4 py-3">
              Phase
            </th>
            <th class="px-4 py-3">
              Libellé client
            </th>
            <th class="px-4 py-3">
              Type
            </th>
            <th class="px-4 py-3">
              Mode
            </th>
            <th class="px-4 py-3 text-right font-mono">
              Heures
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="phase in store.currentProject.phases"
            :key="phase.id"
            class="border-b border-border last:border-0"
          >
            <td class="px-4 py-3 font-medium">
              {{ phase.name }}
            </td>
            <td class="px-4 py-3 text-text-muted">
              {{ phase.client_facing_label || '—' }}
            </td>
            <td class="px-4 py-3">
              {{ phase.phase_type }}
            </td>
            <td class="px-4 py-3">
              {{ phase.billing_mode }}
            </td>
            <td class="px-4 py-3 text-right font-mono">
              {{ fmt.hours(phase.budgeted_hours) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- WBS / Team / Budget placeholders -->
    <div
      v-if="activeTab === 'wbs'"
      class="rounded-lg border border-border bg-surface p-6 text-text-muted"
    >
      Structure WBS hiérarchique — à implémenter
    </div>
    <div
      v-if="activeTab === 'team'"
      class="rounded-lg border border-border bg-surface p-6 text-text-muted"
    >
      Affectation des ressources — à implémenter
    </div>
    <div
      v-if="activeTab === 'budget'"
      class="rounded-lg border border-border bg-surface p-6 text-text-muted"
    >
      Suivi budgétaire — à implémenter
    </div>
  </div>
</template>
