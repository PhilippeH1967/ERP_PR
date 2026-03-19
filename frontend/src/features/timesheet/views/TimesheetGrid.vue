<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useTimesheetStore } from '../stores/useTimesheetStore'
import TimesheetCell from '../components/TimesheetCell.vue'
import WeekNavigator from '../components/WeekNavigator.vue'
import SubmitWeekModal from '../components/SubmitWeekModal.vue'

const store = useTimesheetStore()
const showSubmitModal = ref(false)
const showAddTask = ref(false)
const newTask = ref({ project_id: '', phase_id: '' })

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

async function addTask() {
  if (!newTask.value.project_id) return
  // Create a 0h entry to make the row appear
  await store.saveCell(
    Number(newTask.value.project_id),
    newTask.value.phase_id ? Number(newTask.value.phase_id) : null,
    store.weekDates[0],
    '0',
  )
  showAddTask.value = false
  newTask.value = { project_id: '', phase_id: '' }
  await store.fetchWeek()
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
        <!-- Sparkline (Fix #9) -->
        <div class="mt-2 flex items-end justify-center gap-0.5">
          <div
            class="w-1.5 rounded-sm bg-warning"
            style="height: 16px"
          />
          <div
            class="w-1.5 rounded-sm bg-warning"
            style="height: 18px"
          />
          <div
            class="w-1.5 rounded-sm bg-danger"
            style="height: 22px"
          />
          <div
            class="w-1.5 rounded-sm bg-warning"
            style="height: 14px"
          />
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
        @click="showAddTask = !showAddTask"
      >
        + Ajouter une tâche
      </button>
    </div>

    <!-- Add task form -->
    <div v-if="showAddTask" class="mb-4 flex items-end gap-3 rounded-lg border border-primary/20 bg-primary/5 p-3">
      <div>
        <label class="text-xs font-medium text-text-muted">Projet ID</label>
        <input v-model="newTask.project_id" type="number" class="mt-1 block w-32 rounded border border-border px-2 py-1 text-sm" placeholder="ID projet" />
      </div>
      <div>
        <label class="text-xs font-medium text-text-muted">Phase ID (optionnel)</label>
        <input v-model="newTask.phase_id" type="number" class="mt-1 block w-32 rounded border border-border px-2 py-1 text-sm" placeholder="ID phase" />
      </div>
      <button class="btn-primary" @click="addTask">Ajouter</button>
      <button class="btn-ghost" @click="showAddTask = false">Annuler</button>
    </div>

    <!-- Grid with project grouping (HIGH #3) -->
    <div class="overflow-x-auto rounded-lg border border-border bg-surface">
      <table class="w-full text-sm">
        <thead class="border-b border-border bg-surface-alt">
          <tr>
            <th class="sticky left-0 z-10 bg-surface-alt px-4 py-2 text-left text-xs font-medium uppercase text-text-muted min-w-[250px]">
              Tâche
            </th>
            <th
              v-for="(date, i) in store.weekDates"
              :key="date"
              class="min-w-[80px] px-3 py-2 text-center text-xs font-medium text-text-muted"
            >
              {{ dayLabels[i] }} {{ date.slice(8) }}
            </th>
            <th class="min-w-[70px] px-3 py-2 text-center text-xs font-medium text-text-muted">
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
                class="px-4 py-2 text-xs font-semibold uppercase tracking-wide text-primary"
              >
                <span class="flex items-center gap-1">
                  <button
                    class="text-sm"
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
              <td class="sticky left-0 z-10 bg-surface px-4 py-2 pl-8">
                <div class="flex items-center gap-2">
                  <span
                    v-if="row.is_locked"
                    class="text-text-muted"
                  >🔒</span>
                  <span class="text-sm text-text">{{ row.client_label || row.phase_name }}</span>
                </div>
              </td>
              <TimesheetCell
                v-for="date in store.weekDates"
                :key="date"
                :entry="row.entries[date] || null"
                :project-id="row.project_id"
                :phase-id="row.phase_id"
                :date="date"
                :is-locked="row.is_locked"
                :aria-label="`${row.project_code} ${row.phase_name} ${date}`"
                @save="onCellSave"
              />
              <td class="px-3 py-2 text-center font-mono text-sm font-semibold text-text">
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
      <button class="text-sm text-text-muted hover:text-text">
        Sauvegarder brouillon
      </button>
      <button
        class="rounded-lg bg-primary px-6 py-2.5 font-medium text-white shadow-sm hover:bg-primary-light"
        @click="showSubmitModal = true"
      >
        Soumettre la feuille de temps
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
