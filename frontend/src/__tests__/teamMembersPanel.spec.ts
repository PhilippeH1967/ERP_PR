import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import TeamMembersPanel from '../features/projects/components/TeamMembersPanel.vue'

const MEMBERS = [
  { id: 1, name: 'Alice Martin' },
  { id: 2, name: 'Bob Tremblay' },
]
const ADDABLE = [
  { id: 3, username: 'cdupont' },
  { id: 4, username: 'elavoie' },
]

describe('TeamMembersPanel', () => {
  it('renders one row per member with the name', () => {
    const wrapper = mount(TeamMembersPanel, {
      props: { members: MEMBERS, addableUsers: ADDABLE, canManage: true },
    })
    const rows = wrapper.findAll('[data-member-row]')
    expect(rows).toHaveLength(2)
    expect(rows[0]!.text()).toContain('Alice Martin')
    expect(rows[1]!.text()).toContain('Bob Tremblay')
  })

  it('shows the empty state when there are no members', () => {
    const wrapper = mount(TeamMembersPanel, {
      props: { members: [], addableUsers: ADDABLE, canManage: true },
    })
    expect(wrapper.find('[data-members-empty]').exists()).toBe(true)
  })

  it('hides management controls when canManage is false', () => {
    const wrapper = mount(TeamMembersPanel, {
      props: { members: MEMBERS, addableUsers: ADDABLE, canManage: false },
    })
    expect(wrapper.find('[data-member-add-search]').exists()).toBe(false)
    expect(wrapper.find('[data-member-remove-start]').exists()).toBe(false)
  })

  it('recherche par nom puis émet add avec l’utilisateur choisi', async () => {
    const wrapper = mount(TeamMembersPanel, {
      props: { members: MEMBERS, addableUsers: ADDABLE, canManage: true },
    })
    const input = wrapper.find('[data-member-add-search]')
    await input.setValue('cdupont') // filtre la liste par nom
    const items = wrapper.findAll('[data-member-search-list] button')
    expect(items).toHaveLength(1) // seul cdupont correspond
    await items[0]!.trigger('mousedown')
    await wrapper.find('[data-member-add-confirm]').trigger('click')
    expect(wrapper.emitted('add')).toBeTruthy()
    expect(wrapper.emitted('add')![0]).toEqual([3])
  })

  it('filtre la liste à mesure de la frappe (recherche par nom)', async () => {
    const wrapper = mount(TeamMembersPanel, {
      props: { members: MEMBERS, addableUsers: ADDABLE, canManage: true },
    })
    const input = wrapper.find('[data-member-add-search]')
    await input.trigger('focus')
    expect(wrapper.findAll('[data-member-search-list] button')).toHaveLength(2) // tous
    await input.setValue('ela')
    expect(wrapper.findAll('[data-member-search-list] button')).toHaveLength(1) // elavoie
    expect(wrapper.find('[data-member-search-list]').text()).toContain('elavoie')
  })

  it('disables the add button when no user is selected', () => {
    const wrapper = mount(TeamMembersPanel, {
      props: { members: MEMBERS, addableUsers: ADDABLE, canManage: true },
    })
    const btn = wrapper.find('[data-member-add-confirm]')
    expect((btn.element as HTMLButtonElement).disabled).toBe(true)
  })

  it('asks for confirmation before removing, then emits remove', async () => {
    const wrapper = mount(TeamMembersPanel, {
      props: { members: MEMBERS, addableUsers: ADDABLE, canManage: true },
    })
    await wrapper.find('[data-member-remove-start]').trigger('click')
    await wrapper.find('[data-member-remove-confirm]').trigger('click')
    expect(wrapper.emitted('remove')).toBeTruthy()
    expect(wrapper.emitted('remove')![0]).toEqual([1])
  })

  it('displays a backend error message when provided', () => {
    const wrapper = mount(TeamMembersPanel, {
      props: {
        members: MEMBERS, addableUsers: ADDABLE, canManage: true,
        error: 'Utilisateur introuvable.',
      },
    })
    expect(wrapper.find('[data-member-error]').text()).toContain('Utilisateur introuvable.')
  })
})
