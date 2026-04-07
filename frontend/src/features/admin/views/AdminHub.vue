<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const sections = [
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
    title: 'Roadmap & Documentation',
    desc: 'Fonctionnalités complétées, planifiées et MVP-2',
    icon: '🗺️',
    route: '/admin/roadmap',
    ready: true,
  },
]

function navigate(section: typeof sections[0]) {
  if (section.ready) {
    router.push(section.route)
  }
}
</script>

<template>
  <div>
    <div class="page-header">
      <h1>Administration</h1>
    </div>

    <div class="admin-grid">
      <div
        v-for="section in sections"
        :key="section.key"
        class="admin-card"
        :class="{ disabled: !section.ready }"
        @click="navigate(section)"
      >
        <div class="admin-card-icon">{{ section.icon }}</div>
        <h3 class="admin-card-title">{{ section.title }}</h3>
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
