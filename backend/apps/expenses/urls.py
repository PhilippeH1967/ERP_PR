"""Expense URL configuration."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ExpenseCategoryViewSet, ExpenseLineViewSet, ExpenseReportViewSet

router = DefaultRouter()
router.register(r"expense_reports", ExpenseReportViewSet, basename="expense-report")
router.register(r"expense_categories", ExpenseCategoryViewSet, basename="expense-category")

line_router = DefaultRouter()
line_router.register(r"lines", ExpenseLineViewSet, basename="expense-line")

urlpatterns = [
    path("", include(router.urls)),
    path("expense_reports/<int:report_pk>/", include(line_router.urls)),
]
