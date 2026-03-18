<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useLocale } from '@/shared/composables/useLocale'
import { billingApi } from '../api/billingApi'
import type { Invoice } from '../types/billing.types'

const route = useRoute()
const { fmt } = useLocale()
const invoice = ref<Invoice | null>(null)
const invoiceId = Number(route.params.id)

const statusColors: Record<string, string> = {
  DRAFT: 'bg-text-muted/10 text-text-muted',
  SUBMITTED: 'bg-primary/10 text-primary',
  APPROVED: 'bg-success/10 text-success',
  SENT: 'bg-warning/10 text-warning',
  PAID: 'bg-success/20 text-success',
}

onMounted(async () => {
  const resp = await billingApi.getInvoice(invoiceId)
  invoice.value = resp.data?.data || resp.data
})

async function submitInvoice() {
  await billingApi.submitInvoice(invoiceId)
  const resp = await billingApi.getInvoice(invoiceId)
  invoice.value = resp.data?.data || resp.data
}

async function approveInvoice() {
  await billingApi.approveInvoice(invoiceId)
  const resp = await billingApi.getInvoice(invoiceId)
  invoice.value = resp.data?.data || resp.data
}

async function updateLine(lineId: number, field: string, value: string) {
  await billingApi.updateLine(invoiceId, lineId, { [field]: value })
  const resp = await billingApi.getInvoice(invoiceId)
  invoice.value = resp.data?.data || resp.data
}
</script>

<template>
  <div v-if="invoice">
    <!-- Header -->
    <div class="mb-6 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-semibold text-text">
          <span class="font-mono">{{ invoice.invoice_number }}</span>
        </h1>
        <p class="text-sm text-text-muted">
          Projet {{ invoice.project_code }} · {{ invoice.client_name }}
        </p>
      </div>
      <div class="flex items-center gap-3">
        <span
          class="rounded-full px-3 py-1 text-xs font-medium"
          :class="statusColors[invoice.status]"
        >
          {{ invoice.status }}
        </span>
        <button
          v-if="invoice.status === 'DRAFT'"
          class="rounded-md bg-primary px-4 py-2 text-sm font-medium text-white"
          @click="submitInvoice"
        >
          Soumettre
        </button>
        <button
          v-if="invoice.status === 'SUBMITTED'"
          class="rounded-md bg-success px-4 py-2 text-sm font-medium text-white"
          @click="approveInvoice"
        >
          Approuver
        </button>
      </div>
    </div>

    <!-- CA/Salary ratio banner (Story 5-3) -->
    <div class="mb-4 flex items-center gap-4 rounded-lg border border-primary/20 bg-primary/5 p-3">
      <div class="text-center">
        <div class="font-mono text-lg font-bold text-primary">
          {{ fmt.currency(invoice.total_amount) }}
        </div>
        <div class="text-[10px] text-text-muted">
          Montant total
        </div>
      </div>
      <div class="h-8 w-px bg-border" />
      <div class="text-center">
        <div class="font-mono text-lg font-bold text-text">
          {{ fmt.currency(invoice.tax_tps) }}
        </div>
        <div class="text-[10px] text-text-muted">
          TPS
        </div>
      </div>
      <div class="h-8 w-px bg-border" />
      <div class="text-center">
        <div class="font-mono text-lg font-bold text-text">
          {{ fmt.currency(invoice.tax_tvq) }}
        </div>
        <div class="text-[10px] text-text-muted">
          TVQ
        </div>
      </div>
    </div>

    <!-- 7-Column Invoice Preparation Grid (Story 5-2) -->
    <div class="overflow-x-auto rounded-lg border border-border bg-surface">
      <table class="w-full text-sm">
        <thead class="border-b border-border bg-surface-alt text-xs font-medium uppercase text-text-muted">
          <tr>
            <th class="min-w-[200px] px-3 py-3 text-left">
              Livrable
            </th>
            <th class="min-w-[100px] px-3 py-3 text-right font-mono">
              Contrat
            </th>
            <th class="min-w-[100px] px-3 py-3 text-right font-mono">
              Facturé à ce jour
            </th>
            <th class="min-w-[80px] px-3 py-3 text-right font-mono">
              % Fact.
            </th>
            <th class="min-w-[80px] px-3 py-3 text-right font-mono">
              % Heures
            </th>
            <th class="min-w-[120px] px-3 py-3 text-right font-mono">
              À facturer
            </th>
            <th class="min-w-[80px] px-3 py-3 text-right font-mono">
              % Après
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="line in invoice.lines"
            :key="line.id"
            class="border-b border-border last:border-0 hover:bg-surface-alt"
          >
            <td class="px-3 py-2">
              <div class="flex items-center gap-2">
                <span
                  class="rounded bg-text-muted/10 px-1.5 py-0.5 text-[10px] font-medium"
                >{{ line.line_type }}</span>
                <span>{{ line.deliverable_name }}</span>
              </div>
            </td>
            <td class="px-3 py-2 text-right font-mono">
              {{ fmt.currency(line.total_contract_amount) }}
            </td>
            <td class="px-3 py-2 text-right font-mono">
              {{ fmt.currency(line.invoiced_to_date) }}
            </td>
            <td class="px-3 py-2 text-right font-mono">
              {{ line.pct_billing_advancement }}%
            </td>
            <td class="px-3 py-2 text-right font-mono">
              {{ line.pct_hours_advancement }}%
            </td>
            <td class="px-3 py-2 text-right">
              <input
                :value="line.amount_to_bill"
                type="number"
                step="0.01"
                class="w-full rounded border border-primary/30 bg-primary/5 px-2 py-1 text-right font-mono text-sm focus:border-primary focus:outline-none"
                :disabled="invoice.status !== 'DRAFT'"
                @blur="(e) => updateLine(line.id, 'amount_to_bill', (e.target as HTMLInputElement).value)"
              >
            </td>
            <td class="px-3 py-2 text-right font-mono text-text-muted">
              {{ line.pct_after_billing }}%
            </td>
          </tr>
          <tr v-if="!invoice.lines?.length">
            <td
              colspan="7"
              class="px-3 py-8 text-center text-text-muted"
            >
              Aucune ligne — ajoutez des livrables
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
