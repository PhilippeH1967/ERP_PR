<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/plugins/axios'

const router = useRouter()

interface Tenant {
  id: number
  name: string
  slug: string
  is_active: boolean
  sso_only: boolean
}

const tenant = ref<Tenant | null>(null)
const isLoading = ref(true)
const isSaving = ref(false)
const saveMessage = ref('')

const form = ref({
  name: '',
  sso_only: false,
})

async function fetchTenant() {
  isLoading.value = true
  try {
    // Use auth/me to get tenant_id, then fetch via admin
    const meResp = await apiClient.get('auth/me/')
    const tenantId = meResp.data?.data?.tenant_id
    if (tenantId) {
      // For now, display the info we have
      tenant.value = { id: tenantId, name: '', slug: '', is_active: true, sso_only: false }
      form.value.name = tenant.value.name
    }
  } catch {
    // silent
  } finally {
    isLoading.value = false
  }
}

onMounted(fetchTenant)
</script>

<template>
  <div>
    <div class="page-header">
      <div>
        <button class="btn-back" @click="router.push('/admin')">&larr; Administration</button>
        <h1>Organisation</h1>
      </div>
    </div>

    <div class="settings-grid">
      <!-- Tenant info -->
      <div class="card">
        <div class="card-title">Informations du tenant</div>
        <div class="info-row">
          <span class="info-label">ID</span>
          <span class="info-value">{{ tenant?.id || '—' }}</span>
        </div>
        <div class="info-row">
          <span class="info-label">Statut</span>
          <span class="badge-active">Actif</span>
        </div>
      </div>

      <!-- SSO Config -->
      <div class="card">
        <div class="card-title">Authentification</div>
        <div class="info-row">
          <span class="info-label">Mode SSO uniquement</span>
          <span class="info-value">{{ tenant?.sso_only ? 'Oui' : 'Non' }}</span>
        </div>
        <p class="info-note">
          Si activé, seuls les administrateurs peuvent se connecter avec un mot de passe.
          Les autres utilisateurs doivent utiliser le SSO Microsoft Entra ID.
        </p>
        <p class="info-note">
          Configurable via le panneau d'administration Django : <code>/admin/</code>
        </p>
      </div>

      <!-- Entities -->
      <div class="card">
        <div class="card-title">Entités juridiques</div>
        <p class="info-note">
          Les entités juridiques (Provencher Roy Productions, PRAA, etc.)
          sont configurables via le panneau d'administration Django.
        </p>
        <p class="info-note" style="margin-top: 8px;">
          Chaque entité peut avoir ses propres numéros de TPS/TVQ et paramètres de facturation.
        </p>
      </div>

      <!-- BU -->
      <div class="card">
        <div class="card-title">Unités d'affaires</div>
        <p class="info-note">
          Les unités d'affaires (Architecture, Design urbain, etc.)
          structurent l'organisation et permettent le suivi des KPIs par département.
        </p>
        <p class="info-note" style="margin-top: 8px;">
          Importables via la page <a href="/admin/import" style="color: var(--color-primary);">Import</a>
          (template Unités d'affaires).
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-header { display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 16px; }
.page-header h1 { font-size: 20px; font-weight: 700; color: var(--color-gray-900); margin-top: 2px; }
.btn-back { background: none; border: none; font-size: 12px; color: var(--color-gray-500); cursor: pointer; padding: 0; }
.btn-back:hover { color: var(--color-primary); }

.settings-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
.card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 20px; }
.card-title { font-size: 14px; font-weight: 600; color: var(--color-gray-800); margin-bottom: 14px; padding-bottom: 8px; border-bottom: 1px solid var(--color-gray-100); }

.info-row { display: flex; align-items: center; justify-content: space-between; padding: 6px 0; }
.info-label { font-size: 12px; color: var(--color-gray-500); }
.info-value { font-size: 13px; font-weight: 500; color: var(--color-gray-800); }
.info-note { font-size: 12px; color: var(--color-gray-500); line-height: 1.5; }
.badge-active { font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 10px; background: #DCFCE7; color: #15803D; }
</style>
