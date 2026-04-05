import apiClient from '@/plugins/axios'

const BASE = 'consortiums'

export const consortiumApi = {
  list: (params?: Record<string, string>) => apiClient.get(`${BASE}/`, { params }),
  get: (id: number) => apiClient.get(`${BASE}/${id}/`),
  create: (data: Record<string, unknown>) => apiClient.post(`${BASE}/`, data),
  update: (id: number, data: Record<string, unknown>) => apiClient.patch(`${BASE}/${id}/`, data),
  delete: (id: number) => apiClient.delete(`${BASE}/${id}/`),

  // Members
  listMembers: (consortiumId: number) => apiClient.get(`${BASE}/${consortiumId}/members/`),
  addMember: (consortiumId: number, data: Record<string, unknown>) =>
    apiClient.post(`${BASE}/${consortiumId}/members/`, data),
  updateMember: (consortiumId: number, memberId: number, data: Record<string, unknown>) =>
    apiClient.patch(`${BASE}/${consortiumId}/members/${memberId}/`, data),
  removeMember: (consortiumId: number, memberId: number) =>
    apiClient.delete(`${BASE}/${consortiumId}/members/${memberId}/`),

  // Validation
  validateCoefficients: (consortiumId: number) =>
    apiClient.get(`${BASE}/${consortiumId}/validate_coefficients/`),
}
