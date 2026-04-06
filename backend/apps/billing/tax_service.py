"""Tax calculation service — replaces hardcoded TPS/TVQ rates."""

from decimal import Decimal


def calculate_taxes(subtotal, tax_scheme=None):
    """
    Calculate taxes for a given subtotal using the tax scheme's rates.

    Returns: {
        "taxes_detail": [{"type": "TPS", "label": "TPS", "rate": 5.0, "amount": 125.00}, ...],
        "total_taxes": Decimal,
        "total_with_taxes": Decimal,
        "tax_tps": Decimal,  # backward compat
        "tax_tvq": Decimal,  # backward compat
    }
    """
    subtotal = Decimal(str(subtotal))
    taxes_detail = []
    total_taxes = Decimal("0")
    tax_tps = Decimal("0")
    tax_tvq = Decimal("0")

    if tax_scheme:
        for rate in tax_scheme.rates.filter(is_active=True).order_by("tax_type"):
            pct = Decimal(str(rate.rate))
            amount = (subtotal * pct / Decimal("100")).quantize(Decimal("0.01"))
            taxes_detail.append({
                "type": rate.tax_type,
                "label": rate.label or rate.get_tax_type_display(),
                "rate": float(pct),
                "amount": float(amount),
            })
            total_taxes += amount
            # Backward compat mapping
            if rate.tax_type in ("TPS", "GST"):
                tax_tps += amount
            elif rate.tax_type in ("TVQ", "PST"):
                tax_tvq += amount
            elif rate.tax_type in ("TVH", "HST"):
                tax_tps += amount  # TVH is combined, put in tps for display
    else:
        # Fallback: Québec defaults (TPS 5% + TVQ 9.975%)
        tax_tps = (subtotal * Decimal("5") / Decimal("100")).quantize(Decimal("0.01"))
        tax_tvq = (subtotal * Decimal("9.975") / Decimal("100")).quantize(Decimal("0.01"))
        total_taxes = tax_tps + tax_tvq
        taxes_detail = [
            {"type": "TPS", "label": "TPS (5%)", "rate": 5.0, "amount": float(tax_tps)},
            {"type": "TVQ", "label": "TVQ (9.975%)", "rate": 9.975, "amount": float(tax_tvq)},
        ]

    return {
        "taxes_detail": taxes_detail,
        "total_taxes": total_taxes,
        "total_with_taxes": subtotal + total_taxes,
        "tax_tps": tax_tps,
        "tax_tvq": tax_tvq,
    }


def seed_tax_schemes(tenant):
    """Seed standard Canadian tax schemes."""
    from apps.core.models import TaxRate, TaxScheme

    schemes = [
        {
            "name": "Québec (TPS + TVQ)",
            "province": "Québec",
            "is_default": True,
            "rates": [
                {"tax_type": "TPS", "label": "TPS", "rate": "5.000"},
                {"tax_type": "TVQ", "label": "TVQ", "rate": "9.975"},
            ],
        },
        {
            "name": "Ontario (TVH 13%)",
            "province": "Ontario",
            "rates": [
                {"tax_type": "TVH", "label": "TVH", "rate": "13.000"},
            ],
        },
        {
            "name": "Alberta (TPS seulement)",
            "province": "Alberta",
            "rates": [
                {"tax_type": "TPS", "label": "TPS", "rate": "5.000"},
            ],
        },
        {
            "name": "Colombie-Britannique (TPS + PST)",
            "province": "Colombie-Britannique",
            "rates": [
                {"tax_type": "GST", "label": "GST", "rate": "5.000"},
                {"tax_type": "PST", "label": "PST", "rate": "7.000"},
            ],
        },
        {
            "name": "France (TVA 20%)",
            "province": "France",
            "rates": [
                {"tax_type": "OTHER", "label": "TVA", "rate": "20.000"},
            ],
        },
        {
            "name": "Exonéré (0%)",
            "province": "",
            "rates": [],
        },
    ]

    created = 0
    for s in schemes:
        scheme, is_new = TaxScheme.objects.get_or_create(
            tenant=tenant, name=s["name"],
            defaults={
                "province": s["province"],
                "is_default": s.get("is_default", False),
            },
        )
        if is_new:
            created += 1
            for r in s["rates"]:
                TaxRate.objects.create(
                    tenant=tenant, scheme=scheme,
                    tax_type=r["tax_type"], label=r["label"], rate=r["rate"],
                )

    return created
