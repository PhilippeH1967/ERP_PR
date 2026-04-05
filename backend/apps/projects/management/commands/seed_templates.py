"""Seed standard project templates for Provencher Roy."""

from django.core.management.base import BaseCommand

from apps.core.models import Tenant
from apps.projects.models import ProjectTemplate


ARCHITECTURE_STANDARD = {
    "name": "Architecture standard",
    "code": "ARCH-STD",
    "contract_type": "FORFAITAIRE",
    "description": "Template standard pour projets d'architecture — phases et tâches pré-configurées",
    "phases_config": [
        {
            "name": "Concept",
            "code": "1",
            "client_label": "Phase 1 — Concept",
            "type": "REALIZATION",
            "billing_mode": "FORFAIT",
            "is_mandatory": True,
            "tasks": [
                {"wbs_code": "1.1", "name": "Analyse conditions existantes", "billing_mode": "FORFAIT", "is_billable": True},
                {"wbs_code": "1.2", "name": "Esquisse et options conceptuelles", "billing_mode": "FORFAIT", "is_billable": True},
                {"wbs_code": "1.3", "name": "Estimation classe D", "billing_mode": "FORFAIT", "is_billable": True},
            ],
        },
        {
            "name": "Préliminaire",
            "code": "2",
            "client_label": "Phase 2 — Préliminaire",
            "type": "REALIZATION",
            "billing_mode": "FORFAIT",
            "is_mandatory": True,
            "tasks": [
                {"wbs_code": "2.1", "name": "Plans préliminaires", "billing_mode": "FORFAIT", "is_billable": True},
                {"wbs_code": "2.2", "name": "Devis préliminaires", "billing_mode": "FORFAIT", "is_billable": True},
                {"wbs_code": "2.3", "name": "Estimation classe C", "billing_mode": "FORFAIT", "is_billable": True},
            ],
        },
        {
            "name": "Définitif",
            "code": "3",
            "client_label": "Phase 3 — Définitif",
            "type": "REALIZATION",
            "billing_mode": "FORFAIT",
            "is_mandatory": True,
            "tasks": [
                {"wbs_code": "3.1", "name": "Plans architecturaux détaillés", "billing_mode": "FORFAIT", "is_billable": True},
                {"wbs_code": "3.2", "name": "Plans structure et fondations", "billing_mode": "FORFAIT", "is_billable": True},
                {"wbs_code": "3.3", "name": "Plans et devis MEP", "billing_mode": "FORFAIT", "is_billable": True},
                {"wbs_code": "3.4", "name": "Devis quantitatif", "billing_mode": "FORFAIT", "is_billable": True},
                {"wbs_code": "3.5", "name": "Estimation classe B", "billing_mode": "FORFAIT", "is_billable": True},
            ],
        },
        {
            "name": "Appel d'offres",
            "code": "4",
            "client_label": "Phase 4 — Appel d'offres",
            "type": "REALIZATION",
            "billing_mode": "FORFAIT",
            "is_mandatory": False,
            "tasks": [
                {"wbs_code": "4.1", "name": "Préparation documents d'appel d'offres", "billing_mode": "FORFAIT", "is_billable": True},
                {"wbs_code": "4.2", "name": "Analyse des soumissions", "billing_mode": "FORFAIT", "is_billable": True},
                {"wbs_code": "4.3", "name": "Recommandation d'attribution", "billing_mode": "FORFAIT", "is_billable": True},
            ],
        },
        {
            "name": "Surveillance",
            "code": "5",
            "client_label": "Phase 5 — Surveillance",
            "type": "REALIZATION",
            "billing_mode": "HORAIRE",
            "is_mandatory": False,
            "tasks": [
                {"wbs_code": "5.1", "name": "Surveillance de chantier", "billing_mode": "HORAIRE", "is_billable": True, "hourly_rate": 125},
                {"wbs_code": "5.2", "name": "Réunions de chantier", "billing_mode": "HORAIRE", "is_billable": True, "hourly_rate": 125},
                {"wbs_code": "5.3", "name": "Inspection et réception", "billing_mode": "HORAIRE", "is_billable": True, "hourly_rate": 125},
            ],
        },
        {
            "name": "Qualité",
            "code": "QA",
            "client_label": "Qualité",
            "type": "SUPPORT",
            "billing_mode": "FORFAIT",
            "is_mandatory": False,
            "tasks": [
                {"wbs_code": "QA.1", "name": "Contrôle qualité plans", "billing_mode": "FORFAIT", "is_billable": False},
                {"wbs_code": "QA.2", "name": "Revue de conformité", "billing_mode": "FORFAIT", "is_billable": False},
                {"wbs_code": "QA.3", "name": "Vérification normes", "billing_mode": "FORFAIT", "is_billable": False},
            ],
        },
        {
            "name": "Gestion de projet",
            "code": "GP",
            "client_label": "Gestion de projet",
            "type": "SUPPORT",
            "billing_mode": "FORFAIT",
            "is_mandatory": True,
            "tasks": [
                {"wbs_code": "GP.1", "name": "Coordination équipe", "billing_mode": "FORFAIT", "is_billable": False},
                {"wbs_code": "GP.2", "name": "Réunions client", "billing_mode": "FORFAIT", "is_billable": True},
                {"wbs_code": "GP.3", "name": "Administration projet", "billing_mode": "FORFAIT", "is_billable": False},
            ],
        },
    ],
    "support_services_config": [
        {"code": "BIM", "name": "BIM / Modélisation"},
        {"code": "PAYSAGE", "name": "Architecture de paysage"},
        {"code": "DD", "name": "Développement durable"},
        {"code": "CIVIL", "name": "Génie civil"},
        {"code": "PATRIMOINE", "name": "Patrimoine"},
        {"code": "DESIGN_INT", "name": "Design intérieur"},
        {"code": "ECLAIRAGE", "name": "Éclairage"},
    ],
}


class Command(BaseCommand):
    help = "Seed standard project templates"

    def handle(self, *args, **options):
        tenant = Tenant.objects.first()
        if not tenant:
            self.stdout.write(self.style.ERROR("No tenant found"))
            return

        tmpl, created = ProjectTemplate.objects.update_or_create(
            code=ARCHITECTURE_STANDARD["code"],
            tenant=tenant,
            defaults={
                "name": ARCHITECTURE_STANDARD["name"],
                "contract_type": ARCHITECTURE_STANDARD["contract_type"],
                "description": ARCHITECTURE_STANDARD["description"],
                "phases_config": ARCHITECTURE_STANDARD["phases_config"],
                "support_services_config": ARCHITECTURE_STANDARD["support_services_config"],
                "is_active": True,
            },
        )
        action = "Created" if created else "Updated"
        self.stdout.write(self.style.SUCCESS(
            f"{action} template: {tmpl.name} ({tmpl.code}) — "
            f"{len(tmpl.phases_config)} phases, "
            f"{sum(len(p.get('tasks', [])) for p in tmpl.phases_config)} tasks"
        ))
