import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import HourDistribution from '../shared/components/HourDistribution.vue'

const MEMBERS = [
  { id: 10, name: 'Alice Martin' },
  { id: 11, name: 'Bob Tremblay' },
]
const VIRTUALS = [
  { id: 100, name: 'Architecte senior', default_hourly_rate: '95.00' },
  { id: 101, name: 'Dessinateur junior', default_hourly_rate: '55.00' },
]

describe('HourDistribution', () => {
  it('renders one row per allocation', () => {
    const wrapper = mount(HourDistribution, {
      props: {
        members: MEMBERS,
        virtuals: VIRTUALS,
        modelValue: [
          { kind: 'employee', id: 10, hours: 40 },
          { kind: 'virtual', id: 100, hours: 80 },
        ],
        budgetedHours: 120,
      },
    })
    expect(wrapper.findAll('[data-alloc-row]')).toHaveLength(2)
  })

  it('emits update when adding a row', async () => {
    const wrapper = mount(HourDistribution, {
      props: { members: MEMBERS, virtuals: VIRTUALS, modelValue: [], budgetedHours: 100 },
    })
    await wrapper.find('[data-alloc-add]').trigger('click')
    const events = wrapper.emitted('update:modelValue')
    expect(events).toBeTruthy()
    const payload = events![0]![0] as Array<{ kind: string; id: number; hours: number }>
    expect(payload).toHaveLength(1)
    expect(payload[0]!.hours).toBe(0)
  })

  it('emits update with edited hours', async () => {
    const wrapper = mount(HourDistribution, {
      props: {
        members: MEMBERS,
        virtuals: VIRTUALS,
        modelValue: [{ kind: 'employee', id: 10, hours: 40 }],
        budgetedHours: 100,
      },
    })
    const input = wrapper.find('[data-alloc-hours]')
    await input.setValue('60')
    const events = wrapper.emitted('update:modelValue')
    expect(events).toBeTruthy()
    const payload = events![0]![0] as Array<{ hours: number }>
    expect(payload[0]!.hours).toBe(60)
  })

  it('emits update when removing a row', async () => {
    const wrapper = mount(HourDistribution, {
      props: {
        members: MEMBERS,
        virtuals: VIRTUALS,
        modelValue: [
          { kind: 'employee', id: 10, hours: 40 },
          { kind: 'virtual', id: 100, hours: 80 },
        ],
        budgetedHours: 120,
      },
    })
    await wrapper.findAll('[data-alloc-remove]')[0]!.trigger('click')
    const events = wrapper.emitted('update:modelValue')
    expect(events).toBeTruthy()
    const payload = events![0]![0] as Array<{ id: number }>
    expect(payload).toHaveLength(1)
    expect(payload[0]!.id).toBe(100)
  })

  it('emits create-virtual with name and rate when creating a new virtual profile', async () => {
    const wrapper = mount(HourDistribution, {
      props: { members: MEMBERS, virtuals: VIRTUALS, modelValue: [], budgetedHours: 100 },
    })
    await wrapper.find('[data-alloc-show-vr-form]').trigger('click')
    await wrapper.find('[data-vr-name]').setValue('Chef de projet')
    await wrapper.find('[data-vr-rate]').setValue('120')
    await wrapper.find('[data-vr-submit]').trigger('click')
    const events = wrapper.emitted('create-virtual')
    expect(events).toBeTruthy()
    expect(events![0]![0]).toEqual({ name: 'Chef de projet', rate: '120' })
  })

  it('shows overrun warning when sum exceeds budgetedHours', () => {
    const wrapper = mount(HourDistribution, {
      props: {
        members: MEMBERS,
        virtuals: VIRTUALS,
        modelValue: [
          { kind: 'employee', id: 10, hours: 60 },
          { kind: 'virtual', id: 100, hours: 80 },
        ],
        budgetedHours: 100,
      },
    })
    expect(wrapper.find('[data-alloc-warning]').exists()).toBe(true)
    expect(wrapper.find('[data-alloc-warning]').text()).toContain('140')
  })

  it('does not show warning when sum matches budgetedHours', () => {
    const wrapper = mount(HourDistribution, {
      props: {
        members: MEMBERS,
        virtuals: VIRTUALS,
        modelValue: [{ kind: 'employee', id: 10, hours: 100 }],
        budgetedHours: 100,
      },
    })
    expect(wrapper.find('[data-alloc-warning]').exists()).toBe(false)
  })
})
