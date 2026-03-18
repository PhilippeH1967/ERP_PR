<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useLocale } from '@/shared/composables/useLocale'
import { billingApi } from '../api/billingApi'

const { fmt } = useLocale()

interface Payment {
  id: number
  invoice: number
  amount: string
  payment_date: string
  reference: string
  method: string
}

const payments = ref<Payment[]>([])

onMounted(async () => {
  try {
    const resp = await billingApi.listPayments()
    payments.value = resp.data?.data || resp.data || []
  } catch {
    payments.value = []
  }
})
</script>

<template>
  <div>
    <h1 class="mb-6 text-2xl font-semibold text-text">
      Paiements reçus
    </h1>

    <div class="rounded-lg border border-border bg-surface">
      <table class="w-full text-left text-sm">
        <thead class="border-b border-border text-xs font-medium uppercase text-text-muted">
          <tr>
            <th class="px-4 py-3">
              Facture
            </th>
            <th class="px-4 py-3 text-right font-mono">
              Montant
            </th>
            <th class="px-4 py-3">
              Date
            </th>
            <th class="px-4 py-3">
              Référence
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="p in payments"
            :key="p.id"
            class="border-b border-border last:border-0"
          >
            <td class="px-4 py-3">
              Facture #{{ p.invoice }}
            </td>
            <td class="px-4 py-3 text-right font-mono font-medium">
              {{ fmt.currency(p.amount) }}
            </td>
            <td class="px-4 py-3 text-text-muted">
              {{ fmt.date(p.payment_date) }}
            </td>
            <td class="px-4 py-3 text-text-muted">
              {{ p.reference || '—' }}
            </td>
          </tr>
          <tr v-if="!payments.length">
            <td
              colspan="4"
              class="px-4 py-8 text-center text-text-muted"
            >
              Aucun paiement enregistré
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
