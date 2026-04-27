import { mount, flushPromises } from '@vue/test-utils'
import { beforeEach, describe, expect, it, vi } from 'vitest'

vi.mock('@/plugins/axios', () => ({
  default: { get: vi.fn(), post: vi.fn(), patch: vi.fn(), delete: vi.fn() },
}))

import apiClient from '@/plugins/axios'
import TaxSchemeManager from '../features/admin/components/TaxSchemeManager.vue'

const mockGet = apiClient.get as unknown as ReturnType<typeof vi.fn>
const mockPost = apiClient.post as unknown as ReturnType<typeof vi.fn>
const mockPatch = apiClient.patch as unknown as ReturnType<typeof vi.fn>
const mockDelete = apiClient.delete as unknown as ReturnType<typeof vi.fn>

const SCHEME_QC = {
  id: 1, name: 'Québec — TPS+TVQ', province: 'QC', description: '',
  is_default: true, is_active: true,
  rates: [
    { id: 10, tax_type: 'TPS', label: 'Fédéral', rate: '5.000', is_active: true },
    { id: 11, tax_type: 'TVQ', label: 'Provincial', rate: '9.975', is_active: true },
  ],
}

describe('TaxSchemeManager', () => {
  beforeEach(() => {
    mockGet.mockReset()
    mockPost.mockReset()
    mockPatch.mockReset()
    mockDelete.mockReset()
    mockGet.mockResolvedValue({ data: [SCHEME_QC] })
    mockPost.mockResolvedValue({ data: { id: 99 } })
    mockPatch.mockResolvedValue({ data: {} })
    mockDelete.mockResolvedValue({ data: {} })
  })

  it('charge et affiche les schémas existants', async () => {
    const wrapper = mount(TaxSchemeManager)
    await flushPromises()
    expect(mockGet).toHaveBeenCalledWith('tax_schemes/')
    expect(wrapper.findAll('[data-scheme-row]')).toHaveLength(1)
    expect(wrapper.text()).toContain('Québec — TPS+TVQ')
    expect(wrapper.findAll('[data-rate-row]')).toHaveLength(2)
  })

  it('ouvre le formulaire au clic sur "+ Nouveau schéma"', async () => {
    const wrapper = mount(TaxSchemeManager)
    await flushPromises()
    await wrapper.find('[data-add-scheme]').trigger('click')
    expect(wrapper.find('[data-scheme-form]').exists()).toBe(true)
    expect(wrapper.find('[data-scheme-name]').exists()).toBe(true)
  })

  it('crée un nouveau schéma au clic sur Créer', async () => {
    const wrapper = mount(TaxSchemeManager)
    await flushPromises()
    await wrapper.find('[data-add-scheme]').trigger('click')
    await wrapper.find('[data-scheme-name]').setValue('Ontario — TVH')
    await wrapper.find('[data-scheme-province]').setValue('ON')
    await wrapper.find('[data-save-scheme]').trigger('click')
    await flushPromises()
    expect(mockPost).toHaveBeenCalledWith('tax_schemes/', {
      name: 'Ontario — TVH', province: 'ON', description: '',
    })
  })

  it("refuse de créer un schéma sans nom", async () => {
    const wrapper = mount(TaxSchemeManager)
    await flushPromises()
    await wrapper.find('[data-add-scheme]').trigger('click')
    await wrapper.find('[data-save-scheme]').trigger('click')
    expect(mockPost).not.toHaveBeenCalled()
    expect(wrapper.text()).toContain('Le nom est obligatoire')
  })

  it('demande confirmation inline avant suppression du schéma', async () => {
    const wrapper = mount(TaxSchemeManager)
    await flushPromises()
    await wrapper.find('[data-delete-scheme]').trigger('click')
    expect(mockDelete).not.toHaveBeenCalled()
    const confirmBtn = wrapper.find('[data-delete-scheme-confirm]')
    expect(confirmBtn.exists()).toBe(true)
    await confirmBtn.trigger('click')
    await flushPromises()
    expect(mockDelete).toHaveBeenCalledWith('tax_schemes/1/')
  })

  it('ouvre le formulaire de taux au clic sur "+ Taux"', async () => {
    const wrapper = mount(TaxSchemeManager)
    await flushPromises()
    await wrapper.find('[data-show-rate-form]').trigger('click')
    expect(wrapper.find('[data-rate-form]').exists()).toBe(true)
  })

  it('ajoute un taux à un schéma existant', async () => {
    const wrapper = mount(TaxSchemeManager)
    await flushPromises()
    await wrapper.find('[data-show-rate-form]').trigger('click')
    await wrapper.find('[data-rate-rate]').setValue('13.000')
    await wrapper.find('[data-add-rate]').trigger('click')
    await flushPromises()
    expect(mockPost).toHaveBeenCalledWith(
      'tax_schemes/1/rates/',
      expect.objectContaining({ tax_type: 'TPS' }),
    )
    // Le rate est envoyé comme number par v-model, le backend Django accepte les deux
    const callArgs = mockPost.mock.calls[mockPost.mock.calls.length - 1]!
    const payload = callArgs[1] as { rate: string | number }
    expect(Number(payload.rate)).toBe(13)
  })

  it('demande confirmation inline avant suppression d\'un taux', async () => {
    const wrapper = mount(TaxSchemeManager)
    await flushPromises()
    const deleteBtns = wrapper.findAll('[data-delete-rate]')
    await deleteBtns[0]!.trigger('click')
    expect(mockDelete).not.toHaveBeenCalled()
    const confirmBtn = wrapper.find('[data-delete-rate-confirm]')
    expect(confirmBtn.exists()).toBe(true)
    await confirmBtn.trigger('click')
    await flushPromises()
    expect(mockDelete).toHaveBeenCalledWith('tax_schemes/1/rates/10/')
  })

  it('affiche une astuce sur les taxes attendues (TPS / TVQ)', async () => {
    const wrapper = mount(TaxSchemeManager)
    await flushPromises()
    await wrapper.find('[data-add-scheme]').trigger('click')
    expect(wrapper.text()).toMatch(/TPS 5%.*TVQ 9\.975%/)
  })
})
