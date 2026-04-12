/**
 * useSidebarConfig — Manages user sidebar favorites.
 * Syncs with backend /sidebar/config/. Sprint 2 — B2.
 */
import { ref } from 'vue'
import apiClient from '@/plugins/axios'

const favorites = ref<string[]>([])
const loaded = ref(false)

async function fetchConfig() {
  try {
    const resp = await apiClient.get('sidebar/config/')
    const data = resp.data?.data || resp.data
    favorites.value = data?.favorites || []
    loaded.value = true
  } catch { /* silent */ }
}

async function toggleFavorite(key: string) {
  const idx = favorites.value.indexOf(key)
  const prev = [...favorites.value]
  if (idx >= 0) favorites.value.splice(idx, 1)
  else favorites.value.push(key)
  try {
    await apiClient.patch('sidebar/config/', { favorites: favorites.value })
  } catch {
    favorites.value = prev // rollback
  }
}

function isFavorite(key: string): boolean {
  return favorites.value.includes(key)
}

export function useSidebarConfig() {
  if (!loaded.value) fetchConfig()
  return { favorites, isFavorite, toggleFavorite, fetchConfig }
}
