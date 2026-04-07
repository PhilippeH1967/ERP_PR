<script setup lang="ts">
const version = 'v1.2.000'
const lastUpdate = '2026-04-07'

interface RoadmapItem {
  id: string; feature: string; fr: string; status: 'done' | 'partial' | 'planned' | 'mvp2'
  bloc: number; notes: string
}

const items: RoadmapItem[] = [
  // Bloc 1
  { id: 'B1-01', feature: 'Projets CRUD + WBS Option B (Phase→Tâche)', fr: 'FR1-FR10', status: 'done', bloc: 1, notes: '12 modèles, wizard 5 étapes, templates 7 phases + 23 tâches' },
  { id: 'B1-02', feature: 'Clients 5 onglets', fr: 'FR1', status: 'done', bloc: 1, notes: 'CRUD, contacts, adresses, financier, recherche live' },
  { id: 'B1-03', feature: 'Consortium FR59 + Vue duale FR61/FR62', fr: 'FR59-FR64', status: 'done', bloc: 1, notes: 'Entity, membres, 6 onglets, panneau bleu/jaune' },
  { id: 'B1-04', feature: 'Gantt interactif (phases, zoom, jalons)', fr: 'US-PL06', status: 'done', bloc: 1, notes: 'Composant Vue 3 custom, 3 zooms, édition dates' },
  { id: 'B1-05', feature: 'Sous-tâches 3 niveaux WBS', fr: 'FR1e', status: 'done', bloc: 1, notes: 'Phase → Tâche → Sous-tâche' },
  { id: 'B1-06', feature: 'Transfert de responsable', fr: 'FR15d', status: 'done', bloc: 1, notes: '/projects/transfer avec historique' },
  { id: 'B1-07', feature: 'Public/Privé, Services transversaux', fr: 'FR10', status: 'done', bloc: 1, notes: '7 services (BIM, Paysage, DD...)' },
  { id: 'B1-08', feature: 'Dépendances entre phases (FS/SS)', fr: 'US-PL06', status: 'done', bloc: 1, notes: 'Modèle PhaseDependency, API CRUD' },
  { id: 'B1-09', feature: 'Consortium règles partage variables', fr: 'FR59b-FR59c', status: 'mvp2', bloc: 1, notes: '3 modes mesure, seuil, fréquence' },
  { id: 'B1-10', feature: 'Gantt avancé (drag-drop, chemin critique)', fr: 'US-PL06', status: 'mvp2', bloc: 1, notes: 'Drag natif, auto-scheduling' },

  // Bloc 2
  { id: 'B2-01', feature: 'Feuilles de temps par tâche WBS', fr: 'FR16-FR19', status: 'done', bloc: 2, notes: 'Grille, dropdown WBS groupé par phase' },
  { id: 'B2-02', feature: 'Approbation 3 niveaux (PM/Finance/Paie)', fr: 'FR21-FR22c', status: 'done', bloc: 2, notes: '11 contrôles paie, anti-self-approval' },
  { id: 'B2-03', feature: 'Period locking (freeze + unlock)', fr: 'FR27f-FR27i', status: 'done', bloc: 2, notes: 'Gel global, exceptions, verrouillage phase/personne' },
  { id: 'B2-04', feature: 'Heures contrat dynamiques (labor_rule)', fr: 'FR78', status: 'done', bloc: 2, notes: 'Override > LaborRule > 40h défaut' },
  { id: 'B2-05', feature: 'Relances retardataires (Wed/Fri + escalade)', fr: 'FR26', status: 'done', bloc: 2, notes: 'Celery tasks, email + notification' },
  { id: 'B2-06', feature: 'Corrections rétrospectives Finance', fr: 'FR25', status: 'done', bloc: 2, notes: 'bulk_correct API avec audit trail' },
  { id: 'B2-07', feature: 'Congés/Absences (7 types Québec)', fr: 'Module J', status: 'done', bloc: 2, notes: 'Workflow, banque, auto-create TimeEntry' },
  { id: 'B2-08', feature: 'Fournisseurs/ST (6/6 entités)', fr: 'FR47-FR52', status: 'done', bloc: 2, notes: 'Batch, disputes, holdbacks, summary' },
  { id: 'B2-09', feature: 'Planification ressources + charge', fr: 'US-PL01/PL11', status: 'done', bloc: 2, notes: 'Allocations, surcharge/sous-charge, disponibilité' },
  { id: 'B2-10', feature: 'Import absences HRIS', fr: 'FR27b', status: 'mvp2', bloc: 2, notes: 'Modèle prêt, import handler à créer' },
  { id: 'B2-11', feature: 'Auto-expiry PeriodUnlock', fr: 'FR27c', status: 'mvp2', bloc: 2, notes: 'Celery task à créer' },

  // Bloc 3
  { id: 'B3-01', feature: 'Taxes configurables (6 schémas)', fr: 'FR83', status: 'done', bloc: 3, notes: 'QC, ON, AB, BC, FR, Exonéré' },
  { id: 'B3-02', feature: 'Facturation 7 colonnes + workflow 5 étapes', fr: 'FR30-FR35', status: 'done', bloc: 3, notes: 'Draft→Submit→Approve→Send→Paid' },
  { id: 'B3-03', feature: 'Notes de crédit, paiements, retenues', fr: 'FR36-FR39', status: 'done', bloc: 3, notes: 'CRUD complet' },
  { id: 'B3-04', feature: 'Dépenses (15 catégories, upload reçu)', fr: 'FR40-FR46', status: 'done', bloc: 3, notes: 'Workflow 6 étapes, refacturation' },
  { id: 'B3-05', feature: 'Exports Intacct Phase 1 (CSV)', fr: 'FR84', status: 'done', bloc: 3, notes: '4 types: factures, paiements, dépenses, temps' },
  { id: 'B3-06', feature: 'Intacct Phase 2-3 (API bidirectionnelle)', fr: 'FR84', status: 'mvp2', bloc: 3, notes: 'Sync temps réel, non commencé' },

  // Bloc 4
  { id: 'B4-01', feature: 'Dashboard 5 rôles', fr: 'FR72', status: 'done', bloc: 4, notes: 'Employé, PM, Finance, Directeur, Admin' },
  { id: 'B4-02', feature: 'KPIs PM (CA/salaires, taux facturation)', fr: 'FR73', status: 'done', bloc: 4, notes: 'Ratio cible 2.5x, carnet commandes' },
  { id: 'B4-03', feature: 'Rapports heures (projet/employé/BU)', fr: 'FR74', status: 'done', bloc: 4, notes: 'Page /reports avec filtres + export CSV' },
  { id: 'B4-04', feature: 'System health enrichi', fr: 'FR75', status: 'done', bloc: 4, notes: 'Actifs cette semaine, entrées 7j' },
  { id: 'B4-05', feature: 'Import 13 types (ref + transactionnel)', fr: 'FR84/FR93', status: 'done', bloc: 4, notes: '6 ref data + 7 transactional' },
  { id: 'B4-06', feature: 'Sécurité route guards RBAC', fr: 'FR72', status: 'done', bloc: 4, notes: 'EMPLOYEE bloqué billing/admin/consortiums' },
  { id: 'B4-07', feature: 'ChangePoint migration complète', fr: 'FR84-FR85', status: 'mvp2', bloc: 4, notes: '10+ ans historique, réconciliation' },
  { id: 'B4-08', feature: 'Propositions de services', fr: 'FR53', status: 'mvp2', bloc: 4, notes: 'Lifecycle, conversion projet, reporting' },
  { id: 'B4-09', feature: 'WebSocket temps réel', fr: 'NFR32', status: 'mvp2', bloc: 4, notes: 'Period locks, présence éditeur' },
]

const blocLabels: Record<number, string> = { 1: 'Bloc 1 — Projets', 2: 'Bloc 2 — Production', 3: 'Bloc 3 — Financier', 4: 'Bloc 4 — Pilotage' }
const statusLabels: Record<string, string> = { done: 'Complété', partial: 'Partiel', planned: 'Planifié', mvp2: 'MVP-2' }
const statusColors: Record<string, string> = { done: 'badge-green', partial: 'badge-amber', planned: 'badge-blue', mvp2: 'badge-gray' }

const stats = {
  done: items.filter(i => i.status === 'done').length,
  partial: items.filter(i => i.status === 'partial').length,
  planned: items.filter(i => i.status === 'planned').length,
  mvp2: items.filter(i => i.status === 'mvp2').length,
  total: items.length,
}
</script>

<template>
  <div>
    <div class="mb-6 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-semibold text-text">Roadmap fonctionnelle</h1>
        <p class="text-sm text-text-muted">PR|ERP {{ version }} — Dernière mise à jour : {{ lastUpdate }}</p>
      </div>
    </div>

    <!-- KPIs -->
    <div class="mb-6 grid grid-cols-5 gap-4">
      <div class="kpi-card"><div class="kpi-value text-success">{{ stats.done }}</div><div class="kpi-label">Complétés</div></div>
      <div class="kpi-card"><div class="kpi-value text-warning">{{ stats.partial }}</div><div class="kpi-label">Partiels</div></div>
      <div class="kpi-card"><div class="kpi-value text-primary">{{ stats.planned }}</div><div class="kpi-label">Planifiés</div></div>
      <div class="kpi-card"><div class="kpi-value text-muted">{{ stats.mvp2 }}</div><div class="kpi-label">MVP-2</div></div>
      <div class="kpi-card"><div class="kpi-value">{{ stats.total }}</div><div class="kpi-label">Total</div></div>
    </div>

    <!-- Progress bar -->
    <div class="mb-6">
      <div class="mb-1 flex justify-between text-xs text-text-muted">
        <span>Progression globale</span>
        <span>{{ Math.round(stats.done / stats.total * 100) }}%</span>
      </div>
      <div class="h-3 w-full overflow-hidden rounded-full bg-gray-200">
        <div class="h-3 rounded-full bg-success transition-all" :style="{ width: Math.round(stats.done / stats.total * 100) + '%' }"></div>
      </div>
    </div>

    <!-- Table by bloc -->
    <div v-for="bloc in [1, 2, 3, 4]" :key="bloc" class="mb-6">
      <h2 class="mb-3 text-sm font-semibold uppercase tracking-wide text-text-muted">{{ blocLabels[bloc] }}</h2>
      <div class="rounded-lg border border-border bg-surface">
        <table class="w-full text-left text-sm">
          <thead class="border-b border-border text-xs font-medium uppercase tracking-wide text-text-muted">
            <tr>
              <th class="px-4 py-2" style="width:70px;">ID</th>
              <th class="px-4 py-2">Fonctionnalité</th>
              <th class="px-4 py-2" style="width:100px;">Référence</th>
              <th class="px-4 py-2" style="width:90px;">Statut</th>
              <th class="px-4 py-2">Notes</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in items.filter(i => i.bloc === bloc)" :key="item.id" class="border-b border-border last:border-0">
              <td class="px-4 py-2 font-mono text-xs text-text-muted">{{ item.id }}</td>
              <td class="px-4 py-2 font-medium">{{ item.feature }}</td>
              <td class="px-4 py-2 font-mono text-xs text-text-muted">{{ item.fr }}</td>
              <td class="px-4 py-2">
                <span class="badge" :class="statusColors[item.status]">{{ statusLabels[item.status] }}</span>
              </td>
              <td class="px-4 py-2 text-xs text-text-muted">{{ item.notes }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<style scoped>
.kpi-card { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 14px; text-align: center; }
.kpi-value { font-size: 28px; font-weight: 700; }
.kpi-label { font-size: 10px; color: var(--color-gray-500); text-transform: uppercase; font-weight: 600; margin-top: 4px; }
.text-success { color: #15803D; } .text-warning { color: #92400E; } .text-primary { color: #1D4ED8; } .text-muted { color: var(--color-gray-500); }
.badge { display: inline-flex; padding: 2px 10px; border-radius: 10px; font-size: 10px; font-weight: 600; }
.badge-green { background: #DCFCE7; color: #15803D; }
.badge-amber { background: #FEF3C7; color: #92400E; }
.badge-blue { background: #DBEAFE; color: #1D4ED8; }
.badge-gray { background: var(--color-gray-100); color: var(--color-gray-500); }
.bg-success { background: #15803D; }
</style>
