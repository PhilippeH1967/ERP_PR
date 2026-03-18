export interface ExpenseReport {
  id: number
  employee: number
  project: number | null
  status: 'SUBMITTED' | 'PM_APPROVED' | 'FINANCE_VALIDATED' | 'PAID' | 'REVERSED' | 'REJECTED'
  total_amount: string
  version: number
  lines: ExpenseLine[]
  submitted_at: string
}

export interface ExpenseLine {
  id: number
  category: number
  expense_date: string
  amount: string
  description: string
  receipt_path: string
  is_refacturable: boolean
  tax_type: 'HT' | 'TPS' | 'TVQ'
}

export interface ExpenseCategory {
  id: number
  name: string
  is_refacturable_default: boolean
  requires_receipt: boolean
}
