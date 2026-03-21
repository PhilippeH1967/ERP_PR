<script setup lang="ts">
import { computed } from 'vue'
import { useLocale } from '@/shared/composables/useLocale'

const props = defineProps<{
  weekStart: string
}>()

const emit = defineEmits<{
  navigate: [direction: 'prev' | 'next' | 'today']
}>()

const { fmt } = useLocale()

function getMondayOfToday(): string {
  const d = new Date()
  const day = d.getDay()
  const diff = d.getDate() - day + (day === 0 ? -6 : 1)
  d.setDate(diff)
  return d.toISOString().slice(0, 10)
}

const isCurrentWeek = computed(() => props.weekStart === getMondayOfToday())
</script>

<template>
  <div class="flex items-center gap-3">
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
    <button
      v-if="!isCurrentWeek"
      class="rounded-md px-2 py-1 text-xs font-medium text-primary hover:bg-primary/10"
      @click="emit('navigate', 'today')"
    >
      Aujourd'hui
    </button>
  </div>
</template>
