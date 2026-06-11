import { mount, flushPromises } from '@vue/test-utils'
import { beforeEach, describe, expect, it, vi } from 'vitest'

vi.mock('@/plugins/axios', () => ({
  default: { get: vi.fn(), post: vi.fn(), patch: vi.fn(), delete: vi.fn() },
}))

import apiClient from '@/plugins/axios'
import AssignResourceDialog from '../features/projects/components/AssignResourceDialog.vue'

const mockGet = apiClient.get as unknown as ReturnType<typeof vi.fn>
const mockPost = apiClient.post as unknown as ReturnType<typeof vi.fn>

const USERS = [
  { id: 1, username: 'amonty', email: 'a@x.com', first_name: 'Anne', last_name: 'Monty' },
  { id: 2, username: 'jbel', email: 'j@x.com', first_name: 'Jean', last_name: 'Bélanger' },
]
const VIRTUALS = [{ id: 7, name: 'Architecte senior', is_active: true }]
const TEAMS = [{ id: 3, name: 'Studio BIM' }]
const PHASES = [
  { id: 10, name: 'Conception' },
  { id: 11, name: 'Préliminaires' },
]
const TASKS = [
  { id: 100, phase: 10, parent: null, wbs_code: '1.1', name: 'Esquisse', budgeted_hours: '10', is_active: true },
  { id: 200, phase: 11, parent: null, wbs_code: '3.1', name: 'Plans', budgeted_hours: '0', is_active: true },
  { id: 201, phase: 11, parent: 200, wbs_code: '3.1.1', name: 'Étages', budgeted_hours: '40', is_active: true },
]

function mockApi() {
  mockGet.mockImplementation((url: string) => {
    if (url === 'users/search/') return Promise.resolve({ data: USERS })
    if (url === 'virtual-resources/') return Promise.resolve({ data: VIRTUALS })
    if (url === 'teams/') return Promise.resolve({ data: TEAMS })
    if (url.includes('/phases/')) return Promise.resolve({ data: PHASES })
    if (url.includes('/tasks/')) return Promise.resolve({ data: TASKS })
    return Promise.resolve({ data: [] })
  })
}

function mountDialog(initialScope?: { type: 'project' | 'phase' | 'task'; id?: number | null }) {
  return mount(AssignResourceDialog, {
    props: { open: true, projectId: 3, initialScope },
    global: { stubs: { teleport: true } },
  })
}

describe('AssignResourceDialog — Qui / Où / Combien', () => {
  beforeEach(() => {
    mockGet.mockReset()
    mockPost.mockReset()
    mockApi()
    mockPost.mockResolvedValue({ data: { id: 99 } })
  })

  it('employé + tâche → POST allocations/ avec employee et task', async () => {
    const wrapper = mountDialog()
    await flushPromises()
    // Qui : Anne
    await wrapper.findAll('[data-ard-opt]').find(o => o.text().includes('Anne'))!.trigger('click')
    // Où : tâche feuille 1.1
    await wrapper.findAll('[data-ard-scope]').find(o => o.text().includes('Esquisse'))!.trigger('click')
    // Combien
    await wrapper.find('[data-ard-hpw]').setValue('20')
    await wrapper.find('[data-ard-submit]').trigger('click')
    await flushPromises()
    expect(mockPost).toHaveBeenCalledWith(
      'allocations/',
      expect.objectContaining({ employee: 1, task: 100, project: 3, hours_per_week: 20 }),
    )
    expect(wrapper.emitted('assigned')).toBeTruthy()
  })

  it('équipe + phase → POST assign_team_to_phase', async () => {
    const wrapper = mountDialog()
    await flushPromises()
    await wrapper.find('[data-ard-who-team]').trigger('click')
    await wrapper.findAll('[data-ard-opt]').find(o => o.text().includes('Studio BIM'))!.trigger('click')
    await wrapper.findAll('[data-ard-scope]').find(o => o.text().includes('Phase Préliminaires'))!.trigger('click')
    await wrapper.find('[data-ard-submit]').trigger('click')
    await flushPromises()
    expect(mockPost).toHaveBeenCalledWith(
      'projects/3/assign_team_to_phase/',
      expect.objectContaining({ team_id: 3, phase_id: 11 }),
    )
  })

  it('profil virtuel : « Projet entier » indisponible ; virtuel + tâche → POST virtual_resource', async () => {
    const wrapper = mountDialog()
    await flushPromises()
    await wrapper.find('[data-ard-who-virt]').trigger('click')
    expect(wrapper.find('[data-ard-scope-project]').exists()).toBe(false)
    await wrapper.findAll('[data-ard-opt]').find(o => o.text().includes('Architecte senior'))!.trigger('click')
    await wrapper.findAll('[data-ard-scope]').find(o => o.text().includes('Étages'))!.trigger('click')
    await wrapper.find('[data-ard-submit]').trigger('click')
    await flushPromises()
    expect(mockPost).toHaveBeenCalledWith(
      'allocations/',
      expect.objectContaining({ virtual_resource: 7, task: 201 }),
    )
  })

  it('employé + projet entier → POST members/ (membre sans planification)', async () => {
    const wrapper = mountDialog()
    await flushPromises()
    await wrapper.findAll('[data-ard-opt]').find(o => o.text().includes('Jean'))!.trigger('click')
    await wrapper.find('[data-ard-scope-project]').trigger('click')
    await wrapper.find('[data-ard-submit]').trigger('click')
    await flushPromises()
    expect(mockPost).toHaveBeenCalledWith('projects/3/members/', { user_id: 2 })
  })

  it('bouton Affecter désactivé tant que Qui + Où ne sont pas choisis', async () => {
    const wrapper = mountDialog()
    await flushPromises()
    expect(wrapper.find('[data-ard-submit]').attributes('disabled')).toBeDefined()
    await wrapper.findAll('[data-ard-opt]')[0]!.trigger('click')
    expect(wrapper.find('[data-ard-submit]').attributes('disabled')).toBeDefined()
  })

  it('avertit (non bloquant) quand les heures planifiées dépassent le budget de la tâche', async () => {
    const wrapper = mountDialog()
    await flushPromises()
    await wrapper.findAll('[data-ard-opt]')[0]!.trigger('click')
    await wrapper.findAll('[data-ard-scope]').find(o => o.text().includes('Esquisse'))!.trigger('click') // budget 10 h
    await wrapper.find('[data-ard-hpw]').setValue('20')
    await wrapper.find('[data-ard-start]').setValue('2026-03-02')
    await wrapper.find('[data-ard-end]').setValue('2026-03-30')
    expect(wrapper.find('[data-ard-recap]').text()).toContain('dépassement')
    expect(wrapper.find('[data-ard-submit]').attributes('disabled')).toBeUndefined()
  })

  it('charge les tâches sans pagination tronquée (page_size explicite)', async () => {
    mountDialog()
    await flushPromises()
    const taskCall = mockGet.mock.calls.find(c => String(c[0]).includes('/tasks/'))!
    expect(taskCall[1]?.params?.page_size).toBe('500')
  })

  it('les tâches-mères (regroupements) ne sont pas sélectionnables', async () => {
    const wrapper = mountDialog()
    await flushPromises()
    const labels = wrapper.findAll('[data-ard-scope]').map(o => o.text())
    expect(labels.some(l => l.includes('Étages'))).toBe(true)
    expect(labels.some(l => l.includes('Plans'))).toBe(false) // 200 a une sous-tâche
  })
})
