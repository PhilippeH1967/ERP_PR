export interface TimeEntry {
  id: number
  employee: number
  project: number
  project_code: string
  project_name: string
  phase: number | null
  phase_name: string
  client_label: string
  date: string
  hours: string
  notes: string
  rejection_reason: string
  status: 'DRAFT' | 'SUBMITTED' | 'PM_APPROVED' | 'FINANCE_APPROVED' | 'LOCKED'
  is_favorite: boolean
  version: number
}

export interface WeeklyApproval {
  id: number
  employee: number
  employee_name: string
  week_start: string
  week_end: string
  pm_status: 'PENDING' | 'APPROVED' | 'REJECTED'
  pm_approved_by: number | null
  pm_approved_at: string | null
  finance_status: 'PENDING' | 'APPROVED' | 'REJECTED'
  finance_approved_by: number | null
  finance_approved_at: string | null
}

export interface TimesheetGridRow {
  project_id: number
  project_code: string
  project_name: string
  phase_id: number | null
  phase_name: string
  client_label: string
  entries: Record<string, TimeEntry | null>
  is_locked: boolean
  row_total: number
  is_favorite: boolean
  category: 'project' | 'non-project' | 'absence'
}

/** Rows grouped under a project header */
export interface TimesheetProjectGroup {
  project_id: number
  project_code: string
  project_name: string
  is_favorite: boolean
  category: 'project' | 'non-project' | 'absence'
  rows: TimesheetGridRow[]
  group_total: number
}

export interface TimesheetWeek {
  weekStart: string
  weekEnd: string
  dates: string[]
  groups: TimesheetProjectGroup[]
  dailyTotals: number[]
  weeklyTotal: number
  weeklyNorm: number
  contractHours: number
}
