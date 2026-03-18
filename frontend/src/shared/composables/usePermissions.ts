/**
 * Permissions composable for RBAC role checks in Vue components.
 *
 * Reads roles from JWT claims (decoded from token or API response).
 * Provides reactive role-checking functions for conditional rendering.
 */

import { ref, computed } from 'vue'

interface ProjectRoleEntry {
  project_id: number | null
  role: string
}

const userRoles = ref<ProjectRoleEntry[]>([])

export function usePermissions() {
  function setRoles(roles: ProjectRoleEntry[]) {
    userRoles.value = roles
  }

  function hasRole(role: string, projectId?: number): boolean {
    return userRoles.value.some(
      (r) => r.role === role && (projectId === undefined || r.project_id === projectId),
    )
  }

  const isAdmin = computed(() => hasRole('ADMIN'))
  const isFinance = computed(() => hasRole('FINANCE'))
  const isBUDirector = computed(() => hasRole('BU_DIRECTOR'))

  function isProjectPM(projectId: number): boolean {
    return hasRole('PM', projectId)
  }

  function isProjectDirector(projectId: number): boolean {
    return hasRole('PROJECT_DIRECTOR', projectId)
  }

  function canApproveInvoice(projectId: number): boolean {
    return isFinance.value || isProjectDirector(projectId)
  }

  const canSeeSalaryCosts = computed(() =>
    userRoles.value.some((r) =>
      ['FINANCE', 'PROJECT_DIRECTOR', 'BU_DIRECTOR', 'ADMIN'].includes(r.role),
    ),
  )

  return {
    userRoles,
    setRoles,
    hasRole,
    isAdmin,
    isFinance,
    isBUDirector,
    isProjectPM,
    isProjectDirector,
    canApproveInvoice,
    canSeeSalaryCosts,
  }
}
