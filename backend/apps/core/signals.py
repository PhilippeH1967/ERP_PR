"""
Signals for SSO auto-provisioning.

On first social account login (Microsoft Entra ID), automatically
creates a UserTenantAssociation linking the user to the default tenant.
"""

import structlog
from django.dispatch import receiver

logger = structlog.get_logger()


def get_or_create_default_tenant():
    """Get or create the default tenant for new SSO users."""
    from apps.core.models import Tenant

    tenant, created = Tenant.objects.get_or_create(
        slug="default",
        defaults={"name": "Default", "is_active": True},
    )
    if created:
        logger.info("default_tenant_created", tenant_id=tenant.pk)
    return tenant


def ensure_user_tenant_association(user):
    """Ensure user has a tenant association. Create one if missing."""
    from apps.core.models import UserTenantAssociation

    if not hasattr(user, "tenant_association") or not UserTenantAssociation.objects.filter(
        user=user
    ).exists():
        tenant = get_or_create_default_tenant()
        UserTenantAssociation.objects.create(user=user, tenant=tenant)
        logger.info(
            "user_tenant_association_created",
            user_id=user.pk,
            tenant_id=tenant.pk,
            email=user.email,
        )


try:
    from allauth.socialaccount.signals import social_account_added

    @receiver(social_account_added)
    def on_social_account_added(request, sociallogin, **kwargs):
        """Auto-provision tenant association on first SSO login."""
        user = sociallogin.user
        ensure_user_tenant_association(user)
        logger.info("sso_user_provisioned", user_id=user.pk, email=user.email)

except ImportError:
    pass
