"""Consortium API views."""

from decimal import Decimal

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Consortium, ConsortiumMember
from .serializers import (
    ConsortiumListSerializer,
    ConsortiumMemberSerializer,
    ConsortiumSerializer,
)


class ConsortiumViewSet(viewsets.ModelViewSet):
    """CRUD for consortiums with nested members."""

    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "client__name", "contract_reference"]
    filterset_fields = ["status", "pr_role"]
    ordering_fields = ["name", "created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        qs = Consortium.objects.all()
        if hasattr(self.request, "tenant_id") and self.request.tenant_id:
            qs = qs.filter(tenant_id=self.request.tenant_id)
        return qs.select_related("client").prefetch_related(
            "members", "members__organization"
        )

    def get_serializer_class(self):
        if self.action == "list":
            return ConsortiumListSerializer
        return ConsortiumSerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["if_match_version"] = self.request.headers.get("If-Match")
        return ctx

    def perform_create(self, serializer):
        from apps.core.models import Tenant

        tenant_id = getattr(self.request, "tenant_id", None)
        if tenant_id:
            serializer.save(tenant=Tenant.objects.get(pk=tenant_id))
        else:
            serializer.save(tenant=Tenant.objects.first())

    @action(detail=True, methods=["get"])
    def validate_coefficients(self, request, pk=None):
        """Check if member coefficients sum to 100%."""
        consortium = self.get_object()
        total = consortium.total_coefficient
        return Response({
            "data": {
                "total_coefficient": total,
                "is_valid": total == Decimal("100.00"),
                "members_count": consortium.members.count(),
            }
        })


class ConsortiumMemberViewSet(viewsets.ModelViewSet):
    """CRUD for consortium members — nested under /consortiums/{id}/members/."""

    serializer_class = ConsortiumMemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        consortium_id = self.kwargs.get("consortium_pk")
        return ConsortiumMember.objects.filter(
            consortium_id=consortium_id
        ).select_related("organization")

    def perform_create(self, serializer):
        from apps.core.models import Tenant

        consortium_id = self.kwargs.get("consortium_pk")
        tenant_id = getattr(self.request, "tenant_id", None)
        if tenant_id:
            serializer.save(
                consortium_id=consortium_id,
                tenant=Tenant.objects.get(pk=tenant_id),
            )
        else:
            serializer.save(
                consortium_id=consortium_id,
                tenant=Tenant.objects.first(),
            )

    def create(self, request, *args, **kwargs):
        """Create member with validation."""
        response = super().create(request, *args, **kwargs)

        # Warn if coefficients exceed 100%
        consortium_id = self.kwargs.get("consortium_pk")
        consortium = Consortium.objects.get(pk=consortium_id)
        total = consortium.total_coefficient
        if total > Decimal("100.00"):
            response.data["warning"] = (
                f"Total des coefficients: {total}% — dépasse 100%"
            )
        return response
