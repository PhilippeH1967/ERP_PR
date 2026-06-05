/**
 * Helpers de structure des tâches (Phase → Tâche → Sous-tâche).
 *
 * Règle métier : la phase est un regroupement. Une tâche qui a des
 * sous-tâches devient une « tâche-mère » en lecture seule (pur agrégat) ;
 * seules les tâches saisissables (sans sous-tâche) portent le budget.
 */

export interface TaskLike {
  id: number
  is_chargeable?: boolean
}

export interface PhaseGroupLike<T> {
  phase_name: string
  phase_id: number | null
  tasks: T[]
}

/**
 * Groupes affichés dans l'onglet Tâches : uniquement les phases qui ont au
 * moins une tâche. Les phases standard vides sont masquées ici (elles
 * restent accessibles via le sélecteur « + Tâche » et l'écran Phases).
 */
export function visibleTaskGroups<T>(groups: PhaseGroupLike<T>[]): PhaseGroupLike<T>[] {
  return groups.filter((g) => g.tasks.length > 0)
}

/**
 * Une tâche est en lecture seule (agrégat) lorsqu'elle a des sous-tâches,
 * c.-à-d. ``is_chargeable === false``. Par défaut (champ absent), la tâche
 * est considérée saisissable pour ne pas bloquer les données héritées.
 */
export function isTaskReadOnly(task: TaskLike): boolean {
  return task.is_chargeable === false
}
