<script setup lang="ts">
import { ref, computed } from 'vue'
import SlideOver from '@/shared/components/SlideOver.vue'
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

const selectedCountryCode = ref('CA')
const provinces = computed(() => provincesByCountry[selectedCountryCode.value] || [])

defineProps<{ open: boolean }>()
const emit = defineEmits<{ close: []; created: [] }>()

const isSubmitting = ref(false)
const error = ref('')

interface Duplicate { id: number; name: string; neq: string; match_type: string }
const duplicates = ref<Duplicate[]>([])
const showDuplicateWarning = ref(false)

const form = ref({
  name: '',
  neq: '',
  address: '',
  city: '',
  province: 'Québec',
  postal_code: '',
  country: 'Canada',
  contact_name: '',
  contact_email: '',
  contact_phone: '',
  type_tags: [] as string[],
})

function onCountryChange() {
  const country = countries.find(c => c.code === selectedCountryCode.value)
  form.value.country = country?.name || selectedCountryCode.value
  form.value.province = provinces.value[0] || ''
}

const tagOptions = ['st', 'partner', 'competitor']
const tagLabels: Record<string, string> = { st: 'Sous-traitant', partner: 'Partenaire', competitor: 'Concurrent' }

function toggleTag(tag: string) {
  const idx = form.value.type_tags.indexOf(tag)
  if (idx >= 0) form.value.type_tags.splice(idx, 1)
  else form.value.type_tags.push(tag)
}

async function checkDuplicates() {
  if (!form.value.name.trim() && !form.value.neq.trim()) return
  try {
    const resp = await supplierApi.checkDuplicate({
      name: form.value.name,
      neq: form.value.neq,
    })
    const data = resp.data?.duplicates || resp.data?.data?.duplicates || []
    duplicates.value = data
    if (data.length > 0) showDuplicateWarning.value = true
  } catch { /* silent */ }
}

async function onSubmit() {
  error.value = ''
  if (!form.value.name.trim()) { error.value = 'Le nom est obligatoire.'; return }
  if (!form.value.city.trim()) { error.value = 'La ville est obligatoire.'; return }
  if (!form.value.postal_code.trim()) { error.value = 'Le code postal est obligatoire.'; return }
  if (!form.value.country.trim()) { error.value = 'Le pays est obligatoire.'; return }
  // Check duplicates first if not already warned
  if (!showDuplicateWarning.value && (form.value.name || form.value.neq)) {
    await checkDuplicates()
    if (duplicates.value.length > 0) return // Show warning, don't submit yet
  }
  doCreate()
}

async function doCreate() {
  error.value = ''
  isSubmitting.value = true
  try {
    await supplierApi.createOrganization(form.value)
    emit('created')
    emit('close')
  } catch (e: unknown) {
    const axiosErr = e as { response?: { data?: { error?: { message?: string } } } }
    error.value = axiosErr.response?.data?.error?.message || 'Erreur lors de la création'
  } finally {
    isSubmitting.value = false
    showDuplicateWarning.value = false
    duplicates.value = []
  }
}
</script>

<template>
  <SlideOver :open="open" title="Nouvelle organisation externe" @close="emit('close')">
    <form class="space-y-4" @submit.prevent="onSubmit">
      <div v-if="error" class="rounded bg-danger/10 p-2 text-sm text-danger">{{ error }}</div>

      <!-- Duplicate warning -->
      <div v-if="showDuplicateWarning" class="rounded-lg border border-warning/30 bg-warning/5 p-3">
        <p class="text-sm font-medium text-warning">Doublons potentiels détectés :</p>
        <div v-for="dup in duplicates" :key="dup.id" class="mt-2 flex items-center justify-between rounded bg-white p-2 text-sm">
          <div>
            <span class="font-medium">{{ dup.name }}</span>
            <span v-if="dup.neq" class="ml-2 text-xs text-text-muted">NEQ: {{ dup.neq }}</span>
            <span class="ml-2 rounded bg-warning/10 px-1.5 py-0.5 text-xs text-warning">{{ dup.match_type === 'neq_exact' ? 'NEQ identique' : 'Nom similaire' }}</span>
          </div>
        </div>
        <div class="mt-3 flex gap-2">
          <button type="button" class="btn-ghost" style="font-size:12px;padding:4px 10px;" @click="doCreate">Créer quand même</button>
          <button type="button" class="btn-ghost" style="font-size:12px;padding:4px 10px;" @click="showDuplicateWarning = false; duplicates = []">Modifier</button>
        </div>
      </div>

      <div>
        <label class="text-xs font-medium text-text-muted">Nom *</label>
        <input v-model="form.name" type="text" class="mt-1 w-full rounded-md border border-border px-3 py-1.5 text-sm" placeholder="WSP Global" @blur="checkDuplicates" />
      </div>

      <div>
        <label class="text-xs font-medium text-text-muted">NEQ</label>
        <input v-model="form.neq" type="text" class="mt-1 w-full rounded-md border border-border px-3 py-1.5 text-sm" placeholder="1234567890" @blur="checkDuplicates" />
      </div>

      <div class="grid grid-cols-2 gap-3">
        <div>
          <label class="text-xs font-medium text-text-muted">Ville *</label>
          <input v-model="form.city" type="text" class="mt-1 w-full rounded-md border border-border px-3 py-1.5 text-sm" />
        </div>
        <div>
          <label class="text-xs font-medium text-text-muted">Code postal *</label>
          <input v-model="form.postal_code" type="text" class="mt-1 w-full rounded-md border border-border px-3 py-1.5 text-sm" />
        </div>
      </div>

      <div class="grid grid-cols-2 gap-3">
        <div>
          <label class="text-xs font-medium text-text-muted">Pays *</label>
          <select v-model="selectedCountryCode" @change="onCountryChange" class="mt-1 w-full rounded-md border border-border px-3 py-1.5 text-sm">
            <option v-for="c in countries" :key="c.code" :value="c.code">{{ c.name }}</option>
          </select>
        </div>
        <div>
          <label class="text-xs font-medium text-text-muted">Province / État</label>
          <select v-if="provinces.length" v-model="form.province" class="mt-1 w-full rounded-md border border-border px-3 py-1.5 text-sm">
            <option v-for="p in provinces" :key="p" :value="p">{{ p }}</option>
          </select>
          <input v-else v-model="form.province" type="text" placeholder="Province / État" class="mt-1 w-full rounded-md border border-border px-3 py-1.5 text-sm" />
        </div>
      </div>

      <div>
        <label class="text-xs font-medium text-text-muted">Personne contact</label>
        <input v-model="form.contact_name" type="text" class="mt-1 w-full rounded-md border border-border px-3 py-1.5 text-sm" />
      </div>

      <div class="grid grid-cols-2 gap-3">
        <div>
          <label class="text-xs font-medium text-text-muted">Courriel</label>
          <input v-model="form.contact_email" type="email" class="mt-1 w-full rounded-md border border-border px-3 py-1.5 text-sm" />
        </div>
        <div>
          <label class="text-xs font-medium text-text-muted">Téléphone</label>
          <input v-model="form.contact_phone" type="text" class="mt-1 w-full rounded-md border border-border px-3 py-1.5 text-sm" />
        </div>
      </div>

      <div>
        <label class="mb-2 text-xs font-medium text-text-muted">Rôles</label>
        <div class="flex gap-2">
          <button v-for="tag in tagOptions" :key="tag" type="button"
            class="rounded-full border px-3 py-1 text-xs font-medium transition-colors"
            :class="form.type_tags.includes(tag) ? 'border-primary bg-primary/10 text-primary' : 'border-border text-text-muted hover:bg-surface-alt'"
            @click="toggleTag(tag)">
            {{ tagLabels[tag] }}
          </button>
        </div>
      </div>

      <div class="flex justify-end gap-3 pt-4">
        <button type="button" class="btn-ghost" @click="emit('close')">Annuler</button>
        <button type="submit" class="btn-primary" :disabled="isSubmitting">Créer</button>
      </div>
    </form>
  </SlideOver>
</template>
