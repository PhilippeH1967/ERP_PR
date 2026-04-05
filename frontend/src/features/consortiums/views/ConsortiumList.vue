<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { consortiumApi } from '../api/consortiumApi'

const router = useRouter()
const consortiums = ref<Array<Record<string, unknown>>>([])
const isLoading = ref(false)

async function load() {
  isLoading.value = true
  try {
    const resp = await consortiumApi.list()
    const data = resp.data?.data || resp.data
    consortiums.value = Array.isArray(data) ? data : data?.results || []
  } catch { consortiums.value = [] }
  finally { isLoading.value = false }
}

onMounted(load)

const activeCount = computed(() => consortiums.value.filter(c => c.status === 'ACTIVE').length)
const totalProjects = computed(() => consortiums.value.reduce((s, c) => s + Number(c.projects_count || 0), 0))

const roleLabels: Record<string, string> = { MANDATAIRE: 'Mandataire', PARTENAIRE: 'Partenaire' }
const roleColors: Record<string, string> = { MANDATAIRE: 'badge-blue', PARTENAIRE: 'badge-amber' }
const statusLabels: Record<string, string> = { ACTIVE: 'Actif', COMPLETED: 'Terminé', CANCELLED: 'Annulé' }
const statusColors: Record<string, string> = { ACTIVE: 'badge-green', COMPLETED: 'badge-gray', CANCELLED: 'badge-red' }
</script>

<template>
  <div>
    <div class="mb-6 flex items-center justify-between">
      <h1 class="text-2xl font-semibold text-text">Consortiums</h1>
      <button class="rounded-md bg-primary px-4 py-2 text-sm font-medium text-white" @click="router.push('/consortiums/new')">
        + Nouveau consortium
      </button>
    </div>

    <!-- KPIs -->
    <div class="mb-6 grid grid-cols-3 gap-4">
      <div class="kpi-card">
        <div class="kpi-value">{{ activeCount }}</div>
        <div class="kpi-label">Consortiums actifs</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-value">{{ totalProjects }}</div>
        <div class="kpi-label">Projets liés</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-value">{{ consortiums.length }}</div>
        <div class="kpi-label">Total consortiums</div>
      </div>
    </div>

    <div v-if="isLoading" class="py-12 text-center text-text-muted">Chargement...</div>

    <div v-else-if="!consortiums.length" class="rounded-lg border border-border bg-surface p-12 text-center text-text-muted">
      Aucun consortium — cliquez "+ Nouveau consortium" pour en créer un
    </div>

    <div v-else class="rounded-lg border border-border bg-surface">
      <table class="w-full text-left text-sm">
        <thead class="border-b border-border text-xs font-medium uppercase tracking-wide text-text-muted">
          <tr>
            <th class="px-4 py-3">Consortium</th>
            <th class="px-4 py-3">Client</th>
            <th class="px-4 py-3">Rôle PR</th>
            <th class="px-4 py-3 text-right">Membres</th>
            <th class="px-4 py-3 text-right">Projets</th>
            <th class="px-4 py-3 text-right">Coefficient</th>
            <th class="px-4 py-3">Statut</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="c in consortiums"
            :key="Number(c.id)"
            class="cursor-pointer border-b border-border last:border-0 hover:bg-surface-alt"
            @click="router.push(`/consortiums/${c.id}`)"
          >
            <td class="px-4 py-3 font-medium">{{ c.name }}</td>
            <td class="px-4 py-3 text-text-muted">{{ c.client_name || '—' }}</td>
            <td class="px-4 py-3">
              <span class="badge" :class="roleColors[String(c.pr_role)] || 'badge-gray'">
                {{ roleLabels[String(c.pr_role)] || c.pr_role }}
              </span>
            </td>
            <td class="px-4 py-3 text-right font-mono">{{ c.members_count || 0 }}</td>
            <td class="px-4 py-3 text-right font-mono">{{ c.projects_count || 0 }}</td>
            <td class="px-4 py-3 text-right font-mono" :class="{ 'text-danger': Number(c.total_coefficient) !== 100 && Number(c.members_count) > 0 }">
              {{ c.total_coefficient }}%
            </td>
            <td class="px-4 py-3">
              <span class="badge" :class="statusColors[String(c.status)] || 'badge-gray'">
                {{ statusLabels[String(c.status)] || c.status }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.badge { display: inline-flex; padding: 2px 10px; border-radius: 10px; font-size: 10px; font-weight: 600; }
.badge-green { background: #DCFCE7; color: #15803D; }
.badge-amber { background: #FEF3C7; color: #92400E; }
.badge-blue { background: #DBEAFE; color: #1D4ED8; }
.badge-gray { background: var(--color-gray-100); color: var(--color-gray-500); }
.badge-red { background: #FEE2E2; color: #DC2626; }
.text-danger { color: #DC2626; }
.kpi-card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 16px; text-align: center; }
.kpi-value { font-size: 28px; font-weight: 700; color: var(--color-gray-900); }
.kpi-label { font-size: 11px; color: var(--color-gray-500); text-transform: uppercase; font-weight: 600; margin-top: 4px; }
</style>
