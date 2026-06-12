import { mount, flushPromises } from '@vue/test-utils'
import { beforeEach, describe, expect, it, vi } from 'vitest'

vi.mock('@/plugins/axios', () => ({
  default: { get: vi.fn(), post: vi.fn(), patch: vi.fn(), delete: vi.fn() },
}))

import apiClient from '@/plugins/axios'
import ProjectSettingsTab from '../features/projects/components/ProjectSettingsTab.vue'

const mockGet = apiClient.get as unknown as ReturnType<typeof vi.fn>
const mockPost = apiClient.post as unknown as ReturnType<typeof vi.fn>
const mockPatch = apiClient.patch as unknown as ReturnType<typeof vi.fn>
const mockDelete = apiClient.delete as unknown as ReturnType<typeof vi.fn>

const PROJECT = {
  id: 3, name: 'Centre culturel', start_date: '2026-02-12', end_date: '2026-12-18',
  business_unit: 'Architecture', pm: 1, associate_in_charge: 2,
  construction_cost: 24500000, is_internal: false,
  services_transversaux: ['BIM', 'DD'],
  client: 5, client_name: 'Ville de Montréal',
}
const CLIENTS = [
  { id: 5, name: 'Ville de Montréal' },
  { id: 6, name: 'Université Laval' },
]
const ADDRESSES = [
  { id: 9, address_line_1: '275 rue Notre-Dame E', address_line_2: '', city: 'Montréal', province: 'QC', postal_code: 'H2Y 1C6', country: 'Canada', is_billing: true, is_primary: true },
]
const USERS = [
  { id: 1, username: 'amonty', email: 'a@x.com' },
  { id: 2, username: 'jbel', email: 'j@x.com' },
]
const VIRTUALS = [
  { id: 7, name: 'Architecte senior', default_hourly_rate: '145.00', is_active: true },
  { id: 8, name: 'Ancien profil', default_hourly_rate: '90.00', is_active: false },
]
const BLOCKS = [
  { id: 1, employee: 4, employee_name: 'Marc Privé', phase: null, phase_name: '', task: 100, task_name: 'Esquisse', task_wbs_code: '1.1' },
  { id: 2, employee: 5, employee_name: 'Luc Total', phase: null, phase_name: '', task: null, task_name: '', task_wbs_code: '' },
]

function mockApi() {
  mockGet.mockImplementation((url: string) => {
    if (url === 'virtual-resources/') return Promise.resolve({ data: VIRTUALS })
    if (url === 'time_entry_blocks/') return Promise.resolve({ data: BLOCKS })
    if (url === 'clients/') return Promise.resolve({ data: CLIENTS })
    if (url.includes('/addresses/')) return Promise.resolve({ data: ADDRESSES })
    return Promise.resolve({ data: [] })
  })
}

function mountTab(projectOverrides: Record<string, unknown> = {}) {
  return mount(ProjectSettingsTab, {
    props: {
      projectId: 3,
      project: { ...PROJECT, ...projectOverrides },
      users: USERS,
      businessUnits: [{ id: 1, name: 'Architecture' }],
    },
    global: { stubs: { RouterLink: { template: '<a data-admin-link><slot /></a>' } } },
  })
}

describe('ProjectSettingsTab — onglet ⚙️ Paramètres du projet', () => {
  beforeEach(() => {
    mockGet.mockReset()
    mockPost.mockReset()
    mockPatch.mockReset()
    mockDelete.mockReset()
    mockApi()
    mockPost.mockResolvedValue({ data: { id: 99 } })
    mockPatch.mockResolvedValue({ data: {} })
    mockDelete.mockResolvedValue({ data: {} })
  })

  it('pré-remplit les informations du projet et PATCH à l’enregistrement', async () => {
    const wrapper = mountTab()
    await flushPromises()
    const name = wrapper.find('[data-ps-name]')
    expect((name.element as HTMLInputElement).value).toBe('Centre culturel')
    await name.setValue('Centre culturel — rev')
    await wrapper.find('[data-ps-cc]').setValue('25 000 000')
    await wrapper.find('[data-ps-save]').trigger('click')
    await flushPromises()
    expect(mockPatch).toHaveBeenCalledWith(
      'projects/3/',
      expect.objectContaining({ name: 'Centre culturel — rev', construction_cost: 25000000, pm: 1 }),
    )
    expect(wrapper.emitted('updated')).toBeTruthy()
  })

  it('refuse fin avant début (pas de PATCH, message)', async () => {
    const wrapper = mountTab()
    await flushPromises()
    await wrapper.find('[data-ps-end]').setValue('2026-01-01')
    await wrapper.find('[data-ps-save]').trigger('click')
    expect(mockPatch).not.toHaveBeenCalled()
    expect(wrapper.text()).toContain('antérieure')
  })

  it('masque le coût de construction pour un projet interne', async () => {
    const wrapper = mountTab({ is_internal: true })
    await flushPromises()
    expect(wrapper.find('[data-ps-cc]').exists()).toBe(false)
  })

  it('liste les profils virtuels actifs et supprime avec confirmation inline', async () => {
    const wrapper = mountTab()
    await flushPromises()
    const rows = wrapper.findAll('[data-ps-virtual]')
    expect(rows).toHaveLength(1) // seuls les actifs
    expect(rows[0]!.text()).toContain('Architecte senior')
    await wrapper.find('[data-ps-virtual-delete]').trigger('click')
    expect(mockDelete).not.toHaveBeenCalled()
    await wrapper.find('[data-ps-virtual-delete-confirm]').trigger('click')
    await flushPromises()
    expect(mockDelete).toHaveBeenCalledWith('virtual-resources/7/')
  })

  it('modifie un profil virtuel (PATCH nom + taux)', async () => {
    const wrapper = mountTab()
    await flushPromises()
    await wrapper.find('[data-ps-virtual-edit]').trigger('click')
    await wrapper.find('[data-ps-virtual-name]').setValue('Architecte principal')
    await wrapper.find('[data-ps-virtual-save]').trigger('click')
    await flushPromises()
    expect(mockPatch).toHaveBeenCalledWith(
      'virtual-resources/7/',
      expect.objectContaining({ name: 'Architecte principal' }),
    )
  })

  it('liste les blocages actifs (portée lisible) et débloque', async () => {
    const wrapper = mountTab()
    await flushPromises()
    const rows = wrapper.findAll('[data-ps-block]')
    expect(rows).toHaveLength(2)
    expect(rows[0]!.text()).toContain('Marc Privé')
    expect(rows[0]!.text()).toContain('Esquisse')
    expect(rows[1]!.text()).toContain('Projet entier')
    await rows[0]!.find('[data-ps-unblock]').trigger('click')
    await flushPromises()
    expect(mockDelete).toHaveBeenCalledWith('time_entry_blocks/1/')
  })

  it('carte Client : changer le client du projet → PATCH projects/3/', async () => {
    const wrapper = mountTab()
    await flushPromises()
    await wrapper.find('[data-ps-client-select]').setValue('6')
    await wrapper.find('[data-ps-client-save]').trigger('click')
    await flushPromises()
    expect(mockPatch).toHaveBeenCalledWith('projects/3/', expect.objectContaining({ client: 6 }))
    expect(wrapper.emitted('updated')).toBeTruthy()
  })

  it('carte Client : liste les adresses avec badges facturation/principale', async () => {
    const wrapper = mountTab()
    await flushPromises()
    const rows = wrapper.findAll('[data-ps-address]')
    expect(rows).toHaveLength(1)
    expect(rows[0]!.text()).toContain('275 rue Notre-Dame E')
    expect(rows[0]!.text()).toContain('Facturation')
  })

  it('carte Client : modifier une adresse → PATCH clients/5/addresses/9/', async () => {
    const wrapper = mountTab()
    await flushPromises()
    await wrapper.find('[data-ps-address-edit]').trigger('click')
    await wrapper.find('[data-ps-addr-line1]').setValue('100 rue Sainte-Catherine O')
    await wrapper.find('[data-ps-addr-save]').trigger('click')
    await flushPromises()
    expect(mockPatch).toHaveBeenCalledWith(
      'clients/5/addresses/9/',
      expect.objectContaining({ address_line_1: '100 rue Sainte-Catherine O' }),
    )
  })

  it('carte Client : ajouter une adresse de facturation → POST clients/5/addresses/', async () => {
    const wrapper = mountTab()
    await flushPromises()
    await wrapper.find('[data-ps-address-add]').trigger('click')
    await wrapper.find('[data-ps-addr-line1]').setValue('1 place Ville-Marie')
    await wrapper.find('[data-ps-addr-city]').setValue('Montréal')
    await wrapper.find('[data-ps-addr-billing]').setValue(true)
    await wrapper.find('[data-ps-addr-save]').trigger('click')
    await flushPromises()
    expect(mockPost).toHaveBeenCalledWith(
      'clients/5/addresses/',
      expect.objectContaining({ address_line_1: '1 place Ville-Marie', is_billing: true }),
    )
  })

  it('carte Client : supprimer une adresse avec confirmation inline', async () => {
    const wrapper = mountTab()
    await flushPromises()
    await wrapper.find('[data-ps-address-delete]').trigger('click')
    expect(mockDelete).not.toHaveBeenCalled()
    await wrapper.find('[data-ps-address-delete-confirm]').trigger('click')
    await flushPromises()
    expect(mockDelete).toHaveBeenCalledWith('clients/5/addresses/9/')
  })

  it('expose les liens vers les référentiels admin', async () => {
    const wrapper = mountTab()
    await flushPromises()
    expect(wrapper.findAll('[data-admin-link]').length).toBeGreaterThanOrEqual(3)
  })

  it('affiche les services transversaux en lecture seule', async () => {
    const wrapper = mountTab()
    await flushPromises()
    expect(wrapper.text()).toContain('BIM')
    expect(wrapper.text()).toContain('DD')
  })
})
