from celery import task

from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.db.models import Sum

from .models import IndividualBalance


@task
def balance_added(user_id):
    """
    Task to send an e-mail notification when an order is successfully created
    """

    user = User.objects.get(id=user_id)
    total_balance = IndividualBalance.objects.filter(user=user).aggregate(Sum('balance'))
    total_balance = total_balance['balance__sum']
    total_additional = IndividualBalance.objects.filter(user=user).aggregate(Sum('additional'))
    total_additional = total_additional['additional__sum']
    subject = 'Transaction Report on ITEA'
    message = "Dear {0},\n\nYour  payment is successfully added to your account. Now your total monthly balance is {1} Tk. and total addtioanl balance is {2} Tk.".format(user.get_full_name(), total_balance, total_additional)
    
    mail_sent = send_mail(subject, message,
                          'shafikulislam.dorlove6@gmail.com',
                          [user.email])
    return mail_sent