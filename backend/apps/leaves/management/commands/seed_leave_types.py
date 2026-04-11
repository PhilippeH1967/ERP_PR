"""Seed standard Quebec leave types for all tenants (or a specific one)."""

from django.core.management.base import BaseCommand

from apps.core.models import Tenant
from apps.leaves.services import seed_leave_types


class Command(BaseCommand):
    help = "Seed standard Quebec leave types (7 types)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--tenant",
            type=int,
            default=None,
            help="Tenant ID (default: all tenants)",
        )

    def handle(self, *args, **options):
        if options["tenant"]:
            tenants = Tenant.objects.filter(id=options["tenant"])
        else:
            tenants = Tenant.objects.all()

        if not tenants.exists():
            self.stdout.write(self.style.ERROR("No tenant found"))
            return

        total = 0
        for t in tenants:
            count = seed_leave_types(t)
            total += count
            self.stdout.write(f"  Tenant {t.id} ({t.name}): {count} leave types created")

        self.stdout.write(self.style.SUCCESS(f"Done — {total} leave types seeded across {tenants.count()} tenant(s)"))
