/**
 * Axios API client with interceptor stubs.
 * JWT refresh, 401/403/409/500 handling will be implemented in Story 1.3 and 1.6.
 */

import axios from 'axios'

const apiClient = axios.create({
  baseURL: '/api/v1/',
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
})

// Request interceptor — JWT token injection will be added in Story 1.3
apiClient.interceptors.request.use(
  (config) => config,
  (error) => Promise.reject(error),
)

// Response interceptor — error handling will be enhanced in Story 1.6
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // 401: Token refresh — Story 1.3
    // 403: Permission denied redirect — Story 1.4
    // 409: Optimistic lock conflict dialog — Story 1.2
    // 500: Sentry + toast notification — Story 1.6
    return Promise.reject(error)
  },
)

export default apiClient
