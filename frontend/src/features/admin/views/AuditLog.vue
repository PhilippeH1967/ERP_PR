<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/plugins/axios'

const router = useRouter()

interface SystemHealth {
  active_users: number
  pending_approvals: number
  overdue_invoices: number
}

const health = ref<SystemHealth | null>(null)
const isLoading = ref(true)

async function fetchHealth() {
  isLoading.value = true
  try {
    const resp = await apiClient.get('dashboard/system-health/')
    health.value = resp.data?.data || resp.data
  } catch {
    health.value = null
  } finally {
    isLoading.value = false
  }
}

onMounted(fetchHealth)
</script>

<template>
  <div>
    <div class="page-header">
      <div>
        <button class="btn-back" @click="router.push('/admin')">&larr; Administration</button>
        <h1>Journal d'audit</h1>
      </div>
    </div>

    <!-- System health KPIs -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <span class="kpi-label">Utilisateurs actifs</span>
        <span class="kpi-value">{{ health?.active_users ?? '—' }}</span>
      </div>
      <div class="kpi-card">
        <span class="kpi-label">Approbations en attente</span>
        <span class="kpi-value warning">{{ health?.pending_approvals ?? '—' }}</span>
      </div>
      <div class="kpi-card">
        <span class="kpi-label">Factures en souffrance</span>
        <span class="kpi-value danger">{{ health?.overdue_invoices ?? '—' }}</span>
      </div>
    </div>

    <!-- Audit trail info -->
    <div class="card">
      <div class="card-title">Historique des modifications</div>
      <p class="info-text">
        Toutes les entités financières (factures, paiements, dépenses, feuilles de temps)
        sont suivies automatiquement via django-simple-history.
      </p>
      <p class="info-text">
        Chaque modification enregistre : l'utilisateur, la date, le type de changement,
        et les valeurs avant/après.
      </p>

      <div class="audit-features">
        <div class="audit-feature">
          <span class="feature-icon">&#128203;</span>
          <div>
            <span class="feature-title">Factures</span>
            <span class="feature-desc">Création, soumission, approbation, paiement</span>
          </div>
        </div>
        <div class="audit-feature">
          <span class="feature-icon">&#128336;</span>
          <div>
            <span class="feature-title">Feuilles de temps</span>
            <span class="feature-desc">Saisie, correction, approbation PM</span>
          </div>
        </div>
        <div class="audit-feature">
          <span class="feature-icon">&#129534;</span>
          <div>
            <span class="feature-title">Dépenses</span>
            <span class="feature-desc">Soumission, approbation, validation finance</span>
          </div>
        </div>
        <div class="audit-feature">
          <span class="feature-icon">&#128188;</span>
          <div>
            <span class="feature-title">Projets</span>
            <span class="feature-desc">Avenants, changements de budget, affectations</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Operations log -->
    <div class="card" style="margin-top: 16px;">
      <div class="card-title">Journal des opérations</div>
      <p class="info-text">
        Les opérations en masse (imports, exports) sont journalisées dans la table
        <code>data_ops_operations_log</code>.
      </p>
      <p class="info-text" style="margin-top: 8px;">
        Consultable via <a href="/admin/" target="_blank" style="color: var(--color-primary);">l'admin Django</a>
        ou les futurs endpoints API (MVP-1.5).
      </p>
    </div>
  </div>
</template>

<style scoped>
.page-header { display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 16px; }
.page-header h1 { font-size: 20px; font-weight: 700; color: var(--color-gray-900); margin-top: 2px; }
.btn-back { background: none; border: none; font-size: 12px; color: var(--color-gray-500); cursor: pointer; padding: 0; }
.btn-back:hover { color: var(--color-primary); }

.kpi-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 16px; }
.kpi-card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 16px; }
.kpi-label { display: block; font-size: 11px; color: var(--color-gray-500); text-transform: uppercase; font-weight: 600; letter-spacing: 0.3px; margin-bottom: 4px; }
.kpi-value { font-size: 24px; font-weight: 700; font-family: var(--font-mono); color: var(--color-gray-900); }
.kpi-value.warning { color: var(--color-warning); }
.kpi-value.danger { color: var(--color-danger); }

.card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 20px; }
.card-title { font-size: 14px; font-weight: 600; color: var(--color-gray-800); margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid var(--color-gray-100); }
.info-text { font-size: 13px; color: var(--color-gray-600); line-height: 1.6; }

.audit-features { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-top: 16px; }
.audit-feature { display: flex; align-items: flex-start; gap: 10px; padding: 12px; background: var(--color-gray-50); border-radius: 6px; }
.feature-icon { font-size: 20px; }
.feature-title { display: block; font-size: 13px; font-weight: 600; color: var(--color-gray-800); }
.feature-desc { display: block; font-size: 11px; color: var(--color-gray-500); }
</style>
