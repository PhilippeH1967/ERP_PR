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
  checkDuplicate: (name: string) => apiClient.post(`${BASE}/check_duplicate/`, { name }),
  financialSummary: (id: number) => apiClient.get(`${BASE}/${id}/financial_summary/`),

  // Contacts
  listContacts: (clientId: number) => apiClient.get(`${BASE}/${clientId}/contacts/`),
  createContact: (clientId: number, data: Partial<Contact>) =>
    apiClient.post(`${BASE}/${clientId}/contacts/`, data),
  updateContact: (clientId: number, contactId: number, data: Partial<Contact>) =>
    apiClient.patch(`${BASE}/${clientId}/contacts/${contactId}/`, data),
  deleteContact: (clientId: number, contactId: number) =>
    apiClient.delete(`${BASE}/${clientId}/contacts/${contactId}/`),

  // Addresses
  listAddresses: (clientId: number) => apiClient.get(`${BASE}/${clientId}/addresses/`),
  createAddress: (clientId: number, data: Partial<ClientAddress>) =>
    apiClient.post(`${BASE}/${clientId}/addresses/`, data),
  updateAddress: (clientId: number, addressId: number, data: Partial<ClientAddress>) =>
    apiClient.patch(`${BASE}/${clientId}/addresses/${addressId}/`, data),
  deleteAddress: (clientId: number, addressId: number) =>
    apiClient.delete(`${BASE}/${clientId}/addresses/${addressId}/`),
}
