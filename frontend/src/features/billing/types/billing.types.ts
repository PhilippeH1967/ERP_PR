export interface Invoice {
  id: number
  project: number
  project_code?: string
  project_name?: string
  client: number
  client_name?: string
  invoice_number: string
  status: 'DRAFT' | 'SUBMITTED' | 'APPROVED' | 'SENT' | 'PAID'
  total_amount: string
  tax_tps: string
  tax_tvq: string
  version: number
  lines: InvoiceLine[]
  date_created: string
  date_sent: string | null
  date_paid: string | null
}

export interface InvoiceLine {
  id: number
  deliverable_name: string
  line_type: 'FORFAIT' | 'HORAIRE' | 'ST' | 'DEPENSE'
  total_contract_amount: string
  invoiced_to_date: string
  pct_billing_advancement: string
  pct_hours_advancement: string
  amount_to_bill: string
  pct_after_billing: string
}
