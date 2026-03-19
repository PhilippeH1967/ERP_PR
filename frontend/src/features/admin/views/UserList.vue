<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/plugins/axios'

const router = useRouter()

interface UserInfo {
  id: number
  username: string
  email: string
  is_active: boolean
  is_staff: boolean
  date_joined: string
  roles: string[]
}

const users = ref<UserInfo[]>([])
const isLoading = ref(true)
const showCreateForm = ref(false)
const createError = ref('')

const newUser = ref({
  username: '',
  email: '',
  password: '',
  role: 'EMPLOYEE',
})

const roleLabels: Record<string, string> = {
  EMPLOYEE: 'Employé',
  PM: 'Chef de projet',
  PROJECT_DIRECTOR: 'Associé en charge',
  BU_DIRECTOR: 'Dir. d\'unité',
  FINANCE: 'Finance',
  DEPT_ASSISTANT: 'Adj. département',
  PROPOSAL_MANAGER: 'Gest. propositions',
  ADMIN: 'Administrateur',
}

const roleBadgeClass: Record<string, string> = {
  EMPLOYEE: 'badge-blue',
  PM: 'badge-amber',
  FINANCE: 'badge-green',
  ADMIN: 'badge-red',
  PROJECT_DIRECTOR: 'badge-purple',
  BU_DIRECTOR: 'badge-purple',
  DEPT_ASSISTANT: 'badge-gray',
  PROPOSAL_MANAGER: 'badge-gray',
}

async function fetchUsers() {
  isLoading.value = true
  try {
    const resp = await apiClient.get('users/')
    const data = resp.data?.data || resp.data
    users.value = Array.isArray(data) ? data : data?.results || []
  } catch {
    users.value = []
  } finally {
    isLoading.value = false
  }
}

async function createUser() {
  createError.value = ''
  try {
    await apiClient.post('users/', newUser.value)
    showCreateForm.value = false
    newUser.value = { username: '', email: '', password: '', role: 'EMPLOYEE' }
    await fetchUsers()
  } catch (err: unknown) {
    const axiosErr = err as { response?: { data?: { error?: { message?: string } } } }
    createError.value = axiosErr.response?.data?.error?.message || 'Erreur lors de la création'
  }
}

onMounted(fetchUsers)
</script>

<template>
  <div>
    <div class="page-header">
      <div>
        <button class="btn-back" @click="router.push('/admin')">&larr; Administration</button>
        <h1>Utilisateurs & Rôles</h1>
      </div>
      <button class="btn-primary" @click="showCreateForm = !showCreateForm">+ Nouvel utilisateur</button>
    </div>

    <!-- Create form -->
    <div v-if="showCreateForm" class="card" style="margin-bottom: 16px;">
      <div class="card-title">Nouvel utilisateur</div>
      <div v-if="createError" class="alert-error">{{ createError }}</div>
      <form @submit.prevent="createUser" class="create-form">
        <div class="form-row-4">
          <div class="form-group">
            <label>Nom d'utilisateur</label>
            <input v-model="newUser.username" type="text" required />
          </div>
          <div class="form-group">
            <label>Email</label>
            <input v-model="newUser.email" type="email" required />
          </div>
          <div class="form-group">
            <label>Mot de passe</label>
            <input v-model="newUser.password" type="password" required />
          </div>
          <div class="form-group">
            <label>Rôle</label>
            <select v-model="newUser.role">
              <option v-for="(label, key) in roleLabels" :key="key" :value="key">{{ label }}</option>
            </select>
          </div>
        </div>
        <div class="form-actions">
          <button type="button" class="btn-ghost" @click="showCreateForm = false">Annuler</button>
          <button type="submit" class="btn-primary">Créer</button>
        </div>
      </form>
    </div>

    <!-- Loading -->
    <div v-if="isLoading" class="loading">Chargement...</div>

    <!-- User table -->
    <div v-else class="card">
      <table v-if="users.length">
        <thead>
          <tr>
            <th>Utilisateur</th>
            <th>Email</th>
            <th>Rôles</th>
            <th>Statut</th>
            <th>Inscrit le</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td class="user-name">{{ user.username }}</td>
            <td>{{ user.email }}</td>
            <td>
              <span
                v-for="role in user.roles"
                :key="role"
                class="role-badge"
                :class="roleBadgeClass[role] || 'badge-gray'"
              >
                {{ roleLabels[role] || role }}
              </span>
              <span v-if="!user.roles?.length" class="text-muted">Aucun</span>
            </td>
            <td>
              <span :class="user.is_active ? 'status-active' : 'status-inactive'">
                {{ user.is_active ? 'Actif' : 'Inactif' }}
              </span>
            </td>
            <td class="text-muted">{{ user.date_joined?.substring(0, 10) || '—' }}</td>
          </tr>
        </tbody>
      </table>
      <div v-else class="empty">Aucun utilisateur trouvé. L'API utilisateurs n'est peut-être pas encore configurée.</div>
    </div>

    <div class="info-note" style="margin-top: 12px;">
      La gestion avancée des utilisateurs et rôles est aussi accessible via
      <a href="/admin/" target="_blank" style="color: var(--color-primary);">l'admin Django</a>.
    </div>
  </div>
</template>

<style scoped>
.page-header { display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 16px; }
.page-header h1 { font-size: 20px; font-weight: 700; color: var(--color-gray-900); margin-top: 2px; }
.btn-back { background: none; border: none; font-size: 12px; color: var(--color-gray-500); cursor: pointer; padding: 0; }
.btn-back:hover { color: var(--color-primary); }
.btn-primary { padding: 6px 12px; border-radius: 4px; font-size: 12px; font-weight: 600; cursor: pointer; border: none; background: var(--color-primary); color: white; }
.btn-primary:hover { background: var(--color-primary-dark); }
.btn-ghost { padding: 6px 12px; border-radius: 4px; font-size: 12px; font-weight: 500; cursor: pointer; background: transparent; color: var(--color-gray-600); border: 1px solid var(--color-gray-300); }
.loading { text-align: center; padding: 40px; color: var(--color-gray-500); font-size: 13px; }

.card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 16px; }
.card-title { font-size: 14px; font-weight: 600; color: var(--color-gray-800); margin-bottom: 12px; }
.alert-error { background: var(--color-danger-light); color: var(--color-danger); padding: 8px 12px; border-radius: 6px; font-size: 12px; margin-bottom: 12px; }

table { width: 100%; border-collapse: collapse; }
th { background: var(--color-gray-50); padding: 8px 10px; text-align: left; font-size: 10px; font-weight: 600; color: var(--color-gray-500); text-transform: uppercase; letter-spacing: 0.3px; border-bottom: 2px solid var(--color-gray-200); }
td { padding: 8px 10px; border-bottom: 1px solid var(--color-gray-100); font-size: 13px; }
tr:hover { background: var(--color-gray-50); }
.user-name { font-weight: 600; color: var(--color-gray-800); }
.text-muted { color: var(--color-gray-400); font-size: 12px; }

.role-badge { display: inline-flex; padding: 1px 8px; border-radius: 10px; font-size: 10px; font-weight: 600; margin-right: 4px; }
.badge-blue { background: #DBEAFE; color: #1D4ED8; }
.badge-amber { background: #FEF3C7; color: #92400E; }
.badge-green { background: #DCFCE7; color: #15803D; }
.badge-red { background: #FEE2E2; color: #DC2626; }
.badge-purple { background: #EDE9FE; color: #7C3AED; }
.badge-gray { background: #F3F4F6; color: #6B7280; }

.status-active { font-size: 11px; font-weight: 600; color: #15803D; }
.status-inactive { font-size: 11px; font-weight: 600; color: var(--color-gray-400); }

.form-row-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
.form-group { margin-bottom: 12px; }
.form-group label { display: block; font-size: 11px; font-weight: 600; color: var(--color-gray-600); margin-bottom: 4px; }
.form-group input, .form-group select { width: 100%; padding: 6px 10px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 13px; }
.form-actions { display: flex; justify-content: flex-end; gap: 6px; }
.info-note { font-size: 12px; color: var(--color-gray-500); }
.empty { text-align: center; padding: 30px; color: var(--color-gray-400); font-size: 13px; }
</style>
