import apiClient from '@/plugins/axios'

export const planningApi = {
  // Allocations
  listAllocations: (params?: Record<string, string>) => apiClient.get('allocations/', { params }),
  createAllocation: (data: Record<string, unknown>) => apiClient.post('allocations/', data),
  updateAllocation: (id: number, data: Record<string, unknown>) => apiClient.patch(`allocations/${id}/`, data),
  deleteAllocation: (id: number) => apiClient.delete(`allocations/${id}/`),
  globalPlanning: (params?: Record<string, string>) => apiClient.get('allocations/global_planning/', { params }),
  loadAlerts: () => apiClient.get('allocations/load_alerts/'),

  // Milestones
  listMilestones: (params?: Record<string, string>) => apiClient.get('milestones/', { params }),
  createMilestone: (data: Record<string, unknown>) => apiClient.post('milestones/', data),
  updateMilestone: (id: number, data: Record<string, unknown>) => apiClient.patch(`milestones/${id}/`, data),
  deleteMilestone: (id: number) => apiClient.delete(`milestones/${id}/`),
  autoUpdateOverdue: () => apiClient.post('milestones/auto_update_status/'),

  // Availability
  listAvailability: (params?: Record<string, string>) => apiClient.get('availability/', { params }),
  generateAvailability: (employeeId: number, startDate: string, endDate: string) =>
    apiClient.post('availability/generate/', { employee_id: employeeId, start_date: startDate, end_date: endDate }),

  // Planning standards
  listStandards: (params?: Record<string, string>) => apiClient.get('planning-standards/', { params }),
  createStandard: (data: Record<string, unknown>) => apiClient.post('planning-standards/', data),
  updateStandard: (id: number, data: Record<string, unknown>) => apiClient.patch(`planning-standards/${id}/`, data),
  deleteStandard: (id: number) => apiClient.delete(`planning-standards/${id}/`),

  // Virtual resources
  listVirtualResources: (params?: Record<string, string>) =>
    apiClient.get('virtual-resources/', { params }),
  createVirtualResource: (data: Record<string, unknown>) =>
    apiClient.post('virtual-resources/', data),
  updateVirtualResource: (id: number, data: Record<string, unknown>) =>
    apiClient.patch(`virtual-resources/${id}/`, data),
  deleteVirtualResource: (id: number) => apiClient.delete(`virtual-resources/${id}/`),
  replaceVirtualWithEmployee: (id: number, employeeId: number) =>
    apiClient.post(`virtual-resources/${id}/replace_with_employee/`, { employee: employeeId }),
}
