"""Leave business logic services."""

from datetime import timedelta

from django.utils import timezone


def create_time_entries_for_leave(leave_request):
    """
    Auto-create TimeEntry records for an approved leave request.

    Creates one entry per weekday in the leave period on the tenant's
    internal absence project (matched by is_internal + name pattern).
    """
    from apps.projects.models import Project
    from apps.time_entries.models import TimeEntry

    tenant = leave_request.tenant
    employee = leave_request.employee

    # Find or create internal absence project
    absence_project = Project.objects.filter(
        tenant=tenant, is_internal=True, name__icontains="absence",
    ).first()
    if not absence_project:
        absence_project = Project.objects.filter(
            tenant=tenant, is_internal=True, name__icontains="congé",
        ).first()
    if not absence_project:
        # Create a default absence project
        absence_project = Project.objects.create(
            tenant=tenant,
            code="ABS-INT",
            name=f"Absences — {leave_request.leave_type.name}",
            is_internal=True,
            status="ACTIVE",
        )

    # Create entries for each weekday in the period
    current_date = leave_request.start_date
    end_date = leave_request.end_date
    created = 0

    while current_date <= end_date:
        # Skip weekends
        if current_date.weekday() < 5:
            # Check if entry already exists
            if not TimeEntry.objects.filter(
                employee=employee,
                project=absence_project,
                date=current_date,
            ).exists():
                TimeEntry.objects.create(
                    tenant=tenant,
                    employee=employee,
                    project=absence_project,
                    date=current_date,
                    hours=leave_request.hours_per_day,
                    notes=f"Congé: {leave_request.leave_type.name} — {leave_request.reason or 'N/A'}",
                    status="PM_APPROVED",  # Auto-approved since leave was approved
                )
                created += 1
        current_date += timedelta(days=1)

    # Update leave bank
    update_leave_bank(leave_request)

    # Mark entries as created
    leave_request.time_entries_created = True
    leave_request.save(update_fields=["time_entries_created"])

    return created


def update_leave_bank(leave_request):
    """Update the employee's leave bank after approval."""
    from .models import LeaveBank

    year = leave_request.start_date.year
    bank, created = LeaveBank.objects.get_or_create(
        tenant=leave_request.tenant,
        employee=leave_request.employee,
        leave_type=leave_request.leave_type,
        year=year,
        defaults={"accrued": leave_request.leave_type.max_days_per_year or 0},
    )
    bank.used = float(bank.used) + float(leave_request.total_days)
    bank.save(update_fields=["used"])


def seed_leave_types(tenant):
    """Seed standard Québec leave types for a tenant."""
    from .models import LeaveType

    types = [
        {"code": "VACANCES", "name": "Vacances annuelles", "name_en": "Annual Vacation",
         "is_paid": True, "max_days_per_year": 10, "accrual_rate_monthly": 0.83,
         "can_carry_over": True, "carry_over_max_days": 5, "order": 1},
        {"code": "MALADIE", "name": "Maladie", "name_en": "Sick Leave",
         "is_paid": True, "requires_medical_cert": True, "medical_cert_threshold_days": 3,
         "max_days_per_year": 6, "order": 2},
        {"code": "PERSONNEL", "name": "Personnel", "name_en": "Personal Leave",
         "is_paid": True, "max_days_per_year": 3, "order": 3},
        {"code": "FERIE", "name": "Jour férié", "name_en": "Statutory Holiday",
         "is_paid": True, "order": 4},
        {"code": "PARENTAL", "name": "Congé parental", "name_en": "Parental Leave",
         "is_paid": False, "order": 5},
        {"code": "SANS_SOLDE", "name": "Sans solde", "name_en": "Unpaid Leave",
         "is_paid": False, "order": 6},
        {"code": "DEUIL", "name": "Congé de deuil", "name_en": "Bereavement Leave",
         "is_paid": True, "max_days_per_year": 5, "order": 7},
    ]

    created_count = 0
    for t in types:
        _, created = LeaveType.objects.get_or_create(
            tenant=tenant, code=t["code"],
            defaults=t,
        )
        if created:
            created_count += 1

    return created_count
