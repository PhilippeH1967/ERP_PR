<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { supplierApi } from '../api/supplierApi'

const countries = [
  { code: 'CA', name: 'Canada' },
  { code: 'US', name: 'États-Unis' },
  { code: 'FR', name: 'France' },
  { code: 'BE', name: 'Belgique' },
  { code: 'CH', name: 'Suisse' },
  { code: 'OTHER', name: 'Autre' },
]
const provincesByCountry: Record<string, string[]> = {
  CA: ['Alberta', 'Colombie-Britannique', 'Île-du-Prince-Édouard', 'Manitoba', 'Nouveau-Brunswick', 'Nouvelle-Écosse', 'Ontario', 'Québec', 'Saskatchewan', 'Terre-Neuve-et-Labrador', 'Territoires du Nord-Ouest', 'Nunavut', 'Yukon'],
  US: ['Alabama', 'Alaska', 'Arizona', 'California', 'Colorado', 'Connecticut', 'Florida', 'Georgia', 'Illinois', 'Massachusetts', 'Michigan', 'New York', 'Ohio', 'Pennsylvania', 'Texas', 'Washington', 'Autre'],
  FR: ['Île-de-France', 'Auvergne-Rhône-Alpes', 'Nouvelle-Aquitaine', 'Occitanie', 'Provence-Alpes-Côte d\'Azur', 'Bretagne', 'Autre'],
}
const editCountryCode = ref('CA')
const editProvinces = computed(() => provincesByCountry[editCountryCode.value] || [])

const route = useRoute()
const router = useRouter()
const orgId = Number(route.params.id)

interface BankingInfo { institution?: string; transit?: string; account?: string }
interface Org {
  id: number; name: string; neq: string; address: string; city: string; province: string
  postal_code: string; country: string; contact_name: string; contact_email: string; contact_phone: string
  type_tags: string[]; banking_info: BankingInfo; is_active: boolean
}

const org = ref<Org | null>(null)
const editing = ref(false)
const showDeleteConfirm = ref(false)
const form = ref<Partial<Org>>({})
const error = ref('')

async function fetch() {
  const resp = await supplierApi.getOrganization(orgId)
  org.value = resp.data?.data || resp.data
}

function toggleEditTag(tag: string) {
  const tags = (form.value.type_tags as string[]) || []
  const idx = tags.indexOf(tag)
  if (idx >= 0) tags.splice(idx, 1)
  else tags.push(tag)
  form.value.type_tags = [...tags]
}

function startEdit() {
  form.value = { ...org.value, banking_info: { ...(org.value?.banking_info || {}) } }
  // Resolve country code from name
  const match = countries.find(c => c.name === org.value?.country)
  editCountryCode.value = match?.code || 'OTHER'
  editing.value = true
}

function onEditCountryChange() {
  const country = countries.find(c => c.code === editCountryCode.value)
  form.value.country = country?.name || editCountryCode.value
  form.value.province = editProvinces.value[0] || ''
}

async function save() {
  error.value = ''
  if (!form.value.name?.trim()) {
    error.value = 'Le nom est obligatoire.'
    return
  }
  try {
    await supplierApi.updateOrganization(orgId, form.value)
    editing.value = false
    await fetch()
  } catch (e: unknown) {
    const err = e as { response?: { data?: { error?: { message?: string; details?: Array<{ message?: string }> } } } }
    error.value = err.response?.data?.error?.details?.[0]?.message || err.response?.data?.error?.message || 'Erreur'
  }
}

async function remove() {
  showDeleteConfirm.value = false
  try {
    const { default: apiClient } = await import('@/plugins/axios')
    await apiClient.delete(`external_organizations/${orgId}/`)
  } catch { /* ok */ }
  router.push('/suppliers')
}

function stopEditing() {
  editing.value = false
  showDeleteConfirm.value = false
}

onMounted(fetch)
</script>

<template>
  <div v-if="org">
    <div class="page-header">
      <div>
        <button class="btn-back" @click="router.push('/suppliers')">&larr; Fournisseurs</button>
        <h1>{{ org.name }}</h1>
        <p class="subtitle">NEQ: {{ org.neq || '—' }} · {{ org.city }}, {{ org.province }}</p>
      </div>
      <div class="header-actions">
        <span v-for="tag in org.type_tags" :key="tag" class="badge" :class="tag === 'st' ? 'badge-blue' : tag === 'partner' ? 'badge-purple' : 'badge-gray'">
          {{ tag === 'st' ? 'Sous-traitant' : tag === 'partner' ? 'Partenaire' : 'Concurrent' }}
        </span>
        <button v-if="!editing" class="btn-primary" @click="startEdit">Modifier</button>
        <button v-if="editing" class="btn-ghost" @click="stopEditing">Terminer</button>
        <button v-if="editing" class="btn-danger" @click="showDeleteConfirm = true">Supprimer...</button>
      </div>
    </div>

    <div v-if="error" class="alert-error">{{ error }}</div>

    <!-- Delete confirm banner -->
    <div v-if="showDeleteConfirm" class="alert-danger-banner">
      Supprimer définitivement cette organisation ?
      <div class="banner-actions">
        <button class="btn-danger" @click="remove">Confirmer la suppression</button>
        <button class="btn-ghost" @click="showDeleteConfirm = false">Annuler</button>
      </div>
    </div>

    <!-- View mode -->
    <template v-if="!editing">
      <div class="info-grid">
        <div class="card">
          <h3 class="card-title">Identification</h3>
          <div class="info-pairs">
            <div><span>Nom</span><p>{{ org.name }}</p></div>
            <div><span>NEQ</span><p>{{ org.neq || '—' }}</p></div>
            <div><span>Adresse</span><p>{{ org.address || '—' }}</p></div>
            <div><span>Ville</span><p>{{ org.city || '—' }}, {{ org.province || '—' }} {{ org.postal_code || '' }}</p></div>
            <div><span>Pays</span><p>{{ org.country || '—' }}</p></div>
            <div><span>Rôles</span>
              <p>
                <span v-for="tag in org.type_tags" :key="tag" class="badge" :class="tag === 'st' ? 'badge-blue' : tag === 'partner' ? 'badge-purple' : 'badge-gray'" style="margin-right: 4px;">
                  {{ tag === 'st' ? 'Sous-traitant' : tag === 'partner' ? 'Partenaire' : 'Concurrent' }}
                </span>
                <span v-if="!org.type_tags?.length">—</span>
              </p>
            </div>
          </div>
        </div>
        <div class="card">
          <h3 class="card-title">Contact principal</h3>
          <div class="info-pairs single">
            <div><span>Nom</span><p>{{ org.contact_name || '—' }}</p></div>
            <div><span>Email</span><p>{{ org.contact_email || '—' }}</p></div>
            <div><span>Téléphone</span><p>{{ org.contact_phone || '—' }}</p></div>
          </div>
        </div>
      </div>
      <div v-if="org.banking_info?.institution || org.banking_info?.transit || org.banking_info?.account" class="card" style="margin-top: 12px;">
        <h3 class="card-title">Coordonnées bancaires</h3>
        <div class="info-pairs">
          <div><span>Institution</span><p>{{ org.banking_info?.institution || '—' }}</p></div>
          <div><span>Transit</span><p>{{ org.banking_info?.transit || '—' }}</p></div>
          <div><span>Compte</span><p>{{ org.banking_info?.account || '—' }}</p></div>
        </div>
      </div>
    </template>

    <!-- Edit mode -->
    <template v-if="editing">
      <div class="card">
        <h3 class="card-title">Modifier l'organisation</h3>
        <div class="form-grid">
          <div class="form-group"><label>Nom</label><input v-model="form.name" /></div>
          <div class="form-group"><label>NEQ</label><input v-model="form.neq" /></div>
          <div class="form-group"><label>Adresse</label><input v-model="form.address" /></div>
          <div class="form-group"><label>Ville</label><input v-model="form.city" /></div>
          <div class="form-group"><label>Code postal</label><input v-model="form.postal_code" /></div>
          <div class="form-group">
            <label>Pays</label>
            <select v-model="editCountryCode" @change="onEditCountryChange" class="form-select">
              <option v-for="c in countries" :key="c.code" :value="c.code">{{ c.name }}</option>
            </select>
          </div>
          <div class="form-group">
            <label>Province / État</label>
            <select v-if="editProvinces.length" v-model="form.province" class="form-select">
              <option v-for="p in editProvinces" :key="p" :value="p">{{ p }}</option>
            </select>
            <input v-else v-model="form.province" placeholder="Province / État" />
          </div>
          <div class="form-group form-group-wide">
            <label>Rôles</label>
            <div class="tag-selector">
              <button v-for="tag in ['st', 'partner', 'competitor']" :key="tag" type="button"
                class="tag-btn" :class="(form.type_tags as string[] || []).includes(tag) ? 'tag-active' : ''"
                @click="toggleEditTag(tag)">
                {{ tag === 'st' ? 'Sous-traitant' : tag === 'partner' ? 'Partenaire' : 'Concurrent' }}
              </button>
            </div>
          </div>
          <div class="form-group"><label>Contact nom</label><input v-model="form.contact_name" /></div>
          <div class="form-group"><label>Contact email</label><input v-model="form.contact_email" /></div>
          <div class="form-group"><label>Contact téléphone</label><input v-model="form.contact_phone" /></div>
          <div class="form-group"><label>Banque — Institution</label><input v-model="(form.banking_info as BankingInfo).institution" placeholder="815" /></div>
          <div class="form-group"><label>Banque — Transit</label><input v-model="(form.banking_info as BankingInfo).transit" placeholder="30000" /></div>
          <div class="form-group"><label>Banque — Compte</label><input v-model="(form.banking_info as BankingInfo).account" placeholder="1234567" /></div>
        </div>
        <div class="form-actions">
          <button class="btn-ghost" @click="editing = false">Annuler</button>
          <button class="btn-primary" @click="save">Enregistrer</button>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
.page-header { display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 16px; }
.page-header h1 { font-size: 20px; font-weight: 700; color: var(--color-gray-900); margin-top: 2px; }
.btn-back { background: none; border: none; font-size: 12px; color: var(--color-gray-500); cursor: pointer; padding: 0; }
.subtitle { font-size: 12px; color: var(--color-gray-500); }
.header-actions { display: flex; align-items: center; gap: 6px; }
.btn-danger { padding: 4px 10px; border-radius: 4px; font-size: 11px; font-weight: 600; cursor: pointer; border: none; background: var(--color-danger); color: white; }
.alert-error { background: var(--color-danger-light); color: var(--color-danger); padding: 8px 12px; border-radius: 6px; font-size: 12px; margin-bottom: 12px; }
.alert-danger-banner { background: #FEE2E2; color: #DC2626; padding: 12px 16px; border-radius: 6px; font-size: 13px; font-weight: 600; margin-bottom: 12px; }
.banner-actions { display: flex; gap: 8px; margin-top: 8px; }
.badge { display: inline-flex; padding: 2px 10px; border-radius: 10px; font-size: 10px; font-weight: 600; }
.badge-blue { background: #DBEAFE; color: #1D4ED8; } .badge-purple { background: #EDE9FE; color: #7C3AED; } .badge-gray { background: var(--color-gray-100); color: var(--color-gray-500); }
.info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 16px; }
.card-title { font-size: 11px; font-weight: 600; color: var(--color-gray-400); text-transform: uppercase; margin-bottom: 12px; }
.info-pairs { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 13px; } .info-pairs.single { grid-template-columns: 1fr; }
.info-pairs span { color: var(--color-gray-500); font-size: 11px; } .info-pairs p { font-weight: 600; margin-top: 1px; }
.form-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; }
.form-group { margin-bottom: 8px; } .form-group label { display: block; font-size: 11px; font-weight: 600; color: var(--color-gray-600); margin-bottom: 4px; }
.form-select { width: 100%; padding: 6px 10px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 13px; font-family: inherit; }
.form-group-wide { grid-column: span 3; }
.tag-selector { display: flex; gap: 6px; }
.tag-btn { padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 600; cursor: pointer; border: 1px solid var(--color-gray-300); background: white; color: var(--color-gray-500); transition: all 0.15s; }
.tag-btn.tag-active { border-color: var(--color-primary); background: var(--color-primary-light); color: var(--color-primary); }
.form-actions { display: flex; justify-content: flex-end; gap: 6px; margin-top: 12px; }
</style>
