"""Action center endpoint — role-specific pending actions (Sprint 2 - B1)."""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


def _user_roles(user):
    from apps.core.models import ProjectRole
    roles = set(ProjectRole.objects.filter(user=user).values_list("role", flat=True))
    roles.add("EMPLOYEE")
    return roles


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def action_center(request):
    """Return pending action counts grouped by role."""
    tenant_id = getattr(request, "tenant_id", None)
    roles = _user_roles(request.user)
    actions = []
    tf = {"tenant_id": tenant_id} if tenant_id else {}

    # EMPLOYEE (always)
    from apps.time_entries.models import WeeklyApproval
    pending_ts = WeeklyApproval.objects.filter(**tf, employee=request.user, pm_status="PENDING").count()
    if pending_ts:
        actions.append({"key": "pending_timesheet", "label": "Feuille de temps non soumise", "count": pending_ts, "icon": "clock", "color": "danger", "url": "/timesheets"})

    from apps.expenses.models import ExpenseReport
    pending_exp = ExpenseReport.objects.filter(**tf, employee=request.user, status="SUBMITTED").count()
    if pending_exp:
        actions.append({"key": "pending_expenses", "label": "Depenses en attente", "count": pending_exp, "icon": "receipt", "color": "warning", "url": "/expenses"})

    # PM
    if roles & {"PM", "ADMIN"}:
        ts_approve = WeeklyApproval.objects.filter(**tf, pm_status="PENDING").count()
        if ts_approve:
            actions.append({"key": "timesheets_to_approve", "label": "Feuilles a approuver", "count": ts_approve, "icon": "check", "color": "warning", "url": "/approvals"})

        from apps.suppliers.models import STInvoice
        st_received = STInvoice.objects.filter(**tf, status="received").count()
        if st_received:
            actions.append({"key": "st_invoices_received", "label": "Factures ST a autoriser", "count": st_received, "icon": "truck", "color": "warning", "url": "/st-approvals"})

    # FINANCE
    if roles & {"FINANCE", "ADMIN"}:
        ts_validate = WeeklyApproval.objects.filter(**tf, finance_status="PENDING").count()
        if ts_validate:
            actions.append({"key": "timesheets_to_validate", "label": "Timesheets a valider", "count": ts_validate, "icon": "check-double", "color": "warning", "url": "/approvals"})

        from apps.billing.models import Invoice
        inv_draft = Invoice.objects.filter(**tf, status="DRAFT").count()
        if inv_draft:
            actions.append({"key": "invoices_to_submit", "label": "Factures brouillon", "count": inv_draft, "icon": "file", "color": "primary", "url": "/billing"})

        from apps.suppliers.models import STInvoice as STI2
        st_pay = STI2.objects.filter(**tf, status="authorized").count()
        if st_pay:
            actions.append({"key": "st_to_pay", "label": "Factures ST a payer", "count": st_pay, "icon": "dollar", "color": "warning", "url": "/suppliers"})

        exp_validate = ExpenseReport.objects.filter(**tf, status="PM_APPROVED").count()
        if exp_validate:
            actions.append({"key": "expenses_to_validate", "label": "Notes de frais a valider", "count": exp_validate, "icon": "receipt", "color": "warning", "url": "/expenses"})

    # PAIE
    if roles & {"PAIE", "ADMIN"}:
        ts_paie = WeeklyApproval.objects.filter(**tf, paie_status="PENDING").count()
        if ts_paie:
            actions.append({"key": "timesheets_paie", "label": "Feuilles a valider (paie)", "count": ts_paie, "icon": "shield", "color": "danger", "url": "/approvals"})

    # DIRECTOR
    if roles & {"BU_DIRECTOR", "PROJECT_DIRECTOR", "ADMIN"}:
        from apps.billing.models import Invoice as Inv2
        inv_approve = Inv2.objects.filter(**tf, status="SUBMITTED").count()
        if inv_approve:
            actions.append({"key": "invoices_to_approve", "label": "Factures a approuver", "count": inv_approve, "icon": "stamp", "color": "warning", "url": "/approvals"})

    total = sum(a["count"] for a in actions)
    return Response({"data": {"actions": actions, "total_count": total}})
