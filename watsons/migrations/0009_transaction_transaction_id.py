# Generated by Django 2.0 on 2019-01-06 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watsons', '0008_transaction_transaction_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='transaction_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
