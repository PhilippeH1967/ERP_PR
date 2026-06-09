import { describe, expect, it } from 'vitest'
import { isTaskReadOnly, taskClosureIds, visibleTaskGroups } from '../features/projects/utils/taskStructure'

describe('visibleTaskGroups', () => {
  it('masque les phases sans tâche', () => {
    const groups = [
      { phase_name: 'Concept', phase_id: 1, tasks: [{ id: 1 }] },
      { phase_name: 'Appel offres', phase_id: 2, tasks: [] },
      { phase_name: 'Préliminaires', phase_id: 3, tasks: [{ id: 2 }, { id: 3 }] },
    ]
    const visible = visibleTaskGroups(groups)
    expect(visible.map((g) => g.phase_name)).toEqual(['Concept', 'Préliminaires'])
  })

  it('retourne une liste vide si aucune phase n’a de tâche', () => {
    const groups = [{ phase_name: 'A', phase_id: 1, tasks: [] }]
    expect(visibleTaskGroups(groups)).toEqual([])
  })
})

describe('isTaskReadOnly', () => {
  it('tâche-mère (is_chargeable=false) → lecture seule', () => {
    expect(isTaskReadOnly({ id: 1, is_chargeable: false })).toBe(true)
  })

  it('tâche saisissable (is_chargeable=true) → éditable', () => {
    expect(isTaskReadOnly({ id: 1, is_chargeable: true })).toBe(false)
  })

  it('champ absent → éditable par défaut (héritage)', () => {
    expect(isTaskReadOnly({ id: 1 })).toBe(false)
  })
})

describe('taskClosureIds', () => {
  const all = [
    { id: 1, parent: null },
    { id: 2, parent: 1 },
    { id: 3, parent: 1 },
    { id: 4, parent: null },
  ]

  it('feuille → uniquement elle-même', () => {
    expect(taskClosureIds({ id: 4, parent: null }, all)).toEqual([4])
  })

  it('tâche-mère → elle-même + ses sous-tâches directes', () => {
    expect(taskClosureIds({ id: 1, parent: null }, all)).toEqual([1, 2, 3])
  })
})
