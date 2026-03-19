<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useLocale } from '@/shared/composables/useLocale'
import { billingApi } from '../api/billingApi'

const { fmt } = useLocale()

interface Payment {
  id: number
  invoice: number
  amount: string
  payment_date: string
  reference: string
  method: string
}

const payments = ref<Payment[]>([])
const showCreate = ref(false)
const form = ref({ invoice: '', amount: '', payment_date: '', reference: '', method: 'CHEQUE' })
const error = ref('')

async function fetch() {
  try {
    const resp = await billingApi.listPayments()
    const data = resp.data?.data || resp.data
    payments.value = Array.isArray(data) ? data : data?.results || []
  } catch { payments.value = [] }
}

async function create() {
  error.value = ''
  try {
    await billingApi.createPayment({
      invoice: Number(form.value.invoice),
      amount: form.value.amount,
      payment_date: form.value.payment_date,
      reference: form.value.reference,
      method: form.value.method,
    })
    showCreate.value = false
    form.value = { invoice: '', amount: '', payment_date: '', reference: '', method: 'CHEQUE' }
    await fetch()
  } catch (e: unknown) {
    error.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur'
  }
}

onMounted(fetch)
</script>

<template>
  <div>
    <div class="page-header">
      <h1>Paiements reçus</h1>
      <button class="btn-primary" @click="showCreate = !showCreate">+ Enregistrer paiement</button>
    </div>

    <div v-if="showCreate" class="card" style="margin-bottom: 12px;">
      <div v-if="error" class="alert-error">{{ error }}</div>
      <form @submit.prevent="create" class="form-row-5">
        <div class="form-group"><label>Facture ID</label><input v-model="form.invoice" type="number" required /></div>
        <div class="form-group"><label>Montant</label><input v-model="form.amount" type="number" step="0.01" required /></div>
        <div class="form-group"><label>Date</label><input v-model="form.payment_date" type="date" required /></div>
        <div class="form-group"><label>Référence</label><input v-model="form.reference" type="text" /></div>
        <div class="form-group" style="display:flex;align-items:flex-end;gap:6px;">
          <select v-model="form.method" style="flex:1;"><option value="CHEQUE">Chèque</option><option value="VIREMENT">Virement</option><option value="CARTE">Carte</option></select>
          <button type="submit" class="btn-primary">Enregistrer</button>
          <button type="button" class="btn-ghost" @click="showCreate = false">Annuler</button>
        </div>
      </form>
    </div>

    <div class="card-table">
      <table>
        <thead><tr><th>Facture</th><th class="text-right">Montant</th><th>Date</th><th>Référence</th><th>Méthode</th></tr></thead>
        <tbody>
          <tr v-for="p in payments" :key="p.id">
            <td class="font-mono">Facture #{{ p.invoice }}</td>
            <td class="text-right font-mono font-semibold">{{ fmt.currency(p.amount) }}</td>
            <td class="text-muted">{{ fmt.date(p.payment_date) }}</td>
            <td class="text-muted">{{ p.reference || '—' }}</td>
            <td class="text-muted">{{ p.method }}</td>
          </tr>
          <tr v-if="!payments.length"><td colspan="5" class="empty">Aucun paiement</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.page-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }
.page-header h1 { font-size: 20px; font-weight: 700; color: var(--color-gray-900); }
.card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 16px; }
.card-table { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); overflow: hidden; }
.alert-error { background: var(--color-danger-light); color: var(--color-danger); padding: 8px; border-radius: 6px; font-size: 12px; margin-bottom: 10px; }
.form-row-5 { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; }
.form-group label { display: block; font-size: 11px; font-weight: 600; color: var(--color-gray-600); margin-bottom: 4px; }
.text-right { text-align: right; }
.text-muted { color: var(--color-gray-500); }
.font-mono { font-family: var(--font-mono); font-size: 12px; }
.empty { text-align: center; padding: 30px; color: var(--color-gray-400); }
</style>
