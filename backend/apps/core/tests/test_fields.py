"""Tests for custom serializer fields."""

from decimal import Decimal

from rest_framework import serializers

from apps.core.fields import MoneyField


class MoneyTestSerializer(serializers.Serializer):
    amount = MoneyField()


class TestMoneyField:
    """Tests for MoneyField — ensures Decimal→string serialization."""

    def test_serializes_decimal_to_string(self):
        serializer = MoneyTestSerializer({"amount": Decimal("15234.50")})
        assert serializer.data["amount"] == "15234.50"

    def test_serializes_with_two_decimals(self):
        serializer = MoneyTestSerializer({"amount": Decimal("100")})
        assert serializer.data["amount"] == "100.00"

    def test_validates_string_input(self):
        serializer = MoneyTestSerializer(data={"amount": "999.99"})
        assert serializer.is_valid()
        assert serializer.validated_data["amount"] == Decimal("999.99")

    def test_rejects_non_numeric(self):
        serializer = MoneyTestSerializer(data={"amount": "not-a-number"})
        assert not serializer.is_valid()
