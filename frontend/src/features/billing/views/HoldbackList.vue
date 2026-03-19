<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useLocale } from '@/shared/composables/useLocale'
import { billingApi } from '../api/billingApi'

const { fmt } = useLocale()

interface Holdback { id: number; invoice: number; project: number; percentage: string; accumulated: string; released: string; remaining: string; status: string; created_at: string }

const items = ref<Holdback[]>([])
const showCreate = ref(false)
const form = ref({ invoice: '', percentage: '10', project: '' })
const error = ref('')

async function fetch() {
  try { const r = await billingApi.listHoldbacks(); const d = r.data?.data || r.data; items.value = Array.isArray(d) ? d : d?.results || [] } catch { items.value = [] }
}

async function create() {
  error.value = ''
  try {
    await billingApi.createHoldback({ invoice: Number(form.value.invoice), percentage: form.value.percentage, project: Number(form.value.project) })
    showCreate.value = false; form.value = { invoice: '', percentage: '10', project: '' }; await fetch()
  } catch (e: unknown) { error.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur' }
}

async function remove(id: number) { if (!confirm('Supprimer cette retenue ?')) return; await billingApi.deleteHoldback(id); await fetch() }

onMounted(fetch)
</script>

<template>
  <div>
    <div class="page-header"><h1>Retenues (Holdbacks)</h1><button class="btn-primary" @click="showCreate = !showCreate">+ Nouvelle retenue</button></div>

    <div v-if="showCreate" class="card" style="margin-bottom: 12px;">
      <div v-if="error" class="alert-error">{{ error }}</div>
      <form @submit.prevent="create" class="form-row-3">
        <div class="form-group"><label>Facture ID</label><input v-model="form.invoice" type="number" required /></div>
        <div class="form-group"><label>Projet ID</label><input v-model="form.project" type="number" /></div>
        <div class="form-group"><label>Pourcentage (%)</label><input v-model="form.percentage" type="number" step="0.1" required /><div style="margin-top:6px;display:flex;gap:6px;justify-content:flex-end;"><button type="button" class="btn-ghost" @click="showCreate=false">Annuler</button><button type="submit" class="btn-primary">Créer</button></div></div>
      </form>
    </div>

    <div class="card-table">
      <table>
        <thead><tr><th>Facture</th><th>Projet</th><th class="text-right">%</th><th class="text-right">Accumulé</th><th class="text-right">Libéré</th><th class="text-right">Restant</th><th>Statut</th><th></th></tr></thead>
        <tbody>
          <tr v-for="h in items" :key="h.id">
            <td class="font-mono">#{{ h.invoice }}</td>
            <td class="font-mono">#{{ h.project }}</td>
            <td class="text-right font-mono">{{ h.percentage }}%</td>
            <td class="text-right font-mono">{{ fmt.currency(h.accumulated || '0') }}</td>
            <td class="text-right font-mono success">{{ fmt.currency(h.released || '0') }}</td>
            <td class="text-right font-mono font-semibold">{{ fmt.currency(h.remaining || '0') }}</td>
            <td><span class="badge badge-amber">{{ h.status || 'ACTIVE' }}</span></td>
            <td><button class="btn-icon-danger" @click="remove(h.id)">Supprimer</button></td>
          </tr>
          <tr v-if="!items.length"><td colspan="8" class="empty">Aucune retenue</td></tr>
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
.form-row-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; }
.form-group label { display: block; font-size: 11px; font-weight: 600; color: var(--color-gray-600); margin-bottom: 4px; }
.text-right { text-align: right; } .font-mono { font-family: var(--font-mono); font-size: 12px; }
.success { color: var(--color-success); } .empty { text-align: center; padding: 30px; color: var(--color-gray-400); }
.badge { display: inline-flex; padding: 1px 8px; border-radius: 10px; font-size: 10px; font-weight: 600; }
.badge-amber { background: #FEF3C7; color: #92400E; }
.btn-icon-danger { background: none; border: none; font-size: 11px; cursor: pointer; color: var(--color-danger); }
</style>
