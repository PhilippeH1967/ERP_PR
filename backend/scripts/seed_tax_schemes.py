"""Seed les schémas fiscaux standards.

Idempotent : un schéma déjà présent (par nom + tenant) n'est pas recréé.
Les taux manquants sont ajoutés. Les taux existants ne sont pas modifiés.

Usage (Hostinger):
    docker compose -f docker-compose.prod.yml --env-file .env.production exec django \\
      python manage.py shell < /opt/erp/backend/scripts/seed_tax_schemes.py

Usage (local):
    docker exec -i erp-django-1 python manage.py shell < backend/scripts/seed_tax_schemes.py

Pour exécuter sur un tenant spécifique, modifier TENANT_ID ci-dessous.
"""

TENANT_ID = 1  # Provencher Roy

from apps.core.models import TaxRate, TaxScheme, Tenant  # noqa: E402

# Liste des schémas à seeder (extraits de la base locale, hors "Test QA")
SCHEMES = [
    {
        "name": "Québec (TPS + TVQ)",
        "province": "Québec",
        "description": "Schéma standard Québec",
        "is_default": True,
        "is_active": True,
        "rates": [
            {"tax_type": "TPS", "rate": "5.000", "label": "TPS"},
            {"tax_type": "TVQ", "rate": "9.975", "label": "TVQ"},
        ],
    },
    {
        "name": "Ontario (TVH 13%)",
        "province": "Ontario",
        "description": "Taxe harmonisée Ontario",
        "is_default": False,
        "is_active": True,
        "rates": [
            {"tax_type": "TVH", "rate": "13.000", "label": "TVH"},
        ],
    },
    {
        "name": "Alberta (TPS seulement)",
        "province": "Alberta",
        "description": "Taxe fédérale uniquement",
        "is_default": False,
        "is_active": True,
        "rates": [
            {"tax_type": "TPS", "rate": "5.000", "label": "GST"},
        ],
    },
    {
        "name": "Colombie-Britannique (TPS + PST)",
        "province": "Colombie-Britannique",
        "description": "Taxes fédérale et provinciale BC",
        "is_default": False,
        "is_active": True,
        "rates": [
            {"tax_type": "TPS", "rate": "5.000", "label": "GST"},
            {"tax_type": "PST", "rate": "7.000", "label": "PST"},
        ],
    },
    {
        "name": "France (TVA 20%)",
        "province": "France",
        "description": "TVA standard France",
        "is_default": False,
        "is_active": True,
        "rates": [
            {"tax_type": "OTHER", "rate": "20.000", "label": "TVA"},
        ],
    },
    {
        "name": "Exonéré (0%)",
        "province": "",
        "description": "Aucune taxe applicable",
        "is_default": False,
        "is_active": True,
        "rates": [],
    },
]


def main():
    print("=" * 60)
    print(f"SEED TAX SCHEMES — Tenant ID = {TENANT_ID}")
    print("=" * 60)

    try:
        tenant = Tenant.objects.get(pk=TENANT_ID)
    except Tenant.DoesNotExist:
        print(f"ERROR: Tenant {TENANT_ID} introuvable. Aborting.")
        return

    print(f"Tenant : {tenant.slug} — {tenant.name}")
    print()

    created_schemes = 0
    existing_schemes = 0
    created_rates = 0
    existing_rates = 0

    for spec in SCHEMES:
        scheme, created = TaxScheme.objects.get_or_create(
            tenant=tenant,
            name=spec["name"],
            defaults={
                "province": spec["province"],
                "description": spec["description"],
                "is_default": spec["is_default"],
                "is_active": spec["is_active"],
            },
        )
        if created:
            created_schemes += 1
            print(f"  ✓ Schéma créé : {scheme.name}")
        else:
            existing_schemes += 1
            print(f"  = Schéma existant : {scheme.name}")

        for r_spec in spec["rates"]:
            rate, r_created = TaxRate.objects.get_or_create(
                tenant=tenant,
                scheme=scheme,
                tax_type=r_spec["tax_type"],
                defaults={
                    "rate": r_spec["rate"],
                    "label": r_spec["label"],
                    "is_active": True,
                },
            )
            if r_created:
                created_rates += 1
                print(f"      ✓ Taux ajouté : {rate.tax_type} = {rate.rate}%")
            else:
                existing_rates += 1

    print()
    print("=" * 60)
    print(f"Schémas : {created_schemes} créés, {existing_schemes} déjà présents")
    print(f"Taux    : {created_rates} créés, {existing_rates} déjà présents")
    print("=" * 60)


main()
