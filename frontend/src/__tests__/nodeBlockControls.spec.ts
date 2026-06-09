import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

import NodeBlockControls from '../features/projects/components/NodeBlockControls.vue'

const BLOCKS = [{ id: 5, employee_name: 'Anne Monty' }]
const CANDIDATES = [
  { id: 1, name: 'Jean Bélanger' },
  { id: 2, name: 'Claire Zoé' },
]

function mountControls() {
  return mount(NodeBlockControls, { props: { blocks: BLOCKS, candidates: CANDIDATES } })
}

describe('NodeBlockControls', () => {
  it('affiche les personnes bloquées et émet unblock', async () => {
    const wrapper = mountControls()
    const chips = wrapper.findAll('[data-block-chip]')
    expect(chips).toHaveLength(1)
    expect(chips[0]!.text()).toContain('Anne Monty')
    await wrapper.find('[data-unblock]').trigger('click')
    expect(wrapper.emitted('unblock')![0]).toEqual([5])
  })

  it('ouvre le sélecteur et émet block au clic sur un membre', async () => {
    const wrapper = mountControls()
    expect(wrapper.find('[data-block-search]').exists()).toBe(false)
    await wrapper.find('[data-block-toggle]').trigger('click')
    expect(wrapper.find('[data-block-search]').exists()).toBe(true)
    const candidates = wrapper.findAll('[data-block-candidate]')
    expect(candidates).toHaveLength(2)
    await candidates[0]!.trigger('click')
    expect(wrapper.emitted('block')![0]).toEqual([1])
    // Le sélecteur se referme après sélection.
    expect(wrapper.find('[data-block-search]').exists()).toBe(false)
  })

  it('filtre les candidats par recherche', async () => {
    const wrapper = mountControls()
    await wrapper.find('[data-block-toggle]').trigger('click')
    await wrapper.find('[data-block-search]').setValue('claire')
    const candidates = wrapper.findAll('[data-block-candidate]')
    expect(candidates).toHaveLength(1)
    expect(candidates[0]!.text()).toContain('Claire Zoé')
  })
})
