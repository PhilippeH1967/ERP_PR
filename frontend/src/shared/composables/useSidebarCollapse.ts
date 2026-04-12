/**
 * useSidebarCollapse — Manages collapsed/expanded sidebar sections.
 * Persisted in localStorage. Sprint 2 — B7.
 */
import { ref } from 'vue'

const STORAGE_KEY = 'pr-erp-sidebar-collapsed'

function load(): string[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : []
  } catch {
    return []
  }
}

function save(collapsed: string[]) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(collapsed))
}

const collapsedSections = ref<string[]>(load())

export function useSidebarCollapse() {
  function isCollapsed(sectionLabel: string): boolean {
    return collapsedSections.value.includes(sectionLabel)
  }

  function toggleSection(sectionLabel: string): void {
    const idx = collapsedSections.value.indexOf(sectionLabel)
    if (idx >= 0) {
      collapsedSections.value.splice(idx, 1)
    } else {
      collapsedSections.value.push(sectionLabel)
    }
    save(collapsedSections.value)
  }

  return { isCollapsed, toggleSection, collapsedSections }
}
