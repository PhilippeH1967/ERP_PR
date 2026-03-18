<script setup lang="ts">
import { onMounted } from 'vue'
import { useLocale } from '@/shared/composables/useLocale'
import { useBillingStore } from '../stores/useBillingStore'

const store = useBillingStore()
const { fmt } = useLocale()

const statusColors: Record<string, string> = {
  DRAFT: 'bg-text-muted/10 text-text-muted',
  SUBMITTED: 'bg-primary/10 text-primary',
  APPROVED: 'bg-success/10 text-success',
  SENT: 'bg-warning/10 text-warning',
  PAID: 'bg-success/20 text-success',
}

onMounted(() => store.fetchInvoices())
</script>

<template>
  <div>
    <div class="mb-6 flex items-center justify-between">
      <h1 class="text-2xl font-semibold text-text">
        Facturation
      </h1>
    </div>

    <div class="rounded-lg border border-border bg-surface">
      <table class="w-full text-left text-sm">
        <thead class="border-b border-border text-xs font-medium uppercase tracking-wide text-text-muted">
          <tr>
            <th class="px-4 py-3">
              No facture
            </th>
            <th class="px-4 py-3">
              Projet
            </th>
            <th class="px-4 py-3">
              Client
            </th>
            <th class="px-4 py-3 text-right font-mono">
              Montant
            </th>
            <th class="px-4 py-3">
              Statut
            </th>
            <th class="px-4 py-3">
              Date
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="invoice in store.invoices"
            :key="invoice.id"
            class="cursor-pointer border-b border-border last:border-0 hover:bg-surface-alt"
          >
            <td class="px-4 py-3 font-mono font-medium">
              {{ invoice.invoice_number }}
            </td>
            <td class="px-4 py-3">
              {{ invoice.project_code }}
            </td>
            <td class="px-4 py-3 text-text-muted">
              {{ invoice.client_name }}
            </td>
            <td class="px-4 py-3 text-right font-mono">
              {{ fmt.currency(invoice.total_amount) }}
            </td>
            <td class="px-4 py-3">
              <span
                class="rounded-full px-2 py-0.5 text-xs"
                :class="statusColors[invoice.status] || ''"
              >
                {{ invoice.status }}
              </span>
            </td>
            <td class="px-4 py-3 text-text-muted">
              {{ fmt.date(invoice.date_created) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
