// ISO 8601 week helpers for Manuelle-mode allocation grid.
// The Thursday-of-the-week method (ISO: week 1 contains the year's first Thursday).

export function isoWeekKey(d: Date): string {
  const dt = new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate()))
  const dayNum = dt.getUTCDay() || 7
  dt.setUTCDate(dt.getUTCDate() + 4 - dayNum)
  const yearStart = new Date(Date.UTC(dt.getUTCFullYear(), 0, 1))
  const weekNo = Math.ceil((((dt.getTime() - yearStart.getTime()) / 86400000) + 1) / 7)
  return `${dt.getUTCFullYear()}-W${String(weekNo).padStart(2, '0')}`
}

export function isoWeeksBetween(startISO: string, endISO: string): string[] {
  if (!startISO || !endISO) return []
  const out: string[] = []
  const start = new Date(startISO + 'T00:00:00Z')
  const end = new Date(endISO + 'T00:00:00Z')
  if (Number.isNaN(start.getTime()) || Number.isNaN(end.getTime()) || end < start) return []
  const cursor = new Date(start)
  let last = ''
  while (cursor <= end) {
    const key = isoWeekKey(cursor)
    if (key !== last) {
      out.push(key)
      last = key
    }
    cursor.setUTCDate(cursor.getUTCDate() + 1)
  }
  return out
}

export function weekLabel(key: string): string {
  const m = key.match(/^\d{4}-W(\d{2})$/)
  return m ? `S${m[1]}` : key
}
