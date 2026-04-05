"""Consortium URL routes."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ConsortiumMemberViewSet, ConsortiumViewSet

router = DefaultRouter()
router.register(r"consortiums", ConsortiumViewSet, basename="consortium")

# Nested member routes
member_router = DefaultRouter()
member_router.register(r"members", ConsortiumMemberViewSet, basename="consortium-member")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "consortiums/<int:consortium_pk>/",
        include(member_router.urls),
    ),
]
