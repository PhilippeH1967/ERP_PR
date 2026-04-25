import { setActivePinia, createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'

vi.mock('../features/timesheet/api/timesheetApi', () => ({
  timesheetApi: { week: vi.fn(), submitWeek: vi.fn() },
}))
vi.mock('@/plugins/axios', () => ({ default: { get: vi.fn(), post: vi.fn() } }))

import { useTimesheetStore } from '../features/timesheet/stores/useTimesheetStore'
import type { TimeEntry } from '../features/timesheet/types/timesheet.types'

function entry(over: Partial<TimeEntry>): TimeEntry {
  return {
    id: Math.random(),
    employee: 1,
    project: 1,
    project_code: 'P-001',
    project_name: 'Default',
    phase: null,
    phase_name: '',
    client_label: '',
    task: null,
    task_wbs_code: '',
    task_name: '',
    date: '2026-04-20',
    hours: '0',
    notes: '',
    rejection_reason: '',
    status: 'DRAFT',
    is_favorite: false,
    is_invoiced: false,
    invoiced_on: null,
    category: 'BILLABLE',
    ...over,
  } as TimeEntry
}

describe('useTimesheetStore — favoris localStorage', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    localStorage.clear()
  })

  it('trie un projet marqué favori (localStorage) avant les autres', () => {
    const store = useTimesheetStore()
    store.entries = [
      entry({ project: 10, project_code: 'P-010', project_name: 'Alpha' }),
      entry({ project: 20, project_code: 'P-020', project_name: 'Beta' }),
      entry({ project: 30, project_code: 'P-030', project_name: 'Gamma' }),
    ]
    store.toggleFavorite(20)
    const codes = store.projectGroups.map(g => g.project_code)
    expect(codes[0]).toBe('P-020')
  })

  it('trie alphabétiquement les projets non-favoris', () => {
    const store = useTimesheetStore()
    store.entries = [
      entry({ project: 30, project_code: 'P-030', project_name: 'Gamma' }),
      entry({ project: 10, project_code: 'P-010', project_name: 'Alpha' }),
      entry({ project: 20, project_code: 'P-020', project_name: 'Beta' }),
    ]
    const codes = store.projectGroups.map(g => g.project_code)
    expect(codes).toEqual(['P-010', 'P-020', 'P-030'])
  })

  it('persiste le toggle favori dans localStorage', () => {
    const store = useTimesheetStore()
    store.toggleFavorite(42)
    const stored = JSON.parse(localStorage.getItem('ts_favorites') || '[]')
    expect(stored).toContain(42)
    store.toggleFavorite(42)
    const after = JSON.parse(localStorage.getItem('ts_favorites') || '[]')
    expect(after).not.toContain(42)
  })

  it('isFavorite reflète l\'état du store', () => {
    const store = useTimesheetStore()
    expect(store.isFavorite(7)).toBe(false)
    store.toggleFavorite(7)
    expect(store.isFavorite(7)).toBe(true)
  })

  it('hydrate les favoris depuis localStorage à l\'init', () => {
    localStorage.setItem('ts_favorites', JSON.stringify([99, 100]))
    setActivePinia(createPinia())
    const store = useTimesheetStore()
    expect(store.isFavorite(99)).toBe(true)
    expect(store.isFavorite(100)).toBe(true)
    expect(store.isFavorite(1)).toBe(false)
  })
})
