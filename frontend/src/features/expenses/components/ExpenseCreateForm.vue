<script setup lang="ts">
import { ref } from 'vue'
import SlideOver from '@/shared/components/SlideOver.vue'
import { expenseApi } from '../api/expenseApi'

defineProps<{ open: boolean }>()
const emit = defineEmits<{ close: []; created: [] }>()

const isSubmitting = ref(false)
const error = ref('')
const receiptFile = ref<File | null>(null)
const receiptPreview = ref('')

const form = ref({
  expense_date: '',
  amount: '',
  description: '',
  category: '',
  is_refacturable: false,
  tax_type: 'HT',
})

function onFileChange(e: Event) {
  const input = e.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return
  receiptFile.value = file
  if (file.type.startsWith('image/')) {
    receiptPreview.value = URL.createObjectURL(file)
  } else {
    receiptPreview.value = ''
  }
}

function triggerFileInput() {
  const input = document.getElementById('receipt-input') as HTMLInputElement
  input?.click()
}

async function onSubmit() {
  if (!form.value.amount || !form.value.expense_date) {
    error.value = 'Date et montant obligatoires'
    return
  }
  error.value = ''
  isSubmitting.value = true
  try {
    const reportResp = await expenseApi.createReport({ total_amount: form.value.amount })
    const report = reportResp.data?.data || reportResp.data
    if (report?.id) {
      const lineData: Record<string, unknown> = {
        expense_date: form.value.expense_date,
        amount: form.value.amount,
        description: form.value.description,
        is_refacturable: form.value.is_refacturable,
        tax_type: form.value.tax_type,
      }
      if (form.value.category) lineData.category = Number(form.value.category)
      await expenseApi.createLine(report.id, lineData)

      // Upload receipt if provided
      if (receiptFile.value) {
        await expenseApi.uploadReceipt(report.id, receiptFile.value)
      }
    }
    // Reset
    form.value = { expense_date: '', amount: '', description: '', category: '', is_refacturable: false, tax_type: 'HT' }
    receiptFile.value = null
    receiptPreview.value = ''
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
  <SlideOver :open="open" title="Nouvelle dépense" @close="emit('close')">
    <form class="space-y-4" @submit.prevent="onSubmit">
      <div v-if="error" class="rounded bg-danger/10 p-2 text-sm text-danger">{{ error }}</div>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="text-xs font-medium text-text-muted">Date *</label>
          <input v-model="form.expense_date" type="date" class="mt-1 w-full rounded border border-border px-3 py-1.5 text-sm" />
        </div>
        <div>
          <label class="text-xs font-medium text-text-muted">Montant *</label>
          <input v-model="form.amount" type="number" step="0.01" class="mt-1 w-full rounded border border-border px-3 py-1.5 text-sm font-mono" placeholder="75.50" />
        </div>
      </div>

      <div>
        <label class="text-xs font-medium text-text-muted">Description</label>
        <textarea v-model="form.description" class="mt-1 w-full rounded border border-border px-3 py-1.5 text-sm" rows="2" placeholder="Taxi client, repas affaires..." />
      </div>

      <!-- Receipt upload -->
      <div>
        <label class="text-xs font-medium text-text-muted">Pièce justificative</label>
        <div
          class="mt-1 cursor-pointer rounded-lg border-2 border-dashed border-border p-4 text-center hover:border-primary/30"
          @click="triggerFileInput"
        >
          <input id="receipt-input" type="file" accept="image/*,.pdf" class="hidden" @change="onFileChange" />
          <template v-if="receiptFile">
            <img v-if="receiptPreview" :src="receiptPreview" class="mx-auto mb-2 max-h-24 rounded" />
            <p class="text-sm font-medium text-primary">{{ receiptFile.name }}</p>
            <p class="text-xs text-text-muted">{{ (receiptFile.size / 1024).toFixed(0) }} Ko</p>
          </template>
          <template v-else>
            <div class="text-xl text-text-muted">📎</div>
            <p class="mt-1 text-xs text-text-muted">Cliquez pour sélectionner (PDF, JPG, PNG — max 10 Mo)</p>
          </template>
        </div>
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="text-xs font-medium text-text-muted">Taxes</label>
          <select v-model="form.tax_type" class="mt-1 w-full rounded border border-border px-3 py-1.5 text-sm">
            <option value="HT">Hors taxes</option>
            <option value="TPS">TPS</option>
            <option value="TVQ">TVQ</option>
          </select>
        </div>
        <div class="flex items-end pb-1">
          <label class="flex items-center gap-2 text-sm">
            <input v-model="form.is_refacturable" type="checkbox" />
            Refacturable au client
          </label>
        </div>
      </div>

      <div class="flex justify-end gap-3 pt-3">
        <button type="button" class="btn-ghost" @click="emit('close')">Annuler</button>
        <button type="submit" class="btn-primary" :disabled="isSubmitting">
          {{ isSubmitting ? 'Envoi...' : 'Soumettre' }}
        </button>
      </div>
    </form>
  </SlideOver>
</template>
