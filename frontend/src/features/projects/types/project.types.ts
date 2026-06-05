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
  is_public: boolean
  is_consortium: boolean
  consortium: number | null
  consortium_name?: string
  services_transversaux: string[]
  business_unit: string
  legal_entity: string
  start_date: string | null
  end_date: string | null
  pm: number | null
  associate_in_charge: number | null
  invoice_approver: number | null
  bu_director: number | null
  team_members?: number[]
  team_members_detail?: Array<{ id: number; name: string }>
  version: number
  phases: Phase[]
  support_services: SupportService[]
  total_fees?: string | null
  fee_calculation_method?: 'FORFAIT' | 'COUT_TRAVAUX' | 'HORAIRE'
  fee_rate_pct?: string | null
  construction_cost?: string | number | null
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
  tasks_budgeted_hours?: number
  tasks_budgeted_cost?: number
  planned_hours?: number
  actual_hours?: number
  has_tasks?: boolean
  task_count?: number
  amendment?: number | null
  amendment_number?: number | null
}

export interface SupportService {
  id: number
  code: string
  name: string
  client_facing_label: string
  budgeted_hours: string
  budgeted_cost: string
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
