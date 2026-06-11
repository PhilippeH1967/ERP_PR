/**
 * Helpers d'échéancier (onglet Tâches) — fonctions pures testées.
 */

/** Décale une date ISO (YYYY-MM-DD) de `days` jours. Null/vide → null. */
export function shiftIsoDate(iso: string | null | undefined, days: number): string | null {
  if (!iso) return null
  const d = new Date(iso + 'T00:00:00')
  if (Number.isNaN(d.getTime())) return null
  d.setDate(d.getDate() + days)
  const mm = String(d.getMonth() + 1).padStart(2, '0')
  const dd = String(d.getDate()).padStart(2, '0')
  return `${d.getFullYear()}-${mm}-${dd}`
}

export interface DatedNode {
  id: number
  parent: number | null
  start_date?: string | null
  end_date?: string | null
}

/** Dates dérivées d'une tâche-mère : min(start) / max(end) de ses sous-tâches. */
export function derivedDates(parent: DatedNode, all: DatedNode[]): { start: string | null; end: string | null } {
  const subs = all.filter((t) => t.parent === parent.id)
  const starts = subs.map((s) => s.start_date).filter(Boolean) as string[]
  const ends = subs.map((s) => s.end_date).filter(Boolean) as string[]
  return {
    start: starts.length ? [...starts].sort()[0]! : null,
    end: ends.length ? [...ends].sort().slice(-1)[0]! : null,
  }
}
