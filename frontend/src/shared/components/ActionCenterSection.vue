<script setup lang="ts">
/**
 * ActionCenterSection — "A faire" section at top of sidebar (Sprint 2 - B1).
 */
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/plugins/axios'

const router = useRouter()

interface ActionItem {
  key: string; label: string; count: number; icon: string; color: string; url: string
}

const actions = ref<ActionItem[]>([])
const totalCount = ref(0)
let timer: ReturnType<typeof setInterval> | null = null

async function fetchActions() {
  try {
    const resp = await apiClient.get('action_center/')
    const data = resp.data?.data || resp.data
    actions.value = (data?.actions || []).filter((a: ActionItem) => a.count > 0)
    totalCount.value = data?.total_count || 0
  } catch { actions.value = [] }
}

onMounted(() => {
  fetchActions()
  timer = setInterval(fetchActions, 60000)
})
onUnmounted(() => { if (timer) clearInterval(timer) })

defineExpose({ totalCount })

const colorMap: Record<string, string> = {
  danger: '#DC2626', warning: '#D97706', primary: '#2563EB', success: '#16A34A',
}
</script>

<template>
  <div v-if="actions.length > 0" class="ac-section">
    <div class="ac-header">
      <span class="ac-title">A faire</span>
      <span class="ac-badge">{{ totalCount }}</span>
    </div>
    <div
      v-for="action in actions.slice(0, 5)"
      :key="action.key"
      class="ac-item"
      @click="router.push(action.url)"
    >
      <span class="ac-dot" :style="{ background: colorMap[action.color] || '#9CA3AF' }"></span>
      <span class="ac-label">{{ action.label }}</span>
      <span class="ac-count">{{ action.count }}</span>
    </div>
    <div v-if="actions.length > 5" class="ac-more" @click="router.push('/dashboard')">
      Voir tout ({{ actions.length }})
    </div>
  </div>
</template>

<style scoped>
.ac-section { border-bottom: 1px solid var(--color-gray-200, #E5E7EB); padding: 8px 0 6px; }
.ac-header { display: flex; align-items: center; justify-content: space-between; padding: 4px 20px 6px; }
.ac-title { font-size: 10px; font-weight: 700; color: var(--color-gray-400, #9CA3AF); text-transform: uppercase; letter-spacing: 0.5px; }
.ac-badge { font-size: 10px; font-weight: 700; color: white; background: #DC2626; width: 18px; height: 18px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
.ac-item { display: flex; align-items: center; gap: 8px; padding: 5px 20px 5px 28px; font-size: 12px; color: var(--color-gray-600, #4B5563); cursor: pointer; transition: background 0.1s; }
.ac-item:hover { background: var(--color-gray-200, #E5E7EB); }
.ac-dot { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }
.ac-label { flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.ac-count { font-size: 11px; font-weight: 700; color: var(--color-gray-500, #6B7280); background: var(--color-gray-100, #F3F4F6); padding: 1px 7px; border-radius: 8px; }
.ac-more { padding: 4px 28px; font-size: 10px; color: var(--color-primary, #2563EB); cursor: pointer; font-weight: 600; }
.ac-more:hover { text-decoration: underline; }
</style>
