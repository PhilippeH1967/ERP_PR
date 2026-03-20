<script setup lang="ts">
import { ref, computed } from 'vue'

const emit = defineEmits<{
  submit: [data: Record<string, unknown>]
  cancel: []
}>()

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

const form = ref({
  address_line_1: '',
  address_line_2: '',
  city: '',
  province: 'Québec',
  postal_code: '',
  country: 'Canada',
  is_billing: false,
  is_primary: false,
})

const error = ref('')

const selectedCountryCode = ref('CA')

const provinces = computed(() => provincesByCountry[selectedCountryCode.value] || [])

function onCountryChange() {
  const country = countries.find(c => c.code === selectedCountryCode.value)
  form.value.country = country?.name || selectedCountryCode.value
  form.value.province = provinces.value[0] || ''
}

function onSubmit() {
  error.value = ''
  if (!form.value.address_line_1.trim()) {
    error.value = 'L\'adresse est obligatoire.'
    return
  }
  if (!form.value.city.trim()) {
    error.value = 'La ville est obligatoire.'
    return
  }
  emit('submit', { ...form.value })
  form.value = {
    address_line_1: '', address_line_2: '', city: '',
    province: 'Québec', postal_code: '', country: 'Canada',
    is_billing: false, is_primary: false,
  }
  selectedCountryCode.value = 'CA'
}
</script>

<template>
  <div class="rounded-lg border border-primary/20 bg-primary/5 p-4">
    <h4 class="mb-3 text-sm font-medium text-primary">Nouvelle adresse</h4>

    <div v-if="error" class="mb-3 rounded bg-danger/10 p-2 text-xs text-danger">{{ error }}</div>

    <div class="grid grid-cols-2 gap-3">
      <input v-model="form.address_line_1" type="text" placeholder="Adresse ligne 1 *"
        class="col-span-2 rounded border px-2 py-1.5 text-sm"
        :class="error && !form.address_line_1.trim() ? 'border-danger' : 'border-border'" />
      <input v-model="form.address_line_2" type="text" placeholder="Adresse ligne 2 (suite, bureau...)"
        class="col-span-2 rounded border border-border px-2 py-1.5 text-sm" />

      <input v-model="form.city" type="text" placeholder="Ville *"
        class="rounded border px-2 py-1.5 text-sm"
        :class="error && !form.city.trim() ? 'border-danger' : 'border-border'" />
      <input v-model="form.postal_code" type="text" placeholder="Code postal"
        class="rounded border border-border px-2 py-1.5 text-sm" />

      <!-- Pays -->
      <div>
        <label class="text-xs font-medium text-text-muted">Pays</label>
        <select v-model="selectedCountryCode" @change="onCountryChange"
          class="mt-1 w-full rounded border border-border px-2 py-1.5 text-sm">
          <option v-for="c in countries" :key="c.code" :value="c.code">{{ c.name }}</option>
        </select>
      </div>

      <!-- Province/État (dynamique selon pays) -->
      <div>
        <label class="text-xs font-medium text-text-muted">Province / État</label>
        <select v-if="provinces.length" v-model="form.province"
          class="mt-1 w-full rounded border border-border px-2 py-1.5 text-sm">
          <option v-for="p in provinces" :key="p" :value="p">{{ p }}</option>
        </select>
        <input v-else v-model="form.province" type="text" placeholder="Province / État"
          class="mt-1 w-full rounded border border-border px-2 py-1.5 text-sm" />
      </div>
    </div>

    <!-- Checkboxes avec explications -->
    <div class="mt-3 space-y-2">
      <label class="flex items-start gap-2">
        <input v-model="form.is_billing" type="checkbox" class="mt-0.5" />
        <div>
          <span class="text-sm font-medium">Adresse de facturation</span>
          <p class="text-xs text-text-muted">Cette adresse apparaîtra sur les factures envoyées à ce client.</p>
        </div>
      </label>
      <label class="flex items-start gap-2">
        <input v-model="form.is_primary" type="checkbox" class="mt-0.5" />
        <div>
          <span class="text-sm font-medium">Adresse principale (siège social)</span>
          <p class="text-xs text-text-muted">Adresse officielle de l'organisation, utilisée par défaut dans la correspondance.</p>
        </div>
      </label>
    </div>

    <div class="mt-4 flex gap-2">
      <button class="rounded bg-primary px-3 py-1.5 text-xs font-medium text-white" @click="onSubmit">Ajouter</button>
      <button class="rounded px-3 py-1.5 text-xs text-text-muted hover:bg-surface-alt" @click="emit('cancel')">Annuler</button>
    </div>
  </div>
</template>
