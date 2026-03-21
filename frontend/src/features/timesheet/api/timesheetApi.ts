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
  weeklyStats: () => apiClient.get('time_entries/weekly_stats/'),
  copyPreviousWeek: (weekStart: string) =>
    apiClient.post('time_entries/copy_previous_week/', { week_start: weekStart }),

  // Approvals
  listApprovals: (params?: Record<string, string>) =>
    apiClient.get('weekly_approvals/', { params }),
  approvePM: (id: number) => apiClient.post(`weekly_approvals/${id}/approve_pm/`),
  approveFinance: (id: number) => apiClient.post(`weekly_approvals/${id}/approve_finance/`),
  rejectPM: (id: number, reason: string) => apiClient.post(`weekly_approvals/${id}/reject_pm/`, { reason }),
  rejectFinance: (id: number) => apiClient.post(`weekly_approvals/${id}/reject_finance/`),

  // Period unlocks
  listUnlocks: () => apiClient.get('period_unlocks/'),
  createUnlock: (data: Record<string, unknown>) => apiClient.post('period_unlocks/', data),

  // Locks
  listLocks: (params?: Record<string, string>) => apiClient.get('timesheet_locks/', { params }),
  createLock: (data: Record<string, unknown>) => apiClient.post('timesheet_locks/', data),
  deleteLock: (id: number) => apiClient.delete(`timesheet_locks/${id}/`),
}
