"""Sécurité : create_admin_account ne doit plus contenir de mot de passe en dur.

Le mot de passe est fourni via la variable d'environnement ADMIN_SEED_PASSWORD
(ou l'argument --password) ; à défaut, la commande échoue clairement.
"""

from __future__ import annotations

import pytest
from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import CommandError


@pytest.mark.django_db
class TestCreateAdminAccount:
    def test_fails_without_password(self, monkeypatch):
        monkeypatch.delenv("ADMIN_SEED_PASSWORD", raising=False)
        with pytest.raises(CommandError):
            call_command("create_admin_account", tenant="prov-roy")
        assert not User.objects.filter(username="ph.admin").exists()

    def test_uses_password_argument(self, monkeypatch):
        monkeypatch.delenv("ADMIN_SEED_PASSWORD", raising=False)
        call_command("create_admin_account", tenant="prov-roy", password="S3cret-CI!")
        user = User.objects.get(username="ph.admin")
        assert user.is_superuser and user.is_staff
        assert user.check_password("S3cret-CI!")

    def test_reads_password_from_env(self, monkeypatch):
        monkeypatch.setenv("ADMIN_SEED_PASSWORD", "Env-S3cret!")
        call_command("create_admin_account", tenant="prov-roy")
        user = User.objects.get(username="ph.admin")
        assert user.check_password("Env-S3cret!")
