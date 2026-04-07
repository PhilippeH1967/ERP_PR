"""Seed standard expense categories."""

from django.core.management.base import BaseCommand

from apps.core.models import Tenant
from apps.expenses.models import ExpenseCategory


CATEGORIES = [
    {"name": "Transport — Taxi/VTC", "gl_account": "6230", "is_refacturable_default": True, "requires_receipt": True},
    {"name": "Transport — Avion", "gl_account": "6231", "is_refacturable_default": True, "requires_receipt": True},
    {"name": "Transport — Train", "gl_account": "6232", "is_refacturable_default": True, "requires_receipt": True},
    {"name": "Transport — Kilométrage", "gl_account": "6233", "is_refacturable_default": True, "requires_receipt": False},
    {"name": "Transport — Stationnement", "gl_account": "6234", "is_refacturable_default": True, "requires_receipt": True},
    {"name": "Repas — Client", "gl_account": "6240", "is_refacturable_default": True, "requires_receipt": True},
    {"name": "Repas — Équipe", "gl_account": "6241", "is_refacturable_default": False, "requires_receipt": True},
    {"name": "Hébergement", "gl_account": "6250", "is_refacturable_default": True, "requires_receipt": True},
    {"name": "Fournitures bureau", "gl_account": "6300", "is_refacturable_default": False, "requires_receipt": True},
    {"name": "Logiciel / Abonnement", "gl_account": "6310", "is_refacturable_default": False, "requires_receipt": True},
    {"name": "Formation", "gl_account": "6400", "is_refacturable_default": False, "requires_receipt": True},
    {"name": "Télécom / Internet", "gl_account": "6260", "is_refacturable_default": False, "requires_receipt": True},
    {"name": "Impression / Reproduction", "gl_account": "6320", "is_refacturable_default": True, "requires_receipt": True},
    {"name": "Frais professionnels", "gl_account": "6500", "is_refacturable_default": False, "requires_receipt": True},
    {"name": "Autre", "gl_account": "6999", "is_refacturable_default": False, "requires_receipt": False},
]


class Command(BaseCommand):
    help = "Seed standard expense categories"

    def handle(self, *args, **options):
        tenant = Tenant.objects.first()
        if not tenant:
            self.stdout.write(self.style.ERROR("No tenant found"))
            return

        created = 0
        for cat in CATEGORIES:
            _, is_new = ExpenseCategory.objects.get_or_create(
                tenant=tenant, name=cat["name"],
                defaults=cat,
            )
            if is_new:
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Seeded {created} expense categories (total: {len(CATEGORIES)})"))
