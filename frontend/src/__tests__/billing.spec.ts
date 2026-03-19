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
import { useBillingStore } from '@/features/billing/stores/useBillingStore'

describe('useBillingStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('fetchInvoices populates store', async () => {
    vi.mocked(apiClient.get).mockResolvedValue({
      data: {
        data: [
          { id: 1, invoice_number: 'PROV-001', status: 'DRAFT', total_amount: '50000.00' },
        ],
      },
    })
    const store = useBillingStore()
    await store.fetchInvoices()
    expect(store.invoices).toHaveLength(1)
    expect(store.invoices[0]!.invoice_number).toBe('PROV-001')
  })

  it('fetchInvoice sets currentInvoice', async () => {
    vi.mocked(apiClient.get).mockResolvedValue({
      data: { data: { id: 1, invoice_number: 'INV-1', lines: [], version: 1 } },
    })
    const store = useBillingStore()
    await store.fetchInvoice(1)
    expect(store.currentInvoice?.invoice_number).toBe('INV-1')
  })
})
