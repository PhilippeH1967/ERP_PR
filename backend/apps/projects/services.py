"""Project business logic services."""

from apps.core.models import Tenant

from .models import Phase, Project, ProjectTemplate, SupportService


def create_project_from_template(template_id, project_data, tenant_id=None):
    """
    Create a project from a template, pre-populating phases and support services.
    """
    template = ProjectTemplate.objects.get(pk=template_id)

    tenant = Tenant.objects.get(pk=tenant_id) if tenant_id else template.tenant

    project = Project.objects.create(
        tenant=tenant,
        template=template,
        contract_type=template.contract_type,
        **{k: v for k, v in project_data.items() if k in [
            "code", "name", "client_id", "business_unit", "legal_entity",
            "start_date", "end_date", "is_internal",
        ]},
    )

    # Create phases from template
    for i, phase_config in enumerate(template.phases_config or []):
        Phase.objects.create(
            tenant=tenant,
            project=project,
            code=phase_config.get("code", ""),
            name=phase_config.get("name", f"Phase {i + 1}"),
            client_facing_label=phase_config.get("client_label", ""),
            phase_type=phase_config.get("type", "REALIZATION"),
            billing_mode=phase_config.get("billing_mode", "FORFAIT"),
            order=i,
            is_mandatory=phase_config.get("is_mandatory", False),
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
