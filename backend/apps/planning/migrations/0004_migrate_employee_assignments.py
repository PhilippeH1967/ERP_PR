"""Data migration: EmployeeAssignment → ResourceAllocation.

Unifie la planification des équipes sur ResourceAllocation (Gantt comme source de vérité).
Conversion : hours_per_week = (percentage / 100) * effective_contract_hours_employé.
"""

from datetime import date, timedelta

from django.db import migrations


def forwards(apps, schema_editor):
    EmployeeAssignment = apps.get_model("projects", "EmployeeAssignment")
    ResourceAllocation = apps.get_model("planning", "ResourceAllocation")
    Phase = apps.get_model("projects", "Phase")
    UserTenantAssociation = apps.get_model("core", "UserTenantAssociation")
    LaborRule = apps.get_model("core", "LaborRule")  # noqa: F841 — used via FK traversal

    def weekly_hours_for(user_id):
        try:
            uta = UserTenantAssociation.objects.select_related("labor_rule").get(user_id=user_id)
        except UserTenantAssociation.DoesNotExist:
            return 40.0
        if uta.contract_hours_override:
            return float(uta.contract_hours_override)
        if uta.labor_rule_id:
            return float(uta.labor_rule.weekly_hours)
        return 40.0

    created = skipped = 0
    for ea in EmployeeAssignment.objects.all():
        phase_id = ea.phase_id
        if phase_id is None:
            first_phase = Phase.objects.filter(project_id=ea.project_id).order_by("order", "id").first()
            if first_phase is None:
                skipped += 1
                continue
            phase_id = first_phase.id

        if ResourceAllocation.objects.filter(
            employee_id=ea.employee_id,
            project_id=ea.project_id,
            phase_id=phase_id,
            task_id=None,
        ).exists():
            skipped += 1
            continue

        start = ea.start_date or ea.project.start_date or date.today()
        end = ea.end_date or ea.project.end_date or (start + timedelta(days=90))
        if end < start:
            end = start + timedelta(days=1)

        weekly = weekly_hours_for(ea.employee_id)
        hpw = round((float(ea.percentage) / 100.0) * weekly, 1)
        if hpw < 0.5:
            hpw = 0.5

        ResourceAllocation.objects.create(
            tenant_id=ea.tenant_id,
            employee_id=ea.employee_id,
            project_id=ea.project_id,
            phase_id=phase_id,
            task_id=None,
            start_date=start,
            end_date=end,
            hours_per_week=hpw,
            distribution_mode="uniform",
            time_unit="week",
            time_breakdown=None,
            status="ACTIVE",
            notes=f"Migré depuis EmployeeAssignment #{ea.id} ({ea.percentage}%)",
        )
        created += 1

    print(f"[planning.0004] Migration EA→RA : {created} créées, {skipped} ignorées.")


def backwards(apps, schema_editor):
    ResourceAllocation = apps.get_model("planning", "ResourceAllocation")
    ResourceAllocation.objects.filter(notes__startswith="Migré depuis EmployeeAssignment #").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("planning", "0003_resourceallocation_distribution_mode_and_more"),
        ("projects", "0007_task_end_date_task_start_date"),
        ("core", "0010_sidebar_config"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
