from django.contrib import admin
from .models import ExternalOrganization, STInvoice


@admin.register(ExternalOrganization)
class ExternalOrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "neq", "city", "province", "contact_name", "type_tags", "is_active")
    list_filter = ("is_active", "province", "tenant")
    search_fields = ("name", "neq", "contact_name")
    list_editable = ("is_active",)
    list_per_page = 25


@admin.register(STInvoice)
class STInvoiceAdmin(admin.ModelAdmin):
    list_display = ("invoice_number", "supplier", "project", "amount", "status", "invoice_date")
    list_filter = ("status", "tenant")
    search_fields = ("invoice_number", "supplier__name", "project__code")
    list_editable = ("status",)
    list_per_page = 25
