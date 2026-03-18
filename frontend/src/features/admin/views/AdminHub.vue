<script setup lang="ts">
const sections = [
  {
    key: 'org',
    title: 'Organisation',
    desc: 'Entités, unités d\'affaires, paramètres régionaux',
    icon: '🏢',
  },
  {
    key: 'users',
    title: 'Utilisateurs & Rôles',
    desc: 'Gestion des comptes, affectation des 8 rôles RBAC',
    icon: '👥',
  },
  {
    key: 'billing',
    title: 'Paramètres facturation',
    desc: 'Templates, taxes TPS/TVQ, termes de paiement',
    icon: '💰',
  },
  {
    key: 'categories',
    title: 'Catégories & Listes',
    desc: 'Catégories de dépenses, profils de poste, secteurs',
    icon: '📋',
  },
  {
    key: 'migration',
    title: 'Import / Migration',
    desc: 'ChangePoint import, Excel, réconciliation',
    icon: '📥',
  },
  {
    key: 'audit',
    title: 'Journal d\'audit',
    desc: 'Historique complet des modifications',
    icon: '🔍',
  },
]
</script>

<template>
  <div>
    <h1 class="mb-6 text-2xl font-semibold text-text">
      Administration
    </h1>

    <div class="grid grid-cols-3 gap-4">
      <div
        v-for="section in sections"
        :key="section.key"
        class="cursor-pointer rounded-lg border border-border bg-surface p-6 transition-colors hover:border-primary/30 hover:bg-primary/5"
      >
        <div class="mb-3 text-2xl">
          {{ section.icon }}
        </div>
        <h3 class="text-sm font-semibold text-text">
          {{ section.title }}
        </h3>
        <p class="mt-1 text-xs text-text-muted">
          {{ section.desc }}
        </p>
      </div>
    </div>
  </div>
</template>
