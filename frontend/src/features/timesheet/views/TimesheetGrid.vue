<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useTimesheetStore } from '../stores/useTimesheetStore'
import TimesheetCell from '../components/TimesheetCell.vue'
import WeekNavigator from '../components/WeekNavigator.vue'
import SubmitWeekModal from '../components/SubmitWeekModal.vue'

import apiClient from '@/plugins/axios'

const store = useTimesheetStore()
const showSubmitModal = ref(false)
const showAddTask = ref(false)

// Add task with dropdowns
interface ProjectOption { id: number; code: string; name: string }
interface PhaseOption { id: number; name: string; client_facing_label: string }
const availableProjects = ref<ProjectOption[]>([])
const availablePhases = ref<PhaseOption[]>([])
const selectedProjectId = ref<number | null>(null)
const selectedPhaseId = ref<number | null>(null)

async function loadProjects() {
  try {
    const resp = await apiClient.get('projects/', { params: { status: 'ACTIVE' } })
    const data = resp.data?.data || resp.data
    availableProjects.value = Array.isArray(data) ? data : data?.results || []
  } catch { availableProjects.value = [] }
}

async function onProjectSelect() {
  availablePhases.value = []
  selectedPhaseId.value = null
  if (!selectedProjectId.value) return
  try {
    const resp = await apiClient.get(`projects/${selectedProjectId.value}/phases/`)
    const data = resp.data?.data || resp.data
    availablePhases.value = Array.isArray(data) ? data : data?.results || []
  } catch { availablePhases.value = [] }
}

const dayLabels = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']

// Favorites stored in localStorage
const favorites = ref<Set<number>>(new Set(JSON.parse(localStorage.getItem('ts_favorites') || '[]')))

function toggleFavorite(projectId: number) {
  if (favorites.value.has(projectId)) {
    favorites.value.delete(projectId)
  } else {
    favorites.value.add(projectId)
  }
  localStorage.setItem('ts_favorites', JSON.stringify([...favorites.value]))
}

function isFavorite(projectId: number) {
  return favorites.value.has(projectId)
}

onMounted(() => store.fetchWeek())

function onCellSave(projectId: number, phaseId: number | null, date: string, hours: string) {
  store.saveCell(projectId, phaseId, date, hours)
}

async function onSubmitConfirm() {
  await store.submitWeek()
  showSubmitModal.value = false
}

async function openAddTask() {
  showAddTask.value = true
  selectedProjectId.value = null
  selectedPhaseId.value = null
  availablePhases.value = []
  await loadProjects()
}

async function addTask() {
  if (!selectedProjectId.value) return
  // Use a minimal value to force creation (0 is skipped by saveCell)
  try {
    await apiClient.post('time_entries/', {
      project: selectedProjectId.value,
      phase: selectedPhaseId.value,
      date: store.weekDates[0] || '',
      hours: '0',
    })
  } catch { /* ok */ }
  showAddTask.value = false
  selectedProjectId.value = null
  selectedPhaseId.value = null
  await store.fetchWeek()
}

// Collect rejection reasons grouped by project/phase
interface RejectionInfo { project: string; phase: string; reason: string }
const rejectionReasons = computed<RejectionInfo[]>(() => {
  const seen = new Map<string, RejectionInfo>()
  for (const group of store.projectGroups) {
    for (const row of group.rows) {
      for (const date of store.weekDates) {
        const e = row.entries[date]
        if (e && e.rejection_reason) {
          const key = `${row.project_code}|${row.phase_name}|${e.rejection_reason}`
          if (!seen.has(key)) {
            seen.set(key, {
              project: row.project_code + ' — ' + row.project_name,
              phase: row.phase_name || row.client_label || '',
              reason: e.rejection_reason,
            })
          }
        }
      }
    }
  }
  return Array.from(seen.values())
})

// Row deletion — only if all entries on this row are DRAFT or empty
function canDeleteRow(row: { entries: Record<string, { status: string } | null>; is_locked: boolean }): boolean {
  if (row.is_locked || store.periodLocked) return false
  for (const date of store.weekDates) {
    const e = row.entries[date]
    if (e && e.status !== 'DRAFT') return false
  }
  return true
}

const deletingRow = ref(false)
// eslint-disable-next-line @typescript-eslint/no-explicit-any
async function handleRemoveRow(row: any) {
  if (deletingRow.value) return
  deletingRow.value = true
  try {
    const ids: number[] = []
    for (const date of store.weekDates) {
      const e = row.entries[date]
      if (e && e.id) ids.push(e.id)
    }
    if (ids.length === 0) return
    for (const id of ids) {
      try {
        await apiClient.delete(`time_entries/${id}/`)
      } catch { /* ignore 404 */ }
    }
    await store.fetchWeek()
  } finally {
    deletingRow.value = false
  }
}

function normClass(total: number, norm: number): string {
  if (total === 0) return 'text-text-muted'
  if (total === norm) return 'text-success font-medium'
  if (total > norm * 1.5) return 'text-danger font-medium'
  return 'text-warning font-medium'
}
</script>

<template>
  <div>
    <!-- Header -->
    <div class="mb-4 flex items-center justify-between">
      <h1 class="text-2xl font-semibold text-text">
        Feuilles de temps
      </h1>
      <div class="flex items-center gap-4">
        <WeekNavigator
          :week-start="store.currentWeekStart"
          @navigate="store.navigateWeek"
        />
      </div>
    </div>

    <!-- Status banner (HIGH #1) -->
    <div
      class="mb-4 flex items-center justify-between rounded-lg border p-3"
      :class="{
        'border-success/30 bg-success/5': store.statusMessage.color === 'green',
        'border-warning/30 bg-warning/5': store.statusMessage.color === 'amber',
        'border-border bg-surface-alt': store.statusMessage.color === 'gray',
      }"
    >
      <div class="flex items-center gap-2">
        <div
          class="h-2 w-2 rounded-full"
          :class="{
            'bg-success': store.statusMessage.color === 'green',
            'bg-warning': store.statusMessage.color === 'amber',
            'bg-text-muted': store.statusMessage.color === 'gray',
          }"
        />
        <span class="text-sm">
          Feuille {{ store.statusMessage.text === 'complete' ? 'complète' : 'en cours' }}
          — <strong>{{ store.weeklyTotal }}h saisies sur {{ store.WEEKLY_NORM }}h</strong>
        </span>
      </div>
      <span class="text-xs text-text-muted">Soumission avant samedi 18h</span>
    </div>

    <!-- Period locked banner -->
    <div
      v-if="store.periodLocked"
      class="mb-4 flex items-center gap-2 rounded-lg border border-danger/30 bg-danger/5 p-3"
    >
      <span>&#128274;</span>
      <span class="text-sm text-danger font-medium">
        Cette periode est verrouillee. Aucune modification n'est possible.
      </span>
    </div>

    <!-- Modification requested banner -->
    <div
      v-if="store.hasModificationRequested"
      class="mb-4 rounded-lg border border-warning/30 bg-warning/5 p-3"
    >
      <div class="flex items-center gap-2">
        <span class="text-warning">&#9998;</span>
        <span class="text-sm text-warning">
          <strong>Modification demandee</strong> — Certaines lignes ont ete renvoyees par votre CP pour correction.
          Les cellules editables sont celles qui necessitent votre attention.
        </span>
      </div>
      <div v-if="rejectionReasons.length" class="mt-2 ml-6">
        <div
          v-for="(info, idx) in rejectionReasons"
          :key="idx"
          class="flex items-start gap-2 text-sm text-text mt-1"
        >
          <span class="text-warning mt-0.5">&#8227;</span>
          <span><strong>{{ info.project }}</strong><template v-if="info.phase"> / {{ info.phase }}</template> : {{ info.reason }}</span>
        </div>
      </div>
    </div>

    <!-- Anomaly badge: average > contract -->
    <div
      v-if="store.weeklyStats.average_4_weeks > store.weeklyStats.contract_hours"
      class="mb-4 flex items-center gap-2 rounded-lg border border-warning/30 bg-warning/5 p-3"
    >
      <span class="text-warning">⚠️</span>
      <span class="text-sm text-warning">
        Votre moyenne sur 4 semaines est de {{ store.weeklyStats.average_4_weeks }}h
        — au-dessus de votre contrat de {{ store.weeklyStats.contract_hours }}h.
      </span>
    </div>

    <!-- KPI counters (HIGH #2) -->
    <div class="mb-6 grid grid-cols-4 gap-4">
      <div class="rounded-lg border border-border bg-surface p-4 text-center">
        <div class="text-2xl font-bold text-text">
          {{ store.weeklyTotal }}h
        </div>
        <div class="text-xs text-text-muted">
          Cette semaine
        </div>
        <div class="mt-1 h-2 rounded-full bg-border">
          <div
            class="h-2 rounded-full bg-primary"
            :style="{ width: Math.min(100, (store.weeklyTotal / store.WEEKLY_NORM) * 100) + '%' }"
          />
        </div>
      </div>
      <div class="rounded-lg border border-border bg-surface p-4 text-center">
        <div class="text-2xl font-bold text-success">
          {{ store.weeklyStats.contract_hours }}h
        </div>
        <div class="text-xs text-text-muted">
          Contrat
        </div>
      </div>
      <div class="rounded-lg border border-border bg-surface p-4 text-center">
        <div class="text-2xl font-bold text-text">
          {{ store.weeklyStats.average_4_weeks || '—' }}h
        </div>
        <div class="text-xs text-text-muted">
          Moyenne 4 sem.
        </div>
        <!-- Sparkline from real data -->
        <div class="mt-2 flex items-end justify-center gap-1">
          <div
            v-for="(val, i) in store.weeklyStats.week_totals"
            :key="i"
            class="w-2 rounded-sm"
            :class="val > 45 ? 'bg-danger' : val > 40 ? 'bg-warning' : 'bg-primary'"
            :style="{ height: Math.max(3, Math.round((val / 50) * 28)) + 'px' }"
            :title="val + 'h'"
          />
        </div>
        <div class="mt-1 text-text-muted" style="font-size: 9px;">
          {{ store.weeklyStats.week_totals.map((v: number) => Math.round(v)).join(' → ') }}
        </div>
      </div>
      <div class="rounded-lg border border-border bg-surface p-4 text-center">
        <div class="text-2xl font-bold text-primary">
          {{ store.weeklyStats.billable_rate_percent || '—' }}%
        </div>
        <div class="text-xs text-text-muted">
          Taux facturable
        </div>
      </div>
    </div>

    <!-- Action buttons -->
    <div class="mb-4 flex gap-3">
      <button
        class="flex items-center gap-2 rounded-lg border border-primary/20 bg-primary/5 px-4 py-2 text-sm font-medium text-primary hover:bg-primary/10"
        @click="store.copyPreviousWeek()"
      >
        Copier semaine précédente
      </button>
      <button
        class="flex items-center gap-2 rounded-lg border border-border bg-surface px-4 py-2 text-sm font-medium text-text-muted hover:bg-surface-alt"
        @click="openAddTask"
      >
        + Ajouter une tâche
      </button>
    </div>

    <!-- Add task form -->
    <div v-if="showAddTask" class="mb-4 rounded-lg border border-primary/20 bg-primary/5 p-3">
      <div class="flex items-end gap-3">
        <div style="min-width: 250px;">
          <label class="text-xs font-medium text-text-muted">Projet *</label>
          <select v-model="selectedProjectId" @change="onProjectSelect" class="mt-1 block w-full rounded border border-border px-2 py-1.5 text-sm">
            <option :value="null">— Choisir un projet —</option>
            <option v-for="p in availableProjects" :key="p.id" :value="p.id">{{ p.code }} — {{ p.name }}</option>
          </select>
        </div>
        <div v-if="availablePhases.length" style="min-width: 200px;">
          <label class="text-xs font-medium text-text-muted">Phase</label>
          <select v-model="selectedPhaseId" class="mt-1 block w-full rounded border border-border px-2 py-1.5 text-sm">
            <option :value="null">— Toutes phases —</option>
            <option v-for="ph in availablePhases" :key="ph.id" :value="ph.id">{{ ph.client_facing_label || ph.name }}</option>
          </select>
        </div>
        <button class="btn-primary" :disabled="!selectedProjectId" @click="addTask">Ajouter</button>
        <button class="btn-ghost" @click="showAddTask = false">Annuler</button>
      </div>
    </div>

    <!-- Grid with project grouping (HIGH #3) -->
    <div class="overflow-x-auto rounded-lg border border-border bg-surface">
      <table class="w-full" style="font-size: 12px;">
        <thead class="border-b border-border bg-surface-alt">
          <tr>
            <th class="sticky left-0 z-10 bg-surface-alt px-3 py-1 text-left font-medium uppercase text-text-muted min-w-[200px]" style="font-size: 10px;">
              Tache
            </th>
            <th
              v-for="(date, i) in store.weekDates"
              :key="date"
              class="min-w-[60px] px-1 py-1 text-center font-medium text-text-muted"
              style="font-size: 10px;"
            >
              {{ dayLabels[i] }} {{ date.slice(8) }}
            </th>
            <th class="min-w-[50px] px-1 py-1 text-center font-medium text-text-muted" style="font-size: 10px;">
              Total
            </th>
          </tr>
        </thead>
        <tbody>
          <template
            v-for="group in store.projectGroups"
            :key="group.project_id"
          >
            <!-- Project header row -->
            <tr class="border-b bg-primary/5">
              <td
                :colspan="store.weekDates.length + 2"
                class="px-3 py-1 font-semibold uppercase tracking-wide text-primary"
                style="font-size: 10px;"
              >
                <span class="flex items-center gap-1">
                  <button
                    style="font-size: 12px;"
                    :class="isFavorite(group.project_id) ? 'text-warning' : 'text-text-muted/30 hover:text-warning/60'"
                    @click.stop="toggleFavorite(group.project_id)"
                  >
                    {{ isFavorite(group.project_id) ? '★' : '☆' }}
                  </button>
                  {{ group.project_code }} — {{ group.project_name }}
                </span>
              </td>
            </tr>

            <!-- Phase rows within project -->
            <tr
              v-for="row in group.rows"
              :key="`${row.project_id}-${row.phase_id}`"
              class="border-b border-border hover:bg-surface-alt"
              :class="{ 'bg-gray-50 opacity-60': row.is_locked }"
            >
              <td class="sticky left-0 z-10 bg-surface px-3 py-1 pl-6">
                <div class="flex items-center gap-1">
                  <span
                    v-if="row.is_locked"
                    class="text-text-muted"
                    style="font-size: 10px;"
                  >🔒</span>
                  <span class="text-text" style="font-size: 11px;">{{ row.client_label || row.phase_name }}</span>
                  <button
                    v-if="canDeleteRow(row)"
                    class="ml-auto"
                    style="color: #DC2626; font-size: 13px; font-weight: bold; cursor: pointer; padding: 2px 6px; line-height: 1;"
                    title="Retirer cette ligne"
                    @click="handleRemoveRow(row)"
                  >&#10005;</button>
                </div>
              </td>
              <TimesheetCell
                v-for="date in store.weekDates"
                :key="date"
                :entry="row.entries[date] || null"
                :project-id="row.project_id"
                :phase-id="row.phase_id"
                :date="date"
                :is-locked="row.is_locked || store.periodLocked || (row.entries[date]?.status !== undefined && row.entries[date]?.status !== 'DRAFT')"
                :aria-label="`${row.project_code} ${row.phase_name} ${date}`"
                @save="onCellSave"
              />
              <td class="px-1 py-1 text-center font-mono font-semibold text-text" style="font-size: 11px;">
                {{ row.row_total || '' }}
              </td>
            </tr>
          </template>

          <!-- Empty state -->
          <tr v-if="!store.projectGroups.length && !store.isLoading">
            <td
              :colspan="store.weekDates.length + 2"
              class="px-4 py-8 text-center text-text-muted"
            >
              Aucun projet assigné pour cette semaine
            </td>
          </tr>

          <!-- Daily totals row -->
          <tr
            v-if="store.projectGroups.length"
            class="border-t-2 border-border bg-surface-alt font-semibold"
          >
            <td class="sticky left-0 z-10 bg-surface-alt px-4 py-3 text-sm text-text">
              Total journalier
            </td>
            <td
              v-for="(total, i) in store.dailyTotals"
              :key="i"
              class="px-3 py-3 text-center font-mono text-sm"
              :class="normClass(total, store.DAILY_NORM)"
            >
              {{ total || '' }}
            </td>
            <td class="px-3 py-3 text-center">
              <span class="text-lg font-bold text-text">{{ store.weeklyTotal }}h</span>
              <span class="block text-xs text-text-muted">/ {{ store.WEEKLY_NORM }}h</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Submit button -->
    <div class="mt-4 flex items-center justify-between">
      <span class="text-xs text-success">Sauvegarde automatique active</span>
      <button
        class="rounded-lg px-6 py-2.5 font-medium text-white shadow-sm"
        :class="store.allSubmitted ? 'bg-gray-300 cursor-not-allowed' : 'bg-primary hover:bg-primary-light'"
        :disabled="store.allSubmitted"
        @click="showSubmitModal = true"
      >
        {{ store.allSubmitted ? 'Feuille deja soumise' : 'Soumettre la feuille de temps' }}
      </button>
    </div>

    <!-- Submit modal -->
    <SubmitWeekModal
      :open="showSubmitModal"
      :weekly-total="store.weeklyTotal"
      :weekly-norm="store.WEEKLY_NORM"
      @close="showSubmitModal = false"
      @confirm="onSubmitConfirm"
    />
  </div>
</template>
