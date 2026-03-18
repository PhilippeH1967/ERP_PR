"""
Custom DRF serializer fields for ERP domain requirements.

MoneyField: Serializes Decimal to string in JSON (never float).
"""

from rest_framework import serializers


class MoneyField(serializers.DecimalField):
    """
    Decimal field that always serializes to string in JSON.

    Prevents float rounding errors in financial amounts.
    API output: "15234.50" (string), not 15234.5 (float).
    """

    def __init__(self, **kwargs):
        kwargs.setdefault("max_digits", 12)
        kwargs.setdefault("decimal_places", 2)
        kwargs.setdefault("coerce_to_string", True)
        super().__init__(**kwargs)
