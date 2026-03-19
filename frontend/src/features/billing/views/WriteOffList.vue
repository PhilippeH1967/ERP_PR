<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useLocale } from '@/shared/composables/useLocale'
import { billingApi } from '../api/billingApi'

const { fmt } = useLocale()

interface WriteOff { id: number; invoice: number; amount: string; justification: string; created_at: string }

const items = ref<WriteOff[]>([])
const showCreate = ref(false)
const form = ref({ invoice: '', amount: '', justification: '' })
const error = ref('')

async function fetch() {
  try { const r = await billingApi.listWriteOffs(); const d = r.data?.data || r.data; items.value = Array.isArray(d) ? d : d?.results || [] } catch { items.value = [] }
}

async function create() {
  error.value = ''
  try {
    await billingApi.createWriteOff({ invoice: Number(form.value.invoice), amount: form.value.amount, justification: form.value.justification })
    showCreate.value = false; form.value = { invoice: '', amount: '', justification: '' }; await fetch()
  } catch (e: unknown) { error.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur' }
}

async function remove(id: number) { if (!confirm('Supprimer ?')) return; await billingApi.deleteWriteOff(id); await fetch() }

onMounted(fetch)
</script>

<template>
  <div>
    <div class="page-header"><h1>Radiations (Write-offs)</h1><button class="btn-primary" @click="showCreate = !showCreate">+ Nouvelle radiation</button></div>

    <div v-if="showCreate" class="card" style="margin-bottom: 12px;">
      <div v-if="error" class="alert-error">{{ error }}</div>
      <form @submit.prevent="create" class="form-row-3">
        <div class="form-group"><label>Facture ID</label><input v-model="form.invoice" type="number" required /></div>
        <div class="form-group"><label>Montant</label><input v-model="form.amount" type="number" step="0.01" required /></div>
        <div class="form-group"><label>Justification</label><input v-model="form.justification" type="text" required /><div style="margin-top:6px;display:flex;gap:6px;justify-content:flex-end;"><button type="button" class="btn-ghost" @click="showCreate=false">Annuler</button><button type="submit" class="btn-primary">Créer</button></div></div>
      </form>
    </div>

    <div class="card-table">
      <table>
        <thead><tr><th>Facture</th><th class="text-right">Montant</th><th>Justification</th><th>Date</th><th></th></tr></thead>
        <tbody>
          <tr v-for="w in items" :key="w.id">
            <td class="font-mono">#{{ w.invoice }}</td>
            <td class="text-right font-mono danger">{{ fmt.currency(w.amount) }}</td>
            <td>{{ w.justification }}</td>
            <td class="text-muted">{{ w.created_at?.substring(0, 10) }}</td>
            <td><button class="btn-icon-danger" @click="remove(w.id)">Supprimer</button></td>
          </tr>
          <tr v-if="!items.length"><td colspan="5" class="empty">Aucune radiation</td></tr>
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
.form-row-3 { display: grid; grid-template-columns: 1fr 1fr 2fr; gap: 10px; }
.form-group label { display: block; font-size: 11px; font-weight: 600; color: var(--color-gray-600); margin-bottom: 4px; }
.text-right { text-align: right; } .text-muted { color: var(--color-gray-500); }
.font-mono { font-family: var(--font-mono); font-size: 12px; } .danger { color: var(--color-danger); }
.empty { text-align: center; padding: 30px; color: var(--color-gray-400); }
.btn-icon-danger { background: none; border: none; font-size: 11px; cursor: pointer; color: var(--color-danger); }
</style>
