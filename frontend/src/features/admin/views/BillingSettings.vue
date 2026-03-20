<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/plugins/axios'

const router = useRouter()

interface InvoiceTemplate { id: number; name: string; description: string; is_active: boolean; template_config: Record<string, unknown> }
interface DunningLevel { id: number; level: number; days_overdue: number; email_template: string }

const templates = ref<InvoiceTemplate[]>([])
const dunningLevels = ref<DunningLevel[]>([])
const isLoading = ref(true)

// Template form
const showTmplForm = ref(false)
const editTmplId = ref<number | null>(null)
const tmplForm = ref({ name: '', description: '', template_config: '{}' })

// Dunning form
const showDunningForm = ref(false)
const editDunningId = ref<number | null>(null)
const dunningForm = ref({ level: '', days_overdue: '', email_template: '' })

const error = ref('')

async function fetchData() {
  isLoading.value = true
  try {
    const [t, d] = await Promise.allSettled([apiClient.get('invoice_templates/'), apiClient.get('dunning_levels/')])
    if (t.status === 'fulfilled') { const r = t.value.data?.data || t.value.data; templates.value = Array.isArray(r) ? r : r?.results || [] }
    if (d.status === 'fulfilled') { const r = d.value.data?.data || d.value.data; dunningLevels.value = Array.isArray(r) ? r : r?.results || [] }
  } finally { isLoading.value = false }
}

// Template CRUD
const defaultTemplateConfig = JSON.stringify({
  "sections": ["forfait", "horaire", "st", "depenses", "retenue", "taxes"],
  "logo": true,
  "banking_footer": true,
  "show_hours_detail": false
}, null, 2)
function openCreateTmpl() { editTmplId.value = null; tmplForm.value = { name: '', description: '', template_config: defaultTemplateConfig }; showTmplForm.value = true }
function openEditTmpl(t: InvoiceTemplate) { editTmplId.value = t.id; tmplForm.value = { name: t.name, description: t.description, template_config: JSON.stringify(t.template_config, null, 2) }; showTmplForm.value = true }
async function saveTmpl() {
  error.value = ''
  try {
    const data = { name: tmplForm.value.name, description: tmplForm.value.description, template_config: JSON.parse(tmplForm.value.template_config) }
    if (editTmplId.value) await apiClient.patch(`invoice_templates/${editTmplId.value}/`, data)
    else await apiClient.post('invoice_templates/', data)
    showTmplForm.value = false; await fetchData()
  } catch (e: unknown) { error.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur' }
}
const confirmDeleteTmpl = ref<number | null>(null)
async function deleteTmpl(id: number) { confirmDeleteTmpl.value = null; invoiceTemplates.value = invoiceTemplates.value.filter(t => t.id !== id); try { await apiClient.delete(`invoice_templates/${id}/`) } catch { /* ok */ } }

// Dunning CRUD
function openCreateDunning() { editDunningId.value = null; dunningForm.value = { level: '', days_overdue: '', email_template: '' }; showDunningForm.value = true }
function openEditDunning(d: DunningLevel) { editDunningId.value = d.id; dunningForm.value = { level: String(d.level), days_overdue: String(d.days_overdue), email_template: d.email_template }; showDunningForm.value = true }
async function saveDunning() {
  error.value = ''
  try {
    const data = { level: Number(dunningForm.value.level), days_overdue: Number(dunningForm.value.days_overdue), email_template: dunningForm.value.email_template }
    if (editDunningId.value) await apiClient.patch(`dunning_levels/${editDunningId.value}/`, data)
    else await apiClient.post('dunning_levels/', data)
    showDunningForm.value = false; await fetchData()
  } catch (e: unknown) { error.value = (e as { response?: { data?: { error?: { message?: string } } } }).response?.data?.error?.message || 'Erreur' }
}
const confirmDeleteDunning = ref<number | null>(null)
async function deleteDunning(id: number) { confirmDeleteDunning.value = null; dunningLevels.value = dunningLevels.value.filter(d => d.id !== id); try { await apiClient.delete(`dunning_levels/${id}/`) } catch { /* ok */ } }

onMounted(fetchData)
</script>

<template>
  <div>
    <div class="page-header">
      <div><button class="btn-back" @click="router.push('/admin')">&larr; Administration</button><h1>Paramètres de facturation</h1></div>
    </div>

    <div v-if="error" class="alert-error">{{ error }} <button @click="error=''">×</button></div>
    <div v-if="isLoading" class="loading">Chargement...</div>

    <template v-else>
      <!-- Invoice Templates -->
      <div class="card">
        <div class="card-header"><span class="card-title">Templates de facture</span><button class="btn-primary" @click="openCreateTmpl">+ Nouveau</button></div>
        <div v-if="showTmplForm" class="inline-form">
          <div class="form-row"><div class="form-group"><label>Nom</label><input v-model="tmplForm.name" required /></div><div class="form-group"><label>Description</label><input v-model="tmplForm.description" /></div></div>
          <div class="form-group"><label>Configuration (JSON)</label><textarea v-model="tmplForm.template_config" rows="6" class="mono-input" /><span class="field-hint">Sections possibles : forfait, horaire, st, depenses, retenue, taxes</span></div>
          <div class="form-actions"><button class="btn-ghost" @click="showTmplForm=false">Annuler</button><button class="btn-primary" @click="saveTmpl">{{ editTmplId ? 'Enregistrer' : 'Créer' }}</button></div>
        </div>
        <table v-if="templates.length">
          <thead><tr><th>Nom</th><th>Description</th><th>Sections</th><th>Statut</th><th></th></tr></thead>
          <tbody>
            <tr v-for="t in templates" :key="t.id">
              <td class="font-semibold">{{ t.name }}</td>
              <td class="text-muted">{{ t.description }}</td>
              <td><span v-for="s in ((t.template_config?.sections as string[]) || [])" :key="s" class="section-tag">{{ s }}</span></td>
              <td><span :class="t.is_active ? 'flag-yes' : 'flag-no'">{{ t.is_active ? 'Actif' : 'Inactif' }}</span></td>
              <td class="actions-cell">
                <button class="btn-action" @click="openEditTmpl(t)">Modifier</button>
                <template v-if="confirmDeleteTmpl === t.id"><button class="btn-action danger" @click="deleteTmpl(t.id)">Confirmer</button><button class="btn-action" @click="confirmDeleteTmpl = null">Annuler</button></template>
                <button v-else class="btn-action danger" @click="confirmDeleteTmpl = t.id">Supprimer</button>
              </td>
            </tr>
          </tbody>
        </table>
        <div v-else class="empty">Aucun template</div>
      </div>

      <!-- Dunning Levels -->
      <div class="card" style="margin-top: 16px;">
        <div class="card-header"><span class="card-title">Niveaux de relance</span><button class="btn-primary" @click="openCreateDunning">+ Nouveau</button></div>
        <div v-if="showDunningForm" class="inline-form">
          <div class="form-row-3">
            <div class="form-group"><label>Niveau</label><input v-model="dunningForm.level" type="number" required /></div>
            <div class="form-group"><label>Délai (jours)</label><input v-model="dunningForm.days_overdue" type="number" required /></div>
            <div class="form-group"><label>Template email</label><textarea v-model="dunningForm.email_template" rows="2" /><div style="margin-top:6px;display:flex;gap:4px;justify-content:flex-end;"><button class="btn-ghost" @click="showDunningForm=false">Annuler</button><button class="btn-primary" @click="saveDunning">{{ editDunningId ? 'Enregistrer' : 'Créer' }}</button></div></div>
          </div>
        </div>
        <table v-if="dunningLevels.length">
          <thead><tr><th>Niveau</th><th>Délai</th><th>Template email</th><th></th></tr></thead>
          <tbody>
            <tr v-for="d in dunningLevels" :key="d.id">
              <td class="font-semibold">Niveau {{ d.level }}</td>
              <td>{{ d.days_overdue }} jours</td>
              <td class="text-muted template-cell">{{ d.email_template?.substring(0, 80) }}{{ d.email_template?.length > 80 ? '...' : '' }}</td>
              <td class="actions-cell">
                <button class="btn-action" @click="openEditDunning(d)">Modifier</button>
                <template v-if="confirmDeleteDunning === d.id"><button class="btn-action danger" @click="deleteDunning(d.id)">Confirmer</button><button class="btn-action" @click="confirmDeleteDunning = null">Annuler</button></template>
                <button v-else class="btn-action danger" @click="confirmDeleteDunning = d.id">Supprimer</button>
              </td>
            </tr>
          </tbody>
        </table>
        <div v-else class="empty">Aucun niveau de relance</div>
      </div>

      <!-- Taxes link -->
      <div class="card" style="margin-top: 16px;">
        <div class="card-title">Taxes</div>
        <p class="info-note">Les schémas fiscaux (TPS+TVQ, TVH, etc.) sont configurables dans <a href="/admin/org" style="color:var(--color-primary);">Organisation → Schémas fiscaux</a>.</p>
      </div>
    </template>
  </div>
</template>

<style scoped>
.page-header { display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 16px; }
.page-header h1 { font-size: 20px; font-weight: 700; color: var(--color-gray-900); margin-top: 2px; }
.btn-back { background: none; border: none; font-size: 12px; color: var(--color-gray-500); cursor: pointer; padding: 0; }
.loading { text-align: center; padding: 40px; color: var(--color-gray-500); font-size: 13px; }
.alert-error { background: var(--color-danger-light); color: var(--color-danger); padding: 8px 12px; border-radius: 6px; font-size: 12px; margin-bottom: 12px; display: flex; justify-content: space-between; }
.card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 16px; }
.card-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid var(--color-gray-100); }
.card-title { font-size: 14px; font-weight: 600; color: var(--color-gray-800); }
.inline-form { padding: 12px; background: var(--color-gray-50); border-radius: 6px; margin-bottom: 12px; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; } .form-row-3 { display: grid; grid-template-columns: 1fr 1fr 2fr; gap: 10px; }
.form-group { margin-bottom: 10px; } .form-group label { display: block; font-size: 11px; font-weight: 600; color: var(--color-gray-600); margin-bottom: 4px; }
.form-group textarea { width: 100%; padding: 6px 10px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 13px; font-family: inherit; }
.mono-input { font-family: var(--font-mono); font-size: 11px; }
.form-actions { display: flex; justify-content: flex-end; gap: 6px; }
.text-muted { color: var(--color-gray-500); font-size: 12px; }
.section-tag { display: inline-flex; padding: 1px 6px; border-radius: 3px; font-size: 10px; font-weight: 600; background: var(--color-gray-100); color: var(--color-gray-600); margin-right: 3px; }
.flag-yes { font-size: 11px; font-weight: 600; color: #15803D; } .flag-no { font-size: 11px; color: var(--color-gray-400); }
.actions-cell { text-align: right; white-space: nowrap; }
.btn-action { background: none; border: none; font-size: 11px; cursor: pointer; color: var(--color-primary); padding: 2px 6px; font-weight: 600; } .btn-action:hover { text-decoration: underline; } .btn-action.danger { color: var(--color-danger); }
.template-cell { max-width: 250px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.empty { text-align: center; padding: 24px; color: var(--color-gray-400); font-size: 13px; }
.tax-grid { display: flex; gap: 24px; } .tax-label { font-size: 11px; font-weight: 600; color: var(--color-gray-500); text-transform: uppercase; display: block; } .tax-value { font-size: 20px; font-weight: 700; font-family: var(--font-mono); color: var(--color-gray-800); }
.info-note { font-size: 12px; color: var(--color-gray-500); }
.field-hint { display: block; font-size: 10px; color: var(--color-gray-400); margin-top: 2px; }
</style>
