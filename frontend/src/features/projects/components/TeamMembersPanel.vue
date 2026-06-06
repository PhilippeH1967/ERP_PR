<script setup lang="ts">
import { ref, computed } from 'vue'

interface Member { id: number; name: string }
interface AddableUser { id: number; username: string }

const props = withDefaults(
  defineProps<{
    members: Member[]
    addableUsers: AddableUser[]
    canManage: boolean
    saving?: boolean
    error?: string
  }>(),
  { saving: false, error: '' },
)

const emit = defineEmits<{
  (e: 'add', userId: number): void
  (e: 'remove', userId: number): void
}>()

const addingMemberId = ref<number | null>(null)
const removingMemberId = ref<number | null>(null)

// Dropdown recherchable : filtre la liste par nom (côté client).
const memberSearch = ref('')
const showMemberList = ref(false)
const filteredAddable = computed(() => {
  const q = memberSearch.value.trim().toLowerCase()
  if (!q) return props.addableUsers
  return props.addableUsers.filter((u) => u.username.toLowerCase().includes(q))
})
function pickMember(u: AddableUser) {
  addingMemberId.value = u.id
  memberSearch.value = u.username
  showMemberList.value = false
}
function onSearchBlur() {
  // Léger délai pour laisser le clic sur un item se déclencher avant fermeture.
  setTimeout(() => { showMemberList.value = false }, 150)
}

function confirmAdd() {
  if (!addingMemberId.value) return
  emit('add', addingMemberId.value)
  addingMemberId.value = null
  memberSearch.value = ''
  showMemberList.value = false
}

function confirmRemove(userId: number) {
  removingMemberId.value = null
  emit('remove', userId)
}
</script>

<template>
  <div class="virtuals-panel" data-members-panel>
    <div class="virtuals-header">
      <span class="virtuals-title">Membres de l'équipe</span>
      <span v-if="members.length" class="virtuals-count">
        {{ members.length }} membre{{ members.length > 1 ? 's' : '' }}
      </span>
    </div>
    <p class="virtuals-hint">
      Un membre peut saisir des heures sur ce projet <strong>même sans planification</strong>.
      Ajoutez ici les personnes affectées au projet qui ne sont pas (encore) planifiées.
    </p>

    <div v-if="members.length" class="members-list">
      <div v-for="m in members" :key="m.id" class="virtual-row" data-member-row>
        <div class="virtual-info">
          <span class="team-avatar">{{ m.name.substring(0, 2).toUpperCase() }}</span>
          <div class="virtual-name">{{ m.name }}</div>
        </div>
        <template v-if="canManage">
          <div v-if="removingMemberId === m.id" class="virtual-replace-form">
            <span class="members-confirm-label">Retirer ce membre ?</span>
            <button
              class="btn-action primary"
              data-member-remove-confirm
              @click="confirmRemove(m.id)"
            >
              Confirmer
            </button>
            <button class="btn-action" @click="removingMemberId = null">Annuler</button>
          </div>
          <button
            v-else
            class="btn-action"
            data-member-remove-start
            @click="removingMemberId = m.id"
          >
            Retirer…
          </button>
        </template>
      </div>
    </div>
    <div v-else class="virtuals-empty" data-members-empty>
      Aucun membre ajouté.<br>
      <span class="virtuals-empty-hint">
        Les employés planifiés sur le projet peuvent déjà saisir leurs heures.
        Ajoutez un membre pour autoriser la saisie sans planification.
      </span>
    </div>

    <div v-if="canManage" class="members-add">
      <div class="member-search-wrap">
        <input
          v-model="memberSearch"
          class="select-sm member-search-input"
          placeholder="Rechercher un membre par nom…"
          data-member-add-search
          @focus="showMemberList = true"
          @input="showMemberList = true; addingMemberId = null"
          @blur="onSearchBlur"
        />
        <div v-if="showMemberList && filteredAddable.length" class="member-search-list" data-member-search-list>
          <button
            v-for="u in filteredAddable"
            :key="u.id"
            type="button"
            class="member-search-item"
            :class="{ active: addingMemberId === u.id }"
            @mousedown.prevent="pickMember(u)"
          >{{ u.username }}</button>
        </div>
        <div v-else-if="showMemberList && memberSearch.trim()" class="member-search-empty">Aucun membre trouvé</div>
      </div>
      <button
        class="btn-action primary"
        :disabled="!addingMemberId || saving"
        data-member-add-confirm
        @click="confirmAdd"
      >
        {{ saving ? '…' : 'Ajouter' }}
      </button>
      <div v-if="error" class="virtual-error" data-member-error>{{ error }}</div>
    </div>
  </div>
</template>

<style scoped>
.virtuals-panel { background: var(--color-gray-50); border: 1px solid var(--color-gray-200); border-radius: 6px; padding: 12px; margin-bottom: 16px; }
.virtuals-header { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }
.virtuals-title { font-size: 11px; font-weight: 600; color: var(--color-gray-500); text-transform: uppercase; }
.virtuals-count { font-size: 11px; color: var(--color-primary); font-weight: 600; }
.virtuals-hint { font-size: 12px; color: var(--color-gray-600); margin-bottom: 10px; }
.virtuals-empty { font-size: 13px; color: var(--color-gray-600); padding: 8px 0; }
.virtuals-empty-hint { font-size: 12px; color: var(--color-gray-500); }
.virtual-row { display: flex; align-items: center; justify-content: space-between; gap: 8px; padding: 6px 8px; background: var(--color-white); border: 1px solid var(--color-gray-200); border-radius: 4px; }
.virtual-info { display: flex; align-items: center; gap: 8px; }
.virtual-name { font-size: 13px; font-weight: 500; }
.team-avatar { display: inline-flex; align-items: center; justify-content: center; width: 28px; height: 28px; border-radius: 50%; background: var(--color-primary); color: var(--color-white); font-size: 11px; font-weight: 600; }
.virtual-replace-form { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }
.virtual-error { flex-basis: 100%; font-size: 11px; color: var(--color-danger); }
.members-list { display: flex; flex-direction: column; gap: 6px; margin-bottom: 10px; }
.members-add { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; padding-top: 10px; border-top: 1px solid var(--color-gray-200); }
.members-add .select-sm { padding: 4px 8px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 12px; min-width: 200px; }
.members-confirm-label { font-size: 12px; color: var(--color-gray-600); }
.member-search-wrap { position: relative; min-width: 220px; }
.member-search-input { width: 100%; box-sizing: border-box; }
.member-search-list { position: absolute; top: 100%; left: 0; right: 0; z-index: 20; max-height: 210px; overflow-y: auto; background: var(--color-white); border: 1px solid var(--color-gray-300); border-radius: 4px; box-shadow: 0 4px 10px rgba(0,0,0,0.08); margin-top: 2px; }
.member-search-item { display: block; width: 100%; text-align: left; padding: 6px 10px; font-size: 12px; background: none; border: none; cursor: pointer; color: var(--color-gray-700); }
.member-search-item:hover, .member-search-item.active { background: #EFF6FF; color: var(--color-primary); }
.member-search-empty { position: absolute; top: 100%; left: 0; right: 0; z-index: 20; background: var(--color-white); border: 1px solid var(--color-gray-200); border-radius: 4px; padding: 8px 10px; font-size: 12px; color: var(--color-gray-400); margin-top: 2px; }
</style>
