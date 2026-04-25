import { setActivePinia, createPinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'

vi.mock('../features/timesheet/api/timesheetApi', () => ({
  timesheetApi: {
    listEntries: vi.fn(),
    mandatoryTasks: vi.fn(),
    listLocks: vi.fn().mockResolvedValue({ data: [] }),
  },
}))
vi.mock('@/plugins/axios', () => ({
  default: { get: vi.fn().mockResolvedValue({ data: {} }), post: vi.fn(), patch: vi.fn(), delete: vi.fn() },
}))

import { timesheetApi } from '../features/timesheet/api/timesheetApi'
import { useTimesheetStore } from '../features/timesheet/stores/useTimesheetStore'

const mockList = timesheetApi.listEntries as unknown as ReturnType<typeof vi.fn>
const mockMandatory = timesheetApi.mandatoryTasks as unknown as ReturnType<typeof vi.fn>

describe('useTimesheetStore — tâches obligatoires (always_display_in_timesheet)', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    mockList.mockReset()
    mockMandatory.mockReset()
    mockList.mockResolvedValue({ data: [] })
    mockMandatory.mockResolvedValue({ data: [] })
  })

  it('injecte une ligne pour chaque tâche obligatoire même sans entrée', async () => {
    mockList.mockResolvedValue({ data: [] })
    mockMandatory.mockResolvedValue({
      data: [
        {
          id: 100, project: 1, project_code: 'INT-01', project_name: 'Interne',
          phase: 5, wbs_code: 'C.1', name: 'Congés', display_label: 'Congés',
          phase_name: 'Catalogue', is_billable: false, always_display_in_timesheet: true,
        },
      ],
    })
    const store = useTimesheetStore()
    await store.fetchWeek()
    const rows = store.gridRows
    expect(rows.length).toBe(1)
    expect(rows[0]!.task_name).toBe('Congés')
    expect(rows[0]!.is_mandatory).toBe(true)
    expect(rows[0]!.row_total).toBe(0)
  })

  it('marque la ligne obligatoire is_mandatory=true même si elle a déjà des entrées', async () => {
    mockList.mockResolvedValue({
      data: [{
        id: 1, employee: 1, project: 1, project_code: 'INT-01', project_name: 'Interne',
        phase: 5, phase_name: 'Catalogue', task: 100, task_wbs_code: 'C.1', task_name: 'Congés',
        date: '2026-04-20', hours: '8', notes: '', rejection_reason: '', status: 'DRAFT',
        is_favorite: false, is_invoiced: false, invoiced_on: null, category: 'NON_BILLABLE',
      }],
    })
    mockMandatory.mockResolvedValue({
      data: [{
        id: 100, project: 1, project_code: 'INT-01', project_name: 'Interne',
        phase: 5, wbs_code: 'C.1', name: 'Congés', display_label: 'Congés',
        phase_name: 'Catalogue', is_billable: false, always_display_in_timesheet: true,
      }],
    })
    const store = useTimesheetStore()
    await store.fetchWeek()
    const rows = store.gridRows
    expect(rows.length).toBe(1)
    expect(rows[0]!.is_mandatory).toBe(true)
  })

  it('ne duplique pas une tâche déjà présente dans les entrées', async () => {
    mockList.mockResolvedValue({
      data: [
        {
          id: 1, employee: 1, project: 1, project_code: 'INT-01', project_name: 'Interne',
          phase: 5, phase_name: 'Catalogue', task: 100, task_wbs_code: 'C.1', task_name: 'Congés',
          date: '2026-04-20', hours: '8', notes: '', rejection_reason: '', status: 'DRAFT',
          is_favorite: false, is_invoiced: false, invoiced_on: null, category: 'NON_BILLABLE',
        },
      ],
    })
    mockMandatory.mockResolvedValue({
      data: [
        {
          id: 100, project: 1, project_code: 'INT-01', project_name: 'Interne',
          phase: 5, wbs_code: 'C.1', name: 'Congés', display_label: 'Congés',
          phase_name: 'Catalogue', is_billable: false, always_display_in_timesheet: true,
        },
      ],
    })
    const store = useTimesheetStore()
    await store.fetchWeek()
    expect(store.gridRows.length).toBe(1)
  })
})

// Pour copyMondayToWeek on mocke createEntry (utilisé par saveCell pour les
// nouvelles cellules). Cela vérifie le comportement end-to-end côté store.
vi.mocked(timesheetApi).createEntry = vi.fn().mockResolvedValue({ data: { id: 999 } })
vi.mocked(timesheetApi).updateEntry = vi.fn().mockResolvedValue({ data: {} })

describe('useTimesheetStore — copyMondayToWeek', () => {
  const mockCreate = timesheetApi.createEntry as unknown as ReturnType<typeof vi.fn>
  beforeEach(() => {
    setActivePinia(createPinia())
    mockCreate.mockReset()
    mockCreate.mockResolvedValue({ data: { id: 999 } })
  })

  it('crée une entry pour mardi-vendredi avec la valeur du lundi (4 appels)', async () => {
    const store = useTimesheetStore()
    store.currentWeekStart = '2026-04-20'
    await store.copyMondayToWeek(1, null, '8', 100)
    expect(mockCreate).toHaveBeenCalledTimes(4)
    const dates = mockCreate.mock.calls.map(c => (c[0] as { date: string }).date)
    expect(dates).toEqual(['2026-04-21', '2026-04-22', '2026-04-23', '2026-04-24'])
    mockCreate.mock.calls.forEach(c => {
      expect((c[0] as { hours: string }).hours).toBe('8')
    })
  })

  it('ne copie pas si la valeur du lundi est 0 ou vide', async () => {
    const store = useTimesheetStore()
    store.currentWeekStart = '2026-04-20'
    await store.copyMondayToWeek(1, null, '0', 100)
    await store.copyMondayToWeek(1, null, '', 100)
    expect(mockCreate).not.toHaveBeenCalled()
  })
})
