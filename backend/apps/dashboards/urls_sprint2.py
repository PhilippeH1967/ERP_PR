"""Sprint 2 URLs — search, action center, sidebar badges/config."""

from django.urls import path

from .action_center import action_center
from .search import global_search
from .sidebar_badges import sidebar_badges
from apps.core.sidebar_config import UserSidebarConfigViewSet

urlpatterns = [
    path("search/", global_search, name="global-search"),
    path("action_center/", action_center, name="action-center"),
    path("sidebar/badges/", sidebar_badges, name="sidebar-badges"),
    path("sidebar/config/", UserSidebarConfigViewSet.as_view({"get": "retrieve", "patch": "partial_update"}), name="sidebar-config"),
]
