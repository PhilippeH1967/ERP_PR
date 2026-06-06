"""Seed du catalogue de tâches standard par phase (paramétrage admin).

Idempotent : (re)crée les ``StandardTask`` rattachées aux phases standard de
chaque tenant. Sert de modèle pour démarrer un projet vide (picker proposé tant
que le projet n'a aucune tâche).

Usage :
    python manage.py seed_standard_tasks                 # tous les tenants
    python manage.py seed_standard_tasks --tenant-id 1   # un tenant précis

Si le rôle applicatif least-privilege (DB_APP_USER) est actif, lancer avec
DJANGO_DB_PRIVILEGED=1 (données tenant-scoped, bypass RLS) — cf. deployment.md.
"""

from django.core.management.base import BaseCommand

from apps.core.models import Tenant
from apps.projects.models import StandardPhase, StandardTask

F = "FORFAIT"
H = "HORAIRE"

# Catalogue indexé par CODE de phase standard (cf. seed_standard_phases :
# 0 Étude préparatoire, 1 Concept, 2 Préliminaire, 3 Définitif, 4 Appel d'offres,
# 5 Surveillance, G Gestion de projet, Q Qualité).
CATALOG = {
    "0": [
        ("Programme fonctionnel et technique", F),
        ("Relevés et analyse du site", F),
    ],
    "1": [
        ("Analyse des conditions existantes", F),
        ("Esquisse et options conceptuelles", F),
        ("Estimation classe D", F),
    ],
    "2": [
        ("Plans préliminaires", F),
        ("Devis préliminaires", F),
        ("Estimation classe C", F),
    ],
    "3": [
        ("Plans architecturaux détaillés", F),
        ("Plans structure et fondations", F),
        ("Plans et devis MEP", F),
        ("Devis quantitatif", F),
        ("Estimation classe B", F),
    ],
    "4": [
        ("Préparation documents d'appel d'offres", F),
        ("Analyse des soumissions", F),
        ("Recommandation d'attribution", F),
    ],
    "5": [
        ("Surveillance de chantier", H),
        ("Réunions de chantier", H),
        ("Inspection et réception", H),
    ],
    "G": [
        ("Coordination équipe", F),
        ("Réunions client", F),
        ("Administration projet", F),
    ],
    "Q": [
        ("Contrôle qualité plans", F),
        ("Revue de conformité", F),
        ("Vérification des normes", F),
    ],
}


class Command(BaseCommand):
    help = "Crée/met à jour le catalogue de tâches standard par phase (paramétrage)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--tenant-id",
            type=int,
            default=None,
            help="Limiter à un tenant ; sinon applique à tous les tenants.",
        )

    def handle(self, *args, **options):
        tenant_id = options.get("tenant_id")
        tenants = (
            Tenant.objects.filter(pk=tenant_id) if tenant_id else Tenant.objects.all()
        )
        if not tenants:
            self.stdout.write(self.style.WARNING("Aucun tenant trouvé."))
            return

        total = 0
        for tenant in tenants:
            created_here = 0
            phases = {p.code: p for p in StandardPhase.objects.filter(tenant=tenant)}
            for code, tasks in CATALOG.items():
                phase = phases.get(code)
                if not phase:
                    continue
                for order, (name, billing) in enumerate(tasks):
                    _, created = StandardTask.objects.update_or_create(
                        standard_phase=phase,
                        name=name,
                        defaults={
                            "tenant": tenant,
                            "billing_mode": billing,
                            "order": order,
                            "is_active": True,
                        },
                    )
                    created_here += int(created)
                    total += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f"  ✓ {tenant.name}: catalogue traité ({created_here} tâches créées)"
                )
            )
        self.stdout.write(self.style.SUCCESS(f"Terminé — {total} tâches traitées."))
