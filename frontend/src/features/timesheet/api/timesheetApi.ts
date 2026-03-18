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

  // Approvals
  listApprovals: (params?: Record<string, string>) =>
    apiClient.get('weekly_approvals/', { params }),
  approvePM: (id: number) => apiClient.post(`weekly_approvals/${id}/approve_pm/`),
  approveFinance: (id: number) => apiClient.post(`weekly_approvals/${id}/approve_finance/`),

  // Locks
  listLocks: (params?: Record<string, string>) => apiClient.get('timesheet_locks/', { params }),
  createLock: (data: Record<string, unknown>) => apiClient.post('timesheet_locks/', data),
  deleteLock: (id: number) => apiClient.delete(`timesheet_locks/${id}/`),
}
