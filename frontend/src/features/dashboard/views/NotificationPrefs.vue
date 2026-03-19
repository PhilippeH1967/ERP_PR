<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/plugins/axios'

const router = useRouter()

const prefs = ref({
  email_enabled: true,
  categories: {
    timesheet_reminder: true,
    approval_request: true,
    invoice_status: true,
    expense_status: true,
    project_alert: true,
    system_announcement: true,
  },
})
const saved = ref(false)

async function fetchPrefs() {
  try {
    const resp = await apiClient.get('notification_preferences/')
    const data = resp.data?.data || resp.data
    if (data) {
      prefs.value.email_enabled = data.email_enabled ?? true
      if (data.subscribed_categories?.length) {
        for (const key of Object.keys(prefs.value.categories)) {
          (prefs.value.categories as Record<string, boolean>)[key] = data.subscribed_categories.includes(key)
        }
      }
    }
  } catch { /* use defaults */ }
}

async function save() {
  saved.value = false
  const subscribedCategories = Object.entries(prefs.value.categories)
    .filter(([, v]) => v)
    .map(([k]) => k)
  try {
    await apiClient.put('notification_preferences/', {
      email_enabled: prefs.value.email_enabled,
      subscribed_categories: subscribedCategories,
    })
    saved.value = true
    setTimeout(() => { saved.value = false }, 3000)
  } catch { /* error */ }
}

const categoryLabels: Record<string, string> = {
  timesheet_reminder: 'Rappels feuilles de temps',
  approval_request: 'Demandes d\'approbation',
  invoice_status: 'Changements statut facture',
  expense_status: 'Changements statut dépense',
  project_alert: 'Alertes projet (budget, heures)',
  system_announcement: 'Annonces système',
}

onMounted(fetchPrefs)
</script>

<template>
  <div>
    <div class="page-header">
      <div>
        <button class="btn-back" @click="router.push('/notifications')">&larr; Notifications</button>
        <h1>Préférences de notification</h1>
      </div>
    </div>

    <!-- Email -->
    <div class="card">
      <div class="card-title">Canal de notification</div>
      <label class="toggle-row">
        <input type="checkbox" v-model="prefs.email_enabled" />
        <span>Recevoir les notifications par email</span>
      </label>
    </div>

    <!-- Categories -->
    <div class="card" style="margin-top: 12px;">
      <div class="card-title">Types de notifications</div>
      <div class="categories">
        <label v-for="(_enabled, key) in prefs.categories" :key="key" class="toggle-row">
          <input type="checkbox" v-model="(prefs.categories as Record<string, boolean>)[key as string]" />
          <span>{{ categoryLabels[key as string] || key }}</span>
        </label>
      </div>
    </div>

    <!-- Save -->
    <div class="save-bar">
      <span v-if="saved" class="save-ok">Préférences enregistrées</span>
      <button class="btn-primary" @click="save">Enregistrer</button>
    </div>
  </div>
</template>

<style scoped>
.page-header { display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 16px; }
.page-header h1 { font-size: 20px; font-weight: 700; color: var(--color-gray-900); margin-top: 2px; }
.btn-back { background: none; border: none; font-size: 12px; color: var(--color-gray-500); cursor: pointer; padding: 0; }
.card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 16px; }
.card-title { font-size: 14px; font-weight: 600; color: var(--color-gray-800); margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid var(--color-gray-100); }
.categories { display: flex; flex-direction: column; gap: 6px; }
.toggle-row { display: flex; align-items: center; gap: 10px; font-size: 13px; color: var(--color-gray-700); cursor: pointer; padding: 6px 0; }
.save-bar { display: flex; align-items: center; justify-content: flex-end; gap: 12px; margin-top: 16px; }
.save-ok { font-size: 12px; color: var(--color-success); font-weight: 600; }
</style>
