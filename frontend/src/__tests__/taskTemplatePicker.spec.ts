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
        {
          name: 'Esquisse', client_facing_label: '', billing_mode: 'FORFAIT',
          subtasks: [{ name: 'Variante A', client_facing_label: '', billing_mode: 'FORFAIT' }],
        },
        { name: 'Estimation', client_facing_label: '', billing_mode: 'FORFAIT', subtasks: [] },
      ],
    },
  ],
}

function mountPicker(props: Record<string, unknown> = {}) {
  return mount(TaskTemplatePicker, { props: { projectId: 7, ...props } })
}

describe('TaskTemplatePicker', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    vi.mocked(projectApi.taskSuggestions).mockResolvedValue({ data: SUGG } as never)
    vi.mocked(projectApi.createTask).mockResolvedValue({ data: { id: 99 } } as never)
  })

  it('masqué (niveau projet) quand le projet a déjà des tâches', async () => {
    vi.mocked(projectApi.taskSuggestions).mockResolvedValue(
      { data: { has_tasks: true, groups: [] } } as never,
    )
    const w = mountPicker()
    await flushPromises()
    expect(w.find('[data-task-picker]').exists()).toBe(false)
  })

  it('affiche les tâches ET sous-tâches (tout coché), compte les tâches', async () => {
    const w = mountPicker()
    await flushPromises()
    expect(w.find('[data-task-picker]').exists()).toBe(true)
    expect(w.findAll('[data-suggestion]')).toHaveLength(2) // 2 tâches racines
    expect(w.findAll('[data-suggestion-sub]')).toHaveLength(1) // 1 sous-tâche
    expect(w.text()).toContain('Variante A')
    expect(w.find('[data-create-tasks]').text()).toContain('(2)')
  })

  it('crée la tâche puis sa sous-tâche (parent = tâche créée) et émet created', async () => {
    const w = mountPicker()
    await flushPromises()
    await w.find('[data-create-tasks]').trigger('click')
    await flushPromises()
    // Esquisse (TASK) + Variante A (SUBTASK, parent) + Estimation (TASK) = 3
    expect(projectApi.createTask).toHaveBeenCalledTimes(3)
    expect(projectApi.createTask).toHaveBeenCalledWith(
      7, expect.objectContaining({ name: 'Variante A', task_type: 'SUBTASK', parent: 99 }),
    )
    expect(w.emitted('created')).toBeTruthy()
  })

  it('ciblé sur une phase : visible même si le projet a des tâches + filtre ?phase', async () => {
    vi.mocked(projectApi.taskSuggestions).mockResolvedValue(
      { data: { ...SUGG, has_tasks: true } } as never,
    )
    const w = mountPicker({ phaseId: 1 })
    await flushPromises()
    expect(w.find('[data-task-picker]').exists()).toBe(true) // visible malgré has_tasks
    expect(projectApi.taskSuggestions).toHaveBeenCalledWith(7, { phase: '1' })
  })
})
