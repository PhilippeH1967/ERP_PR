"""
Custom JWT token serializers and authentication utilities.

Extends simplejwt to include tenant_id, email, and roles[] in JWT claims.
Provides /auth/me/ and /auth/config/ endpoints.
"""

import contextlib

from django.conf import settings
from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
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

    def validate(self, attrs):
        """Block local login when tenant has sso_only enabled (except ADMIN)."""
        data = super().validate(attrs)

        user = self.user
        from apps.core.models import ProjectRole, Role

        is_admin = ProjectRole.objects.filter(
            user=user, role=Role.ADMIN
        ).exists()

        if not is_admin:
            with contextlib.suppress(Exception):
                if (
                    hasattr(user, "tenant_association")
                    and user.tenant_association.tenant.sso_only
                ):
                    raise serializers.ValidationError(
                        "SSO login is required for this organization.",
                        code="sso_only",
                    )

        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    """Token obtain endpoint with custom claims."""

    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    """Token refresh endpoint."""

    pass


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def auth_me(request):
    """Return current authenticated user info."""
    user = request.user
    tenant_id = None
    with contextlib.suppress(Exception):
        if hasattr(user, "tenant_association"):
            tenant_id = user.tenant_association.tenant_id

    from apps.core.models import ProjectRole

    roles = list(
        ProjectRole.objects.filter(user=user).values_list("role", flat=True)
    )

    return Response(
        {
            "data": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "tenant_id": tenant_id,
                "roles": roles,
            }
        }
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def auth_config(request):
    """Return auth configuration for the login page."""
    sso_available = bool(settings.SOCIALACCOUNT_PROVIDERS)

    return Response(
        {
            "data": {
                "sso_available": sso_available,
                "sso_only": False,  # Default; tenant-level check after login
            }
        }
    )
