<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/plugins/axios'

const router = useRouter()
const downloadingDump = ref(false)
const dumpError = ref<string | null>(null)

interface AdminSection {
  key: string
  title: string
  desc: string
  icon: string
  route?: string
  action?: string
  ready: boolean
}

const sections: AdminSection[] = [
  {
    key: 'org',
    title: 'Organisation',
    desc: 'Entités, unités d\'affaires, paramètres régionaux',
    icon: '🏢',
    route: '/admin/org',
    ready: true,
  },
  {
    key: 'users',
    title: 'Utilisateurs & Rôles',
    desc: 'Gestion des comptes, affectation des 8 rôles RBAC',
    icon: '👥',
    route: '/admin/users',
    ready: true,
  },
  {
    key: 'billing',
    title: 'Paramètres facturation',
    desc: 'Templates de facture, niveaux de relance, taxes',
    icon: '💰',
    route: '/admin/billing',
    ready: true,
  },
  {
    key: 'categories',
    title: 'Catégories & Listes',
    desc: 'Catégories de dépenses, templates de projet',
    icon: '📋',
    route: '/admin/categories',
    ready: true,
  },
  {
    key: 'timesheet',
    title: 'Feuilles de temps',
    desc: 'Tâches obligatoires, projets internes (congés, administration…)',
    icon: '⏰',
    route: '/admin/timesheet',
    ready: true,
  },
  {
    key: 'standard-phases',
    title: 'Phases standard',
    desc: 'Jeu de phases du cabinet hérité par tout nouveau projet',
    icon: '🧱',
    route: '/admin/standard-phases',
    ready: true,
  },
  {
    key: 'standard-tasks',
    title: 'Tâches standard',
    desc: 'Catalogue de tâches et sous-tâches par phase, proposé au démarrage d\'un projet',
    icon: '🧩',
    route: '/admin/standard-tasks',
    ready: true,
  },
  {
    key: 'teams',
    title: 'Équipes',
    desc: 'Groupes d\'employés réutilisables, affectables en entier sur un projet (Finance/Paie/Admin)',
    icon: '👥',
    route: '/admin/teams',
    ready: true,
  },
  {
    key: 'holidays',
    title: 'Jours fériés',
    desc: 'Fériés par régime de travail (province) — pré-remplis dans les feuilles de temps',
    icon: '🎉',
    route: '/admin/holidays',
    ready: true,
  },
  {
    key: 'leave-types',
    title: 'Types de congés',
    desc: 'Vacances, maladie, personnel, parental — quotas et règles d\'accumulation',
    icon: '🏖️',
    route: '/admin/leave-types',
    ready: true,
  },
  {
    key: 'migration',
    title: 'Import / Migration',
    desc: 'ChangePoint import, Excel, réconciliation',
    icon: '📥',
    route: '/admin/import',
    ready: true,
  },
  {
    key: 'audit',
    title: 'Journal d\'audit',
    desc: 'Historique complet des modifications',
    icon: '🔍',
    route: '/admin/audit',
    ready: true,
  },
  {
    key: 'roadmap',
    title: 'Roadmap',
    desc: 'Fonctionnalités complétées, planifiées et MVP-2',
    icon: '🗺️',
    route: '/admin/roadmap',
    ready: true,
  },
  {
    key: 'docs',
    title: 'Documentation',
    desc: 'Architecture, API, modules, installation, tests',
    icon: '📖',
    route: '/admin/docs',
    ready: true,
  },
  {
    key: 'db-dump',
    title: 'Sauvegarde / Dump',
    desc: 'Télécharger un dump pg_dump de la base courante (support, mirroring local)',
    icon: '💾',
    action: 'download-dump',
    ready: true,
  },
]

async function downloadDump() {
  if (downloadingDump.value) return
  downloadingDump.value = true
  dumpError.value = null
  try {
    const resp = await apiClient.get('admin/db-dump/', { responseType: 'blob' })
    const cd = (resp.headers['content-disposition'] || '') as string
    const match = cd.match(/filename="?([^";]+)"?/i)
    const filename = (match && match[1]) || 'erp-dump.dump'
    const url = window.URL.createObjectURL(resp.data as Blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    document.body.appendChild(a)
    a.click()
    a.remove()
    window.URL.revokeObjectURL(url)
  } catch (e: unknown) {
    const err = e as { response?: { data?: { error?: { message?: string } } } }
    dumpError.value = err?.response?.data?.error?.message ?? 'Erreur lors du téléchargement du dump.'
  } finally {
    downloadingDump.value = false
  }
}

function navigate(section: AdminSection) {
  if (!section.ready) return
  if (section.action === 'download-dump') {
    downloadDump()
    return
  }
  if (section.route) router.push(section.route)
}
</script>

<template>
  <div>
    <div class="page-header">
      <h1>Administration</h1>
    </div>

    <div v-if="dumpError" class="dump-error">{{ dumpError }}</div>

    <div class="admin-grid">
      <div
        v-for="section in sections"
        :key="section.key"
        class="admin-card"
        :class="{ disabled: !section.ready }"
        @click="navigate(section)"
      >
        <div class="admin-card-icon">{{ section.icon }}</div>
        <h3 class="admin-card-title">
          {{ section.title }}
          <span v-if="section.action === 'download-dump' && downloadingDump" class="dump-loading">…</span>
        </h3>
        <p class="admin-card-desc">{{ section.desc }}</p>
        <span v-if="!section.ready" class="admin-card-badge">À venir</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}
.page-header h1 {
  font-size: 24px;
  font-weight: 700;
  color: var(--color-gray-900);
}
.admin-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}
.admin-card {
  position: relative;
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06);
  padding: 24px;
  cursor: pointer;
  transition: all 0.15s;
  border: 1px solid transparent;
}
.admin-card:hover:not(.disabled) {
  border-color: var(--color-primary);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07), 0 2px 4px rgba(0, 0, 0, 0.06);
}
.admin-card.disabled {
  opacity: 0.6;
  cursor: default;
}
.admin-card-icon {
  font-size: 28px;
  margin-bottom: 12px;
}
.admin-card-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-gray-800);
  margin-bottom: 4px;
}
.admin-card-desc {
  font-size: 13px;
  color: var(--color-gray-500);
}
.admin-card-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  font-size: 11px;
  font-weight: 600;
  padding: 2px 10px;
  border-radius: 12px;
  background: var(--color-gray-100);
  color: var(--color-gray-500);
}
</style>
