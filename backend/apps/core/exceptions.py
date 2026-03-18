"""Custom DRF exception handler for standardized API responses."""

from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Custom exception handler that wraps all error responses in the
    standardized format: {"error": {"code": "...", "message": "...", "details": [...]}}
    """
    response = exception_handler(exc, context)

    if response is not None:
        error_code = _get_error_code(exc)
        error_message = _get_error_message(exc, response)
        error_details = _get_error_details(response)

        response.data = {
            "error": {
                "code": error_code,
                "message": error_message,
                "details": error_details,
            }
        }

    return response


def _get_error_code(exc):
    """Extract or derive error code from exception."""
    if hasattr(exc, "default_code"):
        return exc.default_code.upper()
    if isinstance(exc, APIException):
        return "API_ERROR"
    return "UNKNOWN_ERROR"


def _get_error_message(exc, response):
    """Extract human-readable error message."""
    if hasattr(exc, "detail"):
        if isinstance(exc.detail, str):
            return exc.detail
        if isinstance(exc.detail, dict) and "message" in exc.detail:
            return exc.detail["message"]
        if isinstance(exc.detail, list) and exc.detail:
            return str(exc.detail[0])
    return response.reason_phrase or "An error occurred"


def _get_error_details(response):
    """Extract field-level error details for validation errors."""
    original_data = response.data

    # VersionConflictError and similar pass details as a dict directly
    if isinstance(original_data, dict) and "details" in original_data:
        details_value = original_data["details"]
        if isinstance(details_value, (dict, list)):
            return details_value

    details = []
    if isinstance(original_data, dict):
        for field, messages in original_data.items():
            if isinstance(messages, list):
                for message in messages:
                    details.append({"field": field, "message": str(message)})
            elif isinstance(messages, str):
                details.append({"field": field, "message": messages})
    elif isinstance(original_data, list):
        for message in original_data:
            details.append({"message": str(message)})

    return details
