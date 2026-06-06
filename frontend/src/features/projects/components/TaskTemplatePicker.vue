<script setup lang="ts">
/**
 * TaskTemplatePicker — ajout de tâches (et sous-tâches) standard depuis le
 * catalogue (paramétrage admin), groupées par phase.
 *
 * Deux usages :
 *  - sans `phaseId` : démarrage d'un projet VIDE (toutes les phases), affiché
 *    uniquement si le projet n'a aucune tâche.
 *  - avec `phaseId` : ajout ciblé sur UNE phase (vide ou non) — l'endpoint
 *    exclut déjà les tâches présentes (dédup).
 *
 * Création : réutilise l'endpoint tasks/ existant (wbs_code auto-backend). Une
 * tâche cochée est créée puis ses sous-tâches cochées (parent = tâche créée).
 */
import { ref, computed, onMounted } from 'vue'
import { projectApi } from '../api/projectApi'

const props = defineProps<{ projectId: number; phaseId?: number | null }>()
const emit = defineEmits<{ created: [] }>()

interface SuggSub { name: string; client_facing_label: string; billing_mode: string }
interface SuggTask { name: string; client_facing_label: string; billing_mode: string; subtasks: SuggSub[] }
interface SuggGroup { phase_id: number; phase_code: string; phase_name: string; tasks: SuggTask[] }

const groups = ref<SuggGroup[]>([])
const hasTasks = ref(true)
const loading = ref(true)
const creating = ref(false)
const error = ref('')
const checked = ref<Set<string>>(new Set())

function tKey(g: SuggGroup, ti: number): string { return `${g.phase_id}:${ti}` }
function sKey(g: SuggGroup, ti: number, si: number): string { return `${g.phase_id}:${ti}:${si}` }

async function load() {
  loading.value = true
  try {
    const params = props.phaseId != null ? { phase: String(props.phaseId) } : undefined
    const r = await projectApi.taskSuggestions(props.projectId, params)
    const d = r.data?.data || r.data
    hasTasks.value = !!d.has_tasks
    groups.value = d.groups || []
    // Tout coché par défaut (tâches + sous-tâches) : on retire l'inutile.
    const s = new Set<string>()
    groups.value.forEach((g) =>
      g.tasks.forEach((t, ti) => {
        s.add(tKey(g, ti))
        t.subtasks.forEach((_, si) => s.add(sKey(g, ti, si)))
      }),
    )
    checked.value = s
  } catch {
    groups.value = []
    hasTasks.value = true
  } finally {
    loading.value = false
  }
}
onMounted(load)

const isPhaseScoped = computed(() => props.phaseId != null)
const visible = computed(
  () => !loading.value && groups.value.length > 0 && (isPhaseScoped.value || !hasTasks.value),
)
const selectedTaskCount = computed(() => {
  let n = 0
  groups.value.forEach((g) => g.tasks.forEach((_, ti) => { if (checked.value.has(tKey(g, ti))) n++ }))
  return n
})

function isOn(key: string): boolean { return checked.value.has(key) }
function toggle(key: string) {
  const s = new Set(checked.value)
  if (s.has(key)) s.delete(key)
  else s.add(key)
  checked.value = s
}

async function createSelected() {
  error.value = ''
  creating.value = true
  try {
    for (const g of groups.value) {
      for (let ti = 0; ti < g.tasks.length; ti++) {
        if (!checked.value.has(tKey(g, ti))) continue
        const t = g.tasks[ti]!
        const r = await projectApi.createTask(props.projectId, {
          phase: g.phase_id, name: t.name, task_type: 'TASK', billing_mode: t.billing_mode,
        })
        const createdId = (r.data?.data?.id ?? r.data?.id) as number | undefined
        if (!createdId) continue
        for (let si = 0; si < t.subtasks.length; si++) {
          if (!checked.value.has(sKey(g, ti, si))) continue
          const s = t.subtasks[si]!
          await projectApi.createTask(props.projectId, {
            phase: g.phase_id, name: s.name, task_type: 'SUBTASK',
            parent: createdId, billing_mode: s.billing_mode,
          })
        }
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
        <h4 class="ttp-title">{{ isPhaseScoped ? 'Ajouter depuis le modèle' : 'Démarrer depuis un modèle' }}</h4>
        <p class="ttp-sub">
          Cochez les tâches standard à créer{{ isPhaseScoped ? ' pour cette phase' : ' par phase' }}
          (sous-tâches incluses ; déjà présentes exclues). Modifiables ensuite.
        </p>
      </div>
      <button
        class="ttp-create"
        :disabled="creating || selectedTaskCount === 0"
        data-create-tasks
        @click="createSelected"
      >
        {{ creating ? 'Création…' : `Créer la sélection (${selectedTaskCount})` }}
      </button>
    </div>
    <p v-if="error" class="ttp-error" data-error>{{ error }}</p>
    <div class="ttp-groups">
      <div v-for="g in groups" :key="g.phase_id" class="ttp-group">
        <div class="ttp-phase">{{ g.phase_code }} · {{ g.phase_name }}</div>
        <div v-for="(t, ti) in g.tasks" :key="ti" class="ttp-task-block" data-suggestion>
          <label class="ttp-task">
            <input type="checkbox" :checked="isOn(tKey(g, ti))" @change="toggle(tKey(g, ti))" />
            <span class="ttp-task-name">{{ t.name }}</span>
            <span class="ttp-badge">{{ t.billing_mode === 'HORAIRE' ? 'Horaire' : 'Forfait' }}</span>
          </label>
          <label
            v-for="(s, si) in t.subtasks"
            :key="si"
            class="ttp-subtask"
            data-suggestion-sub
            :class="{ 'ttp-disabled': !isOn(tKey(g, ti)) }"
          >
            <input
              type="checkbox"
              :checked="isOn(sKey(g, ti, si))"
              :disabled="!isOn(tKey(g, ti))"
              @change="toggle(sKey(g, ti, si))"
            />
            <span class="ttp-task-name">{{ s.name }}</span>
          </label>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.ttp { border: 1px solid #DBEAFE; background: #F8FAFF; border-radius: 8px; padding: 14px 16px; margin-bottom: 14px; }
.ttp-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 16px; margin-bottom: 10px; }
.ttp-title { font-size: 14px; font-weight: 700; color: #1E3A8A; margin: 0; }
.ttp-sub { font-size: 12px; color: #6B7280; margin: 2px 0 0; max-width: 64ch; }
.ttp-create { flex-shrink: 0; background: #2563EB; color: white; border: none; border-radius: 6px; padding: 8px 14px; font-size: 12px; font-weight: 600; cursor: pointer; white-space: nowrap; }
.ttp-create:disabled { opacity: 0.5; cursor: not-allowed; }
.ttp-error { color: #DC2626; font-size: 12px; margin: 0 0 8px; }
.ttp-groups { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 12px; }
.ttp-group { background: white; border: 1px solid #E5E7EB; border-radius: 6px; padding: 8px 10px; }
.ttp-phase { font-size: 11px; font-weight: 700; color: #6B7280; text-transform: uppercase; letter-spacing: 0.3px; margin-bottom: 6px; }
.ttp-task-block { padding: 2px 0; }
.ttp-task { display: flex; align-items: center; gap: 7px; padding: 3px 0; font-size: 12px; color: #374151; cursor: pointer; }
.ttp-subtask { display: flex; align-items: center; gap: 7px; padding: 2px 0 2px 22px; font-size: 11px; color: #6B7280; cursor: pointer; }
.ttp-subtask.ttp-disabled { opacity: 0.45; cursor: not-allowed; }
.ttp-task input, .ttp-subtask input { cursor: pointer; }
.ttp-task-name { flex: 1; }
.ttp-badge { font-size: 9px; font-weight: 600; color: #6B7280; background: #F3F4F6; border-radius: 4px; padding: 1px 5px; }
</style>
