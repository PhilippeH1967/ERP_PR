/**
 * useSidebarMenu — Composable that returns a role-adaptive sidebar configuration.
 *
 * The sidebar items, sections, and contextual logo subtitle are determined by the
 * user's dominant role. The matrix is the single source of truth for all menus.
 *
 * Source: _bmad-output/tech-specs/tech-spec-sidebar-quick-win-2026-04-11.md
 * Mockup: _bmad-output/mockups/flux/sidebar-quick-win-personas.html
 */

import { computed } from 'vue'
import { useAuth } from './useAuth'

export interface SidebarItem {
  /** i18n key under sidebar.item.* */
  key: string
  /** Vue Router path */
  path: string
  /** Emoji or icon */
  icon: string
}

export interface SidebarSection {
  /** i18n key under sidebar.section.* */
  label: string
  items: SidebarItem[]
}

export interface SidebarConfig {
  /** Subtitle key under role.subtitle.* — drives the topbar logo */
  subtitle: string
  sections: SidebarSection[]
}

/**
 * Priority order: when a user has multiple roles, the first match wins.
 * ADMIN sees the most powerful menu, EMPLOYEE the most reduced.
 */
const ROLE_PRIORITY = [
  'ADMIN',
  'BU_DIRECTOR',
  'PROJECT_DIRECTOR',
  'FINANCE',
  'PAIE',
  'PM',
  'PROPOSAL_MANAGER',
  'DEPT_ASSISTANT',
  'EMPLOYEE',
] as const

type DominantRole = (typeof ROLE_PRIORITY)[number]

/** Help section is identical across all roles */
const HELP_SECTION: SidebarSection = {
  label: 'sidebar.section.help',
  items: [
    { key: 'sidebar.item.help_center', path: '/help', icon: '❓' },
  ],
}

/**
 * Single source of truth: the menu matrix per dominant role.
 * Aligned with mockup _bmad-output/mockups/flux/sidebar-quick-win-personas.html
 */
const ROLE_MENU_MAP: Record<DominantRole, SidebarConfig> = {
  EMPLOYEE: {
    subtitle: 'production',
    sections: [
      {
        label: 'sidebar.section.my_work',
        items: [
          { key: 'sidebar.item.my_dashboard', path: '/dashboard', icon: '📊' },
          { key: 'sidebar.item.my_timesheets', path: '/timesheets', icon: '🕐' },
          { key: 'sidebar.item.my_leaves', path: '/leaves', icon: '🏖️' },
          { key: 'sidebar.item.my_expenses', path: '/expenses', icon: '🧾' },
        ],
      },
      {
        label: 'sidebar.section.my_projects',
        items: [
          { key: 'sidebar.item.assigned_projects', path: '/projects', icon: '📁' },
        ],
      },
      HELP_SECTION,
    ],
  },

  PM: {
    subtitle: 'production',
    sections: [
      {
        label: 'sidebar.section.my_work',
        items: [
          { key: 'sidebar.item.my_dashboard', path: '/dashboard', icon: '📊' },
          { key: 'sidebar.item.my_timesheets', path: '/timesheets', icon: '🕐' },
          { key: 'sidebar.item.my_leaves', path: '/leaves', icon: '🏖️' },
          { key: 'sidebar.item.my_expenses', path: '/expenses', icon: '🧾' },
        ],
      },
      {
        label: 'sidebar.section.pilotage_projects',
        items: [
          { key: 'sidebar.item.my_projects', path: '/projects', icon: '📁' },
          { key: 'sidebar.item.to_approve', path: '/approvals', icon: '✅' },
          { key: 'sidebar.item.planning_2_months', path: '/planning', icon: '📅' },
        ],
      },
      {
        label: 'sidebar.section.finance_projects',
        items: [
          { key: 'sidebar.item.invoices_to_validate', path: '/billing', icon: '📄' },
          { key: 'sidebar.item.subcontractor_invoices', path: '/suppliers', icon: '🏭' },
        ],
      },
      {
        label: 'sidebar.section.references',
        items: [
          { key: 'sidebar.item.clients', path: '/clients', icon: '🤝' },
        ],
      },
      HELP_SECTION,
    ],
  },

  PROJECT_DIRECTOR: {
    subtitle: 'direction',
    sections: [
      {
        label: 'sidebar.section.my_work',
        items: [
          { key: 'sidebar.item.my_dashboard', path: '/dashboard', icon: '📊' },
          { key: 'sidebar.item.my_timesheets', path: '/timesheets', icon: '🕐' },
          { key: 'sidebar.item.my_leaves', path: '/leaves', icon: '🏖️' },
          { key: 'sidebar.item.my_expenses', path: '/expenses', icon: '🧾' },
        ],
      },
      {
        label: 'sidebar.section.pilotage_projects',
        items: [
          { key: 'sidebar.item.supervised_projects', path: '/projects', icon: '📁' },
          { key: 'sidebar.item.invoice_approvals', path: '/approvals', icon: '✅' },
          { key: 'sidebar.item.expense_approvals', path: '/expenses', icon: '🧾' },
          { key: 'sidebar.item.reports', path: '/reports', icon: '📈' },
        ],
      },
      {
        label: 'sidebar.section.consortiums',
        items: [
          { key: 'sidebar.item.my_consortiums', path: '/consortiums', icon: '🏗️' },
          { key: 'sidebar.item.consortium_invoices', path: '/consortiums', icon: '📄' },
          { key: 'sidebar.item.consortium_suppliers', path: '/consortiums', icon: '🏭' },
        ],
      },
      {
        label: 'sidebar.section.references',
        items: [
          { key: 'sidebar.item.clients', path: '/clients', icon: '🤝' },
        ],
      },
      HELP_SECTION,
    ],
  },

  BU_DIRECTOR: {
    subtitle: 'direction',
    sections: [
      {
        label: 'sidebar.section.my_work',
        items: [
          { key: 'sidebar.item.my_dashboard', path: '/dashboard', icon: '📊' },
          { key: 'sidebar.item.my_timesheets', path: '/timesheets', icon: '🕐' },
          { key: 'sidebar.item.my_leaves', path: '/leaves', icon: '🏖️' },
          { key: 'sidebar.item.my_expenses', path: '/expenses', icon: '🧾' },
        ],
      },
      {
        label: 'sidebar.section.pilotage_bu',
        items: [
          { key: 'sidebar.item.portfolio_projects', path: '/projects', icon: '📁' },
          { key: 'sidebar.item.approvals', path: '/approvals', icon: '✅' },
          { key: 'sidebar.item.bu_reports', path: '/reports', icon: '📈' },
        ],
      },
      {
        label: 'sidebar.section.consortiums',
        items: [
          { key: 'sidebar.item.all_consortiums', path: '/consortiums', icon: '🏗️' },
          { key: 'sidebar.item.consortium_invoices', path: '/consortiums', icon: '📄' },
          { key: 'sidebar.item.consortium_suppliers', path: '/consortiums', icon: '🏭' },
          { key: 'sidebar.item.distributions', path: '/consortiums', icon: '💰' },
        ],
      },
      {
        label: 'sidebar.section.references',
        items: [
          { key: 'sidebar.item.clients', path: '/clients', icon: '🤝' },
        ],
      },
      HELP_SECTION,
    ],
  },

  FINANCE: {
    subtitle: 'finance',
    sections: [
      {
        label: 'sidebar.section.my_work',
        items: [
          { key: 'sidebar.item.dashboard', path: '/dashboard', icon: '📊' },
          { key: 'sidebar.item.my_timesheets', path: '/timesheets', icon: '🕐' },
          { key: 'sidebar.item.my_leaves', path: '/leaves', icon: '🏖️' },
        ],
      },
      {
        label: 'sidebar.section.production',
        items: [
          { key: 'sidebar.item.timesheets_to_validate', path: '/approvals', icon: '✅' },
          { key: 'sidebar.item.period_lock_payroll', path: '/period-locks', icon: '🔒' },
        ],
      },
      {
        label: 'sidebar.section.finance_projects',
        items: [
          { key: 'sidebar.item.billing', path: '/billing', icon: '📄' },
          { key: 'sidebar.item.payments', path: '/payments', icon: '💳' },
          { key: 'sidebar.item.expense_reports', path: '/expenses', icon: '🧾' },
          { key: 'sidebar.item.suppliers', path: '/suppliers', icon: '🏭' },
          { key: 'sidebar.item.reports', path: '/reports', icon: '📈' },
        ],
      },
      {
        label: 'sidebar.section.consortiums',
        items: [
          { key: 'sidebar.item.all_consortiums', path: '/consortiums', icon: '🏗️' },
          { key: 'sidebar.item.consortium_invoices', path: '/consortiums', icon: '📄' },
          { key: 'sidebar.item.consortium_suppliers', path: '/consortiums', icon: '🏭' },
          { key: 'sidebar.item.distributions', path: '/consortiums', icon: '💰' },
        ],
      },
      {
        label: 'sidebar.section.intacct',
        items: [
          { key: 'sidebar.item.intacct_import', path: '/admin/import', icon: '📥' },
          { key: 'sidebar.item.intacct_export', path: '/admin/import', icon: '📤' },
          { key: 'sidebar.item.intacct_history', path: '/admin/audit', icon: '📋' },
        ],
      },
      {
        label: 'sidebar.section.references',
        items: [
          { key: 'sidebar.item.clients', path: '/clients', icon: '🤝' },
        ],
      },
      HELP_SECTION,
    ],
  },

  PAIE: {
    subtitle: 'paie',
    sections: [
      {
        label: 'sidebar.section.payroll_validation',
        items: [
          { key: 'sidebar.item.dashboard', path: '/dashboard', icon: '📊' },
          { key: 'sidebar.item.to_validate', path: '/approvals', icon: '✅' },
          { key: 'sidebar.item.period_lock', path: '/period-locks', icon: '🔒' },
        ],
      },
      HELP_SECTION,
    ],
  },

  DEPT_ASSISTANT: {
    subtitle: 'assistance',
    sections: [
      {
        label: 'sidebar.section.my_work',
        items: [
          { key: 'sidebar.item.dashboard', path: '/dashboard', icon: '📊' },
          { key: 'sidebar.item.my_timesheets', path: '/timesheets', icon: '🕐' },
          { key: 'sidebar.item.my_leaves', path: '/leaves', icon: '🏖️' },
        ],
      },
      {
        label: 'sidebar.section.assistance',
        items: [
          { key: 'sidebar.item.projects', path: '/projects', icon: '📁' },
          { key: 'sidebar.item.approvals', path: '/approvals', icon: '✅' },
          { key: 'sidebar.item.billing_readonly', path: '/billing', icon: '📄' },
        ],
      },
      {
        label: 'sidebar.section.delegations',
        items: [
          { key: 'sidebar.item.my_delegations', path: '/delegations', icon: '👥' },
        ],
      },
      HELP_SECTION,
    ],
  },

  PROPOSAL_MANAGER: {
    subtitle: 'commercial',
    sections: [
      {
        label: 'sidebar.section.commercial',
        items: [
          { key: 'sidebar.item.dashboard', path: '/dashboard', icon: '📊' },
          { key: 'sidebar.item.proposals', path: '/projects', icon: '📋' },
          { key: 'sidebar.item.clients', path: '/clients', icon: '🤝' },
        ],
      },
      HELP_SECTION,
    ],
  },

  ADMIN: {
    subtitle: 'admin',
    sections: [
      {
        label: 'sidebar.section.my_work',
        items: [
          { key: 'sidebar.item.dashboard', path: '/dashboard', icon: '📊' },
          { key: 'sidebar.item.my_timesheets', path: '/timesheets', icon: '🕐' },
        ],
      },
      {
        label: 'sidebar.section.pilotage_projects',
        items: [
          { key: 'sidebar.item.projects', path: '/projects', icon: '📁' },
          { key: 'sidebar.item.approvals', path: '/approvals', icon: '✅' },
          { key: 'sidebar.item.planning', path: '/planning', icon: '📅' },
        ],
      },
      {
        label: 'sidebar.section.finance_projects',
        items: [
          { key: 'sidebar.item.billing', path: '/billing', icon: '📄' },
          { key: 'sidebar.item.expense_reports', path: '/expenses', icon: '🧾' },
        ],
      },
      {
        label: 'sidebar.section.references',
        items: [
          { key: 'sidebar.item.clients', path: '/clients', icon: '🤝' },
          { key: 'sidebar.item.consortiums', path: '/consortiums', icon: '🏗️' },
          { key: 'sidebar.item.suppliers', path: '/suppliers', icon: '🏭' },
        ],
      },
      {
        label: 'sidebar.section.administration',
        items: [
          { key: 'sidebar.item.admin', path: '/admin', icon: '⚙️' },
        ],
      },
      HELP_SECTION,
    ],
  },
}

/**
 * Compute the dominant role for a user based on the priority list.
 * Returns 'EMPLOYEE' as fallback if no recognized role is found.
 */
export function resolveDominantRole(userRoles: string[] | undefined | null): DominantRole {
  if (!userRoles || userRoles.length === 0) return 'EMPLOYEE'
  for (const r of ROLE_PRIORITY) {
    if (userRoles.includes(r)) return r
  }
  return 'EMPLOYEE'
}

export function useSidebarMenu() {
  const { currentUser } = useAuth()

  const dominantRole = computed<DominantRole>(() =>
    resolveDominantRole(currentUser.value?.roles),
  )

  const config = computed<SidebarConfig>(() => ROLE_MENU_MAP[dominantRole.value])

  const sections = computed<SidebarSection[]>(() => config.value.sections)

  const subtitleKey = computed(() => `role.subtitle.${config.value.subtitle}`)

  return {
    dominantRole,
    sections,
    subtitleKey,
  }
}
