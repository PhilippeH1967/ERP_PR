<script setup lang="ts">
import { ref } from 'vue'
import SlideOver from '@/shared/components/SlideOver.vue'
import { supplierApi } from '../api/supplierApi'

defineProps<{
  open: boolean
}>()

const emit = defineEmits<{
  close: []
  created: []
}>()

const isSubmitting = ref(false)
const error = ref('')

const form = ref({
  name: '',
  neq: '',
  address: '',
  city: '',
  province: 'Québec',
  postal_code: '',
  contact_name: '',
  contact_email: '',
  contact_phone: '',
  type_tags: [] as string[],
})

const tagOptions = ['st', 'partner', 'competitor']

function toggleTag(tag: string) {
  const idx = form.value.type_tags.indexOf(tag)
  if (idx >= 0) {
    form.value.type_tags.splice(idx, 1)
  } else {
    form.value.type_tags.push(tag)
  }
}

async function onSubmit() {
  if (!form.value.name.trim()) {
    error.value = 'Le nom est obligatoire'
    return
  }
  error.value = ''
  isSubmitting.value = true
  try {
    await supplierApi.createOrganization(form.value)
    emit('created')
    emit('close')
  } catch {
    error.value = 'Erreur lors de la création'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <SlideOver
    :open="open"
    title="Nouvelle organisation externe"
    @close="emit('close')"
  >
    <form
      class="space-y-4"
      @submit.prevent="onSubmit"
    >
      <div
        v-if="error"
        class="rounded bg-danger/10 p-2 text-sm text-danger"
      >
        {{ error }}
      </div>

      <div>
        <label class="text-xs font-medium text-text-muted">Nom *</label>
        <input
          v-model="form.name"
          type="text"
          class="mt-1 w-full rounded-md border border-border px-3 py-2 text-sm"
          placeholder="WSP Global"
        >
      </div>

      <div>
        <label class="text-xs font-medium text-text-muted">NEQ</label>
        <input
          v-model="form.neq"
          type="text"
          class="mt-1 w-full rounded-md border border-border px-3 py-2 text-sm"
          placeholder="1234567890"
        >
      </div>

      <div class="grid grid-cols-2 gap-3">
        <div>
          <label class="text-xs font-medium text-text-muted">Ville</label>
          <input
            v-model="form.city"
            type="text"
            class="mt-1 w-full rounded-md border border-border px-3 py-2 text-sm"
          >
        </div>
        <div>
          <label class="text-xs font-medium text-text-muted">Province</label>
          <input
            v-model="form.province"
            type="text"
            class="mt-1 w-full rounded-md border border-border px-3 py-2 text-sm"
          >
        </div>
      </div>

      <div>
        <label class="text-xs font-medium text-text-muted">Personne contact</label>
        <input
          v-model="form.contact_name"
          type="text"
          class="mt-1 w-full rounded-md border border-border px-3 py-2 text-sm"
        >
      </div>

      <div class="grid grid-cols-2 gap-3">
        <div>
          <label class="text-xs font-medium text-text-muted">Courriel</label>
          <input
            v-model="form.contact_email"
            type="email"
            class="mt-1 w-full rounded-md border border-border px-3 py-2 text-sm"
          >
        </div>
        <div>
          <label class="text-xs font-medium text-text-muted">Téléphone</label>
          <input
            v-model="form.contact_phone"
            type="text"
            class="mt-1 w-full rounded-md border border-border px-3 py-2 text-sm"
          >
        </div>
      </div>

      <div>
        <label class="mb-2 text-xs font-medium text-text-muted">Rôles</label>
        <div class="flex gap-2">
          <button
            v-for="tag in tagOptions"
            :key="tag"
            type="button"
            class="rounded-full border px-3 py-1 text-xs font-medium transition-colors"
            :class="form.type_tags.includes(tag)
              ? 'border-primary bg-primary/10 text-primary'
              : 'border-border text-text-muted hover:bg-surface-alt'"
            @click="toggleTag(tag)"
          >
            {{ tag === 'st' ? 'Sous-traitant' : tag === 'partner' ? 'Partenaire' : 'Concurrent' }}
          </button>
        </div>
      </div>

      <div class="flex justify-end gap-3 pt-4">
        <button
          type="button"
          class="rounded-md px-4 py-2 text-sm text-text-muted hover:bg-surface-alt"
          @click="emit('close')"
        >
          Annuler
        </button>
        <button
          type="submit"
          class="rounded-md bg-primary px-4 py-2 text-sm font-medium text-white disabled:opacity-50"
          :disabled="isSubmitting"
        >
          Créer
        </button>
      </div>
    </form>
  </SlideOver>
</template>
