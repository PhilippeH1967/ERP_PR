import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'

vi.mock('@/plugins/axios', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    patch: vi.fn(),
    delete: vi.fn(),
  },
}))

import apiClient from '@/plugins/axios'
import { useTimesheetStore } from '@/features/timesheet/stores/useTimesheetStore'
import type { TimeEntry } from '@/features/timesheet/types/timesheet.types'

const makeEntry = (overrides: Partial<TimeEntry> = {}): TimeEntry => ({
  id: 1,
  employee: 1,
  project: 10,
  phase: 20,
  date: '2026-03-16',
  hours: '7.5',
  notes: '',
  status: 'DRAFT',
  is_favorite: false,
  version: 1,
  ...overrides,
})

describe('useTimesheetStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('gridRows transforms entries into project×phase rows', () => {
    const store = useTimesheetStore()
    store.entries = [
      makeEntry({ id: 1, project: 10, phase: 20, date: '2026-03-16', hours: '7.5' }),
      makeEntry({ id: 2, project: 10, phase: 20, date: '2026-03-17', hours: '8.0' }),
      makeEntry({ id: 3, project: 11, phase: 30, date: '2026-03-16', hours: '4.0' }),
    ]

    expect(store.gridRows).toHaveLength(2)
    expect(store.gridRows[0]?.project_id).toBe(10)
    expect(store.gridRows[1]?.project_id).toBe(11)
  })

  it('calculates row totals correctly', () => {
    const store = useTimesheetStore()
    store.currentWeekStart = '2026-03-16'
    store.entries = [
      makeEntry({ id: 1, project: 10, phase: 20, date: '2026-03-16', hours: '7.5' }),
      makeEntry({ id: 2, project: 10, phase: 20, date: '2026-03-17', hours: '8.0' }),
    ]

    expect(store.gridRows[0]?.row_total).toBe(15.5)
  })

  it('calculates daily totals correctly', () => {
    const store = useTimesheetStore()
    store.currentWeekStart = '2026-03-16'
    store.entries = [
      makeEntry({ id: 1, project: 10, phase: 20, date: '2026-03-16', hours: '7.5' }),
      makeEntry({ id: 2, project: 11, phase: 30, date: '2026-03-16', hours: '4.0' }),
    ]

    // Monday (index 0) should be 11.5
    expect(store.dailyTotals[0]).toBe(11.5)
  })

  it('calculates weekly total', () => {
    const store = useTimesheetStore()
    store.currentWeekStart = '2026-03-16'
    store.entries = [
      makeEntry({ id: 1, date: '2026-03-16', hours: '8' }),
      makeEntry({ id: 2, date: '2026-03-17', hours: '8' }),
      makeEntry({ id: 3, date: '2026-03-18', hours: '8', project: 11, phase: 30 }),
    ]

    expect(store.weeklyTotal).toBe(24)
  })

  it('fetchWeek calls API with date range', async () => {
    vi.mocked(apiClient.get).mockResolvedValue({ data: { data: [] } })
    const store = useTimesheetStore()
    store.currentWeekStart = '2026-03-16'

    await store.fetchWeek()

    expect(apiClient.get).toHaveBeenCalledWith('time_entries/', {
      params: { date__gte: '2026-03-16', date__lte: expect.any(String) },
    })
  })

  it('saveCell calls createEntry for new cell', async () => {
    vi.mocked(apiClient.post).mockResolvedValue({ data: { data: makeEntry({ id: 99 }) } })
    const store = useTimesheetStore()
    store.entries = []

    await store.saveCell(10, 20, '2026-03-16', '7.5')

    expect(apiClient.post).toHaveBeenCalledWith('time_entries/', {
      project: 10,
      phase: 20,
      date: '2026-03-16',
      hours: '7.5',
    })
  })

  it('saveCell calls updateEntry for existing cell', async () => {
    const existing = makeEntry({ id: 5, project: 10, phase: 20, date: '2026-03-16', version: 2 })
    vi.mocked(apiClient.patch).mockResolvedValue({ data: { data: { ...existing, hours: '8' } } })
    const store = useTimesheetStore()
    store.entries = [existing]

    await store.saveCell(10, 20, '2026-03-16', '8')

    expect(apiClient.patch).toHaveBeenCalledWith(
      'time_entries/5/',
      { hours: '8' },
      { headers: { 'If-Match': '2' } },
    )
  })
})
