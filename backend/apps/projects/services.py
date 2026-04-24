"""Project business logic services."""

from django.db import transaction
from django.utils import timezone

from apps.core.models import ProjectRole, Role, Tenant

from .models import Amendment, Phase, Project, ProjectTemplate, SupportService, Task


class AmendmentTransitionError(Exception):
    """Raised when an amendment state transition is not allowed."""


_ALLOWED_TRANSITIONS = {
    Amendment.AmendmentStatus.DRAFT: {Amendment.AmendmentStatus.SUBMITTED},
    Amendment.AmendmentStatus.SUBMITTED: {
        Amendment.AmendmentStatus.APPROVED,
        Amendment.AmendmentStatus.REJECTED,
    },
    Amendment.AmendmentStatus.APPROVED: set(),
    Amendment.AmendmentStatus.REJECTED: set(),
}


def _assert_transition(amendment, target):
    if target not in _ALLOWED_TRANSITIONS.get(amendment.status, set()):
        raise AmendmentTransitionError(
            f"Transition de '{amendment.status}' vers '{target}' non autorisée."
        )


def _is_project_director(user, tenant):
    """True if ``user`` holds PROJECT_DIRECTOR role on the tenant."""
    if user is None or not user.is_authenticated:
        return False
    return ProjectRole.objects.filter(
        user=user,
        tenant=tenant,
        role=Role.PROJECT_DIRECTOR,
    ).exists()


@transaction.atomic
def submit_amendment(amendment, *, actor):
    """DRAFT → SUBMITTED. Any authenticated actor.

    Used by PM / Assistante / Finance to push an amendment to the Associé en charge
    for approval.
    """
    _assert_transition(amendment, Amendment.AmendmentStatus.SUBMITTED)
    amendment.status = Amendment.AmendmentStatus.SUBMITTED
    amendment._history_user = actor  # captured by HistoricalRecords
    amendment.save(update_fields=["status", "version", "updated_at"])
    return amendment


@transaction.atomic
def approve_amendment(amendment, *, actor):
    """SUBMITTED → APPROVED. Only PROJECT_DIRECTOR (Associé en charge)."""
    if not _is_project_director(actor, amendment.tenant):
        raise PermissionError("Seul un Associé en charge peut approuver un avenant.")
    _assert_transition(amendment, Amendment.AmendmentStatus.APPROVED)
    amendment.status = Amendment.AmendmentStatus.APPROVED
    amendment.approved_by = actor
    amendment.approval_date = timezone.now()
    amendment._history_user = actor
    amendment.save(
        update_fields=["status", "approved_by", "approval_date", "version", "updated_at"],
    )
    return amendment


@transaction.atomic
def reject_amendment(amendment, *, actor, reason=""):
    """SUBMITTED → REJECTED. Only PROJECT_DIRECTOR (Associé en charge)."""
    if not _is_project_director(actor, amendment.tenant):
        raise PermissionError("Seul un Associé en charge peut rejeter un avenant.")
    _assert_transition(amendment, Amendment.AmendmentStatus.REJECTED)
    amendment.status = Amendment.AmendmentStatus.REJECTED
    if reason:
        amendment.description = (
            f"{amendment.description}\n\n[Rejet — {timezone.now():%Y-%m-%d}] {reason}"
        )
    amendment._history_user = actor
    amendment.save(update_fields=["status", "description", "version", "updated_at"])
    return amendment


def create_project_from_template(template_id, project_data, tenant_id=None):
    """
    Create a project from a template, pre-populating phases, tasks, and support services.

    Template phases_config format:
    [
        {
            "name": "Concept",
            "code": "1",
            "client_label": "Phase 1 — Concept",
            "type": "REALIZATION",
            "billing_mode": "FORFAIT",
            "is_mandatory": true,
            "tasks": [
                {
                    "wbs_code": "1.1",
                    "name": "Analyse conditions existantes",
                    "client_label": "",
                    "billing_mode": "FORFAIT",
                    "is_billable": true,
                    "budgeted_hours": 0,
                    "budgeted_cost": 0,
                    "hourly_rate": null
                }
            ]
        }
    ]
    """
    template = ProjectTemplate.objects.get(pk=template_id)

    tenant = Tenant.objects.get(pk=tenant_id) if tenant_id else template.tenant

    # Accepted project fields (both "client" and "client_id" for compatibility)
    project_fields = [
        "code",
        "name",
        "client",
        "client_id",
        "business_unit",
        "legal_entity",
        "start_date",
        "end_date",
        "is_internal",
        "is_public",
        "is_consortium",
        "consortium",
        "consortium_id",
        "services_transversaux",
        "address",
        "city",
        "postal_code",
        "country",
        "surface",
        "surface_unit",
        "currency",
        "tags",
        "title_on_invoice",
        "pm",
        "pm_id",
        "associate_in_charge",
        "associate_in_charge_id",
        "invoice_approver",
        "invoice_approver_id",
    ]

    # Normalize FK fields: convert "client": 5 → "client_id": 5
    fk_fields = {
        "client": "client_id",
        "pm": "pm_id",
        "associate_in_charge": "associate_in_charge_id",
        "invoice_approver": "invoice_approver_id",
        "consortium": "consortium_id",
    }
    cleaned = {}
    for k, v in project_data.items():
        if k not in project_fields or v is None:
            continue
        # If it's a FK shortcut (e.g. "client": 5), convert to "client_id": 5
        if k in fk_fields and isinstance(v, (int, str)):
            cleaned[fk_fields[k]] = int(v)
        elif k.endswith("_id"):
            cleaned[k] = int(v) if isinstance(v, str) else v
        else:
            cleaned[k] = v

    project = Project.objects.create(
        tenant=tenant,
        template=template,
        contract_type=template.contract_type,
        **cleaned,
    )

    # Optional phase budgets override (passed by wizard step 2)
    phase_budgets = project_data.get("phase_budgets") or {}

    # Create phases and tasks from template
    for i, phase_config in enumerate(template.phases_config or []):
        budget_override = phase_budgets.get(str(i)) or phase_budgets.get(i) or {}
        phase = Phase.objects.create(
            tenant=tenant,
            project=project,
            code=phase_config.get("code", str(i + 1)),
            name=phase_config.get("name", f"Phase {i + 1}"),
            client_facing_label=phase_config.get("client_label", ""),
            phase_type=phase_config.get("type", "REALIZATION"),
            billing_mode=phase_config.get("billing_mode", "FORFAIT"),
            order=i,
            is_mandatory=phase_config.get("is_mandatory", False),
            budgeted_hours=budget_override.get("budgeted_hours")
            or phase_config.get("budgeted_hours", 0)
            or 0,
            budgeted_cost=budget_override.get("budgeted_cost")
            or phase_config.get("budgeted_cost", 0)
            or 0,
        )

        # Create tasks under this phase
        for j, task_config in enumerate(phase_config.get("tasks", [])):
            Task.objects.create(
                tenant=tenant,
                project=project,
                phase=phase,
                wbs_code=task_config.get("wbs_code", f"{phase.code}.{j + 1}"),
                name=task_config.get("name", f"Tâche {j + 1}"),
                client_facing_label=task_config.get("client_label", ""),
                billing_mode=task_config.get("billing_mode", phase.billing_mode),
                order=j,
                budgeted_hours=task_config.get("budgeted_hours", 0),
                budgeted_cost=task_config.get("budgeted_cost", 0),
                hourly_rate=task_config.get("hourly_rate"),
                is_billable=task_config.get("is_billable", True),
            )

    # Create support services from template
    for svc_config in template.support_services_config or []:
        SupportService.objects.create(
            tenant=tenant,
            project=project,
            name=svc_config.get("name", ""),
            client_facing_label=svc_config.get("client_label", ""),
        )

    return project


# --------------------------------------------------------------------------- #
# Closure checklist (F3.8)
# --------------------------------------------------------------------------- #

_TIME_ENTRIES_VALIDATED_STATUSES = {"FINANCE_APPROVED", "PAIE_VALIDATED", "LOCKED"}
_INVOICE_FINALIZED_STATUSES = {"APPROVED", "SENT", "PAID"}
_EXPENSE_CLOSED_STATUSES = {"FINANCE_VALIDATED", "PAID", "REVERSED", "REJECTED"}


def compute_closure_checklist(project: Project) -> dict:
    """Évalue les prérequis de clôture d'un projet.

    Returns a dict ``{can_close: bool, checks: [...]}`` where each check has
    keys ``code``, ``label``, ``passed``, ``detail`` and optionally
    ``severity`` ("warning" → non-bloquant, absent → bloquant).
    """
    from apps.billing.models import Invoice
    from apps.expenses.models import ExpenseReport
    from apps.planning.models import ResourceAllocation, VirtualResource
    from apps.time_entries.models import TimeEntry

    today = timezone.now().date()
    checks: list[dict] = []

    # 1. Heures de travail validées
    pending_time = TimeEntry.objects.filter(project=project).exclude(
        status__in=_TIME_ENTRIES_VALIDATED_STATUSES,
    ).count()
    checks.append({
        "code": "TIME_ENTRIES",
        "label": "Heures de travail validées",
        "passed": pending_time == 0,
        "detail": (
            "Toutes les heures sont validées"
            if pending_time == 0
            else f"{pending_time} heure(s) non validée(s)"
        ),
    })

    # 2. Factures finalisées
    draft_invoices = Invoice.objects.filter(project=project).exclude(
        status__in=_INVOICE_FINALIZED_STATUSES,
    ).count()
    checks.append({
        "code": "INVOICES",
        "label": "Factures finalisées",
        "passed": draft_invoices == 0,
        "detail": (
            "Toutes les factures sont finalisées"
            if draft_invoices == 0
            else f"{draft_invoices} facture(s) en brouillon ou soumise(s)"
        ),
    })

    # 3. Dépenses traitées
    pending_expenses = ExpenseReport.objects.filter(project=project).exclude(
        status__in=_EXPENSE_CLOSED_STATUSES,
    ).count()
    checks.append({
        "code": "EXPENSES",
        "label": "Dépenses traitées",
        "passed": pending_expenses == 0,
        "detail": (
            "Toutes les dépenses sont traitées"
            if pending_expenses == 0
            else f"{pending_expenses} rapport(s) en attente"
        ),
    })

    # 4. Profils virtuels remplacés (warning)
    active_virtuals = VirtualResource.objects.filter(
        project=project, is_active=True,
    ).count()
    checks.append({
        "code": "VIRTUAL_RESOURCES",
        "label": "Profils virtuels remplacés",
        "passed": active_virtuals == 0,
        "detail": (
            "Aucun profil virtuel actif"
            if active_virtuals == 0
            else f"{active_virtuals} profil(s) virtuel(s) actif(s) — remplacer par un employé avant clôture"
        ),
        "severity": "warning",
    })

    # 5. Allocations futures (warning)
    future_allocs = ResourceAllocation.objects.filter(
        project=project, end_date__gt=today,
    ).count()
    checks.append({
        "code": "FUTURE_ALLOCATIONS",
        "label": "Allocations soldées",
        "passed": future_allocs == 0,
        "detail": (
            "Aucune allocation future"
            if future_allocs == 0
            else f"{future_allocs} allocation(s) dont la fin est dans le futur"
        ),
        "severity": "warning",
    })

    blockers = [c for c in checks if not c["passed"] and c.get("severity") != "warning"]
    return {
        "can_close": len(blockers) == 0,
        "checks": checks,
    }
