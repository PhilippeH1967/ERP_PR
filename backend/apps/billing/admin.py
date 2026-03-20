from django.contrib import admin
from .models import BillingDossier, ClientLabel, CreditNote, DunningAction, DunningLevel, Holdback, Invoice, InvoiceLine, InvoiceTemplate, Payment, PaymentAllocation, WriteOff


class InvoiceLineInline(admin.TabularInline):
    model = InvoiceLine
    extra = 0
    fields = ("deliverable_name", "line_type", "total_contract_amount", "invoiced_to_date", "amount_to_bill")


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("invoice_number", "project", "client", "total_amount", "status", "date_created")
    list_filter = ("status", "tenant")
    search_fields = ("invoice_number", "project__code", "client__name")
    list_editable = ("status",)
    inlines = [InvoiceLineInline]
    list_per_page = 25


@admin.register(InvoiceLine)
class InvoiceLineAdmin(admin.ModelAdmin):
    list_display = ("invoice", "deliverable_name", "line_type", "total_contract_amount", "amount_to_bill")


@admin.register(CreditNote)
class CreditNoteAdmin(admin.ModelAdmin):
    list_display = ("credit_note_number", "invoice", "amount", "reason", "status", "created_at")
    list_filter = ("status",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("invoice", "amount", "payment_date", "method", "reference")
    list_filter = ("method",)
    search_fields = ("reference", "invoice__invoice_number")


@admin.register(PaymentAllocation)
class PaymentAllocationAdmin(admin.ModelAdmin):
    list_display = ("payment", "invoice", "amount")


@admin.register(Holdback)
class HoldbackAdmin(admin.ModelAdmin):
    list_display = ("invoice", "percentage", "accumulated", "released", "remaining")


@admin.register(WriteOff)
class WriteOffAdmin(admin.ModelAdmin):
    list_display = ("invoice", "amount", "justification", "created_at")


@admin.register(InvoiceTemplate)
class InvoiceTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "is_active", "tenant")
    list_filter = ("is_active",)


@admin.register(ClientLabel)
class ClientLabelAdmin(admin.ModelAdmin):
    list_display = ("client", "project", "label_key", "label_value")


@admin.register(DunningLevel)
class DunningLevelAdmin(admin.ModelAdmin):
    list_display = ("level", "days_overdue", "tenant")
    list_editable = ("days_overdue",)


@admin.register(DunningAction)
class DunningActionAdmin(admin.ModelAdmin):
    list_display = ("invoice", "dunning_level", "sent_at")


@admin.register(BillingDossier)
class BillingDossierAdmin(admin.ModelAdmin):
    list_display = ("invoice", "generated_at")
