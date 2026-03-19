import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'

// Mock axios
vi.mock('@/plugins/axios', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    patch: vi.fn(),
    delete: vi.fn(),
  },
}))

import apiClient from '@/plugins/axios'
import { useClientStore } from '@/features/clients/stores/useClientStore'

describe('useClientStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('fetchClients populates store', async () => {
    const mockClients = [
      { id: 1, name: 'Client A', alias: 'CA', status: 'active' },
      { id: 2, name: 'Client B', alias: 'CB', status: 'active' },
    ]
    vi.mocked(apiClient.get).mockResolvedValue({ data: { data: mockClients } })

    const store = useClientStore()
    await store.fetchClients()

    expect(store.clients).toHaveLength(2)
    expect(store.clients[0]!.name).toBe('Client A')
    expect(store.isLoading).toBe(false)
  })

  it('fetchClient sets currentClient', async () => {
    const mockClient = { id: 1, name: 'Detail', alias: 'D', version: 1, contacts: [], addresses: [] }
    vi.mocked(apiClient.get).mockResolvedValue({ data: { data: mockClient } })

    const store = useClientStore()
    await store.fetchClient(1)

    expect(store.currentClient?.name).toBe('Detail')
  })

  it('createClient calls API', async () => {
    vi.mocked(apiClient.post).mockResolvedValue({ data: { data: { id: 3, name: 'New' } } })

    const store = useClientStore()
    const result = await store.createClient({ name: 'New', alias: 'N' })

    expect(apiClient.post).toHaveBeenCalledWith('clients/', { name: 'New', alias: 'N' })
    expect(result.name).toBe('New')
  })
})
