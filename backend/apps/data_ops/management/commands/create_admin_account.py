"""
Create the initial admin account for the application.

Le mot de passe n'est JAMAIS en dur : il est lu depuis la variable
d'environnement ``ADMIN_SEED_PASSWORD`` (ou l'argument ``--password``).

Usage:
    ADMIN_SEED_PASSWORD='...' python manage.py create_admin_account --tenant=provencher-roy
    python manage.py create_admin_account --tenant=provencher-roy --password='...'
"""

import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create the initial admin account"

    def add_arguments(self, parser):
        parser.add_argument("--tenant", type=str, required=True)
        parser.add_argument(
            "--password",
            type=str,
            default=None,
            help="Mot de passe admin. À défaut, lu depuis ADMIN_SEED_PASSWORD.",
        )

    def handle(self, *args, **options):
        from apps.core.models import ProjectRole, Tenant, UserTenantAssociation

        password = options.get("password") or os.environ.get("ADMIN_SEED_PASSWORD")
        if not password:
            raise CommandError(
                "Mot de passe requis : passez --password ou définissez la "
                "variable d'environnement ADMIN_SEED_PASSWORD."
            )

        tenant_slug = options["tenant"]
        tenant, _ = Tenant.objects.get_or_create(
            slug=tenant_slug,
            defaults={"name": tenant_slug.replace("-", " ").title()},
        )

        username = "ph.admin"
        email = "admin@provencher-roy.com"

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "first_name": "Philippe",
                "last_name": "Admin",
                "is_staff": True,
                "is_superuser": True,
            },
        )

        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Admin créé: {username}"))
        else:
            self.stdout.write(f"Admin existe déjà: {username}")

        UserTenantAssociation.objects.get_or_create(
            user=user, defaults={"tenant": tenant}
        )

        ProjectRole.objects.get_or_create(
            tenant=tenant, user=user, project_id=None, role="ADMIN",
        )

        # Le mot de passe n'est volontairement PAS ré-affiché (secret).
        self.stdout.write(self.style.SUCCESS(f"""
╔══════════════════════════════════════╗
║  COMPTE ADMINISTRATEUR              ║
╠══════════════════════════════════════╣
║  Username : {username:<24}║
║  Email    : {email:<24}║
║  Tenant   : {tenant.name:<24}║
║  Role     : ADMIN (superuser)       ║
╚══════════════════════════════════════╝
   Mot de passe : défini via ADMIN_SEED_PASSWORD / --password.
⚠️  Changez-le après la première connexion.
"""))
