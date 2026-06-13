/**
 * Discipline de soumission & heures facturées — correctifs revue PR #73.
 *
 * - Dates calculées en heure LOCALE (pas de dérive UTC le soir, fuseau ouest)
 * - lateBlocked ne s'applique qu'à la semaine courante/future
 * - fetchWeek ne pré-remplit pas les fériés quand la saisie est bloquée
 * - saveCell expose le message d'erreur du backend (LATE_TIMESHEETS, ENTRY_INVOICED)
 * - goToWeek vide les entrées immédiatement (pas de lignes périmées)
 * - TimesheetCell affiche l'erreur backend et ne flashe pas « succès » sur échec
 */
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { beforeEach, describe, expect, it, vi } from 'vitest'

vi.mock('@/plugins/axios', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    patch: vi.fn(),
    delete: vi.fn(),
  },
}))

import apiClient from '@/plugins/axios'
import TimesheetCell from '@/features/timesheet/components/TimesheetCell.vue'
import {
  getDatesForWeek,
  getMondayOfWeek,
  useTimesheetStore,
} from '@/features/timesheet/stores/useTimesheetStore'
import type { TimeEntry } from '@/features/timesheet/types/timesheet.types'

const makeEntry = (overrides: Partial<TimeEntry> = {}): TimeEntry => ({
  id: 1,
  employee: 1,
  project: 10,
  project_code: 'PR-001',
  project_name: 'Test Project',
  phase: 20,
  phase_name: 'Concept',
  task: null,
  task_name: '',
  task_wbs_code: '',
  client_label: 'Phase 1',
  date: '2026-03-16',
  hours: '7.5',
  notes: '',
  rejection_reason: '',
  status: 'DRAFT',
  is_favorite: false,
  is_invoiced: false,
  version: 1,
  ...overrides,
})

describe('helpers de dates — heure locale', () => {
  it('getMondayOfWeek ne dérive pas en UTC le soir (fuseau ouest)', () => {
    // Lundi 8 juin 2026, 21h heure LOCALE : en UTC c'est déjà mardi pour un
    // fuseau à l'ouest (ex. Montréal UTC-4) — le lundi attendu reste le 8.
    const mondayEvening = new Date(2026, 5, 8, 21, 0, 0)
    expect(getMondayOfWeek(mondayEvening)).toBe('2026-06-08')
  })

  it('getMondayOfWeek rattache le dimanche au lundi précédent', () => {
    const sundayEvening = new Date(2026, 5, 14, 23, 0, 0)
    expect(getMondayOfWeek(sundayEvening)).toBe('2026-06-08')
  })

  it('getDatesForWeek produit les 7 dates locales de la semaine', () => {
    expect(getDatesForWeek('2026-06-08')).toEqual([
      '2026-06-08', '2026-06-09', '2026-06-10', '2026-06-11',
      '2026-06-12', '2026-06-13', '2026-06-14',
    ])
  })
})

describe('useTimesheetStore — discipline de soumission', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('lateBlocked actif sur la semaine courante, pas sur une semaine passée', () => {
    const store = useTimesheetStore()
    store.lateBlocking = true
    // currentWeekStart par défaut = semaine courante
    expect(store.lateBlocked).toBe(true)
    store.currentWeekStart = '2020-01-06'
    expect(store.lateBlocked).toBe(false)
  })

  it('fetchWeek ne pré-remplit pas les fériés quand la saisie est bloquée', async () => {
    vi.mocked(apiClient.get).mockImplementation((url: string) => {
      if (url === 'time_entries/unsubmitted_weeks/') {
        return Promise.resolve({ data: { weeks: ['2020-01-06'], blocking: true } })
      }
      if (url === 'time_entries/holidays/') {
        return Promise.resolve({
          data: [{ date: getMondayOfWeek(new Date()), name: 'Férié', is_paid: true, daily_hours: 8 }],
        })
      }
      if (url === 'time_entries/is_period_locked/') {
        return Promise.resolve({ data: { locked: false } })
      }
      return Promise.resolve({ data: { data: [] } })
    })
    vi.mocked(apiClient.post).mockResolvedValue({ data: { created: 0 } })

    const store = useTimesheetStore()
    await store.fetchWeek()

    expect(apiClient.post).not.toHaveBeenCalledWith(
      'time_entries/prefill_holidays/',
      expect.anything(),
    )
  })

  it('saveCell expose le message du backend dans saveError', async () => {
    vi.mocked(apiClient.post).mockRejectedValue({
      response: {
        status: 400,
        data: {
          error: {
            code: 'LATE_TIMESHEETS',
            message: 'Saisie bloquée : vous devez d\'abord soumettre vos feuilles de temps en retard (semaines du 2026-01-05).',
          },
        },
      },
    })
    const store = useTimesheetStore()
    store.entries = []

    await expect(store.saveCell(10, 20, '2026-06-08', '7.5', 50)).rejects.toBeTruthy()
    expect(store.saveError?.type).toBe('error')
    expect(store.saveError?.message).toContain('Saisie bloquée')
  })

  it('goToWeek vide les entrées immédiatement (pas de lignes périmées)', async () => {
    let resolveFetch: (v: unknown) => void = () => {}
    vi.mocked(apiClient.get).mockReturnValue(
      new Promise((resolve) => { resolveFetch = resolve }) as never,
    )
    const store = useTimesheetStore()
    store.entries = [makeEntry()]

    const pending = store.goToWeek('2026-03-09')
    expect(store.entries).toEqual([])
    resolveFetch({ data: { data: [] } })
    await pending
  })
})

describe('TimesheetCell — erreurs backend affichées', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.resetAllMocks()
  })

  function mountCell(entry: TimeEntry | null = null) {
    return mount(TimesheetCell, {
      props: {
        entry,
        projectId: 10,
        phaseId: 20,
        taskId: 50,
        date: '2026-06-08',
        isLocked: false,
      },
    })
  }

  it('affiche le message backend et pas de flash succès quand la sauvegarde échoue', async () => {
    vi.mocked(apiClient.post).mockRejectedValue({
      response: {
        status: 400,
        data: { error: { code: 'LATE_TIMESHEETS', message: 'Saisie bloquée : soumettez vos semaines en retard.' } },
      },
    })
    const wrapper = mountCell()
    const input = wrapper.find('input')
    await input.setValue('8')
    await input.trigger('blur')
    await vi.waitFor(() => {
      expect(wrapper.text()).toContain('Saisie bloquée')
    })
    expect(wrapper.find('input').classes()).not.toContain('bg-success/10')
  })

  it('affiche le message ENTRY_INVOICED et revient à la valeur initiale', async () => {
    // saveCell appelle toujours POST (l'entrée n'est pas dans store.entries dans ce test)
    vi.mocked(apiClient.post).mockRejectedValue({
      response: {
        status: 400,
        data: { error: { code: 'ENTRY_INVOICED', message: 'Modification impossible : cette heure a été facturée au client.' } },
      },
    })
    const wrapper = mountCell(makeEntry({ id: 1, hours: '7.5' }))
    const input = wrapper.find('input')
    await input.setValue('9')
    await input.trigger('blur')
    await vi.waitFor(() => {
      expect(wrapper.text()).toContain('facturée au client')
    })
    expect(wrapper.find('input').classes()).not.toContain('bg-success/10')
    expect((wrapper.find('input').element as HTMLInputElement).value).toBe('7.5')
  })

  it('flash succès uniquement après une sauvegarde réussie', async () => {
    vi.mocked(apiClient.post).mockResolvedValue({
      data: { data: makeEntry({ id: 99, date: '2026-06-08', hours: '8' }) },
    })
    const wrapper = mountCell()
    const input = wrapper.find('input')
    await input.setValue('8')
    await input.trigger('blur')
    await vi.waitFor(() => {
      expect(wrapper.find('input').classes()).toContain('bg-success/10')
    })
  })
})
