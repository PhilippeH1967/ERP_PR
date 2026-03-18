<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useLocale } from '@/shared/composables/useLocale'
import { projectApi } from '../api/projectApi'
import { useProjectStore } from '../stores/useProjectStore'

const route = useRoute()
const store = useProjectStore()
const { fmt } = useLocale()
const activeTab = ref('overview')

interface DashboardData {
  hours_consumed: string
  budget_hours: string
  budget_utilization_percent: number
  health: 'green' | 'yellow' | 'red'
}

interface WBSNode {
  id: number
  standard_label: string
  client_facing_label: string
  element_type: string
  budgeted_hours: string
  children: WBSNode[]
}

const dashboard = ref<DashboardData | null>(null)
const wbsTree = ref<WBSNode[]>([])

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

const projectId = Number(route.params.id)

onMounted(async () => {
  await store.fetchProject(projectId)
  // Fetch dashboard KPIs
  try {
    const resp = await projectApi.dashboard(projectId)
    dashboard.value = resp.data?.data || resp.data
  } catch {
    dashboard.value = null
  }
  // Fetch WBS tree
  try {
    const resp = await projectApi.listWBS(projectId)
    wbsTree.value = resp.data?.data || resp.data || []
  } catch {
    wbsTree.value = []
  }
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
      class="space-y-6"
    >
      <!-- Health KPIs -->
      <div
        v-if="dashboard"
        class="grid grid-cols-3 gap-4"
      >
        <div class="rounded-lg border border-border bg-surface p-4 text-center">
          <div
            class="text-3xl font-bold"
            :class="{
              'text-success': dashboard.health === 'green',
              'text-warning': dashboard.health === 'yellow',
              'text-danger': dashboard.health === 'red',
            }"
          >
            {{ dashboard.budget_utilization_percent }}%
          </div>
          <div class="text-xs text-text-muted">
            Utilisation budget
          </div>
        </div>
        <div class="rounded-lg border border-border bg-surface p-4 text-center">
          <div class="font-mono text-2xl font-bold text-text">
            {{ fmt.hours(dashboard.hours_consumed) }}
          </div>
          <div class="text-xs text-text-muted">
            Heures consommées
          </div>
        </div>
        <div class="rounded-lg border border-border bg-surface p-4 text-center">
          <div class="font-mono text-2xl font-bold text-text">
            {{ fmt.hours(dashboard.budget_hours) }}
          </div>
          <div class="text-xs text-text-muted">
            Budget heures
          </div>
        </div>
      </div>

      <div class="grid grid-cols-2 gap-6">
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

      <!-- WBS Tree -->
      <div
        v-if="activeTab === 'wbs'"
        class="rounded-lg border border-border bg-surface p-6"
      >
        <div
          v-if="wbsTree.length"
          class="space-y-2"
        >
          <div
            v-for="node in wbsTree"
            :key="node.id"
            class="rounded border border-border p-3"
          >
            <div class="flex items-center justify-between">
              <div>
                <span class="rounded bg-primary/10 px-1.5 py-0.5 text-[10px] font-medium text-primary">{{ node.element_type }}</span>
                <span class="ml-2 text-sm font-medium">{{ node.client_facing_label || node.standard_label }}</span>
              </div>
              <span class="font-mono text-xs text-text-muted">{{ node.budgeted_hours }}h</span>
            </div>
            <div
              v-if="node.children?.length"
              class="ml-6 mt-2 space-y-1"
            >
              <div
                v-for="child in node.children"
                :key="child.id"
                class="flex items-center justify-between rounded bg-surface-alt p-2 text-sm"
              >
                <span>{{ child.client_facing_label || child.standard_label }}</span>
                <span class="font-mono text-xs text-text-muted">{{ child.budgeted_hours }}h</span>
              </div>
            </div>
          </div>
        </div>
        <p
          v-else
          class="text-sm text-text-muted"
        >
          Aucun élément WBS
        </p>
      </div>

      <!-- Team -->
      <div
        v-if="activeTab === 'team'"
        class="rounded-lg border border-border bg-surface p-6 text-text-muted"
      >
        L'affectation des ressources sera disponible prochainement.
      </div>

      <!-- Budget -->
      <div
        v-if="activeTab === 'budget'"
        class="rounded-lg border border-border bg-surface p-6"
      >
        <div
          v-if="dashboard"
          class="space-y-4"
        >
          <div class="flex items-center gap-4">
            <div class="h-3 flex-1 rounded-full bg-border">
              <div
                class="h-3 rounded-full"
                :class="{
                  'bg-success': dashboard.health === 'green',
                  'bg-warning': dashboard.health === 'yellow',
                  'bg-danger': dashboard.health === 'red',
                }"
                :style="{ width: Math.min(100, dashboard.budget_utilization_percent) + '%' }"
              />
            </div>
            <span class="font-mono text-sm font-medium">{{ dashboard.budget_utilization_percent }}%</span>
          </div>
          <div class="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span class="text-text-muted">Heures consommées</span>
              <p class="font-mono font-medium">
                {{ fmt.hours(dashboard.hours_consumed) }}
              </p>
            </div>
            <div>
              <span class="text-text-muted">Budget total</span>
              <p class="font-mono font-medium">
                {{ fmt.hours(dashboard.budget_hours) }}
              </p>
            </div>
          </div>
        </div>
        <p
          v-else
          class="text-sm text-text-muted"
        >
          Aucune donnée budgétaire
        </p>
      </div>
    </div>
  </div>
</template>
