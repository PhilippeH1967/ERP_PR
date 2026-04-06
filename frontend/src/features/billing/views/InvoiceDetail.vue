<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
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
const newLine = ref({ deliverable_name: '', line_type: 'DEPENSE', total_contract_amount: '0', amount_to_bill: '0' })
const markingHours = ref(false)
const markHoursResult = ref('')
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
    newLine.value = { deliverable_name: '', line_type: 'DEPENSE', total_contract_amount: '0', amount_to_bill: '0' }
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

async function markHoursInvoiced() {
  markingHours.value = true
  markHoursResult.value = ''
  actionError.value = ''
  try {
    const resp = await billingApi.markHoursInvoiced(invoiceId)
    const data = resp.data?.data || resp.data
    markHoursResult.value = `${data.marked_count} entree(s) de temps marquee(s) comme facturee(s).`
  } catch (e: unknown) {
    actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur'
  } finally {
    markingHours.value = false
  }
}

async function deleteDraft() {
  if (!invoice.value || invoice.value.status !== 'DRAFT') return
  try {
    await billingApi.deleteInvoice(invoiceId)
    router.push('/billing')
  } catch (e: unknown) {
    actionError.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur lors de la suppression'
  }
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

const lineError = ref('')
const lineWarning = ref('')
const pendingOverride = ref<{ lineId: number; field: string; value: string } | null>(null)

// Auto-calculated totals
const subtotal = computed(() => {
  if (!invoice.value?.lines) return 0
  return invoice.value.lines.reduce((sum: number, line: { amount_to_bill: string | number }) => sum + (parseFloat(String(line.amount_to_bill)) || 0), 0)
})
// Dynamic % calculations
function pctFact(line: { total_contract_amount: string | number; invoiced_to_date: string | number }): number {
  const contract = parseFloat(String(line.total_contract_amount)) || 0
  const invoiced = parseFloat(String(line.invoiced_to_date)) || 0
  return contract > 0 ? Math.round(invoiced / contract * 100) : 0
}
function pctAfter(line: { total_contract_amount: string | number; invoiced_to_date: string | number; amount_to_bill: string | number }): number {
  const contract = parseFloat(String(line.total_contract_amount)) || 0
  const invoiced = parseFloat(String(line.invoiced_to_date)) || 0
  const toBill = parseFloat(String(line.amount_to_bill)) || 0
  return contract > 0 ? Math.round((invoiced + toBill) / contract * 100) : 0
}

// Dynamic taxes from API (taxes_detail JSON) — fallback to hardcoded Québec
const taxesDetail = computed(() => {
  const detail = (invoice.value as Record<string, unknown>)?.taxes_detail as Array<{ type: string; label: string; rate: number; amount: number }> | undefined
  if (detail && detail.length) return detail
  // Fallback
  return [
    { type: 'TPS', label: 'TPS (5%)', rate: 5, amount: Math.round(subtotal.value * 0.05 * 100) / 100 },
    { type: 'TVQ', label: 'TVQ (9.975%)', rate: 9.975, amount: Math.round(subtotal.value * 0.09975 * 100) / 100 },
  ]
})
const totalTaxes = computed(() => taxesDetail.value.reduce((s, t) => s + t.amount, 0))
const totalTTC = computed(() => {
  const apiTotal = Number((invoice.value as Record<string, unknown>)?.total_with_taxes || 0)
  return apiTotal > 0 ? apiTotal : Math.round((subtotal.value + totalTaxes.value) * 100) / 100
})
// Backward compat
const taxTPS = computed(() => taxesDetail.value.filter(t => ['TPS', 'GST'].includes(t.type)).reduce((s, t) => s + t.amount, 0))
const taxTVQ = computed(() => taxesDetail.value.filter(t => ['TVQ', 'PST'].includes(t.type)).reduce((s, t) => s + t.amount, 0))

async function updateLine(lineId: number, field: string, value: string, force = false) {
  lineError.value = ''
  lineWarning.value = ''
  pendingOverride.value = null
  try {
    const payload: Record<string, unknown> = { [field]: value }
    if (force) payload.force_override = true
    await billingApi.updateLine(invoiceId, lineId, payload)
    await reload()
  } catch (e: unknown) {
    const resp = (e as { response?: { data?: Record<string, unknown> } }).response
    const data = resp?.data as Record<string, unknown> | undefined
    const error = data?.error as Record<string, unknown> | undefined
    const details = error?.details as Array<{ field: string; message: string }> | undefined
    const msg = details?.length ? details.map(d => d.message).join('. ') : String(error?.message || 'Erreur')
    if (msg.includes('Confirmez pour continuer')) {
      lineWarning.value = msg.replace(' Confirmez pour continuer.', '')
      pendingOverride.value = { lineId, field, value }
    } else {
      lineError.value = msg
    }
  }
}
function confirmOverride() {
  if (pendingOverride.value) {
    updateLine(pendingOverride.value.lineId, pendingOverride.value.field, pendingOverride.value.value, true)
  }
}
function cancelOverride() {
  lineWarning.value = ''
  pendingOverride.value = null
  reload()
}
</script>

<template>
  <div v-if="invoice" class="invoice-detail">
    <!-- 1. Breadcrumb -->
    <div class="breadcrumb">
      <a href="#" @click.prevent="router.push('/billing')">Facturation</a>
      <span>&gt;</span>
      <span>{{ invoice.project_code }}</span>
      <span>&gt;</span>
      <span>{{ invoice.invoice_number }}</span>
    </div>

    <!-- 2. Header -->
    <div class="page-header">
      <div>
        <div class="header-client">{{ invoice.client_name }}</div>
        <h1>{{ invoice.project_code }} — {{ invoice.project_name || 'Facture libre' }}</h1>
        <div class="subtitle">
          {{ invoice.invoice_number }} &bull;
          Statut: <span class="badge" :class="statusColors[invoice.status]">{{ statusLabels[invoice.status] }}</span>
        </div>
      </div>
    </div>

    <!-- 3. Workflow bar -->
    <div class="workflow-bar">
      <div
        class="wf-step"
        :class="{
          'wf-done': ['SUBMITTED','APPROVED','SENT','PAID'].includes(invoice.status),
          'wf-active': invoice.status === 'DRAFT'
        }"
      >
        <div class="wf-num">1</div>
        <span>Brouillon</span>
      </div>
      <span class="wf-arrow">&#9654;</span>
      <div
        class="wf-step"
        :class="{
          'wf-done': ['APPROVED','SENT','PAID'].includes(invoice.status),
          'wf-active': invoice.status === 'SUBMITTED'
        }"
      >
        <div class="wf-num">2</div>
        <span>Soumise</span>
      </div>
      <span class="wf-arrow">&#9654;</span>
      <div
        class="wf-step"
        :class="{
          'wf-done': ['SENT','PAID'].includes(invoice.status),
          'wf-active': invoice.status === 'APPROVED'
        }"
      >
        <div class="wf-num">3</div>
        <span>Approuvee</span>
      </div>
      <span class="wf-arrow">&#9654;</span>
      <div
        class="wf-step"
        :class="{
          'wf-done': invoice.status === 'PAID',
          'wf-active': invoice.status === 'SENT'
        }"
      >
        <div class="wf-num">4</div>
        <span>Envoyee / Payee</span>
      </div>
    </div>

    <!-- 4. Error / warning banners -->
    <div v-if="actionError" class="alert-error">{{ actionError }}</div>
    <div v-if="lineError" class="line-error">{{ lineError }}</div>
    <div v-if="lineWarning" class="line-warning">
      <span>&#9888; {{ lineWarning }}</span>
      <div class="warning-actions">
        <button class="btn-warning-confirm" @click="confirmOverride">Confirmer le depassement</button>
        <button class="btn-ghost-sm" @click="cancelOverride">Annuler</button>
      </div>
    </div>

    <!-- 5. Payment form -->
    <div v-if="showPaymentForm" class="card payment-card">
      <div class="card-title">Enregistrer un paiement</div>
      <form @submit.prevent="recordPayment" class="payment-form">
        <div class="form-row-4">
          <div class="form-group">
            <label>Montant</label>
            <input v-model="paymentForm.amount" type="number" step="0.01" required :placeholder="invoice.total_amount" class="no-spinners" />
          </div>
          <div class="form-group">
            <label>Date</label>
            <input v-model="paymentForm.payment_date" type="date" required />
          </div>
          <div class="form-group">
            <label>Reference</label>
            <input v-model="paymentForm.reference" type="text" placeholder="No cheque / virement" />
          </div>
          <div class="form-group">
            <label>Methode</label>
            <select v-model="paymentForm.method">
              <option value="CHEQUE">Cheque</option>
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

    <!-- 6. Seven-column table -->
    <div class="card table-card">
      <div class="table-header">
        <div class="card-title">Lignes de facturation — 7 colonnes</div>
        <div class="table-legend">
          <span class="legend-item"><span class="legend-swatch legend-edit"></span> Cellules editables</span>
          <span class="legend-item"><span class="legend-swatch legend-readonly"></span> Lecture seule</span>
        </div>
      </div>

      <div class="table-scroll">
        <table>
          <thead>
            <tr>
              <th class="th-label" style="min-width: 240px;">Phase / Tache</th>
              <th class="th-mono" style="min-width: 100px;">Montant contrat</th>
              <th class="th-mono" style="min-width: 100px;">Facture a ce jour</th>
              <th class="th-mono" style="min-width: 70px;">% Fact.</th>
              <th class="th-mono" style="min-width: 70px;">% Heures</th>
              <th class="th-mono th-editable" style="min-width: 120px;">Facturer ce mois</th>
              <th class="th-mono" style="min-width: 70px;">% apres</th>
              <th v-if="invoice.status === 'DRAFT' && isEditingLines" class="th-mono" style="min-width: 60px;"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="line in invoice.lines" :key="line.id" class="data-row">
              <td class="cell-name">
                <span class="line-type-badge">{{ line.line_type }}</span>
                {{ line.deliverable_name }}
                <a
                  v-if="invoice.project"
                  :href="`/projects/${invoice.project}`"
                  target="_blank"
                  class="budget-link"
                  title="Voir le budget du projet (nouvel onglet)"
                >&#8599;</a>
              </td>
              <td class="cell-mono cell-readonly">{{ fmt.currency(line.total_contract_amount) }}</td>
              <td class="cell-mono cell-readonly">{{ fmt.currency(line.invoiced_to_date) }}</td>
              <td class="cell-mono cell-readonly" :class="{ 'text-danger': pctFact(line) > 100 }">{{ pctFact(line) }}%</td>
              <td class="cell-mono cell-readonly">{{ line.pct_hours_advancement }}%</td>
              <td class="cell-editable">
                <input
                  :value="line.amount_to_bill"
                  type="number"
                  step="0.01"
                  class="bill-input no-spinners"
                  :class="{ 'bill-input-active': invoice.status === 'DRAFT' && isEditingLines }"
                  :disabled="!(invoice.status === 'DRAFT' && isEditingLines)"
                  @blur="(e) => updateLine(line.id, 'amount_to_bill', (e.target as HTMLInputElement).value)"
                />
              </td>
              <td class="cell-mono cell-after" :class="{ 'text-danger': pctAfter(line) > 100, 'text-success': pctAfter(line) === 100 }">{{ pctAfter(line) }}%</td>
              <td v-if="invoice.status === 'DRAFT' && isEditingLines" class="cell-delete">
                <template v-if="confirmDeleteLine === line.id">
                  <button class="btn-action danger" @click="deleteLine(line.id)">Confirmer</button>
                  <button class="btn-action" @click="confirmDeleteLine = null">Annuler</button>
                </template>
                <button v-else class="btn-action danger" @click="confirmDeleteLine = line.id">&times;</button>
              </td>
            </tr>
            <tr v-if="!invoice.lines?.length">
              <td :colspan="invoice.status === 'DRAFT' && isEditingLines ? 8 : 7" class="empty">Aucune ligne</td>
            </tr>
          </tbody>
          <!-- 7. Table footer with totals -->
          <tfoot>
            <tr class="row-subtotal">
              <td>Sous-total</td>
              <td></td>
              <td></td>
              <td></td>
              <td></td>
              <td class="cell-mono cell-total-edit">{{ fmt.currency(subtotal) }}</td>
              <td></td>
              <td v-if="invoice.status === 'DRAFT' && isEditingLines"></td>
            </tr>
            <tr v-for="tax in taxesDetail" :key="tax.type" class="row-tax">
              <td>{{ tax.label }} ({{ tax.rate }}%)</td>
              <td></td>
              <td></td>
              <td></td>
              <td></td>
              <td class="cell-mono">{{ fmt.currency(tax.amount) }}</td>
              <td></td>
              <td v-if="invoice.status === 'DRAFT' && isEditingLines"></td>
            </tr>
            <tr class="row-total-ttc">
              <td>TOTAL TTC</td>
              <td></td>
              <td></td>
              <td></td>
              <td></td>
              <td class="cell-mono cell-grand-total">{{ fmt.currency(totalTTC) }}</td>
              <td></td>
              <td v-if="invoice.status === 'DRAFT' && isEditingLines"></td>
            </tr>
          </tfoot>
        </table>
      </div>
    </div>

    <!-- 7b. Add free line form (after table) -->
    <div v-if="showAddLine" class="card add-line-card">
      <div class="card-title" style="padding: 12px 20px 0;">Ajouter une ligne libre</div>
      <div class="add-line-row">
        <form @submit.prevent="createLine" class="add-line-form">
          <div class="form-group" style="flex: 2.5;">
            <label>Libelle</label>
            <input v-model="newLine.deliverable_name" required placeholder="Description de la ligne" />
          </div>
          <div class="form-group" style="flex: 0.8;">
            <label>Type</label>
            <select v-model="newLine.line_type">
              <option value="DEPENSE">Depense</option>
              <option value="AUTRE">Autre</option>
              <option value="ST">ST</option>
            </select>
          </div>
          <div class="form-group" style="flex: 0.8;">
            <label>Montant</label>
            <input v-model="newLine.amount_to_bill" type="number" step="0.01" class="no-spinners input-right" />
          </div>
          <div class="form-group" style="flex: 0.8; display: flex; align-items: flex-end; gap: 4px;">
            <button type="button" class="btn-ghost" @click="showAddLine = false">Annuler</button>
            <button type="submit" class="btn-primary">Ajouter</button>
          </div>
        </form>
      </div>
    </div>

    <!-- 7c. Mark hours as invoiced -->
    <div v-if="markHoursResult" class="alert-success">{{ markHoursResult }}</div>

    <!-- 8. Aging Analysis -->
    <div v-if="agingData" class="aging-section">
      <h3 class="section-title">Analyse d'anciennete</h3>
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

    <!-- 9. Footer action bar -->
    <div class="footer-actions">
      <div class="footer-left">
        <button class="btn-ghost" @click="router.push('/billing')">&larr; Retour a la liste</button>
        <button v-if="invoice.status === 'DRAFT'" class="btn-danger-outline" @click="deleteDraft">Supprimer ce brouillon</button>
      </div>
      <div class="footer-right">
        <button class="btn-ghost" @click="openPrint">Imprimer</button>

        <!-- DRAFT actions -->
        <template v-if="invoice.status === 'DRAFT'">
          <button v-if="!isEditingLines" class="btn-ghost" @click="isEditingLines = true">Modifier les lignes</button>
          <template v-else>
            <button class="btn-ghost" @click="showAddLine = !showAddLine">+ Ajouter ligne</button>
            <button class="btn-ghost" @click="stopEditingLines">Terminer</button>
          </template>
          <button class="btn-primary" @click="submitInvoice">Soumettre pour approbation &rarr;</button>
        </template>

        <!-- SUBMITTED -->
        <button v-if="invoice.status === 'SUBMITTED'" class="btn-success" @click="approveInvoice">Approuver</button>

        <!-- APPROVED -->
        <button v-if="invoice.status === 'APPROVED'" class="btn-primary" @click="markSent">Marquer envoyee</button>

        <!-- SENT -->
        <template v-if="invoice.status === 'SENT'">
          <button class="btn-ghost" :disabled="markingHours" @click="markHoursInvoiced">
            {{ markingHours ? 'En cours...' : 'Marquer les heures comme facturees' }}
          </button>
          <button class="btn-success" @click="showPaymentForm = !showPaymentForm">Enregistrer paiement</button>
        </template>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* ── Layout ───────────────────────────────────────────── */
.invoice-detail { max-width: 1200px; margin: 0 auto; padding-bottom: 80px; }

/* ── Breadcrumb ───────────────────────────────────────── */
.breadcrumb { font-size: 12px; color: var(--color-gray-500); margin-bottom: 8px; display: flex; gap: 6px; align-items: center; }
.breadcrumb a { color: var(--color-primary); text-decoration: none; }
.breadcrumb a:hover { text-decoration: underline; }

/* ── Header ───────────────────────────────────────────── */
.page-header { margin-bottom: 16px; }
.header-client { font-size: 16px; font-weight: 700; color: var(--color-primary); margin-bottom: 2px; }
.page-header h1 { font-size: 22px; font-weight: 700; color: var(--color-gray-900); margin: 0 0 4px 0; }
.subtitle { font-size: 13px; color: var(--color-gray-500); display: flex; align-items: center; gap: 4px; flex-wrap: wrap; }

/* ── Badge ────────────────────────────────────────────── */
.badge { display: inline-flex; padding: 2px 10px; border-radius: 10px; font-size: 10px; font-weight: 600; vertical-align: middle; }
.badge-gray { background: var(--color-gray-100); color: var(--color-gray-500); }
.badge-blue { background: #DBEAFE; color: #1D4ED8; }
.badge-green { background: #DCFCE7; color: #15803D; }
.badge-amber { background: #FEF3C7; color: #92400E; }
.badge-green-solid { background: #15803D; color: white; }

/* ── Workflow bar ─────────────────────────────────────── */
.workflow-bar {
  display: flex; align-items: center; gap: 0; margin-bottom: 16px;
  background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  padding: 10px 16px; overflow-x: auto;
}
.wf-step {
  display: flex; align-items: center; gap: 8px;
  padding: 6px 14px; border-radius: 6px;
  font-size: 12px; font-weight: 500; color: var(--color-gray-400);
  background: var(--color-gray-100); white-space: nowrap;
}
.wf-step.wf-active { background: var(--color-primary); color: white; font-weight: 600; }
.wf-step.wf-done { background: #DCFCE7; color: #15803D; font-weight: 600; }
.wf-num {
  width: 20px; height: 20px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
  font-size: 11px; font-weight: 700; background: rgba(255,255,255,0.3); color: inherit;
}
.wf-step.wf-active .wf-num { background: rgba(255,255,255,0.25); }
.wf-step.wf-done .wf-num { background: rgba(21,128,61,0.15); }
.wf-arrow { color: var(--color-gray-300); margin: 0 8px; font-size: 10px; }

/* ── Alerts ───────────────────────────────────────────── */
.alert-error { background: #FEE2E2; color: #DC2626; padding: 10px 16px; border-radius: 6px; font-size: 13px; margin-bottom: 12px; border: 1px solid #FECACA; }
.line-error { background: #FEE2E2; color: #DC2626; padding: 8px 14px; border-radius: 6px; font-size: 12px; margin-bottom: 8px; }
.line-warning { background: #FEF3C7; color: #92400E; padding: 10px 14px; border-radius: 6px; font-size: 12px; margin-bottom: 8px; border: 1px solid #FCD34D; }
.alert-success { background: #DCFCE7; color: #15803D; padding: 10px 16px; border-radius: 6px; font-size: 13px; margin-bottom: 12px; border: 1px solid #BBF7D0; }
.warning-actions { display: flex; gap: 8px; margin-top: 6px; }
.btn-warning-confirm { padding: 4px 12px; border-radius: 4px; font-size: 11px; font-weight: 600; background: #D97706; color: white; border: none; cursor: pointer; }
.btn-warning-confirm:hover { background: #B45309; }
.btn-ghost-sm { padding: 4px 12px; border-radius: 4px; font-size: 11px; cursor: pointer; background: none; border: 1px solid var(--color-gray-300); color: var(--color-gray-600); }

/* ── Card / Payment ───────────────────────────────────── */
.card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }
.card-title { font-size: 14px; font-weight: 600; color: var(--color-gray-800); }
.payment-card { padding: 16px; margin-bottom: 12px; }
.form-row-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
.form-group { margin-bottom: 12px; }
.form-group label { display: block; font-size: 11px; font-weight: 600; color: var(--color-gray-600); margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.3px; }
.form-group input, .form-group select { width: 100%; padding: 6px 8px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 12px; }
.form-group input:focus, .form-group select:focus { outline: none; border-color: var(--color-primary); box-shadow: 0 0 0 2px rgba(37,99,235,0.12); }
.form-actions { display: flex; justify-content: flex-end; gap: 6px; }
.input-right { text-align: right; }

/* ── Table card ───────────────────────────────────────── */
.table-card { margin-bottom: 16px; overflow: hidden; }
.table-header {
  padding: 14px 20px; display: flex; justify-content: space-between; align-items: center;
  border-bottom: 1px solid var(--color-gray-200);
}
.table-legend { display: flex; gap: 16px; font-size: 12px; color: var(--color-gray-500); }
.legend-item { display: flex; align-items: center; gap: 4px; }
.legend-swatch { width: 10px; height: 10px; border-radius: 2px; }
.legend-edit { background: #FFFBEB; border: 1px solid #FCD34D; }
.legend-readonly { background: var(--color-gray-50); border: 1px solid var(--color-gray-200); }

.add-line-card { margin-bottom: 16px; overflow: hidden; }
.add-line-row { padding: 10px 20px; background: var(--color-gray-50); }
.add-line-form { display: flex; gap: 10px; align-items: flex-end; }

.table-scroll { overflow-x: auto; }

table { width: 100%; border-collapse: collapse; }

/* ── Table head ───────────────────────────────────────── */
thead th {
  padding: 10px 12px; text-align: right; font-size: 11px; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.4px; color: var(--color-gray-500);
  background: var(--color-gray-50); border-bottom: 2px solid var(--color-gray-200);
  white-space: nowrap;
}
.th-label { text-align: left !important; min-width: 240px; }
.th-mono { font-family: var(--font-mono); }
.th-editable { background: #FFFBEB !important; }

/* ── Table body ───────────────────────────────────────── */
.data-row { border-bottom: 1px solid var(--color-gray-100); }
.data-row:hover { background: var(--color-gray-50); }

td { padding: 8px 12px; font-size: 14px; color: var(--color-gray-700); }
.cell-name { text-align: left; font-weight: 500; }
.cell-mono { text-align: right; font-family: var(--font-mono); font-size: 13px; }
.cell-readonly { color: var(--color-gray-600); }
.cell-after { text-align: right; font-family: var(--font-mono); font-size: 13px; color: var(--color-gray-500); }
.cell-editable { text-align: right; background: rgba(37,99,235,0.04); }
.cell-delete { text-align: right; white-space: nowrap; }

.line-type-badge { font-size: 9px; font-weight: 600; padding: 1px 5px; border-radius: 3px; background: var(--color-gray-100); color: var(--color-gray-500); margin-right: 4px; text-transform: uppercase; }
.budget-link { font-size: 11px; color: var(--color-primary); text-decoration: none; margin-left: 4px; opacity: 0.6; }
.budget-link:hover { opacity: 1; text-decoration: underline; }

.bill-input {
  width: 100%; max-width: 110px; padding: 4px 8px; text-align: right;
  font-family: var(--font-mono); font-size: 13px; font-weight: 600;
  border: 1px solid var(--color-gray-200); border-radius: 3px;
  background: transparent; color: var(--color-gray-500);
}
.bill-input-active {
  background: #FFFBEB; border-color: #FCD34D; color: var(--color-gray-900);
}
.bill-input-active:focus {
  border-color: var(--color-primary); background: rgba(37,99,235,0.06);
  outline: none; box-shadow: 0 0 0 2px rgba(37,99,235,0.15);
}
.bill-input:disabled { cursor: default; }

.empty { text-align: center; padding: 30px; color: var(--color-gray-400); font-size: 13px; }

/* ── Table footer (totals) ────────────────────────────── */
tfoot td { padding: 8px 12px; font-size: 13px; }

.row-subtotal {
  background: var(--color-gray-50); border-top: 2px solid var(--color-gray-300);
}
.row-subtotal td { font-weight: 700; color: var(--color-gray-700); }
.cell-total-edit { font-weight: 700; font-size: 15px; background: rgba(37,99,235,0.08); }

.row-tax td { color: var(--color-gray-500); background: var(--color-gray-50); }
.row-tax .cell-mono { font-size: 13px; }

.row-total-ttc {
  background: var(--color-gray-800) !important;
}
.row-total-ttc td {
  color: white !important; font-weight: 700; font-size: 14px; padding: 10px 12px;
}
.cell-grand-total { font-size: 16px !important; color: #93c5fd !important; }

/* ── Aging ────────────────────────────────────────────── */
.aging-section { margin-bottom: 16px; }
.section-title { font-size: 14px; font-weight: 600; color: var(--color-gray-800); margin-bottom: 10px; }
.aging-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
.aging-card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); padding: 14px; }
.aging-label { display: block; font-size: 11px; color: var(--color-gray-500); text-transform: uppercase; font-weight: 600; margin-bottom: 4px; letter-spacing: 0.3px; }
.aging-value { font-size: 20px; font-weight: 700; font-family: var(--font-mono); color: var(--color-gray-900); }
.aging-value.warning { color: var(--color-warning); }
.aging-value.danger { color: var(--color-danger); }

/* ── Footer action bar ────────────────────────────────── */
.footer-actions {
  display: flex; justify-content: space-between; align-items: center;
  padding: 14px 20px; background: white; border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08); margin-top: 16px;
  position: sticky; bottom: 12px; z-index: 10;
  border: 1px solid var(--color-gray-200);
}
.footer-left { display: flex; align-items: center; gap: 8px; }
.footer-right { display: flex; align-items: center; gap: 8px; }
.btn-danger-outline { padding: 6px 12px; border-radius: 4px; font-size: 12px; font-weight: 600; cursor: pointer; background: none; border: 1px solid #DC2626; color: #DC2626; }
.btn-danger-outline:hover { background: #FEE2E2; }

/* ── Buttons ──────────────────────────────────────────── */
.btn-primary {
  padding: 7px 16px; border-radius: 6px; font-size: 12px; font-weight: 600;
  cursor: pointer; border: none; background: var(--color-primary); color: white;
  transition: background 0.15s;
}
.btn-primary:hover { background: #1D4ED8; }

.btn-success {
  padding: 7px 16px; border-radius: 6px; font-size: 12px; font-weight: 600;
  cursor: pointer; border: none; background: var(--color-success); color: white;
  transition: background 0.15s;
}
.btn-success:hover { filter: brightness(0.9); }

.btn-ghost {
  padding: 7px 14px; border-radius: 6px; font-size: 12px; font-weight: 500;
  cursor: pointer; background: none; border: 1px solid var(--color-gray-300);
  color: var(--color-gray-600); transition: all 0.15s;
}
.btn-ghost:hover { background: var(--color-gray-50); border-color: var(--color-gray-400); }

.btn-action { background: none; border: none; font-size: 11px; cursor: pointer; color: var(--color-primary); padding: 2px 6px; font-weight: 600; }
.btn-action:hover { text-decoration: underline; }
.btn-action.danger { color: var(--color-danger); }

/* ── No spinners ──────────────────────────────────────── */
.no-spinners::-webkit-outer-spin-button,
.no-spinners::-webkit-inner-spin-button { -webkit-appearance: none; margin: 0; }
.no-spinners { -moz-appearance: textfield; }
</style>
