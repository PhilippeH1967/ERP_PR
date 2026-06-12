import { mount, flushPromises } from '@vue/test-utils'
import { describe, expect, it, vi } from 'vitest'

const mockRoute = { path: '/projects/15', query: { tab: 'structure/tasks' } }
vi.mock('vue-router', () => ({ useRoute: () => mockRoute }))

import HelpPanel from '../features/help/components/HelpPanel.vue'

function mountPanel() {
  return mount(HelpPanel, {
    props: { open: true },
    global: { stubs: { teleport: true, RouterLink: { template: '<a data-help-guide-link><slot /></a>' } } },
  })
}

describe('HelpPanel — panneau d’aide contextuelle', () => {
  it('affiche le contexte de l’écran courant (Échéancier › Tâches)', async () => {
    const wrapper = mountPanel()
    await flushPromises()
    expect(wrapper.find('[data-help-title]').text().toLowerCase()).toContain('tâches')
    expect(wrapper.findAll('[data-help-item]').length).toBeGreaterThan(2)
    expect(wrapper.text()).toContain('Fiche tâche')
  })

  it('pointe vers le guide complet et émet close au clic', async () => {
    const wrapper = mountPanel()
    await flushPromises()
    expect(wrapper.find('[data-help-guide-link]').exists()).toBe(true)
    await wrapper.find('.hp-x').trigger('click')
    expect(wrapper.emitted('close')).toBeTruthy()
  })
})
