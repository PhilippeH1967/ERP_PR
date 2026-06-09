<script setup lang="ts">
/**
 * Contrôles de blocage de saisie pour un nœud (phase / tâche / sous-tâche) de
 * l'onglet Équipe. Affiche les personnes bloquées (chips rouges + débloquer) et
 * un sélecteur pour bloquer un membre du projet. Le POST/DELETE est géré par le
 * parent (émissions `block` / `unblock`).
 */
import { computed, ref } from 'vue'

interface BlockChip { id: number; employee_name: string }
interface Member { id: number; name: string }

const props = defineProps<{ blocks: BlockChip[]; candidates: Member[] }>()
const emit = defineEmits<{ block: [number]; unblock: [number] }>()

const open = ref(false)
const search = ref('')

const filtered = computed(() => {
  const q = search.value.trim().toLowerCase()
  return props.candidates.filter((m) => !q || m.name.toLowerCase().includes(q)).slice(0, 20)
})

function pick(id: number) {
  emit('block', id)
  open.value = false
  search.value = ''
}
</script>

<template>
  <span class="nbc">
    <span
      v-for="b in blocks" :key="b.id"
      class="person-chip person-chip--blocked"
      title="Saisie bloquée pour cette personne"
      data-block-chip
    >
      🔒 {{ b.employee_name }}
      <button class="nbc-x" data-unblock title="Débloquer" @click.stop="emit('unblock', b.id)">×</button>
    </span>
    <button class="nbc-btn" data-block-toggle :title="open ? 'Fermer' : 'Bloquer la saisie pour une personne'" @click.stop="open = !open">🔓 Bloquer</button>
    <div v-if="open" class="nbc-picker" @click.stop>
      <input
        v-model="search" type="text" class="nbc-search"
        placeholder="Rechercher un membre à bloquer…" data-block-search
      />
      <div v-if="!filtered.length" class="nbc-empty">Aucun membre disponible</div>
      <button
        v-for="m in filtered" :key="m.id"
        class="nbc-item" data-block-candidate
        @click.stop="pick(m.id)"
      >🔒 {{ m.name }}</button>
    </div>
  </span>
</template>

<style scoped>
.nbc { display: inline-flex; align-items: center; gap: 4px; position: relative; }
.person-chip--blocked { background: #FEE2E2; color: #B91C1C; border: 1px solid #FCA5A5; }
.nbc-x { background: none; border: none; color: #B91C1C; cursor: pointer; font-size: 12px; padding: 0 2px; line-height: 1; }
.nbc-btn { background: none; border: none; cursor: pointer; font-size: 11px; opacity: 0.55; padding: 0 2px; }
.nbc-btn:hover { opacity: 1; }
.nbc-picker { position: absolute; top: 100%; right: 0; z-index: 50; background: white; border: 1px solid var(--color-gray-200); border-radius: 6px; box-shadow: 0 4px 10px rgba(0,0,0,0.12); padding: 6px; min-width: 200px; max-height: 240px; overflow-y: auto; }
.nbc-search { width: 100%; padding: 5px 8px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 12px; margin-bottom: 4px; box-sizing: border-box; }
.nbc-item { display: block; width: 100%; text-align: left; background: none; border: none; padding: 5px 8px; font-size: 12px; cursor: pointer; border-radius: 4px; color: var(--color-gray-700); }
.nbc-item:hover { background: var(--color-gray-50); }
.nbc-empty { padding: 6px 8px; font-size: 11px; color: var(--color-gray-400); }
</style>
