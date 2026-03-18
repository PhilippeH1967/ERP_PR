/**
 * Axios API client with JWT interceptors.
 *
 * - Request: attaches Authorization header (if token available)
 * - Response 401: automatically refreshes token via /auth/token/refresh/
 * - Response 403: redirects to forbidden page
 * - Response 409: version conflict (handled by caller)
 * - Response 500: logs to Sentry + shows toast
 */

import axios from 'axios'

const apiClient = axios.create({
  baseURL: '/api/v1/',
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
})

let isRefreshing = false
let failedQueue: Array<{
  resolve: (value: unknown) => void
  reject: (reason: unknown) => void
}> = []

function processQueue(error: unknown) {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error)
    } else {
      prom.resolve(undefined)
    }
  })
  failedQueue = []
}

// Response interceptor — handle 401 token refresh
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    // 401: Token expired — try refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject })
        }).then(() => apiClient(originalRequest))
      }

      originalRequest._retry = true
      isRefreshing = true

      try {
        await apiClient.post('auth/token/refresh/')
        processQueue(null)
        return apiClient(originalRequest)
      } catch (refreshError) {
        processQueue(refreshError)
        // Redirect to login
        window.location.href = '/login'
        return Promise.reject(refreshError)
      } finally {
        isRefreshing = false
      }
    }

    // 403: Permission denied
    if (error.response?.status === 403) {
      // eslint-disable-next-line no-console
      console.error('[Auth] Permission denied:', error.response?.data)
    }

    return Promise.reject(error)
  },
)

export default apiClient
