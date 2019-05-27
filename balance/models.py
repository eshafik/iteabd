from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone


class IndividualBalance(models.Model):
    user = models.ForeignKey(User,
                             related_name='balances',
                             on_delete=models.CASCADE)
    balance = models.DecimalField(default=0, max_digits=12,
                                  decimal_places=4)
    additional = models.DecimalField(default=0, max_digits=12, 
                                  decimal_places=4)
    due_month = models.PositiveIntegerField(null=True, blank=True)
    payment_details = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return self.user.username



class OrganizationBalance(models.Model):
    invest_expense = models.DecimalField(null=True, blank=True,
                                  max_digits=12, decimal_places=4)
    invest_income = models.DecimalField(null=True, blank=True,
                                  max_digits=12, decimal_places=4)
    extra_expense = models.DecimalField(null=True, blank=True,
                                  max_digits=12, decimal_places=4)
    extra_income = models.DecimalField(null=True, blank=True,
                                  max_digits=12, decimal_places=4)
    investment_details = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated']
    
    def __str__(self):
        return self.updated


class InvestorBalance(models.Model):
    name = models.CharField(max_length=255)
    balance = models.DecimalField(null=True, blank=True,
                                  max_digits=12, decimal_places=4)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated']
    
    def __str__(self):
        return self.name
