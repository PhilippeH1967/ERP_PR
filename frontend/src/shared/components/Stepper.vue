<script setup lang="ts">
import { computed } from 'vue'

interface Step {
  key: string
  label: string
}

const props = defineProps<{
  steps: Step[]
  currentKey: string
  rejectedKey?: string | null
  rejectedTooltip?: string
}>()

const currentIndex = computed(() => {
  const i = props.steps.findIndex(s => s.key === props.currentKey)
  return i === -1 ? 0 : i
})

const rejected = computed(() => Boolean(props.rejectedKey))

function state(index: number): 'done' | 'active' | 'todo' | 'rejected' {
  if (rejected.value && props.steps[index]?.key === props.rejectedKey) return 'rejected'
  if (index < currentIndex.value) return 'done'
  if (index === currentIndex.value) return 'active'
  return 'todo'
}
</script>

<template>
  <div class="stepper" role="progressbar" :aria-valuenow="currentIndex + 1" :aria-valuemin="1" :aria-valuemax="steps.length">
    <template v-for="(step, i) in steps" :key="step.key">
      <div class="stepper-node" :class="['stepper-' + state(i)]" :title="state(i) === 'rejected' ? rejectedTooltip : undefined">
        <span class="stepper-dot">
          <span v-if="state(i) === 'done'">&#10003;</span>
          <span v-else-if="state(i) === 'rejected'">&#10005;</span>
          <span v-else>{{ i + 1 }}</span>
        </span>
        <span class="stepper-label">{{ step.label }}</span>
      </div>
      <div v-if="i < steps.length - 1" class="stepper-bar" :class="{ 'stepper-bar-done': state(i) === 'done' }"></div>
    </template>
  </div>
</template>

<style scoped>
.stepper { display: flex; align-items: center; gap: 4px; padding: 8px 0; }
.stepper-node { display: flex; flex-direction: column; align-items: center; gap: 4px; min-width: 64px; }
.stepper-dot {
  width: 24px; height: 24px; border-radius: 50%;
  display: inline-flex; align-items: center; justify-content: center;
  font-size: 11px; font-weight: 700;
  background: var(--color-gray-200); color: var(--color-gray-500);
  border: 2px solid var(--color-gray-200);
  transition: all 0.15s;
}
.stepper-label { font-size: 10px; font-weight: 600; color: var(--color-gray-500); text-align: center; }
.stepper-bar { flex: 1; height: 2px; background: var(--color-gray-200); margin-bottom: 18px; }
.stepper-bar-done { background: var(--color-success); }
.stepper-done .stepper-dot { background: var(--color-success); border-color: var(--color-success); color: white; }
.stepper-done .stepper-label { color: var(--color-success); }
.stepper-active .stepper-dot { background: var(--color-primary); border-color: var(--color-primary); color: white; box-shadow: 0 0 0 3px var(--color-primary-light); }
.stepper-active .stepper-label { color: var(--color-primary); }
.stepper-rejected .stepper-dot { background: var(--color-danger); border-color: var(--color-danger); color: white; }
.stepper-rejected .stepper-label { color: var(--color-danger); }
</style>
