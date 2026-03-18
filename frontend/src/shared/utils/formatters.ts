/**
 * Locale-aware currency, number, and percentage formatters.
 *
 * Currency rules:
 *   EN: $10,200.50 (dollar prefix, comma thousands, period decimal)
 *   FR: 10 200,50 $ (space thousands, comma decimal, dollar suffix)
 *
 * All monetary values from API are strings (not floats) to avoid rounding.
 */

type Locale = 'fr' | 'en'

const LOCALE_MAP: Record<Locale, string> = {
  fr: 'fr-CA',
  en: 'en-CA',
}

/**
 * Format a monetary amount string with locale-aware separators.
 * Input: "15234.50" (API string format)
 * Output FR: "15 234,50 $"
 * Output EN: "$15,234.50"
 */
export function formatCurrency(amount: string | number, locale: Locale = 'fr'): string {
  const num = typeof amount === 'string' ? parseFloat(amount) : amount
  if (isNaN(num)) return ''
  return new Intl.NumberFormat(LOCALE_MAP[locale], {
    style: 'currency',
    currency: 'CAD',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(num)
}

/**
 * Format a number with locale-aware thousands/decimal separators.
 */
export function formatNumber(
  value: number | string,
  locale: Locale = 'fr',
  decimals: number = 2,
): string {
  const num = typeof value === 'string' ? parseFloat(value) : value
  if (isNaN(num)) return ''
  return new Intl.NumberFormat(LOCALE_MAP[locale], {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(num)
}

/**
 * Format a percentage value. Input: 65.5 → "65,50 %" (FR) or "65.50%" (EN)
 */
export function formatPercent(value: number | string, locale: Locale = 'fr'): string {
  const num = typeof value === 'string' ? parseFloat(value) : value
  if (isNaN(num)) return ''
  return new Intl.NumberFormat(LOCALE_MAP[locale], {
    style: 'percent',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(num / 100)
}

/**
 * Format hours (e.g., 7.5 → "7,5 h" in FR, "7.5 h" in EN)
 */
export function formatHours(hours: number | string, locale: Locale = 'fr'): string {
  const num = typeof hours === 'string' ? parseFloat(hours) : hours
  if (isNaN(num)) return ''
  const formatted = new Intl.NumberFormat(LOCALE_MAP[locale], {
    minimumFractionDigits: 1,
    maximumFractionDigits: 1,
  }).format(num)
  return `${formatted}\u00a0h`
}
