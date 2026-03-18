import { defineStore } from 'pinia'
import { ref } from 'vue'
import { timesheetApi } from '../api/timesheetApi'
import type { TimeEntry, WeeklyApproval } from '../types/timesheet.types'

export const useTimesheetStore = defineStore('timesheet', () => {
  const entries = ref<TimeEntry[]>([])
  const approvals = ref<WeeklyApproval[]>([])
  const isLoading = ref(false)

  async function fetchEntries(params?: Record<string, string>) {
    isLoading.value = true
    try {
      const response = await timesheetApi.listEntries(params)
      entries.value = response.data?.data || response.data
    } finally {
      isLoading.value = false
    }
  }

  async function saveEntry(id: number, hours: string, version: number) {
    await timesheetApi.updateEntry(id, { hours }, version)
  }

  async function submitWeek(weekStart: string) {
    return timesheetApi.submitWeek(weekStart)
  }

  async function fetchApprovals(params?: Record<string, string>) {
    const response = await timesheetApi.listApprovals(params)
    approvals.value = response.data?.data || response.data
  }

  return { entries, approvals, isLoading, fetchEntries, saveEntry, submitWeek, fetchApprovals }
})
