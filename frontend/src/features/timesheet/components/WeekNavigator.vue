<script setup lang="ts">
import { useLocale } from '@/shared/composables/useLocale'

defineProps<{
  weekStart: string
}>()

const emit = defineEmits<{
  navigate: [direction: 'prev' | 'next']
}>()

const { fmt } = useLocale()
</script>

<template>
  <div class="flex items-center gap-4">
    <button
      class="rounded-md px-3 py-1 text-sm text-text-muted hover:bg-surface-alt"
      @click="emit('navigate', 'prev')"
    >
      ◀
    </button>
    <span class="text-sm font-medium text-text">
      Semaine du {{ fmt.date(weekStart) }}
    </span>
    <button
      class="rounded-md px-3 py-1 text-sm text-text-muted hover:bg-surface-alt"
      @click="emit('navigate', 'next')"
    >
      ▶
    </button>
  </div>
</template>
