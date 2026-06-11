"""Rattrapage : services transversaux → phases SUPPORT imputables.

Les projets créés AVANT la conversion (PR #41 / migration projects 0016)
peuvent avoir leurs services transversaux uniquement dans le JSON
``Project.services_transversaux``, sans phase SUPPORT ni tâche imputable —
ils n'apparaissent alors ni dans l'Échéancier, ni dans Équipe & charge, ni au
budget. Cette commande comble les manques, dans les deux sens :

1. Service du JSON sans phase SUPPORT correspondante → crée la phase + sa
   tâche feuille (via ``instantiate_support_services``, idempotent par code).
2. Phase SUPPORT **sans aucune tâche** → crée la tâche feuille imputable du
   même nom (cas d'une phase convertie/créée à la main restée vide).

Usage :
    python manage.py backfill_support_phases             # tous les projets
    python manage.py backfill_support_phases --dry-run   # aperçu
    python manage.py backfill_support_phases --project-id 15

Si le rôle applicatif least-privilege (DB_APP_USER) est actif, lancer avec
DJANGO_DB_PRIVILEGED=1 — cf. deployment.md.
"""

from __future__ import annotations

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.projects.models import Phase, Project, Task
from apps.projects.services import (
    SUPPORT_SERVICE_LABELS,
    _unique_support_wbs,
    instantiate_support_services,
)


class Command(BaseCommand):
    help = (
        "Crée les phases SUPPORT + tâches imputables manquantes pour les "
        "services transversaux des projets existants. Idempotente."
    )

    def add_arguments(self, parser):
        parser.add_argument("--project-id", type=int, default=None)
        parser.add_argument("--dry-run", action="store_true", default=False)

    @transaction.atomic
    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        qs = Project.objects.all()
        if options.get("project_id"):
            qs = qs.filter(pk=options["project_id"])

        created_phases = 0
        created_tasks = 0
        for project in qs:
            # 1. Services du JSON sans phase SUPPORT.
            existing = set(
                project.phases.filter(phase_type=Phase.PhaseType.SUPPORT).values_list(
                    "code", flat=True
                )
            )
            missing = [
                c for c in (project.services_transversaux or []) if c and c not in existing
            ]
            if missing:
                self.stdout.write(
                    f"  projet {project.pk} ({project.code}) : phases manquantes "
                    f"→ {', '.join(SUPPORT_SERVICE_LABELS.get(c, c) for c in missing)}"
                )
                if not dry_run:
                    created = instantiate_support_services(project)
                    created_phases += len(created)
                    created_tasks += len(created)

            # 2. Phases SUPPORT restées sans tâche → tâche feuille imputable.
            for phase in project.phases.filter(phase_type=Phase.PhaseType.SUPPORT):
                if Task.objects.filter(phase=phase).exists():
                    continue
                self.stdout.write(
                    f"  projet {project.pk} ({project.code}) : phase « {phase.name} » "
                    f"sans tâche → tâche imputable ajoutée"
                )
                if not dry_run:
                    Task.objects.create(
                        tenant=project.tenant,
                        project=project,
                        phase=phase,
                        wbs_code=_unique_support_wbs(project, phase.code),
                        name=phase.name,
                        client_facing_label=phase.client_facing_label,
                        billing_mode=phase.billing_mode,
                        order=0,
                    )
                    created_tasks += 1

        prefix = "[dry-run] " if dry_run else ""
        self.stdout.write(
            self.style.SUCCESS(
                f"{prefix}{created_phases} phase(s) SUPPORT et "
                f"{created_tasks} tâche(s) créées."
            )
        )
