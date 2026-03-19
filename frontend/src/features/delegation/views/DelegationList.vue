<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import apiClient from '@/plugins/axios'

interface Delegation {
  id: number
  delegator: number
  delegator_name: string
  delegate: number
  delegate_name: string
  scope: string
  project_id: number | null
  start_date: string
  end_date: string
  is_active: boolean
}

const delegations = ref<Delegation[]>([])
const isLoading = ref(true)
const showCreate = ref(false)
const error = ref('')
const form = ref({ delegate: '', scope: 'all', project_id: '', start_date: '', end_date: '' })

const today = new Date().toISOString().slice(0, 10)
const activeDelegations = computed(() => delegations.value.filter(d => d.is_active && d.end_date >= today))
const expiredDelegations = computed(() => delegations.value.filter(d => !d.is_active || d.end_date < today))

async function fetch() {
  isLoading.value = true
  try {
    const resp = await apiClient.get('delegations/')
    delegations.value = resp.data?.data || []
  } catch { delegations.value = [] }
  finally { isLoading.value = false }
}

async function create() {
  error.value = ''
  try {
    const data: Record<string, unknown> = {
      delegate: Number(form.value.delegate),
      scope: form.value.scope,
      start_date: form.value.start_date,
      end_date: form.value.end_date,
    }
    if (form.value.scope === 'project' && form.value.project_id) {
      data.project_id = Number(form.value.project_id)
    }
    await apiClient.post('delegations/', data)
    showCreate.value = false
    form.value = { delegate: '', scope: 'all', project_id: '', start_date: '', end_date: '' }
    await fetch()
  } catch (e: unknown) {
    error.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur'
  }
}

async function remove(id: number) {
  if (!confirm('Révoquer cette délégation ?')) return
  await apiClient.delete(`delegations/${id}/`)
  await fetch()
}

onMounted(fetch)
</script>

<template>
  <div>
    <div class="page-header">
      <h1>Délégations</h1>
      <button class="btn-primary" @click="showCreate = !showCreate">+ Nouvelle délégation</button>
    </div>

    <!-- Info -->
    <div class="info-banner">
      Les délégations permettent à un utilisateur d'agir au nom d'un autre
      (approbation de feuilles de temps, validation de dépenses, etc.).
      Toutes les actions effectuées par délégation sont journalisées.
    </div>

    <!-- Create form -->
    <div v-if="showCreate" class="card" style="margin-bottom: 12px;">
      <div class="card-title">Nouvelle délégation</div>
      <div v-if="error" class="alert-error">{{ error }}</div>
      <form @submit.prevent="create">
        <div class="form-row-4">
          <div class="form-group">
            <label>Délégué (user ID)</label>
            <input v-model="form.delegate" type="number" required placeholder="ID utilisateur" />
          </div>
          <div class="form-group">
            <label>Portée</label>
            <select v-model="form.scope">
              <option value="all">Tous les projets</option>
              <option value="project">Projet spécifique</option>
            </select>
          </div>
          <div class="form-group">
            <label>Date début</label>
            <input v-model="form.start_date" type="date" required />
          </div>
          <div class="form-group">
            <label>Date fin</label>
            <input v-model="form.end_date" type="date" required />
          </div>
        </div>
        <div v-if="form.scope === 'project'" class="form-group" style="max-width: 200px;">
          <label>Projet ID</label>
          <input v-model="form.project_id" type="number" placeholder="ID projet" />
        </div>
        <div class="form-actions">
          <button type="button" class="btn-ghost" @click="showCreate = false">Annuler</button>
          <button type="submit" class="btn-primary">Créer</button>
        </div>
      </form>
    </div>

    <div v-if="isLoading" class="loading">Chargement...</div>

    <!-- Active -->
    <template v-if="activeDelegations.length">
      <h2 class="section-title">Actives ({{ activeDelegations.length }})</h2>
      <div class="delegation-grid">
        <div v-for="d in activeDelegations" :key="d.id" class="delegation-card active">
          <div class="delegation-header">
            <div class="delegation-arrow">
              <span class="delegation-user">{{ d.delegator_name }}</span>
              <span class="arrow">→</span>
              <span class="delegation-user highlight">{{ d.delegate_name }}</span>
            </div>
            <button class="btn-action danger" @click="remove(d.id)">Révoquer</button>
          </div>
          <div class="delegation-meta">
            <span class="badge" :class="d.scope === 'all' ? 'badge-blue' : 'badge-amber'">
              {{ d.scope === 'all' ? 'Tous projets' : `Projet #${d.project_id}` }}
            </span>
            <span class="date-range">{{ d.start_date }} → {{ d.end_date }}</span>
          </div>
        </div>
      </div>
    </template>

    <!-- Expired -->
    <template v-if="expiredDelegations.length">
      <h2 class="section-title" style="margin-top: 20px;">Expirées ({{ expiredDelegations.length }})</h2>
      <div class="delegation-grid">
        <div v-for="d in expiredDelegations" :key="d.id" class="delegation-card expired">
          <div class="delegation-header">
            <div class="delegation-arrow">
              <span class="delegation-user">{{ d.delegator_name }}</span>
              <span class="arrow">→</span>
              <span class="delegation-user">{{ d.delegate_name }}</span>
            </div>
          </div>
          <div class="delegation-meta">
            <span class="badge badge-gray">{{ d.scope === 'all' ? 'Tous projets' : `Projet #${d.project_id}` }}</span>
            <span class="date-range">{{ d.start_date }} → {{ d.end_date }}</span>
          </div>
        </div>
      </div>
    </template>

    <!-- Empty -->
    <div v-if="!isLoading && !delegations.length" class="empty-state">
      <p>Aucune délégation active.</p>
      <button class="btn-primary" @click="showCreate = true">Créer une délégation</button>
    </div>
  </div>
</template>

<style scoped>
.page-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }
.page-header h1 { font-size: 20px; font-weight: 700; color: var(--color-gray-900); }
.info-banner { background: #DBEAFE; color: #1D4ED8; padding: 10px 14px; border-radius: 6px; font-size: 12px; line-height: 1.5; margin-bottom: 16px; }
.loading { text-align: center; padding: 40px; color: var(--color-gray-500); font-size: 13px; }
.card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 16px; }
.card-title { font-size: 14px; font-weight: 600; color: var(--color-gray-800); margin-bottom: 12px; }
.alert-error { background: var(--color-danger-light); color: var(--color-danger); padding: 8px; border-radius: 6px; font-size: 12px; margin-bottom: 10px; }
.form-row-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }
.form-group { margin-bottom: 10px; } .form-group label { display: block; font-size: 11px; font-weight: 600; color: var(--color-gray-600); margin-bottom: 4px; }
.form-actions { display: flex; justify-content: flex-end; gap: 6px; }

.section-title { font-size: 13px; font-weight: 600; color: var(--color-gray-500); text-transform: uppercase; margin-bottom: 10px; }
.delegation-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }
.delegation-card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 14px; }
.delegation-card.active { border-left: 3px solid var(--color-primary); }
.delegation-card.expired { opacity: 0.6; }
.delegation-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; }
.delegation-arrow { display: flex; align-items: center; gap: 6px; }
.delegation-user { font-size: 13px; font-weight: 600; color: var(--color-gray-800); }
.delegation-user.highlight { color: var(--color-primary); }
.arrow { color: var(--color-gray-400); font-size: 14px; }
.delegation-meta { display: flex; align-items: center; gap: 8px; }
.date-range { font-size: 11px; color: var(--color-gray-500); }
.badge { display: inline-flex; padding: 1px 8px; border-radius: 10px; font-size: 10px; font-weight: 600; }
.badge-blue { background: #DBEAFE; color: #1D4ED8; } .badge-amber { background: #FEF3C7; color: #92400E; }
.badge-gray { background: var(--color-gray-100); color: var(--color-gray-500); }
.btn-action { background: none; border: none; font-size: 11px; cursor: pointer; color: var(--color-primary); font-weight: 600; }
.btn-action.danger { color: var(--color-danger); }
.empty-state { text-align: center; padding: 40px; color: var(--color-gray-500); }
.empty-state p { margin-bottom: 12px; }
</style>
