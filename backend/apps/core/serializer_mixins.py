"""Serializer mixins for role-based field filtering (FR67)."""

COST_FIELDS = {
    "budgeted_cost",
    "hourly_budget_max",
    "construction_cost",
    "contract_value",
    "budget_impact",
}


class CostFieldFilterMixin:
    """
    Mixin that hides cost/salary fields from users without can_see_salary_costs permission.

    Usage: Add to any serializer that exposes financial fields.
    The serializer's context must include 'request' (standard DRF behavior).
    """

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request")
        if not request or not hasattr(request, "user") or not request.user.is_authenticated:
            return fields

        # Check if user can see cost fields
        from apps.core.models import ProjectRole, Role

        can_see = ProjectRole.objects.filter(
            user=request.user,
            role__in=[Role.FINANCE, Role.PROJECT_DIRECTOR, Role.BU_DIRECTOR, Role.ADMIN],
        ).exists()

        if not can_see:
            for field_name in COST_FIELDS:
                fields.pop(field_name, None)

        return fields
