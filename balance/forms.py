from django import forms
from django.contrib.auth.models import User

# from datetimepicker.widgets import DateTimePicker

from .models import IndividualBalance, OrganizationBalance


class IndividualBalanceForm(forms.Form):
    add_balance = forms.DecimalField(max_digits=12, decimal_places=4)
    additonal = forms.DecimalField(max_digits=12, decimal_places=4)
    due_month = forms.IntegerField()
    details = forms.CharField(widget=forms.Textarea)


class OrganizationBalanceForm(forms.Form):
    invest_expense = forms.DecimalField(max_digits=12, decimal_places=4)
    invest_income = forms.DecimalField(max_digits=12, decimal_places=4)
    extra_expense = forms.DecimalField(max_digits=12, decimal_places=4)
    extra_income = forms.DecimalField(max_digits=12, decimal_places=4)
    details = forms.CharField(widget=forms.Textarea)


class InvestorBalanceForm(forms.Form):
    name = forms.CharField(max_length=255)
    amount = forms.DecimalField(max_digits=12, decimal_places=4)


class DateForm(forms.Form):
    start = forms.DateField(label="From ", widget=forms.TextInput(attrs=
                                {
                                    'class': 'datepicker',
                                    'style': 'width:200px; height:30px;'
                                }))
                               
    end = forms.DateField(label="To ", widget=forms.TextInput(attrs=
                                {
                                    'class': 'datepicker',
                                    'style': 'width:200px; height:30px;'
                                }))
