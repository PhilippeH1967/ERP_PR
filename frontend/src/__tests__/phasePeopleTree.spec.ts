import { describe, expect, it } from 'vitest'
import {
  buildPhasePeopleTree,
  filterTreeByPerson,
  visiblePhaseNodes,
  type AllocInput,
  type PhaseGroupInput,
} from '../features/projects/utils/phasePeopleTree'

const GROUPS: PhaseGroupInput[] = [
  {
    phase_id: 1,
    phase_name: 'Conception',
    tasks: [
      { id: 10, parent: null, name: 'Plans', wbs_code: '1.1', is_active: true },
      { id: 11, parent: 10, name: 'Esquisse', wbs_code: '1.1.1', is_active: true },
      { id: 12, parent: null, name: 'Relevés', wbs_code: '1.2', is_active: true },
    ],
  },
  { phase_id: 2, phase_name: 'Exécution', tasks: [] },
]

const ALLOCS: AllocInput[] = [
  // Anne sur la sous-tâche 11
  { id: 1, employee: 100, employee_name: 'Anne Monty', phase: null, task: 11, hours_per_week: 10 },
  // Jean sur la tâche 10
  { id: 2, employee: 101, employee_name: 'Jean Bélanger', phase: null, task: 10, hours_per_week: 5 },
  // Profil virtuel sur la phase 1 directement
  { id: 3, virtual_resource: 7, virtual_resource_name: 'Architecte senior', phase: 1, task: null, hours_per_week: 8 },
]

describe('buildPhasePeopleTree', () => {
  it('place chaque personne au bon niveau (phase / tâche / sous-tâche)', () => {
    const tree = buildPhasePeopleTree(GROUPS, ALLOCS)
    const concept = tree[0]!
    // Personne allouée à la phase directement (le profil virtuel).
    expect(concept.people.map((p) => p.name)).toEqual(['Architecte senior'])
    expect(concept.people[0]!.kind).toBe('virtual')

    const plans = concept.tasks.find((t) => t.id === 10)!
    expect(plans.people.map((p) => p.name)).toEqual(['Jean Bélanger'])
    // La sous-tâche imbriquée porte Anne.
    const esquisse = plans.subtasks.find((t) => t.id === 11)!
    expect(esquisse.people.map((p) => p.name)).toEqual(['Anne Monty'])
  })

  it('imbrique les sous-tâches sous leur tâche-mère', () => {
    const tree = buildPhasePeopleTree(GROUPS, ALLOCS)
    const concept = tree[0]!
    expect(concept.tasks.map((t) => t.id)).toEqual([10, 12]) // racines uniquement
    expect(concept.tasks.find((t) => t.id === 10)!.subtasks.map((t) => t.id)).toEqual([11])
  })
})

describe('visiblePhaseNodes', () => {
  it('masque les phases sans tâche ni personne', () => {
    const tree = buildPhasePeopleTree(GROUPS, ALLOCS)
    const visible = visiblePhaseNodes(tree)
    expect(visible.map((p) => p.phase_name)).toEqual(['Conception']) // « Exécution » vide masquée
  })
})

describe('filterTreeByPerson', () => {
  it('ne garde que les nœuds où la personne recherchée est affectée', () => {
    const tree = buildPhasePeopleTree(GROUPS, ALLOCS)
    const filtered = filterTreeByPerson(tree, 'anne')
    expect(filtered).toHaveLength(1)
    const concept = filtered[0]!
    // Seule la branche menant à Anne (tâche 10 → sous-tâche 11) est conservée.
    expect(concept.tasks.map((t) => t.id)).toEqual([10])
    expect(concept.tasks[0]!.subtasks.map((t) => t.id)).toEqual([11])
  })

  it('trouve une personne allouée au niveau phase', () => {
    const tree = buildPhasePeopleTree(GROUPS, ALLOCS)
    const filtered = filterTreeByPerson(tree, 'architecte')
    expect(filtered).toHaveLength(1)
    expect(filtered[0]!.people[0]!.name).toBe('Architecte senior')
  })

  it('requête vide → arbre inchangé', () => {
    const tree = buildPhasePeopleTree(GROUPS, ALLOCS)
    expect(filterTreeByPerson(tree, '  ')).toBe(tree)
  })
})
