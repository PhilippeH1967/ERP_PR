/**
 * Authentication composable for SSO + JWT flow.
 *
 * Provides reactive auth state, login/logout methods, and token management.
 */

import { ref, computed } from 'vue'
import apiClient from '@/plugins/axios'

interface User {
  id: number
  email: string
  tenant_id: number | null
  roles: string[]
}

const currentUser = ref<User | null>(null)
const isLoading = ref(false)

export function useAuth() {
  const isAuthenticated = computed(() => currentUser.value !== null)

  async function login() {
    // Redirect to SSO login (Entra ID OIDC via django-allauth)
    window.location.href = '/accounts/openid_connect/login/?process=login'
  }

  async function logout() {
    try {
      currentUser.value = null
      window.location.href = '/accounts/logout/'
    } catch {
      currentUser.value = null
    }
  }

  async function refreshToken(): Promise<boolean> {
    try {
      await apiClient.post('/auth/token/refresh/')
      return true
    } catch {
      currentUser.value = null
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
    login,
    logout,
    refreshToken,
    fetchCurrentUser,
  }
}
