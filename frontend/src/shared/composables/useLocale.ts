/**
 * Locale composable for language switching and formatting context.
 *
 * Integrates with Vue I18n for reactive locale changes.
 * Provides formatting functions bound to current locale.
 */

import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { formatCurrency, formatHours, formatNumber, formatPercent } from '@/shared/utils/formatters'
import { formatDate, formatDateTime } from '@/shared/utils/dateUtils'

export type AppLocale = 'fr' | 'en'

export function useLocale() {
  const { locale } = useI18n()

  const currentLocale = computed<AppLocale>(() => (locale.value === 'en' ? 'en' : 'fr'))

  function switchLocale(newLocale: AppLocale) {
    locale.value = newLocale
    document.documentElement.lang = newLocale
    localStorage.setItem('erp_locale', newLocale)
  }

  function initLocale() {
    const saved = localStorage.getItem('erp_locale') as AppLocale | null
    if (saved && (saved === 'fr' || saved === 'en')) {
      switchLocale(saved)
    }
  }

  // Bound formatting functions using current locale
  const fmt = {
    currency: (amount: string | number) => formatCurrency(amount, currentLocale.value),
    number: (value: number | string, decimals?: number) =>
      formatNumber(value, currentLocale.value, decimals),
    percent: (value: number | string) => formatPercent(value, currentLocale.value),
    hours: (hours: number | string) => formatHours(hours, currentLocale.value),
    date: formatDate,
    dateTime: (date: Date | string) =>
      formatDateTime(date, currentLocale.value === 'fr' ? 'fr-CA' : 'en-CA'),
  }

  return {
    currentLocale,
    switchLocale,
    initLocale,
    fmt,
  }
}
