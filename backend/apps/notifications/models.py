"""Notification and preference models."""

from django.conf import settings
from django.db import models

from apps.core.models import TenantScopedModel


class Notification(TenantScopedModel):
    """User notification — in-app + email."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications"
    )
    notification_type = models.CharField(max_length=50)
    message = models.TextField()
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "notifications_notification"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.notification_type} → {self.user}"


class NotificationPreference(TenantScopedModel):
    """User notification preferences."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="notification_preference",
    )
    email_enabled = models.BooleanField(default=True)
    subscribed_categories = models.JSONField(default=list)

    class Meta:
        db_table = "notifications_preference"

    def __str__(self):
        return f"Prefs for {self.user}"
