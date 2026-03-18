<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{
  value: string | number
  label: string
  type?: 'text' | 'number' | 'textarea'
  placeholder?: string
}>()

const emit = defineEmits<{
  save: [value: string | number]
}>()

const isEditing = ref(false)
const localValue = ref(props.value)
const showFeedback = ref(false)

watch(
  () => props.value,
  (v) => {
    localValue.value = v
  },
)

function startEdit() {
  isEditing.value = true
}

function onBlur() {
  isEditing.value = false
  if (localValue.value !== props.value) {
    emit('save', localValue.value)
    showFeedback.value = true
    setTimeout(() => {
      showFeedback.value = false
    }, 500)
  }
}
</script>

<template>
  <div>
    <label class="text-xs font-medium text-text-muted">{{ label }}</label>
    <div
      v-if="!isEditing"
      class="mt-0.5 cursor-pointer rounded px-2 py-1 text-sm transition-colors hover:bg-surface-alt"
      :class="{ 'bg-success/10': showFeedback }"
      @click="startEdit"
    >
      {{ value || placeholder || '—' }}
    </div>
    <textarea
      v-else-if="type === 'textarea'"
      v-model="localValue"
      class="mt-0.5 w-full rounded border border-primary/30 px-2 py-1 text-sm focus:border-primary focus:outline-none"
      rows="3"
      @blur="onBlur"
    />
    <input
      v-else
      v-model="localValue"
      :type="type || 'text'"
      class="mt-0.5 w-full rounded border border-primary/30 px-2 py-1 text-sm focus:border-primary focus:outline-none"
      @blur="onBlur"
      @keydown.enter="onBlur"
    >
  </div>
</template>
