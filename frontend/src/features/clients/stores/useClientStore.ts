import { defineStore } from 'pinia'
import { ref } from 'vue'
import { clientApi } from '../api/clientApi'
import type { Client } from '../types/client.types'

export const useClientStore = defineStore('clients', () => {
  const clients = ref<Client[]>([])
  const currentClient = ref<Client | null>(null)
  const isLoading = ref(false)
  const pagination = ref({ count: 0, next: null as string | null, previous: null as string | null })
  const saveError = ref<string | null>(null)

  async function fetchClients(params?: Record<string, string>) {
    isLoading.value = true
    try {
      const response = await clientApi.list(params)
      const payload = response.data
      if (payload?.data && payload?.meta) {
        clients.value = payload.data
        pagination.value = payload.meta
      } else if (Array.isArray(payload?.data)) {
        clients.value = payload.data
      } else if (Array.isArray(payload)) {
        clients.value = payload
      }
    } finally {
      isLoading.value = false
    }
  }

  function fetchPage(direction: 'prev' | 'next') {
    const url = direction === 'next' ? pagination.value.next : pagination.value.previous
    if (!url) return
    const params = Object.fromEntries(new URL(url, window.location.origin).searchParams)
    fetchClients(params)
  }

  async function fetchClient(id: number) {
    isLoading.value = true
    try {
      const response = await clientApi.get(id)
      currentClient.value = response.data?.data || response.data
    } finally {
      isLoading.value = false
    }
  }

  async function createClient(data: Partial<Client>) {
    const response = await clientApi.create(data)
    return response.data?.data || response.data
  }

  async function updateClient(id: number, data: Partial<Client>) {
    saveError.value = null
    const version = currentClient.value?.version
    try {
      const response = await clientApi.update(id, data, version)
      currentClient.value = response.data?.data || response.data
      return currentClient.value
    } catch (err: unknown) {
      const axiosErr = err as { response?: { status: number } }
      if (axiosErr.response?.status === 409) {
        saveError.value = 'conflict'
      } else {
        saveError.value = 'error'
      }
      throw err
    }
  }

  async function addContact(clientId: number, data: Record<string, unknown>) {
    await clientApi.createContact(clientId, data)
    await fetchClient(clientId)
  }

  async function addAddress(clientId: number, data: Record<string, unknown>) {
    await clientApi.createAddress(clientId, data)
    await fetchClient(clientId)
  }

  return {
    clients, currentClient, isLoading, pagination, saveError,
    fetchClients, fetchPage, fetchClient, createClient, updateClient,
    addContact, addAddress,
  }
})
