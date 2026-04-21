<script setup lang="ts">
import { onMounted, ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { consortiumApi } from '../api/consortiumApi'
import apiClient from '@/plugins/axios'

const route = useRoute()
const router = useRouter()
const consortiumId = Number(route.params.id)
const data = ref<Record<string, unknown> | null>(null)
const isLoading = ref(true)
const activeTab = ref('overview')

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
const prMember = computed(() => members.value.find(m => m.is_pr))

// Associated projects
const projects = ref<Array<Record<string, unknown>>>([])
const projectsLoading = ref(false)

async function loadProjects() {
  projectsLoading.value = true
  try {
    const resp = await apiClient.get('projects/', { params: { is_consortium: true } })
    const all = resp.data?.data || resp.data
    const list = Array.isArray(all) ? all : all?.results || []
    // Filter projects belonging to this consortium
    projects.value = list.filter((p: Record<string, unknown>) => Number(p.consortium) === consortiumId)
  } catch { projects.value = [] }
  finally { projectsLoading.value = false }
}

// Placeholder financials (will be computed from real data later)
const financials = computed(() => {
  return {
    // Consortium view
    ca_client: 0,
    costs_members: 0,
    costs_st: 0,
    margin_consortium: 0,
    margin_pct: 0,
    // PR view
    ca_pr_invoices: 0,
    ca_pr_profit_share: 0,
    ca_pr_total: 0,
    pr_coefficient: Number(prMember.value?.coefficient || 0),
  }
})

// Tab lazy loading
watch(activeTab, (tab) => {
  if (tab === 'projects' && !projects.value.length) loadProjects()
})

const tabs = [
  { key: 'overview', label: 'Vue d\'ensemble' },
  { key: 'dual', label: 'Vue duale' },
  { key: 'projects', label: 'Projets' },
  { key: 'invoices', label: 'Factures partenaires' },
  { key: 'distributions', label: 'Distributions' },
  { key: 'taxes', label: 'Déclarations taxes' },
]

const roleLabel: Record<string, string> = { MANDATAIRE: 'Mandataire (responsable)', PARTENAIRE: 'Partenaire' }
const roleBadge: Record<string, string> = { MANDATAIRE: 'badge-blue', PARTENAIRE: 'badge-amber' }
const statusLabel: Record<string, string> = { ACTIVE: 'Actif', COMPLETED: 'Terminé', CANCELLED: 'Annulé' }
const statusColor: Record<string, string> = { ACTIVE: 'badge-green', COMPLETED: 'badge-gray', CANCELLED: 'badge-red' }

function formatAmount(v: number): string {
  return v.toLocaleString('fr-CA', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}
</script>

<template>
  <div v-if="isLoading" class="py-12 text-center text-text-muted">Chargement...</div>
  <div v-else-if="!data" class="py-12 text-center text-text-muted">Consortium introuvable</div>
  <div v-else>
    <!-- Header -->
    <div class="page-header">
      <div>
        <button class="btn-back" @click="router.push('/consortiums')">&larr; Consortiums</button>
        <h1>{{ data.name }}</h1>
        <p class="header-sub">{{ data.client_name }}</p>
      </div>
      <div class="header-actions">
        <span class="badge" :class="roleBadge[String(data.pr_role)] || 'badge-gray'">
          {{ roleLabel[String(data.pr_role)] || data.pr_role }}
        </span>
        <span class="badge" :class="statusColor[String(data.status)] || 'badge-gray'">
          {{ statusLabel[String(data.status)] || data.status }}
        </span>
        <button class="btn-primary" @click="router.push(`/consortiums/${consortiumId}/edit`)">Modifier</button>
      </div>
    </div>

    <!-- Tabs -->
    <div class="tabs">
      <button v-for="tab in tabs" :key="tab.key" class="tab" :class="{ active: activeTab === tab.key }" @click="activeTab = tab.key">
        {{ tab.label }}
      </button>
    </div>

    <!-- ═══ Vue d'ensemble ═══ -->
    <template v-if="activeTab === 'overview'">
      <!-- KPIs -->
      <div class="kpi-grid">
        <div class="kpi-card"><div class="kpi-value">{{ members.length }}</div><div class="kpi-label">Membres</div></div>
        <div class="kpi-card"><div class="kpi-value" :class="totalCoeff === 100 ? 'text-success' : 'text-danger'">{{ totalCoeff }}%</div><div class="kpi-label">Coefficients</div></div>
        <div class="kpi-card"><div class="kpi-value">{{ Number(data.projects_count || 0) }}</div><div class="kpi-label">Projets</div></div>
        <div class="kpi-card"><div class="kpi-value mono">0,00 $</div><div class="kpi-label">CA Client</div></div>
      </div>

      <!-- Info cards -->
      <div class="grid-2">
        <div class="card">
          <h3>Informations</h3>
          <div class="info-row"><span>Client (donneur d'ouvrage)</span><p>{{ data.client_name }}</p></div>
          <div class="info-row"><span>Rôle PR</span><p>{{ roleLabel[String(data.pr_role)] }}</p></div>
          <div class="info-row"><span>Réf. contrat</span><p>{{ data.contract_reference || '—' }}</p></div>
          <div class="info-row"><span>Statut</span><p><span class="badge" :class="statusColor[String(data.status)]">{{ statusLabel[String(data.status)] }}</span></p></div>
        </div>
        <div class="card">
          <h3>Membres</h3>
          <table class="mini-table">
            <thead><tr><th>Membre</th><th>Spécialité</th><th class="text-right">%</th></tr></thead>
            <tbody>
              <tr v-for="m in members" :key="Number(m.id)">
                <td><span v-if="m.is_pr" class="pr-badge">PR</span> {{ m.display_name }}</td>
                <td class="text-muted">{{ m.specialty || '—' }}</td>
                <td class="text-right font-mono">{{ m.coefficient }}%</td>
              </tr>
            </tbody>
          </table>
          <div v-if="totalCoeff !== 100" class="coeff-warning">Total {{ totalCoeff }}% — doit être 100%</div>
        </div>
      </div>

      <div v-if="data.description" class="card" style="margin-top:12px;">
        <h3>Notes</h3>
        <p style="font-size:13px;">{{ data.description }}</p>
      </div>
    </template>

    <!-- ═══ Vue duale (FR61/FR62) ═══ -->
    <template v-if="activeTab === 'dual'">
      <div class="dual-grid">
        <!-- Panneau Consortium (bleu) -->
        <div class="dual-panel dual-consortium">
          <h3>Vue Consortium (client)</h3>
          <p class="dual-desc">Revenus et coûts du consortium envers le donneur d'ouvrage</p>
          <div class="dual-kpis">
            <div><span>CA Client</span><p class="mono">{{ formatAmount(financials.ca_client) }} $</p></div>
            <div><span>Coûts membres</span><p class="mono">{{ formatAmount(financials.costs_members) }} $</p></div>
            <div><span>Coûts ST</span><p class="mono">{{ formatAmount(financials.costs_st) }} $</p></div>
            <div><span>Marge</span><p class="mono">{{ formatAmount(financials.margin_consortium) }} $ ({{ financials.margin_pct }}%)</p></div>
          </div>
        </div>

        <!-- Panneau Provencher (jaune) -->
        <div class="dual-panel dual-provencher">
          <h3>Vue Provencher (firme)</h3>
          <p class="dual-desc">CA PR = factures au consortium + part de profit</p>
          <div class="dual-kpis">
            <div><span>Factures PR → Consortium</span><p class="mono">{{ formatAmount(financials.ca_pr_invoices) }} $</p></div>
            <div><span>Part de profit</span><p class="mono">{{ formatAmount(financials.ca_pr_profit_share) }} $</p></div>
            <div><span>CA Provencher total</span><p class="mono font-bold">{{ formatAmount(financials.ca_pr_total) }} $</p></div>
            <div><span>Coefficient PR</span><p class="mono">{{ financials.pr_coefficient }}%</p></div>
          </div>
        </div>
      </div>

      <!-- Alerte ratio effort vs coefficient -->
      <div class="alert-info" style="margin-top:12px;">
        Les données financières seront calculées automatiquement à partir des factures et feuilles de temps des projets liés au consortium.
      </div>

      <!-- Tableau comparatif 3 modes -->
      <div class="card" style="margin-top:12px;">
        <h3>Comparatif par partenaire — 3 modes de mesure</h3>
        <table class="data-table">
          <thead>
            <tr>
              <th>Partenaire</th>
              <th class="text-right">Coeff. contractuel</th>
              <th class="text-right">Effort (heures)</th>
              <th class="text-right">Effort ($)</th>
              <th class="text-right">Écart coeff/heures</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="m in members" :key="'cmp-' + Number(m.id)">
              <td><span v-if="m.is_pr" class="pr-badge">PR</span> {{ m.display_name }}</td>
              <td class="text-right font-mono">{{ m.coefficient }}%</td>
              <td class="text-right font-mono text-muted">0h (0%)</td>
              <td class="text-right font-mono text-muted">0,00 $ (0%)</td>
              <td class="text-right"><span class="badge badge-gray">n/d</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>

    <!-- ═══ Projets ═══ -->
    <template v-if="activeTab === 'projects'">
      <div class="tab-header">
        <h3>Projets associés au consortium</h3>
      </div>
      <div v-if="projectsLoading" class="empty">Chargement...</div>
      <div v-else-if="!projects.length" class="empty">Aucun projet associé à ce consortium</div>
      <table v-else class="data-table">
        <thead>
          <tr>
            <th>Code</th>
            <th>Projet</th>
            <th>Statut</th>
            <th>Règles</th>
            <th class="text-right">Budget ($)</th>
            <th class="text-right">Facturé ($)</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in projects" :key="Number(p.id)" class="cursor-pointer" @click="router.push(`/projects/${p.id}`)">
            <td class="font-mono font-semibold">{{ p.code }}</td>
            <td>{{ p.name }}</td>
            <td><span class="badge" :class="p.status === 'ACTIVE' ? 'badge-green' : 'badge-gray'">{{ p.status === 'ACTIVE' ? 'Actif' : p.status }}</span></td>
            <td><span class="badge badge-blue">Consortium</span></td>
            <td class="text-right font-mono text-muted">—</td>
            <td class="text-right font-mono text-muted">—</td>
          </tr>
        </tbody>
      </table>
      <div v-for="m in members" :key="'proj-m-' + Number(m.id)" class="card" style="margin-top:12px;">
        <h4 style="font-size:12px;font-weight:600;color:var(--color-gray-600);">
          <span v-if="m.is_pr" class="pr-badge">PR</span> {{ m.display_name }} — {{ m.coefficient }}%
        </h4>
        <p class="text-muted" style="font-size:12px;margin-top:4px;">Détail répartition par projet — données disponibles après saisie des feuilles de temps</p>
      </div>
    </template>

    <!-- ═══ Factures partenaires ═══ -->
    <template v-if="activeTab === 'invoices'">
      <!-- KPIs -->
      <div class="kpi-grid">
        <div class="kpi-card"><div class="kpi-value mono">0,00 $</div><div class="kpi-label">Total factures</div></div>
        <div class="kpi-card"><div class="kpi-value mono">0,00 $</div><div class="kpi-label">Par partenaire (moy.)</div></div>
        <div class="kpi-card"><div class="kpi-value">0</div><div class="kpi-label">En attente</div></div>
        <div class="kpi-card"><div class="kpi-value">0</div><div class="kpi-label">Autorisées</div></div>
      </div>

      <div class="tab-header" style="margin-top:12px;">
        <h3>Factures des partenaires</h3>
        <button class="btn-primary btn-sm">+ Saisir facture</button>
      </div>

      <div class="empty">
        Aucune facture partenaire enregistrée.<br>
        <span class="text-muted" style="font-size:11px;">Les factures seront groupées par Projet → Partenaire avec statuts Reçue / Autorisée / Payée.</span>
      </div>
    </template>

    <!-- ═══ Distributions profit ═══ -->
    <template v-if="activeTab === 'distributions'">
      <div class="kpi-grid">
        <div class="kpi-card"><div class="kpi-value mono">0,00 $</div><div class="kpi-label">Marge distribuable</div></div>
        <div class="kpi-card"><div class="kpi-value mono">0,00 $</div><div class="kpi-label">Distribué</div></div>
        <div class="kpi-card"><div class="kpi-value mono">0,00 $</div><div class="kpi-label">Non distribué</div></div>
        <div class="kpi-card"><div class="kpi-value text-muted">—</div><div class="kpi-label">Prochaine évaluation</div></div>
      </div>

      <div class="tab-header" style="margin-top:12px;">
        <h3>Historique des distributions</h3>
        <button class="btn-primary btn-sm">+ Nouvelle distribution</button>
      </div>

      <div class="empty">
        Aucune distribution enregistrée.<br>
        <span class="text-muted" style="font-size:11px;">Saisie manuelle : date, montant par membre, justification. Le workflow guidé (5 étapes) sera disponible en MVP-2.</span>
      </div>

      <!-- Simulateur placeholder -->
      <div class="card" style="margin-top:12px;">
        <h3>Simulateur de distribution</h3>
        <p class="text-muted" style="font-size:12px;">Sélectionnez un projet, un mode de calcul (coefficient / heures / $), et un montant pour simuler la répartition entre partenaires.</p>
        <div class="grid-3" style="margin-top:12px;">
          <div>
            <label class="field-label">Projet</label>
            <select class="field-input" disabled><option>— Sélectionner —</option></select>
          </div>
          <div>
            <label class="field-label">Mode</label>
            <select class="field-input" disabled>
              <option>Coefficient contractuel</option>
              <option>Effort en heures</option>
              <option>Effort en $</option>
            </select>
          </div>
          <div>
            <label class="field-label">Montant à distribuer</label>
            <input class="field-input" type="text" disabled placeholder="0,00 $" />
          </div>
        </div>
        <table v-if="members.length" class="data-table" style="margin-top:12px;">
          <thead><tr><th>Partenaire</th><th class="text-right">Coefficient</th><th class="text-right">Montant simulé</th></tr></thead>
          <tbody>
            <tr v-for="m in members" :key="'sim-' + Number(m.id)">
              <td><span v-if="m.is_pr" class="pr-badge">PR</span> {{ m.display_name }}</td>
              <td class="text-right font-mono">{{ m.coefficient }}%</td>
              <td class="text-right font-mono text-muted">0,00 $</td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>

    <!-- ═══ Déclarations taxes ═══ -->
    <template v-if="activeTab === 'taxes'">
      <!-- Config -->
      <div class="card">
        <h3>Configuration fiscale</h3>
        <div class="grid-3">
          <div class="info-row"><span>Fréquence</span><p>Trimestrielle</p></div>
          <div class="info-row"><span>No TPS</span><p>—</p></div>
          <div class="info-row"><span>No TVQ</span><p>—</p></div>
        </div>
      </div>

      <!-- Déclaration courante -->
      <div class="card" style="margin-top:12px;">
        <h3>Déclaration courante — TPS/TVQ</h3>
        <table class="data-table">
          <thead>
            <tr>
              <th>Taxe</th>
              <th class="text-right">Perçue sur ventes</th>
              <th class="text-right">CTI/RTI (crédits)</th>
              <th class="text-right">Ajustements</th>
              <th class="text-right">Net à remettre</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="font-semibold">TPS (5%)</td>
              <td class="text-right font-mono">0,00 $</td>
              <td class="text-right font-mono">0,00 $</td>
              <td class="text-right font-mono">0,00 $</td>
              <td class="text-right font-mono font-semibold">0,00 $</td>
            </tr>
            <tr>
              <td class="font-semibold">TVQ (9,975%)</td>
              <td class="text-right font-mono">0,00 $</td>
              <td class="text-right font-mono">0,00 $</td>
              <td class="text-right font-mono">0,00 $</td>
              <td class="text-right font-mono font-semibold">0,00 $</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Historique -->
      <div class="tab-header" style="margin-top:12px;">
        <h3>Historique des déclarations</h3>
      </div>
      <div class="empty">Aucune déclaration enregistrée</div>

      <!-- Conformité -->
      <div class="card" style="margin-top:12px;">
        <h3>Analyse de conformité fiscale</h3>
        <p class="text-muted" style="font-size:12px;">Vérifications automatiques : concordance ventes/TPS/TVQ, CTI/RTI vs factures, crédits non réclamés, ponctualité, variance cumulative. Disponible après enregistrement de la première déclaration.</p>
      </div>
    </template>
  </div>
</template>

<style scoped>
.page-header { display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 16px; }
.page-header h1 { font-size: 20px; font-weight: 700; color: var(--color-gray-900); margin-top: 2px; }
.header-sub { font-size: 13px; color: var(--color-gray-500); margin-top: 2px; }
.btn-back { background: none; border: none; font-size: 12px; color: var(--color-gray-500); cursor: pointer; padding: 0; }
.header-actions { display: flex; align-items: center; gap: 8px; }
.btn-primary { padding: 6px 14px; border-radius: 6px; font-size: 13px; font-weight: 600; background: var(--color-primary); color: white; border: none; cursor: pointer; }
.btn-sm { padding: 5px 12px; font-size: 12px; }

.tabs { display: flex; gap: 0; border-bottom: 2px solid var(--color-gray-200); margin-bottom: 16px; overflow-x: auto; }
.tab { padding: 8px 14px; font-size: 12px; font-weight: 500; color: var(--color-gray-500); cursor: pointer; border: none; background: none; border-bottom: 2px solid transparent; margin-bottom: -2px; white-space: nowrap; }
.tab.active { color: var(--color-primary); border-bottom-color: var(--color-primary); font-weight: 600; }

.badge { display: inline-flex; padding: 2px 10px; border-radius: 10px; font-size: 10px; font-weight: 600; }
.badge-green { background: #DCFCE7; color: #15803D; }
.badge-amber { background: #FEF3C7; color: #92400E; }
.badge-blue { background: #DBEAFE; color: #1D4ED8; }
.badge-gray { background: var(--color-gray-100); color: var(--color-gray-500); }
.badge-red { background: #FEE2E2; color: #DC2626; }

.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 16px; }
.kpi-card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 14px; text-align: center; }
.kpi-value { font-size: 24px; font-weight: 700; color: var(--color-gray-900); }
.kpi-value.mono { font-family: var(--font-mono); font-size: 20px; }
.kpi-label { font-size: 10px; color: var(--color-gray-500); text-transform: uppercase; font-weight: 600; margin-top: 4px; }
.text-success { color: #15803D; } .text-danger { color: #DC2626; } .text-muted { color: var(--color-gray-500); font-size: 12px; }

.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; }
.card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 16px; }
.card h3 { font-size: 11px; font-weight: 600; color: var(--color-gray-400); text-transform: uppercase; margin-bottom: 12px; }
.info-row { margin-bottom: 8px; }
.info-row span { display: block; font-size: 11px; color: var(--color-gray-500); }
.info-row p { font-weight: 600; font-size: 13px; margin: 2px 0 0; }

.mini-table { width: 100%; font-size: 12px; border-collapse: collapse; }
.mini-table th { font-size: 10px; font-weight: 600; text-transform: uppercase; color: var(--color-gray-400); padding: 4px 0; text-align: left; border-bottom: 1px solid var(--color-gray-200); }
.mini-table td { padding: 6px 0; border-bottom: 1px solid var(--color-gray-100); }
.mini-table .text-right { text-align: right; }
.font-mono { font-family: var(--font-mono); }

.pr-badge { display: inline-flex; padding: 1px 5px; border-radius: 3px; font-size: 9px; font-weight: 700; background: #DBEAFE; color: #1D4ED8; margin-right: 4px; }
.coeff-warning { margin-top: 8px; padding: 6px 10px; background: #FEF3C7; border-radius: 4px; font-size: 11px; color: #92400E; font-weight: 600; }

/* Dual view */
.dual-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.dual-panel { border-radius: 8px; padding: 20px; }
.dual-panel h3 { font-size: 14px; font-weight: 700; margin-bottom: 4px; }
.dual-desc { font-size: 11px; margin-bottom: 16px; }
.dual-consortium { background: #EFF6FF; border: 1px solid #BFDBFE; }
.dual-consortium h3 { color: #1D4ED8; }
.dual-consortium .dual-desc { color: #3B82F6; }
.dual-provencher { background: #FFFBEB; border: 1px solid #FDE68A; }
.dual-provencher h3 { color: #92400E; }
.dual-provencher .dual-desc { color: #D97706; }
.dual-kpis { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.dual-kpis > div span { display: block; font-size: 10px; color: var(--color-gray-500); text-transform: uppercase; font-weight: 600; }
.dual-kpis > div p { font-size: 16px; font-weight: 700; margin: 2px 0 0; color: var(--color-gray-900); }
.font-bold { font-weight: 700; }

.alert-info { padding: 10px 14px; background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 6px; font-size: 12px; color: #1D4ED8; }

.data-table { width: 100%; border-collapse: collapse; font-size: 13px; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.data-table thead th { padding: 8px 12px; font-size: 11px; font-weight: 600; text-transform: uppercase; color: var(--color-gray-500); background: var(--color-gray-50); border-bottom: 2px solid var(--color-gray-200); text-align: left; white-space: nowrap; }
.data-table tbody td { padding: 8px 12px; border-bottom: 1px solid var(--color-gray-100); text-align: left; vertical-align: middle; }
.data-table tbody tr:hover { background: var(--color-gray-50); }
.text-right { text-align: right !important; }
.font-semibold { font-weight: 600; }
.cursor-pointer { cursor: pointer; }

.tab-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
.tab-header h3 { font-size: 15px; font-weight: 600; color: var(--color-gray-800); }
.empty { text-align: center; padding: 24px; color: var(--color-gray-400); font-size: 13px; background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }

.field-label { display: block; font-size: 12px; font-weight: 600; color: var(--color-gray-600); margin-bottom: 4px; }
.field-input { width: 100%; padding: 8px 12px; border: 1px solid var(--color-gray-300); border-radius: 6px; font-size: 13px; }
</style>
