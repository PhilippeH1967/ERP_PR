import apiClient from '@/plugins/axios'

export const supplierApi = {
  listOrganizations: (params?: Record<string, string>) =>
    apiClient.get('external_organizations/', { params }),
  getOrganization: (id: number) => apiClient.get(`external_organizations/${id}/`),
  createOrganization: (data: Record<string, unknown>) =>
    apiClient.post('external_organizations/', data),
  updateOrganization: (id: number, data: Record<string, unknown>) =>
    apiClient.patch(`external_organizations/${id}/`, data),
  checkDuplicate: (data: { name?: string; neq?: string }) =>
    apiClient.post('external_organizations/check_duplicate/', data),

  // ST Invoices
  listSTInvoices: (params?: Record<string, string>) => apiClient.get('st_invoices/', { params }),
  createSTInvoice: (data: Record<string, unknown>) => apiClient.post('st_invoices/', data),
  updateSTInvoice: (id: number, data: Record<string, unknown>) => apiClient.patch(`st_invoices/${id}/`, data),
  deleteSTInvoice: (id: number) => apiClient.delete(`st_invoices/${id}/`),
  authorizeSTInvoice: (id: number) => apiClient.post(`st_invoices/${id}/authorize/`),
  markSTInvoicePaid: (id: number) => apiClient.post(`st_invoices/${id}/mark_paid/`),
  disputeSTInvoice: (id: number, reason: string) => apiClient.post(`st_invoices/${id}/dispute/`, { reason }),
  batchAuthorize: (ids: number[]) => apiClient.post('st_invoices/batch_authorize/', { invoice_ids: ids }),
  batchPay: (ids: number[]) => apiClient.post('st_invoices/batch_pay/', { invoice_ids: ids }),
  summaryBySupplier: () => apiClient.get('st_invoices/summary_by_supplier/'),

  // Payments
  listPayments: (params?: Record<string, string>) => apiClient.get('st_payments/', { params }),
  createPayment: (data: Record<string, unknown>) => apiClient.post('st_payments/', data),

  // Credit Notes
  listCreditNotes: () => apiClient.get('st_credit_notes/'),
  createCreditNote: (data: Record<string, unknown>) => apiClient.post('st_credit_notes/', data),

  // Disputes
  listDisputes: () => apiClient.get('st_disputes/'),
  resolveDispute: (id: number, notes: string) => apiClient.post(`st_disputes/${id}/resolve/`, { resolution_notes: notes }),

  // Holdbacks
  listHoldbacks: () => apiClient.get('st_holdbacks/'),
  createHoldback: (data: Record<string, unknown>) => apiClient.post('st_holdbacks/', data),
  releaseHoldback: (id: number, amount: number) => apiClient.post(`st_holdbacks/${id}/release/`, { amount }),
}
