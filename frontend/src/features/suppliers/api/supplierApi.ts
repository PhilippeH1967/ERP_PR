import apiClient from '@/plugins/axios'

export const supplierApi = {
  listOrganizations: (params?: Record<string, string>) =>
    apiClient.get('external_organizations/', { params }),
  getOrganization: (id: number) => apiClient.get(`external_organizations/${id}/`),
  createOrganization: (data: Record<string, unknown>) =>
    apiClient.post('external_organizations/', data),
  updateOrganization: (id: number, data: Record<string, unknown>) =>
    apiClient.patch(`external_organizations/${id}/`, data),

  // ST Invoices
  listSTInvoices: (params?: Record<string, string>) => apiClient.get('st_invoices/', { params }),
  createSTInvoice: (data: Record<string, unknown>) => apiClient.post('st_invoices/', data),
  updateSTInvoice: (id: number, data: Record<string, unknown>) => apiClient.patch(`st_invoices/${id}/`, data),
  deleteSTInvoice: (id: number) => apiClient.delete(`st_invoices/${id}/`),
  authorizeSTInvoice: (id: number) => apiClient.post(`st_invoices/${id}/authorize/`),
  markSTInvoicePaid: (id: number) => apiClient.post(`st_invoices/${id}/mark_paid/`),
}
