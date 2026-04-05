import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import apiClient from '@/plugins/axios'
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
  const weeklyStats = ref({ contract_hours: 40, average_4_weeks: 0, billable_rate_percent: 0, week_totals: [0, 0, 0, 0] as number[] })

  const weekDates = computed(() => getDatesForWeek(currentWeekStart.value))
  const weekEnd = computed(() => weekDates.value[6] || '')

  // Build flat rows — keyed by project+task (or project+phase for legacy entries)
  const gridRows = computed<TimesheetGridRow[]>(() => {
    const rowMap = new Map<string, TimesheetGridRow>()
    for (const entry of entries.value) {
      // Key by task if available, fallback to phase
      const key = entry.task
        ? `${entry.project}-T${entry.task}`
        : `${entry.project}-P${entry.phase === null ? '_null_' : entry.phase}`
      if (!rowMap.has(key)) {
        rowMap.set(key, {
          project_id: entry.project,
          project_code: entry.project_code || `P-${entry.project}`,
          project_name: entry.project_name || `Project ${entry.project}`,
          phase_id: entry.phase,
          phase_name: entry.phase_name || '',
          task_id: entry.task || null,
          task_name: entry.task_name || '',
          task_wbs_code: entry.task_wbs_code || '',
          client_label: entry.client_label || entry.task_name || entry.phase_name || '',
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
      const hasLock = row.phase_id ? locks.value.some((l) => l.phase === row.phase_id) : false
      row.is_locked = hasLock
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

  const MAX_DAILY_HOURS = 15

  function getDailyTotal(date: string): number {
    return roundTotal(
      gridRows.value.reduce((sum, row) => sum + safeHours(row.entries[date]?.hours), 0),
    )
  }

  function canSaveHours(projectId: number, phaseId: number | null, date: string, newHours: string, taskId?: number | null): { ok: boolean; message: string } {
    const newVal = parseFloat(newHours || '0')
    // Get current value for this cell — match by task first, fallback to phase
    const row = taskId
      ? gridRows.value.find(r => r.project_id === projectId && r.task_id === taskId)
      : gridRows.value.find(r => r.project_id === projectId && r.phase_id === phaseId)
    const currentVal = row?.entries[date] ? safeHours(row.entries[date]?.hours) : 0
    const diff = newVal - currentVal
    const currentDayTotal = getDailyTotal(date)
    const newDayTotal = roundTotal(currentDayTotal + diff)

    if (newDayTotal > MAX_DAILY_HOURS) {
      return { ok: false, message: `Total journalier dépasserait ${MAX_DAILY_HOURS}h (actuellement ${currentDayTotal}h + ${newVal}h = ${newDayTotal}h)` }
    }
    return { ok: true, message: '' }
  }

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

  // Period locked — checked globally via API
  const periodLocked = ref(false)

  // Detect if some entries were sent back for modification (DRAFT mixed with SUBMITTED on same week)
  const hasModificationRequested = computed(() => {
    const statuses = new Set<string>()
    for (const row of gridRows.value) {
      for (const date of weekDates.value) {
        const e = row.entries[date]
        if (e) statuses.add(e.status)
      }
    }
    return statuses.has('DRAFT') && statuses.has('SUBMITTED')
  })

  // All submitted — no DRAFT entries remaining
  const allSubmitted = computed(() => {
    let hasEntries = false
    for (const row of gridRows.value) {
      for (const date of weekDates.value) {
        const e = row.entries[date]
        if (e) {
          hasEntries = true
          if (e.status === 'DRAFT') return false
        }
      }
    }
    return hasEntries
  })

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
        const lockCheckResp = await apiClient.get('time_entries/is_period_locked/', { params: { week_start: currentWeekStart.value } })
        const lockData = lockCheckResp.data?.data || lockCheckResp.data
        periodLocked.value = lockData?.locked || false
      } catch {
        periodLocked.value = false
      }
      try {
        const statsResp = await timesheetApi.weeklyStats(currentWeekStart.value)
        const stats = statsResp.data?.data || statsResp.data
        if (stats) weeklyStats.value = { ...weeklyStats.value, ...stats }
      } catch {
        // Stats are optional
      }
    } finally {
      isLoading.value = false
    }
  }

  async function navigateWeek(direction: 'prev' | 'next' | 'today') {
    if (direction === 'today') {
      currentWeekStart.value = getMondayOfWeek(new Date())
    } else {
      const current = new Date(currentWeekStart.value)
      current.setDate(current.getDate() + (direction === 'next' ? 7 : -7))
      currentWeekStart.value = current.toISOString().slice(0, 10)
    }
    entries.value = [] // Clear immediately to avoid stale rows
    periodLocked.value = false // Reset until fetchWeek updates it
    await fetchWeek()
  }

  async function saveCell(
    projectId: number,
    phaseId: number | null,
    date: string,
    hours: string,
    taskId?: number | null,
  ) {
    saveError.value = null
    // Find existing entry — match by task first, fallback to phase
    const existing = taskId
      ? entries.value.find((e) => e.project === projectId && e.task === taskId && e.date === date)
      : entries.value.find((e) => e.project === projectId && e.phase === phaseId && e.date === date)
    try {
      if (existing) {
        const resp = await timesheetApi.updateEntry(existing.id, { hours }, existing.version)
        const updated = resp.data?.data || resp.data
        const idx = entries.value.findIndex((e) => e.id === existing.id)
        if (idx >= 0 && updated) entries.value[idx] = updated
      } else if (hours !== '0' && hours !== '') {
        const payload: Record<string, unknown> = { project: projectId, date, hours }
        if (taskId) payload.task = taskId
        if (phaseId) payload.phase = phaseId
        const resp = await timesheetApi.createEntry(payload)
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
    weeklyStats, statusMessage, hasModificationRequested, allSubmitted, periodLocked,
    fetchWeek, navigateWeek, saveCell,
    submitWeek, copyPreviousWeek, canSaveHours,
    DAILY_NORM, WEEKLY_NORM, CONTRACT_HOURS, MAX_DAILY_HOURS,
  }
})
