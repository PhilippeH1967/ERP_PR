"""Custom DRF renderers for standardized API responses."""

from rest_framework.renderers import JSONRenderer


class WrappedJSONRenderer(JSONRenderer):
    """
    Wraps successful responses in {"data": ...} format.
    Error responses are handled by the custom exception handler.

    Success (single): {"data": {...}}
    Success (list):   {"data": [...], "meta": {"count": N, "next": "...", "previous": "..."}}
    Error:            {"error": {"code": "...", "message": "...", "details": [...]}}
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get("response") if renderer_context else None

        if response and response.status_code >= 400:
            # Error responses are already formatted by custom_exception_handler
            return super().render(data, accepted_media_type, renderer_context)

        if isinstance(data, dict) and ("data" in data or "error" in data):
            # Already wrapped (e.g., by pagination or manual wrapping)
            return super().render(data, accepted_media_type, renderer_context)

        # Wrap successful response
        wrapped = {"data": data}
        return super().render(wrapped, accepted_media_type, renderer_context)
