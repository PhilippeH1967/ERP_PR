export interface Project {
  id: number
  code: string
  name: string
  client: number | null
  client_name?: string
  template: number | null
  contract_type: 'FORFAITAIRE' | 'CONSORTIUM' | 'CO_DEV' | 'CONCEPTION_CONSTRUCTION'
  status: 'ACTIVE' | 'ON_HOLD' | 'COMPLETED' | 'CANCELLED'
  is_internal: boolean
  business_unit: string
  legal_entity: string
  start_date: string | null
  end_date: string | null
  pm: number | null
  associate_in_charge: number | null
  invoice_approver: number | null
  bu_director: number | null
  version: number
  phases: Phase[]
  support_services: SupportService[]
  created_at: string
  updated_at: string
}

export interface Phase {
  id: number
  code: string
  name: string
  client_facing_label: string
  phase_type: 'REALIZATION' | 'SUPPORT'
  billing_mode: 'FORFAIT' | 'HORAIRE'
  order: number
  start_date: string | null
  end_date: string | null
  is_mandatory: boolean
  is_locked: boolean
  budgeted_hours: string
  budgeted_cost: string
}

export interface SupportService {
  id: number
  code: string
  name: string
  client_facing_label: string
  budgeted_hours: string
  budgeted_cost: string
}

export interface WBSElement {
  id: number
  parent: number | null
  phase: number | null
  standard_label: string
  client_facing_label: string
  element_type: 'PHASE' | 'TASK' | 'SUBTASK'
  order: number
  budgeted_hours: string
  budgeted_cost: string
  is_billable: boolean
  children: WBSElement[]
}

export interface ProjectTemplate {
  id: number
  name: string
  code: string
  contract_type: string
  description: string
  phases_config: Record<string, unknown>[]
  support_services_config: Record<string, unknown>[]
}
