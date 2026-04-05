<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { consortiumApi } from '../api/consortiumApi'

const route = useRoute()
const router = useRouter()
const consortiumId = Number(route.params.id)
const data = ref<Record<string, unknown> | null>(null)
const isLoading = ref(true)

async function load() {
  isLoading.value = true
  try {
    const resp = await consortiumApi.get(consortiumId)
    data.value = resp.data?.data || resp.data
  } catch { data.value = null }
  finally { isLoading.value = false }
}

onMounted(load)

const members = computed(() => (data.value?.members || []) as Array<Record<string, unknown>>)
const totalCoeff = computed(() => Number(data.value?.total_coefficient || 0))
const projects = computed(() => Number(data.value?.projects_count || 0))

const roleLabel: Record<string, string> = { MANDATAIRE: 'Mandataire (responsable)', PARTENAIRE: 'Partenaire' }
const statusLabel: Record<string, string> = { ACTIVE: 'Actif', COMPLETED: 'Terminé', CANCELLED: 'Annulé' }
const statusColor: Record<string, string> = { ACTIVE: 'badge-green', COMPLETED: 'badge-gray', CANCELLED: 'badge-red' }
</script>

<template>
  <div v-if="isLoading" class="py-12 text-center text-text-muted">Chargement...</div>
  <div v-else-if="!data" class="py-12 text-center text-text-muted">Consortium introuvable</div>
  <div v-else>
    <button class="mb-2 text-xs text-text-muted hover:text-primary" @click="router.push('/consortiums')">&larr; Consortiums</button>
    <div class="mb-6 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-semibold text-text">{{ data.name }}</h1>
        <p class="text-sm text-text-muted">{{ data.client_name }} — {{ roleLabel[String(data.pr_role)] || data.pr_role }}</p>
      </div>
      <div class="flex items-center gap-3">
        <span class="badge" :class="statusColor[String(data.status)] || 'badge-gray'">{{ statusLabel[String(data.status)] || data.status }}</span>
        <button class="rounded-md bg-primary px-4 py-2 text-sm font-medium text-white" @click="router.push(`/consortiums/${consortiumId}/edit`)">Modifier</button>
      </div>
    </div>

    <!-- Info -->
    <div class="mb-4 grid grid-cols-2 gap-4">
      <div class="info-card">
        <h3>Informations</h3>
        <div class="info-row"><span>Client</span><p>{{ data.client_name }}</p></div>
        <div class="info-row"><span>Rôle PR</span><p>{{ roleLabel[String(data.pr_role)] || data.pr_role }}</p></div>
        <div class="info-row"><span>Réf. contrat</span><p>{{ data.contract_reference || '—' }}</p></div>
        <div class="info-row"><span>Projets liés</span><p>{{ projects }}</p></div>
      </div>
      <div class="info-card">
        <h3>Coefficients</h3>
        <div class="info-row"><span>Membres</span><p>{{ members.length }}</p></div>
        <div class="info-row">
          <span>Total coefficient</span>
          <p :class="totalCoeff === 100 ? 'text-success' : 'text-danger'">{{ totalCoeff }}% {{ totalCoeff === 100 ? '✓' : '(≠ 100%)' }}</p>
        </div>
      </div>
    </div>

    <!-- Members table -->
    <div class="rounded-lg border border-border bg-surface">
      <table class="w-full text-left text-sm">
        <thead class="border-b border-border text-xs font-medium uppercase tracking-wide text-text-muted">
          <tr>
            <th class="px-4 py-3">Membre</th>
            <th class="px-4 py-3">Spécialité</th>
            <th class="px-4 py-3 text-right">Coefficient</th>
            <th class="px-4 py-3">Contact</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="m in members" :key="Number(m.id)" class="border-b border-border last:border-0">
            <td class="px-4 py-3 font-medium">
              <span v-if="m.is_pr" class="mr-1 inline-flex rounded bg-primary/10 px-1.5 py-0.5 text-[10px] font-bold text-primary">PR</span>
              {{ m.display_name }}
            </td>
            <td class="px-4 py-3 text-text-muted">{{ m.specialty || '—' }}</td>
            <td class="px-4 py-3 text-right font-mono font-semibold">{{ m.coefficient }}%</td>
            <td class="px-4 py-3 text-text-muted">{{ m.contact_name || '—' }}</td>
          </tr>
          <tr v-if="!members.length">
            <td colspan="4" class="px-4 py-8 text-center text-text-muted">Aucun membre</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="data.description" class="mt-4 rounded-lg border border-border bg-surface p-4">
      <h3 class="mb-2 text-xs font-semibold uppercase text-text-muted">Notes</h3>
      <p class="text-sm">{{ data.description }}</p>
    </div>
  </div>
</template>

<style scoped>
.badge { display: inline-flex; padding: 2px 10px; border-radius: 10px; font-size: 10px; font-weight: 600; }
.badge-green { background: #DCFCE7; color: #15803D; }
.badge-gray { background: var(--color-gray-100); color: var(--color-gray-500); }
.badge-red { background: #FEE2E2; color: #DC2626; }
.info-card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 16px; }
.info-card h3 { font-size: 11px; font-weight: 600; color: var(--color-gray-400); text-transform: uppercase; margin-bottom: 12px; }
.info-row { margin-bottom: 8px; }
.info-row span { display: block; font-size: 11px; color: var(--color-gray-500); }
.info-row p { font-weight: 600; font-size: 13px; margin: 2px 0 0; }
.text-success { color: #15803D; }
.text-danger { color: #DC2626; }
</style>
