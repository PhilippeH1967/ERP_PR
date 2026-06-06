import { mount, flushPromises } from '@vue/test-utils'
import { describe, expect, it, vi, beforeEach } from 'vitest'

vi.mock('@/plugins/axios', () => ({
  default: { get: vi.fn(), post: vi.fn(), patch: vi.fn(), delete: vi.fn() },
}))

import apiClient from '@/plugins/axios'
import GanttChart from '@/features/planning/components/GanttChart.vue'

// Deux phases : "Concept" a des tâches, "Vide" n'en a pas (doit être masquée).
const GANTT = {
  data: {
    project: { code: 'P1', name: 'Projet', start_date: '2026-03-01', end_date: '2026-06-01' },
    phases: [
      { id: 1, name: 'Concept', client_label: '', code: '1', type: 'REALIZATION', start_date: null, end_date: null, billing_mode: 'FORFAIT', budgeted_hours: 0, is_mandatory: false, order: 0 },
      { id: 2, name: 'Vide', client_label: '', code: '2', type: 'REALIZATION', start_date: null, end_date: null, billing_mode: 'FORFAIT', budgeted_hours: 0, is_mandatory: false, order: 1 },
    ],
    milestones: [],
    dependencies: [],
  },
}
const TASKS = {
  data: [
    { id: 11, phase: 1, wbs_code: '1.1', name: 'Feuille', client_facing_label: '', budgeted_hours: 10, progress_pct: 0, task_type: 'TASK', is_chargeable: true, start_date: '2026-03-01', end_date: '2026-04-01' },
    { id: 12, phase: 1, wbs_code: '1.2', name: 'Mere', client_facing_label: '', budgeted_hours: 0, progress_pct: 0, task_type: 'TASK', is_chargeable: false, start_date: null, end_date: null },
  ],
}
const PHASES = {
  data: [
    { id: 1, tasks_budgeted_hours: 10, planned_hours: 0, actual_hours: 0, tasks_start_date: '2026-03-01', tasks_end_date: '2026-04-01' },
    { id: 2, tasks_budgeted_hours: 0, planned_hours: 0, actual_hours: 0, tasks_start_date: null, tasks_end_date: null },
  ],
}

function mockApi() {
  vi.mocked(apiClient.get).mockImplementation((url: string) => {
    if (url.includes('gantt/project_gantt')) return Promise.resolve(GANTT)
    if (url.includes('/tasks/')) return Promise.resolve(TASKS)
    if (url.includes('/phases/')) return Promise.resolve(PHASES)
    return Promise.resolve({ data: [] })
  })
}

async function mountGantt() {
  const wrapper = mount(GanttChart, {
    props: { projectId: 1 },
    global: { stubs: { PhaseSlideOver: true, TaskSlideOver: true } },
  })
  await flushPromises()
  await flushPromises()
  return wrapper
}

describe('GanttChart', () => {
  beforeEach(() => mockApi())

  it('masque les phases sans tâche', async () => {
    const wrapper = await mountGantt()
    expect(wrapper.text()).toContain('Concept')
    expect(wrapper.text()).not.toContain('Vide')
  })

  it('rend la tâche feuille cliquable et la tâche-mère en agrégat (non cliquable)', async () => {
    const wrapper = await mountGantt()
    const leaf = wrapper.find('.gantt-task-clickable')
    const aggregate = wrapper.find('.gantt-task-aggregate')
    expect(leaf.exists()).toBe(true)
    expect(leaf.text()).toContain('Feuille')
    expect(aggregate.exists()).toBe(true)
    expect(aggregate.text()).toContain('Mere')
  })
})
