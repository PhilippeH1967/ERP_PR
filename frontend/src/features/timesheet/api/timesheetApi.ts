import apiClient from '@/plugins/axios'
import type { TimeEntry } from '../types/timesheet.types'

export const timesheetApi = {
  listEntries: (params?: Record<string, string>) => apiClient.get('time_entries/', { params }),
  createEntry: (data: Partial<TimeEntry>) => apiClient.post('time_entries/', data),
  updateEntry: (id: number, data: Partial<TimeEntry>, version?: number) =>
    apiClient.patch(`time_entries/${id}/`, data, {
      headers: version ? { 'If-Match': String(version) } : {},
    }),
  submitWeek: (weekStart: string) =>
    apiClient.post('time_entries/submit_week/', { week_start: weekStart }),
  weeklyStats: (weekStart?: string) =>
    apiClient.get('time_entries/weekly_stats/', { params: weekStart ? { week_start: weekStart } : {} }),
  copyPreviousWeek: (weekStart: string) =>
    apiClient.post('time_entries/copy_previous_week/', { week_start: weekStart }),

  // Approvals
  listApprovals: (params?: Record<string, string>) =>
    apiClient.get('weekly_approvals/', { params }),
  approvePM: (id: number) => apiClient.post(`weekly_approvals/${id}/approve_pm/`),
  approveFinance: (id: number) => apiClient.post(`weekly_approvals/${id}/approve_finance/`),
  rejectPM: (id: number, reason: string) => apiClient.post(`weekly_approvals/${id}/reject_pm/`, { reason }),
  rejectFinance: (id: number) => apiClient.post(`weekly_approvals/${id}/reject_finance/`),
  approvalEntries: (id: number) => apiClient.get(`weekly_approvals/${id}/entries/`),
  pmDashboard: (weekStart?: string) =>
    apiClient.get('weekly_approvals/pm_dashboard/', { params: weekStart ? { week_start: weekStart } : {} }),
  financeDashboard: (weekStart?: string) =>
    apiClient.get('weekly_approvals/finance_dashboard/', { params: weekStart ? { week_start: weekStart } : {} }),
  paieDashboard: (weekStart?: string) =>
    apiClient.get('weekly_approvals/paie_dashboard/', { params: weekStart ? { week_start: weekStart } : {} }),
  validatePaie: (id: number) => apiClient.post(`weekly_approvals/${id}/validate_paie/`),
  bulkValidatePaie: (approvalIds: number[]) =>
    apiClient.post('weekly_approvals/bulk_validate_paie/', { approval_ids: approvalIds }),
  rejectPaie: (id: number) => apiClient.post(`weekly_approvals/${id}/reject_paie/`),

  // Per-entry PM actions
  approveEntries: (entryIds: number[]) =>
    apiClient.post('time_entries/approve_entries/', { entry_ids: entryIds }),
  approveAllMyEntries: (employeeId: number, weekStart: string) =>
    apiClient.post('time_entries/approve_all_my_entries/', { employee_id: employeeId, week_start: weekStart }),
  rejectEntries: (entryIds: number[], reason: string) =>
    apiClient.post('time_entries/reject_entries/', { entry_ids: entryIds, reason }),

  // FR25 — Finance bulk correction
  bulkCorrect: (corrections: Array<{ entry_id: number; hours: number; reason?: string }>) =>
    apiClient.post('time_entries/bulk_correct/', { corrections }),

  // FR27d — Transfer hours between projects/tasks
  transferHours: (entryIds: number[], targetProject: number, targetTask?: number, reason?: string) =>
    apiClient.post('time_entries/transfer_hours/', {
      entry_ids: entryIds,
      target_project: targetProject,
      target_task: targetTask || null,
      reason: reason || 'Transfert d\'heures',
    }),

  // Period unlocks
  listUnlocks: () => apiClient.get('period_unlocks/'),
  createUnlock: (data: Record<string, unknown>) => apiClient.post('period_unlocks/', data),

  // Locks
  listLocks: (params?: Record<string, string>) => apiClient.get('timesheet_locks/', { params }),
  createLock: (data: Record<string, unknown>) => apiClient.post('timesheet_locks/', data),
  deleteLock: (id: number) => apiClient.delete(`timesheet_locks/${id}/`),
}
