"""
Custom JWT token serializers and authentication utilities.

Extends simplejwt to include tenant_id, email, and roles[] in JWT claims.
"""

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Add custom claims (tenant_id, email, roles) to JWT access token."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Standard claims
        token["email"] = user.email

        # Tenant claim — from UserTenantAssociation
        import contextlib

        tenant_id = None
        with contextlib.suppress(Exception):
            if hasattr(user, "tenant_association"):
                tenant_id = user.tenant_association.tenant_id
        token["tenant_id"] = tenant_id

        # Roles claim — populated from ProjectRole model
        from apps.core.models import ProjectRole

        roles = list(
            ProjectRole.objects.filter(user=user).values("project_id", "role")
        )
        token["roles"] = [
            {"project_id": r["project_id"], "role": r["role"]} for r in roles
        ]

        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    """Token obtain endpoint with custom claims."""

    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    """Token refresh endpoint."""

    pass
