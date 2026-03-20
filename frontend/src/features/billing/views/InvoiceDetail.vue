<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useLocale } from '@/shared/composables/useLocale'
import { billingApi } from '../api/billingApi'
import type { Invoice } from '../types/billing.types'

const route = useRoute()
const router = useRouter()
const { fmt } = useLocale()
const invoice = ref<Invoice | null>(null)
const invoiceId = Number(route.params.id)
const agingData = ref<Record<string, unknown> | null>(null)
const showPaymentForm = ref(false)
const paymentForm = ref({ amount: '', payment_date: '', reference: '', method: 'CHEQUE' })
const isEditingLines = ref(false)
const showAddLine = ref(false)
const newLine = ref({ deliverable_name: '', line_type: 'FORFAIT', total_contract_amount: '0', amount_to_bill: '0' })
const confirmDeleteLine = ref<number | null>(null)
const actionError = ref('')

const statusLabels: Record<string, string> = {
  DRAFT: 'Brouillon',
  SUBMITTED: 'Soumise',
  APPROVED: 'Approuvée',
  SENT: 'Envoyée',
  PAID: 'Payée',
}
const statusColors: Record<string, string> = {
  DRAFT: 'badge-gray',
  SUBMITTED: 'badge-blue',
  APPROVED: 'badge-green',
  SENT: 'badge-amber',
  PAID: 'badge-green-solid',
}

async function reload() {
  const resp = await billingApi.getInvoice(invoiceId)
  invoice.value = resp.data?.data || resp.data
}

onMounted(async () => {
  await reload()
  try {
    const agResp = await billingApi.agingAnalysis(invoiceId)
    agingData.value = agResp.data?.data || agResp.data
  } catch { /* aging optional */ }
})

async function submitInvoice() {
  actionError.value = ''
  try {
    await billingApi.submitInvoice(invoiceId)
    await reload()
  } catch (e: unknown) {
    actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur'
  }
}

async function approveInvoice() {
  actionError.value = ''
  try {
    await billingApi.approveInvoice(invoiceId)
    await reload()
  } catch (e: unknown) {
    actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur'
  }
}

async function markSent() {
  actionError.value = ''
  try {
    await billingApi.updateInvoice(invoiceId, { status: 'SENT' })
    await reload()
  } catch (e: unknown) {
    actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur'
  }
}

async function recordPayment() {
  actionError.value = ''
  try {
    await billingApi.createPayment({
      invoice: invoiceId,
      amount: paymentForm.value.amount,
      payment_date: paymentForm.value.payment_date,
      reference: paymentForm.value.reference,
      method: paymentForm.value.method,
    })
    showPaymentForm.value = false
    paymentForm.value = { amount: '', payment_date: '', reference: '', method: 'CHEQUE' }
    await reload()
  } catch (e: unknown) {
    actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur'
  }
}

async function createLine() {
  actionError.value = ''
  try {
    await billingApi.createLine(invoiceId, newLine.value)
    showAddLine.value = false
    newLine.value = { deliverable_name: '', line_type: 'FORFAIT', total_contract_amount: '0', amount_to_bill: '0' }
    await reload()
  } catch (e: unknown) { actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur' }
}

async function deleteLine(lineId: number) {
  await billingApi.deleteLine(invoiceId, lineId)
  confirmDeleteLine.value = null
  await reload()
}

function stopEditingLines() {
  isEditingLines.value = false
  showAddLine.value = false
  confirmDeleteLine.value = null
}

function openPrint() {
  const token = localStorage.getItem('access_token')
  // Open print view with auth — fetch HTML and open in new window
  fetch(`/api/v1/invoices/${invoiceId}/print/`, {
    headers: { Authorization: `Bearer ${token}` },
  })
    .then(r => r.text())
    .then(html => {
      const w = window.open('', '_blank')
      if (w) { w.document.write(html); w.document.close() }
    })
}

async function updateLine(lineId: number, field: string, value: string) {
  await billingApi.updateLine(invoiceId, lineId, { [field]: value })
  await reload()
}
</script>

<template>
  <div v-if="invoice">
    <!-- Header -->
    <div class="page-header">
      <div>
        <button class="btn-back" @click="router.push('/billing')">&larr; Facturation</button>
        <h1>
          <span class="font-mono">{{ invoice.invoice_number }}</span>
        </h1>
        <p class="subtitle">Projet {{ invoice.project_code }} · {{ invoice.client_name }}</p>
      </div>
      <div class="header-actions">
        <span class="badge" :class="statusColors[invoice.status]">{{ statusLabels[invoice.status] }}</span>
        <button v-if="invoice.status === 'DRAFT'" class="btn-primary" @click="submitInvoice">Soumettre</button>
        <button v-if="invoice.status === 'SUBMITTED'" class="btn-success" @click="approveInvoice">Approuver</button>
        <button v-if="invoice.status === 'APPROVED'" class="btn-primary" @click="markSent">Marquer envoyée</button>
        <button v-if="invoice.status === 'SENT'" class="btn-success" @click="showPaymentForm = !showPaymentForm">Enregistrer paiement</button>
        <button class="btn-ghost" @click="openPrint">Imprimer</button>
      </div>
    </div>

    <div v-if="actionError" class="alert-error">{{ actionError }}</div>

    <!-- Payment form -->
    <div v-if="showPaymentForm" class="card" style="margin-bottom: 12px;">
      <div class="card-title">Enregistrer un paiement</div>
      <form @submit.prevent="recordPayment" class="payment-form">
        <div class="form-row-4">
          <div class="form-group">
            <label>Montant</label>
            <input v-model="paymentForm.amount" type="number" step="0.01" required :placeholder="invoice.total_amount" />
          </div>
          <div class="form-group">
            <label>Date</label>
            <input v-model="paymentForm.payment_date" type="date" required />
          </div>
          <div class="form-group">
            <label>Référence</label>
            <input v-model="paymentForm.reference" type="text" placeholder="No chèque / virement" />
          </div>
          <div class="form-group">
            <label>Méthode</label>
            <select v-model="paymentForm.method">
              <option value="CHEQUE">Chèque</option>
              <option value="VIREMENT">Virement</option>
              <option value="CARTE">Carte</option>
            </select>
          </div>
        </div>
        <div class="form-actions">
          <button type="button" class="btn-ghost" @click="showPaymentForm = false">Annuler</button>
          <button type="submit" class="btn-success">Enregistrer</button>
        </div>
      </form>
    </div>

    <!-- Amounts banner -->
    <div class="amounts-banner">
      <div class="amount-item">
        <div class="amount-value primary">{{ fmt.currency(invoice.total_amount) }}</div>
        <div class="amount-label">Montant total</div>
      </div>
      <div class="amount-sep" />
      <div class="amount-item">
        <div class="amount-value">{{ fmt.currency(invoice.tax_tps) }}</div>
        <div class="amount-label">TPS</div>
      </div>
      <div class="amount-sep" />
      <div class="amount-item">
        <div class="amount-value">{{ fmt.currency(invoice.tax_tvq) }}</div>
        <div class="amount-label">TVQ</div>
      </div>
    </div>

    <!-- Line management -->
    <div v-if="invoice.status === 'DRAFT'" class="line-actions">
      <button v-if="!isEditingLines" class="btn-primary" @click="isEditingLines = true">Modifier les lignes</button>
      <template v-else>
        <button class="btn-ghost" @click="showAddLine = !showAddLine">+ Ajouter ligne</button>
        <button class="btn-ghost" @click="stopEditingLines">Terminer</button>
      </template>
    </div>
    <div v-if="showAddLine" class="card" style="margin-bottom: 8px;">
      <form @submit.prevent="createLine" class="form-row-4">
        <div class="form-group"><label>Livrable</label><input v-model="newLine.deliverable_name" required /></div>
        <div class="form-group"><label>Type</label><select v-model="newLine.line_type"><option value="FORFAIT">Forfait</option><option value="HORAIRE">Horaire</option><option value="ST">ST</option><option value="DEPENSE">Dépense</option></select></div>
        <div class="form-group"><label>Montant contrat</label><input v-model="newLine.total_contract_amount" type="number" step="0.01" /></div>
        <div class="form-group"><label>À facturer</label><input v-model="newLine.amount_to_bill" type="number" step="0.01" /><div style="margin-top:4px;display:flex;gap:4px;justify-content:flex-end;"><button type="button" class="btn-ghost" @click="showAddLine=false">Annuler</button><button type="submit" class="btn-primary">Ajouter</button></div></div>
      </form>
    </div>

    <!-- 7-Column Grid -->
    <div class="card-table">
      <table>
        <thead>
          <tr>
            <th style="min-width: 180px;">Livrable</th>
            <th class="text-right mono-th" style="min-width: 90px;">Contrat</th>
            <th class="text-right mono-th" style="min-width: 90px;">Facturé</th>
            <th class="text-right mono-th" style="min-width: 60px;">% Fact.</th>
            <th class="text-right mono-th" style="min-width: 60px;">% Heures</th>
            <th class="text-right mono-th" style="min-width: 100px;">À facturer</th>
            <th class="text-right mono-th" style="min-width: 60px;">% Après</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="line in invoice.lines" :key="line.id">
            <td>
              <span class="line-type-badge">{{ line.line_type }}</span>
              {{ line.deliverable_name }}
            </td>
            <td class="text-right font-mono">{{ fmt.currency(line.total_contract_amount) }}</td>
            <td class="text-right font-mono">{{ fmt.currency(line.invoiced_to_date) }}</td>
            <td class="text-right font-mono">{{ line.pct_billing_advancement }}%</td>
            <td class="text-right font-mono">{{ line.pct_hours_advancement }}%</td>
            <td class="text-right">
              <input
                :value="line.amount_to_bill"
                type="number"
                step="0.01"
                class="bill-input"
                :disabled="!(invoice.status === 'DRAFT' && isEditingLines)"
                @blur="(e) => updateLine(line.id, 'amount_to_bill', (e.target as HTMLInputElement).value)"
              />
            </td>
            <td class="text-right font-mono text-muted">{{ line.pct_after_billing }}%</td>
            <td v-if="invoice.status === 'DRAFT' && isEditingLines" class="text-right">
              <template v-if="confirmDeleteLine === line.id">
                <button class="btn-action danger" @click="deleteLine(line.id)">Confirmer</button>
                <button class="btn-action" @click="confirmDeleteLine = null">Annuler</button>
              </template>
              <button v-else class="btn-action danger" @click="confirmDeleteLine = line.id">×</button>
            </td>
          </tr>
          <tr v-if="!invoice.lines?.length">
            <td colspan="7" class="empty">Aucune ligne</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Aging Analysis -->
    <div v-if="agingData" class="aging-section">
      <h3 class="section-title">Analyse d'ancienneté</h3>
      <div class="aging-grid">
        <div class="aging-card">
          <span class="aging-label">0-30 jours</span>
          <span class="aging-value">{{ fmt.currency(agingData.range_0_30 as string || '0') }}</span>
        </div>
        <div class="aging-card">
          <span class="aging-label">31-60 jours</span>
          <span class="aging-value warning">{{ fmt.currency(agingData.range_31_60 as string || '0') }}</span>
        </div>
        <div class="aging-card">
          <span class="aging-label">61-90 jours</span>
          <span class="aging-value danger">{{ fmt.currency(agingData.range_61_90 as string || '0') }}</span>
        </div>
        <div class="aging-card">
          <span class="aging-label">90+ jours</span>
          <span class="aging-value danger">{{ fmt.currency(agingData.range_90_plus as string || '0') }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-header { display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 16px; }
.page-header h1 { font-size: 20px; font-weight: 700; color: var(--color-gray-900); margin-top: 2px; }
.btn-back { background: none; border: none; font-size: 12px; color: var(--color-gray-500); cursor: pointer; padding: 0; }
.subtitle { font-size: 12px; color: var(--color-gray-500); }
.header-actions { display: flex; align-items: center; gap: 8px; }
.btn-success { padding: 6px 12px; border-radius: 4px; font-size: 12px; font-weight: 600; cursor: pointer; border: none; background: var(--color-success); color: white; }
.alert-error { background: var(--color-danger-light); color: var(--color-danger); padding: 8px 12px; border-radius: 6px; font-size: 12px; margin-bottom: 12px; }

.badge { display: inline-flex; padding: 2px 10px; border-radius: 10px; font-size: 10px; font-weight: 600; }
.badge-gray { background: var(--color-gray-100); color: var(--color-gray-500); }
.badge-blue { background: #DBEAFE; color: #1D4ED8; }
.badge-green { background: #DCFCE7; color: #15803D; }
.badge-amber { background: #FEF3C7; color: #92400E; }
.badge-green-solid { background: #15803D; color: white; }

.card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 16px; }
.card-title { font-size: 14px; font-weight: 600; color: var(--color-gray-800); margin-bottom: 12px; }
.card-table { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); overflow-x: auto; margin-bottom: 16px; }

.amounts-banner { display: flex; align-items: center; gap: 16px; padding: 12px 16px; background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 12px; }
.amount-item { text-align: center; }
.amount-value { font-family: var(--font-mono); font-size: 16px; font-weight: 700; color: var(--color-gray-800); }
.amount-value.primary { color: var(--color-primary); }
.amount-label { font-size: 10px; color: var(--color-gray-500); }
.amount-sep { width: 1px; height: 28px; background: var(--color-gray-200); }

.text-right { text-align: right; }
.text-muted { color: var(--color-gray-500); }
.font-mono { font-family: var(--font-mono); font-size: 12px; }
.mono-th { font-family: var(--font-mono); }
.line-type-badge { font-size: 9px; font-weight: 600; padding: 1px 5px; border-radius: 3px; background: var(--color-gray-100); color: var(--color-gray-500); margin-right: 4px; }
.bill-input { width: 100%; padding: 4px 8px; border: 1px solid var(--color-primary); border-radius: 3px; background: rgba(37,99,235,0.05); text-align: right; font-family: var(--font-mono); font-size: 12px; }
.bill-input:disabled { background: transparent; border-color: var(--color-gray-200); color: var(--color-gray-500); }
.empty { text-align: center; padding: 30px; color: var(--color-gray-400); }
.line-actions { display: flex; gap: 8px; margin-bottom: 8px; }
.btn-action { background: none; border: none; font-size: 11px; cursor: pointer; color: var(--color-primary); padding: 2px 6px; font-weight: 600; }
.btn-action:hover { text-decoration: underline; } .btn-action.danger { color: var(--color-danger); }

.form-row-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
.form-group { margin-bottom: 12px; }
.form-group label { display: block; font-size: 11px; font-weight: 600; color: var(--color-gray-600); margin-bottom: 4px; }
.form-actions { display: flex; justify-content: flex-end; gap: 6px; }

.aging-section { margin-top: 16px; }
.section-title { font-size: 14px; font-weight: 600; color: var(--color-gray-800); margin-bottom: 10px; }
.aging-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
.aging-card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 14px; }
.aging-label { display: block; font-size: 11px; color: var(--color-gray-500); text-transform: uppercase; font-weight: 600; margin-bottom: 4px; }
.aging-value { font-size: 20px; font-weight: 700; font-family: var(--font-mono); color: var(--color-gray-900); }
.aging-value.warning { color: var(--color-warning); }
.aging-value.danger { color: var(--color-danger); }
</style>
