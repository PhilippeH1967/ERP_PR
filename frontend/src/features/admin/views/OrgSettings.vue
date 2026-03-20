<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/plugins/axios'

const router = useRouter()
const activeTab = ref('bu')
const isLoading = ref(true)

// Business Units
interface BU { id: number; name: string; code: string; is_active: boolean }
const bus = ref<BU[]>([])
const showBUForm = ref(false)
const editBUId = ref<number | null>(null)
const buForm = ref({ name: '', code: '' })

// Position Profiles
interface Position { id: number; name: string; code: string; category: string; hourly_cost_rate: string | null; is_active: boolean }
const positions = ref<Position[]>([])
const showPosForm = ref(false)
const editPosId = ref<number | null>(null)
const posForm = ref({ name: '', code: '', category: '', hourly_cost_rate: '' })

// Tax Configurations
interface TaxConfig { id: number; legal_entity: string; tps_rate: string; tvq_rate: string; is_active: boolean }
const taxes = ref<TaxConfig[]>([])
const showTaxForm = ref(false)
const editTaxId = ref<number | null>(null)
const taxForm = ref({ legal_entity: '', tps_rate: '5.000', tvq_rate: '9.975' })

// Labor Rules
interface LaborRule { id: number; name: string; weekly_hours: string; daily_hours: string; overtime_threshold_weekly: string; statutory_holidays: string[]; rest_days: number[]; is_active: boolean }
const rules = ref<LaborRule[]>([])
const showRuleForm = ref(false)
const editRuleId = ref<number | null>(null)
const ruleForm = ref({ name: '', weekly_hours: '40.0', daily_hours: '8.0', overtime_threshold_weekly: '40.0', overtime_threshold_daily: '8.0', statutory_holidays: '[]', rest_days: '[5, 6]' })

const error = ref('')

// Fetch all
async function fetchAll() {
  isLoading.value = true
  const endpoints = [
    { key: 'bu', url: 'business_units/' },
    { key: 'pos', url: 'position_profiles/' },
    { key: 'tax', url: 'tax_configurations/' },
    { key: 'rule', url: 'labor_rules/' },
  ]
  for (const ep of endpoints) {
    try {
      const r = await apiClient.get(ep.url)
      const d = r.data?.data || r.data
      const list = Array.isArray(d) ? d : d?.results || []
      if (ep.key === 'bu') bus.value = list
      if (ep.key === 'pos') positions.value = list
      if (ep.key === 'tax') taxes.value = list
      if (ep.key === 'rule') rules.value = list
    } catch { /* silent */ }
  }
  isLoading.value = false
}

// Generic CRUD helpers
async function saveBU() {
  error.value = ''
  try {
    if (editBUId.value) await apiClient.patch(`business_units/${editBUId.value}/`, buForm.value)
    else await apiClient.post('business_units/', buForm.value)
    showBUForm.value = false; editBUId.value = null; await fetchAll()
  } catch { error.value = 'Erreur' }
}
async function deleteBU(id: number) { await apiClient.delete(`business_units/${id}/`); await fetchAll() }
function editBU(b: BU) { editBUId.value = b.id; buForm.value = { name: b.name, code: b.code }; showBUForm.value = true }

async function savePos() {
  error.value = ''
  try {
    if (editPosId.value) await apiClient.patch(`position_profiles/${editPosId.value}/`, posForm.value)
    else await apiClient.post('position_profiles/', posForm.value)
    showPosForm.value = false; editPosId.value = null; await fetchAll()
  } catch { error.value = 'Erreur' }
}
async function deletePos(id: number) { await apiClient.delete(`position_profiles/${id}/`); await fetchAll() }
function editPos(p: Position) { editPosId.value = p.id; posForm.value = { name: p.name, code: p.code, category: p.category, hourly_cost_rate: p.hourly_cost_rate || '' }; showPosForm.value = true }

async function saveTax() {
  error.value = ''
  try {
    if (editTaxId.value) await apiClient.patch(`tax_configurations/${editTaxId.value}/`, taxForm.value)
    else await apiClient.post('tax_configurations/', taxForm.value)
    showTaxForm.value = false; editTaxId.value = null; await fetchAll()
  } catch { error.value = 'Erreur' }
}
async function deleteTax(id: number) { await apiClient.delete(`tax_configurations/${id}/`); await fetchAll() }
function editTax(t: TaxConfig) { editTaxId.value = t.id; taxForm.value = { legal_entity: t.legal_entity, tps_rate: t.tps_rate, tvq_rate: t.tvq_rate }; showTaxForm.value = true }

async function saveRule() {
  error.value = ''
  try {
    const data = {
      ...ruleForm.value,
      statutory_holidays: JSON.parse(ruleForm.value.statutory_holidays || '[]'),
      rest_days: JSON.parse(ruleForm.value.rest_days || '[5, 6]'),
    }
    if (editRuleId.value) await apiClient.patch(`labor_rules/${editRuleId.value}/`, data)
    else await apiClient.post('labor_rules/', data)
    showRuleForm.value = false; editRuleId.value = null; await fetchAll()
  } catch { error.value = 'Erreur — vérifiez le format JSON des congés/jours repos' }
}
async function deleteRule(id: number) { await apiClient.delete(`labor_rules/${id}/`); await fetchAll() }
function editRule(r: LaborRule) {
  editRuleId.value = r.id
  ruleForm.value = {
    name: r.name, weekly_hours: r.weekly_hours, daily_hours: r.daily_hours,
    overtime_threshold_weekly: r.overtime_threshold_weekly, overtime_threshold_daily: r.overtime_threshold_weekly,
    statutory_holidays: JSON.stringify(r.statutory_holidays), rest_days: JSON.stringify(r.rest_days),
  }
  showRuleForm.value = true
}

onMounted(fetchAll)
</script>

<template>
  <div>
    <div class="page-header">
      <div>
        <button class="btn-back" @click="router.push('/admin')">&larr; Administration</button>
        <h1>Organisation & Configuration</h1>
      </div>
    </div>

    <div v-if="error" class="alert-error">{{ error }} <button @click="error=''">×</button></div>

    <!-- Tabs -->
    <div class="tabs">
      <button :class="{ active: activeTab === 'bu' }" @click="activeTab = 'bu'">Unités d'affaires ({{ bus.length }})</button>
      <button :class="{ active: activeTab === 'positions' }" @click="activeTab = 'positions'">Profils de poste ({{ positions.length }})</button>
      <button :class="{ active: activeTab === 'taxes' }" @click="activeTab = 'taxes'">Taxes ({{ taxes.length }})</button>
      <button :class="{ active: activeTab === 'labor' }" @click="activeTab = 'labor'">Règles RH ({{ rules.length }})</button>
    </div>

    <div v-if="isLoading" class="loading">Chargement...</div>

    <!-- ═══ Business Units ═══ -->
    <template v-if="activeTab === 'bu' && !isLoading">
      <div class="section-actions"><button class="btn-primary" @click="showBUForm = true; editBUId = null; buForm = { name: '', code: '' }">+ Nouvelle unité</button></div>
      <div v-if="showBUForm" class="card form-card">
        <div class="form-row-2">
          <div class="form-group"><label>Nom *</label><input v-model="buForm.name" required /></div>
          <div class="form-group"><label>Code</label><input v-model="buForm.code" placeholder="ARCH" /></div>
        </div>
        <div class="form-actions"><button class="btn-ghost" @click="showBUForm = false">Annuler</button><button class="btn-primary" @click="saveBU">{{ editBUId ? 'Enregistrer' : 'Créer' }}</button></div>
      </div>
      <div class="card-table">
        <table>
          <thead><tr><th>Nom</th><th>Code</th><th style="text-align:right">Actions</th></tr></thead>
          <tbody>
            <tr v-for="b in bus" :key="b.id">
              <td class="font-semibold">{{ b.name }}</td>
              <td class="font-mono text-muted">{{ b.code || '—' }}</td>
              <td class="actions-cell"><button class="btn-action" @click="editBU(b)">Modifier</button><button class="btn-action danger" @click="deleteBU(b.id)">Supprimer</button></td>
            </tr>
            <tr v-if="!bus.length"><td colspan="3" class="empty">Aucune unité d'affaires</td></tr>
          </tbody>
        </table>
      </div>
    </template>

    <!-- ═══ Position Profiles ═══ -->
    <template v-if="activeTab === 'positions' && !isLoading">
      <div class="section-actions"><button class="btn-primary" @click="showPosForm = true; editPosId = null; posForm = { name: '', code: '', category: '', hourly_cost_rate: '' }">+ Nouveau profil</button></div>
      <div v-if="showPosForm" class="card form-card">
        <div class="form-row-4">
          <div class="form-group"><label>Nom *</label><input v-model="posForm.name" required /></div>
          <div class="form-group"><label>Code</label><input v-model="posForm.code" placeholder="ARCH" /></div>
          <div class="form-group"><label>Catégorie</label><input v-model="posForm.category" placeholder="Professionnel" /></div>
          <div class="form-group"><label>Taux horaire coût ($)</label><input v-model="posForm.hourly_cost_rate" type="number" step="0.01" /></div>
        </div>
        <div class="form-actions"><button class="btn-ghost" @click="showPosForm = false">Annuler</button><button class="btn-primary" @click="savePos">{{ editPosId ? 'Enregistrer' : 'Créer' }}</button></div>
      </div>
      <div class="card-table">
        <table>
          <thead><tr><th>Nom</th><th>Code</th><th>Catégorie</th><th>Taux horaire</th><th style="text-align:right">Actions</th></tr></thead>
          <tbody>
            <tr v-for="p in positions" :key="p.id">
              <td class="font-semibold">{{ p.name }}</td>
              <td class="font-mono text-muted">{{ p.code || '—' }}</td>
              <td>{{ p.category || '—' }}</td>
              <td class="font-mono">{{ p.hourly_cost_rate ? `${p.hourly_cost_rate} $` : '—' }}</td>
              <td class="actions-cell"><button class="btn-action" @click="editPos(p)">Modifier</button><button class="btn-action danger" @click="deletePos(p.id)">Supprimer</button></td>
            </tr>
            <tr v-if="!positions.length"><td colspan="5" class="empty">Aucun profil de poste</td></tr>
          </tbody>
        </table>
      </div>
    </template>

    <!-- ═══ Tax Configurations ═══ -->
    <template v-if="activeTab === 'taxes' && !isLoading">
      <div class="section-actions"><button class="btn-primary" @click="showTaxForm = true; editTaxId = null; taxForm = { legal_entity: '', tps_rate: '5.000', tvq_rate: '9.975' }">+ Nouvelle entité</button></div>
      <div v-if="showTaxForm" class="card form-card">
        <div class="form-row-3">
          <div class="form-group"><label>Entité juridique *</label><input v-model="taxForm.legal_entity" required placeholder="Provencher Roy Productions" /></div>
          <div class="form-group"><label>TPS (%)</label><input v-model="taxForm.tps_rate" type="number" step="0.001" /></div>
          <div class="form-group"><label>TVQ (%)</label><input v-model="taxForm.tvq_rate" type="number" step="0.001" /></div>
        </div>
        <div class="form-actions"><button class="btn-ghost" @click="showTaxForm = false">Annuler</button><button class="btn-primary" @click="saveTax">{{ editTaxId ? 'Enregistrer' : 'Créer' }}</button></div>
      </div>
      <div class="card-table">
        <table>
          <thead><tr><th>Entité juridique</th><th>TPS</th><th>TVQ</th><th style="text-align:right">Actions</th></tr></thead>
          <tbody>
            <tr v-for="t in taxes" :key="t.id">
              <td class="font-semibold">{{ t.legal_entity }}</td>
              <td class="font-mono">{{ t.tps_rate }}%</td>
              <td class="font-mono">{{ t.tvq_rate }}%</td>
              <td class="actions-cell"><button class="btn-action" @click="editTax(t)">Modifier</button><button class="btn-action danger" @click="deleteTax(t.id)">Supprimer</button></td>
            </tr>
            <tr v-if="!taxes.length"><td colspan="4" class="empty">Aucune configuration de taxes</td></tr>
          </tbody>
        </table>
      </div>
    </template>

    <!-- ═══ Labor Rules ═══ -->
    <template v-if="activeTab === 'labor' && !isLoading">
      <div class="section-actions"><button class="btn-primary" @click="showRuleForm = true; editRuleId = null; ruleForm = { name: '', weekly_hours: '40.0', daily_hours: '8.0', overtime_threshold_weekly: '40.0', overtime_threshold_daily: '8.0', statutory_holidays: '[]', rest_days: '[5, 6]' }">+ Nouvelle règle</button></div>
      <div v-if="showRuleForm" class="card form-card">
        <div class="form-row-3">
          <div class="form-group"><label>Nom *</label><input v-model="ruleForm.name" required placeholder="Québec standard" /></div>
          <div class="form-group"><label>Heures/semaine</label><input v-model="ruleForm.weekly_hours" type="number" step="0.5" /></div>
          <div class="form-group"><label>Heures/jour</label><input v-model="ruleForm.daily_hours" type="number" step="0.5" /></div>
        </div>
        <div class="form-row-2">
          <div class="form-group"><label>Seuil overtime hebdo</label><input v-model="ruleForm.overtime_threshold_weekly" type="number" step="0.5" /></div>
          <div class="form-group"><label>Seuil overtime quotidien</label><input v-model="ruleForm.overtime_threshold_daily" type="number" step="0.5" /></div>
        </div>
        <div class="form-row-2">
          <div class="form-group"><label>Congés statutaires (JSON)</label><input v-model="ruleForm.statutory_holidays" placeholder='["2026-01-01", "2026-07-01"]' /></div>
          <div class="form-group"><label>Jours de repos (JSON)</label><input v-model="ruleForm.rest_days" placeholder="[5, 6] = Sam/Dim" /></div>
        </div>
        <div class="form-actions"><button class="btn-ghost" @click="showRuleForm = false">Annuler</button><button class="btn-primary" @click="saveRule">{{ editRuleId ? 'Enregistrer' : 'Créer' }}</button></div>
      </div>
      <div class="card-table">
        <table>
          <thead><tr><th>Nom</th><th>Heures/sem</th><th>Heures/jour</th><th>Seuil OT</th><th>Congés</th><th style="text-align:right">Actions</th></tr></thead>
          <tbody>
            <tr v-for="r in rules" :key="r.id">
              <td class="font-semibold">{{ r.name }}</td>
              <td class="font-mono">{{ r.weekly_hours }}h</td>
              <td class="font-mono">{{ r.daily_hours }}h</td>
              <td class="font-mono">{{ r.overtime_threshold_weekly }}h</td>
              <td class="text-muted">{{ r.statutory_holidays?.length || 0 }} jours</td>
              <td class="actions-cell"><button class="btn-action" @click="editRule(r)">Modifier</button><button class="btn-action danger" @click="deleteRule(r.id)">Supprimer</button></td>
            </tr>
            <tr v-if="!rules.length"><td colspan="6" class="empty">Aucune règle RH</td></tr>
          </tbody>
        </table>
      </div>
    </template>
  </div>
</template>

<style scoped>
.page-header { display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 16px; }
.page-header h1 { font-size: 20px; font-weight: 700; color: var(--color-gray-900); margin-top: 2px; }
.btn-back { background: none; border: none; font-size: 12px; color: var(--color-gray-500); cursor: pointer; padding: 0; }
.alert-error { background: var(--color-danger-light); color: var(--color-danger); padding: 8px 12px; border-radius: 6px; font-size: 12px; margin-bottom: 12px; display: flex; justify-content: space-between; }
.loading { text-align: center; padding: 40px; color: var(--color-gray-500); font-size: 13px; }

.tabs { display: flex; gap: 0; border-bottom: 2px solid var(--color-gray-200); margin-bottom: 16px; }
.tabs button { padding: 8px 14px; font-size: 12px; font-weight: 500; color: var(--color-gray-500); cursor: pointer; border: none; background: none; border-bottom: 2px solid transparent; margin-bottom: -2px; }
.tabs button.active { color: var(--color-primary); border-bottom-color: var(--color-primary); font-weight: 600; }

.section-actions { margin-bottom: 10px; }
.card-table { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); overflow: hidden; }
.form-card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 16px; margin-bottom: 10px; }
.form-row-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.form-row-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; }
.form-row-4 { display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 12px; }
.form-group { margin-bottom: 8px; }
.form-group label { display: block; font-size: 11px; font-weight: 600; color: var(--color-gray-600); margin-bottom: 4px; }
.form-actions { display: flex; justify-content: flex-end; gap: 6px; margin-top: 8px; }
.font-mono { font-family: var(--font-mono); font-size: 12px; }
.text-muted { color: var(--color-gray-500); font-size: 12px; }
.actions-cell { text-align: right; white-space: nowrap; width: 1%; }
.btn-action { background: none; border: none; font-size: 11px; cursor: pointer; color: var(--color-primary); padding: 2px 6px; font-weight: 600; }
.btn-action:hover { text-decoration: underline; }
.btn-action.danger { color: var(--color-danger); }
.empty { text-align: center; padding: 24px; color: var(--color-gray-400); }
</style>
