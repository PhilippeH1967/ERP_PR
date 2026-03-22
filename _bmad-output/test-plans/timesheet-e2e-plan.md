# Timesheet E2E Test Plan

## Document Info

| Field          | Value                          |
|----------------|--------------------------------|
| Feature        | Timesheet (time_entries)       |
| Date           | 2026-03-22                     |
| Source Files   | `backend/apps/time_entries/models.py`, `views.py`, `urls.py`, `payroll_controls.py` |
| API Endpoints  | `/api/time_entries/`, `/api/weekly_approvals/`, `/api/timesheet_locks/`, `/api/period_unlocks/` |

---

## 1. Test Users and Test Data

### 1.1 Minimum Test Users

| User ID | Username         | Role(s)          | Notes                                      |
|---------|------------------|------------------|---------------------------------------------|
| U1      | `emp_alice`      | EMPLOYEE         | Primary employee under test                 |
| U2      | `emp_bob`        | EMPLOYEE         | Second employee (for multi-PM scenarios)    |
| U3      | `pm_carol`       | PM               | PM on Project-A and Project-B               |
| U4      | `pm_dave`        | PM               | PM on Project-C only (multi-PM scenario)    |
| U5      | `finance_eve`    | FINANCE          | Finance approver                            |
| U6      | `paie_frank`     | PAIE             | Payroll validator                           |
| U7      | `admin_grace`    | ADMIN            | System administrator                        |
| U8      | `emp_self_pm`    | EMPLOYEE, PM     | Employee who is also PM on their own project (self-approval test) |

### 1.2 Minimum Test Data

| Entity        | ID / Code   | Details                                                     |
|---------------|-------------|-------------------------------------------------------------|
| Tenant        | T1          | Default tenant, all users associated                        |
| Project-A     | `PRJ-A`     | External (billable), `pm=pm_carol`                          |
| Project-B     | `PRJ-B`     | External (billable), `pm=pm_carol`                          |
| Project-C     | `PRJ-C`     | External (billable), `pm=pm_dave`                           |
| Project-INT   | `PRJ-INT`   | Internal (`is_internal=True`), `pm=pm_carol`                |
| Project-SICK  | `PRJ-SICK`  | Internal, name="Maladie", `pm=pm_carol`                    |
| Project-LEAVE | `PRJ-LEAVE` | Internal, name="Conge / Vacances", `pm=pm_carol`           |
| Phase-A1      | PH-A1       | Phase on Project-A                                          |
| Phase-A2      | PH-A2       | Phase on Project-A                                          |
| Week-CURRENT  | W1          | A full Sun-Sat week in the future (e.g. 2026-03-29 to 2026-04-04) |
| Week-PREV     | W0          | The week before W1                                          |
| Week-OLD      | W-OLD       | A week in the past (e.g. 2026-01-04 to 2026-01-10) for freeze tests |

### 1.3 Contract Assumptions

- All employees have a 40h/week contract (hardcoded in `payroll_controls.py`).

---

## 2. Employee Flow

### TC-EMP-01: Navigate Weeks

**Preconditions:** `emp_alice` is authenticated. No entries exist yet.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `GET /api/time_entries/weekly_stats/` (no `week_start` param) | Returns stats for the current week. `contract_hours=40`, `week_totals` is a 4-element array, `average_4_weeks` and `billable_rate_percent` are present. |
| 2 | `GET /api/time_entries/weekly_stats/?week_start=2026-03-29` | Returns stats scoped to that specific week. |
| 3 | `GET /api/time_entries/?date__gte=2026-03-29&date__lte=2026-04-04` | Returns empty list (no entries yet). |

**Postconditions:** No state change.

---

### TC-EMP-02: Add Task and Enter Hours

**Preconditions:** `emp_alice` authenticated. Projects A, B, INT exist.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `POST /api/time_entries/` with `{project: PRJ-A, phase: PH-A1, date: "2026-03-30", hours: 8}` | 201 Created. Entry returned with `status="DRAFT"`, `employee=emp_alice`. |
| 2 | `POST /api/time_entries/` with `{project: PRJ-A, phase: PH-A1, date: "2026-03-31", hours: 8}` | 201 Created. Second entry. |
| 3 | `POST /api/time_entries/` with `{project: PRJ-B, phase: null, date: "2026-03-30", hours: 2}` | 201 Created. Different project, same day. |
| 4 | `POST /api/time_entries/` with `{project: PRJ-A, phase: PH-A1, date: "2026-03-30", hours: 4}` | 400 Error. UniqueConstraint violation (same employee+project+phase+date). |
| 5 | `PATCH /api/time_entries/{id_from_step_1}/` with `{hours: 7.5, notes: "Reunion client"}` | 200 OK. Hours updated to 7.5, notes saved. |

**Postconditions:** 3 DRAFT entries exist for emp_alice in week W1.

---

### TC-EMP-03: Submit Week

**Preconditions:** `emp_alice` has 5 DRAFT entries covering Mon-Fri of W1 (40h total).

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `POST /api/time_entries/submit_week/` with `{week_start: "2026-03-29"}` | `{submitted_count: 5}`. |
| 2 | `GET /api/time_entries/?date__gte=2026-03-29&date__lte=2026-04-04` | All 5 entries now have `status="SUBMITTED"`. |
| 3 | `GET /api/weekly_approvals/?employee={alice_id}&week_start=2026-03-29` | One WeeklyApproval record exists with `pm_status="PENDING"`, `finance_status="PENDING"`. |

**Postconditions:** WeeklyApproval created. All entries SUBMITTED.

---

### TC-EMP-04: See Rejection and Re-submit

**Preconditions:** `emp_alice` has SUBMITTED entries for W1. PM has rejected some entries.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `GET /api/time_entries/?date__gte=2026-03-29&date__lte=2026-04-04` | Rejected entries show `status="DRAFT"` and `rejection_reason` is populated (e.g. "Mauvais code projet"). |
| 2 | `PATCH /api/time_entries/{rejected_id}/` with `{project: PRJ-B, hours: 8}` | 200 OK. Entry corrected. |
| 3 | `POST /api/time_entries/submit_week/` with `{week_start: "2026-03-29"}` | `{submitted_count: N}` where N = number of corrected DRAFT entries. `rejection_reason` cleared. |
| 4 | `GET /api/time_entries/{rejected_id}/` | `status="SUBMITTED"`, `rejection_reason=""`. |

**Postconditions:** Corrected entries re-submitted.

---

### TC-EMP-05: Blocked by Locked Period

**Preconditions:** Admin has locked period W1 (all entries status=LOCKED).

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `GET /api/time_entries/is_period_locked/?week_start=2026-03-29` | `{locked: true}`. |
| 2 | `POST /api/time_entries/` with `{project: PRJ-A, date: "2026-03-30", hours: 8}` | 400 Error with `code="PERIOD_LOCKED"`. |
| 3 | `PATCH /api/time_entries/{locked_entry_id}/` with `{hours: 4}` | 400 Error with `code="ENTRY_LOCKED"`. |
| 4 | `DELETE /api/time_entries/{locked_entry_id}/` | 400 Error with `code="ENTRY_LOCKED"`. |
| 5 | `POST /api/time_entries/submit_week/` with `{week_start: "2026-03-29"}` | 400 Error with `code="PERIOD_LOCKED"`. |

**Postconditions:** No changes possible on locked entries.

---

### TC-EMP-06: Blocked by Frozen Period

**Preconditions:** Admin has set `freeze_before=2026-03-01`. Employee tries to enter hours on 2026-02-15.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `POST /api/time_entries/` with `{project: PRJ-A, date: "2026-02-15", hours: 8}` | 400 Error with `code="PERIOD_FROZEN"`, message mentions freeze date. |
| 2 | `GET /api/time_entries/is_period_locked/?week_start=2026-02-15` | `{locked: true, reason: "Gele avant le 2026-03-01"}`. |

**Postconditions:** No entry created.

---

### TC-EMP-07: Copy Previous Week

**Preconditions:** `emp_alice` has entries in week W0. Week W1 is open.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `POST /api/time_entries/copy_previous_week/` with `{week_start: "2026-03-29"}` | `{copied_count: N}` matching number of W0 entries. |
| 2 | `GET /api/time_entries/?date__gte=2026-03-29&date__lte=2026-04-04` | New DRAFT entries exist with same project/phase/hours as W0, dates shifted +7 days. |
| 3 | Re-call `POST /api/time_entries/copy_previous_week/` with same week | `{copied_count: 0}` (duplicates skipped). |

**Postconditions:** W1 populated with DRAFT copies.

---

### TC-EMP-08: Copy Previous Week Blocked by Lock

**Preconditions:** Week W1 is locked.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `POST /api/time_entries/copy_previous_week/` with `{week_start: "2026-03-29"}` | 400 Error with `code="PERIOD_LOCKED"`. |

**Postconditions:** No entries created.

---

### TC-EMP-09: Favorite Flag

**Preconditions:** `emp_alice` has a DRAFT entry.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `PATCH /api/time_entries/{id}/` with `{is_favorite: true}` | 200 OK. `is_favorite=true`. |
| 2 | `GET /api/time_entries/?is_favorite=true` | Entry returned in results. |

---

## 3. PM Flow

### TC-PM-01: View PM Dashboard

**Preconditions:** `pm_carol` is PM on PRJ-A and PRJ-B. `emp_alice` and `emp_bob` have SUBMITTED entries on those projects for W1.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `GET /api/weekly_approvals/pm_dashboard/?week_start=2026-03-29` (as `pm_carol`) | Response contains `kpis` (total_hours, billable_rate, pending_count, employee_count), `projects` array with PRJ-A and PRJ-B, `employees` array with alice and bob. |
| 2 | Verify `employees[].pm_status` | Both show `"PENDING"`. |
| 3 | Verify `employees[].trend_4w` | Array of 4 floats (3 previous weeks + current). |
| 4 | Verify `employees[].projects` | Per-project breakdown with hours, project_code, project_name. |

**Postconditions:** No state change.

---

### TC-PM-02: View Approval Entry Details

**Preconditions:** `emp_alice` has a WeeklyApproval for W1.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `GET /api/weekly_approvals/{approval_id}/entries/` (as `pm_carol`) | Returns list of TimeEntry objects with extra fields: `pm_name`, `is_my_project`, `approval_color`. |
| 2 | Entries on PRJ-A (carol's project) | `is_my_project=true`, `approval_color="mine"` (while SUBMITTED). |
| 3 | Entries on PRJ-C (dave's project, if any) | `is_my_project=false`, `approval_color="other"`. |

**Postconditions:** No state change.

---

### TC-PM-03: Approve Specific Entries

**Preconditions:** `emp_alice` has SUBMITTED entries on PRJ-A (pm_carol's project).

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `POST /api/time_entries/approve_entries/` with `{entry_ids: [id1, id2]}` (as `pm_carol`) | `{approved_count: 2}`. |
| 2 | `GET /api/time_entries/{id1}/` | `status="PM_APPROVED"`. |
| 3 | If ALL of alice's entries for the week are now PM_APPROVED, check WeeklyApproval | `pm_status="APPROVED"`, `pm_approved_by=pm_carol`, `pm_approved_at` is set. |

**Postconditions:** Entries moved to PM_APPROVED.

---

### TC-PM-04: Approve All Entries for Employee/Week

**Preconditions:** `emp_bob` has SUBMITTED entries on PRJ-B for W1.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `POST /api/time_entries/approve_all_my_entries/` with `{employee_id: bob_id, week_start: "2026-03-29"}` (as `pm_carol`) | `{approved_count: N}`. |
| 2 | All bob's entries on carol's projects for W1 | `status="PM_APPROVED"`. |

**Postconditions:** All relevant entries approved in bulk.

---

### TC-PM-05: Reject Entries

**Preconditions:** `emp_alice` has SUBMITTED entries on PRJ-A.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `POST /api/time_entries/reject_entries/` with `{entry_ids: [id1], reason: "Mauvais code projet"}` (as `pm_carol`) | `{rejected_count: 1, reason: "Mauvais code projet"}`. |
| 2 | `GET /api/time_entries/{id1}/` | `status="DRAFT"`, `rejection_reason="Mauvais code projet"`. |

**Postconditions:** Entry reverted to DRAFT with reason.

---

### TC-PM-06: Reject via WeeklyApproval

**Preconditions:** `emp_alice` has a PENDING WeeklyApproval for W1 with SUBMITTED entries.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `POST /api/weekly_approvals/{approval_id}/reject_pm/` with `{reason: "Heures incorrectes"}` (as `pm_carol`) | 200. `pm_status="REJECTED"`. |
| 2 | `GET /api/time_entries/?employee={alice_id}&date__gte=2026-03-29&date__lte=2026-04-04` | All SUBMITTED entries reverted to `status="DRAFT"`, `rejection_reason="Heures incorrectes"`. |

**Postconditions:** Entries back to DRAFT, approval rejected.

---

### TC-PM-07: Anti-Self-Approval

**Preconditions:** `emp_self_pm` has SUBMITTED entries on their own project.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `POST /api/time_entries/approve_entries/` with own entry IDs (as `emp_self_pm`) | 403 with `code="SELF_APPROVAL"`. |
| 2 | `POST /api/time_entries/approve_all_my_entries/` with `{employee_id: self_id, week_start: ...}` | 403 with `code="SELF_APPROVAL"`. |
| 3 | `POST /api/weekly_approvals/{own_approval_id}/approve_pm/` | 403 with `code="SELF_APPROVAL"`. |

**Postconditions:** No approval recorded.

---

### TC-PM-08: Multi-PM Scenario

**Preconditions:** `emp_alice` has entries on PRJ-A (pm_carol) AND PRJ-C (pm_dave) in W1, all SUBMITTED.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `pm_carol` approves alice's PRJ-A entries via `approve_entries` | PRJ-A entries = PM_APPROVED. PRJ-C entries unchanged (SUBMITTED). |
| 2 | `pm_carol` calls `pm_dashboard` | Alice still shows `pm_status="PENDING"` because PRJ-C entries are not approved. |
| 3 | `pm_dave` approves alice's PRJ-C entries | All entries now PM_APPROVED. |
| 4 | WeeklyApproval for alice | `pm_status="APPROVED"` (auto-updated after last approval). |
| 5 | `pm_carol` calls `pm_dashboard` | Alice shows `pm_status="APPROVED"`, `approved_by_other` may be populated if dave approved last. |

**Postconditions:** Full PM approval achieved across two PMs.

---

### TC-PM-09: PM Cannot Approve Entries on Other PM's Project

**Preconditions:** `emp_alice` has SUBMITTED entries on PRJ-C (pm_dave's project).

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `POST /api/time_entries/approve_entries/` with PRJ-C entry IDs (as `pm_carol`) | `{approved_count: 0}`. The filter `project_id__in=my_project_ids` excludes PRJ-C. |

**Postconditions:** No entries approved.

---

### TC-PM-10: Reject Already-Approved Weekly Approval Fails

**Preconditions:** WeeklyApproval for alice, W1 has `pm_status="APPROVED"`.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `POST /api/weekly_approvals/{approval_id}/reject_pm/` | 400 with `code="INVALID_STATUS"` (only PENDING can be rejected). |

**Postconditions:** No state change.

---

## 4. Paie Flow

### TC-PAIE-01: View Paie Dashboard

**Preconditions:** Multiple employees have entries for W1 with various statuses. `paie_frank` authenticated.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `GET /api/weekly_approvals/paie_dashboard/?week_start=2026-03-29` (as `paie_frank`) | Response contains `kpis` (total_employees, submitted, pm_approved, validated, missing, alerts_error, alerts_warning, clean), `employees` array sorted by severity (errors first). |
| 2 | Employee with no entries | `severity="error"`, alert `code="MISSING_TIMESHEET"`. |
| 3 | Employee with 32h, no absences | Alert `code="INCOMPLETE_HOURS"`, `severity="warning"`. |
| 4 | Employee with all PM_APPROVED | `all_pm_approved=true`. |

**Postconditions:** No state change.

---

### TC-PAIE-02: Payroll Controls - Overtime with Sick Leave

**Preconditions:** `emp_alice` has 42h total (2h overtime) + 8h on Project-SICK ("Maladie") in W1. All PM_APPROVED.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `GET /api/weekly_approvals/paie_dashboard/?week_start=2026-03-29` | Alice's alerts include `code="OVERTIME_WITH_SICK"`, `severity="error"`. |

---

### TC-PAIE-03: Payroll Controls - Day Over 10h

**Preconditions:** `emp_alice` has 12h on a single day.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Paie dashboard for that week | Alert `code="DAY_OVER_10H"`, `severity="warning"`. |

---

### TC-PAIE-04: Payroll Controls - Weekend Work

**Preconditions:** `emp_alice` has 4h on a Saturday.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Paie dashboard | Alert `code="WEEKEND_WORK"`, `severity="warning"`, message mentions "samedi". |

---

### TC-PAIE-05: Payroll Controls - Legal Max 50h

**Preconditions:** `emp_alice` has 52h in W1, all PM_APPROVED.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Paie dashboard | Alert `code="LEGAL_MAX_50H"`, `severity="error"`. |

---

### TC-PAIE-06: Payroll Controls - Sick and Work Same Day

**Preconditions:** `emp_alice` has 4h on PRJ-SICK + 4h on PRJ-A on the same date.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Paie dashboard | Alert `code="SICK_AND_WORK_SAME_DAY"`, `severity="error"`. |

---

### TC-PAIE-07: Payroll Controls - Consecutive Overtime

**Preconditions:** `emp_alice` has >40h for 3+ consecutive weeks (including current).

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Paie dashboard | Alert `code="CONSECUTIVE_OVERTIME"`, `severity="error"`, mentions burn-out risk. |

---

### TC-PAIE-08: Payroll Controls - Unusual Trend

**Preconditions:** `emp_alice` averaged 40h over previous 4 weeks but has 50h this week (>20% deviation).

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Paie dashboard | Alert `code="UNUSUAL_TREND"`, `severity="info"`. |

---

### TC-PAIE-09: Payroll Controls - PM Not Approved

**Preconditions:** `emp_alice` has SUBMITTED entries (not yet PM_APPROVED).

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Paie dashboard | Alert `code="PM_NOT_APPROVED"`, `severity="error"`. |

---

### TC-PAIE-10: Validate Paie (Single)

**Preconditions:** `emp_alice` has all entries PM_APPROVED for W1. WeeklyApproval exists.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `POST /api/weekly_approvals/{approval_id}/validate_paie/` (as `paie_frank`) | 200. `paie_status="APPROVED"`, `paie_validated_by=paie_frank`, `paie_validated_at` set. |
| 2 | `GET /api/time_entries/?employee={alice_id}&date__gte=2026-03-29&date__lte=2026-04-04` | Entries that were PM_APPROVED are now `status="PAIE_VALIDATED"`. |

**Postconditions:** Entries advanced to PAIE_VALIDATED.

---

### TC-PAIE-11: Validate Paie Fails if Not All PM Approved

**Preconditions:** `emp_alice` has a mix of SUBMITTED and PM_APPROVED entries. WeeklyApproval exists.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `POST /api/weekly_approvals/{approval_id}/validate_paie/` (as `paie_frank`) | 400 with `code="NOT_ALL_PM_APPROVED"`. |

**Postconditions:** No entries changed.

---

### TC-PAIE-12: Bulk Validate Paie

**Preconditions:** `emp_alice` and `emp_bob` both have all PM_APPROVED entries. Two WeeklyApprovals exist.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `POST /api/weekly_approvals/bulk_validate_paie/` with `{approval_ids: [aid1, aid2]}` (as `paie_frank`) | `{validated_count: 2, skipped_count: 0, skipped: []}`. |
| 2 | Both approvals | `paie_status="APPROVED"`. |

**Postconditions:** Both employees' entries at PAIE_VALIDATED.

---

### TC-PAIE-13: Bulk Validate Paie - Partial Skip

**Preconditions:** `emp_alice` all PM_APPROVED. `emp_bob` has SUBMITTED entries (not all approved).

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `POST /api/weekly_approvals/bulk_validate_paie/` with both IDs | `{validated_count: 1, skipped_count: 1, skipped: [{id: bob_aid, reason: "Not all PM approved"}]}`. |

**Postconditions:** Alice validated, Bob skipped.

---

### TC-PAIE-14: Bulk Validate Paie - Self-Approval Skip

**Preconditions:** `paie_frank` has entries and a WeeklyApproval for himself.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `POST /api/weekly_approvals/bulk_validate_paie/` including frank's approval ID | Skipped with `reason: "Self-approval"`. |

---

### TC-PAIE-15: Reject Paie

**Preconditions:** `emp_alice` has `paie_status="APPROVED"` (entries at PAIE_VALIDATED).

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `POST /api/weekly_approvals/{approval_id}/reject_paie/` (as `paie_frank`) | 200. `paie_status="REJECTED"`, `paie_validated_by=null`, `paie_validated_at=null`. |
| 2 | `GET /api/time_entries/?employee={alice_id}&date__gte=2026-03-29&date__lte=2026-04-04` | Entries reverted from PAIE_VALIDATED to `status="PM_APPROVED"`. |

**Postconditions:** Entries back at PM_APPROVED level.

---

### TC-PAIE-16: Reject Paie Fails if Not Previously Validated

**Preconditions:** WeeklyApproval has `paie_status="PENDING"`.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `POST /api/weekly_approvals/{approval_id}/reject_paie/` | 400 with `code="INVALID_STATUS"`. |

---

### TC-PAIE-17: Paie Anti-Self-Approval

**Preconditions:** `paie_frank` has a WeeklyApproval for himself with all PM_APPROVED entries.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `POST /api/weekly_approvals/{frank_approval_id}/validate_paie/` (as `paie_frank`) | 403 with `code="SELF_APPROVAL"`. |

---

## 5. Finance Flow

### TC-FIN-01: View Finance Dashboard

**Preconditions:** Multiple employees have WeeklyApprovals for W1 with various pm_status and finance_status values.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `GET /api/weekly_approvals/finance_dashboard/?week_start=2026-03-29` (as `finance_eve`) | Response contains `kpis` (total_approvals, pending_finance, approved_finance, rejected_finance), `employees` array. |
| 2 | Employee with `pm_status=APPROVED`, `finance_status=PENDING` | Shows as pending for finance. |
| 3 | Verify `employees[].total_week_hours` and `pm_approved_hours` | Correct aggregations. |

**Postconditions:** No state change.

---

### TC-FIN-02: Finance Approve

**Preconditions:** `emp_alice` has WeeklyApproval with `pm_status=APPROVED`, `finance_status=PENDING`.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `POST /api/weekly_approvals/{approval_id}/approve_finance/` (as `finance_eve`) | 200. `finance_status="APPROVED"`, `finance_approved_by=finance_eve`, `finance_approved_at` set. |

**Postconditions:** Finance approval recorded.

---

### TC-FIN-03: Finance Reject

**Preconditions:** `emp_alice` has WeeklyApproval with `finance_status=PENDING`.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `POST /api/weekly_approvals/{approval_id}/reject_finance/` (as `finance_eve`) | 200. `finance_status="REJECTED"`. |

**Postconditions:** Finance rejection recorded.

---

### TC-FIN-04: Finance Reject Fails if Not Pending

**Preconditions:** WeeklyApproval has `finance_status="APPROVED"`.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `POST /api/weekly_approvals/{approval_id}/reject_finance/` | 400 with `code="INVALID_STATUS"`. |

---

### TC-FIN-05: Finance Anti-Self-Approval

**Preconditions:** `finance_eve` has a WeeklyApproval for herself.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `POST /api/weekly_approvals/{eve_approval_id}/approve_finance/` (as `finance_eve`) | 403 with `code="SELF_APPROVAL"`. |

---

### TC-FIN-06: Finance View Entry Details

**Preconditions:** `emp_alice` has a WeeklyApproval for W1.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `GET /api/weekly_approvals/{approval_id}/entries/` (as `finance_eve`) | Returns full entry list with project details, hours, statuses, pm_name, approval_color. |

---

## 6. Admin Flow

### TC-ADM-01: Admin Sees All on PM Dashboard

**Preconditions:** `admin_grace` has ADMIN role. Multiple PMs have projects.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `GET /api/weekly_approvals/pm_dashboard/?week_start=2026-03-29` (as `admin_grace`) | Sees ALL projects (not just owned), all employees across all projects. |

**Postconditions:** No state change.

---

### TC-ADM-02: Lock Period

**Preconditions:** `emp_alice` and `emp_bob` have entries (various statuses) in W1.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `POST /api/time_entries/lock_period/` with `{period_start: "2026-03-29", period_end: "2026-04-04"}` (as `admin_grace`) | `{locked_count: N}` where N = number of non-LOCKED entries in that week. |
| 2 | `GET /api/time_entries/?date__gte=2026-03-29&date__lte=2026-04-04` | All entries have `status="LOCKED"`. |
| 3 | `GET /api/time_entries/is_period_locked/?week_start=2026-03-29` | `{locked: true}`. |

**Postconditions:** All entries in W1 locked.

---

### TC-ADM-03: Lock Period Requires Sunday Start

**Preconditions:** Admin authenticated.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `POST /api/time_entries/lock_period/` with `{period_start: "2026-03-30", period_end: "2026-04-05"}` (Monday start) | 400 with `code="INVALID_PERIOD"`, message about dimanche. |
| 2 | `POST /api/time_entries/lock_period/` with `{period_start: "2026-03-29", period_end: "2026-04-05"}` (Sun to Sun) | 400 with `code="INVALID_PERIOD"`, message about samedi. |

---

### TC-ADM-04: Unlock Period

**Preconditions:** W1 is locked (all entries LOCKED).

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `POST /api/time_entries/unlock_period/` with `{period_start: "2026-03-29", period_end: "2026-04-04"}` (as `admin_grace`) | `{unlocked_count: N}`. |
| 2 | `GET /api/time_entries/?date__gte=2026-03-29&date__lte=2026-04-04` | All entries have `status="SUBMITTED"` (not DRAFT). |
| 3 | `GET /api/time_entries/is_period_locked/?week_start=2026-03-29` | `{locked: false}`. |

**Postconditions:** Entries reverted to SUBMITTED for re-processing.

---

### TC-ADM-05: Freeze Before Date (lock_before)

**Preconditions:** Entries exist across multiple weeks (Jan, Feb, Mar 2026).

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `POST /api/time_entries/lock_before/` with `{before_date: "2026-03-01"}` (as `admin_grace`) | `{locked_count: N, before_date: "2026-03-01"}`. All entries before March 1st now LOCKED. |
| 2 | `POST /api/time_entries/` with `{project: PRJ-A, date: "2026-02-15", hours: 8}` (as `emp_alice`) | 400 with `code="PERIOD_FROZEN"`. |
| 3 | `POST /api/time_entries/` with `{project: PRJ-A, date: "2026-03-15", hours: 8}` (as `emp_alice`) | 201 Created (date is after freeze). |
| 4 | PeriodFreeze record created | `freeze_before=2026-03-01`, `frozen_by=admin_grace`. |

**Postconditions:** Global freeze active. New entries on frozen dates blocked.

---

### TC-ADM-06: Freeze Advances (Does Not Regress)

**Preconditions:** Freeze already set to `2026-03-01`.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `POST /api/time_entries/lock_before/` with `{before_date: "2026-04-01"}` | New PeriodFreeze created with `freeze_before=2026-04-01`. |
| 2 | `POST /api/time_entries/lock_before/` with `{before_date: "2026-02-01"}` | No new PeriodFreeze created (2026-02-01 < existing 2026-04-01). Entries before Feb 1 still locked. |

---

### TC-ADM-07: Period Summary

**Preconditions:** Entries exist across multiple weeks with various statuses.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `GET /api/time_entries/period_summary/` (as `admin_grace`) | `{weeks: [...]}` with each week showing `week_start`, `week_end`, `entry_count`, `total_hours`, `employee_count`, `statuses`, `status` ("locked"/"partial"/"open"). Most recent first. |
| 2 | A week where all entries are LOCKED | `status="locked"`. |
| 3 | A week with mix of LOCKED and DRAFT | `status="partial"`. |
| 4 | A week with no LOCKED entries | `status="open"`. |

---

### TC-ADM-08: Lock/Unlock Role Enforcement

**Preconditions:** `emp_alice` (EMPLOYEE role only) authenticated.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `POST /api/time_entries/lock_period/` (as `emp_alice`) | 403 with `code="FORBIDDEN"`. |
| 2 | `POST /api/time_entries/unlock_period/` (as `emp_alice`) | 403 with `code="FORBIDDEN"`. |
| 3 | `POST /api/time_entries/lock_before/` (as `emp_alice`) | 403 with `code="FORBIDDEN"`. |
| 4 | `GET /api/time_entries/period_summary/` (as `emp_alice`) | 403 with `code="FORBIDDEN"`. |

**Postconditions:** No state change. Only ADMIN, FINANCE, PAIE can lock/unlock.

---

## 7. Period Lock Flow (Detailed)

### TC-LOCK-01: Full Lock-Unlock Cycle

**Preconditions:** W1 has entries in SUBMITTED/PM_APPROVED status.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `POST /api/time_entries/lock_period/` with W1 dates (as `admin_grace`) | Entries locked. |
| 2 | `POST /api/time_entries/` with date in W1 (as `emp_alice`) | 400 `PERIOD_LOCKED`. |
| 3 | `PATCH /api/time_entries/{id}/` on W1 entry | 400 `ENTRY_LOCKED`. |
| 4 | `DELETE /api/time_entries/{id}/` on W1 entry | 400 `ENTRY_LOCKED`. |
| 5 | `POST /api/time_entries/submit_week/` for W1 | 400 `PERIOD_LOCKED`. |
| 6 | `POST /api/time_entries/unlock_period/` with W1 dates | Entries reverted to SUBMITTED. |
| 7 | `PATCH /api/time_entries/{id}/` with `{hours: 5}` (as `emp_alice`) | 200 OK. Entry editable again. |
| 8 | `POST /api/time_entries/submit_week/` for W1 | Succeeds (DRAFT entries submitted). |

---

### TC-LOCK-02: Freeze with Exception Unlock

**Preconditions:** `freeze_before=2026-03-01`. `emp_alice` needs to correct entries on 2026-02-15.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `POST /api/time_entries/` with date=2026-02-15 (as `emp_alice`) | 400 `PERIOD_FROZEN`. |
| 2 | `POST /api/period_unlocks/` with `{period_start: "2026-02-15", period_end: "2026-02-21", reason: "CORRECTION", justification: "Erreur de saisie"}` (as `admin_grace`) | 201 Created. PeriodUnlock record. |
| 3 | `GET /api/time_entries/is_period_locked/?week_start=2026-02-15` | `{locked: false, reason: "Deverrouillee temporairement"}`. |
| 4 | `POST /api/time_entries/` with date=2026-02-16 (as `emp_alice`) | 201 Created. Exception allows entry on frozen date. |
| 5 | `PATCH /api/time_entries/{locked_entry_in_range}/` with `{hours: 6}` | 200 OK (if entry is not individually LOCKED status). |

**Postconditions:** Employee can modify entries within the exception window.

---

### TC-LOCK-03: Revoke Exception Unlock

**Preconditions:** PeriodUnlock exists for 2026-02-15 to 2026-02-21. Entries in that range have been modified (status SUBMITTED/DRAFT).

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `DELETE /api/period_unlocks/{unlock_id}/` (as `admin_grace`) | 200/204. PeriodUnlock deleted. |
| 2 | All entries in 2026-02-15 to 2026-02-21 | `status="LOCKED"` (re-locked on destroy). |
| 3 | `POST /api/time_entries/` with date=2026-02-16 (as `emp_alice`) | 400 `PERIOD_FROZEN` (exception no longer active). |

**Postconditions:** Period re-locked, exception revoked.

---

### TC-LOCK-04: PeriodUnlock Reasons

**Preconditions:** Admin authenticated.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `POST /api/period_unlocks/` with `reason: "CORRECTION"` | 201 Created. |
| 2 | `POST /api/period_unlocks/` with `reason: "AMENDMENT"` | 201 Created. |
| 3 | `POST /api/period_unlocks/` with `reason: "AUDIT"` | 201 Created. |
| 4 | `POST /api/period_unlocks/` with `reason: "INVALID"` | 400 Error (not a valid choice). |

---

### TC-LOCK-05: TimesheetLock (Phase-Level)

**Preconditions:** Project-A with Phase-A1 exists.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `POST /api/timesheet_locks/` with `{project: PRJ-A, phase: PH-A1, lock_type: "PHASE"}` (as `admin_grace`) | 201 Created. `locked_by=admin_grace`, `locked_at` auto-set. |
| 2 | `GET /api/timesheet_locks/` | Lock record visible with project, phase, lock_type, locked_by. |

---

### TC-LOCK-06: TimesheetLock (Person-Level)

**Preconditions:** Project-A exists.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `POST /api/timesheet_locks/` with `{project: PRJ-A, person: alice_id, lock_type: "PERSON"}` (as `admin_grace`) | 201 Created. |
| 2 | `GET /api/timesheet_locks/` | Lock record shows person-level lock on alice for PRJ-A. |
| 3 | `DELETE /api/timesheet_locks/{lock_id}/` | 204. Lock removed. |

---

## 8. Cross-Cutting Concerns

### TC-XCUT-01: Optimistic Concurrency (If-Match)

**Preconditions:** `emp_alice` has a DRAFT entry with `version=1`.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `PATCH /api/time_entries/{id}/` with `If-Match: 1`, `{hours: 5}` | 200 OK. Version incremented to 2. |
| 2 | `PATCH /api/time_entries/{id}/` with `If-Match: 1` (stale), `{hours: 6}` | 409 Conflict (version mismatch). |

---

### TC-XCUT-02: Tenant Isolation

**Preconditions:** Two tenants exist (T1 and T2). `emp_alice` is on T1 only.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `GET /api/time_entries/` (as alice, tenant T1) | Returns alice's T1 entries only. |
| 2 | Entries from T2 | Never appear in alice's results. |

---

### TC-XCUT-03: Employee Can Only See Own Entries

**Preconditions:** `emp_alice` and `emp_bob` both have entries.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `GET /api/time_entries/` (as `emp_alice`) | Only alice's entries returned (queryset filtered by `employee=request.user`). |
| 2 | `GET /api/time_entries/{bob_entry_id}/` (as `emp_alice`) | 404 Not Found. |

---

### TC-XCUT-04: Entry Filtering

**Preconditions:** `emp_alice` has entries on multiple projects, dates, and statuses.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | `GET /api/time_entries/?project={prj_a_id}` | Only PRJ-A entries. |
| 2 | `GET /api/time_entries/?status=DRAFT` | Only DRAFT entries. |
| 3 | `GET /api/time_entries/?date__gte=2026-03-29&date__lte=2026-04-04` | Only entries in W1. |
| 4 | `GET /api/time_entries/?phase={ph_a1_id}` | Only entries on Phase-A1. |

---

### TC-XCUT-05: History Tracking

**Preconditions:** `emp_alice` creates, updates, and submits an entry.

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | After create, update hours, submit | `django-simple-history` creates HistoricalRecords for each change. |
| 2 | Query historical records | Full audit trail with old/new values, timestamps, user who made the change. |

---

## 9. Status Transition Matrix

Reference for all test scenarios. Valid transitions:

```
DRAFT ──submit_week──> SUBMITTED
SUBMITTED ──approve_entries──> PM_APPROVED
SUBMITTED ──reject_entries──> DRAFT (with rejection_reason)
SUBMITTED ──reject_pm (weekly)──> DRAFT (with rejection_reason)
PM_APPROVED ──validate_paie──> PAIE_VALIDATED
PAIE_VALIDATED ──reject_paie──> PM_APPROVED
Any (except LOCKED) ──lock_period/lock_before──> LOCKED
LOCKED ──unlock_period──> SUBMITTED
```

---

## 10. Test Data Setup Script (Pseudocode)

```python
# 1. Create tenant
tenant = Tenant.objects.create(name="Test Corp")

# 2. Create users
alice = User.objects.create_user("emp_alice", password="test123")
bob = User.objects.create_user("emp_bob", password="test123")
carol = User.objects.create_user("pm_carol", password="test123")
dave = User.objects.create_user("pm_dave", password="test123")
eve = User.objects.create_user("finance_eve", password="test123")
frank = User.objects.create_user("paie_frank", password="test123")
grace = User.objects.create_user("admin_grace", password="test123")
self_pm = User.objects.create_user("emp_self_pm", password="test123")

# 3. Associate users to tenant
for u in [alice, bob, carol, dave, eve, frank, grace, self_pm]:
    UserTenantAssociation.objects.create(user=u, tenant=tenant)

# 4. Create roles
ProjectRole.objects.create(user=alice, role="EMPLOYEE", tenant=tenant)
ProjectRole.objects.create(user=bob, role="EMPLOYEE", tenant=tenant)
ProjectRole.objects.create(user=carol, role="PM", tenant=tenant)
ProjectRole.objects.create(user=dave, role="PM", tenant=tenant)
ProjectRole.objects.create(user=eve, role="FINANCE", tenant=tenant)
ProjectRole.objects.create(user=frank, role="PAIE", tenant=tenant)
ProjectRole.objects.create(user=grace, role="ADMIN", tenant=tenant)
ProjectRole.objects.create(user=self_pm, role="EMPLOYEE", tenant=tenant)
ProjectRole.objects.create(user=self_pm, role="PM", tenant=tenant)

# 5. Create projects
prj_a = Project.objects.create(code="PRJ-A", name="Project Alpha", pm=carol, is_internal=False, tenant=tenant)
prj_b = Project.objects.create(code="PRJ-B", name="Project Beta", pm=carol, is_internal=False, tenant=tenant)
prj_c = Project.objects.create(code="PRJ-C", name="Project Charlie", pm=dave, is_internal=False, tenant=tenant)
prj_int = Project.objects.create(code="PRJ-INT", name="Internal", pm=carol, is_internal=True, tenant=tenant)
prj_sick = Project.objects.create(code="PRJ-SICK", name="Maladie", pm=carol, is_internal=True, tenant=tenant)
prj_leave = Project.objects.create(code="PRJ-LEAVE", name="Conge Vacances", pm=carol, is_internal=True, tenant=tenant)

# 6. Create phases
phase_a1 = Phase.objects.create(name="Phase A1", project=prj_a, tenant=tenant)
phase_a2 = Phase.objects.create(name="Phase A2", project=prj_a, tenant=tenant)

# 7. Self-PM project
prj_self = Project.objects.create(code="PRJ-SELF", name="Self PM Project", pm=self_pm, is_internal=False, tenant=tenant)
```

---

## 11. Test Execution Order (Recommended)

1. **Setup**: Run data setup script
2. **Employee basic flow**: TC-EMP-01 through TC-EMP-09
3. **PM approval flow**: TC-PM-01 through TC-PM-10
4. **Paie controls**: TC-PAIE-01 through TC-PAIE-09 (requires specific data per control)
5. **Paie validation**: TC-PAIE-10 through TC-PAIE-17
6. **Finance flow**: TC-FIN-01 through TC-FIN-06
7. **Admin locking**: TC-ADM-01 through TC-ADM-08
8. **Period lock lifecycle**: TC-LOCK-01 through TC-LOCK-06
9. **Cross-cutting**: TC-XCUT-01 through TC-XCUT-05

Total: **55 test scenarios** covering 6 user roles and the complete timesheet lifecycle.
