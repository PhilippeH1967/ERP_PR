"""Rétro-correction du WBS des sous-tâches mal numérotées.

Avant le correctif de ``TaskViewSet.perform_create``, le picker de tâches
standard du wizard créait des sous-tâches avec un WBS à **2 niveaux**
(``{code_phase}.{n}``, ex. ``1.2``) au lieu de ``{wbs_parent}.{séquence}``
(ex. ``1.1.1``). Cette commande renumérote ces sous-tâches **sous leur parent**.

- Ne touche **que** les sous-tâches dont le WBS n'est pas déjà
  ``{wbs_parent}.{entier}`` (les sous-tâches correctes sont laissées telles
  quelles) ; **idempotente**.
- Évite les collisions (siblings déjà corrects, autres tâches du projet).
- ``--dry-run`` affiche les changements sans rien écrire.

Usage :
    python manage.py fix_subtask_wbs                 # tous les projets
    python manage.py fix_subtask_wbs --dry-run        # aperçu
    python manage.py fix_subtask_wbs --project-id 5   # un projet précis

Si le rôle applicatif least-privilege (DB_APP_USER) est actif, lancer avec
DJANGO_DB_PRIVILEGED=1 (données tenant-scoped, bypass RLS) — cf. deployment.md.
"""

from __future__ import annotations

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.projects.models import Task


def _is_correct(sub_wbs: str, parent_wbs: str) -> bool:
    """True si ``sub_wbs`` est déjà ``{parent_wbs}.{entier}`` (un seul niveau
    sous le parent)."""
    prefix = f"{parent_wbs}."
    if not parent_wbs or not sub_wbs.startswith(prefix):
        return False
    return sub_wbs[len(prefix):].isdigit()


class Command(BaseCommand):
    help = (
        "Renumérote les sous-tâches au WBS incorrect (2 niveaux) en "
        "{wbs_parent}.{séquence} (3 niveaux). Idempotente."
    )

    def add_arguments(self, parser):
        parser.add_argument("--project-id", type=int, default=None)
        parser.add_argument("--dry-run", action="store_true", default=False)

    @transaction.atomic
    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        project_id = options.get("project_id")

        subs = Task.objects.filter(parent__isnull=False).select_related("parent")
        if project_id:
            subs = subs.filter(project_id=project_id)

        by_parent: dict[int, list[Task]] = {}
        parent_obj: dict[int, Task] = {}
        for sub in subs:
            by_parent.setdefault(sub.parent_id, []).append(sub)
            parent_obj[sub.parent_id] = sub.parent

        total = 0
        # Parents les moins profonds d'abord (par profondeur de WBS) afin qu'un
        # parent lui-même corrigé le soit avant ses propres enfants.
        for parent_id in sorted(
            by_parent, key=lambda pid: (parent_obj[pid].wbs_code or "").count(".")
        ):
            parent = Task.objects.get(pk=parent_id)  # wbs_code à jour
            children = sorted(by_parent[parent_id], key=lambda t: (t.order, t.id))

            assigned: set[int] = set()
            next_n = 1
            for child in children:
                if _is_correct(child.wbs_code, parent.wbs_code):
                    continue
                while next_n in assigned or (
                    Task.objects.filter(
                        project_id=child.project_id,
                        wbs_code=f"{parent.wbs_code}.{next_n}",
                    )
                    .exclude(pk=child.pk)
                    .exists()
                ):
                    next_n += 1
                assigned.add(next_n)
                new_wbs = f"{parent.wbs_code}.{next_n}"
                next_n += 1
                self.stdout.write(
                    f"  projet {child.project_id} : {child.wbs_code} → {new_wbs} "
                    f"({child.name})"
                )
                if not dry_run:
                    child.wbs_code = new_wbs
                    child.save(update_fields=["wbs_code"])
                total += 1

        prefix = "[dry-run] " if dry_run else ""
        if total:
            self.stdout.write(
                self.style.SUCCESS(f"{prefix}{total} sous-tâche(s) renumérotée(s).")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f"{prefix}Aucune sous-tâche à corriger.")
            )
