"""Seed du projet interne + tâches obligatoires de la feuille de temps.

Idempotent : (re)crée, pour un ou tous les tenants, un projet interne
« Interne » contenant les tâches toujours affichées dans la grille de saisie
de chaque employé (Congés, Formation, Maladie). Ces tâches portent le flag
``always_display_in_timesheet`` que lit l'endpoint ``time_entries/mandatory_tasks``.

Utilisé au paramétrage initial et **après un nettoyage de la base** : sans ces
tâches, la grille de saisie n'affiche plus les lignes obligatoires.

Usage :
    python manage.py seed_internal_mandatory_tasks                 # tous les tenants
    python manage.py seed_internal_mandatory_tasks --tenant-id 1   # un tenant précis

Si le rôle applicatif least-privilege (DB_APP_USER) est actif, lancer avec
DJANGO_DB_PRIVILEGED=1 (données tenant-scoped, bypass RLS) — cf. deployment.md.
"""

from __future__ import annotations

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.core.models import Tenant
from apps.projects.models import Phase, Project, Task

# Projet interne hébergeant les tâches non-projet (absences, temps interne).
INTERNAL_PROJECT = {"code": "INT-01", "name": "Interne"}
INTERNAL_PHASE = {"code": "ABS", "name": "Absences & temps interne"}

# Tâches toujours affichées dans la grille de saisie de chaque employé.
# Feuilles saisissables, non-facturables (temps interne).
MANDATORY_TASKS = [
    {"wbs_code": "ABS.1", "name": "Congés"},
    {"wbs_code": "ABS.2", "name": "Formation"},
    {"wbs_code": "ABS.3", "name": "Maladie"},
]


class Command(BaseCommand):
    help = (
        "Crée/met à jour le projet interne et les tâches obligatoires "
        "(Congés, Formation, Maladie) toujours affichées dans la feuille de temps."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--tenant-id",
            type=int,
            default=None,
            help="Limiter à un tenant ; sinon applique à tous les tenants.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        tenant_id = options.get("tenant_id")
        tenants = (
            Tenant.objects.filter(pk=tenant_id) if tenant_id else Tenant.objects.all()
        )
        if not tenants:
            self.stdout.write(self.style.WARNING("Aucun tenant trouvé."))
            return

        for tenant in tenants:
            project, _ = Project.objects.update_or_create(
                tenant=tenant,
                code=INTERNAL_PROJECT["code"],
                defaults={
                    "name": INTERNAL_PROJECT["name"],
                    "status": "ACTIVE",
                    "is_internal": True,
                },
            )
            phase, _ = Phase.objects.update_or_create(
                tenant=tenant,
                project=project,
                code=INTERNAL_PHASE["code"],
                defaults={"name": INTERNAL_PHASE["name"], "order": 0},
            )
            created_here = 0
            for spec in MANDATORY_TASKS:
                _, created = Task.objects.update_or_create(
                    tenant=tenant,
                    project=project,
                    phase=phase,
                    wbs_code=spec["wbs_code"],
                    defaults={
                        "name": spec["name"],
                        "always_display_in_timesheet": True,
                        "is_active": True,
                        "is_billable": False,
                    },
                )
                created_here += int(created)
            self.stdout.write(
                self.style.SUCCESS(
                    f"  ✓ {tenant.name}: projet interne « {project.name} » + "
                    f"{len(MANDATORY_TASKS)} tâches obligatoires "
                    f"({created_here} créées, "
                    f"{len(MANDATORY_TASKS) - created_here} mises à jour)"
                )
            )
        self.stdout.write(self.style.SUCCESS("Terminé."))
