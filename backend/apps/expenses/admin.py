from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import ExpenseApproval, ExpenseCategory, ExpenseLine, ExpenseReport


class ExpenseLineInline(admin.TabularInline):
    model = ExpenseLine
    extra = 0
    fields = ("expense_date", "amount", "description", "category", "is_refacturable", "tax_type")


@admin.register(ExpenseReport)
class ExpenseReportAdmin(SimpleHistoryAdmin):
    list_display = ("id", "employee", "total_amount", "status", "submitted_at", "tenant")
    list_filter = ("status", "tenant")
    search_fields = ("employee__username",)
    inlines = [ExpenseLineInline]
    list_per_page = 25


@admin.register(ExpenseLine)
class ExpenseLineAdmin(admin.ModelAdmin):
    list_display = ("report", "expense_date", "amount", "description", "category", "is_refacturable")
    list_filter = ("is_refacturable", "tax_type")


@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_refacturable_default", "requires_receipt", "gl_account", "tenant")
    list_filter = ("is_refacturable_default", "requires_receipt")
    list_editable = ("gl_account",)


@admin.register(ExpenseApproval)
class ExpenseApprovalAdmin(admin.ModelAdmin):
    list_display = ("report", "approved_by", "role_level", "status", "date")
    list_filter = ("status",)
