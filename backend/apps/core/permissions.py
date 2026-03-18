"""
RBAC predicates (django-rules) and DRF permission classes.

Predicates evaluate user roles from ProjectRole model.
DRF permission classes compose predicates for API endpoint protection.
"""

import rules
from rest_framework.permissions import BasePermission

from apps.core.models import ProjectRole, Role

# ============================================================
# django-rules predicates
# ============================================================


@rules.predicate
def is_admin(user):
    """User has ADMIN role (global, any project)."""
    return ProjectRole.objects.filter(user=user, role=Role.ADMIN).exists()


@rules.predicate
def is_finance(user):
    """User has FINANCE role (global or any project)."""
    return ProjectRole.objects.filter(user=user, role=Role.FINANCE).exists()


@rules.predicate
def is_bu_director(user):
    """User has BU_DIRECTOR role."""
    return ProjectRole.objects.filter(user=user, role=Role.BU_DIRECTOR).exists()


@rules.predicate
def is_project_pm(user, project_id):
    """User has PM role on the specified project."""
    if project_id is None:
        return False
    return ProjectRole.objects.filter(
        user=user, role=Role.PM, project_id=project_id
    ).exists()


@rules.predicate
def is_project_director(user, project_id):
    """User has PROJECT_DIRECTOR role on the specified project."""
    if project_id is None:
        return False
    return ProjectRole.objects.filter(
        user=user, role=Role.PROJECT_DIRECTOR, project_id=project_id
    ).exists()


@rules.predicate
def can_approve_invoice(user, project_id):
    """User can approve invoices: FINANCE or PROJECT_DIRECTOR on project."""
    return is_finance(user) or (
        bool(project_id) and is_project_director(user, project_id)
    )


@rules.predicate
def can_see_salary_costs(user):
    """User can see salary cost fields: FINANCE, PROJECT_DIRECTOR, or BU_DIRECTOR (FR67)."""
    return ProjectRole.objects.filter(
        user=user,
        role__in=[Role.FINANCE, Role.PROJECT_DIRECTOR, Role.BU_DIRECTOR, Role.ADMIN],
    ).exists()


@rules.predicate
def cannot_approve_own(user, owner_id):
    """Anti-self-approval: user cannot approve their own records (FR22b)."""
    return user.pk != owner_id


# Register rules
rules.add_rule("is_admin", is_admin)
rules.add_rule("is_finance", is_finance)
rules.add_rule("is_bu_director", is_bu_director)
rules.add_rule("is_project_pm", is_project_pm)
rules.add_rule("is_project_director", is_project_director)
rules.add_rule("can_approve_invoice", can_approve_invoice)
rules.add_rule("can_see_salary_costs", can_see_salary_costs)
rules.add_rule("cannot_approve_own", cannot_approve_own)


# ============================================================
# DRF Permission Classes
# ============================================================


class IsAdmin(BasePermission):
    """Requires ADMIN role."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and is_admin(request.user)


class IsFinance(BasePermission):
    """Requires FINANCE role."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and is_finance(request.user)


class HasProjectRole(BasePermission):
    """
    Configurable permission requiring specific role(s) on a project.

    Usage:
        class MyView(APIView):
            permission_classes = [HasProjectRole]
            required_roles = [Role.PM, Role.PROJECT_DIRECTOR]
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        required_roles = getattr(view, "required_roles", [])
        if not required_roles:
            return True

        project_id = view.kwargs.get("project_id") or request.query_params.get("project_id")

        return ProjectRole.objects.filter(
            user=request.user,
            role__in=required_roles,
            project_id=project_id,
        ).exists()
