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

  // Admin routes require ADMIN role
  if (to.path.startsWith('/admin')) {
    const { currentUser } = useAuth()
    const roles = currentUser.value?.roles || []
    if (!roles.includes('ADMIN')) {
      next({ name: 'dashboard' })
      return
    }
  }

  next()
}
