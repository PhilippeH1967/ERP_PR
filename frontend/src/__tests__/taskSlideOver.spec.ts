import { mount, flushPromises } from '@vue/test-utils'
import { beforeEach, describe, expect, it, vi } from 'vitest'

vi.mock('@/plugins/axios', () => ({
  default: { get: vi.fn(), post: vi.fn(), patch: vi.fn(), delete: vi.fn() },
}))

import apiClient from '@/plugins/axios'
import TaskSlideOver from '../features/planning/components/TaskSlideOver.vue'

const mockGet = apiClient.get as unknown as ReturnType<typeof vi.fn>
const mockPost = apiClient.post as unknown as ReturnType<typeof vi.fn>
const mockPatch = apiClient.patch as unknown as ReturnType<typeof vi.fn>
const mockDelete = apiClient.delete as unknown as ReturnType<typeof vi.fn>

const TASK = {
  id: 5, name: 'Plans', client_facing_label: 'Client drawings', wbs_code: '1.1',
  phase: 1, phase_name: 'Concept',
  start_date: '2026-01-01', end_date: '2026-03-01',
  budgeted_hours: '80', budgeted_cost: '9600', billing_mode: 'FORFAIT',
  hourly_rate: '120', is_active: true, progress_pct: 0,
}
const PHASES = [
  { id: 1, name: 'Concept' },
  { id: 2, name: 'Préliminaires' },
]
const ALLOCS = [
  {
    id: 10, employee: 1, employee_name: 'Anne Monty', virtual_resource: null,
    virtual_resource_name: '', hours_per_week: 20, start_date: '2026-01-01',
    end_date: '2026-02-01', status: 'ACTIVE', distribution_mode: 'uniform',
    time_unit: 'week', time_breakdown: null,
  },
  {
    id: 11, employee: null, employee_name: '', virtual_resource: 7,
    virtual_resource_name: 'Architecte senior', hours_per_week: 15,
    start_date: '2026-01-01', end_date: '2026-02-01', status: 'ACTIVE',
    distribution_mode: 'uniform', time_unit: 'week', time_breakdown: null,
  },
]
const VIRTUALS = [
  { id: 7, name: 'Architecte senior', is_active: true },
  { id: 8, name: 'Dessinateur junior', is_active: true },
]
const USERS = [
  { id: 1, username: 'amonty', email: 'a@x.com', first_name: 'Anne', last_name: 'Monty' },
  { id: 2, username: 'jbel', email: 'j@x.com', first_name: 'Jean', last_name: 'Bélanger' },
]
const TEAMS = [
  { id: 3, name: 'Studio BIM' },
  { id: 4, name: 'Équipe paysage' },
]

function mockApi() {
  mockGet.mockImplementation((url: string) => {
    if (url.includes('/phases/')) return Promise.resolve({ data: PHASES })
    if (url.includes('/tasks/')) return Promise.resolve({ data: TASK })
    if (url === 'allocations/') return Promise.resolve({ data: ALLOCS })
    if (url === 'virtual-resources/') return Promise.resolve({ data: VIRTUALS })
    if (url === 'users/search/') return Promise.resolve({ data: USERS })
    if (url === 'teams/') return Promise.resolve({ data: TEAMS })
    return Promise.resolve({ data: [] })
  })
}

function mountSlideOver() {
  return mount(TaskSlideOver, {
    props: { open: true, projectId: 3, taskId: 5 },
    global: { stubs: { teleport: true } },
  })
}

describe('TaskSlideOver — affectation employés + ressources virtuelles', () => {
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

  it('affiche les employés et les ressources virtuelles dans deux sections séparées', async () => {
    const wrapper = mountSlideOver()
    await flushPromises()

    const empSection = wrapper.find('[data-section="employee"]')
    const virtSection = wrapper.find('[data-section="virtual"]')
    expect(empSection.exists()).toBe(true)
    expect(virtSection.exists()).toBe(true)
    // Employé réel dans la section équipe, pas dans la virtuelle.
    expect(empSection.text()).toContain('Anne Monty')
    expect(empSection.text()).not.toContain('Architecte senior')
    // Ressource virtuelle dans sa section, avec un marqueur « Virtuel ».
    expect(virtSection.text()).toContain('Architecte senior')
    expect(virtSection.text()).toMatch(/Virtuel/i)
  })

  it('le picker propose les ressources virtuelles et POST virtual_resource', async () => {
    const wrapper = mountSlideOver()
    await flushPromises()

    await wrapper.find('[data-assign-open]').trigger('click')
    await flushPromises()

    const virtOpts = wrapper.findAll('[data-assign-virtual]')
    expect(virtOpts.length).toBeGreaterThan(0)
    const dessinateur = virtOpts.find((o) => o.text().includes('Dessinateur junior'))!
    expect(dessinateur).toBeTruthy()
    await dessinateur.trigger('click')
    await flushPromises()

    expect(mockPost).toHaveBeenCalledWith(
      'allocations/',
      expect.objectContaining({ virtual_resource: 8, project: 3, task: 5 }),
    )
    const payload = mockPost.mock.calls.at(-1)![1] as Record<string, unknown>
    expect(payload.employee).toBeUndefined()
  })

  it('le picker propose les équipes et POST assign_team_to_task', async () => {
    const wrapper = mountSlideOver()
    await flushPromises()

    await wrapper.find('[data-assign-open]').trigger('click')
    await flushPromises()

    const teamOpts = wrapper.findAll('[data-assign-team]')
    expect(teamOpts.length).toBe(2)
    const bim = teamOpts.find((o) => o.text().includes('Studio BIM'))!
    await bim.trigger('click')
    await flushPromises()

    expect(mockPost).toHaveBeenCalledWith(
      'projects/3/assign_team_to_task/',
      expect.objectContaining({ team_id: 3, task_id: 5 }),
    )
  })

  it('affecter un employé POST employee (régression)', async () => {
    const wrapper = mountSlideOver()
    await flushPromises()

    await wrapper.find('[data-assign-open]').trigger('click')
    await flushPromises()

    const empOpts = wrapper.findAll('[data-assign-employee]')
    const jean = empOpts.find((o) => o.text().includes('jbel'))!
    await jean.trigger('click')
    await flushPromises()

    expect(mockPost).toHaveBeenCalledWith(
      'allocations/',
      expect.objectContaining({ employee: 2, project: 3, task: 5 }),
    )
    const payload = mockPost.mock.calls.at(-1)![1] as Record<string, unknown>
    expect(payload.virtual_resource).toBeUndefined()
  })

  it('fiche unique : identité pré-remplie et PATCH nom/libellé/phase', async () => {
    const wrapper = mountSlideOver()
    await flushPromises()
    const nameInput = wrapper.find('[data-tso-name]')
    expect((nameInput.element as HTMLInputElement).value).toBe('Plans')
    await nameInput.setValue('Plans révisés')
    await wrapper.find('[data-tso-phase]').setValue('2')
    await wrapper.find('[data-tso-save-identity]').trigger('click')
    await flushPromises()
    expect(mockPatch).toHaveBeenCalledWith(
      'projects/3/tasks/5/',
      expect.objectContaining({ name: 'Plans révisés', phase: 2 }),
    )
  })

  it('fiche unique : budget éditable (PATCH heures/coût/mode)', async () => {
    const wrapper = mountSlideOver()
    await flushPromises()
    await wrapper.find('[data-tso-bh]').setValue('100')
    await wrapper.find('[data-tso-save-budget]').trigger('click')
    await flushPromises()
    expect(mockPatch).toHaveBeenCalledWith(
      'projects/3/tasks/5/',
      expect.objectContaining({ budgeted_hours: '100' }),
    )
  })

  it('fiche unique : fermer la saisie PATCH is_active=false', async () => {
    const wrapper = mountSlideOver()
    await flushPromises()
    await wrapper.find('[data-tso-active]').trigger('click')
    await flushPromises()
    expect(mockPatch).toHaveBeenCalledWith(
      'projects/3/tasks/5/',
      expect.objectContaining({ is_active: false }),
    )
  })

  it('fiche unique : suppression avec confirmation inline puis DELETE', async () => {
    const wrapper = mountSlideOver()
    await flushPromises()
    await wrapper.find('[data-tso-delete]').trigger('click')
    expect(mockDelete).not.toHaveBeenCalled()
    await wrapper.find('[data-tso-delete-confirm]').trigger('click')
    await flushPromises()
    expect(mockDelete).toHaveBeenCalledWith('projects/3/tasks/5/')
  })
})
