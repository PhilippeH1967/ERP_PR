/**
 * Vue I18n configuration for bilingual FR/EN support.
 * Full i18n content will be populated in Story 1.5.
 */

import { createI18n } from 'vue-i18n'

import en from '@/locales/en.json'
import fr from '@/locales/fr.json'

export const i18n = createI18n({
  legacy: false,
  locale: 'fr',
  fallbackLocale: 'en',
  messages: {
    fr,
    en,
  },
})
