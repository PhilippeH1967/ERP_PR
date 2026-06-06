import apiClient from '@/plugins/axios'
import type { Phase, Project } from '../types/project.types'

const BASE = 'projects'

export const projectApi = {
  list: (params?: Record<string, string>) => apiClient.get(`${BASE}/`, { params }),
  get: (id: number) => apiClient.get<{ data: Project }>(`${BASE}/${id}/`),
  create: (data: Partial<Project>) => apiClient.post(`${BASE}/`, data),
  update: (id: number, data: Partial<Project>, version?: number) =>
    apiClient.patch(`${BASE}/${id}/`, data, {
      headers: version ? { 'If-Match': String(version) } : {},
    }),
  delete: (id: number) => apiClient.delete(`${BASE}/${id}/`),
  createFromTemplate: (templateId: number, projectData: Record<string, unknown>) =>
    apiClient.post(`${BASE}/create_from_template/`, {
      template_id: templateId,
      project: projectData,
    }),
  dashboard: (id: number) => apiClient.get(`${BASE}/${id}/dashboard/`),
  teamStats: (id: number) => apiClient.get(`${BASE}/${id}/team_stats/`),

  // Team membership (allows time entry without a planning allocation)
  listMembers: (id: number) => apiClient.get(`${BASE}/${id}/members/`),
  addMember: (id: number, userId: number) =>
    apiClient.post(`${BASE}/${id}/members/`, { user_id: userId }),
  removeMember: (id: number, userId: number) =>
    apiClient.delete(`${BASE}/${id}/members/${userId}/`),

  // Templates
  listTemplates: () => apiClient.get('project_templates/'),

  // Phases
  listPhases: (projectId: number) => apiClient.get(`${BASE}/${projectId}/phases/`),
  createPhase: (projectId: number, data: Partial<Phase>) =>
    apiClient.post(`${BASE}/${projectId}/phases/`, data),
  updatePhase: (projectId: number, phaseId: number, data: Partial<Phase>) =>
    apiClient.patch(`${BASE}/${projectId}/phases/${phaseId}/`, data),
  deletePhase: (projectId: number, phaseId: number) =>
    apiClient.delete(`${BASE}/${projectId}/phases/${phaseId}/`),

  // Tasks
  listTasks: (projectId: number) => apiClient.get(`${BASE}/${projectId}/tasks/`),
  taskSuggestions: (projectId: number) => apiClient.get(`${BASE}/${projectId}/task_suggestions/`),
  createTask: (projectId: number, data: Record<string, unknown>) =>
    apiClient.post(`${BASE}/${projectId}/tasks/`, { project: projectId, ...data }),
  updateTask: (projectId: number, taskId: number, data: Record<string, unknown>) => apiClient.patch(`${BASE}/${projectId}/tasks/${taskId}/`, data),
  deleteTask: (projectId: number, taskId: number) => apiClient.delete(`${BASE}/${projectId}/tasks/${taskId}/`),

  // Amendments
  listAmendments: (projectId: number) => apiClient.get(`${BASE}/${projectId}/amendments/`),
  createAmendment: (projectId: number, data: Record<string, unknown>) =>
    apiClient.post(`${BASE}/${projectId}/amendments/`, data),
  updateAmendment: (projectId: number, amendmentId: number, data: Record<string, unknown>) =>
    apiClient.patch(`${BASE}/${projectId}/amendments/${amendmentId}/`, data),
  deleteAmendment: (projectId: number, amendmentId: number) =>
    apiClient.delete(`${BASE}/${projectId}/amendments/${amendmentId}/`),
  submitAmendment: (projectId: number, amendmentId: number) =>
    apiClient.post(`${BASE}/${projectId}/amendments/${amendmentId}/submit/`),
  approveAmendment: (projectId: number, amendmentId: number) =>
    apiClient.post(`${BASE}/${projectId}/amendments/${amendmentId}/approve/`),
  rejectAmendment: (projectId: number, amendmentId: number, reason: string) =>
    apiClient.post(`${BASE}/${projectId}/amendments/${amendmentId}/reject/`, { reason }),
  amendmentScope: (projectId: number, amendmentId: number) =>
    apiClient.get(`${BASE}/${projectId}/amendments/${amendmentId}/scope/`),

  // Budget summary (original + current contract value + approved amendments breakdown)
  budgetSummary: (projectId: number) =>
    apiClient.get(`${BASE}/${projectId}/budget-summary/`),
}
