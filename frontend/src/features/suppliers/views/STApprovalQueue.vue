<script setup lang="ts">
/**
 * ST Invoice Approval Queue for PM.
 * Shows subcontractor invoices pending authorization, grouped by project.
 * PM can authorize individual or batch invoices, or navigate to project ST detail.
 */
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useLocale } from '@/shared/composables/useLocale'
import { supplierApi } from '../api/supplierApi'

const router = useRouter()
const { fmt } = useLocale()

interface STInvoice {
  id: number
  supplier: number
  supplier_name: string
  project: number
  project_code: string
  invoice_number: string
  invoice_date: string
  amount: string
  status: string
  budget_refacturable: string
}

const invoices = ref<STInvoice[]>([])
const isLoading = ref(true)
const selectedIds = ref<Set<number>>(new Set())
const successMessage = ref('')

async function fetchPending() {
  isLoading.value = true
  try {
    const resp = await supplierApi.listSTInvoices({ status: 'received' })
    const data = resp.data?.data || resp.data
    invoices.value = Array.isArray(data) ? data : data?.results || []
  } catch {
    invoices.value = []
  } finally {
    isLoading.value = false
  }
}

onMounted(fetchPending)

// Group invoices by project
interface ProjectGroup {
  projectId: number
  projectCode: string
  invoices: STInvoice[]
  totalAmount: number
}

const groupedByProject = computed<ProjectGroup[]>(() => {
  const map = new Map<number, ProjectGroup>()
  for (const inv of invoices.value) {
    if (!map.has(inv.project)) {
      map.set(inv.project, {
        projectId: inv.project,
        projectCode: inv.project_code,
        invoices: [],
        totalAmount: 0,
      })
    }
    const group = map.get(inv.project)!
    group.invoices.push(inv)
    group.totalAmount += parseFloat(inv.amount || '0')
  }
  return Array.from(map.values()).sort((a, b) => b.totalAmount - a.totalAmount)
})

function toggleSelect(id: number) {
  if (selectedIds.value.has(id)) selectedIds.value.delete(id)
  else selectedIds.value.add(id)
}

function selectAllForProject(group: ProjectGroup) {
  const allSelected = group.invoices.every(i => selectedIds.value.has(i.id))
  if (allSelected) {
    group.invoices.forEach(i => selectedIds.value.delete(i.id))
  } else {
    group.invoices.forEach(i => selectedIds.value.add(i.id))
  }
}

async function authorizeSelected() {
  if (selectedIds.value.size === 0) return
  try {
    await supplierApi.batchAuthorize(Array.from(selectedIds.value))
    successMessage.value = `${selectedIds.value.size} facture(s) autorisee(s)`
    selectedIds.value.clear()
    await fetchPending()
    setTimeout(() => { successMessage.value = '' }, 3000)
  } catch {
    // handled by interceptor
  }
}

async function authorizeSingle(id: number) {
  try {
    await supplierApi.authorizeSTInvoice(id)
    successMessage.value = 'Facture autorisee'
    await fetchPending()
    setTimeout(() => { successMessage.value = '' }, 3000)
  } catch {
    // handled
  }
}

function goToProjectST(projectId: number) {
  router.push(`/projects/${projectId}`)
}
</script>

<template>
  <div>
    <div class="mb-6 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-semibold text-text">Factures sous-traitants a valider</h1>
        <p class="text-sm text-text-muted mt-1">
          Factures ST au statut "Recue" sur vos projets — classees par projet
        </p>
      </div>
      <div class="flex items-center gap-3">
        <span v-if="selectedIds.size > 0" class="text-sm font-medium text-primary">
          {{ selectedIds.size }} selectionnee(s)
        </span>
        <button
          v-if="selectedIds.size > 0"
          class="rounded-md bg-primary px-4 py-2 text-sm font-medium text-white hover:bg-primary/90"
          @click="authorizeSelected"
        >
          Autoriser la selection ({{ selectedIds.size }})
        </button>
      </div>
    </div>

    <!-- Success toast -->
    <div
      v-if="successMessage"
      class="mb-4 rounded-md bg-success/10 px-4 py-3 text-sm font-medium text-success"
    >
      {{ successMessage }}
    </div>

    <!-- Loading -->
    <div v-if="isLoading" class="text-center py-12 text-text-muted">Chargement...</div>

    <!-- Empty state -->
    <div
      v-else-if="groupedByProject.length === 0"
      class="rounded-lg border border-border bg-surface p-12 text-center"
    >
      <div class="text-3xl mb-3">&#9989;</div>
      <h3 class="text-lg font-semibold text-text mb-1">Aucune facture ST a autoriser</h3>
      <p class="text-sm text-text-muted">Toutes les factures sous-traitants de vos projets sont traitees.</p>
    </div>

    <!-- Grouped by project -->
    <div v-else class="space-y-6">
      <div v-for="group in groupedByProject" :key="group.projectId" class="rounded-lg border border-border bg-surface">
        <!-- Project header -->
        <div class="flex items-center justify-between px-5 py-3 border-b border-border bg-surface-alt">
          <div class="flex items-center gap-3">
            <input
              type="checkbox"
              :checked="group.invoices.every(i => selectedIds.has(i.id))"
              @change="selectAllForProject(group)"
              class="rounded"
            >
            <div>
              <span class="font-semibold text-text">{{ group.projectCode }}</span>
              <span class="ml-2 text-xs text-text-muted">{{ group.invoices.length }} facture(s)</span>
            </div>
          </div>
          <div class="flex items-center gap-4">
            <span class="font-mono text-sm font-semibold text-text">{{ fmt.currency(group.totalAmount) }}</span>
            <button
              class="rounded px-3 py-1 text-xs font-medium text-primary hover:bg-primary/5 border border-primary/30"
              @click="goToProjectST(group.projectId)"
            >
              Voir projet &rarr;
            </button>
          </div>
        </div>

        <!-- Invoice rows -->
        <table class="w-full text-left text-sm">
          <thead class="text-xs font-medium uppercase tracking-wide text-text-muted">
            <tr>
              <th class="px-5 py-2 w-10"></th>
              <th class="px-3 py-2">N&deg; facture</th>
              <th class="px-3 py-2">Fournisseur</th>
              <th class="px-3 py-2">Date</th>
              <th class="px-3 py-2 text-right">Montant</th>
              <th class="px-3 py-2 text-right">Refacturable</th>
              <th class="px-5 py-2 text-right"></th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="inv in group.invoices"
              :key="inv.id"
              class="border-t border-border last:border-0 hover:bg-surface-alt"
            >
              <td class="px-5 py-2">
                <input
                  type="checkbox"
                  :checked="selectedIds.has(inv.id)"
                  @change="toggleSelect(inv.id)"
                  class="rounded"
                >
              </td>
              <td class="px-3 py-2 font-mono text-xs">{{ inv.invoice_number }}</td>
              <td class="px-3 py-2 font-medium">{{ inv.supplier_name }}</td>
              <td class="px-3 py-2 text-text-muted">{{ inv.invoice_date }}</td>
              <td class="px-3 py-2 text-right font-mono font-semibold">{{ fmt.currency(inv.amount) }}</td>
              <td class="px-3 py-2 text-right font-mono text-text-muted">{{ fmt.currency(inv.budget_refacturable || '0') }}</td>
              <td class="px-5 py-2 text-right">
                <button
                  class="rounded bg-primary px-3 py-1 text-xs font-medium text-white hover:bg-primary/90"
                  @click="authorizeSingle(inv.id)"
                >
                  Autoriser
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
