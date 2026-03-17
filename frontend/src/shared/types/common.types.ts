/**
 * Common shared types used across the application.
 */

/** Standardized API success response */
export interface ApiResponse<T> {
  data: T
}

/** Standardized API paginated response */
export interface ApiPaginatedResponse<T> {
  data: T[]
  meta: {
    count: number
    next: string | null
    previous: string | null
  }
}

/** Standardized API error response */
export interface ApiErrorResponse {
  error: {
    code: string
    message: string
    details: ApiErrorDetail[]
  }
}

/** API error detail (field-level) */
export interface ApiErrorDetail {
  field?: string
  message: string
}
