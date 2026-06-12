<script setup lang="ts">
/**
 * HolidaySettings — paramétrage des jours fériés (Administration, admin).
 * Les fériés varient selon le régime de travail (LaborRule = lieu/province) :
 * un férié peut viser un régime précis ou « Tous les régimes ». Dans la grille
 * de temps, le férié est pré-rempli au max d'heures/jour de chaque employé.
 */
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/plugins/axios'

const router = useRouter()

interface Holiday { id: number; name: string; date: string; is_paid: boolean; labor_rule: number | null; labor_rule_name: string }
interface Rule { id: number; name: string }

const holidays = ref<Holiday[]>([])
const rules = ref<Rule[]>([])
const isLoading = ref(true)

function arr(d: unknown): unknown[] {
  const x = (d as { data?: unknown })?.data ?? d
  return Array.isArray(x) ? x : (x as { results?: unknown[] })?.results || []
}

async function fetchAll() {
  isLoading.value = true
  try {
    const [hr, rr] = await Promise.all([
      apiClient.get('public_holidays/', { params: { page_size: '500' } }),
      apiClient.get('labor_rules/', { params: { page_size: '200' } }),
    ])
    holidays.value = (arr(hr.data) as Holiday[]).sort((a, b) => a.date.localeCompare(b.date))
    rules.value = arr(rr.data) as Rule[]
  } catch {
    holidays.value = []
    rules.value = []
  } finally {
    isLoading.value = false
  }
}
onMounted(fetchAll)

const byYear = computed(() => {
  const groups: Record<string, Holiday[]> = {}
  for (const h of holidays.value) {
    const y = h.date.slice(0, 4)
    if (!groups[y]) groups[y] = []
    groups[y].push(h)
  }
  return groups
})

/* ── Form (création / édition) ── */
const showForm = ref(false)
const editingId = ref<number | null>(null)
const saveError = ref('')
const form = ref({ name: '', date: '', labor_rule: '' as string, is_paid: true })

function openCreate() {
  editingId.value = null
  saveError.value = ''
  form.value = { name: '', date: '', labor_rule: '', is_paid: true }
  showForm.value = true
}
function openEdit(h: Holiday) {
  editingId.value = h.id
  saveError.value = ''
  form.value = { name: h.name, date: h.date, labor_rule: h.labor_rule != null ? String(h.labor_rule) : '', is_paid: h.is_paid }
  showForm.value = true
}
async function save() {
  saveError.value = ''
  if (!form.value.name.trim() || !form.value.date) {
    saveError.value = 'Le nom et la date sont obligatoires.'
    return
  }
  const payload = {
    name: form.value.name.trim(),
    date: form.value.date,
    is_paid: form.value.is_paid,
    labor_rule: form.value.labor_rule ? Number(form.value.labor_rule) : null,
  }
  try {
    if (editingId.value) await apiClient.patch(`public_holidays/${editingId.value}/`, payload)
    else await apiClient.post('public_holidays/', payload)
    showForm.value = false
    editingId.value = null
    await fetchAll()
  } catch (e: unknown) {
    const err = (e as { response?: { data?: { error?: { message?: string; details?: Array<{ message?: string }> } } } }).response?.data?.error
    saveError.value = err?.details?.[0]?.message || err?.message || 'Erreur de sauvegarde'
  }
}

const confirmDeleteId = ref<number | null>(null)
async function remove(id: number) {
  confirmDeleteId.value = null
  holidays.value = holidays.value.filter(h => h.id !== id) // optimiste
  try { await apiClient.delete(`public_holidays/${id}/`) } catch { await fetchAll() }
}
</script>

<template>
  <div>
    <div class="page-header">
      <div>
        <button class="btn-back" @click="router.push('/admin')">&larr; Administration</button>
        <h1>Jours fériés</h1>
      </div>
    </div>

    <p class="hint">
      Fériés par <strong>régime de travail</strong> (lieu/province — les régimes définissent aussi les heures/jour).
      Dans la grille de temps, chaque férié est <strong>pré-rempli</strong> sur la tâche « Férié » au maximum
      d'heures/jour de l'employé (son contrat personnel prime). Un férié « Tous les régimes » s'applique à tout le monde.
    </p>

    <div class="actions-bar">
      <span class="count">{{ holidays.length }} férié{{ holidays.length > 1 ? 's' : '' }}</span>
      <button class="btn-primary" data-hol-add @click="openCreate">+ Nouveau férié</button>
    </div>

    <div v-if="isLoading" class="loading">Chargement…</div>
    <template v-else>
      <div v-for="(list, year) in byYear" :key="year" class="card" style="margin-bottom:10px;">
        <h3 class="year-title">{{ year }}</h3>
        <table>
          <thead><tr><th style="width:110px;">Date</th><th>Nom</th><th>Régime (lieu)</th><th style="width:60px;">Payé</th><th style="width:170px;"></th></tr></thead>
          <tbody>
            <tr v-for="h in list" :key="h.id" data-hol-row>
              <td class="mono">{{ h.date }}</td>
              <td class="name-cell">{{ h.name }}</td>
              <td>{{ h.labor_rule ? h.labor_rule_name : 'Tous les régimes' }}</td>
              <td><span :class="h.is_paid ? 'flag-yes' : 'flag-no'">{{ h.is_paid ? 'Oui' : 'Non' }}</span></td>
              <td class="actions-cell">
                <button class="btn-icon" @click="openEdit(h)">Modifier</button>
                <template v-if="confirmDeleteId === h.id">
                  <button class="btn-icon btn-icon-danger" data-hol-delete-confirm @click="remove(h.id)">Confirmer</button>
                  <button class="btn-icon" @click="confirmDeleteId = null">Annuler</button>
                </template>
                <button v-else class="btn-icon btn-icon-danger" data-hol-delete @click="confirmDeleteId = h.id">Supprimer…</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-if="!holidays.length" class="card"><div class="empty">Aucun jour férié — cliquez « + Nouveau férié ».</div></div>
    </template>

    <div v-if="showForm" class="modal-overlay" @click.self="showForm = false">
      <div class="modal">
        <div class="modal-header">
          <h2>{{ editingId ? 'Modifier le férié' : 'Nouveau férié' }}</h2>
          <button class="modal-close" @click="showForm = false">&times;</button>
        </div>
        <div class="modal-body">
          <div v-if="saveError" class="alert-error" style="margin-bottom:10px;">{{ saveError }}</div>
          <div class="form-group">
            <label>Nom *</label>
            <input v-model="form.name" type="text" data-hol-name placeholder="Ex : Fête nationale" />
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Date *</label>
              <input v-model="form.date" type="date" data-hol-date />
            </div>
            <div class="form-group">
              <label>Régime (lieu de travail)</label>
              <select v-model="form.labor_rule" data-hol-rule>
                <option value="">Tous les régimes</option>
                <option v-for="r in rules" :key="r.id" :value="String(r.id)">{{ r.name }}</option>
              </select>
            </div>
          </div>
          <label class="checkbox-label"><input v-model="form.is_paid" type="checkbox" /> Payé (pré-rempli dans la feuille de temps)</label>
          <div class="form-actions">
            <button type="button" class="btn-ghost" @click="showForm = false">Annuler</button>
            <button type="button" class="btn-primary" data-hol-save @click="save">{{ editingId ? 'Enregistrer' : 'Créer' }}</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-header { display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 16px; }
.page-header h1 { font-size: 20px; font-weight: 700; color: var(--color-gray-900); margin-top: 2px; }
.btn-back { background: none; border: none; font-size: 12px; color: var(--color-gray-500); cursor: pointer; padding: 0; }
.btn-back:hover { color: var(--color-primary); }
.hint { font-size: 12px; color: var(--color-gray-600); margin: 0 0 14px; max-width: 90ch; }
.actions-bar { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
.count { font-size: 12px; color: var(--color-gray-500); }
.loading { text-align: center; padding: 40px; color: var(--color-gray-500); font-size: 13px; }
.card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); overflow: hidden; }
.year-title { font-size: 13px; font-weight: 800; color: var(--color-gray-800); padding: 10px 12px 0; margin: 0; }
table { width: 100%; border-collapse: collapse; }
th { background: var(--color-gray-50); padding: 7px 10px; text-align: left; font-size: 10px; font-weight: 600; color: var(--color-gray-500); text-transform: uppercase; border-bottom: 2px solid var(--color-gray-200); }
td { padding: 8px 10px; border-bottom: 1px solid var(--color-gray-100); font-size: 13px; }
.mono { font-family: var(--font-mono, monospace); font-size: 12px; }
.name-cell { font-weight: 600; color: var(--color-gray-800); }
.flag-yes { font-size: 11px; font-weight: 600; color: #15803D; }
.flag-no { font-size: 11px; color: var(--color-gray-400); }
.actions-cell { text-align: right; white-space: nowrap; }
.btn-primary { padding: 6px 12px; border-radius: 4px; font-size: 12px; font-weight: 600; cursor: pointer; border: none; background: var(--color-primary); color: white; }
.btn-ghost { padding: 6px 12px; border-radius: 4px; font-size: 12px; cursor: pointer; background: transparent; color: var(--color-gray-600); border: 1px solid var(--color-gray-300); }
.btn-icon { background: none; border: none; font-size: 11px; cursor: pointer; color: var(--color-primary); padding: 2px 6px; }
.btn-icon:hover { text-decoration: underline; }
.btn-icon-danger { color: var(--color-danger); }
.empty { text-align: center; padding: 30px; color: var(--color-gray-400); font-size: 13px; }
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.3); z-index: 8000; display: flex; align-items: flex-start; justify-content: center; padding-top: 80px; }
.modal { background: white; border-radius: 8px; box-shadow: 0 10px 15px rgba(0,0,0,0.1); width: 100%; max-width: 460px; }
.modal-header { padding: 14px 20px; border-bottom: 1px solid var(--color-gray-200); display: flex; align-items: center; justify-content: space-between; }
.modal-header h2 { font-size: 15px; font-weight: 600; color: var(--color-gray-800); }
.modal-close { background: none; border: none; font-size: 22px; cursor: pointer; color: var(--color-gray-400); }
.modal-body { padding: 20px; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.form-group { margin-bottom: 14px; }
.form-group label { display: block; font-size: 11px; font-weight: 600; color: var(--color-gray-600); margin-bottom: 4px; }
.form-group input, .form-group select { width: 100%; padding: 6px 10px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 13px; box-sizing: border-box; }
.checkbox-label { display: flex; align-items: center; gap: 6px; font-size: 13px; color: var(--color-gray-700); cursor: pointer; }
.form-actions { display: flex; justify-content: flex-end; gap: 6px; margin-top: 16px; padding-top: 12px; border-top: 1px solid var(--color-gray-200); }
.alert-error { background: #fde8e4; color: var(--color-danger); padding: 8px 12px; border-radius: 6px; font-size: 12px; }
</style>
