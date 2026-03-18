<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import SlideOver from '@/shared/components/SlideOver.vue'
import { useClientStore } from '../stores/useClientStore'

defineProps<{
  open: boolean
}>()

const emit = defineEmits<{
  close: []
}>()

const router = useRouter()
const store = useClientStore()
const isSubmitting = ref(false)
const error = ref('')

const form = ref({
  name: '',
  legal_entity: '',
  alias: '',
  sector: '',
  status: 'active',
})

async function onSubmit() {
  if (!form.value.name.trim()) {
    error.value = 'Le nom est obligatoire'
    return
  }
  error.value = ''
  isSubmitting.value = true
  try {
    const client = await store.createClient(form.value)
    emit('close')
    if (client?.id) {
      router.push(`/clients/${client.id}`)
    }
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
    title="Nouveau client"
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
          class="mt-1 w-full rounded-md border border-border px-3 py-2 text-sm focus:border-primary focus:outline-none"
          placeholder="Ville de Montréal"
        >
      </div>

      <div>
        <label class="text-xs font-medium text-text-muted">Alias / Acronyme</label>
        <input
          v-model="form.alias"
          type="text"
          class="mt-1 w-full rounded-md border border-border px-3 py-2 text-sm focus:border-primary focus:outline-none"
          placeholder="VDM"
        >
      </div>

      <div>
        <label class="text-xs font-medium text-text-muted">Entité juridique</label>
        <input
          v-model="form.legal_entity"
          type="text"
          class="mt-1 w-full rounded-md border border-border px-3 py-2 text-sm focus:border-primary focus:outline-none"
          placeholder="Corporation"
        >
      </div>

      <div>
        <label class="text-xs font-medium text-text-muted">Secteur</label>
        <input
          v-model="form.sector"
          type="text"
          class="mt-1 w-full rounded-md border border-border px-3 py-2 text-sm focus:border-primary focus:outline-none"
          placeholder="Public, Privé, Institutionnel..."
        >
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
          {{ isSubmitting ? 'Création...' : 'Créer le client' }}
        </button>
      </div>
    </form>
  </SlideOver>
</template>
