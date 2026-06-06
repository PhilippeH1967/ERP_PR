import { mount, flushPromises } from '@vue/test-utils'
import { describe, it, expect, vi, beforeEach } from 'vitest'

vi.mock('@/features/planning/api/planningApi', () => ({
  planningApi: {
    getMilestone: vi.fn(),
    updateMilestone: vi.fn(),
    deleteMilestone: vi.fn(),
  },
}))

import { planningApi } from '@/features/planning/api/planningApi'
import MilestoneSlideOver from '@/features/planning/components/MilestoneSlideOver.vue'

const MS = {
  id: 5, title: 'Permis', date: '2026-03-15',
  status: 'UPCOMING', color: '#3B82F6', description: 'Dépôt permis',
}

function mountPanel() {
  return mount(MilestoneSlideOver, {
    props: { open: true, milestoneId: 5 },
    global: { stubs: { teleport: true } },
  })
}

describe('MilestoneSlideOver', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    vi.mocked(planningApi.getMilestone).mockResolvedValue({ data: MS } as never)
    vi.mocked(planningApi.updateMilestone).mockResolvedValue({ data: MS } as never)
    vi.mocked(planningApi.deleteMilestone).mockResolvedValue({ data: {} } as never)
  })

  it('affiche le jalon en lecture (titre, date FR, statut)', async () => {
    const w = mountPanel()
    await flushPromises()
    expect(w.text()).toContain('Permis')
    expect(w.text()).toContain('15/03/2026')
    expect(w.text()).toContain('À venir')
  })

  it('édite puis enregistre → PATCH + événement updated', async () => {
    const w = mountPanel()
    await flushPromises()
    await w.find('[data-edit]').trigger('click')
    await w.find('[data-input-title]').setValue('Permis révisé')
    await w.find('[data-save]').trigger('click')
    await flushPromises()
    expect(planningApi.updateMilestone).toHaveBeenCalledWith(
      5, expect.objectContaining({ title: 'Permis révisé', date: '2026-03-15' }),
    )
    expect(w.emitted('updated')).toBeTruthy()
  })

  it('refuse d’enregistrer sans titre (validation, pas d’appel API)', async () => {
    const w = mountPanel()
    await flushPromises()
    await w.find('[data-edit]').trigger('click')
    await w.find('[data-input-title]').setValue('   ')
    await w.find('[data-save]').trigger('click')
    await flushPromises()
    expect(planningApi.updateMilestone).not.toHaveBeenCalled()
    expect(w.find('[data-error]').exists()).toBe(true)
  })

  it('supprime avec confirmation inline → DELETE + updated + close', async () => {
    const w = mountPanel()
    await flushPromises()
    // Pas de bouton rouge direct : on déclenche d’abord la confirmation.
    await w.find('[data-delete]').trigger('click')
    await w.find('[data-delete-confirm]').trigger('click')
    await flushPromises()
    expect(planningApi.deleteMilestone).toHaveBeenCalledWith(5)
    expect(w.emitted('updated')).toBeTruthy()
    expect(w.emitted('close')).toBeTruthy()
  })
})
