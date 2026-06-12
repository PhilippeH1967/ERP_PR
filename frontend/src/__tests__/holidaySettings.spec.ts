import { mount, flushPromises } from '@vue/test-utils'
import { beforeEach, describe, expect, it, vi } from 'vitest'

vi.mock('@/plugins/axios', () => ({
  default: { get: vi.fn(), post: vi.fn(), patch: vi.fn(), delete: vi.fn() },
}))
vi.mock('vue-router', () => ({ useRouter: () => ({ push: vi.fn() }) }))

import apiClient from '@/plugins/axios'
import HolidaySettings from '../features/admin/views/HolidaySettings.vue'

const mockGet = apiClient.get as unknown as ReturnType<typeof vi.fn>
const mockPost = apiClient.post as unknown as ReturnType<typeof vi.fn>
const mockDelete = apiClient.delete as unknown as ReturnType<typeof vi.fn>

const RULES = [
  { id: 1, name: 'Québec 37.5h' },
  { id: 2, name: 'Ontario 40h' },
]
const HOLIDAYS = [
  { id: 10, name: 'Fête nationale', date: '2026-06-24', is_paid: true, labor_rule: 1, labor_rule_name: 'Québec 37.5h' },
  { id: 11, name: 'Jour de l\'an', date: '2026-01-01', is_paid: true, labor_rule: null, labor_rule_name: '' },
]

function mockApi() {
  mockGet.mockImplementation((url: string) => {
    if (url === 'public_holidays/') return Promise.resolve({ data: HOLIDAYS })
    if (url === 'labor_rules/') return Promise.resolve({ data: RULES })
    return Promise.resolve({ data: [] })
  })
}

describe('HolidaySettings — paramétrage des jours fériés', () => {
  beforeEach(() => {
    mockGet.mockReset()
    mockPost.mockReset()
    mockDelete.mockReset()
    mockApi()
    mockPost.mockResolvedValue({ data: { id: 99 } })
    mockDelete.mockResolvedValue({ data: {} })
  })

  it('liste les fériés avec leur régime (ou « Tous les régimes »)', async () => {
    const wrapper = mount(HolidaySettings)
    await flushPromises()
    const rows = wrapper.findAll('[data-hol-row]')
    expect(rows).toHaveLength(2)
    expect(wrapper.text()).toContain('Fête nationale')
    expect(wrapper.text()).toContain('Québec 37.5h')
    expect(wrapper.text()).toContain('Tous les régimes')
  })

  it('crée un férié rattaché à un régime', async () => {
    const wrapper = mount(HolidaySettings)
    await flushPromises()
    await wrapper.find('[data-hol-add]').trigger('click')
    await wrapper.find('[data-hol-name]').setValue('Fête du Canada')
    await wrapper.find('[data-hol-date]').setValue('2026-07-01')
    await wrapper.find('[data-hol-rule]').setValue('2')
    await wrapper.find('[data-hol-save]').trigger('click')
    await flushPromises()
    expect(mockPost).toHaveBeenCalledWith(
      'public_holidays/',
      expect.objectContaining({ name: 'Fête du Canada', date: '2026-07-01', labor_rule: 2 }),
    )
  })

  it('refuse un férié sans nom ou sans date', async () => {
    const wrapper = mount(HolidaySettings)
    await flushPromises()
    await wrapper.find('[data-hol-add]').trigger('click')
    await wrapper.find('[data-hol-save]').trigger('click')
    expect(mockPost).not.toHaveBeenCalled()
    expect(wrapper.text()).toContain('obligatoires')
  })

  it('supprime avec confirmation inline', async () => {
    const wrapper = mount(HolidaySettings)
    await flushPromises()
    const fnRow = wrapper.findAll('[data-hol-row]').find(r => r.text().includes('Fête nationale'))!
    await fnRow.find('[data-hol-delete]').trigger('click')
    expect(mockDelete).not.toHaveBeenCalled()
    await fnRow.find('[data-hol-delete-confirm]').trigger('click')
    await flushPromises()
    expect(mockDelete).toHaveBeenCalledWith('public_holidays/10/')
  })
})
