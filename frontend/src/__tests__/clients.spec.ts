import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'

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

  it('fetchClients with pagination meta', async () => {
    vi.mocked(apiClient.get).mockResolvedValue({
      data: {
        data: [{ id: 1, name: 'Test', alias: 'T', status: 'active' }],
        meta: { count: 1, next: null, previous: null },
      },
    })
    const store = useClientStore()
    await store.fetchClients()
    expect(store.clients).toHaveLength(1)
    expect(store.pagination.count).toBe(1)
  })

  it('updateClient sends If-Match header', async () => {
    vi.mocked(apiClient.patch).mockResolvedValue({
      data: { data: { id: 1, name: 'Updated', version: 2 } },
    })
    const store = useClientStore()
    store.currentClient = { id: 1, name: 'Old', version: 1 } as unknown as ReturnType<typeof useClientStore>['currentClient']
    await store.updateClient(1, { name: 'Updated' })
    expect(apiClient.patch).toHaveBeenCalledWith(
      'clients/1/',
      { name: 'Updated' },
      { headers: { 'If-Match': '1' } },
    )
  })

  it('addContact refreshes client', async () => {
    vi.mocked(apiClient.post).mockResolvedValue({ data: {} })
    vi.mocked(apiClient.get).mockResolvedValue({ data: { data: { id: 1, contacts: [{ id: 1 }] } } })
    const store = useClientStore()
    await store.addContact(1, { name: 'Jean' })
    expect(apiClient.post).toHaveBeenCalled()
    expect(apiClient.get).toHaveBeenCalled()
  })
})
