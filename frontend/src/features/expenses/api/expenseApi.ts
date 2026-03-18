import apiClient from '@/plugins/axios'

export const expenseApi = {
  listReports: (params?: Record<string, string>) => apiClient.get('expense_reports/', { params }),
  getReport: (id: number) => apiClient.get(`expense_reports/${id}/`),
  createReport: (data: Record<string, unknown>) => apiClient.post('expense_reports/', data),
  listLines: (reportId: number) => apiClient.get(`expense_reports/${reportId}/lines/`),
  createLine: (reportId: number, data: Record<string, unknown>) =>
    apiClient.post(`expense_reports/${reportId}/lines/`, data),
  listCategories: () => apiClient.get('expense_categories/'),
}
