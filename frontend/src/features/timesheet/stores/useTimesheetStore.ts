import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { timesheetApi } from '../api/timesheetApi'
import type {
  TimeEntry,
  TimesheetGridRow,
  TimesheetProjectGroup,
  TimesheetWeek,
} from '../types/timesheet.types'

const DAILY_NORM = 8
const WEEKLY_NORM = 40
const CONTRACT_HOURS = 40

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

function safeHours(hours: string | number | undefined): number {
  const n = Number(hours)
  return Number.isFinite(n) ? n : 0
}

function roundTotal(n: number): number {
  return Math.round(n * 100) / 100
}

export const useTimesheetStore = defineStore('timesheet', () => {
  const entries = ref<TimeEntry[]>([])
  const locks = ref<Array<{ phase: number | null; person: number | null }>>([])
  const isLoading = ref(false)
  const currentWeekStart = ref(getMondayOfWeek(new Date()))
  const saveError = ref<{ type: string; entryId?: number } | null>(null)
  const weeklyStats = ref({ contract_hours: 40, average_4_weeks: 0, billable_rate_percent: 0 })

  const weekDates = computed(() => getDatesForWeek(currentWeekStart.value))
  const weekEnd = computed(() => weekDates.value[6] || '')

  // Build flat rows
  const gridRows = computed<TimesheetGridRow[]>(() => {
    const rowMap = new Map<string, TimesheetGridRow>()
    for (const entry of entries.value) {
      const key = `${entry.project}-${entry.phase === null ? '_null_' : entry.phase}`
      if (!rowMap.has(key)) {
        rowMap.set(key, {
          project_id: entry.project,
          project_code: entry.project_code || `P-${entry.project}`,
          project_name: entry.project_name || `Project ${entry.project}`,
          phase_id: entry.phase,
          phase_name: entry.phase_name || '',
          client_label: entry.client_label || entry.phase_name || '',
          entries: {},
          is_locked: false,
          row_total: 0,
          is_favorite: entry.is_favorite,
          category: 'project',
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

  // Group rows by project (mockup conformity)
  const projectGroups = computed<TimesheetProjectGroup[]>(() => {
    const groupMap = new Map<number, TimesheetProjectGroup>()
    for (const row of gridRows.value) {
      if (!groupMap.has(row.project_id)) {
        groupMap.set(row.project_id, {
          project_id: row.project_id,
          project_code: row.project_code,
          project_name: row.project_name,
          is_favorite: row.is_favorite,
          category: row.category,
          rows: [],
          group_total: 0,
        })
      }
      const group = groupMap.get(row.project_id)
      if (group) {
        group.rows.push(row)
        group.group_total = roundTotal(group.group_total + row.row_total)
      }
    }
    // Sort: favorites first, then by project code
    return Array.from(groupMap.values()).sort((a, b) => {
      if (a.is_favorite && !b.is_favorite) return -1
      if (!a.is_favorite && b.is_favorite) return 1
      return a.project_code.localeCompare(b.project_code)
    })
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
    groups: projectGroups.value,
    dailyTotals: dailyTotals.value,
    weeklyTotal: weeklyTotal.value,
    weeklyNorm: WEEKLY_NORM,
    contractHours: weeklyStats.value.contract_hours || CONTRACT_HOURS,
  }))

  // Status banner
  const statusMessage = computed(() => {
    if (weeklyTotal.value >= WEEKLY_NORM) return { text: 'complete', color: 'green' }
    if (weeklyTotal.value > 0) return { text: 'en-cours', color: 'amber' }
    return { text: 'vide', color: 'gray' }
  })

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
      try {
        const statsResp = await timesheetApi.weeklyStats()
        const stats = statsResp.data?.data || statsResp.data
        if (stats?.contract_hours) weeklyStats.value = stats
      } catch {
        // Stats are optional
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

  async function saveCell(
    projectId: number,
    phaseId: number | null,
    date: string,
    hours: string,
  ) {
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
          project: projectId,
          phase: phaseId,
          date,
          hours,
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

  async function copyPreviousWeek() {
    await timesheetApi.copyPreviousWeek(currentWeekStart.value)
    await fetchWeek()
  }

  return {
    entries, isLoading, saveError, currentWeekStart, currentWeek,
    gridRows, projectGroups, dailyTotals, weeklyTotal, weekDates,
    weeklyStats, statusMessage, fetchWeek, navigateWeek, saveCell,
    submitWeek, copyPreviousWeek,
    DAILY_NORM, WEEKLY_NORM, CONTRACT_HOURS,
  }
})
