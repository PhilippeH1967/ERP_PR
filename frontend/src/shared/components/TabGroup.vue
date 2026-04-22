<script setup lang="ts">
import { computed } from 'vue'

interface SubTab { key: string; label: string }
interface RootTab { key: string; label: string; subTabs?: SubTab[] }

const props = defineProps<{
  tabs: RootTab[]
  rootTab: string
  subTab: string | null
  storageKey: string
}>()

const emit = defineEmits<{ update: [{ rootTab: string; subTab: string | null }] }>()

const activeRoot = computed(() => props.tabs.find(t => t.key === props.rootTab) || props.tabs[0])
const subTabs = computed<SubTab[]>(() => activeRoot.value?.subTabs || [])

function readMemory(): Record<string, string> {
  try { return JSON.parse(sessionStorage.getItem(props.storageKey) || '{}') } catch { return {} }
}

function writeMemory(rootKey: string, subKey: string) {
  const mem = readMemory()
  mem[rootKey] = subKey
  sessionStorage.setItem(props.storageKey, JSON.stringify(mem))
}

function selectRoot(root: RootTab) {
  if (!root.subTabs || root.subTabs.length === 0) {
    emit('update', { rootTab: root.key, subTab: null })
    return
  }
  const mem = readMemory()
  const remembered = mem[root.key]
  const knownKeys = root.subTabs.map(s => s.key)
  const target = remembered && knownKeys.includes(remembered) ? remembered : root.subTabs[0]!.key
  emit('update', { rootTab: root.key, subTab: target })
}

function selectSub(sub: SubTab) {
  writeMemory(props.rootTab, sub.key)
  emit('update', { rootTab: props.rootTab, subTab: sub.key })
}
</script>

<template>
  <div class="tab-group">
    <div class="tab-root-bar" role="tablist">
      <button
        v-for="t in tabs"
        :key="t.key"
        data-tab-root
        class="tab-root-btn"
        :class="{ active: t.key === rootTab }"
        role="tab"
        :aria-selected="t.key === rootTab"
        @click="selectRoot(t)"
      >
        {{ t.label }}
      </button>
    </div>
    <div v-if="subTabs.length" class="tab-sub-bar" role="tablist">
      <button
        v-for="s in subTabs"
        :key="s.key"
        data-tab-sub
        class="tab-sub-btn"
        :class="{ active: s.key === subTab }"
        role="tab"
        :aria-selected="s.key === subTab"
        @click="selectSub(s)"
      >
        {{ s.label }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.tab-group { border-bottom: 1px solid var(--color-gray-200); margin-bottom: 16px; }
.tab-root-bar { display: flex; gap: 4px; padding: 0 4px; }
.tab-root-btn {
  background: none; border: none; padding: 10px 16px; font-size: 13px; font-weight: 600;
  color: var(--color-gray-500); cursor: pointer; border-bottom: 2px solid transparent;
  transition: color 0.15s, border-color 0.15s;
}
.tab-root-btn:hover { color: var(--color-gray-700); }
.tab-root-btn.active { color: var(--color-primary); border-bottom-color: var(--color-primary); }

.tab-sub-bar {
  display: flex; gap: 2px; padding: 6px 12px;
  background: var(--color-gray-50); border-top: 1px solid var(--color-gray-200);
}
.tab-sub-btn {
  background: none; border: none; padding: 4px 10px; font-size: 12px; font-weight: 500;
  color: var(--color-gray-600); cursor: pointer; border-radius: 4px;
  transition: background 0.12s, color 0.12s;
}
.tab-sub-btn:hover { background: var(--color-gray-200); }
.tab-sub-btn.active { background: var(--color-primary); color: white; }
</style>
