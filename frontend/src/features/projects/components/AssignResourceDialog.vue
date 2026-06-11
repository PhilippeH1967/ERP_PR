<script setup lang="ts">
/**
 * AssignResourceDialog — dialogue unifié d'affectation (mockup 03 de l'audit UX).
 * Trois questions : Qui ? (employé / équipe / profil virtuel) · Où ? (projet
 * entier / phase / tâche feuille) · Combien ? (h-sem, période).
 *
 * Remplace les canaux parallèles : ajout de membre, dropdown « + Équipe » par
 * phase, pickers d'allocation. Routage selon la combinaison :
 * - employé + projet  → POST projects/{id}/members/
 * - employé/virtuel + phase|tâche → POST allocations/
 * - équipe + projet|phase|tâche   → POST assign_team[_to_phase|_to_task]/
 */
import { computed, ref, watch } from 'vue'
import apiClient from '@/plugins/axios'

type WhoType = 'emp' | 'team' | 'virt'
type ScopeType = 'project' | 'phase' | 'task'

const props = defineProps<{
  open: boolean
  projectId: number
  initialScope?: { type: ScopeType; id?: number | null }
}>()
const emit = defineEmits<{ close: []; assigned: [] }>()

interface UserL { id: number; username: string; email: string; first_name?: string; last_name?: string }
interface TaskL { id: number; phase: number | null; parent: number | null; wbs_code: string; name: string; budgeted_hours: string | number; is_active: boolean }

const users = ref<UserL[]>([])
const virtuals = ref<Array<{ id: number; name: string }>>([])
const teams = ref<Array<{ id: number; name: string }>>([])
const phases = ref<Array<{ id: number; name: string }>>([])
const tasks = ref<TaskL[]>([])

const whoType = ref<WhoType>('emp')
const whoId = ref<number | null>(null)
const search = ref('')
const scopeType = ref<ScopeType | null>(null)
const scopeId = ref<number | null>(null)
const hpw = ref(20)
const start = ref(new Date().toISOString().slice(0, 10))
const end = ref(new Date(Date.now() + 90 * 86400000).toISOString().slice(0, 10))
const saving = ref(false)
const error = ref('')

function arr(d: unknown): unknown[] {
  const x = (d as { data?: unknown })?.data ?? d
  return Array.isArray(x) ? x : (x as { results?: unknown[] })?.results || []
}

async function load() {
  error.value = ''
  whoId.value = null
  search.value = ''
  if (props.initialScope) {
    scopeType.value = props.initialScope.type
    scopeId.value = props.initialScope.id ?? null
  } else { scopeType.value = null; scopeId.value = null }
  try {
    const [ur, vr, tr, pr, tk] = await Promise.all([
      apiClient.get('users/search/'),
      apiClient.get('virtual-resources/', { params: { project: props.projectId, is_active: true } }),
      apiClient.get('teams/'),
      apiClient.get(`projects/${props.projectId}/phases/`, { params: { page_size: '200' } }),
      apiClient.get(`projects/${props.projectId}/tasks/`, { params: { page_size: '500' } }),
    ])
    users.value = arr(ur.data) as UserL[]
    virtuals.value = arr(vr.data) as Array<{ id: number; name: string }>
    teams.value = arr(tr.data) as Array<{ id: number; name: string }>
    phases.value = arr(pr.data) as Array<{ id: number; name: string }>
    tasks.value = arr(tk.data) as TaskL[]
  } catch { error.value = 'Chargement impossible.' }
}
watch(() => props.open, (o) => { if (o) load() }, { immediate: true })

function userLabel(u: UserL) { return `${u.first_name || ''} ${u.last_name || ''}`.trim() || u.username }
const isLeaf = (t: TaskL) => !tasks.value.some(x => x.parent === t.id)

const whoOptions = computed(() => {
  const q = search.value.trim().toLowerCase()
  if (whoType.value === 'emp') return users.value.filter(u => !q || userLabel(u).toLowerCase().includes(q) || u.username.toLowerCase().includes(q)).map(u => ({ id: u.id, label: userLabel(u), sub: u.email }))
  if (whoType.value === 'team') return teams.value.filter(t => !q || t.name.toLowerCase().includes(q)).map(t => ({ id: t.id, label: t.name, sub: 'tous les membres' }))
  return virtuals.value.filter(v => !q || v.name.toLowerCase().includes(q)).map(v => ({ id: v.id, label: v.name, sub: 'profil virtuel' }))
})

// Portée « Projet entier » indisponible pour un profil virtuel (une allocation
// cible une phase OU une tâche).
const projectScopeAvailable = computed(() => whoType.value !== 'virt')

interface ScopeRow { type: ScopeType; id: number; label: string; indent: number; wbs?: string }
const scopeRows = computed<ScopeRow[]>(() => {
  const rows: ScopeRow[] = []
  for (const p of phases.value) {
    rows.push({ type: 'phase', id: p.id, label: `Phase ${p.name}`, indent: 0 })
    for (const t of tasks.value.filter(t => t.phase === p.id && !t.parent)) {
      if (isLeaf(t)) rows.push({ type: 'task', id: t.id, label: t.name, indent: 1, wbs: t.wbs_code })
      else for (const s of tasks.value.filter(x => x.parent === t.id)) {
        rows.push({ type: 'task', id: s.id, label: s.name, indent: 2, wbs: s.wbs_code })
      }
    }
  }
  return rows
})

function setWho(t: WhoType) {
  whoType.value = t
  whoId.value = null
  if (t === 'virt' && scopeType.value === 'project') { scopeType.value = null; scopeId.value = null }
}
function pickScope(r: ScopeRow) { scopeType.value = r.type; scopeId.value = r.id }

const whoLabel = computed(() => whoOptions.value.find(o => o.id === whoId.value)?.label
  || (whoType.value === 'emp' ? users.value.filter(u => u.id === whoId.value).map(userLabel)[0] : undefined))
const scopeLabel = computed(() => {
  if (scopeType.value === 'project') return 'Projet entier'
  if (scopeType.value === 'phase') return 'Phase ' + (phases.value.find(p => p.id === scopeId.value)?.name || '')
  if (scopeType.value === 'task') { const t = tasks.value.find(t => t.id === scopeId.value); return t ? `${t.wbs_code} ${t.name}` : '' }
  return ''
})
const weeks = computed(() => Math.max(1, Math.round((new Date(end.value).getTime() - new Date(start.value).getTime()) / (7 * 86400000))))
const plannedTotal = computed(() => hpw.value * weeks.value)
const overBudget = computed(() => {
  if (scopeType.value !== 'task') return false
  const t = tasks.value.find(t => t.id === scopeId.value)
  const b = Number(t?.budgeted_hours || 0)
  return b > 0 && plannedTotal.value > b
})
const canSubmit = computed(() => whoId.value != null && scopeType.value != null && (scopeType.value === 'project' || scopeId.value != null))

async function submit() {
  if (!canSubmit.value || saving.value) return
  saving.value = true
  error.value = ''
  const base = { hours_per_week: hpw.value, start_date: start.value, end_date: end.value }
  try {
    if (whoType.value === 'team') {
      if (scopeType.value === 'project') await apiClient.post(`projects/${props.projectId}/assign_team/`, { team_id: whoId.value })
      else if (scopeType.value === 'phase') await apiClient.post(`projects/${props.projectId}/assign_team_to_phase/`, { team_id: whoId.value, phase_id: scopeId.value, ...base })
      else await apiClient.post(`projects/${props.projectId}/assign_team_to_task/`, { team_id: whoId.value, task_id: scopeId.value, ...base })
    } else if (scopeType.value === 'project') {
      await apiClient.post(`projects/${props.projectId}/members/`, { user_id: whoId.value })
    } else {
      const who = whoType.value === 'emp' ? { employee: whoId.value } : { virtual_resource: whoId.value }
      const where = scopeType.value === 'phase' ? { phase: scopeId.value } : { task: scopeId.value }
      await apiClient.post('allocations/', { ...who, ...where, project: props.projectId, ...base, distribution_mode: 'uniform', time_unit: 'week' })
    }
    emit('assigned')
    emit('close')
  } catch (e: unknown) {
    const d = (e as { response?: { data?: Record<string, unknown> } }).response?.data
    const first = d ? Object.values(d)[0] : null
    error.value = Array.isArray(first) ? String(first[0]) : (typeof first === 'string' ? first : 'Affectation impossible.')
  } finally { saving.value = false }
}
</script>

<template>
  <Teleport to="body">
    <div v-if="open" class="ard-overlay" @click.self="emit('close')">
      <div class="ard-modal">
        <div class="ard-head">
          <h2>Affecter une ressource</h2>
          <button class="ard-x" @click="emit('close')">&times;</button>
        </div>
        <div v-if="error" class="ard-error">{{ error }}</div>

        <div class="ard-sect">
          <h4>1 · Qui ?</h4>
          <div class="ard-who">
            <button class="ard-whob" :class="{ active: whoType === 'emp' }" data-ard-who-emp @click="setWho('emp')">👤 Employé</button>
            <button class="ard-whob" :class="{ active: whoType === 'team' }" data-ard-who-team @click="setWho('team')">👥 Équipe</button>
            <button class="ard-whob" :class="{ active: whoType === 'virt' }" data-ard-who-virt @click="setWho('virt')">◇ Profil virtuel</button>
          </div>
          <input v-model="search" class="ard-search" type="text" placeholder="Rechercher…" data-ard-search />
          <div class="ard-list">
            <div v-for="o in whoOptions" :key="o.id" class="ard-opt" :class="{ sel: whoId === o.id }" data-ard-opt @click="whoId = o.id">
              {{ o.label }} <span class="ard-sub">{{ o.sub }}</span>
            </div>
            <div v-if="!whoOptions.length" class="ard-empty">Aucun résultat</div>
          </div>
        </div>

        <div class="ard-sect">
          <h4>2 · Où ?</h4>
          <div class="ard-scope">
            <div v-if="projectScopeAvailable" class="ard-srow" :class="{ sel: scopeType === 'project' }" data-ard-scope-project @click="scopeType = 'project'; scopeId = null">
              <input type="radio" :checked="scopeType === 'project'" /> <b>Projet entier</b>
              <span class="ard-sub">{{ whoType === 'team' ? 'ajoute tous les membres au projet' : 'membre sans planification précise' }}</span>
            </div>
            <div v-for="r in scopeRows" :key="r.type + r.id" class="ard-srow" :class="[{ sel: scopeType === r.type && scopeId === r.id }, 'i' + r.indent]" data-ard-scope @click="pickScope(r)">
              <input type="radio" :checked="scopeType === r.type && scopeId === r.id" />
              <span v-if="r.wbs" class="ard-wbs">{{ r.wbs }}</span>{{ r.label }}
            </div>
          </div>
        </div>

        <div class="ard-sect">
          <h4>3 · Combien ?</h4>
          <div class="ard-row">
            <div class="ard-fg"><label>Heures / semaine</label><input v-model.number="hpw" type="number" min="0.5" step="0.5" data-ard-hpw /></div>
            <div class="ard-fg"><label>Du</label><input v-model="start" type="date" data-ard-start /></div>
            <div class="ard-fg"><label>Au</label><input v-model="end" type="date" data-ard-end /></div>
          </div>
          <div v-if="whoLabel && scopeLabel" class="ard-recap" data-ard-recap>
            ✅ <b>{{ whoLabel }}</b> → <b>{{ scopeLabel }}</b>
            <template v-if="scopeType !== 'project'"> à <b>{{ hpw }} h/sem</b> du {{ start }} au {{ end }} (≈ {{ plannedTotal }} h)</template>
            <div v-if="overBudget" class="ard-warn">⚠ Budget de la tâche dépassé — dépassement signalé, non bloquant.</div>
          </div>
          <p v-else class="ard-hint">Choisissez une ressource et une portée pour voir le récapitulatif.</p>
        </div>

        <div class="ard-foot">
          <button class="ard-btn" @click="emit('close')">Annuler</button>
          <button class="ard-btn primary" :disabled="!canSubmit || saving" data-ard-submit @click="submit">{{ saving ? '…' : 'Affecter' }}</button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.ard-overlay { position: fixed; inset: 0; background: rgba(0,0,0,.32); z-index: 9000; display: flex; align-items: flex-start; justify-content: center; padding-top: 48px; }
.ard-modal { width: 620px; max-width: 94vw; max-height: 86vh; overflow-y: auto; background: #fff; border-radius: 14px; box-shadow: 0 16px 40px rgba(0,0,0,.22); }
.ard-head { padding: 14px 20px; border-bottom: 1px solid var(--color-gray-200); display: flex; align-items: center; }
.ard-head h2 { font-size: 15px; font-weight: 700; margin: 0; flex: 1; color: var(--color-gray-800); }
.ard-x { background: none; border: none; font-size: 22px; color: var(--color-gray-400); cursor: pointer; }
.ard-error { margin: 12px 20px 0; background: #fde8e4; color: var(--color-danger); padding: 8px 12px; border-radius: 6px; font-size: 12px; }
.ard-sect { padding: 13px 20px; border-bottom: 1px solid var(--color-gray-100); }
.ard-sect h4 { margin: 0 0 9px; font-size: 10px; font-weight: 800; text-transform: uppercase; letter-spacing: .04em; color: var(--color-gray-500); }
.ard-who { display: flex; gap: 8px; margin-bottom: 9px; }
.ard-whob { flex: 1; border: 1px solid var(--color-gray-200); border-radius: 9px; padding: 8px; font-size: 12px; font-weight: 700; color: var(--color-gray-500); background: #fff; cursor: pointer; }
.ard-whob.active { border-color: var(--color-primary); color: var(--color-primary); background: #EFF6FF; }
.ard-search { width: 100%; padding: 7px 11px; border: 1px solid var(--color-gray-300); border-radius: 7px; font-size: 12px; margin-bottom: 6px; box-sizing: border-box; }
.ard-list { max-height: 150px; overflow-y: auto; }
.ard-opt { display: flex; align-items: center; gap: 9px; padding: 6px 10px; border-radius: 7px; cursor: pointer; font-size: 12px; }
.ard-opt:hover { background: var(--color-gray-50); }
.ard-opt.sel { background: #EFF6FF; outline: 1px solid #BFDBFE; }
.ard-sub { font-size: 10px; color: var(--color-gray-400); margin-left: auto; }
.ard-empty { padding: 8px; font-size: 12px; color: var(--color-gray-400); }
.ard-scope { border: 1px solid var(--color-gray-200); border-radius: 9px; overflow: hidden; max-height: 200px; overflow-y: auto; }
.ard-srow { display: flex; align-items: center; gap: 9px; padding: 7px 12px; border-bottom: 1px solid var(--color-gray-100); font-size: 12px; cursor: pointer; }
.ard-srow:last-child { border-bottom: none; }
.ard-srow:hover { background: var(--color-gray-50); }
.ard-srow.sel { background: #EFF6FF; }
.ard-srow.i1 { padding-left: 32px; }
.ard-srow.i2 { padding-left: 52px; color: var(--color-gray-500); }
.ard-wbs { font-family: var(--font-mono, monospace); font-size: 10px; color: var(--color-gray-400); }
.ard-row { display: flex; gap: 10px; }
.ard-fg { flex: 1; }
.ard-fg label { display: block; font-size: 10px; font-weight: 700; color: var(--color-gray-500); margin-bottom: 3px; }
.ard-fg input { width: 100%; padding: 6px 9px; border: 1px solid var(--color-gray-300); border-radius: 6px; font-size: 12px; box-sizing: border-box; }
.ard-recap { margin-top: 12px; background: var(--color-gray-50); border: 1px solid var(--color-gray-200); border-radius: 9px; padding: 10px 13px; font-size: 12px; color: var(--color-gray-700); }
.ard-warn { color: #B45309; margin-top: 4px; }
.ard-hint { font-size: 11px; color: var(--color-gray-400); margin: 10px 0 0; }
.ard-foot { padding: 13px 20px; background: var(--color-gray-50); display: flex; justify-content: flex-end; gap: 8px; }
.ard-btn { border: 1px solid var(--color-gray-200); background: #fff; border-radius: 7px; padding: 8px 14px; font-size: 12px; font-weight: 700; color: var(--color-gray-700); cursor: pointer; }
.ard-btn.primary { background: var(--color-primary); color: #fff; border-color: var(--color-primary); }
.ard-btn.primary:disabled { opacity: .4; cursor: not-allowed; }
</style>
