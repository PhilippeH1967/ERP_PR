<script setup lang="ts">
import { onMounted } from 'vue'
import { useTimesheetStore } from '../stores/useTimesheetStore'

const store = useTimesheetStore()
const days = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']

onMounted(() => store.fetchEntries())
</script>

<template>
  <div>
    <div class="mb-6 flex items-center justify-between">
      <h1 class="text-2xl font-semibold text-text">
        Feuille de temps
      </h1>
      <button
        class="rounded-md bg-primary px-4 py-2 text-sm font-medium text-white"
        @click="store.submitWeek('2026-03-16')"
      >
        Soumettre la semaine
      </button>
    </div>

    <div class="overflow-x-auto rounded-lg border border-border bg-surface">
      <table class="w-full text-sm">
        <thead class="border-b border-border text-xs font-medium uppercase tracking-wide text-text-muted">
          <tr>
            <th class="sticky left-0 bg-surface px-4 py-3 text-left">
              Projet / Phase
            </th>
            <th
              v-for="day in days"
              :key="day"
              class="min-w-[80px] px-3 py-3 text-center"
            >
              {{ day }}
            </th>
            <th class="px-3 py-3 text-center font-mono">
              Total
            </th>
          </tr>
        </thead>
        <tbody>
          <tr class="border-b border-border text-center text-text-muted">
            <td
              class="sticky left-0 bg-surface px-4 py-8 text-left"
              :colspan="days.length + 2"
            >
              Chargement des projets assignés...
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
