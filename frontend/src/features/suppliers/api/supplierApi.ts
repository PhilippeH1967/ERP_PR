import apiClient from '@/plugins/axios'

export const supplierApi = {
  listOrganizations: (params?: Record<string, string>) =>
    apiClient.get('external_organizations/', { params }),
  getOrganization: (id: number) => apiClient.get(`external_organizations/${id}/`),
  createOrganization: (data: Record<string, unknown>) =>
    apiClient.post('external_organizations/', data),
  updateOrganization: (id: number, data: Record<string, unknown>) =>
    apiClient.patch(`external_organizations/${id}/`, data),
}
