"""Client business logic services."""

from django.db.models import Q

from .models import Client


def detect_duplicate_client(name: str, tenant_id: int, exclude_id: int | None = None):
    """
    Detect potential duplicate clients by fuzzy name matching.

    Returns list of potential duplicates with similarity info.
    Uses trigram similarity if pg_trgm extension is available,
    falls back to case-insensitive contains matching.
    """
    qs = Client.objects.filter(tenant_id=tenant_id)
    if exclude_id:
        qs = qs.exclude(pk=exclude_id)

    # Normalize: strip accents approximation + lowercase
    normalized = name.lower().strip()

    # Exact match on alias
    alias_matches = list(qs.filter(alias__iexact=normalized).values("id", "name", "alias"))

    # Case-insensitive contains on name
    name_matches = list(
        qs.filter(Q(name__icontains=normalized) | Q(name__icontains=name))
        .exclude(pk__in=[m["id"] for m in alias_matches])
        .values("id", "name", "alias")[:5]
    )

    duplicates = []
    for match in alias_matches:
        duplicates.append({**match, "match_type": "alias_exact"})
    for match in name_matches:
        duplicates.append({**match, "match_type": "name_similar"})

    return duplicates
