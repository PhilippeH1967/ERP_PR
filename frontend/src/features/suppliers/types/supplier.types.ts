export interface ExternalOrganization {
  id: number
  name: string
  neq: string
  address: string
  city: string
  province: string
  postal_code: string
  country: string
  contact_name: string
  contact_email: string
  contact_phone: string
  type_tags: string[]
  is_active: boolean
}

export interface STInvoice {
  id: number
  project: number
  supplier: number
  invoice_number: string
  invoice_date: string
  amount: string
  source: 'manual' | 'api'
  status: 'received' | 'authorized' | 'paid' | 'disputed' | 'credited'
  budget_internal: string
  budget_refacturable: string
  budget_absorbed: string
}
