"""
Core DRF mixins for optimistic locking and tenant-aware operations.
"""

from rest_framework.exceptions import APIException


class VersionConflictError(APIException):
    """Raised when optimistic lock version mismatch is detected."""

    status_code = 409
    default_detail = "Record modified by another user"
    default_code = "VERSION_CONFLICT"


class OptimisticLockMixin:
    """
    DRF serializer mixin that enforces optimistic locking via version field.

    On update:
    1. Reads expected version from serializer context (If-Match header or payload)
    2. Compares with current DB version
    3. If mismatch: raises VersionConflictError (409)
    4. If match: proceeds with save (version auto-incremented by VersionedModel.save())

    Usage in serializer:
        class InvoiceSerializer(OptimisticLockMixin, ModelSerializer):
            class Meta:
                model = Invoice
                fields = ["id", "amount", "version", ...]

    Usage in view:
        def get_serializer_context(self):
            ctx = super().get_serializer_context()
            ctx["if_match_version"] = self.request.headers.get("If-Match")
            return ctx
    """

    def update(self, instance, validated_data):
        # Get expected version from context (If-Match header) or payload
        expected_version = self._get_expected_version(validated_data)

        if expected_version is not None and instance.version != expected_version:
            raise VersionConflictError(
                detail={
                    "code": "VERSION_CONFLICT",
                    "message": "Record modified by another user",
                    "details": {
                        "current_version": instance.version,
                        "your_version": expected_version,
                    },
                }
            )

        return super().update(instance, validated_data)

    def _get_expected_version(self, validated_data):
        """Extract expected version from If-Match header or validated data."""
        # Try If-Match header first
        context = self.context or {}
        if_match = context.get("if_match_version")
        if if_match is not None:
            try:
                return int(if_match)
            except (ValueError, TypeError):
                pass

        # Fall back to version in payload (remove it so it's not saved directly)
        version = validated_data.pop("version", None)
        if version is not None:
            try:
                return int(version)
            except (ValueError, TypeError):
                pass

        return None
