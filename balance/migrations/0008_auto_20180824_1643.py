# Generated by Django 2.0.5 on 2018-08-24 16:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('balance', '0007_auto_20180824_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individualbalance',
            name='updated',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='organizationbalance',
            name='updated',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
