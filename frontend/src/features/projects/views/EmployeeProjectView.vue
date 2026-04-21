<script setup lang="ts">
/**
 * Employee-specific project view.
 * Shows: global project progress, tasks by person, and the employee's own tasks.
 * Simpler than ProjectDetail (12 tabs) which is for PM/Finance.
 */
import { onMounted, ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import apiClient from '@/plugins/axios'

const route = useRoute()
const router = useRouter()
const projectId = computed(() => Number(route.params.id))

interface Project { id: number; code: string; name: string; client_name: string; status: string; start_date: string; end_date: string; pm: number }
interface Phase { id: number; name: string; client_facing_label: string; budgeted_hours: string; billing_mode: string; is_locked: boolean }
interface Task { id: number; phase: number; phase_name: string; wbs_code: string; name: string; client_facing_label: string; budgeted_hours: string; progress_pct: number }
interface TimeEntry { id: number; phase: number; task: number; task_name: string; date: string; hours: string; status: string }
interface Assignment { id: number; employee: number; employee_name: string; phase: number; phase_name: string; hours_per_week: string }

const project = ref<Project | null>(null)
const phases = ref<Phase[]>([])
const tasks = ref<Task[]>([])
const myEntries = ref<TimeEntry[]>([])
const assignments = ref<Assignment[]>([])
const isLoading = ref(true)

onMounted(async () => {
  isLoading.value = true
  try {
    const [pResp, phResp, tResp, teResp, aResp] = await Promise.all([
      apiClient.get(`projects/${projectId.value}/`),
      apiClient.get(`projects/${projectId.value}/phases/`),
      apiClient.get(`projects/${projectId.value}/tasks/`),
      apiClient.get(`time_entries/`, { params: { project: projectId.value } }),
      apiClient.get(`allocations/`, { params: { project: projectId.value, page_size: '500' } }),
    ])
    project.value = pResp.data?.data || pResp.data
    const phData = phResp.data?.data || phResp.data
    phases.value = Array.isArray(phData) ? phData : phData?.results || []
    const tData = tResp.data?.data || tResp.data
    tasks.value = Array.isArray(tData) ? tData : tData?.results || []
    const teData = teResp.data?.data || teResp.data
    const allEntries = Array.isArray(teData) ? teData : teData?.results || []
    myEntries.value = allEntries // all visible to employee are their own
    const aData = aResp.data?.data || aResp.data
    assignments.value = Array.isArray(aData) ? aData : aData?.results || []
  } catch {
    // handled
  } finally {
    isLoading.value = false
  }
})

// Global progress
const totalBudgetHours = computed(() =>
  phases.value.reduce((sum, p) => sum + parseFloat(p.budgeted_hours || '0'), 0),
)
const totalActualHours = computed(() =>
  myEntries.value.reduce((sum, e) => sum + parseFloat(e.hours || '0'), 0),
)
const globalProgressPct = computed(() =>
  totalBudgetHours.value > 0 ? Math.round((totalActualHours.value / totalBudgetHours.value) * 100) : 0,
)

// My tasks (grouped by phase)
interface PhaseTaskGroup { phaseName: string; tasks: Task[] }
const myTasksByPhase = computed<PhaseTaskGroup[]>(() => {
  const map = new Map<string, Task[]>()
  for (const t of tasks.value) {
    const key = t.phase_name || 'Sans phase'
    if (!map.has(key)) map.set(key, [])
    map.get(key)!.push(t)
  }
  return Array.from(map.entries()).map(([phaseName, tasks]) => ({ phaseName, tasks }))
})

// My hours by phase
const myHoursByPhase = computed(() => {
  const map = new Map<number, number>()
  for (const e of myEntries.value) {
    const current = map.get(e.phase) || 0
    map.set(e.phase, current + parseFloat(e.hours || '0'))
  }
  return map
})

// Team members (from assignments)
interface TeamMember { name: string; phases: string[]; totalAllocation: number }
const teamMembers = computed<TeamMember[]>(() => {
  const map = new Map<string, TeamMember>()
  for (const a of assignments.value) {
    const name = a.employee_name || `Employe #${a.employee}`
    if (!map.has(name)) map.set(name, { name, phases: [], totalAllocation: 0 })
    const m = map.get(name)!
    if (a.phase_name && !m.phases.includes(a.phase_name)) m.phases.push(a.phase_name)
    m.totalAllocation += parseFloat(a.hours_per_week || '0')
  }
  return Array.from(map.values()).sort((a, b) => b.totalAllocation - a.totalAllocation)
})

function progressColor(pct: number) {
  if (pct < 50) return 'var(--color-primary)'
  if (pct < 80) return 'var(--color-success, #16A34A)'
  if (pct < 100) return '#D97706'
  return '#DC2626'
}
</script>

<template>
  <div>
    <div v-if="isLoading" class="text-center py-12 text-text-muted">Chargement...</div>

    <template v-else-if="project">
      <!-- Header -->
      <div class="mb-6">
        <button class="text-sm text-primary mb-2 hover:underline" @click="router.push('/projects')">
          &larr; Retour a mes projets
        </button>
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-semibold text-text">{{ project.name }}</h1>
            <p class="text-sm text-text-muted mt-1">
              <span class="font-mono font-semibold">{{ project.code }}</span>
              &middot; {{ project.client_name || 'Pas de client' }}
              &middot; {{ project.start_date }} &rarr; {{ project.end_date || 'En cours' }}
            </p>
          </div>
          <span class="rounded-full px-3 py-1 text-xs font-semibold" :class="project.status === 'ACTIVE' ? 'bg-success/10 text-success' : 'bg-text-muted/10 text-text-muted'">
            {{ project.status }}
          </span>
        </div>
      </div>

      <!-- Global progress -->
      <div class="grid grid-cols-3 gap-4 mb-6">
        <div class="rounded-lg border border-border bg-surface p-5">
          <p class="text-xs font-semibold uppercase text-text-muted mb-1">Avancement global</p>
          <p class="text-3xl font-bold font-mono" :style="{ color: progressColor(globalProgressPct) }">{{ globalProgressPct }}%</p>
          <div class="mt-2 h-2 rounded-full bg-border overflow-hidden">
            <div class="h-full rounded-full" :style="{ width: `${Math.min(100, globalProgressPct)}%`, background: progressColor(globalProgressPct) }"></div>
          </div>
          <p class="text-xs text-text-muted mt-2">{{ totalActualHours.toFixed(1) }}h realisees / {{ totalBudgetHours.toFixed(1) }}h budgetees</p>
        </div>
        <div class="rounded-lg border border-border bg-surface p-5">
          <p class="text-xs font-semibold uppercase text-text-muted mb-1">Mes heures sur ce projet</p>
          <p class="text-3xl font-bold font-mono text-primary">{{ totalActualHours.toFixed(1) }} h</p>
          <p class="text-xs text-text-muted mt-2">{{ myEntries.length }} entrees de temps</p>
        </div>
        <div class="rounded-lg border border-border bg-surface p-5">
          <p class="text-xs font-semibold uppercase text-text-muted mb-1">Phases du projet</p>
          <p class="text-3xl font-bold font-mono">{{ phases.length }}</p>
          <p class="text-xs text-text-muted mt-2">{{ phases.filter(p => !p.is_locked).length }} actives &middot; {{ phases.filter(p => p.is_locked).length }} verrouillees</p>
        </div>
      </div>

      <!-- Phases + My hours -->
      <div class="rounded-lg border border-border bg-surface mb-6">
        <div class="px-5 py-3 border-b border-border">
          <h2 class="text-sm font-semibold text-text">Phases du projet &mdash; Mes heures</h2>
        </div>
        <table class="w-full text-left text-sm">
          <thead class="text-xs font-medium uppercase tracking-wide text-text-muted">
            <tr>
              <th class="px-5 py-2">Phase</th>
              <th class="px-3 py-2">Mode</th>
              <th class="px-3 py-2 text-right">Budget heures</th>
              <th class="px-3 py-2 text-right">Mes heures</th>
              <th class="px-3 py-2">Avancement</th>
              <th class="px-3 py-2">Statut</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="ph in phases" :key="ph.id" class="border-t border-border hover:bg-surface-alt">
              <td class="px-5 py-2">
                <span class="font-medium">{{ ph.client_facing_label || ph.name }}</span>
              </td>
              <td class="px-3 py-2 text-text-muted text-xs">{{ ph.billing_mode }}</td>
              <td class="px-3 py-2 text-right font-mono">{{ parseFloat(ph.budgeted_hours || '0').toFixed(0) }}h</td>
              <td class="px-3 py-2 text-right font-mono font-semibold">{{ (myHoursByPhase.get(ph.id) || 0).toFixed(1) }}h</td>
              <td class="px-3 py-2" style="width: 120px;">
                <div class="h-1.5 rounded-full bg-border overflow-hidden">
                  <div
                    class="h-full rounded-full"
                    :style="{
                      width: `${Math.min(100, parseFloat(ph.budgeted_hours || '0') > 0 ? ((myHoursByPhase.get(ph.id) || 0) / parseFloat(ph.budgeted_hours)) * 100 : 0)}%`,
                      background: progressColor(parseFloat(ph.budgeted_hours || '0') > 0 ? ((myHoursByPhase.get(ph.id) || 0) / parseFloat(ph.budgeted_hours)) * 100 : 0),
                    }"
                  ></div>
                </div>
              </td>
              <td class="px-3 py-2">
                <span v-if="ph.is_locked" class="text-xs text-text-muted">🔒 Verrouillee</span>
                <span v-else class="text-xs text-success">Active</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- My tasks -->
      <div class="rounded-lg border border-border bg-surface mb-6">
        <div class="px-5 py-3 border-b border-border">
          <h2 class="text-sm font-semibold text-text">Mes taches</h2>
        </div>
        <div v-if="myTasksByPhase.length === 0" class="px-5 py-8 text-center text-text-muted text-sm">
          Aucune tache assignee sur ce projet.
        </div>
        <div v-else>
          <div v-for="group in myTasksByPhase" :key="group.phaseName" class="border-t border-border first:border-t-0">
            <div class="px-5 py-2 bg-surface-alt text-xs font-semibold text-text-muted uppercase">{{ group.phaseName }}</div>
            <table class="w-full text-left text-sm">
              <tbody>
                <tr v-for="task in group.tasks" :key="task.id" class="border-t border-border hover:bg-surface-alt">
                  <td class="px-5 py-2 font-mono text-xs text-text-muted" style="width: 80px;">{{ task.wbs_code }}</td>
                  <td class="px-3 py-2 font-medium">{{ task.client_facing_label || task.name }}</td>
                  <td class="px-3 py-2 text-right font-mono" style="width: 80px;">{{ parseFloat(task.budgeted_hours || '0').toFixed(0) }}h</td>
                  <td class="px-3 py-2 text-right" style="width: 80px;">
                    <span class="text-xs font-semibold" :style="{ color: progressColor(task.progress_pct || 0) }">{{ task.progress_pct || 0 }}%</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Team overview -->
      <div class="rounded-lg border border-border bg-surface">
        <div class="px-5 py-3 border-b border-border">
          <h2 class="text-sm font-semibold text-text">Equipe du projet</h2>
        </div>
        <div v-if="teamMembers.length === 0" class="px-5 py-8 text-center text-text-muted text-sm">
          Aucune affectation trouvee.
        </div>
        <table v-else class="w-full text-left text-sm">
          <thead class="text-xs font-medium uppercase tracking-wide text-text-muted">
            <tr>
              <th class="px-5 py-2">Nom</th>
              <th class="px-3 py-2">Phases</th>
              <th class="px-3 py-2 text-right">Allocation</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="m in teamMembers" :key="m.name" class="border-t border-border hover:bg-surface-alt">
              <td class="px-5 py-2 font-medium">{{ m.name }}</td>
              <td class="px-3 py-2 text-text-muted text-xs">{{ m.phases.join(', ') || '—' }}</td>
              <td class="px-3 py-2 text-right font-mono">{{ m.totalAllocation }}%</td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>

    <div v-else class="text-center py-12 text-text-muted">Projet introuvable.</div>
  </div>
</template>
