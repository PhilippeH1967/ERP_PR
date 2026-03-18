<script setup lang="ts">
import { useRouter } from 'vue-router'
import BaseModal from '@/shared/components/BaseModal.vue'

defineProps<{
  open: boolean
  duplicates: Array<{ id: number; name: string; alias: string; match_type: string }>
}>()

const emit = defineEmits<{
  close: []
  proceed: []
}>()

const router = useRouter()

function viewExisting(id: number) {
  emit('close')
  router.push(`/clients/${id}`)
}
</script>

<template>
  <BaseModal
    :open="open"
    title="Doublons potentiels détectés"
    @close="emit('close')"
  >
    <div class="space-y-3">
      <p class="text-sm text-text-muted">
        Les clients suivants ressemblent au nom saisi :
      </p>
      <div
        v-for="dup in duplicates"
        :key="dup.id"
        class="flex items-center justify-between rounded border border-warning/30 bg-warning/5 p-3"
      >
        <div>
          <p class="text-sm font-medium text-text">
            {{ dup.name }}
          </p>
          <p class="text-xs text-text-muted">
            {{ dup.alias ? `Alias: ${dup.alias}` : '' }}
            · {{ dup.match_type === 'alias_exact' ? 'Correspondance alias exacte' : 'Nom similaire' }}
          </p>
        </div>
        <button
          class="rounded px-3 py-1 text-xs font-medium text-primary hover:bg-primary/10"
          @click="viewExisting(dup.id)"
        >
          Voir
        </button>
      </div>
    </div>

    <template #actions>
      <button
        class="rounded-md px-4 py-2 text-sm text-text-muted hover:bg-surface-alt"
        @click="emit('close')"
      >
        Annuler
      </button>
      <button
        class="rounded-md bg-warning px-4 py-2 text-sm font-medium text-white"
        @click="emit('proceed')"
      >
        Créer quand même
      </button>
    </template>
  </BaseModal>
</template>
