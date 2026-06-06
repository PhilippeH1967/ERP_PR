import { mount, flushPromises } from '@vue/test-utils'
import { beforeEach, describe, expect, it, vi } from 'vitest'

vi.mock('@/plugins/axios', () => ({
  default: { get: vi.fn(), post: vi.fn(), patch: vi.fn(), delete: vi.fn() },
}))
vi.mock('vue-router', () => ({ useRouter: () => ({ push: vi.fn() }) }))

import apiClient from '@/plugins/axios'
import StandardTaskSettings from '../features/admin/views/StandardTaskSettings.vue'

const mockGet = apiClient.get as unknown as ReturnType<typeof vi.fn>
const mockPost = apiClient.post as unknown as ReturnType<typeof vi.fn>
const mockDelete = apiClient.delete as unknown as ReturnType<typeof vi.fn>

const PHASES = [
  { id: 1, code: 'CONCEPT', name: 'Conception', order: 1 },
  { id: 2, code: 'EXEC', name: 'Exécution', order: 2 },
]
const TASKS = [
  {
    id: 10,
    standard_phase: 1,
    parent: null,
    name: 'Plans préliminaires',
    client_facing_label: '',
    billing_mode: 'FORFAIT',
    order: 0,
    is_active: true,
  },
  {
    id: 11,
    standard_phase: 1,
    parent: 10,
    name: 'Esquisse',
    client_facing_label: '',
    billing_mode: 'HORAIRE',
    order: 0,
    is_active: true,
  },
]

function mockApi(tasks: unknown[] = TASKS, phases: unknown[] = PHASES) {
  mockGet.mockImplementation((url: string) => {
    if (url === 'standard_phases/') return Promise.resolve({ data: phases })
    if (url === 'standard_tasks/') return Promise.resolve({ data: tasks })
    return Promise.resolve({ data: [] })
  })
}

describe('StandardTaskSettings — catalogue tâches/sous-tâches standard', () => {
  beforeEach(() => {
    mockGet.mockReset()
    mockPost.mockReset()
    mockDelete.mockReset()
    mockApi()
    mockPost.mockResolvedValue({ data: { id: 99 } })
    mockDelete.mockResolvedValue({ data: {} })
  })

  it('groupe les tâches racines et leurs sous-tâches sous chaque phase', async () => {
    const wrapper = mount(StandardTaskSettings)
    await flushPromises()
    expect(mockGet).toHaveBeenCalledWith('standard_phases/')
    expect(mockGet).toHaveBeenCalledWith('standard_tasks/')
    expect(wrapper.findAll('.phase-card')).toHaveLength(2)
    expect(wrapper.findAll('.task-row')).toHaveLength(1)
    expect(wrapper.findAll('.subtask-row')).toHaveLength(1)
    expect(wrapper.text()).toContain('Plans préliminaires')
    expect(wrapper.text()).toContain('Esquisse')
  })

  it('ouvre « + Tâche » pour une phase (titre = code · nom de phase)', async () => {
    const wrapper = mount(StandardTaskSettings)
    await flushPromises()
    await wrapper.findAll('.phase-head .btn-primary')[1]!.trigger('click') // phase EXEC
    expect(wrapper.find('.modal').exists()).toBe(true)
    expect(wrapper.text()).toContain('Nouvelle tâche — EXEC')
  })

  it('ouvre « + Sous-tâche » avec le parent pré-renseigné', async () => {
    const wrapper = mount(StandardTaskSettings)
    await flushPromises()
    const subBtn = wrapper
      .findAll('.task-actions .btn-icon')
      .find((b) => b.text() === '+ Sous-tâche')!
    expect(subBtn).toBeTruthy()
    await subBtn.trigger('click')
    expect(wrapper.text()).toContain('Nouvelle sous-tâche — Plans préliminaires')
  })

  it('crée une tâche racine (POST standard_phase renseignée, parent null)', async () => {
    const wrapper = mount(StandardTaskSettings)
    await flushPromises()
    await wrapper.findAll('.phase-head .btn-primary')[0]!.trigger('click') // phase CONCEPT
    await wrapper.find('.modal input[type=text]').setValue('Étude de faisabilité')
    await wrapper.find('.modal form').trigger('submit')
    await flushPromises()
    expect(mockPost).toHaveBeenCalledWith(
      'standard_tasks/',
      expect.objectContaining({ standard_phase: 1, parent: null, name: 'Étude de faisabilité' }),
    )
  })

  it('refuse une tâche sans nom', async () => {
    const wrapper = mount(StandardTaskSettings)
    await flushPromises()
    await wrapper.findAll('.phase-head .btn-primary')[0]!.trigger('click')
    await wrapper.find('.modal form').trigger('submit')
    expect(mockPost).not.toHaveBeenCalled()
    expect(wrapper.text()).toContain('Le nom est obligatoire')
  })

  it('demande confirmation inline avant suppression d’une tâche', async () => {
    const wrapper = mount(StandardTaskSettings)
    await flushPromises()
    await wrapper.find('.task-row .btn-icon-danger').trigger('click')
    expect(mockDelete).not.toHaveBeenCalled()
    const confirmBtn = wrapper
      .findAll('.task-row .btn-icon-danger')
      .find((b) => b.text() === 'Confirmer')!
    expect(confirmBtn).toBeTruthy()
    await confirmBtn.trigger('click')
    await flushPromises()
    expect(mockDelete).toHaveBeenCalledWith('standard_tasks/10/')
  })

  it('affiche un état vide invitant à définir d’abord les phases standard', async () => {
    mockApi([], [])
    const wrapper = mount(StandardTaskSettings)
    await flushPromises()
    expect(wrapper.text()).toContain('Aucune phase standard')
  })
})
