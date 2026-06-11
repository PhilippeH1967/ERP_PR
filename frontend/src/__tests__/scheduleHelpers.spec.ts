import { describe, expect, it } from 'vitest'
import { derivedDates, shiftIsoDate } from '../features/projects/utils/scheduleHelpers'

describe('shiftIsoDate', () => {
  it('décale en avant', () => {
    expect(shiftIsoDate('2026-03-02', 10)).toBe('2026-03-12')
  })
  it('décale en arrière et traverse les mois', () => {
    expect(shiftIsoDate('2026-03-02', -5)).toBe('2026-02-25')
  })
  it('traverse les années', () => {
    expect(shiftIsoDate('2026-12-28', 7)).toBe('2027-01-04')
  })
  it('null / vide / invalide → null', () => {
    expect(shiftIsoDate(null, 10)).toBeNull()
    expect(shiftIsoDate('', 10)).toBeNull()
    expect(shiftIsoDate('pas-une-date', 10)).toBeNull()
  })
})

describe('derivedDates', () => {
  const all = [
    { id: 1, parent: null },
    { id: 2, parent: 1, start_date: '2026-03-10', end_date: '2026-04-01' },
    { id: 3, parent: 1, start_date: '2026-03-02', end_date: '2026-05-15' },
    { id: 4, parent: null, start_date: '2026-06-01', end_date: '2026-06-30' },
  ]
  it('min des débuts / max des fins des sous-tâches', () => {
    expect(derivedDates(all[0]!, all)).toEqual({ start: '2026-03-02', end: '2026-05-15' })
  })
  it('aucune sous-tâche datée → null/null', () => {
    expect(derivedDates(all[3]!, all)).toEqual({ start: null, end: null })
  })
})
