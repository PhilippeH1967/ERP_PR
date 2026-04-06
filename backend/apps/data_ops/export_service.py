"""Intacct Phase 1 — CSV export service for accounting integration."""

import csv
import io
from decimal import Decimal


def export_invoices_csv(tenant):
    """Export invoices in Intacct-compatible CSV format."""
    from apps.billing.models import Invoice

    invoices = Invoice.objects.filter(
        tenant=tenant, status__in=["APPROVED", "SENT", "PAID"]
    ).select_related("client", "project", "tax_scheme").order_by("date_created")

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "invoice_number", "client_name", "project_code",
        "date_created", "date_sent", "date_paid", "status",
        "subtotal", "tax_tps", "tax_tvq", "total_with_taxes",
        "tax_scheme", "currency",
    ])
    for inv in invoices:
        writer.writerow([
            inv.invoice_number,
            inv.client.name if inv.client else "",
            inv.project.code if inv.project else "",
            inv.date_created,
            inv.date_sent or "",
            inv.date_paid or "",
            inv.status,
            float(inv.total_amount),
            float(inv.tax_tps),
            float(inv.tax_tvq),
            float(inv.total_with_taxes),
            inv.tax_scheme.name if inv.tax_scheme else "Default",
            "CAD",
        ])

    return output.getvalue()


def export_payments_csv(tenant):
    """Export payments in Intacct-compatible CSV format."""
    from apps.billing.models import Payment

    payments = Payment.objects.filter(
        tenant=tenant
    ).select_related("invoice", "invoice__client").order_by("payment_date")

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "payment_id", "invoice_number", "client_name",
        "amount", "payment_date", "method", "reference",
    ])
    for p in payments:
        writer.writerow([
            p.id,
            p.invoice.invoice_number,
            p.invoice.client.name if p.invoice.client else "",
            float(p.amount),
            p.payment_date,
            p.method,
            p.reference,
        ])

    return output.getvalue()


def export_expenses_csv(tenant):
    """Export expense reports in Intacct-compatible CSV format."""
    from apps.expenses.models import ExpenseLine, ExpenseReport

    reports = ExpenseReport.objects.filter(
        tenant=tenant, status__in=["FINANCE_VALIDATED", "PAID"]
    ).select_related("employee", "project").order_by("submitted_at")

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "report_id", "employee", "project_code", "status",
        "submitted_date", "total_amount",
        "line_date", "line_category", "line_amount",
        "line_description", "is_refacturable", "gl_account",
    ])
    for report in reports:
        lines = report.lines.select_related("category").all()
        for line in lines:
            writer.writerow([
                report.id,
                report.employee.username,
                report.project.code if report.project else "",
                report.status,
                report.submitted_at.date() if report.submitted_at else "",
                float(report.total_amount),
                line.expense_date,
                line.category.name if line.category else "",
                float(line.amount),
                line.description,
                line.is_refacturable,
                line.category.gl_account if line.category else "",
            ])

    return output.getvalue()


def export_time_entries_csv(tenant, month=None, year=None):
    """Export time entries for payroll/accounting integration."""
    from apps.time_entries.models import TimeEntry

    qs = TimeEntry.objects.filter(tenant=tenant).select_related(
        "employee", "project", "task"
    ).order_by("date")

    if month and year:
        qs = qs.filter(date__year=year, date__month=month)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "employee", "date", "project_code", "task_wbs",
        "hours", "status", "is_billable", "is_invoiced",
    ])
    for e in qs:
        writer.writerow([
            e.employee.username,
            e.date,
            e.project.code if e.project else "",
            e.task.wbs_code if e.task else "",
            float(e.hours),
            e.status,
            not (e.project.is_internal if e.project else True),
            e.is_invoiced,
        ])

    return output.getvalue()
