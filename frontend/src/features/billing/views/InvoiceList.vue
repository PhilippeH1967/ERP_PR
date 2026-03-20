<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useLocale } from '@/shared/composables/useLocale'
import { useBillingStore } from '../stores/useBillingStore'
import { billingApi } from '../api/billingApi'

const store = useBillingStore()
const router = useRouter()
const { fmt } = useLocale()

const showCreate = ref(false)
const createForm = ref({ project: '', client: '', invoice_number: '' })
const createError = ref('')

// Auto-fill client when project changes
async function onProjectChange() {
  if (!createForm.value.project) return
  try {
    const resp = await billingApi.getInvoice  // unused, use apiClient
    const { default: apiClient } = await import('@/plugins/axios')
    const projResp = await apiClient.get(`projects/${createForm.value.project}/`)
    const proj = projResp.data?.data || projResp.data
    if (proj?.client) createForm.value.client = String(proj.client)
  } catch { /* silent */ }
  // Auto-generate invoice number
  createForm.value.invoice_number = `PROV-${Date.now().toString().slice(-6)}`
}

const statusColors: Record<string, string> = {
  DRAFT: 'badge-gray',
  SUBMITTED: 'badge-blue',
  APPROVED: 'badge-green',
  SENT: 'badge-amber',
  PAID: 'badge-green-solid',
}

const statusLabels: Record<string, string> = {
  DRAFT: 'Brouillon',
  SUBMITTED: 'Soumise',
  APPROVED: 'Approuvée',
  SENT: 'Envoyée',
  PAID: 'Payée',
}

async function createInvoice() {
  createError.value = ''
  try {
    const resp = await billingApi.createInvoice({
      project: Number(createForm.value.project),
      client: Number(createForm.value.client),
      invoice_number: createForm.value.invoice_number,
    })
    const data = resp.data?.data || resp.data
    showCreate.value = false
    createForm.value = { project: '', client: '', invoice_number: '' }
    router.push(`/billing/${data.id}`)
  } catch (err: unknown) {
    const e = err as { response?: { data?: { error?: { message?: string } } } }
    createError.value = e.response?.data?.error?.message || 'Erreur lors de la création'
  }
}

onMounted(() => store.fetchInvoices())
</script>

<template>
  <div>
    <div class="page-header">
      <h1>Facturation</h1>
      <button class="btn-primary" @click="showCreate = !showCreate">+ Nouvelle facture</button>
    </div>

    <!-- Create form -->
    <div v-if="showCreate" class="card" style="margin-bottom: 12px;">
      <div class="card-title">Nouvelle facture</div>
      <div v-if="createError" class="alert-error">{{ createError }}</div>
      <form @submit.prevent="createInvoice" class="create-form">
        <div class="form-row-3">
          <div class="form-group">
            <label>Projet ID *</label>
            <input v-model="createForm.project" type="number" required placeholder="Ex: 1" @change="onProjectChange" />
          </div>
          <div class="form-group">
            <label>Client ID *</label>
            <input v-model="createForm.client" type="number" required placeholder="Auto-rempli" />
          </div>
          <div class="form-group">
            <label>No facture *</label>
            <input v-model="createForm.invoice_number" type="text" required placeholder="PROV-XXXXXX" />
          </div>
        </div>
        <div class="form-actions">
          <button type="button" class="btn-ghost" @click="showCreate = false">Annuler</button>
          <button type="submit" class="btn-primary">Créer</button>
        </div>
      </form>
    </div>

    <!-- Table -->
    <div class="card-table">
      <table>
        <thead>
          <tr>
            <th>No facture</th>
            <th>Projet</th>
            <th>Client</th>
            <th class="text-right">Montant</th>
            <th>Statut</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="invoice in store.invoices"
            :key="invoice.id"
            class="row-link"
            @click="router.push(`/billing/${invoice.id}`)"
          >
            <td class="font-mono font-medium">{{ invoice.invoice_number }}</td>
            <td>{{ invoice.project_code }}</td>
            <td class="text-muted">{{ invoice.client_name }}</td>
            <td class="text-right font-mono">{{ fmt.currency(invoice.total_amount) }}</td>
            <td>
              <span class="badge" :class="statusColors[invoice.status]">
                {{ statusLabels[invoice.status] || invoice.status }}
              </span>
            </td>
            <td class="text-muted">{{ fmt.date(invoice.date_created) }}</td>
          </tr>
          <tr v-if="!store.invoices?.length">
            <td colspan="6" class="empty">Aucune facture</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.page-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }
.page-header h1 { font-size: 20px; font-weight: 700; color: var(--color-gray-900); }
.card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 16px; }
.card-title { font-size: 14px; font-weight: 600; color: var(--color-gray-800); margin-bottom: 12px; }
.card-table { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); overflow: hidden; }
.alert-error { background: var(--color-danger-light); color: var(--color-danger); padding: 8px 12px; border-radius: 6px; font-size: 12px; margin-bottom: 12px; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.form-row-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; }
.form-group { margin-bottom: 12px; }
.form-group label { display: block; font-size: 11px; font-weight: 600; color: var(--color-gray-600); margin-bottom: 4px; }
.form-actions { display: flex; justify-content: flex-end; gap: 6px; }
.row-link { cursor: pointer; }
.row-link:hover { background: var(--color-gray-50); }
.text-right { text-align: right; }
.text-muted { color: var(--color-gray-500); }
.empty { text-align: center; padding: 30px; color: var(--color-gray-400); }

.badge { display: inline-flex; padding: 1px 8px; border-radius: 10px; font-size: 10px; font-weight: 600; }
.badge-gray { background: var(--color-gray-100); color: var(--color-gray-500); }
.badge-blue { background: #DBEAFE; color: #1D4ED8; }
.badge-green { background: #DCFCE7; color: #15803D; }
.badge-amber { background: #FEF3C7; color: #92400E; }
.badge-green-solid { background: #15803D; color: white; }
</style>
