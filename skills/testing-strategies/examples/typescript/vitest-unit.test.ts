/**
 * Unit Testing Examples with Vitest
 *
 * Demonstrates: Unit testing pure functions and business logic
 *
 * Dependencies:
 * - npm install -D vitest
 *
 * Usage:
 * - npx vitest run vitest-unit.test.ts
 */

import { describe, test, expect } from 'vitest'

// ====================
// System Under Test
// ====================

interface CartItem {
  price: number
  quantity: number
  taxable?: boolean
}

function calculateTotal(items: CartItem[], taxRate = 0): number {
  const subtotal = items.reduce((sum, item) => sum + (item.price * item.quantity), 0)
  const taxableAmount = items
    .filter(item => item.taxable !== false)
    .reduce((sum, item) => sum + (item.price * item.quantity), 0)
  const tax = taxableAmount * taxRate
  return Math.round((subtotal + tax) * 100) / 100
}

function formatCurrency(amount: number, locale = 'en-US', currency = 'USD'): string {
  return new Intl.NumberFormat(locale, {
    style: 'currency',
    currency
  }).format(amount)
}

function validateEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

// ====================
// Unit Tests
// ====================

describe('calculateTotal', () => {
  test('calculates total for single item', () => {
    const items: CartItem[] = [{ price: 10, quantity: 1 }]
    expect(calculateTotal(items)).toBe(10)
  })

  test('calculates total for multiple items', () => {
    const items: CartItem[] = [
      { price: 10, quantity: 2 },
      { price: 5, quantity: 1 }
    ]
    expect(calculateTotal(items)).toBe(25)
  })

  test('applies tax rate correctly', () => {
    const items: CartItem[] = [{ price: 10, quantity: 1 }]
    expect(calculateTotal(items, 0.1)).toBe(11)
  })

  test('handles non-taxable items', () => {
    const items: CartItem[] = [
      { price: 10, quantity: 1, taxable: true },
      { price: 5, quantity: 1, taxable: false }
    ]
    expect(calculateTotal(items, 0.1)).toBe(16) // Only $10 taxed: 10 + 1 + 5 = 16
  })

  test('rounds to two decimal places', () => {
    const items: CartItem[] = [{ price: 10.99, quantity: 1 }]
    expect(calculateTotal(items, 0.075)).toBe(11.81) // 10.99 * 1.075 = 11.81425 → 11.81
  })

  test('handles empty cart', () => {
    expect(calculateTotal([])).toBe(0)
  })

  test('handles zero quantity', () => {
    const items: CartItem[] = [{ price: 10, quantity: 0 }]
    expect(calculateTotal(items)).toBe(0)
  })
})

describe('formatCurrency', () => {
  test('formats USD currency', () => {
    expect(formatCurrency(1234.56)).toBe('$1,234.56')
  })

  test('formats EUR currency', () => {
    expect(formatCurrency(1234.56, 'de-DE', 'EUR')).toBe('1.234,56 €')
  })

  test('handles zero amount', () => {
    expect(formatCurrency(0)).toBe('$0.00')
  })

  test('handles negative amounts', () => {
    expect(formatCurrency(-50.25)).toBe('-$50.25')
  })

  test('rounds to currency precision', () => {
    expect(formatCurrency(10.999)).toBe('$11.00')
  })
})

describe('validateEmail', () => {
  test('accepts valid email', () => {
    expect(validateEmail('user@example.com')).toBe(true)
  })

  test('accepts email with plus addressing', () => {
    expect(validateEmail('user+tag@example.com')).toBe(true)
  })

  test('accepts email with subdomain', () => {
    expect(validateEmail('user@mail.example.com')).toBe(true)
  })

  test('rejects email without @', () => {
    expect(validateEmail('userexample.com')).toBe(false)
  })

  test('rejects email without domain', () => {
    expect(validateEmail('user@')).toBe(false)
  })

  test('rejects email without username', () => {
    expect(validateEmail('@example.com')).toBe(false)
  })

  test('rejects email with spaces', () => {
    expect(validateEmail('user @example.com')).toBe(false)
  })

  test('rejects empty string', () => {
    expect(validateEmail('')).toBe(false)
  })
})

// ====================
// Testing with Test Fixtures
// ====================

describe('calculateTotal with fixtures', () => {
  // Fixture: Sample cart for testing
  const sampleCart: CartItem[] = [
    { price: 19.99, quantity: 2, taxable: true },
    { price: 5.00, quantity: 1, taxable: false },
    { price: 12.50, quantity: 3, taxable: true }
  ]

  test('calculates subtotal correctly', () => {
    expect(calculateTotal(sampleCart, 0)).toBe(82.48)
  })

  test('applies tax to taxable items only', () => {
    // Taxable: (19.99 * 2) + (12.50 * 3) = 39.98 + 37.50 = 77.48
    // Tax: 77.48 * 0.08 = 6.20
    // Total: 82.48 + 6.20 = 88.68
    expect(calculateTotal(sampleCart, 0.08)).toBe(88.68)
  })
})

// ====================
// Parametrized Tests (Testing Multiple Cases)
// ====================

describe('parametrized currency formatting', () => {
  const testCases = [
    { amount: 0, locale: 'en-US', currency: 'USD', expected: '$0.00' },
    { amount: 1234.56, locale: 'en-US', currency: 'USD', expected: '$1,234.56' },
    { amount: 1234.56, locale: 'de-DE', currency: 'EUR', expected: '1.234,56 €' },
    { amount: 1234.56, locale: 'ja-JP', currency: 'JPY', expected: '¥1,235' },
    { amount: -100, locale: 'en-US', currency: 'USD', expected: '-$100.00' }
  ]

  testCases.forEach(({ amount, locale, currency, expected }) => {
    test(`formats ${amount} as ${currency} in ${locale}`, () => {
      expect(formatCurrency(amount, locale, currency)).toBe(expected)
    })
  })
})

// ====================
// Edge Case Testing
// ====================

describe('edge cases', () => {
  test('handles very large numbers', () => {
    const items: CartItem[] = [{ price: 999999.99, quantity: 1 }]
    expect(calculateTotal(items)).toBe(999999.99)
  })

  test('handles very small prices', () => {
    const items: CartItem[] = [{ price: 0.01, quantity: 100 }]
    expect(calculateTotal(items)).toBe(1)
  })

  test('handles floating point precision', () => {
    const items: CartItem[] = [{ price: 0.1, quantity: 3 }]
    // 0.1 * 3 should be 0.3, not 0.30000000000000004
    expect(calculateTotal(items)).toBe(0.3)
  })
})
