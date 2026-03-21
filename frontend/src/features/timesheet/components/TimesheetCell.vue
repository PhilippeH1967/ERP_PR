<script setup lang="ts">
import { ref, watch } from 'vue'
import type { TimeEntry } from '../types/timesheet.types'

const props = defineProps<{
  entry: TimeEntry | null
  projectId: number
  phaseId: number | null
  date: string
  isLocked: boolean
  ariaLabel?: string
}>()

const emit = defineEmits<{
  save: [projectId: number, phaseId: number | null, date: string, hours: string]
}>()

const localValue = ref(props.entry ? props.entry.hours : '')
const showFeedback = ref(false)
const showError = ref(false)

watch(
  () => props.entry?.hours,
  (newVal) => {
    if (newVal !== undefined) localValue.value = newVal
  },
)

async function onBlur() {
  const val = localValue.value.toString().trim()
  const original = props.entry?.hours || ''
  if (val === original) return
  if (val === '' && !props.entry) return

  // Validate: max 15h per cell, no negative
  const numVal = parseFloat(val || '0')
  if (numVal < 0) {
    localValue.value = original
    showError.value = true
    setTimeout(() => { showError.value = false }, 1500)
    return
  }
  if (numVal > 15) {
    localValue.value = original
    showError.value = true
    setTimeout(() => { showError.value = false }, 1500)
    return
  }

  showError.value = false
  try {
    emit('save', props.projectId, props.phaseId, props.date, val || '0')
    showFeedback.value = true
    setTimeout(() => {
      showFeedback.value = false
    }, 500)
  } catch {
    showError.value = true
    localValue.value = original
  }
}

function onKeydown(event: KeyboardEvent) {
  if (event.key === 'ArrowUp' || event.key === 'ArrowDown') {
    event.preventDefault()
    const el = event.target as HTMLInputElement
    // Skip disabled (locked) cells
    const selector = `input[data-col="${props.date}"]:not(:disabled)`
    const cells = Array.from(
      el.closest('table')?.querySelectorAll(selector) || [],
    ) as HTMLInputElement[]
    const idx = cells.indexOf(el)
    const next = event.key === 'ArrowDown' ? cells[idx + 1] : cells[idx - 1]
    next?.focus()
  }
}
</script>

<template>
  <td class="px-0 py-0">
    <input
      v-model="localValue"
      type="number"
      step="0.5"
      min="0"
      max="15"
      :aria-label="ariaLabel || `${date}`"
      class="h-10 w-full border-0 bg-transparent px-2 text-center font-mono text-sm focus:bg-primary/5 focus:outline-none"
      :class="{
        'bg-success/10': showFeedback,
        'bg-danger/10': showError,
        'bg-gray-100 text-text-muted cursor-not-allowed': isLocked,
      }"
      :disabled="isLocked"
      :data-col="date"
      @blur="onBlur"
      @keydown="onKeydown"
    >
  </td>
</template>
