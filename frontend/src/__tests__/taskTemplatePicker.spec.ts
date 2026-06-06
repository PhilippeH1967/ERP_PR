import { mount, flushPromises } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'

vi.mock('@/features/projects/api/projectApi', () => ({
  projectApi: { taskSuggestions: vi.fn(), createTask: vi.fn() },
}))

import { projectApi } from '@/features/projects/api/projectApi'
import TaskTemplatePicker from '@/features/projects/components/TaskTemplatePicker.vue'

const SUGG = {
  has_tasks: false,
  groups: [
    {
      phase_id: 1, phase_code: '1', phase_name: 'Concept',
      tasks: [
        { name: 'Esquisse', client_facing_label: '', billing_mode: 'FORFAIT' },
        { name: 'Estimation classe D', client_facing_label: '', billing_mode: 'FORFAIT' },
      ],
    },
    {
      phase_id: 2, phase_code: '5', phase_name: 'Surveillance',
      tasks: [{ name: 'Réunions de chantier', client_facing_label: '', billing_mode: 'HORAIRE' }],
    },
  ],
}

function mountPicker() {
  return mount(TaskTemplatePicker, { props: { projectId: 7 } })
}

describe('TaskTemplatePicker', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    vi.mocked(projectApi.taskSuggestions).mockResolvedValue({ data: SUGG } as never)
    vi.mocked(projectApi.createTask).mockResolvedValue({ data: {} } as never)
  })

  it('reste masqué quand le projet a déjà des tâches', async () => {
    vi.mocked(projectApi.taskSuggestions).mockResolvedValue(
      { data: { has_tasks: true, groups: [] } } as never,
    )
    const w = mountPicker()
    await flushPromises()
    expect(w.find('[data-task-picker]').exists()).toBe(false)
  })

  it('affiche les suggestions par phase (tout coché) à l’état vide', async () => {
    const w = mountPicker()
    await flushPromises()
    expect(w.find('[data-task-picker]').exists()).toBe(true)
    expect(w.findAll('[data-suggestion]')).toHaveLength(3)
    expect(w.text()).toContain('Esquisse')
    expect(w.text()).toContain('Concept')
    expect(w.find('[data-create-tasks]').text()).toContain('(3)') // 3 cochées
  })

  it('crée les tâches sélectionnées et émet created', async () => {
    const w = mountPicker()
    await flushPromises()
    // Décocher la 1re → 2 restantes
    await w.findAll('[data-suggestion] input')[0]!.trigger('change')
    expect(w.find('[data-create-tasks]').text()).toContain('(2)')
    await w.find('[data-create-tasks]').trigger('click')
    await flushPromises()
    expect(projectApi.createTask).toHaveBeenCalledTimes(2)
    expect(projectApi.createTask).toHaveBeenCalledWith(
      7, expect.objectContaining({ phase: expect.any(Number), name: expect.any(String) }),
    )
    expect(w.emitted('created')).toBeTruthy()
  })
})
