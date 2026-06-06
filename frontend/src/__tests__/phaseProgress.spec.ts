import { describe, it, expect } from 'vitest'
import {
  pct,
  progressHoursPct,
  progressCostPct,
  progressFeesPct,
} from '@/features/projects/utils/phaseProgress'

describe('phaseProgress', () => {
  it('pct : consommé / budget, arrondi à 1 décimale', () => {
    expect(pct(50, 100)).toBe(50)
    expect(pct(1, 3)).toBe(33.3)
  })

  it('pct : 0 quand le budget est nul, négatif ou absent (jamais de division par 0)', () => {
    expect(pct(50, 0)).toBe(0)
    expect(pct(50, undefined)).toBe(0)
    expect(pct(50, null)).toBe(0)
  })

  it('avancement heures = heures réelles / heures budgétées', () => {
    expect(progressHoursPct({ actual_hours: 30, tasks_budgeted_hours: 40 })).toBe(75)
  })

  it('avancement coût = coût réel / coût budgété', () => {
    expect(progressCostPct({ actual_cost: 500, tasks_budgeted_cost: 1000 })).toBe(50)
  })

  it('avancement honoraires = facturé / honoraires contractés', () => {
    expect(progressFeesPct({ invoiced_amount: 300, fees_contract_amount: 1200 })).toBe(25)
  })

  it('gère les valeurs en string renvoyées par DRF', () => {
    expect(progressHoursPct({ actual_hours: '20', tasks_budgeted_hours: '80' })).toBe(25)
    expect(progressFeesPct({ invoiced_amount: '0', fees_contract_amount: '1000' })).toBe(0)
  })
})
