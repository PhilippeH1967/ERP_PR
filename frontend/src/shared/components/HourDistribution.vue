<script setup lang="ts">
import { computed, ref } from 'vue'

interface Member { id: number; name: string }
interface Virtual { id: number; name: string; default_hourly_rate: string }
interface Allocation { kind: 'employee' | 'virtual'; id: number; hours: number }

const props = defineProps<{
  members: Member[]
  virtuals: Virtual[]
  modelValue: Allocation[]
  budgetedHours?: number
  disabled?: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [Allocation[]]
  'create-virtual': [{ name: string; rate: string }]
}>()

const showVrForm = ref(false)
const vrName = ref('')
const vrRate = ref('0')

const sumHours = computed(() =>
  props.modelValue.reduce((s, a) => s + Number(a.hours || 0), 0),
)

const hasOverrun = computed(() =>
  typeof props.budgetedHours === 'number'
    && props.budgetedHours > 0
    && sumHours.value > props.budgetedHours,
)

function pickDefaultMember(): Allocation | null {
  const used = new Set(
    props.modelValue.filter(a => a.kind === 'employee').map(a => a.id),
  )
  const firstMember = props.members.find(m => !used.has(m.id))
  if (firstMember) return { kind: 'employee', id: firstMember.id, hours: 0 }
  const firstVirtual = props.virtuals.find(v => !used.has(v.id))
  if (firstVirtual) return { kind: 'virtual', id: firstVirtual.id, hours: 0 }
  return null
}

function addRow() {
  const row = pickDefaultMember()
  if (!row) return
  emit('update:modelValue', [...props.modelValue, row])
}

function removeRow(idx: number) {
  const next = props.modelValue.slice()
  next.splice(idx, 1)
  emit('update:modelValue', next)
}

function updateSelection(idx: number, value: string) {
  const [kind, rawId] = value.split(':')
  const id = Number(rawId)
  if (!kind || !id) return
  const next = props.modelValue.slice()
  next[idx] = { ...next[idx]!, kind: kind as 'employee' | 'virtual', id }
  emit('update:modelValue', next)
}

function updateHours(idx: number, value: string) {
  const next = props.modelValue.slice()
  next[idx] = { ...next[idx]!, hours: Number(value || 0) }
  emit('update:modelValue', next)
}

function submitVirtual() {
  const name = vrName.value.trim()
  if (!name) return
  emit('create-virtual', { name, rate: String(vrRate.value ?? '0') })
  vrName.value = ''
  vrRate.value = '0'
  showVrForm.value = false
}
</script>

<template>
  <div class="hd-wrapper">
    <div class="hd-header">
      <span class="hd-title">Répartition par personne</span>
      <span v-if="budgetedHours" class="hd-sum" :class="{ 'hd-sum-warn': hasOverrun }">
        {{ sumHours }}h / {{ budgetedHours }}h
      </span>
      <span v-else class="hd-sum">{{ sumHours }}h</span>
    </div>

    <div v-if="!modelValue.length" class="hd-empty">
      Aucune personne affectée. Cliquez sur « + Ajouter » pour répartir les heures.
    </div>

    <div
      v-for="(alloc, idx) in modelValue"
      :key="`${alloc.kind}-${alloc.id}-${idx}`"
      data-alloc-row
      class="hd-row"
    >
      <select
        class="hd-select"
        :value="`${alloc.kind}:${alloc.id}`"
        :disabled="disabled"
        @change="updateSelection(idx, ($event.target as HTMLSelectElement).value)"
      >
        <optgroup v-if="members.length" label="Employés">
          <option v-for="m in members" :key="`e-${m.id}`" :value="`employee:${m.id}`">
            {{ m.name }}
          </option>
        </optgroup>
        <optgroup v-if="virtuals.length" label="Profils virtuels">
          <option v-for="v in virtuals" :key="`v-${v.id}`" :value="`virtual:${v.id}`">
            {{ v.name }}
          </option>
        </optgroup>
      </select>
      <input
        data-alloc-hours
        class="hd-hours"
        type="number"
        min="0"
        step="0.5"
        :value="alloc.hours"
        :disabled="disabled"
        @input="updateHours(idx, ($event.target as HTMLInputElement).value)"
      />
      <span class="hd-unit">h</span>
      <button
        data-alloc-remove
        type="button"
        class="hd-btn-remove"
        :disabled="disabled"
        title="Retirer cette personne"
        @click="removeRow(idx)"
      >
        ✕
      </button>
    </div>

    <div v-if="hasOverrun" data-alloc-warning class="hd-warning">
      Total ({{ sumHours }}h) dépasse le budget ({{ budgetedHours }}h)
    </div>

    <div class="hd-actions">
      <button
        data-alloc-add
        type="button"
        class="hd-btn-add"
        :disabled="disabled"
        @click="addRow"
      >
        + Ajouter
      </button>
      <button
        data-alloc-show-vr-form
        type="button"
        class="hd-btn-link"
        :disabled="disabled"
        @click="showVrForm = !showVrForm"
      >
        {{ showVrForm ? '× Annuler' : '+ Nouveau profil virtuel' }}
      </button>
    </div>

    <div v-if="showVrForm" class="hd-vr-form">
      <input
        v-model="vrName"
        data-vr-name
        class="hd-input"
        placeholder="Libellé (ex. Architecte senior)"
      />
      <input
        v-model="vrRate"
        data-vr-rate
        type="number"
        min="0"
        step="0.01"
        class="hd-input hd-input-sm"
        placeholder="Taux $/h"
      />
      <button
        data-vr-submit
        type="button"
        class="hd-btn-primary"
        :disabled="!vrName.trim()"
        @click="submitVirtual"
      >
        Créer
      </button>
    </div>
  </div>
</template>

<style scoped>
.hd-wrapper { display: flex; flex-direction: column; gap: 6px; padding: 8px; background: var(--color-gray-50); border-radius: 4px; border: 1px solid var(--color-gray-200); }
.hd-header { display: flex; align-items: center; justify-content: space-between; }
.hd-title { font-size: 10px; font-weight: 700; color: var(--color-gray-600); text-transform: uppercase; letter-spacing: 0.3px; }
.hd-sum { font-size: 11px; font-family: var(--font-mono); color: var(--color-gray-700); }
.hd-sum-warn { color: var(--color-danger); font-weight: 700; }
.hd-empty { font-size: 11px; color: var(--color-gray-400); font-style: italic; }
.hd-row { display: flex; align-items: center; gap: 6px; }
.hd-select { flex: 1; padding: 4px 6px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 12px; background: white; }
.hd-hours { width: 70px; padding: 4px 6px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 12px; }
.hd-unit { font-size: 11px; color: var(--color-gray-500); }
.hd-btn-remove { background: none; border: none; color: var(--color-gray-400); cursor: pointer; font-size: 12px; padding: 2px 6px; border-radius: 4px; }
.hd-btn-remove:hover:not(:disabled) { color: var(--color-danger); background: var(--color-danger-light); }
.hd-btn-remove:disabled { opacity: 0.4; cursor: not-allowed; }
.hd-warning { font-size: 11px; color: var(--color-danger); font-weight: 600; }
.hd-actions { display: flex; gap: 8px; }
.hd-btn-add, .hd-btn-link { background: none; border: 1px dashed var(--color-gray-300); color: var(--color-primary); font-size: 11px; font-weight: 600; cursor: pointer; padding: 4px 8px; border-radius: 4px; }
.hd-btn-add:hover:not(:disabled), .hd-btn-link:hover:not(:disabled) { background: var(--color-primary-light); border-color: var(--color-primary); }
.hd-btn-add:disabled, .hd-btn-link:disabled { opacity: 0.5; cursor: not-allowed; }
.hd-vr-form { display: flex; gap: 6px; padding: 6px; background: white; border: 1px solid var(--color-gray-200); border-radius: 4px; }
.hd-input { flex: 1; padding: 4px 6px; border: 1px solid var(--color-gray-300); border-radius: 4px; font-size: 12px; }
.hd-input-sm { width: 90px; flex: 0 0 auto; }
.hd-btn-primary { background: var(--color-primary); color: white; border: none; padding: 4px 10px; border-radius: 4px; font-size: 12px; font-weight: 600; cursor: pointer; }
.hd-btn-primary:disabled { opacity: 0.4; cursor: not-allowed; }
</style>
