"""Convertit les ``SupportService`` existants (services transversaux non
imputables) en **phases de type SUPPORT** contenant **une tâche feuille
imputable** — afin que la saisie de temps soit possible sur les services
transversaux. Voir aussi ``services.create_support_phase``.
"""

from django.db import migrations


def _support_code(svc):
    if svc.code:
        return svc.code
    slug = "".join(c for c in (svc.name or "") if c.isalnum()).upper()[:50]
    return slug or f"SVC{svc.id}"


def support_services_to_phases(apps, schema_editor):
    SupportService = apps.get_model("projects", "SupportService")
    Phase = apps.get_model("projects", "Phase")
    Task = apps.get_model("projects", "Task")

    for svc in SupportService.objects.all():
        code = _support_code(svc)
        # Idempotence : ne pas dupliquer si une phase SUPPORT de même code existe.
        if Phase.objects.filter(
            project_id=svc.project_id, phase_type="SUPPORT", code=code
        ).exists():
            svc.delete()
            continue

        max_order = (
            Phase.objects.filter(project_id=svc.project_id)
            .order_by("-order")
            .values_list("order", flat=True)
            .first()
            or 0
        )
        phase = Phase.objects.create(
            tenant_id=svc.tenant_id,
            project_id=svc.project_id,
            code=code,
            name=svc.name,
            client_facing_label=svc.client_facing_label,
            phase_type="SUPPORT",
            billing_mode=svc.billing_mode,
            order=max_order + 1,
        )
        n = 1
        while Task.objects.filter(
            project_id=svc.project_id, wbs_code=f"{code}.{n}"
        ).exists():
            n += 1
        Task.objects.create(
            tenant_id=svc.tenant_id,
            project_id=svc.project_id,
            phase=phase,
            wbs_code=f"{code}.{n}",
            name=svc.name,
            client_facing_label=svc.client_facing_label,
            billing_mode=svc.billing_mode,
            budgeted_hours=svc.budgeted_hours,
            budgeted_cost=svc.budgeted_cost,
            is_billable=svc.is_billable,
            order=0,
        )
        svc.delete()


def phases_to_support_services(apps, schema_editor):
    """Inverse best-effort : chaque phase SUPPORT n'ayant qu'**une seule tâche
    feuille** redevient un ``SupportService`` (la phase et sa tâche sont
    supprimées). Caveat : une phase SUPPORT créée à la main avec une unique
    tâche serait elle aussi reconvertie — acceptable car ce reverse ne sert
    qu'en développement."""
    SupportService = apps.get_model("projects", "SupportService")
    Phase = apps.get_model("projects", "Phase")
    Task = apps.get_model("projects", "Task")

    for phase in Phase.objects.filter(phase_type="SUPPORT"):
        tasks = list(Task.objects.filter(phase=phase))
        if len(tasks) != 1 or tasks[0].parent_id is not None:
            continue
        task = tasks[0]
        SupportService.objects.create(
            tenant_id=phase.tenant_id,
            project_id=phase.project_id,
            code=phase.code,
            name=phase.name,
            client_facing_label=phase.client_facing_label,
            billing_mode=task.billing_mode,
            budgeted_hours=task.budgeted_hours,
            budgeted_cost=task.budgeted_cost,
            is_billable=task.is_billable,
        )
        task.delete()
        phase.delete()


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0015_remove_standardtask_uq_standard_task_phase_name_and_more"),
    ]

    operations = [
        migrations.RunPython(support_services_to_phases, phases_to_support_services),
    ]
