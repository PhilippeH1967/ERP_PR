import apiClient from '@/plugins/axios'

export const billingApi = {
  listInvoices: (params?: Record<string, string>) => apiClient.get('invoices/', { params }),
  getInvoice: (id: number) => apiClient.get(`invoices/${id}/`),
  createInvoice: (data: Record<string, unknown>) => apiClient.post('invoices/', data),
  updateInvoice: (id: number, data: Record<string, unknown>) => apiClient.patch(`invoices/${id}/`, data),
  deleteInvoice: (id: number) => apiClient.delete(`invoices/${id}/`),
  createFromProject: (projectId: number) => apiClient.post('invoices/create_from_project/', { project_id: projectId }),
  submitInvoice: (id: number) => apiClient.post(`invoices/${id}/submit/`),
  approveInvoice: (id: number) => apiClient.post(`invoices/${id}/approve/`),
  agingAnalysis: (id: number) => apiClient.get(`invoices/${id}/aging_analysis/`),
  markHoursInvoiced: (id: number) => apiClient.post(`invoices/${id}/mark_hours_invoiced/`),
  printView: (id: number) => `${apiClient.defaults.baseURL}invoices/${id}/print/`,

  // Lines
  listLines: (invoiceId: number) => apiClient.get(`invoices/${invoiceId}/lines/`),
  createLine: (invoiceId: number, data: Record<string, unknown>) =>
    apiClient.post(`invoices/${invoiceId}/lines/`, data),
  updateLine: (invoiceId: number, lineId: number, data: Record<string, unknown>) =>
    apiClient.patch(`invoices/${invoiceId}/lines/${lineId}/`, data),
  deleteLine: (invoiceId: number, lineId: number) =>
    apiClient.delete(`invoices/${invoiceId}/lines/${lineId}/`),

  // Payments
  listPayments: (params?: Record<string, string>) => apiClient.get('payments/', { params }),
  createPayment: (data: Record<string, unknown>) => apiClient.post('payments/', data),

  // Credit notes
  listCreditNotes: () => apiClient.get('credit_notes/'),
  createCreditNote: (data: Record<string, unknown>) => apiClient.post('credit_notes/', data),
  updateCreditNote: (id: number, data: Record<string, unknown>) => apiClient.patch(`credit_notes/${id}/`, data),
  deleteCreditNote: (id: number) => apiClient.delete(`credit_notes/${id}/`),

  // Holdbacks
  listHoldbacks: () => apiClient.get('holdbacks/'),
  createHoldback: (data: Record<string, unknown>) => apiClient.post('holdbacks/', data),
  updateHoldback: (id: number, data: Record<string, unknown>) => apiClient.patch(`holdbacks/${id}/`, data),
  deleteHoldback: (id: number) => apiClient.delete(`holdbacks/${id}/`),

  // Write-offs
  listWriteOffs: () => apiClient.get('write_offs/'),
  createWriteOff: (data: Record<string, unknown>) => apiClient.post('write_offs/', data),
  deleteWriteOff: (id: number) => apiClient.delete(`write_offs/${id}/`),

  // Templates
  listTemplates: () => apiClient.get('invoice_templates/'),
}
