"""Client serializers for REST API."""

from rest_framework import serializers

from apps.core.mixins import OptimisticLockMixin

from .models import Client, ClientAddress, Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            "id", "name", "role", "email", "phone",
            "language_preference", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


_ADDR_PARTICLES = {"d", "de", "du", "des", "l", "la", "le", "les", "the"}
_ADDR_ABBREV = {
    "avenue": "av", "ave": "av",
    "boulevard": "boul", "blvd": "boul", "bd": "boul",
    "chemin": "ch",
    "place": "pl",
    "route": "rte",
}


def _addr_key(value: str) -> str:
    """Clé de comparaison anti-doublon : minuscules, accents et ponctuation
    retirés (« d'Oxford » → « oxford »), particules françaises ignorées
    (d, de, du…), abréviations de voie normalisées (avenue → av…)."""
    import unicodedata

    text = unicodedata.normalize("NFKD", str(value or ""))
    text = "".join(c for c in text if not unicodedata.combining(c)).lower()
    text = "".join(c if c.isalnum() else " " for c in text)
    tokens = [_ADDR_ABBREV.get(t, t) for t in text.split() if t not in _ADDR_PARTICLES]
    return " ".join(tokens)


class ClientAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientAddress
        fields = [
            "id", "address_line_1", "address_line_2", "city",
            "province", "postal_code", "country", "is_billing", "is_primary",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, attrs):
        """Anti-doublon : refuse une adresse dont la **ligne 1 + ville**
        normalisées (accents, ponctuation, particules, abréviations de voie)
        existent déjà chez ce client. Le code postal ne « sauve » pas un
        doublon : une adresse civique n'a qu'un seul code postal — une
        différence de postal sur la même rue/ville est presque toujours une
        coquille. L'adresse en cours d'édition est exclue de la comparaison."""
        client_id = (
            self.instance.client_id
            if self.instance is not None
            else self.context.get("view").kwargs.get("client_pk")
            if self.context.get("view")
            else None
        )
        if client_id is None:
            return attrs

        def merged(field: str) -> str:
            if field in attrs:
                return attrs[field]
            return getattr(self.instance, field, "") if self.instance else ""

        key = (_addr_key(merged("address_line_1")), _addr_key(merged("city")))
        if not key[0]:
            return attrs
        qs = ClientAddress.objects.filter(client_id=client_id)
        if self.instance is not None:
            qs = qs.exclude(pk=self.instance.pk)
        for existing in qs:
            if key == (
                _addr_key(existing.address_line_1),
                _addr_key(existing.city),
            ):
                raise serializers.ValidationError(
                    "Cette adresse existe déjà pour ce client "
                    f"(« {existing.address_line_1}, {existing.city} ») — "
                    "même rue et même ville ; vérifiez le code postal."
                )
        return attrs


class ClientSerializer(OptimisticLockMixin, serializers.ModelSerializer):
    contacts = ContactSerializer(many=True, read_only=True)
    addresses = ClientAddressSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = [
            "id", "name", "legal_entity", "alias", "sector", "status",
            "payment_terms_days", "default_invoice_template",
            "associe_en_charge", "notes", "version",
            "contacts", "addresses",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class ClientListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views."""

    class Meta:
        model = Client
        fields = ["id", "name", "alias", "sector", "status", "created_at"]
