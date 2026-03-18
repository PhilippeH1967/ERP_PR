import apiClient from '@/plugins/axios'
import type { Client, ClientAddress, Contact } from '../types/client.types'

const BASE = 'clients'

export const clientApi = {
  list: (params?: Record<string, string>) => apiClient.get(`${BASE}/`, { params }),
  get: (id: number) => apiClient.get<{ data: Client }>(`${BASE}/${id}/`),
  create: (data: Partial<Client>) => apiClient.post(`${BASE}/`, data),
  update: (id: number, data: Partial<Client>, version?: number) =>
    apiClient.patch(`${BASE}/${id}/`, data, {
      headers: version ? { 'If-Match': String(version) } : {},
    }),
  delete: (id: number) => apiClient.delete(`${BASE}/${id}/`),
  financialSummary: (id: number) => apiClient.get(`${BASE}/${id}/financial_summary/`),

  // Contacts
  listContacts: (clientId: number) => apiClient.get(`${BASE}/${clientId}/contacts/`),
  createContact: (clientId: number, data: Partial<Contact>) =>
    apiClient.post(`${BASE}/${clientId}/contacts/`, data),

  // Addresses
  listAddresses: (clientId: number) => apiClient.get(`${BASE}/${clientId}/addresses/`),
  createAddress: (clientId: number, data: Partial<ClientAddress>) =>
    apiClient.post(`${BASE}/${clientId}/addresses/`, data),
}
