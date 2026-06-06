/**
 * Calculs d'avancement par phase (overview projet).
 *
 * Logique pure, isolée du composant pour être testable unitairement. Toutes les
 * valeurs peuvent arriver en string (DRF sérialise certains décimaux en string).
 *
 * - Avancement HEURES   = heures réelles / heures budgétées (tâches)
 * - Avancement COÛT     = coût réel (heures × taux tâche) / coût budgété
 * - Avancement HONORAIRES = facturé / honoraires contractés
 */

export interface PhaseFinancials {
  tasks_budgeted_hours?: number | string | null
  tasks_budgeted_cost?: number | string | null
  actual_hours?: number | string | null
  actual_cost?: number | string | null
  invoiced_amount?: number | string | null
  fees_contract_amount?: number | string | null
}

function num(v: number | string | null | undefined): number {
  const n = Number(v)
  return isNaN(n) ? 0 : n
}

/** % = consommé / budget, arrondi à 1 décimale ; 0 si budget ≤ 0 ou absent. */
export function pct(
  consumed: number | string | null | undefined,
  budget: number | string | null | undefined,
): number {
  const b = num(budget)
  if (b <= 0) return 0
  return Math.round((num(consumed) / b) * 1000) / 10
}

export function progressHoursPct(phase: PhaseFinancials): number {
  return pct(phase.actual_hours, phase.tasks_budgeted_hours)
}

export function progressCostPct(phase: PhaseFinancials): number {
  return pct(phase.actual_cost, phase.tasks_budgeted_cost)
}

export function progressFeesPct(phase: PhaseFinancials): number {
  return pct(phase.invoiced_amount, phase.fees_contract_amount)
}
