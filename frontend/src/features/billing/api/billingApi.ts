import apiClient from '@/plugins/axios'

export const billingApi = {
  listInvoices: (params?: Record<string, string>) => apiClient.get('invoices/', { params }),
  getInvoice: (id: number) => apiClient.get(`invoices/${id}/`),
  createInvoice: (data: Record<string, unknown>) => apiClient.post('invoices/', data),
  submitInvoice: (id: number) => apiClient.post(`invoices/${id}/submit/`),
  approveInvoice: (id: number) => apiClient.post(`invoices/${id}/approve/`),
  agingAnalysis: (id: number) => apiClient.get(`invoices/${id}/aging_analysis/`),

  // Lines
  listLines: (invoiceId: number) => apiClient.get(`invoices/${invoiceId}/lines/`),
  createLine: (invoiceId: number, data: Record<string, unknown>) =>
    apiClient.post(`invoices/${invoiceId}/lines/`, data),
  updateLine: (invoiceId: number, lineId: number, data: Record<string, unknown>) =>
    apiClient.patch(`invoices/${invoiceId}/lines/${lineId}/`, data),

  // Payments
  listPayments: (params?: Record<string, string>) => apiClient.get('payments/', { params }),
  createPayment: (data: Record<string, unknown>) => apiClient.post('payments/', data),

  // Credit notes
  listCreditNotes: () => apiClient.get('credit_notes/'),
  createCreditNote: (data: Record<string, unknown>) => apiClient.post('credit_notes/', data),

  // Holdbacks
  listHoldbacks: () => apiClient.get('holdbacks/'),

  // Templates
  listTemplates: () => apiClient.get('invoice_templates/'),
}
