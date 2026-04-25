import { mount, flushPromises } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'

vi.mock('@/plugins/axios', () => ({
  default: { get: vi.fn(), post: vi.fn(), delete: vi.fn() },
}))
vi.mock('@/shared/composables/useAuth', () => ({
  useAuth: () => ({
    currentUser: { value: { roles: ['ADMIN'] } },
  }),
}))

import apiClient from '@/plugins/axios'
const mockGet = apiClient.get as unknown as ReturnType<typeof vi.fn>
const mockPost = apiClient.post as unknown as ReturnType<typeof vi.fn>
const mockDelete = apiClient.delete as unknown as ReturnType<typeof vi.fn>

import PeriodLocks from '../features/timesheet/views/PeriodLocks.vue'

function defaultMocks() {
  mockGet.mockImplementation((url: string) => {
    if (url.includes('period_summary')) return Promise.resolve({ data: { weeks: [
      { week_start: '2026-04-13', week_end: '2026-04-19', entry_count: 5, total_hours: 40, employee_count: 1, statuses: ['LOCKED'], status: 'locked' },
    ] } })
    if (url.includes('period_unlocks')) return Promise.resolve({ data: [
      { id: 99, period_start: '2026-03-01', period_end: '2026-03-07', reason: 'CORRECTION', justification: 'Erreur de saisie', unlocked_by: 1, unlocked_at: '2026-04-01T10:00:00Z' },
    ] })
    if (url.includes('timesheet_locks')) return Promise.resolve({ data: [
      { id: 7, project: 1, project_name: 'Projet A', project_code: 'P-A', phase: 2, phase_name: 'Concept', lock_type: 'PHASE', locked_by: 1, locked_by_name: 'Admin', locked_at: '2026-04-01T10:00:00Z' },
    ] })
    if (url.includes('projects')) return Promise.resolve({ data: [] })
    return Promise.resolve({ data: [] })
  })
  mockPost.mockResolvedValue({ data: { locked_count: 0 } })
  mockDelete.mockResolvedValue({ data: {} })
}

describe('PeriodLocks — confirmation inline (F4.7)', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    mockGet.mockReset()
    mockPost.mockReset()
    mockDelete.mockReset()
    defaultMocks()
  })

  it('demande confirmation avant de supprimer un déverrouillage', async () => {
    const wrapper = mount(PeriodLocks)
    await flushPromises()
    const btn = wrapper.find('[data-revoke-unlock]')
    expect(btn.exists()).toBe(true)
    expect(btn.text()).toMatch(/Révoquer|Revoquer/)
    await btn.trigger('click')
    // Premier clic : ne supprime pas, affiche Confirmer/Annuler
    expect(mockDelete).not.toHaveBeenCalled()
    const confirm = wrapper.find('[data-revoke-unlock-confirm]')
    expect(confirm.exists()).toBe(true)
    await confirm.trigger('click')
    await flushPromises()
    expect(mockDelete).toHaveBeenCalledWith(expect.stringContaining('period_unlocks/99'))
  })

  it('demande confirmation avant de supprimer un verrouillage par tâche', async () => {
    const wrapper = mount(PeriodLocks)
    await flushPromises()
    const btn = wrapper.find('[data-delete-task-lock]')
    expect(btn.exists()).toBe(true)
    await btn.trigger('click')
    expect(mockDelete).not.toHaveBeenCalled()
    const confirm = wrapper.find('[data-delete-task-lock-confirm]')
    expect(confirm.exists()).toBe(true)
    await confirm.trigger('click')
    await flushPromises()
    expect(mockDelete).toHaveBeenCalledWith(expect.stringContaining('timesheet_locks/7'))
  })

  it('annule la confirmation au clic sur Annuler', async () => {
    const wrapper = mount(PeriodLocks)
    await flushPromises()
    await wrapper.find('[data-delete-task-lock]').trigger('click')
    expect(wrapper.find('[data-delete-task-lock-confirm]').exists()).toBe(true)
    await wrapper.find('[data-delete-task-lock-cancel]').trigger('click')
    expect(wrapper.find('[data-delete-task-lock-confirm]').exists()).toBe(false)
    expect(mockDelete).not.toHaveBeenCalled()
  })
})
