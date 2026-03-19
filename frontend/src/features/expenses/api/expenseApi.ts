import apiClient from '@/plugins/axios'

export const expenseApi = {
  listReports: (params?: Record<string, string>) => apiClient.get('expense_reports/', { params }),
  getReport: (id: number) => apiClient.get(`expense_reports/${id}/`),
  createReport: (data: Record<string, unknown>) => apiClient.post('expense_reports/', data),
  updateReport: (id: number, data: Record<string, unknown>) => apiClient.patch(`expense_reports/${id}/`, data),
  deleteReport: (id: number) => apiClient.delete(`expense_reports/${id}/`),
  listLines: (reportId: number) => apiClient.get(`expense_reports/${reportId}/lines/`),
  createLine: (reportId: number, data: Record<string, unknown>) =>
    apiClient.post(`expense_reports/${reportId}/lines/`, data),
  updateLine: (reportId: number, lineId: number, data: Record<string, unknown>) =>
    apiClient.patch(`expense_reports/${reportId}/lines/${lineId}/`, data),
  deleteLine: (reportId: number, lineId: number) =>
    apiClient.delete(`expense_reports/${reportId}/lines/${lineId}/`),
  listCategories: () => apiClient.get('expense_categories/'),
  uploadReceipt: (reportId: number, file: File) => {
    const formData = new FormData()
    formData.append('receipt', file)
    return apiClient.post(`expense_reports/${reportId}/upload_receipt/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
}
