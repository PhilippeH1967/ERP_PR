"""User sidebar configuration model + API (Sprint 2 - B2)."""

from django.conf import settings
from django.db import models
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAuthenticated


class UserSidebarConfig(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sidebar_config"
    )
    favorites = models.JSONField(default=list, blank=True)
    collapsed_sections = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "core_user_sidebar_config"

    def __str__(self):
        return f"SidebarConfig({self.user})"


class UserSidebarConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSidebarConfig
        fields = ["favorites", "collapsed_sections", "updated_at"]


class UserSidebarConfigViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def retrieve(self, request):
        config, _ = UserSidebarConfig.objects.get_or_create(user=request.user)
        return viewsets.Response({"data": UserSidebarConfigSerializer(config).data})

    def partial_update(self, request):
        config, _ = UserSidebarConfig.objects.get_or_create(user=request.user)
        ser = UserSidebarConfigSerializer(config, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return viewsets.Response({"data": ser.data})
