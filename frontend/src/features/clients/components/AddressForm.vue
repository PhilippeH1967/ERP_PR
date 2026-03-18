<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
  submit: [data: Record<string, unknown>]
  cancel: []
}>()

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

function onSubmit() {
  if (!form.value.address_line_1.trim() || !form.value.city.trim()) return
  emit('submit', { ...form.value })
  form.value = {
    address_line_1: '', address_line_2: '', city: '',
    province: 'Québec', postal_code: '', country: 'Canada',
    is_billing: false, is_primary: false,
  }
}
</script>

<template>
  <div class="rounded-lg border border-primary/20 bg-primary/5 p-4">
    <h4 class="mb-3 text-sm font-medium text-primary">
      Nouvelle adresse
    </h4>
    <div class="grid grid-cols-2 gap-3">
      <input
        v-model="form.address_line_1"
        type="text"
        placeholder="Adresse ligne 1 *"
        class="col-span-2 rounded border border-border px-2 py-1.5 text-sm"
      >
      <input
        v-model="form.address_line_2"
        type="text"
        placeholder="Adresse ligne 2"
        class="col-span-2 rounded border border-border px-2 py-1.5 text-sm"
      >
      <input
        v-model="form.city"
        type="text"
        placeholder="Ville *"
        class="rounded border border-border px-2 py-1.5 text-sm"
      >
      <input
        v-model="form.province"
        type="text"
        placeholder="Province"
        class="rounded border border-border px-2 py-1.5 text-sm"
      >
      <input
        v-model="form.postal_code"
        type="text"
        placeholder="Code postal *"
        class="rounded border border-border px-2 py-1.5 text-sm"
      >
      <div class="flex items-center gap-4">
        <label class="flex items-center gap-1.5 text-sm">
          <input
            v-model="form.is_billing"
            type="checkbox"
          >
          Facturation
        </label>
        <label class="flex items-center gap-1.5 text-sm">
          <input
            v-model="form.is_primary"
            type="checkbox"
          >
          Principale
        </label>
      </div>
    </div>
    <div class="mt-3 flex gap-2">
      <button
        class="rounded bg-primary px-3 py-1.5 text-xs font-medium text-white"
        @click="onSubmit"
      >
        Ajouter
      </button>
      <button
        class="rounded px-3 py-1.5 text-xs text-text-muted hover:bg-surface-alt"
        @click="emit('cancel')"
      >
        Annuler
      </button>
    </div>
  </div>
</template>
