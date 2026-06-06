<script setup lang="ts">
/**
 * TaskTemplatePicker — démarrage d'un projet VIDE depuis le catalogue de tâches
 * standard (paramétrage admin), groupées par phase. L'utilisateur coche/décoche
 * puis crée les tâches. Ne s'affiche QUE si le projet n'a aucune tâche
 * (has_tasks=False) ; dès qu'il y a des tâches, le composant disparaît.
 *
 * La création réutilise l'endpoint tasks/ existant (wbs_code auto-généré côté
 * backend) — la logique de gestion des tâches n'est pas modifiée.
 */
import { ref, computed, onMounted } from 'vue'
import { projectApi } from '../api/projectApi'

const props = defineProps<{ projectId: number }>()
const emit = defineEmits<{ created: [] }>()

interface SuggTask { name: string; client_facing_label: string; billing_mode: string }
interface SuggGroup { phase_id: number; phase_code: string; phase_name: string; tasks: SuggTask[] }

const groups = ref<SuggGroup[]>([])
const hasTasks = ref(true) // masqué par défaut tant que non chargé
const loading = ref(true)
const creating = ref(false)
const error = ref('')
const selected = ref<Set<string>>(new Set())

function k(g: SuggGroup, i: number): string { return `${g.phase_id}:${i}` }

async function load() {
  loading.value = true
  try {
    const r = await projectApi.taskSuggestions(props.projectId)
    const d = r.data?.data || r.data
    hasTasks.value = !!d.has_tasks
    groups.value = d.groups || []
    // Tout coché par défaut : on part du jeu standard, on retire l'inutile.
    const s = new Set<string>()
    groups.value.forEach((g) => g.tasks.forEach((_, i) => s.add(k(g, i))))
    selected.value = s
  } catch {
    groups.value = []
    hasTasks.value = true
  } finally {
    loading.value = false
  }
}
onMounted(load)

const visible = computed(() => !loading.value && !hasTasks.value && groups.value.length > 0)
const selectedCount = computed(() => selected.value.size)

function isChecked(g: SuggGroup, i: number): boolean { return selected.value.has(k(g, i)) }
function toggle(g: SuggGroup, i: number) {
  const key = k(g, i)
  const s = new Set(selected.value)
  if (s.has(key)) s.delete(key)
  else s.add(key)
  selected.value = s
}

async function createSelected() {
  error.value = ''
  creating.value = true
  try {
    for (const g of groups.value) {
      for (let i = 0; i < g.tasks.length; i++) {
        if (!selected.value.has(k(g, i))) continue
        const t = g.tasks[i]!
        await projectApi.createTask(props.projectId, {
          phase: g.phase_id, name: t.name, task_type: 'TASK', billing_mode: t.billing_mode,
        })
      }
    }
    emit('created')
  } catch {
    error.value = 'Échec de la création de certaines tâches. Réessayez.'
  } finally {
    creating.value = false
  }
}
</script>

<template>
  <div v-if="visible" class="ttp" data-task-picker>
    <div class="ttp-head">
      <div>
        <h4 class="ttp-title">Démarrer depuis un modèle</h4>
        <p class="ttp-sub">
          Ce projet n'a aucune tâche. Cochez les tâches standard à créer par phase
          (vous pourrez les modifier ou en ajouter ensuite).
        </p>
      </div>
      <button
        class="ttp-create"
        :disabled="creating || selectedCount === 0"
        data-create-tasks
        @click="createSelected"
      >
        {{ creating ? 'Création…' : `Créer les tâches sélectionnées (${selectedCount})` }}
      </button>
    </div>
    <p v-if="error" class="ttp-error" data-error>{{ error }}</p>
    <div class="ttp-groups">
      <div v-for="g in groups" :key="g.phase_id" class="ttp-group">
        <div class="ttp-phase">{{ g.phase_code }} · {{ g.phase_name }}</div>
        <label v-for="(t, i) in g.tasks" :key="i" class="ttp-task" data-suggestion>
          <input type="checkbox" :checked="isChecked(g, i)" @change="toggle(g, i)" />
          <span class="ttp-task-name">{{ t.name }}</span>
          <span class="ttp-badge">{{ t.billing_mode === 'HORAIRE' ? 'Horaire' : 'Forfait' }}</span>
        </label>
      </div>
    </div>
  </div>
</template>

<style scoped>
.ttp { border: 1px solid #DBEAFE; background: #F8FAFF; border-radius: 8px; padding: 14px 16px; margin-bottom: 14px; }
.ttp-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 16px; margin-bottom: 10px; }
.ttp-title { font-size: 14px; font-weight: 700; color: #1E3A8A; margin: 0; }
.ttp-sub { font-size: 12px; color: #6B7280; margin: 2px 0 0; max-width: 60ch; }
.ttp-create { flex-shrink: 0; background: #2563EB; color: white; border: none; border-radius: 6px; padding: 8px 14px; font-size: 12px; font-weight: 600; cursor: pointer; white-space: nowrap; }
.ttp-create:disabled { opacity: 0.5; cursor: not-allowed; }
.ttp-error { color: #DC2626; font-size: 12px; margin: 0 0 8px; }
.ttp-groups { display: grid; grid-template-columns: repeat(auto-fill, minmax(230px, 1fr)); gap: 12px; }
.ttp-group { background: white; border: 1px solid #E5E7EB; border-radius: 6px; padding: 8px 10px; }
.ttp-phase { font-size: 11px; font-weight: 700; color: #6B7280; text-transform: uppercase; letter-spacing: 0.3px; margin-bottom: 6px; }
.ttp-task { display: flex; align-items: center; gap: 7px; padding: 3px 0; font-size: 12px; color: #374151; cursor: pointer; }
.ttp-task input { cursor: pointer; }
.ttp-task-name { flex: 1; }
.ttp-badge { font-size: 9px; font-weight: 600; color: #6B7280; background: #F3F4F6; border-radius: 4px; padding: 1px 5px; }
</style>
