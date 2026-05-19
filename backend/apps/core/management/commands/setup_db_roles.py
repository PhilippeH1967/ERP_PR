"""
Create the least-privilege application database role.

Background (audit finding F1): the Django connection role in the current
deployment is the table owner AND a PostgreSQL superuser (the postgres
image creates POSTGRES_USER as superuser). Both owners and superusers
BYPASS Row-Level Security — even with FORCE ROW LEVEL SECURITY — so tenant
isolation at the DB layer is inert when the app connects with that role.

This command creates a dedicated `NOSUPERUSER NOBYPASSRLS` login role with
only DML privileges. Run it once (with the privileged/owner connection),
then point the running Django process at this role via DB_APP_USER /
DB_APP_PASSWORD. Migrations and `setup_rls` keep using the owner role.

Idempotent: safe to run repeatedly.

Usage:
    python manage.py setup_db_roles --password '<secret>'
    # or set DB_APP_USER / DB_APP_PASSWORD in the environment
"""

import os

import structlog
from django.core.management.base import BaseCommand, CommandError
from django.db import connection, transaction

logger = structlog.get_logger()


class Command(BaseCommand):
    help = "Create the least-privilege (NOSUPERUSER, NOBYPASSRLS) app DB role"

    def add_arguments(self, parser):
        parser.add_argument(
            "--role",
            default=os.environ.get("DB_APP_USER", "erp_app"),
            help="Login role name (default: env DB_APP_USER or 'erp_app')",
        )
        parser.add_argument(
            "--password",
            default=os.environ.get("DB_APP_PASSWORD", ""),
            help="Login password (default: env DB_APP_PASSWORD)",
        )

    def handle(self, *args, **options):
        role = options["role"]
        password = options["password"]

        # Defend against SQL injection on the identifier: role names are
        # validated, the password is always parameter-bound.
        if not role.isidentifier():
            raise CommandError(f"Invalid role name: {role!r}")
        if not password:
            raise CommandError(
                "A password is required (--password or DB_APP_PASSWORD env)."
            )

        quoted_role = connection.ops.quote_name(role)

        with transaction.atomic(), connection.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM pg_roles WHERE rolname = %s", [role]
            )
            exists = cursor.fetchone() is not None

            if exists:
                cursor.execute(
                    f"ALTER ROLE {quoted_role} "
                    f"NOSUPERUSER NOBYPASSRLS LOGIN PASSWORD %s",
                    [password],
                )
                self.stdout.write(
                    self.style.WARNING(f"Role {role} already existed — updated.")
                )
            else:
                cursor.execute(
                    f"CREATE ROLE {quoted_role} "
                    f"NOSUPERUSER NOBYPASSRLS LOGIN PASSWORD %s",
                    [password],
                )
                self.stdout.write(
                    self.style.SUCCESS(f"Role {role} created.")
                )

            # DML only — no DDL, no ownership. RLS now applies to this role.
            cursor.execute(
                f"GRANT USAGE ON SCHEMA public TO {quoted_role};"
            )
            cursor.execute(
                f"GRANT SELECT, INSERT, UPDATE, DELETE "
                f"ON ALL TABLES IN SCHEMA public TO {quoted_role};"
            )
            cursor.execute(
                f"GRANT USAGE, SELECT "
                f"ON ALL SEQUENCES IN SCHEMA public TO {quoted_role};"
            )
            # Future tables/sequences created by the owner during later
            # migrations inherit the same grants automatically.
            cursor.execute(
                f"ALTER DEFAULT PRIVILEGES IN SCHEMA public "
                f"GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES "
                f"TO {quoted_role};"
            )
            cursor.execute(
                f"ALTER DEFAULT PRIVILEGES IN SCHEMA public "
                f"GRANT USAGE, SELECT ON SEQUENCES TO {quoted_role};"
            )

        logger.info("db_app_role_configured", role=role)
        self.stdout.write(
            self.style.SUCCESS(
                f"Done: {role} is NOSUPERUSER/NOBYPASSRLS with DML only. "
                f"Point DB_APP_USER/DB_APP_PASSWORD at it for the runtime "
                f"process; keep migrations on the owner role."
            )
        )
