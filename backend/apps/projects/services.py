"""Project business logic services."""

from apps.core.models import Tenant

from .models import Phase, Project, ProjectTemplate, SupportService, Task


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

    # Accepted project fields
    project_fields = [
        "code", "name", "client_id", "business_unit", "legal_entity",
        "start_date", "end_date", "is_internal",
        "address", "city", "postal_code", "country",
        "surface", "surface_unit", "currency", "tags", "title_on_invoice",
        "pm_id", "associate_in_charge_id",
    ]

    project = Project.objects.create(
        tenant=tenant,
        template=template,
        contract_type=template.contract_type,
        **{k: v for k, v in project_data.items() if k in project_fields and v is not None},
    )

    # Create phases and tasks from template
    for i, phase_config in enumerate(template.phases_config or []):
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
