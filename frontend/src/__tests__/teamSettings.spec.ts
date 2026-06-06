import { mount, flushPromises } from '@vue/test-utils'
import { beforeEach, describe, expect, it, vi } from 'vitest'

vi.mock('@/plugins/axios', () => ({
  default: { get: vi.fn(), post: vi.fn(), patch: vi.fn(), delete: vi.fn() },
}))
vi.mock('vue-router', () => ({ useRouter: () => ({ push: vi.fn() }) }))

import apiClient from '@/plugins/axios'
import TeamSettings from '../features/admin/views/TeamSettings.vue'

const mockGet = apiClient.get as unknown as ReturnType<typeof vi.fn>
const mockPost = apiClient.post as unknown as ReturnType<typeof vi.fn>
const mockPatch = apiClient.patch as unknown as ReturnType<typeof vi.fn>
const mockDelete = apiClient.delete as unknown as ReturnType<typeof vi.fn>

const TEAMS = [
  {
    id: 1,
    name: 'Studio A',
    members: [10, 11],
    member_details: [
      { id: 10, username: 'amonty', name: 'Anne Monty' },
      { id: 11, username: 'jbelanger', name: 'Jean Bélanger' },
    ],
    is_active: true,
  },
]
const USERS = [
  { id: 10, username: 'amonty', first_name: 'Anne', last_name: 'Monty' },
  { id: 11, username: 'jbelanger', first_name: 'Jean', last_name: 'Bélanger' },
  { id: 12, username: 'czoe', first_name: 'Claire', last_name: 'Zoé' },
]

function mockApi() {
  mockGet.mockImplementation((url: string) => {
    if (url === 'teams/') return Promise.resolve({ data: TEAMS })
    if (url === 'users/search/') return Promise.resolve({ data: USERS })
    return Promise.resolve({ data: [] })
  })
}

describe('TeamSettings — paramétrage des équipes (finance/paie/admin)', () => {
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

  it('charge équipes + utilisateurs et affiche les lignes avec leurs membres', async () => {
    const wrapper = mount(TeamSettings)
    await flushPromises()
    expect(mockGet).toHaveBeenCalledWith('teams/')
    expect(mockGet).toHaveBeenCalledWith('users/search/')
    expect(wrapper.findAll('[data-team-row]')).toHaveLength(1)
    expect(wrapper.text()).toContain('Studio A')
    expect(wrapper.text()).toContain('Anne Monty')
    expect(wrapper.text()).toContain('Jean Bélanger')
  })

  it('ouvre le formulaire de création avec tous les employés proposés', async () => {
    const wrapper = mount(TeamSettings)
    await flushPromises()
    await wrapper.find('[data-team-add]').trigger('click')
    expect(wrapper.find('[data-team-name]').exists()).toBe(true)
    expect(wrapper.findAll('[data-team-member-opt]')).toHaveLength(3)
  })

  it('crée une équipe avec les membres sélectionnés (payload members)', async () => {
    const wrapper = mount(TeamSettings)
    await flushPromises()
    await wrapper.find('[data-team-add]').trigger('click')
    await wrapper.find('[data-team-name]').setValue('Équipe BIM')
    await wrapper.findAll('[data-team-member-opt] input[type=checkbox]')[0]!.setValue(true)
    await wrapper.find('[data-team-save]').trigger('click')
    await flushPromises()
    expect(mockPost).toHaveBeenCalledWith(
      'teams/',
      expect.objectContaining({ name: 'Équipe BIM', is_active: true }),
    )
    const payload = mockPost.mock.calls.at(-1)![1] as { members: number[] }
    expect(payload.members).toContain(10)
  })

  it("refuse de créer une équipe sans nom", async () => {
    const wrapper = mount(TeamSettings)
    await flushPromises()
    await wrapper.find('[data-team-add]').trigger('click')
    await wrapper.find('[data-team-save]').trigger('click')
    expect(mockPost).not.toHaveBeenCalled()
    expect(wrapper.text()).toContain("Le nom de l'équipe est obligatoire")
  })

  it('filtre la liste des membres par recherche nom (sans Entrée)', async () => {
    const wrapper = mount(TeamSettings)
    await flushPromises()
    await wrapper.find('[data-team-add]').trigger('click')
    await wrapper.find('[data-team-member-search]').setValue('claire')
    expect(wrapper.findAll('[data-team-member-opt]')).toHaveLength(1)
    expect(wrapper.text()).toContain('Claire Zoé')
  })

  it('édite une équipe existante via PATCH', async () => {
    const wrapper = mount(TeamSettings)
    await flushPromises()
    await wrapper.find('[data-team-edit]').trigger('click')
    expect((wrapper.find('[data-team-name]').element as HTMLInputElement).value).toBe('Studio A')
    await wrapper.find('[data-team-name]').setValue('Studio A — rev')
    await wrapper.find('[data-team-save]').trigger('click')
    await flushPromises()
    expect(mockPatch).toHaveBeenCalledWith(
      'teams/1/',
      expect.objectContaining({ name: 'Studio A — rev' }),
    )
  })

  it('demande confirmation inline avant suppression (pas de confirm() natif)', async () => {
    const wrapper = mount(TeamSettings)
    await flushPromises()
    await wrapper.find('[data-team-row] .btn-icon-danger').trigger('click')
    expect(mockDelete).not.toHaveBeenCalled()
    const confirmBtn = wrapper
      .findAll('[data-team-row] button')
      .find((b) => b.text() === 'Confirmer')!
    expect(confirmBtn).toBeTruthy()
    await confirmBtn.trigger('click')
    await flushPromises()
    expect(mockDelete).toHaveBeenCalledWith('teams/1/')
  })
})
