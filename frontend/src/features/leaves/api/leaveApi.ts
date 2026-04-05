import apiClient from '@/plugins/axios'

export const leaveApi = {
  // Types
  listTypes: () => apiClient.get('leave_types/'),
  seedTypes: () => apiClient.post('leave_types/seed/'),

  // Banks
  myBalances: () => apiClient.get('leave_banks/my_balances/'),
  listBanks: (params?: Record<string, string>) => apiClient.get('leave_banks/', { params }),

  // Requests
  listRequests: (params?: Record<string, string>) => apiClient.get('leave_requests/', { params }),
  createRequest: (data: Record<string, unknown>) => apiClient.post('leave_requests/', data),
  approve: (id: number) => apiClient.post(`leave_requests/${id}/approve/`),
  reject: (id: number, reason: string) => apiClient.post(`leave_requests/${id}/reject/`, { reason }),
  cancel: (id: number) => apiClient.post(`leave_requests/${id}/cancel/`),

  // Holidays
  listHolidays: () => apiClient.get('public_holidays/'),
}
