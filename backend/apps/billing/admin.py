from django.contrib import admin

from .models import (
    BillingDossier,
    ClientLabel,
    CreditNote,
    DunningAction,
    DunningLevel,
    Holdback,
    Invoice,
    InvoiceLine,
    InvoiceTemplate,
    Payment,
    PaymentAllocation,
    WriteOff,
)

admin.site.register(Invoice)
admin.site.register(InvoiceLine)
admin.site.register(CreditNote)
admin.site.register(Payment)
admin.site.register(PaymentAllocation)
admin.site.register(Holdback)
admin.site.register(WriteOff)
admin.site.register(InvoiceTemplate)
admin.site.register(ClientLabel)
admin.site.register(DunningLevel)
admin.site.register(DunningAction)
admin.site.register(BillingDossier)
