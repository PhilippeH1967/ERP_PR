<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{
  message: string
  type?: 'success' | 'error' | 'warning' | 'info'
  duration?: number
}>()

const emit = defineEmits<{
  dismiss: []
}>()

const visible = ref(true)

const typeClasses: Record<string, string> = {
  success: 'bg-success/10 text-success border-success/30',
  error: 'bg-danger/10 text-danger border-danger/30',
  warning: 'bg-warning/10 text-warning border-warning/30',
  info: 'bg-primary/10 text-primary border-primary/30',
}

watch(
  () => props.message,
  () => {
    visible.value = true
    if (props.duration !== 0) {
      setTimeout(() => {
        visible.value = false
        emit('dismiss')
      }, props.duration || 5000)
    }
  },
  { immediate: true },
)
</script>

<template>
  <div
    v-if="visible"
    class="fixed right-4 top-4 z-50 max-w-sm rounded-md border px-4 py-3 text-sm shadow-lg"
    :class="typeClasses[type || 'info']"
  >
    {{ message }}
  </div>
</template>
