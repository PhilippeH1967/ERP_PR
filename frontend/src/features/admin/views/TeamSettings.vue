<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/plugins/axios'

const router = useRouter()

interface UserLite { id: number; username: string; first_name?: string; last_name?: string }
interface Team {
  id: number
  name: string
  members: number[]
  member_details: { id: number; username: string; name: string }[]
  is_active: boolean
}

const teams = ref<Team[]>([])
const allUsers = ref<UserLite[]>([])
const isLoading = ref(true)

function userLabel(u: UserLite): string {
  return `${u.first_name || ''} ${u.last_name || ''}`.trim() || u.username
}

async function fetchAll() {
  isLoading.value = true
  try {
    const [tr, ur] = await Promise.all([
      apiClient.get('teams/'),
      apiClient.get('users/search/'),
    ])
    const td = tr.data?.data || tr.data
    const ud = ur.data?.data || ur.data
    teams.value = Array.isArray(td) ? td : td?.results || []
    allUsers.value = Array.isArray(ud) ? ud : ud?.results || []
  } catch {
    teams.value = []
    allUsers.value = []
  } finally {
    isLoading.value = false
  }
}

// --- Form ---
const showForm = ref(false)
const editingId = ref<number | null>(null)
const saveError = ref('')
const formName = ref('')
const formActive = ref(true)
const memberIds = ref<Set<number>>(new Set())
const memberSearch = ref('')

const filteredUsers = computed(() => {
  const q = memberSearch.value.trim().toLowerCase()
  if (!q) return allUsers.value
  return allUsers.value.filter(
    (u) => userLabel(u).toLowerCase().includes(q) || u.username.toLowerCase().includes(q),
  )
})
const selectedCount = computed(() => memberIds.value.size)

function openCreate() {
  editingId.value = null
  saveError.value = ''
  formName.value = ''
  formActive.value = true
  memberIds.value = new Set()
  memberSearch.value = ''
  showForm.value = true
}

function openEdit(t: Team) {
  editingId.value = t.id
  saveError.value = ''
  formName.value = t.name
  formActive.value = t.is_active
  memberIds.value = new Set(t.members)
  memberSearch.value = ''
  showForm.value = true
}

function toggleMember(id: number) {
  const s = new Set(memberIds.value)
  if (s.has(id)) s.delete(id)
  else s.add(id)
  memberIds.value = s
}

async function save() {
  saveError.value = ''
  if (!formName.value.trim()) { saveError.value = "Le nom de l'équipe est obligatoire."; return }
  const payload = { name: formName.value.trim(), is_active: formActive.value, members: [...memberIds.value] }
  try {
    if (editingId.value) await apiClient.patch(`teams/${editingId.value}/`, payload)
    else await apiClient.post('teams/', payload)
    showForm.value = false
    editingId.value = null
    await fetchAll()
  } catch (e: unknown) {
    const d = (e as { response?: { data?: Record<string, unknown> } }).response?.data
    const first = d ? Object.values(d)[0] : null
    saveError.value = Array.isArray(first) ? String(first[0]) : (typeof first === 'string' ? first : 'Erreur')
  }
}

const confirmDeleteId = ref<number | null>(null)
async function deleteTeam(id: number) {
  confirmDeleteId.value = null
  teams.value = teams.value.filter((t) => t.id !== id)
  try { await apiClient.delete(`teams/${id}/`) } catch { /* ok */ }
}

onMounted(fetchAll)
</script>

<template>
  <div>
    <div class="page-header">
      <div>
        <button class="btn-back" @click="router.push('/admin')">&larr; Administration</button>
        <h1>Équipes</h1>
      </div>
    </div>

    <p class="hint">
      Équipes réutilisables (groupes d'employés). On peut affecter une équipe <strong>en entier</strong>
      sur un projet. Création / modification réservées à <strong>Finance, Paie et Admin</strong>.
    </p>

    <div class="actions-bar">
      <span class="count">{{ teams.length }} équipe{{ teams.length > 1 ? 's' : '' }}</span>
      <button class="btn-primary" data-team-add @click="openCreate">+ Nouvelle équipe</button>
    </div>

    <div v-if="isLoading" class="loading">Chargement…</div>
    <div v-else class="card">
      <table v-if="teams.length">
        <thead>
          <tr><th>Nom</th><th>Membres</th><th style="width:70px;">Active</th><th></th></tr>
        </thead>
        <tbody>
          <tr v-for="t in teams" :key="t.id" :class="{ 'row-inactive': !t.is_active }" data-team-row>
            <td class="name-cell">{{ t.name }}</td>
            <td class="members-cell">
              <span v-if="!t.member_details.length" class="muted">—</span>
              <span v-for="m in t.member_details" v-else :key="m.id" class="member-chip">{{ m.name }}</span>
            </td>
            <td><span :class="t.is_active ? 'flag-yes' : 'flag-no'">{{ t.is_active ? 'Oui' : 'Non' }}</span></td>
            <td class="actions-cell">
              <button class="btn-icon" data-team-edit @click="openEdit(t)">Modifier</button>
              <template v-if="confirmDeleteId === t.id">
                <button class="btn-icon btn-icon-danger" @click="deleteTeam(t.id)">Confirmer</button>
                <button class="btn-icon" @click="confirmDeleteId = null">Annuler</button>
              </template>
              <button v-else class="btn-icon btn-icon-danger" @click="confirmDeleteId = t.id">Supprimer</button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="empty">Aucune équipe. Cliquez « + Nouvelle équipe » pour démarrer.</div>
    </div>

    <div v-if="showForm" class="modal-overlay" @click.self="showForm = false">
      <div class="modal">
        <div class="modal-header">
          <h2>{{ editingId ? "Modifier l'équipe" : 'Nouvelle équipe' }}</h2>
          <button class="modal-close" @click="showForm = false">&times;</button>
        </div>
        <div class="modal-body">
          <div v-if="saveError" class="alert-error" style="margin-bottom:10px;">{{ saveError }}</div>
          <div class="form-group">
            <label>Nom de l'équipe *</label>
            <input v-model="formName" type="text" data-team-name placeholder="Ex: Studio A, Équipe BIM" />
          </div>
          <div class="form-group">
            <label>Membres <span class="count">({{ selectedCount }})</span></label>
            <input v-model="memberSearch" type="text" class="member-search" placeholder="Rechercher un employé par nom…" data-team-member-search />
            <div class="member-picker">
              <label v-for="u in filteredUsers" :key="u.id" class="member-opt" data-team-member-opt>
                <input type="checkbox" :checked="memberIds.has(u.id)" @change="toggleMember(u.id)" />
                <span>{{ userLabel(u) }}</span>
              </label>
              <div v-if="!filteredUsers.length" class="member-empty">Aucun employé trouvé</div>
            </div>
          </div>
          <label class="checkbox-label"><input type="checkbox" v-model="formActive" /> Active</label>
          <div class="form-actions">
            <button type="button" class="btn-ghost" @click="showForm = false">Annuler</button>
            <button type="button" class="btn-primary" data-team-save @click="save">{{ editingId ? 'Enregistrer' : 'Créer' }}</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-header { display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 16px; }
.page-header h1 { font-size: 20px; font-weight: 700; color: var(--color-gray-900); margin-top: 2px; }
.btn-back { background: none; border: none; font-size: 12px; color: var(--color-gray-500); cursor: pointer; padding: 0; }
.btn-back:hover { color: var(--color-primary); }
.hint { font-size: 12px; color: var(--color-gray-600); margin: 0 0 14px; max-width: 80ch; }
.actions-bar { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
.count { font-size: 12px; color: var(--color-gray-500); }
.loading { text-align: center; padding: 40px; color: var(--color-gray-500); font-size: 13px; }
.card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); overflow: hidden; }
table { width: 100%; border-collapse: collapse; }
th { background: var(--color-gray-50); padding: 7px 10px; text-align: left; font-size: 10px; font-weight: 600; color: var(--color-gray-500); text-transform: uppercase; border-bottom: 2px solid var(--color-gray-200); }
td { padding: 8px 10px; border-bottom: 1px solid var(--color-gray-100); font-size: 13px; vertical-align: top; }
.row-inactive td { opacity: 0.55; }
.name-cell { font-weight: 600; color: var(--color-gray-800); }
.members-cell { display: flex; flex-wrap: wrap; gap: 4px; }
.member-chip { font-size: 11px; background: #EFF6FF; color: var(--color-primary); border-radius: 10px; padding: 1px 8px; }
.muted { color: var(--color-gray-400); }
.flag-yes { font-size: 11px; font-weight: 600; color: #15803D; }
.flag-no { font-size: 11px; color: var(--color-gray-400); }
.actions-cell { text-align: right; white-space: nowrap; }
.btn-primary { padding: 6px 12px; border-radius: 4px; font-size: 12px; font-weight: 600; cursor: pointer; border: none; background: var(--color-primary); color: white; }
.btn-ghost { padding: 6px 12px; border-radius: 4px; font-size: 12px; cursor: pointer; background: transparent; color: var(--color-gray-600); border: 1px solid var(--color-gray-300); }
.btn-icon { background: none; border: none; font-size: 11px; cursor: pointer; color: var(--color-primary); padding: 2px 6px; }
.btn-icon:hover { text-decoration: underline; }
.btn-icon-danger { color: var(--color-danger); }
.empty { text-align: center; padding: 30px; color: var(--color-gray-400); font-size: 13px; }
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.3); z-index: 8000; display: flex; align-items: flex-start; justify-content: center; padding-top: 70px; }
.modal { background: white; border-radius: 8px; box-shadow: 0 10px 15px rgba(0,0,0,0.1); width: 100%; max-width: 480px; }
.modal-header { padding: 14px 20px; border-bottom: 1px solid var(--color-gray-200); display: flex; align-items: center; justify-content: space-between; }
.modal-header h2 { font-size: 15px; font-weight: 600; color: var(--color-gray-800); }
.modal-close { background: none; border: none; font-size: 22px; cursor: pointer; color: var(--color-gray-400); }
.modal-body { padding: 20px; }
.form-group { margin-bottom: 14px; }
.form-group label { display: block; font-size: 11px; font-weight: 600; color: var(--color-gray-600); margin-bottom: 4px; }
.form-group input[type=text] { width: 100%; padding: 6px 10px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 13px; box-sizing: border-box; }
.member-search { margin-bottom: 6px; }
.member-picker { max-height: 200px; overflow-y: auto; border: 1px solid var(--color-gray-200); border-radius: 4px; padding: 4px; }
.member-opt { display: flex; align-items: center; gap: 8px; padding: 4px 6px; font-size: 12px; color: var(--color-gray-700); cursor: pointer; border-radius: 4px; }
.member-opt:hover { background: var(--color-gray-50); }
.member-empty { padding: 8px; font-size: 12px; color: var(--color-gray-400); }
.checkbox-label { display: flex; align-items: center; gap: 6px; font-size: 13px; color: var(--color-gray-700); cursor: pointer; }
.form-actions { display: flex; justify-content: flex-end; gap: 6px; margin-top: 16px; padding-top: 12px; border-top: 1px solid var(--color-gray-200); }
.alert-error { background: #fde8e4; color: var(--color-danger); padding: 8px 12px; border-radius: 6px; font-size: 12px; }
</style>
