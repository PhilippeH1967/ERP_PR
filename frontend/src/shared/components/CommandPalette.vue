<script setup lang="ts">
/**
 * CommandPalette — Cmd+K universal search (Sprint 2 - B3).
 */
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/plugins/axios'

const router = useRouter()
const isOpen = ref(false)
const query = ref('')
const results = ref<Array<{ type: string; id: number; title: string; subtitle: string; url: string }>>([])
const isLoading = ref(false)
const selectedIndex = ref(0)
const inputRef = ref<HTMLInputElement | null>(null)

const typeLabels: Record<string, string> = { project: 'Projets', client: 'Clients', invoice: 'Factures', employee: 'Employes' }
const typeIcons: Record<string, string> = { project: '📁', client: '🤝', invoice: '📄', employee: '👤' }

function open() {
  isOpen.value = true
  query.value = ''
  results.value = []
  selectedIndex.value = 0
  nextTick(() => inputRef.value?.focus())
}
function close() { isOpen.value = false }

// Keyboard shortcut
function onKeydown(e: KeyboardEvent) {
  if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
    e.preventDefault()
    isOpen.value ? close() : open()
  }
  if (e.key === 'Escape' && isOpen.value) close()
}
onMounted(() => document.addEventListener('keydown', onKeydown))
onUnmounted(() => document.removeEventListener('keydown', onKeydown))

// Navigation
function onModalKeydown(e: KeyboardEvent) {
  if (e.key === 'ArrowDown') { e.preventDefault(); selectedIndex.value = Math.min(selectedIndex.value + 1, results.value.length - 1) }
  if (e.key === 'ArrowUp') { e.preventDefault(); selectedIndex.value = Math.max(selectedIndex.value - 1, 0) }
  if (e.key === 'Enter') {
    const r = results.value[selectedIndex.value]
    if (r) selectResult(r)
  }
}

function selectResult(r: { url: string }) {
  close()
  router.push(r.url)
}

// Debounced search
let searchTimer: ReturnType<typeof setTimeout> | null = null
watch(query, (q) => {
  if (searchTimer) clearTimeout(searchTimer)
  const trimmed = q.trim()
  if (trimmed.length < 2) { results.value = []; return }
  isLoading.value = true
  searchTimer = setTimeout(async () => {
    try {
      const resp = await apiClient.get('search/', { params: { q: trimmed } })
      results.value = resp.data?.data?.results || []
    } catch { results.value = [] }
    finally { isLoading.value = false }
    selectedIndex.value = 0
  }, 300)
})

// Group results by type
function groupedResults() {
  const map = new Map<string, typeof results.value>()
  for (const r of results.value) {
    if (!map.has(r.type)) map.set(r.type, [])
    map.get(r.type)!.push(r)
  }
  return map
}

function flatIndex(type: string, idx: number): number {
  let flat = 0
  for (const [t, items] of groupedResults()) {
    if (t === type) return flat + idx
    flat += items.length
  }
  return flat
}
</script>

<template>
  <Teleport to="body">
    <div v-if="isOpen" class="cp-overlay" @click.self="close">
      <div class="cp-modal" @keydown="onModalKeydown">
        <div class="cp-search">
          <span class="cp-search-icon">&#128269;</span>
          <input
            ref="inputRef"
            v-model="query"
            class="cp-input"
            placeholder="Rechercher un projet, client, facture..."
            autocomplete="off"
          >
          <kbd class="cp-kbd">ESC</kbd>
        </div>

        <div class="cp-results">
          <div v-if="isLoading" class="cp-empty">Recherche en cours...</div>
          <div v-else-if="query.trim().length >= 2 && results.length === 0" class="cp-empty">
            Aucun resultat pour "{{ query }}"
          </div>
          <div v-else-if="query.trim().length < 2 && results.length === 0" class="cp-empty cp-hint">
            Tapez au moins 2 caracteres pour rechercher
          </div>
          <template v-else>
            <div v-for="[type, items] of groupedResults()" :key="type">
              <div class="cp-group-label">{{ typeLabels[type] || type }}</div>
              <div
                v-for="(r, i) in items"
                :key="r.id"
                class="cp-result"
                :class="{ selected: flatIndex(type, i) === selectedIndex }"
                @click="selectResult(r)"
                @mouseenter="selectedIndex = flatIndex(type, i)"
              >
                <span class="cp-result-icon">{{ typeIcons[r.type] || '📋' }}</span>
                <div class="cp-result-text">
                  <div class="cp-result-title">{{ r.title }}</div>
                  <div v-if="r.subtitle" class="cp-result-sub">{{ r.subtitle }}</div>
                </div>
                <span class="cp-result-arrow">&#8594;</span>
              </div>
            </div>
          </template>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.cp-overlay { position: fixed; inset: 0; z-index: 9999; background: rgba(0,0,0,0.5); display: flex; align-items: flex-start; justify-content: center; padding-top: 20vh; }
.cp-modal { width: 600px; max-height: 400px; background: white; border-radius: 12px; box-shadow: 0 25px 50px rgba(0,0,0,0.25); overflow: hidden; display: flex; flex-direction: column; }
.cp-search { display: flex; align-items: center; gap: 10px; padding: 14px 16px; border-bottom: 1px solid #E5E7EB; }
.cp-search-icon { font-size: 18px; color: #9CA3AF; }
.cp-input { flex: 1; border: none; outline: none; font-size: 15px; color: #111827; background: transparent; }
.cp-input::placeholder { color: #9CA3AF; }
.cp-kbd { font-size: 10px; font-family: monospace; padding: 2px 6px; background: #F3F4F6; border: 1px solid #D1D5DB; border-radius: 4px; color: #6B7280; }
.cp-results { flex: 1; overflow-y: auto; padding: 8px 0; }
.cp-empty { padding: 24px 16px; text-align: center; font-size: 13px; color: #9CA3AF; }
.cp-hint { font-style: italic; }
.cp-group-label { padding: 8px 16px 4px; font-size: 10px; font-weight: 700; color: #9CA3AF; text-transform: uppercase; letter-spacing: 0.5px; }
.cp-result { display: flex; align-items: center; gap: 10px; padding: 8px 16px; cursor: pointer; transition: background 0.1s; }
.cp-result:hover, .cp-result.selected { background: #EFF6FF; }
.cp-result-icon { font-size: 16px; width: 24px; text-align: center; }
.cp-result-text { flex: 1; min-width: 0; }
.cp-result-title { font-size: 13px; font-weight: 600; color: #111827; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.cp-result-sub { font-size: 11px; color: #6B7280; margin-top: 1px; }
.cp-result-arrow { font-size: 12px; color: #9CA3AF; }
</style>
