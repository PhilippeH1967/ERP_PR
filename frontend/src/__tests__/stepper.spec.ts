import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import Stepper from '../shared/components/Stepper.vue'

const STEPS = [
  { key: 'DRAFT', label: 'Brouillon' },
  { key: 'SUBMITTED', label: 'Soumis' },
  { key: 'APPROVED', label: 'Approuvé' },
]

describe('Stepper', () => {
  it('renders the right number of nodes and bars', () => {
    const wrapper = mount(Stepper, { props: { steps: STEPS, currentKey: 'DRAFT' } })
    expect(wrapper.findAll('.stepper-node')).toHaveLength(3)
    expect(wrapper.findAll('.stepper-bar')).toHaveLength(2)
  })

  it('marks past steps done, current active, future todo', () => {
    const wrapper = mount(Stepper, { props: { steps: STEPS, currentKey: 'SUBMITTED' } })
    const nodes = wrapper.findAll('.stepper-node')
    expect(nodes[0]!.classes()).toContain('stepper-done')
    expect(nodes[1]!.classes()).toContain('stepper-active')
    expect(nodes[2]!.classes()).toContain('stepper-todo')
  })

  it('marks rejectedKey as rejected and exposes tooltip', () => {
    const wrapper = mount(Stepper, {
      props: { steps: STEPS, currentKey: 'SUBMITTED', rejectedKey: 'APPROVED', rejectedTooltip: 'Motif' },
    })
    const nodes = wrapper.findAll('.stepper-node')
    expect(nodes[2]!.classes()).toContain('stepper-rejected')
    expect(nodes[2]!.attributes('title')).toBe('Motif')
  })

  it('falls back to first step if currentKey is unknown', () => {
    const wrapper = mount(Stepper, { props: { steps: STEPS, currentKey: 'FOO' } })
    expect(wrapper.attributes('aria-valuenow')).toBe('1')
  })
})
