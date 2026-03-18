export interface Client {
  id: number
  name: string
  alias: string
  legal_entity: string
  sector: string
  status: 'active' | 'inactive' | 'archived'
  payment_terms_days: number
  default_invoice_template: string
  associe_en_charge: string
  notes: string
  version: number
  contacts: Contact[]
  addresses: ClientAddress[]
  created_at: string
  updated_at: string
}

export interface Contact {
  id: number
  name: string
  role: string
  email: string
  phone: string
  language_preference: 'fr' | 'en'
}

export interface ClientAddress {
  id: number
  address_line_1: string
  address_line_2: string
  city: string
  province: string
  postal_code: string
  country: string
  is_billing: boolean
  is_primary: boolean
}
