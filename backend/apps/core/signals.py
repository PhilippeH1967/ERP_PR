"""
Signals for SSO auto-provisioning.

On first social account login (Microsoft Entra ID), automatically
creates a UserTenantAssociation linking the user to the default tenant.
"""

import structlog
from django.dispatch import receiver

logger = structlog.get_logger()


def get_or_create_default_tenant():
    """Get or create the default tenant for new SSO users.

    Audit F8: the SSO provisioning is single-tenant by design (the slug
    is configurable via SSO_DEFAULT_TENANT_SLUG). This is correct for a
    single-organisation deployment; enabling multi-org SSO requires a
    real tenant-resolution step (OIDC issuer / email domain) before this
    function — see the ambiguity guard in ensure_user_tenant_association.
    """
    from django.conf import settings

    from apps.core.models import Tenant

    slug = getattr(settings, "SSO_DEFAULT_TENANT_SLUG", "default")
    tenant, created = Tenant.objects.get_or_create(
        slug=slug,
        defaults={"name": slug.capitalize(), "is_active": True},
    )
    if created:
        logger.info("default_tenant_created", tenant_id=tenant.pk, slug=slug)
    return tenant


def ensure_user_tenant_association(user):
    """Ensure user has a tenant association. Create one if missing.

    Fails loud (structured warning) if more than one active tenant exists
    and multi-org SSO has not been explicitly enabled, since silently
    collapsing every SSO user into one tenant would break isolation.
    """
    from django.conf import settings

    from apps.core.models import Tenant, UserTenantAssociation

    if not hasattr(user, "tenant_association") or not UserTenantAssociation.objects.filter(
        user=user
    ).exists():
        if (
            not getattr(settings, "SSO_ALLOW_MULTI_TENANT", False)
            and Tenant.objects.filter(is_active=True).count() > 1
        ):
            logger.warning(
                "sso_multi_tenant_ambiguous",
                user_id=user.pk,
                email=getattr(user, "email", ""),
                detail=(
                    "Plusieurs tenants actifs mais provisioning SSO "
                    "mono-tenant — résolution de tenant requise avant "
                    "d'activer le SSO multi-organisation."
                ),
            )
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
