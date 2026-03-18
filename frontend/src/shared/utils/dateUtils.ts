/**
 * Date formatting utilities — Quebec standard YYYY-MM-DD.
 *
 * All dates use ISO 8601 format (YYYY-MM-DD) regardless of locale.
 * Time formatting respects locale (24h for FR, 12h for EN).
 */

/**
 * Format a date as YYYY-MM-DD (Quebec standard).
 */
export function formatDate(date: Date | string): string {
  const d = typeof date === 'string' ? new Date(date) : date
  if (isNaN(d.getTime())) return ''
  return d.toISOString().slice(0, 10)
}

/**
 * Format a date with time, locale-aware.
 */
export function formatDateTime(date: Date | string, locale: string = 'fr-CA'): string {
  const d = typeof date === 'string' ? new Date(date) : date
  if (isNaN(d.getTime())) return ''
  return new Intl.DateTimeFormat(locale, {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  }).format(d)
}

/**
 * Get the start of the week (Monday) for a given date.
 */
export function getWeekStart(date: Date): Date {
  const d = new Date(date)
  const day = d.getDay()
  const diff = d.getDate() - day + (day === 0 ? -6 : 1)
  d.setDate(diff)
  d.setHours(0, 0, 0, 0)
  return d
}
