# Generated by Django 2.0.5 on 2019-05-04 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('balance', '0014_auto_20190504_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individualbalance',
            name='payment_details',
            field=models.TextField(blank=True, null=True),
        ),
    ]
