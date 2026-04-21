"""Billing business logic — financial calculations and aggregations."""

from datetime import date
from decimal import Decimal

from django.db.models import Sum
from rest_framework.exceptions import ValidationError

from apps.billing.models import Invoice, InvoiceMode, Payment


def assert_line_belongs_to_invoice(invoice, *, task=None, amendment=None):
    """Validate a line's amendment scope is consistent with its invoice mode.

    - MERGED invoice: line may have or omit ``amendment`` freely.
    - AMENDMENT_DEDICATED invoice: the line's amendment MUST match the
      invoice's amendment (and therefore cannot be a main-project line).
    """
    if invoice.invoice_mode != InvoiceMode.AMENDMENT_DEDICATED:
        return
    if amendment is None:
        raise ValidationError(
            {
                "amendment": (
                    "Une facture dédiée avenant ne peut pas contenir "
                    "de ligne appartenant au périmètre principal."
                )
            }
        )
    if amendment.pk != invoice.amendment_id:
        raise ValidationError(
            {"amendment": ("Cette ligne appartient à un autre avenant que celui de la facture.")}
        )


def get_client_financial_summary(
    client_id: int,
    tenant_id: int,
    date_from: str | None = None,
    date_to: str | None = None,
) -> dict:
    """Aggregate financial data for a client, optionally filtered by period."""
    invoices = Invoice.objects.filter(client_id=client_id, tenant_id=tenant_id)
    if date_from:
        invoices = invoices.filter(date_created__gte=date_from)
    if date_to:
        invoices = invoices.filter(date_created__lte=date_to)

    total_invoiced = invoices.aggregate(total=Sum("total_amount"))["total"] or Decimal("0")

    payments_qs = Payment.objects.filter(invoice__client_id=client_id, invoice__tenant_id=tenant_id)
    if date_from:
        payments_qs = payments_qs.filter(payment_date__gte=date_from)
    if date_to:
        payments_qs = payments_qs.filter(payment_date__lte=date_to)

    total_paid = payments_qs.aggregate(total=Sum("amount"))["total"] or Decimal("0")
    outstanding = total_invoiced - total_paid
    projects_count = invoices.values("project_id").distinct().count()

    # CA by year
    from django.db.models.functions import ExtractYear

    ca_by_year = {}
    yearly = (
        Invoice.objects.filter(client_id=client_id, tenant_id=tenant_id)
        .annotate(year=ExtractYear("date_created"))
        .values("year")
        .annotate(total=Sum("total_amount"))
        .order_by("-year")
    )
    for row in yearly:
        if row["year"]:
            ca_by_year[str(row["year"])] = str(row["total"] or 0)

    return {
        "total_ca": str(total_invoiced),
        "total_paid": str(total_paid),
        "invoices_outstanding": str(outstanding),
        "projects_count": projects_count,
        "ca_by_year": ca_by_year,
    }


def get_aging_analysis(client_id: int, tenant_id: int) -> dict:
    """Invoice aging by 0-30, 31-60, 61-90, 90+ days."""
    today = date.today()
    sent_invoices = Invoice.objects.filter(
        client_id=client_id,
        tenant_id=tenant_id,
        status="SENT",
        date_sent__isnull=False,
    )

    buckets = {
        "0_30": Decimal("0"),
        "31_60": Decimal("0"),
        "61_90": Decimal("0"),
        "90_plus": Decimal("0"),
    }

    for inv in sent_invoices:
        days = (today - inv.date_sent).days
        paid = inv.payments.aggregate(total=Sum("amount"))["total"] or Decimal("0")
        balance = inv.total_amount - paid
        if balance <= 0:
            continue
        if days <= 30:
            buckets["0_30"] += balance
        elif days <= 60:
            buckets["31_60"] += balance
        elif days <= 90:
            buckets["61_90"] += balance
        else:
            buckets["90_plus"] += balance

    return {k: str(v) for k, v in buckets.items()}


def calculate_ca_salary_ratio(project_id: int, tenant_id: int) -> dict:
    """CA/Salary ratio for a project — invoiced vs salary costs."""
    invoiced = Invoice.objects.filter(
        project_id=project_id,
        tenant_id=tenant_id,
    ).aggregate(total=Sum("total_amount"))["total"] or Decimal("0")

    # Salary costs from time entries × internal rates (simplified)
    from apps.time_entries.models import TimeEntry

    hours = TimeEntry.objects.filter(
        project_id=project_id,
        tenant_id=tenant_id,
    ).aggregate(total=Sum("hours"))["total"] or Decimal("0")

    # Placeholder rate — will use RateGrid when available
    avg_rate = Decimal("85.00")
    salary_cost = hours * avg_rate

    ratio = (invoiced / salary_cost * 100) if salary_cost > 0 else Decimal("0")

    return {
        "invoiced": str(invoiced),
        "salary_cost": str(salary_cost),
        "ratio_percent": str(ratio.quantize(Decimal("0.01"))),
        "hours_consumed": str(hours),
    }
