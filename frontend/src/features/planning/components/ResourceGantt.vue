<script setup lang="ts">
/**
 * ResourceGantt — Global resource planning Gantt.
 * Rows = employees, Columns = weeks, Cells = allocation bars by project.
 * Filterable by BU, supervisor, project.
 */
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { planningApi } from '../api/planningApi'

const router = useRouter()

interface Allocation {
  project_code: string; project_name: string; phase_name: string
  hours_per_week: number; start_date: string; end_date: string
}

interface Employee {
  employee_id: number; employee_name: string; contract_hours: number
  total_planned_hours_week: number; allocations: Allocation[]
  load_status: string; load_percent: number
}

const employees = ref<Employee[]>([])
const isLoading = ref(true)

// Filters
const filterBU = ref('')
const filterSearch = ref('')

// Timeline: 12 weeks from today
const weeksToShow = ref(12)
const startOffset = ref(0) // weeks offset from current week

const weeks = computed(() => {
  const result: { start: string; end: string; label: string; isCurrent: boolean }[] = []
  const now = new Date()
  const monday = new Date(now)
  monday.setDate(now.getDate() - now.getDay() + 1 + startOffset.value * 7) // Monday of offset week
  for (let i = 0; i < weeksToShow.value; i++) {
    const wStart = new Date(monday)
    wStart.setDate(monday.getDate() + i * 7)
    const wEnd = new Date(wStart)
    wEnd.setDate(wStart.getDate() + 4) // Friday
    const isCurrent = i === -startOffset.value
    const label = `${String(wStart.getDate()).padStart(2, '0')}/${String(wStart.getMonth() + 1).padStart(2, '0')}`
    result.push({
      start: wStart.toISOString().substring(0, 10),
      end: wEnd.toISOString().substring(0, 10),
      label,
      isCurrent: wStart <= now && wEnd >= now,
    })
  }
  return result
})

const periodStart = computed(() => weeks.value[0]?.start || '')
const periodEnd = computed(() => weeks.value[weeks.value.length - 1]?.end || '')

async function load() {
  isLoading.value = true
  try {
    const resp = await planningApi.globalPlanning({ start_date: periodStart.value, end_date: periodEnd.value })
    const data = resp.data?.data || resp.data
    employees.value = data?.employees || []
  } catch { employees.value = [] }
  finally { isLoading.value = false }
}

onMounted(load)

// Filtered employees
const filteredEmployees = computed(() => {
  let list = employees.value
  if (filterSearch.value) {
    const q = filterSearch.value.toLowerCase()
    list = list.filter(e => e.employee_name.toLowerCase().includes(q))
  }
  return list.sort((a, b) => a.employee_name.localeCompare(b.employee_name))
})

// Check if an allocation is active during a given week
function allocationsForWeek(emp: Employee, week: { start: string; end: string }): Allocation[] {
  return emp.allocations.filter(a => a.start_date <= week.end && a.end_date >= week.start)
}

function weekLoadPercent(emp: Employee, week: { start: string; end: string }): number {
  const allocs = allocationsForWeek(emp, week)
  const totalH = allocs.reduce((s, a) => s + a.hours_per_week, 0)
  return emp.contract_hours > 0 ? Math.round(totalH / emp.contract_hours * 100) : 0
}

function weekLoadColor(pct: number): string {
  if (pct === 0) return ''
  if (pct > 120) return '#FEE2E2' // red bg
  if (pct > 100) return '#FEF3C7' // amber bg
  if (pct >= 80) return '#DCFCE7' // green bg
  return '#DBEAFE' // blue bg (under)
}

function weekLoadTextColor(pct: number): string {
  if (pct > 120) return '#DC2626'
  if (pct > 100) return '#92400E'
  if (pct >= 80) return '#166534'
  if (pct > 0) return '#1D4ED8'
  return '#9CA3AF'
}

// Project colors (auto-assign)
const projectColors = computed(() => {
  const colors = ['#3B82F6', '#F59E0B', '#10B981', '#8B5CF6', '#EC4899', '#F97316', '#06B6D4', '#84CC16']
  const codes = new Set<string>()
  for (const e of employees.value) for (const a of e.allocations) codes.add(a.project_code)
  const map: Record<string, string> = {}
  let i = 0
  for (const code of codes) { map[code] = colors[i % colors.length]; i++ }
  return map
})

function prevPeriod() { startOffset.value -= 4; load() }
function nextPeriod() { startOffset.value += 4; load() }
function resetPeriod() { startOffset.value = 0; load() }
</script>

<template>
  <div class="rg-container">
    <!-- Header -->
    <div class="rg-header">
      <div>
        <h2 class="rg-title">Planification des ressources</h2>
        <p class="rg-subtitle">Vue globale — {{ weeks.length }} semaines a partir du {{ periodStart }}</p>
      </div>
      <div class="rg-controls">
        <input v-model="filterSearch" type="text" placeholder="Filtrer par nom..." class="rg-search" />
        <div class="rg-nav">
          <button class="rg-nav-btn" @click="prevPeriod">&larr; 4 sem.</button>
          <button class="rg-nav-btn rg-nav-today" @click="resetPeriod">Aujourd'hui</button>
          <button class="rg-nav-btn" @click="nextPeriod">4 sem. &rarr;</button>
        </div>
      </div>
    </div>

    <!-- KPIs -->
    <div class="rg-kpis">
      <div class="rg-kpi">
        <span class="rg-kpi-value">{{ filteredEmployees.length }}</span>
        <span class="rg-kpi-label">Employes</span>
      </div>
      <div class="rg-kpi">
        <span class="rg-kpi-value" style="color:#DC2626;">{{ filteredEmployees.filter(e => e.load_status === 'critical' || e.load_status === 'overload').length }}</span>
        <span class="rg-kpi-label">En surcharge</span>
      </div>
      <div class="rg-kpi">
        <span class="rg-kpi-value" style="color:#1D4ED8;">{{ filteredEmployees.filter(e => e.load_status === 'underload').length }}</span>
        <span class="rg-kpi-label">Sous-charge</span>
      </div>
      <div class="rg-kpi">
        <span class="rg-kpi-value" style="color:#16A34A;">{{ filteredEmployees.filter(e => e.load_status === 'normal').length }}</span>
        <span class="rg-kpi-label">Normal</span>
      </div>
    </div>

    <!-- Legend -->
    <div class="rg-legend">
      <span v-for="(color, code) in projectColors" :key="code" class="rg-legend-item">
        <span class="rg-legend-dot" :style="{ background: color }"></span>
        {{ code }}
      </span>
      <span class="rg-legend-sep">|</span>
      <span class="rg-legend-item"><span class="rg-legend-dot" style="background:#DCFCE7; border:1px solid #16A34A;"></span> 80-100%</span>
      <span class="rg-legend-item"><span class="rg-legend-dot" style="background:#FEF3C7; border:1px solid #D97706;"></span> 100-120%</span>
      <span class="rg-legend-item"><span class="rg-legend-dot" style="background:#FEE2E2; border:1px solid #DC2626;"></span> &gt;120%</span>
    </div>

    <div v-if="isLoading" style="padding:40px; text-align:center; color:#9CA3AF;">Chargement...</div>
    <div v-else-if="!filteredEmployees.length" style="padding:40px; text-align:center; color:#9CA3AF;">Aucun employe avec allocation sur cette periode</div>

    <!-- Gantt grid -->
    <div v-else class="rg-grid-wrapper">
      <table class="rg-grid">
        <thead>
          <tr>
            <th class="rg-emp-header">Employe</th>
            <th class="rg-emp-header" style="width:50px;">Charge</th>
            <th
              v-for="week in weeks" :key="week.start"
              class="rg-week-header"
              :class="{ 'rg-current-week': week.isCurrent }"
            >
              {{ week.label }}
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="emp in filteredEmployees" :key="emp.employee_id">
            <td class="rg-emp-cell">
              <span class="rg-emp-name">{{ emp.employee_name }}</span>
              <span class="rg-emp-contract">{{ emp.contract_hours }}h/sem</span>
            </td>
            <td class="rg-load-cell">
              <span class="rg-load-badge" :style="{ color: weekLoadTextColor(emp.load_percent), background: weekLoadColor(emp.load_percent) }">
                {{ emp.load_percent }}%
              </span>
            </td>
            <td
              v-for="week in weeks" :key="week.start"
              class="rg-week-cell"
              :class="{ 'rg-current-week': week.isCurrent }"
              :style="{ background: weekLoadColor(weekLoadPercent(emp, week)) }"
              :title="allocationsForWeek(emp, week).map(a => a.project_code + ': ' + a.hours_per_week + 'h').join('\n') || 'Pas d\'allocation'"
            >
              <div v-if="allocationsForWeek(emp, week).length" class="rg-cell-bars">
                <div
                  v-for="(alloc, i) in allocationsForWeek(emp, week)" :key="i"
                  class="rg-cell-bar"
                  :style="{ background: projectColors[alloc.project_code] || '#9CA3AF', height: Math.min(100, (alloc.hours_per_week / emp.contract_hours) * 100) + '%' }"
                  :title="alloc.project_code + ' — ' + alloc.project_name + ': ' + alloc.hours_per_week + 'h/sem'"
                ></div>
              </div>
              <span v-if="weekLoadPercent(emp, week) > 0" class="rg-cell-pct" :style="{ color: weekLoadTextColor(weekLoadPercent(emp, week)) }">
                {{ weekLoadPercent(emp, week) }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.rg-container { background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); overflow: hidden; }
.rg-header { display: flex; align-items: center; justify-content: space-between; padding: 16px; border-bottom: 1px solid #E5E7EB; flex-wrap: wrap; gap: 12px; }
.rg-title { font-size: 18px; font-weight: 700; color: #111827; margin: 0; }
.rg-subtitle { font-size: 12px; color: #6B7280; margin-top: 2px; }
.rg-controls { display: flex; align-items: center; gap: 12px; }
.rg-search { padding: 6px 12px; border: 1px solid #D1D5DB; border-radius: 6px; font-size: 12px; width: 180px; }
.rg-nav { display: flex; gap: 4px; }
.rg-nav-btn { padding: 5px 12px; border: 1px solid #D1D5DB; border-radius: 4px; font-size: 11px; font-weight: 600; background: white; cursor: pointer; color: #4B5563; }
.rg-nav-btn:hover { background: #F3F4F6; }
.rg-nav-today { background: #2563EB; color: white; border-color: #2563EB; }
.rg-nav-today:hover { background: #1D4ED8; }

.rg-kpis { display: flex; gap: 16px; padding: 12px 16px; border-bottom: 1px solid #E5E7EB; }
.rg-kpi { display: flex; align-items: baseline; gap: 6px; }
.rg-kpi-value { font-size: 20px; font-weight: 700; font-family: var(--font-mono, monospace); }
.rg-kpi-label { font-size: 11px; color: #6B7280; }

.rg-legend { display: flex; align-items: center; gap: 12px; padding: 8px 16px; border-bottom: 1px solid #E5E7EB; flex-wrap: wrap; }
.rg-legend-item { display: flex; align-items: center; gap: 4px; font-size: 10px; color: #6B7280; }
.rg-legend-dot { width: 12px; height: 8px; border-radius: 2px; flex-shrink: 0; }
.rg-legend-sep { color: #D1D5DB; }

.rg-grid-wrapper { overflow-x: auto; }
.rg-grid { width: 100%; border-collapse: collapse; font-size: 11px; }
.rg-grid th, .rg-grid td { border: 1px solid #E5E7EB; }
.rg-emp-header { position: sticky; left: 0; background: #F9FAFB; z-index: 2; padding: 6px 10px; font-size: 10px; font-weight: 600; color: #6B7280; text-transform: uppercase; text-align: left; white-space: nowrap; }
.rg-week-header { padding: 6px 4px; text-align: center; font-size: 9px; font-weight: 600; color: #6B7280; min-width: 50px; background: #F9FAFB; }
.rg-current-week { background: #EFF6FF !important; border-bottom-color: #3B82F6; }

.rg-emp-cell { position: sticky; left: 0; background: white; z-index: 1; padding: 6px 10px; white-space: nowrap; }
.rg-emp-name { font-weight: 600; font-size: 12px; color: #111827; }
.rg-emp-contract { display: block; font-size: 9px; color: #9CA3AF; }
.rg-load-cell { text-align: center; padding: 4px; }
.rg-load-badge { padding: 2px 6px; border-radius: 8px; font-size: 10px; font-weight: 700; }

.rg-week-cell { padding: 2px; vertical-align: bottom; height: 36px; position: relative; text-align: center; }
.rg-cell-bars { display: flex; gap: 1px; align-items: flex-end; height: 100%; justify-content: center; }
.rg-cell-bar { width: 8px; min-height: 3px; border-radius: 2px 2px 0 0; }
.rg-cell-pct { position: absolute; bottom: 1px; left: 50%; transform: translateX(-50%); font-size: 8px; font-weight: 600; opacity: 0.7; }
</style>
