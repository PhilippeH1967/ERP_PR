"""Seed du jeu global de phases standard du cabinet (paramétrage).

Idempotent : (re)crée les phases standard pour un ou tous les tenants, sans
doublon (clé tenant + code). Utilisé au paramétrage initial et après un
nettoyage de la base.

Usage :
    python manage.py seed_standard_phases                 # tous les tenants
    python manage.py seed_standard_phases --tenant-id 1   # un tenant précis

Si le rôle applicatif least-privilege (DB_APP_USER) est actif, lancer avec
DJANGO_DB_PRIVILEGED=1 (données tenant-scoped, bypass RLS) — cf. deployment.md.
"""

from django.core.management.base import BaseCommand

from apps.core.models import Tenant
from apps.projects.models import Phase, StandardPhase

# Jeu standard du cabinet (basé sur le parcours forfaitaire architecture).
# Modifiable ici : c'est la source des « phases de départ ».
STANDARD_PHASES = [
    {"code": "0", "name": "Étude préparatoire", "type": Phase.PhaseType.REALIZATION},
    {"code": "1", "name": "Concept", "type": Phase.PhaseType.REALIZATION},
    {"code": "2", "name": "Préliminaire", "type": Phase.PhaseType.REALIZATION},
    {"code": "3", "name": "Définitif", "type": Phase.PhaseType.REALIZATION},
    {"code": "4", "name": "Appel d'offres", "type": Phase.PhaseType.REALIZATION},
    {"code": "5", "name": "Surveillance", "type": Phase.PhaseType.REALIZATION},
    {
        "code": "G", "name": "Gestion de projet",
        "type": Phase.PhaseType.SUPPORT, "is_mandatory": True,
    },
    {"code": "Q", "name": "Qualité", "type": Phase.PhaseType.SUPPORT},
]


class Command(BaseCommand):
    help = "Crée/met à jour le jeu global de phases standard (paramétrage)."

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
            for order, spec in enumerate(STANDARD_PHASES):
                _, created = StandardPhase.objects.update_or_create(
                    tenant=tenant,
                    code=spec["code"],
                    defaults={
                        "name": spec["name"],
                        "client_facing_label": spec.get("client_facing_label", ""),
                        "phase_type": spec["type"],
                        "order": order,
                        "is_mandatory": spec.get("is_mandatory", False),
                        "is_active": True,
                    },
                )
                created_here += int(created)
                total += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f"  ✓ {tenant.name}: {len(STANDARD_PHASES)} phases standard "
                    f"({created_here} créées, {len(STANDARD_PHASES) - created_here} mises à jour)"
                )
            )
        self.stdout.write(self.style.SUCCESS(f"Terminé — {total} phases traitées."))
