"""Notification API views."""

from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Notification


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def notification_list(request):
    """List notifications for current user."""
    qs = Notification.objects.filter(user=request.user).order_by("-created_at")[:50]
    unread = request.query_params.get("unread")
    if unread == "true":
        qs = qs.filter(read_at__isnull=True)

    result = [
        {
            "id": n.id,
            "type": n.notification_type,
            "message": n.message,
            "read": n.read_at is not None,
            "created_at": n.created_at.isoformat(),
        }
        for n in qs
    ]
    unread_count = Notification.objects.filter(
        user=request.user, read_at__isnull=True
    ).count()

    return Response({"data": result, "unread_count": unread_count})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def notification_mark_read(request, pk):
    """Mark a notification as read."""
    notif = Notification.objects.get(pk=pk, user=request.user)
    notif.read_at = timezone.now()
    notif.save(update_fields=["read_at"])
    return Response({"status": "ok"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def notification_mark_all_read(request):
    """Mark all notifications as read."""
    Notification.objects.filter(
        user=request.user, read_at__isnull=True
    ).update(read_at=timezone.now())
    return Response({"status": "ok"})
