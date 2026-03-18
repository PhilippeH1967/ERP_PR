<script setup lang="ts">
import { onMounted } from 'vue'
import { useProjectStore } from '../stores/useProjectStore'
import ProjectWizard from '../components/ProjectWizard.vue'

const store = useProjectStore()
onMounted(() => store.fetchTemplates())
</script>

<template>
  <ProjectWizard />
</template>
