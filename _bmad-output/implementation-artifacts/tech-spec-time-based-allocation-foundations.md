---
title: 'Time-based Resource Allocation — Foundations'
slug: 'time-based-allocation-foundations'
created: '2026-04-19'
revised: '2026-04-19 (post-adversarial-review)'
status: 'ready-for-dev'
stepsCompleted: [1, 2, 3, 4, 'R']
tech_stack:
  - 'Backend: Django 5 + DRF + django-filter'
  - 'Frontend: Vue 3 (Composition API) + TypeScript + Vite'
  - 'DB: PostgreSQL (JSONField for time_breakdown and curve)'
  - 'Tests: pytest + pytest-django + APIClient'
files_to_modify:
  - 'backend/apps/planning/models.py'
  - 'backend/apps/planning/serializers.py'
  - 'backend/apps/planning/views.py'
  - 'backend/apps/planning/urls.py'
  - 'backend/apps/planning/admin.py'
  - 'backend/apps/planning/tests.py'
  - 'backend/apps/planning/migrations/ (new)'
  - 'backend/apps/projects/models.py'
  - 'backend/apps/projects/serializers.py'
  - 'backend/apps/projects/views.py (GanttViewSet task payload)'
  - 'backend/apps/projects/migrations/ (new)'
  - 'frontend/src/features/planning/api/planningApi.ts'
  - 'frontend/src/features/planning/components/PhaseSlideOver.vue'
  - 'frontend/src/features/planning/components/GanttChart.vue'
  - 'frontend/src/features/planning/components/TaskSlideOver.vue (NEW)'
code_patterns:
  - 'TenantScopedModel base class + per-request tenant filtering in get_queryset'
  - 'DRF ModelViewSet + SerializerMethodField for display-only computed fields'
  - 'DjangoFilterBackend with filterset_fields for query param filtering'
  - 'Vue 3 script setup + defineProps/defineEmits + ref/computed'
  - 'Slide-over pattern: Teleport to body, right-anchored panel, inline edit with PATCH'
  - 'Frontend API unwrap: resp.data?.data || resp.data'
test_patterns:
  - 'pytest.mark.django_db + APIClient.force_authenticate'
  - 'setup_method creates Tenant + User + ProjectRole + Project fixtures'
  - 'Model-level unit tests on @property methods and clean() validators'
  - 'Integration tests on full DRF endpoints via /api/v1/*'
---

# Tech-Spec: Time-based Resource Allocation — Foundations

**Created:** 2026-04-19
**Revised:** 2026-04-19 — integrates 14 findings from adversarial review (F1–F11, F14, F15, F18)

## Overview

### Problem Statement

Current `ResourceAllocation` records only express *who* is assigned to a phase with a *uniform* weekly-hours figure between two dates. Project managers (PM) and studio assistants cannot:
- Plan staff at the **task** level (only phase-level is possible today, and even so the `task` FK on `ResourceAllocation` is defined but unused).
- Express **non-uniform** hour distributions over time (e.g. front-loaded 40/20/10/5 or custom weekly input).
- Reuse standard load curves per phase type across projects.
- Edit start/end dates of an allocation directly in the UI (currently read-only in `PhaseSlideOver.vue`).

This blocks accurate planning, realistic load forecasting, and overload detection.

### Solution

Introduce a `distribution_mode` concept on `ResourceAllocation` with three modes (`uniform`, `standard`, `manual`), an optional `time_breakdown` JSON field for manual/standard modes, and a new tenant-scoped `PlanningStandard` catalog (load curves bound to a phase code). Add `start_date`/`end_date` to `Task`. Make allocation dates editable in `PhaseSlideOver`, create a minimal `TaskSlideOver` on the same pattern, and make task bars clickable in `GanttChart` using the task's own dates.

Sprint 1 ships the **foundations**: all backend plumbing, Uniforme fully working end-to-end, and Manuelle (week unit only) as the first advanced mode. Standard mode and month unit ship in Sprint 2.

### Scope

**In Scope:**
- Backend
  - `Task`: add nullable `start_date`, `end_date`; expose them in `TaskSerializer` and the Gantt payload.
  - `ResourceAllocation`: add `distribution_mode` (`uniform` | `standard` | `manual`), `time_unit` (`week` | `month`), `time_breakdown` (JSONField nullable), `standard` (nullable FK to `PlanningStandard`, `on_delete=SET_NULL`).
  - `ResourceAllocation.clean()`: enforce phase XOR task (exactly one).
  - `ResourceAllocation.save()`: call `full_clean()` and coerce `time_breakdown` to `None` when mode != manual.
  - `ResourceAllocation.total_planned_hours`: recompute based on `distribution_mode`; exposed through a `SerializerMethodField` (not a storage-typed field).
  - New `PlanningStandard` model (tenant-scoped, `phase_code` free CharField, `curve` JSON as normalized relative array summing to 1.0).
  - Django admin for `PlanningStandard`.
  - DRF CRUD endpoints for `PlanningStandard` + `?phase_code=` filter.
- Frontend
  - `PhaseSlideOver.vue`: allocation `start_date` / `end_date` become editable `<input type="date">`.
  - `PhaseSlideOver.vue`: segmented control for 3 modes per allocation (Uniforme / Standard / Manuelle).
  - Uniforme mode: `hours_per_week` input (already exists, wire through the new mode).
  - Manuelle mode (week only): inline mini-grid with one cell per ISO week between start/end; tab navigation; live `total_planned_hours` recalc.
  - Standard mode stub: UI slot present but selector disabled (ships in Sprint 2).
  - New `TaskSlideOver.vue`: minimal clone of `PhaseSlideOver` showing task dates + allocations list (same edition affordances).
  - `GanttChart.vue`: task bars use `task.start_date/end_date` with a fallback to the parent phase's dates; clickable to open `TaskSlideOver`.

**Out of Scope (Sprint 2+):**
- Full Standard mode UI (curve selection + application + preview).
- Month time_unit toggle in Manuelle mode.
- Inline editing on `ResourceGantt.vue` (remains display-only).
- Binding `PlanningStandard` into `ProjectTemplate.phases_config`.
- Multi-project overload/conflict detection.
- Drag & drop on Gantt.

## Context for Development

### Codebase Patterns

- **Tenant scoping**: all business models inherit `TenantScopedModel` (see `ResourceAllocation` in `backend/apps/planning/models.py:20`). `PlanningStandard` MUST follow the same pattern. `get_queryset` MUST filter on `tenant_id=self.request.tenant_id` when present.
- **Timestamps**: models gain `created_at`, `updated_at`, `tenant` via `TenantScopedModel` base (no explicit declaration needed).
- **DRF ViewSets**: one `ModelViewSet` per resource, registered in `backend/apps/planning/urls.py` via `DefaultRouter`. Filter params passed via `DjangoFilterBackend` + `filterset_fields` (see `ResourceAllocationViewSet.filterset_fields = ['employee', 'project', 'status']`). `perform_create` sets `tenant=_get_tenant(self.request)` and `created_by=self.request.user`.
- **Serializer display fields**: read-only `SerializerMethodField` for derived names (`employee_name`), `source="relation.field"` for traversal (`project_code = CharField(source="project.code", read_only=True)`).
- **Validation**: Django-side, use `clean()` at the model level for XOR rules. DRF serializer `validate()` also enforces the same rule on partial updates (PATCH) taking `self.instance` into account. `save()` overrides call `full_clean()` to prevent shell/ORM bypass of `clean()`.
- **Frontend slide-overs**: `PhaseSlideOver.vue` is the reference pattern — `Teleport to="body"` + right-anchored 450px panel + sectioned content (`.pso-section`). Local reactive state (`ref`), API calls directly via `apiClient.patch/post/delete/get`. The allocation-edit UX must match the existing `.pso-team-item` row visual language.
- **Gantt**: `GanttChart.vue:320-328` already renders task bars but they are **display-only** (no `@click`) AND they currently use `phase.start_date` / `phase.end_date` instead of `task.start_date` / `task.end_date`. Both issues are fixed in Task 24.
- **Allocation API calls**: `PhaseSlideOver.vue` currently calls `apiClient.patch('allocations/${id}/', ...)` directly (line 139). `planningApi.ts` module exists (`planningApi.updateAllocation`) but is not used by `PhaseSlideOver`. **Decision**: keep existing direct-call style in `PhaseSlideOver` for consistency with current implementation (do not refactor in this sprint). New endpoints for `PlanningStandard` MUST be added to `planningApi.ts`.
- **Frontend API unwrap**: responses wrapped — always use `const d = resp.data?.data || resp.data` then `Array.isArray(d) ? d : d?.results || []`.
- **Phase model quirk**: `Phase.phase_type` is a `TextChoices` with only 2 values (`REALIZATION` / `SUPPORT`). The **functional phase identifier** (ESQUISSE, APS, DD, CHANTIER, etc.) is `Phase.code` — a free `CharField(max_length=50)`. `PlanningStandard` matching uses `Phase.code`, not `Phase.phase_type`.

### Files to Reference

| File | Purpose |
| ---- | ------- |
| `backend/apps/planning/models.py:20-79` | `ResourceAllocation` — extend with new fields, `clean()` XOR, `save()` override |
| `backend/apps/planning/models.py` (end of file) | Add `PlanningStandard` model |
| `backend/apps/planning/serializers.py:8-32` | `ResourceAllocationSerializer` — add fields, `validate()`, `validate_time_breakdown()`; add `PlanningStandardSerializer` |
| `backend/apps/planning/views.py:29-48` | `ResourceAllocationViewSet` — extend `filterset_fields`; add `PlanningStandardViewSet` |
| `backend/apps/planning/urls.py:11-16` | Register `router.register(r"planning-standards", PlanningStandardViewSet, basename="planning-standard")` |
| `backend/apps/planning/admin.py` | Register `PlanningStandard` with `ModelAdmin` |
| `backend/apps/planning/tests.py:15-63` | Test patterns — mirror structure for `PlanningStandard` + XOR + new mode computations + ISO week helper |
| `backend/apps/projects/models.py:210-269` | `Task` — add `start_date`, `end_date` between `order` (line 244) and `budgeted_hours` (line 245) |
| `backend/apps/projects/models.py:185` | `Phase.code` — authoritative source for `phase_code` matching in `PlanningStandard` |
| `backend/apps/projects/serializers.py:57-74` | `TaskSerializer.Meta.fields` — **must be extended with `start_date`, `end_date`** (see Task 14b) |
| `backend/apps/projects/views.py` (GanttViewSet) | Task payload returned by Gantt endpoint must include `start_date`, `end_date` (see Task 14c) |
| `frontend/src/features/planning/api/planningApi.ts:3-23` | Add `listStandards`, `createStandard`, `updateStandard`, `deleteStandard` |
| `frontend/src/features/planning/components/PhaseSlideOver.vue:265-286` | Allocation rows — replace read-only period with editable date inputs; add segmented control |
| `frontend/src/features/planning/components/PhaseSlideOver.vue:171-183` | `assignEmployee` — add `distribution_mode: 'uniform'` default in payload |
| `frontend/src/features/planning/components/GanttChart.vue:320-328` | Task bars — use `task.start_date/end_date` with phase fallback; add `@click` to open `TaskSlideOver` |
| `frontend/src/features/planning/components/TaskSlideOver.vue` (NEW) | Clone minimal de `PhaseSlideOver` — sections: Dates, Allocations (with 3 modes), no budget/chart sections |

### Technical Decisions

- **Q1 — Migration data**: Existing `ResourceAllocation` rows adopt the Django field defaults (`distribution_mode='uniform'`, `time_unit='week'`, `time_breakdown=null`, `standard=null`) at the moment the new columns are added. No separate `RunPython` data-migration is required (see "Task 8 removed" note below). No user-visible behavior change.
- **Q2 — Curve storage**: `PlanningStandard.curve` is a JSON array of relative floats summing to 1.0 (normalized). Example: `[0.4, 0.3, 0.2, 0.1]` means 40% in slot 1, 30% in slot 2, etc. Rescaled to actual allocation duration at application time (Sprint 2). Validation at model level: `sum(curve) ≈ 1.0 ± 0.01`.
- **Q3 — `phase_code` (renamed from `phase_type`)**: Free `CharField(max_length=50)`. Matches `Phase.code` values (ESQUISSE, APS, DD, CHANTIER, etc.) — NOT `Phase.phase_type` (which is REALIZATION/SUPPORT).
- **Q4 — Tenancy**: `PlanningStandard` inherits `TenantScopedModel`. Each tenant curates its own catalog.
- **XOR phase/task on `ResourceAllocation`**: exactly one of `phase` or `task` must be non-null. Enforced in `ResourceAllocation.clean()` AND in `ResourceAllocationSerializer.validate()` (for PATCH partial updates). Existing rows (phase set, task null) remain valid — validated by the pre-migration DB audit in Task 0.
- **`total_planned_hours` computation**:
  - `uniform`: `total_weeks * hours_per_week` (existing logic preserved).
  - `manual`: `sum(time_breakdown.values())`, casting each to float, returning 0.0 if breakdown is empty/None/malformed.
  - `standard`: Sprint 2 — Sprint 1 returns `uniform` fallback when `standard` FK set but UI cannot yet populate `time_breakdown` from curve.
  - **Serializer exposure**: `total_planned_hours` MUST be a `SerializerMethodField` (or `ReadOnlyField`), NOT a `DecimalField`. A `DecimalField` implies an underlying DB column and breaks on `max_digits` if manual totals exceed 7 digits.
- **Manuelle grid keys**: ISO week format `"YYYY-Www"` (e.g., `"2026-W18"`). Range computed from `start_date` and `end_date` using ISO calendar. Missing keys treated as `0`. JSON keys validated by regex `^\d{4}-W(0[1-9]|[1-4]\d|5[0-3])$` (week unit) or `^\d{4}-(0[1-9]|1[0-2])$` (month unit).
- **`Task.start_date` / `Task.end_date`**: both nullable. No cascade/validation against parent `Phase` dates in Sprint 1. Gantt falls back to the parent phase's dates if task dates are missing.
- **Date ordering**: both on `Task` and on `ResourceAllocation`, when both dates are present, `end_date >= start_date` is enforced at the serializer level (`validate()`). Model-level enforcement deferred to Sprint 2 (impacts existing rows unpredictably).
- **`time_breakdown` hygiene**: `save()` on `ResourceAllocation` coerces `time_breakdown = None` when `distribution_mode != 'manual'`, preventing stale data from a previous mode toggle.
- **`PlanningStandard` orphan policy**: `ResourceAllocation.standard` is `on_delete=SET_NULL`. Deleting a `PlanningStandard` sets the FK to null on all allocations that referenced it; already-computed `time_breakdown` is preserved. Acceptable for Sprint 1 (`standard` is a stub).
- **Admin surface**: Only `PlanningStandard` gets new admin registration. `ResourceAllocation` admin may also gain new fields (`distribution_mode`, `time_unit`) in list_display if admin exists — check `admin.py` to decide.
- **No backward-compat shim**: `ResourceAllocation.task` FK already present; no rename or migration needed for it.
- **No change to existing computed endpoints**: `global_planning` and `load_alerts` continue to use `hours_per_week` as-is. Taking into account `distribution_mode='manual'` precise per-week values is a Sprint 2+ enhancement.

## Implementation Plan

### Tasks

Tasks are ordered by dependency: pre-migration audit first, then backend data model, backend API, backend tests, frontend foundations, frontend advanced UI. A dev agent should complete them in order.

#### Phase A — Backend data model

- [ ] **Task 0: Pre-migration DB audit (blocker check)** _(resolves F3)_
  - File: ad-hoc shell command, no code change.
  - Action: From `backend/`, run:
    ```bash
    python manage.py shell -c "from apps.planning.models import ResourceAllocation; \
print('no_phase_no_task=', ResourceAllocation.objects.filter(phase__isnull=True, task__isnull=True).count()); \
print('both_set=', ResourceAllocation.objects.filter(phase__isnull=False, task__isnull=False).count())"
    ```
  - Expected result: both counts equal `0`.
  - If either count > 0: **STOP**. Clean the affected rows (delete or repair the intended FK) BEFORE applying Task 4 (XOR validation) — otherwise the next `full_clean()` / `save()` on those rows will fail.
  - Notes: Run on every environment that will receive the migration (local → staging → prod).

- [ ] **Task 1: Add dates to `Task` model**
  - File: `backend/apps/projects/models.py`
  - Action: Insert two nullable `DateField`s into class `Task`, between the `order` field (line 244) and the `budgeted_hours` field (line 245):
    ```python
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    ```
  - Notes: No validation cascade with parent `Phase` dates. No change to `__str__` or `Meta`.

- [ ] **Task 2: Generate Task dates migration**
  - File: `backend/apps/projects/migrations/` (new file)
  - Action: Run `python manage.py makemigrations projects` from `backend/`. Verify the generated migration only adds `start_date` and `end_date` (no other drift).
  - Notes: Commit the generated migration file.

- [ ] **Task 3: Extend `ResourceAllocation` with distribution mode fields** _(resolves F15)_
  - File: `backend/apps/planning/models.py`
  - Action: In class `ResourceAllocation`, add the following before the `status` field (line 51):
    ```python
    class DistributionMode(models.TextChoices):
        UNIFORM = "uniform", "Uniforme"
        STANDARD = "standard", "Standard"
        MANUAL = "manual", "Manuelle"

    class TimeUnit(models.TextChoices):
        WEEK = "week", "Semaine"
        MONTH = "month", "Mois"

    distribution_mode = models.CharField(
        max_length=10,
        choices=DistributionMode.choices,
        default=DistributionMode.UNIFORM,
    )
    time_unit = models.CharField(
        max_length=10,  # F15: fits "week"/"month" with headroom for future "quarter"
        choices=TimeUnit.choices,
        default=TimeUnit.WEEK,
    )
    time_breakdown = models.JSONField(
        null=True, blank=True,
        help_text="For manual/standard modes: {\"2026-W18\": 20, ...} (week) or {\"2026-05\": 80, ...} (month)",
    )
    standard = models.ForeignKey(
        "planning.PlanningStandard",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="applied_allocations",
    )
    ```
  - Notes: `DistributionMode` and `TimeUnit` nested classes must be placed at the top of the class body (before fields). The `standard` FK targets the new model defined in Task 6 — forward reference via string is required.

- [ ] **Task 4: Implement XOR validation in `ResourceAllocation.clean()`**
  - File: `backend/apps/planning/models.py`
  - Action: Add a `clean()` method to `ResourceAllocation` (before the `__str__` method, line 67):
    ```python
    def clean(self):
        super().clean()
        from django.core.exceptions import ValidationError
        has_phase = self.phase_id is not None
        has_task = self.task_id is not None
        if has_phase == has_task:
            raise ValidationError(
                "Allocation must target exactly one of phase or task (not both, not neither)."
            )
    ```
  - Notes: Existing allocations in the database (all have phase, no task) remain valid — confirmed by Task 0.

- [ ] **Task 5: Update `total_planned_hours` + harden `save()`** _(resolves F10, F11)_
  - File: `backend/apps/planning/models.py`
  - Action A — replace the existing `total_planned_hours` property (lines 77-79) with:
    ```python
    @property
    def total_planned_hours(self):
        if self.distribution_mode == self.DistributionMode.MANUAL and self.time_breakdown:
            try:
                return float(sum(float(v) for v in self.time_breakdown.values()))
            except (TypeError, ValueError):
                return 0.0
        # uniform or standard (Sprint 1: standard falls back to uniform)
        return float(self.hours_per_week) * self.total_weeks
    ```
  - Action B — add a `save()` override immediately after `clean()`:
    ```python
    def save(self, *args, **kwargs):
        # F10: clear stale breakdown if mode changed away from manual
        if self.distribution_mode != self.DistributionMode.MANUAL:
            self.time_breakdown = None
        # F11: enforce clean() on every persistence path (ORM, admin, shell)
        self.full_clean()
        super().save(*args, **kwargs)
    ```
  - Notes: `total_weeks` property is preserved unchanged. `save()` raises `ValidationError` on invalid writes even outside DRF.

- [ ] **Task 6: Add `PlanningStandard` model**
  - File: `backend/apps/planning/models.py`
  - Action: Append at the end of the file (after `PhaseDependency`):
    ```python
    class PlanningStandard(TenantScopedModel):
        """Reusable load curve template, bound to a phase code (e.g., ESQUISSE, APS)."""

        name = models.CharField(max_length=100)
        description = models.TextField(blank=True, default="")
        phase_code = models.CharField(
            max_length=50, db_index=True,
            help_text="Matches projects.Phase.code (e.g., ESQUISSE, APS, DD, CHANTIER)",
        )
        time_unit = models.CharField(
            max_length=10,
            choices=ResourceAllocation.TimeUnit.choices,
            default=ResourceAllocation.TimeUnit.WEEK,
        )
        curve = models.JSONField(
            default=list,
            help_text="Normalized relative distribution: [0.4, 0.3, 0.2, 0.1] — sum must equal 1.0 ± 0.01",
        )
        is_active = models.BooleanField(default=True)

        class Meta:
            db_table = "planning_standard"
            ordering = ["phase_code", "name"]

        def __str__(self):
            return f"{self.name} [{self.phase_code}]"

        def clean(self):
            super().clean()
            from django.core.exceptions import ValidationError
            if not isinstance(self.curve, list) or not self.curve:
                raise ValidationError("Curve must be a non-empty list of floats.")
            try:
                total = sum(float(v) for v in self.curve)
            except (TypeError, ValueError):
                raise ValidationError("All curve values must be numeric.")
            if abs(total - 1.0) > 0.01:
                raise ValidationError(
                    f"Curve values must sum to 1.0 ± 0.01, got {total:.3f}."
                )
    ```
  - Notes: The `standard` FK added in Task 3 is resolved lazily (string reference). Declaring the FK before the model in the same module is safe.

- [ ] **Task 7: Generate allocation + standard migration**
  - File: `backend/apps/planning/migrations/` (new file)
  - Action: Run `python manage.py makemigrations planning`. Verify it creates `PlanningStandard` AND adds fields to `ResourceAllocation` in a single migration.
  - Notes: Defaults are applied by the `AddField` operation — existing rows pick up `distribution_mode='uniform'`, `time_unit='week'` automatically.

- **Task 8: REMOVED** _(resolves F4)_
  - Rationale: the previous plan included an empty `RunPython` backfill (`.filter(distribution_mode="").update(...)`) but the Django field defaults set every existing row to `'uniform'` at column-add time. The filter matches zero rows. The correctness of the migration is verified by the test in Task 17b.

#### Phase B — Backend API

- [ ] **Task 9: Update `ResourceAllocationSerializer`** _(resolves F5, F6, F14)_
  - File: `backend/apps/planning/serializers.py`
  - Action A — field declaration change (F6): replace
    ```python
    total_planned_hours = serializers.DecimalField(max_digits=8, decimal_places=1, read_only=True)
    ```
    with
    ```python
    total_planned_hours = serializers.SerializerMethodField()

    def get_total_planned_hours(self, obj):
        return obj.total_planned_hours
    ```
  - Action B — extend `Meta.fields` (line 20-27) with `"distribution_mode"`, `"time_unit"`, `"time_breakdown"`, `"standard"` between existing fields.
  - Action C — add `validate()` enforcing XOR on PATCH-aware data (F5):
    ```python
    def validate(self, attrs):
        # F5: on PATCH, attrs may omit phase/task — merge with self.instance
        has_phase_key = "phase" in attrs
        has_task_key = "task" in attrs
        phase = attrs.get("phase") if has_phase_key else getattr(self.instance, "phase", None)
        task = attrs.get("task") if has_task_key else getattr(self.instance, "task", None)
        if (phase is None) == (task is None):
            raise serializers.ValidationError(
                {"phase": "Allocation must target exactly one of phase or task."}
            )
        # Date ordering guard (F18)
        start = attrs.get("start_date", getattr(self.instance, "start_date", None))
        end = attrs.get("end_date", getattr(self.instance, "end_date", None))
        if start and end and end < start:
            raise serializers.ValidationError({"end_date": "end_date must be on or after start_date."})
        return attrs
    ```
  - Action D — add `validate_time_breakdown()` (F14):
    ```python
    import re
    _WEEK_KEY = re.compile(r"^\d{4}-W(0[1-9]|[1-4]\d|5[0-3])$")
    _MONTH_KEY = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")

    def validate_time_breakdown(self, value):
        if value in (None, {}):
            return value
        if not isinstance(value, dict):
            raise serializers.ValidationError("time_breakdown must be an object.")
        time_unit = self.initial_data.get("time_unit") or getattr(self.instance, "time_unit", "week")
        pattern = self._WEEK_KEY if time_unit == "week" else self._MONTH_KEY
        for k, v in value.items():
            if not pattern.match(str(k)):
                raise serializers.ValidationError(
                    f"Invalid key '{k}' for time_unit={time_unit}. Expected format 'YYYY-Www' or 'YYYY-MM'."
                )
            try:
                float(v)
            except (TypeError, ValueError):
                raise serializers.ValidationError(f"Value for '{k}' must be numeric.")
        return value
    ```

- [ ] **Task 10: Add `PlanningStandardSerializer`**
  - File: `backend/apps/planning/serializers.py`
  - Action: Add a new serializer at the end of the file:
    ```python
    from .models import PlanningStandard  # add to existing import

    class PlanningStandardSerializer(serializers.ModelSerializer):
        class Meta:
            model = PlanningStandard
            fields = [
                "id", "name", "description", "phase_code",
                "time_unit", "curve", "is_active",
                "created_at",
            ]
            read_only_fields = ["id", "created_at"]

        def validate_curve(self, value):
            if not isinstance(value, list) or not value:
                raise serializers.ValidationError("Curve must be a non-empty list.")
            try:
                total = sum(float(v) for v in value)
            except (TypeError, ValueError):
                raise serializers.ValidationError("All curve values must be numeric.")
            if abs(total - 1.0) > 0.01:
                raise serializers.ValidationError(
                    f"Curve values must sum to 1.0 ± 0.01 (got {total:.3f})."
                )
            return value
    ```

- [ ] **Task 11: Add `PlanningStandardViewSet`**
  - File: `backend/apps/planning/views.py`
  - Action: Add import `from .models import ..., PlanningStandard` (line 14), `from .serializers import ..., PlanningStandardSerializer`. Append a new viewset at the end of the file:
    ```python
    class PlanningStandardViewSet(viewsets.ModelViewSet):
        """CRUD for reusable load-curve standards (tenant-scoped)."""

        serializer_class = PlanningStandardSerializer
        permission_classes = [IsAuthenticated]
        filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
        filterset_fields = ["phase_code", "time_unit", "is_active"]
        ordering = ["phase_code", "name"]

        def get_queryset(self):
            qs = PlanningStandard.objects.all()
            if hasattr(self.request, "tenant_id") and self.request.tenant_id:
                qs = qs.filter(tenant_id=self.request.tenant_id)
            return qs

        def perform_create(self, serializer):
            serializer.save(tenant=_get_tenant(self.request))
    ```

- [ ] **Task 12: Update `ResourceAllocationViewSet` filter set**
  - File: `backend/apps/planning/views.py:35`
  - Action: Change `filterset_fields = ["employee", "project", "status"]` to `filterset_fields = ["employee", "project", "status", "phase", "task", "distribution_mode"]`.

- [ ] **Task 13: Register `PlanningStandard` routes**
  - File: `backend/apps/planning/urls.py`
  - Action: Import `PlanningStandardViewSet` from `.views` and add: `router.register(r"planning-standards", PlanningStandardViewSet, basename="planning-standard")` before `urlpatterns = router.urls`.

- [ ] **Task 14: Register `PlanningStandard` in Django admin**
  - File: `backend/apps/planning/admin.py`
  - Action: Register the model:
    ```python
    from django.contrib import admin
    from .models import PlanningStandard

    @admin.register(PlanningStandard)
    class PlanningStandardAdmin(admin.ModelAdmin):
        list_display = ("name", "phase_code", "time_unit", "is_active", "tenant")
        list_filter = ("phase_code", "time_unit", "is_active", "tenant")
        search_fields = ("name", "description", "phase_code")
    ```
  - Notes: If `admin.py` already has imports/registrations for other planning models, add without disrupting them.

- [ ] **Task 14b: Expose Task dates in `TaskSerializer`** _(resolves F1 — blocker)_
  - File: `backend/apps/projects/serializers.py:57-74`
  - Action: Add `"start_date"` and `"end_date"` to `TaskSerializer.Meta.fields`:
    ```python
    fields = [
        "id", "project", "phase", "phase_name", "parent",
        "wbs_code", "name", "client_facing_label", "display_label",
        "task_type", "billing_mode", "order",
        "start_date", "end_date",               # NEW
        "budgeted_hours", "budgeted_cost", "hourly_rate",
        "is_billable", "is_active", "progress_pct",
        "planned_hours", "actual_hours",
    ]
    ```
  - Action (validation): add
    ```python
    def validate(self, attrs):
        start = attrs.get("start_date", getattr(self.instance, "start_date", None))
        end = attrs.get("end_date", getattr(self.instance, "end_date", None))
        if start and end and end < start:
            raise serializers.ValidationError({"end_date": "end_date must be on or after start_date."})
        return attrs
    ```
  - Notes: Without this change, `PATCH /api/v1/tasks/{id}/` would silently drop `start_date`/`end_date` — every frontend task-date edit would be a no-op.

- [ ] **Task 14c: Expose Task dates in the Gantt payload** _(resolves F2 — blocker, part 1/3)_
  - File: `backend/apps/projects/views.py` (locate `GanttViewSet` or the Gantt endpoint that serializes tasks — usually an `@action` on `ProjectViewSet` or a standalone viewset). Search for the key that currently emits `tasks` under each phase.
  - Action: Ensure the task dict in the response includes `"start_date"` and `"end_date"` (ISO strings or null). If it is produced via a bespoke dict, add the two keys; if via a serializer, reuse the updated `TaskSerializer` (Task 14b).
  - Notes: Without this change, even with `TaskSerializer` updated, the Gantt endpoint may return tasks without dates. Confirm with `curl /api/v1/projects/{id}/gantt/ | jq '.phases[0].tasks[0]'`.

#### Phase C — Backend tests

- [ ] **Task 15: Tests for `ResourceAllocation.clean()` XOR + `save()` hardening**
  - File: `backend/apps/planning/tests.py`
  - Action: Add a new test class `TestAllocationXORValidation` following the existing `setup_method` pattern (lines 17-24). Cover:
    - phase set + task null → valid.
    - phase null + task set → valid.
    - both set → `ValidationError` (via `.full_clean()` AND via `.save()`).
    - neither set → `ValidationError`.
    - PATCH via API setting both → 400.
    - PATCH via API setting neither (unsetting phase with no task) → 400.
    - Save with `distribution_mode='uniform'` and `time_breakdown={"2026-W18": 10}` → reloaded object has `time_breakdown=None` (F10).

- [ ] **Task 16: Tests for `total_planned_hours` per mode**
  - File: `backend/apps/planning/tests.py`
  - Action: Add a test class `TestTotalPlannedHoursModes`:
    - uniform (default) → preserves existing behavior (10 weeks × 20h = 200h).
    - manual with `time_breakdown = {"2026-W18": 10, "2026-W19": 15}` → returns 25.0.
    - standard (no breakdown yet) → falls back to uniform calculation.
    - manual with empty dict / None → returns 0.0.

- [ ] **Task 17: Tests for `PlanningStandard` CRUD + tenant isolation**
  - File: `backend/apps/planning/tests.py`
  - Action: Add a test class `TestPlanningStandardAPI`:
    - create valid standard (curve sums to 1.0) → 201.
    - create invalid curve (sums to 1.5) → 400 with clear error.
    - create with non-list curve → 400.
    - GET list filtered by `phase_code=ESQUISSE` → returns only matching.
    - GET list from tenant A must NOT return tenant B standards.

- [ ] **Task 17b: Migration regression test** _(replaces deleted Task 8)_
  - File: `backend/apps/planning/tests.py`
  - Action: Add a test that creates a `ResourceAllocation` using raw SQL-ish fixtures representing the pre-migration shape (phase set, task null, no distribution_mode column), runs all migrations, then asserts `distribution_mode='uniform'`, `time_unit='week'`, and `total_planned_hours` equals the pre-migration value. Simpler alternative: in the standard `setup_method`, assert that the factory-built allocation has `distribution_mode='uniform'` by default.

- [ ] **Task 17c: ISO week helper edge cases** _(resolves F7 — week 52/01 boundary)_
  - File: `backend/apps/planning/tests.py` (or a new `tests_iso_week.py`)
  - Action: If the ISO week helper lives on the backend (it lives on the frontend in this sprint — see Task 22), add a Python unit test that calls the equivalent helper for:
    - Range `2026-12-21 → 2027-01-10` (spans week 52/53 → 01/02).
    - Range `2020-12-28 → 2021-01-03` (Monday through Sunday of ISO week 2020-W53).
    - Range `2024-01-01 → 2024-01-07` (first Monday of the year).
  - Notes: If the helper is frontend-only, add these as frontend-manual-test checklist items in the Testing Strategy section instead.

#### Phase D — Frontend foundations

- [ ] **Task 18: Extend `planningApi.ts`**
  - File: `frontend/src/features/planning/api/planningApi.ts`
  - Action: Add 4 new methods at the end of the `planningApi` object (before the closing `}`):
    ```typescript
    // Planning standards
    listStandards: (params?: Record<string, string>) => apiClient.get('planning-standards/', { params }),
    createStandard: (data: Record<string, unknown>) => apiClient.post('planning-standards/', data),
    updateStandard: (id: number, data: Record<string, unknown>) => apiClient.patch(`planning-standards/${id}/`, data),
    deleteStandard: (id: number) => apiClient.delete(`planning-standards/${id}/`),
    ```

- [ ] **Task 19: Add editable dates to allocation rows in `PhaseSlideOver.vue`** _(resolves F18)_
  - File: `frontend/src/features/planning/components/PhaseSlideOver.vue`
  - Action: Lines 266-284 (`.pso-team-item` block). Replace the read-only `<span class="pso-team-period">{{ alloc.start_date }} → {{ alloc.end_date }}</span>` with two `<input type="date">` bound to `alloc.start_date` and `alloc.end_date`, each calling `updateAllocation(alloc.id, 'start_date', ...)` or `'end_date'` on `@change`. Add minimal CSS for the new compact date inputs (reuse `.pso-input` sizing but smaller).
  - Client-side guard: before PATCH, if `end_date && start_date && end_date < start_date`, revert the local ref and show a brief inline hint (no modal). The backend also rejects the invalid combo (F18) — client guard just saves a round-trip.
  - Notes: Keep the `hours_per_week` input as-is (line 275-280).

- [ ] **Task 20: Add segmented control for distribution mode in `PhaseSlideOver.vue`**
  - File: `frontend/src/features/planning/components/PhaseSlideOver.vue`
  - Action: In the `.pso-team-item` layout, add a row below the dates row showing a 3-button segmented control: `[Uniforme] [Standard] [Manuelle]`. Wire `@click` to `updateAllocation(alloc.id, 'distribution_mode', 'uniform' | 'standard' | 'manual')`. The `Standard` button is disabled (greyed, tooltip "Bientôt disponible") in Sprint 1. Update the `AllocationData` interface (line 26-30) to include `distribution_mode: 'uniform' | 'standard' | 'manual'`, `time_unit: 'week' | 'month'`, `time_breakdown: Record<string, number> | null`.
  - Notes: Switching FROM `manual` back to `uniform` does NOT need to send `time_breakdown: null` — the backend `save()` override (Task 5, Action B) clears it automatically. Still, passing `time_breakdown: null` explicitly is harmless and keeps the client state in sync.

- [ ] **Task 21: Default `distribution_mode='uniform'` on allocation creation**
  - File: `frontend/src/features/planning/components/PhaseSlideOver.vue:171-183`
  - Action: Add `distribution_mode: 'uniform'` and `time_unit: 'week'` to the `apiClient.post('allocations/', {...})` payload.

#### Phase E — Frontend Manuelle grid + Task slide-over

- [ ] **Task 22: Implement Manuelle mini-grid (week unit)** _(resolves F7)_
  - File: `frontend/src/features/planning/components/PhaseSlideOver.vue`
  - Action: When an allocation has `distribution_mode === 'manual'`, render below the segmented control a horizontally-scrolling mini-grid: one cell per ISO week between `alloc.start_date` and `alloc.end_date`. Each cell is a small numeric input (width ~40px). On `@change`, update `alloc.time_breakdown[weekKey] = value`, then PATCH the full updated `time_breakdown` JSON via `updateAllocation(alloc.id, 'time_breakdown', alloc.time_breakdown)`. Display the live total below the grid.
  - ISO week helper pseudo-code (place in a local `utils/isoWeek.ts` or inline):
    ```typescript
    // Returns ["YYYY-Www", ...] for all ISO weeks touched by [start, end] inclusive.
    function isoWeekKey(d: Date): string {
      // ISO 8601: week 1 contains the year's first Thursday
      const dt = new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate()));
      const dayNum = dt.getUTCDay() || 7;                  // Mon=1..Sun=7
      dt.setUTCDate(dt.getUTCDate() + 4 - dayNum);         // nearest Thursday
      const yearStart = new Date(Date.UTC(dt.getUTCFullYear(), 0, 1));
      const weekNo = Math.ceil((((dt.getTime() - yearStart.getTime()) / 86400000) + 1) / 7);
      return `${dt.getUTCFullYear()}-W${String(weekNo).padStart(2, "0")}`;
    }

    export function isoWeeksBetween(startISO: string, endISO: string): string[] {
      const out: string[] = [];
      const start = new Date(startISO + "T00:00:00Z");
      const end = new Date(endISO + "T00:00:00Z");
      const cursor = new Date(start);
      let last = "";
      while (cursor <= end) {
        const key = isoWeekKey(cursor);
        if (key !== last) { out.push(key); last = key; }
        cursor.setUTCDate(cursor.getUTCDate() + 1);
      }
      return out;
    }
    ```
  - Missing keys in `time_breakdown` default to 0. Support tab navigation between cells (native browser behavior with plain `<input>` works).
  - **MUST validate** on Hostinger staging with a range spanning ISO week 52 → 01 (e.g., `2026-12-21 → 2027-01-10`). Off-by-one at year boundaries is the classic failure mode of this algorithm.

- [ ] **Task 23: Create `TaskSlideOver.vue`**
  - File: `frontend/src/features/planning/components/TaskSlideOver.vue` (NEW)
  - Action: Copy `PhaseSlideOver.vue` structure, but:
    - Props: `open: boolean`, `projectId: number`, `taskId: number | null`.
    - Load task via `GET projects/${projectId}/tasks/${taskId}/` (or whichever endpoint exists — verify in `projects/urls.py`).
    - Load allocations via `GET allocations/?project=${projectId}&task=${taskId}`.
    - Section Dates: edit `task.start_date` and `task.end_date` via `PATCH projects/${projectId}/tasks/${taskId}/`. Requires Task 14b (TaskSerializer exposes the fields).
    - Section Équipe: same allocation editing UX as `PhaseSlideOver` (dates + segmented control + Manuelle grid), but allocation payload uses `task: taskId` instead of `phase: phaseId`.
    - REMOVE: Budget section, monthly chart section (not relevant at task level in Sprint 1).
  - Notes: Reuse the scoped CSS from `PhaseSlideOver.vue` by copying the `<style>` block. Factor shared helpers (isoWeeksBetween, segmented control) into a `utils/` file if copy-paste exceeds ~80 lines.

- [ ] **Task 24: Wire clickable task bars in `GanttChart.vue`** _(resolves F2 — blocker, part 2/3 + 3/3)_
  - File: `frontend/src/features/planning/components/GanttChart.vue:320-328`
  - **Sub-task 24a (F2 — part 2/3)**: Update the `GanttTask` / task-payload TypeScript interface to add `start_date: string | null; end_date: string | null;`. Search for where the Gantt payload type is declared (likely in the same file or in `features/planning/types.ts`).
  - **Sub-task 24b (F2 — part 3/3)**: Change `barStyle(phase.start_date, phase.end_date)` to use task dates first, phase dates as fallback:
    ```vue
    :style="{
      ...barStyle(task.start_date || phase.start_date, task.end_date || phase.end_date),
      backgroundColor: '#E5E7EB'
    }"
    ```
    Also gate the `v-if` on `(task.start_date || phase.start_date) && (task.end_date || phase.end_date)`.
  - **Sub-task 24c**: Add `@click="openTaskSlideOver(task.id)"` on the `.gantt-bar-task` div. Add a reactive ref `selectedTaskId` and handlers `openTaskSlideOver(id)` / `closeTaskSlideOver()`. Import and render `<TaskSlideOver :open="taskOpen" :project-id="projectId" :task-id="selectedTaskId" @close="closeTaskSlideOver" @updated="load" />` alongside the existing `PhaseSlideOver` usage.
  - Notes: Verify `cursor: pointer` is applied to `.gantt-bar-task`. After 24c, confirm in the browser that editing `task.start_date` in `TaskSlideOver` causes the Gantt bar to resize after reload.

### Acceptance Criteria

#### Data model

- [ ] **AC 1**: Given `Task` model now has `start_date` and `end_date`, when a task is saved without dates, then the row persists and `start_date` / `end_date` are `null`.

- [ ] **AC 2**: Given a `ResourceAllocation` has `phase` set and `task` null, when `full_clean()` runs, then no `ValidationError` is raised.

- [ ] **AC 3**: Given a `ResourceAllocation` has both `phase` and `task` set, when `full_clean()` runs (or `.save()` runs via any path, including `QuerySet.create`), then a `ValidationError` with message containing "exactly one" is raised.

- [ ] **AC 4**: Given a `ResourceAllocation` has neither `phase` nor `task`, when `full_clean()` runs, then a `ValidationError` is raised.

- [ ] **AC 5**: Given a `ResourceAllocation` with `distribution_mode='uniform'`, `hours_per_week=20`, and a 10-week range, when `total_planned_hours` is read, then it returns `200.0`.

- [ ] **AC 6**: Given a `ResourceAllocation` with `distribution_mode='manual'` and `time_breakdown={"2026-W18": 10, "2026-W19": 15}`, when `total_planned_hours` is read, then it returns `25.0`.

- [ ] **AC 7**: Given a `ResourceAllocation` with `distribution_mode='standard'` but no `time_breakdown` filled yet, when `total_planned_hours` is read, then it returns the uniform fallback (Sprint 1 behavior).

- [ ] **AC 8**: Given a `PlanningStandard` is created with `curve=[0.4, 0.3, 0.2, 0.1]`, when saved, then it persists successfully.

- [ ] **AC 9**: Given a `PlanningStandard` is created with `curve=[0.5, 0.5, 0.5]` (sum=1.5), when saved, then `ValidationError` / DRF 400 is raised with an error mentioning "1.0".

- [ ] **AC 10**: Given `PlanningStandard` instances exist under Tenant A and Tenant B, when an authenticated user under Tenant A calls `GET /api/v1/planning-standards/`, then only Tenant A's standards appear in the response.

- [ ] **AC 11**: Given the existing `ResourceAllocation` rows (created before this feature), when the migration runs, then all rows have `distribution_mode='uniform'` and `time_unit='week'` and continue to compute `total_planned_hours` identically to before.

- [ ] **AC 11b (F10)**: Given an allocation is saved with `distribution_mode='uniform'` but `time_breakdown={"2026-W18": 10}`, when reloaded, then `time_breakdown` is `None`.

- [ ] **AC 11c (F11)**: Given code calls `ResourceAllocation(phase=..., task=...).save()` directly (bypassing DRF), then `ValidationError` is raised — the invalid row never reaches the database.

#### API

- [ ] **AC 12**: Given a `GET /api/v1/allocations/?phase=42` is issued, when the response is returned, then all allocations have `phase=42`.

- [ ] **AC 13**: Given a `GET /api/v1/planning-standards/?phase_code=ESQUISSE` is issued, when the response is returned, then only standards with `phase_code=ESQUISSE` appear.

- [ ] **AC 14**: Given a `POST /api/v1/allocations/` with `distribution_mode='manual'`, `time_breakdown={"2026-W18": 10}`, and valid phase, when the request is sent, then the allocation is created with status 201 and the breakdown is persisted.

- [ ] **AC 14b (F14)**: Given a `POST /api/v1/allocations/` with `time_unit='week'` and `time_breakdown={"2026-M05": 80}` (month key mismatched to week unit), when the request is sent, then a 400 with error message mentioning "Invalid key" is returned.

- [ ] **AC 14c (F1)**: Given a `PATCH /api/v1/tasks/{id}/` with `{"start_date": "2026-05-04", "end_date": "2026-05-24"}`, when the request is sent, then the response contains both dates AND a subsequent `GET` returns the new values. (Fails without Task 14b.)

- [ ] **AC 14d (F5)**: Given an existing allocation with `phase=42, task=null`, when `PATCH` is sent with body `{"distribution_mode": "manual"}` (neither phase nor task in payload), then the request succeeds — the serializer's `validate()` correctly reads `self.instance.phase`.

- [ ] **AC 14e (F18)**: Given a `PATCH /api/v1/allocations/{id}/` with `end_date` earlier than `start_date`, when sent, then a 400 is returned.

#### Frontend — PhaseSlideOver

- [ ] **AC 15**: Given a user opens `PhaseSlideOver` for a phase with 2 allocations, when the panel renders, then each allocation row shows two editable `<input type="date">` fields for start and end dates (no longer plain text).

- [ ] **AC 16**: Given the user changes an allocation's `start_date` input, when the input blurs or the date changes, then a `PATCH /api/v1/allocations/{id}/` is sent with the new `start_date`.

- [ ] **AC 17**: Given an allocation row with `distribution_mode='uniform'`, when the user clicks the `Manuelle` button in the segmented control, then `distribution_mode='manual'` is PATCHed and the Manuelle mini-grid appears below.

- [ ] **AC 18**: Given the `Standard` button in the segmented control, when the user hovers it, then a "Bientôt disponible" tooltip appears AND clicking has no effect (Sprint 1 stub).

- [ ] **AC 19**: Given an allocation in `manual` mode with dates 2026-05-04 → 2026-05-24 (3 weeks), when the Manuelle grid renders, then exactly 3 cells appear with labels like `S18`, `S19`, `S20`.

- [ ] **AC 19b (F7)**: Given an allocation in `manual` mode with dates `2026-12-21 → 2027-01-10`, when the Manuelle grid renders, then the cells are labelled (in order) `S52 S53 S01 S02` (2026-W52, 2026-W53, 2027-W01, 2027-W02), all four present, no duplicates.

- [ ] **AC 20**: Given the user types `8` into the first cell of the Manuelle grid, when the change is committed, then `time_breakdown["2026-W18"] = 8` is PATCHed on the allocation and the live total below the grid updates.

- [ ] **AC 21**: Given the user adds a new employee via the assign form, when the allocation is created, then the payload includes `distribution_mode: 'uniform'` and `time_unit: 'week'`.

#### Frontend — TaskSlideOver + GanttChart

- [ ] **AC 22**: Given a task bar is rendered in the Gantt with `showTasks=true`, when the user clicks the bar, then `TaskSlideOver` opens for that task.

- [ ] **AC 22b (F2)**: Given a task has `start_date=2026-05-04, end_date=2026-05-10` and its parent phase has `start_date=2026-04-01, end_date=2026-06-30`, when the Gantt renders the task bar, then the bar uses the task's dates (narrower bar), not the phase's.

- [ ] **AC 22c (F2)**: Given a task has no dates set but its parent phase has dates, when the Gantt renders, then the task bar uses the phase's dates as a fallback (existing behavior preserved).

- [ ] **AC 23**: Given `TaskSlideOver` is open for a task with no prior allocations, when the user assigns a new employee, then the created allocation has `task={taskId}` and `phase=null`.

- [ ] **AC 24**: Given `TaskSlideOver` is open, when the user edits the task's start/end dates, then a `PATCH projects/{projectId}/tasks/{taskId}/` is sent and the slide-over reloads with updated dates.

- [ ] **AC 25**: Given `TaskSlideOver` is open, when the user views the panel, then the Budget section and monthly chart are NOT displayed (these remain phase-level concerns).

## Additional Context

### Dependencies

**External libraries**: none new (all features implementable with existing stack).

**Backend**:
- Django 5, DRF, django-filter — already installed.
- PostgreSQL `jsonb` column type for `time_breakdown` and `curve` — already used elsewhere (`ProjectTemplate.phases_config`).

**Frontend**:
- Native `<input type="date">` — no datepicker library.
- ISO week helper: 15-20 lines of JS, no library (Thursday-of-the-week method — see Task 22 pseudo-code).
- No new Vue dependencies.

**Internal dependencies**:
- Existing `TenantScopedModel` base — used as-is.
- Existing tenant middleware (`request.tenant_id`) — relied upon.
- Existing user search endpoint `/api/v1/users/search/` — used by `PhaseSlideOver` assign flow, reused as-is.

### Testing Strategy

**Backend — pytest**:
- **Unit (model layer)**:
  - `ResourceAllocation.clean()` — 4 XOR cases.
  - `ResourceAllocation.save()` — both-set via direct `.save()` raises; mode change clears `time_breakdown`.
  - `ResourceAllocation.total_planned_hours` — uniform / manual / standard / empty manual.
  - `PlanningStandard.clean()` — 3 curve validation cases (valid, wrong sum, non-list, non-numeric).
- **Integration (DRF)**:
  - `POST /api/v1/allocations/` with each mode + serializer-level XOR + `time_breakdown` key regex + date ordering.
  - `PATCH /api/v1/allocations/{id}/` with body missing phase/task — `self.instance` correctly consulted (AC 14d).
  - `PATCH /api/v1/tasks/{id}/` with dates — round-trip (AC 14c).
  - `GET /api/v1/allocations/?phase=X&task=Y&distribution_mode=manual` filters.
  - `POST/GET /api/v1/planning-standards/` + `?phase_code=` filter + tenant isolation (2 tenants).
- **Migration**:
  - Run `python manage.py migrate` on a DB with 1-2 pre-existing allocations, assert `distribution_mode='uniform'` after migration (Task 17b).

**Frontend — manual testing on Hostinger staging** (aligned with the iterative UX process, memory ref: `feedback_ux_process`):
1. Open a project, open a phase via Gantt click → `PhaseSlideOver`.
2. Edit an existing allocation's start date → verify network PATCH + reload.
3. Toggle to Manuelle mode → verify grid appears with correct number of weeks.
4. Type values in the grid → verify total updates and PATCH is sent.
5. Toggle back to Uniforme → verify `time_breakdown` is null on reload (backend cleared it).
6. **ISO week 52/01 boundary**: create an allocation spanning `2026-12-21 → 2027-01-10`, toggle to Manuelle, verify 4 cells `S52 S53 S01 S02`.
7. Click a task bar in the Gantt → verify `TaskSlideOver` opens.
8. Edit the task's dates in `TaskSlideOver` → verify Gantt bar resizes after reload (AC 22b).
9. Task with no dates → verify Gantt bar uses phase dates (AC 22c).
10. Assign an employee at task level → verify allocation appears with `task` set.
11. Switch to Django admin → create a `PlanningStandard` → verify it persists and is visible only in current tenant.

**Frontend — automated tests**: deferred to a later QA pass (no Vue component test framework currently in use).

### Notes

**High-risk items**:
- **Migration ordering**: Task 3 adds a forward-reference FK to `PlanningStandard` (string `"planning.PlanningStandard"`), and Task 6 declares the model. Django resolves string references lazily, so declaring the FK before the model in the same module is safe. `makemigrations` must run AFTER both edits are saved.
- **XOR validation enforcement**: model `clean()` + `save()` override (Task 5B) + serializer `validate()` (Task 9C) triple-gate the rule. Any of these alone is insufficient; together they cover DRF, admin, ORM, and shell paths.
- **ISO week arithmetic**: JS `Date` doesn't have native ISO week support. The algorithm in Task 22 is the standard Thursday method. **Mandatory manual test** on the 52/53 → 01 boundary before declaring the Manuelle grid done.
- **Pre-migration audit (Task 0)**: must be run on every environment. Silently-invalid rows would crash production on the first `save()` after deploy.

**Known limitations**:
- Standard mode in Sprint 1 is a stub: the button is present but disabled in the UI. Full selection + curve application ships in Sprint 2.
- `time_unit='month'` is supported at the model level but has no UI surface in Sprint 1 (Manuelle grid is week-only). `validate_time_breakdown` still accepts month keys for API-direct callers.
- `ResourceGantt.vue` remains display-only. Inline editing from the global view is Sprint 2+.
- No conflict detection if a person is over-allocated across multiple projects; existing `load_alerts` endpoint still uses `hours_per_week` aggregation (does not yet consider `time_breakdown`).
- Admin surface for `PlanningStandard` is basic (Django admin only); no dedicated Vue CRUD screen in Sprint 1.
- `PlanningStandard` deletion uses `on_delete=SET_NULL`. Allocations that referenced it keep their already-filled `time_breakdown` but lose the link to the original curve (acceptable while `standard` is a stub; revisit when Sprint 2 activates standard-mode UX).
- Date ordering (`end_date >= start_date`) is enforced at the DRF serializer layer, not at the DB or model `clean()`. Rows created via shell or raw SQL can violate this invariant — acceptable for Sprint 1, revisit when data quality issues arise.

**Future considerations (out of scope, worth noting)**:
- Sprint 2: full Standard mode UX (curve preview, rescale to allocation duration, write to `time_breakdown`).
- Sprint 2: month toggle in Manuelle grid.
- Sprint 2: `ResourceGantt` inline editing (assistante de studio workflow).
- Sprint 3+: binding `PlanningStandard` IDs into `ProjectTemplate.phases_config` so a new project auto-proposes curves per phase.
- Sprint 3+: multi-project overload detection using `time_breakdown` precise values.
- Sprint 3+: drag & drop on Gantt bars to edit dates visually.

**UX deployment**: changes will be tested on Philippe's Hostinger staging per the project's iterative UX feedback loop. User feedback may reshape Sprint 2 priorities.

### Adversarial Review — Changes Log (2026-04-19)

14 findings from the `R` review are integrated into this revision:

| # | Severity | Summary | Addressed in |
|---|---|---|---|
| F1 | Critical | `TaskSerializer.fields` missing `start_date`/`end_date` | Task 14b + AC 14c |
| F2 | Critical | Gantt bars use phase dates, not task dates | Task 14c + Task 24a/24b + AC 22b/22c |
| F3 | Critical | No pre-migration audit for XOR compatibility | Task 0 |
| F4 | Critical | Task 8 data migration matched zero rows | Task 8 removed, replaced by Task 17b |
| F5 | High | Serializer `validate()` XOR wrong on PATCH | Task 9C + AC 14d |
| F6 | High | `total_planned_hours` typed as `DecimalField` | Task 9A |
| F7 | High | ISO week algorithm risk at 52/01 boundary | Task 22 pseudo-code + AC 19b + Task 17c |
| F8 | High | No regex for `time_breakdown` keys | Technical Decisions + Task 9D |
| F9 | Medium | `PlanningStandard` orphan policy undocumented | Technical Decisions + Known limitations |
| F10 | High | `time_breakdown` not cleared on mode toggle | Task 5 (Action B) + AC 11b |
| F11 | High | `clean()` bypassable via `.create()` / raw save | Task 5 (Action B) + AC 11c |
| F14 | High | No `validate_time_breakdown` serializer | Task 9D + AC 14b |
| F15 | Medium | `time_unit` `max_length=5` too tight | Task 3 (`max_length=10`) |
| F18 | Medium | No `end_date >= start_date` check | Task 9C + Task 14b + AC 14e + Known limitations |

Findings not addressed (tracked for Sprint 2): F12 (backend ISO week helper reuse), F13 (Gantt memoization), F16 (admin list_display for ResourceAllocation), F17 (bulk PATCH for time_breakdown), F19 (Django check framework for migration safety), F20 (tenant-scoped tests for planning standards UI surface), F21–F25 (UX polish on segmented control, accessibility audit, keyboard nav on Manuelle grid, Gantt bar focus ring, mobile layout).
