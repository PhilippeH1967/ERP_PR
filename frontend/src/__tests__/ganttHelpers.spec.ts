import { describe, expect, it } from 'vitest'
import {
  isAggregateTask,
  phasesWithTasks,
  totalPlannedHours,
  isOverBudget,
} from '../features/planning/utils/ganttHelpers'

describe('isAggregateTask', () => {
  it('tâche-mère (is_chargeable=false) → agrégat', () => {
    expect(isAggregateTask({ is_chargeable: false })).toBe(true)
  })
  it('feuille (is_chargeable=true) → non agrégat', () => {
    expect(isAggregateTask({ is_chargeable: true })).toBe(false)
  })
  it('champ absent → feuille par défaut', () => {
    expect(isAggregateTask({})).toBe(false)
  })
})

describe('phasesWithTasks', () => {
  it('ne garde que les phases ayant au moins une tâche', () => {
    const phases = [{ id: 1 }, { id: 2 }, { id: 3 }]
    const tasks = [{ phase: 1 }, { phase: 1 }, { phase: 3 }]
    expect(phasesWithTasks(phases, tasks).map((p) => p.id)).toEqual([1, 3])
  })
  it('retourne vide si aucune tâche', () => {
    expect(phasesWithTasks([{ id: 1 }], [])).toEqual([])
  })
})

describe('totalPlannedHours', () => {
  it('Σ (h/sem × semaines)', () => {
    const allocs = [
      { hours_per_week: 10, start_date: 'a', end_date: 'b' },
      { hours_per_week: 5, start_date: 'c', end_date: 'd' },
    ]
    // weeksOf renvoie 2 pour le 1er, 3 pour le 2e
    const weeksOf = (s: string) => (s === 'a' ? 2 : 3)
    expect(totalPlannedHours(allocs, weeksOf)).toBe(10 * 2 + 5 * 3) // 35
  })
  it('au moins 1 semaine si weeksOf renvoie 0', () => {
    expect(totalPlannedHours([{ hours_per_week: 8, start_date: 'x', end_date: 'y' }], () => 0)).toBe(8)
  })
})

describe('isOverBudget', () => {
  it('planifié > budget → vrai', () => {
    expect(isOverBudget(90, 80)).toBe(true)
  })
  it('planifié <= budget → faux', () => {
    expect(isOverBudget(80, 80)).toBe(false)
  })
  it('budget 0 → jamais en dépassement', () => {
    expect(isOverBudget(10, 0)).toBe(false)
  })
})
