"""
Create the initial admin account for the application.

Usage:
    python manage.py create_admin_account --tenant=provencher-roy
"""

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create the initial admin account"

    def add_arguments(self, parser):
        parser.add_argument("--tenant", type=str, required=True)

    def handle(self, *args, **options):
        from apps.core.models import ProjectRole, Tenant, UserTenantAssociation

        tenant_slug = options["tenant"]
        tenant, _ = Tenant.objects.get_or_create(
            slug=tenant_slug,
            defaults={"name": tenant_slug.replace("-", " ").title()},
        )

        username = "ph.admin"
        email = "admin@provencher-roy.com"
        password = "Pr0v3nch3r!2026"

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

        self.stdout.write(self.style.SUCCESS(f"""
╔══════════════════════════════════════╗
║  COMPTE ADMINISTRATEUR              ║
╠══════════════════════════════════════╣
║  Username : {username:<24}║
║  Password : {password:<24}║
║  Email    : {email:<24}║
║  Tenant   : {tenant.name:<24}║
║  Role     : ADMIN (superuser)       ║
╚══════════════════════════════════════╝

⚠️  Changez le mot de passe après la première connexion!
"""))
