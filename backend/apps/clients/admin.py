from django.contrib import admin
from .models import Client, ClientAddress, Contact


class ContactInline(admin.TabularInline):
    model = Contact
    extra = 0


class AddressInline(admin.TabularInline):
    model = ClientAddress
    extra = 0


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "alias", "sector", "status", "tenant", "created_at")
    list_filter = ("status", "sector", "tenant")
    search_fields = ("name", "alias", "legal_entity")
    list_editable = ("status",)
    inlines = [ContactInline, AddressInline]
    list_per_page = 25


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "client", "role", "email", "phone")
    search_fields = ("name", "email", "client__name")


@admin.register(ClientAddress)
class ClientAddressAdmin(admin.ModelAdmin):
    list_display = ("client", "address_line_1", "city", "province", "is_primary", "is_billing")
    list_filter = ("is_primary", "is_billing", "province")
