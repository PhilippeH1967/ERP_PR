<script setup lang="ts">
import BaseModal from '@/shared/components/BaseModal.vue'

defineProps<{
  open: boolean
  weeklyTotal: number
  weeklyNorm: number
}>()

const emit = defineEmits<{
  close: []
  confirm: []
}>()
</script>

<template>
  <BaseModal
    :open="open"
    title="Soumettre la semaine"
    @close="emit('close')"
  >
    <div class="text-sm">
      <p v-if="weeklyTotal < weeklyNorm" class="text-warning">
        Vous avez saisi {{ weeklyTotal }}/{{ weeklyNorm }} heures.
        Soumettre quand même ?
      </p>
      <p v-else-if="weeklyTotal > weeklyNorm" class="text-danger">
        Vous avez saisi {{ weeklyTotal }} heures (&gt;{{ weeklyNorm }}h).
        Vérifiez avant de soumettre.
      </p>
      <p v-else class="text-success">
        {{ weeklyTotal }}/{{ weeklyNorm }} heures saisies. Prêt à soumettre.
      </p>
    </div>

    <template #actions>
      <button
        class="rounded-md px-4 py-2 text-sm text-text-muted hover:bg-surface-alt"
        @click="emit('close')"
      >
        Annuler
      </button>
      <button
        class="rounded-md bg-primary px-4 py-2 text-sm font-medium text-white"
        @click="emit('confirm')"
      >
        Soumettre
      </button>
    </template>
  </BaseModal>
</template>
