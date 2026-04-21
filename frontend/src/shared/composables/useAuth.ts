/**
 * Authentication composable — local login (JWT) + optional SSO.
 *
 * Provides reactive auth state, login methods, and token management.
 */

import { ref, computed } from 'vue'
import apiClient from '@/plugins/axios'

interface User {
  id: number
  email: string
  username: string
  first_name?: string
  last_name?: string
  tenant_id: number | null
  roles: string[]
}

interface AuthConfig {
  sso_available: boolean
  sso_only: boolean
}

const currentUser = ref<User | null>(null)
const isLoading = ref(false)
const authConfig = ref<AuthConfig>({ sso_available: false, sso_only: false })

export function useAuth() {
  const isAuthenticated = computed(() => currentUser.value !== null)

  /** Fetch auth config (SSO availability) — call before showing login form. */
  async function fetchAuthConfig() {
    try {
      const response = await apiClient.get('/auth/config/')
      authConfig.value = response.data?.data || response.data
    } catch {
      // Default: local login only
      authConfig.value = { sso_available: false, sso_only: false }
    }
  }

  /** Local login with username + password (JWT). */
  async function loginWithCredentials(
    username: string,
    password: string,
  ): Promise<void> {
    const response = await apiClient.post('/auth/token/', { username, password })
    const data = response.data?.data || response.data
    // Store tokens for subsequent requests
    if (data.access) {
      localStorage.setItem('access_token', data.access)
    }
    if (data.refresh) {
      localStorage.setItem('refresh_token', data.refresh)
    }
    // Fetch user profile
    await fetchCurrentUser()
  }

  /** Redirect to SSO login (Entra ID OIDC via django-allauth). */
  async function loginSSO() {
    window.location.href = '/accounts/openid_connect/login/?process=login'
  }

  async function logout() {
    try {
      currentUser.value = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      window.location.href = '/login'
    } catch {
      currentUser.value = null
    }
  }

  async function refreshToken(): Promise<boolean> {
    try {
      const refresh = localStorage.getItem('refresh_token')
      if (!refresh) return false
      const response = await apiClient.post('/auth/token/refresh/', { refresh })
      const data = response.data?.data || response.data
      if (data.access) {
        localStorage.setItem('access_token', data.access)
      }
      return true
    } catch {
      currentUser.value = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      return false
    }
  }

  async function fetchCurrentUser() {
    isLoading.value = true
    try {
      const response = await apiClient.get('/auth/me/')
      currentUser.value = response.data?.data || response.data
    } catch {
      currentUser.value = null
    } finally {
      isLoading.value = false
    }
  }

  return {
    currentUser,
    isAuthenticated,
    isLoading,
    authConfig,
    fetchAuthConfig,
    loginWithCredentials,
    loginSSO,
    logout,
    refreshToken,
    fetchCurrentUser,
  }
}
