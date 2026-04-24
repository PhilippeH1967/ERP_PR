import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import ProjectCloseModal from '../features/projects/components/ProjectCloseModal.vue'

const CHECK_PASSING = { code: 'TIME_ENTRIES', label: 'Heures validées', passed: true, detail: 'OK' }
const CHECK_BLOCKING = { code: 'INVOICES', label: 'Factures', passed: false, detail: '2 brouillons' }
const CHECK_WARNING = {
  code: 'VIRTUAL_RESOURCES', label: 'Profils virtuels', passed: false,
  detail: '1 actif', severity: 'warning',
}

describe('ProjectCloseModal', () => {
  it('renders one line per check with icon + label + detail', () => {
    const wrapper = mount(ProjectCloseModal, {
      props: {
        open: true,
        canClose: true,
        checks: [CHECK_PASSING, CHECK_BLOCKING, CHECK_WARNING],
      },
    })
    const rows = wrapper.findAll('[data-check-row]')
    expect(rows).toHaveLength(3)
    expect(rows[0]!.text()).toContain('Heures validées')
    expect(rows[0]!.text()).toContain('OK')
    expect(rows[1]!.text()).toContain('2 brouillons')
    expect(rows[2]!.text()).toContain('1 actif')
  })

  it('disables the close button when canClose is false', () => {
    const wrapper = mount(ProjectCloseModal, {
      props: {
        open: true,
        canClose: false,
        checks: [CHECK_BLOCKING],
      },
    })
    const btn = wrapper.find('[data-close-confirm]')
    expect((btn.element as HTMLButtonElement).disabled).toBe(true)
  })

  it('enables the close button when canClose is true', () => {
    const wrapper = mount(ProjectCloseModal, {
      props: {
        open: true,
        canClose: true,
        checks: [CHECK_PASSING, CHECK_WARNING],
      },
    })
    const btn = wrapper.find('[data-close-confirm]')
    expect((btn.element as HTMLButtonElement).disabled).toBe(false)
  })

  it('emits confirm when the close button is clicked', async () => {
    const wrapper = mount(ProjectCloseModal, {
      props: {
        open: true,
        canClose: true,
        checks: [CHECK_PASSING],
      },
    })
    await wrapper.find('[data-close-confirm]').trigger('click')
    expect(wrapper.emitted('confirm')).toBeTruthy()
  })

  it('emits close when cancel is clicked', async () => {
    const wrapper = mount(ProjectCloseModal, {
      props: { open: true, canClose: true, checks: [CHECK_PASSING] },
    })
    await wrapper.find('[data-close-cancel]').trigger('click')
    expect(wrapper.emitted('close')).toBeTruthy()
  })

  it('marks a passed check with ✓ and a failing blocker with ✗', () => {
    const wrapper = mount(ProjectCloseModal, {
      props: {
        open: true,
        canClose: false,
        checks: [CHECK_PASSING, CHECK_BLOCKING],
      },
    })
    const rows = wrapper.findAll('[data-check-row]')
    expect(rows[0]!.attributes('data-passed')).toBe('true')
    expect(rows[1]!.attributes('data-passed')).toBe('false')
    expect(rows[1]!.attributes('data-severity')).not.toBe('warning')
  })

  it('marks a warning with severity="warning" even when passed=false', () => {
    const wrapper = mount(ProjectCloseModal, {
      props: { open: true, canClose: true, checks: [CHECK_WARNING] },
    })
    const row = wrapper.find('[data-check-row]')
    expect(row.attributes('data-severity')).toBe('warning')
    expect(row.attributes('data-passed')).toBe('false')
  })
})
