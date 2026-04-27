<script setup lang="ts">
/**
 * TaxSchemeManager — composant partagé de gestion des schémas fiscaux.
 *
 * Utilisé dans /admin/org et /admin/billing pour permettre la création
 * et la modification des schémas (TPS+TVQ, TVH, etc.) et de leurs taux
 * sans passer par l'admin Django.
 */
import { onMounted, ref } from 'vue'
import apiClient from '@/plugins/axios'

interface TaxRateItem {
  id: number
  tax_type: string
  label: string
  rate: string
  is_active: boolean
}

interface TaxScheme {
  id: number
  name: string
  province: string
  description: string
  is_default: boolean
  is_active: boolean
  rates: TaxRateItem[]
}

const schemes = ref<TaxScheme[]>([])
const isLoading = ref(true)
const error = ref('')

const showSchemeForm = ref(false)
const editSchemeId = ref<number | null>(null)
const schemeForm = ref({ name: '', province: '', description: '' })

const showRateForm = ref<number | null>(null)
const rateForm = ref({ tax_type: 'TPS', rate: '5.000', label: '' })
const editingRate = ref<{ id: number; rate: string } | null>(null)

const confirmDeleteScheme = ref<number | null>(null)
const confirmDeleteRate = ref<{ schemeId: number; rateId: number } | null>(null)

const taxTypes = [
  { value: 'TPS', label: 'TPS (Taxe fédérale)' },
  { value: 'TVQ', label: 'TVQ (Taxe Québec)' },
  { value: 'TVH', label: 'TVH (Taxe harmonisée)' },
  { value: 'GST', label: 'GST (Federal)' },
  { value: 'PST', label: 'PST (Provincial)' },
  { value: 'HST', label: 'HST (Harmonized)' },
  { value: 'OTHER', label: 'Autre' },
]

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

async function fetchSchemes() {
  isLoading.value = true
  try {
    const r = await apiClient.get('tax_schemes/')
    const d = r.data?.data || r.data
    schemes.value = Array.isArray(d) ? d : d?.results || []
  } catch (e: unknown) {
    error.value = extractError(e)
  } finally {
    isLoading.value = false
  }
}

function openCreateScheme() {
  editSchemeId.value = null
  schemeForm.value = { name: '', province: '', description: '' }
  showSchemeForm.value = true
}

function openEditScheme(s: TaxScheme) {
  editSchemeId.value = s.id
  schemeForm.value = { name: s.name, province: s.province, description: s.description }
  showSchemeForm.value = true
}

async function saveScheme() {
  error.value = ''
  if (!schemeForm.value.name.trim()) {
    error.value = 'Le nom est obligatoire'
    return
  }
  try {
    if (editSchemeId.value) {
      await apiClient.patch(`tax_schemes/${editSchemeId.value}/`, schemeForm.value)
    } else {
      await apiClient.post('tax_schemes/', schemeForm.value)
    }
    showSchemeForm.value = false
    editSchemeId.value = null
    await fetchSchemes()
  } catch (e: unknown) {
    error.value = extractError(e)
  }
}

async function deleteScheme(id: number) {
  if (confirmDeleteScheme.value !== id) {
    confirmDeleteScheme.value = id
    return
  }
  confirmDeleteScheme.value = null
  schemes.value = schemes.value.filter(s => s.id !== id)
  try {
    await apiClient.delete(`tax_schemes/${id}/`)
  } catch (e: unknown) {
    error.value = extractError(e)
    await fetchSchemes()
  }
}

function openAddRate(schemeId: number) {
  showRateForm.value = schemeId
  rateForm.value = { tax_type: 'TPS', rate: '5.000', label: '' }
}

async function addRate(schemeId: number) {
  error.value = ''
  try {
    await apiClient.post(`tax_schemes/${schemeId}/rates/`, rateForm.value)
    showRateForm.value = null
    await fetchSchemes()
  } catch (e: unknown) {
    error.value = extractError(e)
  }
}

function startEditRate(r: TaxRateItem) {
  editingRate.value = { id: r.id, rate: r.rate }
}

async function saveRate(schemeId: number) {
  if (!editingRate.value) return
  try {
    await apiClient.patch(
      `tax_schemes/${schemeId}/rates/${editingRate.value.id}/`,
      { rate: editingRate.value.rate },
    )
    editingRate.value = null
    await fetchSchemes()
  } catch (e: unknown) {
    error.value = extractError(e)
  }
}

async function deleteRate(schemeId: number, rateId: number) {
  if (
    !confirmDeleteRate.value
    || confirmDeleteRate.value.schemeId !== schemeId
    || confirmDeleteRate.value.rateId !== rateId
  ) {
    confirmDeleteRate.value = { schemeId, rateId }
    return
  }
  confirmDeleteRate.value = null
  try {
    await apiClient.delete(`tax_schemes/${schemeId}/rates/${rateId}/`)
    await fetchSchemes()
  } catch (e: unknown) {
    error.value = extractError(e)
  }
}

onMounted(fetchSchemes)
</script>

<template>
  <div class="card">
    <div class="card-header">
      <span class="card-title">Schémas fiscaux</span>
      <button class="btn-primary" data-add-scheme @click="openCreateScheme">
        + Nouveau schéma
      </button>
    </div>

    <div v-if="error" class="alert-error">
      {{ error }}
      <button type="button" @click="error = ''">×</button>
    </div>

    <!-- Scheme form (create / edit) -->
    <div v-if="showSchemeForm" class="inline-form" data-scheme-form>
      <h4 class="form-title">{{ editSchemeId ? 'Modifier le schéma' : 'Nouveau schéma fiscal' }}</h4>
      <div class="form-row">
        <div class="form-group">
          <label>Nom *</label>
          <input v-model="schemeForm.name" data-scheme-name placeholder="ex. Québec — TPS+TVQ" />
        </div>
        <div class="form-group">
          <label>Province</label>
          <input v-model="schemeForm.province" data-scheme-province placeholder="ex. QC" />
        </div>
      </div>
      <div class="form-group">
        <label>Description</label>
        <input v-model="schemeForm.description" placeholder="Description optionnelle" />
      </div>
      <p class="hint">Après création, ajoute les taux (TPS 5%, TVQ 9.975%, etc.) via le bouton "+ Taux".</p>
      <div class="form-actions">
        <button class="btn-ghost" @click="showSchemeForm = false; editSchemeId = null">Annuler</button>
        <button class="btn-primary" data-save-scheme @click="saveScheme">
          {{ editSchemeId ? 'Enregistrer' : 'Créer' }}
        </button>
      </div>
    </div>

    <div v-if="isLoading" class="empty">Chargement…</div>
    <div v-else-if="!schemes.length" class="empty">
      Aucun schéma fiscal. Crée le premier avec « + Nouveau schéma » ci-dessus.
    </div>

    <!-- Schemes list -->
    <div v-for="s in schemes" :key="s.id" class="scheme-block" data-scheme-row>
      <div class="scheme-header">
        <div>
          <span class="scheme-name">{{ s.name }}</span>
          <span v-if="s.province" class="scheme-province">{{ s.province }}</span>
          <span v-if="s.is_default" class="badge badge-primary">Par défaut</span>
          <span v-if="!s.is_active" class="badge badge-muted">Inactif</span>
        </div>
        <div class="scheme-actions">
          <button class="btn-action" @click="openEditScheme(s)">Modifier</button>
          <template v-if="confirmDeleteScheme === s.id">
            <button class="btn-action danger" data-delete-scheme-confirm @click="deleteScheme(s.id)">Confirmer</button>
            <button class="btn-action" @click="confirmDeleteScheme = null">Annuler</button>
          </template>
          <button v-else class="btn-action danger" data-delete-scheme @click="deleteScheme(s.id)">Supprimer…</button>
        </div>
      </div>

      <div v-if="s.description" class="scheme-desc">{{ s.description }}</div>

      <table class="rates-table">
        <thead>
          <tr>
            <th>Type</th>
            <th>Libellé</th>
            <th class="text-right">Taux (%)</th>
            <th class="text-right">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in s.rates" :key="r.id" data-rate-row>
            <td><span class="rate-type">{{ r.tax_type }}</span></td>
            <td>{{ r.label || '—' }}</td>
            <td class="text-right font-mono">
              <template v-if="editingRate?.id === r.id">
                <input
                  v-model="editingRate.rate"
                  type="number"
                  step="0.001"
                  min="0"
                  class="rate-input"
                  data-edit-rate-input
                />
              </template>
              <template v-else>{{ r.rate }}</template>
            </td>
            <td class="text-right">
              <template v-if="editingRate?.id === r.id">
                <button class="btn-action" data-save-rate @click="saveRate(s.id)">Enregistrer</button>
                <button class="btn-action" @click="editingRate = null">Annuler</button>
              </template>
              <template v-else>
                <button class="btn-action" data-edit-rate @click="startEditRate(r)">Modifier</button>
                <template v-if="confirmDeleteRate?.schemeId === s.id && confirmDeleteRate?.rateId === r.id">
                  <button class="btn-action danger" data-delete-rate-confirm @click="deleteRate(s.id, r.id)">Confirmer</button>
                  <button class="btn-action" @click="confirmDeleteRate = null">Annuler</button>
                </template>
                <button v-else class="btn-action danger" data-delete-rate @click="deleteRate(s.id, r.id)">Supprimer…</button>
              </template>
            </td>
          </tr>
          <tr v-if="!s.rates?.length">
            <td colspan="4" class="empty-rates">Aucun taux — ajoute TPS et TVQ ci-dessous</td>
          </tr>
        </tbody>
      </table>

      <!-- Rate form -->
      <div v-if="showRateForm === s.id" class="rate-form" data-rate-form>
        <select v-model="rateForm.tax_type" class="rate-select">
          <option v-for="t in taxTypes" :key="t.value" :value="t.value">{{ t.label }}</option>
        </select>
        <input
          v-model="rateForm.rate"
          type="number"
          step="0.001"
          min="0"
          placeholder="Taux %"
          class="rate-input"
          data-rate-rate
        />
        <input
          v-model="rateForm.label"
          placeholder="Libellé (optionnel)"
          class="rate-label"
        />
        <button class="btn-primary btn-sm" data-add-rate @click="addRate(s.id)">Ajouter</button>
        <button class="btn-ghost btn-sm" @click="showRateForm = null">Annuler</button>
      </div>
      <button v-else class="btn-add-rate" data-show-rate-form @click="openAddRate(s.id)">
        + Taux
      </button>
    </div>
  </div>
</template>

<style scoped>
.card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 16px; }
.card-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid var(--color-gray-100); }
.card-title { font-size: 14px; font-weight: 600; color: var(--color-gray-800); }

.btn-primary { background: var(--color-primary); color: white; border: none; padding: 6px 12px; border-radius: 4px; font-size: 12px; font-weight: 600; cursor: pointer; }
.btn-primary:hover { filter: brightness(0.95); }
.btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-ghost { background: none; border: 1px solid var(--color-gray-300); color: var(--color-gray-700); padding: 6px 12px; border-radius: 4px; font-size: 12px; cursor: pointer; }
.btn-sm { padding: 4px 10px; font-size: 11px; }

.alert-error { background: #FEE2E2; color: #B91C1C; padding: 8px 12px; border-radius: 6px; font-size: 12px; margin-bottom: 12px; display: flex; justify-content: space-between; }
.alert-error button { background: none; border: none; cursor: pointer; color: inherit; font-size: 14px; }

.inline-form { padding: 12px; background: var(--color-gray-50); border-radius: 6px; margin-bottom: 12px; }
.form-title { font-size: 13px; font-weight: 600; margin-bottom: 8px; color: var(--color-gray-800); }
.form-row { display: grid; grid-template-columns: 2fr 1fr; gap: 10px; }
.form-group { margin-bottom: 10px; }
.form-group label { display: block; font-size: 11px; font-weight: 600; color: var(--color-gray-600); margin-bottom: 4px; }
.form-group input { width: 100%; padding: 6px 10px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 13px; }
.hint { font-size: 11px; color: var(--color-gray-500); font-style: italic; margin: 6px 0; }
.form-actions { display: flex; justify-content: flex-end; gap: 6px; margin-top: 8px; }

.empty { text-align: center; padding: 24px; color: var(--color-gray-400); font-size: 13px; }

.scheme-block { padding: 12px; background: var(--color-gray-50); border-radius: 6px; margin-bottom: 12px; border: 1px solid var(--color-gray-200); }
.scheme-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.scheme-name { font-weight: 600; font-size: 14px; color: var(--color-gray-800); }
.scheme-province { font-size: 11px; color: var(--color-gray-500); margin-left: 8px; padding: 2px 6px; background: var(--color-gray-200); border-radius: 3px; }
.scheme-actions { display: flex; gap: 4px; }
.scheme-desc { font-size: 12px; color: var(--color-gray-600); margin-bottom: 8px; }

.badge { display: inline-flex; padding: 2px 8px; border-radius: 10px; font-size: 10px; font-weight: 600; margin-left: 8px; }
.badge-primary { background: var(--color-primary-light); color: var(--color-primary); }
.badge-muted { background: var(--color-gray-200); color: var(--color-gray-600); }

.rates-table { width: 100%; font-size: 12px; border-collapse: collapse; margin-bottom: 8px; }
.rates-table thead th { padding: 6px 10px; font-weight: 600; color: var(--color-gray-600); font-size: 10px; text-align: left; background: white; border-bottom: 1px solid var(--color-gray-200); }
.rates-table tbody td { padding: 6px 10px; border-bottom: 1px solid var(--color-gray-100); background: white; }
.rate-type { font-weight: 600; color: var(--color-primary); font-family: var(--font-mono); }
.text-right { text-align: right; }
.font-mono { font-family: var(--font-mono); }
.empty-rates { text-align: center; color: var(--color-gray-400); font-style: italic; }

.rate-form { display: flex; gap: 6px; padding: 8px; background: white; border-radius: 4px; margin-bottom: 6px; }
.rate-select { padding: 4px 8px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 12px; min-width: 180px; }
.rate-input { padding: 4px 8px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 12px; width: 90px; font-family: var(--font-mono); }
.rate-label { padding: 4px 8px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 12px; flex: 1; }

.btn-action { background: none; border: none; font-size: 11px; cursor: pointer; color: var(--color-primary); padding: 2px 6px; font-weight: 600; }
.btn-action:hover { text-decoration: underline; }
.btn-action.danger { color: var(--color-danger); }
.btn-add-rate { background: none; border: 1px dashed var(--color-gray-400); color: var(--color-primary); padding: 5px 12px; border-radius: 4px; font-size: 11px; cursor: pointer; font-weight: 600; }
.btn-add-rate:hover { background: var(--color-primary-light); border-color: var(--color-primary); }
</style>
