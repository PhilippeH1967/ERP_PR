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

        # Roles claim — will be populated by Story 1.4 (RBAC)
        token["roles"] = []

        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    """Token obtain endpoint with custom claims."""

    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    """Token refresh endpoint."""

    pass
