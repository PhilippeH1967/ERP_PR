/**
 * Router navigation guards for authentication and authorization.
 */

import type { NavigationGuardNext, RouteLocationNormalized } from 'vue-router'
import { useAuth } from '@/shared/composables/useAuth'

let initialized = false

/**
 * Auth guard: redirects unauthenticated users to /login.
 * On first navigation, tries to restore session from stored token.
 * Public routes must have `meta: { public: true }`.
 */
export async function authGuard(
  to: RouteLocationNormalized,
  _from: RouteLocationNormalized,
  next: NavigationGuardNext,
) {
  if (to.meta.public) {
    next()
    return
  }

  const { isAuthenticated, fetchCurrentUser } = useAuth()

  // On first load, try to restore session if token exists
  if (!initialized) {
    initialized = true
    const token = localStorage.getItem('access_token')
    if (token && !isAuthenticated.value) {
      await fetchCurrentUser()
    }
  }

  if (!isAuthenticated.value) {
    next({ name: 'login', query: { redirect: to.fullPath } })
    return
  }

  // Role-based route protection
  const { currentUser } = useAuth()
  const roles = currentUser.value?.roles || []

  // Admin routes require ADMIN role
  if (to.path.startsWith('/admin')) {
    if (!roles.includes('ADMIN')) {
      next({ name: 'dashboard' })
      return
    }
  }

  // Billing/Payments/CreditNotes/Holdbacks/WriteOffs — Finance, ADMIN, PM, PROJECT_DIRECTOR
  const financeRoutes = ['/billing', '/payments', '/credit-notes', '/holdbacks', '/write-offs']
  if (financeRoutes.some(r => to.path.startsWith(r))) {
    const allowed = ['ADMIN', 'FINANCE', 'PM', 'PROJECT_DIRECTOR']
    if (!roles.some(r => allowed.includes(r))) {
      next({ name: 'dashboard' })
      return
    }
  }

  // Approvals — PM, PROJECT_DIRECTOR, FINANCE, PAIE, ADMIN
  if (to.path.startsWith('/approvals')) {
    const allowed = ['ADMIN', 'FINANCE', 'PM', 'PROJECT_DIRECTOR', 'PAIE']
    if (!roles.some(r => allowed.includes(r))) {
      next({ name: 'dashboard' })
      return
    }
  }

  // Period locks — FINANCE, PAIE, ADMIN
  if (to.path.startsWith('/period-locks')) {
    const allowed = ['ADMIN', 'FINANCE', 'PAIE']
    if (!roles.some(r => allowed.includes(r))) {
      next({ name: 'dashboard' })
      return
    }
  }

  // Consortiums — ADMIN, FINANCE, PM, PROJECT_DIRECTOR
  if (to.path.startsWith('/consortiums')) {
    const allowed = ['ADMIN', 'FINANCE', 'PM', 'PROJECT_DIRECTOR']
    if (!roles.some(r => allowed.includes(r))) {
      next({ name: 'dashboard' })
      return
    }
  }

  next()
}
