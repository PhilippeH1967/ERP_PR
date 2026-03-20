<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/plugins/axios'

const router = useRouter()

interface UserInfo { id: number; username: string; email: string; is_active: boolean; is_staff: boolean; date_joined: string; roles: string[] }

const users = ref<UserInfo[]>([])
const isLoading = ref(true)
const showCreateForm = ref(false)
const error = ref('')
const editingUserId = ref<number | null>(null)
const editRole = ref('')

const newUser = ref({ username: '', email: '', password: '', role: 'EMPLOYEE' })

const roleLabels: Record<string, string> = {
  EMPLOYEE: 'Employé', PM: 'Chef de projet', PROJECT_DIRECTOR: 'Associé en charge',
  BU_DIRECTOR: 'Dir. d\'unité', FINANCE: 'Finance', DEPT_ASSISTANT: 'Adj. département',
  PROPOSAL_MANAGER: 'Gest. propositions', ADMIN: 'Administrateur',
}
const roleBadgeClass: Record<string, string> = {
  EMPLOYEE: 'badge-blue', PM: 'badge-amber', FINANCE: 'badge-green', ADMIN: 'badge-red',
  PROJECT_DIRECTOR: 'badge-purple', BU_DIRECTOR: 'badge-purple', DEPT_ASSISTANT: 'badge-gray', PROPOSAL_MANAGER: 'badge-gray',
}

async function fetch() {
  isLoading.value = true
  try { const r = await apiClient.get('users/'); users.value = r.data?.data || [] }
  catch { users.value = [] }
  finally { isLoading.value = false }
}

async function createUser() {
  error.value = ''
  try {
    await apiClient.post('users/create/', newUser.value)
    showCreateForm.value = false; newUser.value = { username: '', email: '', password: '', role: 'EMPLOYEE' }; await fetch()
  } catch (e: unknown) { error.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur' }
}

async function toggleActive(user: UserInfo) {
  await apiClient.patch(`users/${user.id}/`, { is_active: !user.is_active })
  await fetch()
}

function startEditRole(user: UserInfo) {
  editingUserId.value = user.id
  editRole.value = user.roles[0] || 'EMPLOYEE'
}

async function saveRole(userId: number) {
  await apiClient.patch(`users/${userId}/`, { role: editRole.value })
  editingUserId.value = null
  await fetch()
}

// Password change
const changingPasswordId = ref<number | null>(null)
const newPassword = ref('')

async function savePassword(userId: number) {
  if (!newPassword.value || newPassword.value.length < 8) {
    error.value = 'Le mot de passe doit contenir au moins 8 caractères.'
    return
  }
  error.value = ''
  await apiClient.patch(`users/${userId}/`, { password: newPassword.value })
  changingPasswordId.value = null
  newPassword.value = ''
}

// Delete user
async function deleteUser(user: UserInfo) {
  if (!confirm(`Supprimer l'utilisateur "${user.username}" ? Cette action est irréversible.`)) return
  error.value = ''
  try {
    await apiClient.delete(`users/${user.id}/delete/`)
    await fetch()
  } catch (e: unknown) {
    error.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur'
  }
}

onMounted(fetch)
</script>

<template>
  <div>
    <div class="page-header">
      <div><button class="btn-back" @click="router.push('/admin')">&larr; Administration</button><h1>Utilisateurs & Rôles</h1></div>
      <button class="btn-primary" @click="showCreateForm = !showCreateForm">+ Nouvel utilisateur</button>
    </div>

    <div v-if="showCreateForm" class="card create-card">
      <div class="card-title">Nouvel utilisateur</div>
      <div v-if="error" class="alert-error">{{ error }}</div>
      <form @submit.prevent="createUser">
        <div class="create-grid">
          <div class="form-group">
            <label>Nom d'utilisateur *</label>
            <input v-model="newUser.username" type="text" required placeholder="Ex: jean.dupont" class="form-input" />
          </div>
          <div class="form-group">
            <label>Email *</label>
            <input v-model="newUser.email" type="email" required placeholder="jean.dupont@provencher-roy.com" class="form-input" />
          </div>
          <div class="form-group">
            <label>Mot de passe *</label>
            <input v-model="newUser.password" type="password" required placeholder="Minimum 8 caractères" class="form-input" />
          </div>
          <div class="form-group">
            <label>Rôle *</label>
            <select v-model="newUser.role" class="form-input">
              <option v-for="(l, k) in roleLabels" :key="k" :value="k">{{ l }}</option>
            </select>
          </div>
        </div>
        <div class="create-actions">
          <button type="button" class="btn-ghost" @click="showCreateForm=false">Annuler</button>
          <button type="submit" class="btn-primary">Créer l'utilisateur</button>
        </div>
      </form>
    </div>

    <div v-if="isLoading" class="loading">Chargement...</div>

    <div v-else class="card-table">
      <table v-if="users.length">
        <thead><tr><th>Utilisateur</th><th>Email</th><th>Rôle</th><th>Statut</th><th>Inscrit</th><th>Actions</th></tr></thead>
        <tbody>
          <template v-for="user in users" :key="user.id">
            <tr>
              <td class="font-semibold">{{ user.username }}</td>
              <td class="text-muted">{{ user.email }}</td>
              <td>
                <template v-if="editingUserId === user.id">
                  <div class="inline-edit">
                    <select v-model="editRole" class="role-select"><option v-for="(l, k) in roleLabels" :key="k" :value="k">{{ l }}</option></select>
                    <button class="btn-action" @click="saveRole(user.id)">OK</button>
                    <button class="btn-action" @click="editingUserId=null">×</button>
                  </div>
                </template>
                <template v-else>
                  <span v-for="role in user.roles" :key="role" class="role-badge" :class="roleBadgeClass[role] || 'badge-gray'">{{ roleLabels[role] || role }}</span>
                  <span v-if="!user.roles?.length" class="text-muted">Aucun</span>
                </template>
              </td>
              <td><span :class="user.is_active ? 'flag-yes' : 'flag-no'">{{ user.is_active ? 'Actif' : 'Inactif' }}</span></td>
              <td class="text-muted">{{ user.date_joined?.substring(0, 10) }}</td>
              <td class="actions-cell">
                <button class="btn-action" @click="startEditRole(user)">Rôle</button>
                <button class="btn-action" @click="changingPasswordId = changingPasswordId === user.id ? null : user.id">Mdp</button>
                <button class="btn-action" :class="user.is_active ? 'danger' : 'success'" @click="toggleActive(user)">{{ user.is_active ? 'Désactiver' : 'Activer' }}</button>
                <button class="btn-action danger" @click="deleteUser(user)">Supprimer</button>
              </td>
            </tr>
            <tr v-if="changingPasswordId === user.id">
              <td colspan="6" class="password-row">
                <div class="password-form">
                  <span class="password-label">Nouveau mot de passe pour {{ user.username }} :</span>
                  <input v-model="newPassword" type="password" placeholder="Min. 8 caractères" class="password-input" />
                  <button class="btn-primary" @click="savePassword(user.id)">Changer</button>
                  <button class="btn-ghost" @click="changingPasswordId = null; newPassword = ''">Annuler</button>
                </div>
              </td>
            </tr>
          </template>
        </tbody>
      </table>
      <div v-else class="empty">Aucun utilisateur</div>
    </div>
  </div>
</template>

<style scoped>
.page-header { display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 16px; }
.page-header h1 { font-size: 20px; font-weight: 700; color: var(--color-gray-900); margin-top: 2px; }
.btn-back { background: none; border: none; font-size: 12px; color: var(--color-gray-500); cursor: pointer; padding: 0; }
.loading { text-align: center; padding: 40px; color: var(--color-gray-500); font-size: 13px; }
.card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 16px; }
.card-title { font-size: 14px; font-weight: 600; color: var(--color-gray-800); margin-bottom: 12px; }
.card-table { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); overflow: hidden; }
.alert-error { background: var(--color-danger-light); color: var(--color-danger); padding: 8px; border-radius: 6px; font-size: 12px; margin-bottom: 10px; }
.create-card { margin-bottom: 12px; }
.create-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.create-actions { display: flex; justify-content: flex-end; gap: 8px; margin-top: 16px; padding-top: 12px; border-top: 1px solid var(--color-gray-100); }
.form-group { margin-bottom: 4px; }
.form-group label { display: block; font-size: 11px; font-weight: 600; color: var(--color-gray-700); margin-bottom: 5px; }
.form-input { width: 100%; padding: 8px 12px; border: 1px solid var(--color-gray-300); border-radius: 6px; font-size: 13px; font-family: inherit; background: white; }
.form-input:focus { outline: none; border-color: var(--color-primary); box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1); }
.form-input::placeholder { color: var(--color-gray-400); }
.text-muted { color: var(--color-gray-500); font-size: 12px; }
.role-badge { display: inline-flex; padding: 1px 8px; border-radius: 10px; font-size: 10px; font-weight: 600; margin-right: 3px; }
.badge-blue { background: #DBEAFE; color: #1D4ED8; } .badge-amber { background: #FEF3C7; color: #92400E; }
.badge-green { background: #DCFCE7; color: #15803D; } .badge-red { background: #FEE2E2; color: #DC2626; }
.badge-purple { background: #EDE9FE; color: #7C3AED; } .badge-gray { background: #F3F4F6; color: #6B7280; }
.flag-yes { font-size: 11px; font-weight: 600; color: #15803D; } .flag-no { font-size: 11px; font-weight: 600; color: var(--color-danger); }
.actions-cell { text-align: right; white-space: nowrap; }
.btn-action { background: none; border: none; font-size: 11px; cursor: pointer; color: var(--color-primary); padding: 2px 6px; font-weight: 600; }
.btn-action:hover { text-decoration: underline; } .btn-action.danger { color: var(--color-danger); } .btn-action.success { color: var(--color-success); }
.inline-edit { display: inline-flex; align-items: center; gap: 4px; }
.role-select { padding: 2px 6px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 11px; }
.empty { text-align: center; padding: 30px; color: var(--color-gray-400); font-size: 13px; }
.password-row { background: var(--color-gray-50); }
.password-form { display: flex; align-items: center; gap: 8px; padding: 4px 0; }
.password-label { font-size: 12px; color: var(--color-gray-600); white-space: nowrap; }
.password-input { padding: 5px 10px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 12px; width: 200px; }
.password-input:focus { outline: none; border-color: var(--color-primary); }
</style>
