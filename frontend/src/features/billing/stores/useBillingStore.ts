import { defineStore } from 'pinia'
import { ref } from 'vue'
import { billingApi } from '../api/billingApi'
import type { Invoice } from '../types/billing.types'

export const useBillingStore = defineStore('billing', () => {
  const invoices = ref<Invoice[]>([])
  const currentInvoice = ref<Invoice | null>(null)
  const isLoading = ref(false)

  async function fetchInvoices(params?: Record<string, string>) {
    isLoading.value = true
    try {
      const response = await billingApi.listInvoices(params)
      invoices.value = response.data?.data || response.data
    } finally {
      isLoading.value = false
    }
  }

  async function fetchInvoice(id: number) {
    const response = await billingApi.getInvoice(id)
    currentInvoice.value = response.data?.data || response.data
  }

  return { invoices, currentInvoice, isLoading, fetchInvoices, fetchInvoice }
})
