import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { timesheetApi } from '../api/timesheetApi'
import type { TimeEntry, TimesheetGridRow, TimesheetWeek } from '../types/timesheet.types'

const DAILY_NORM = 8
const WEEKLY_NORM = 40

function getDatesForWeek(weekStart: string): string[] {
  const dates: string[] = []
  const start = new Date(weekStart)
  for (let i = 0; i < 7; i++) {
    const d = new Date(start)
    d.setDate(start.getDate() + i)
    dates.push(d.toISOString().slice(0, 10))
  }
  return dates
}

function getMondayOfWeek(d: Date): string {
  const date = new Date(d)
  const day = date.getDay()
  const diff = date.getDate() - day + (day === 0 ? -6 : 1)
  date.setDate(diff)
  return date.toISOString().slice(0, 10)
}

export const useTimesheetStore = defineStore('timesheet', () => {
  const entries = ref<TimeEntry[]>([])
  const locks = ref<Array<{ phase: number | null; person: number | null }>>([])
  const isLoading = ref(false)
  const currentWeekStart = ref(getMondayOfWeek(new Date()))

  const weekDates = computed(() => getDatesForWeek(currentWeekStart.value))
  const weekEnd = computed(() => weekDates.value[6] || '')

  function safeHours(hours: string | number | undefined): number {
    const n = Number(hours)
    return Number.isFinite(n) ? n : 0
  }

  function roundTotal(n: number): number {
    return Math.round(n * 100) / 100
  }

  const gridRows = computed<TimesheetGridRow[]>(() => {
    const rowMap = new Map<string, TimesheetGridRow>()
    for (const entry of entries.value) {
      const key = `${entry.project}-${entry.phase === null ? '_null_' : entry.phase}`
      if (!rowMap.has(key)) {
        rowMap.set(key, {
          project_id: entry.project,
          project_code: `P-${entry.project}`,
          project_name: `Project ${entry.project}`,
          phase_id: entry.phase,
          phase_name: entry.phase ? `Phase ${entry.phase}` : '',
          client_label: entry.phase ? `Phase ${entry.phase}` : '',
          entries: {},
          is_locked: false,
          row_total: 0,
        })
      }
      const row = rowMap.get(key)
      if (row) row.entries[entry.date] = entry
    }
    for (const row of rowMap.values()) {
      row.row_total = roundTotal(
        weekDates.value.reduce((sum, date) => sum + safeHours(row.entries[date]?.hours), 0),
      )
      if (row.phase_id) {
        row.is_locked = locks.value.some((l) => l.phase === row.phase_id)
      }
    }
    return Array.from(rowMap.values())
  })

  const dailyTotals = computed(() =>
    weekDates.value.map((date) =>
      roundTotal(
        gridRows.value.reduce((sum, row) => sum + safeHours(row.entries[date]?.hours), 0),
      ),
    ),
  )

  const weeklyTotal = computed(() => roundTotal(dailyTotals.value.reduce((a, b) => a + b, 0)))

  const currentWeek = computed<TimesheetWeek>(() => ({
    weekStart: currentWeekStart.value,
    weekEnd: weekEnd.value,
    dates: weekDates.value,
    rows: gridRows.value,
    dailyTotals: dailyTotals.value,
    weeklyTotal: weeklyTotal.value,
    weeklyNorm: WEEKLY_NORM,
  }))

  async function fetchWeek() {
    isLoading.value = true
    try {
      const params = { date__gte: currentWeekStart.value, date__lte: weekEnd.value }
      const response = await timesheetApi.listEntries(params)
      entries.value = response.data?.data || response.data || []
      try {
        const lockResp = await timesheetApi.listLocks()
        locks.value = lockResp.data?.data || lockResp.data || []
      } catch {
        locks.value = []
      }
    } finally {
      isLoading.value = false
    }
  }

  function navigateWeek(direction: 'prev' | 'next') {
    const current = new Date(currentWeekStart.value)
    current.setDate(current.getDate() + (direction === 'next' ? 7 : -7))
    currentWeekStart.value = current.toISOString().slice(0, 10)
    fetchWeek()
  }

  const saveError = ref<{ type: string; entryId?: number } | null>(null)

  async function saveCell(projectId: number, phaseId: number | null, date: string, hours: string) {
    saveError.value = null
    const existing = entries.value.find(
      (e) => e.project === projectId && e.phase === phaseId && e.date === date,
    )
    try {
      if (existing) {
        const resp = await timesheetApi.updateEntry(existing.id, { hours }, existing.version)
        const updated = resp.data?.data || resp.data
        const idx = entries.value.findIndex((e) => e.id === existing.id)
        if (idx >= 0 && updated) entries.value[idx] = updated
      } else if (hours !== '0' && hours !== '') {
        const resp = await timesheetApi.createEntry({
          project: projectId, phase: phaseId, date, hours,
        })
        const created = resp.data?.data || resp.data
        if (created) entries.value.push(created)
      }
    } catch (err: unknown) {
      const axiosErr = err as { response?: { status: number } }
      if (axiosErr.response?.status === 409) {
        saveError.value = { type: 'conflict', entryId: existing?.id }
      } else {
        saveError.value = { type: 'error' }
      }
      throw err
    }
  }

  async function submitWeek() {
    await timesheetApi.submitWeek(currentWeekStart.value)
    await fetchWeek()
  }

  return {
    entries, isLoading, saveError, currentWeekStart, currentWeek, gridRows,
    dailyTotals, weeklyTotal, weekDates, fetchWeek, navigateWeek,
    saveCell, submitWeek, DAILY_NORM, WEEKLY_NORM,
  }
})
