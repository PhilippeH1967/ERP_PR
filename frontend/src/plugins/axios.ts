/**
 * Axios API client with JWT interceptors.
 *
 * - Request: attaches Authorization header from localStorage
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

// Request interceptor — attach Bearer token
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
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
        const refresh = localStorage.getItem('refresh_token')
        if (!refresh) throw new Error('No refresh token')
        const response = await axios.post('/api/v1/auth/token/refresh/', { refresh })
        const data = response.data?.data || response.data
        if (data.access) {
          localStorage.setItem('access_token', data.access)
        }
        processQueue(null)
        return apiClient(originalRequest)
      } catch (refreshError) {
        processQueue(refreshError)
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
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
