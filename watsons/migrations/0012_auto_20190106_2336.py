# Generated by Django 2.0 on 2019-01-06 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watsons', '0011_transaction_delta_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_total',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
