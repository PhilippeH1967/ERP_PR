"""Notification URL configuration."""

from django.urls import path

from .views import notification_list, notification_mark_all_read, notification_mark_read

urlpatterns = [
    path("notifications/", notification_list, name="notification-list"),
    path("notifications/<int:pk>/read/", notification_mark_read, name="notification-read"),
    path("notifications/read-all/", notification_mark_all_read, name="notification-read-all"),
]
