<script setup lang="ts">
/**
 * HelpPanel — panneau d'aide contextuelle ouvert par le « ? » de la barre du
 * haut. Le contenu dépend de l'écran courant (route + onglet de la fiche
 * projet) et renvoie vers la section correspondante du guide complet (/help).
 */
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { resolveHelpContext } from '../helpContent'

const props = defineProps<{ open: boolean }>()
const emit = defineEmits<{ close: [] }>()

const route = useRoute()
const context = computed(() =>
  resolveHelpContext(route.path, typeof route.query.tab === 'string' ? route.query.tab : undefined),
)
const guideLink = computed(() => ({ path: '/help', query: { section: context.value.guideSection } }))

void props
</script>

<template>
  <Teleport to="body">
    <div v-if="open" class="hp-overlay" @click.self="emit('close')">
      <div class="hp-panel" data-help-panel>
        <div class="hp-head">
          <h2 data-help-title>{{ context.title }}</h2>
          <button class="hp-x" aria-label="Fermer" @click="emit('close')">&times;</button>
        </div>
        <div class="hp-body">
          <p class="hp-intro">{{ context.intro }}</p>
          <h4 class="hp-sub">Ce que vous pouvez faire ici</h4>
          <div v-for="(it, i) in context.items" :key="i" class="hp-item" data-help-item>
            <div class="hp-item-title">{{ it.title }}</div>
            <div class="hp-item-body">{{ it.body }}</div>
          </div>
          <template v-if="context.tips?.length">
            <h4 class="hp-sub">💡 Astuces</h4>
            <p v-for="(tp, i) in context.tips" :key="i" class="hp-tip">{{ tp }}</p>
          </template>
        </div>
        <div class="hp-foot">
          <RouterLink :to="guideLink" class="hp-guide" data-help-guide-link @click="emit('close')">
            📖 Ouvrir le guide complet →
          </RouterLink>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.hp-overlay { position: fixed; inset: 0; z-index: 9500; background: rgba(0,0,0,0.25); display: flex; justify-content: flex-end; }
.hp-panel { width: 400px; max-width: 92vw; height: 100%; background: #fff; box-shadow: -6px 0 24px rgba(0,0,0,0.16); display: flex; flex-direction: column; }
.hp-head { display: flex; align-items: center; gap: 10px; padding: 16px 18px; border-bottom: 1px solid var(--color-gray-200); }
.hp-head h2 { font-size: 15px; font-weight: 800; margin: 0; flex: 1; color: var(--color-gray-900); }
.hp-x { background: none; border: none; font-size: 22px; color: var(--color-gray-400); cursor: pointer; }
.hp-body { flex: 1; overflow-y: auto; padding: 14px 18px; }
.hp-intro { font-size: 13px; color: var(--color-gray-600); margin: 0 0 12px; }
.hp-sub { font-size: 10px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.04em; color: var(--color-gray-500); margin: 14px 0 8px; }
.hp-item { padding: 8px 10px; border: 1px solid var(--color-gray-100); border-radius: 8px; margin-bottom: 6px; background: var(--color-gray-50); }
.hp-item-title { font-size: 12px; font-weight: 700; color: var(--color-gray-800); }
.hp-item-body { font-size: 12px; color: var(--color-gray-600); margin-top: 2px; line-height: 1.45; }
.hp-tip { font-size: 12px; color: var(--color-gray-600); background: #FFFBEB; border: 1px solid #FDE68A; border-radius: 8px; padding: 8px 10px; margin: 0 0 6px; }
.hp-foot { padding: 12px 18px; border-top: 1px solid var(--color-gray-200); background: var(--color-gray-50); }
.hp-guide { font-size: 12px; font-weight: 700; color: var(--color-primary); text-decoration: none; }
.hp-guide:hover { text-decoration: underline; }
</style>
