from django.contrib import admin

from .models import ExpenseApproval, ExpenseCategory, ExpenseLine, ExpenseReport

admin.site.register(ExpenseReport)
admin.site.register(ExpenseLine)
admin.site.register(ExpenseCategory)
admin.site.register(ExpenseApproval)
