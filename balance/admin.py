from django.contrib import admin

from . models import IndividualBalance, OrganizationBalance


@admin.register(IndividualBalance)
class IndividualBalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'due_month', 'payment_details', 'updated')
    list_filter = ('user', 'balance', 'updated')
    search_fields = ('user', 'balance')
    date_hierarchy = 'updated'


@admin.register(OrganizationBalance)
class IndividualBalanceAdmin(admin.ModelAdmin):
    list_display = ('invest_expense', 'invest_income', 'extra_expense', 'extra_income', 'investment_details')

