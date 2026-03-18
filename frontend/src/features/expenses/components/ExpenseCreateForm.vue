<script setup lang="ts">
import { ref } from 'vue'
import SlideOver from '@/shared/components/SlideOver.vue'
import { expenseApi } from '../api/expenseApi'

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
  expense_date: '',
  amount: '',
  description: '',
  category: '',
  is_refacturable: false,
  tax_type: 'HT',
})

async function onSubmit() {
  if (!form.value.amount || !form.value.expense_date) {
    error.value = 'Date et montant obligatoires'
    return
  }
  error.value = ''
  isSubmitting.value = true
  try {
    // Create report + line in one flow
    const reportResp = await expenseApi.createReport({
      total_amount: form.value.amount,
    })
    const report = reportResp.data?.data || reportResp.data
    if (report?.id) {
      await expenseApi.createLine(report.id, {
        expense_date: form.value.expense_date,
        amount: form.value.amount,
        description: form.value.description,
        is_refacturable: form.value.is_refacturable,
        tax_type: form.value.tax_type,
      })
    }
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
    title="Nouvelle dépense"
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

      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="text-xs font-medium text-text-muted">Date *</label>
          <input
            v-model="form.expense_date"
            type="date"
            class="mt-1 w-full rounded-md border border-border px-3 py-2 text-sm"
          >
        </div>
        <div>
          <label class="text-xs font-medium text-text-muted">Montant *</label>
          <input
            v-model="form.amount"
            type="number"
            step="0.01"
            class="mt-1 w-full rounded-md border border-border px-3 py-2 text-sm font-mono"
            placeholder="75.50"
          >
        </div>
      </div>

      <div>
        <label class="text-xs font-medium text-text-muted">Description</label>
        <textarea
          v-model="form.description"
          class="mt-1 w-full rounded-md border border-border px-3 py-2 text-sm"
          rows="2"
          placeholder="Taxi client, repas affaires..."
        />
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="text-xs font-medium text-text-muted">Taxes</label>
          <select
            v-model="form.tax_type"
            class="mt-1 w-full rounded-md border border-border px-3 py-2 text-sm"
          >
            <option value="HT">
              Hors taxes
            </option>
            <option value="TPS">
              TPS
            </option>
            <option value="TVQ">
              TVQ
            </option>
          </select>
        </div>
        <div class="flex items-end pb-2">
          <label class="flex items-center gap-2 text-sm">
            <input
              v-model="form.is_refacturable"
              type="checkbox"
            >
            Refacturable au client
          </label>
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
          Soumettre
        </button>
      </div>
    </form>
  </SlideOver>
</template>
