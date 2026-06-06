/**
 * Helpers purs (testables) de la logique de planification Gantt.
 *
 * Règles métier : seules les tâches saisissables (feuilles) se planifient ;
 * les phases sans tâche sont masquées ; le planifié est contrôlé contre le
 * budget (non bloquant).
 */

export interface ChargeableLike {
  is_chargeable?: boolean
}

/** Une tâche AVEC sous-tâches (is_chargeable === false) est un agrégat
 *  (comme une phase) : non planifiable. Par défaut (champ absent) = feuille. */
export function isAggregateTask(t: ChargeableLike): boolean {
  return t.is_chargeable === false
}

export interface PhaseLike {
  id: number
}
export interface TaskPhaseRef {
  phase: number
}

/** Phases à afficher dans le Gantt : uniquement celles ayant au moins une tâche. */
export function phasesWithTasks<P extends PhaseLike>(phases: P[], tasks: TaskPhaseRef[]): P[] {
  return phases.filter((p) => tasks.some((t) => t.phase === p.id))
}

export interface AllocationLike {
  hours_per_week: number
  start_date: string
  end_date: string
}

/**
 * Heures planifiées TOTALES = Σ (h/sem × nombre de semaines) sur les allocations.
 * `weeksOf` calcule le nombre de semaines entre deux dates (injecté pour rester pur).
 */
export function totalPlannedHours(
  allocs: AllocationLike[],
  weeksOf: (start: string, end: string) => number,
): number {
  return allocs.reduce(
    (sum, a) => sum + a.hours_per_week * Math.max(1, weeksOf(a.start_date, a.end_date)),
    0,
  )
}

/** Contrôle non bloquant : vrai si le planifié dépasse un budget (> 0). */
export function isOverBudget(planned: number, budget: number): boolean {
  return budget > 0 && planned > budget
}
