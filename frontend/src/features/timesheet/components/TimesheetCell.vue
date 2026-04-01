<script setup lang="ts">
import { ref, watch } from 'vue'
import type { TimeEntry } from '../types/timesheet.types'
import { useTimesheetStore } from '../stores/useTimesheetStore'

const store = useTimesheetStore()
const errorMessage = ref('')

const props = defineProps<{
  entry: TimeEntry | null
  projectId: number
  phaseId: number | null
  date: string
  isLocked: boolean
  isInvoiced?: boolean
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
    errorMessage.value = 'Max 15h par cellule'
    setTimeout(() => { showError.value = false; errorMessage.value = '' }, 2000)
    return
  }

  // Check daily total
  const check = store.canSaveHours(props.projectId, props.phaseId, props.date, val || '0')
  if (!check.ok) {
    localValue.value = original
    showError.value = true
    errorMessage.value = check.message
    setTimeout(() => { showError.value = false; errorMessage.value = '' }, 3000)
    return
  }

  showError.value = false
  errorMessage.value = ''
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
  <td class="px-0 py-0" style="position:relative;">
    <span v-if="isInvoiced" class="invoiced-badge" title="Facture">$</span>
    <div v-if="errorMessage" class="cell-error-tooltip">{{ errorMessage }}</div>
    <input
      v-model="localValue"
      type="number"
      step="0.5"
      min="0"
      max="15"
      :aria-label="ariaLabel || `${date}`"
      class="w-full border-0 bg-transparent px-1 text-center font-mono focus:bg-primary/5 focus:outline-none"
      style="height: 28px; font-size: 11px;"
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

<style scoped>
/* Hide number input spinners */
input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
input[type="number"] {
  -moz-appearance: textfield;
}

.invoiced-badge {
  position: absolute;
  top: 1px;
  right: 2px;
  font-size: 8px;
  font-weight: 700;
  color: #15803D;
  background: #DCFCE7;
  border-radius: 2px;
  padding: 0 2px;
  line-height: 1.2;
  z-index: 5;
  pointer-events: none;
}

.cell-error-tooltip {
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  background: #DC2626;
  color: white;
  font-size: 10px;
  padding: 3px 8px;
  border-radius: 4px;
  white-space: nowrap;
  z-index: 100;
  pointer-events: none;
}
</style>
