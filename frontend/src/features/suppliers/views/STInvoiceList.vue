<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useLocale } from '@/shared/composables/useLocale'

const { fmt } = useLocale()

interface STInvoice {
  id: number
  supplier: number
  project: number
  invoice_number: string
  invoice_date: string
  amount: string
  status: string
}

const invoices = ref<STInvoice[]>([])

onMounted(async () => {
  // ST invoices not yet exposed via dedicated API — placeholder
  invoices.value = []
})
</script>

<template>
  <div>
    <div class="mb-6 flex items-center justify-between">
      <h1 class="text-2xl font-semibold text-text">
        Factures sous-traitants
      </h1>
      <button class="rounded-md bg-primary px-4 py-2 text-sm font-medium text-white">
        + Nouvelle facture ST
      </button>
    </div>

    <div class="rounded-lg border border-border bg-surface">
      <table class="w-full text-left text-sm">
        <thead class="border-b border-border text-xs font-medium uppercase text-text-muted">
          <tr>
            <th class="px-4 py-3">
              No facture
            </th>
            <th class="px-4 py-3 text-right font-mono">
              Montant
            </th>
            <th class="px-4 py-3">
              Date
            </th>
            <th class="px-4 py-3">
              Statut
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="inv in invoices"
            :key="inv.id"
            class="border-b border-border last:border-0"
          >
            <td class="px-4 py-3 font-mono">
              {{ inv.invoice_number }}
            </td>
            <td class="px-4 py-3 text-right font-mono">
              {{ fmt.currency(inv.amount) }}
            </td>
            <td class="px-4 py-3 text-text-muted">
              {{ fmt.date(inv.invoice_date) }}
            </td>
            <td class="px-4 py-3">
              <span class="rounded-full bg-primary/10 px-2 py-0.5 text-xs text-primary">
                {{ inv.status }}
              </span>
            </td>
          </tr>
          <tr v-if="!invoices.length">
            <td
              colspan="4"
              class="px-4 py-8 text-center text-text-muted"
            >
              Aucune facture ST enregistrée
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
