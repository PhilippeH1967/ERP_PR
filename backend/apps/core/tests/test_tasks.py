"""Tests for core Celery tasks (tenant-scoped, run via tenant_context)."""

from datetime import date, timedelta

import pytest
from django.contrib.auth.models import User

from apps.core.models import Delegation, Tenant
from apps.core.tasks import expire_delegations


@pytest.mark.django_db
class TestExpireDelegations:
    _seq = 0

    def _delegation(self, tenant, end):
        TestExpireDelegations._seq += 1
        n = TestExpireDelegations._seq
        u1 = User.objects.create_user(f"d1_{tenant.slug}_{n}", password="x")
        u2 = User.objects.create_user(f"d2_{tenant.slug}_{n}", password="x")
        return Delegation.objects.create(
            tenant=tenant,
            delegator=u1,
            delegate=u2,
            scope="all",
            start_date=date(2026, 1, 1),
            end_date=end,
            is_active=True,
        )

    def test_expires_past_delegations_per_tenant(self):
        ta = Tenant.objects.create(name="A", slug="exp-a")
        tb = Tenant.objects.create(name="B", slug="exp-b")
        yesterday = date.today() - timedelta(days=1)
        tomorrow = date.today() + timedelta(days=1)

        d_a = self._delegation(ta, yesterday)
        d_b = self._delegation(tb, yesterday)
        d_future = self._delegation(ta, tomorrow)

        result = expire_delegations()

        d_a.refresh_from_db()
        d_b.refresh_from_db()
        d_future.refresh_from_db()
        assert d_a.is_active is False
        assert d_b.is_active is False  # every active tenant processed
        assert d_future.is_active is True  # not past end_date
        assert result["expired"] == 2

    def test_inactive_tenant_skipped(self):
        inactive = Tenant.objects.create(name="Inact", slug="exp-inact", is_active=False)
        d = self._delegation(inactive, date.today() - timedelta(days=1))

        result = expire_delegations()

        d.refresh_from_db()
        assert d.is_active is True  # inactive tenant not iterated
        assert result["expired"] == 0
