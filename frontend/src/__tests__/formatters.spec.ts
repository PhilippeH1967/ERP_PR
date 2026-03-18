import { describe, expect, it } from 'vitest'
import { formatCurrency, formatHours, formatNumber, formatPercent } from '@/shared/utils/formatters'
import { formatDate } from '@/shared/utils/dateUtils'

describe('formatCurrency', () => {
  it('formats FR currency correctly', () => {
    const result = formatCurrency('10200.50', 'fr')
    // fr-CA format: varies by runtime, check essentials
    expect(result).toContain('10')
    expect(result).toContain('200')
    expect(result).toContain('50')
    expect(result).toContain('$')
  })

  it('formats EN currency correctly', () => {
    const result = formatCurrency('10200.50', 'en')
    expect(result).toContain('$')
    expect(result).toContain('10')
    expect(result).toContain('200')
    expect(result).toContain('50')
  })

  it('handles string input', () => {
    expect(formatCurrency('15234.50', 'fr')).toBeTruthy()
  })

  it('handles invalid input', () => {
    expect(formatCurrency('abc', 'fr')).toBe('')
  })
})

describe('formatNumber', () => {
  it('formats with locale separators', () => {
    const result = formatNumber(1234.56, 'fr')
    expect(result).toBeTruthy()
    expect(result).toContain('1')
    expect(result).toContain('234')
  })
})

describe('formatPercent', () => {
  it('formats percentage', () => {
    const result = formatPercent(65.5, 'fr')
    expect(result).toContain('65')
    expect(result).toContain('%')
  })
})

describe('formatHours', () => {
  it('formats hours with h suffix', () => {
    const result = formatHours(7.5, 'fr')
    expect(result).toContain('7')
    expect(result).toContain('h')
  })
})

describe('formatDate', () => {
  it('formats as YYYY-MM-DD', () => {
    expect(formatDate('2026-03-17T14:30:00Z')).toBe('2026-03-17')
  })

  it('handles Date object', () => {
    const result = formatDate(new Date('2026-01-15'))
    expect(result).toBe('2026-01-15')
  })

  it('handles invalid date', () => {
    expect(formatDate('invalid')).toBe('')
  })
})
