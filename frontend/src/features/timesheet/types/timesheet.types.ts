export interface TimeEntry {
  id: number
  employee: number
  project: number
  phase: number | null
  date: string
  hours: string
  notes: string
  status: 'DRAFT' | 'SUBMITTED' | 'PM_APPROVED' | 'FINANCE_APPROVED' | 'LOCKED'
  is_favorite: boolean
  version: number
}

export interface WeeklyApproval {
  id: number
  employee: number
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
  entries: Record<string, TimeEntry | null> // key = 'YYYY-MM-DD'
  is_locked: boolean
}
