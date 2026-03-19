import apiClient from '@/plugins/axios'
import type { Phase, Project, WBSElement } from '../types/project.types'

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

  // WBS
  listWBS: (projectId: number) => apiClient.get(`${BASE}/${projectId}/wbs/`),
  createWBSElement: (projectId: number, data: Partial<WBSElement>) =>
    apiClient.post(`${BASE}/${projectId}/wbs/`, data),
  deleteWBSElement: (projectId: number, wbsId: number) =>
    apiClient.delete(`${BASE}/${projectId}/wbs/${wbsId}/`),

  // Amendments
  listAmendments: (projectId: number) => apiClient.get(`${BASE}/${projectId}/amendments/`),
  createAmendment: (projectId: number, data: Record<string, unknown>) =>
    apiClient.post(`${BASE}/${projectId}/amendments/`, data),
  updateAmendment: (projectId: number, amendmentId: number, data: Record<string, unknown>) =>
    apiClient.patch(`${BASE}/${projectId}/amendments/${amendmentId}/`, data),
  deleteAmendment: (projectId: number, amendmentId: number) =>
    apiClient.delete(`${BASE}/${projectId}/amendments/${amendmentId}/`),

  // Assignments
  listAssignments: (projectId: number) => apiClient.get(`${BASE}/${projectId}/assignments/`),
  createAssignment: (projectId: number, data: Record<string, unknown>) =>
    apiClient.post(`${BASE}/${projectId}/assignments/`, data),
  updateAssignment: (projectId: number, assignmentId: number, data: Record<string, unknown>) =>
    apiClient.patch(`${BASE}/${projectId}/assignments/${assignmentId}/`, data),
  deleteAssignment: (projectId: number, assignmentId: number) =>
    apiClient.delete(`${BASE}/${projectId}/assignments/${assignmentId}/`),
}
