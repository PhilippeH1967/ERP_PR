<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/plugins/axios'

const router = useRouter()

interface LeaveType {
  id: number
  code: string
  name: string
  name_en: string
  is_paid: boolean
  requires_medical_cert: boolean
  medical_cert_threshold_days: number
  max_days_per_year: string | null
  accrual_rate_monthly: string
  can_carry_over: boolean
  carry_over_max_days: string | null
  is_active: boolean
  order: number
}

const types = ref<LeaveType[]>([])
const isLoading = ref(true)
const showForm = ref(false)
const editingId = ref<number | null>(null)
const error = ref('')
const confirmDeleteId = ref<number | null>(null)
const seedingNow = ref(false)

const form = ref({
  code: '',
  name: '',
  name_en: '',
  is_paid: true,
  requires_medical_cert: false,
  medical_cert_threshold_days: 3,
  max_days_per_year: '',
  accrual_rate_monthly: '0',
  can_carry_over: false,
  carry_over_max_days: '',
  is_active: true,
  order: 0,
})

function extractError(e: unknown): string {
  const data = (e as { response?: { data?: unknown } }).response?.data
  if (!data || typeof data !== 'object') return 'Erreur'
  const obj = data as Record<string, unknown>
  const errObj = obj.error as { message?: string } | undefined
  if (errObj?.message) return errObj.message
  const parts: string[] = []
  for (const [field, val] of Object.entries(obj)) {
    if (Array.isArray(val)) parts.push(`${field}: ${val.join(', ')}`)
    else if (typeof val === 'string') parts.push(`${field}: ${val}`)
  }
  return parts.length ? parts.join(' · ') : 'Erreur'
}

async function fetchTypes() {
  isLoading.value = true
  try {
    const r = await apiClient.get('leave_types/')
    const d = r.data?.data || r.data
    types.value = Array.isArray(d) ? d : d?.results || []
  } catch (e: unknown) {
    error.value = extractError(e)
  } finally {
    isLoading.value = false
  }
}

function openCreate() {
  editingId.value = null
  form.value = {
    code: '', name: '', name_en: '',
    is_paid: true, requires_medical_cert: false, medical_cert_threshold_days: 3,
    max_days_per_year: '', accrual_rate_monthly: '0',
    can_carry_over: false, carry_over_max_days: '',
    is_active: true, order: 0,
  }
  showForm.value = true
}

function openEdit(t: LeaveType) {
  editingId.value = t.id
  form.value = {
    code: t.code, name: t.name, name_en: t.name_en,
    is_paid: t.is_paid,
    requires_medical_cert: t.requires_medical_cert,
    medical_cert_threshold_days: t.medical_cert_threshold_days,
    max_days_per_year: t.max_days_per_year ?? '',
    accrual_rate_monthly: t.accrual_rate_monthly,
    can_carry_over: t.can_carry_over,
    carry_over_max_days: t.carry_over_max_days ?? '',
    is_active: t.is_active,
    order: t.order,
  }
  showForm.value = true
}

async function save() {
  error.value = ''
  if (!form.value.code.trim() || !form.value.name.trim()) {
    error.value = 'Code et nom sont obligatoires.'
    return
  }
  const payload: Record<string, unknown> = {
    code: form.value.code.trim(),
    name: form.value.name.trim(),
    name_en: form.value.name_en,
    is_paid: form.value.is_paid,
    requires_medical_cert: form.value.requires_medical_cert,
    medical_cert_threshold_days: Number(form.value.medical_cert_threshold_days) || 0,
    max_days_per_year: form.value.max_days_per_year === '' ? null : Number(form.value.max_days_per_year),
    accrual_rate_monthly: form.value.accrual_rate_monthly,
    can_carry_over: form.value.can_carry_over,
    carry_over_max_days: form.value.carry_over_max_days === '' ? null : Number(form.value.carry_over_max_days),
    is_active: form.value.is_active,
    order: Number(form.value.order) || 0,
  }
  try {
    if (editingId.value) {
      await apiClient.patch(`leave_types/${editingId.value}/`, payload)
    } else {
      await apiClient.post('leave_types/', payload)
    }
    showForm.value = false
    editingId.value = null
    await fetchTypes()
  } catch (e: unknown) {
    error.value = extractError(e)
  }
}

async function deleteType(id: number) {
  if (confirmDeleteId.value !== id) {
    confirmDeleteId.value = id
    return
  }
  confirmDeleteId.value = null
  types.value = types.value.filter(t => t.id !== id)
  try {
    await apiClient.delete(`leave_types/${id}/`)
  } catch (e: unknown) {
    error.value = extractError(e)
    await fetchTypes()
  }
}

async function seedDefaults() {
  if (!confirm('Créer les 7 types de congé standards Québec (Vacances, Maladie, Personnel, Férié, Parental, Sans solde, Deuil) ?')) return
  seedingNow.value = true
  error.value = ''
  try {
    await apiClient.post('leave_types/seed/')
    await fetchTypes()
  } catch (e: unknown) {
    error.value = extractError(e)
  } finally {
    seedingNow.value = false
  }
}

onMounted(fetchTypes)
</script>

<template>
  <div>
    <div class="page-header">
      <div>
        <button class="btn-back" @click="router.push('/admin')">&larr; Administration</button>
        <h1>Types de congés</h1>
      </div>
      <div class="flex gap-2">
        <button
          v-if="!types.length && !isLoading"
          class="btn-secondary"
          data-seed-defaults
          :disabled="seedingNow"
          @click="seedDefaults"
        >
          {{ seedingNow ? '…' : 'Charger les types Québec standard' }}
        </button>
        <button class="btn-primary" data-add-type @click="openCreate">+ Nouveau type</button>
      </div>
    </div>

    <p class="page-intro">
      Configure les types de congés disponibles (vacances, maladie, personnel, etc.).
      Chaque type peut avoir un quota annuel, un taux d'accumulation mensuel, et un
      report d'année en année.
    </p>

    <div v-if="error" class="alert-error">{{ error }} <button @click="error=''">×</button></div>
    <div v-if="isLoading" class="loading">Chargement…</div>

    <template v-else>
      <!-- Form -->
      <div v-if="showForm" class="form-card" data-leave-form>
        <h3 class="form-title">{{ editingId ? 'Modifier le type' : 'Nouveau type de congé' }}</h3>
        <div class="form-grid">
          <div class="form-group">
            <label>Code *</label>
            <input v-model="form.code" data-form-code placeholder="ex. VAC, MAL, PERS" />
          </div>
          <div class="form-group">
            <label>Nom (FR) *</label>
            <input v-model="form.name" data-form-name placeholder="Vacances annuelles" />
          </div>
          <div class="form-group">
            <label>Nom (EN)</label>
            <input v-model="form.name_en" placeholder="Annual leave" />
          </div>
          <div class="form-group">
            <label>Ordre d'affichage</label>
            <input v-model="form.order" type="number" min="0" />
          </div>
          <div class="form-group">
            <label>Quota annuel (jours)</label>
            <input v-model="form.max_days_per_year" type="number" step="0.5" min="0" placeholder="Vide = illimité" />
          </div>
          <div class="form-group">
            <label>Accumulation mensuelle (j/mois)</label>
            <input v-model="form.accrual_rate_monthly" type="number" step="0.01" min="0" placeholder="0 = alloué d'un coup" />
          </div>
          <div class="form-group">
            <label>Report max (jours)</label>
            <input v-model="form.carry_over_max_days" type="number" step="0.5" min="0" :disabled="!form.can_carry_over" />
          </div>
          <div class="form-group">
            <label>Délai certificat médical (jours)</label>
            <input v-model="form.medical_cert_threshold_days" type="number" min="0" :disabled="!form.requires_medical_cert" />
          </div>
        </div>
        <div class="checkbox-row">
          <label><input v-model="form.is_paid" type="checkbox" /> Payé</label>
          <label><input v-model="form.requires_medical_cert" type="checkbox" /> Certificat médical requis</label>
          <label><input v-model="form.can_carry_over" type="checkbox" /> Reportable</label>
          <label><input v-model="form.is_active" type="checkbox" /> Actif</label>
        </div>
        <div class="form-actions">
          <button class="btn-ghost" @click="showForm = false; editingId = null">Annuler</button>
          <button class="btn-primary" data-save @click="save">{{ editingId ? 'Enregistrer' : 'Créer' }}</button>
        </div>
      </div>

      <!-- Empty state -->
      <div v-if="!types.length" class="empty-card">
        <p>Aucun type de congé configuré.</p>
        <p class="hint">
          Tu peux soit cliquer sur <strong>"Charger les types Québec standard"</strong> pour seeder
          les 7 types courants, soit créer manuellement chaque type avec <strong>"+ Nouveau type"</strong>.
        </p>
      </div>

      <!-- Table -->
      <table v-else class="data-table" data-types-table>
        <thead>
          <tr>
            <th>Code</th>
            <th>Nom (FR)</th>
            <th>Quota / an</th>
            <th>Accrual</th>
            <th>Payé</th>
            <th>Cert. médical</th>
            <th>Statut</th>
            <th class="text-right">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="t in types" :key="t.id" data-type-row>
            <td class="font-mono font-semibold">{{ t.code }}</td>
            <td>
              {{ t.name }}
              <span v-if="t.name_en" class="text-muted">({{ t.name_en }})</span>
            </td>
            <td class="font-mono">{{ t.max_days_per_year ?? '—' }}</td>
            <td class="font-mono">{{ t.accrual_rate_monthly }}/mois</td>
            <td class="text-center">{{ t.is_paid ? '✓' : '—' }}</td>
            <td class="text-center">
              <span v-if="t.requires_medical_cert">✓ ({{ t.medical_cert_threshold_days }}j)</span>
              <span v-else>—</span>
            </td>
            <td>
              <span :class="t.is_active ? 'badge-active' : 'badge-inactive'">
                {{ t.is_active ? 'Actif' : 'Inactif' }}
              </span>
            </td>
            <td class="text-right">
              <button class="btn-action" @click="openEdit(t)">Modifier</button>
              <template v-if="confirmDeleteId === t.id">
                <button class="btn-action danger" data-delete-confirm @click="deleteType(t.id)">Confirmer</button>
                <button class="btn-action" @click="confirmDeleteId = null">Annuler</button>
              </template>
              <button v-else class="btn-action danger" data-delete @click="deleteType(t.id)">Supprimer…</button>
            </td>
          </tr>
        </tbody>
      </table>
    </template>
  </div>
</template>

<style scoped>
.page-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 8px; }
.page-header h1 { font-size: 20px; font-weight: 700; margin-top: 4px; color: var(--color-gray-900); }
.btn-back { background: none; border: none; font-size: 12px; color: var(--color-gray-500); cursor: pointer; padding: 0; }
.page-intro { font-size: 13px; color: var(--color-gray-600); margin-bottom: 16px; line-height: 1.5; }

.btn-primary { background: var(--color-primary); color: white; border: none; padding: 6px 12px; border-radius: 4px; font-size: 12px; font-weight: 600; cursor: pointer; }
.btn-primary:hover:not(:disabled) { filter: brightness(0.95); }
.btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-secondary { background: white; color: var(--color-gray-700); border: 1px solid var(--color-gray-300); padding: 6px 12px; border-radius: 4px; font-size: 12px; font-weight: 600; cursor: pointer; }
.btn-secondary:hover:not(:disabled) { background: var(--color-gray-50); }
.btn-ghost { background: none; border: 1px solid var(--color-gray-300); color: var(--color-gray-700); padding: 6px 12px; border-radius: 4px; font-size: 12px; cursor: pointer; }
.btn-action { background: none; border: none; font-size: 11px; cursor: pointer; color: var(--color-primary); padding: 2px 6px; font-weight: 600; }
.btn-action:hover { text-decoration: underline; }
.btn-action.danger { color: var(--color-danger); }

.alert-error { background: #FEE2E2; color: #B91C1C; padding: 8px 12px; border-radius: 6px; font-size: 12px; margin-bottom: 12px; display: flex; justify-content: space-between; }
.alert-error button { background: none; border: none; cursor: pointer; color: inherit; font-size: 14px; }
.loading { text-align: center; padding: 40px; color: var(--color-gray-500); font-size: 13px; }

.form-card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 16px; margin-bottom: 16px; }
.form-title { font-size: 14px; font-weight: 600; margin-bottom: 12px; color: var(--color-gray-800); }
.form-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 12px; }
.form-group label { display: block; font-size: 11px; font-weight: 600; color: var(--color-gray-600); margin-bottom: 4px; }
.form-group input { width: 100%; padding: 6px 10px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 13px; }
.checkbox-row { display: flex; gap: 16px; padding: 8px 0; flex-wrap: wrap; font-size: 13px; }
.checkbox-row label { display: flex; align-items: center; gap: 6px; cursor: pointer; }
.form-actions { display: flex; justify-content: flex-end; gap: 6px; padding-top: 12px; border-top: 1px solid var(--color-gray-100); margin-top: 12px; }

.empty-card { text-align: center; padding: 40px 20px; background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.empty-card p { color: var(--color-gray-600); font-size: 13px; }
.hint { font-size: 12px; color: var(--color-gray-500); margin-top: 8px; line-height: 1.5; }

.data-table { width: 100%; background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); border-collapse: collapse; font-size: 12px; }
.data-table thead th { padding: 10px 12px; font-weight: 600; color: var(--color-gray-600); font-size: 11px; text-align: left; background: var(--color-gray-50); border-bottom: 1px solid var(--color-gray-200); }
.data-table tbody td { padding: 8px 12px; border-bottom: 1px solid var(--color-gray-100); }
.font-mono { font-family: var(--font-mono); }
.font-semibold { font-weight: 600; }
.text-muted { color: var(--color-gray-500); font-size: 11px; }
.text-center { text-align: center; }
.text-right { text-align: right; }
.flex { display: flex; }
.gap-2 { gap: 8px; }
.badge-active { display: inline-flex; padding: 1px 8px; border-radius: 10px; font-size: 10px; font-weight: 600; background: #DCFCE7; color: #15803D; }
.badge-inactive { display: inline-flex; padding: 1px 8px; border-radius: 10px; font-size: 10px; font-weight: 600; background: var(--color-gray-200); color: var(--color-gray-600); }
</style>
