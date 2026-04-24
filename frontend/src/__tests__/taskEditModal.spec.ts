import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import TaskEditModal from '../features/projects/components/TaskEditModal.vue'

const TASK = {
  id: 42,
  name: 'Étude de site',
  wbs_code: '3.1',
  client_facing_label: '',
  budgeted_hours: '80',
  budgeted_cost: '6400',
  billing_mode: 'FORFAIT',
  is_billable: true,
}

describe('TaskEditModal', () => {
  it('pré-remplit les champs depuis la tâche', () => {
    const wrapper = mount(TaskEditModal, {
      props: { open: true, task: TASK, canSeeCosts: true },
    })
    expect((wrapper.find('[data-tem-name]').element as HTMLInputElement).value).toBe('Étude de site')
    expect((wrapper.find('[data-tem-wbs]').element as HTMLInputElement).value).toBe('3.1')
    expect((wrapper.find('[data-tem-hours]').element as HTMLInputElement).value).toBe('80')
    expect((wrapper.find('[data-tem-cost]').element as HTMLInputElement).value).toBe('6400')
  })

  it('émet save avec le payload modifié', async () => {
    const wrapper = mount(TaskEditModal, {
      props: { open: true, task: TASK, canSeeCosts: true },
    })
    await wrapper.find('[data-tem-name]').setValue('Étude de site v2')
    await wrapper.find('[data-tem-wbs]').setValue('3.1.1')
    await wrapper.find('[data-tem-client-label]').setValue('Phase 1 — Étude')
    await wrapper.find('[data-tem-hours]').setValue('100')
    await wrapper.find('[data-tem-cost]').setValue('8000')
    await wrapper.find('[data-tem-save]').trigger('click')
    const events = wrapper.emitted('save')
    expect(events).toBeTruthy()
    const payload = events![0]![0] as Record<string, unknown>
    expect(payload.name).toBe('Étude de site v2')
    expect(payload.wbs_code).toBe('3.1.1')
    expect(payload.client_facing_label).toBe('Phase 1 — Étude')
    expect(payload.budgeted_hours).toBe('100')
    expect(payload.budgeted_cost).toBe('8000')
  })

  it('masque le champ coût quand canSeeCosts est false', () => {
    const wrapper = mount(TaskEditModal, {
      props: { open: true, task: TASK, canSeeCosts: false },
    })
    expect(wrapper.find('[data-tem-cost]').exists()).toBe(false)
  })

  it('bloque save si le nom est vide', async () => {
    const wrapper = mount(TaskEditModal, {
      props: { open: true, task: TASK, canSeeCosts: true },
    })
    await wrapper.find('[data-tem-name]').setValue('')
    await wrapper.find('[data-tem-save]').trigger('click')
    expect(wrapper.emitted('save')).toBeFalsy()
    expect(wrapper.find('[data-tem-error]').text()).toContain('obligatoire')
  })

  it('émet close au clic sur Annuler', async () => {
    const wrapper = mount(TaskEditModal, {
      props: { open: true, task: TASK, canSeeCosts: true },
    })
    await wrapper.find('[data-tem-cancel]').trigger('click')
    expect(wrapper.emitted('close')).toBeTruthy()
  })
})
