"""
Create test user accounts for all roles.

Usage:
    python manage.py seed_test_users --tenant 1
"""

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create test user accounts for all roles"

    def add_arguments(self, parser):
        parser.add_argument("--tenant", type=int, required=True)

    def handle(self, *args, **options):
        from apps.core.models import ProjectRole, Tenant, UserTenantAssociation

        t = Tenant.objects.get(id=options["tenant"])
        pwd = "Test1234!"
        accounts = [
            ("admin@provencher-roy.com", "Admin", "PR", "ADMIN", True),
            ("pm@test.com", "Jean-Francois", "PM", "PM", False),
            ("pm2@test.com", "Marie", "PM2", "PM", False),
            ("finance@test.com", "Nathalie", "Finance", "FINANCE", False),
            ("paie@test.com", "Sylvie", "Paie", "PAIE", False),
            ("employe@test.com", "Marc", "Employe", "EMPLOYEE", False),
            ("director@test.com", "Pierre", "Director", "BU_DIRECTOR", False),
            ("assistant@test.com", "Sophie", "Assistant", "DEPT_ASSISTANT", False),
        ]
        for email, first, last, role, is_super in accounts:
            u, created = User.objects.get_or_create(
                username=email.split("@")[0],
                defaults={
                    "email": email,
                    "first_name": first,
                    "last_name": last,
                    "is_staff": is_super,
                    "is_superuser": is_super,
                },
            )
            if created:
                u.set_password(pwd)
                u.save()
            UserTenantAssociation.objects.get_or_create(user=u, defaults={"tenant": t})
            ProjectRole.objects.get_or_create(tenant=t, user=u, project_id=None, role=role)
            status = "CREATED" if created else "EXISTS"
            self.stdout.write(f"  {status:>7} {email:<30} {role}")

        self.stdout.write(self.style.SUCCESS(f"\nDone - {len(accounts)} accounts (password: Test1234!)"))
