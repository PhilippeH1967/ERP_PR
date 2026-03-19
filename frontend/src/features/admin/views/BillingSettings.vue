<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/plugins/axios'

const router = useRouter()

interface InvoiceTemplate {
  id: number
  name: string
  description: string
  is_active: boolean
  template_config: Record<string, unknown>
}

interface DunningLevel {
  id: number
  level: number
  days_overdue: number
  email_template: string
}

const invoiceTemplates = ref<InvoiceTemplate[]>([])
const dunningLevels = ref<DunningLevel[]>([])
const isLoading = ref(true)

async function fetchData() {
  isLoading.value = true
  try {
    const [tmplResp, dunningResp] = await Promise.allSettled([
      apiClient.get('invoice_templates/'),
      apiClient.get('dunning_levels/'),
    ])
    if (tmplResp.status === 'fulfilled') {
      const d = tmplResp.value.data?.data || tmplResp.value.data
      invoiceTemplates.value = Array.isArray(d) ? d : d?.results || []
    }
    if (dunningResp.status === 'fulfilled') {
      const d = dunningResp.value.data?.data || dunningResp.value.data
      dunningLevels.value = Array.isArray(d) ? d : d?.results || []
    }
  } finally {
    isLoading.value = false
  }
}

onMounted(fetchData)
</script>

<template>
  <div>
    <div class="page-header">
      <div>
        <button class="btn-back" @click="router.push('/admin')">&larr; Administration</button>
        <h1>Paramètres de facturation</h1>
      </div>
    </div>

    <div v-if="isLoading" class="loading">Chargement...</div>

    <template v-else>
      <!-- Invoice templates -->
      <div class="card">
        <div class="card-header">
          <span class="card-title">Templates de facture</span>
          <span class="count-badge">{{ invoiceTemplates.length }}</span>
        </div>
        <table v-if="invoiceTemplates.length">
          <thead>
            <tr>
              <th>Nom</th>
              <th>Description</th>
              <th>Sections</th>
              <th>Statut</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="tmpl in invoiceTemplates" :key="tmpl.id">
              <td class="name-cell">{{ tmpl.name }}</td>
              <td>{{ tmpl.description }}</td>
              <td>
                <span
                  v-for="section in (tmpl.template_config?.sections as string[]) || []"
                  :key="section"
                  class="section-tag"
                >
                  {{ section }}
                </span>
              </td>
              <td>
                <span :class="tmpl.is_active ? 'status-active' : 'status-inactive'">
                  {{ tmpl.is_active ? 'Actif' : 'Inactif' }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
        <div v-else class="empty">Aucun template de facture.</div>
      </div>

      <!-- Dunning levels -->
      <div class="card" style="margin-top: 16px;">
        <div class="card-header">
          <span class="card-title">Niveaux de relance</span>
          <span class="count-badge">{{ dunningLevels.length }}</span>
        </div>
        <table v-if="dunningLevels.length">
          <thead>
            <tr>
              <th>Niveau</th>
              <th>Délai (jours)</th>
              <th>Template email</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="dl in dunningLevels" :key="dl.id">
              <td class="name-cell">Niveau {{ dl.level }}</td>
              <td>{{ dl.days_overdue }} jours</td>
              <td class="template-preview">{{ dl.email_template?.substring(0, 80) }}...</td>
            </tr>
          </tbody>
        </table>
        <div v-else class="empty">Aucun niveau de relance configuré.</div>
      </div>

      <!-- Tax info -->
      <div class="card" style="margin-top: 16px;">
        <div class="card-title">Taxes</div>
        <div class="tax-grid">
          <div class="tax-item">
            <span class="tax-label">TPS</span>
            <span class="tax-value">5.0%</span>
          </div>
          <div class="tax-item">
            <span class="tax-label">TVQ</span>
            <span class="tax-value">9.975%</span>
          </div>
        </div>
        <p class="info-note" style="margin-top: 10px;">
          Les taux de taxes sont configurables par entité juridique via l'admin Django.
        </p>
      </div>
    </template>
  </div>
</template>

<style scoped>
.page-header { display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 16px; }
.page-header h1 { font-size: 20px; font-weight: 700; color: var(--color-gray-900); margin-top: 2px; }
.btn-back { background: none; border: none; font-size: 12px; color: var(--color-gray-500); cursor: pointer; padding: 0; }
.btn-back:hover { color: var(--color-primary); }
.loading { text-align: center; padding: 40px; color: var(--color-gray-500); font-size: 13px; }

.card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 16px; }
.card-header { display: flex; align-items: center; gap: 8px; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid var(--color-gray-100); }
.card-title { font-size: 14px; font-weight: 600; color: var(--color-gray-800); }
.count-badge { font-size: 10px; font-weight: 700; padding: 1px 8px; border-radius: 10px; background: var(--color-gray-100); color: var(--color-gray-500); }

table { width: 100%; border-collapse: collapse; }
th { background: var(--color-gray-50); padding: 7px 10px; text-align: left; font-size: 10px; font-weight: 600; color: var(--color-gray-500); text-transform: uppercase; letter-spacing: 0.3px; border-bottom: 2px solid var(--color-gray-200); }
td { padding: 8px 10px; border-bottom: 1px solid var(--color-gray-100); font-size: 13px; }
tr:hover { background: var(--color-gray-50); }
.name-cell { font-weight: 600; color: var(--color-gray-800); }
.template-preview { font-size: 12px; color: var(--color-gray-500); max-width: 300px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

.section-tag { display: inline-flex; padding: 1px 7px; border-radius: 4px; font-size: 10px; font-weight: 600; background: var(--color-gray-100); color: var(--color-gray-600); margin-right: 3px; }
.status-active { font-size: 11px; font-weight: 600; color: #15803D; }
.status-inactive { font-size: 11px; font-weight: 600; color: var(--color-gray-400); }

.tax-grid { display: flex; gap: 24px; }
.tax-item { display: flex; flex-direction: column; }
.tax-label { font-size: 11px; font-weight: 600; color: var(--color-gray-500); text-transform: uppercase; }
.tax-value { font-size: 20px; font-weight: 700; font-family: var(--font-mono); color: var(--color-gray-800); }

.info-note { font-size: 12px; color: var(--color-gray-500); }
.empty { text-align: center; padding: 24px; color: var(--color-gray-400); font-size: 13px; }
</style>
