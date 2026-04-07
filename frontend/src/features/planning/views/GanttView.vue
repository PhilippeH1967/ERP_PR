<script setup lang="ts">
import { useRoute } from 'vue-router'
import GanttChart from '../components/GanttChart.vue'

const route = useRoute()
const projectId = Number(route.params.projectId || route.query.project || 0)
</script>

<template>
  <div>
    <h1 class="mb-6 text-2xl font-semibold text-text">Gantt projet</h1>
    <div v-if="!projectId" class="rounded-lg border border-border bg-surface p-8 text-center text-text-muted">
      Sélectionnez un projet pour afficher le diagramme de Gantt
    </div>
    <GanttChart v-else :project-id="projectId" />
  </div>
</template>
