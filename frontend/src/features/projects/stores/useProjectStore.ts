import { defineStore } from 'pinia'
import { ref } from 'vue'
import { projectApi } from '../api/projectApi'
import type { Project, ProjectTemplate } from '../types/project.types'

export const useProjectStore = defineStore('projects', () => {
  const projects = ref<Project[]>([])
  const currentProject = ref<Project | null>(null)
  const templates = ref<ProjectTemplate[]>([])
  const isLoading = ref(false)

  async function fetchProjects(params?: Record<string, string>) {
    isLoading.value = true
    try {
      const response = await projectApi.list(params)
      projects.value = response.data?.data || response.data
    } finally {
      isLoading.value = false
    }
  }

  async function fetchProject(id: number) {
    isLoading.value = true
    try {
      const response = await projectApi.get(id)
      currentProject.value = response.data?.data || response.data
    } finally {
      isLoading.value = false
    }
  }

  async function fetchTemplates() {
    const response = await projectApi.listTemplates()
    templates.value = response.data?.data || response.data
  }

  async function createFromTemplate(templateId: number, data: Record<string, unknown>) {
    const response = await projectApi.createFromTemplate(templateId, data)
    return response.data?.data || response.data
  }

  async function createProject(data: Partial<Project>) {
    const response = await projectApi.create(data)
    return response.data?.data || response.data
  }

  return {
    projects,
    currentProject,
    templates,
    isLoading,
    fetchProjects,
    fetchProject,
    fetchTemplates,
    createFromTemplate,
    createProject,
  }
})
