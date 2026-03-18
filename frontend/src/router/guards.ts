/**
 * Router navigation guards for authentication and authorization.
 */

import type { NavigationGuardNext, RouteLocationNormalized } from 'vue-router'
import { useAuth } from '@/shared/composables/useAuth'

/**
 * Auth guard: redirects unauthenticated users to /login.
 * Public routes must have `meta: { public: true }`.
 */
export function authGuard(
  to: RouteLocationNormalized,
  _from: RouteLocationNormalized,
  next: NavigationGuardNext,
) {
  const { isAuthenticated } = useAuth()

  if (to.meta.public || isAuthenticated.value) {
    next()
  } else {
    next({ name: 'login', query: { redirect: to.fullPath } })
  }
}
