import { defineStore } from 'pinia'
import { ref } from 'vue'
import { clientApi } from '../api/clientApi'
import type { Client } from '../types/client.types'

export const useClientStore = defineStore('clients', () => {
  const clients = ref<Client[]>([])
  const currentClient = ref<Client | null>(null)
  const isLoading = ref(false)

  async function fetchClients(params?: Record<string, string>) {
    isLoading.value = true
    try {
      const response = await clientApi.list(params)
      clients.value = response.data?.data || response.data
    } finally {
      isLoading.value = false
    }
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
    const version = currentClient.value?.version
    const response = await clientApi.update(id, data, version)
    currentClient.value = response.data?.data || response.data
    return currentClient.value
  }

  return { clients, currentClient, isLoading, fetchClients, fetchClient, createClient, updateClient }
})
