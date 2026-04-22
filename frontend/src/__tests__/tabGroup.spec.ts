import { mount } from '@vue/test-utils'
import { beforeEach, describe, expect, it } from 'vitest'
import TabGroup from '../shared/components/TabGroup.vue'

const ROOT_TABS = [
  { key: 'overview', label: "Vue d'ensemble" },
  {
    key: 'structure',
    label: 'Structure',
    subTabs: [
      { key: 'phases', label: 'Phases' },
      { key: 'tasks', label: 'Tâches' },
      { key: 'gantt', label: 'Gantt' },
    ],
  },
  {
    key: 'finances',
    label: 'Finances',
    subTabs: [
      { key: 'budget', label: 'Budget' },
      { key: 'invoices', label: 'Factures' },
    ],
  },
]

describe('TabGroup', () => {
  beforeEach(() => {
    sessionStorage.clear()
  })

  it('renders root tabs and emits change on click', async () => {
    const wrapper = mount(TabGroup, {
      props: { tabs: ROOT_TABS, rootTab: 'overview', subTab: null, storageKey: 't1' },
    })
    const rootBtns = wrapper.findAll('[data-tab-root]')
    expect(rootBtns).toHaveLength(3)
    await rootBtns[1]!.trigger('click')
    const events = wrapper.emitted('update')
    expect(events).toBeTruthy()
    // clicking "structure" should default to first sub-tab "phases"
    expect(events![0]).toEqual([{ rootTab: 'structure', subTab: 'phases' }])
  })

  it('renders sub-tabs only when root has children', async () => {
    const wrapper = mount(TabGroup, {
      props: { tabs: ROOT_TABS, rootTab: 'structure', subTab: 'phases', storageKey: 't2' },
    })
    const subBtns = wrapper.findAll('[data-tab-sub]')
    expect(subBtns).toHaveLength(3)
    expect(subBtns[0]!.text()).toContain('Phases')
  })

  it('hides sub-tab bar when active root has no children', () => {
    const wrapper = mount(TabGroup, {
      props: { tabs: ROOT_TABS, rootTab: 'overview', subTab: null, storageKey: 't3' },
    })
    expect(wrapper.findAll('[data-tab-sub]')).toHaveLength(0)
  })

  it('persists last sub-tab per root in sessionStorage', async () => {
    const wrapper = mount(TabGroup, {
      props: { tabs: ROOT_TABS, rootTab: 'structure', subTab: 'phases', storageKey: 'proj-42' },
    })
    const subBtns = wrapper.findAll('[data-tab-sub]')
    await subBtns[2]!.trigger('click') // gantt
    const stored = JSON.parse(sessionStorage.getItem('proj-42') || '{}')
    expect(stored.structure).toBe('gantt')
  })

  it('restores persisted sub-tab when clicking back on a root with memory', async () => {
    sessionStorage.setItem('proj-99', JSON.stringify({ finances: 'invoices' }))
    const wrapper = mount(TabGroup, {
      props: { tabs: ROOT_TABS, rootTab: 'overview', subTab: null, storageKey: 'proj-99' },
    })
    const rootBtns = wrapper.findAll('[data-tab-root]')
    await rootBtns[2]!.trigger('click') // finances
    const events = wrapper.emitted('update') as Array<[{ rootTab: string; subTab: string | null }]>
    expect(events[events.length - 1]![0]).toEqual({ rootTab: 'finances', subTab: 'invoices' })
  })
})
