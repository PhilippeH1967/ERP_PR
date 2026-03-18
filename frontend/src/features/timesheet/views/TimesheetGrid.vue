<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useTimesheetStore } from '../stores/useTimesheetStore'
import TimesheetCell from '../components/TimesheetCell.vue'
import WeekNavigator from '../components/WeekNavigator.vue'
import SubmitWeekModal from '../components/SubmitWeekModal.vue'

const store = useTimesheetStore()
const showSubmitModal = ref(false)

const dayLabels = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']

onMounted(() => store.fetchWeek())

function onCellSave(projectId: number, phaseId: number | null, date: string, hours: string) {
  store.saveCell(projectId, phaseId, date, hours)
}

async function onSubmitConfirm() {
  await store.submitWeek()
  showSubmitModal.value = false
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
    <div class="mb-6 flex items-center justify-between">
      <h1 class="text-2xl font-semibold text-text">
        Feuille de temps
      </h1>
      <div class="flex items-center gap-4">
        <WeekNavigator
          :week-start="store.currentWeekStart"
          @navigate="store.navigateWeek"
        />
        <button
          class="rounded-md bg-primary px-4 py-2 text-sm font-medium text-white"
          @click="showSubmitModal = true"
        >
          Soumettre la semaine
        </button>
      </div>
    </div>

    <!-- Weekly progress -->
    <div class="mb-4 flex items-center gap-3">
      <div class="h-2 flex-1 rounded-full bg-border">
        <div
          class="h-2 rounded-full transition-all"
          :class="store.weeklyTotal >= store.WEEKLY_NORM ? 'bg-success' : 'bg-primary'"
          :style="{ width: Math.min(100, (store.weeklyTotal / store.WEEKLY_NORM) * 100) + '%' }"
        />
      </div>
      <span
        class="text-sm font-mono"
        :class="normClass(store.weeklyTotal, store.WEEKLY_NORM)"
      >
        {{ store.weeklyTotal }}/{{ store.WEEKLY_NORM }}h
      </span>
    </div>

    <!-- Grid -->
    <div class="overflow-x-auto rounded-lg border border-border bg-surface">
      <table class="w-full text-sm">
        <thead class="border-b border-border text-xs font-medium uppercase tracking-wide text-text-muted">
          <tr>
            <th class="sticky left-0 z-10 bg-surface px-4 py-3 text-left min-w-[200px]">
              Projet / Phase
            </th>
            <th
              v-for="(date, i) in store.weekDates"
              :key="date"
              class="min-w-[80px] px-1 py-3 text-center"
            >
              <div>{{ dayLabels[i] }}</div>
              <div class="text-[10px] font-normal">
                {{ date.slice(5) }}
              </div>
            </th>
            <th class="min-w-[70px] px-2 py-3 text-center font-mono">
              Total
            </th>
          </tr>
        </thead>
        <tbody>
          <!-- Data rows -->
          <tr
            v-for="row in store.gridRows"
            :key="`${row.project_id}-${row.phase_id}`"
            class="border-b border-border last:border-0"
            :class="{ 'bg-gray-50 opacity-60': row.is_locked }"
          >
            <td class="sticky left-0 z-10 bg-surface px-4 py-2">
              <div class="flex items-center gap-2">
                <span
                  v-if="row.is_locked"
                  class="text-text-muted"
                >🔒</span>
                <div>
                  <span class="font-mono text-xs text-text-muted">{{ row.project_code }}</span>
                  <span class="ml-2 text-sm">{{ row.client_label || row.phase_name }}</span>
                </div>
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
              @save="onCellSave"
            />
            <td class="px-2 py-2 text-center font-mono text-sm font-medium">
              {{ row.row_total || '' }}
            </td>
          </tr>

          <!-- Empty state -->
          <tr v-if="!store.gridRows.length && !store.isLoading">
            <td
              :colspan="store.weekDates.length + 2"
              class="px-4 py-8 text-center text-text-muted"
            >
              Aucun projet assigné pour cette semaine
            </td>
          </tr>

          <!-- Daily totals -->
          <tr
            v-if="store.gridRows.length"
            class="border-t-2 border-border bg-surface-alt font-medium"
          >
            <td class="sticky left-0 z-10 bg-surface-alt px-4 py-2 text-xs uppercase text-text-muted">
              Total jour
            </td>
            <td
              v-for="(total, i) in store.dailyTotals"
              :key="i"
              class="px-1 py-2 text-center font-mono text-sm"
              :class="normClass(total, store.DAILY_NORM)"
            >
              {{ total || '' }}
            </td>
            <td
              class="px-2 py-2 text-center font-mono text-sm"
              :class="normClass(store.weeklyTotal, store.WEEKLY_NORM)"
            >
              {{ store.weeklyTotal }}
            </td>
          </tr>
        </tbody>
      </table>
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
