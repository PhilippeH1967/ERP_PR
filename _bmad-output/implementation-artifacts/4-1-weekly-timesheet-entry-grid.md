# Story 4.1: Weekly Timesheet Entry Grid

Status: in-progress

## Story

As an **employee**,
I want to enter my time on a weekly grid by project and phase with auto-save and keyboard navigation,
So that my hours are accurately recorded for billing and project tracking.

## Acceptance Criteria

1. **Given** an authenticated employee **When** I open /timesheets **Then** I see a weekly grid with rows = my project×phase and columns = Mon–Sun
2. **And** Each cell is an editable input accepting 0–24 (decimal hours)
3. **And** Tab moves to the next cell, arrow keys navigate the grid
4. **And** Auto-save triggers on blur within <500ms (NFR2), cell shows green feedback
5. **And** Daily total row shows sum per column with norm indicator (8h)
6. **And** Weekly total shows "X/40 heures saisies" with progress bar
7. **And** Locked phases appear grayed with lock icon (FR20)
8. **And** Client-facing labels displayed on rows
9. **And** "Soumettre la semaine" validates and shows under/over warning (FR19)
10. **And** Optimistic locking: 409 conflict shows dialog

## Tasks / Subtasks

### Backend (DONE)
- [x] Create TimeEntry model (employee, project, phase, date, hours, status, version)
- [x] TimeEntryStatus choices (DRAFT→SUBMITTED→PM_APPROVED→FINANCE_APPROVED→LOCKED)
- [x] UniqueConstraint on employee+project+phase+date
- [x] HistoricalRecords audit trail
- [x] TimeEntrySerializer + TimeEntryViewSet with CRUD
- [x] Filter by employee, project, phase, date, status
- [x] submit_week action endpoint
- [x] Backend tests (5 model + 5 view tests)

### Frontend (TODO)
- [ ] Task F1: Enhance types and store (AC: #1)
  - [ ] F1.1 Update `timesheet.types.ts`: add `TimesheetWeek` (weekStart, rows, dailyTotals, weeklyTotal)
  - [ ] F1.2 Update `useTimesheetStore.ts`: add `currentWeekStart`, `gridRows` computed (entries → project×phase×day grid), `navigateWeek()`
  - [ ] F1.3 Add `getDatesForWeek()` utility returning 7 ISO date strings

- [ ] Task F2: Build interactive grid (AC: #1, #2, #3, #8)
  - [ ] F2.1 Rewrite `TimesheetGrid.vue`: data-driven table with sticky left column, 7 day columns, total column
  - [ ] F2.2 Create `TimesheetCell.vue`: editable input (number, step=0.5, min=0, max=24), focus/blur
  - [ ] F2.3 Tab/Shift+Tab navigation between cells via tabindex
  - [ ] F2.4 Arrow key navigation (up/down rows, left/right days)
  - [ ] F2.5 Week navigator header: ◀ prev | "Semaine du 16 mars 2026" | next ▶

- [ ] Task F3: Auto-save with optimistic update (AC: #4, #10)
  - [ ] F3.1 On blur: debounce 300ms, call updateEntry with If-Match version
  - [ ] F3.2 Optimistic update: reflect value immediately, revert on error
  - [ ] F3.3 Green feedback: bg-success/10 for 500ms after save
  - [ ] F3.4 On 409: show conflict dialog (BaseModal)
  - [ ] F3.5 New cell (no entry): createEntry instead of update

- [ ] Task F4: Totals and indicators (AC: #5, #6)
  - [ ] F4.1 Daily total row with norm comparison (green ✓ =8h, amber ⚠ ≠8h)
  - [ ] F4.2 Row total column (sum of 7 days)
  - [ ] F4.3 Weekly progress bar "X/40 heures saisies"

- [ ] Task F5: Lock indicators (AC: #7)
  - [ ] F5.1 Fetch locks on grid load
  - [ ] F5.2 Locked rows: gray bg, lock icon, input disabled

- [ ] Task F6: Submission validation (AC: #9)
  - [ ] F6.1 Create `SubmitWeekModal.vue` with under/over warning
  - [ ] F6.2 On confirm: submitWeek(), disable editing

- [ ] Task F7: Tests (AC: #1–#10)
  - [ ] F7.1 Test grid transformation (entries → rows)
  - [ ] F7.2 Test daily/weekly totals
  - [ ] F7.3 Test store actions
  - [ ] F7.4 ESLint 0 errors

## Dev Notes

### Grid Data Transformation Pattern

```typescript
const gridRows = computed(() => {
  const rowMap = new Map<string, TimesheetGridRow>()
  for (const entry of entries.value) {
    const key = `${entry.project}-${entry.phase}`
    if (!rowMap.has(key)) {
      rowMap.set(key, { project_id: entry.project, phase_id: entry.phase, entries: {}, is_locked: false })
    }
    rowMap.get(key)!.entries[entry.date] = entry
  }
  return Array.from(rowMap.values())
})
```

### Auto-Save Pattern (TimesheetCell.vue)

```typescript
async function onBlur() {
  if (localValue === originalValue) return
  try {
    if (entry) await timesheetApi.updateEntry(entry.id, { hours: localValue }, entry.version)
    else await timesheetApi.createEntry({ project, phase, date, hours: localValue })
    showGreenFeedback()
  } catch (err) {
    if (err.response?.status === 409) showConflictDialog()
    else revertValue()
  }
}
```

### Files to CREATE
- `features/timesheet/components/TimesheetCell.vue`
- `features/timesheet/components/WeekNavigator.vue`
- `features/timesheet/components/SubmitWeekModal.vue`

### Files to MODIFY
- `features/timesheet/views/TimesheetGrid.vue` (skeleton → full grid)
- `features/timesheet/stores/useTimesheetStore.ts` (add grid transform)
- `features/timesheet/types/timesheet.types.ts` (add TimesheetWeek)

### References
- [Source: epics.md — Story 4.1 AC]
- [Source: ux-design-specification.md — Grid layout, cell interaction]
- [Source: architecture.md — NFR2 <500ms, TimeEntry model]

## Dev Agent Record

### Agent Model Used
Claude Opus 4.6 (1M context)

### Debug Log References

### Completion Notes List
- Backend: TimeEntry model, API, 10 tests — DONE
- Frontend: skeleton grid — IN PROGRESS, needs interactive implementation

### Change Log
- 2026-03-18: Backend implemented as part of Epic 4 batch
- 2026-03-18: Story reopened — frontend grid not yet interactive

### File List

**Backend (done):**
- backend/apps/time_entries/models.py
- backend/apps/time_entries/serializers.py
- backend/apps/time_entries/views.py
- backend/apps/time_entries/urls.py
- backend/apps/time_entries/tests/test_models.py
- backend/apps/time_entries/tests/test_views.py

**Frontend (in progress):**
- frontend/src/features/timesheet/views/TimesheetGrid.vue
- frontend/src/features/timesheet/stores/useTimesheetStore.ts
- frontend/src/features/timesheet/types/timesheet.types.ts
- frontend/src/features/timesheet/api/timesheetApi.ts
