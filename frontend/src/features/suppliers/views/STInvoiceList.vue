<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useLocale } from '@/shared/composables/useLocale'
import { supplierApi } from '../api/supplierApi'

const { fmt } = useLocale()

interface STInvoice {
  id: number; supplier: number; supplier_name: string; project: number; project_code: string
  invoice_number: string; invoice_date: string; amount: string; status: string
}

const invoices = ref<STInvoice[]>([])
const showCreate = ref(false)
const filter = ref('all')
const form = ref({ supplier: '', project: '', invoice_number: '', invoice_date: '', amount: '' })
const error = ref('')

const statusLabels: Record<string, string> = { received: 'Reçue', authorized: 'Autorisée', paid: 'Payée' }
const statusColors: Record<string, string> = { received: 'badge-blue', authorized: 'badge-amber', paid: 'badge-green-solid' }

async function fetch() {
  try {
    const params: Record<string, string> = {}
    if (filter.value !== 'all') params.status = filter.value
    const resp = await supplierApi.listSTInvoices(params)
    const data = resp.data?.data || resp.data
    invoices.value = Array.isArray(data) ? data : data?.results || []
  } catch { invoices.value = [] }
}

async function create() {
  error.value = ''
  try {
    await supplierApi.createSTInvoice({
      supplier: Number(form.value.supplier), project: Number(form.value.project),
      invoice_number: form.value.invoice_number, invoice_date: form.value.invoice_date,
      amount: form.value.amount,
    })
    showCreate.value = false
    form.value = { supplier: '', project: '', invoice_number: '', invoice_date: '', amount: '' }
    await fetch()
  } catch (e: unknown) {
    error.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur'
  }
}

async function authorize(id: number) {
  try { await supplierApi.authorizeSTInvoice(id); await fetch() }
  catch (e: unknown) { error.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur' }
}

async function markPaid(id: number) {
  try { await supplierApi.markSTInvoicePaid(id); await fetch() }
  catch (e: unknown) { error.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur' }
}

async function remove(id: number) {
  if (!confirm('Supprimer cette facture ST ?')) return
  await supplierApi.deleteSTInvoice(id); await fetch()
}

onMounted(fetch)
</script>

<template>
  <div>
    <div class="page-header">
      <h1>Factures sous-traitants</h1>
      <button class="btn-primary" @click="showCreate = !showCreate">+ Nouvelle facture ST</button>
    </div>

    <!-- Filter tabs -->
    <div class="filter-tabs">
      <button :class="{ active: filter === 'all' }" @click="filter = 'all'; fetch()">Toutes</button>
      <button :class="{ active: filter === 'received' }" @click="filter = 'received'; fetch()">Reçues</button>
      <button :class="{ active: filter === 'authorized' }" @click="filter = 'authorized'; fetch()">Autorisées</button>
      <button :class="{ active: filter === 'paid' }" @click="filter = 'paid'; fetch()">Payées</button>
    </div>

    <div v-if="error" class="alert-error">{{ error }} <button @click="error=''">&times;</button></div>

    <!-- Create form -->
    <div v-if="showCreate" class="card" style="margin-bottom: 12px;">
      <form @submit.prevent="create" class="form-row-5">
        <div class="form-group"><label>Fournisseur ID</label><input v-model="form.supplier" type="number" required /></div>
        <div class="form-group"><label>Projet ID</label><input v-model="form.project" type="number" required /></div>
        <div class="form-group"><label>No facture</label><input v-model="form.invoice_number" type="text" required /></div>
        <div class="form-group"><label>Date</label><input v-model="form.invoice_date" type="date" required /></div>
        <div class="form-group"><label>Montant</label><input v-model="form.amount" type="number" step="0.01" required />
          <div style="margin-top:6px;display:flex;gap:4px;justify-content:flex-end;">
            <button type="button" class="btn-ghost" @click="showCreate=false">Annuler</button>
            <button type="submit" class="btn-primary">Créer</button>
          </div>
        </div>
      </form>
    </div>

    <!-- Table -->
    <div class="card-table">
      <table>
        <thead>
          <tr>
            <th>No facture</th>
            <th>Fournisseur</th>
            <th>Projet</th>
            <th class="text-right">Montant</th>
            <th>Date</th>
            <th>Statut</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="inv in invoices" :key="inv.id">
            <td class="font-mono">{{ inv.invoice_number }}</td>
            <td>{{ inv.supplier_name || `#${inv.supplier}` }}</td>
            <td class="font-mono">{{ inv.project_code || `#${inv.project}` }}</td>
            <td class="text-right font-mono font-semibold">{{ fmt.currency(inv.amount) }}</td>
            <td class="text-muted">{{ fmt.date(inv.invoice_date) }}</td>
            <td><span class="badge" :class="statusColors[inv.status]">{{ statusLabels[inv.status] || inv.status }}</span></td>
            <td class="actions-cell">
              <button v-if="inv.status === 'received'" class="btn-action" @click="authorize(inv.id)">Autoriser</button>
              <button v-if="inv.status === 'authorized'" class="btn-action success" @click="markPaid(inv.id)">Payer</button>
              <button v-if="inv.status === 'received'" class="btn-action danger" @click="remove(inv.id)">Supprimer</button>
            </td>
          </tr>
          <tr v-if="!invoices.length"><td colspan="7" class="empty">Aucune facture ST</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.page-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }
.page-header h1 { font-size: 20px; font-weight: 700; color: var(--color-gray-900); }
.filter-tabs { display: flex; gap: 0; border-bottom: 2px solid var(--color-gray-200); margin-bottom: 12px; }
.filter-tabs button { padding: 6px 14px; font-size: 12px; font-weight: 500; color: var(--color-gray-500); cursor: pointer; border: none; background: none; border-bottom: 2px solid transparent; margin-bottom: -2px; }
.filter-tabs button.active { color: var(--color-primary); border-bottom-color: var(--color-primary); font-weight: 600; }
.alert-error { background: var(--color-danger-light); color: var(--color-danger); padding: 8px 12px; border-radius: 6px; font-size: 12px; margin-bottom: 12px; display: flex; justify-content: space-between; }
.card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 16px; }
.card-table { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); overflow: hidden; }
.form-row-5 { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; }
.form-group label { display: block; font-size: 11px; font-weight: 600; color: var(--color-gray-600); margin-bottom: 4px; }
.text-right { text-align: right; } .text-muted { color: var(--color-gray-500); }
.font-mono { font-family: var(--font-mono); font-size: 12px; }
.badge { display: inline-flex; padding: 1px 8px; border-radius: 10px; font-size: 10px; font-weight: 600; }
.badge-blue { background: #DBEAFE; color: #1D4ED8; } .badge-amber { background: #FEF3C7; color: #92400E; }
.badge-green-solid { background: #15803D; color: white; }
.actions-cell { white-space: nowrap; }
.btn-action { background: none; border: none; font-size: 11px; cursor: pointer; color: var(--color-primary); padding: 2px 6px; font-weight: 600; }
.btn-action:hover { text-decoration: underline; }
.btn-action.success { color: var(--color-success); }
.btn-action.danger { color: var(--color-danger); }
.empty { text-align: center; padding: 30px; color: var(--color-gray-400); }
</style>
