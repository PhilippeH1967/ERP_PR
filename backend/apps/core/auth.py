"""
Custom JWT token serializers and authentication utilities.

Extends simplejwt to include tenant_id, email, and roles[] in JWT claims.
Provides /auth/me/ and /auth/config/ endpoints.
"""

import contextlib

from django.conf import settings
from rest_framework import serializers, status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.core.permissions import IsAdmin
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


def _caller_tenant_id(request):
    """Tenant of the authenticated caller, from the server-side OneToOne
    association (never trust client-supplied tenant for admin scoping)."""
    from django.core.exceptions import ObjectDoesNotExist

    try:
        return request.user.tenant_association.tenant_id
    except (AttributeError, ObjectDoesNotExist):
        return None


def _tenant_user_ids(tenant_id):
    """Ids of users belonging to the given tenant.

    Membership = a UserTenantAssociation in the tenant OR a ProjectRole in
    the tenant (both are server-side, tenant-scoped signals). Empty set
    when tenant_id is None (fail-closed).
    """
    from apps.core.models import ProjectRole, UserTenantAssociation

    if not tenant_id:
        return set()
    assoc_ids = UserTenantAssociation.objects.filter(
        tenant_id=tenant_id
    ).values_list("user_id", flat=True)
    role_ids = ProjectRole.objects.filter(
        tenant_id=tenant_id
    ).values_list("user_id", flat=True)
    return set(assoc_ids) | set(role_ids)


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
            try:
                if (
                    hasattr(user, "tenant_association")
                    and user.tenant_association.tenant.sso_only
                ):
                    raise serializers.ValidationError(
                        "Connexion SSO obligatoire pour cette organisation.",
                        code="sso_only",
                    )
            except serializers.ValidationError:
                raise  # Re-raise validation errors
            except Exception:
                pass  # Suppress only unexpected errors (missing association, etc.)

        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    """Token obtain endpoint with custom claims."""

    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    """Token refresh endpoint."""

    pass


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def auth_logout(request):
    """Blacklist a refresh token (logout / token revocation — audit F5).

    The refresh token itself is the credential; idempotent so a missing
    or already-blacklisted token still returns success.
    """
    from rest_framework_simplejwt.exceptions import TokenError
    from rest_framework_simplejwt.tokens import RefreshToken

    raw = request.data.get("refresh")
    if not raw:
        return Response(
            {"error": {"code": "NO_REFRESH", "message": "Token refresh requis."}},
            status=400,
        )
    with contextlib.suppress(TokenError):
        RefreshToken(raw).blacklist()
    return Response({"data": {"detail": "Déconnecté."}}, status=200)


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


@api_view(["DELETE"])
@permission_classes([IsAdmin])
def user_delete(request, pk):
    """Delete a user (admin only). Cannot delete yourself."""
    from django.contrib.auth import get_user_model

    User = get_user_model()
    if pk == request.user.pk:
        return Response(
            {"error": {"code": "SELF_DELETE", "message": "Impossible de supprimer votre propre compte."}},
            status=400,
        )
    tenant_id = _caller_tenant_id(request)
    user = User.objects.filter(
        pk=pk, id__in=_tenant_user_ids(tenant_id)
    ).first()
    if user is None:
        return Response(
            {"error": {"code": "NOT_FOUND", "message": "Utilisateur introuvable."}},
            status=404,
        )
    user.delete()
    return Response(status=204)


@api_view(["PATCH"])
@permission_classes([IsAdmin])
def user_update(request, pk):
    """Update user (toggle active, change role)."""
    from django.contrib.auth import get_user_model

    from apps.core.models import ProjectRole, Tenant

    User = get_user_model()
    tenant_id = _caller_tenant_id(request)
    user = User.objects.filter(
        pk=pk, id__in=_tenant_user_ids(tenant_id)
    ).first()
    if user is None:
        return Response(
            {"error": {"code": "NOT_FOUND", "message": "Utilisateur introuvable."}},
            status=404,
        )
    data = request.data

    if "is_active" in data:
        user.is_active = data["is_active"]
        user.save(update_fields=["is_active"])

    if "password" in data and data["password"]:
        user.set_password(data["password"])
        user.save(update_fields=["password"])

    if "role" in data:
        tenant = Tenant.objects.filter(pk=tenant_id).first()
        ProjectRole.objects.filter(user=user).delete()
        if data["role"] and tenant:
            ProjectRole.objects.create(
                user=user, role=data["role"], tenant=tenant
            )

    roles = list(
        ProjectRole.objects.filter(user=user).values_list("role", flat=True)
    )
    return Response(
        {
            "data": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_active": user.is_active,
                "roles": roles,
            }
        }
    )


@api_view(["POST"])
@permission_classes([IsAdmin])
def user_create(request):
    """Create a new user with role and tenant association."""
    from django.contrib.auth import get_user_model

    from apps.core.models import ProjectRole, Tenant, UserTenantAssociation

    User = get_user_model()
    data = request.data

    if User.objects.filter(username=data.get("username", "")).exists():
        return Response(
            {"error": {"code": "DUPLICATE", "message": "Ce nom d'utilisateur existe déjà."}},
            status=400,
        )

    tenant_id = _caller_tenant_id(request)
    tenant = Tenant.objects.filter(pk=tenant_id).first()
    if tenant is None:
        return Response(
            {"error": {"code": "NO_TENANT", "message": "Tenant appelant introuvable."}},
            status=400,
        )

    user = User.objects.create_user(
        username=data["username"],
        email=data.get("email", ""),
        password=data["password"],
    )

    # Tenant association — always the caller's tenant
    UserTenantAssociation.objects.get_or_create(user=user, defaults={"tenant": tenant})

    # Role
    role = data.get("role")
    if role and tenant:
        ProjectRole.objects.create(user=user, role=role, tenant=tenant)

    roles = list(ProjectRole.objects.filter(user=user).values_list("role", flat=True))
    return Response(
        {"data": {"id": user.id, "username": user.username, "email": user.email, "roles": roles}},
        status=201,
    )


@api_view(["GET"])
@permission_classes([IsAdmin])
def user_list(request):
    """List all users with their roles (admin only)."""
    from django.contrib.auth import get_user_model

    from apps.core.models import ProjectRole

    User = get_user_model()
    tenant_id = _caller_tenant_id(request)
    users = (
        User.objects.filter(id__in=_tenant_user_ids(tenant_id))
        .order_by("username")
    )

    result = []
    for user in users:
        roles = list(
            ProjectRole.objects.filter(user=user).values_list("role", flat=True)
        )
        result.append(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_active": user.is_active,
                "is_staff": user.is_staff,
                "date_joined": user.date_joined.isoformat(),
                "roles": roles,
            }
        )

    return Response({"data": result})


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def delegation_list_create(request):
    """List and create delegations."""
    from apps.core.models import Delegation

    if request.method == "GET":
        qs = Delegation.objects.select_related("delegator", "delegate").all()
        if hasattr(request, "tenant_id") and request.tenant_id:
            qs = qs.filter(tenant_id=request.tenant_id)
        result = []
        for d in qs:
            result.append(
                {
                    "id": d.id,
                    "delegator": d.delegator_id,
                    "delegator_name": d.delegator.get_full_name() or d.delegator.username,
                    "delegate": d.delegate_id,
                    "delegate_name": d.delegate.get_full_name() or d.delegate.username,
                    "scope": d.scope,
                    "project_id": d.project_id,
                    "start_date": d.start_date.isoformat(),
                    "end_date": d.end_date.isoformat(),
                    "is_active": d.is_active,
                }
            )
        return Response({"data": result})

    # POST
    from apps.core.models import Tenant
    from django.contrib.auth import get_user_model

    User = get_user_model()
    data = request.data
    tenant_id = getattr(request, "tenant_id", None)
    tenant = Tenant.objects.get(pk=tenant_id) if tenant_id else Tenant.objects.first()

    # Validation
    delegate_id = data.get("delegate")
    scope = data.get("scope", "all")
    project_id = data.get("project_id")
    start_date = data.get("start_date")
    end_date = data.get("end_date")

    if not delegate_id or not start_date or not end_date:
        return Response(
            {"error": {"code": "VALIDATION", "message": "delegate, start_date et end_date sont obligatoires."}},
            status=400,
        )
    if int(delegate_id) == request.user.id:
        return Response(
            {"error": {"code": "SELF_DELEGATION", "message": "Impossible de se déléguer soi-même."}},
            status=400,
        )
    if start_date > end_date:
        return Response(
            {"error": {"code": "INVALID_DATES", "message": "La date de début doit précéder la date de fin."}},
            status=400,
        )
    if scope == "project" and not project_id:
        return Response(
            {"error": {"code": "MISSING_PROJECT", "message": "Un projet est requis pour la portée 'projet'."}},
            status=400,
        )

    delegation = Delegation.objects.create(
        tenant=tenant,
        delegator=request.user,
        delegate=User.objects.get(pk=delegate_id),
        scope=scope,
        project_id=project_id if scope == "project" else None,
        start_date=start_date,
        end_date=end_date,
    )
    return Response(
        {
            "data": {
                "id": delegation.id,
                "delegator": delegation.delegator_id,
                "delegate": delegation.delegate_id,
                "scope": delegation.scope,
                "start_date": delegation.start_date.isoformat(),
                "end_date": delegation.end_date.isoformat(),
                "is_active": delegation.is_active,
            }
        },
        status=201,
    )


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delegation_delete(request, pk):
    """Delete a delegation."""
    from apps.core.models import Delegation

    delegation = Delegation.objects.get(pk=pk)
    delegation.delete()
    return Response(status=204)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_search(request):
    """Search users by username or email.

    Params:
      q : texte libre (filtre sur username + email + first/last name)
      role : ProjectRole.role (PM, PROJECT_DIRECTOR, FINANCE, etc.) ; on peut
             passer plusieurs rôles séparés par virgule (ex: PM,PROJECT_DIRECTOR)
             → retourne uniquement les users ayant au moins un de ces rôles
             dans le tenant courant.
      limit : nombre max de résultats (défaut 10 sans role, 200 avec role).
    """
    from django.contrib.auth import get_user_model
    from django.db.models import Q

    from apps.core.models import ProjectRole

    User = get_user_model()
    q = request.query_params.get("q", "").strip()
    roles_param = request.query_params.get("role", "").strip()
    roles = [r.strip() for r in roles_param.split(",") if r.strip()] if roles_param else []

    qs = User.objects.filter(
        is_active=True, id__in=_tenant_user_ids(_caller_tenant_id(request))
    )
    if q:
        qs = qs.filter(
            Q(username__icontains=q)
            | Q(email__icontains=q)
            | Q(first_name__icontains=q)
            | Q(last_name__icontains=q),
        )

    if roles:
        tenant_id = getattr(request, "tenant_id", None)
        role_qs = ProjectRole.objects.filter(role__in=roles)
        if tenant_id:
            role_qs = role_qs.filter(tenant_id=tenant_id)
        user_ids = role_qs.values_list("user_id", flat=True).distinct()
        qs = qs.filter(id__in=user_ids)

    try:
        limit = int(request.query_params.get("limit", "200" if roles else "10"))
    except ValueError:
        limit = 200 if roles else 10
    limit = max(1, min(limit, 500))

    qs = qs.order_by("username")[:limit]
    result = [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "first_name": u.first_name,
            "last_name": u.last_name,
        }
        for u in qs
    ]
    return Response({"data": result})


@api_view(["GET"])
@authentication_classes([])  # endpoint 100% public : ignorer tout token (même expiré)
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
