"""Project serializers."""

from rest_framework import serializers

from apps.core.mixins import OptimisticLockMixin
from apps.core.serializer_mixins import CostFieldFilterMixin

from .models import (
    Amendment,
    FinancialPhase,
    Phase,
    Project,
    ProjectTemplate,
    StandardPhase,
    SupportService,
    Task,
)


def _chargeable_tasks(phase):
    """Tâches *saisissables* d'une phase : celles sans sous-tâche (feuilles).

    Le budget, les heures planifiées et réelles vivent uniquement sur ces
    nœuds ; les tâches-mères ne font qu'agréger leurs sous-tâches. Filtrer
    ici évite tout double-comptage Phase ⇇ mère ⇇ sous-tâche.
    """
    return phase.tasks.filter(subtasks__isnull=True)


def compute_phase_aggregates(phases):
    """Agrégats de TOUTES les phases en un nombre BORNÉ de requêtes (anti N+1).

    Retourne ``{phase_id: {...}}``. À injecter dans le contexte du
    ``PhaseSerializer`` (clé ``phase_aggregates``) ; sinon chaque phase
    recalcule ses agrégats à l'unité (repli).
    """
    from django.db.models import Count, Max, Min, Sum

    ids = [p.id for p in phases]
    out = {
        pid: {
            "tasks_budgeted_hours": 0.0, "tasks_budgeted_cost": 0.0,
            "task_count": 0, "tasks_start_date": None, "tasks_end_date": None,
            "actual_hours": 0.0, "planned_hours": 0.0,
        }
        for pid in ids
    }
    if not ids:
        return out
    # Budget : tâches saisissables (feuilles)
    for r in (
        Task.objects.filter(phase_id__in=ids, subtasks__isnull=True)
        .values("phase_id").annotate(bh=Sum("budgeted_hours"), bc=Sum("budgeted_cost"))
    ):
        out[r["phase_id"]]["tasks_budgeted_hours"] = float(r["bh"] or 0)
        out[r["phase_id"]]["tasks_budgeted_cost"] = float(r["bc"] or 0)
    # Count + dates : toutes les tâches
    for r in (
        Task.objects.filter(phase_id__in=ids)
        .values("phase_id").annotate(c=Count("id"), smin=Min("start_date"), emax=Max("end_date"))
    ):
        out[r["phase_id"]]["task_count"] = r["c"]
        out[r["phase_id"]]["tasks_start_date"] = r["smin"].isoformat() if r["smin"] else None
        out[r["phase_id"]]["tasks_end_date"] = r["emax"].isoformat() if r["emax"] else None
    # Heures réelles (saisies sur les tâches)
    from apps.time_entries.models import TimeEntry
    for r in (
        TimeEntry.objects.filter(task__phase_id__in=ids)
        .values("task__phase_id").annotate(s=Sum("hours"))
    ):
        out[r["task__phase_id"]]["actual_hours"] = float(r["s"] or 0)
    # Heures planifiées (total_planned_hours = propriété Python → 1 requête + boucle mémoire)
    from apps.planning.models import ResourceAllocation
    for a in ResourceAllocation.objects.filter(
        task__phase_id__in=ids, status="ACTIVE"
    ).select_related("task"):
        out[a.task.phase_id]["planned_hours"] += a.total_planned_hours
    return out


class PhaseSerializer(CostFieldFilterMixin, serializers.ModelSerializer):
    tasks_budgeted_hours = serializers.SerializerMethodField()
    tasks_budgeted_cost = serializers.SerializerMethodField()
    planned_hours = serializers.SerializerMethodField()
    actual_hours = serializers.SerializerMethodField()
    has_tasks = serializers.SerializerMethodField()
    task_count = serializers.SerializerMethodField()
    tasks_start_date = serializers.SerializerMethodField()
    tasks_end_date = serializers.SerializerMethodField()
    amendment_number = serializers.IntegerField(
        source="amendment.amendment_number", read_only=True, default=None
    )

    class Meta:
        model = Phase
        fields = [
            "id", "code", "name", "client_facing_label", "phase_type",
            "billing_mode", "order", "start_date", "end_date",
            "tasks_start_date", "tasks_end_date",
            "is_mandatory", "is_locked", "budgeted_hours", "budgeted_cost",
            "tasks_budgeted_hours", "tasks_budgeted_cost",
            "planned_hours", "actual_hours", "has_tasks", "task_count",
            "amendment", "amendment_number",
        ]
        read_only_fields = ["id", "amendment_number"]

    def _agg(self, obj):
        """Agrégats pré-calculés en bloc (anti N+1), si fournis dans le contexte."""
        return (self.context.get("phase_aggregates") or {}).get(obj.id)

    def get_tasks_start_date(self, obj):
        """Date de début la plus tôt parmi les tâches/sous-tâches de la phase."""
        a = self._agg(obj)
        if a is not None:
            return a["tasks_start_date"]
        from django.db.models import Min
        d = obj.tasks.aggregate(d=Min("start_date"))["d"]
        return d.isoformat() if d else None

    def get_tasks_end_date(self, obj):
        """Date de fin la plus tardive parmi les tâches/sous-tâches de la phase."""
        a = self._agg(obj)
        if a is not None:
            return a["tasks_end_date"]
        from django.db.models import Max
        d = obj.tasks.aggregate(d=Max("end_date"))["d"]
        return d.isoformat() if d else None

    def get_tasks_budgeted_hours(self, obj):
        """Σ des heures budgétées des tâches saisissables (feuilles)."""
        a = self._agg(obj)
        if a is not None:
            return a["tasks_budgeted_hours"]
        from django.db.models import Sum
        total = _chargeable_tasks(obj).aggregate(s=Sum("budgeted_hours"))["s"]
        return float(total) if total else 0

    def get_tasks_budgeted_cost(self, obj):
        """Σ des coûts budgétés des tâches saisissables (feuilles)."""
        a = self._agg(obj)
        if a is not None:
            return a["tasks_budgeted_cost"]
        from django.db.models import Sum
        total = _chargeable_tasks(obj).aggregate(s=Sum("budgeted_cost"))["s"]
        return float(total) if total else 0

    def get_planned_hours(self, obj):
        """Σ des heures planifiées des allocations posées sur les tâches."""
        a = self._agg(obj)
        if a is not None:
            return a["planned_hours"]
        from apps.planning.models import ResourceAllocation
        total = 0
        for alloc in ResourceAllocation.objects.filter(
            task__phase=obj, status="ACTIVE"
        ):
            total += alloc.total_planned_hours
        return total

    def get_actual_hours(self, obj):
        """Σ des heures réelles saisies sur les tâches de la phase."""
        a = self._agg(obj)
        if a is not None:
            return a["actual_hours"]
        from django.db.models import Sum
        from apps.time_entries.models import TimeEntry
        total = TimeEntry.objects.filter(task__phase=obj).aggregate(s=Sum("hours"))["s"]
        return float(total) if total else 0

    def get_has_tasks(self, obj):
        a = self._agg(obj)
        if a is not None:
            return a["task_count"] > 0
        return obj.tasks.exists()

    def get_task_count(self, obj):
        a = self._agg(obj)
        if a is not None:
            return a["task_count"]
        return obj.tasks.count()


class TaskSerializer(CostFieldFilterMixin, serializers.ModelSerializer):
    phase_name = serializers.CharField(source="phase.name", read_only=True)
    display_label = serializers.SerializerMethodField()
    planned_hours = serializers.SerializerMethodField()
    actual_hours = serializers.SerializerMethodField()
    is_chargeable = serializers.SerializerMethodField()
    effective_budgeted_hours = serializers.SerializerMethodField()
    effective_budgeted_cost = serializers.SerializerMethodField()
    wbs_code = serializers.CharField(max_length=20, required=False, allow_blank=True, default="")
    amendment_number = serializers.IntegerField(
        source="amendment.amendment_number", read_only=True, default=None
    )

    class Meta:
        model = Task
        fields = [
            "id", "project", "phase", "phase_name", "parent",
            "wbs_code", "name", "client_facing_label", "display_label",
            "task_type", "billing_mode", "order",
            "start_date", "end_date",
            "budgeted_hours", "budgeted_cost", "hourly_rate",
            "effective_budgeted_hours", "effective_budgeted_cost", "is_chargeable",
            "is_billable", "is_active", "always_display_in_timesheet",
            "progress_pct",
            "planned_hours", "actual_hours",
            "amendment", "amendment_number",
        ]
        read_only_fields = [
            "id", "display_label", "phase_name", "planned_hours", "actual_hours",
            "is_chargeable", "effective_budgeted_hours", "effective_budgeted_cost",
            "amendment_number",
        ]

    def get_display_label(self, obj):
        return obj.client_facing_label or obj.name

    def get_is_chargeable(self, obj):
        """True si la tâche est saisissable (aucune sous-tâche)."""
        return not obj.subtasks.exists()

    def get_effective_budgeted_hours(self, obj):
        """Budget heures : propre si saisissable, sinon Σ des sous-tâches."""
        from django.db.models import Sum
        if self.get_is_chargeable(obj):
            return float(obj.budgeted_hours or 0)
        total = obj.subtasks.aggregate(s=Sum("budgeted_hours"))["s"]
        return float(total) if total else 0

    def get_effective_budgeted_cost(self, obj):
        """Budget coût : propre si saisissable, sinon Σ des sous-tâches."""
        from django.db.models import Sum
        if self.get_is_chargeable(obj):
            return float(obj.budgeted_cost or 0)
        total = obj.subtasks.aggregate(s=Sum("budgeted_cost"))["s"]
        return float(total) if total else 0

    def validate(self, attrs):
        start = attrs.get("start_date", getattr(self.instance, "start_date", None))
        end = attrs.get("end_date", getattr(self.instance, "end_date", None))
        if start and end and end < start:
            raise serializers.ValidationError(
                {"end_date": "end_date must be on or after start_date."}
            )
        return attrs

    def get_planned_hours(self, obj):
        """Heures planifiées : propres si saisissable, sinon Σ des sous-tâches."""
        from apps.planning.models import ResourceAllocation
        if self.get_is_chargeable(obj):
            qs = obj.resource_allocations.filter(status="ACTIVE")
        else:
            qs = ResourceAllocation.objects.filter(task__parent=obj, status="ACTIVE")
        return sum(alloc.total_planned_hours for alloc in qs)

    def get_actual_hours(self, obj):
        """Heures réelles : propres si saisissable, sinon Σ des sous-tâches."""
        from django.db.models import Sum
        from apps.time_entries.models import TimeEntry
        if self.get_is_chargeable(obj):
            qs = TimeEntry.objects.filter(task=obj)
        else:
            qs = TimeEntry.objects.filter(task__parent=obj)
        total = qs.aggregate(s=Sum("hours"))["s"]
        return float(total) if total else 0


class SupportServiceSerializer(CostFieldFilterMixin, serializers.ModelSerializer):
    class Meta:
        model = SupportService
        fields = [
            "id", "code", "name", "client_facing_label",
            "budgeted_hours", "budgeted_cost", "billing_mode", "is_billable",
        ]
        read_only_fields = ["id"]


class StandardPhaseSerializer(serializers.ModelSerializer):
    """Jeu global de phases standard (paramétrage admin)."""

    class Meta:
        model = StandardPhase
        fields = [
            "id", "code", "name", "client_facing_label",
            "phase_type", "order", "is_mandatory", "is_active",
        ]
        read_only_fields = ["id"]


class ProjectSerializer(CostFieldFilterMixin, OptimisticLockMixin, serializers.ModelSerializer):
    phases = PhaseSerializer(many=True, read_only=True)
    support_services = SupportServiceSerializer(many=True, read_only=True)
    client_name = serializers.CharField(source="client.name", read_only=True, default="")
    consortium_name = serializers.CharField(source="consortium.name", read_only=True, default="")
    team_members = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    team_members_detail = serializers.SerializerMethodField()

    def get_team_members_detail(self, obj):
        """Team members as ``[{id, name}]`` — membership is managed via the
        dedicated ``members`` action, not this serializer."""
        members = []
        for user in obj.team_members.all():
            name = user.get_full_name().strip() or user.username
            members.append({"id": user.pk, "name": name})
        return members

    class Meta:
        model = Project
        fields = [
            "id", "code", "name", "client", "client_name", "template", "contract_type",
            "status", "is_internal", "is_public", "is_consortium", "consortium", "consortium_name",
            "services_transversaux", "business_unit", "legal_entity",
            "start_date", "end_date", "construction_cost",
            "address", "city", "postal_code", "country",
            "surface", "surface_unit", "currency", "tags", "title_on_invoice",
            "pm", "associate_in_charge", "invoice_approver", "bu_director",
            "team_members", "team_members_detail",
            "total_fees", "fee_calculation_method", "fee_rate_pct",
            "version", "phases", "support_services",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class ProjectListSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source="client.name", read_only=True, default="")
    pm_name = serializers.SerializerMethodField()
    active_phase = serializers.SerializerMethodField()
    budget_hours = serializers.SerializerMethodField()
    total_invoiced = serializers.SerializerMethodField()

    def get_pm_name(self, obj):
        if obj.pm:
            name = obj.pm.get_full_name()
            return name if name.strip() else obj.pm.username
        return ""

    def get_active_phase(self, obj):
        """Return the first non-locked realization phase name."""
        phase = obj.phases.filter(
            phase_type="REALIZATION", is_locked=False
        ).order_by("order").first()
        return phase.name if phase else ""

    def get_budget_hours(self, obj):
        """Sum of budgeted hours across all tasks (or phases if no tasks)."""
        from django.db.models import Sum
        total = obj.tasks.aggregate(s=Sum("budgeted_hours"))["s"]
        if total:
            return float(total)
        total = obj.phases.aggregate(s=Sum("budgeted_hours"))["s"]
        return float(total) if total else 0

    def get_total_invoiced(self, obj):
        """Sum of approved/sent/paid invoice amounts."""
        from django.db.models import Sum
        from apps.billing.models import Invoice
        total = Invoice.objects.filter(
            project=obj, status__in=["APPROVED", "SENT", "PAID"]
        ).aggregate(s=Sum("total_amount"))["s"]
        return float(total) if total else 0

    class Meta:
        model = Project
        fields = [
            "id", "code", "name", "client", "client_name",
            "contract_type", "status", "is_internal", "is_public", "is_consortium",
            "business_unit", "pm", "pm_name",
            "active_phase", "budget_hours", "total_invoiced",
            "start_date", "end_date", "created_at",
        ]


class ProjectTemplateSerializer(serializers.ModelSerializer):
    projects_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = ProjectTemplate
        fields = [
            "id", "name", "code", "contract_type", "description",
            "is_active", "phases_config", "support_services_config",
            "projects_count",
        ]
        read_only_fields = ["id", "projects_count"]


class AmendmentSerializer(OptimisticLockMixin, serializers.ModelSerializer):
    class Meta:
        model = Amendment
        fields = [
            "id", "amendment_number", "description", "status",
            "budget_impact", "requested_by", "approved_by", "approval_date",
            "version", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "amendment_number", "requested_by", "approved_by", "approval_date", "created_at", "updated_at"]


class FinancialPhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialPhase
        fields = [
            "id", "name", "code", "billing_mode",
            "fixed_amount", "hourly_budget_max",
        ]
        read_only_fields = ["id"]


