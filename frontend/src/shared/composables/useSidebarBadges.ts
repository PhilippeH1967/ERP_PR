/**
 * useSidebarBadges — Fetches badge counts, health indicators, and freshness.
 * Polls every 60 seconds. Sprint 2 — B4 + B5.
 */
import { ref, onMounted, onUnmounted } from 'vue'
import apiClient from '@/plugins/axios'

const badges = ref<Record<string, number>>({})
const health = ref<Record<string, string>>({})
const hasNew = ref<Record<string, boolean>>({})
const isLoaded = ref(false)
let timer: ReturnType<typeof setInterval> | null = null
let consumers = 0

async function fetchBadges() {
  try {
    const resp = await apiClient.get('sidebar/badges/')
    const data = resp.data?.data || resp.data
    if (data) {
      badges.value = data.badges || {}
      health.value = data.health || {}
      hasNew.value = data.has_new || {}
      isLoaded.value = true
    }
  } catch { /* silent */ }
}

export function useSidebarBadges() {
  onMounted(() => {
    consumers++
    if (consumers === 1) {
      fetchBadges()
      timer = setInterval(fetchBadges, 60000)
    }
  })
  onUnmounted(() => {
    consumers--
    if (consumers === 0 && timer) {
      clearInterval(timer)
      timer = null
    }
  })
  return { badges, health, hasNew, isLoaded }
}
