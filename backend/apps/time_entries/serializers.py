"""Time entry serializers."""

from rest_framework import serializers

from apps.core.mixins import OptimisticLockMixin

from .models import (
    PeriodUnlock,
    TimeEntry,
    TimeEntryBlock,
    TimesheetLock,
    WeeklyApproval,
)


class TimeEntrySerializer(OptimisticLockMixin, serializers.ModelSerializer):
    """TimeEntry with nested project/phase names for grid display."""

    employee_name = serializers.SerializerMethodField()
    project_code = serializers.CharField(source="project.code", read_only=True)
    project_name = serializers.CharField(source="project.name", read_only=True)
    phase_name = serializers.SerializerMethodField()
    client_label = serializers.SerializerMethodField()
    task_wbs_code = serializers.CharField(source="task.wbs_code", read_only=True, default="")
    task_name = serializers.SerializerMethodField()
    task_parent_name = serializers.SerializerMethodField()
    task_is_billable = serializers.SerializerMethodField()

    class Meta:
        model = TimeEntry
        fields = [
            "id", "employee", "employee_name", "project", "project_code", "project_name",
            "phase", "phase_name", "task", "task_wbs_code", "task_name",
            "task_parent_name", "task_is_billable",
            "client_label",
            "date", "hours", "notes", "rejection_reason", "status", "is_favorite",
            "is_invoiced", "version",
            "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "employee", "employee_name", "project_code", "project_name",
            "phase_name", "task_wbs_code", "task_name",
            "task_parent_name", "task_is_billable",
            "client_label", "rejection_reason", "is_invoiced",
            "created_at", "updated_at",
        ]

    def get_employee_name(self, obj):
        if obj.employee:
            name = f"{obj.employee.first_name} {obj.employee.last_name}".strip()
            return name or obj.employee.username
        return ""

    def get_phase_name(self, obj):
        if obj.phase:
            return obj.phase.name
        return ""

    def get_client_label(self, obj):
        # Prefer task label, fallback to phase
        if obj.task:
            return obj.task.client_facing_label or obj.task.name
        if obj.phase:
            return obj.phase.client_facing_label or obj.phase.name
        return ""

    def get_task_name(self, obj):
        if obj.task:
            return obj.task.client_facing_label or obj.task.name
        return ""

    def get_task_parent_name(self, obj) -> str:
        """Référentiel d'une sous-tâche : libellé (client) de sa tâche-mère."""
        parent = obj.task.parent if obj.task and obj.task.parent_id else None
        if not parent:
            return ""
        return parent.client_facing_label or parent.name

    def get_task_is_billable(self, obj):
        """Caractère facturable de la tâche (badge $ dans la grille)."""
        return obj.task.is_billable if obj.task else None

    def validate_hours(self, value):
        """Reject negative hours and absurd values >24h/day."""
        if value is None:
            return value
        if value < 0:
            raise serializers.ValidationError("Les heures ne peuvent pas etre negatives.")
        if value > 24:
            raise serializers.ValidationError("Les heures ne peuvent pas depasser 24h sur une journee.")
        return value

    def validate(self, attrs):
        """La saisie se fait sur une tâche **saisissable** (feuille) et **ouverte**.

        On refuse :
        - une tâche-mère (regroupement de sous-tâches) → choisir une sous-tâche ;
        - une tâche **fermée** (``is_active=False``) → plus d'imputation possible.
        """
        task = attrs.get("task") or getattr(self.instance, "task", None)
        if task is not None and task.subtasks.exists():
            raise serializers.ValidationError({
                "task": "Saisie impossible sur une tâche-mère (regroupement) — "
                        "choisir une sous-tâche.",
            })
        if task is not None and not task.is_active:
            raise serializers.ValidationError({
                "task": "Saisie impossible : cette tâche est fermée.",
            })
        if task is not None:
            employee = getattr(self.instance, "employee", None)
            if employee is None:
                request = (self.context or {}).get("request")
                employee = getattr(request, "user", None) if request else None
            employee_id = getattr(employee, "pk", None)
            if employee_id and TimeEntryBlock.blocks(employee_id, task):
                raise serializers.ValidationError({
                    "task": "Saisie bloquée : vous n'êtes pas autorisé à "
                            "imputer du temps sur cette tâche.",
                })
        return attrs


class WeeklyApprovalSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()

    class Meta:
        model = WeeklyApproval
        fields = [
            "id", "employee", "employee_name", "week_start", "week_end",
            "pm_status", "pm_approved_by", "pm_approved_at",
            "finance_status", "finance_approved_by", "finance_approved_at",
            "paie_status", "paie_validated_by", "paie_validated_at",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_employee_name(self, obj):
        u = obj.employee
        full = f"{u.first_name} {u.last_name}".strip()
        return full or u.email


class TimesheetLockSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source="project.name", read_only=True)
    project_code = serializers.CharField(source="project.code", read_only=True)
    phase_name = serializers.SerializerMethodField()
    locked_by_name = serializers.SerializerMethodField()

    class Meta:
        model = TimesheetLock
        fields = [
            "id", "project", "project_name", "project_code",
            "phase", "phase_name",
            "person", "lock_type",
            "locked_by", "locked_by_name", "locked_at",
        ]
        read_only_fields = ["id", "locked_at", "project_name", "project_code", "phase_name", "locked_by_name"]

    def get_phase_name(self, obj):
        if obj.phase:
            return obj.phase.name
        return ""

    def get_locked_by_name(self, obj):
        if obj.locked_by:
            full = f"{obj.locked_by.first_name} {obj.locked_by.last_name}".strip()
            return full or obj.locked_by.email
        return ""


class PeriodUnlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodUnlock
        fields = [
            "id", "period_start", "period_end", "reason",
            "justification", "unlocked_by", "unlocked_at",
        ]
        read_only_fields = ["id", "unlocked_at"]


class TimeEntryBlockSerializer(serializers.ModelSerializer):
    """Blocage de saisie d'un employé sur une tâche (ou une phase entière)."""

    employee_name = serializers.SerializerMethodField()
    phase_name = serializers.CharField(source="phase.name", read_only=True, default="")
    task_name = serializers.CharField(source="task.name", read_only=True, default="")
    task_wbs_code = serializers.CharField(
        source="task.wbs_code", read_only=True, default=""
    )

    class Meta:
        model = TimeEntryBlock
        fields = [
            "id", "project", "employee", "employee_name",
            "phase", "phase_name", "task", "task_name", "task_wbs_code",
            "reason", "created_by", "created_at",
        ]
        read_only_fields = ["id", "created_by", "created_at"]

    def get_employee_name(self, obj):
        u = obj.employee
        full = f"{u.first_name} {u.last_name}".strip()
        return full or u.username

    def validate(self, attrs):
        """Cible une tâche, une phase, ou **aucune** (= projet entier). On
        interdit seulement « phase ET tâche » simultanément."""
        phase = attrs.get("phase") if "phase" in attrs else getattr(self.instance, "phase", None)
        task = attrs.get("task") if "task" in attrs else getattr(self.instance, "task", None)
        if phase is not None and task is not None:
            raise serializers.ValidationError(
                "Un blocage cible une phase OU une tâche, pas les deux."
            )
        return attrs
